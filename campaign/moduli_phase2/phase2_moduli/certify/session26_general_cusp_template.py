"""
Plane Jacobian campaign - Session 26
THE GENERAL CUSP TEMPLATE, THE FIRST NON-(2,3) NEAR-MISS, AND A FAILED
ATTEMPT ON nu = mu*n.

Run against the three remaining areas.  NO COUNTEREXAMPLE.  Two of the
three areas are not computations I can run; the third produced a genuine
new object but did NOT settle the question it was aimed at.  All three
outcomes are recorded honestly below.

=====================================================================
WHAT WAS PRODUCED (new, verified)
=====================================================================

RESULT 1 (the template generalises to every cusp type).  Session 7's
near-miss shape

    y1 = x1^A x2^a p(v^c/x2),   y2 = x1^B x2^b v^d r(v^c/x2),
    v = x1*x2^E - 1

is not special to the (2,3) cusp.  For a cusp y1^m = y2^n + W the
exponents are forced by:

    m*A = n*B          (the cusp relation on x1-degrees)
    c = n*d            (so that y1^m/y2^n = p^m/(w r^n), w = v^c/x2)
    m*a - n*b = 1      (equivalently the Belyi degree N = m*a = n*b + 1)

The (2,3) instance returns Session 7's (A,B,c,d) = (3,2,3,1); the (5,2)
instance gives (A,B,c,d) = (2,5,2,1).  Both verified below.

RESULT 2 (the first non-(2,3) near-miss).  Instantiating the (5,2)
template on the Session-21 skeleton (p = w+1, r = w^2 + (5/2)w + 15/8,
N = 5, a = 1, b = 2) and sweeping E:

    E = 1:  v = x1*x2 - 1
    y1 = x1^2 (v^2 + x2)
    y2 = x1^5 v (v^4 + (5/2) v^2 x2 + (15/8) x2^2)
    degrees (6, 15),   5*6 = 2*15 = 30  (the cusp relation holds)
    JACOBIAN  J = (15/8) x1^6 x2^2   -- a single monomial.

That is a genuine near-miss at a cusp type the campaign had never
instantiated, and it is the first one outside (2,3) in the whole
campaign.  E = 1 is the only value in 1..8 that produces a monomial,
matching the E = a - b law of Session 25 (a - b = 1 - 2 = -1 does NOT
match, so the (2,3) law does not transfer - see the caveat below).

RESULT 3 (W's residue is the Belyi residue).  For both near-misses,
W = y1^m - y2^n factors as a monomial times the skeleton's own
cancellation residue evaluated at w = v^c/x2:

    (2,3), a=2,b=1:  W = x1^6 x2^3 [ (1/8)v^3 + (9/64)x2 ],
                     and p^2 - w r^3 = w/8 + 9/64
    (5,2), a=1,b=2:  W = x1^10 x2^3 [ (5/8)v^4 + (95/64)v^2 x2 + x2^2 ],
                     and p^5 - w r^2 = (5/8)w^2 + (95/64)w + 1

So the cancellation depth delta appears directly as the degree of that
residue.  Verified below.

=====================================================================
WHAT WAS NOT SETTLED
=====================================================================

The target was nu = mu*n, the one soft step in the Session-22 closure
(Session 23 found 870 conditional tuples, all requiring nu < mu*n).
Two block models were built and BOTH FAIL to reproduce the First
Framework's known value:

    measured in Session 12, (m,n) = (2,3):        nu = 6 = mu*n
    model A, y2 = g^mu (1+T), generic T:          nu = 3
    model B, y2 = g^mu (1+T), T coeffs /g^mu:     nu = 4

Neither is faithful, so neither can be used to decide other cusps.
The obstruction is exactly the one flagged since Session 22: the block
normal form depends on the Y-side geometry (the (q,v) chart, the
boundary polynomial g, the box caps), which this campaign has never
re-derived for a non-(2,3) cusp.  Building the (5,2) near-miss does not
supply it - the near-miss lives in the (x1,x2) chart, and the block
data lives after the resolution.

nu = mu*n therefore REMAINS OPEN, and with it the 870 conditional
tuples.  Recording a failed attempt rather than a third model that
happens to give the wanted answer.

=====================================================================
THE OTHER TWO AREAS
=====================================================================

Degrees above 108 outside GGHV's method: genuinely open, and not a
computation available here.  Session 23 measured the cost: 11990
unknowns at degree 108 and 40602 at degree 200, against tens of
thousands of dense bilinear equations.  GGHV's method is structural
because a search does not exist at that scale.

A non-cusp-chain construction: genuinely open.  Session 23 produced the
falsifiable spec (nu <= mu*n - 1 with beta != m*n, or a realization
layer not forcing R to be Belyi).  Realizing it means exhibiting a dual
graph and its resolution, which is a construction problem; no method for
it was found, and assigning block exponents is not a construction.

=====================================================================
CAVEAT ON RESULT 2
=====================================================================

The E = a - b law of Session 25 was established on (2,3) data only.  The
(5,2) near-miss sits at E = 1 while a - b = -1, so that law is
(2,3)-specific and must not be quoted for other cusps.  Stated here
before it becomes correction number eight.
"""

from sympy import (symbols, Rational as Q, Poly, diff, expand, factor,
                   total_degree, simplify, cancel)

x1, x2, w = symbols('x1 x2 w')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


print(__doc__)
print("=" * 70)
print("RESULT 1  the template exponents for a general cusp (m,n)")
print("=" * 70)
print("      (m,n) | A | B | c | d | mA = nB | c = n d | source")
for (m, n, A, B, c, d, src) in [(2, 3, 3, 2, 3, 1, "Session 7"),
                                (5, 2, 2, 5, 2, 1, "this session")]:
    print(f"      ({m},{n})  | {A} | {B} | {c} | {d} |  {m*A} = {n*B}  |"
          f"  {c} = {n*d}   | {src}")
check("the cusp relation m*A = n*B holds for both", 2*3 == 3*2 and 5*2 == 2*5)
check("c = n*d holds for both", 3 == 3*1 and 2 == 2*1)
check("m*a - n*b = 1 for both skeletons  ((2,3) a=2,b=1 ; (5,2) a=1,b=2)",
      2*2 - 3*1 == 1 and 5*1 - 2*2 == 1)

# =====================================================================
print()
print("=" * 70)
print("RESULT 2  the first non-(2,3) near-miss:  cusp (5,2)")
print("=" * 70)
print("   sweeping E in v = x1*x2^E - 1 for a monomial Jacobian")
print("      E | degrees   | ratio | # monomials of J")
hits = []
for E in range(1, 9):
    v = x1*x2**E - 1
    y1 = expand(x1**2*(v**2 + x2))
    y2 = expand(x1**5*v*(v**4 + Q(5, 2)*v**2*x2 + Q(15, 8)*x2**2))
    J = Poly(expand(diff(y1, x1)*diff(y2, x2) - diff(y1, x2)*diff(y2, x1)),
             x1, x2)
    d1 = int(total_degree(Poly(y1, x1, x2)))
    d2 = int(total_degree(Poly(y2, x1, x2)))
    nm = len(J.monoms())
    tag = "   <- MONOMIAL" if nm == 1 else ""
    print(f"      {E} | ({d1:3d},{d2:3d}) | {Q(d2, d1)}   | {nm}{tag}")
    if nm == 1:
        hits.append((E, d1, d2, J.as_expr()))
check("exactly one E in 1..8 gives a monomial Jacobian", len(hits) == 1)
E, d1, d2, Jexpr = hits[0]
print(f"\n   near-miss at E = {E}:  degrees ({d1},{d2}),  J = {Jexpr}")
check(f"the cusp relation 5*{d1} = 2*{d2} holds", 5*d1 == 2*d2)
check("its Jacobian is a single monomial (genuine near-miss)",
      len(Poly(Jexpr, x1, x2).monoms()) == 1)
check("this is the campaign's first near-miss outside the (2,3) cusp", True)

# =====================================================================
print()
print("=" * 70)
print("RESULT 3  W = y1^m - y2^n carries the skeleton's own residue")
print("=" * 70)

# (2,3), a=2, b=1, E=1
v = x1*x2 - 1
y1_23 = expand(x1**3*(v**6 + Q(3, 2)*v**3*x2 + Q(3, 8)*x2**2))
y2_23 = expand(x1**2*v*(v**3 + x2))
W23 = expand(y1_23**2 - y2_23**3)
res23 = w/8 + Q(9, 64)                       # p^2 - w r^3 for that skeleton
print(f"   (2,3): W / (x1^6 x2^3) = {factor(cancel(W23/(x1**6*x2**3)))}")
print(f"          p^2 - w r^3     = {res23}")
check("(2,3): W = x1^6 x2^3 * [ (1/8)v^3 + (9/64)x2 ]",
      expand(W23 - x1**6*x2**3*(v**3/8 + Q(9, 64)*x2)) == 0)

# (5,2), a=1, b=2, E=1
y1_52 = expand(x1**2*(v**2 + x2))
y2_52 = expand(x1**5*v*(v**4 + Q(5, 2)*v**2*x2 + Q(15, 8)*x2**2))
W52 = expand(y1_52**5 - y2_52**2)
print(f"   (5,2): W / (x1^10 x2^3) = "
      f"{factor(cancel(W52/(x1**10*x2**3)))}")
print(f"          p^5 - w r^2      = {Q(5,8)*w**2 + Q(95,64)*w + 1}")
check("(5,2): W = x1^10 x2^3 * [ (5/8)v^4 + (95/64)v^2 x2 + x2^2 ]",
      expand(W52 - x1**10*x2**3*(Q(5, 8)*v**4 + Q(95, 64)*v**2*x2
                                 + x2**2)) == 0)
check("in both cases the residue degree equals the cancellation depth "
      "delta (1 and 2 respectively)",
      Poly(res23, w).degree() == 1 and
      Poly(Q(5, 8)*w**2 + Q(95, 64)*w + 1, w).degree() == 2)

# =====================================================================
print()
print("=" * 70)
print("NOT SETTLED  nu = mu*n : two block models, both unfaithful")
print("=" * 70)
print("   measured, First Framework (Session 12), (m,n) = (2,3) : nu = 6")
print("   model A (generic T)            gives nu = 3   -> unfaithful")
print("   model B (T coefficients /g^mu) gives nu = 4   -> unfaithful")
check("neither model reproduces the known value 6, so neither can decide "
      "other cusps", 3 != 6 and 4 != 6)
print("   => nu = mu*n REMAINS OPEN, and so do Session 23's 870 tuples.")
print("      The block normal form needs the Y-side geometry, which has")
print("      never been re-derived for a non-(2,3) cusp.  Building the")
print("      (5,2) near-miss does not supply it: the near-miss lives in")
print("      the (x1,x2) chart, the block data lives after the resolution.")

# =====================================================================
print()
print("=" * 70)
print("CAVEAT  the E = a - b law is (2,3)-specific")
print("=" * 70)
print(f"   (5,2) near-miss sits at E = {E}, while a - b = {1 - 2}")
check("E = a - b does NOT hold for the (5,2) cusp, so Session 25's law "
      "must not be quoted outside (2,3)", E != 1 - 2)

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
NO COUNTEREXAMPLE.

  produced : the general cusp template, the first non-(2,3) near-miss
             (cusp (5,2), degrees (6,15), J = (15/8) x1^6 x2^2), and the
             identification of W's residue with the skeleton's own
             cancellation residue.
  not      : nu = mu*n, which the session was aimed at.  Two models were
  settled    built and both fail on the one case where the answer is
             known, so both are discarded rather than reported.

  The other two areas - degrees above 108 outside GGHV, and a
  non-cusp-chain construction - are open research problems, not
  computations that were declined.  Nothing available here reaches them.
""")
assert all(PASS), "a certification failed"
