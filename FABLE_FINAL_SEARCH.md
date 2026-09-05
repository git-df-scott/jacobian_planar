# The corrected search, and what it shows: the equation is easy, the polygon is not

Fable, 2026-08-23. Code: `fable_xcol/truesearch.py`, `pinned.py`,
`verify924.py`. This supersedes every numerical result earlier in the session
(see `FABLE_ERRATUM_LADDER.md` for why those were invalid).

## The instrument, finally correct

Earlier searches scored by a ladder-internal residual that silently omitted the
conditions from kernel-carrying rungs. The corrected objective is the **complete
set of coefficients of `[P,Q] - x^K`**, computed from the explicit polynomials,
over a **fixed key set** so the residual cannot change length mid-optimisation,
with an **analytic Jacobian** (the bracket is bilinear, so it is exact and
cheap — this is what made the search feasible at all).

Controls: the exact pair `P = x^2/2, Q = y` scores bracket error **0**.

Collapse is self-penalising here: `P,Q -> 0` gives bracket `0`, so the residual
tends to `|x^K| = 1`, not `0`. No barrier is needed to exclude it.

## The result on (9,24) Prop 4.2 sub-case (3)

| search | `\|\|[P,Q] - x\|\|` | vertices |
|---|---|---|
| vertices **free** | **~1e-9** (machine zero) | collapse to ~1e-10 |
| vertices **pinned** (`p_18_6 = q_27_9 = 1`, scaling gauge) | **0.951** | nonzero by construction |

**`[P,Q] = x` is easily solvable** — the optimiser reaches machine precision
from random starts in ~30 s. **But every solution found has the Newton vertices
vanishing.** Pin them and the equation cannot be satisfied at all: 200 trials,
best residual 0.951, against 1.0 for "no cancellation whatsoever".

## What this means

The difficulty of this problem is **not** the differential equation. It is the
**Newton polygon**. The solution variety of `[P,Q] = x^K` is large and easy to
land on; the required polygon carves out a locus that the numerics cannot reach.
That is the same phenomenon as:

* the first-order obstruction (`FABLE_CE_STRATEGY.md`): `p_14_8` and `p_16_8`
  are pinned at zero by **every** tangent direction at a family-A point;
* the period criterion (`FABLE_PERIODS.md`): the degenerate families have
  simply-connected fibres, so the period conditions are vacuous there;
* the shape ranking (`FABLE_SHAPE_RANKING.md`): every admissible shape is
  over-determined, this one least so at slack -11.

Four independent routes, one conclusion: **solutions concentrate on the
degenerate stratum, and the nondegenerate locus is where the obstruction lives.**

## Verdict on this case

**Strong numerical evidence that (9,24) sub-case (3) is EMPTY** — which
*supports* GGHV Theorem 5.1 rather than refuting it. I had hoped this case might
expose a gap in that unreplicated theorem; the evidence points the other way.

Not a proof. A Gröbner certificate on the exact system is what would settle it,
and the numerics here have been wrong five times before being made right.

## Status

**No counterexample.** All examined shapes: NO VERDICT, with the numerical
evidence pointing toward emptiness in the two least-constrained ones —
(9,24) sub-case (3) and (8,28) sub-case (2).
