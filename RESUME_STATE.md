# RESUME STATE

## OPUS 5 SESSION, 2026-08-13 ~22:0x-23:xx UTC (priority-queue execution)

**Environment gotcha, read this first:** the container came up with **no
Singular**. `apt-get install -y singular` (4.3.2) restores it; `apt-get install
-y msolve` adds msolve. Every campaign script assumes Singular on PATH, so a
fresh container silently has no engine until you do this. (After a *restart*
rather than a fresh container, both survive — the filesystem persists.)

**Container lifetime is the binding constraint on exact-Q, measured.** This
session lost every process to a restart after roughly 2.5 hours of wall time,
with the root filesystem intact. Consequence: any single monolithic Groebner
run budgeted longer than ~2h will never land, no matter how generous its
timeout — the exact-Q fallback charts carry a 6h timeout they can never reach.
Design accordingly: prefer marker-resumable per-branch pipelines (the staged
route) over one big GB, because a restart costs a stage there and the whole
run here.

Queue status at checkpoint:

| item | state |
|---|---|
| P0 pentagon endgame | T1 PASS (tower_check restored — it had been overwritten by tower_lift's append). T2/T4 **STALLED**, measured: one sample's level 16 does not finish in 1400s at 1.8GB with 9 levels still below it. T5 engines both lost (slimgb 2x slower than std; msolve dies in hash-table growth). Verdicts in trackB1_report.md §B1d; escalated in FABLE_REVIEW.md item 2. **No verdict on case (1).** |
| P1 exact-Q leaf 2 | RUNNING. `trackB_exactQ.py`; the char-0 edge eliminant factorization is the long pole (QELIM_TIMEOUT env, default 10800s). Resume: `python3 trackB_exactQ.py` (markers resume). |
| P2 leaf 1 | RUNNING. p=65521: eliminant ELIMDEG 43, 7 factors, rk0-rk5 + r0a sub-branches all EMPTY so far. `trackB_leaf1_chain.sh` queues p=65539, p=65599, then leaf-1 exact-Q, unattended. Resume: `JCP=<p> python3 trackB_leaf1_sweep.py`, then `JCLEAF=1 python3 trackB_exactQ.py`. |
| P3 above-125 | **BLOCKED, escalated** (FABLE_REVIEW.md item 1): the above-125 Newton polygons are published nowhere. 1708.07936 §6 gives chain data only; GGHV 2204.14178 §4 gives polygons only for (9,27), (9,24), (8,28), (7,21), derived case-by-case by hand with no general recipe. P3b-P3d are ready and pair-agnostic the moment a polygon pair is ruled. |
| P4 Track C | C2 **COMPLETE** (ten forced R's, k=3..12; D = 5k-2 derived, handoff's D = 3k+4 wrong from k=4 on and it manufactures a spurious death at k=4). C4 enumeration run for INPUT ONLY (Fable-grade). C3 **not started — `trackC_c3_ladder.py` was never written**; trackC_phase4.py's `c3` subcommand imports it and will fail until it exists. |

Tooling added this session: `JCLEAF` selects the leaf in trackB_staged (edge
equation indices now derived, not hardcoded); trackB_exactQ namespaces markers
by leaf; `JCENGINE=std|slimgb` switches the tower's per-level GB engine;
trackB1_msolve_export.py exports any structured system to msolve format with
Rabinowitsch saturation.

PR for this session's work: https://github.com/git-df-scott/jacobian_planar/pull/4

---

# (earlier) RESUME STATE — updated 2026-08-13 ~05:5x UTC (main loop continuing on CPU)

## CAMPAIGN-REDEFINING FINDINGS (Track A, complete — see trackA_report.md)

1. The lost session's ENTIRE r0-r6 hunt lived in the d_2_2 = 0 slice (leaf 1).
   The unsound R1 dropped the sibling at the FIRST fork. Leaf 2 (d_3_5 := 0,
   d_2_2 free; 44 eqs / 22 vars) is never-explored generic ground, and
   Sol(case 2) = Sol(leaf 2), so closing leaf 2 closes case (2).
2. Prop 4.3 has a SECOND case the handoff never saw: pentagon polygons,
   186 unknowns / 302 equations (trackA_system_case1.json). Attack route:
   top-edge leading forms force lP = a*S^2, lQ = b*S^3 for one slope-1 form S
   (5 coeffs) — parametrize and reduce. Case (1) must die too before any
   (8,28) closure claim.

## Compute in flight (survives nothing — restart from these commands if lost)

- Leaf 2 mod 65521:  python3 trackB_leaf_runner.py trackA_reduced_system.json 2 65521
- Leaf 1 control:    python3 trackB_leaf_runner.py trackA_reduced_system.json 1 65521
  (leaf 1 must reproduce handoff-compatible numbers: their vdim 1144 / deg-43
   eliminant story lived in this slice, mod the same prime)
- Outputs land in trackB_leaf{1,2}_p65521.out; Singular script files .sing.

# Original hard-stop record (2026-08-13 ~05:2x UTC)

The account's monthly spend limit terminated the running agents (Tracks A and C).
Per the N2 hard-stop discipline: this is an expected pause point, not a failure.
Everything below is exact resume instructions.

## Status at stop

| Track | Status | Deliverables on disk |
|---|---|---|
| E (literature) | **COMPLETE** — all premises verified, none changed | trackE_literature_verified.md (committed) |
| F (gate + regression) | **COMPLETE** — gate live, 6/6 rejections; regression zero divergences; h0 = −13·n3 verified | jc2_bulletproof.py, jc2_gate_validation.md, trackF_regression_report.md (committed) |
| A (system + eliminator) | **IN PROGRESS at kill** — partial checkpoints on disk (trackA_gghv_system.py, trackA_eliminator.py, trackA_elim_case1.log + whatever this commit adds) | resume, do not restart |
| C (master identity + Phase 4) | **KILLED EARLY** — little/no disk output expected | restart from brief |
| B (branch hunt) | NOT STARTED — blocked by A | — |
| D (above-125 recon) | NOT STARTED | — |

## To resume (any future session)

1. Read this file, then /tmp/claude-0/-home-user-jacobian-planar/19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad/agent_prompts.md
   (durable agent briefs; if the scratchpad was wiped, the briefs' content requirements
   are reconstructible from NIGHT_PLAN.md + trackE_literature_verified.md).
2. Relaunch Track A per its brief — it MUST resume from its partial deliverables
   (checkpoint discipline is in the brief header). Key tripwire already relayed:
   the open shape's reduced bracket is [P,Q] = x^2 (Track E, verified).
3. When A completes: launch Track B (brief section TRACK B) and Track C (TRACK C).
4. Track D only when CPU is idle.
5. Morning-report synthesis per NIGHT_PLAN.md §8 — four defined outcomes, no inflation.

## Key certified facts available to resumed work

- (72,108)/(8,28) is the sole open pair below 125 (GGHV, verbatim, verified).
- Gate: `from jc2_bulletproof import bulletproof_gate` — any candidate must pass.
- Sessions 1-8/10 all reproduce; Sessions 9/11-18 prose-only, pending Track C.
- gcd ≥ 36 filter RETRACTED — banned.
- mod-p (p ≡ 1 mod 3) = evidence only; exact Q = proof standard.

## Triggers

- One auto-revival trigger armed ~6h after the stop; it fires the resume protocol
  above. If the spend limit is still in force it will simply fail and the campaign
  waits for the next manual "go".

PR: https://github.com/git-df-scott/jacobian_planar/pull/3

## Branch-hunt scoreboard at spend-limit stop #2 (2026-08-13 ~14:45 UTC)

CASE (2), leaf 2 (d_2_2 free — never explored before tonight), mod 65521:
  r1 EMPTY | r2 EMPTY | r3 EMPTY | r4 EMPTY | r5 EMPTY | r6 EMPTY   (all DEAD)
  r0b: stage 1 DONE (d_3_3=0 edge fiber: dim 0, VDIM 338, trackB_st1_r0b.json);
       stage 2b CRASHED inside the Singular call (likely 2400s timeout or kill;
       trackB_st2_r0b.sing is on disk — inspect trackB_st2_r0b.sing.out, rerun:
       python3 trackB_staged.py r0b   — markers skip completed stage 1).
       If heavy: sub-branch the 338-point fiber via its lex GB univariate factor.
  r0a: NOT STARTED — run: python3 trackB_staged.py r0a
       (d_9_15=0 fiber, expect vdim ~280 per handoff; same sub-branch plan.)
NEXT after r0a/r0b: repeat all verdicts at primes 65539, 65599 (edit P in
trackB_staged.py or parametrize), then exact over Q; then leaf 1 same treatment
(old campaign's slice, unverified by us beyond edge numbers); then case (1).

Track B1 (pentagons): agent died on spend limit AFTER progress — see
trackB1_report.md (checkpointed; includes full-system mod-p artifacts).
Track C: died early again; trackC_report.md has its state.

NO scheduled triggers remain armed (all previous ticks consumed). On resume,
re-arm the 45-min tick chain per agent_prompts.md header.

## PAUSE POINT (user-ordered), 2026-08-13 21:25 UTC

VERDICT SCOREBOARD:
- Case (2) mod 65521: FULLY CLOSED — r1-r6, r0a, r0b all EMPTY.
- Case (2) mod 65539: rk0-rk4 EMPTY, r0a EMPTY (all terminals); r0b was at its
  final vdim-6 stage2b when paused. p65599 sweep NOT started.
  Resume: JCP=65539 python3 trackB_prime_sweep.py && JCP=65599 python3 trackB_prime_sweep.py
  (markers auto-skip everything finished)
- Exact-Q: eliminant factorization over Q was mid-run (trackB_Q_elim.sing).
  Resume: python3 trackB_exactQ.py
- Case (1) pentagons: NO VERDICT YET — tower machinery built+validated, kernels
  explained by structure theorem, ~120 obstructions on ~55 params; plan T1-T5 in
  trackB1_report.md (agent was mid-T1/T2, actively checkpointing at 21:21).
  Resume: relaunch TRACK B1 agent per agent_prompts.md (reads its own report).
- Track C: checkpoint stale since 13:56 — relaunch per agent_prompts.md; C1
  (master identity) + C4 (slice enumeration) are the priorities.
- Track D: untouched.
No triggers armed (21:41 tick deleted at pause). All processes die with the
container; every computation resumes from markers.
