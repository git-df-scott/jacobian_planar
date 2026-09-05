# ASTRA state — 2026-09-05

## September 5 corrected degree-144 strike — current

[Astra 11](ASTRA_11_CORRECTED_DEGREE144.md): **OPEN, no CE**.
The archived compiler sends the original top corner to `(4,8)` under its
stated maps but uses `(4,4)` in its output. Its degree-144 slice calculations
therefore do not establish treatment of the full published `(108,144)` case.
The original lower corner `(1,0)` is now derived. The reduced upper-axis
boundary still requires proof; do not substitute the old `c'` ladder.

The corrected first auxiliary leading equation has 17 marked normalized
solutions in five number-field factors, with degrees `1,2,4,4,6`.
The type-I.b terminal equation has two conjugate shapes. These are endpoint
classifications, not global Keller components. A new simple-root theorem
excludes the complete slice with P rows `2,7,12` and Q rows `1,6,11,16`
for all 17 leading solutions, in arbitrary coefficient degrees. Other rows
remain live. Run `python astra11/verify.py` for exact reproduction.

## September 5 search beyond the collision algebra — current

[Astra 10](ASTRA_10_OUTSIDE_COLLISION_SEARCH.md) remains **OPEN: no CE**.
It proves three new scoped obstructions, with written proofs and nine
passing exact checks in astra10:

- Every P=p^m*u+s*A(p), m>=1, A arbitrary, has no polynomial Keller mate.
  For A(0)!=0 the compact hyperelliptic time form is holomorphic; the
  exceptional coefficients fail by residues or a vanishing gradient.
- The pencil W^2=D0(p)+4t*p*(p-1), deg D0>=3, has no rational primitive
  for dp/((p-a)^k*W), for arbitrary k>=1 and a!=0,1. Exactness would force
  an isotrivial three-point-cover family, contradicted by branch cross-ratios.
  The report gives the corresponding polynomial P family with arbitrary
  coefficient degrees. This does not exclude every multiple-pole embedding.
- A rational total-space model with an exact elliptic primitive of degree
  six was reconstructed and excluded in every faithful polynomial chart.
  More generally P^m Q^n=f(r), for a polynomial Keller pair, rational r,
  and polynomial f, forces f to be a pure translated power of degree
  dividing gcd(m,n). This closes the model with (m,n,deg f)=(1,2,6).

No polynomial pair passed the global test. The new arguments are not
externally reviewed or proof-assistant formalized. No universal finite
component reduction for JC2 is claimed. The collision algebra remains
fully closed by Astra 9, independently of this new search.

## September 5 full collision-route closure — current

[Astra 9](ASTRA_9_FULL_COLLISION_ROUTE_CLOSURE.md) proves
**FULL COLLISION-ROUTE CLOSURE**. For arbitrary finite P,Q in
C[b,c]+Delta*C[v,c], a constant Jacobian must be zero.

- Collision parity forces a nonmonomial positive mixed-weight leading form.
- Such a form has the forbidden slope-one Newton edge: an exact algebraic
  fibre branch makes the polynomial potential have a nonzero residue.
- Thus both components must have nonpositive mixed weight, which makes their
  Jacobian divisible by c and therefore zero on c=0.
- This covers the entire (6,9) resonance, both rho alternatives, every N,
  and all higher degrees. No polynomial potential passes the global criterion.
- The proof is in astra9, with seven passing exact checks and an independent
  published match for the slope-one obstruction. It is not proof-assistant
  formalized. The general JC2 conjecture is not settled by this scoped theorem.

The older OPEN paragraphs below are historical and superseded for this lane.

## September 5 degree-15 strike — historical

[Astra 8](ASTRA_8_DEGREE15_STRIKE.md) remains **OPEN**. The requested full-route
decisive outcome has not been established.

- The entire noncube-h (6,9) component is excluded by an exact global pole
  argument and a nonzero resultant, with unbounded coefficient degrees.
- A necessary invariant valid in arbitrary degree says that a nonconstant
  polynomial m-th root f of a component's leading coefficient must be a power
  of one linear factor, of exponent at least two.
- Consequently the remaining (6,9) collision system has h=c^(3N), N>=2,
  after constant target scalings. It reduces to five explicit algebraic
  first-integral equations, polynomial reconstruction and two parity identities.
- Both rho=2/3 and rho=4/3 force a double-root leading cubic. The resonant
  system is not eliminated and its irreducibility is not established.
- This is not a single irreducible gap for the entire collision route:
  no reduction from arbitrary larger degrees to degree 15 is proved.
- Exact scripts, proofs and certificates are in astra8. No conductor lifting,
  coefficient sweep, counterexample, or full-route closure is claimed.

## September 5 first live systems resolved — latest update

[Astra 7](ASTRA_7_LIVE_SYSTEMS_CLOSED.md) proves **BOTH LIVE SYSTEMS CLOSED**:
the complete (4,10) and (6,8) coordinate v-degree systems are impossible,
with arbitrary coefficient degrees in c.

- (4,10) reduces to a cubic first-integral relation and a Jacobian with a
  forced vanishing factor at c=0.
- (6,8) reduces to four algebraic first integrals. Exact pole comparisons
  and a resultant force a final Jacobian expression to vanish at c=0.
- Both leading roots, rho=2/3 and rho=4/3, and the whole non-even-trace
  root component are covered. No division by an unknown function occurs
  in the (6,8) proof.
- Combined with Astra 6, no admissible potential has v-degree at most 14.
  The next unexcluded range is potential v-degree 15, coordinate degrees
  (6,9), up to exchange and the existing target reductions.
- The full collision subalgebra and JC2 remain open. Written proofs and
  exact certificates are in astra7; they are not externally reviewed or
  machine-formalized. No conductor lifting or coefficient sweep was run.

## September 5 global polynomial-potential strike — latest update

[Astra 6](ASTRA_6_GLOBAL_POTENTIAL_STRIKE.md) continues the global problem
without further conductor-adic lifting. Verdict: **OPEN**.

- The potential test is necessary and sufficient: admissible H, its actual
  gcd g in B, and (H_c+v)g_v-H_v g_c=g. The mate's membership is automatic.
- Written global arguments exclude every potential of v-degree at most 13,
  with no bound on c-degree. This is not a full subalgebra obstruction.
- The first remaining degree range is 14, with coordinate degrees (4,10)
  and (6,8). Both exact rational coefficient systems are retained.
- In (6,8), the two possible highest common roots are v(cv-2/3) and
  v(cv-4/3). The first must not be discarded by division in a residue test.
- Any (6,8) candidate must have a quadratic approximate root with non-even
  rational trace. The even-root branch, including denominators away from
  c=0, is excluded by an exact half-integer valuation obstruction.
- Exact verification scripts and expanded residual equations are in astra6.
  The new written proofs are not externally reviewed or formally mechanized.

## September 5 conductor strike — latest update

[Astra 5](ASTRA_5_CONDUCTOR_STRIKE.md) resolves the formal correction problem
and supersedes any recommendation to use increasing conductor order as a
candidate discriminator.

- Every immersed even Laurent trace has formal Keller extensions to all
  orders. The complete recurrence retains its free kernels.
- The old first-jet trace pair fails the global residue 4/3 condition and is
  excluded with arbitrary polynomial normal corrections.
- An explicit family passes every finite conductor order and the corrected
  trace period, but its formal limit cannot be polynomial. Separate residues
  at infinity detect the global failure.
- The C[c,cv] and C[v,cv] component families are excluded from counterexamples
  in all degrees. Stronger mixed-weight bounds are proved in the new report.
- The remaining conductor attack is global: the exact polynomial-potential
  gcd/closedness gate, or the necessary hyperbola factorization. The whole
  subalgebra remains open; no polynomial counterexample was obtained.

## September 5 audit update

[Astra 4](ASTRA_4_MISSED_ROUTES.md) supersedes the affected search priorities
below. The September 4 record remains the frozen historical base.

- A written all-degree proof excludes the full monic y-height (4,6) family,
  including arbitrary x-degrees and initial coefficients. Exact algebra passes.
- Rational mates and generic regular primitives are equivalent by whole-fibre
  denominator clearing, including reducible fibres. Night21's contrary claim
  is corrected; polynomiality remains the torsion-versus-zero question.
- Target-code fixed-sheet counts require an additional justification before
  they can universally be called staying counts. A marked re-screen leaves
  no survivor among 39 retained complete signatures, but does not cover all
  archived representations or repair the entire target implementation.
- H3 remains topologically excluded even with the new marking relaxation.
  Its deeper source-tree search is removed from the counterexample priorities.
- The x=1 subalgebra has an exact conductor/parity presentation. Low-degree
  ambient projections are already excluded; arbitrary-degree polynomial
  Keller pairs in that subalgebra remain a restricted construction question.
- Astra 2 and Astra 3 independent certificate verifiers were replayed and pass.

The new written proofs have not been externally reviewed or formalized.

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
  escaping-curve Euler equation in `OFF_BY_ONE.md`, using actual staying and
  escaping counts. Failure of either equation excludes that marked blueprint
  before curve realization. The historical fixed=staying implementation has
  the additional hypothesis identified by Astra 4.

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
   three, then kill its elliptic de Rham component exactly. It must escape
   Astra 10's arbitrary-degree templates; exactness alone is insufficient,
   as the new faithful-chart obstruction demonstrates.
2. Complete the upper-boundary reconstruction and nongraded compatibility
   for Astra 11's corrected published degree-(108,144) case. Retain its
   17 leading solutions and two terminal shapes; avoid the excluded row slice.
   Both Proposition 4.3 polygons are now closed by separate proofs.

## LIVE TOPOLOGICAL LANES

1. Add source intersection data to each group-first record at generation time,
   using the bridge equations rather than post-processing curve realizations.
2. Enumerate peripheral braid factorizations only for group records satisfying
   both Euler budgets and source complementarity.
3. Resolve the fixed/staying-sheet distinction before claiming a complete
   target census; use longitude-consistent marks and local boundary incidence
   unless a Keller-specific theorem removes the distinction.

## ATTACK ROUTING AFTER ASTRA 9

1. **Global collision-subalgebra construction — CLOSED.** Astra 9's arbitrary-
   degree parity and infinity-residue theorem excludes the entire algebra.
   No further coefficient systems or conductor lifts are a live CE target here.
2. **Residue-free construction outside Astra 10.** Multiple pole locations
   or a different pencil may escape the proved families. An exact primitive
   must still admit a faithful polynomial chart, and cannot violate the new
   mixed-power rigidity theorem. No explicit survivor is currently known.
3. **Corrected above-125 target.** Astra 11 derives the lower corner and
   catches the lost upper support for `(8,28)->(7/4,3)`, `(m,n)=(3,4)`.
   Prove the reduced upper boundary and handle the remaining coefficient
   rows. The completed (2,3) pentagon descent does not transfer to this ratio.

## DO-NOT-REPEAT LIST

- Do not use the old `(4,3)->(4,4)` base as the full degree-144 case.
  The displayed transformation retains `(4,8)`. Do not equate the 17
  leading solutions with global candidates, or silently discard nongraded
  rows after the simple-root obstruction.
- Do not increase m or alter A inside p^m*u+s*A(p), or increase k in
  Astra 10's varying hyperelliptic pencil, to seek a mate. The all-degree
  proofs cover those choices. Do not resurrect its exact degree-six twist
  by changing a birational plane chart; the mixed-power obstruction is
  chart-independent. The stated exceptional hypotheses remain explicit.
- Do not reopen C[b,c]+Delta*C[v,c] in higher degrees. The full obstruction
  is now in astra9/FULL_COLLISION_OBSTRUCTION.md; a concrete flaw in that
  proof would be needed to reopen the lane.
- Do not count arbitrary-order conductor jets, even with the correct trace
  residue and both displayed coordinates varying, as evidence of polynomial
  termination. The explicit Astra 5 control passes those tests and never
  polynomializes.
- Do not resume monic y-height (4,6) shooting; the all-degree obstruction now
  includes its formerly omitted charts and parameters.
- Do not pursue deeper source trees as a rescue of the already excluded H3
  class. A different group/curve/marking class needs its own budgets.
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
