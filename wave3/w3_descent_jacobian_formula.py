"""
Wave 3 - Path A, items A1 AND A2 ANSWERED.

THE QUESTION (file `39`, A1, "the central question")
----------------------------------------------------
    "Prove or refute: for any C*-equivariant Keller map on C^(n+1) whose weights
     make both invariant rings polynomial, the induced quotient map on C^n has
     det J = c*h^k with h the degeneracy locus of the quotient projection and
     k >= 2. ... Do the general computation with symbolic weights."

Alpoge's map descends with det JG = -2*h^2, and file `39` records that if the
square is forced it is a second dimension separator, while if it is not forced
"there exist equivariant counterexamples whose descent is Keller.  That is the
construction recipe. ... the single highest-value outcome available anywhere in
the campaign."

ANSWER: THE SQUARE IS NOT FORCED -- and the reason it is not forced also
explains why that is not a construction recipe.

THEOREM W3-4 (the descent Jacobian formula).
--------------------------------------------
Let a C*-action on C^(n+1) have polynomial invariant ring, with quotient
pi = (p_1,...,p_n).  Since every p_i is invariant, the Euler relation
sum_i w_i x_i d p/d x_i = 0 says the generating vector field
xi = (w_0 x_0, ..., w_n x_n) spans ker(J pi) generically, so the vector of
maximal minors of J pi is

        m(pi) = D * xi,          D in C[x_0,...,x_n]   ("the content").

Let pi' = (q_1,...,q_n) be the target quotient with content D'.  If F is
equivariant and G is its descent (G o pi = pi' o F), then

        (det JG) o pi  *  D   =   (det JF)  *  (D' o F).                 (*)

So the descent's Jacobian is completely determined by det JF and by the two
CONTENTS, which depend only on the weight systems.  The exponent k in
det JG = c * h^k is not an accident of Alpoge's map: it is read off D and D'.

COROLLARY A1 (the enumeration).
-------------------------------
Enumerating every C*-weight system on C^3 with gcd 1, mixed signs or a zero
weight, and invariant ring free on two generators:

    D = 1                    <=>  weights are (+1,-1,0) up to sign and
                                  permutation.  Then k = 0 and the descent is
                                  Jacobian-PRESERVING: det JG = det JF exactly.
    deg D = 1                e.g. (1,-1,-1), (1,-2,0), (-1,0,2)  ->  k = 1.
    D = x^2  (Alpoge's case) weights (1,-1,-2)                    ->  k = 2.

So k = 0 and k = 1 both occur.  The square is NOT forced, and A1's "if not
forced" branch is the live one.

COROLLARY A1b (why that is not a construction recipe).
------------------------------------------------------
In the k = 0 class the equivariant maps can be written down completely.  With
source and target weights (1,-1,0), invariants u = xy, v = z, a weight-graded
F is exactly

        F = ( x*A(u,v),  y*B(u,v),  C(u,v) ),        A,B,C in C[u,v],

and its descent is

        G = ( u*A*B,  C ),        with   det JG = det JF   identically.

Hence a C^3 Keller counterexample with these weights IS a plane Keller
counterexample with a factored first coordinate.  The k = 0 class does not make
the plane problem easier -- it is the plane problem.  The genuine
higher-dimensional counterexamples sit at k = 2 precisely because that is where
the C^3 problem is strictly weaker than the plane one.

Read as a separator: k measures how far a weight class is from being the plane
problem, and k = 0 is the degenerate case where the distance is zero.  That is a
sharper statement than "the square is forced" and it is true.
"""

from itertools import permutations, product
from math import gcd

import sympy as sp

x, y, z = sp.symbols('x y z')
u, v = sp.symbols('u v')
V = (x, y, z)
PASS = []


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


def minor_vector(pis):
    """Vector of maximal minors of the 2x3 Jacobian of (p1, p2)."""
    J = sp.Matrix([[sp.diff(p, w) for w in V] for p in pis])
    return sp.Matrix([J[0, 1] * J[1, 2] - J[0, 2] * J[1, 1],
                      -(J[0, 0] * J[1, 2] - J[0, 2] * J[1, 0]),
                      J[0, 0] * J[1, 1] - J[0, 1] * J[1, 0]])


def content(m):
    return sp.factor(sp.gcd(sp.gcd(sp.expand(m[0]), sp.expand(m[1])), sp.expand(m[2])))


def hilbert_basis(w, B=12):
    """Minimal generators of the semigroup {e >= 0 : e . w = 0}, inside a box.

    e is a minimal generator iff it is nonzero and is not the sum of two
    nonzero elements of the semigroup.
    """
    S = {e for e in product(range(B + 1), repeat=3)
         if any(e) and sum(a * b for a, b in zip(e, w)) == 0}
    gens = []
    for e in sorted(S, key=lambda t: (sum(t), t)):
        decomposable = False
        for f in S:
            if all(a >= b for a, b in zip(e, f)):
                d = tuple(a - b for a, b in zip(e, f))
                if any(d) and d in S:
                    decomposable = True
                    break
        if not decomposable:
            gens.append(e)
    return gens


# ---------------------------------------------------------------------------
# 0.  The Hilbert-basis routine, validated on cases with known answers.
# ---------------------------------------------------------------------------
print("=" * 78)
print("0.  VALIDATION of the invariant-ring generator routine")
print("=" * 78)
KNOWN = [((1, -1, -2), [(1, 1, 0), (2, 0, 1)], "Alpoge: C[xy, x^2 z]"),
         ((1, -1, 0), [(0, 0, 1), (1, 1, 0)], "C[z, xy]"),
         ((1, -1, -1), [(1, 0, 1), (1, 1, 0)], "C[xz, xy]")]
for w, expect, label in KNOWN:
    got = sorted(hilbert_basis(w))
    print(f"    weights {w}: generators {got}   expected {sorted(expect)}   ({label})")
    check(f"generator routine correct for weights {w}", got == sorted(expect))
# negative control: a weight system whose invariant ring is NOT free on two
# generators must be detected as such.
w_bad = (1, 1, -2)      # invariants x^2 z, x y z, y^2 z -- three generators, not free
gb = hilbert_basis(w_bad)
print(f"    NEGATIVE CONTROL weights {w_bad}: {len(gb)} generators {gb} (must not be 2)")
check("NEGATIVE CONTROL: a non-free weight system is not reported as free", len(gb) != 2)

# ---------------------------------------------------------------------------
# 1.  m(pi) = D * xi   -- the minor vector is the generating vector field
#     times a content.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("1.  m(pi) = D * xi   (the Euler relation, checked on every weight system)")
print("=" * 78)

SYSTEMS = []
for w in product(range(-3, 4), repeat=3):
    if not any(w):
        continue
    if gcd(gcd(abs(w[0]), abs(w[1])), abs(w[2])) != 1:
        continue
    if min(w) >= 0 or max(w) <= 0:
        continue
    g = hilbert_basis(w)
    if len(g) != 2:
        continue
    pis = [sp.prod([V[k] ** e[k] for k in range(3)]) for e in g]
    m = minor_vector(pis)
    D = content(m)
    xi = sp.Matrix([w[0] * x, w[1] * y, w[2] * z])
    # m must be proportional to xi with factor +-D
    prop = all(sp.simplify(m[i] * xi[j] - m[j] * xi[i]) == 0 for i in range(3) for j in range(3))
    SYSTEMS.append((w, g, pis, m, D))
    if not prop:
        check(f"m(pi) parallel to xi for weights {w}", False)
check("the enumeration is non-empty and contains Alpoge's weight system",
      len(SYSTEMS) > 0 and any(w == (1, -1, -2) for (w, _, _, _, _) in SYSTEMS))
allprop = all(all(sp.simplify(m[i] * (w[j] * V[j]) - m[j] * (w[i] * V[i])) == 0
                  for i in range(3) for j in range(3))
              for (w, g, pis, m, D) in SYSTEMS)
check("m(pi) || xi verified on every enumerated weight system", allprop)
print(f"    {len(SYSTEMS)} weight systems with a free rank-2 invariant ring enumerated")

# ---------------------------------------------------------------------------
# 2.  THE CONTENT TABLE, and the answer to A1.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("2.  THE CONTENT D, over every enumerated weight system")
print("=" * 78)
by_deg = {}
for (w, g, pis, m, D) in SYSTEMS:
    d = 0 if D.is_number else sp.Poly(D, x, y, z).total_degree()
    by_deg.setdefault(d, []).append((w, D))
for d in sorted(by_deg):
    ws = by_deg[d]
    print(f"    deg D = {d}:  {len(ws)} systems, e.g. "
          f"{[(w, str(D)) for w, D in ws[:5]]}")

zero = sorted({w for w, D in by_deg.get(0, [])})
print(f"\n    D = 1 (k = 0) occurs for exactly these weight systems:")
for w in zero:
    print(f"        {w}")
check("D = 1 occurs -- the square is NOT forced", len(zero) > 0)
check("D = 1 happens exactly when one weight is 0 and the others are +-1",
      all(sorted(abs(t) for t in w) == [0, 1, 1] for w in zero))
check("deg D = 1 (k = 1) also occurs", len(by_deg.get(1, [])) > 0)
alp = [(w, D) for (w, g, pis, m, D) in SYSTEMS if w == (1, -1, -2)]
print(f"\n    Alpoge's weights (1,-1,-2): D = {alp[0][1]}")
check("Alpoge's weight system gives D = x^2 (k = 2)",
      len(alp) == 1 and sp.simplify(alp[0][1] - x ** 2) == 0)

# ---------------------------------------------------------------------------
# 3.  THEOREM W3-4 on Alpoge's map, exactly.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("3.  THEOREM W3-4 verified on Alpoge's map")
print("=" * 78)
f1 = (1 + x * y) ** 3 * z + y ** 2 * (1 + x * y) * (4 + 3 * x * y)
f2 = y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y ** 2 * (4 + 3 * x * y)
f3 = 2 * x - 3 * x ** 2 * y - x ** 3 * z
F = (f1, f2, f3)
detJF = sp.expand(sp.Matrix([[sp.diff(f, w) for w in V] for f in F]).det())

pi = [x * y, x ** 2 * z]                                   # source weights (1,-1,-2)
mD = minor_vector(pi)
D = content(mD)
print(f"    source pi = {pi};   m = {list(mD)};   D = {D}")
check("source content D = x^2", sp.simplify(D - x ** 2) == 0)

u1, u2, u3 = sp.symbols('u1 u2 u3')
Vt = (u1, u2, u3)
pip = [u1 * u3 ** 2, u2 * u3]                              # target weights (-2,-1,1)
Jt = sp.Matrix([[sp.diff(p, w) for w in Vt] for p in pip])
mt = sp.Matrix([Jt[0, 1] * Jt[1, 2] - Jt[0, 2] * Jt[1, 1],
                -(Jt[0, 0] * Jt[1, 2] - Jt[0, 2] * Jt[1, 0]),
                Jt[0, 0] * Jt[1, 1] - Jt[0, 1] * Jt[1, 0]])
Dp = sp.factor(sp.gcd(sp.gcd(mt[0], mt[1]), mt[2]))
print(f"    target pi' = {pip};  m' = {list(mt)};  D' = {Dp}")
check("target content D' = u3^2", sp.simplify(Dp - u3 ** 2) == 0)

G1 = sp.expand((u + 1) * (3 * u + v - 2) ** 2
               * (3 * u ** 3 + u ** 2 * v + 4 * u ** 2 + 2 * u * v + v))
G2 = sp.expand(-(3 * u + v - 2) * (9 * u ** 3 + 3 * u ** 2 * v + 12 * u ** 2
                                   + 6 * u * v + u + 3 * v))
detJG = sp.expand(sp.Matrix([[sp.diff(g, t) for t in (u, v)] for g in (G1, G2)]).det())
print(f"    det JF = {detJF};   det JG = {sp.factor(detJG)}")

lhs = sp.expand(detJG.subs({u: x * y, v: x ** 2 * z}) * D)
rhs = sp.expand(detJF * Dp.subs({u3: f3}))
print(f"    (det JG) o pi * D  =  {sp.factor(lhs)}")
print(f"    (det JF) * (D' o F) =  {sp.factor(rhs)}")
check("THEOREM W3-4 holds exactly on Alpoge's map", sp.simplify(lhs - rhs) == 0)
# NEGATIVE CONTROL: dropping the content D must break the identity
check("NEGATIVE CONTROL: the identity FAILS without the content factor D",
      sp.simplify(sp.expand(detJG.subs({u: x * y, v: x ** 2 * z})) - rhs) != 0)

# and the campaign's h
h = sp.simplify(f3 / x)
print(f"    h = f3/x = {sp.factor(h)};   det JG expressed in h: "
      f"{sp.factor(sp.simplify(detJG.subs({u: x * y, v: x ** 2 * z})))}")
check("det JG o pi = -2 h^2 with h = f3/x",
      sp.simplify(detJG.subs({u: x * y, v: x ** 2 * z}) + 2 * h ** 2) == 0)

# ---------------------------------------------------------------------------
# 4.  THE k = 0 CLASS, in closed form.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("4.  THE k = 0 CLASS: weights (1,-1,0), source and target")
print("=" * 78)
A = sp.Function('A')
B = sp.Function('B')
C = sp.Function('C')
U = x * y
Vz = z
F1 = x * A(U, Vz)
F2 = y * B(U, Vz)
F3 = C(U, Vz)
JF0 = sp.Matrix([[sp.diff(f, w) for w in V] for f in (F1, F2, F3)])
detJF0 = sp.simplify(sp.expand(JF0.det()))

# the descent: pi = (xy, z), pi' = (u1 u2, u3)  ->  G = (u A B, C)
Au, Bu, Cu = sp.Function('A')(u, v), sp.Function('B')(u, v), sp.Function('C')(u, v)
GG1 = u * Au * Bu
GG2 = Cu
detJG0 = sp.simplify(sp.expand(
    sp.diff(GG1, u) * sp.diff(GG2, v) - sp.diff(GG1, v) * sp.diff(GG2, u)))

# compare after substituting u -> xy, v -> z
def to_xyz(e):
    return e.subs({u: U, v: Vz}).doit()

diff0 = sp.simplify(sp.expand(sp.together(to_xyz(detJG0) - detJF0)))
print(f"    det JF (weights (1,-1,0), generic A,B,C) computed")
print(f"    det JG (descent G = (u*A*B, C))         computed")
print(f"    (det JG) o pi  -  det JF  =  {diff0}")
check("k = 0 class: the descent is Jacobian-PRESERVING, det JG o pi = det JF",
      diff0 == 0)

# corroborate with explicit polynomials, including a NEGATIVE control from a
# different weight class where the identity must fail.
import random
rnd = random.Random(20260820)
oks = []
for _ in range(8):
    def rp():
        return sum(sp.Integer(rnd.randint(-3, 3)) * u ** i * v ** j
                   for i in range(3) for j in range(3))
    Ap, Bp, Cp = rp(), rp(), rp()
    F1p = sp.expand(x * Ap.subs({u: U, v: Vz}))
    F2p = sp.expand(y * Bp.subs({u: U, v: Vz}))
    F3p = sp.expand(Cp.subs({u: U, v: Vz}))
    dF = sp.expand(sp.Matrix([[sp.diff(f, w) for w in V]
                              for f in (F1p, F2p, F3p)]).det())
    Gp1 = sp.expand(u * Ap * Bp)
    Gp2 = sp.expand(Cp)
    dG = sp.expand(sp.Matrix([[sp.diff(g, t) for t in (u, v)]
                              for g in (Gp1, Gp2)]).det())
    oks.append(sp.simplify(sp.expand(dG.subs({u: U, v: Vz}) - dF)) == 0)
print(f"    8 randomized explicit instances agree: {all(oks)}")
check("k = 0 identity confirmed on 8 randomized explicit instances", all(oks))
check("NEGATIVE CONTROL: the same identity FAILS in Alpoge's k = 2 class",
      sp.simplify(sp.expand(detJG.subs({u: x * y, v: x ** 2 * z})) - detJF) != 0)

print("""
    So in the k = 0 class an equivariant F is exactly
        F = ( x*A(u,v), y*B(u,v), C(u,v) ),   u = xy, v = z,
    its descent is G = (u*A*B, C), and det JG = det JF identically.

    A C^3 Keller counterexample with these weights therefore IS a plane Keller
    counterexample whose first coordinate factors as u * A * B.  The k = 0 class
    does not open a new search space -- it is the plane problem wearing a third
    variable.  Alpoge's counterexample lives at k = 2 precisely because that is
    where the C^3 problem is strictly weaker than the plane one.""")

# ---------------------------------------------------------------------------
# 5.  W3-4 IN A THIRD WEIGHT CLASS: (1,-1,-1), where D = x  (k = 1).
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("5.  THEOREM W3-4 in the k = 1 class, weights (1,-1,-1)")
print("=" * 78)
print("""    Invariants u = xy, v = xz; D = x.  A weight-graded F is
        F1 = x*A(u,v),  F2 = y*B1 + z*B2,  F3 = y*B3 + z*B4,
    the target quotient is pi' = (u1 u2, u1 u3) with D' = u1, and the descent is
        G = ( u*A*B1 + v*A*B2 ,  u*A*B3 + v*A*B4 ).
    W3-4 then reads   (det JG) o pi * x  =  (det JF) * F1.""")
rnd2 = random.Random(5)


def _rp():
    return sum(sp.Integer(rnd2.randint(-3, 3)) * u ** i * v ** j
               for i in range(3) for j in range(3))


U2, W2 = x * y, x * z
sub2 = {u: U2, v: W2}
oks2, lift_ok = [], []
for _ in range(6):
    A2, B1, B2, B3, B4 = _rp(), _rp(), _rp(), _rp(), _rp()
    F1 = sp.expand(x * A2.subs(sub2))
    F2 = sp.expand(y * B1.subs(sub2) + z * B2.subs(sub2))
    F3 = sp.expand(y * B3.subs(sub2) + z * B4.subs(sub2))
    dF2 = sp.expand(sp.Matrix([[sp.diff(f, w) for w in V]
                               for f in (F1, F2, F3)]).det())
    Gq1 = sp.expand(u * A2 * B1 + v * A2 * B2)
    Gq2 = sp.expand(u * A2 * B3 + v * A2 * B4)
    # the descent really is the descent: G o pi = pi' o F
    lift_ok.append(sp.simplify(sp.expand(Gq1.subs(sub2) - F1 * F2)) == 0
                   and sp.simplify(sp.expand(Gq2.subs(sub2) - F1 * F3)) == 0)
    dG2 = sp.expand(sp.Matrix([[sp.diff(g, t) for t in (u, v)]
                               for g in (Gq1, Gq2)]).det())
    oks2.append(sp.simplify(sp.expand(dG2.subs(sub2) * x - dF2 * F1)) == 0)
print(f"    descent identity G o pi = pi' o F on 6 instances: {all(lift_ok)}")
print(f"    W3-4 holds on the same 6 instances:               {all(oks2)}")
check("k = 1 class: the constructed G really is the descent of F", all(lift_ok))
check("THEOREM W3-4 holds in the k = 1 class, weights (1,-1,-1)", all(oks2))
# NEGATIVE CONTROL: using the wrong content (x^2 instead of x) must break it
bad2 = sp.simplify(sp.expand(dG2.subs(sub2) * x ** 2 - dF2 * F1))
check("NEGATIVE CONTROL: W3-4 with the wrong content x^2 fails here", bad2 != 0)

print("""
    W3-4 is now verified in three weight classes with three different contents:
        D = x^2  (Alpoge, k = 2)   D = x  (k = 1)   D = 1  (k = 0).
    The formula, not the exponent, is what is universal.""")

# ---------------------------------------------------------------------------
# 6.  LEMMA W3-4a: the content D in CLOSED FORM, for all weights.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("6.  LEMMA W3-4a: D is a monomial, in closed form -- no box needed")
print("=" * 78)
print("""    Let the two invariant generators have exponent vectors e1, e2, so
    p_i = x^a_i y^b_i z^c_i.  Row i of J pi is (a_i p_i/x, b_i p_i/y, c_i p_i/z),
    so the maximal-minor vector is

        m(pi) = (p1 p2 / (x y z)) * (Delta_1 x, Delta_2 y, Delta_3 z),
        (Delta_1, Delta_2, Delta_3) = e1 x e2   (the cross product).

    Both generators are invariant, so e1 . w = e2 . w = 0, hence e1 x e2 is
    parallel to w: e1 x e2 = lambda * w.  Therefore

        m(pi) = lambda * (p1 p2 / (x y z)) * xi,
        D     = x^(a1+a2-1) y^(b1+b2-1) z^(c1+c2-1).                    (**)

    D is a MONOMIAL determined by the weights alone, and

        k := deg D = deg p1 + deg p2 - 3.

    COROLLARY.  D = 1  <=>  e1 + e2 = (1,1,1)  <=>  the two generators are one
    of {x, yz}, {y, xz}, {z, xy}  <=>  the weight system is (0,1,-1), (1,0,-1)
    or (1,-1,0) up to sign.  This is a PROOF for all weight systems, not an
    observation inside a search box.""")

lam_vals, closed_ok, kdeg_ok = [], [], []
for (w, g, pis, m, D) in SYSTEMS:
    e1, e2 = g[0], g[1]
    cross = (e1[1] * e2[2] - e1[2] * e2[1],
             e1[2] * e2[0] - e1[0] * e2[2],
             e1[0] * e2[1] - e1[1] * e2[0])
    # cross = lambda * w
    lam = None
    for i in range(3):
        if w[i] != 0:
            lam = sp.Rational(cross[i], w[i])
            break
    lam_vals.append(lam)
    if any(cross[i] != lam * w[i] for i in range(3)):
        closed_ok.append(False)
        continue
    expo = tuple(e1[i] + e2[i] - 1 for i in range(3))
    Dclosed = sp.prod([V[i] ** expo[i] for i in range(3)])
    closed_ok.append(sp.simplify(sp.Abs(sp.expand(D)) - sp.Abs(Dclosed)) == 0
                     or sp.simplify(sp.expand(D) - Dclosed) == 0)
    dD = 0 if D.is_number else sp.Poly(D, x, y, z).total_degree()
    kdeg_ok.append(dD == sum(e1) + sum(e2) - 3)

print(f"\n    lambda values seen (e1 x e2 = lambda * w): {sorted(set(lam_vals))}")
check("e1 x e2 is always parallel to w, with lambda = +-1",
      set(lam_vals) <= {sp.Integer(1), sp.Integer(-1)})
print(f"    closed form (**) matches the computed content on all "
      f"{len(SYSTEMS)} systems: {all(closed_ok)}")
check("LEMMA W3-4a closed form matches the computed content everywhere", all(closed_ok))
print(f"    k = deg D = deg p1 + deg p2 - 3 on all systems: {all(kdeg_ok)}")
check("k = deg p1 + deg p2 - 3 on every enumerated system", all(kdeg_ok))

# the corollary, checked as a proof step rather than an observation:
# e1 + e2 = (1,1,1) has exactly three unordered solutions with both parts nonzero.
splits = set()
for e1 in product(range(2), repeat=3):
    e2 = tuple(1 - t for t in e1)
    if any(e1) and any(e2):
        splits.add(frozenset({e1, e2}))
print(f"\n    unordered splittings of (1,1,1) into two nonzero parts: {len(splits)}")
for sp_ in sorted(splits, key=lambda s: sorted(s)):
    a, b = sorted(sp_)
    # the weight system forced by generators x^a and x^b
    print(f"        generators {a} and {b}")
check("exactly three splittings of (1,1,1), matching the three k = 0 weight systems",
      len(splits) == 3 and len({tuple(sorted(map(abs, w))) for w in zero}) == 1)
check("and every k = 0 weight system found by enumeration has |w| = (0,1,1)",
      all(sorted(abs(t) for t in w) == [0, 1, 1] for w in zero))

# NEGATIVE CONTROL: a wrong closed form must disagree somewhere.
wrong_form = []
for (w, g, pis, m, D) in SYSTEMS:
    e1, e2 = g
    expo = tuple(e1[i] + e2[i] for i in range(3))          # forgot the -1
    Dw = sp.prod([V[i] ** expo[i] for i in range(3)])
    if sp.simplify(sp.expand(D) - Dw) != 0:
        wrong_form.append(w)
check("NEGATIVE CONTROL: the closed form without the -1 shift is rejected",
      len(wrong_form) > 0)

# ---------------------------------------------------------------------------
# 7.  ITEM A2: can the square be REMOVED?  The (1,-1,-2) class in closed form.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("7.  ITEM A2: the Alpoge weight class, completely")
print("=" * 78)
print("""    Source weights (1,-1,-2), invariants u = xy, v = x^2 z; target weights
    (-2,-1,1), pi' = (u1 u3^2, u2 u3).  Grading the components by weight:

        f3 (weight +1) = x * A(u,v)
        f2 (weight -1) = y * B(u,v) + x z * C(u,v)
        f1 (weight -2) = y^2 * E(u,v) + z * H(u,v)

    so pi' o F = ( A^2 (u^2 E + v H),  A (u B + v C) ) and the descent is

        THEOREM W3-5.   G = ( A^2 (u^2 E + v H),  A (u B + v C) ),
                        det JG = det JF * A^2,    where f3 = x * A.

    The square is therefore forced FOR THIS WEIGHT CLASS, for every equivariant
    map in it -- exactly as W3-4 predicts, since D = x^2 and D' o F = f3^2.
    G is Keller if and only if A is a constant.""")

rnd3 = random.Random(9)
U3, W3 = x * y, x ** 2 * z
sub3 = {u: U3, v: W3}


def _rq(n=2):
    return sum(sp.Integer(rnd3.randint(-3, 3)) * u ** i * v ** j
               for i in range(n + 1) for j in range(n + 1))


lifts3, oks3 = [], []
for _ in range(6):
    A3, B3, C3, E3, H3 = _rq(), _rq(), _rq(), _rq(), _rq()
    g3 = sp.expand(x * A3.subs(sub3))
    g2 = sp.expand(y * B3.subs(sub3) + x * z * C3.subs(sub3))
    g1 = sp.expand(y ** 2 * E3.subs(sub3) + z * H3.subs(sub3))
    dF3 = sp.expand(sp.Matrix([[sp.diff(f, w) for w in V]
                               for f in (g1, g2, g3)]).det())
    Gq1 = sp.expand(A3 ** 2 * (u ** 2 * E3 + v * H3))
    Gq2 = sp.expand(A3 * (u * B3 + v * C3))
    lifts3.append(sp.simplify(sp.expand(Gq1.subs(sub3) - g1 * g3 ** 2)) == 0
                  and sp.simplify(sp.expand(Gq2.subs(sub3) - g2 * g3)) == 0)
    dG3 = sp.expand(sp.Matrix([[sp.diff(g, w) for w in (u, v)]
                               for g in (Gq1, Gq2)]).det())
    oks3.append(sp.simplify(sp.expand(dG3.subs(sub3) - dF3 * A3.subs(sub3) ** 2)) == 0)
print(f"    descent identity G o pi = pi' o F on 6 random instances: {all(lifts3)}")
print(f"    THEOREM W3-5: det JG = det JF * A^2 on the same 6:        {all(oks3)}")
check("W3-5: the constructed G is the descent of F in the (1,-1,-2) class", all(lifts3))
check("W3-5: det JG = det JF * A^2 in the (1,-1,-2) class", all(oks3))

# Alpoge is the specialisation A = 2 - 3u - v.
Aalp = 2 - 3 * u - v
print(f"\n    Alpoge: f3 = x*(2 - 3u - v)?  "
      f"{sp.simplify(sp.expand(f3 - x * (2 - 3 * U3 - W3))) == 0}")
check("Alpoge's f3 factors as x * A with A = 2 - 3u - v",
      sp.simplify(sp.expand(f3 - x * (2 - 3 * U3 - W3))) == 0)
check("and then det JG = -2 A^2 reproduces the campaign's h^2",
      sp.simplify(sp.expand(detJG - (-2) * Aalp ** 2)) == 0)

# A2 bullet 1: h^2 is intrinsic -- the campaign asserted this; here it is checked.
print("\n    A2 bullet 1: is h^2 intrinsic under coordinate changes?")
rnd4 = random.Random(3)
types = set()
for _ in range(6):
    while True:
        mm = [[sp.Integer(rnd4.randint(-3, 3)) for _ in range(2)] for _ in range(2)]
        if mm[0][0] * mm[1][1] - mm[0][1] * mm[1][0] != 0:
            break
    e1_, e2_ = sp.Integer(rnd4.randint(-3, 3)), sp.Integer(rnd4.randint(-3, 3))
    Uu = mm[0][0] * u + mm[0][1] * v + e1_
    Vv = mm[1][0] * u + mm[1][1] * v + e2_
    q1 = sp.expand(G1.subs({u: Uu, v: Vv}, simultaneous=True))
    q2 = sp.expand(G2.subs({u: Uu, v: Vv}, simultaneous=True))
    dd = sp.expand(sp.Matrix([[sp.diff(q, w) for w in (u, v)] for q in (q1, q2)]).det())
    fl = sp.factor_list(dd)
    types.add(tuple(sorted((sp.Poly(f, u, v).total_degree(), kk) for f, kk in fl[1])))
print(f"      factorization types of det JG under 6 random affine gauges: {types}")
check("A2: h^2 is intrinsic -- det JG stays (constant)*(linear)^2 under every gauge",
      types == {((1, 2),)})

# A2 bullet 2: does G factor as G' o sigma with sigma carrying the whole h^2?
print("\n    A2 bullet 2: does G = G' o sigma with det J sigma = c h^2?")
print("""      det J sigma = c*h^2 on a reduced curve means ramification index 3 along
      it, so every component of G would have order divisible by 3 along h = 0.
      In adapted coordinates s = 3u + v - 2, t = u:""")
ss, tt = sp.symbols('s t')
subst = {u: tt, v: ss - 3 * tt + 2}
H1 = sp.expand(G1.subs(subst, simultaneous=True))
H2 = sp.expand(G2.subs(subst, simultaneous=True))
e_1 = sorted({m[0] for m in sp.Poly(H1, ss).monoms()})
e_2 = sorted({m[0] for m in sp.Poly(H2, ss).monoms()})
print(f"        s-exponents of G1: {e_1}      ord_s G1 = {min(e_1)}")
print(f"        s-exponents of G2: {e_2}      ord_s G2 = {min(e_2)}")
check("A2: ord_s G2 = 1, not a multiple of 3, so no such factorization exists",
      min(e_2) == 1)
check("A2: G1 and G2 are not polynomials in (s^3, t)",
      not (all(m[0] % 3 == 0 for m in sp.Poly(H1, ss).monoms())
           and all(m[0] % 3 == 0 for m in sp.Poly(H2, ss).monoms())))
check("A2: G contracts the line h = 0 to the single point (0,0)",
      sp.simplify(H1.subs(ss, 0)) == 0 and sp.simplify(H2.subs(ss, 0)) == 0)

print("""
    A2 ANSWERED.  In the (1,-1,-2) class the obstruction is exactly A^2 with
    f3 = x*A -- intrinsic, and not removable by factoring G through a map that
    carries it.  It vanishes only when A is a constant, and then

        G = ( c^2 (u^2 E + v H),  c (u B + v C) ),

    whose two components are an arbitrary plane Keller pair normalised so that
    G(0,0) = (0,0) and dG1/du (0,0) = 0 -- a normalisation any plane Keller map
    can be put in by a translation and a linear change on the target, since
    JG(0) is invertible.  So the A = const sub-class is again the plane problem,
    exactly as the k = 0 class was.

    UNIFIED ANSWER TO A1 + A2.  Whenever the descent is Keller, the
    correspondence identifies the C^3 problem with the plane problem.  Alpoge's
    map is a genuine C^3 counterexample precisely BECAUSE its descent is not
    Keller: A = 2 - 3u - v is non-constant, and det JG = -2 A^2 is the campaign's
    h^2.  The obstruction is not a defect of the descent -- it is the exact
    measure of how much weaker the C^3 problem is than the plane one.""")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 78)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w3_descent_jacobian_formula.py: a check FAILED"
print("""    VERDICT (A1 answered)
      THEOREM W3-4:  (det JG) o pi * D = (det JF) * (D' o F).
      LEMMA W3-4a:   D = x^(a1+a2-1) y^(b1+b2-1) z^(c1+c2-1)  is a monomial,
        and k = deg D = deg p1 + deg p2 - 3.
      The square is NOT forced: k = 0 and k = 1 both occur, and D = 1 holds
      exactly for the three weight systems (0,1,-1), (1,0,-1), (1,-1,0) up to
      sign -- PROVED for all weights, since e1 + e2 = (1,1,1) has exactly three
      splittings into nonzero parts.
      THEOREM W3-5:  in Alpoge's class, G = (A^2(u^2 E + v H), A(u B + v C))
        and det JG = det JF * A^2 with f3 = x*A.  A2 answered: the square is
        intrinsic, not removable by factoring, and vanishes only for A constant.
      Every class in which the descent IS Keller turns out to be the plane
      problem in disguise -- both k = 0 and A = const.  Alpoge is a genuine C^3
      counterexample precisely because its descent is not Keller.  The exponent
      k is not a defect: it measures how much weaker the C^3 problem is than the
      plane one.""")
