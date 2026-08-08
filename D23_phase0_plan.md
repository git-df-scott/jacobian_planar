# D=23 Transfer Campaign — Phase 0 Plan (Session N2)

Target: Borisov's Second Framework (arXiv:1901.04073 §4), chain degree D = 23,
target degree pair (435, 290). Test the Sessions 16–18 transfer conjecture:
the endgame mechanism `3v(v+1)R' = D·R` is fatal whenever 3 ∤ D; here 23 ≡ 2 (mod 3).

Note: `D23_transfer_check_context.md` was not present in the repository (the only
context commit was the task prompt itself, later deleted). Working discipline is
taken from the task text + the Sessions 1–18 file: exact-arithmetic certification,
plan-then-checkpoint, DIES / DOES NOT DIE with the three-way honesty labels
("mechanism doesn't apply" vs "applies, no contradiction" vs "proved it dies").
Checkpoint discipline: the Phase-0 stop-and-wait was resolved by the user's
explicit go-ahead ("continue working throughout the night").

## Phase 0 — Belyi rederivation for the (-2)-curve degree-23 map

### 0.1 Functional form (VERIFIED against the paper's §4 text, differs from D=13's Session-7 map)

Session 7's First-Framework object was the degree-16 **(-5)-curve** map
B = p²/(w·r³) (profile 8×2 / 5×3+1×1 / 1×13+3×1), certified through the miracle
cancellation deg(p² − w·r³) = 3. The Second Framework's **(-2)-curve** map is a
different shape: since {∞} has a unique preimage (order 23), it is a **polynomial
(Shabat) Belyi map** of degree 23 — the analog of the First Framework's degree-13
(-2)-curve map, i.e. of the realization target R, not of (p, r). Profile
(from §4, confirmed in the TeX source):

- above {0}: 1 point of order 1, 4 points of order 3, 2 points of order 5
- above {1}: 1 point of order 7, 16 points of order 1
- above {∞}: one point, order 23.

Riemann–Hurwitz: (0 + 4·2 + 2·4) + (6 + 0) + 22 = 44 = 2·23 − 2 ✓ (genus 0).

So with the affine normalization (order-1 point above 0 at t=0, order-7 point
above 1 at t=1 — this kills the entire affine reparametrization group):

    B(t) = c · t · a(t)³ · b(t)⁵,   a monic quartic, b monic quadratic,
    B(t) − 1 = c · (t−1)⁷ · s(t),   s of degree 16, squarefree.

### 0.2 The dessin and its count

B⁻¹([0,1]) is a bipartite plane TREE (V = 7+17 = 24, E = 23, one face). Black
vertices (over 0) have degrees {1,3,3,3,3,5,5}; white (over 1) have {7,1×16}.
Structure theorem (elementary): the only internal white vertex is the degree-7
one, so every black vertex is adjacent to it — the tree is the "star of stars":
central white vertex W, its 7 black neighbors of degrees 1,3,3,3,3,5,5, each
black vertex of degree d carrying d−1 white leaves (Σ(d−1) = 16 ✓). Hence:

- **unique as an abstract graph** (exactly Borisov's remark), and
- as a **plane tree**: one dessin per cyclic arrangement of {1,3,3,3,3,5,5}
  around W up to rotation = 105/7 = **15 dessins** (Burnside; 7 prime, only the
  identity rotation fixes an arrangement). 3 are reflection-symmetric (real
  fields), 12 form 6 chiral (complex-conjugate) pairs.

So the paper's ramification data pins the graph but NOT the dessin: 15 candidates.
Plan: derive **all 15**, making every downstream conclusion dessin-independent;
separately identify which one Borisov drew (figure parse, in progress).

### 0.3 Master equation (the D=23 analog of the miracle cancellation)

B' = c·a²b⁴·L with  **L := a·b + 3t·a'·b + 5t·a·b'**  (degree 6, leading coeff
1+12+10 = 23). Belyi ⇔ all criticality not over 0 concentrates at t=1:

    **L(t) = 23·(t−1)⁶**,   plus  B(1) = 1  ⇒  c = 1/(a(1)³·b(1)⁵).

This is 6 polynomial equations (coefficients t⁰..t⁵) in 6 unknowns
(a₃,a₂,a₁,a₀,b₁,b₀), **bilinear** in the groups (a-coeffs)×(b-coeffs).
Multihomogeneous Bézout bound: C(6,2) = **15 = the dessin count**. The [t⁰]
equation reads a₀b₀ = 23, giving a(0)≠0, b(0)≠0 for free.

Everything else (order-exactly-7 tangency at 1, squarefreeness of s, simplicity
of the 16 points, disjointness of fibers) follows from L-identity + genericity
checks, each certified exactly.

### 0.4 Solution strategy (Session-7 method: numeric generation, exact certification)

1. Symbolically certify the form derivation (sympy): B' = c·a²b⁴·L identity.
2. Multistart Newton (mpmath, high precision) on the bilinear system; collect
   distinct roots; expect 15. Polish to 250+ digits.
3. Resolvent reconstruction: ∏ᵢ(X − coordᵢ) over all 15 roots has RATIONAL
   coefficients (the solution set is Galois-stable and complete); rationalize,
   verify, factor over ℚ (PARI/GP) → Galois orbit structure.
4. Exact reconstruction per orbit: number field K = ℚ[θ]/(f), coordinates as
   ℚ-polynomials in θ via integer-relation (PSLQ); then **all verification exact**:
   - master identity L − 23(t−1)⁶ ≡ 0 over K,
   - disc(a) ≠ 0, disc(b) ≠ 0, Res(a,b) ≠ 0, a(1)b(1) ≠ 0 (via norms to ℚ),
   - B − 1 = c(t−1)⁷s exact division, deg s = 16, disc(s) ≠ 0, Res(s, t·a·b) ≠ 0,
   - ramification profile match (follows; checked anyway).
5. Completeness: 15 distinct certified maps + combinatorial count 15 ⇒ ALL
   dessins realized (no Bézout-at-infinity argument needed).
6. Dessin identification: numeric arc-tracing of B⁻¹([0,1]) per solution to get
   its cyclic order; match against the paper's figure.

Success criteria: full ledger PASS for ≥1 orbit ⇒ Phase 0 succeeded; all 15 ⇒
succeeded with completeness. Partial outcomes reported per task discipline.

## Phase 1 preview (gated on Phase 0)

Rebuild, in order: transfer-hypothesis checks from published §4 data (cusp
(3,2)-proportionality — already spot-confirmed: (−15,−10), (60,40), (105,70),
(165,110), (270,180), (435,290) are all multiples of (3,2); chain e=23, f=1;
realization target is a polynomial by construction — Borisov says so directly),
then chart factor, chain layer, rigidity analog, endgame operator
T₂₃(R) = (v+1)^k·(3v(v+1)R' − 23·R) = −c with exact kernel/infeasibility
computation. Honest conditionality labels on anything whose D=13 analog took
Sessions 8–15 to certify and cannot be fully rebuilt in one session.
