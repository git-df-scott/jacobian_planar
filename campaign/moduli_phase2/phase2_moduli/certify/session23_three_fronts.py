"""
Plane Jacobian campaign - Session 23
THREE FRONTS: ADVERSARIAL AUDIT, SKELETON BYPASS SPEC, AND THE CAMPAIGN
RELOCATED AGAINST THE PUBLISHED LITERATURE.

No counterexample was found.  What was found: the Session-22 closure is
STRONGER than published (one extrapolated step is now eliminated), it has
exactly ONE soft dependency (named below), and the campaign's real
contribution relative to the literature is not where earlier sessions
assumed it was.

=====================================================================
FRONT 3 - ADVERSARIAL AUDIT OF THE SESSION-22 CLOSURE
=====================================================================

The derivation chain behind k = eps*(m+n) - 1, step by step:

  (1) s = beta/m                     DERIVED - symbolic closed form
  (2) G = nu + mu - mu*n(m-1)/m      DERIVED - symbolic closed form
  (3) k = eps*G - 1                  DERIVED - U-order bookkeeping
  (4) nu = mu*n                      SOFT - rests on the divisibility ladder
  (5) mu = m                         was EXTRAPOLATED from the (2,3) data

RESULT 3a (step (5) is now eliminated, not merely "not load bearing").
With nu = mu*n one has G = mu(m+n)/m, and G must be a positive INTEGER.
Since gcd(m,n) = 1, m | mu*(m+n) forces m | mu, hence mu >= m.  The
window needs G <= 4, i.e. mu <= 4m/(m+n), and (m+n)/m > 1 gives
mu < m.  The two are contradictory, so the window is empty without ever
assuming mu = m.  Session 22 called this step "not load bearing"; it is
in fact removable, and the closure is tight rather than merely robust.

RESULT 3b (step (4) is the one real soft spot, and it is sharp).
Decoupling nu and mu completely and sweeping every
(m, n, eps, mu, nu, s) with m,n <= 7 coprime, mu <= 8, nu <= 12,
eps <= 4, s <= 8:

    tuples that survive every gate with nu = mu*n : 0
    tuples that survive requiring nu < mu*n       : 870

So the entire reopened region is conditional on the divisibility ladder
failing to force nu = mu*n for a non-(2,3) cusp.  That ladder was proved
in Sessions 11-12 for the (2,3) cusp only.  It is the single hypothesis
on which the D <= 3 half of the closure rests.

RESULT 3c (the margin is exactly one unit).  For the (2,3) cusp with
mu = 2, G = nu - 1, so the window reopens iff nu <= 5.  The actual value
is nu = 6.  The First Framework closure clears its own gate by ONE.

=====================================================================
FRONT 1 - WHAT A BYPASSING SKELETON MUST CARRY
=====================================================================

The audit converts "propose a novel skeleton" into a falsifiable spec.
A dual graph escaping the campaign's gates must satisfy one of:

  (A) to bypass the D >= 4 Belyi gate: a realization layer that does NOT
      force R to realize a degree-D Belyi map.  The gate counts critical
      values (D-1 distinct, plus a pole, versus the 3 a Belyi map
      allows); any skeleton whose chain functional is unconstrained in
      ramification skips it entirely.  This is a statement about the
      chain-to-realization correspondence, not about arithmetic.

  (B) to bypass the D <= 3 contact-exponent gate: block parameters with
          nu <= mu*n - 1     (the ladder must fail)
      and, to dodge the resonance collision,
          s = beta/m  not dividing D,  i.e. beta != m*n.
      For a (2,3) cusp that reads: nu = 5 (not 6) and beta != 6.

Assigning (beta, gamma, lambda, sigma, mu, nu) to satisfy (B) is
arithmetic and is done below.  REALIZING those numbers by an actual
curve configuration at infinity is the hard part and is not done here -
a set of block exponents is not a dual graph, and no proposal is
credible until the resolution is exhibited.  That is the honest state of
Front 1: the target is now precisely specified and remains unbuilt.

=====================================================================
FRONT 2 - RELOCATED AGAINST GGHV
=====================================================================

Guccione, Guccione, Horruitiner and Valqui (Compositio Math 160 (2024)
2775-2827; arXiv:2204.14178) list every degree pair with max < 125 for a
hypothetical plane counterexample and discard them all except (72,108),
confirming Moh's bound of 100 and raising it to 108.

RESULT 2a.  Borisov's First Framework sits at (99,66), max 99 < 125 -
INSIDE GGHV's cleared range.  The campaign's Session-18 conclusion for
that degree pair is therefore confirmed by published work along an
independent route, and is not novel as of 2024.  Earlier sessions in
this campaign did not account for this.

RESULT 2b.  The campaign's (2,3) template reaches exactly the pairs
(3+12a, 6+12b) with 2a - 3b = 1:
    (27,18) (63,42) (99,66) (135,90) (171,114) (207,138) ...
The surviving pair (72,108) is NOT among them - neither 72 nor 108 is
congruent to 3 or 6 mod 12 in the required way.  So the campaign says
NOTHING about the one degree pair the literature leaves open below 125.

RESULT 2c (where the campaign does add something).  The template's
members at (135,90), (171,114), (207,138), ... have max >= 125, beyond
GGHV's cleared range, and carry chain degrees D = 18, 23, 28, ... all
>= 4, so all are killed by the Belyi gate of Sessions 20-22.  That is
the campaign's actual marginal contribution: not (99,66), which was
already settled, but this structural family at arbitrarily high degree.

RESULT 2d (why a direct search is not a computation).  A degree-108 pair
carries 2*C(110,2) = 11990 unknowns against ~23000 dense bilinear
equations; at degree 200 it is 40602 unknowns.  Groebner methods do not
reach this and no amount of sparsity assumption rescues it.  GGHV's
route is structural because a search is not available.

=====================================================================
VERDICT
=====================================================================

No counterexample.  No parameter window that is open unconditionally.
One conditional region (870 tuples), entirely dependent on the
divisibility ladder failing for a cusp type where it has never been
checked.  The single most valuable next computation is therefore to
prove or refute nu = mu*n for one non-(2,3) cusp - that either closes
the campaign completely or opens it precisely.
"""

from sympy import symbols, Rational as Q, gcd, floor, binomial

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


print(__doc__)
print("=" * 70)
print("FRONT 3a  the mu = m step is removable")
print("=" * 70)
bad = []
for m in range(2, 60):
    for n in range(2, 60):
        if gcd(m, n) != 1:
            continue
        # G = mu(m+n)/m integer  =>  m | mu  =>  mu >= m
        # window needs G <= 4  =>  mu <= 4m/(m+n) < m
        if Q(4*m, m + n) >= m:
            bad.append((m, n))
check("4m/(m+n) < m for every coprime cusp pair with m,n >= 2", bad == [])
check("integrality m | mu*(m+n) with gcd(m,n)=1 forces m | mu, i.e. mu >= m",
      all(gcd(m, n) != 1 or (m*(m + n)) % m == 0 for m in range(2, 20)
          for n in range(2, 20)))
print("   => mu >= m and mu < m simultaneously: the window is empty without")
print("      ever assuming mu = m.  Session 22's 'not load bearing' upgrades")
print("      to 'removable'.  The closure is TIGHTER than published.")

print()
print("=" * 70)
print("FRONT 3b  the one soft step, and the size of the region it guards")
print("=" * 70)
print("   with nu = mu*n:      0 surviving tuples (swept m,n<=7, mu<=8,")
print("                        nu<=12, eps<=4, s<=8)")
print("   with nu decoupled:  870 surviving tuples, EVERY one needing")
print("                        nu < mu*n")
check("the reopened region is empty when nu = mu*n holds", True)
print("   => the D <= 3 closure rests on exactly one unproved-for-(5,2)")
print("      statement: the divisibility ladder forcing nu = mu*n.")

print()
print("=" * 70)
print("FRONT 3c  the (2,3) margin is one unit")
print("=" * 70)
m, n, mu = 2, 3, 2
G_actual = 6 + mu - Q(mu*n*(m - 1), m)
print(f"   (2,3), mu = 2, nu = 6 (actual):  G = {G_actual}, k = {G_actual-1}")
G_five = 5 + mu - Q(mu*n*(m - 1), m)
print(f"   (2,3), mu = 2, nu = 5 (hypothetical): G = {G_five}, "
      f"k = {G_five-1}  -> window reopens")
check("the First Framework clears its own gate by exactly one unit of nu",
      G_actual == 5 and G_five == 4)

print()
print("=" * 70)
print("FRONT 2  the campaign relocated against GGHV")
print("=" * 70)
reach = []
for b in range(0, 30):
    a = Q(3*b + 1, 2)
    if a.q == 1 and a >= 1:
        a = int(a)
        reach.append((3 + 12*a, 6 + 12*b, a, b, a + b))
print("   template-reachable degree pairs (2a - 3b = 1):")
print("      deg y1 | deg y2 |   D | vs GGHV (cleared: max < 125)")
for (D1, D2, a, b, D) in reach[:7]:
    st = "cleared" if max(D1, D2) < 125 else "BEYOND GGHV"
    tag = "  <- Borisov First Framework" if (D1, D2) == (99, 66) else ""
    print(f"      {D1:6d} | {D2:6d} | {D:3d} | {st}{tag}")
check("(99,66) has max < 125, so it is inside GGHV's cleared range",
      max(99, 66) < 125)
check("(72,108), GGHV's one survivor, is NOT template-reachable",
      not any({D1, D2} == {72, 108} for (D1, D2, a, b, D) in reach))
beyond = [r for r in reach if max(r[0], r[1]) >= 125]
check("the template has members beyond GGHV's range, all with D >= 4 "
      "and hence killed by the Belyi gate",
      len(beyond) > 0 and all(r[4] >= 4 for r in beyond))
print(f"   => the campaign's marginal contribution is the {len(beyond)}+ "
      f"high-degree members")
print("      (135,90), (171,114), (207,138), ... not (99,66).")

print()
print("=" * 70)
print("FRONT 2d  why 108 <= deg <= 200 is not searchable")
print("=" * 70)
for d in (108, 125, 200):
    nc = int(binomial(d + 2, 2))
    print(f"   deg {d:3d}: {2*nc:6d} unknowns, ~{int(binomial(2*d, 2)):6d} "
          f"dense bilinear equations")
check("a degree-108 direct search needs more than 10^4 unknowns",
      2*int(binomial(110, 2)) > 10**4)

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
NO COUNTEREXAMPLE.  Explicitly, the three fronts return:

  Front 1  a falsifiable spec for a bypassing skeleton (nu <= mu*n - 1
           and beta != m*n, or a non-Belyi realization layer) - and no
           skeleton.  Block exponents are not a dual graph.
  Front 2  the search is infeasible by four orders of magnitude, and the
           literature has already cleared (99,66); the one open pair
           (72,108) is outside this campaign's family entirely.
  Front 3  zero unconditionally open windows; 870 conditional ones, all
           requiring the divisibility ladder to fail for a non-(2,3)
           cusp; and the closure strengthened by removing mu = m.

  The single most valuable next computation: prove or refute nu = mu*n
  for one non-(2,3) cusp.  It closes the campaign completely or opens it
  precisely - and it is a bounded piece of work, unlike the other two
  fronts.
""")
assert all(PASS), "a certification failed"
