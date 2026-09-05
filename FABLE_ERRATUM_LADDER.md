# ERRATUM: the ladder residual did not measure the bracket. Signal retracted.

Fable, 2026-08-23. Code: `fable_xcol/verify924.py`.

## What was claimed

The (9,24) Prop 4.2 sub-case (3) search reported a residual descending steadily
`7.7e-2 -> 4.6e-2 -> 3.2e-2 -> 2.4e-2 -> 1.5e-2 -> 1.1e-2` with the Newton
vertices **growing** rather than collapsing. I reported that as the first
non-collapse signal of the session and as the live thread.

## What is true

**The residual was not measuring `[P,Q] - x`.** Verified by building `P` and `Q`
as explicit polynomials from the ladder's own output and computing the bracket
directly:

    control  P = x^2/2, Q = y      ->  bracket error 0            (instrument OK)

    best ladder point, ||F|| = 1.087e-02:
        max |coefficient of ([P,Q] - x)|      = 6.87e+01
        relative to the bracket's own scale   = 1.000000
        nonzero error coefficients            = 75

**A relative error of exactly 1.0 means the bracket does not cancel at all.**
The point is not close to a solution in any sense.

## The bug

In `case924.run`, residuals were appended only on rungs where the coefficient
matrix had full column rank. Wherever the rung had a nontrivial kernel, the code
took the kernel directions as free parameters and **appended nothing** — so the
conditions imposed by those rungs were never entered into the objective. The
optimiser was minimising a strict subset of the equations while the remainder
went entirely unchecked, which is why the "residual" could fall while the actual
bracket error stayed at 100%.

The same defect affects the `sc2solve.py` numbers for sub-case (2). Its ~3e-2
plateau should be treated as **unverified** until re-measured against the direct
bracket. (Its *structural* results — the rank/gate/freedom counts in
`FABLE_BRANCH_RANKING.md` and `FABLE_SHAPE_RANKING.md`, computed in exact mod-p
arithmetic — are unaffected, because they never used this residual.)

## The rule this establishes

**No search number in this problem means anything until the candidate's
polynomials are built and the bracket is computed directly.** The ladder is a
convenient parametrisation, not a measurement of the equation. Every optimiser
here will happily minimise whatever subset of the system it is handed.

This is the fifth degeneracy/measurement trap encountered, after:
1. the bihomogeneous scaling collapse (VARPRO),
2. the min-norm kernel collapse (`lstsq` returning 0 on a homogeneous rung),
3. the high-column collapse (rungs 13-19 vanishing as `a_3..a_8 -> 0`),
4. `lstsq` least-squaring through an *inconsistent* rung, masking a real gate,
5. **this one** — residuals silently omitted on kernel-carrying rungs.

Traps 1-4 produced encouraging numbers that dissolved on exact recheck. Trap 5
is the first that would have produced a **false counterexample claim**, and it
was caught only by the end-to-end bracket check. That check is why
`fable_xcol/verify.py` exists and why nothing is called a witness until it
passes.

## Status

No counterexample. (9,24) sub-case (3): **NO VERDICT**, and the encouraging
signal is **withdrawn**. The correct instrument for any future search on this
case is: parametrise by the ladder, but score by the direct bracket error.
