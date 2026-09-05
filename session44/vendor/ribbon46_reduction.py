#!/usr/bin/env python3
# VENDORED unchanged from codex/sol6-collision-first:collision_first/ribbon46_reduction.py (commit 4fbdccb)
"""Exact upper-row reduction for the live collision ribbon of heights (4,6).

Use formal row coefficients

    P = p0+p1*y+p2*y^2+p3*y^3+y^4,
    Q = q0+...+q5*y^5+c*y^6.

The y^8 down through y^3 Jacobian rows are exact polynomial one-forms in the
four p-rows.  This script integrates each one over Q, reconstructs q5,...,q0,
and verifies those seven upper rows vanish identically.  The whole original
Keller equation is thereby reduced to the three surviving rows

    E2=0, E1=0, E0=1,

plus the two original-coordinate collision values.  No division by a
coefficient or genericity assumption is used after the top gauges.
"""
import sympy as sp


p = sp.symbols("p0:4")
dp = sp.symbols("dp0:4")
c = sp.Symbol("c", nonzero=True)
A = sp.symbols("A0:6")
P = list(p)+[sp.Integer(1)]


def derivative(expression):
    return sp.expand(sum(sp.diff(expression, p[i])*dp[i] for i in range(4)))


def row(q, degree):
    return sp.expand(sum(
        derivative(P[i])*j*q[j]-i*P[i]*derivative(q[j])
        for i in range(5) for j in range(7)
        if i+j-1 == degree and j in q
    ))


def integrate_closed_form(form):
    coefficients = [sp.expand(sp.diff(form, differential)) for differential in dp]
    assert sp.expand(form-sum(a*b for a, b in zip(coefficients, dp))) == 0
    assert all(sp.expand(sp.diff(coefficients[i], p[j])
                         -sp.diff(coefficients[j], p[i])) == 0
               for i in range(4) for j in range(i+1, 4))
    parameter = sp.Symbol("parameter")
    scaling = {variable: parameter*variable for variable in p}
    primitive = sp.integrate(
        sum(p[i]*coefficients[i].subs(scaling) for i in range(4)),
        (parameter, 0, 1),
    )
    primitive = sp.expand(primitive)
    assert sp.expand(derivative(primitive)-form) == 0
    return primitive


q = {6: c}
for degree in range(8, 2, -1):
    q_index = degree-3
    # The i=4 term is -4*D(q_index); all other q rows are already known.
    form = row(q, degree)/4
    q[q_index] = integrate_closed_form(form)+A[q_index]

assert all(sp.expand(row(q, degree)) == 0 for degree in range(3, 10))
survivors = {degree: row(q, degree) for degree in (2, 1, 0)}
term_counts = {degree: len(sp.Poly(value, *(p+dp+A+(c,))).terms())
               for degree, value in survivors.items()}

# Degree-126 weighted triangle: deg p_i=84-21i and the reconstructed
# deg q_j=126-21j.  Hence deg_x E_k <=188-21k.
x_degree_bounds = {degree: 188-21*degree for degree in survivors}
equation_counts = {degree: bound+1 for degree, bound in x_degree_bounds.items()}
assert sum(equation_counts.values()) == 504

print("COLLISION RIBBON (4,6) UPPER REDUCTION: PASS")
print("q5,...,q0 integrated exactly; Jacobian rows y^3,...,y^9 vanish")
print("surviving formal term counts:", term_counts)
print("degree-126 coefficient equations:", equation_counts, "total=504")
print("reduced frontier: 212 P coefficients + 7 constants; E2=E1=0, E0=1")
