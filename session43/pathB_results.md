# Path B / Item B2 — μ_n-equivariant plane Keller map sweep (sympy)

Date: 2026-08-22. Sweep code: `sweep.py`, driver `driver.py`, raw per-cell JSON in
`cells.jsonl` (89 cell-runs), auto table in `table.md`. sympy 1.14.0.

## Setup

Hypothesis under test: μ_n-equivariance only, i.e. F(ζx, ζ^b y) = (ζ^p F1, ζ^q F2)
for ζ^n = 1. A μ_n-equivariant F1 is supported on monomials x^i y^j with
i + b·j ≡ p (mod n); F2 likewise with character q. General F1, F2 with unknown
coefficients up to total degree D; Keller condition imposed by setting every
nonconstant coefficient of det JF to zero. Solved exactly over QQ
(Groebner grevlex → sympy solve, all branches), each branch specialized at random
integer parameter values with det ≠ 0 and classified by the Jung–van der Kulk
elementary-reduction algorithm (repeatedly subtract c·G2^k from G1 when the top
form of G1 is c·(top form of G2)^k, until linear):

- **linear/affine** — both components degree ≤ 1 (the C*-style full collapse)
- **nonlinear-tame-automorphism** — genuinely nonlinear, but reduces to an
  invertible linear map by elementary (de Jonquières-type) reductions → certified
  tame automorphism
- **degenerate(det=0)** — branch forces det JF ≡ 0 (not Keller; discarded).
  In pre-fix D=3 rows this class is labeled `no-keller-specialization`
  (spot-checked identical on re-run: see re-run of (2,1,1,3) and (3,−1,0,3))
- **CANDIDATE** — nonlinear solution NOT elementary-reducible (loud flag)

## Structural fact (found analytically, confirmed by every sweep cell)

det JF of a μ_n-equivariant map is itself μ_n-semi-invariant of character
p + q − 1 − b (mod n). Its constant term carries character 0, so a cell can
contain a Keller map ONLY IF **p + q ≡ 1 + b (mod n)** — exactly the congruence
slack B2 predicted. All cells swept satisfy q = (1 + b − p) mod n; the sweep
confirms every off-congruence class is empty automatically.

A second instant emptiness criterion: det JF's constant term is
a10·b01 − a01·b10, so a cell with no usable linear monomials (e.g. every
"even" character class for n=2, b odd: class p=0 contains only even-degree
monomials) contains NO Keller map at any degree D. This resolves the two D=4
timeout cells (2,±1,p=0) analytically: empty.

## VERDICT

**The C*-collapse-to-linear does NOT persist under μ_n — but collapse to
AUTOMORPHISM does, and in a strong, structured form.**

1. **Nonlinear Keller solutions appear** as soon as the congruence slack allows
   them (unlike the C* case, where every tested cell forced diagonal linear
   maps). Examples found by the solver (random specialization of positive-
   dimensional solution families):
   - n=2, b=1, p=q=1, deg 3: F = (8x³ + x + 32y, 2x³ + 5x + 8y)
   - n=2, b=−1, p=q=1, deg 3: F = (x³ + 8x + 4y, 2x³ + 5x + 8y)
   - n=3, b=1, p=q=1, deg 4: F = (3x⁴ + 8y, 6x) and the linearly conjugated
     F = (5(x/4+y)⁴·(…)+29x/9+4y, 9(x/4+y)⁴·(…)+6x+8y) family
2. **Every single nonzero-Jacobian branch in every solved cell classified as
   linear/affine or as a tame automorphism reducible by elementary steps.**
   Total branch census over all 89 cell-runs: 42+ nonlinear-tame-automorphism,
   12 linear/affine, ~87 degenerate(det=0), **0 CANDIDATE**. No solution
   resisted elementary reduction; nothing needed an injectivity fallback test.
3. Structure of the nonlinear solutions: in every case both components share a
   single "direction" — F1, F2 ∈ span{x, y, ℓ(x,y)^d} for one linear form ℓ,
   i.e. (linear) ∘ (one de Jonquières shear) ∘ (linear). The μ_n slack buys
   exactly the equivariant triangular shears (e.g. y-shear by x^d when
   d·1 ≡ b (mod n)) and their linear conjugates/compositions — nothing more at
   the degrees tested.

So: μ_n-equivariance genuinely enlarges the Keller solution set relative to C*
(new slack is real), but only by tame de Jonquières-type automorphisms.
**Collapse persists in the automorphism sense in every swept cell. NO CANDIDATE
found.**

## Coverage

- **D=3, complete**: all (n, b) with n ∈ {2,3,4,6},
  b ∈ {1, −1, ±2, ±3, 5 (n=6), 3,4 (n=6)} — 21 weight pairs, all n characters
  each = 81 cells, every one solved exactly over QQ (no timeouts).
- **D=4**: priority cells n=2, b=±1 (p=1 solved; p=0 empty analytically) and
  n=3, b=1 (all p solved; p=q=1 is the big one: 14 vars / 11 eqs, 24 branches,
  4 nonlinear tame, 0 candidates).
  Note for n=2 odd characters, D=4 support = D=3 support (parity), so the D=4
  rows there confirm stability; for n=3, b=1 the quartic shear y ↦ y + x⁴
  (4 ≡ 1 mod 3) duly appears and is tame.
- **D=5/6**: attempted for n=2,3, b=±1 (24-var systems); QQ and mod-p Groebner
  both exceeded the per-cell timeout (120s) — not completed within budget.
  Untested territory: degree-5 terms for n=2 odd class, degree ≥5 for n=3.
- Caveat: branch classification is at random integer specializations of
  positive-dimensional solution families (12 retries per branch); a
  measure-zero special locus inside a branch could in principle behave
  differently, but every branch's generic point is a tame automorphism, and by
  Moh's theorem (plane JC true up to deg 100) no true counterexample can hide
  at these degrees anyway — the sweep's question was tame/structured vs wild,
  and the answer everywhere was tame.

## Per-cell table

See `table.md` for the full 89-row table (n, b, p, q, D, vars/eqs, branch
census, example nonlinear solution per cell). Highlights:

| n | b | p,q | D | outcome |
|---|---|-----|---|---------|
| 2 | 1 | 1,1 | 4 | 3 nonlinear tame + 1 linear + 2 degenerate — collapse-to-automorphism: YES |
| 2 | −1 | 1,1 | 4 | same structure — YES |
| 2 | ±1 | 0,0 | any | empty (no linear monomials in class ⇒ det const ≡ 0) |
| 3 | 1 | 1,1 | 4 | 4 nonlinear tame (deg-4 shears) + 1 linear — YES |
| 3 | −1 | 1,2 / 2,1 | 3 | 4 nonlinear tame each — YES |
| 3 | ±2 | all | 3 | linear or empty |
| 4 | ±1,±3,2 | all | 3 | linear, small tame families, or empty — YES everywhere |
| 6 | ±1,5,2,3,4 | all | 3 | linear, small tame families, or empty — YES everywhere |

**Collapse-persists (automorphism sense): YES in every solved cell. CANDIDATES: none.**

## Suggested next step for B2

The D≥5 cells for n=2,3 (24 coefficient vars) need a faster engine than sympy
(msolve/Singular, or exploit the torus normalization a_x=1, b_y=1 to cut 4
vars). The structural pattern above suggests a provable statement: a
μ_n-equivariant Keller map in a slack cell is (linear)∘(equivariant de
Jonquières)∘(linear); the sweep found zero evidence against it.
