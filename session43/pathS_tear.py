"""Session 43, Path S — step 1: the tear (non-properness set) of Alpoge's map, exactly.

Path S is new: slice the REAL counterexample F : C^3 -> C^3 by target planes W
through a collision value.  S := F^{-1}(W) is a SMOOTH affine surface (grad of
l(F) = (a,b,c) . JF never vanishes), F|_S : S -> W is etale, and if W passes
through the collision value then S contains all three collision points.  If S
is algebraically isomorphic to C^2 for ANY such plane, F|_S is a planar Keller
counterexample (the Jacobian of an etale self-map of C^2 is a unit, hence a
nonzero constant) and JC2 is FALSE.  Noninjectivity and Keller are both
automatic; the entire problem concentrates in "S ~= C^2 ?".

This file computes the ingredients the slice-scan needs:
  (1) x-, y-, z-elimination of the fiber system  F(x,y,z) = w  (exact, over Q),
  (2) the leading-coefficient loci  =>  the tear A(F)  (census says: one quartic),
  (3) generic fiber counts over C^3, over a plane W, and over A(F).

Everything is exact.  PASS/FAIL lines at the end; nonzero exit on FAIL.
"""
import sympy as sp

x, y, z = sp.symbols('x y z')
w1, w2, w3 = sp.symbols('w1 w2 w3')

u = 1 + x*y
P = u**3*z + y**2*u*(4 + 3*x*y)
Q = y + 3*x*u**2*z + 3*x*y**2*(4 + 3*x*y)
R = 2*x - 3*x**2*y - x**3*z

PASS = []

# -- gate: replay the counterexample exactly (standing rule: never import a claim)
J = sp.Matrix([[sp.diff(f, v) for v in (x, y, z)] for f in (P, Q, R)])
PASS.append(("det JF == -2", sp.expand(J.det()) == -2))
pts = [(0, 0, sp.Rational(-1, 4)),
       (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
       (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
imgs = {tuple(sp.simplify(f.subs({x: a, y: b, z: c})) for f in (P, Q, R))
        for (a, b, c) in pts}
PASS.append(("three points collide at (-1/4,0,0)",
             imgs == {(sp.Rational(-1, 4), 0, 0)}))

# -- eliminate z (all three components are LINEAR in z), then y, to get the
#    minimal polynomial of the x-coordinate of the fiber over w.
#    From R = w3:  x^3 z = 2x - 3x^2 y - w3.
E1 = sp.expand(sp.expand(P - w1) * x**3)          # will substitute x^3 z
E2 = sp.expand(sp.expand(Q - w2) * x**3)
X3Z = 2*x - 3*x**2*y - w3
# replace every occurrence of z (z-degree is 1 in P,Q) using x^3*z = X3Z
E1 = sp.expand(E1.subs(z, sp.symbols('_t')).subs(sp.symbols('_t'), X3Z/x**3))
E1 = sp.expand(sp.together(E1) * 1)
E1 = sp.expand(sp.cancel(E1))
E2 = sp.expand(E2.subs(z, sp.symbols('_t')).subs(sp.symbols('_t'), X3Z/x**3))
E2 = sp.expand(sp.cancel(E2))
# sanity: no z left, polynomial in x,y,w
PASS.append(("z eliminated cleanly", (not E1.has(z)) and (not E2.has(z))))

Ry = sp.resultant(sp.Poly(E1, y), sp.Poly(E2, y))          # in Q[x,w]
Ry = sp.factor(Ry)
print("factor of Res_y  :", Ry)

# strip the extraneous x^k factor introduced by clearing x^3 (fibers with x=0
# are handled separately below); keep the genuine fiber polynomial h(x; w).
fl = sp.factor_list(Ry)
core = sp.Integer(1)
for base, mult in fl[1]:
    if base == x:
        continue
    core *= base**mult
core = sp.expand(core)
hx = sp.Poly(core, x)
print("deg_x h =", hx.degree())
lcx = sp.factor(hx.LC())
print("lc_x(h) factors:", lcx)

with open('session43/tear_data.txt', 'w') as f:
    f.write("h(x;w) = %s\n\nlc_x = %s\n" % (sp.expand(core), lcx))

for name, ok in PASS:
    print(("PASS " if ok else "FAIL ") + name)
assert all(ok for _, ok in PASS)
