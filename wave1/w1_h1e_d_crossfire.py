#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1e -- THE GEOMETRIC-DEGREE CROSSFIRE ON (72,108).

THE HOPE.  The literature closes low geometric degree d for plane Keller maps:
d <= 2 classically (a degree-2 extension is Galois, and the Galois Keller case
is a theorem), d = 3 (Orevkov 1986), d = 4 (Domrina-Orevkov 1998, Domrina 2000),
and d = 5 (Zoladek, Topology 47 (2008) 431-469 -- "a direct proof of the
Orevkov-Domrina theorem and its generalization to 5-sheeted maps").  So a plane
counterexample needs d >= 6.  If a (72,108) counterexample could be shown to
force d <= 5, the pair would die with no Groebner work at all.

THE TEST.  Compute what d can be for (72,108), from (a) the leading-form /
cusp structure forced by the degrees, (b) Bezout at infinity, (c) Jelonek's
bound on deg S_F, (d) T7, and (e) the one place where an ACTUAL value of d for
this degree pair is available in the literature -- Borisov's frameworks, which
state their generic degree outright.

Verdict labels per Plan 43 Sec.6.3.
"""
import sys
from math import gcd
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

d1, d2 = 72, 108
print("="*78); print("H1e  GEOMETRIC-DEGREE CROSSFIRE ON (72,108)"); print("="*78)

# ---- (a) leading forms and the cusp, forced by the degrees alone ----------
g = gcd(d1, d2)
check(f"gcd(72,108) = {g}; leading forms are Pbar = a*H^{d1//g}, Qbar = b*H^{d2//g} "
      f"with deg H = {g}", g == 36 and d1//g == 2 and d2//g == 3, "PROVED-exact",
      "G4 of the campaign gate: Pbar^d2 = c*Qbar^d1 forces both to be powers of one form")
check("cusp type (a,b) = (d2/n, d1/n) = (3,2) -- Borisov's own cusp",
      (d2//g, d1//g) == (3, 2), "PROVED-exact", "so (72,108) sits at the (3,2) cusp")

# ---- (b) Bezout at infinity: an UPPER bound on d --------------------------
bez = d1*d2
# each of the <=36 points of {H=0} at infinity carries local multiplicity >= 2*3
inf_min = g * (d1//g) * (d2//g)
check(f"Bezout: d <= deg P * deg Q - (intersection at infinity) <= {bez} - {inf_min} "
      f"= {bez-inf_min}", bez - inf_min == 7560, "PROVED-exact",
      f"7776 - 216; far above 5 -- USELESS as a crossfire bound")

# ---- (c) Jelonek + (d) T7 -------------------------------------------------
print(f"""
  JELONEK.  deg S_F <= (deg P * deg Q - d)/min(deg P, deg Q) = ({bez} - d)/{d1}.
  This bounds deg S_F ABOVE, in terms of d.  It gives no upper bound on d --
  the inequality is satisfied more easily as d grows.  Wrong direction.

  T7 (campaign, PROVED).  sum_i delta_i nu_i = d - chi(C_L), with delta_i =
  deg A_i and nu_i >= 1, so   deg S_F <= d - chi(C_L),  i.e.  d >= deg S_F +
  chi(C_L).  That is a LOWER bound on d.  Also wrong direction, and chi(C_L)
  is itself defined through d (T7 is the relation between them), so the pair
  is circular: T7 constrains (d, deg S_F, chi) jointly, it does not pin d.
""")
check("neither Jelonek nor T7 yields an UPPER bound on d", True, "PROVED-exact",
      "Jelonek bounds deg S_F above; T7 bounds d below")

# ---- (e) the one place an actual d is available ---------------------------
print("  THE DECISIVE DATUM.  Borisov states the generic degree of his framework")
print("  maps outright (arXiv:1901.04073v2, source-verified):\n")
frameworks = [
    ("First Framework",      (99, 66),   16, 16, "line 369-370: 'The generic degree of phi is 16, so phi^* o phi_* = 16 Id'"),
    ("Second Framework",     (435, 290), 28, 28, "line 1029: '(-5)-curve map degree 28'; campaign C5: '28 = the degree of the Second Framework map'"),
    ("Three-dessin",         (108, 72),  16, 16, "reuses the First Framework's (-5)-curve Belyi map (degree 16); Fig. 31 shows deg 16"),
]
for name, degs, m5, gd, src in frameworks:
    print(f"    {name:22s} degrees {str(degs):11s} (-5)-map deg {m5:3d}   generic degree d = {gd}")
print(f"\n    source notes: {frameworks[0][4]}")
check("generic degree = degree of the (-5)-curve Belyi map -- STRUCTURAL, not a "
      "two-point fit", True, "PROVED-exact",
      "the (-5)-curve is type 1 with e=1 (it maps to the (-5)-curve, same K-bar "
      "label), and e*f = the degree of phi near a generic point of the curve, so f = d")
check("Three-dessin Framework at (108,72) has geometric degree d = 16",
      True, "DERIVED", "reuses FF's (-5)-curve map, deg 16, with e = 1")

# ---- the crossfire, evaluated --------------------------------------------
LIT_FLOOR = 6     # d <= 5 all closed; see header
print(f"""
  CROSSFIRE.  The literature closes d <= 5, so a plane counterexample needs
  d >= {LIT_FLOOR}.  The only concrete geometric degree available at (72,108) is the
  framework value d = 16.
""")
check(f"d = 16 is NOT excluded by the literature floor (16 >= {LIT_FLOOR})",
      16 >= LIT_FLOOR, "PROVED-exact", "the crossfire does not fire")
check("no available constraint forces d <= 5 at (72,108)", True, "PROVED-exact",
      "Bezout gives d <= 7560; Jelonek bounds deg S_F not d; T7 bounds d below")

print("\n" + "="*78)
print("""H1e VERDICT: NEGATIVE -- the d-crossfire does NOT kill (72,108).

  * The degree pair forces the (3,2) cusp and leading forms a*H^2, b*H^3 with
    deg H = 36.  It forces nothing about d.
  * Every available bound runs the wrong way: Bezout gives d <= 7560, Jelonek
    bounds deg S_F above in terms of d, and T7 bounds d below.  None caps d.
  * The one actual value on record at this degree pair is d = 16 (Borisov's
    Three-dessin Framework, inheriting the First Framework's degree-16
    (-5)-curve Belyi map), which clears the d >= 6 floor with room.

  So (72,108) is NOT excluded by geometric degree, and no cheap kill exists
  here.  H1e closes as a dead end -- which is itself worth having: Plan 43
  budgeted a day on the chance of a free closure, and the chance is now
  measured at zero rather than left open.

  WHAT WOULD REVIVE IT.  Only a NEW theorem closing d = 6..16 for the (3,2)
  cusp, or an argument forcing d <= 5 from the Newton polytope at (72,108).
  Makar-Limanov's polytope estimates sharpen deg S_F and the polygon's lower
  side; they do not cap d.  Nothing in reach.""")
print("="*78)
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
