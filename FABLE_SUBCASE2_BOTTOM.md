# Sub-case (2) from the bottom: the low rungs collapse to two parameters

Fable, 2026-08-23. Code: `fable_xcol/sc2bottom.py` (verified, with a Gröbner
certificate), `sc2ladder.py`. Complements the top-down x-column descent, which
is independently running through rung 10.

Structural facts already proved (`FABLE_SOURCE_AUDIT.md`): the hull of
sub-case (2) meets `x = 0` only at the origin, so after the additive gauge
`a_0 = b_0 = 0` — `P` and `Q` are both divisible by `x` — and `a_1(0) != 0`
because it *is* the Newton vertex `(1,0)`.

## Rung 0 forces `b_1 = 0`

Rung `d = 0` is `a_1 b_1' - a_1' b_1 = 0`, a vanishing Wronskian, so `b_1 = c·a_1`.
But `a_1` has a nonzero constant term (the vertex) while `b_1` is supported on
`y^1..y^2`, so `c = 0`:

    **b_1 == 0**

Certificate, not just a solve: the Gröbner basis of
`{rung 0, a1_0 invertible, b_1 != 0}` is **[1]** — no such point exists.

## Rung 2 collapses the rest of the bottom

With `b_0 = b_1 = 0` and `a_0 = 0`, rung `d = 1` is vacuous and rung `d = 2` —
the only rung carrying the `x^2` on the right — reduces to the single ODE

    a_1 b_2' - 2 a_1' b_2 = 1 ,   b_2 supported on y^1..y^4 .

Solved exactly, one branch:

    a1_2 = 0 ,   a1_1 = 2 a1_0^2 b2_2 ,   b2_1 = 1/a1_0 ,   b2_3 = b2_4 = 0

so, writing `A = a1_0` and `B = b2_2`,

    **a_1 = A (1 + 2 A B y) ,   b_2 = y/A + B y^2**

verified by direct substitution. The bottom block therefore goes from **9
coefficients to 2 free parameters** `(A, B)`, with `A != 0`.

## A correction to my own hand argument

I first claimed `a_1` must be a *constant*, by integrating
`(b_2/a_1^2)' = 1/a_1^3` and observing that `a_1` with a simple root gives
`b_2 = -1/(2c)`, a nonzero constant, which violates `val(b_2) >= 1`.
**That was wrong: I dropped the constant of integration.** The general solution
is `b_2 = a_1^2 (INT dy/a_1^3 + K)`, and for `a_1 = c(y-r)` the choice
`K = 1/(2 c^3 r^2)` kills the constant term and leaves a genuine polynomial. So
`a_1` may be linear, exactly as the exact solve reports.

This is the campaign's own erratum class A14 — *"the rank drop is the ODE's free
constant of integration"* — and I reproduced it within the hour. Recording it
because the failure mode is evidently easy to repeat.

## Where this leaves sub-case (2)

Two independent attacks are now closing on it from both ends:

* **top-down** (x-column descent): rungs 18 → 10 closed, gates at 17/15/13/11
  only, zero branch points, denominators confined to forced-nonzero vertices,
  and **zero free parameters left at rung 10**;
* **bottom-up** (this note): rungs 0, 1, 2 closed, `b_1 = 0`, and the bottom
  block down to two parameters `(A, B)`.

The gap is the middle rungs. Sub-case (2) is 92 equations in 70 unknowns, and
both ends are now pinned, so the remaining work is genuinely small — this is
the branch most likely to yield a *certificate* (either an explicit point or an
emptiness proof), which is what the mission asks for.

## Status

No counterexample. Sub-case (2): **NO VERDICT**, but materially closer than any
chart in this campaign has been.
