# The plan, and an honest search-space argument

## Instrument built: the forced-vertex oracle

`forced.py`.  The 66 conditions are exactly affine in the 13 late variables and
`p_16_8` is one of them.  So instead of solving for the late block and hoping
`p_16_8` comes out nonzero — it is 0 on every known family — **force it to 1**
and make consistency the question:

    M' . late'  =  -(v + m) ,      m = the p_16_8 column, late' the other 12

Consistent  <=>  `rank(M') == rank([M' | -(v+m)])`.  Milliseconds per point, and
a consistent early point is a genuine solution with `p_16_8 != 0`, i.e. a
counterexample candidate subject to the six-vertex test.

Controls, all passing:

| control | result |
|---|---|
| planted right-hand side (Example 10) | consistent, rank 12/12 |
| right-hand side perturbed off the column space | inconsistent |
| **real data:** families A and B, which have `p_16_8 = 0` | **correctly inconsistent** |

The third is the one that matters: the instrument says NO on points where the
answer is known to be no, for the right reason.

## Why this instrument cannot be pointed at random points

Generic early points give rank 12 vs 13 — inconsistent.  That is not bad luck,
it is the geometry: the consistency locus has **codimension ~54 in a
46-dimensional early space**.  Sampling points, sampling lines, or sampling
sparse supports cannot meet a locus of that codimension; the probability is
`O(p^-54)`.

This is exactly the criticism I made of `pent/pent_slice.py`, and it applies to
me with equal force.  **Any plan of the form "run the fast oracle over many
points" is dead on arrival**, and saying so now is cheaper than discovering it
after a few million evaluations.

## What follows: only structure can find this

Every result obtained so far came from **closed-form reduction**, and each one
worked by collapsing the 66 conditions into a handful of explicit equations:

- x-independent stratum: 66 conditions -> 5 equations, cascading through perfect
  squares `128 c_8^2`, `1029 c_7^2`, `12960 c_6^2` to `c_6 = c_7 = c_8 = 0`.
- x-degree <= 1: the three x-slots of Q decouple; `i=2` is the ODE
  `sigma R' - 2 sigma' R = 1` forcing `sigma` affine; `i=1` is linear in f;
  `i=0`'s first equation factors as
  `15 lam^6 (3c_3 lam^2 - 8c_4 lam + 15c_5 - lam^4)^2`.

Against four saturated Groebner attempts, all NO VERDICT, across both
representations and a 10x budget range.

## Today's order of work

1. **x-degree 2 in closed form.**  Complete the square: `P = a(x + b/2a)^2 + e`,
   so with `w = x + b/2a` and `w^2 = (u-e)/a`,

       Q_y|_u  =  x^2/P_x  =  w/(2a)  -  b/(2a^2)  +  b^2/(8a^3 w) .

   Q is polynomial in `(x,y)` hence in `(w,y)`; the odd-in-`w` terms are the
   obstruction.  This is a finite computation, not a search, and it is the
   direct analogue of what settled x-degree <= 1.

2. **The vertex constraints as a parametrisation, not a filter.**  For a genuine
   solution `m = 8`, so `a_8(y) = y^14 (p_14_8 + p_15_8 y + p_16_8 y^2)` and the
   leading relation `b_n^8 = c a_8^n` forces `4 | n`, hence `n in {4,8,12}` given
   `n <= 13`; and for `n = 4, 12` it forces the quadratic to be a perfect square,
   `p_15_8^2 = 4 p_14_8 p_16_8`.  With `p_16_8 = 1` that is
   `p_15_8 = 2s, p_14_8 = s^2` — still **affine in the remaining 10 late
   variables**, so the oracle survives the substitution and the search space
   drops by two dimensions per branch.  (Idealised-problem hypothesis: needs Q
   polynomial.)

3. **Only then**, with the residual system small enough, hand it to a solver.

## Honest odds

Low.  Forty sessions plus last night have produced no witness, and the
codimension argument above says the remaining freedom is small.  What is
realistic today is another structural reduction — and the reason to want one is
that each reduction so far has shrunk the problem by an order of magnitude, and
that is the only trend in the campaign pointing the right way.
