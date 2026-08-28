"""night9 — LAST-TERM KILL.

Measurements only.  Every result is labelled with its characteristic or with
the ring it was computed in.  No assessment of what any of these numbers mean
is offered.

INPUT.  Every matched lift recorded in night9/altitude/ whose exact integer
residual

    R(x,y) = P_x Q_y - P_y Q_x - 1     (computed over Z)

consists of a SINGLE monomial c * x^A * y^B.  (88 such lifts exist across the
60 altitude supports, so the fallback to two-term residuals is not taken.)

FOR EACH CASE.
  * The bracket coefficient of x^A y^B is written symbolically in the pair's
    coefficients:  R_[A,B] = sum over pairs (m,n) with
    (m0+n0-1, m1+n1-1) = (A,B) of (m0 n1 - m1 n0) a_m b_n, minus 1 when
    (A,B) = (0,0).  The FREE SET is the set of coefficient names occurring in
    that formula.
  * EXACT INTEGER LOCAL SEARCH.  Every coefficient in the free set ranges
    independently over [-4 .. 4]; every other coefficient is held at its lift
    value.  For each of the 9^k assignments the FULL residual over Z is
    computed -- ALL rows of the equation index set, not merely the target
    monomial -- together with both collision differences over Z.
  * HALT EVENT: an assignment whose full residual is identically zero over Z
    AND whose two collision differences are both zero over Z.
  * The LANDSCAPE OF NEAR-MISSES is recorded at three strata, since the box
    turns out to contain assignments that kill the residual entirely but
    violate (C):
      - over the WHOLE box;
      - over the assignments satisfying both collision equalities over Z;
      - over the assignments satisfying (C) AND passing the additive
        degeneracy screen of keller_solver.degenerate_screen.
    At each stratum: the minimum number of non-zero residual rows and, among
    assignments attaining it, the minimum content gcd, with an attaining
    assignment.  Assignments whose residual vanishes identically over Z are
    counted separately and split by (C) and by the degeneracy screen.

The residual is computed directly from the bilinear tensor of the (K) system
in exact Python integers -- no floating point, no modular reduction anywhere.

Outputs: night9/lastterm/<hash>_<i>.json, night9/lastterm_index.json,
and the summary night9/LASTTERM.md.
"""
import json
import os
import sys
from itertools import product
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from keller_solver import build_system, degenerate_screen  # noqa: E402

BOX = list(range(-4, 5))                 # [-4 .. 4]


def rows_over_Z(eqs, pairs, a, b):
    """Exact integer residual, one entry per equation index, as a dict."""
    out = {}
    for e in eqs:
        v = 0
        for (mi, ni, c) in pairs[e]:
            v += c * a[mi] * b[ni]
        if e == (0, 0):
            v -= 1
        if v:
            out[e] = v
    return out


def collisions_over_Z(SP, SQ, a, b):
    cP = sum(a[i] for i, m in enumerate(SP) if m[0] == 0) - \
        sum(a[i] for i, m in enumerate(SP) if m[1] == 0)
    cQ = sum(b[j] for j, n in enumerate(SQ) if n[0] == 0) - \
        sum(b[j] for j, n in enumerate(SQ) if n[1] == 0)
    return cP, cQ


def content(rows):
    g = 0
    for v in rows.values():
        g = gcd(g, abs(v))
    return g


def formula_string(pairs_e, e):
    parts = []
    for (mi, ni, c) in sorted(pairs_e):
        s = "%+d*a_%d*b_%d" % (c, mi, ni)
        parts.append(s)
    body = "".join(parts) if parts else "0"
    if e == (0, 0):
        body += "-1"
    return body


def main():
    outdir = os.path.join(HERE, "lastterm")
    os.makedirs(outdir, exist_ok=True)
    cases = []

    for f in sorted(os.listdir(os.path.join(HERE, "altitude"))):
        d = json.load(open(os.path.join(HERE, "altitude", f)))
        SP = [tuple(m) for m in d["support_P"]]
        SQ = [tuple(m) for m in d["support_Q"]]
        eqs, pairs, cP, cQ = build_system(SP, SQ)
        for i, z in enumerate(d["matched_lifts_over_Z"]):
            if z["residual_n_terms"] != 1:
                continue
            a0 = list(z["balanced_lift_mod_6"]["a"])
            b0 = list(z["balanced_lift_mod_6"]["b"])
            R0 = rows_over_Z(eqs, pairs, a0, b0)
            assert len(R0) == 1, "expected a single-term residual"
            e = next(iter(R0))
            free_a = sorted({mi for (mi, ni, c) in pairs[e]})
            free_b = sorted({ni for (mi, ni, c) in pairs[e]})
            k = len(free_a) + len(free_b)

            strata = {"all": None, "collisions_ok": None,
                      "collisions_ok_and_nondegenerate": None}
            halts = []
            n_assign = 0
            zero_all = zero_coll = zero_coll_nd = 0
            for va in product(BOX, repeat=len(free_a)):
                a = list(a0)
                for idx, v in zip(free_a, va):
                    a[idx] = v
                for vb in product(BOX, repeat=len(free_b)):
                    b = list(b0)
                    for idx, v in zip(free_b, vb):
                        b[idx] = v
                    n_assign += 1
                    R = rows_over_Z(eqs, pairs, a, b)
                    dP, dQ = collisions_over_Z(SP, SQ, a, b)
                    coll = (dP == 0 and dQ == 0)
                    deg = degenerate_screen(SP, SQ, a, b)[0]
                    if not R:
                        zero_all += 1
                        if coll:
                            zero_coll += 1
                            if not deg:
                                zero_coll_nd += 1
                    if not R and coll:
                        halts.append({"a": list(a), "b": list(b),
                                      "degenerate_by_additive_screen": deg})
                    key = (len(R), content(R) if R else 0)
                    entry = (key, {"a": list(a), "b": list(b)},
                             {"collision_P_diff_over_Z": dP,
                              "collision_Q_diff_over_Z": dQ,
                              "collisions_hold_over_Z": coll},
                             {str(kk): vv for kk, vv in R.items()},
                             deg)
                    for name, ok in (("all", True),
                                     ("collisions_ok", coll),
                                     ("collisions_ok_and_nondegenerate",
                                      coll and not deg)):
                        if ok and (strata[name] is None or key < strata[name][0]):
                            strata[name] = entry

            rec = {
                "label": "CANDIDATE-UNVERIFIED",
                "hash": d["hash"],
                "lift_index_in_altitude_json": i,
                "max_total_degree": d["max_total_degree"],
                "support_P": [list(m) for m in SP],
                "support_Q": [list(m) for m in SQ],
                "ring": "Z (exact integer arithmetic throughout)",
                "lift_mod_6": {"a": a0, "b": b0},
                "single_term_residual": {
                    "monomial_x_exponent": e[0],
                    "monomial_y_exponent": e[1],
                    "coefficient_over_Z": R0[e],
                    "bracket_coefficient_formula": formula_string(pairs[e], e),
                },
                "free_set": {"a_indices": free_a, "b_indices": free_b,
                             "size": k},
                "box": "[-4..4] independently on each free coefficient; all "
                       "other coefficients held at the lift value",
                "assignments_examined": n_assign,
                "full_residual_computed_on_all_rows": True,
                "n_equation_rows": len(eqs),
                "HALT_EVENTS": halts,
                "n_halt_events": len(halts),
                "assignments_with_residual_identically_zero_over_Z": {
                    "total": zero_all,
                    "also_satisfying_collisions": zero_coll,
                    "also_satisfying_collisions_and_nondegenerate":
                        zero_coll_nd,
                },
                "near_miss_minimum_by_stratum": {
                    name: (None if s is None else {
                        "min_nonzero_residual_rows": s[0][0],
                        "content_gcd_at_minimum": s[0][1],
                        "attaining_assignment": s[1],
                        "collisions_there": s[2],
                        "residual_rows_there": s[3],
                        "degenerate_by_additive_screen": s[4],
                    })
                    for name, s in strata.items()
                },
            }
            path = os.path.join(outdir, "%s_%d.json" % (d["hash"], i))
            with open(path, "w") as g:
                json.dump(rec, g, indent=1)
            cases.append({"hash": d["hash"], "i": i, "free_size": k,
                          "assignments": n_assign,
                          "monomial": [e[0], e[1]],
                          "coefficient_over_Z": R0[e],
                          "formula": rec["single_term_residual"][
                              "bracket_coefficient_formula"],
                          "n_halt_events": len(halts),
                          "zero_residual_assignments": zero_all,
                          "zero_residual_with_collisions": zero_coll,
                          "zero_residual_with_collisions_nondegenerate":
                              zero_coll_nd,
                          "min_rows_all": strata["all"][0][0],
                          "min_rows_coll": (strata["collisions_ok"][0][0]
                                            if strata["collisions_ok"] else None),
                          "min_content_coll": (strata["collisions_ok"][0][1]
                                               if strata["collisions_ok"] else None),
                          "min_rows_coll_nondeg":
                              (strata["collisions_ok_and_nondegenerate"][0][0]
                               if strata["collisions_ok_and_nondegenerate"] else None),
                          "min_content_coll_nondeg":
                              (strata["collisions_ok_and_nondegenerate"][0][1]
                               if strata["collisions_ok_and_nondegenerate"] else None),
                          "file": os.path.relpath(path, HERE)})
            sc = strata["collisions_ok_and_nondegenerate"]
            print("%s#%d free=%d box=%d term=%+d*x^%d*y^%d halts=%d "
                  "zeroR=%d(coll %d, coll+nondeg %d) minC+ND=%s"
                  % (d["hash"], i, k, n_assign, R0[e], e[0], e[1], len(halts),
                     zero_all, zero_coll, zero_coll_nd,
                     ("(%d,%d)" % (sc[0][0], sc[0][1])) if sc else "none"),
                  flush=True)

    idx = {"n_single_term_lifts": len(cases),
           "total_zero_residual_assignments":
               sum(c["zero_residual_assignments"] for c in cases),
           "total_zero_residual_with_collisions":
               sum(c["zero_residual_with_collisions"] for c in cases),
           "two_term_fallback_taken": False,
           "box": "[-4..4] per free coefficient",
           "ring": "Z",
           "total_halt_events": sum(c["n_halt_events"] for c in cases),
           "cases": cases}
    with open(os.path.join(HERE, "lastterm_index.json"), "w") as g:
        json.dump(idx, g, indent=1)
    print("\ncases: %d   total HALT events: %d"
          % (len(cases), idx["total_halt_events"]))


if __name__ == "__main__":
    main()
