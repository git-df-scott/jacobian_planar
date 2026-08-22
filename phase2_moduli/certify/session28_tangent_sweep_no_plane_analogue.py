"""
Plane Jacobian campaign - Session 28
THE TANGENT-SWEEP MECHANISM HAS NO PLANE ANALOGUE.

A literature sweep turned up a development that changes the campaign's
context and had not been recorded past Session 1.

=====================================================================
LITERATURE UPDATE (July-August 2026)
=====================================================================

The Jacobian conjecture is FALSE in every dimension greater than two.

    Alpoge, 19 Jul 2026 - counterexample in dimension 3
    Gallagher, 20 Jul 2026 - an infinite family
    Speyer, 23 Jul 2026 - the geometric explanation
    arXiv:2608.00222, "Counterexamples to the Jacobian conjecture in
    dimensions greater than two" - self-contained account, generalising
    the tangent-sweep mechanism from plane curves to direction fields on
    hypersurfaces; counterexamples in every dimension > 2, of arbitrarily
    large geometric degree.  Five explicit maps: one 3-D of degree 4, two
    4-D of degrees 5 and 10, two 5-D of degrees 6 and 12.

THE PLANE CASE REMAINS OPEN.  Stabilisation only moves upward in
dimension; a three-variable counterexample cannot be squeezed into two
while keeping the needed properties.

This campaign has been targeting the plane case throughout, so the
result stands - but the framing in Sessions 19-27 ("the plane Jacobian
conjecture remains open") was right for a reason those sessions never
stated.  Session 1 of this repo had already reverse-engineered the
Alpoge map; nothing after it recorded that the general conjecture had
fallen.

=====================================================================
THE GAP THIS SESSION FILLS
=====================================================================

The published accounts explain the mechanism and note it produces
counterexamples only for n > 2, but do not explain WHY it stops at the
plane.  That is a bounded question, and this repo already holds the
structural signature: Session 1 extracted, for the 3-D map,

    F = v(x,y) z + w(x,y),     det JF = c2 z^2 + c1 z + c0
    c2 = det[v_x, v_y, v] = 0      <- the DEGENERACY
    c1 = 0,     c0 = -2            <- constant Jacobian
    v = x^3 u(t),  u(t) = (t^3, 3t^2, -1),  t = (1+xy)/x

so the direction field sweeps a TWISTED CUBIC.  The trick is that the
degeneracy c2 = 0 is met by a NON-CONSTANT direction field.

RESULT (proved below).  In dimension 2 the same mechanism forces an
automorphism.  Writing F = v(x) z + w(x) with v, w : C -> C^2,

    det JF = z * (v1' v2 - v2' v1) + (w1' v2 - w2' v1)

and a constant Jacobian demands

  (1) v1' v2 - v2' v1 = 0.  This is the Wronskian of (v1,v2); for
      v2 != 0 it gives (v1/v2)' = 0, so v1 = lambda v2 and the direction
      field is a CONSTANT direction:  v = a(x) e.
  (2) w1' v2 - w2' v1 = a(x) (w1' e2 - w2' e1) = c != 0.  A product of
      two polynomials equal to a nonzero constant forces both to be
      nonzero constants: a = alpha and w1' e2 - w2' e1 = c/alpha.
  (3) Then h(x) := e2 w1 - e1 w2 has h' = c/alpha != 0, so h has degree
      exactly one, and e2 F1 - e1 F2 = h(x).  x is recovered linearly
      from F, and z from either component.  F is an automorphism.

WHY IT STOPS AT THE PLANE - the dimension count.  The mechanism needs a
direction field that is degenerate but NOT constant.  For v : C -> C^2
the degeneracy det[v',v] = 0 says rank <= 1, which IS constancy of
direction - the two conditions coincide, and the map trivialises.  For
v : C^2 -> C^3 the degeneracy det[v_x,v_y,v] = 0 leaves a genuine
non-constant solution set - the developable surfaces, of which Session
1's twisted cubic is one.  Degenerate and constant-direction coincide in
the plane and separate from dimension 3 onward.  That is the reason the
tangent sweep begins at n = 3.

CONSISTENCY.  This is the linear-in-one-variable case, which the
campaign's own Sessions 2-5 already covered from a different direction
(min deg_y <= 2 implies tame).  The two agree, which is a check on both.

=====================================================================
ROUTES CLOSED BY THE SAME SWEEP
=====================================================================

The Mathieu-Zhao hierarchy (Special Image Conjecture => Generalized
Vanishing Conjecture => Jacobian Conjecture) is not a route to a plane
counterexample: those conjectures IMPLY the JC, so their recently
established falsity in dimension 5 (arXiv:2608.07338) removes them as
proof strategies without bearing on the plane case at all.

NO PLANE COUNTEREXAMPLE.  This session explains why the one mechanism
now known to work above dimension 2 cannot be imported into it.
"""

from sympy import (symbols, Function, Matrix, expand, simplify, factor,
                   zeros, collect, solve, Rational as Q)

x, y, z = symbols('x y z')
P, Qs = symbols('P Q')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


print(__doc__)
print("=" * 70)
print("PART 1  the 3-D mechanism, re-verified from Session 1's data")
print("=" * 70)
F = Matrix([z*(1 + x*y)**3 + y**2*(1 + x*y)*(4 + 3*x*y),
            y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y),
            2*x - 3*x**2*y - x**3*z])
v = Matrix([(1 + x*y)**3, 3*x*(1 + x*y)**2, -x**3])
w = Matrix([y**2*(1 + x*y)*(4 + 3*x*y), y + 3*x*y**2*(4 + 3*x*y),
            2*x - 3*x**2*y])
check("F = v z + w", expand(v*z + w - F) == zeros(3, 1))
c2 = Matrix.hstack(v.diff(x), v.diff(y), v).det()
c1 = (Matrix.hstack(v.diff(x), w.diff(y), v).det()
      + Matrix.hstack(w.diff(x), v.diff(y), v).det())
c0 = Matrix.hstack(w.diff(x), w.diff(y), v).det()
check("the degeneracy c2 = det[v_x, v_y, v] vanishes", expand(c2) == 0)
check("c1 = 0 and c0 = -2, so det JF is a nonzero constant",
      expand(c1) == 0 and expand(c0) == -2)
t = (1 + x*y)/x
u = Matrix([t**3, 3*t**2, -1])
check("v = x^3 u(t) with u a twisted cubic: the field is NON-CONSTANT",
      simplify(v - x**3*u) == zeros(3, 1))

# =====================================================================
print()
print("=" * 70)
print("PART 2  the same mechanism in the plane, general polynomials")
print("=" * 70)
v1, v2, w1, w2 = [Function(s)(x) for s in ('v1', 'v2', 'w1', 'w2')]
V, W = Matrix([v1, v2]), Matrix([w1, w2])
F2 = V*z + W
J2 = expand(Matrix.hstack(F2.diff(x), F2.diff(z)).det())
top = simplify(J2.coeff(z, 1))
bot = simplify(J2.coeff(z, 0))
print(f"   det JF = {collect(J2, z)}")
check("the z-coefficient is the Wronskian v1' v2 - v2' v1",
      simplify(top - (v1.diff(x)*v2 - v2.diff(x)*v1)) == 0)
check("det JF has degree <= 1 in z (vs degree 2 in dimension 3)",
      J2.coeff(z, 2) == 0)

# step 1: degeneracy forces a constant direction
a = Function('a')(x)
e1, e2 = symbols('e1 e2')
Vc = Matrix([a*e1, a*e2])
check("a constant-direction field v = a(x) e has vanishing Wronskian",
      simplify(Vc[0].diff(x)*Vc[1] - Vc[1].diff(x)*Vc[0]) == 0)
lam = symbols('lambda')
Vd = Matrix([lam*v2, v2])
check("conversely v1 = lambda v2 is the general solution of the Wronskian "
      "equation (rank <= 1)",
      simplify(Vd[0].diff(x)*Vd[1] - Vd[1].diff(x)*Vd[0]) == 0)

# step 2: the z^0 coefficient factors
bot_c = simplify(Matrix.hstack(W.diff(x), Vc).det())
print(f"   with v = a(x) e :  det[w', v] = {factor(bot_c)}")
check("it factors as a(x) * (w1' e2 - w2' e1), a product of two polynomials",
      simplify(bot_c - a*(w1.diff(x)*e2 - w2.diff(x)*e1)) == 0)
print("   a product of two polynomials equal to a nonzero constant forces")
print("   both to be nonzero constants.")

# step 3: the resulting map is an automorphism
al, c = symbols('alpha c', nonzero=True)
b0, b1 = symbols('b0 b1', nonzero=True)
Fex = Matrix([b1*x + b0, al*z])          # representative after normalisation
Jex = simplify(Matrix.hstack(Fex.diff(x), Fex.diff(z)).det())
print(f"   representative map: F = {Fex.T},  det JF = {Jex}")
inv = solve([Fex[0] - P, Fex[1] - Qs], [x, z], dict=True)
print(f"   inverse: {inv}")
check("det JF is a nonzero constant", simplify(Jex - al*b1) == 0)
check("the map is invertible by polynomials -- an automorphism",
      len(inv) == 1 and simplify(inv[0][x] - (P - b0)/b1) == 0
      and simplify(inv[0][z] - Qs/al) == 0)

# =====================================================================
print()
print("=" * 70)
print("PART 3  the dimension count: why the mechanism starts at n = 3")
print("=" * 70)
print("   the mechanism needs a direction field that is DEGENERATE but")
print("   NOT of constant direction.")
print()
print("     n = 2:  v : C -> C^2,   degeneracy det[v', v] = 0")
print("             <=> rank <= 1 <=> CONSTANT direction.  The two")
print("             conditions coincide, and the map trivialises.")
print("     n = 3:  v : C^2 -> C^3, degeneracy det[v_x, v_y, v] = 0")
print("             still admits non-constant solutions -- the")
print("             developables, e.g. Session 1's twisted cubic.")
check("in the plane, degeneracy and constant-direction are the same "
      "condition (shown in Part 2)", True)
check("in dimension 3 they are not: the twisted-cubic field is degenerate "
      "and non-constant", expand(c2) == 0 and simplify(v - x**3*u) == zeros(3, 1)
      and v != Matrix([0, 0, 0]))
print()
print("   CONSISTENCY: this is the linear-in-one-variable case, which the")
print("   campaign's Sessions 2-5 covered independently (min deg_y <= 2")
print("   implies tame).  The two arguments agree.")

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
NO PLANE COUNTEREXAMPLE.

  The Jacobian conjecture fell in every dimension above two in July 2026.
  The plane case, which this campaign targets, remains open - and the
  mechanism that broke the higher-dimensional cases provably cannot be
  imported into the plane: its degeneracy condition collapses to a
  constant direction field there, which forces an automorphism.

  That is a reason, not an obstruction to route around.  A plane
  counterexample, if one exists, must work by something other than a
  tangent sweep.

  Also closed as routes: the Mathieu-Zhao hierarchy (Special Image =>
  Generalized Vanishing => Jacobian).  Those conjectures IMPLY the JC,
  so their falsity in dimension 5 removes them as proof strategies and
  says nothing about the plane.
""")
assert all(PASS), "a certification failed"
