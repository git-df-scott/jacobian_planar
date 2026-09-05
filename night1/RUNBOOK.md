# night1 RUNBOOK — deformation depth map (JC2)

Engine: `night1/engine.py` (Fable-authored, DO NOT modify its mathematics).
Method + guardrails documented in the engine docstring. All results are
MODULAR (F_p) and are reported as such. No cell is ever to be called a
"counterexample" or "candidate" — deep cells are recorded, interpretation
happens in the morning session only.

## Night-shift procedure (executor)
1. `python3 night1/engine.py controls` — must print CONTROLS: PASS.
   If FAIL: STOP. Write the failure into night1/OVERNIGHT_LOG.md, commit,
   push, end. Do not attempt to fix the engine.
2. Run specs in order: spec_n1, spec_n2, spec_n3 via
   `python3 night1/engine.py grid --spec night1/spec_<X>.json`.
   The engine self-aborts if any calibrated cell dies (engine-bug trap).
3. After EACH spec completes: `git add night1 && git commit && git push`.
   Commit messages: "night1: results for <spec>". No model names anywhere.
4. Append to night1/OVERNIGHT_LOG.md after each spec: rows written, wall
   time, the 10 deepest NON-calibrated cells (F, g, d, p, depth, status,
   indep_check), and whether the two primes agree on those cells.
   No interpretation, no adjectives, no conclusions.
5. If a run crashes: log the traceback in OVERNIGHT_LOG.md, commit, skip to
   the next spec. Never edit engine.py; driver-level workarounds only.
6. If total wall time approaches the limit, stop starting new specs, commit
   everything, write "STOPPED EARLY AT <point>" in the log.

## Reading depth (for the morning, not the night)
- calibrated=1 rows are controls (provably-polynomial flows); their depth
  is meaningless as data and must survive by construction.
- Depth of live probes is read RELATIVE to cap: interesting = depth high
  and growing sub-linearly or not at all when d increases (a cap-stable
  survivor), agreeing at both primes, indep_check=PASS.
- "survived" at kmax is NOT a finding; it is a prompt to re-run that cell
  with a larger kmax in the morning.
