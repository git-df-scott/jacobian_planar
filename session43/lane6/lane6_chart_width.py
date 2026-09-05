#!/usr/bin/env python3
"""Is the prior local ansatz p1(0) = p2(0) = p3(0) = 0 a gauge or a restriction?

The collision normalisation P(0,0)=P(1,0)=Q(0,0)=Q(1,0)=0 forces only
p0(0) = p0(1) = 0.  The prior recurrence script additionally takes

    p1 = u x + ...,   p2 = v x + ...,   p3 = w x + ...,

i.e. p_i(0) = 0 for i = 1,2,3.  The y-shears y -> y + f(x) that preserve both
the weighted triangle (deg f <= 21) and the two collision points must satisfy
f(0) = f(1) = 0, so they cannot move p1(0), p2(0), p3(0).

This script restores generic constants g1, g2, g3 and asks rung 0 whether they
are obstructed.  It uses the independently validated q_j' chain at index 0
(see lane6_core.py; the chain was proved identical to ribbon46_reduction.py's
survivors objects).  Gauges a = c = 1, A4 = 0.
"""
import sys

import sympy as sp

g1, g2, g3, u, v, w = sp.symbols("g1 g2 g3 u v w")
A1, A2, A3, A5 = sp.symbols("A1 A2 A3 A5")
c = sp.Integer(1)
A4 = sp.Integer(0)


def rung0():
    """The three rung-0 equations E0[0]-1, E1[0], E2[0] with generic g."""
    q5 = A5 + sp.Rational(3, 2) * c * g3
    q5p = sp.Rational(3, 2) * c * w
    q4p = (5 * w * q5 - 3 * g3 * q5p + 6 * c * v) / 4
    q3p = (4 * w * A4 - 3 * g3 * q4p + 5 * v * q5 - 2 * g2 * q5p + 6 * c * u) / 4
    q2p = (3 * w * A3 - 3 * g3 * q3p + 4 * v * A4 - 2 * g2 * q4p
           + 5 * u * q5 - g1 * q5p - 6 * c) / 4
    q1p = (2 * w * A2 - 3 * g3 * q2p + 3 * v * A3 - 2 * g2 * q3p
           + 4 * u * A4 - g1 * q4p - 5 * q5) / 4
    q0p = (w * A1 - 3 * g3 * q1p + 2 * v * A2 - 2 * g2 * q2p
           + 3 * u * A3 - g1 * q3p - 4 * A4) / 4
    E0 = -g1 * q0p - A1 - 1
    E1 = -2 * g2 * q0p + u * A1 - g1 * q1p - 2 * A2
    E2 = (-3 * g3 * q0p + v * A1 - 2 * g2 * q1p + 2 * u * A2
          - g1 * q2p - 3 * A3)
    return [E0, E1, E2]


def main():
    print("=" * 74)
    print("CHART WIDTH: are p1(0), p2(0), p3(0) forced to vanish at rung 0?")
    print("=" * 74)
    eqs = rung0()
    sol = sp.solve(eqs, [A1, A2, A3], dict=True)
    print("rung-0 system with GENERIC g1,g2,g3 : %d solution branch(es) for "
          "(A1,A2,A3)" % len(sol))
    ok = len(sol) == 1
    if ok:
        s = sol[0]
        den = sp.factor(sp.together(s[A1]).as_numer_denom()[1])
        print("  unique solution; the only degeneracy is the vanishing of")
        print("    ", den)
        zero = {g1: 0, g2: 0, g3: 0}
        got = [sp.simplify(s[A1].subs(zero)), sp.simplify(s[A2].subs(zero)),
               sp.simplify(s[A3].subs(zero))]
        want = [sp.Integer(-1), -u / 2, -(u ** 2 + v) / 3]
        agree = all(sp.simplify(a - b) == 0 for a, b in zip(got, want))
        print("  specialises at g = (0,0,0) to A1,A2,A3 =", got)
        print("  matches the documented -1, -u/2, -(u^2+v)/3 :", agree)
        ok = ok and agree
    print()
    print("VERDICT: rung 0 imposes NO condition on g1,g2,g3 -- it merely")
    print("re-solves A1,A2,A3.  So p1(0), p2(0), p3(0) are unobstructed extra")
    print("directions of the frontier which the prior ansatz sets to zero by")
    print("hand.  The full local problem has parameters")
    print("    (a, c, p1(0), p2(0), p3(0), u, v, w)  ->  6 essential after the")
    print("2-torus, versus the 3 swept in lane6_complete.py.")
    print()
    print("CHART WIDTH TEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
