# Ranking every reduced shape below degree 125 — and the target it points to

Fable, 2026-08-23. Code: `fable_xcol/shapesweep.py` (exact, mod `2^31-1`).

The bottom-up freedom-vs-conditions accounting depends only on the two Newton
polygons and the bracket exponent, so it can be swept over shapes without
deriving each case's automorphism reduction. Run over every reduced shape GGHV
state explicitly (Prop 4.1, Prop 4.2's three sub-cases, Prop 4.3's two):

| shape | bracket | unknowns | freedom | conditions | **slack** | 1st gate |
|---|---|---|---|---|---|---|
| (9,27) Prop 4.1 | `x` | 252 | 46 | 193 | **-147** | 1 |
| (8,28) sub-case 1 — *the pentagon* | `x^2` | 184 | 25 | 137 | **-112** | 2 |
| (9,24) Prop 4.2 (1) | `x` | 186 | 32 | 140 | **-108** | 1 |
| (9,24) Prop 4.2 (2) | `x` | 120 | 21 | 90 | **-69** | 1 |
| (8,28) sub-case 2 — *quadrilateral* | `x^2` | 70 | 19 | 38 | **-19** | 9 |
| **(9,24) Prop 4.2 (3)** | `x` | **54** | **17** | **28** | **-11** | 1 |

`slack = freedom - conditions`; less negative means more room for a solution.

## What it says

Every shape this campaign has actually worked sits at slack **-108 or worse**.
The two shapes with real room are **(9,24) Prop 4.2 sub-case (3)** at **-11** and
**(8,28) sub-case (2)** at **-19** — the latter being the branch nobody had built
before today.

## The convergence that matters

**(9,24) Prop 4.2 sub-case (3) is the best-scoring shape in the entire sub-125
landscape, and it is closed only by Theorem 5.1 of GGHV section 5** — which this
campaign's own audit (`session43/COR57_TEST.md`,
`EXCLUSION_AUDIT_SUMMARY.md`) records as:

> *"the single highest-value unverified exclusion in the campaign"*

and notes that the same section's Corollary 5.7 *"rests on an imported Corollary
7.2 from GGV 2017 that nobody re-checked"*, with *"no third-party replication and
no erratum anywhere"*.

So a structural statistic computed from Newton polygons alone — with no
knowledge of the campaign's history — independently selects the exact case whose
exclusion the campaign already distrusts.

**If Theorem 5.1 has a gap, (9,24) Prop 4.2 sub-case (3) is where a plane
counterexample lives.** It is also the smallest system in the landscape (54
unknowns, 28 conditions), so it is the cheapest to attack once section 5 is
checked.

## Recommended order of work

1. **Verify GGHV Theorem 5.1 and its imported Corollary 7.2 (GGV 2017).** This
   is now the highest-value task in the campaign by two independent measures.
   If it holds, (9,24) is genuinely dead and the landscape below 125 reduces to
   sub-case (2) alone. If it has a gap, sub-case (3) is the prime target.
2. **Finish (8,28) sub-case (2)** — 38 conditions in 19 parameters, an explicit
   finite system; numerical search plateaus at ~3% residual with vertices
   nonzero, pointing toward EMPTY, but a Gröbner certificate is needed.
3. **Apply this same statistic to the 24 open cases above 125**
   (`FABLE_24_OPEN_CASES.md`) once their reductions are derived. It is the first
   principled way this campaign has had to choose a target rather than inherit
   one.

## Caveats

Slack is a heuristic, not a theorem: at several rungs candidate gates vanish
identically, so the conditions are demonstrably dependent and the true rank is
what decides each case. The counts are taken at a generic point reached by
random kernel choices; a special locus can behave differently (the
deleted-stratum hazard logged throughout this campaign).

## Status

No counterexample. All shapes: **NO VERDICT**. What is new is a measured
ranking of the whole sub-125 landscape and a specific, testable proposition
about where a witness could still be hiding.
