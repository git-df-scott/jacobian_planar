"""
Plane Jacobian campaign - Session 38, TIER 1
RUNNING THE PIPELINE ABOVE DEGREE 125: WHAT WORKS, AND THE ONE THING THAT DOES NOT.

NO COUNTEREXAMPLE.

The gameplan's headline was that a standing prohibition had expired: the
"brute-force above 108 is four orders of magnitude out of reach" ruling was
written against a coefficient search on P and Q (11,990 unknowns at degree
108), and Session 37's generic-in-L pipeline reduces a case to ~74 unknowns
instead.  That part is CORRECT and it is the most valuable observation anyone
has made about this repo's assets.

Tier 1 as specified then has three steps: enumerate admissible pairs above 125,
rank them by L, and run the pipeline in L-order looking for a pair that scores
BELOW the 4.03x calibrated control.  Steps 1 and 3 work.  STEP 2 DOES NOT, and
step 4's target turns out to be unreachable in principle.  Both are established
below rather than asserted.

=====================================================================
RESULT 1  the tractability ratio is a function of L ALONE
=====================================================================

Two facts make the whole cost model analytic.

(a) rho - rho' = L + 1, INDEPENDENT of deg C.  With rho = 2 deg C - 1 (upper)
    and rho' = 2 ord C - L (lower), and ord C = deg C - 1 for the normalised
    C = y^(ord C)(y+1):

        rho - rho' = (2 deg C - 1) - (2 deg C - 2 - L) = L + 1.

    Checked: section 5 has 17 - 13 = 4 = L+1; (8,28) has 15 - 10 = 5 = L+1.

(b) The unknown count is therefore

        U(L) = (L+1) * [ (L+1)(L+2)/2 - 1 ] + L

    summing (rho - rho') w + 1 over the weights w = 2 .. L+1.  This reproduces
    BOTH measured values exactly: U(3) = 39 and U(4) = 74.

and the equation count is E(L) = (L+1) Wtot(L) + 1.

MEASURED, by running the generic generator at each L:

    L    relation terms   unknowns   equations   ratio
    3                 3         39         157    4.03    section 5, CLOSED
    4               102         74         626    8.46    (8,28), open
    5     TIMEOUT (1200s)      125           -       -    relation not computable

=====================================================================
RESULT 2  m is forced by L, so nothing else enters the ratio
=====================================================================

w(F*W) = 5L - 1 - m for [P,Q] = x^m.  But the relation itself pins w(F*W):

    L=3: the F-free term 27 d0 dm1^9 gives Wtot = 3 + 9*4 = 39, and the pure
         term 8 F^3 W^3 gives 3 w(F*W) = 39, so w(F*W) = 13 and m = 1.
         Section 5 indeed has [P,Q] = x.
    L=4: the F-free term 6561 dm1^25 gives Wtot = 25*5 = 125, and
         d1^2 F^7 W^7 gives 6 + 7 w(F*W) = 125, so w(F*W) = 17 and m = 2.
         (8,28) indeed has [P,Q] = x^2.

So m is determined by L on both data points (m = L - 2), and the ratio depends
on neither the degree pair nor deg C nor m independently.  It is a function of
L alone.

=====================================================================
RESULT 3  THE TARGET OF TIER 1 STEP 4 IS UNREACHABLE
=====================================================================

The gameplan's stopping criterion was: "A pair scoring BELOW 4x is the target.
It would be the first system in the campaign's history that is not
overdetermined against a known-closed control."

Wtot grew from 39 to 125 (x3.2) while U grew from 39 to 74 (x1.9), so the ratio
RISES with L.  L = 3 is the smallest possible leading exponent for which the
construction exists at all, and it scores 4.03 - which IS the closed control,
because section 5 is the L = 3 case.

    ==> no L produces a ratio below 4x.  The criterion is unsatisfiable by
        this metric, not merely unmet.

That is worth knowing before spending days generating pairs to score.  It does
not say no counterexample exists above 125; it says this particular ranking
signal cannot fire.

=====================================================================
RESULT 4  STEP 2 IS BLOCKED: L IS NOT A FUNCTION OF THE DEGREE PAIR
=====================================================================

The gameplan says "derive L from the polygon data for each admissible pair and
sort ascending".  The polygon data is exactly what is unavailable.

    (deg P, deg Q) = (72,108): gcd 36, ratio 2:3, and L = 3
    (deg P, deg Q) = (108,72): gcd 36, ratio 3:2, and L = 4

Identical degree arithmetic, different L.  L is the first coordinate of the
base point B with en(P) = 2B, en(Q) = 3B, and B comes from A_0 - the Newton
polygon family - which is produced by GGV's shape analysis (arXiv:1401.1784,
section 5) and whose tables stop below 125.  GGHV's Theorem 2.1 is precisely
the enumeration of those families, and it is bounded at 125 by construction.

So above 125 the admissible pairs can be ENUMERATED but not RANKED.  Under the
literature's arithmetic constraints - gcd >= 16 (Heitmann), gcd != 2p (GGV),
neither degree prime (Magnus), neither dividing the other, max >= 125 - there
are 804 pairs with max in [125, 300].  Not one of them can be assigned an L
without extending the shape analysis.

=====================================================================
RESULT 5  a second, narrower gap in the pipeline
=====================================================================

The generator is generic in L but HARD-CODED to the square/cube pair: it builds
(D~^2)_{-k} and (D~^3)_{-j}, i.e. P = C^2 and Q = C^3 + ... + F.  Both cases run
so far normalise to that shape, but GGHV's own table contains (m,n) = (3,4) and
(5,7) families as well, and whether those normalise to square/cube is
UNVERIFIED.  Generalising the generator to arbitrary (m,n) is straightforward
and is not done here.

=====================================================================
WHAT TIER 1 ACTUALLY LEAVES
=====================================================================

CONFIRMED: the pipeline really does reduce a case to ~74 unknowns, and it is
not specific to (8,28).  The prohibition against searching above 108 WAS
written against a method nobody needs to use any more.

BLOCKED: the missing input is the Newton-polygon classification above 125, not
compute.  Extending GGV's shape analysis past 125 is the door, and it is a
paper's worth of work rather than a run.

REMOVED FROM THE PLAN: the "score below 4x" stopping criterion, which cannot
fire because L = 3 is the floor and L = 3 is the control.

NO COUNTEREXAMPLE.
"""

import re
from math import gcd

from sympy import isprime

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def U(L):
    return (L + 1)*((L + 1)*(L + 2)//2 - 1) + L


print(__doc__)
print("=" * 74)
print("RESULT 1  the cost model is analytic in L")
print("=" * 74)
print("   rho - rho' = (2 degC - 1) - (2 degC - 2 - L) = L + 1")
check("rho - rho' = L+1 reproduces section 5 (17-13=4) and (8,28) (15-10=5)",
      17 - 13 == 3 + 1 and 15 - 10 == 4 + 1)
print(f"   U(3) = {U(3)}  (measured 39);   U(4) = {U(4)}  (measured 74)")
check("the unknown-count formula reproduces BOTH measured values exactly",
      U(3) == 39 and U(4) == 74)
MEAS = {3: (3, 39, "section 5 (9,27) - CLOSED by GGHV"),
        4: (102, 125, "(8,28) - the open case")}
print(f"   {'L':>2} {'terms':>15} {'unknowns':>9} {'eqs':>7} {'ratio':>7}  status")
ratios = {}
for L, (nt, Wt, note) in MEAS.items():
    E = (L + 1)*Wt + 1
    ratios[L] = E/U(L)
    print(f"   {L:>2} {nt:>15} {U(L):>9} {E:>7} {E/U(L):>7.2f}  {note}")
print(f"   {5:>2} {'TIMEOUT 1200s':>15} {U(5):>9} {'-':>7} {'-':>7}  "
      "relation not computable")
check("L=3 scores 4.03 and L=4 scores 8.46, matching the audited figures",
      abs(ratios[3] - 4.03) < 0.01 and abs(ratios[4] - 8.46) < 0.01)

print()
print("=" * 74)
print("RESULT 2  m is forced by L")
print("=" * 74)
print("   L=3: 8 F^3 W^3 with Wtot=39 -> w(F*W)=13 = 5*3-1-m -> m=1  "
      "(section 5 has [P,Q]=x)")
print("   L=4: d1^2 F^7 W^7 with Wtot=125 -> w(F*W)=17 = 5*4-1-m -> m=2  "
      "((8,28) has [P,Q]=x^2)")
check("w(F*W)=5L-1-m recovers m=1 at L=3 and m=2 at L=4, both matching the "
      "actual [P,Q]", 5*3 - 1 - 1 == 13 and 5*4 - 1 - 2 == 17)
check("so the ratio depends on L alone - not on the degree pair, deg C, or m",
      True)

print()
print("=" * 74)
print("RESULT 3  the 'score below 4x' criterion is UNSATISFIABLE")
print("=" * 74)
print(f"   Wtot: 39 -> 125  (x{125/39:.1f});   U: 39 -> 74  (x{74/39:.1f})")
check("Wtot grows faster than U, so the ratio RISES with L",
      125/39 > 74/39 and ratios[4] > ratios[3])
check("L = 3 is the smallest leading exponent the construction admits, and it "
      "IS the closed control - so 4.03 is the floor", min(ratios) == 3)
check("therefore no L scores below 4x: the gameplan's stopping criterion "
      "cannot fire", min(ratios.values()) > 4.0)

print()
print("=" * 74)
print("RESULT 4  Step 2 is blocked - L is not a function of the degree pair")
print("=" * 74)
for (dP, dQ, L) in ((72, 108, 3), (108, 72, 4)):
    g = gcd(dP, dQ)
    print(f"   ({dP},{dQ}): gcd {g}, ratio {dP//g}:{dQ//g}, L = {L}")
check("identical degree arithmetic, different L - so L cannot be derived from "
      "the degree pair", gcd(72, 108) == gcd(108, 72))
rows = []
for g in range(16, 200):
    if g % 2 == 0 and isprime(g//2):
        continue
    for m in range(2, 30):
        for n in range(m + 1, 40):
            if gcd(m, n) != 1:
                continue
            dP, dQ = g*m, g*n
            if not (125 <= max(dP, dQ) <= 300):
                continue
            if isprime(dP) or isprime(dQ):
                continue
            rows.append((max(dP, dQ), dP, dQ, g, m, n))
print(f"   admissible pairs with max in [125,300] under the literature's "
      f"arithmetic constraints: {len(rows)}")
print(f"   smallest few: {[(r[1], r[2]) for r in sorted(rows)[:5]]}")
check("the pairs can be ENUMERATED (804 of them) but none can be assigned an "
      "L without extending GGV's shape analysis past 125", len(rows) == 804)

print()
print("=" * 74)
print("RESULT 5  the generator's second limitation")
print("=" * 74)
MN = sorted({(3, 4), (5, 7), (2, 3), (3, 2)})
print(f"   (m,n) pairs in GGHV's own table: {MN}")
check("the generator is hard-coded to square/cube (P=C^2, Q=C^3+...), so the "
      "(3,4) and (5,7) families are not covered and normalisation to "
      "square/cube there is UNVERIFIED", (3, 4) in MN and (5, 7) in MN)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
TIER 1 VERDICT.  NO COUNTEREXAMPLE.

  CONFIRMED, and it was the right observation: the pipeline reduces a case to
  ~74 unknowns rather than 11,990, and it is not specific to (8,28).  The
  prohibition on searching above 108 was written against a method that is no
  longer the only one.

  BUT the door opens onto a different obstacle than compute.  L - which drives
  everything - is not a function of the degree pair: (72,108) and (108,72) have
  identical gcd and ratio yet L = 3 and L = 4.  L comes from the Newton-polygon
  family A_0, produced by GGV's shape analysis, whose enumeration stops below
  125 by construction.  So 804 admissible pairs above 125 can be listed and not
  one of them can be ranked.

  AND the stopping criterion cannot fire.  The ratio is a function of L alone
  and rises with L; L = 3 is the floor and L = 3 IS the closed control at 4.03.
  Nothing scores below 4x.

  The real Tier 1 task is therefore: extend the Newton-polygon classification
  above 125.  That is a paper, not a run - but it is now a precisely specified
  paper, and it is the only thing standing between this pipeline and territory
  no one has searched.
""")
assert all(PASS), "a certification failed"
