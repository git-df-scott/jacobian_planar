#!/usr/bin/env python3
"""End-to-end controls for the sweep verdict.

POSITIVE control.  At p = 67 the point (u,v,w) = (57,61,25) passes the first
three cap conditions.  This script rebuilds its truncated rows independently
and replays them through the ORIGINAL ``survivors`` objects of
ribbon46_reduction.py, checking mod 67 that

    E2 = 0, E1 = 0, E0 = 1     coefficientwise through x^24,
    deg p3 <= 21 (p3[22] = p3[23] = p3[24] = 0),

and that the FOURTH cap condition genuinely fails:  [x^25](E0 - 1) != 0 even
though p3[25] is pinned to 0.  So the pipeline is demonstrably able to certify
a point that satisfies conditions -- a real candidate would not be missed.

NEGATIVE control.  The published rational seed (u,v,w) = (1,0,0) must fail at
the very first cap condition, reproducing the known boundary certificate.
"""
import sys
from fractions import Fraction

import numpy as np
import sympy as sp

from lane6_core import FpRing, run
from lane6_sweep import CAPS
from ribbon46_reduction import A, c as csym, dp, p as psym, survivors

P = 67
x = sp.Symbol("x")


def replay(u, v, w, N):
    """Rebuild rows from the F_p engine and replay them through survivors."""
    R = FpRing(P, 1)
    r = run(R, R.const(u), R.const(v), R.const(w), N, caps=CAPS)
    top = N + 1

    def poly(arr):
        return sum(int(arr[n][0]) * x ** n for n in range(top + 1))

    rows = [x ** 84 - x, poly(r["p1"]), poly(r["p2"]), poly(r["p3"])]
    sub = {psym[i]: rows[i] for i in range(4)}
    sub.update({dp[i]: sp.diff(rows[i], x) for i in range(4)})
    sub[csym] = sp.Integer(1)
    sub[A[0]] = sp.Integer(0)
    sub[A[4]] = sp.Integer(0)
    for j in (1, 2, 3, 5):
        sub[A[j]] = sp.Integer(int(r["A%d" % j][0]))

    resid = {}
    for degree, target in ((2, 0), (1, 0), (0, 1)):
        pol = sp.Poly(sp.expand((survivors[degree] - target).subs(sub)), x)
        resid[degree] = {}
        for n in range(N + 1):
            q = sp.Rational(pol.coeff_monomial(x ** n))
            den = int(q.q)
            assert den % P != 0, "denominator divisible by p at x^%d" % n
            resid[degree][n] = (int(q.p) * pow(den, P - 2, P)) % P
    return r, rows, resid


def main():
    ok = True
    print("=" * 74)
    print("POSITIVE CONTROL: p=67, (u,v,w) = (57,61,25)")
    print("=" * 74)
    r, rows, resid = replay(57, 61, 25, 25)
    print("deg p3 =", sp.degree(rows[3], x), " (cap requires <= 21)")
    print("p3[22], p3[23], p3[24], p3[25] =",
          [int(r["p3"][n][0]) for n in (22, 23, 24, 25)])
    for degree, target, label in ((2, 0, "E2"), (1, 0, "E1"), (0, 1, "E0-1")):
        bad = [n for n in range(25) if resid[degree][n]]
        print("  %-4s coefficients x^0..x^24 mod 67 : %s"
              % (label, "ALL VANISH" if not bad else "nonzero at %s" % bad))
        if bad:
            ok = False
    e25 = resid[0][25]
    print("  [x^25](E0-1) mod 67 =", e25,
          "-> fourth cap condition FAILS" if e25 else "-> would be a CANDIDATE")
    if e25 == 0:
        ok = False
    # the engine's own recorded condition values must agree
    eng = [int(r["cond"][("p3", n)][0]) % P for n in (22, 23, 24, 25)]
    print("  engine-recorded conditions E0[22..25] =", eng,
          "(matches SymPy replay:",
          eng == [resid[0][22], resid[0][23], resid[0][24], resid[0][25]], ")")
    if eng != [resid[0][n] for n in (22, 23, 24, 25)]:
        ok = False

    print()
    print("=" * 74)
    print("NEGATIVE CONTROL: the published rational seed (u,v,w) = (1,0,0)")
    print("=" * 74)
    r2, rows2, resid2 = replay(1, 0, 0, 23)
    bad = [n for n in range(22) if resid2[0][n] or resid2[1][n] or resid2[2][n]]
    print("  E2,E1,E0-1 coefficients x^0..x^21 mod 67:",
          "ALL VANISH" if not bad else "nonzero at %s" % bad)
    print("  [x^22](E0-1) mod 67 =", resid2[0][22],
          "-> first cap condition FAILS, as the published certificate says")
    if bad or resid2[0][22] == 0:
        ok = False

    print()
    print("=" * 74)
    print("CONTROLS:", "PASS" if ok else "FAIL")
    print("=" * 74)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
