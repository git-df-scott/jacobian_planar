# H1b — the pentagons: status after Wave 1

No counterexample. No verdict. Nothing promoted. One false-positive episode,
recorded in full because the mechanism is reusable.

## Certified findings

| # | finding | standard |
|---|---|---|
| 1 | y-adic Jacobian **rank 60 of 61**, reproduced by a fully independent rebuild (own polygons — 61 lattice points — own bracket expansion, own recursion, own dual-number differentiation, own elimination) at p = 65521 **and** p = 1000003, three random points each | `CERTIFIED` |
| 2 | the rank deficiency is **exactly p_00**, the constant term of P. Structural: `[P,Q]` sees P only through its derivatives | `CERTIFIED` |
| 3 | **P's overall scale is a second gauge**: `[cP, Q/c] = [P,Q]`, and the recursion sends `Q → Q/c` when `P → cP`, so every support condition is unchanged. Conditions are homogeneous of degree −1 in the scale — verified by the Euler relation `J(x)·x = −F(x)` (4e-05 relative) | `CERTIFIED` |
| 4 | rank **saturates at level j ≤ 23** (66 conditions, rank 60); everything beyond is surplus — **314 further equations** any candidate must also satisfy | `CERTIFIED` |
| 5 | the cascade is **affine in the newest slice** at every level 13–17 (exact second-difference test over F_p), and genuinely nonlinear in earlier slices. So 15 linear equations determine the 13 late parameters and leave 2 compatibility conditions on the 48 early ones | `CERTIFIED` |
| 6 | the conditions have **degree 12–23** in the parameters (measured by interpolation along a line with p_10 held fixed) | `CERTIFIED` |

## What finding 6 means, and why it explains the campaign's history

A degree-12 form in 61 variables admits ~10¹⁴ monomials. **These conditions
cannot be written down.** No exact elimination engine can be handed this system
— which is precisely what the record shows: msolve dies in monomial hash-table
growth on the 166-variable form (`Enlarging exponent vector for hash table
failed for esz = 16777216`), and the symbolic tower stalls at level 16 at
1.8 GB. Those are not tuning failures. Evaluation-based search is the only
route currently in reach.

## Correction to this session's own step-1b claim

Step 1b concluded "the pentagon system is **square** modulo gauge: 60 essential
parameters, generic rank 60". That was **two gauges short**. The full gauge group
is 3-dimensional (translation, overall scale, coordinate scale), so the count is
**58 essential parameters against 60 independent conditions** — the system is
**overdetermined by 2** modulo gauge, before the 314 surplus conditions. The
operative conclusion is unchanged and strengthened: solutions, if any, are
isolated modulo gauge, and dimension excludes nothing.

*(Recorded in two steps: step 3 v2 corrected 60 → 59 on finding the overall
scale; step 3c corrected 59 → 58 on finding the coordinate scale.)*

## The false-positive episode (v1 of the hit-detector)

v1 ran Newton over ℂ on the square subsystem and reported **five candidate
hits** — roots with `‖F‖ ~ 1e-9` that also killed the 314 surplus conditions.
All five were artefacts of a defect in v1.

**Mechanism.** The conditions are homogeneous of degree −1 in P's scale
(finding 3), so scaling P up divides the absolute residual by the same factor
while changing nothing real. Measured directly: as `c` runs over six orders of
magnitude, `max|F|` falls from 6.4e+15 to 6.4e+09 while the ratio
`forbidden/allowed` stays pinned at **1.1721e+06**. v1's stopping test was
**absolute** (`‖F‖ < 1e-9`), so Newton walked straight down that direction:
`‖x‖ → ~1e10`, Q collapsed to ~1e-9 everywhere, and every support condition was
met vacuously. At the deepest level the "vanishing" coefficients were **larger**
than the allowed ones (ratio 1.36 and 1.05 at the two roots examined).

**Caught by** the adversarial diagnosis Plan 43 §6.1 step 5 mandates — comparing
each forbidden coefficient against the allowed coefficients at the same level,
rather than against zero.

**Scope.** The defect never reached a committed claim. The buggy detector was
untracked at the time of diagnosis, and the committed H1b results (findings 1–2)
contain no floating-point arithmetic at all — they are exact F_p computations.

**Other defects found in v1 during the same audit:** no `__main__` guard (so
importing it re-ran the entire search); docstring claimed dual-number Jacobians
where the code used finite differences; dead branch left in the line search.

## v2, corrected

Gauge-fixes both `p_00 = 0` and `p_10 = 1` (legitimate — both are true gauges),
and replaces the objective with the **scale-invariant** ratio
`max_j (forbidden / allowed)`, which no rescaling can move. 30 random starts:

    best scale-invariant ratios: 1.70e-09, 1.50e-05, 1.51e-05, 1.53e-05, ...
    genuine candidates: 0

**This is not evidence of emptiness** and is not recorded as such. Newton has a
tiny basin on a degree-12..23 system; non-convergence from random starts is the
expected default.

## The 1.70e-09 outlier — RESOLVED as an artefact

One v2 start reached ratio 1.70e-09. It is **not** a near-solution.

**The gauge group on P is 3-dimensional, not 2.** Beyond the translation
(`p_00`) and the overall scale (`P → cP, Q → Q/c`), the bracket forces a
**coordinate scale** `(x,y) → (λx, λ⁻³y)` — from `[P∘σ,Q∘σ] = λμ[P,Q]∘σ` and
`[P,Q] = x²`, giving `λ³μ = 1`. It maps solutions to solutions, since every
coefficient is multiplied by a nonzero power of λ.

**Why it broke v2's objective.** Composing with the `g1` that restores
`p_10 = 1`, the coefficient of `x^i` in `Q_j` scales by `λ^{i−3j+1}` — an
exponent that **depends on i**. Forbidden coefficients are the low-i ones,
allowed are high-i, so growing λ inflates the denominator of the ratio. Measured
on a random point, nothing solved anywhere along the path:

| λ | ratio | max\|allowed\| | max\|forbidden\| |
|---|---|---|---|
| 0.5 | 8.78e+10 | 1.55e+19 | 1.36e+30 |
| 1.0 | 8.32e+07 | 1.01e+05 | 8.93e+09 |
| 4.0 | 7.39e+02 | 5.66e-18 | 5.43e-19 |
| 16.0 | 9.78e-01 | 8.43e-37 | 7.19e-42 |

Eleven orders of magnitude, monotonically, with nothing solved. The outlier
carries exactly that signature: `max|allowed| = 2.16e+09` against
`max|forbidden| = 1.44`, with a **1.34e+09 dynamic range in P's own
coefficients**. A genuine near-solution shows small forbidden coefficients
against an **O(1)** configuration, not an inflated one.

**Verdict: ARTEFACT.** Same disease as v1, one gauge deeper — v1 collapsed the
numerator, v2's outlier inflated the denominator. Resolved, closed, not carried
forward.

## Where H1b stands

The pentagons remain **undecided**, and are now known to be a genuine
hit-target: dimension excludes nothing, the system is overdetermined by 1
modulo gauge plus 314 surplus conditions, and the only tractable handle is
evaluation. Next moves, in order: re-examine the 1.70e-09 outlier; replace
random-start Newton with homotopy continuation on the 59-dimensional gauge
slice; and port the Route-2-style independent reformulation the plan asks for,
so that any future verdict has two provenance-disjoint derivations.


## Standing requirement for any future pentagon detector

1. Fix **all three** gauges: `p_00 = 0`, plus two coefficients of **different
   weight `i − 3j`** (which pins `g1` and `g2` separately).
2. Use an **absolute** normalisation, not a ratio. A ratio objective is
   breakable from either end — v1 shrank the numerator, v2's outlier inflated
   the denominator.
3. Require the allowed coefficients to be **O(1)** as an *acceptance condition*,
   not a post-hoc sanity check.
