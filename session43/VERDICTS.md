# Session 43 verdict ledger (2026-08-22)

Standing rule applied throughout: a 0-byte .out with a nonzero/137 exit is
OOM or TIMEOUT — NEVER "EMPTY".

## A. Torus-sliced resisters — PROVISIONAL EMPTY, control not yet run

Two of the six wave6 resisters are decided across their full chart
decomposition at p=65521.  Each resisted 1800 s budgets unsliced; sliced,
every piece returned instantly.

| system | piece | msolve | wall |
|---|---|---|---|
| w6_289012_1 | nonzero chart (c_1,c_2,c_3,c_5,x = 1) | [-1] | <1 s |
| w6_289012_1 | c_2 = 0 stratum | trivially inconsistent (nonzero constant generator) | — |
| w6_289012_1 | c_3 = 0 stratum | [-1] | <1 s |
| w6_289012_1 | c_5 = 0 stratum | [-1] | <1 s |
| w6_582584_1 | nonzero chart (c_1,c_2,c_3,c_4,x = 1) | [-1] | <1 s |
| w6_582584_1 | c_2 = 0 stratum | trivially inconsistent | — |
| w6_582584_1 | c_3 = 0 stratum | [-1] | <1 s |
| w6_582584_1 | c_4 = 0 stratum | [-1] | <1 s |
| w6_289012_0 | nonzero chart | [-1] | <1 s |

Gauge soundness CHECKED: the 3 genuine weight vectors restricted to the
gauged variables have determinant -242 (w6_289012_1) and -338 (w6_582584_1),
both nonzero mod 65521, so setting those variables to 1 is a legitimate
chart of the torus action and the chart+strata decomposition is exhaustive.

**NOT YET BANKED.**  Required before these are quoted as verdicts:
1. a planted-solution positive control through the identical slice pipeline
   (campaign rule: a pipeline that decides everything instantly must be
   shown capable of returning NONEMPTY);
2. a second prime;
3. propagation through the hash-dedup map (each of these decides several
   records across registers).

## B. Undecided, with cause

| item | outcome | cause |
|---|---|---|
| d=8 corrected frontier cell (m16_d8_p1000003) | NO VERDICT | OOM at 663 s under MY OWN concurrency (3 heavy jobs in one cgroup).  Never had a fair solo trial. |
| MISS-3 (b16seed2_d12_N_p1000003) | NO VERDICT | OOM at 2809 s / 13.9 GB while effectively solo.  GENUINE: exceeds the 14 GB shared cgroup. |
| d12slice / d12sliceZ (L-S family gate) | NO VERDICT | OOM at 3.6 GB / ~5 GB, both under contention I created.  NOT a fair trial; rerun solo before concluding they need a bigger box. |

## C. Environment correction (supersedes earlier interim claims)

There is NO ~3.5 GB per-process cap.  One shared ~14 GB memcg; msolve
reached 13.9 GB.  Earlier "3.5 GB cap" statements in this session's interim
notes are WRONG and are retracted here.  The campaign's one-heavy-at-a-time
rule was violated three times tonight by me, reproducing the exact failure
class already logged twice in CATCHES.md class (ix).

Consequences:
- MISS-3's "predicted FAST (non-resonant seed)" forecast is REFUTED with a
  hard number: >14 GB, >45 min on msolve's default Gröbner+RUR path.
- Untried knob, in the original brief and never reached: `msolve -g 2`
  (Gröbner-only, skips the RUR stage that most plausibly drove the blow-up),
  with -t 1.  This is where the next attempt should start.
- The three archived 0-byte N-chart .out files in wave5/ms2/ are almost
  certainly this same OOM, not silent successes.  Re-check before any of
  them is quoted.
