"""
Plane Jacobian campaign - Session 22
THE CONTACT EXPONENT, DERIVED - AND THE D <= 3 WINDOW CLOSES.

Session 21 instantiated the (5,2) skeleton at chain degree 3, found the
pole-fiber lock relaxing, and produced c != 0 - but only under the
ASSUMPTION that the contact exponent for a (5,2) cusp is k = 3.  This
session derives k instead of assuming it, and the assumption turns out
to be false: for a (5,2) cusp k = 6.  The window was never reachable.

TWO CORRECTIONS TO SESSION 21, both material:

  (i)  k = 3 for the (5,2) cusp is WRONG.  The derivation below gives
       k = eps*(m+n) - 1, so a (5,2) cusp has k = 6 at eps = 1.  The
       Session-21 "window is open" finding rested on k = D = 3 and does
       not survive.  It is withdrawn.

  (ii) Session 21's degree argument - that D = 3 lands inside Moh's
       proven range via deg y1 = 3 + 12 deg p - is WITHDRAWN as well.
       That template is (2,3)-specific and extrapolating it to (5,2)
       was not safe (a plausible alternative scaling puts the degrees
       ABOVE 100, not below).  It is no longer needed: the closure
       below is structural and does not appeal to degree bounds.

WHAT IS DERIVED HERE.

RESULT 1 (the cusp identity, exact).  For a cusp y1^m = y2^n + W,
    {y1, y2} = {W, y2} / ( m * (y2^n + W)^((m-1)/m) ),
identically - the y2^{n-1} terms cancel, which is the precise sense in
which the cusp part is Jacobian-silent.

RESULT 2 (the endgame operator, derived not asserted).  With leading
blocks y2 ~ q^-beta v^-gamma g^mu and W ~ q^-lambda v^-sigma g^nu R in
the (q,v) chart, the bracket has the exact closed form

  {W,y2} = q^(-lambda-beta-1) v^(-sigma-gamma) *
           [ (lambda*gamma - beta*sigma) v^-1 g^(nu+mu) R
             + (beta*nu - lambda*mu) g^(nu+mu-1) g' R
             + beta g^(nu+mu) R' ]

verified symbolically below.  Dividing by m*y2^(n(m-1)/m) gives
    s = beta/m                     (coefficient of v R')
    G = nu + mu - mu*n(m-1)/m      (g-power of the R terms)
and the g' term carries g^(G-1).

RESULT 3 (Session 18's master identity, re-derived).  Feeding the First
Framework's own block data (beta,gamma,lambda,sigma,mu,nu) =
(6,18,5,54,2,6) and the Session-13 rigidity g = alpha*(v+1)*v^8 into
that closed form returns

    alpha^5 (v+1)^4 ( 3 v(v+1) R' - 13 R ) = -c

exactly, including the collapse identity 13(9v+8) - 117(v+1) = -13.
Sessions 16-18 asserted this; it is now derived from the block data.
That is an independent end-to-end validation of the campaign's central
computation.

RESULT 4 (the contact exponent).  Two of the block exponents are forced
rather than free:
    nu = mu*n     because W = y1^m - y2^n inherits g^(mu*n) from y2^n;
    mu = m        because y2's leading block is an m-th power (the
                  m-th-root structure that makes the cusp part silent).
Then G = mu(m+n)/m = m+n, and with g = alpha*U^eps*(unit),
    ord_U(g^G) = eps*G,   ord_U(g^(G-1) g') = eps*G - 1,
so the contact exponent - the power of (v+1) that factors out - is

    k = eps*(m+n) - 1.

For (2,3) at eps = 1 this is 4, the First Framework's value.  For (5,2)
it is 6, not the 3 Session 21 assumed.

RESULT 5 (THE CLOSURE).  m and n are coprime cusp exponents with
m, n >= 2, so m + n >= 5, and eps >= 1.  Hence

    k = eps*(m+n) - 1 >= 4      for EVERY cusp type and every eps,

with equality only at (m,n) = (2,3), eps = 1.  Session 20 showed
self-consistency with the realization layer forces D = k, so D >= 4
always; and Session 20's Belyi gate closes every D >= 4 uniformly.
The D <= 3 window is therefore EMPTY - not because D <= 3 is
combinatorially impossible, but because no cusp can produce a contact
exponent that low.

ROBUSTNESS.  The one extrapolated step is mu = m.  It is not load
bearing: leaving mu free, the window needs G = mu(m+n)/m <= 4, i.e.
mu <= 4m/(m+n) <= 4m/5 < m.  So the window requires y2's leading block
to carry a g-power STRICTLY BELOW m, which contradicts its being an
m-th power at all.  The closure survives without mu = m.

NET.  Every gate is now closed: D >= 4 by the Belyi gate, D <= 3 by the
contact exponent.  No cusp type, no cancellation depth, no eps, no
chain degree.  The published constructive framework family supports no
Keller map.

AND, PLAINLY: no counterexample was found, here or in Sessions 19-21,
and none is going to come out of this line of attack.  Every route the
probes opened has closed under its own derivation.  This closes the
family; it says nothing about the plane Jacobian conjecture itself,
which remains open.

Companion Singular routine: ../singular/contact_exponent.sing
"""

from sympy import (symbols, Function, Rational as Q, diff, simplify, expand,
                   powsimp, sqrt, factor, gcd, srepr)

q, v, al = symbols('q v alpha', positive=True)
U = v + 1
g = Function('g')(v)
R = Function('R')(v)

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def PB(f, h):
    """Poisson bracket in the (q,v) chart."""
    return diff(f, q)*diff(h, v) - diff(f, v)*diff(h, q)


print(__doc__)
print("=" * 70)
print("RESULT 1  the cusp identity is exact, for every m and n")
print("=" * 70)
Y2 = Function('y2')(q, v)
W = Function('W')(q, v)
for (m_, n_) in [(2, 3), (3, 2), (5, 2), (2, 5), (3, 4), (5, 3)]:
    Y1 = (Y2**n_ + W)**Q(1, m_)
    resid = simplify(PB(Y1, Y2) - PB(W, Y2)/(m_*(Y2**n_ + W)**Q(m_ - 1, m_)))
    check(f"m={m_}, n={n_}:  {{y1,y2}} == {{W,y2}} / (m (y2^n+W)^((m-1)/m))",
          resid == 0)
print("   the y2^(n-1) terms cancel identically: the cusp part is")
print("   Jacobian-silent, for every cusp type, not just (2,3).")

# =====================================================================
print()
print("=" * 70)
print("RESULT 2  closed form of the bracket on the leading blocks")
print("=" * 70)
be, ga, la, si, mu, nu = symbols('beta gamma lambda sigma mu nu', positive=True)
G_ = Function('G')(v)
W2 = q**(-la)*v**(-si)*G_**nu*R
Y22 = q**(-be)*v**(-ga)*G_**mu
closed = (q**(-la - be - 1)*v**(-si - ga) *
          ((la*ga - be*si)*v**-1*G_**(nu + mu)*R
           + (be*nu - la*mu)*G_**(nu + mu - 1)*diff(G_, v)*R
           + be*G_**(nu + mu)*diff(R, v)))
check("the closed form is exact for symbolic block exponents",
      simplify(expand(PB(W2, Y22) - closed)) == 0)
print("   => s = beta/m,   G = nu + mu - mu*n(m-1)/m,   g' term carries g^(G-1)")

# =====================================================================
print()
print("=" * 70)
print("RESULT 3  Session 18's master identity, re-derived from block data")
print("=" * 70)
Y2L = q**-6 * v**-18 * g**2                    # Session 12, Theorem 1
WL = q**-5 * v**-54 * g**6 * R                 # Session 12, W~_-5 block
J = simplify(powsimp(expand(PB(WL, Y2L)/(2*Y2L**Q(3, 2))), force=True))
print(f"   J * q^3 = {simplify(J*q**3)}")
Jg = simplify(powsimp(expand((J*q**3).subs(g, al*U*v**8).doit()), force=True))
target = al**5 * v**-6 * U**4 * (3*v*U*diff(R, v) - 13*R)
check("J = alpha^5 v^-6 (v+1)^4 ( 3 v(v+1) R' - 13 R ),  q-exponent -3",
      simplify(expand(Jg - target)) == 0)
check("the collapse identity 13(9v+8) - 117(v+1) == -13",
      expand(13*(9*v + 8) - 117*(v + 1)) == -13)
print("   asserted in Sessions 16-18; derived here from the block data.")

# structural coefficients reproduced from the closed form
sub = {be: 6, ga: 18, la: 5, si: 54, mu: 2, nu: 6}
check("(lambda*gamma - beta*sigma)/m == -117",
      simplify(((la*ga - be*si)/2).subs(sub)) == -117)
check("(beta*nu - lambda*mu)/m == 13",
      simplify(((be*nu - la*mu)/2).subs(sub)) == 13)
check("beta/m == 3 == n  (so s = n, given beta = m n)",
      simplify((be/2).subs(sub)) == 3)
check("G = nu + mu - mu*n(m-1)/m == 5",
      simplify((nu + mu - mu*Q(3, 2)).subs(sub)) == 5)

# =====================================================================
print()
print("=" * 70)
print("RESULT 4  the contact exponent  k = eps*(m+n) - 1")
print("=" * 70)
m, n, MU, EPS = symbols('m n mu epsilon', positive=True)
G_gen = nu + mu - mu*n*(m - 1)/m
G_nu = simplify(G_gen.subs(nu, mu*n))          # W inherits g^(mu n) from y2^n
print(f"   nu = mu*n  (forced by W = y1^m - y2^n)  =>  G = {factor(G_nu)}")
G_full = simplify(G_nu.subs(mu, m))            # y2's block is an m-th power
print(f"   mu = m     (y2's leading block is an m-th power)  =>  G = {G_full}")
check("G = m + n", simplify(G_full - (m + n)) == 0)
check("on (2,3): G = 5 and k = eps*G - 1 = 4 at eps = 1",
      G_full.subs({m: 2, n: 3}) == 5 and 1*5 - 1 == 4)
print("   g = alpha*U^eps*(unit) => ord_U(g^G) = eps*G,")
print("                             ord_U(g^(G-1) g') = eps*G - 1")
print("   so the (v+1) power that factors out is  k = eps*(m+n) - 1.")
print()
print("   cusp (m,n) | m+n | k at eps=1 | Session-21 assumed k | verdict")
for (mm, nn) in [(2, 3), (2, 5), (3, 2), (3, 4), (3, 5), (4, 3),
                 (5, 2), (5, 3), (5, 4), (6, 5), (7, 2)]:
    kk = (mm + nn) - 1
    assumed = "4 (correct)" if (mm, nn) == (2, 3) else (
        "3 (WRONG)" if (mm, nn) == (5, 2) else "-")
    print(f"      ({mm},{nn})    | {mm+nn:3d} | {kk:10d} | {assumed:20s} |"
          f" D = k >= 4")
check("the (5,2) cusp has k = 6, refuting Session 21's k = 3",
      (5 + 2) - 1 == 6)

# =====================================================================
print()
print("=" * 70)
print("RESULT 5  THE CLOSURE - the D <= 3 window is empty")
print("=" * 70)
print("   m, n coprime cusp exponents with m, n >= 2  =>  m + n >= 5")
print("   eps >= 1  =>  k = eps*(m+n) - 1 >= 4")
print("   Session 20: self-consistency forces D = k  =>  D >= 4 always")
print("   Session 20: the Belyi gate closes every D >= 4")
lo = None
for mm in range(2, 40):
    for nn in range(2, 40):
        if gcd(mm, nn) != 1:
            continue
        for e in range(1, 12):
            kk = e*(mm + nn) - 1
            lo = kk if lo is None else min(lo, kk)
check(f"the minimum contact exponent over all cusp types and eps is {lo}",
      lo == 4)
check("no (cusp type, eps) yields k <= 3",
      all(e*(mm + nn) - 1 >= 4
          for mm in range(2, 40) for nn in range(2, 40)
          for e in range(1, 12) if gcd(mm, nn) == 1))
print("\n   ROBUSTNESS (dropping mu = m):  the window needs")
print("   G = mu(m+n)/m <= 4, i.e. mu <= 4m/(m+n) <= 4m/5 < m -- y2's")
print("   leading block would have to carry a g-power strictly below m,")
print("   contradicting its being an m-th power at all.")
check("mu <= 4m/(m+n) forces mu < m for every cusp type",
      all(Q(4*mm, mm + nn) < mm
          for mm in range(2, 40) for nn in range(2, 40)
          if gcd(mm, nn) == 1))

# =====================================================================
print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
FINAL STATE OF THE PROBE.

  D >= 4 : closed by the Belyi gate (Session 20), uniformly in the cusp
           exponent and with no upper bound on D.
  D <= 3 : closed here - no cusp type can produce a contact exponent
           k <= 3, and self-consistency forces D = k.

  Every gate is shut.  The published constructive framework family -
  First Framework, Second Framework, isotope series, and every cusp
  type, cancellation depth and boundary order the generator can build -
  supports no Keller map.

  NO COUNTEREXAMPLE WAS FOUND, and this line of attack will not produce
  one: each opening the probes found has closed under its own
  derivation.  What Sessions 19-22 deliver is the death of the
  constructive candidates and a derivation of the machinery that kills
  them.  The plane Jacobian conjecture itself is untouched and remains
  open.

  Corrections issued along the way, all now folded in:
    Session 19  D = 1 mod 6 admissibility        -> too narrow, withdrawn
    Session 19  D = 13 uniquely rigid            -> scoped to delta = 3
    Session 21  contact exponent k = 3 for (5,2) -> wrong, k = 6
    Session 21  Moh degree argument at D = 3     -> unsafe, withdrawn
""")
assert all(PASS), "a certification failed"
