# The x-degree <= 1 stratum is at least 3-dimensional

Family B (`FAMILY_B.md`) turns out to be a 1-parameter slice of a larger family.

## The family

    sigma(y) = 1 + lambda y                                   (forced: see below)
    f(y)     = y + c_2 y^2 + c_3 y^3 + c_4 y^4 + c_5 y^5      (c_6 = c_7 = c_8 = 0)
    P(x,y)   = x sigma(y) + f(y)

subject to **two relations**:

    (i=1 block, linear)      c_2 = ( 3 c_3 lam^5 - 6 c_4 lam^4 + 10 c_5 lam^3 ) / lam^6
    (i=0 block, quadratic)   3 c_3 lam^2 - 8 c_4 lam + 15 c_5 = lam^4

Three free parameters: `lambda, c_4, c_5`, with `c_3` and `c_2` determined.
Family B is the slice `c_4 = c_5 = 0` (then `c_3 = lam^2/3`, `c_2 = lam`,
i.e. `f' = sigma^2`).

## How it was found

For P affine in x the three x-slots of Q decouple (`FAMILY_B.md`):

- **i=2** is the ODE `sigma R' - 2 sigma' R = 1`, forcing `sigma = 1 + lambda y`
  (checked for `deg sigma = 1,2,3`; higher coefficients driven to zero).
- **i=1** is *linear* in the coefficients of f, and gives exactly one relation —
  at general lambda the one above, whose `lambda = 1` case has binomial
  coefficients `3, -6, 10, -15, 21, -28`.
- **i=0** is quadratic, and its first equation factors as a perfect square:

      15 lam^6 ( 3 c_3 lam^2 - 8 c_4 lam + 15 c_5 - lam^4 )^2

  so the quadratic block reduces to one linear condition on the same
  coefficients.  (At `lambda = 1` this is `(3c_3 - 8c_4 + 15c_5 - 1)^2`.)

## Verification

All 66 conditions evaluated at eight independent parameter choices:

| lambda | c_4 | c_5 | result |
|---|---|---|---|
| 1 | 0 | 0 | 66/66 |
| 1 | 1 | 0 | 66/66 |
| 1 | 0 | 1 | 66/66 |
| 2 | 0 | 0 | 66/66 |
| 2 | 1 | 0 | 66/66 |
| 3 | 2 | 5 | 66/66 |
| 5 | 1/2 | -1/3 | 66/66 |
| 7 | 3 | 1 | 66/66 |

Including rational and larger parameter values, so this is not a small-integer
coincidence.

## Scope, stated carefully

- The `sigma = 1 + lambda y` step assumes **Q polynomial**; for the truncated
  export the i=2 conditions are weaker.  An msolve run on that 9-variable block
  segfaulted under a 3 GB `ulimit` (exit 139, 71 s) — **NO VERDICT**, and the
  cap's fault, not the mathematics'.
- I set `c_6 = c_7 = c_8 = 0` from the `lambda = 1` Groebner basis, whose other
  elements (`c_7(c_5 c_7 - 2 c_6^2)`, `c_5 c_8 + c_6 c_7`, `c_6^3 c_7`,
  `c_6 c_7^2`, `2 c_6 c_8 + c_7^2`) admit **further branches** — e.g.
  `c_6 = c_7 = 0` with `c_8` free requires `c_5 c_8 = 0`.  Those branches are
  not explored, so this is a **verified family, not a complete classification**
  of the stratum.

## Why it matters

The degenerate locus of `pent_L23.ms` is now known to contain at least
`4 + 3 = 7` parameters' worth of solutions across two strata, none of which is
anywhere near a (72,108) configuration — every member has `p_{j,i} = 0` for
`i >= 2`, hence all three P-vertices `p_8_0, p_14_8, p_16_8` vanish.  The
unsaturated export is very far from saying what the campaign wanted it to say,
and each additional family makes the case stronger that the saturated
formulation is the only meaningful target.
