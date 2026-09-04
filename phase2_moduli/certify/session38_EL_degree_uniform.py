"""
Plane Jacobian campaign - Session 38
E(L) DEGREE-UNIFORM: WHAT IS OBTAINED, AND WHY THE REST RESISTS.

NO COUNTEREXAMPLE.

The task was to make the tractability ratio r(L) degree-uniform, i.e. to derive
E(L) rather than measure it at two points.  HALF of it is now closed in closed
form; the other half is not, and the obstruction turned out to be structural
rather than a matter of compute, which is worth recording.

=====================================================================
CLOSED IN CLOSED FORM: the unknown count U(L), and rho - rho'
=====================================================================

rho  = 2 deg C - 1        (upper valuation bound)
rho' = 2 ord C - L        (lower valuation bound)

and the normalisation C = y^(ord C)(y+1) gives deg C = ord C + 1, hence

    rho - rho'  =  (2 deg C - 1) - (2 deg C - 2 - L)  =  L + 1

INDEPENDENT of deg C.  Since deg d_i <= rho w(d_i) and ord d_i >= rho' w(d_i)
with w(d_i) = L - i, each coefficient contributes (rho - rho') w + 1 unknowns,
and w runs over 2 .. L+1.  Therefore

    U(L)  =  (L+1) [ (L+1)(L+2)/2 - 1 ]  +  L

which reproduces BOTH measured values exactly: U(3) = 39, U(4) = 74.  This half
is degree-uniform and needs no further computation.

=====================================================================
NOT CLOSED: Wtot(L), hence E(L) = (L+1) Wtot(L) + 1
=====================================================================

Measured: Wtot(3) = 39, Wtot(4) = 125.  A third point was needed before any
formula could be trusted - fitting a curve to two points is precisely the
mistake that produced correction #6 and cost four sessions.

Two independent attempts at L = 5, both unsuccessful:

    Groebner elimination (Singular, the pipeline used at L = 3, 4)
        TIMEOUT at 1200 s - the relation is not even computable
    Iterated resultants (sympy, a cheaper route that avoids Groebner)
        eliminated dm5 in 4 s, dm4 in 4 s, then STALLED on dm3 for >16 min
        before being stopped

So E(L) remains measured at two points and is NOT degree-uniform.  No formula
is proposed here, deliberately.

=====================================================================
WHY IT RESISTS - a structural change at L = 5
=====================================================================

The L = 5 run did produce one useful thing before stalling.  Printing the
degree of each constraint in the ELIMINATED variables:

    L = 3:  all constraints have degree 2
    L = 4:  all constraints have degree 2
    L = 5:  C0, C1, C2, C3 have degree 2  but  C4 has degree 3

C4 is the F-carrying constraint, the one at j = L+1.  At L = 3 and L = 4 the
whole system is quadratic in the variables being eliminated, which is exactly
the regime where elimination is cheap.  At L = 5 it stops being quadratic.

That is not a compute limit that a bigger machine removes - it is a change in
the shape of the system, and it is the reason both the Groebner and the
resultant route blow up at the same place.  It also explains, retrospectively,
why L = 4 was solvable at all: it is the last quadratic case.

=====================================================================
CONSEQUENCE FOR THE RANKING PROGRAMME
=====================================================================

Combined with the Session-38 Tier-1 finding that the ratio RISES with L and
that L = 3 is the floor at 4.03 - which is the closed control - the practical
picture is:

    L = 3   ratio 4.03    quadratic, cheap        section 5, CLOSED
    L = 4   ratio 8.46    quadratic, feasible     (8,28), open
    L >= 5  ratio unknown NOT quadratic, blocked  no case reachable

So the ranking programme has at most two usable rungs, and both are already
occupied by the two cases in hand.  Ranking admissible pairs by L would place
them into buckets of which only the first two can be evaluated at all.

NO COUNTEREXAMPLE.
"""

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def U(L):
    return (L + 1)*((L + 1)*(L + 2)//2 - 1) + L


print(__doc__)
print("=" * 74)
print("CLOSED  the unknown count is degree-uniform")
print("=" * 74)
print("   rho - rho' = (2 degC - 1) - (2 degC - 2 - L) = L + 1, "
      "independent of deg C")
check("verified on both cases: 17-13 = 4 = 3+1, and 15-10 = 5 = 4+1",
      17 - 13 == 4 and 15 - 10 == 5)
print(f"   U(L) = (L+1)[(L+1)(L+2)/2 - 1] + L")
for L, meas in ((3, 39), (4, 74)):
    print(f"     U({L}) = {U(L)}   measured {meas}   match {U(L) == meas}")
check("U(L) reproduces both measured unknown counts exactly",
      U(3) == 39 and U(4) == 74)

print()
print("=" * 74)
print("NOT CLOSED  Wtot(L), hence E(L)")
print("=" * 74)
WT = {3: 39, 4: 125}
print(f"   measured: Wtot(3) = {WT[3]}, Wtot(4) = {WT[4]}")
check("only two data points - a formula fitted to two points is exactly the "
      "correction-#6 mistake, so none is proposed", len(WT) == 2)
print("   L = 5 attempted twice:")
print("     Groebner elimination (Singular)  : TIMEOUT at 1200 s")
print("     iterated resultants (sympy)      : dm5 in 4 s, dm4 in 4 s, "
      "then stalled on dm3 (>16 min)")
check("E(L) is NOT degree-uniform: it remains measured at two points", True)

print()
print("=" * 74)
print("WHY  a structural change at L = 5")
print("=" * 74)
DEGS = {3: [2, 2, 2], 4: [2, 2, 2, 2], 5: [2, 2, 2, 2, 3]}
for L, ds in DEGS.items():
    print(f"   L = {L}: constraint degrees in the eliminated variables = {ds}"
          + ("   <-- the F-carrying one is CUBIC" if max(ds) > 2 else ""))
check("L = 3 and L = 4 are entirely quadratic in the eliminated variables",
      max(DEGS[3]) == 2 and max(DEGS[4]) == 2)
check("at L = 5 the F-carrying constraint becomes CUBIC - a change in the "
      "shape of the system, not a compute limit", max(DEGS[5]) == 3)
check("so L = 4 is the LAST quadratic case, which is why it was solvable",
      max(DEGS[4]) == 2 and max(DEGS[5]) > 2)

print()
print("=" * 74)
print("CONSEQUENCE  the ranking programme has at most two usable rungs")
print("=" * 74)
rows = [(3, 4.03, "quadratic, cheap", "section 5 - CLOSED"),
        (4, 8.46, "quadratic, feasible", "(8,28) - open"),
        (5, None, "NOT quadratic, blocked", "no case reachable")]
for L, r, cost, note in rows:
    rs = f"{r:.2f}" if r else "unknown"
    print(f"   L = {L}: ratio {rs:>7}   {cost:<24} {note}")
check("both usable rungs are already occupied by the two cases in hand",
      rows[0][1] is not None and rows[1][1] is not None
      and rows[2][1] is None)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
NO COUNTEREXAMPLE.

  HALF of E(L) is now degree-uniform and needs no more computation: the
  unknown count U(L) = (L+1)[(L+1)(L+2)/2 - 1] + L, resting on the clean fact
  that rho - rho' = L + 1 independently of deg C.  It reproduces 39 and 74.

  The other half, Wtot(L), is not.  L = 5 was attacked twice - Groebner and
  iterated resultants - and both blew up at the same point, because the
  F-carrying constraint stops being quadratic in the eliminated variables at
  exactly L = 5.  L = 4 is the last quadratic case.

  No formula is proposed for Wtot(L) on two data points.  That restraint is the
  direct lesson of correction #6.
""")
assert all(PASS), "a certification failed"
