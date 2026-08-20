#!/usr/bin/env python3
"""PLAN 43 -- KILL OR CONFIRM THEOREM 3.

THEOREM 3, verbatim, from `Sessions 1-18 status reports` line 1062:

    R = 2 v^39 (A~_4 - g^3 S_13)/g^3 has poles confined to {v = 0, v = -1};
    the Belyi-13 fibers have 13/9/5/1 points; only the 1-point fiber fits a
    <=2-point pole set, so the pole fiber is the order-13 point at v = infinity
    and R is a DEGREE-13 POLYNOMIAL.  The forced divisibilities close the v = 0
    pole exactly (boundary partition sigma_1^13, v-order 0).

VERDICT: **CONFIRMED** -- the conclusion is true.  But the recorded PROOF has a
real gap, and the repair is shorter than the original: a divisibility count
replaces the fiber count entirely.

THE GAP.  The fiber step fixes the pole divisor's MULTIPLICITY (13) but not its
LOCATION.  The next sentence closes v = 0.  Nothing in the quoted text closes
v = -1.  Section 4 below exhibits an explicit R satisfying EVERY constraint the
quoted argument imposes which is NOT a polynomial -- so the quoted chain does
not entail its own conclusion.

THE PROOF THAT DOES WORK.  Session 11 defines
        R(v) = v^39 * W~_-5(U) / g(U)^6,      U = v + 1,
with W~_-5 a block -- hence a polynomial -- of degree 6*deg(g) - 26 = 28, and
THEOREM 2 (certified here by w1_L3_step2_pinning.py) gives g = alpha U (U-1)^8.
Since v^39 = (U-1)^39 and g^6 = alpha^6 U^6 (U-1)^48,

        R = W~_-5(U) / ( alpha^6 * U^6 * (U-1)^9 ).

Let U^a (U-1)^b be the gcd of W~_-5 with the denominator, so a <= 6, b <= 9.
After cancelling, R has numerator degree 28 - a - b and denominator degree
15 - a - b, so its degree AS A MAP is 28 - a - b.  The framework's
13-realization demands map-degree 13, so a + b = 15.  With a <= 6 and b <= 9
that forces a = 6 and b = 9 exactly: the denominator cancels COMPLETELY.
Hence R is a polynomial, of degree 28 - 15 = 13.  QED.

No Belyi passport, no fiber counting, no divisibility argument at v = 0.
"""
import sys
from sympy import (symbols, Poly, expand, cancel, fraction, simplify, gcd,
                   degree, div, factor_list)

FAIL = []
def check(label, cond, status, extra=""):
    if not cond: FAIL.append(label)
    print(f"  {'PASS' if cond else 'FAIL'}  {label}   <{status}>"
          + (f"   [{extra}]" if extra else ""), flush=True)

U, v = symbols('U v')

def mult(poly_expr, pt, var):
    """Exact multiplicity of (var - pt) in a polynomial."""
    p = Poly(poly_expr, var)
    k = 0
    while k < 500:
        q, r = div(p, Poly(var - pt, var))
        if r.as_expr() != 0:
            return k
        p = q; k += 1
    return k

def mapdeg(expr, var):
    n, d = fraction(cancel(expr))
    return max(Poly(n, var).degree(), Poly(d, var).degree())

print("=" * 78)
print("THEOREM 3 -- KILL OR CONFIRM")
print("=" * 78)

# ------------------------------------------------------------- 1. inputs --
print("\n1. INPUTS, each with provenance and each verified, not asserted\n")
gU = U*(U - 1)**8                               # g / alpha
DEG_G = Poly(gU, U).degree()
check("THEOREM 2's g = alpha*U*(U-1)^8 has degree 9 in U", DEG_G == 9,
      "CERTIFIED (w1_L3_step2_pinning.py)", f"computed deg = {DEG_G}")
check("  g vanishes at U = 0 to order exactly 1", mult(gU, 0, U) == 1,
      "PROVED-exact", f"multiplicity {mult(gU, 0, U)}")
check("  g vanishes at U = 1 to order exactly 8", mult(gU, 1, U) == 8,
      "PROVED-exact", f"multiplicity {mult(gU, 1, U)}")

DEG_W = 6*DEG_G - 26
check("Session 11's ledger deg W~_-5 = 6*deg(g) - 26 evaluates to 28",
      DEG_W == 28, "PROVED-exact", f"6*{DEG_G} - 26 = {DEG_W}")

# --------------------------------------------- 2. the U-coordinate form ---
print("\n2. R IN THE U-COORDINATE, computed rather than quoted\n")
red = cancel((U - 1)**39 / (gU**6))             # v^39 / (g/alpha)^6
nn, dd = fraction(red)
check("v^39 / (g/alpha)^6 reduces to 1 / (U^6 (U-1)^9)",
      simplify(red - 1/(U**6*(U - 1)**9)) == 0, "PROVED-exact",
      f"reduced to {red}")
DEN = expand(U**6*(U - 1)**9)
A_MAX = mult(DEN, 0, U)
B_MAX = mult(DEN, 1, U)
check("denominator's multiplicity at U = 0 is 6 (bounds the v = -1 pole)",
      A_MAX == 6, "PROVED-exact", f"computed {A_MAX}")
check("denominator's multiplicity at U = 1 is 9 (bounds the v =  0 pole)",
      B_MAX == 9, "PROVED-exact", f"computed {B_MAX}")
roots = sorted({r for r in Poly(DEN, U).all_roots()})
check("the denominator has NO roots other than U = 0 and U = 1",
      roots == [0, 1], "PROVED-exact", f"roots = {roots}")
check("so R's finite poles lie only at v = -1 and v = 0",
      roots == [0, 1] and Poly(DEN, U).degree() == A_MAX + B_MAX,
      "PROVED-exact", f"deg den = {Poly(DEN, U).degree()} = {A_MAX}+{B_MAX}")

# ------------------------------------------------- 3. the divisibility ----
print("\n3. THE PROOF -- a divisibility count, run over every possible (a,b)\n")
DEG_R = 13          # the framework's 13-realization (Session 11), not THEOREM 3
print(f"   Write gcd(W~_-5, U^6 (U-1)^9) = U^a (U-1)^b, so 0<=a<=6, 0<=b<=9.")
print(f"   After cancelling, map-degree(R) = {DEG_W} - a - b.")
print(f"   The 13-realization demands map-degree(R) = {DEG_R}.\n")
sols = [(a, b) for a in range(A_MAX + 1) for b in range(B_MAX + 1)
        if DEG_W - a - b == DEG_R]
check("exactly ONE (a,b) in the allowed box gives map-degree 13",
      len(sols) == 1, "PROVED-exact", f"solutions {sols}")
check("and it is (a,b) = (6,9) -- the denominator cancels COMPLETELY",
      sols == [(A_MAX, B_MAX)], "PROVED-exact",
      f"a = {sols[0][0]} = a_max, b = {sols[0][1]} = b_max")
check("=> R has no finite pole => R IS A POLYNOMIAL",
      sols[0] == (A_MAX, B_MAX), "PROVED-exact",
      "full cancellation leaves denominator 1")
check("=> deg R = 28 - 15 = 13", DEG_W - A_MAX - B_MAX == DEG_R,
      "PROVED-exact", f"{DEG_W} - {A_MAX} - {B_MAX} = {DEG_W-A_MAX-B_MAX}")

# concrete instance: build an actual W of degree 28 divisible by U^6(U-1)^9
Wc = expand(U**6*(U - 1)**9*(U**13 + 3*U**7 - 5*U + 2))
check("  concrete witness: a degree-28 W~ divisible by U^6(U-1)^9 exists",
      Poly(Wc, U).degree() == DEG_W, "PROVED-exact",
      f"deg = {Poly(Wc, U).degree()}")
Rc = cancel(Wc/DEN)
check("  and the resulting R is a polynomial of degree exactly 13",
      fraction(Rc)[1] == 1 and Poly(fraction(Rc)[0], U).degree() == DEG_R,
      "PROVED-exact", f"den = {fraction(Rc)[1]}, deg = {Poly(fraction(Rc)[0],U).degree()}")

# ------------------------------------------------------- 4. THE GAP -------
print("\n4. THE GAP IN THE RECORDED PROOF -- shown by an explicit witness\n")
FIBERS = [13, 9, 5, 1]
rh = sum(13 - f for f in FIBERS)
check("the quoted passport 13/9/5/1 is Riemann-Hurwitz consistent at degree 13",
      rh == 2*13 - 2, "PROVED-exact", f"sum(13-f) = {rh}, 2*13-2 = {2*13-2}")
small = [f for f in FIBERS if f <= 3]
check("among 13/9/5/1 only the 1-point fiber has <=3 points (quoted step "
      "reproduced)", small == [1], "PROVED-exact", f"{small}")

# THE WITNESS: satisfies every constraint the quoted argument states, yet is
# not a polynomial.  Built and tested, not asserted.
Rw = 1/(v + 1)**13
w_mapdeg = mapdeg(Rw, v)
w_pole_m1 = mult(fraction(cancel(Rw))[1], -1, v)
w_pole_0 = mult(fraction(cancel(Rw))[1], 0, v)
w_is_poly = (fraction(cancel(Rw))[1] == 1)
print(f"   witness R = 1/(v+1)^13")
check("  witness: finite poles confined to {v=0, v=-1}  (quoted premise 1)",
      sorted({r for r in Poly(fraction(cancel(Rw))[1], v).all_roots()}) == [-1],
      "PROVED-exact", "only v = -1")
check("  witness: pole fiber is a SINGLE point of multiplicity 13 "
      "(quoted premise 2 -- the 1-point fiber)",
      w_mapdeg == 13 and w_pole_m1 == 13, "PROVED-exact",
      f"map-degree {w_mapdeg}, pole order at v=-1 is {w_pole_m1}")
check("  witness: v = 0 is NOT a pole (quoted premise 3, the divisibilities)",
      w_pole_0 == 0, "PROVED-exact", f"pole order at v=0 is {w_pole_0}")
check("  witness is NOT a polynomial -- so the quoted premises do NOT entail "
      "the quoted conclusion", not w_is_poly, "GAP-CONFIRMED",
      "all three quoted premises hold, conclusion fails")
check("  the divisibility count REJECTS the witness: it needs a=13 at U=0, "
      "but a <= 6", 13 > A_MAX, "PROVED-exact", f"13 > {A_MAX}")

# --------------------------------------------------- 5. cross-checks ------
print("\n5. CROSS-CHECKS AGAINST THE CAMPAIGN'S OWN DATA\n")
check("the near-miss R = n3 has degree 0, not 13 -- so it is a boundary point, "
      "exactly as Session 11 records", 0 != DEG_R, "CONSISTENT", "0 != 13")
Rp = (243*v**4 - 81*v**3 + 54*v**2 - 42*v + 35)/(455*(v + 1)**4)
check("the endgame pole-branch solution has map-degree 4, not 13",
      mapdeg(Rp, v) == 4, "PROVED-exact", f"map-degree {mapdeg(Rp,v)}")
check("  so THEOREM 3 excludes it independently of the pole-order bound",
      mapdeg(Rp, v) != DEG_R, "PROVED-exact", "4 != 13")

print("\n" + "=" * 78)
print("VERDICT: THEOREM 3 -- CONFIRMED (conclusion), PROOF REPAIRED (method).")
print("""
  CONFIRMED: R is a polynomial of degree exactly 13.

  The recorded proof does NOT establish it.  Its fiber step fixes the pole
  divisor's multiplicity but not its location; the text closes v = 0 and leaves
  v = -1 open, and 1/(v+1)^13 satisfies every premise it states while failing
  its conclusion.  That witness is built and tested in section 4.

  The repair is shorter and uses strictly less:
      R = W~_-5(U) / (alpha^6 U^6 (U-1)^9),  deg W~_-5 = 28
      gcd(W~_-5, U^6(U-1)^9) = U^a (U-1)^b,  a <= 6, b <= 9
      map-degree(R) = 28 - a - b = 13  =>  a + b = 15  =>  (a,b) = (6,9)
      => the denominator cancels completely => R is a polynomial of degree 13.

  The Belyi passport 13/9/5/1 is reproduced and shown Riemann-Hurwitz
  consistent, but it is NOT load-bearing.  Neither is the v = 0 divisibility
  argument.

  DEPENDENCIES:
    g = alpha U (U-1)^8   THEOREM 2 -- CERTIFIED (w1_L3_step2_pinning.py)
    deg W~_-5 = 28        Session 11 ledger, arithmetic from deg g = 9
    W~_-5 polynomial      by construction: it is a block of the expansion
    deg R = 13            the framework's own 13-realization, NOT THEOREM 3

  The sub-question flagged earlier -- is g^3 S_13 regular at v = -1 -- DISSOLVES:
  the W~_-5 form never constructs g^3 S_13.

  CONSEQUENCE.  Both uncertified legs of the Sessions 16-18 First Framework
  emptiness theorem are now discharged: THEOREM 2 certified, THEOREM 3 confirmed.
  Every (72,108) statement that inherited CONDITIONAL(R-poly) can be re-labelled,
  and the Three-dessin (108,72) kill loses its last conditionality.
""")
print("=" * 78)
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
print("all checks passed")
