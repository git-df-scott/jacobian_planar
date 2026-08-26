#!/usr/bin/env python3
"""Exact algebraic *truncated linear slice* in the live (4,6) frontier.

This restores linear lower coefficients omitted by the sparse-edge closure but
sets all quadratic coefficients to zero.  Since the equations are first order,
quadratic coefficients also enter the x^1 residual.  Thus this is an exact
special polynomial slice, not a formal first-jet lifting result and not a
Keller map or counterexample.  See ribbon46_recurrence_rungs.py for the proper
kernel-retaining recurrence.
"""
import sympy as sp

from ribbon46_reduction import A, c, dp, p, survivors


x, u, v = sp.symbols("x u v")
b, d, e = sp.symbols("b d e")
rows = [x**84-x, b*x**63+u*x, d*x**42+v*x, e*x**21]
substitution = {p[i]: rows[i] for i in range(4)}
substitution.update({dp[i]: sp.diff(rows[i], x) for i in range(4)})

# The constant equations solve the integration constants; the remaining
# linear equations solve A5 and leave two equations in the two linear jets.
A1 = -1
A2 = -u/2
A3 = -(v+u**2)/3
A5 = -(3*u**2*v+u**4+v**2)/5
substitution.update({c: 1, A[1]: A1, A[2]: A2, A[3]: A3, A[5]: A5})

f = -u**6-u**4*v+6*u**2*v**2-24*u+3*v**3
g = -u**5-4*u**3*v-3*u*v**2-6
h = u**15+96*u**10-2052*u**5-216
linear_v = -7*u**12-663*u**7+16380*u**2+3258*v

groebner = sp.groebner([f, g], v, u, order="lex")
assert [sp.factor(poly.as_expr()) for poly in groebner.polys] == [linear_v, h]
assert h.subs(u, 0) != 0

# Independent replay against the three original surviving one-forms.
for degree, target in ((2, 0), (1, 0), (0, 1)):
    residual = sp.Poly(sp.together((survivors[degree]-target).subs(substitution)), x)
    assert sp.factor(residual.coeff_monomial(1)) == 0
    coefficient = sp.factor(residual.coeff_monomial(x))
    numerator = sp.together(coefficient.subs(v,
        (7*u**12+663*u**7-16380*u**2)/3258)).as_numer_denom()[0]
    assert sp.rem(numerator, h, domain=sp.QQ) == 0

print("COLLISION RIBBON (4,6) TRUNCATED LINEAR SLICE: PASS")
print("h(u)=u^15+96*u^10-2052*u^5-216=0")
print("3258*v=7*u^12+663*u^7-16380*u^2")
print("all E2,E1,E0 coefficients through x^1 vanish exactly modulo h")
print("NOT A FORMAL-JET CLAIM: quadratic coefficients were fixed to zero")

