# night9 — LAST-TERM KILL

Scope note. Measurements only. Every result is labelled with its
characteristic or with the ring it was computed in. No assessment of what any
of these numbers mean is offered.

Script: `night9/lastterm.py`. Raw data: `night9/lastterm/<hash>_<i>.json`,
index `night9/lastterm_index.json`, run log `night9/lastterm_log.txt`.
Every object produced is filed **CANDIDATE-UNVERIFIED**.

## 1. Selection

From `night9/altitude/`, every matched lift whose exact integer residual

    R(x,y) = P_x Q_y - P_y Q_x - 1      (over Z)

is a **single monomial** `c * x^A * y^B`. There are **88** such lifts, across
**21** distinct supports (a lift and its negation give the same residual, and
several patterns repeat, so there are **44** distinct
`(support, residual monomial)` cases). Since 88 >= 10, the two-term fallback
was **not** taken.

Coefficient `|c|` ranges over 48 .. 21726.

## 2. The bracket coefficient of the residual monomial

For each case the coefficient of `x^A y^B` in `P_x Q_y - P_y Q_x` was written
symbolically,

    R_[A,B] = sum over pairs (m,n) with (m0+n0-1, m1+n1-1) = (A,B)
              of (m0*n1 - m1*n0) * a_m * b_n      (minus 1 when (A,B)=(0,0))

**In all 88 cases that sum has exactly ONE term**, i.e. the formula is a
single product `c * a_m * b_n` (column "formula" below). Consequently the free
set has size **2** in every case, and the prescribed box `[-4..4]` per free
coefficient is **81 assignments** per case — exhaustively searched.

## 3. The exact integer local search

For each of the 81 assignments the **full** residual over Z was computed on
**all** rows of the equation index set (not merely the target monomial),
together with both collision differences over Z. All arithmetic is exact
Python integer arithmetic; no floating point and no modular reduction.

### HALT EVENTS

**0.** Across all 88 cases and all 7128 assignments, **no assignment has
residual identically zero over Z together with both collision differences
zero**. Nothing to halt-and-commit on.

### The landscape of near-misses

The box does contain residual-killing assignments, but they fail (C):

| stratum | measurement |
|---|---|
| assignments with residual identically zero over Z | **1496** (exactly 17 in each of the 88 cases) |
| of those, also satisfying both collision equalities over Z | **0** |
| of those, also non-degenerate under the additive screen | **0** |

`17 = 9 + 9 - 1` is exactly the number of box points with `a_m = 0` or
`b_n = 0`. Since the formula is the single product `c*a_m*b_n`, the target row
vanishes precisely there — and, as the count records, **every other row of the
system is already zero at every point of the box**, so killing the target term
kills the whole residual. At all 17 such points the additive degeneracy screen
fires and both collision differences are non-zero.

Minimum achieved over the box, by stratum (minimum number of non-zero residual
rows; among assignments attaining it, minimum content gcd):

| stratum | min non-zero rows | attained in |
|---|---|---|
| whole box | **0** | 88 / 88 cases |
| collisions hold over Z | **1** | 88 / 88 cases |
| collisions hold and non-degenerate | **1** | 88 / 88 cases |

Within the collision-respecting stratum, the minimum content gcd equals
`|c|`, the lift's own residual coefficient, in **88 of 88** cases: the box
**improved on the lift in 0 cases** and matched it in 88.

## 4. Case table

One row per distinct `(support, residual monomial)`; "lifts" is how many of the
88 lifts share it. "zeroR" counts box assignments with residual identically
zero over Z; "zeroR+C" counts those that also satisfy both collision
equalities. The last two columns are the minimum over the
collision-respecting, non-degenerate stratum.

| hash | lifts | monomial | c | formula | box | zeroR | zeroR+C | min rows | min content |
|---|---|---|---|---|---|---|---|---|---|
| `0ba45c61d577` | 2 | x^11*y^101 | -1224 | `-1224*a_1*b_3` | 81 | 17 | 0 | 1 | 1224 |
| `0ba45c61d577` | 2 | x^1*y^101 | -204 | `-204*a_1*b_2` | 81 | 17 | 0 | 1 | 204 |
| `0ba45c61d577` | 2 | x^11*y^23 | -288 | `-288*a_0*b_3` | 81 | 17 | 0 | 1 | 288 |
| `0ba45c61d577` | 2 | x^1*y^23 | -48 | `-48*a_0*b_2` | 81 | 17 | 0 | 1 | 48 |
| `0f2efd22ee8f` | 2 | x^25*y^65 | -1716 | `-1716*a_0*b_2` | 81 | 17 | 0 | 1 | 1716 |
| `21bd08557217` | 2 | x^5*y^25 | -156 | `-156*a_1*b_2` | 81 | 17 | 0 | 1 | 156 |
| `21bd08557217` | 2 | x^5*y^114 | -690 | `-690*a_2*b_2` | 81 | 17 | 0 | 1 | 690 |
| `21bd08557217` | 2 | x^5*y^131 | -792 | `-792*a_3*b_2` | 81 | 17 | 0 | 1 | 792 |
| `21bd08557217` | 2 | x^5*y^138 | -834 | `-834*a_4*b_2` | 81 | 17 | 0 | 1 | 834 |
| `21bd08557217` | 2 | x^5*y^13 | -84 | `-84*a_0*b_2` | 81 | 17 | 0 | 1 | 84 |
| `21bd08557217` | 2 | x^5*y^144 | -870 | `-870*a_5*b_2` | 81 | 17 | 0 | 1 | 870 |
| `2db81810e7ad` | 2 | x^119*y^33 | -4080 | `-4080*a_0*b_7` | 81 | 17 | 0 | 1 | 4080 |
| `2e4c72090e2e` | 2 | x^146*y^141 | -20874 | `-20874*a_0*b_5` | 81 | 17 | 0 | 1 | 20874 |
| `3aa3f2d1cd2f` | 2 | x^123*y^122 | -15252 | `-15252*a_1*b_4` | 81 | 17 | 0 | 1 | 15252 |
| `405a469bffcf` | 2 | x^71*y^102 | -7416 | `-7416*a_0*b_4` | 81 | 17 | 0 | 1 | 7416 |
| `41fcb750b183` | 2 | x^11*y^88 | -1068 | `-1068*a_0*b_4` | 81 | 17 | 0 | 1 | 1068 |
| `41fcb750b183` | 2 | x^11*y^91 | -1104 | `-1104*a_1*b_4` | 81 | 17 | 0 | 1 | 1104 |
| `41fcb750b183` | 2 | x^11*y^140 | -1692 | `-1692*a_2*b_4` | 81 | 17 | 0 | 1 | 1692 |
| `492665aa006d` | 2 | x^121*y^113 | -13908 | `-13908*a_0*b_5` | 81 | 17 | 0 | 1 | 13908 |
| `92153ee43036` | 2 | x^117*y^74 | -8850 | `-8850*a_0*b_3` | 81 | 17 | 0 | 1 | 8850 |
| `a0c736f067a4` | 2 | x^139*y^110 | -15540 | `-15540*a_0*b_5` | 81 | 17 | 0 | 1 | 15540 |
| `a0c736f067a4` | 2 | x^139*y^113 | -15960 | `-15960*a_1*b_5` | 81 | 17 | 0 | 1 | 15960 |
| `a0c736f067a4` | 2 | x^156*y^113 | -17898 | `-17898*a_1*b_6` | 81 | 17 | 0 | 1 | 17898 |
| `abda1496949e` | 2 | x^122*y^45 | -5658 | `-5658*a_0*b_6` | 81 | 17 | 0 | 1 | 5658 |
| `ad2397183dda` | 2 | x^135*y^32 | -4488 | `-4488*a_0*b_6` | 81 | 17 | 0 | 1 | 4488 |
| `b8cb03dd9688` | 2 | x^113*y^94 | -10830 | `-10830*a_1*b_4` | 81 | 17 | 0 | 1 | 10830 |
| `b8cb03dd9688` | 2 | x^113*y^107 | -12312 | `-12312*a_2*b_4` | 81 | 17 | 0 | 1 | 12312 |
| `b8cb03dd9688` | 2 | x^113*y^147 | -16872 | `-16872*a_3*b_4` | 81 | 17 | 0 | 1 | 16872 |
| `b8cb03dd9688` | 2 | x^113*y^37 | -4332 | `-4332*a_0*b_4` | 81 | 17 | 0 | 1 | 4332 |
| `ba6b62170c52` | 2 | x^132*y^113 | -15162 | `-15162*a_1*b_5` | 81 | 17 | 0 | 1 | 15162 |
| `c37a1c94c6f2` | 2 | x^43*y^29 | -1320 | `-1320*a_0*b_5` | 81 | 17 | 0 | 1 | 1320 |
| `c37a1c94c6f2` | 2 | x^2*y^29 | -90 | `-90*a_0*b_2` | 81 | 17 | 0 | 1 | 90 |
| `c7ba7509d0b2` | 2 | x^142*y^131 | -18876 | `-18876*a_1*b_4` | 81 | 17 | 0 | 1 | 18876 |
| `e07f72fc152b` | 2 | x^152*y^141 | -21726 | `-21726*a_1*b_6` | 81 | 17 | 0 | 1 | 21726 |
| `e07f72fc152b` | 2 | x^152*y^25 | -3978 | `-3978*a_0*b_6` | 81 | 17 | 0 | 1 | 3978 |
| `e07f72fc152b` | 2 | x^29*y^141 | -4260 | `-4260*a_1*b_4` | 81 | 17 | 0 | 1 | 4260 |
| `e07f72fc152b` | 2 | x^29*y^25 | -780 | `-780*a_0*b_4` | 81 | 17 | 0 | 1 | 780 |
| `ef38fc7d5f53` | 2 | x^15*y^83 | -1344 | `-1344*a_1*b_4` | 81 | 17 | 0 | 1 | 1344 |
| `ef38fc7d5f53` | 2 | x^15*y^2 | -48 | `-48*a_0*b_4` | 81 | 17 | 0 | 1 | 48 |
| `efae6ba71cb6` | 2 | x^103*y^125 | -13104 | `-13104*a_1*b_4` | 81 | 17 | 0 | 1 | 13104 |
| `efae6ba71cb6` | 2 | x^159*y^89 | -14400 | `-14400*a_0*b_6` | 81 | 17 | 0 | 1 | 14400 |
| `efae6ba71cb6` | 2 | x^159*y^125 | -20160 | `-20160*a_1*b_6` | 81 | 17 | 0 | 1 | 20160 |
| `efae6ba71cb6` | 2 | x^103*y^89 | -9360 | `-9360*a_0*b_4` | 81 | 17 | 0 | 1 | 9360 |
| `fb644eab941d` | 2 | x^45*y^122 | -5658 | `-5658*a_1*b_4` | 81 | 17 | 0 | 1 | 5658 |

## 5. Files

* `night9/lastterm.py` — the selection, the symbolic bracket formula, and the
  exact integer box search.
* `night9/lastterm/<hash>_<i>.json` — one file per case: supports, the lift,
  the residual monomial and its symbolic formula, the free set, the box, the
  halt-event list (empty in all cases), the zero-residual assignment counts
  split by (C) and by the degeneracy screen, and the near-miss minimum at each
  of the three strata with an attaining assignment.
* `night9/lastterm_index.json` — the 88-case index.
* `night9/lastterm_log.txt` — the run log.
