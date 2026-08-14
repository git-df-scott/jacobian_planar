# AUDIT REPORT

## OVERNIGHT REPORT — 2026-08-14, 07:00 local (13:00 UTC)

**Outcome classification (NIGHT_PLAN §8): PARTIAL.** No counterexample. No
non-EMPTY verdict anywhere in the campaign, ever. No candidate has reached the
gate. Nothing is certified over Q yet, so no closure claim either.

### 1. Verdict tally
- **46 EMPTY verdicts**, **0 non-EMPTY**, 0 SURVIVOR lines.
- Case (2) leaf 2 (the never-before-searched d_2_2-free locus, Sol(case 2) =
  Sol(leaf 2)): **fully dead at three primes** — 65521, 65539, 65599 — branch
  decomposition re-derived independently at each prime, r0 fibers closed by
  recursive univariate radicalization (338 -> 6 and 280 -> {1,2}).
- Case (2) leaf 1 (the old campaign's slice): **dead at p=65521 and p=65539**
  (the latter a full 5277s sweep, all 7 branches). p=65599 is stuck on ONE
  terminal branch, `L1_p65599_r0b_f0_f0_f0_f0` — a vdim-6 endpoint that needs
  more contiguous CPU than a container window provides; it is restarted and
  killed each cycle. Not a mathematical obstruction; an environment tax.

### 2. Exact-Q certificate status
- **0 charts CLOSED. The route was rebuilt twice and the blocker is now gone.**
- The char-0 edge eliminant — the single computation everything stalled on —
  **completed via msolve**: `trackB_edgeQ.msolve.out`, 796KB, elimination
  polynomial **degree 1144**, matching the independently certified vdim. That
  is the unblock; the remaining Q work is factor-over-Q then per-factor branch
  closure (Decision 4), which is window-sized and mirrors the proven mod-p
  pattern.
- Monolithic per-chart Q runs (mine, both direct and modStd) are **measured
  dead ends** and are retired. The Opus session's Nullstellensatz-certificate
  machinery (cofactors T with I*T = 1, verified by exact polynomial arithmetic,
  replayable independently of how the basis was found) stands ready and is the
  right acceptance bar for every Q verdict.
- One log line at 02:11:02 reading STALLED is an operator kill during an engine
  switch, annotated in-log as not a verdict.

### 3. Overnight Opus-session integration
Merged into the audit branch: the msolve edge eliminant, leaf-1 sweep
progress, the C3 ladder certification (13 PASS), the C2 correction
(D = 5k-2 derived; the old handoff's 3k+4 wrong from k=4 and manufacturing a
spurious death), and the C4 refined sweep (22 of 23 slices carry a forced R —
the ODE layer discriminates almost nothing, so all separation lives in the
realization layer, which is gated by the THEOREM 3 gap).

### 4. Pentagon case (1) — Decision 2 state
**No verdict. The numeric tower prescribed by Decision 2 is not yet written.**
The symbolic tower is retired (measured: level 17 costs 79s/150MB, level 16
does not finish in 1400s, nine levels below it). The rewrite — (S,a,b)
instantiated in F_p first, every level a small dense linear solve, no symbolic
carry — is the single highest-value piece of work outstanding, because an
exhaustive p=31 sweep is a genuine complete statement about the pentagons and
they are the last open door below degree 125.

### 5. Environment ledger (design constraints, measured)
Container lifetime ~1-2.5h, frequently much less; processes die with it,
filesystem survives. Any monolithic run budgeted past a window cannot land.
Marker-resumable staged pipelines are the only design that makes progress here
— which is why the mod-p sweeps completed and the monolithic Q charts did not.

---

## Addendum — Opus 5 priority-queue session, 2026-08-13/14

Status line per OPUS_PLAN P1: **stalled-with-data on P0 and P3; P1 and P2 in
flight with the exact-Q route rebuilt; P4 advanced with one certified result
and one certified gap.** No counterexample. No non-EMPTY verdict anywhere. No
candidate has reached the gate.

**Environment.** The container came up without Singular — the campaign's
engine — and it had to be reinstalled before anything could run. A later
restart killed every process after ~2.5h of wall time with the filesystem
intact. Both facts are now recorded in RESUME_STATE.md, and the second is a
design constraint, not an annoyance: any monolithic Groebner run budgeted
beyond ~2h cannot land here, whatever timeout it carries.

**P0 pentagon endgame — STALLED, measured.** `--tower-check` had been dead
since the pause commit (appending `tower_lift` overwrote `tower_check`'s def
line, leaving the body unreachable after a `return`); restored, and T1 now
PASSES. T2 is stalled on per-sample cost: level 17 costs 79s/150MB and level
16 does not finish in 1400s at 1.8GB, with nine levels still below it and any
kill living below all of them. T4's 4.47M-sample sweep is three further orders
out. T5's engines both lost — slimgb is 2x slower and 3.5x heavier than std,
and msolve dies in monomial hash-table growth. **No verdict on case (1).**

**P3 above-125 — BLOCKED, escalated.** The Newton polygons for every
above-125 pair are unpublished. 1708.07936 §6 gives chain data only; GGHV
2204.14178 §4 gives polygons for (9,27), (9,24), (8,28), (7,21) alone, derived
case-by-case by hand with no general recipe. P3b-P3d are built and
pair-agnostic; they are blocked on an input only a Fable-grade derivation can
produce. Engine calibration was done anyway and is itself informative: msolve
on the RAW case-(2) system (73 vars) grew past 10GB in ~8 minutes and was
killed without a verdict — the elimination-first pipeline is what makes this
family finite, whatever the engine.

**P1 exact-Q — route rebuilt, in flight.** The char-0 edge eliminant burned
over an hour twice with no output, so the fallback (per-chart closure with no
eliminant) now runs on `modStd` — modular GB over Q with rational
reconstruction — and every EMPTY verdict is backed by an explicit
Nullstellensatz certificate: cofactors T with I*T = 1, extracted by `lift`,
verified by exact polynomial arithmetic in the same run, written to disk. A
chart is logged CLOSED only when dim = -1 AND the certificate verifies;
otherwise UNCERTIFIED. The certificate replays with polynomial multiplication
alone, independent of how the basis was found.

**P2 leaf 1 — in flight, 15 branches EMPTY so far.** The staged pipeline is
now leaf-parametrized (`JCLEAF`) and derives the Newton-edge equation indices
from the equations instead of hardcoding them, with leaf 2's indices pinned by
assertion as a regression check. p=65521 complete; p=65539 through its final
r0b branch; p=65599 and leaf-1 exact-Q queued unattended. Leaf 1's eliminant
reproduces ELIMDEG 43 — the same degree as leaf 2's and as the handoff's
deg-43 story, an independent cross-check of the shared edge subsystem.

**P4 Track C — one certified result, one certified gap.**
- C2 COMPLETE: the ten forced R's at k = 3..12, each unique up to a scalar,
  each passing the exact block check. D(k) = 5k - 2 is DERIVED from C1's
  order matching; **the handoff's D = 3k+4 is wrong** from k = 4 on, and under
  it the k = 4 slice returns DEAD_resonance — the wrong relation manufactures
  a death. Our k = 3 forced S matches the handoff's exactly; the sign of c
  does not (+455 vs -455), logged as a convention discrepancy.
- C4 enumerated and swept for INPUT ONLY (it is Fable-grade): 22 of the 23
  refined slices carry a forced R, the sole death being the degenerate (1,2).
  The ODE layer does not discriminate; whatever separates these slices lives
  in the realization layer.
- C3 layer 1 CERTIFIED (13 PASS): the formal (b/a)-th root, chain <=>
  square-root agreement, the first deviation block 2g^6*delta entering
  LINEARLY (the structural reason the endgame is an ODE), and a ladder
  operator whose divisibility behaviour checks out.
- **C3 layer 2 GAP, and it is load-bearing.** THEOREM 2 (total rigidity) and
  THEOREM 3 (pole-fiber, hence R polynomial) are prose whose executable
  engines died with the transcripts, and neither is reproduced. C1 forces the
  pole ORDER; the fiber-counting step that makes R a POLYNOMIAL is not
  recovered. **Every (72,108) statement assuming a polynomial R inherits this
  gap — the C2 table included.** Flagged for Fable rather than papered over.

---

# (earlier) AUDIT REPORT — JC2 Counterexample Campaign, night of 2026-08-12/13

**Outcome class (NIGHT_PLAN §8): PARTIAL → upgraded findings below.**
No counterexample was found as of this writing. What WAS found is better than
anyone had a right to expect from an audit: **the previous campaign's coverage
claims were structurally wrong, and the genuinely open search space below
degree 125 is substantially larger than the Sessions 19–20 handoff believed.**
Two Gröbner runs on the newly-exposed ground are in flight at this writing.

---

## 1. The two campaign-redefining findings (Track A, certified)

### Finding 1 — the "6 of 7 branches dead" verdict covered only a slice
The Sessions 19–20 elimination pipeline used an unsound rule: on a monomial
equation `u·w = 0` it silently set one variable to zero instead of branching.
Track A rebuilt the elimination soundly (or-branching, machine-replayable
certificates, verified replays) and found that at the VERY FIRST fork of the
normalized (8,28) case-(2) system, the sound tree splits:

- **Leaf 1** (`d_2_2 := 0`): 20 vars / 41 eqs — exactly the state the old
  campaign's whole r0–r6 hunt lived in. Its 7-var/6-eq Newton-edge subsystem
  is reproduced exactly.
- **Leaf 2** (`d_3_5 := 0`, `d_2_2` free): 22 vars / 44 eqs — **never explored
  by anyone.** Moreover the certificates show `d_3_5 = 0` is forced inside
  leaf 1, so Sol(case 2) = Sol(leaf 2): the old campaign searched the
  `d_2_2 = 0` slice of the true variety. **Closing leaf 2 closes case (2);
  a point on leaf 2 with the nonvanishing side conditions is a counterexample
  lead.**

### Finding 2 — a second polynomial system nobody knew about
GGHV Prop 4.3 is a disjunction of TWO Newton-polygon cases. The handoff's
72-unknown/92-equation system is case (2) (quadrilaterals) ONLY. Case (1)
(pentagons, extra vertices (0,8)/(0,12)) gives a **186-unknown / 302-equation
system absent from the handoff entirely.** Even a full closure of case (2)
does not close the (8,28) shape. Track A's structural analysis found the
natural attack: the pentagon top edges force the leading forms to satisfy
`lP = a·S²`, `lQ = b·S³` for a single slope-1 form S with 5 coefficients —
a parametrization invisible to the old R1/R2 pipeline.

**Consequence:** the (72,108) door below degree 125 is open wider than the
2022–2026 literature consensus assumed. This is where a plane counterexample
lives, if one lives below 125 at all.

## 2. Verified foundations (Tracks E and F, complete)

- **Every literature premise verified verbatim** (trackE_literature_verified.md):
  GGHV's ≥125-or-(72,108) theorem; the (8,28) shape "left open" in the
  authors' own words; the silent retraction of the gcd≥25/36 theorem
  (1708.09367 v1→v2, no erratum — that filter is banned); the July 2026
  refutation of the Jacobian conjecture in EVERY dimension ≥ 3
  (Alpöge–Gallagher–Speyer–Gao line, explicit "two-dimensional case remains
  open and is untouched"); Borisov's Second Framework data (435,290)/D=23
  confirmed, no explicit Belyi polynomials published for it; Borisov's
  Three-dessin framework independently predicts degree pair (108,72) —
  converging with GGHV's open case. 2024–2026 sweep: nobody has closed
  (72,108). **Premises stand.**
- **The old repo's executable record fully reproduces** (trackF_regression_report.md):
  Sessions 1–8/10 rerun with ZERO divergences; the C³ map's generic fiber
  size is 3 (constant Jacobian, non-injective — dim-3 counterexample
  behavior, coherent with the 2026 refutation); Session 6's frontier sweep
  has NO live templates; the cross-epoch identity h₀ = −13·n₃ verified by
  independent arithmetic. Sessions 9/11–18 remain prose-only (their checks
  died with the lost transcripts) — their generalization is Track C's open
  re-derivation.
- **The bulletproof gate is live** (jc2_bulletproof.py + jc2_gate_validation.md):
  6/6 known non-counterexamples rejected, including Borisov's own near-miss
  failing at exactly the predicted gate. Any candidate from any track must
  pass it, plus GGHV automorphism-chain inversion.

## 3. Compute in flight at this writing

| Run | Target | Engine | Status |
|---|---|---|---|
| leaf 2, p=65521 | THE new ground (Sol(case 2)) | Singular groebner, Rabinowitsch nonvanishing | running, ~12 CPU-min, 2.7 GB |
| leaf 1, p=65521 | control (must be handoff-compatible) | same | running |

Results auto-commit via trackB_autopush.sh even if no model wakes again.
mod-p is scouting evidence ONLY (p ≡ 1 mod 3); any verdict that matters gets
redone exactly over Q; any surviving point gets CRT-lifted, verified in the
hash-pinned original system WITH side conditions, then gated.

## 4. Honest scorecard vs the night's goal

The user asked for a counterexample by morning. What exists by morning:
- No counterexample (and no fabricated one — the gate exists precisely so
  that nothing less than a real one can ever be claimed).
- The search space where one could live is now correctly mapped for the
  first time: leaf 2 + case (1), both genuinely unexplored by the field.
- A sound, certificate-emitting elimination engine, a validated candidate
  gate, a verified literature base, and a fully reproducible pipeline —
  the infrastructure a real hunt needs.
- The previous campaign's central negative claims are now known to be
  under-covering; its positive machinery (edge subsystem, normalization)
  is independently confirmed.

## 5. Next steps, ranked (for the next session)

1. Read leaf-2 verdict; if EMPTY mod p → two more primes, then exact-Q
   closure attempt (that plus leaf-1/case-(1) closure = "no counterexample
   below 125", a publishable bound improvement 108 → 125).
   If NONEMPTY → extract mod-p points, CRT lift, gate. This is the live lead.
2. Case (1) pentagons via the S-parametrization (trackA_report.md §A4 has
   the derivation; 186/302 system on disk, hash-pinned).
3. Track C: re-derive the master identity (stands up or knocks down the
   Sessions 11–18 prose theorems + the ten Phase-4 forced R's).
4. Track D: (75,125) shape system above 125.

## 6. File inventory (all committed, PR #3)

trackA_gghv_system.py / trackA_eliminator.py / trackA_report.md /
trackA_system_case{1,2}.json / trackA_reduced_system*.json (leaf tree,
certificates; 302MB case-1 intermediate kept local-only) /
trackB_leaf_runner.py / trackB_autopush.sh / trackB_leaf*_p65521.* /
jc2_bulletproof.py / jc2_gate_validation.md / trackF_regression_report.md /
trackE_literature_verified.md / NIGHT_PLAN.md / RESUME_STATE.md.
