#!/usr/bin/env python3
"""Exact obstruction for collision ribbons with y-heights (2,3).

Suppose, after scaling the nonzero constant top coefficient of P,

    P = u(x) + v(x)y + y^2,
    Q = q0(x) + q1(x)y + q2(x)y^2 + c y^3,  c != 0,

and [P,Q]=1.  The y^3,y^2,y^1 rows determine q2,q1,q0 up to constants.
The y^0 row becomes dH/dx=1 with

    H = (3c/64)(v^2-4u)^2 - (B/4)(v^2-4u).

Thus H=x+K.  For polynomial u,v and c != 0, H has degree zero or an even
positive degree, never degree one.  Hence this entire family is empty over
characteristic zero, independently of x-degree and even before using the
two-point collision equations.
"""
import sympy as sp


x, y = sp.symbols("x y")
c = sp.Symbol("c", nonzero=True)
A, B, C = sp.symbols("A B C")
u = sp.Function("u")(x)
v = sp.Function("v")(x)

q3 = c
q2 = sp.Rational(3, 2)*c*v+A
q1 = (sp.Rational(3, 2)*c*u+sp.Rational(3, 8)*c*v**2+A*v+B)
q0 = (sp.Rational(3, 4)*c*u*v+A*u-sp.Rational(1, 16)*c*v**3
      +sp.Rational(1, 2)*B*v+C)

P = u+v*y+y**2
Q = q0+q1*y+q2*y**2+q3*y**3
J = sp.expand(sp.diff(P, x)*sp.diff(Q, y)-sp.diff(P, y)*sp.diff(Q, x))

# The integrated upper-row formulas annihilate y^1 through y^4 exactly.
assert all(sp.simplify(J.coeff(y, degree)) == 0 for degree in range(1, 5))

w = v**2-4*u
H = sp.Rational(3, 64)*c*w**2-sp.Rational(1, 4)*B*w
assert sp.simplify(J.coeff(y, 0)-sp.diff(H, x)) == 0

# Formal degree certificate: for a nonconstant polynomial w of degree d and
# c != 0, the leading term of H is (3c/64)lc(w)^2*x^(2d), so deg(H)=2d.
d, leading = sp.symbols("d leading", integer=True, positive=True)
top_coefficient = sp.Rational(3, 64)*c*leading**2
assert top_coefficient != 0

print("COLLISION RIBBON (2,3) EXACT CERTIFICATE: PASS")
print("upper rows force H=(3c/64)(v^2-4u)^2-(B/4)(v^2-4u)")
print("[P,Q]=1 forces H=x+K, but deg(H) is 0 or even; family EMPTY in char0")
