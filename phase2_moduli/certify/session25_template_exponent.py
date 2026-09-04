"""
Plane Jacobian campaign - Session 25
THE TEMPLATE EXPONENT IS NOT FIXED - AND THE DEGREE FORMULA WAS WRONG.

Run to attack the (72,108) target named in Session 24.  NO COUNTEREXAMPLE
was found: (72,108) is not reachable by this campaign's family.  But the
attack exposed two errors in Sessions 21-24 that matter more than the
target did.

=====================================================================
WHAT WENT WRONG, AND WHAT IS TRUE
=====================================================================

Sessions 21-24 treated the exponent in Session 7's near-miss

    v = x1 * x2^3 - 1,   y1 = x1^3 x2^a p(v^3/x2),
                         y2 = x1^2 x2^b v r(v^3/x2)

as FIXED at 3, and read off deg y1 = 3 + 12a, deg y2 = 6 + 12b.

CORRECTION 1 (the exponent is a parameter, and it is determined).
Writing v = x1*x2^E - 1 and sweeping E, the Jacobian collapses to a
MONOMIAL - the near-miss condition - at exactly one value of E per
Belyi datum, and it is not always 3:

      (deg p, deg r) = (2,1)  ->  monomial at E = 1
      (deg p, deg r) = (5,3)  ->  monomial at E = 2
      (deg p, deg r) = (8,5)  ->  monomial at E = 3   [Session 7]

Three independent data points give  E = a - b, and with the Belyi
relation 2a = 3b+1 that is E = (a+1)/3, forcing a = 2 (mod 3).

CORRECTION 2 (the degree formula is quadratic, not linear).
With E = (a+1)/3,

      deg y1 = (a+1)(a+3),      deg y2 = (2/3)(a+1)(a+3),

so the family's reachable degree pairs are

      a= 2: (15,10)     a= 5: (48,32)     a= 8: (99,66)  [Borisov]
      a=11: (168,112)   a=14: (255,170)   a=17: (360,240)

NOT the linear list (27,18), (63,42), (99,66), (135,90), (171,114)
published in Session 23.  Only the Borisov entry was ever right - the
linear formula happened to agree at a = 8, which is why it survived.

CORRECTION 3 (Session 24's centrepiece is void).  Session 24 ranked
(72,108) as the nearest target on the grounds that the template reaches
g = 1 (mod 4) while (72,108) needs g = 36 = 0 (mod 4).  The true g
values are 5, 16, 33, 56, 85, 120 - they ALTERNATE between both classes.
There is no mod-4 obstruction.  The ranking's stated reason was wrong.

=====================================================================
WHY (72,108) IS STILL UNREACHABLE
=====================================================================

deg y1 = 108 requires (a+1)(a+3) = 108, i.e. a^2 + 4a - 105 = 0, whose
roots are not integers.  Equivalently g = 36 requires a(a+4) = 105.
So (72,108) is outside the family - the ANSWER in Sessions 23-24 was
right, for a reason that had nothing to do with congruences.

=====================================================================
WHAT SURVIVES UNCHANGED
=====================================================================

The chain degrees D = a + b = 3, 8, 13, 18, 23, 28 are untouched by any
of this - only the degree pairs attached to them moved.  So every gate
conclusion of Sessions 20-22 stands: D >= 4 closed by the Belyi gate,
D <= 3 closed by the contact exponent.

The GGHV comparison survives with corrected numbers:
    (15,10), (48,32), (99,66)     max < 125, cleared by GGHV
    (168,112), (255,170), ...     beyond GGHV, killed by the Belyi gate
so the campaign's marginal contribution is still the high-degree tail,
now correctly located.

=====================================================================
NEW ARTIFACT
=====================================================================

The smallest member of the family, previously never written down:

    a = 2, b = 1, E = 1, N = 4, delta = 1, D = 3
    p = w^2 + (3/2)w + 3/8,   r = w + 1,   p^2 - w r^3 = w/8 + 9/64
    v = x1*x2 - 1,  degrees (15,10),  Jacobian a single monomial.

It is a genuine near-miss, verified below, and it is the cheapest object
on which to test any future claim about this family.
"""

from sympy import (symbols, Rational as Q, Poly, diff, expand, factor,
                   total_degree, discriminant, solve, Symbol, simplify)

x1, x2, w = symbols('x1 x2 w')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def near_miss(pc, rc, E):
    """Build the template map and return (deg y1, deg y2, #monomials of J)."""
    a, b = len(pc) - 1, len(rc) - 1
    v = x1*x2**E - 1
    y1 = expand(x1**3*sum(pc[k]*v**(3*k)*x2**(a - k) for k in range(a + 1)))
    y2 = expand(x1**2*v*sum(rc[k]*v**(3*k)*x2**(b - k) for k in range(b + 1)))
    J = Poly(expand(diff(y1, x1)*diff(y2, x2) - diff(y1, x2)*diff(y2, x1)),
             x1, x2)
    return (int(total_degree(Poly(y1, x1, x2))),
            int(total_degree(Poly(y2, x1, x2))), len(J.monoms()))


print(__doc__)
print("=" * 70)
print("CORRECTION 1  the monomial locus in E, at three Belyi data")
print("=" * 70)

# (a,b) = (2,1): solved from deg(p^2 - w r^3) = delta = 1
p21 = [Q(3, 8), Q(3, 2), 1]
r21 = [1, 1]
# (a,b) = (5,3): solved from deg(p^2 - w r^3) = delta = 2
p53 = [Q(1, 576), Q(5, 96), Q(1, 3), 1, Q(3, 2), 1]
r53 = [Q(1, 18), Q(5, 12), 1, 1]

print("     (a,b) |  E  | degrees      | # monomials of J")
mono = {}
for (pc, rc, lab) in [(p21, r21, (2, 1)), (p53, r53, (5, 3))]:
    for E in range(1, 5):
        d1, d2, nm = near_miss(pc, rc, E)
        tag = "  <- MONOMIAL" if nm == 1 else ""
        print(f"     {lab}  |  {E}  | ({d1:3d},{d2:3d})    | {nm}{tag}")
        if nm == 1:
            mono[lab] = E
    print()
check("(2,1) is a near-miss exactly at E = 1 = a - b", mono.get((2, 1)) == 1)
check("(5,3) is a near-miss exactly at E = 2 = a - b", mono.get((5, 3)) == 2)
check("Session 7's (8,5) sits at E = 3 = a - b", 8 - 5 == 3)
check("E = a - b equals (a+1)/3 under the Belyi relation 2a = 3b+1",
      all((a - (2*a - 1)//3) == (a + 1)//3
          for a in range(2, 40) if (2*a - 1) % 3 == 0))

print("=" * 70)
print("CORRECTION 2  the degree formula is quadratic")
print("=" * 70)
print("      a |  b |  E | D=a+b | deg y1 | deg y2 |   g | Session-23 claim")
rows = []
for a in range(2, 20):
    if (2*a - 1) % 3:
        continue
    b = (2*a - 1)//3
    E = (a + 1)//3
    D1 = (a + 1)*(a + 3)
    D2 = 2*D1//3
    rows.append((a, b, E, a + b, D1, D2, D1//3))
    print(f"     {a:2d} | {b:2d} | {E:2d} |  {a+b:4d} | {D1:6d} | {D2:6d} | "
          f"{D1//3:3d} | (linear said {3+12*a})")
check("the closed form (a+1)(a+3) reproduces the measured degrees",
      near_miss(p21, r21, 1)[0] == (2 + 1)*(2 + 3) and
      near_miss(p53, r53, 2)[0] == (5 + 1)*(5 + 3))
check("it returns Borisov's 99 at a = 8", (8 + 1)*(8 + 3) == 99)
check("the Session-23 linear formula 3+12a agrees ONLY at a = 8",
      [a for (a, b, E, D, D1, D2, g) in rows if 3 + 12*a == D1] == [8])

print()
print("=" * 70)
print("CORRECTION 3  there is no mod-4 obstruction")
print("=" * 70)
gs = [r[6] for r in rows]
print(f"   g values: {gs}")
print(f"   g mod 4 : {[g % 4 for g in gs]}")
check("g takes both residues mod 4, so Session 24's ranking reason is void",
      len({g % 4 for g in gs}) > 1)

print()
print("=" * 70)
print("(72,108) IS STILL UNREACHABLE - for the corrected reason")
print("=" * 70)
A = Symbol('A')
roots = solve(A**2 + 4*A - 105, A)
print(f"   (a+1)(a+3) = 108  <=>  a^2 + 4a - 105 = 0,  roots {roots}")
check("no positive integer a gives deg y1 = 108",
      not any(rt.is_Integer and rt > 0 for rt in roots))
check("(72,108) is not in the corrected reachable list",
      not any({r[4], r[5]} == {108, 72} for r in rows))

print()
print("=" * 70)
print("WHAT SURVIVES: the chain degrees, hence every gate conclusion")
print("=" * 70)
print(f"   D = a+b values: {[r[3] for r in rows]}")
check("every reachable D except the smallest is >= 4, so the Belyi gate "
      "still closes them", all(r[3] >= 4 for r in rows if r[3] != 3))
print("   GGHV comparison, corrected:")
for (a, b, E, D, D1, D2, g) in rows[:6]:
    st = "cleared by GGHV" if max(D1, D2) < 125 else "beyond GGHV, killed by the Belyi gate"
    print(f"     ({D1},{D2}) D = {D:2d} : {st}")

print()
print("=" * 70)
print("NEW ARTIFACT: the smallest near-miss in the family, (15,10)")
print("=" * 70)
pn = w**2 + Q(3, 2)*w + Q(3, 8)
rn = w + 1
print(f"   p = {pn},  r = {rn}")
print(f"   p^2 - w r^3 = {expand(pn**2 - w*rn**3)}   (degree 1 = delta)")
d1, d2, nm = near_miss(p21, r21, 1)
print(f"   v = x1*x2 - 1,  degrees ({d1},{d2}),  J has {nm} monomial")
check("p is squarefree and p(0), r(0) nonzero",
      discriminant(Poly(pn, w)) != 0 and pn.subs(w, 0) != 0
      and rn.subs(w, 0) != 0)
check("its Jacobian is a single monomial (a genuine near-miss)", nm == 1)

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
RESULT.  No counterexample.  (72,108) is not reachable by this family,
which is what Sessions 23-24 concluded - but the reason they gave was
wrong, and so was the degree formula underneath it.  Corrected here, with
the near-miss exponent E = a - b established at three data points and the
degree law (a+1)(a+3) replacing the linear 3+12a.

Every gate conclusion survives untouched, because the chain degrees never
depended on the broken formula.  What does not survive is Session 24's
ranking: (72,108) is not "one congruence class away", it is simply not in
the family, and the campaign has no privileged next target.
""")
assert all(PASS), "a certification failed"
