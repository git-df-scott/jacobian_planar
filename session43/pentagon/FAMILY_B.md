# A second degenerate family — and it lies in the *rigid* chart

`DEGENERATE_FAMILY.md` and `CLASSIFICATION.md` settled the stratum
`P = x + f(y)` (all `p_{j,i} = 0` for `i >= 1`), which has `p_1_1 = 0`.  This is a
structurally different family with **`p_1_1 != 0`**, so it sits inside the rigid
chart `{p_1_0 != 0, p_1_1 != 0}` that `PENTAGON_RIGIDITY.md` left open.

## The family

For every `lambda`:

    sigma(y) = 1 + lambda y
    f(y)     = y + lambda y^2 + lambda^2 y^3 / 3          (equivalently  f' = sigma^2)
    P(x,y)   = x sigma(y) + f(y)
    Q(x,y)   = x^2 y + x y^2 + y^3/3
               + lambda ( x^2 y^2/2 + 4 x y^3/3 + 7 y^4/12 )
               + lambda^2 ( x y^4/3 + y^5/3 )
               + lambda^3 y^6/18

In pentagon coordinates: `p_1_0 = 1`, `p_1_1 = lambda`, `p_2_0 = lambda`,
`p_3_0 = lambda^2/3`, all other `p_{j,i} = 0`.

## Verification

| check | result |
|---|---|
| `{P,Q} = x^2`, symbolic in `lambda` over Q | **exact** |
| Q polynomial in (x,y) | **yes** |
| 66 conditions, my evaluator, `lambda = 1,2,3,5,1000` | **66/66 vanish, every value** |
| 66 conditions, substituted into the **original** `pent_L23.ms` (`lambda = 1`) | **66/66 vanish** |

## Why `f' = sigma^2` is the right condition

With `u = P` as first integral, `Q_y|_u = x^2/P_x = (u-f)^2 sigma^{-3}`, so
`Q = int_0^y (u-f(t))^2 sigma(t)^{-3} dt`.  For `sigma = 1 + lambda t`,
`sigma^{-3} dt = -d(sigma^{-2})/(2 lambda)`, and integrating by parts,

    int (u-f)^2 sigma^{-3} dt
      = -(1/(2 lambda)) (u-f)^2 sigma^{-2}  -  (1/lambda) int (u-f) f' sigma^{-2} dt .

Setting **`f' = sigma^2`** kills the `sigma^{-2}` in the remaining integral, so it
becomes `-(1/lambda) int (u-f) dt`, a polynomial; and the boundary term is
polynomial too because `u - f = x sigma`, so `(u-f)^2 sigma^{-2} = x^2`.  Both
pieces are polynomial exactly when `f' = sigma^2`.  That is the whole mechanism.

## Consequence

The exported pentagon system is **NONEMPTY in both charts**:

| chart | verdict |
|---|---|
| `p_1_1 = 0` (Codex's claimed stratum) | **NONEMPTY** — family A, 4-parameter, classified exactly |
| `p_1_1 != 0` (the rigid chart) | **NONEMPTY** — family B above |

So the last open chart of the rigidity analysis is closed, and closed the wrong
way for the campaign: there is no chart in which `pent_L23.ms` is empty.  Every
Groebner attack on it was doomed regardless of engine, budget or gauge.

Both families have `p_{j,i} = 0` for all `i >= 2`, hence `p_16_8 = 0`.  So the
saturation at the pentagon vertex `p_16_8` still removes both, and the saturated
question remains the right corrected target — and remains **NO VERDICT**.

## Wider point

Two structurally unrelated families surfaced within an hour of asking the
question properly, after forty sessions in which the system was only ever
attacked head-on.  Both were found by *evaluating* rather than eliminating: the
straight-line evaluator makes a point-test cost milliseconds, so sparse and
structured points can be swept directly.  The lesson for the remaining targets
is that a cheap exact evaluator plus a sparse sweep should precede any Groebner
budget, and that any export lacking explicit non-degeneracy rows should be
assumed to admit families like these until checked.

## Deformation sweep into x-degree >= 2 (evidence, not proof)

Both known families have `p_{j,i} = 0` for all `i >= 2`, i.e. P is affine in x.
The natural question is whether either deforms into genuine x-degree.

Swept all 42 coefficients with `i >= 2`, one at a time, along family B at
`lambda = 1` and `lambda = 7`: for each, the 66 conditions were interpolated
exactly as univariate polynomials in the new coefficient `t` (degree <= 11), and
their GCD taken.  A common nonzero root would be a deformation.

**Result: 0 of 42, at both lambda values.**

**Control error, recorded.**  The first version of this sweep reported all 84
cases as candidates with a degree-1 GCD.  Those were spurious: the GCD was `X`
itself, whose root is `t = 0` — the base point of the family, which is a
solution by construction.  Stripping the trivial root leaves nothing.  A sweep
whose "hits" are all the point you started from is finding its own input, and it
would have been easy to report the first run as 84 leads.

So on these families the answer is that no single `i >= 2` coefficient can be
switched on.  That is **evidence, not a proof**: it tests one-parameter
deformations along two lines, and a solution with several `i >= 2` coefficients
simultaneously nonzero would not be seen.  `NO VERDICT` on the saturated
question stands.

## Why sigma must be affine: the i=2 block is an ODE

The `i = 2` slot of Q is `R = sigma^2 * int_0^y sigma^{-3}`.  Differentiating,
`R' = 2(sigma'/sigma) R + 1/sigma`, i.e.

    **sigma R' - 2 sigma' R = 1** ,     sigma(0) = 1,  R(0) = 0 .

So the `i = 2` conditions say precisely that this linear ODE has a solution R
which is a polynomial (for the idealised problem; the export only needs its
coefficients `y^15..y^23` to vanish).

Degree count: if `deg sigma = d` then `deg R = 2d` (the top terms of `sigma R'`
and `2 sigma' R` cancel unless `d + deg R - 1 = 0`), giving `3d + 1` unknowns
against `3d` conditions — a 1-parameter family expected at every d.  Solving it:

| `deg sigma` | polynomial solutions |
|---|---|
| 1 | `sigma = 1 + lambda y`, `R = y + lambda y^2/2` |
| 2 | **same** — the quadratic coefficient is forced to 0 |
| 3 | **same** — both higher coefficients forced to 0 |

(`d = 4` exceeded the solve budget; `d <= 3` is what is checked.)

So the expected 1-parameter family at each degree collapses onto the affine one:
**`sigma` must be `1 + lambda y`.**  There is no `deg sigma = 2` or `3` analogue,
which is why family B has a single parameter and why the sweep above found no
deformation into higher x-degree.  It also confirms, from a second direction,
that the `i >= 2` coefficients of P cannot be reached from these strata.

Scope: this classifies the **idealised** problem (Q polynomial).  For the
truncated export the conditions are weaker, so it is a strong indication rather
than a proof there.
