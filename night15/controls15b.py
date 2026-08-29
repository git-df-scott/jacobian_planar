"""night15 -- C1 addendum (HIGH-DEGREE coordinates) and the shear control.

controls15.py builds its coordinate pairs by composing triangular maps and
then screens the FIRST member of the pair, which is always the low-degree one.
This addendum screens the SECOND member, which is where the degree lives, and
adds the G3 shear control: P and P o phi (phi a Jacobian-1 automorphism) have
isomorphic fibres carrying the same eta, so the period verdict must agree.
"""

import json
import os
import sys
from fractions import Fraction as F

import pk15 as P14
import sy15
import mono15
import exact_he15
import gen15
from controls15 import T_shift, S_swap, bracket, run_screen, brief

HERE = os.path.dirname(os.path.abspath(__file__))
x = {(1, 0): F(1)}
y = {(0, 1): F(1)}


def build():
    out = []
    FG = (x, y)
    FG = T_shift(FG, {3: F(1)})
    FG = S_swap(FG)
    FG = T_shift(FG, {3: F(1), 1: F(2)})
    out.append(("deg9 coordinate (deg_y 3)", FG[1], P14.pscal(-1, FG[0])))
    FG = (x, y)
    FG = T_shift(FG, {2: F(1)})
    FG = S_swap(FG)
    FG = T_shift(FG, {5: F(1), 2: F(-1)})
    out.append(("deg10 coordinate (deg_y 5)", FG[1], P14.pscal(-1, FG[0])))
    FG = (x, y)
    FG = T_shift(FG, {2: F(1), 1: F(1)})
    FG = S_swap(FG)
    FG = T_shift(FG, {3: F(2)})
    FG = S_swap(FG)
    FG = T_shift(FG, {2: F(1)})
    out.append(("deg12 coordinate", FG[1], P14.pscal(-1, FG[0])))
    return out


def main():
    CS = [F(0), F(1), F(-1)]
    rec = {"C1_high_degree": [], "shear_control": []}
    print("=" * 78)
    print("C1 (addendum) -- HIGH-DEGREE coordinates with an exact mate")
    print("=" * 78)
    for lab, P, Q in build():
        br = bracket(P, Q)
        assert br == {(0, 0): F(1)}, (lab, br)
        sy, _ = sy15.certify(P, node_budget=200000)
        print("\n%s   deg P=%d deg_y=%d  [P,Q]-1 = 0 exactly, SY=%s"
              % (lab, P14.tdeg(P), max(j for (i, j) in P), sy))
        fib = run_screen(P, CS, lab)
        for r in fib:
            print("   " + brief(r))
        sys.stdout.flush()
        rec["C1_high_degree"].append(
            {"label": lab, "deg_P": P14.tdeg(P), "SY": sy,
             "P": P14.to_str(P), "Q": P14.to_str(Q), "fibres": fib})

    print()
    print("=" * 78)
    print("SHEAR CONTROL -- P and P o phi must give the same period verdict")
    print("=" * 78)
    C = gen15.corpus()
    picks = [C[4], C[10], C[60]]
    for P0, lab, meta in picks:
        Ps = gen15.shear(P0, {1: F(1), 2: F(-1)}, {1: F(2), 0: F(1)})
        a = exact_he15.screen(P0, F(1))
        b = exact_he15.screen(Ps, F(1))
        print("%-42s base=%-14s sheared=%-14s deg %d -> %d  MATCH=%s"
              % (lab[:42], a.get("verdict"), b.get("verdict"),
                 P14.tdeg(P0), P14.tdeg(Ps), a.get("verdict") == b.get("verdict")))
        rec["shear_control"].append(
            {"label": lab, "base": a.get("verdict"), "sheared": b.get("verdict"),
             "deg_base": P14.tdeg(P0), "deg_sheared": P14.tdeg(Ps),
             "match": a.get("verdict") == b.get("verdict")})
        sys.stdout.flush()
    with open(os.path.join(HERE, "controls15b.json"), "w") as fh:
        json.dump(rec, fh, indent=1, default=str)
    print("\nwritten controls15b.json")


if __name__ == "__main__":
    main()
