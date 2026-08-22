# Levels 10, 9, 8 — and where the descent actually ends

## The shape of the problem changed

The descent introduces new unknowns only in a finite window:

    new h piece at level L  <=>  L - 12 in [-1, 5]   <=>  L in [11, 17]
    new g piece at level L  <=>  L -  8 in [0, 11]   <=>  L in [ 8, 19]

So **levels 20 down to 8 introduce every unknown in the pentagon**, and
**levels 7, 6, 5, 4, 3, 2, 1, 0, -1, -2 introduce none**.  Those ten levels are
pure polynomial conditions on whatever carried parameters survive.  This is not
a rank computation any more; it is one explicit finite system.  Reaching level
8 was never the finish line — it is where the finish line begins.

## Level 10

    8 equations, 6 new unknowns (g2_0 .. g2_5), rank 5.

The left nullspace has dimension 3, so there are **three** gates:

    gate 3 :  32 g8_6 (3 g6_4 - g9_8^2)
    gate 2 :  8 (3 g6_4 g8_7 + 3 g6_5 g8_6 - 3 g8_6 g9_8 h5_5 - g8_7 g9_8^2)
    gate 1 :  linear in h2_2

**Correction of a natural misreading.**  `rank[M|v] - rank[M] = 1` here, and
that is *not* the number of conditions.  It measures how far `v` sits outside
the column space at a *generic* point of the carried-parameter space.
Consistency requires `n . v = 0` for **every** `n` in the left nullspace, so all
three gates are necessary.

gate 3 is a product, hence a union of two components:

  * on `3 g6_4 = g9_8^2`, gate 2 collapses to `24 g8_6 (g6_5 - g9_8 h5_5)`
  * on `g8_6 = 0`,        gate 2 collapses to `8 g8_7 (3 g6_4 - g9_8^2)`

Either way level 10 **closes**, with kernel 1 and residual identically zero.

## Level 9

Four gates.  gate 1 is a **perfect square**

    5 (2 g7_9 - 4 g8_9 + 9 h5_5)^2

so `2 g7_9 - 4 g8_9 + 9 h5_5 = 0` is forced: a single component, not a branch.
gate 4 is the product `8 g7_6 (3 g6_4 - g9_8^2)` (or `-4 g8_7^2 g9_8` on the
other level-10 component).  Level 9 **closes**.

## Level 8 — and the retraction it forced

Level 8 produced two **pure power** gates:

    gate 7 :  -8 g8_6^3     ->  g8_6 = 0
    gate 4 :  -4 g8_7^3     ->  g8_7 = 0

A pure power is unconditional — one component, no branch choice.  So the
`g8_6 != 0` branch taken at level 9 is **empty**, and every imposition derived
on it (`g9_8 = 0`, `h5_5 = 0`, `g5_4 = g8_6 g9_10 / 2`, `g7_9 = 2 g8_9`) is
**void**.  Same for `g8_7 != 0`.  Those impositions were discarded and the
bottom of the descent re-run from the level-19..11 solution with
`g8_6 = g8_7 = 0` imposed from the start.  On that component level 8 **closes**,
with gate 1 a second perfect square,

    -16 (3 g6_8 - 6 g7_8 + 9 g8_8 - g9_10^2 - 12 g9_8)^2 .

Level 8's solution divides by `g9_8`, so that branch carries `g9_8 != 0`.

## Level 7 and below

Level 7 gives seven pure conditions.  The last is `4 g7_6^2 g9_8 / 3`, so with
`g9_8 != 0` **`g7_6 = 0` is forced**, which annihilates two more of the seven.

## Which vertices must stay nonzero

From the Newton-polygon dictionary (`w = j - i`, `x^i y^(i+a) = y^a s^i`):

    p_8_0   = h_8 at s^0    = c0 tau^8      pinned by the witness
    p_16_8  = h_8 at s^8    = c0            pinned
    p_14_8  = h_6 at s^8    = leading coeff pinned
    q_12_0  = g_12 at s^0   = c1 tau^12     pinned
    q_24_12 = g_12 at s^12  = c1            pinned
    q_21_12 = g_9  at s^12  = g9_12         **NOT automatic** — must be checked

`g9_12` is determined by the descent and must be verified nonzero before any
candidate counts as a counterexample.

## A soundness check on the z-basis

Every free support `hsup(a)`, `gsup(b)` is exactly `{0, 1, ..., d}`.  A support
that is contiguous from 0 spans the same space in the `z = s - tau` basis as in
the `s` basis, so rewriting each piece in `z` loses nothing and adds nothing.
The only non-contiguous supports are `hsup(-1) = {1}` and `gsup(-1) = {2}` —
the two gauge-fixed pieces, which are set to `s` and `s^2` exactly rather than
expanded in `z`.  Checked.

## Status

Pentagon **NO VERDICT**.  No explicit `(P, Q)` yet.  The remaining content is
the ten-level pure-condition system at levels 7 down to -2.
