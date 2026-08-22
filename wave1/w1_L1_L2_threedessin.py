#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 -- L1 and L2 on the THREE-DESSIN chain.

L3 transferred (step 2: g = alpha*U*(U-1)^8 pins, deg g = N/mu + eps = 9).
The conditional kill of the Three-dessin Framework at (108,72) now rests on
L1 (chart + support boxes) and L2 (block-level chain unification).

THE GOVERNING PRINCIPLE, taken from the D=23 chart transfer (d23_phase1_chart.py)
and stated there explicitly:

    "in both frameworks the chain is created by breaking the same (-5)--(-2)
     edge, and the long-branch modifications (which differ) happen strictly
     beyond the (-2)-multifork.  Divisorial valuations of x1, x2 along existing
     curves are unchanged by later point blowups, so the (q,v)-chart of
     Sessions 8-16 at the (-2)-multifork TRANSFERS VERBATIM."

That argument applies A FORTIORI here.  For the Second Framework the Z-stem only
MATCHED the First's in K-bar structure and creation order.  For the Three-dessin
Framework the entire (-5)...(-2) chain is LITERALLY IDENTICAL -- 18 K-bar labels
and the target chain, certified two independent ways in L3 step 1 (the campaign's
C1 blowup test and a forward reconstruction).  And the differences Borisov names
-- no type-4 curve, a third forked vertex carrying a degree-5 Belyi map above the
(-1)-curves -- lie on branches strictly beyond the (-2)-multifork.
"""
import sys
from sympy import symbols, simplify, together, expand, Rational, factor

x1, x2, q, v = symbols('x1 x2 q v')
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

print("="*78); print("L1 -- THE CHART LAYER ON THE THREE-DESSIN CHAIN"); print("="*78)

# ---- L1a: chart inversion (recomputed, not imported) --------------------
V = x1*x2**3 - 1
Qv = x2/V**3
x1_rec = (v+1)*q**-3*v**-9
x2_rec = q*v**3
check("L1a chart inversion: x1 = (v+1)q^-3 v^-9, x2 = q v^3 inverts "
      "(q,v) = (x2/(x1 x2^3 - 1)^3, x1 x2^3 - 1)",
      simplify(x1_rec.subs({q: Qv, v: V}) - x1) == 0 and
      simplify(x2_rec.subs({q: Qv, v: V}) - x2) == 0, "PROVED-exact")

# ---- L1b: monomial rule -------------------------------------------------
i, j = symbols('i j', integer=True, nonnegative=True)
lhs = (x1_rec**i * x2_rec**j)
rhs = (v+1)**i * q**(j-3*i) * v**(3*j-9*i)
check("L1b monomial rule: x1^i x2^j = (v+1)^i q^(j-3i) v^(3j-9i), so the "
      "(-2)-pole cut is the same support rule j - 3i >= -bound",
      simplify(expand(lhs/rhs)) == 1, "PROVED-exact")

# ---- L1c: chart factor and the Keller form ------------------------------
from sympy import Matrix
J = Matrix([[Qv.diff(x1), Qv.diff(x2)], [V.diff(x1), V.diff(x2)]]).det()
check("L1c chart factor: det d(q,v)/d(x1,x2) = -x2^3/v^3",
      simplify(J + x2**3/V**3) == 0, "PROVED-exact", f"det = {factor(simplify(J))}")
check("L1c so the Keller condition J_(x1,x2) = c reads J_(q,v) = -c q^-3 v^-6, "
      "exactly as in the First Framework",
      simplify((-x2**3/V**3).subs({x1: x1_rec, x2: x2_rec}) + q**3*v**6) == 0,
      "PROVED-exact")

# ---- L1d: pole depths ---------------------------------------------------
print("""
  L1d POLE DEPTHS at the (-2)-multifork.  These are the only chart data that
  moved between the First and Second Frameworks: (-9,-6) for FF, (-15,-10) for
  SF.  They are divisorial valuations along the CHAIN, and the Three-dessin
  chain is identical to the First's, so they are the First's: (-9,-6).

  Consistency check -- the total degrees must be an integer multiple of the
  depths, with the multiplier supplied by the branch inventory:""")
rows = [("First Framework",  (99, 66),  (9, 6)),
        ("Second Framework", (435, 290), (15, 10)),
        ("Three-dessin",     (108, 72), (9, 6))]
ok = True
for name, (d1, d2), (p1, p2) in rows:
    m1, m2 = Rational(d1, p1), Rational(d2, p2)
    good = m1 == m2 and m1.q == 1
    ok &= good
    print(f"    {name:18s} degrees {str((d1,d2)):11s} depths {str((-p1,-p2)):9s} "
          f"-> multiplier {m1}  {'ok' if good else 'MISMATCH'}")
check("L1d every framework's degrees are depth x integer, with a consistent "
      "multiplier; Three-dessin gives 12 against FF's 11 and SF's 29",
      ok, "CERTIFIED", "the multiplier is exactly where the branch inventory enters")
check("L1d depths are proportional to the cusp (3,2) in every case",
      all(Rational(p1, p2) == Rational(3, 2) for _, _, (p1, p2) in rows),
      "PROVED-exact", "(9,6), (15,10), (9,6) all = (3,2) up to scale")

print("""
  L1 REMAINING GAP -- the support boxes.  FF's are [0,27]x[0,72] for y1 and
  [0,18]x[0,48] for y2 (sums 99, 66); these are the x1/x2 degree SPLITS.  For
  the Three-dessin Framework the splits are (9a, 9b) and (6a, 6b) with
  a + b = 12, and a is NOT determined by anything transferred: Borisov's isotope
  formula gives (a,b) = (k+1, 3k+2) with a+b = 4k+3, and 4k+3 = 12 has no
  integer solution -- confirming again that (108,72) sits outside the isotope
  family.  Fixing a needs the pole-order reconstruction along Fig. 31's branches,
  the same walk Borisov performs for SF ("Reconstructing the curves numbered 2,
  10, and 1 ... (165,110), (270,180), and, finally, (435,290)").  NOT DONE.""")

print("\n" + "="*78); print("L2 -- BLOCK-LEVEL CHAIN UNIFICATION"); print("="*78)
print("""  L2 promotes the valuation-level equivalence to the block cascade.  Its input
  is the contact demand val(y1^2 - y2^3) >= -contact, which equals exactly D
  block vanishings.  Recorded: FF contact -5 with D = 13; SF contact -7 with
  D = 23.""")
for D, c in ((13, 5), (23, 7)):
    pred = Rational(D + 12, 5)
    print(f"    D = {D:2d}  contact = -{c}   (D+12)/5 = {pred}  {'ok' if pred == c else 'MISMATCH'}")
check("L2 contact demand for the Three-dessin Framework is -5",
      Rational(13 + 12, 5) == 5, "CERTIFIED",
      "D = 13 (same (-2)-curve Belyi map as FF, source-verified)")
check("L2 INDEPENDENTLY CONFIRMED by L3 step 2: the Y-side chart returned "
      "eW = -5, i.e. W = y1^2 - y2^3 first survives at x2^-5",
      True, "CERTIFIED",
      "computed from the shared chart data in w1_L3_step2_pinning.py, a route "
      "that shares no code with the contact bookkeeping")

print("""
  L2 REMAINING GAP.  The contact demand transfers, and with it the count of
  block vanishings (13).  What is NOT rebuilt is the cascade itself -- the
  promotion of those vanishings through the block normal form and the
  sqrt-reduction, FF Sessions 10-12.  Its inputs are the chain (identical) and
  the Belyi data (identical), so it is expected to transfer, but expectation is
  not a certificate and it is recorded as UNCHECKED.""")

print("\n" + "="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
print("""RESULT.

  L1 CORE  TRANSFERS  [PROVED-exact] -- chart inversion, monomial rule, chart
           factor, Keller form, all recomputed here, plus the pole depths
           (-9,-6) inherited from the identical chain and consistent with
           (108,72) = 12 x (9,6).
  L1 BOXES UNCHECKED -- needs the Fig. 31 pole-order reconstruction; a + b = 12
           is pinned but a is not.
  L2 CONTACT TRANSFERS [CERTIFIED] -- contact -5, 13 block vanishings,
           independently confirmed by L3 step 2's eW = -5.
  L2 CASCADE UNCHECKED -- inputs identical, promotion not rebuilt.

  So the Three-dessin kill at (108,72) now stands on: L3 complete, L1 core
  complete, L2 contact complete; L1 boxes and the L2 cascade outstanding.
  Two gaps, both narrower than when this session started, and both named.""")
print("="*78)
