# Session 43 — orientation, torus diagnostic, live runs (2026-08-22)

Read against the LIVE branch claude/opus-5-counterexample-plan-sep6yk (90
commits past the transfer bundle), not the session 39-42 handoff docs.

## Findings this session
1. Bundle restore (MISS-7) was already complete; live branch is authoritative.
2. msolve 0.6.5 + Singular install cleanly via apt in fresh containers —
   the solver bottleneck was container-specific, not environmental.
3. Grading diagnostic (torus_scan.py) run on all 29 parseable .ms systems:
   - ALL SIX wave6 TIMEOUT resisters have grading-torus rank 5
     (3 genuine gradings + 2 spurious free vars c_1, x that appear in no
     polynomial). Resistance-is-geometry confirmed on the full resister set.
   - Perfect Z/N split in wave5/ms2: every *_Z_* system rank 1 with weight
     (mu0 -> -1, t -> +1); every *_N_* counterpart rank 0.
   - 23 sliced systems written (torus_sliced/): 41->36 and 23->18 vars.
   - Caveat: slicing v=1 covers the v!=0 chart; v=0 strata need recursion.
4. Literature (lit_results.md): arXiv:2608.00222 (Gao) is EXPLICITLY the
   tangent-sweep mechanism generalized (Path E abort condition fired — E1
   done by reading). Five new explicit maps extracted for the Path A
   descent census (re-verify formulas symbolically before use). No plane
   construction claimed; no geometric-degree-2 member exists.
5. Launched: corrected d=8 frontier cell (P1), one torus-sliced resister,
   d12 bifurcation slice probe with adequate memory, d12-N (printed-system,
   diagnostic only). Verdicts to be committed when they land.

## Standing conclusions after the mechanism audit
- Every known higher-dimensional counterexample mechanism is sweep-based
  (Gao explicit + Alpoge/Gallagher/Speyer), and the sweep is proved dead in
  the plane (live-branch theorem). Headline claim upgrades to "every KNOWN
  mechanism", correctly hedged.
- Combined with the deck-group theorem: a plane CE must be a non-Galois
  degree->=3 cover via a mechanism unknown in dimension 3.

## Next actions (ranked)
1. Grading diagnostic on the reduced pentagon system (241eq/123unk), slice,
   first fair msolve run on a fresh container.
2. Act on the d12 slice verdict: dim>=1 -> mu0-walk (Hensel); else move the
   Lyapunov-Schmidt base to d=27.
3. Gao's five maps through the Path A quotient descent: measure exponent k.
4. Run remaining torus-sliced resisters (six verdicts decide ~20 records
   via the hash-dedup map).
5. Cascade vanishing-pivot case: design on paper before any 4th attempt.
