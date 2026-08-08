# D=23 Transfer Campaign — Phase 0 Report: SUCCEEDED (with completeness)

Session N2. Target: the degree-23 (-2)-curve Belyi map of Borisov's Second
Framework (arXiv:1901.04073 §4), for which the paper publishes ramification
data only — no explicit polynomials.

## Outcome, in the task's three-way language

**Succeeded, unconditionally, and more than asked**: explicit Belyi data
derived and certified in exact arithmetic — not for one dessin but for **all
15 dessins compatible with the published ramification data at once**, because
they turn out to form a **single Galois orbit** over one degree-15 number
field. No assumptions beyond the paper's stated profile were needed. The
anticipated partial-outcome ("ramification data alone doesn't pin a unique
dessin") is resolved rather than suffered: the data indeed pins only the
abstract graph (15 plane trees realize it), but certifying the whole orbit
makes every downstream use dessin-independent, and the specific dessin drawn
in the paper's Figure 28 is identified within the orbit.

## The object

With the affine normalization (order-1 point above 0 at t=0, order-7 point
above 1 at t=1):

    B(t) = c · t · a(t)³ · b(t)⁵ ,  a monic quartic, b monic quadratic,
    B(t) − 1 = c · (t−1)⁷ · s(t) ,  s degree 16, squarefree,

profile {0}: 1×1+4×3+2×5 | {1}: 1×7+16×1 | {∞}: 1×23 (RH: 16+6+22 = 44 ✓).
This is a **Shabat polynomial** — a different functional form from Session 7's
First-Framework (-5)-curve map p²/(w·r³), exactly as the task's scope note
warned. It is the analog of the First Framework's *degree-13 (-2)-curve map*
(the endgame realization target R), which is the right object for the
transfer test.

**Master equation** (the D=23 analog of Session 7's miracle-cancellation
constant h): B' = c·a²b⁴·L with

    L := a·b + 3t·a'·b + 5t·a·b'  =  23·(t−1)⁶ ,   c = 1/(a(1)³b(1)⁵).

## Structure theorems (this session)

1. **Star-of-stars**: the dessin's only internal white vertex is the order-7
   one, so the tree is forced: central white hub adjacent to all 7 black
   vertices (degrees 1,3,3,3,3,5,5), each black vertex of degree d carrying
   d−1 white leaves. Unique as a graph (= Borisov's remark); as a plane tree
   there are exactly **105/7 = 15** dessins (Burnside, 7 prime): 3
   reflection-symmetric, 6 chiral pairs.

2. **Triangularity**: coefficients [t⁵..t²] of the master equation solve
   a₃,a₂,a₁,a₀ *linearly* (constant denominators) in (b₁,b₀); [t⁰] reads
   a₀b₀ = 23. The remaining two equations have Res_{b₀} of degree exactly
   15 = the dessin count (= the multihomogeneous Bézout bound C(6,2) for the
   bilinear system).

3. **Single Galois orbit**: the eliminant f(b₁) (deg 15) is **irreducible
   over ℚ** with exactly **3 real roots**. So all 15 dessins are conjugate,
   defined over one field K = ℚ[w]/(f), and gcd(E1,E2) over K is linear in
   b₀: exactly one solution per root — **exactly 15 solutions, in bijection
   with the 15 plane trees**. Certifying once over K certifies all 15.
   (Compare D=13's Session-7 map: field ℚ(√−3). The jump in arithmetic
   complexity from the First to the Second Framework is from a quadratic
   field to a degree-15 field.)

## Certification ledger (exact; PARI/GP over K, cross-checked in sympy)

    f irreducible over Q: 1;  real roots: 3;  gcd(E1,E2) degree in y: 1
    [PASS] master identity  L == 23(t-1)^6
    [PASS] a squarefree (disc != 0 in K)
    [PASS] b squarefree (disc != 0 in K)
    [PASS] gcd(a,b)=1  (Res != 0)
    [PASS] a(1) != 0, b(1) != 0
    [PASS] a(0)b(0) = 23  (0-fiber avoids t=0 collision & t=1)
    [PASS] B - 1 == c(t-1)^7 s  exactly
    [PASS] deg s = 16
    [PASS] s(1) != 0  (order at t=1 exactly 7)
    [PASS] s squarefree (16 simple points above 1)
    [PASS] 1-fiber disjoint from 0-fiber
    [PASS] deg B = 23 (unique pole at infinity, order 23)

12/12. Since K is a field, each nonvanishing certificate holds in **every**
embedding: all 15 dessins certified simultaneously. Independent sympy
verification (d23_phase0_belyi.py): elimination reproduced, master identity
re-verified over K[t], exact (t−1)⁷-division re-verified, nonvanishing
witnessed mod p = 2⁶¹−1. Exact coefficients in `d23_belyi_data/` (b₀, a₃,
a₂, a₁, a₀, c as ℚ-polynomials in the generator w = b₁; f; 100-digit roots).

## Dessin identification (numeric labeling; d23_phase0_dessins.py)

All 23 edges of B⁻¹([0,1]) traced per embedding (predictor–corrector with
factored-form evaluation; 0 failures). Result: the 15 embeddings realize the
15 necklaces **bijectively**; conjugate embeddings give mirror necklaces; the
3 real embeddings give the 3 symmetric necklaces. The dessin drawn in the
paper's Figure 28 — cyclic order (5,1,5,3,3,3,3), parsed from the TeX
source — is the real embedding **β ≈ 0.1250089**, i.e. root 3 in
`d23_belyi_data/d23_roots.txt`.

## Files

- `d23_phase0_belyi.py` — self-contained sympy derivation + verification
- `d23_phase0_certify.gp` — full exact PARI/GP ledger (12/12 PASS)
- `d23_phase0_dessins.py` — arc tracing, necklace bijection, Fig. 28 match
- `d23_belyi_data/` — exact coefficients over K, 100-digit embeddings

## Gate decision

Phase 0 produced certified data → **Phase 1 is unlocked** (chart factor,
chain layer, rigidity, endgame for D=23).
