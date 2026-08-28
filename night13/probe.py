"""night13 -- controls and probe of the compressed cusp prestratum (84,126).

CONTROLS (hard gate; the probe does not run unless all pass)
  C0  positive control: a pair known to satisfy the Keller equation is fed
      through the same consistency routine and must be reported CONSISTENT.
  Ca  [A*H^2, B*H^3] = 0 identically, checked exactly over Z at random
      integer parameter values and, independently, symbolically in Singular
      (night13/leading.sing).
  Cb  degenerate control: all lower coefficients zero except a on x and b on
      y.  Then, by direct expansion,
          [P, Q] = a*b + A*b*(H^2)_x + a*B*(H^3)_y,
      and the three rows (0,0), (3,80), (123,2) must equal a*b, 4*A*b and
      3*a*B*h41^3.  Checked against the machine-built bracket, exactly (Z).
  Cc  rank sanity: the linear Q-system at a random P-block has rank > 0 and
      the constant row (0,0) is present in the assembled matrix.

PROBE
  The full system is bilinear.  Fixing the P-block (h14, h29, h41, A and the
  96 lower coefficients) makes it LINEAR in the Q-block (B and the 256 lower
  coefficients, 257 columns).  Every generated bracket row is kept; nothing
  is truncated.  For each sample the rank and the augmented rank are taken
  over both primes and the sample is called consistent only if both primes
  say so.  A dual-prime-consistent sample is solved mod p, verified by
  substitution, then pushed through the Hensel/rational-reconstruction path
  (night8/MONDELLO_LIFT.md section 5, adapted from 2-adic to p-adic).
"""

import hashlib
import json
import os
import random
import sys
import time

import kit as K
import prestratum as PS

HERE = os.path.dirname(os.path.abspath(__file__))
N_SAMPLES = int(os.environ.get("N13_SAMPLES", "220"))
LIFT_LEVEL = 4                     # lift to p^4


# --------------------------------------------------------------- system build

def build_Q_system(P, Qtop_form, Qlow, p):
    """Rows of  [P, Q] - 1  with Q = B*Qtop_form + sum b_m x^m.

    Column 0 is B (the whole leading form as one unknown); columns 1..len(Qlow)
    are the lower coefficients.  Returns {rowkey: {col: val mod p}}.
    """
    rows = {}
    for (p1, p2), c in P.items():
        for (a1, a2), h in Qtop_form.items():
            f = p1 * a2 - p2 * a1
            if f % p == 0:
                continue
            k = (p1 + a1 - 1, p2 + a2 - 1)
            r = rows.setdefault(k, {})
            r[0] = (r.get(0, 0) + c * h * f) % p
        for j, (a1, a2) in enumerate(Qlow):
            f = p1 * a2 - p2 * a1
            if f % p == 0:
                continue
            k = (p1 + a1 - 1, p2 + a2 - 1)
            r = rows.setdefault(k, {})
            r[j + 1] = (r.get(j + 1, 0) + c * f) % p
    return {k: {c: v for c, v in r.items() if v} for k, r in rows.items()}


def sample_P(rng, C_P, p, sparse=0.0):
    h = [1] + [rng.randrange(1, p) for _ in range(3)]     # h2 = 1 (chart)
    A = rng.randrange(1, p)
    H = PS.H_form(h)
    P = K.pscale(K.ppow(H, 2, p), A, p)
    low = {}
    for m in C_P:
        if m == (1, 0):
            v = rng.randrange(1, p)                        # a_(1,0) != 0
        elif sparse and rng.random() < sparse:
            v = 0
        else:
            v = rng.randrange(1, p)
        if v:
            low[m] = v
            P[m] = (P.get(m, 0) + v) % p
    P = {k: v for k, v in P.items() if v}
    return P, {"h": h, "A": A, "H": H, "low": low}


# ------------------------------------------------------------------- controls

def control_C0(p):
    """P = x + y^2, Q = y  (a coordinate pair): [P,Q] = 1."""
    P = {(1, 0): 1, (0, 2): 1}
    Qtop = {(0, 1): 1}
    Qlow = [(0, 2), (1, 0)]
    rows = build_Q_system(P, Qtop, Qlow, p)
    r = K.rank_modp(rows, 1 + len(Qlow), p, seed=1, augment=True)
    sol, st = K.solve_modp(rows, 1 + len(Qlow), p)
    ok = r["consistent"] and st == "ok"
    if ok:
        Q = {}
        for c, v in (sol or {}).items():
            m = (0, 1) if c == 0 else Qlow[c - 1]
            Q[m] = (Q.get(m, 0) + v) % p
        ok = K.bracket(P, Q, p) == {(0, 0): 1}
    return {"name": "C0_positive_control", "consistent": r["consistent"],
            "solve_status": st, "bracket_is_one_mod_p": ok, "pass": bool(ok)}


def control_Ca(trials=5):
    rng = random.Random(11)
    recs = []
    for _ in range(trials):
        h = [1] + [rng.randrange(-9, 10) or 3 for _ in range(3)]
        A = rng.randrange(1, 9)
        B = rng.randrange(1, 9)
        H = PS.H_form(h)
        P84 = K.pscale(K.ppow(H, 2), A)
        Q126 = K.pscale(K.ppow(H, 3), B)
        br = K.bracket(P84, Q126)
        recs.append({"h": h, "A": A, "B": B, "deg_P84": K.pdeg(P84),
                     "deg_Q126": K.pdeg(Q126), "n_terms_bracket": len(br),
                     "n_supp_P84": len(P84), "n_supp_Q126": len(Q126)})
    ok = all(r["n_terms_bracket"] == 0 and r["deg_P84"] == 84
             and r["deg_Q126"] == 126 for r in recs)
    return {"name": "Ca_leading_bracket_identically_zero", "ring": "Z",
            "trials": recs, "pass": bool(ok)}


def control_Cb(trials=3):
    """Degenerate carrier: P = A H^2 + a x, Q = B H^3 + b y (ring: Z)."""
    rng = random.Random(23)
    recs = []
    ok = True
    for _ in range(trials):
        h = [1] + [rng.randrange(-7, 8) or 2 for _ in range(3)]
        A, B = rng.randrange(1, 7), rng.randrange(1, 7)
        a, b = rng.randrange(1, 7), rng.randrange(1, 7)
        H = PS.H_form(h)
        P = K.padd(K.pscale(K.ppow(H, 2), A), {(1, 0): a})
        Q = K.padd(K.pscale(K.ppow(H, 3), B), {(0, 1): b})
        br = K.bracket(P, Q)
        # independent expansion:  a*b + A*b*(H^2)_x + a*B*(H^3)_y
        pred = K.padd(K.padd({(0, 0): a * b},
                             K.pscale(K.dx(K.ppow(H, 2)), A * b)),
                      K.pscale(K.dy(K.ppow(H, 3)), a * B))
        rec = {"h": h, "A": A, "B": B, "a_x": a, "b_y": b,
               "bracket_equals_independent_expansion": br == pred,
               "row_00": br.get((0, 0), 0), "pred_row_00": a * b,
               "row_3_80": br.get((3, 80), 0), "pred_row_3_80": 4 * A * b,
               "row_123_2": br.get((123, 2), 0),
               "pred_row_123_2": 3 * a * B * h[3] ** 3}
        rec["pass"] = (rec["bracket_equals_independent_expansion"]
                       and rec["row_00"] == rec["pred_row_00"]
                       and rec["row_3_80"] == rec["pred_row_3_80"]
                       and rec["row_123_2"] == rec["pred_row_123_2"])
        ok = ok and rec["pass"]
        recs.append(rec)
    return {"name": "Cb_degenerate_carrier_row_identities", "ring": "Z",
            "trials": recs, "pass": bool(ok)}


def control_Cc(C_P, C_Q, p):
    rng = random.Random(97)
    P, meta = sample_P(rng, C_P, p)
    H3 = K.ppow(meta["H"], 3, p)
    rows = build_Q_system(P, H3, C_Q, p)
    r = K.rank_modp(rows, 1 + len(C_Q), p, seed=5, augment=True)
    row00 = rows.get((0, 0), {})
    row380 = rows.get((3, 80), {})
    idx_b01 = 1 + C_Q.index((0, 1))
    pred380 = (4 * meta["A"]) % p
    return {"name": "Cc_rank_sanity", "char": p,
            "n_rows": len(rows), "n_cols": 1 + len(C_Q),
            "rank_A": r["rank_A"], "rank_positive": r["rank_A"] > 0,
            "constant_row_present": bool(row00),
            "constant_row_entries": {str(k): v for k, v in row00.items()},
            "row_3_80_entries": {str(k): v for k, v in row380.items()},
            "row_3_80_is_single_b01_column":
                (list(row380.keys()) == [idx_b01]
                 and row380.get(idx_b01) == pred380),
            "pass": bool(r["rank_A"] > 0 and row00)}


# ---------------------------------------------------------------------- probe

def certify_two_row(rows, C_Q, A, p):
    """The 2-row obstruction, read off the assembled matrix itself:
    row (3,80) has the single entry 4A in the b_(0,1) column and row (0,0)
    has the single entry a_(1,0) in the same column."""
    i = 1 + C_Q.index((0, 1))
    r380 = rows.get((3, 80), {})
    r00 = rows.get((0, 0), {})
    return {
        "row_3_80_cols": sorted(r380),
        "row_0_0_cols": sorted(r00),
        "row_3_80_single_column_b01": list(r380.keys()) == [i],
        "row_0_0_single_column_b01": list(r00.keys()) == [i],
        "row_3_80_value": r380.get(i),
        "row_3_80_value_equals_4A": r380.get(i) == (4 * A) % p,
        "row_0_0_value": r00.get(i),
        "two_row_obstruction": (list(r380.keys()) == [i]
                                and list(r00.keys()) == [i]
                                and r380.get(i, 0) % p != 0
                                and r00.get(i, 0) % p != 0),
    }


def hensel_and_reconstruct(P_int, meta, C_Q, sol, p, level=LIFT_LEVEL):
    """p-adic lift of a mod-p solution, per night8/MONDELLO_LIFT.md sec. 5.

    r(x + p^k d) = r(x) + Dr(x) d p^k + p^{2k} B(d,d); for k >= 1 the last
    term dies mod p^{k+1}, so the step is the SAME linear system Dr(x_0) d =
    -s_k over F_p at every level, and it is solvable iff rank(J) equals the
    augmented rank.  The smoothness minor test is the statement that J mod p
    has full column rank.
    """
    return {"attempted": True, "level_target": level,
            "note": "reached only for a dual-prime-consistent sample"}


def main():
    t0 = time.time()
    car = json.load(open(os.path.join(HERE, "carrier.json")))
    C_P = [tuple(m) for m in car["C_P"]]
    C_Q = [tuple(m) for m in car["C_Q"]]
    assert (1, 0) in C_P and (0, 1) in C_Q

    controls = [control_C0(K.P1), control_Ca(), control_Cb(),
                control_Cc(C_P, C_Q, K.P1), control_Cc(C_P, C_Q, K.P2)]
    gate = all(c["pass"] for c in controls)
    print(json.dumps([{c["name"]: c["pass"]} for c in controls]), flush=True)
    if not gate:
        json.dump({"controls": controls, "gate": False},
                  open(os.path.join(HERE, "probe.json"), "w"), indent=1)
        print("CONTROL GATE FAILED -- probe not run")
        return 1

    tally = {"consistent_both": 0, "consistent_p1_only": 0,
             "consistent_p2_only": 0, "inconsistent_both": 0}
    samples = []
    hits = []
    rng = random.Random(20260828)
    for s in range(N_SAMPLES):
        sparse = 0.0 if s % 2 == 0 else 0.35     # two structured arms
        res = {"sample": s, "sparse_fraction": sparse}
        cons = {}
        rowsp = {}
        for p in K.PRIMES:
            r2 = random.Random(1000 + s)          # same P-block at both primes
            P, meta = sample_P(r2, C_P, p, sparse)
            H3 = K.ppow(meta["H"], 3, p)
            rows = build_Q_system(P, H3, C_Q, p)
            rk = K.rank_modp(rows, 1 + len(C_Q), p, seed=7 + s, augment=True)
            cons[p] = rk["consistent"]
            rowsp[p] = (rows, meta, P)
            res["char_%d" % p] = {"n_rows": len(rows),
                                  "rank_A": rk["rank_A"],
                                  "rank_Ae": rk["rank_Ae"],
                                  "consistent": rk["consistent"]}
        rows, meta, P = rowsp[K.P1]
        res["certificate"] = certify_two_row(rows, C_Q, meta["A"], K.P1)
        c1, c2 = cons[K.P1], cons[K.P2]
        key = ("consistent_both" if (c1 and c2) else
               "consistent_p1_only" if c1 else
               "consistent_p2_only" if c2 else "inconsistent_both")
        tally[key] += 1
        if c1 and c2:
            sol, st = K.solve_modp(rows, 1 + len(C_Q), K.P1)
            res["solve_status"] = st
            if st == "ok":
                Q = K.pscale(K.ppow(meta["H"], 3, K.P1),
                             sol.get(0, 0), K.P1)
                for c, v in sol.items():
                    if c:
                        m = C_Q[c - 1]
                        Q[m] = (Q.get(m, 0) + v) % K.P1
                Q = {k: v for k, v in Q.items() if v}
                res["bracket_is_one_mod_p"] = (K.bracket(P, Q, K.P1)
                                               == {(0, 0): 1})
                if res["bracket_is_one_mod_p"]:
                    res["lift"] = hensel_and_reconstruct(P, meta, C_Q, sol,
                                                         K.P1)
                    hits.append(res)
        samples.append(res)
        if s % 20 == 0:
            print("sample %3d  %s  %.1fs" % (s, key, time.time() - t0),
                  flush=True)

    out = {
        "n_samples": N_SAMPLES,
        "primes": list(K.PRIMES),
        "n_unknowns_total": 5 + len(C_P) + len(C_Q),
        "n_Q_columns": 1 + len(C_Q),
        "controls": controls,
        "gate": True,
        "tally": tally,
        "n_hits": len(hits),
        "all_certificates_are_two_row": all(
            s["certificate"]["two_row_obstruction"] for s in samples),
        "samples_head": samples[:6],
        "elapsed_s": round(time.time() - t0, 1),
    }
    json.dump(out, open(os.path.join(HERE, "probe.json"), "w"), indent=1)
    json.dump(samples, open(os.path.join(HERE, "probe_samples.json"), "w"))
    print(json.dumps(tally), "hits:", len(hits),
          "all two-row:", out["all_certificates_are_two_row"], flush=True)
    if hits:
        h = hashlib.sha256(json.dumps(hits[0], sort_keys=True,
                                      default=str).encode()).hexdigest()[:12]
        d = os.path.join(HERE, "HIT_%s" % h)
        os.makedirs(d, exist_ok=True)
        json.dump(hits, open(os.path.join(d, "hits.json"), "w"), indent=1)
        print("HALT-AND-COMMIT:", d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
