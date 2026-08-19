Path A — The Quotient Descent
Session 39, run in parallel with Path B. Both are cheap. Status of the core computation: DONE and verified. This document is about what to do with it.

The finding
Session 38's census showed Alpöge's map is C*-equivariant with source weights (1,−1,−2) and target weights (−2,−1,1). Both are C*-actions on C³ with the same weight multiset, so both invariant rings are free on two generators:
source: a − b − 2c = 0 ⟹ C[xy, x²z], since x^{b+2c}y^b z^c = (xy)^b(x²z)^c
target: −2a − b + c = 0 ⟹ C[f₁f₃², f₂f₃]
Both quotients are C². F maps orbits to orbits. So F descends to a polynomial self-map of the plane. Setting u = xy, v = x²z, the substitution y → u/x, z → v/x² leaves both target generators x-free — verified, not assumed:
G₁(u,v) = (u+1)·(3u+v−2)²·(3u³ + u²v + 4u² + 2uv + v)
G₂(u,v) = −(3u+v−2)·(9u³ + 3u²v + 12u² + 6uv + u + 3v)

Three facts, all exact.
deg G = (6,4) — ratio 3:2, the same ratio as (108,72).
G is non-injective. The upstairs collision (0,0,−1/4), (1,−3/2,13/2), (−1,3/2,13/2) ↦ (−1/4,0,0) descends: the last two lie in one C*-orbit and collapse, leaving two distinct quotient points (0,0) and (−3/2,13/2), both mapping to (0,0).
det JG = −2·(3u + v − 2)². A nonzero constant times the square of a line. That line is h = f₃/x. One of the two colliding points, (−3/2, 13/2), lies on h = 0.
Certifier: session39_descent_verified.py, ends in assert all(PASS), 8/8.

Why this is the most promising path
Every previous route asked what a plane counterexample must satisfy and found the constraints unsatisfiable. This is the first object in the campaign that is a non-injective plane polynomial map arising directly from a real counterexample. It is not a candidate that failed a filter; it is the actual shadow, and it misses Keller by one specific, named, structured factor.
h² is not a near miss in the vague sense. It is a perfect square, and a perfect square of a non-constant polynomial can never be a unit. That is either an accident of this example or a theorem about descent — and which one it is, is the question.

Procedure
A1 — Is the square forced? [the central question, 1–2 days]
Prove or refute: for any C*-equivariant Keller map on C^{n+1} whose weights make both invariant rings polynomial, the induced quotient map on C^n has det J = c·h^k with h the degeneracy locus of the quotient projection and k ≥ 2.
Sketch to check: π = (xy, x²z) has Jπ = [[y,x,0],[2xz,0,x²]], whose 2×2 minors are −2x²z, x²y, x³ — all divisible by x². The chain rule through a projection that degenerates to order 2 should force a square. Do the general computation with symbolic weights (w₁,…,w_{n+1}) rather than the specific (1,−1,−2).
If forced: that is a second dimension separator, and a strong one — it says the C* mechanism cannot descend, for a reason internal to the quotient rather than to the sweep. The campaign has had exactly one separator since Session 32. Write it up immediately.
If not forced: there exist equivariant counterexamples whose descent is Keller. That is the construction recipe. Characterise the weight systems where k = 0, then search for a C³ counterexample with those weights. This is the single highest-value outcome available anywhere in the campaign.
A2 — Can the square be removed? [1 day]
Ask whether G is correctable rather than merely defective.
Coordinate changes on the quotient multiply det JG by a constant, so h² is intrinsic. Confirmed. But generator choice is not the only freedom — check whether a different C*-action on the same F (e.g. a subgroup μ_n ⊂ C*, whose invariant ring is larger) gives a different, possibly non-square, obstruction. A μ_n-quotient of C³ is a 3-fold, not a surface, so this needs care about what "descent" means; do it properly or not at all.
Check whether G factors as G = G' ∘ σ with σ carrying the whole h² and G' Keller. Factor both components; G₁ already displays (u+1), (3u+v−2)², and a cubic.
Check whether G is a composition of a Keller map with a non-invertible map of Jacobian h². If so, the Keller factor is worth extracting and examining on its own.
A3 — Run the whole census through the descent [half a day]
Gallagher's family and arXiv:2608.00222. For each member:
Is it C*-equivariant? With which weights?
Are both invariant rings polynomial?
Compute the descent, its degrees, det J, and the exponent k in c·h^k.
Look for k varying. If some member gives k = 1, that is one composition away from Keller. If k is always even, that is evidence for A1's theorem. If any member gives k = 0 — stop, verify by §7 HIT protocol, and escalate.
A4 — Reverse the descent [2 days, only if A1 says "not forced"]
Given a target plane Keller map, ask what C³ map it lifts from. The lift is constrained: weights, equivariance, and det JF constant upstairs. This turns "find a plane counterexample" into "find a C³ counterexample with prescribed weights," and the C³ problem is known to have solutions. That is a categorically better starting position than any previous route.

Success / abort
Success. Either the square is proved forced — a new separator, publishable, and it explains a structural fact nobody knew — or a weight system with k = 0 is identified, at which point Path A becomes the counterexample construction and everything else pauses.
Abort. If A1 stalls on the general-weights computation past two days, fall back to A3, which is pure computation on existing examples and cannot stall.
Deliverable. certifiers/session39_pathA_descent.py extending the verified script; a note stating which of "forced" / "not forced" holds and with what proof status.

Honest odds
k = 0 for some member of the known families: low, but this is the only route in the campaign where the search space is a set of objects that are known to exist.
A1 proving the square forced: moderate to good, and it is worth doing on its own — a second dimension separator is the scarcest currency the campaign has, and every proof strategy that fails the separation test is known wrong as of July 2026.

Verify with this 
import sympy as sp

x, y, z, u, v, lam = sp.symbols('x y z u v lam')
PASS = []

# Alpoge's degree-7 counterexample in C^3
f1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
f2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z

J = sp.Matrix([[sp.diff(f, w) for w in (x, y, z)] for f in (f1, f2, f3)])
detJ = sp.simplify(sp.expand(J.det()))
PASS.append(("det JF is the constant -2", detJ == -2))

# C*-equivariance: weights (1,-1,-2) on source, (-2,-1,1) on target
sub = {x: lam*x, y: y/lam, z: z/lam**2}
for f, w in ((f1, -2), (f2, -1), (f3, 1)):
    lhs = sp.simplify(sp.expand(f.subs(sub, simultaneous=True) - lam**w * f))
    PASS.append((f"component weight {w}", lhs == 0))

# Invariant rings.  Source: a-b-2c=0  ->  C[xy, x^2 z].
# Target: -2a-b+c=0 ->  C[f1*f3^2, f2*f3].   Both free on two generators.
w1 = sp.expand(f1 * f3**2)
w2 = sp.expand(f2 * f3)

# Rewrite in u = xy, v = x^2 z.  Substitute y -> u/x, z -> v/x^2 and check x cancels.
def to_uv(expr):
    e = sp.simplify(sp.expand(expr.subs({y: u/x, z: v/x**2})))
    e = sp.simplify(sp.cancel(sp.together(e)))
    return sp.expand(sp.simplify(e))

W1 = to_uv(w1)
W2 = to_uv(w2)
PASS.append(("W1 is x-free (descends)", sp.simplify(sp.diff(W1, x)) == 0))
PASS.append(("W2 is x-free (descends)", sp.simplify(sp.diff(W2, x)) == 0))

W1 = sp.expand(W1)
W2 = sp.expand(W2)

print("G_1(u,v) =", sp.factor(W1))
print()
print("G_2(u,v) =", sp.factor(W2))
print()
print("deg G_1 =", sp.Poly(W1, u, v).total_degree(), "  deg G_2 =", sp.Poly(W2, u, v).total_degree())

JG = sp.Matrix([[sp.diff(g, t) for t in (u, v)] for g in (W1, W2)])
detJG = sp.expand(JG.det())
print()
print("det JG =", sp.factor(detJG))
print()
print("det JG is constant? ", sp.simplify(sp.diff(detJG, u)) == 0 and sp.simplify(sp.diff(detJG, v)) == 0)

# Non-injectivity downstairs, inherited from the known collision upstairs.
pts3 = [(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
        (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
pts2 = [(px*py, px**2*pz) for (px, py, pz) in pts3]
print()
print("upstairs collision maps to quotient points:", pts2)
imgs = [(W1.subs({u: a, v: b}), W2.subs({u: a, v: b})) for (a, b) in pts2]
print("images under G:", imgs)
distinct = len(set(pts2))
PASS.append(("quotient points collapse 3 -> 2", distinct == 2))
PASS.append(("G is non-injective on those", len(set(imgs)) == 1 and distinct == 2))

# Where does the Jacobian degenerate?
print()
print("det JG factors:", sp.factor_list(detJG))

for name, ok in PASS:
    print(("PASS " if ok else "FAIL ") + name)
assert all(ok for _, ok in PASS)

Path B — The Equivariant Search, Generalized
Session 39, parallel to Path A.

What Session 38 established, and the gap it leaves
Alpöge's map is C*-equivariant: all three components weighted-homogeneous under weights (1,−1,−2), verified by direct substitution. The plane analogue was tested — 11 weight pairs (a,b) with a > 0 > b, all admissible (p,q) with p+q = a+b forced by constant Jacobian, total degree ≤ 8 — and collapsed completely: 22 branches with nonzero constant Jacobian, every one a diagonal linear map.
upstairs:  weighted-homogeneous and a counterexample exists
plane:     weighted-homogeneous forces diagonal linear, everywhere tested

That is the shape of a separator. But it is bounded-degree evidence, not a theorem — Session 38 was explicit about this, and correctly threw away the Euler-relation proof that would have made it degree-uniform, because the identical hole (a small fibre over a non-properness point saying nothing about the generic fibre) sinks it.
The gap: C*-equivariance is a very strong hypothesis, and it is the only one tested. Between it and no symmetry at all lie several strictly weaker structures, and none has been examined.

The ladder of hypotheses, weakest constraint first
Structure
Condition
Space size
Tested
C*-equivariant
F(λ·z) = λ^w·F(z), all λ
tiny
yes — collapses
μ_n-equivariant
as above, λ^n = 1 only
grows with n
no
semi-invariant
F(λ·z) = A(λ)·F(z), A a character-valued matrix
larger
no
finite non-abelian
F ∘ g = ρ(g) ∘ F, g ∈ G finite
varies
no
filtered / graded-lifting
top weighted-homogeneous part equivariant, lower terms free
much larger
no

The last row is the interesting one. A map need not be equivariant to have an equivariant leading form. Alpöge's map has a full C*-symmetry, but a plane counterexample only needs its top-degree behaviour to be structured — which is exactly what the Newton-polygon machinery has been saying all along. [DERIVED-S39]

Procedure
B1 — The literature check, first, before any computation [half a day]
Is the plane weighted-homogeneous Keller case already a theorem? Search for: quasi-homogeneous polynomial automorphisms; the Jacobian conjecture for weighted-homogeneous maps; Bass–Connell–Wright reduction to cubic homogeneous; Wang's degree-2 theorem; de Bondt's work on homogeneous and quasi-homogeneous cases.
If it is a theorem: cite it, upgrade the Session 38 result from bounded-degree evidence to a clean statement, and the separator is free.
If it is not: the degree-uniform proof is an open target worth attempting, and it is bounded and well-posed.
Either way this is thirty minutes to two hours and it determines whether B2 is a search or a proof.
B2 — μ_n-equivariance in the plane [2 days]
Strictly weaker than C*, and the search space grows with n rather than staying tiny. Set up: F(ζx, ζ^b y) = (ζ^p F₁, ζ^q F₂) for ζ a primitive n-th root of unity. The constant-Jacobian condition gives p + q ≡ 1 + b (mod n) rather than as an integer identity — which is exactly the slack that killed the C* case. Over Z/n the constraint is a congruence, not an equation, so solutions exist where they did not before.
Sweep n = 2, 3, 4, 6 against total degree ≤ 12. Record whether the collapse to diagonal-linear persists, and if it breaks, at which n and which degree.
This is the highest-value item in Path B. It is the first hypothesis strictly between "no symmetry" and the one that collapses.
B3 — Equivariant leading forms [2 days]
Drop equivariance of the map and require it only of the top weighted-homogeneous part. Write F = F_top + F_lower with F_top equivariant. The Keller condition splits by weight: det J(F_top) must be the top part and must vanish (else it dominates), while the constant comes from cross terms.
This is precisely the structure the cusp-chain and Newton-polygon routes kept producing (A = αh^k, B = βh^{k−1}, powers of a common h), which suggests the two frameworks are describing the same phenomenon in different languages. Check whether B3's equations reproduce the Session 30 sweep cascade. If they do, that is a unification worth having and it recycles 30 sessions of machinery.
B4 — Cross-check against Path A [half a day]
Path A's descent has det JG = −2h² with h linear. Ask whether G is itself equivariant for some action — its degrees are (6,4) and its structure is visibly graded. If the descent of an equivariant map is equivariant, then B2 and Path A are studying the same object from two sides and results transfer.

Success / abort
Success. Either the weighted-homogeneous collapse is upgraded to a theorem (a separator, no more caveats), or μ_n breaks the collapse and produces a non-linear Keller map with symmetry — which is then a counterexample candidate to be run through the §7 HIT protocol.
Abort. If B2 collapses identically for n ≤ 6 up to degree 12, record it and stop; the finite-symmetry ansatz is dead and B3 is the remaining sub-path.
Deliverable. certifiers/session39_pathB_equivariant.py; a literature note answering B1 definitively.

Honest odds
A counterexample from B2: low. The C* collapse is total, and weakening to μ_n may only recover the same diagonal solutions with more index bookkeeping.
A separator from B1 + B3: good, and cheap. Given that any strategy failing the n = 2 vs n = 3 distinction is known wrong, and the campaign has one separator, this is worth the two days regardless of the counterexample question.
Do not skip B1. Spending two days searching a space that was classified in 2005 is exactly the failure mode the tooling ledger exists to prevent.

