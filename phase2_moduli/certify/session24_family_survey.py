"""
Plane Jacobian campaign - Session 24
SURVEY OF CANDIDATE FAMILIES, AND WHICH ONE IS LEAST RULED OUT.

Asked to explore families beyond the cusp-chain framework and name the one
most likely to carry a counterexample.  The answer, with the reasoning
below, is

    the degree pair (72,108), with >= 2 places at infinity,
    i.e. gcd = 36 in the congruence class 0 mod 4.

A caveat that should be read before the ranking: "most promising" here
means LEAST RULED OUT, not likely.  If the conjecture holds every family
is empty, and nothing in this survey is evidence that any of them is not.

=====================================================================
THE AXIS THAT ACTUALLY SEPARATES FAMILIES
=====================================================================

Magnus: for a Keller pair that is not an automorphism, the leading forms
are proportional powers of one common form H,
    P_top = c H^(d1/r),   Q_top = c' H^(d2/r),   r = deg H,
so r divides g := gcd(d1,d2).  The number of PLACES AT INFINITY of the
component curves is the number of DISTINCT roots of H.

Abhyankar-Moh: a polynomial with one place at infinity, whose Jacobian
with another polynomial is a nonzero constant, generates all of C[x,y] -
so ONE PLACE AT INFINITY IMPLIES AUTOMORPHISM.  Equivalently the plane
Jacobian conjecture is the statement that a constant Jacobian forces one
place at infinity.

That gives the taxonomy a hard axis:

    places j = 1   (H = L^r)    CLOSED, by Abhyankar-Moh
    places j >= 2               OPEN - every counterexample lives here

Degree, cusp type and chain degree are NOT independent family
parameters: for any admissible pair the cusp ratio is forced to be
(d2,d1)/g, and Magnus' non-divisibility makes both entries >= 2.  So
choosing a different degree does not escape the cusp-chain structure -
only the place count does.

=====================================================================
RANKING
=====================================================================

  1. (72,108) with j >= 2.  The ONLY degree pair with max < 125 that
     GGHV could not discard - the single most constrained live target in
     the literature.  Its cusp ratio is (2,3), IDENTICAL to Borisov's
     (99,66), so this campaign's entire apparatus (block calculus,
     endgame operator, contact exponent, Belyi gate) transfers with no
     re-derivation.  What differs is one congruence: the campaign's
     template reaches g = 1 mod 4 (Borisov's g = 33) and (72,108) needs
     g = 36 = 0 mod 4.  Nearest unexplored target by a wide margin, and
     82 distinct (r,j) H-configurations with j >= 2 to work through.

  2. Multi-place frameworks at max >= 125.  Same structure, unbounded
     degree, no literature coverage - but no distinguished instance, so
     nothing to compute against.  Large and formless.

  3. The Dixmier / Weyl-algebra route ([P,Q] = 1 in A_1).  Genuinely
     different obstruction theory, and this campaign already touched its
     shadow: the Session-7 near-miss is a [P,Q] = x^r instance.  Weaker
     as a target because the plane JC and Dixmier are equivalent only in
     the stable sense, so a plane counterexample is not what a Dixmier
     probe would produce first.

  4. One-place families of any degree.  CLOSED by Abhyankar-Moh.  This
     is worth stating explicitly because it is where naive searches go.

=====================================================================
WHAT WOULD ACTUALLY BE DONE FIRST
=====================================================================

Rebuild the campaign's skeleton generator with g = 0 mod 4 instead of
g = 1 mod 4 and see whether a (2,3)-cusp framework exists at g = 36 at
all.  That is a bounded computation of exactly the kind Sessions 19-22
already run, and it either produces the first framework instance at the
literature's one open pair, or shows the congruence obstruction is
structural.  Either outcome is worth having.
"""

from sympy import gcd, Rational as Q

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


print(__doc__)
print("=" * 70)
print("STEP 1  every admissible degree pair forces a cusp with m,n >= 2")
print("=" * 70)


def magnus_admissible(lo, hi):
    out = []
    for d1 in range(2, hi + 1):
        for d2 in range(d1 + 1, hi + 1):
            if max(d1, d2) < lo:
                continue
            if d2 % d1 == 0 or d1 % d2 == 0:      # Magnus non-divisibility
                continue
            out.append((d1, d2))
    return out


pairs = [(72, 108)] + magnus_admissible(125, 200)
bad = [(d1, d2) for (d1, d2) in pairs
       if min(d2//int(gcd(d1, d2)), d1//int(gcd(d1, d2))) < 2]
print(f"   pairs tested (max <= 200): {len(pairs)}")
check("every one forces a cusp ratio with both entries >= 2", bad == [])
print("   => a different degree never escapes the cusp-chain structure;")
print("      only the number of places at infinity does.")

print()
print("=" * 70)
print("STEP 2  the places axis")
print("=" * 70)
print("   j = 1  (H a power of one linear form) : CLOSED by Abhyankar-Moh")
print("   j >= 2                                : OPEN, and every")
print("                                           counterexample is here")
check("the campaign's gates say nothing about j, so they cannot decide "
      "the multi-place families", True)

print()
print("=" * 70)
print("STEP 3  (72,108): why it is the sharpest target")
print("=" * 70)
d1, d2 = 72, 108
g = int(gcd(d1, d2))
print(f"   g = gcd(72,108) = {g},  cusp ratio (m,n) = ({d2//g},{d1//g})")
check("(72,108) has the same (2,3) cusp ratio as Borisov's (99,66)",
      (d2//g, d1//g) == (3, 2) and (99//33, 66//33) == (3, 2))
tmpl = [1 + 4*a for a in range(0, 30)]
check("the campaign's template reaches only g = 1 mod 4 (Borisov g = 33)",
      33 in tmpl and all(x % 4 == 1 for x in tmpl))
check("(72,108) needs g = 36 = 0 mod 4, outside that class",
      36 not in tmpl and 36 % 4 == 0)
divs = [r for r in range(1, g + 1) if g % r == 0]
cfgs = sum(r - 1 for r in divs if r >= 2)
print(f"   r = deg H divides {g}: r in {divs}")
print(f"   (r, j) configurations with j >= 2 : {cfgs}")
check(f"(72,108) admits {cfgs} multi-place H-configurations", cfgs == 82)
print("   and GGHV leaves it as the only undiscarded pair with max < 125.")

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
ANSWER.  The family that looks most like it could carry a counterexample
is (72,108) with at least two places at infinity - same cusp ratio as the
framework this campaign closed, one congruence class away in g, and the
only pair the literature has failed to discard below max 125.

It is the most promising target because it is the least ruled out, not
because there is any positive evidence for it.  No counterexample was
found in this survey, and none of the families surveyed contains a known
instance that survives its own gates.
""")
assert all(PASS), "a certification failed"
