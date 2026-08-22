# MISS-3 results — 2026-08-22

## Solver availability
- `apt-get install -y msolve` -> **msolve 0.6.5** installed (0.6.5-1build2). OK.
- `apt-get install -y singular` -> **Singular** installed. OK.

## Target system
- File: `state/wave5/ms2/b16seed2_d12_N_p1000003.ms` (45,358 bytes)
- 37 vars: a2..a23, b2..b11, mu0, mu2, mu3, t, u; char p = 1000003.
- Prior `.out` files in ms2/ for the N-variant systems (b16r12seed_N_*) are 0 bytes = prior runs never finished/killed. All Z-variant runs gave `[-1]` (EMPTY).

## Context (from state/STATE_FULL.md, state/BIFURCATION.md)
- MISS-3 = d=12 chart N, seed a24=1/20 (the NON-resonant rational root of row0). Together with the already-EMPTY seed -1/12 twin it closes the whole d=12 chart N. Predicted fast (no in-range resonance at 1/20).
- The d12slice probe (mu0=0, a24=-1/12 slice, 34 vars, mod 65521) is the bifurcation-program gate: dim>=1 = degenerate family EXISTS at the resonant root = base point for the Lyapunov-Schmidt mu0-direction CE attack. Both prior runs OOM'd at ~2.4GB (halt 14) — never decided.

## Runs (in progress)
1. `msolve -t 4 -f state/wave5/ms2/b16seed2_d12_N_p1000003.ms -o miss3_b16seed2_d12_N_p1000003.out` — RUNNING
2. d12 slice probe: found pre-generated `wave5/bifurcation/d12slice.sing` and `d12sliceZ.sing` inside `/home/user/jacobian_planar/state_transfer.tgz` (extracted to `scratchpad/repo/`). Both prior runs died with `Singular error: no more memory` at ~2.4GB (halt 14) — NOT a verdict. This box has ~14GB free; rerunning:
   `Singular -q repo/wave5/bifurcation/d12slice.sing` — RUNNING

## Verdicts
(pending)
