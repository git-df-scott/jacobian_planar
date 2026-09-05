# Session 44 night runbook — order: 1, 4, 3, 5, 2

Constraint: ~2h45m of active compute before reset; long jobs go to background
early. Execution starts on the user's word. NOTHING is a result until its
verification gate passes and it is committed.

## Verification protocol (binding, every lead)

- Every instrument carries a control that FAILS if the suspected bug class is
  present (a control that cannot see the risked terms calibrates nothing).
- Every EMPTY: two independent routes when feasible (msolve + second gauge /
  direct-vs-reduced system / second prime for modular work).
- Every NONEMPTY: extract the witness, replay it by direct substitution in
  exact arithmetic, only then report.
- Commit after each lead; failures and retractions recorded as loudly as wins.

## Lead 1 — the µ1-crack (0:00–1:15, top priority)

The first positive signal of the campaign: at deg(q1)=8, `µ1≠0` came back
NONEMPTY (conjecture-refuting if real) while `µ2≠0` stayed EMPTY. But the
(3.5) transcription failed the §3.1 Laurent control (−6µ0y³ residual), so
everything Abel-derived is suspect until re-founded.

1. Fix `b16_direct.py`'s msolve output parsing (C2 UNPARSED); get C1+C2 green.
   The direct bracket system is ground truth — no transcription to trust.
2. Pin (3.5): either re-derive it mechanically from the direct system via the
   paper's substitution chain (sympy), or repair the sign/placement against
   BOTH controls (deg-3 planted pair AND §3.1 Laurent µ0=1 example).
3. Re-run the full ladder µ0≠0 (deg 2–12) and conjecture queries µ1≠0/µ2≠0
   (deg 3–8) on the corrected foundation. Cross-check at least two cells
   against the direct system (j=1,2).
4. Branch on the crack:
   - REAL → extract the deg-8 µ1-family witnesses (msolve parametrization),
     exact replay, map the family (dimension, definition field), test µ1≠0 at
     deg 9–12, then run µ0≠0 at deg 13–16 restricted to the µ1-mechanism's
     stratum. This is the ride-the-crack path toward a CE.
   - ARTIFACT → retract in B16_ABEL_LADDER.md loudly, re-establish the ladder
     on the corrected equation, extend µ0≠0 to deg 13–16.
   Win either way: verified refutation of the 2013 conjecture (real math), or
   a corrected, extended, double-founded ladder.

## Lead 4 — the 24 published untouched shapes (1:15–2:00)

1. Verify the FABLE_24 extraction against arXiv:1708.07936 §6 directly (the
   campaign's own flagged prerequisite; fetch the PDF).
2. First target: chain-length-1, corner (8,28), (m,n)=(3,4), max=144. Build
   its direct bracket system from the GGV normal form (same construction as
   b16_direct, different corner data). Control: a planted consistency check +
   reproduce one known discarded case's verdict with the same builder.
3. Budget cap: if the Prop-4.3-analogue derivation resists verification in
   ~30 min, fall back to the campaign's fable_xcol pipeline (sol3 branch,
   documented as "runs unchanged" for these cases).
4. Launch the µ-saturated emptiness query (background if heavy; char-0 first,
   two primes as fallback).
   Win: the first verdict ever recorded on a published untouched case.

## Lead 3 — reducible-tear sieve v2 (2:00–2:30)

1. Arithmetic layer first: enumerate admissible (n_i, χ_i) data for
   2-component tears from Session 43's Euler identity Σ(d−n_i)χ(A_i)=d−1
   (pure integer combinatorics, includes the 7 deeper-point configs).
2. Group layer: 2-component model configurations with standard π₁
   presentations (disjoint quasihomogeneous components first); reuse the
   validated homology engine. Controls: d=2..5 must remain empty.
3. Win: surviving topological types = construction targets (the generative
   path), or the floor theorem extends to reducible tears.

## Lead 5 — above-150 (2:30–2:50, scoping)

1. `gghv_audit/all_cases_max_le_300.json` already exists on the mailbox
   branch, produced by the mechanized 19/19-control enumerator. Read it,
   count (150,300], cross-reference the 464-audit and the 36+5 TIMEOUTs,
   rank by system size.
2. Emit the ranked target list; if budget remains, build the smallest case's
   direct system and queue it.
   Win: the "blocked on chain-compiler" territory becomes a ranked queue.

## Lead 2 — B≥17 (last; memo during background waits)

1. Establish why the shape theory stops at 16 (Heitmann's bound is B≥16;
   GGV analyzed only the minimal case). Derive the B=17 corner-constraint
   skeleton mechanically where possible (the (1,−1) leading-form analysis).
2. Deliverable tonight: a feasibility memo + the first constraint skeleton
   for gcd=17 — the first map of genuinely unmapped territory.

## Standing background jobs to carry through the night

- Any msolve run > 5 min goes to background immediately with a logged
  completion marker; check and fold in at each lead boundary.
- Commit + push at every lead boundary; PR #20 comment at end of night.
