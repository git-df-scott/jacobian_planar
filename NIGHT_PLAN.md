# NIGHT PLAN — Counterexample Campaign (JC2)

**Date:** 2026-08-12 evening → 2026-08-13 morning (user local, UTC−06:00)
**Repo branch:** `claude/counter-example-audit-dnu9l9`
**Start signal:** user "go", or the armed 10:20 p.m. trigger (04:20 UTC), whichever first.
**End state:** morning report at ~7:00 a.m. local (13:00 UTC) with one of the
defined outcomes (§7), full audit trail committed.

---

## 0. Objective and honest framing

Target: a counterexample to the plane Jacobian conjecture (a Keller pair
(P,Q) with J(P,Q)=1 and non-dividing degrees), or failing that, the
maximum-strength closure of the open attack surface.

Ground truth to build on (from Sessions 1–20, to be re-verified, not trusted):

- GGHV (arXiv:2204.14178, 2022): any counterexample has max degree ≥ 125 **or**
  degree pair (72,108)/(108,72). Within (72,108), shape (9,27) is closed;
  shape **(8,28) is open** — GGHV explicitly could not solve its system.
- Sessions 19–20 reduced the (8,28) system (72 unknowns / 92 quadratics) to a
  7-variable Newton-edge subsystem with 7 branches; **6 died mod 65521, r0
  unfinished**; ALL verdicts provisional pending the R1 or-branching soundness
  audit; everything is mod-p only.
- The only known route that outputs an actual map: Phase-4 direct construction
  (ten forced R's at (72,108), one (ρ=3, m=1) slice; ρ≠3 slices unexplored).
- Above 125 nothing is exhaustively closed; smallest admissible pairs
  (75,125), (84,126), (96,128), (88,132), (90,135) (per 1708.07936 §6,
  to re-verify).

So the counterexample, if reachable tonight, lives in exactly one of:
(i) a surviving branch of (8,28); (ii) a branch the old unsound eliminator
silently dropped; (iii) a Phase-4 realization; (iv) an above-125 shape.
Tracks B, A, C, D below attack precisely these, concurrently.

---

## 1. Track A — Soundness gate (GATEKEEPER, runs first)

**Question:** are the six DEAD verdicts real, and is the branch tree complete?

1. Reconstruct GGHV Prop 4.3's (8,28) system **from the paper text alone**
   (72 unknowns, 92 quadratic equations). No reuse of Session-20 memory.
2. Certify the reconstruction: count of unknowns/equations must match; the
   scaling symmetry (d_2_1 = 1 WLOG) must be re-proved, not assumed.
3. Build the eliminator with **correct R1 or-branching**: `u·w = 0` spawns
   BOTH child branches, tree explored exhaustively; every branch closure
   emits a machine-checkable certificate (the sequence of forced substitutions).
4. Divisibility checked at pivot *selection* (the Session-20 infinite-loop fix).
5. Re-derive the 20-var reduction and the 7-branch slope-2 edge decomposition
   independently; diff against the handoff's account.

**Kill criterion for the track:** reconstruction disagrees with the paper →
stop everything downstream, report the discrepancy.
**Deliverables:** `trackA_system.py`, `trackA_eliminator.py`, branch-tree
certificate, diff report.

## 2. Track B — The (8,28) hunt (MAIN EVENT)

Blocked by Track A's eliminator. Then:

1. Re-run r1–r6 with the sound eliminator, three 16-bit primes ≡ 1 (mod 3)
   (65521 first), Rabinowitsch vertex-nonvanishing, containment check printed
   on every saturation.
2. **r0:** decompose its 280-point edge into sub-branches (the move that
   rescued r4/r5/r6); run each sub-branch as a separate background process;
   memory-capped, checkpointed.
3. Anything alive across all primes → exact lift over ℚ (CRT + rational
   reconstruction, then exact verification in the original 92 equations).
4. Any ℚ-point with all Newton-polygon vertex coefficients nonzero →
   **Track F gate immediately** (bulletproof gate + GGHV automorphism-chain
   inversion). Only a gated, chain-inverted map counts as a counterexample.

**Outcomes:** survivor → candidate map; all-dead over ℚ with sound branching →
**theorem-grade: no counterexample below degree 125** (bound moves 108→125).
Either outcome is major. This track gets the most CPU.

## 3. Track C — Phase-4 direct construction (the map-producing route)

Independent of A/B (different mathematics), starts in Wave 2:

1. Re-derive the ten forced R's (k=3..12) from the Session-19 master identity
   `[q^D]K = g0^(a+b)(k·R' + D·R·(log g0)')` — re-prove the identity first
   (it exists only in the lost transcripts).
2. Build the realization layer for **k=3, D=13** (Sessions 10–13 tower
   machinery is the template and survives in the repo report): does the forced
   `R = S(v)/(v+1)^4` extend to a full boundary-compatible pair at (72,108)?
3. Enumerate the admissible (ρ, m) lattice beyond the (ρ=3, m=1) slice —
   the handoff admits Phase 4 covers ONE slice. New slices = new candidate
   structures nobody has looked at.

**Outcome:** an explicit obstruction per slice, or a surviving jet → escalate
to full construction.

## 4. Track D — Above-125 frontier (the long game)

Cheap reconnaissance in Wave 2, real work only if Waves 1–2 leave CPU idle
or (8,28) closes early:

1. Re-verify the admissible-pair list above 125 from 1708.07936 §6.
2. **(75,125)** first: its gcd=25 was an *exception* in the retracted gcd
   theorem (1708.09367 v1→v2 silent retraction) — possibly softer than
   believed. Build its GGHV-style shape system; measure size; if the Prop-4.3
   pipeline transfers, queue it behind Track B on the same eliminator.
3. Do NOT use the gcd≥36 filter anywhere (retracted).

## 5. Track E — Verification net (cheap, continuous)

1. Verbatim verification of every literature claim in the S19–20 handoff
   (GGHV theorem statements, Gao 2608.00222's explicit plane-case disclaimer,
   the 1708.09367 v1/v2 diff). Papers already downloaded to scratchpad.
2. Study Gao's dim-≥3 mechanism for transferable technology to dim 2.
3. arXiv sweep 2025–2026 for anything new on JC2 (don't repeat a stale-premise
   mistake: Sessions 7–18 spent months on a pair closed in 2022).
4. Regression: re-run all executable Sessions 1–18 certifications from the
   repo report (they are the only certifications that still exist anywhere).

## 6. Track F — Synthesis, gate, and ledger (continuous)

1. Rebuild `jc2_bulletproof.py` from its spec in the handoff (G0–G6; two
   independent bracket evaluations sharing no code; default = reject;
   errored gate = failure). Validate on known non-counterexamples INCLUDING
   the near-miss family before any candidate arrives.
2. Maintain `AUDIT_REPORT.md`; commit after every wave; every result carries
   its exact resume state (the N2 discipline).
3. Standing rules, adopted verbatim from the handoff:
   - mod-p empty is evidence, never proof; mod-p solutions prove nothing.
   - p ≡ 1 (mod 3) only.
   - every saturation prints its containment check.
   - candidates must pass the gate AND have nonzero vertex coefficients AND
     survive automorphism-chain inversion.
   - "it's slow so it must be deep" = instrument before concluding. Every such
     hypothesis in Session 20 was a bug.

---

## 7. Wave schedule and usage pacing

Token spend is dominated by model reasoning, NOT by CPU: long computations run
as **background Bash processes** (free), the session sleeps between harvests
via scheduled wakeups. This is how we run all night without burning the cap
in five minutes.

| Wave | Local time | Work | Token posture |
|---|---|---|---|
| W1 | 10:20 p.m.–12:00 | Track A complete; E.4 regression; F gate built | full effort (derivations) |
| W2 | 12:00–3:00 a.m. | Track B branch runs (background CPU); C.1–C.2; E.1–E.3 | LOW — launch & sleep, hourly harvest wakeups |
| W3 | 3:00–6:00 a.m. | B survivors → lift+gate; else C.3 slices + D.2 | scales with findings |
| W4 | 6:00–7:00 a.m. | Synthesis, ℚ-verification of every closure, commit, PR, morning report | medium |

Concurrency: 4 CPUs → at most 3 compute processes + 1 for the session.
Agent fan-out capped accordingly (workflow slots ≈ 2); breadth comes from the
night's length, not from parallel width.

Checkpoint commits: end of every wave, plus immediately on any survivor.
If a usage cap hits: commit as-is with resume note (N2 hard-stop discipline);
background processes keep running through the pause and results are harvested
on resume — the night is not lost.

## 8. Defined outcomes for the morning report

1. **COUNTEREXAMPLE:** a gated, chain-inverted Keller pair. (Stated plainly,
   with the full certificate. Nothing less gets this word.)
2. **SURVIVOR:** a ℚ-point of the (8,28) system or a live Phase-4 jet that
   passed every check we could run but isn't yet a map — with the exact
   remaining steps.
3. **CLOSURE:** (8,28) dead over ℚ with sound branching → no counterexample
   below degree 125. A real theorem, publishable, and the bound's first
   movement since 2022.
4. **PARTIAL:** exact state of every branch, what's still running, and the
   resume command for tomorrow night.

No outcome will be dressed up as a bigger one.
