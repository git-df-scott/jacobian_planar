# RESUME STATE — hard stop at monthly spend limit, 2026-08-13 ~05:2x UTC

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
