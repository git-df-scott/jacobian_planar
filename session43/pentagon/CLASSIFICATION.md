# Complete classification of the x-independent stratum — exact, over Q

A theorem rather than an observation.  `DEGENERATE_FAMILY.md` exhibited
solutions with `deg f <= 5`; this shows there are **no others** in that stratum.

## Setup

Take `P = x + f(y)` (every `p_{j,i} = 0` for `i >= 1`).  The pentagon support
allows `p_{j,0}` for `j <= 8`, so `f = y + c_2 y^2 + ... + c_8 y^8`, the gauge
being `c_1 = p_1_0 = 1`.  Solving `{P,Q} = x^2` with `u = P` as first integral
gives, in closed form,

    Q  =  x^2 y  +  2x ( y f(y) - F(y) )  +  G(y),
    F(y) = int_0^y f,     G(y) = int_0^y ( f(y) - f(s) )^2 ds .

So Q has **only three x-coefficients**.  The 66 conditions `Q[j][i] = 0`
(j = 13..23, i = 0..j-13) therefore collapse:

- `i = 2` slot is `y`, which has no `y^j` for `j >= 2` — automatic;
- `i = 1` slot is `2(y f - F)`, of degree `<= 9 < 14` — automatic;
- `i = 0` slot is `G`, of degree `<= 17`, so exactly the coefficients of
  `y^13 ... y^17` must vanish.

**Five equations, and they are explicit:**

    y^17 :  128 c_8^2 / 153
    y^16 :  119 c_7 c_8 / 72
    y^15 :  ( 2048 c_6 c_8 + 1029 c_7^2 ) / 1260
    y^14 :  5 ( 80 c_5 c_8 + 81 c_6 c_7 ) / 252
    y^13 :  ( 25088 c_4 c_8 + 25725 c_5 c_7 + 12960 c_6^2 ) / 16380

## The cascade

`y^17` forces `c_8 = 0`.  Then `y^15` reads `1029 c_7^2 = 0`, forcing `c_7 = 0`.
Then `y^13` reads `12960 c_6^2 = 0`, forcing `c_6 = 0`.  The remaining two
equations are then identically satisfied, and `c_2, c_3, c_4, c_5` are free.

`sympy.solve` on the five equations returns exactly one solution family:
`c_6 = c_7 = c_8 = 0`.

## Theorem

**The solutions of the exported pentagon system with `P = x + f(y)` are exactly
`deg f <= 5` — a 4-parameter family, and nothing else.**  Exact, in
characteristic zero.

The three squares `c_8^2`, `c_7^2`, `c_6^2` appearing as the top coefficients
are the reason the cut-off is sharp: each top coefficient of `G` is a perfect
square in the leading unknown, so the cascade is forced and cannot branch.  It
also explains the `2 deg f + 1 = 13` boundary observed numerically -- `deg f = 6`
makes `deg G = 13` and switches on exactly the `y^13` equation, which is the one
condition that broke in the numerical test.

## Why it matters

1. It settles the stratum completely, so no further search there is needed --
   by either agent.  Codex's claimed chart `{p_1_1 = 0, p_1_0 != 0}` contains
   all of it.
2. Every member has `p_{j,i} = 0` for `i >= 1`, hence `p_16_8 = 0`.  So
   saturating at the pentagon vertex `p_16_8` removes this entire family, which
   confirms that the saturated question is the right corrected target.
3. It is a worked example of the export's defect: a whole 4-dimensional family
   of solutions that are nowhere near a (72,108) configuration, admitted because
   the export carries no non-degeneracy conditions.

## Status

Exact and complete for the stratum `P = x + f(y)`.  Says nothing about strata
with `i >= 1`, which remain `NO VERDICT`.
