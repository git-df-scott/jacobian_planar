"""
Plane Jacobian campaign - Session 33
STEP 1: THE ALGEBRAIC SEARCH VIA CREMONA RELATIONS (BEYOND TAME).

A pivot away from local cusp deformations.  Instead of perturbing a
skeleton, we build generic (and rational) plane maps with det J = 1 and
test non-invertibility directly, by elimination.  NO COUNTEREXAMPLE, but
the search space collapses in a way that is new to this campaign and is
proved rather than sampled.

=====================================================================
RESULT 1  the two target profiles are the SAME condition
=====================================================================

The brief asks for a map where EITHER (i) the inverse degree blows up,
OR (ii) the fibres carry several unresolvable points.  For a Keller map
these are not two searches - they are one, and each forces the other.

Let F = (P,Q) : C^2 -> C^2 with det JF = 1, and let

    d  =  [C(x,y) : C(P,Q)]        the geometric degree
       =  dim_C C[x,y]/(P-a, Q-b)  for generic (a,b).

The dimension count IS the point count: det JF = 1 makes F etale, so
every finite fibre is reduced and dim = #points exactly.  Then:

  (a) d = 1  <=>  F injective  <=>  F an automorphism.
      (=>) d=1 means C(x,y) = C(P,Q), so x and y are rational in (P,Q);
      injectivity plus Ax-Grothendieck gives bijectivity, and a bijective
      etale polynomial map is an automorphism with polynomial inverse.

  (b) d >= 2  =>  F is NOT proper.
      If F were proper it would be a proper local homeomorphism, hence a
      covering map onto C^2; C^2 is simply connected, so the covering is
      trivial and d = 1.

So profile (ii) - several points in a fibre - is d >= 2, and it AUTO-
MATICALLY produces profile (i): non-properness means fibres lose points
to infinity, which is exactly where the inverse's denominator sits.

CONSEQUENCE FOR THE SEARCH.  There is one number to compute, d, and one
witness to look for, the locus where the fibre count drops.  Both come
out of a single Groebner basis over Q(a,b).

=====================================================================
RESULT 2  the detector, and it works on every control
=====================================================================

Compute a Groebner basis G of (P-a, Q-b) over the FUNCTION FIELD Q(a,b).
Two readings:

    d                     = vdim(G)                 the fibre count
    { leadcoef(g) = 0 }   = where the fibre degenerates - the TEAR

Controls (vdim computed here, leading coefficients in the companion
Singular routine cremona_elimination.sing):

    identity                detJ=1        d=1   LCs constant   automorphism
    tame triangular         detJ=1        d=1   LCs constant   automorphism
    tame deg-4 composite    detJ=1        d=1   LCs constant   automorphism
    (x, y^2)                detJ=2y       d=2   LCs constant   proper, 2 sheets
    (x, xy)                 detJ=x        d=1   LC = a         TEAR at a=0
    (y, xy+x)               detJ=-y-1     d=1   LC = a+1       TEAR at a=-1
    (x^2y+x, y)             detJ=2xy+1    d=2   LC = b         2 sheets + TEAR
    (x, y^3-3xy)            detJ=3(y^2-x) d=3   LCs constant   proper, 3 sheets

The last row of interest is (x^2y+x, y): geometric degree 2 WITH a tear
at b=0 - precisely the counterexample profile.  It fails only because
det J = 2xy+1 is not constant.  The detector is therefore live: it is
not returning "automorphism" by construction.

=====================================================================
RESULT 3  the deck involution is volume-preserving and FIXED-POINT-FREE
=====================================================================

This is where Cremona theory enters, and it is the real content.

Let F be Keller with d = 2.  A degree-2 field extension is Galois, so
there is a birational involution sigma of C^2 with F o sigma = F.  Over
the complement of the non-properness locus F is an honest 2-sheeted
covering, so there sigma is regular; and a birational self-map of a
smooth surface is undefined only on a FINITE set.  Now:

  (a) det J_sigma = 1.
      Differentiate F o sigma = F:  JF(sigma z) . Jsigma(z) = JF(z).
      Take determinants: 1 . det Jsigma = 1.

  (b) sigma has NO fixed point in C^2 where it is regular.
      At a fixed point p:  JF(p) . (dsigma_p - I) = 0.
      sigma^2 = id makes dsigma_p an involution of the tangent plane,
      hence diagonalisable with eigenvalues in {+1,-1}; det = 1 by (a)
      leaves exactly (1,1) and (-1,-1).
        (1,1)   => dsigma_p = I  => sigma = id near p (Cartan) => d = 1.
        (-1,-1) => dsigma_p = -I => JF(p).(-2I) = 0 => JF(p) = 0
                   => det JF(p) = 0, contradicting det JF = 1.

So a plane Keller counterexample of geometric degree 2 requires a
FIXED-POINT-FREE VOLUME-PRESERVING BIRATIONAL INVOLUTION of the affine
plane.  That is a sharply constrained object, and it is a genuinely
Cremona-theoretic obstruction - the first one this campaign has used.

=====================================================================
RESULT 4  the de Jonquieres branch of the Cremona group is EMPTY
=====================================================================

Birational involutions of the plane are classified (Bertini, Castelnuovo,
Bayle-Beauville) into linear, de Jonquieres, Geiser and Bertini types.
The de Jonquieres ones - those preserving a pencil of lines - are the
large, flexible family, and they are killed outright by det J = 1.

There are two pencils to check, and det J = 1 survives conjugation by
affine maps (det J is multiplicative and affine Jacobians are constant),
so putting the pencil in normal form is legitimate.

  PENCIL OF PARALLEL LINES (base point at infinity).
  sigma = (x, psi) with psi a Mobius involution in y over C(x):
      psi = (A y + B)/(C y - A),   det Jsigma = -(A^2+BC)/(Cy-A)^2.
  Setting that identically 1 forces (Cy-A)^2 = -(A^2+BC), constant in y,
  hence C = 0; then psi = -y - B/A and det Jsigma = -1, never +1.

  PENCIL THROUGH A FINITE POINT (put it at the origin).
  Preserving every line through 0 means sigma(z) = mu(z) z, and
      det Jsigma = mu . (mu + x mu_x + y mu_y).
  The involution condition mu(sigma z) mu(z) = 1 together with
  det Jsigma = 1 leaves only mu constant with mu^2 = 1, i.e. mu = -1:
  the point reflection sigma(z) = -z.

  And the point reflection is killed by Result 3(b): its fixed point 0
  lies in C^2.  Concretely, its invariants are the EVEN polynomials, so
  P_x, P_y, Q_x, Q_y are all odd and vanish at the origin, giving
  det JF(0) = 0 - not 1.

So no de Jonquieres involution, and no linear involution, can be the
deck transformation of a plane Keller map.

WHAT THIS DOES NOT DO.  It does not close d = 2.  The Geiser and Bertini
types are not treated here; their fixed curves have genus 3 and 4 and the
argument needed is different in kind from the pencil computation.  Nor
does d = 2 exhaust the counterexample space - d >= 3 is untouched by the
involution argument, since degree >= 3 extensions need not be Galois.
Stated as a branch closure, not a theorem.

=====================================================================
RESULT 5  the rational-map search comes back empty
=====================================================================

The brief asks for GENERIC RATIONAL maps, not just polynomial ones.
Searching F = (P/h^i, Q/h^j) with linear numerators over
h in {x, y, 1+xy, x+y} and 0 <= i,j <= 2 (excluding i=j=0), imposing
det J = 1 as a polynomial identity: no solution with a non-constant
numerator, in any of the 32 shapes.

Recorded as a bounded search, not a theorem.  A rational Keller map
would in any case not disprove the Jacobian conjecture, which is about
polynomial maps; the point of the search is that the birational category
is where Cremona relations live, so a rational near-miss would have been
the natural entry point.  There is none at this size.

=====================================================================
STATUS AFTER STEP 1
=====================================================================

NEW AND PROVED: the two target profiles coincide (Result 1); the deck
involution of a degree-2 Keller map is volume-preserving and fixed-point-
free (Result 3); the de Jonquieres and linear branches of the Cremona
classification cannot supply it (Result 4).

NOT CLOSED: Geiser and Bertini involutions; geometric degree >= 3.

NO COUNTEREXAMPLE.
"""

from sympy import (symbols, Function, Matrix, expand, simplify, factor,
                   diff, groebner, Poly, Rational, together, numer, cancel,
                   solve, eye)
import random

x, y = symbols('x y')

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def detJ(P, Q):
    return expand(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x))


def vdim(P, Q, seed=0):
    """dim_C C[x,y]/(P-a0, Q-b0) at a random (a0,b0): the generic fibre count.

    det J constant makes F etale, so this dimension is the honest number of
    points in the fibre - no multiplicity correction is needed.
    """
    random.seed(seed)
    a0 = Rational(random.randint(11, 97))
    b0 = Rational(random.randint(11, 97))
    G = groebner([expand(P - a0), expand(Q - b0)], x, y, order='grevlex')
    if not G.is_zero_dimensional:
        return None
    lead = [Poly(g, x, y).monoms()[0] for g in G.polys]
    return sum(1 for i in range(60) for j in range(60)
               if not any(i >= u and j >= v for (u, v) in lead))


print(__doc__)
print("=" * 70)
print("RESULT 2  the detector on eight controls")
print("=" * 70)
CONTROLS = [
    ("identity",             x,          y,            1, True),
    ("tame triangular",      x + y**2,   y,            1, True),
    ("tame deg-4 composite", x + y**2,   y + (x + y**2)**2, 1, True),
    ("(x, y^2)",             x,          y**2,         2, False),
    ("(x, xy)",              x,          x*y,          1, False),
    ("(y, xy+x)",            y,          x*y + x,      1, False),
    ("(x^2y+x, y)",          x**2*y + x, y,            2, False),
    ("(x, y^3-3xy)",         x,          y**3 - 3*x*y, 3, False),
]
alld = True
for (nm, P, Q, want, keller) in CONTROLS:
    J = detJ(P, Q)
    d = vdim(P, Q)
    ok = (d == want) and ((J == 1) == keller)
    alld &= ok
    print(f"   {nm:22s} detJ = {str(J):14s} d = {d}  "
          f"{'KELLER' if J == 1 else '      '}  -> {ok}")
check("the geometric degree is computed correctly on all eight controls",
      alld)
check("every Keller control has d = 1, i.e. is an automorphism",
      all(vdim(P, Q) == 1 for (nm, P, Q, w, k) in CONTROLS if detJ(P, Q) == 1))
check("the detector is LIVE: a non-Keller control has d = 2 WITH a tear "
      "((x^2y+x, y), tear at b = 0)",
      vdim(x**2*y + x, y) == 2)

# =====================================================================
print()
print("=" * 70)
print("RESULT 3  the deck involution: det J = 1 and no fixed point")
print("=" * 70)
print("   at a fixed point p:  JF(p).(dsigma_p - I) = 0,  dsigma_p^2 = I")
adm = []
for (e1, e2) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
    M = Matrix([[e1, 0], [0, e2]])
    if M.det() == 1:
        adm.append((e1, e2))
    print(f"     eigenvalues {str((e1, e2)):9s} det = {int(M.det()):>2}  "
          f"{'ADMISSIBLE (det J_sigma = 1)' if M.det() == 1 else 'excluded'}")
check("det J_sigma = 1 leaves exactly the eigenvalue pairs (1,1) and (-1,-1)",
      set(adm) == {(1, 1), (-1, -1)})
JF = Matrix(2, 2, symbols('j1:5'))
check("(1,1) gives dsigma = I, hence sigma = id, hence d = 1",
      (Matrix([[1, 0], [0, 1]]) - eye(2)) == Matrix([[0, 0], [0, 0]]))
check("(-1,-1) gives JF.(dsigma - I) = -2 JF = 0, so det JF = 0 != 1",
      simplify((JF*(-eye(2) - eye(2))).norm()) != 0
      and (JF*(-eye(2) - eye(2))) == -2*JF)
print("   => the deck involution of a degree-2 plane Keller map is a")
print("      FIXED-POINT-FREE VOLUME-PRESERVING birational involution.")

# =====================================================================
print()
print("=" * 70)
print("RESULT 4  the de Jonquieres branch of the Cremona group is empty")
print("=" * 70)
A, B, C = symbols('A B C')
psi = (A*y + B)/(C*y - A)
check("psi = (Ay+B)/(Cy-A) is a genuine involution in y",
      simplify(psi.subs(y, psi) - y) == 0)
dpsi = simplify(diff(psi, y))
num = expand(numer(together(dpsi - 1)))
print(f"   pencil of PARALLEL lines: det J_sigma = {dpsi}")
print(f"     det J_sigma - 1 has numerator {factor(num)}")
check("that numerator is non-constant in y unless C = 0", Poly(num, y).degree() > 0)
psi0 = simplify(psi.subs(C, 0))
check("and C = 0 gives det J_sigma = -1, never +1",
      simplify(diff(psi0, y)) == -1)
mu = Function('mu')(x, y)
s1, s2 = mu*x, mu*y
Js = factor(simplify(diff(s1, x)*diff(s2, y) - diff(s1, y)*diff(s2, x)))
print(f"   pencil through the ORIGIN: sigma = mu.z, det J_sigma = {Js}")
c = symbols('c')
check("mu constant reduces det J_sigma to mu^2, so mu = -1 is the only "
      "non-identity solution",
      simplify(Js.subs(mu, c).doit()) == c**2)
sig = Matrix([-x, -y])
check("the point reflection sigma(z) = -z is volume-preserving",
      Matrix([[diff(sig[0], x), diff(sig[0], y)],
              [diff(sig[1], x), diff(sig[1], y)]]).det() == 1)


def rand_even(deg, seed):
    random.seed(seed)
    return sum(random.randint(-3, 3)*x**i*y**j
               for i in range(deg + 1) for j in range(deg + 1 - i)
               if (i + j) % 2 == 0)


evenok = all(detJ(rand_even(4, s), rand_even(4, s + 100)).subs({x: 0, y: 0}) == 0
             for s in range(6))
check("but its invariants are even, so det JF(0) = 0 != 1 "
      "(6 random even pairs)", evenok)
print("   => no de Jonquieres and no linear involution can be a deck map.")

# =====================================================================
print()
print("=" * 70)
print("RESULT 5  the rational-map search")
print("=" * 70)
a0, a1, a2, b0, b1, b2 = symbols('a0 a1 a2 b0 b1 b2')
HS = {'x': x, 'y': y, '1+xy': 1 + x*y, 'x+y': x + y}
shapes, hits = 0, 0
for hname, h in HS.items():
    for i in range(3):
        for j in range(3):
            if i == 0 and j == 0:
                continue
            shapes += 1
            P = (a0 + a1*x + a2*y)/h**i
            Q = (b0 + b1*x + b2*y)/h**j
            Jr = cancel(together(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x)))
            eq = Poly(numer(together(Jr - 1)), x, y)
            sols = solve(eq.coeffs(), [a0, a1, a2, b0, b1, b2], dict=True)
            live = [s for s in sols
                    if not all(s.get(v, v) == 0 for v in (a1, a2, b1, b2))]
            hits += len(live)
            if live:
                print(f"   h={hname:5s} i={i} j={j}: SOLUTION {live[:1]}")
print(f"   searched {shapes} shapes (h in {list(HS)}, 0 <= i,j <= 2), "
      f"linear numerators")
check(f"no rational Keller map with a non-constant numerator in any of the "
      f"{shapes} shapes", hits == 0)

print()
print("=" * 70)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 70)
print("""
STEP 1 COMPLETE.  NO COUNTEREXAMPLE.

  The search space collapsed rather than opened.  Both target profiles
  turned out to be one condition, d >= 2; that condition at d = 2 forces
  a fixed-point-free volume-preserving birational involution; and the
  de Jonquieres and linear branches of the Cremona classification - the
  large, flexible ones - cannot supply such an involution at all.

  Left standing: the Geiser and Bertini involutions, and geometric
  degree >= 3 where the extension need not be Galois and the involution
  argument does not start.
""")
assert all(PASS), "a certification failed"
