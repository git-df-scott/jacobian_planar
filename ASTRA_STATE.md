# ASTRA state — 2026-09-04

## CURRENT VERIFIED THEOREMS

- **THEOREM — Keller escape bridge.**  At a resolved source dicritical
  component E mapping with tangential degree d_E to a smooth point of a target
  non-properness component, a generic transverse meridian cycle has length
  r_E=1-k_E, where k_E=-ord_E(dx wedge dy).  Consequently
  c_i=sum_E d_E and e_i=sum_E d_E(1-k_E).  If the target parametrization has
  bidegree (alpha_i,beta_i), its coordinate horizontal degrees on E are
  alpha_i d_E and beta_i d_E.

- **THEOREM — Euler/escape budgets.**  Every target blueprint in the
  stratified-cover model must satisfy both the source Euler equation and the
  escaping-curve Euler equation in `OFF_BY_ONE.md`.  Failure of either equation
  excludes the blueprint before curve realization.

- **THEOREM — mate period obstruction.**  If the Gelfand--Leray form is a
  nonzero holomorphic differential on a compact positive-genus fibre, it is not
  exact.  Hence P has no rational or polynomial Keller mate.

- **THEOREM with cited geometry — two Briançon polynomials.**  The exact
  boundary calculation for `g` and `g'`, combined with the published
  irreducible genus-one fibre theorem, excludes a mate in every degree.

- The necessary target-side conditions in PR #24 and the exact-Q monomial
  certificates in PR #23 retain only their explicitly stated scopes.

## CURRENT EXACT COMPUTATIONAL RESULTS

- `EXACT-Q`: the identity-automorphism compactification control has pole
  vectors `(1,0,1)` and `(1,1,0)`, geometric degree 1, and Keller delta
  `(0,0,0)`.
- `EXACT-Q`, bounded: on all 11,465 archived boundary-tree records through six
  blowups, neither H3 target bidegree (3,5) nor (3,6) admits even one coordinate
  pole/horizontal divisor satisfying exact nonnegative complementarity.  There
  are zero joint survivors.
- `EXACT-Q`: the independent H3 enumeration has 45 double transpositions,
  16 labeled triples after fixing one generator, one simultaneous-conjugacy
  orbit, generated-group order 60, staying counts `(0,1,0)`, Euler 1, and
  coarse chi(R)=0.
- `ADMISSIBLE-SHAPE`: the PR #24 abstract screen reproduces 5,261 rows and 635
  basic signatures.  These are not group or curve realizations.
- `EXACT-Q`: five positive Poisson witnesses pass `{P,Q}=x^2` exactly.
- `EMPTY-mod-p`: graded case (2) is empty at p=32003 across its five leading
  orbits.  Characteristic zero remains `UNKNOWN`.
- `EXACT-Q`: both degree-ten Briançon gradients have Groebner basis `[1]`; all
  three infinity valuations of eta on the t=1 fibres are zero.
- PR #23's 25 monomial certificates remain exact-Q for their generated polygon
  strata; the above-125 case interpretation remains conditional.

## WALLS

- GAP, Singular, and msolve are unavailable in the current runtime.  No
  timeout, installation failure, or absent executable is a mathematical
  result.
- The full PR #24 curve-by-curve low-index enumeration was not replayed here.
- Case (2) lacks a compact exact-Q lower-level certificate and a reconciliation
  of the degree-35 versus degree-1144 characteristic-zero objects.
- The highest-ranked published above-125 case, (108,144) from the chain
  `(8,28)->(7/4,3)` with (m,n)=(3,4), stops at the translation gate: the paper
  does not print the compiler's assumed A'_t and the c' ladder is uncorrected.
- Target/source compatibility is presently implemented only for generic
  dicritical data and the archived tree list through six blowups; singular
  boundary maps and larger trees remain open.

## RETRACTED CLAIMS

- Stale B=16 d=6 through d=12 `EMPTY` rows are void after the GGV
  transcription correction.
- Case-(2) `EMPTY over Qbar` is not established by the audited evidence.
- A modular nonempty or empty fibre is not a characteristic-zero verdict.
- The unrestricted `general.py` / `batch.py` graded EMPTY claims are retracted;
  their common-degree restriction excluded positive witness W3.
- Above-125 monomial kills are not closures of published cases until the
  compiler provenance is repaired.
- Target `TIMEOUT`, OOM, and missing GAP runs are `UNKNOWN`.

## LIVE EXPLICIT-POLYNOMIAL LANES

1. Construct an all-irreducible, gradient-unimodular, non-coordinate
   Briançon-type P whose eta has a residue-free pole divisor of degree at least
   three, then kill its elliptic de Rham component exactly.
2. Turn the graded case-(2) modular descent into an exact-Q orbit certificate,
   after proving that the characteristic-zero residual object is the same one.
3. Reconstruct a published above-125 Newton case directly from its primary
   chain data; only then derive and run its graded one-variable descent.

## LIVE TOPOLOGICAL LANES

1. Add source intersection data to each group-first record at generation time,
   using the bridge equations rather than post-processing curve realizations.
2. Enumerate peripheral braid factorizations only for group records satisfying
   both Euler budgets and source complementarity.
3. Determine the minimum boundary depth forced by an H3 dicritical of
   discrepancy -1 and coordinate degrees (3d,5d)/(3d,6d), instead of blindly
   raising the tree bound.

## TOP THREE ATTACKS

1. **Source lower bound for H3.**  Convert the new six-blowup emptiness into a
   depth/intersection theorem, or derive the first possible depth and unique
   boundary skeleton.
2. **Residue-free Briançon construction.**  Search embeddings realizing a
   triple-pole exact differential, with Gate 0 and positive controls first.
3. **Exact-Q graded descent.**  Lift the 1+1+3 orbit factorization and lower
   linear chain over Q; do not run another monolithic Groebner job.

## DO-NOT-REPEAT LIST

- Do not scan generic coefficient boxes or restart B=16.
- Do not run the case-(2) y-adic depth-6 wall.
- Do not call a finite target blueprint an algebraic realization.
- Do not enlarge target singularity count or source tree size without a forced
  invariant.
- Do not use above-125 compiler output as published-case evidence until A'_t
  and cmax/c' provenance are fixed.
- Do not promote modular results, numerical near-hits, or solver failures.
- Do not apply an ambient three-dimensional Keller statement to a surface
  restriction without proving the induced two-dimensional Jacobian condition.
- Do not call any explicit pair a CEC before exact bracket and independent
  noninvertibility verification.

Current counterexample status: **no CEC and no CE**.
