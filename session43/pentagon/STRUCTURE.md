# Structural consequences of {P,Q} = x^2

Derived from the bracket form (`BRACKET.md`).  These are necessary conditions on
any solution, so they prune the search rather than merely describing it.

## 1. Solutions with x-degree 1 in P are forced to be degenerate

Write `P = x(1+g(y)) + f(y)` (the general P of x-degree <= 1 with the gauge).
`u = P` is a first integral of the bracket, and in coordinates `(u,y)`,
`x = (u-f)/(1+g)`, so the equation collapses to

    Q_y|_u  =  x^2 / P_x  =  (u - f)^2 / (1+g)^3 .

An antiderivative of a rational function is a polynomial only if the function is
already a polynomial.  Reading off the coefficient of `u^2`, we need
`1/(1+g)^3` to be a polynomial in y, hence `1+g` is a nonzero constant, hence

    **g is constant.**

In the pentagon variables `g(y) = sum_j p_{j,1} y^j`, so this says
`p_{j,1} = 0` for all `j >= 1`.  Combined with `f` free, the x-degree-1 solutions
are exactly the degenerate family of `DEGENERATE_FAMILY.md`.

This is consistent with the one-parameter scan: every family
`p_1_0 = 1, p_{j,1} = t` was scanned and none admitted a nonzero root.

## 2. The leading-coefficient relation, and why it is the campaign's bottom edge

Write `P = sum_{i<=m} a_i(y) x^i` with `a_m != 0`, and `Q = sum_{j<=n} b_j(y) x^j`
with `b_n != 0`.  Both `P_x Q_y` and `P_y Q_x` have x-degree `m+n-1`.  When
`m+n-1 > 2` the right-hand side `x^2` cannot supply that degree, so the leading
coefficients must cancel:

    m a_m b_n' - n a_m' b_n = 0
    =>  b_n'/b_n = (n/m) a_m'/a_m
    =>  **b_n^m = c a_m^n**   for a constant c.

This is the classical cusp / resonance relation.  For `(m,n) = (2,3)` it reads
`b_3^2 = c a_2^3`, whose differential form is exactly

    2 f g' - 3 f' g = 0,

i.e. the homogeneous version of the campaign's bottom-edge equation
`2 f g' - 3 f' g = w^2` (`wave6/bottomedge/analyse.py`).

So the bottom edge is not a separate object bolted on to the pentagon: **it is
the leading-coefficient relation of `{P,Q} = x^2`**, with `w^2` appearing exactly
in the boundary case `m+n-1 = 2` where `x^2` does reach the top degree.  The
`2,3` weighting that runs through the whole campaign is the `(m,n) = (2,3)`
instance of this identity.

## 3. Where this leaves the search

Any non-degenerate solution needs `m >= 2` (x-degree at least 2 in P), and then
its top coefficients are pinned by `b_n^m = c a_m^n` -- a strong, cheap,
necessary condition that can be imposed *before* any Groebner work, exactly the
lockpick strategy (derive necessary conditions, parameterise their locus, search
there) rather than sampling the ambient space.

Status: derivations above are exact; no witness and no emptiness proof for the
saturated system.  `NO VERDICT` there.
