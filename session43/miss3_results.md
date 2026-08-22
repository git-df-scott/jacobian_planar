# MISS-3 results — 2026-08-22 (agent run 01:15Z-01:28Z, hard 13-min budget)

## Solver availability
- `apt-get update && apt-get install -y msolve` -> **msolve 0.6.5 (0.6.5-1build2) INSTALLED, works**.
- `apt-get install -y singular` -> **Singular INSTALLED, works**.
- Environment constraint discovered: the bash cgroup OOM-kills any single job at ~3.5-3.6GB anon-rss (verified via dmesg: `CONSTRAINT_MEMCG ... claude-code-bash ... Killed process (Singular) total-vm:3611084kB`). Total box RAM 15GB is irrelevant; the per-cgroup cap is the binding limit.

## Target system (MISS-3)
- File: `state/wave5/ms2/b16seed2_d12_N_p1000003.ms` (45,358 bytes)
- 37 vars (a2..a23, b2..b11, mu0, mu2, mu3, t, u), p=1000003, 46 generators.
- Verified: tail generators `mu0*t-1, mu2*u-1` — genuine Rabinowitsch-saturated chart N (mu0!=0, mu2!=0). Seed 1/20 (non-resonant) per STATE_FULL/AUDIT_EOD: this run + the -1/12 twin = whole d=12 chart N.
- All sibling Z-chart .out files in ms2/ read `[-1]` (EMPTY); all prior N-chart .out files are 0 bytes (never finished).

## Commands run
1. `msolve -t 4 -f state/wave5/ms2/b16seed2_d12_N_p1000003.ms -o miss3_b16seed2_d12_N_p1000003.out`
   - **VERDICT: UNDECIDED (still running at budget exhaustion).** Ran 9+ minutes, RSS steady-growing 2.1->2.6GB, 4 threads, no output produced. The "predicted FAST" call did NOT hold within a 9-minute window at p=1000003 — the non-resonant seed is not trivially fast for msolve 0.6.5 defaults. No crash: computation was healthy, just long. Process left running at agent exit (pid 10401); output file `miss3_b16seed2_d12_N_p1000003.out` will contain `[-1]` (EMPTY) or a parametrization (NONEMPTY) if it completes.
   - Interpretation guard: `[-1]` = EMPTY; anything else = candidate witness needing verification (per w6_msolve_bridge.py convention).
2. Singular `std()` cross-check on the same ideal (`miss3_sing.sing`, dim/reduce(1,G)): started, then **deliberately killed by me at ~5 min** to free the memory cgroup for the primary msolve run. Not a verdict.

## d12 slice probe (bifurcation gate, from opus_kit/d12slice_probe.py)
Found pre-generated inputs inside `/home/user/jacobian_planar/state_transfer.tgz` -> `wave5/bifurcation/d12slice.sing` (full slice: mu0=0, a24=-1/12, 34 vars mod 65521) and `d12sliceZ.sing` (additional mu2=0, 33 vars). Prior archived runs BOTH died `Singular error: no more memory` at ~2.4GB — recorded as FAILURE, not verdict.
3. `Singular -q repo/wave5/bifurcation/d12slice.sing` (full slice):
   - **VERDICT: UNDECIDED (OOM again).** OOM-killed at 3.6GB anon-rss, wall 312s (exit 137). Third memory death for this computation. It needs a machine allowing >4GB (probe header says ~10GB free); this sandbox's ~3.5GB cgroup cap cannot decide it.
4. `Singular -q repo/wave5/bifurcation/d12sliceZ.sing` (mu2=0 slice):
   - **VERDICT: UNDECIDED (in flight at budget exhaustion, likely OOM-bound).** At agent exit: 8+ min wall, RSS 4.4GB and climbing (already past the anon-rss level that killed run 3; will almost certainly be OOM-killed). No dim output produced. FAILURE-trajectory, not a verdict.

## Bottom line
- **b16seed2_d12_N_p1000003 (MISS-3): UNDECIDED — no witness found, no emptiness certificate yet.** msolve works here and made healthy progress; the computation simply needs a longer slot (give it 30-60 min, single job, nothing else in the cgroup). No evidence of NONEMPTY; the uniform `[-1]` record of every completed sibling makes EMPTY the expected outcome, but that is prior, not verdict.
- **d12 slice (family-existence gate): UNDECIDED — memory-bound, not solver-bound.** Three OOM deaths at 2.4-3.6GB. Actionable fix: run on a box with a real >=8GB per-process allowance, or restructure (facstd / eliminate block ordering / degree cap) before std.
- Both Singular and msolve are now installed in this container; the queue runner (STATE_FULL item E.1) can execute here if given per-job memory headroom and longer wall slots.

## Post-budget observation (01:28Z)
- msolve (MISS-3) at 10:00 elapsed, RSS 3.8GB — now itself inside the cgroup kill zone (~3.5-3.6GB anon-rss); if it dies with exit 137 and an empty .out, that is an OOM kill, not a verdict.
- d12sliceZ Singular at 9:10, RSS 4.8GB, still alive — the cap may be somewhat above the 3.6GB kill observed earlier, but the trajectory is unchanged.

## Reproduction
- Inputs: `scratchpad/state/wave5/ms2/b16seed2_d12_N_p1000003.ms`, `scratchpad/repo/wave5/bifurcation/d12slice{,Z}.sing`
- Partial outputs: `scratchpad/miss3_b16seed2_d12_N_p1000003.out` (0 bytes at exit), `scratchpad/d12slice_full.out`, `scratchpad/d12sliceZ_full.out`, `scratchpad/miss3_sing.sing`
