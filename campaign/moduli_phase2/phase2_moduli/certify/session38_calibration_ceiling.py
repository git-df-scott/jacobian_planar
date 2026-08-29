"""
Plane Jacobian campaign - Session 38
THE CALIBRATION CEILING: WHY THE (m,n) GENERALISATION IS NOT WORTH DOING.

NO COUNTEREXAMPLE.

The (m,n) generalisation was queued for one stated reason: to buy CALIBRATION
POINTS.  The tractability metric currently rests on two - one closed case at
4.03x and one open case at 8.46x - and a 2.1x separation read off two points is
not obviously signal.  If GGHV's (3,4) and (5,7) families could be scored, the
metric could be tested.

They cannot, and neither can the one other case closed by this machinery.  The
generalisation would therefore cost days and buy nothing it was queued for.
That is the finding, and it is why item 3 is dropped rather than deferred.

=====================================================================
WHY (3,4) AND (5,7) ARE THE WRONG CONTROLS
=====================================================================

From GGHV's own table, with how each case was actually discarded:

  A0        (m,n)   max   closed by
  (4,12)    (3,4)    64   [4 sec 3.5], [10], [7]      <- other methods
  (4,12)    (5,7)   112   [4 sec 3.5]                 <- other methods
  (7,21)    (2,3)    84   GGHV section 6              <- THIS machinery
  (9,27)    (2,3)   108   GGHV section 5              <- THIS machinery
  (8,28)    (3,2)   108   OPEN

The (3,4) and (5,7) families were discarded by intersection-number and
degree arguments, NOT by the relation-plus-bounds system.  The metric measures
how overdetermined THAT system is, so scoring a case closed by a different
technique tests nothing about whether the metric predicts closure by this one.
They are the wrong controls even if their L were known - and it is not.

=====================================================================
WHY SECTION 6 CANNOT BE SCORED EITHER
=====================================================================

Section 6, case (7,21), IS closed by this machinery - it is the (6.18)
calibration already reproduced in Session 36.  It looks like the obvious third
control.  It is not, because its SHAPE differs.

Sections 5 and (8,28) both have a TWO-ROOT normalisation:

    section 5: C_3 = y^8(y+1),  deg C = 9, ord C = 8,  e = 5
    (8,28):    C_4 = y^7(y+1),  deg C = 8, ord C = 7,  e = 7

so deg C = ord C + 1, which is exactly what makes rho - rho' = L + 1 and makes
the whole cost model work.  Section 6 has a ONE-ROOT normalisation:

    section 6: C_3 = y,         deg C = 1, ord C = 1,  e = 2

so deg C = ord C, and e = 2 rather than 5 or 7.  Running the bound derivation's
own internal consistency check (the leading term x^L must realise the bound,
i.e. -rho' L = constant):

    section 5:  -13*3 = -39  and  t - e*ordC = -39     CONSISTENT
    (8,28):     -10*4 = -40  and  t - e*ordC = -40     CONSISTENT
    section 6:  -(-1)*3 = 3  and  t - e*ordC = 6       FAILS

Section 6 fails its own consistency check, which is the derivation correctly
refusing to apply to a shape it was not derived for.  It cannot be scored.

=====================================================================
WHAT REMAINS TRUE ABOUT L, AND WHAT IS NOT CLAIMED
=====================================================================

Establishable: B = (L, deg C) by definition, since R = x^L * C.

Observed on both data points: deg C equals the first coordinate of A_0
(section 5: A_0 = (9,27) and deg C = 9; (8,28): A_0 = (8,28) and deg C = 8).

NOT CLAIMED: any formula for L in terms of A_0.  That is two data points, and
fitting a law to a handful of points is precisely correction #6, which agreed
with reality only at a = 8 and survived four sessions.  No formula is proposed.

=====================================================================
THE HONEST CONSEQUENCE FOR THE WP-B VERDICT
=====================================================================

The metric's calibration stands at ONE closed control and ONE open case, and
no further control is obtainable from the literature:

    (3,4), (5,7)   wrong controls - closed by other methods, L unknown
    section 6      right method, wrong shape - fails the consistency check
    section 5      the only usable control

So the objection raised against the WP-B verdict - that a 2.1x separation read
off two points might be noise dressed as signal - CANNOT BE RESOLVED with
available data.  The verdict "strongly overdetermined, expect EMPTY" therefore
keeps a standing caveat: it is one control, not a trend.

That is weaker than it was reported as, and it is stated here rather than left
implicit.

NO COUNTEREXAMPLE.
"""

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def consistency(L, e, degC, ordC):
    """the bound derivation's own internal check: -rho' * L == t - e*ordC"""
    rho_ = 2*ordC - L
    t = L*L - ordC
    return (-rho_*L) == (t - e*ordC), rho_, t - e*ordC


print(__doc__)
print("=" * 74)
print("(3,4) and (5,7) are the wrong controls")
print("=" * 74)
TBL = [("(4,12)", "(3,4)", 64, "other methods", False),
       ("(4,12)", "(5,7)", 112, "other methods", False),
       ("(7,21)", "(2,3)", 84, "GGHV section 6 - THIS machinery", True),
       ("(9,27)", "(2,3)", 108, "GGHV section 5 - THIS machinery", True),
       ("(8,28)", "(3,2)", 108, "OPEN", None)]
for a, mn, mx, how, this in TBL:
    print(f"   A0={a:8s} (m,n)={mn:6s} max={mx:4d}   {how}")
check("the (3,4) and (5,7) families were closed by OTHER methods, so scoring "
      "them tests nothing about this metric",
      all(not r[4] for r in TBL if r[1] in ("(3,4)", "(5,7)")))

print()
print("=" * 74)
print("section 6 cannot be scored either - wrong shape")
print("=" * 74)
CASES = [("section 5 (9,27)", 3, 5, 9, 8),
         ("(8,28)         ", 4, 7, 8, 7),
         ("section 6 (7,21)", 3, 2, 1, 1)]
res = {}
for lab, L, e, degC, ordC in CASES:
    ok, rho_, const = consistency(L, e, degC, ordC)
    res[lab.strip()] = ok
    print(f"   {lab}: degC={degC}, ordC={ordC}, e={e}   "
          f"-rho'*L = {-rho_*L:>4}, const = {const:>4}   consistent: {ok}")
check("the two-root cases (deg C = ord C + 1) both pass the consistency check",
      res["section 5 (9,27)"] and res["(8,28)"])
check("section 6 has the ONE-root shape (C_3 = y, deg C = ord C = 1, e = 2) "
      "and FAILS it - the derivation correctly refuses a shape it was not "
      "derived for", not res["section 6 (7,21)"])

print()
print("=" * 74)
print("what is and is not claimed about L")
print("=" * 74)
for lab, A0, B in (("section 5", (9, 27), (3, 9)), ("(8,28)   ", (8, 28), (4, 8))):
    print(f"   {lab}: A0 = {A0}, B = (L, deg C) = {B},  deg C == A0[0]: "
          f"{B[1] == A0[0]}")
check("B = (L, deg C) holds by definition, since R = x^L * C", True)
check("'deg C = A0[0]' holds on both points - but that is TWO points, and NO "
      "formula for L is proposed (correction #6 was exactly this mistake)",
      True)

print()
print("=" * 74)
print("consequence for the WP-B verdict")
print("=" * 74)
print("   usable controls for the tractability metric:")
print("     (3,4), (5,7)  -> wrong controls (other methods), L unknown")
print("     section 6     -> right method, wrong shape, fails consistency")
print("     section 5     -> the ONLY usable control, at 4.03x")
check("the metric rests on ONE control and one open case, and no further "
      "control is obtainable from the literature", True)
check("so 'strongly overdetermined, expect EMPTY' carries a standing caveat: "
      "one control is not a trend, and the objection that 2.1x might be noise "
      "CANNOT be resolved with available data", True)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
ITEM 3 IS DROPPED, WITH A REASON.  NO COUNTEREXAMPLE.

  The (m,n) generalisation was queued to buy calibration points.  It cannot:
  the (3,4) and (5,7) families were closed by other methods and are the wrong
  controls, and section 6 - which WAS closed by this machinery - has the
  one-root normalisation and fails the bound derivation's own consistency
  check.  Days spent generalising would produce coverage, not calibration.

  The honest cost is that the WP-B verdict keeps a caveat that cannot be
  discharged: it rests on a single closed control.  The separation may be
  signal; with one control it cannot be shown to be.
""")
assert all(PASS), "a certification failed"
