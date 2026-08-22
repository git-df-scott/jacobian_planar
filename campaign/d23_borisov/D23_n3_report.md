# Session N2 continuation — N3 core COMPLETE: the SF (−5)-curve map (P, R)

The Session-7-analog milestone for the Second Framework, done in exact
arithmetic. This was the blocking item for the entire L2–L4 rebuild (the
near-miss anchor that cross-validates every later layer).

## What was proven / certified

**1. The h-invariant formulation (d23_n3_msolve.py).** For B = P²/(wR³),
P monic deg m, R monic deg d (2m = 3d+1), demanding
h := 2P′Rw − P(R+3wR′) constant is a system of m+d−1 **bilinear** equations.
Structural theorem (verified symbolically for FF and SF):

    P·h = R·w·N′ − (R + 3wR′)·N,      N := P² − wR³.

Corollaries when h = h₀ ≠ 0 constant: deg N = m−d **exactly** (the miracle
cancellation is forced), and reading leading coefficients,

    h₀ = −D·n_{m−d},  D = 2m−(m−d) = the chain degree —

the **cross-epoch identity** (FF: h₀ = −13n₃, certified in Sessions 16–18,
now a two-line consequence; SF: h₀ = −23n₅). Saturating h₀ ≠ 0 also forces
gcd(P,R) = 1, R squarefree, P(0) ≠ 0, R(0) ≠ 0 (one-line arguments each),
which kills the degenerate components (e.g. P = w²T³, R = wT², B constant)
that make the unsaturated ideal positive-dimensional.

**2. Exact solution by msolve (0.6.5, apt).** With the rational slice
r₈ = 1 (the scale w → λw acts as r₈ ↦ λ⁻¹r₈; no root extractions) and the
saturation variable t·h₀ = 1:

- **FF validation** (12+1 equations, 13 vars): solved in 0.03 s, dimension
  0, eliminant degree **2** = exactly the two First-Framework dessins (the
  certified Session-7 pair over its quadratic field). The certified sliced
  solution satisfies all 12 h-equations symbolically. (Contrast: the blind
  multistart needed ~600 restarts per hit here.)
- **SF target** (22+1 equations, 23 vars): solved in **milliseconds**,
  dimension 0, eliminant of degree **14** — after ~8.6M blind restarts had
  found nothing. The right formulation beat brute force by ~10 orders.

**3. Structure of the solution set.**

- The eliminant is **irreducible of degree 14 over ℚ** with **zero real
  roots**: the 14 SF (−5)-map dessins form a **single Galois orbit** over a
  degree-14 field, and **none is mirror-symmetric** — all chiral, 7
  conjugate pairs. (This explains exactly the 1.19M-restart real-slice
  zero of the earlier hunt, and parallels Phase 0's single degree-15 orbit
  for the (−2)-map. Fields so far: FF: quadratic ℚ(√−3); SF: degrees 14
  and 15.)
- **Completeness**: all seven excluded strata r₈ = … = r_{k+1} = 0,
  r_k = 1 are EMPTY (msolve), and r ≡ 0 mod w is excluded by h₀ ≠ 0.
  So exactly 14 solutions, period.

**4. Certification ledger over K₁₄ (d23_n3_certifyPR.gp, 11/11 PASS).**

    E irreducible: 1 | deg: 14 | real roots: 0
    [PASS] h = 2P'Rw - P(R+3wR') exactly CONSTANT over K14
    [PASS] miracle cancellation deg(P^2 - wR^3) = 5  (28 -> 5, 23-fold)
    [PASS] cross-epoch identity h0 = -23 n5
    [PASS] h0 != 0
    [PASS] P squarefree (14 order-2 points over 0)
    [PASS] R squarefree (9 order-3 points over inf)
    [PASS] N squarefree (5 simple points over 1)
    [PASS] gcd(P,R) = 1 | gcd(P,N) = 1 | gcd(R,N) = 1
    [PASS] P(0), R(0) != 0

Profile certified: {0}: 14×2; {∞}: 9×3 + 1×1; {1}: 1×23 + 5×1 — all 14
embeddings at once. (msolve parametrization convention resolved exactly via
the forced cascade value p₁₃ = 3/2: coordinates are −par_i(θ)/(E′(θ)·cst_i).)

**5. The SF MIRACLE MAP — with an honest correction
(d23_n3_jacobian_identity.py).** Abstract theorem, proved symbolically for
arbitrary P, R:

    y₁ = x₁³x₂⁸·P(w),  y₂ = x₁²x₂⁵·v·R(w),  v = x₁x₂³−1, w = v³/x₂
    ⟹  J(y₁, y₂) = −h(w)·x₁⁴·x₂¹²,

and the general-prefactor computation shows the collapse to −h is SPECIAL
to the (3,2)-prefactor pair: for y₁ = x₁ᵃx₂^{3a−1}P, y₂ = x₁ᶜx₂^{3c−1}vR,

    J = (v+1)^{a+c−1}·[(c−a)vPR + (v+1)PR + w(((3−a)v+3)PR′ + ((c−2)v−2)P′R)],

which equals −(v+1)^{a+c−1}h iff (a,c) = (3,2). With h ≡ h₀ certified, the
(3,8)/(2,5) map is a genuine miracle map for SF — **but it is LAURENT, not
polynomial** (deg P = 14 > 8 leaves x₂-negative terms; caught by the NM1
support check in d23_n3_layer1_nearmiss.py). CORRECTION to the earlier
box claim: the (45,120)/(30,80) boxes and the "(165,110) = pre-surgery
degrees" reading are withdrawn; (165,110) is the pole pair on the
reconstructed curve 2. The polynomial SF near-miss requires the
long-branch surgery structure, and the paper's reconstruction ladder is
now recognized as **Fibonacci**: (60,40), (105,70), (165,110), (270,180),
(435,290) — each rung the sum of the previous two, the signature of
iterated elementary (de Jonquières-type) transformations; likewise the
isotope family's degrees grow by exact steps 36k+27 = 99 + 36(k−2).
Constructing the polynomial near-miss through that surgery is the first
N4 task. Independent of this, NM2–NM4 certify the Laurent object's
(−2)-pole saturation (−15,−10), all 460 (−5)-pole conditions, and the
G-block reproduction G₁ = P(w)/w², G₂ = R(w)/w — the (−5)-side and chain
anchoring stand.

## Data

`d23_PR_data/`: eliminant E (deg 14), h₀ and all coefficients p₀..p₁₃,
r₀..r₇ as exact elements of K₁₄ (polynomials in θ), raw msolve output.

## Still open (N4 queue)

- **Polynomial near-miss via the surgery**: track the long-branch
  reconstruction (the Fibonacci ladder) as explicit elementary
  transformations; derive the true support region/box caps in the final
  coordinates (the reopened L1-box gap, now with the right picture).
- Identification of Borisov's Fig. 27 dessin among the 14 embeddings
  (clean-dessin arc tracing).
- Then L2 (block cascade anchored on the certified G-blocks) → L3
  (rigidity pins) → L4 → unconditional D=23 endgame closure.

Note: the layer-1 CONDITIONS (pole cuts j−3i ≥ −15/−10, the 460
(−5)-pole equations, ranks 314/144) are box-independent and stand; only
the box CAPS in d23_n3_layer1.py are provisional pending the surgery
analysis.
