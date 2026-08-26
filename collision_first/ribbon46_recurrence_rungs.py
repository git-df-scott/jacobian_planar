#!/usr/bin/env python3
"""Kernel-retaining local recurrence for the live collision (4,6) system.

This verifies the x^0, x^1, and x^2 recurrence levels exactly.  The calculation
is local at x=0 with p0=-x (the x^84 term first affects much later levels).
It proves a generic formal branch survives these levels; it does not prove
polynomial termination, the second collision endpoint, or a counterexample.
"""
import sympy as sp

from ribbon46_reduction import A, c, dp, p, survivors


x = sp.Symbol("x")
u, v, w = sp.symbols("u v w")
a, b, t = sp.symbols("a b t")
r, s, z = sp.symbols("r s z")

rows = [
    -x,
    u*x+a*x**2+r*x**3,
    v*x+b*x**2+s*x**3,
    w*x+t*x**2+z*x**3,
]
substitution = {p[i]: rows[i] for i in range(4)}
substitution.update({dp[i]: sp.diff(rows[i], x) for i in range(4)})

# Rung x^0: u,v,w are free and the first three active integration constants
# are fixed.  A0,A4 do not enter the surviving differential identities.
A1 = -1
A2 = -u/2
A3 = -(u**2+v)/3

# Rung x^1: the obstruction fixes A5, the two image equations fix a,b, and t
# is the retained kernel coefficient.
A5 = -(u**4+3*u**2*v+2*u*w+v**2)/5
a_value = (u**5+4*u**3*v+3*u**2*w+3*u*v**2+2*v*w+6)/4
b_value = -sp.Rational(3, 8)*(
    u**6+3*u**4*v+2*u**3*w-2*u*v*w+12*u-v**3-w**2
)

constants = {c: 1, A[1]: A1, A[2]: A2, A[3]: A3, A[5]: A5}
residuals = {}
for degree, target in ((2, 0), (1, 0), (0, 1)):
    residuals[degree] = sp.Poly(
        sp.expand((survivors[degree]-target).subs(substitution).subs(constants)), x
    )

for degree in (2, 1, 0):
    assert sp.factor(residuals[degree].coeff_monomial(1)) == 0
    assert sp.factor(residuals[degree].coeff_monomial(x).subs(
        {a: a_value, b: b_value}
    )) == 0

# Rung x^2: E0 is the obstruction.  It is independent of the new r,s,z and
# linear in the previous kernel t with coefficient 3*u/4.
obstruction = sp.factor(residuals[0].coeff_monomial(x**2).subs(
    {a: a_value, b: b_value}
))
assert all(sp.diff(obstruction, variable) == 0 for variable in (r, s, z))
assert sp.factor(sp.diff(obstruction, t)) == 3*u/4
t_value = sp.factor(-obstruction.subs(t, 0)/(sp.Rational(3, 4)*u))
assert sp.factor(obstruction.subs(t, t_value)) == 0

# With that obstruction removed, E2,E1 determine r,s uniquely while z is the
# next retained kernel.  The coefficient matrix is nonsingular identically.
upper = [sp.factor(residuals[degree].coeff_monomial(x**2).subs(
    {a: a_value, b: b_value, t: t_value}
)) for degree in (2, 1)]
matrix = sp.Matrix([[sp.diff(expression, variable) for variable in (r, s)]
                    for expression in upper])
assert matrix == sp.Matrix([[-3*u, -3], [-3, 0]])
assert matrix.det() == -9

# A completely rational planted specialization independently replays all
# three residuals through x^2.  It is the next seed for automated descent.
rational_rows = [
    -x,
    x+sp.Rational(7, 4)*x**2+sp.Rational(1, 4)*x**3,
    -sp.Rational(39, 8)*x**2-sp.Rational(49, 8)*x**3,
    sp.Rational(33, 8)*x**2,
]
rational_substitution = {p[i]: rational_rows[i] for i in range(4)}
rational_substitution.update({
    dp[i]: sp.diff(rational_rows[i], x) for i in range(4)
})
rational_substitution.update({
    c: 1, A[1]: -1, A[2]: -sp.Rational(1, 2),
    A[3]: -sp.Rational(1, 3), A[5]: -sp.Rational(1, 5),
})
for degree, target in ((2, 0), (1, 0), (0, 1)):
    replay = sp.Poly(sp.expand(
        (survivors[degree]-target).subs(rational_substitution)
    ), x)
    assert all(replay.coeff_monomial(x**power) == 0 for power in range(3))

print("COLLISION RIBBON (4,6) KERNEL-RETAINING RECURRENCE: PASS")
print("x^0: free u,v,w; A1,A2,A3 determined")
print("x^1: A5,p1[2],p2[2] determined; p3[2] retained")
print("x^2: obstruction coefficient in p3[2] is 3*u/4")
print("generic u!=0 fixes p3[2]; det for p1[3],p2[3] is -9")
print("rational seed: u=1,v=w=z=0; p1[2:4]=7/4,1/4;")
print("               p2[2:4]=-39/8,-49/8; p3[2]=33/8")
print("SURVIVES THROUGH x^2; p3[3] is the next kernel; NOT A CE")
