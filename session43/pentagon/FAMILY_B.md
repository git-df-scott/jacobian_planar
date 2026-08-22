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
