# The operator {u,-}: every cascade level collapses to ONE equation

## Setup

`u = x y^2 - tau y` is `w`-homogeneous of weight 1 (`w = deg_y - deg_x`) and
**primitive**: `u - c` is irreducible for generic `c` (the fibre is the rational
curve `x = (tau y + c)/y^2`).  So the ring of first integrals of `{u,-}` is
exactly `C[u]` — **CONTROL: PASS**.

On the weight-`k` basis `{x^i y^(i+k)}` the operator is explicitly **bidiagonal**:

    {u, x^i y^(i+k)} = (k - i) x^i y^(i+k+1) + tau * i * x^(i-1) y^(i+k)

mapping weight `k` to weight `k+1` — **CONTROL: PASS** at every `i, k` tested.
Its kernel on weight `k` is `span(u^k)`, and the coefficient recursion
`c_{m+1}/c_m = -(k-m)/(tau(m+1))` reproduces `u^k = sum_m C(k,m)(-tau)^(k-m)
x^m y^(m+k)` exactly.

## The collapse

At level `L` the two new unknowns are `P_{L-12}` and `Q_{L-8}`, each meeting a
known top form (`Q_12 = c1 u^12`, `P_8 = c0 u^8`).  Then

    {P_{L-12}, c1 u^12} + {c0 u^8, Q_{L-8}}
      = -12 c1 u^11 {u, P_{L-12}} + 8 c0 u^7 {u, Q_{L-8}}
      = u^7 * {u, 8 c0 Q_{L-8} - 12 c1 u^4 P_{L-12}}

**CONTROL: PASS**, symbolically, with `P_a` and `Q_b` free functions.  So writing
`W_L := 8 c0 Q_{L-8} - 12 c1 u^4 P_{L-12}`, level `L` is the single equation

    **{u, W_L} = -(known) / u^7 .**

## Two obstructions per level, both explicit

1. **Divisibility.**  The known part — everything carried down from higher
   levels — must be divisible by `u^7`.  This is a hard, checkable condition and
   there is no freedom to satisfy it with.
2. **Image.**  The quotient must lie in the image of the bidiagonal `{u,-}`.
   Since the kernel is one-dimensional, the image has codimension
   `dim(weight k+1) - dim(weight k) + 1` in the target, and both dimensions are
   read straight off the Newton polygon.

The solution `W_L` is then determined **up to `C[u]`**, i.e. up to one constant
per level.

## Why this matters to the campaign's history

`OPEN_ITEMS.md` calls the rational-function cascade *"the single blocker shared
by almost everything else"*, and three attempts at it were retracted after
manufacturing false obstructions.  `GENERAL_LADDER.md` diagnosed the cause: the
levels are first-order equations whose constants of integration ARE the kernel
freedom, and a greedy particular solution destroys them (the same mechanism as
ERRATA A3).

Here the kernel is **named**: it is `C[u]`, one constant per level, with `u`
explicit.  Nothing has to be guessed, so nothing can be greedily mis-chosen.

## Status

Pentagon **NO VERDICT**.  The cascade is now 22 levels of one equation each,
against a bidiagonal operator whose kernel, image and obstructions are all
computable from the Newton polygon alone.
