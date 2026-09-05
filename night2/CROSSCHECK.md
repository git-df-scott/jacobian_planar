# night2 CROSSCHECK — execution record

Executor record only. No interpretation.

Run date (UTC): 2026-08-28. Repo root: `/home/user/jacobian_planar`, branch `claude/fable-6o0nqe`.

Two implementations compared:
- ours: `night2/sep.py` (never executed before this record)
- external: `night2/sol/separator_pipeline.py` plus its own checkers

---

## STEP 1 — external checkers, verbatim

Command (run from `night2/sol`):

```
python3 verify_deliverables.py
```

Complete stdout:

```
PASS V1 Python syntax
PASS V2 CSV shape, controls, rank-nullity, and cross-prime agreement
PASS V3 exact d=3 certificate checker
PASS V4 report/theory required conclusions
PASS DELIVERABLES all fast integrity checks completed
```

Exit status: 0. Result: PASS. (V3 is the line that invokes `certify_separator_d3.py`.)

---

## STEP 2 — external pipeline smoke reproduction, fresh seed 555

Commands (run from `night2/sol`), identical apart from `--prime`:

```
python3 separator_pipeline.py --d 3 --prime 999983  --batch 96 --patience 3 --max-samples 2000 --holdout 12 --seed 555 --csv /tmp/sol_d3.csv
python3 separator_pipeline.py --d 3 --prime 1000003 --batch 96 --patience 3 --max-samples 2000 --holdout 12 --seed 555 --csv /tmp/sol_d3_p2.csv
```

Both exited 0. Recorded values:

| prime | samples | rank | separators | shipped claim | verdict |
|---|---|---|---|---|---|
| 999983 | 480 | 174 | 57 | rank 174, sep 57 | MATCH |
| 1000003 | 480 | 174 | 57 | rank 174, sep 57 | MATCH |

Both runs printed `PASS S0`, `PASS S1`, `PASS S2`, `PASS I1`, `PASS I2`, `PASS I3`, `PASS GRID`.

Note on `samples`: this run reached saturation at 480 samples; the shipped CSV row records 384. The invocation here uses a different seed, batch, patience and holdout than the shipped default, so the sample count at which the loop stops is not expected to reproduce. Rank and separator count are the compared quantities and both reproduced.

---

## STEP 3 — our pipeline, first ever execution

Commands (run from repo root), defaults otherwise (`--seed 44`, `--batches 8`):

```
python3 night2/sep.py --d 3 --prime 999983  --out night2/results
python3 night2/sep.py --d 3 --prime 1000003 --out night2/results
python3 night2/sep.py --d 4 --prime 999983  --out night2/results
python3 night2/sep.py --d 4 --prime 1000003 --out night2/results
python3 night2/sep.py --d 5 --prime 999983  --out night2/results
python3 night2/sep.py --d 5 --prime 1000003 --out night2/results
```

Outcome: all six runs exited 0. No crash, no traceback. No control failure: every run
reported `I1_rank_saturated = true`, `I2_heldout_violations = 0`,
`I3_trivial_separators = 0`, and verdict `PASS`. S1 is checked inline per sample and
did not abort any run.

**Mechanical fixes applied to `night2/sep.py`: NONE.** The file was executed exactly as
committed; no edits of any kind were made to it.

Stdout, verbatim:

```
d=3 p=999983: 57 deg<=2 separators, I2 violations=0, I3 trivial=0 -> PASS
d=3 p=1000003: 57 deg<=2 separators, I2 violations=0, I3 trivial=0 -> PASS
d=4 p=999983: 101 deg<=2 separators, I2 violations=0, I3 trivial=0 -> PASS
d=4 p=1000003: 101 deg<=2 separators, I2 violations=0, I3 trivial=0 -> PASS
d=5 p=999983: 358 deg<=2 separators, I2 violations=0, I3 trivial=0 -> PASS
d=5 p=1000003: 358 deg<=2 separators, I2 violations=0, I3 trivial=0 -> PASS
```

Per-run batch progression (samples, rank) read from `night2/results/sep_d<d>_p<p>.json`.
Our rank is reported as the saturated rank; `separators = n_feat - rank`.

| d | prime | n_feat | (samples, rank) per batch | saturated rank | separators |
|---|---|---|---|---|---|
| 3 | 999983 | 231 | (198,148) (396,174) (594,174) | 174 | 57 |
| 3 | 1000003 | 231 | (198,148) (396,174) (594,174) | 174 | 57 |
| 4 | 999983 | 496 | (200,187) (400,322) (600,395) (800,395) | 395 | 101 |
| 4 | 1000003 | 496 | (200,187) (400,322) (600,395) (800,395) | 395 | 101 |
| 5 | 999983 | 946 | (198,192) (396,346) (594,471) (792,527) (990,560) (1188,588) (1386,588) | 588 | 358 |
| 5 | 1000003 | 946 | (198,192) (396,346) (594,471) (792,527) (990,560) (1188,588) (1386,588) | 588 | 358 |

Multidegree components enumerated by our sampler: d=3 `[], [2], [3]`;
d=4 `[], [2], [3], [4], [2,2]`; d=5 `[], [2], [3], [4], [5], [2,2]`.

Artifacts written: `night2/results/sep_d{3,4,5}_p{999983,1000003}.json` and the
corresponding `sepbasis_*.npy` separator bases.

---

## STEP 4 — comparison table

Theirs from `night2/sol/separator_counts.csv` (d3 rank 174 / sep 57, d4 rank 395 /
sep 101, d5 rank 588 / sep 358; the CSV lists identical values at both primes).

Recorded fact, stated without interpretation: the saturated rank is intrinsic — it is the
Hilbert function of the automorphism locus mod p — so two dominant samplers must agree
on it exactly.

| d | prime | our rank | their rank | rank verdict | our separators | their separators | separator verdict | our count lower/higher |
|---|---|---|---|---|---|---|---|---|
| 3 | 999983 | 174 | 174 | AGREE | 57 | 57 | AGREE | equal |
| 3 | 1000003 | 174 | 174 | AGREE | 57 | 57 | AGREE | equal |
| 4 | 999983 | 395 | 395 | AGREE | 101 | 101 | AGREE | equal |
| 4 | 1000003 | 395 | 395 | AGREE | 101 | 101 | AGREE | equal |
| 5 | 999983 | 588 | 588 | AGREE | 358 | 358 | AGREE | equal |
| 5 | 1000003 | 588 | 588 | AGREE | 358 | 358 | AGREE | equal |

AGREE in all 6 cells, for both rank and separator count. No cell differs, so there is no
cell where our count is lower or higher.

Cross-prime: our own runs return identical rank and separator count at 999983 and
1000003 for every d tested (3, 4, 5).
