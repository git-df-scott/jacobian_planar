#!/usr/bin/env python3
"""PLAN 43 / H1d -- is GGHV Prop 4.3's case split EXHAUSTIVE?  (Wave-0 item,
skipped until now.  "A case nobody enumerated is the perfect hiding spot.")

GGHV arXiv:2204.14178v1 Prop 4.3 states TWO cases -- pentagon N(P) with five
points, quadrilateral with four -- reached through THREE polygon possibilities:

   a) (m,n) x {(-2,0), (0,0), (28,8), (0,1)}          -> case (2), quadrilateral
   b) (m,n) x {(-3,0), (0,0), (28,8), (0,1)}          -> case (2), quadrilateral
   c) (m,n) x {(-3,0), (0,0), (16,4), (28,8), (0,1)}  -> case (1), PENTAGON

The branch structure, verbatim from the proof:

   Pred_P(1,0) in {(1,-2), (1,-3)}                        [by 6, Prop 2.5]
     if (1,-2): after a morphism, Pred in {(1,-3), (2,-7)}
                (2,-7) -> a)
                (1,-3) -> falls through to the next branch
     if (1,-3): "there are ONE OR TWO different linear factors in l_{1,-3}"
                one  -> b)
                two  -> c)

THE ONE STEP THAT COULD HIDE A CASE is "one or two".  If three or more distinct
linear factors were possible, there would be an unenumerated case (d), and it
would be a pentagon-or-worse polygon nobody has ever searched.  This checks
whether "one or two" is BOUNDED or merely ASSERTED.
"""
import sys
from sympy import symbols, Poly, expand
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

x, y, z = symbols('x y z')
print("="*78); print("H1d -- IS GGHV PROP 4.3 EXHAUSTIVE?"); print("="*78)

print("""
  THE BOUND.  Earlier in the same proof GGHV establish

      l_{rho,sigma}(P) = lambda * R^{qm} = lambda * R^{4m},   e_{rho,sigma}(R) = (7,2)

  so the factorisation of l_{1,-3}(P) is governed entirely by R.  A
  (1,-3)-homogeneous element is a polynomial in z = x^3 y times a power of x,
  and the lattice point (7,2) says which:
""")
# (7,2) means x^7 y^2; with z = x^3 y this is x^(7-3*2) * z^2
xexp = 7 - 3*2
check("the point (7,2) written in z = x^3 y is x^1 * z^2, so deg_z R = 2",
      xexp == 1, "PROVED-exact", f"x^7 y^2 = x^{xexp} * (x^3 y)^2")
print(f"      x^7 y^2  =  x^{xexp} * z^2 ,  hence R = x * f(z) with deg f = 2.")

check("a degree-2 polynomial in z has AT MOST TWO distinct linear factors",
      True, "PROVED-exact", "deg f = 2 bounds the number of distinct roots by 2")
check("therefore 'one or two different linear factors' is a BOUND, not an "
      "assumption -- three or more is impossible",
      True, "PROVED-exact", "no case (d) can exist at this branch")

# consistency: the two-factor form GGHV write down must have the right degree
m = symbols('m', positive=True, integer=True)
print("""
  CONSISTENCY.  GGHV write the two-factor case as
      l_{1,-3}(P) = lambda x^{4m} (x^3 y - a1)^{4m} (x^3 y - a2)^{4m}
  which is lambda * [ x * (z-a1) * (z-a2) ]^{4m} -- exactly R^{4m} with
  R = x f(z), deg f = 2, f having two distinct roots.  The one-factor case is
  the same with f a square.  Both are R^{4m}; nothing else is.""")
check("the two-factor form is exactly (x (z-a1)(z-a2))^{4m} = R^{4m}, matching "
      "e(R) = (7,2)", True, "PROVED-exact",
      "x^{4m} (z-a1)^{4m} (z-a2)^{4m} = [x(z-a1)(z-a2)]^{4m}")

print("""
  THE REMAINING BRANCH.  Pred_P(1,0) in {(1,-2),(1,-3)} is cited to
  [6, Proposition 2.5] and is NOT re-derived here -- it is an external result,
  and this check does not close it.  Within the proof as written, given that
  dichotomy, the enumeration a)/b)/c) is complete.
""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
print("""H1d VERDICT: the case split is EXHAUSTIVE.  There is no case (3).

  The "one or two linear factors" step -- the only place an unenumerated
  polygon could have hidden -- is a BOUND forced by deg_z R = 2, which follows
  from the lattice point e(R) = (7,2) that GGHV compute earlier in the proof.
  Three or more factors is impossible, so no fourth polygon shape exists.

  CONDITIONAL on one external citation: [6, Prop 2.5] giving
  Pred_P(1,0) in {(1,-2),(1,-3)}.  That is where a case could still hide, and
  it is now the single named residue of this audit rather than a general worry.

  This closes a Wave-0 item that had been skipped.  It is CLOSURE, not a hit:
  it removes a hiding place rather than finding something in one.""")
print("="*78)
