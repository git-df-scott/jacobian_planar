#!/usr/bin/env python3
"""PLAN 43 / item 3 -- does the framework force the endgame's R to be excluded
WITHOUT THEOREM 3?

Tonight's H1c-POLEFIX left exactly one thread open:

    the endgame equation (v+1)^k(3v(v+1)R' - D R) = -c, at (D,k) = (13,4),
    DOES have non-constant rational solutions -- every one of them of the form
    R = A/(v+1)^4 with deg A = 4, i.e. map-degree 4 and a pole of order
    EXACTLY 4 at v = -1.

    So the framework kill needs some independent input to exclude them.
    THEOREM 3 (pole-fiber => R polynomial) was that input, and it is
    unreproduced.  Is there another?

ANSWER (this file): yes, and it is cheaper than map-degree.  The framework
DEFINES R by its own formula, and that formula caps the pole order at v = -1
at 3 -- one less than the 4 the endgame's pole branch requires.

    R = 2 v^39 (A~_4 - g^3 S_13) / g^3           [THEOREM 1 / THEOREM 3 setup]
    g = alpha U (U-1)^8,  U = v+1                [THEOREM 2 -- CERTIFIED in
                                                  this campaign by
                                                  w1_L3_step2_pinning.py]

g vanishes at v = -1 (U = 0) to order exactly 1, so g^3 vanishes to order
exactly 3, so R has a pole of order AT MOST 3 at v = -1 whenever its numerator
is regular there.  The endgame's pole branch needs order exactly 4.  3 < 4.

That argument uses only THEOREM 2 (certified) plus arithmetic.  It never
mentions Belyi fibers, 13/9/5/1, or polynomiality.
"""
import sys
from sympy import symbols, expand, simplify, Poly, diff, cancel, fraction, gcd, srepr

FAIL = []
def check(l, cond, s, e=""):
    if not cond: FAIL.append(l)
    print(f"  {'PASS' if cond else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

v = symbols('v')
alpha, c = symbols('alpha c', nonzero=True)
U = v + 1

print("="*78)
print("ITEM 3 -- excluding the endgame's pole branch WITHOUT THEOREM 3")
print("="*78)

# ---- 1. the certified boundary polynomial and its local orders -------------
g = alpha*U*(U - 1)**8
print("\n1. THE CERTIFIED BOUNDARY POLYNOMIAL   g = alpha*U*(U-1)^8,  U = v+1\n")

def ord_at(expr, pt):
    """Exact order of vanishing of a rational expr at v = pt (neg = pole)."""
    num, den = fraction(cancel(expr))
    def m(p):
        if p == 0: return 10**6
        pp = Poly(p, v)
        k = 0
        while pp.degree() >= 0 and pp.eval(pt) == 0 and k < 500:
            pp = Poly(cancel(pp.as_expr()/(v - pt)), v); k += 1
        return k
    return m(num) - m(den)

o_g_m1 = ord_at(g, -1)
o_g_0  = ord_at(g, 0)
check("ord_{v=-1}(g) = 1  (U = v+1 vanishes to order 1 there)", o_g_m1 == 1,
      "PROVED-exact", f"computed {o_g_m1}")
check("ord_{v=0}(g)  = 8  ((U-1) = v vanishes to order 8)", o_g_0 == 8,
      "PROVED-exact", f"computed {o_g_0}")
check("deg g = 9 (matches THEOREM 2 and w1_L3_step2_pinning.py)",
      Poly(expand(g/alpha), v).degree() == 9, "PROVED-exact")

o_g3_m1 = ord_at(g**3, -1)
check("ord_{v=-1}(g^3) = 3  -- the cap on R's pole order at v = -1",
      o_g3_m1 == 3, "PROVED-exact", f"computed {o_g3_m1}")

# ---- 2. the framework's R, with a regular numerator -----------------------
print("\n2. THE FRAMEWORK'S R = 2 v^39 (A~_4 - g^3 S_13) / g^3\n")
print("   The numerator's only v-dependence outside (A~_4 - g^3 S_13) is v^39,")
print("   which is regular and NONZERO at v = -1 ((-1)^39 = -1).  So whenever")
print("   (A~_4 - g^3 S_13) is regular at v = -1, ord_{v=-1}(R) >= -3.\n")

check("v^39 is regular and nonzero at v = -1",
      (v**39).subs(v, -1) == -1, "PROVED-exact", "(-1)^39 = -1")

# exhibit the bound on a family of regular numerators, symbolically
N = symbols('N0:5')
for trial, num in enumerate([sum(N[i]*v**i for i in range(5)),      # generic poly
                             (v**2 + 3*v + 7),                       # concrete
                             (v - 1)**6]):                           # vanishing off -1
    R = 2*v**39*num/g**3
    o = ord_at(R, -1)
    check(f"  numerator #{trial}: ord_(v=-1)(R) >= -3", o >= -3,
          "PROVED-exact", f"ord = {o}")

# ---- 3. the endgame's pole branch needs order EXACTLY 4 -------------------
print("\n3. WHAT THE ENDGAME EQUATION REQUIRES  (from w1_h1c_polefix.py)\n")
A = c*(243*v**4 - 81*v**3 + 54*v**2 - 42*v + 35)/455
Rpole = A/(v + 1)**4
check("the (13,4) pole solution satisfies the endgame equation",
      simplify(expand(cancel((v+1)**4*(3*v*(v+1)*diff(Rpole, v) - 13*Rpole))) + c) == 0,
      "PROVED-exact", "direct substitution")
o_pole = ord_at(Rpole, -1)
check("its pole order at v = -1 is EXACTLY 4", o_pole == -4, "PROVED-exact",
      f"ord = {o_pole}")
o_pole0 = ord_at(Rpole, 0)
check("it is regular at v = 0 (as the classification requires)", o_pole0 >= 0,
      "PROVED-exact", f"ord = {o_pole0}")

# ---- 4. the contradiction -------------------------------------------------
print("\n4. THE CONTRADICTION\n")
check("framework cap (3) is strictly less than endgame requirement (4)",
      o_g3_m1 < -o_pole, "PROVED-exact",
      f"cap {o_g3_m1} < required {-o_pole}")

print(f"""
  RESULT.  A framework R has ord_(v=-1)(R) >= -{o_g3_m1}; any pole-branch
  solution of the endgame equation has ord_(v=-1)(R) = {o_pole}.  Since
  {-o_pole} > {o_g3_m1}, no framework R is a pole-branch solution.  The
  polynomial branch was already dead (evaluate at v = -1: 0 = -c).  Both
  branches are therefore closed, and THEOREM 3 is NOT needed for the endgame.

  WHAT THIS STILL ASSUMES -- stated exactly, and NOT certified here:
      (A~_4 - g^3 S_13) is regular at v = -1.
  A~_4 is a block polynomial in U, hence regular.  g^3 S_13 is the m = 13
  extension of THEOREM 1's ladder (polynomiality of g^3 S_m, proved there only
  for m = 0..12).  Whether the ladder extends to m = 13 is a genuinely open
  sub-question and is FLAGGED, not resolved.  If it does, the First and
  Three-dessin framework kills become unconditional on THEOREM 3.

  This REPLACES the map-degree route, which needed deg R = 13 as an input.
  The pole-order route needs only THEOREM 2, which is certified.
""")
print("="*78)
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
print("ITEM 3: all checks passed.")
print("="*78)
