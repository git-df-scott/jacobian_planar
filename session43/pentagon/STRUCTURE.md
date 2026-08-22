# Structural consequences of {P,Q} = x^2 — with their hypotheses stated

**Correction notice.**  An earlier version of this file asserted §1 and §2 as
constraints on the *exported* pentagon system.  That was wrong, and the error is
recorded rather than quietly fixed.  Both arguments require **Q to be a
polynomial in y**.  In `pent_L23.ms` Q is only a power series in y truncated at
level 23, and the conditions constrain levels 13..23 alone — so a factor like
`(1+g)^{-3}` may legitimately be expanded as a series and nothing forbids it.
The arguments below are therefore statements about the **idealised problem**
(`{P,Q} = x^2` with P and Q both polynomials), which is what an actual
counterexample would have to satisfy, and **not** about the truncated export.

## 1. Idealised problem: x-degree-1 solutions are forced degenerate

Let `P = x(1+g(y)) + f(y)` and require **Q polynomial**.  `u = P` is a first
integral, `x = (u-f)/(1+g)`, and the equation collapses to

    Q_y|_u  =  x^2 / P_x  =  (u - f)^2 / (1+g)^3 .

An antiderivative of a rational function is a polynomial only if the function
already is one.  The coefficient of `u^2` is `1/(1+g)^3`, so `1+g` must be a
nonzero constant, i.e. `g` is constant, i.e. `p_{j,1} = 0` for all `j >= 1`.
Together with `f` free this is exactly the degenerate family of
`DEGENERATE_FAMILY.md`.

**Scope: idealised problem only.**  For the truncated export the step fails, and
what I actually have there is evidence, not proof: putting a single nonzero
`p_{j,1}` on top of the degenerate family leaves 21–26 of the 66 conditions
nonzero at a random point (j = 2..6), and the one-parameter scan over all 58
coordinates found no nonzero root.  Random points miss measure-zero loci — the
same objection I raised against the r=45 slice search — so this is
**NO VERDICT**.

## 2. Idealised problem: the leading relation is the campaign's bottom edge

Let `P = sum_{i<=m} a_i(y) x^i`, `Q = sum_{j<=n} b_j(y) x^j`, both **polynomial**,
`a_m, b_n != 0`.  `P_x Q_y` and `P_y Q_x` both have x-degree `m+n-1`.  When
`m+n-1 > 2` the right-hand side `x^2` cannot reach that degree, so the leading
coefficients cancel:

    m a_m b_n' - n a_m' b_n = 0   =>   **b_n^m = c a_m^n** .

For `(m,n) = (2,3)` the differential form of this is precisely

    2 f g' - 3 f' g = 0,

the homogeneous version of the campaign's bottom-edge equation
`2 f g' - 3 f' g = w^2` (`wave6/bottomedge/analyse.py`).  The `w^2` appears
exactly in the boundary case `m+n-1 = 2`, where `x^2` does reach the top degree.

So in the idealised problem **the bottom edge is the leading-coefficient
relation of `{P,Q} = x^2`**, and the 2,3-weighting that runs through the whole
campaign is its `(m,n) = (2,3)` instance.  This part is unaffected by the
truncation caveat, because the campaign's bottom edge is itself a statement
about polynomials `f, g`.

## 3. A derived, unverified case split for the saturated question

If the export is saturated at the corner (`p_16_8 != 0`) then `m = 8`, and

    a_8(y) = y^14 ( p_14_8 + p_15_8 y + p_16_8 y^2 ) .

In the idealised problem §2 forces `a_8 = lambda h^{8/g}` with `g = gcd(8,n)`.
Valuation 14 then forces `8/g` to divide 14, so `8/g in {1,2}`, i.e.
`g in {4,8}`, giving

    n = 8            (g = 8),      or
    n in {4,12}      (g = 4, and then p_15_8^2 = 4 p_14_8 p_16_8) .

A finite case split, cheap to impose before any solver — the lockpick strategy
rather than sampling the ambient space.  **Derived, not verified, and subject to
the same idealised-problem hypothesis.**  Recorded as a lead.

## Status

§2 is exact for polynomial (P,Q).  §1 is exact for polynomial (P,Q) and does
**not** transfer to the export.  §3 is derived and unchecked.  Nothing here is a
verdict on `pent_L23.ms`.
