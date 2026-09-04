# ASTRA state — 2026-09-04

Closing record: `JC2_COMPLETE_RECORD.md` and `record/README.md` inventory all
44 remote branches at the cutoff and recover two unpublished Codex commits.
`RECORD_CORRECTIONS.md` governs interpretation of historical claims.

## CURRENT VERIFIED THEOREMS

- **THEOREM — Keller escape bridge.**  At a resolved source dicritical
  component E mapping with tangential degree d_E to a smooth point of a target
  non-properness component, a generic transverse meridian cycle has length
  r_E=1-k_E, where k_E=-ord_E(dx wedge dy).  Consequently
  c_i=sum_E d_E and e_i=sum_E d_E(1-k_E).  If the target parametrization has
  bidegree (alpha_i,beta_i), its coordinate horizontal degrees on E are
  alpha_i d_E and beta_i d_E.

- **THEOREM — generic-fibre bridge.**  Adjunction on the source boundary gives
  `chi(P fibre)=sum_E(k_E-1)dP_E`.  The escape components supply
  `-sum_i alpha_i e_i`, so the remaining P-horizontal components must have
  weighted contribution D; identically for Q.  For H3 this recovers fibre
  Euler values `-6` and `-14/-18` and forces a +6 non-escape budget for each
  coordinate.

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

- **Written exact obstruction from closeout:** the recovered night26 model
  `t=r^2+2u^2r, R=r^3` cannot admit a faithful Keller plane chart. Since r is
  rational and r^3 polynomial, integral closure makes r polynomial; the
  Jacobian is then divisible by r^2. Its archived GO recommendation is
  superseded. This excludes that model, not every degree-six construction.

- `EXACT-Q` with written completeness and valuation arguments: GGHV
  Proposition 4.3(1), the pentagon, is excluded in characteristic zero. The
  complete graded prefix has five parameters after a justified right-edge
  normalization. Six independently multiplied finite-field certificates
  exclude both charts of its weighted projective compactification; every
  exact coefficient operator has verified good reduction at the chosen prime.
  See `ASTRA_3_PENTAGON_PROJECTIVE.md`. Together with Astra 2 this excludes
  both polygons of Proposition 4.3 and its original case called (8,28), not
  JC2 or the different above-125 (3,4) chain. No external peer review or
  proof-assistant formalization is claimed.

- `EXACT-Q` with a written completeness proof: GGHV Proposition 4.3(2) is
  excluded in characteristic zero. A five-dessin count proves completeness
  of the five leading scaling orbits; a complete lower parametrization and
  26-term Nullstellensatz certificate exclude every extension with the required
  top corner. Independent FLINT verification passes. See
  `ASTRA_2_CASE2_EXACT_DESCENT.md`. Astra 3 closes the neighboring pentagon.

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
- `EMPTY-mod-p`: the historical p=32003 case-(2) result remains valid in its
  original scope; the new characteristic-zero result above supersedes UNKNOWN.
- `EXACT-Q`: both degree-ten Briançon gradients have Groebner basis `[1]`; all
  three infinity valuations of eta on the t=1 fibres are zero.
- PR #23's 25 monomial certificates remain exact-Q for their generated polygon
  strata; the above-125 case interpretation remains conditional.

## WALLS

- Singular 4.3.1 was provisioned locally for the second Astra run, and PARI/GP
  2.15.2 for the third. GAP and msolve were not provisioned. No timeout or
  absent executable is evidence. Three direct exact pentagon eliminations
  timed out; the successful proof instead controls the projective boundary.
- The full PR #24 curve-by-curve low-index enumeration was not replayed here.
- The historical degree-1144 object's provenance remains unresolved. The new
  case-(2) proof reconstructs its inputs directly from the published polygon
  and proves the five/35 count independently; it does not identify that object.
- The highest-ranked published above-125 case, (108,144) from the chain
  `(8,28)->(7/4,3)` with (m,n)=(3,4), stops at the translation gate: the paper
  does not print the compiler's assumed A'_t and the c' ladder is uncorrected.
- Target/source compatibility is presently implemented only for generic
  dicritical data and the archived tree list through six blowups; singular
  boundary maps and larger trees remain open.

## RETRACTED CLAIMS

- Stale B=16 d=6 through d=12 `EMPTY` rows are void after the GGV
  transcription correction.
- Earlier case-(2) `EMPTY over Qbar` claims remain unsupported by their old
  evidence. The new result has a separate completeness proof and exact
  certificate; it does not retroactively validate those claims.
- An affine modular nonempty or empty fibre alone is not a characteristic-zero
  verdict. Astra 3 additionally verifies good reduction and excludes the whole
  projective special fibre, then supplies the valuation argument.
- The unrestricted `general.py` / `batch.py` graded EMPTY claims are retracted;
  their common-degree restriction excluded positive witness W3.
- Above-125 monomial kills are not closures of published cases until the
  compiler provenance is repaired.
- Target `TIMEOUT`, OOM, and missing GAP runs are `UNKNOWN`.

## LIVE EXPLICIT-POLYNOMIAL LANES

1. Construct an all-irreducible, gradient-unimodular, non-coordinate
   Briançon-type P whose eta has a residue-free pole divisor of degree at least
   three, then kill its elliptic de Rham component exactly.
2. Reconstruct a published above-125 Newton case directly from its primary
   chain data; only then derive and run its graded one-variable descent.
   Both Proposition 4.3 polygons are now closed by separate proofs.

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
3. **Above-125 provenance repair.** Derive the missing lower corner and c'
   range for `(8,28)->(7/4,3)`, `(m,n)=(3,4)`, before generating equations.
   The completed (2,3) pentagon descent does not transfer to this ratio.

## DO-NOT-REPEAT LIST

- Do not scan generic coefficient boxes or restart B=16.
- Do not run the case-(2) y-adic depth-6 wall.
- Do not restart either Proposition 4.3 polygon without a concrete flaw in
  Astra 2 or Astra 3. Replay their certificates before reopening them.
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
