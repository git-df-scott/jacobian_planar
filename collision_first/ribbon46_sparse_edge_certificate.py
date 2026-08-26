#!/usr/bin/env python3
"""Exact closure of the first sparse (4,6) degree-(84,126) edge chart.

The chart keeps every outer weighted-edge monomial and the normalized
collision factor on the bottom row:

    p0=a*(x^84-x), p1=b*x^63+r1,
    p2=d*x^42+r2, p3=e*x^21+r3.

The constants r1,r2,r3 are retained (rather than silently set to zero).  In
the already verified upper-row reduction, the coefficient of x in E1 is
3*a^2*c.  The required vertices give a != 0 and c != 0, so the chart is empty
over characteristic zero.  This is a coefficient certificate, not a
numerical screen.
"""
import sympy as sp

from ribbon46_reduction import A, c, dp, p, survivors


x = sp.Symbol("x")
a, b, d, e, r1, r2, r3 = sp.symbols("a b d e r1 r2 r3")
rows = [a*(x**84-x), b*x**63+r1, d*x**42+r2, e*x**21+r3]
substitution = {p[i]: rows[i] for i in range(4)}
substitution.update({dp[i]: sp.diff(rows[i], x) for i in range(4)})

E1 = sp.Poly(sp.together(survivors[1].subs(substitution)), x)
certificate = sp.factor(E1.coeff_monomial(x))
assert certificate == 3*a**2*c

# Negative controls: changing the collision tail or removing the top Q vertex
# must destroy the displayed obstruction.
tail = sp.Symbol("tail")
changed = dict(substitution)
changed[p[0]] = a*(x**84-tail*x)
changed[dp[0]] = sp.diff(changed[p[0]], x)
assert sp.factor(sp.Poly(survivors[1].subs(changed), x).coeff_monomial(x)) \
       == 3*a**2*c*tail**2
assert certificate.subs(c, 0) == 0

print("COLLISION RIBBON (4,6) SPARSE EDGE CERTIFICATE: PASS")
print("coeff_x(E1) = 3*a^2*c; required a*c != 0; chart EMPTY in char0")
print("retained constants: r1,r2,r3; no division or generic lower-jet assumption")

