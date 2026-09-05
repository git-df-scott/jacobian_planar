"""night12 v2 -- mate search against certified non-coordinate targets.

ARM A  high-degree, bound-respecting.  F2/F2b objects at deg P in [124,132]
       built by `v2_families.py`, each carrying, before any mate system is
       built, three exact certificates checked coefficientwise over Q:
         U   the Bezout identity A*P_x + B*P_y = 1  (gradient unimodular)
         R   the factorisation P - kappa = v*(h0 + g*v)  (reducible fibre;
             with U this makes the fibre disconnected, so P is not a
             coordinate)
         SY  the Shpilrain-Yu reduction, run independently
       Mate systems at deg Q <= deg P - 1, deg P + 31, deg P + 63, on the
       Newton-polygon-similar carrier, plus a fourth WIDE stage at
       deg Q <= deg P + 63 on the full degree triangle thinned to the cap.

ARM B  low-degree, escalating.  Five structurally diverse objects from
       night14's 79 certified U-PASS + SY-NON_COORDINATE records, with
       deg Q escalating 10, 30, 60, 100, 126.

HONESTY OF THE EMPTY VERDICTS.  Every EMPTY here is relative to the support
actually used, and is recorded with that support's parameters (`deg_Q_bound`,
`n_raw`, `thin_t`, `n_used`, `deflated_kernel_dim`, `carrier`).  For ARM B the
published degree bound means a mate would need deg Q >= 125, so only the
deg Q <= 126 stage is capable of deciding anything; the earlier stages are
recorded as calibration and are labelled `support_relative`.

Kernel deflation.  The trivial directions Q -> Q + h(P) are quotiented by
deleting the column at lead(P)^k for exactly those k whose whole support fits
the carrier -- a P^k that does not fit contributes no kernel and is not
deflated, since deleting its column would shrink the search space rather than
quotient it.

The hit gate is v1's, unchanged: a mate certified over Q by E3 on a P that is
certified NON_COORDINATE halts the run and is written to night12/HIT_<hash>/.
"""

import hashlib
import json
import os
import sys
import time
from fractions import Fraction
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matekit as M
import exact
import sy
import screens
import v2_families as VF

CAP_NP = 5000          # Newton-polygon-similar carriers (never reached in ARM A)
CAP_WIDE = 2500        # the wide stage's thinning cap
RECDIR = os.path.join(HERE, "V2_RECORDS")


def phash(P):
    s = json.dumps(sorted((list(k), str(Fraction(v))) for k, v in P.items()))
    return hashlib.sha256(s.encode()).hexdigest()[:12]


def integerise(P):
    """scale P by the lcm of its coefficient denominators.

    Exact and harmless to the search: constants bracket to zero, so
    [P + kappa, Q] = [P, Q]; and for a nonzero rational lam,
    [lam*P, Q] = lam*[P, Q], so Q is a mate of P exactly when Q/lam is a mate
    of lam*P.  Coordinate-ness is likewise invariant under scaling by a nonzero
    constant.  The scale factor is recorded so the correspondence is explicit,
    and it is needed because the scheduling prime's reduction is only defined
    on integers.
    """
    from math import gcd
    den = 1
    for v in P.values():
        f = Fraction(v)
        den = den * f.denominator // gcd(den, f.denominator)
    Q = {k: int(Fraction(v) * den) for k, v in P.items()}
    Q = {k: v for k, v in Q.items() if v != 0}
    return Q, den


def pstr(P):
    return {("%d,%d" % k): [int(Fraction(v).numerator), int(Fraction(v).denominator)]
            for k, v in sorted(P.items())}


# ------------------------------------------------------------------ carriers

def _deflate(S, P, D):
    """delete the column at lead(P)^k for every power that fits the carrier."""
    Sset = set(S)
    lead = max(P, key=lambda m: (m[0] + m[1], m[0]))
    d = M.pdeg(P)
    drop = set()
    Pk = {(0, 0): Fraction(1)}
    k = 0
    while k * d <= D:
        if not set(Pk).issubset(Sset):
            break
        drop.add((lead[0] * k, lead[1] * k))
        Pk = M.pmul(Pk, P)
        k += 1
    return sorted(Sset - drop), len(drop)


def _thin(S, cap, keep, tmax):
    """thin S to at most `cap` points on the sublattice of stride t.

    The thinning is recomputed from the ORIGINAL point set at each candidate
    stride, not applied cumulatively on top of the previous stride.  The
    cumulative form (which v1 uses) compounds the strides -- t = 2 then t = 3
    leaves only the points divisible by 6, about 1/36 of the set, while
    recording `thin_t = 3` -- so it overshoots the cap by a wide margin and the
    recorded index understates how much was removed.  Recomputing from the
    base keeps the used support as close to the cap as the lattice allows and
    makes `thin_t` mean what it says.  `n_used` was accurate either way; this
    changes how much support the stage actually gets.
    """
    base = sorted(set(S))
    if len(base) <= cap:
        return base, 1
    kept = keep & set(base)
    for t in range(2, tmax + 1):
        T = sorted(set(p for p in base if p[0] % t == 0 and p[1] % t == 0) | kept)
        if len(T) <= cap:
            return T, t
    return sorted(kept), tmax


def carrier_np(P, D, cap=CAP_NP):
    """Newton-polygon-similar carrier: NP(P) scaled to the stage bound, with
    the anchors adjoined both scaled and unscaled (see v1.general_carrier)."""
    d = M.pdeg(P)
    if D < 1:
        return [], {"carrier": "np_similar", "deg_Q_bound": D, "n_raw": 0,
                    "thin_t": 1, "n_used": 0, "deflated_kernel_dim": 0}
    verts = M._hull(sorted(set([(p[0] * D, p[1] * D) for p in P]
                               + [(p[0] * D, p[1] * D) for p in M.BASE]
                               + [(p[0] * d, p[1] * d) for p in M.BASE])))
    S = [(a, b) for a in range(D + 1) for b in range(D + 1 - a)
         if M._inside(verts, (a * d, b * d))]
    info = {"carrier": "np_similar", "deg_Q_bound": D, "n_raw": len(S), "thin_t": 1}
    S, info["thin_t"] = _thin(S, cap, set(M.BASE), 40)
    S, nd = _deflate(S, P, D)
    info["n_used"] = len(S)
    info["deflated_kernel_dim"] = nd
    return S, info


def carrier_wide(P, D, cap=CAP_WIDE):
    """the full degree-D triangle, thinned on both exponents to the cap.

    Before thinning this strictly contains the Newton-polygon-similar carrier.
    AFTER thinning it does not: at stride t it keeps only the points with both
    exponents divisible by t, so it is a coarse sample spread over the WHOLE
    degree-D triangle, whereas the similar carrier is a dense sample of one
    sub-polygon.  The two are therefore complementary supports, not nested
    ones, and an EMPTY on each is a separate statement.  Neither is a claim
    about all Q of degree <= D.
    """
    S = [(a, b) for a in range(D + 1) for b in range(D + 1 - a)]
    info = {"carrier": "wide_triangle", "deg_Q_bound": D, "n_raw": len(S),
            "thin_t": 1}
    S, info["thin_t"] = _thin(S, cap, set(M.BASE) | set(P), 60)
    S, nd = _deflate(S, P, D)
    info["n_used"] = len(S)
    info["deflated_kernel_dim"] = nd
    return S, info


# ---------------------------------------------------------------- one object

def run_one(job):
    P_raw = job["P"]
    P, scale = integerise(P_raw)
    h = phash(P_raw)
    rec = {"hash": h, "arm": job["arm"], "family": job["family"],
           "tag": job["tag"], "deg_P": M.pdeg(P), "n_supp_P": len(P),
           "P": pstr(P_raw), "P_integerised": pstr(P),
           "integerising_scale": scale,
           "certs": dict(job.get("certs", {})),
           "stages": []}
    t0 = time.time()

    v, st = sy.certify(P)
    rec["SY_verdict"] = v
    rec["SY_nodes"] = st["nodes"]
    rec["SY_leaves"] = st["leaves"]
    d3 = screens.S3_diagnostics(P)
    rec.update(d3)

    rec["outcome"] = "EMPTY_all_stages_tried"
    for (D, kind, decisive) in job["stages"]:
        S, info = (carrier_np(P, D) if kind == "np" else carrier_wide(P, D))
        info["decisive_for_published_bound"] = decisive
        if not S:
            rec["stages"].append({**info, "verdict": "EMPTY_trivial_carrier"})
            continue
        ts = time.time()
        out, rows, Qd = exact.decide(P, S, want_lambda=True)
        out.update(info)
        out["secs"] = round(time.time() - ts, 1)
        out["support_relative"] = True
        rec["stages"].append(out)
        if out["verdict"] == "MATE_over_Q":
            rec["outcome"] = "MATE"
            rec["deg_Q"] = M.pdeg(Qd)
            rec["div_ordered"] = str(M.divisibility_ordered(M.pdeg(P), M.pdeg(Qd)))
            rec["Q"] = {("%d,%d" % k): [int(x.numerator), int(x.denominator)]
                        for k, x in sorted(Qd.items())}
            rec["bracket_is_one"] = bool(M.is_one(M.bracket(P, Qd)))
            # translate back to a mate of the ORIGINAL (unscaled) P
            Qorig = {k: x * scale for k, x in Qd.items()}
            rec["Q_for_original_P"] = {
                ("%d,%d" % k): [int(x.numerator), int(x.denominator)]
                for k, x in sorted(Qorig.items())}
            rec["bracket_is_one_original"] = bool(
                M.is_one(M.bracket(P_raw, Qorig)))
            break
        if out["verdict"] == "NOT_CERTIFIED":
            rec["outcome"] = "NOT_CERTIFIED_at_degQ_%d" % D

    rec["hit"] = bool(rec["outcome"] == "MATE"
                      and rec["SY_verdict"] == "NON_COORDINATE")
    rec["secs"] = round(time.time() - t0, 1)
    return rec


# --------------------------------------------------------------------- pools

def jobs_A():
    out = []
    for ob in VF.pool_A():
        okb, nb = VF.verify_bezout(ob)
        okf, nf, d1, d2 = VF.verify_factorisation(ob)
        dP = ob["deg_P"]
        out.append({
            "arm": "A", "P": ob["P"], "family": ob["family"], "tag": ob["tag"],
            "certs": {
                "U_bezout_A_Px_plus_B_Py_eq_1": okb,
                "U_bezout_residual_terms": nb,
                "R_factorisation_P_minus_kappa_eq_v_times_h0_plus_gv": okf,
                "R_factor_degrees": [d1, d2],
                "R_kappa": [int(ob["kappa"].numerator), int(ob["kappa"].denominator)],
                "params": {"n": ob["n"], "T": ob["T"],
                           "a": str(ob["a"]), "c": str(ob["c"]),
                           "h0": str(ob["h0"])},
            },
            "stages": [(dP - 1, "np", False), (dP + 31, "np", False),
                       (dP + 63, "np", True), (dP + 63, "wide", True)],
        })
    return out


def jobs_B():
    """five structurally diverse night14 crux objects + x + x^2*y."""
    n14 = os.path.join(os.path.dirname(HERE), "night14")
    recs = json.load(open(os.path.join(n14, "records.json")))
    crux = [r for r in recs
            if r["u_q"] == "PASS" and r["sy"] == "NON_COORDINATE"]

    def genus(r):
        g = [f[2] for f in r["fib_detail"] if isinstance(f, list) and f[2]]
        return max(g) if g else 0

    picked = []
    # at least two positive-genus F2b
    f2b_pg = sorted([r for r in crux if r["family"] == "F2b" and genus(r) > 0],
                    key=lambda r: (-genus(r), -r["tdeg"]))
    picked += f2b_pg[:2]
    # the most structurally distinct of the remaining families
    for fam in ("F1b", "F3", "F4", "F2"):
        cand = [r for r in crux if r["family"] == fam
                and r["hash"] not in {p["hash"] for p in picked}]
        if cand:
            picked.append(sorted(cand, key=lambda r: -r["tdeg"])[0])
        if len(picked) >= 5:
            break

    out = []
    for r in picked[:5]:
        P = {tuple(m[0]): Fraction(m[1]) for m in r["monomials"]} \
            if isinstance(r["monomials"][0][0], (list, tuple)) else None
        if P is None:
            continue
        out.append({"arm": "B", "P": P, "family": r["family"],
                    "tag": "night14 %s %s" % (r["family"], r["hash"]),
                    "certs": {"night14_hash": r["hash"],
                              "night14_U": r["u_q"], "night14_SY": r["sy"],
                              "night14_FIB": r["fib"],
                              "night14_fib_detail": r["fib_detail"],
                              "night14_label": r["label"]},
                    "stages": [(10, "np", False), (30, "np", False),
                               (60, "np", False), (100, "np", False),
                               (126, "np", True)]})
    # the brief names this one explicitly
    out.append({"arm": "B", "P": {(1, 0): Fraction(1), (2, 1): Fraction(1)},
                "family": "brief", "tag": "x + x^2*y",
                "certs": {"note": "named in the V2 brief; "
                                  "x + x^2*y = x*(1 + x*y), reducible fibre"},
                "stages": [(10, "np", False), (30, "np", False),
                           (60, "np", False), (100, "np", False),
                           (126, "np", True)]})
    return out


# ---------------------------------------------------------------------- main

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = []
    if which in ("all", "A"):
        jobs += jobs_A()
    if which in ("all", "B"):
        jobs += jobs_B()
    print("v2: %d objects (%s)"
          % (len(jobs), {a: sum(1 for j in jobs if j["arm"] == a)
                         for a in ("A", "B")}), flush=True)

    with Pool(4) as p:
        res = p.map(run_one, jobs, chunksize=1)

    os.makedirs(RECDIR, exist_ok=True)
    for r in res:
        json.dump(r, open(os.path.join(RECDIR, r["hash"] + ".json"), "w"), indent=1)
    out = os.path.join(HERE, "v2_records_%s.json" % which)
    json.dump(res, open(out, "w"), indent=1)

    nhit = 0
    for r in res:
        if r["hit"]:
            d = os.path.join(HERE, "HIT_" + r["hash"])
            os.makedirs(d, exist_ok=True)
            json.dump(r, open(os.path.join(d, "record.json"), "w"), indent=1)
            nhit += 1
    print("v2 done. objects: %d ; mates: %d ; HITs: %d"
          % (len(res), sum(1 for r in res if r["outcome"] == "MATE"), nhit),
          flush=True)


if __name__ == "__main__":
    main()
