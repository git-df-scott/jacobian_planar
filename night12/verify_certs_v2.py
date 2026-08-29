"""night12 v2 -- independent re-verification of every v2 certificate.

Trusts nothing in `V2_RECORDS/*.json` except the raw data: the stored `P`, the
stored construction parameters, the stored lambda vectors and the stored
carrier parameters.  Everything else is rebuilt here.  `exact.decide` and
`v2_families` are NOT called; the object-level certificates are re-derived
from the stored `P` alone (plus `n, a, c, h0, kappa`), so a recorded
certificate that does not actually hold is caught.

Object level, per P:

  U'  the factor `v` is RECOVERED from P by exact division,
      `v = (P_y - h0) / (2*g)` with `g = c*(x-a)^n`, and the division is
      required to be exact (nonzero remainder is a failure).  The Bezout pair
      is then rebuilt from the recovered `v`

          A = 4*g*(x-a)/(n*h0^2)
          B = ( h0 - (2*g/n)*(n*v + 2*(x-a)*v_x) ) / h0^2

      and `A*P_x + B*P_y - 1` is expanded coefficientwise over Q.

  R'  `P - kappa - v*(h0 + g*v)` is expanded coefficientwise over Q from the
      same recovered `v`, and both factors are required nonconstant.

  SY' `sy.certify` is re-run on the integerised P and compared with the
      recorded verdict.

  UT' (ARM B only) night14's Singular U-test is re-run in characteristic 0 on
      the same P, an instrument outside night12 entirely.

Stage level, per stage:

  E1' `lambda_exact` -- the carrier is rebuilt from the recorded
      (carrier, deg_Q_bound), the Keller row dictionary is rebuilt from
      scratch, the unknown count is required to match the record, and
      `lambda^T A = 0` is checked on EVERY column with `lambda^T e_00 = 1`,
      over Q.

  E2' `rank_full_column_exact` -- re-run at a DIFFERENT scheduling prime and a
      different compression seed than the run used, requiring
      `rank(A) = n` and `rank([A|e]) = n+1` again.  Both are lower bounds for
      the ranks over Q at any prime, so an independent prime reproducing them
      is an independent exact inconsistency certificate, not a repetition of
      the same computation.
"""

import collections
import json
import os
import sys
import time
from fractions import Fraction
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
N14 = os.path.join(os.path.dirname(HERE), "night14")

import matekit as M
import sy
import v2

RECHECK_PRIME = 1000003          # not the run's 999983
RECHECK_SEED = 20260901          # not the run's 20260831

# A rank recheck costs the same elimination the run itself paid, and on this
# host that is several minutes per wide stage.  Stages above this many unknowns
# are recorded as `skipped_cost` -- NOT as verified, and never as failed -- so
# the coverage of this pass is explicit rather than implied.  Set from the
# command line: `python3 verify_certs_v2.py <max_n>` (0 = no cap).
MAX_RANK_N = int(sys.argv[1]) if len(sys.argv) > 1 else 0

CACHE = os.path.join(HERE, "V2_VERIFY")


# ------------------------------------------------------------- unpack helpers

def unpack(d):
    return {tuple(int(t) for t in k.split(",")): Fraction(int(v[0]), int(v[1]))
            for k, v in d.items()}


def _scal(c, A):
    c = Fraction(c)
    return {k: c * v for k, v in A.items() if c * v != 0}


def _xma_pow(a, n):
    out = {(0, 0): Fraction(1)}
    base = {(1, 0): Fraction(1), (0, 0): Fraction(-a)}
    for _ in range(n):
        out = M.pmul(out, base)
    return out


def _udiv(num, den):
    """exact division of univariate dicts {i: coeff} in x; returns None if the
    remainder is nonzero."""
    num = {i: Fraction(c) for i, c in num.items() if c != 0}
    den = {i: Fraction(c) for i, c in den.items() if c != 0}
    if not den:
        return None
    dd = max(den)
    lc = den[dd]
    q = {}
    while num:
        nd = max(num)
        if nd < dd:
            return None
        f = num[nd] / lc
        q[nd - dd] = f
        for i, c in den.items():
            k = nd - dd + i
            num[k] = num.get(k, Fraction(0)) - f * c
            if num[k] == 0:
                del num[k]
    return q


def divide_by_x_poly(N, gx):
    """exact division of a bivariate dict by a polynomial in x only."""
    byy = collections.defaultdict(dict)
    for (i, j), c in N.items():
        byy[j][i] = c
    gu = {i: c for (i, jj), c in gx.items() if jj == 0}
    if len(gu) != len(gx):
        return None
    out = {}
    for j, u in byy.items():
        q = _udiv(u, gu)
        if q is None:
            return None
        for i, c in q.items():
            if c != 0:
                out[(i, j)] = c
    return out


# ------------------------------------------------------------- object checks

def recheck_object_A(rec):
    """re-derive U and R from the stored P alone plus (n, a, c, h0, kappa)."""
    P = unpack(rec["P"])
    pr = rec["certs"]["params"]
    n = int(pr["n"])
    a, c, h0 = Fraction(pr["a"]), Fraction(pr["c"]), Fraction(pr["h0"])
    kap = Fraction(int(rec["certs"]["R_kappa"][0]), int(rec["certs"]["R_kappa"][1]))
    g = _scal(c, _xma_pow(a, n))

    # recover v by exact division:  P_y - h0 = 2*g*v
    N = M.padd(M.dy(P), {(0, 0): -h0})
    v = divide_by_x_poly(N, _scal(2, g))
    if v is None:
        return {"U": False, "R": False, "why": "v not recoverable by exact division"}
    # v must be y + tau(x)
    shape_ok = (v.get((0, 1)) == 1
                and all(j == 0 for (i, j) in v if (i, j) != (0, 1)))

    xma = {(1, 0): Fraction(1), (0, 0): -a}
    vx = M.dx(v)
    A = _scal(Fraction(4) / (n * h0 * h0), M.pmul(g, xma))
    inner = M.padd(_scal(n, v), _scal(2, M.pmul(xma, vx)))
    B = _scal(Fraction(1) / (h0 * h0),
              M.padd({(0, 0): h0}, _scal(Fraction(-2) / n, M.pmul(g, inner))))
    RU = M.padd(M.padd(M.pmul(A, M.dx(P)), M.pmul(B, M.dy(P))),
                {(0, 0): Fraction(-1)})
    badU = sum(1 for x in RU.values() if x != 0)

    f1 = v
    f2 = M.padd({(0, 0): h0}, M.pmul(g, v))
    RR = M.padd(M.padd(P, {(0, 0): -kap}), _scal(-1, M.pmul(f1, f2)))
    badR = sum(1 for x in RR.values() if x != 0)
    return {"U": badU == 0, "R": badR == 0 and M.pdeg(f1) >= 1 and M.pdeg(f2) >= 1,
            "v_shape_ok": bool(shape_ok),
            "factor_degs": [M.pdeg(f1), M.pdeg(f2)],
            "badU": badU, "badR": badR}


def recheck_utest_B(P):
    """night14's Singular U-test, char 0, on the same P."""
    sys.path.insert(0, N14)
    try:
        import utest14
        r = utest14.utest(P, timeout=300)
    except Exception as e:                                # noqa: BLE001
        return {"u_q": "ERROR", "detail": str(e)[:120]}
    if isinstance(r, tuple):
        r = r[0] if isinstance(r[0], dict) else {"u_q": r[0]}
    return r if isinstance(r, dict) else {"u_q": str(r)}


# -------------------------------------------------------------- stage checks

def rebuild_carrier(P, st):
    D = int(st["deg_Q_bound"])
    if st["carrier"] == "np_similar":
        return v2.carrier_np(P, D)
    return v2.carrier_wide(P, D)


def check_lambda(P, st):
    S, info = rebuild_carrier(P, st)
    if not S:
        return False, "empty carrier"
    if len(S) != st["n_unknowns"]:
        return False, "carrier size %d != recorded %d" % (len(S), st["n_unknowns"])
    rows, _ = M.build_system(P, S)
    lam = {(int(k[0]), int(k[1])): Fraction(int(v[0]), int(v[1]))
           for k, v in st["lambda_vector"]}
    acc = {}
    for key, wt in lam.items():
        for j, val in rows.get(key, {}).items():
            acc[j] = acc.get(j, Fraction(0)) + wt * Fraction(val)
    nz = [j for j, x in acc.items() if x != 0]
    if nz:
        return False, "lambda^T A nonzero on %d of %d columns" % (len(nz), len(S))
    if lam.get((0, 0), Fraction(0)) != 1:
        return False, "lambda^T e_00 = %s" % lam.get((0, 0), 0)
    return True, "ok (%d columns)" % len(S)


def check_rank(P, st):
    if MAX_RANK_N and st.get("n_unknowns", 0) > MAX_RANK_N:
        return None, "skipped_cost (n = %d > cap %d)" % (st["n_unknowns"], MAX_RANK_N)
    S, info = rebuild_carrier(P, st)
    if not S:
        return False, "empty carrier"
    if len(S) != st["n_unknowns"]:
        return False, "carrier size %d != recorded %d" % (len(S), st["n_unknowns"])
    rows, _ = M.build_system(P, S)
    n = len(S)
    r = M.consistency_mod_p(rows, n, RECHECK_PRIME, seed=RECHECK_SEED)
    if r["consistent"]:
        return False, "consistent at the recheck prime"
    if r["rank_A"] == n and r["rank_Ae"] == n + 1:
        return True, "rank_A=%d=n, rank_Ae=%d at p=%d" % (n, r["rank_Ae"],
                                                          RECHECK_PRIME)
    return False, "rank_A=%d (n=%d), rank_Ae=%d at p=%d" % (
        r["rank_A"], n, r["rank_Ae"], RECHECK_PRIME)


# -------------------------------------------------------------------- driver

def one(fn):
    t0 = time.time()
    rec = json.load(open(fn))
    cpath = os.path.join(CACHE, os.path.basename(fn))
    if os.path.exists(cpath):
        return json.load(open(cpath))
    P = unpack(rec["P_integerised"])
    out = {"hash": rec["hash"], "arm": rec["arm"], "tag": rec["tag"],
           "deg_P": rec["deg_P"], "stages": [], "fails": []}

    v, _st = sy.certify(P)
    out["SY_recheck"] = v
    out["SY_recorded"] = rec["SY_verdict"]
    if v != rec["SY_verdict"]:
        out["fails"].append([rec["hash"], "SY", "%s != %s" % (v, rec["SY_verdict"])])

    if rec["arm"] == "A":
        o = recheck_object_A(rec)
        out["U_recheck"] = o["U"]
        out["R_recheck"] = o["R"]
        out["v_shape_ok"] = o.get("v_shape_ok")
        out["factor_degs"] = o.get("factor_degs")
        if not o["U"]:
            out["fails"].append([rec["hash"], "U", o.get("why", "bad %s" % o.get("badU"))])
        if not o["R"]:
            out["fails"].append([rec["hash"], "R", o.get("why", "bad %s" % o.get("badR"))])
    else:
        u = recheck_utest_B(P)
        out["UT_recheck"] = u.get("u_q", u.get("verdict", "?"))
        if out["UT_recheck"] != "PASS":
            out["fails"].append([rec["hash"], "UT", str(u)[:120]])

    for st in rec["stages"]:
        c = st.get("certificate")
        item = {"carrier": st.get("carrier"), "deg_Q_bound": st.get("deg_Q_bound"),
                "n_unknowns": st.get("n_unknowns"), "certificate": c}
        if c == "lambda_exact":
            if not st.get("lambda_vector"):
                item["ok"], item["why"] = None, "lambda not recorded"
            else:
                item["ok"], item["why"] = check_lambda(P, st)
        elif c == "rank_full_column_exact":
            item["ok"], item["why"] = check_rank(P, st)
        else:
            item["ok"], item["why"] = None, "no certificate to recheck"
        if item["ok"] is False:
            out["fails"].append([rec["hash"], "%s@%s" % (c, st.get("deg_Q_bound")),
                                 item["why"]])
        out["stages"].append(item)

    out["secs"] = round(time.time() - t0, 1)
    os.makedirs(CACHE, exist_ok=True)
    json.dump(out, open(cpath, "w"), indent=1)
    return out


def main():
    fns = sorted(os.path.join(v2.RECDIR, f) for f in os.listdir(v2.RECDIR)
                 if f.endswith(".json"))
    print("re-verifying %d v2 records (recheck prime %d, seed %d, rank cap %s)"
          % (len(fns), RECHECK_PRIME, RECHECK_SEED, MAX_RANK_N or "none"),
          flush=True)
    with Pool(4) as p:
        res = p.map(one, fns, chunksize=1)

    tally = collections.Counter()
    fails = []
    for r in res:
        tally[(r["arm"], "SY", r["SY_recheck"] == r["SY_recorded"])] += 1
        if r["arm"] == "A":
            tally[("A", "U_bezout", bool(r["U_recheck"]))] += 1
            tally[("A", "R_factorisation", bool(r["R_recheck"]))] += 1
        else:
            tally[("B", "night14_U_test_char0", r.get("UT_recheck"))] += 1
        for s in r["stages"]:
            tally[(r["arm"], s["certificate"], s["ok"])] += 1
        fails += r["fails"]

    print("\nindependent re-verification of v2 certificates")
    print("(carriers, Keller systems and Bezout pairs rebuilt from scratch;")
    print(" exact.decide and v2_families not used)\n")
    for k in sorted(tally, key=str):
        print("  %-4s %-28s %-12s %d" % (k[0], k[1], str(k[2]), tally[k]))
    print("\nFAILURES: %d" % len(fails))
    for f in fails:
        print("  ", f)
    json.dump({"recheck_prime": RECHECK_PRIME, "recheck_seed": RECHECK_SEED,
               "tally": {" | ".join(str(x) for x in k): v for k, v in tally.items()},
               "per_object": res, "failures": fails},
              open(os.path.join(HERE, "verify_certs_v2.json"), "w"), indent=1)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
