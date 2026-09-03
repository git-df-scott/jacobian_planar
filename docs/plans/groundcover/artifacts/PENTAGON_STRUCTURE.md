# Pentagon case (1), degree pair (72,108) — structure audit of `trackB1_sat_Q.ms`

Date: 2026-09-02. All numbers below are recomputed from the files, exactly over Q
(Python `fractions`), no Groebner, no floating point. Scripts in this directory:
`msparse.py`, `analyze_1to4.py`, `analyze_4to6.py`, `analyze_refine.py`, `analyze_final.py`.
Raw outputs: `part1to3.json`, `part4to6.json`, `refine_torus.json`, `final.json`.

## 0. Files (all found)

| role | path |
|---|---|
| char-0 system | `wt/mailbox/wave6/frontier/trackB1_sat_Q.ms` |
| twin p=1000003 | `wt/mailbox/wave6/frontier/trackB1_sat_p1000003.ms` |
| twin p=65521 | `wt/canon/campaign/audit_tracks/trackB1_case1_full_p65521.ms` (byte-identical copy also at `wt/hunt/campaign/audit_tracks/`) |
| block index | `wt/mailbox/wave6/frontier/tb1_square_block.json`, `tb1_blocks.json` |

## 1. Census — the mailbox numbers are right, the README numbers are wrong

| quantity | measured |
|---|---|
| variables | **166** |
| generators | **284** |
| total terms (monomials with nonzero coeff) | **8774** |
| max total degree | **5** |
| max abs coefficient | **468** |
| all coefficients integral? | **yes** (every coeff is a rational with denominator 1) |

Variable families (166 total):

| family | count | notes |
|---|---|---|
| `c_i_j` | 51 | c-block |
| `d_i_j` | 110 | d-block |
| `s_i_j` | 4 | `s_1_5, s_2_6, s_3_7, s_4_8` — a **third** block, not part of the bilinear split |
| `zsat` | 1 | Rabinowitsch saturation variable, appears **only** in generator 283 |

**Verdict: mailbox numbers (166 / 284 / deg 5 / 8774) match to the digit.**
**README numbers (164 vars / 288 quadrics / 6821 terms over Q(alpha)) do NOT match**, and
no such object exists here: the file is over **Q**, not Q(alpha) — no parameter `alpha`
appears as a variable or in any coefficient — and its max degree is 5, not 2, so it is not
a system of quadrics. Grepping the READMEs for `164 var` / `288 quadric` / `6,821` found
nothing. The README object appears not to exist; the mailbox description is the accurate one.

## 2. Third-prime lift check — CLEAN

Reduced `trackB1_sat_Q.ms` mod each prime and compared **monomial for monomial, generator
by generator, in file order**:

- **p = 1000003**: identical variable list; 284/284 generators agree **exactly** (same
  monomial support, same reduced coefficients). Zero mismatches, zero rescalings needed.
- **p = 65521**: 284/284 generators agree, 283 of them **exactly**. The single difference
  is cosmetic and is in generator 283 only: the p=65521 file names the saturation variable
  **`w_sat`** where the Q and p=1000003 files name it **`zsat`**. Same monomial, same
  coefficients, same position. Nothing mathematical differs.

So the common-integer lift is confirmed against a third prime. The char-0 file is a faithful
lift of both modular twins.

## 3. Bilinearity — TRUE for 283 of 284 generators; the only exception is the saturation row

Split used: c-block = all 51 `c_*`; d-block = all 110 `d_*`. The 4 `s_*` variables and
`zsat` are in **neither** block — they must be a third block, because `s` occurs to degree
up to **3** (see profile) and so cannot be absorbed into either side without breaking
bilinearity.

Full monomial degree profile `(deg_c, deg_d, deg_s, deg_zsat)` over all 8774 terms:

| profile | count | shape |
|---|---|---|
| (0,0,0,0) | 3 | constants |
| (0,0,1,0) | 4 | `s` |
| (0,0,2,0) | 10 | `s^2` |
| (0,1,0,0) | 99 | `d` |
| (0,1,1,0) | 431 | `d*s` |
| (0,1,2,0) | 1069 | `d*s^2` |
| (1,0,0,0) | 95 | `c` |
| (1,0,1,0) | 200 | `c*s` |
| (1,0,2,0) | 496 | `c*s^2` |
| (1,0,3,0) | 990 | `c*s^3` |
| (1,1,0,0) | **5376** | `c*d` — the bilinear core |
| (2,1,1,1) | 1 | **the exception** |

`deg_c <= 1` and `deg_d <= 1` hold for **8773 of 8774 monomials**. Note also that no
monomial carries `c`, `d` and `s` simultaneously: a `c*d` term never has an `s` factor.

**Exception list (complete, one entry):**

| generator index (0-based) | monomial | coeff | deg_c | deg_d | deg_s | deg_zsat |
|---|---|---|---|---|---|---|
| 283 | `c_1_0*c_8_14*d_12_21*s_4_8*zsat` | +1 | 2 | 1 | 1 | 1 |

Generator 283 in full is `-1 + c_1_0*c_8_14*d_12_21*s_4_8*zsat`, i.e. the Rabinowitsch row
saturating the four nondegeneracy conditions `c_1_0, c_8_14, d_12_21, s_4_8` at once. It is
the sole source of degree 5 and the sole bilinearity violation.

**So the CATCHES.md claim "the bilinearity of every monomial is INTACT" is confirmed on the
284-generator system modulo the saturation row, which is not a system equation but a
bookkeeping row.**

### What `tb1_square_block.json` actually defines

It is **not** a c/d split. It defines a **square subsystem**: a list of 60 equation indices
(max index 282 — i.e. it deliberately excludes the saturation row 283) and a list of 60
variable names (23 `c_*`, 35 `d_*`, 2 `s_*` — namely `s_3_7`, `s_4_8`). `tb1_blocks.json`
is a separate ledger of 8 small candidate blocks with their `ne`/`nv`/`surplus`. Because it
is not a two-block split, the c/d split above was used for the bilinearity test.

## 4. Torus / L-grading — the L = 2*alpha - beta grading is REFUTED on this file

Method: for each generator, form all exponent-vector differences between its monomials
(7358 distinct primitive rows over all 284 generators; 7357 excluding the saturation row).
A weight vector `w` is a grading iff it is orthogonal to every such row. Rank was computed
mod a 61-bit prime for speed, then the nullspace basis was **verified exactly over Z against
every row**, so the reported nullity is exact (nullity_Q <= nullity_p, and the exhibited
basis proves nullity_Q >= the same number).

| system | difference rows | matrix rank | **torus rank (nullity)** |
|---|---|---|---|
| all 284 generators | 7358 | 166 | **0** |
| generators 0..282 (saturation row dropped) | 7357 | 165 | **1** |

The single weight surviving when the saturation row is dropped is supported **only on
`zsat`** (basis vector: `zsat -> 1`, all 165 other variables -> 0). Since `zsat` appears in
no other generator, this is a vacuous weight. **The effective torus acting on the 165
genuine variables has rank 0.** There is no nontrivial grading of any kind — not
`2*alpha - beta`, and not any other linear weight, including any per-family offsets (the
lattice computation quantifies over all 166 weights freely, so it subsumes those).

Direct check of the named candidate and neighbours, counting **non-homogeneous generators**
among the 283 non-saturation generators:

| candidate weight w(x_i_j) | violating generators |
|---|---|
| **2i - j** (the claim) | **207 / 283** |
| i | 60 / 283 |
| j | 206 / 283 |
| i + j | 207 / 283 |

Where it breaks, and why it is structural: e.g. generator 21 is
`-2*c_0_1 + 2*c_1_0*d_1_2` — a degree-1 c-monomial added to a degree-2 c*d-monomial. Any
grading must then force `w(d_1_2) = 0`; generators 22..28, 41..44 etc. repeat this shape
(`c_0_k` alone against `c_0_m*d_2_n` and `c_1_m*d_1_n`) and the forcing cascades until every
weight is 0. Generators 0..19 are fine under `2i-j` — the damage starts at index 21.

**Reading:** the bilinearity claim survives, the grading claim does not. The most likely
explanation is that this saved file has already had a gauge/normalisation substitution
applied (see section 5: `c_1_0 - 1` is literally a generator here, and a row like
`c_1_0 - 1 = 0` de-homogenises any grading in which `c_1_0` has nonzero weight) — CATCHES.md
itself names "`c_1_0 - 1 = 0` as the bracket-point-(2,0) row". So the L-grading was probably
intact on the *ungauged* system and is genuinely broken on this one. Either way, **no one
should rely on an L-grading when working with `trackB1_sat_Q.ms` as saved.**

## 5. The free branch (c_1_0 nonzero => d_0_1 = d_1_1 = 0) — reduces, but does NOT prove empty

Setup. Generator 0 is `c_1_0*d_0_1` and generator 20 is `c_1_0*d_1_1`; `c_1_0` is saturated
nonzero by generator 283, so the `c_1_0 = 0` branch is empty and the surviving branch forces
`d_0_1 = d_1_1 = 0`. Substituted those, then ran a **sound affine-linear fixed point**: at
each step, take any generator all of whose monomials have total degree <= 1 (i.e. an affine
form with constant rational coefficients), solve it for one variable, substitute exactly
over Q everywhere, drop that generator, repeat. Every step is an equivalence, so an
inconsistency found here would be a genuine char-0 EMPTY.

Result after 14 rounds (fixed point reached, no blow-up; term count fell 8774 -> 8519):

| | before | after |
|---|---|---|
| generators | 284 | **269** |
| variables occurring | 166 | **151** |
| variables eliminated | — | **15** |
| max total degree | 5 | **4** |

Eliminations found (exact, over Q):

```
d_0_1 = 0            d_1_1 = 0            c_1_0 = 1            d_0_2 = 0
d_2_2 = (1/2) c_1_1  d_3_3 = (2/3) c_2_2  d_2_3 = c_1_2        d_3_4 = c_2_3
d_4_5 = c_3_4        d_2_4 = (5/4) c_1_3  d_3_5 = (6/5) c_2_4  d_4_6 = (7/6) c_3_5
d_5_7 = (8/7) c_4_6  c_0_1 = d_1_2        c_0_2 = (3/4) d_1_3
```

Two structural remarks worth carrying forward: (a) `c_1_0 = 1` appears as a *derived* linear
row (from generator 39), matching the "bracket-point-(2,0)" normalisation in CATCHES.md;
(b) there is a clean pattern `d_{k,k+2} = ((k+3)/(k+2)) * c_{k-1,k+1}` and
`d_{k,k+1} = c_{k-1,k}` in the diagonal chain.

**Constants found: NONE. No generator reduced to a nonzero constant.**

**Therefore: the free branch is NOT proved empty over Q by this method.** Stated loudly,
because it is the easy result to misread: `empty_over_Q = false` here means *undecided*, not
*nonempty*. The linear fixed point is sound but weak — it only exploits rows that are already
affine-linear. **Case (1) still has NO VERDICT after this pass.** Double-checked: the search
for a nonzero-constant generator runs at the top of every round including the final one, and
the final system genuinely has 269 nonempty generators none of which is a constant.

## 6. The c-linear system M(d) c = b(d) — over-determined, full column rank

Because `deg_c <= 1` on generators 0..282, fixing numerical values for every non-`c` variable
(all `d_*`, all `s_*`, `zsat`) turns those 283 generators into an inhomogeneous **linear**
system in the 51 `c_*` unknowns. Generator 283 is excluded (it has `deg_c = 2`).

Two independent random rational points (seeds 11 and 4242; entries random rationals with
numerator up to 10^6 and denominator up to 997), exact rank over Q:

| seed | rows | rank M | rank [M \| b] | consistent |
|---|---|---|---|---|
| 11 | 283 | **51** | 52 | no |
| 4242 | 283 | **51** | 52 | no |

- **n_c_unknowns = 51**, **generic rank(M) = 51 = full column rank**, rows = 283.
- The system is **massively over-determined**: 283 equations in 51 unknowns, surplus 232.
- rank([M|b]) = 52 > 51 at a generic d-point, i.e. **the generic fibre is empty**, exactly as
  it must be — the d-points that admit a c are a proper closed subvariety.

**What this means for the d-block projection (the question for tomorrow): it is viable.**
Since rank(M) = 51 generically, `c` is **uniquely determined** by `(d, s)` wherever a solution
exists — so eliminating the whole c-block is a well-posed projection with no c-fibre
dimension to track. The image is cut out by the vanishing of the 52x52 minors of the
augmented matrix `[M(d,s) | b(d,s)]`. Practical caution: there are C(283,52) such minors
nominally, so the projection must be done by picking a rank-51 row subset and using
Cramer/pseudo-inverse residuals, not by enumerating minors. A sensible concrete plan is to
solve `c = M^+ b` from 51 independent rows (entries rational functions in d, s) and substitute
into the remaining 232 rows.

## Caveats

1. `empty_over_Q = false` in section 5 means **undecided**, not nonempty. No claim of
   nonemptiness is made or supported anywhere in this document.
2. The torus rank is exact and verified over Z; the rank-mod-p step was only used to select
   pivot rows, and the exhibited nullspace basis was then checked against all 7357/7358 rows
   in exact integer arithmetic, which pins the nullity from both sides.
3. The c-system rank in section 6 is a rank at two specific random rational points. That
   certifies `generic rank >= 51`, and since there are only 51 columns, `rank = 51` generically
   is exact. The *inconsistency* at a random point likewise certifies generic inconsistency.
4. Section 4 refutes the L-grading **for this file as saved**. It does not refute the claim
   for whatever ungauged system CATCHES.md was describing; the `c_1_0 = 1` row is the likely
   culprit and that hypothesis was not separately tested.
5. Generator indices are 0-based and follow file order.
