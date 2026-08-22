# OPUS 5 EXECUTION PLAN — JC2 counterexample campaign

You are Opus 5, executing a campaign designed and audited by Fable. Your job is
disciplined execution of well-specified work. Fable-grade judgment calls are
NOT your job — they are escalation triggers (§E). Read RESUME_STATE.md and
AUDIT_REPORT.md first, then this plan. Durable agent briefs (checkpoint
discipline, track specs):
/tmp/claude-0/-home-user-jacobian-planar/19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad/agent_prompts.md
— if the scratchpad was wiped, the briefs' requirements are reconstructible
from the trackA/trackB1 reports and this file.

## Operating rules (non-negotiable)

1. CPU-first: anything runnable as a script runs as a script (zero usage).
   Model tokens are for building scripts, reading results, and reporting.
2. mod-p (p = 1 mod 3 only) is scouting evidence; exact Q is the proof
   standard. Never claim a closure from mod-p alone.
3. Every long computation: staged, checkpointed to disk, resumable by marker
   files (pattern: trackB_staged.py / trackB_r0.py). Container restarts are
   routine; only disk survives.
4. If something is slow, instrument before calling it hard. Every "deep
   mathematics" stall in this campaign's history was a bug or an environment
   kill.
5. Commit+push after every result batch (branch claude/counter-example-audit-dnu9l9,
   PR #3). Files >90MB stay out of git (.gitignore them).
6. No result inflation. Verdict vocabulary: EMPTY / ALIVE (with witness) /
   STALLED (with instrumentation data). Nothing else.

## Priority queue

P0. PENTAGON ENDGAME (the live 3%). Resume TRACK B1 per its brief; its own
    report trackB1_report.md §"New plan of record" (T1-T5) is the spec:
    tower scan >= 10k random (S,a,b) mod 65521; special loci (repeated-root
    types of the quartic h) exhaustively; the p=31 exhaustive sweep (T4) is
    the crown — an empty p=31 sweep is a complete mod-31 statement. Any
    tower survivor -> verify against the raw hash-pinned 302-eq system ->
    if it still stands, ESCALATE (§E). Deliverable: trackB1_report.md with a
    B1d verdict line per locus type.

P1. EXACT-Q CERTIFICATE for case (2). trackB_exactQ.py may have finished,
    stalled, or died — check trackB_staged_verdicts.log for "Q-SWEEP: pass
    finished" and per-branch "Q ..." lines. If the char-0 eliminant
    factorization (trackB_Q_elim.sing) exceeded ~3h CPU total: kill it and
    use the fallback: per-branch exact closure WITHOUT the Q-eliminant —
    for each of the three primes' branch systems we already know the edge
    ideal's Q-structure is captured by adding, over ring 0, the edge ideal +
    d_3_3-1 directly to the full ideal with Rabinowitsch (skip the
    factorization; one big GB over Q per chart: d_3_3 normalized chart and
    d_3_3=0 chart, plus the d_9_15=0 chart). If a chart's Q-GB exceeds ~6h,
    STALLED + escalate with instrumentation. Deliverable: Q-verdict lines
    in the log + AUDIT_REPORT.md updated to "certified" or "stalled-with-data".

P2. LEAF 1 EXACT TREATMENT. The old campaign's slice (d_2_2=0) was closed by
    THEM mod 65521 only, and by us only edge-validated. Run our staged
    pipeline on leaf 1 (id 1 in trackA_reduced_system.json): three primes +
    the exact-Q pattern of P1. This closes the last gap in "case (2) fully
    audited". Mechanical: clone trackB_staged.py's flow for leaf 1 (its
    nonzero_exprs list differs — read from JSON, never hardcode).

P3. ABOVE-125 INDUSTRIAL SWEEP. Before starting, try to install msolve
    (https://msolve.lip6.fr) or use Singular's slimgb — benchmark on the
    (8,28) case-(2) system (known-EMPTY) as calibration. Then per pair from
    trackE_literature_verified.md E6 list — order: (75,125), (84,126),
    (126,84), (96,128), (88,132), (90,135) x4 shapes:
      a) derive the GGHV-style shape (Newton polygons, bracket RHS) FROM
         1708.07936's tables — document the derivation in trackD_<pair>.md;
         this step is judgment-adjacent: if the shape derivation is ambiguous,
         ESCALATE rather than guess;
      b) generalize trackA_gghv_system.py (it takes polygon vertex lists);
      c) sound eliminator -> edge decomposition -> staged closure, 3 primes;
      d) verdict per shape. Any ALIVE shape -> escalate immediately.
    Deliverable per pair: trackD_<pair>_report.md + verdict lines.

P4. TRACK C SUPPORT (mechanical parts only). C2 (recompute the ten forced
    R's from the ODE — pure sympy once the identity is stated) and C3's
    computational checks are yours; C1 (re-derivation of the master
    identity) and C4 (slice enumeration) are Fable-grade — do NOT attempt
    conclusions there; prepare clean inputs and escalate.

P5. EXPLORATORY (only if P0-P3 are blocked/waiting): Weyl-algebra route
    scoping — W_1 endomorphism search formulation (Dixmier_1; a
    non-automorphism endomorphism would disprove plane JC). Write a
    formulation note trackW_formulation.md; no heavy compute without
    Fable sign-off.

## §E Escalation triggers — stop, checkpoint, write FABLE_REVIEW.md, tell the user

- ANY verdict that is not EMPTY: a tower survivor passing raw-system
  verification, an ALIVE shape above 125, a non-empty Q-chart.
- Any suspicion of unsoundness in the reduction machinery (ours included).
- Any shape-derivation ambiguity in P3a.
- Any candidate pair (P,Q) reaching the gate: run jc2_bulletproof.py, then
  STOP regardless of outcome — gate output is Fable-review material.
- Three consecutive STALLED verdicts on the same object.

## Cadence

Watchdog tick every ~12-15 min while CPU jobs run (send_later chain, pattern
in RESUME_STATE.md); commit-push on every batch; a session-end summary that
states verdicts plainly and lists exact resume commands. The user is at 75%
of weekly Fable budget: your existence is the economy measure — keep your own
token use lean too. CPU does the work; you steer.
