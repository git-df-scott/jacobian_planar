# AUDIT REPORT — JC2 Counterexample Campaign, night of 2026-08-12/13

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
