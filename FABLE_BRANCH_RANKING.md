# Which branch could actually hold a counterexample? A quantitative answer

Fable, 2026-08-23. Code: `fable_xcol/pentcount.py` (exact, mod `2^31-1`).

The same bottom-up freedom-vs-gate accounting, run on **both** sub-cases of GGHV
Prop 4.3 with the new-unknown index derived from the supports rather than
hardcoded. This is the first quantitative comparison of the two branches.

## Pentagon, sub-case (1) — 184 unknowns

| rung | eqs | new | rank | gates | freedom added | cum |
|---|---|---|---|---|---|---|
| -1 | 0 | 20 | 0 | 0 | **20** | 20 |
| 0 | 21 | 23 | 21 | 0 | 2 | 22 |
| 1 | 21 | 23 | 21 | 0 | 2 | 24 |
| **2** | 22 | 21 | 20 | **1** | 1 | 25 |
| 3–11 | … | … | … | 1,3,5,6,7,10,10,10,10 | 0 | 25 |
| 12–19 | | 0 | – | 13,12,11,10,9,8,7,4 | 0 | 25 |

**Total freedom 25; total conditions ≈ 137. Over-determined by ~112.**
First obstruction at **rung 2** — almost immediately.

## Quadrilateral, sub-case (2) — 70 unknowns

| rung | eqs | new | rank | gates | freedom added | cum |
|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 0 | 0 | **5** | 5 |
| 2–8 | 6 | 7 | 5 | 0 | 2 each | 19 |
| **9** | 6 | 4 | 4 | **1** | 0 | 19 |
| 10–12 | 6 | 4 | 4 | 1 each | 0 | 19 |
| 13–19 | 6 | 0 | – | 5,5,5,5,5,5,4 | 0 | 19 |

**Total freedom 19; total conditions ≈ 38. Over-determined by ~19.**
First obstruction at **rung 9** — seven rungs later than the pentagon.

## The ranking

| | pentagon (1) | quadrilateral (2) |
|---|---|---|
| unknowns | 184 | 70 |
| freedom created | 25 | 19 |
| conditions | ~137 | **~38** |
| over-determined by | **112** | **19** |
| first gate at rung | **2** | **9** |

**Sub-case (2) is close to six times less over-determined than the pentagon, and
its first obstruction appears seven rungs later.** By this measure it is by a
wide margin the better place for a counterexample to live — and it is the branch
nobody had built before today.

Conversely the pentagon, which this campaign has worked for weeks, is
over-determined by 112 conditions against 25 parameters. That is consistent with
its six independent EMPTY verdicts and suggests those were not accidents of the
particular slice: the branch is structurally starved of freedom.

## Honest caveats

- Over-determination is a heuristic, not a proof in either direction. At several
  rungs the candidate gates partly vanish identically, so these conditions are
  demonstrably dependent and the true rank of each system is what matters.
- These counts are at a generic point reached by random kernel choices; a
  special locus could behave differently. That is exactly the deleted-stratum
  hazard logged elsewhere in this campaign.
- The numbers refine my earlier estimate ("~40 conditions in 16 unknowns") to
  **38 conditions in 19 parameters** — the earlier version used the sub-case (2)
  index convention before it was derived from the supports.

## Where this leaves the hunt

1. **Sub-case (2)** is the target: 38 conditions in 19 parameters, an explicitly
   finite system well within reach of a real Gröbner engine. Numerical search
   over it plateaus at a residual of ~3% with the vertices genuinely nonzero
   (not a collapse), which points toward emptiness — but that is evidence, not
   a certificate.
2. **The pentagon** should be treated as effectively dead for witness-hunting
   purposes and finished off as an emptiness result.
3. **The 24 open cases above 125** (`FABLE_24_OPEN_CASES.md`) should be ranked by
   this same statistic before any of them is attacked. It is cheap to compute —
   supports come straight from the polygon — and it is the first principled way
   this campaign has had to choose a target rather than inherit one.

## Status

No counterexample. Pentagon and sub-case (2): **NO VERDICT**.
