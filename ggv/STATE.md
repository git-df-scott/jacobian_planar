# GGV B=16 evidence campaign -- state at handoff

Branch: `claude/ggv-conjecture-evidence-r9almu`, based on
`claude/opus-5-counterexample-plan-sep6yk`.  No existing file was edited; every
path under `ggv/` is new.  `STATUS.md`, `MANIFEST.md`, `ADJUDICATION.md` and all
existing pull requests are untouched.

This file records what ran and what did not.  It contains no mathematics.

## Gate -- required before any computation, re-run after every runner change

`ggv/logs/GATE.log`, ALL PASS (9 checks):
`wave5/w5_b16_abel.py` prints ALL PASS; `wave5/ms2/b16r_d5_{A,B}_p1000003.ms`
both re-solve to `[-1]`; and five controls on the runner itself -- a
zero-dimensional ideal must not classify EMPTY, a 0-byte artifact must not
classify EMPTY, a literal `[-1]:` must, an over-deadline run must be recorded
TIMEOUT with no surviving msolve process, and a killed run must still report a
peak RSS.

## Task status

| task | scope | state |
|---|---|---|
| G1 | ladder d=8..12, reduced charts, 3 primes, chart A then B | INPUTS COMPLETE; **ZERO RUNS RECORDED** -- `ggv/ladder.tsv` absent, stopped on request |
| G2 | chart-A mu-eliminants, d=3..8 | d=3,4 COMPLETE with all controls; d=5 recorded TIMEOUT (both engines); d=6,7,8 NOT RUN -- stopped on request |
| G3 | chart-B mu-eliminants, d=3..8 | COMPLETE, ALL PASS |
| G4 | descent-recursion table, d=3..10 | COMPLETE, ALL PASS |
| G5 | reproduction of GGV's printed d=3 family | COMPLETE, ALL PASS |

## G1 -- what exists and what does not

Inputs for all 10 (d, chart) pairs are generated, certified and committed:
`ggv/ms_ladder/` (30 files, 3 primes each), manifest `ggv/ladder_inputs.json`,
generation log `ggv/logs/G1_gen.log` (ALL PASS: every prime 1 mod 3, quasi-
homogeneity confirmed per d, header/characteristic/row-count verified against
the builder for every file written, no constant generator).

Runs: **`ggv/ladder.tsv` does not exist.**  No ladder cell completed under the
final runner, so no row was ever written and the file was never created.  Its
absence means "no cell recorded", not "no cell found a solution".  The one row
collected before the peak-RSS fix was discarded deliberately rather than kept
with a missing memory figure (see defect 6 below), and G1 was still queued
behind G2 when the campaign was stopped.  The cell
`d=8, chart A, p=1000003` was measured four times and produced no output
artifact every time -- 900 s under the final runner, and three separate 2700 s
attempts before that, at ~100% of one core throughout.  See
`ggv/logs/G1_prior_attempts.md` for the deadline history and why the sweep
deadline is 900 s.  The remaining cells are NOT RUN, not empty and not failed.

To continue: `./ggv/g_queue.sh` -- it resumes both G2 and G1, skipping every
cell already recorded, without repeating or double-writing anything.

## Deliberate deadlines, all recorded rather than silent

Every row `ggv/ladder.tsv` will carry once G1 runs has `timeout_s`,
`mem_policy`, `peak_rss_kb` and `rss_source` columns; every block of every
eliminant file already carries `status`, `wall_s` and `peak_rss_kb`.  The d >= 5 elimination deadline of 300 s is set
from measurement, not guessed: at d=5 chart A saturated, msolve produced no
eliminant in 900 s and Singular none in 540 s
(`ggv/logs/G2_d5_engine_probe.log`).  No input was truncated and no cell was
capped without the cap appearing in the artifact.

## Verdict classes used

`EMPTY` ( `[-1]:` ) | `CANDIDATE-UNVERIFIED` (artifact present, not `[-1]`) |
`TIMEOUT` | `STALLED-OOM` | `CRASH` | `NO-OUTPUT` | `RUN-ERROR`.
A 0-byte or missing output file is a failed run and never a verdict.

## Defects found and fixed during the campaign, each with a control

1. Timeout leaked the engine: only the direct child was killed, so an orphaned
   msolve overlapped the next job.  Fixed by process-group kill; GATE-4.
2. A 13 GiB `ulimit -v` turned survivable runs into SIGSEGV on a failed
   allocation.  Removed in favour of `oom_score_adj=1000` and the kernel OOM
   killer, per the campaign tooling contract.
3. An exception launching a cell silently dropped that cell and every later
   cell.  Now recorded `RUN-ERROR`; self-test T2.
4. `-P 1` fired on TIMEOUT/OOM, burning a second full deadline for no
   information.  Now fires only for `CANDIDATE-UNVERIFIED`; self-test T3/T4.
5. 0-byte artifacts were left on disk where they could be committed as results.
   Now deleted; self-test T5.
6. Peak RSS was `-1` for killed runs.  Now sampled from `/proc` VmHWM; GATE-4.
7. The msolve `-g 2` parser fed msolve's `#` header into Singular as if it were
   a generator; and `normalise()` accepted Singular error text as an eliminant.
   Both fixed and guarded.
8. The negative control could not fail -- dropping one generator from a heavily
   overdetermined ideal changes nothing.  Replaced with the ideal of the first
   generator alone, which is required to differ; the drop-one probe is retained
   as recorded data, not as a control.

`ggv/g_selftest.py` (stub engine, no msolve) covers 3,4,5 plus resume and a
negative control on itself: ALL PASS.  `./ggv/g_selfscan.sh` reports 0
compile-time-constant check conditions under `ggv/`.


## Two faults found while verifying the stop, both fixed

1. **A leftover engine survived the stop for 22 minutes.**  The stop killed the
   engines before the drivers, so a driver outlived its engine, launched the
   next one, and only then died -- leaving a Singular process on
   `chartA_d6_sat` running at 1 GiB.  This is the same class of fault as defect
   1 below, which was fixed *inside* the runner but not in the manual stop
   procedure.  `ggv/g_stop.sh` now kills drivers first, then engines, then
   VERIFIES nothing survived and exits non-zero if anything did.

2. **Three 0-byte engine outputs had been committed** --
   `chartA_d5_sat.msolve.gb`, `chartA_d5_unsat.msolve.gb`,
   `chartA_d6_sat.msolve.gb`.  Each was a timed-out elimination that wrote no
   bytes.  Under the campaign rule that a 0-byte output is a failed run and
   never a verdict, committing them is a hazard: a reader can mistake an empty
   file for an empty variety.  They are removed; `g23_eliminants.py` now deletes
   a 0-byte engine output at the point it is produced, exactly as the ladder
   driver already did; and `ggv/g_selfscan.sh` refuses any commit while a
   0-byte artifact exists anywhere under `ggv/`.  That guard is negative-
   controlled: planting a 0-byte file makes it exit 1, removing it exits 0.

   The corresponding `.ms` and `.sing` INPUTS are kept -- those are real inputs,
   not outcomes -- and each eliminant file already records the run as
   `status: TIMEOUT` with `generators: <none: run did not produce an artifact>`.

Note on d=6 chart A: the elimination was interrupted mid-run by the stop, so
`ggv/mu_eliminants/chartA_d6.txt` does not exist and d=6 is NOT RUN, not
timed out.

## Engine provenance and acceptance controls

`ggv/engine_build/` records how msolve and Singular were built and installed on
this machine, with full transcripts, since the repository has no `BUILD.md`.
`ggv/engine_controls/` holds the small inputs and exact outputs used to accept
the engines before any campaign run, including the msolve empty/zero-dimensional
pair and the Singular printing-format checks that the cross-engine comparison
depends on.
