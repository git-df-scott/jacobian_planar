# JC2 — complete Claude, Codex/Sol and Astra campaign record

September 5 follow-up: [Astra 4 missed-routes audit](ASTRA_4_MISSED_ROUTES.md)
adds scoped proofs and corrections. The historical cutoff and inventory in
this document are unchanged.

Closed-record date: **2026-09-04**. Repository:
[git-df-scott/jacobian_planar](https://github.com/git-df-scott/jacobian_planar).
Research cutoff: Astra 3 commit
[`64e925e320af`](https://github.com/git-df-scott/jacobian_planar/commit/64e925e320afb74f1dcf285fee0803d6a6c2b659).
This closeout also recovers two previously unpublished Codex commits and
corrects the proposed model in the second of them.

**No explicit counterexample to the planar Jacobian conjecture has been
produced.** The strongest latest explicit-polygon result is the
computer-assisted characteristic-zero exclusion of both configurations in
GGHV Proposition 4.3. That closes the original case called `(8,28)` in that
proposition. It does not settle every JC2 degree configuration, the disputed
`(9,27)` reduction, or the different above-125 `(3,4)` chain.

## 1. What is preserved

This is a readable synthesis plus an exhaustive, reproducible repository
inventory. It covers the following frozen material:

| Material | Count | Complete record |
|---|---:|---|
| Remote branches | 44 | [Branch index](record/BRANCHES.md) |
| Commits reachable from those branches | 1,287 | [Chronology](record/CHRONOLOGY.md) |
| Additional recovered local commits | 2 | [Recovery manifest](record/RECOVERY.json), original patch and Git bundle |
| Total catalogued commits | 1,289 | [Full messages, parents, trees and changed paths](record/COMMITS.jsonl) |
| Pull requests | 26 | [Original descriptions and discussions](record/PULL_REQUESTS.md) |
| Retrieved PR discussion entries | 4 | [Normalized metadata](record/PR_DISCUSSIONS.json) |
| Branch/file occurrences | 35,078 | [Complete file catalog](record/FILES.jsonl) |
| Distinct path/blob records at branch heads | 10,062 | Same catalog, including modes, sizes and branch membership |
| Distinct file paths at branch heads | 9,952 | Same catalog |
| Distinct report path/blob versions | 581 | [Every report with a pinned source link](record/REPORT_INDEX.md) |

These counts deliberately deduplicate shared ancestry and identical file
versions. They are not counts of independent experiments or verified theorems.
The snapshot precedes the archival commit itself. Old and superseded files
remain available at immutable commit links; no contradictory histories have
been silently merged into one verdict.

“Complete” here means all fetched repository refs and their reachable history,
all PRs visible at the cutoff, and the two local commits recovered during
closeout. It does not mean every private conversation or lost inline run has
been reconstructed. No new full mathematical audit of all 1,289 commits is
claimed. Historical results below retain their original evidence limits;
the correction ledger governs conflicts.

## 2. Objective and evidence standard

The original target is an explicit pair `P,Q in C[x,y]`, preferably over Q,
with

\[
P_xQ_y-P_yQ_x=c\ne0
\]

and an independently established failure of polynomial invertibility. An
explicit collision of distinct points is one sufficient witness. No pair in
this record has passed both requirements.

The campaign also studies reduced Newton-polygon systems with bracket `x`
or `x^2`, formal deformations, monodromy representations, rational primitives
on curves, and boundary trees. A survivor of one of those systems is not
automatically an original plane Keller map. Reverse polynomiality, vertex
nonvanishing, support completeness and faithful function-field realization
are recurring missing steps.

| Evidence category | What it establishes |
|---|---|
| Exact characteristic-zero identity | The stated identity or contradiction over the specified field, subject to correctness of the target derivation |
| Written theorem plus checked algebra | A scoped mathematical argument; written completeness/geometry is not automatically machine-formalized |
| Finite-field certificate | The specified system over that finite field or its algebraic closure; no automatic characteristic-zero promotion |
| Bounded census | Only its explicit objects, degree range, supports, fields and resource limits |
| Numerical near-hit | A diagnostic until exact lifting and the original counterexample gate succeed |
| Timeout, OOM, parser error, missing executable | No mathematical verdict |
| Blueprint or necessary-condition survivor | A constraint-compatible abstract object, not an algebraic realization |

## 3. Claude's early campaign: sessions 1–18

The preserved [1,199-line session record](docs/history/sessions-01-18-status.md)
contains code, report text and references to inline executions. It is the
primary historical source for this phase; later repairs supersede some of its
theorem wording.

| Sessions | Work performed | Outcome and later qualification |
|---|---|---|
| 1 | Reverse-engineered a three-dimensional map: affine pencil in z, twisted-cubic direction field, determinant decomposition, generic and exceptional fibre computations | Supplied geometric motivation and controls. Numerical back-substitution there is not an exact planar counterexample certificate. |
| 2–4 | Low y-degree Keller equations, Wronskian reduction, explicit triangular normal forms, `(2,3)` and odd-degree cusp cascades, pinned-leading-coefficient sweeps | Derived scoped tame/mateless statements and exposed the first repeated-root and middle-coefficient obstructions. Broad extrapolations require the stated hypotheses. |
| 5–6 | Rational shifts, residue gates, pole growth under back-translation, binomial slices, first genuine middle-coefficient frontier | Developed the distinction between a rational/formal mate and a polynomial mate. |
| 7 | Reconstructed the First Framework degree-16 Belyi data over `Q(sqrt(-3))`, corrected coefficient transcription, derived a near-miss bracket identity | Exact near-miss and chart controls; its monomial Jacobian is not constant. |
| 8–11 | Built cross-chart support and pole conditions for the `(99,66)` framework, derived degree ledgers, constructed the Laurent-block cascade and divisibility ladder | Reduced a large realization problem to structured one-variable data. Linearization at a degenerate near-miss was recognized as insufficient. |
| 12–15 | Formal square-root reduction of the cube tower; boundary-rigidity and pole-fibre claims; parameter census and box-cap verification | The stored statements survive as history; the claimed polynomiality of rational R and some proof dependencies were later challenged. |
| 16–18 | First Framework endgame and initial emptiness claim | The original proof evaluated at a possible pole. Later waves repaired the realization obstruction rather than validating that evaluation. |

The enduring assets were explicit chart formulae, Belyi identities, Laurent
support constraints and the endgame operator. The original final proof text
must be read together with the later rational escape-hatch correction.

## 4. Second Framework, sessions 19–38, and proof repair

The work split across several branches; chronological session numbers alone
do not uniquely identify a source. The full descriptions are preserved in
[PRs #1–9](record/PULL_REQUESTS.md).

**Second Framework / D=23.** PR #1 records a degree-23 Belyi reconstruction
with an irreducible degree-15 eliminant and a separate degree-14 field for
the other Belyi component, exact passport checks, harmonicity corrections,
cross-epoch identities and a polynomial near-miss. Its original conditional
endgame language was subsequently revised. The actual files remain on
[`claude/d23-borisov-transfer-test-vpr3m6`](https://github.com/git-df-scott/jacobian_planar/tree/7296164f70765387952fc49ed385b1fff59d2533).

**The “mod-3 wall” was a valuation-multiplicity question.** PR #2 separates
the primitive boundary multiplicity from a coincident cusp exponent or chart
slope, derives a general leading-block identity and exhibits the rational
escape hatch. Its modular direct hunt produced a point satisfying the
displayed equations but losing required corner coefficients. That is a
degeneration, not a counterexample.

**The staged hunt and priority queue.** PRs #3–4 rebuilt targets, restored
the accidentally overwritten `tower_check`, compared Singular engines,
introduced saturated msolve exports and leaf-specific branch bookkeeping,
and corrected the dangerous caching of an empty factor list after a failed
factorization. PR #4 is the one merged PR among the 26 in the frozen snapshot;
the other historical work remains largely on separate branches.

**Sessions 19–38.** PR #5 records 28 certifiers, 292 checks and 36 decided
Gröbner cases as that run's own tallies. It reproduces two published
calibration relations and retracts Session 36's claim that the `(8,28)`
elimination relation was absent: the `F` valuation had been carried over
incorrectly, and the omitted level `j=5` contains the needed term. Restoring
it produced a reported degree-31, 102-term relation at two primes. This is
historical modular evidence, not by itself a characteristic-zero closure.

**Waves 0–3 and adjudication.** PRs #6–9 repeatedly tested the proof itself.
The statement that the rational endgame has no solution by evaluation at
`v=-1` was false: rational R may have a pole there. Later work solves the
operator and compares the forced pole order with realization demands.
Further corrections restore an omitted multiplicity epsilon, retract
exhaustiveness of a nine-chart list, and recognize that two alleged
independent closures shared an equivalent premise. The framework-family
obstruction is retained in the inherited record only with its corrected
realization hypotheses. None of this closes arbitrary JC2 maps.

The audits also caught hardcoded-true checks, tests that could not fail,
false “ABSENT” labels caused by incomplete fetches, and a mixed-sign theorem
whose hypothesis disappeared in a summary. All are indexed in
[RECORD_CORRECTIONS.md](RECORD_CORRECTIONS.md).

## 5. B=16, degree territory, resisters and the pentagon reconstruction

This phase occupies the canonical `wave5/`, `wave6/`, `ggv/`, support and
resister branches, chiefly PRs #9–14. The frozen
[Claude CATCHES ledger](https://github.com/git-df-scott/jacobian_planar/blob/b233c708e9b43c597f6f2fa2e82a9b04fb5dd55a/CATCHES.md)
has 2,073 lines and takes precedence over stale positive summaries.

**B=16.** The campaign transcribed the GGV system, reproduced small examples,
studied leading quadratics and resonances, split charts and seeds, and ran
both modular and exact eliminations. It subsequently found a load-bearing
row-3 error in the printed/transcribed equations. All verdicts based on that
system were void for B=16. Some corrected small cases were rerun, but the
documents disagree about how far restoration was completed. This closeout
does not select the largest claimed range or rerun the ladder. Corrected
`d=8`, resonant `d=12,27`, and unsaturated variants retain the exact scope
recorded in their own valid inputs and logs. A purported universal rank
criterion was exposed as a test that could not fail.

**Territory enumeration and above 125.** The record contains implementations
of chain/corner algorithms, comparisons with published tables, same-sign
weighted-homogeneous sweeps, symmetry slices, lift pipelines and above-bound
queues. Counts such as 474 cases through 300, 464 cases in a subrange, 429
compiler-blocked cases and 804 admissible degree pairs refer to different
enumerations and dates; they must not be added or treated as a single census.
The late audit identifies the unprinted final lower corner and an outdated
`c'` ladder as unresolved provenance assumptions. Exact monomial identities
remain exact for their generated strata without closing the paper's cases.

**Resister infrastructure.** PR #12 preserves regenerated inputs selected by
checksums, a planted control, engine versions, bridge limits, swap/OOM
investigation and every timeout/failure classification. Canon's global
deduplication found that 49 timeout records represented only 16 distinct
systems. This was a reduction of repeated work, not 33 new exclusions.

**Pentagon target repair.** PR #13 records exact factorization of a degree-nine
bottom eliminant into degrees `1+1+2+5`, distinguishing degenerate roots from
the admissible quintic orbit. Earlier guesses from prime counts had correctly
been retracted before the exact computation. It also derives a quotient
Jacobian identity for the C*-descent route and shows why the relevant
constant-Jacobian descent already requires a plane collision upstairs.

PR #14 proves the unsaturated `pent_L23.ms` core is inhabited by explicit
degenerate families in both charts. Examples include `P=x+f(y)` with bounded
degree and a separate `p_1_1!=0` family. This explains why attempts to prove
that core empty could never succeed. Missing saturation and a residual torus
were mathematical target errors, not merely slow solvers.

## 6. Earlier Codex/Sol work: exact levels and collision-first searches

The report index includes every `codex/*` branch, including those with no PR.
Git author names alone do not determine which model wrote a file; this
section follows the names and attribution in the branch reports.

| Workstream | Recorded contribution | Scope at the cutoff |
|---|---|---|
| Pentagon level 17 / PR #16 | Retained kernel constants, tame positive controls, explicit one-variable descent and a divisibility condition | Necessary conditions; no full pentagon realization |
| Level 16 | Replaced an overstrong divisibility claim with joint conditions and an explicit characteristic-zero surviving witness | Earlier quick kill retracted |
| Level 14 | Rational constant obstruction on one branch | Branch-specific exclusion |
| `pentagon-p11-zero-search` | Audited the residual torus and bottom-vertex transfer, investigated formal order-two gates and structured slices | Slice results do not exhaust the full polygon; Astra 3 later supplies a separate complete exclusion |
| Sol 3 all-five | Correct reverse Laurent lift, residual degree bound retaining omitted root strata, rigid two-edge jets, degree-144 diagnostics | Modular jet exclusions and an exact restricted inverse-lift contradiction; no full above-125 case closure |
| Sol 5 degree-144 lift | Continued polynomiality/collision checks on reduced hits | Reduced numerical hits fail the required reverse-lift gate |
| Sol 5 collision-first | Original Keller coefficient matrix with fixed collision values; exact all-x-degree closure of the height `(2,3)` ribbon | A scoped exact exclusion, independent of imposing a collision |
| Sol 5 height `(4,6)` | Reconstructed upper Q rows with integration constants; reduced to three remaining Jacobian identities | At the reported degree-126 triangle: 212 P coefficients plus seven constants, 504 equations; a construction target, not a solution |
| Sol 6 collision-first | Rational planted seed survives through `x^21` and dies at `x^22`; mapped the generic obstruction | A finite formal jet is not a polynomial counterexample |

The direct source reports include
[Sol 3](https://github.com/git-df-scott/jacobian_planar/blob/e43947e4cabc548961430dc05525736efd7e1277/SOL3_ALL_FIVE.md),
[Sol 5](https://github.com/git-df-scott/jacobian_planar/blob/1d814dd8b07016bd424b1e7c876ef4c8bf06f779/SOL5_COLLISION_FIRST.md),
and [Sol 6](https://github.com/git-df-scott/jacobian_planar/blob/fd113a59ab34c4be58942818dab61cc72c27e01a/SOL6_COLLISION_FIRST.md).

## 7. Claude/Fable's later sessions and the night1–26 programme

PR #17 consolidates direct bracket searches, period-based ideas, target-label
corrections and numerical vertex-collapse observations. Its omitted-kernel
and broad graded-EMPTY claims were later corrected. PR #18 introduces the
thin-polygon grading `rho=2i-j`, `T=xy^2`, its triangular one-variable equations,
the leading hyperelliptic exactness condition, modular orbit exclusions and
five exact positive witnesses. Astra's later proofs build on that instrument
while independently supplying the missing completeness and characteristic-zero
steps.

The later “Session 43” and “Session 44” reports are present on PRs #19 and
#20. They are different records from earlier work also called Plan 43.
Session 43 retracts its first unvalidated numbers and repairs twelve bugs,
including incorrect inclusion–exclusion at multiple intersections, counting
infinity points over Q instead of C, and modular-majority fibre decisions.
Session 44 builds obstruction hunters, exposes the `u=0` kernel stratum,
and develops group/topological sieves. A finite grid surviving or failing is
kept at its stated field and chart scope.

The night programme is preserved principally on the
[Fable branch](https://github.com/git-df-scott/jacobian_planar/tree/a105bc93e43b9766b90763b2c62ef9df26ddfc36)
and the later
[mate branch](https://github.com/git-df-scott/jacobian_planar/tree/df7471deb9207422b2a5f0b8661f3a7f05f7fee6).
Every listed directory's reports, scripts and results are in the file catalog.

| Night | Work and evidence retained |
|---|---|
| 1 | Calibrated deformation-depth engine over finite fields; Hamiltonian directions, degree caps, positive and overflow controls, independently expanded stored towers |
| 2 | Cross-checks, Sol's full night report, formal-tower and theoretical follow-up records |
| 3 | Original Keller-plus-collision systems with explicit supports and mandatory controls; modular solves and resource walls |
| 4 | Formal inverse-tail evaluator with known-answer and independent recomposition checks; GGHV extraction and tail notes |
| 5 | Restored campaign inputs, cascade/engine validation, Session 44 documents and source extracts; preserved retractions alongside recovered claims |
| 6 | Leading-face and E3 kernel measurements; rational/number-field integration checks; characteristic-zero projective/Bezout calculations on the stated systems; degree-(84,126) coverage and triage |
| 7 | Resultant-based nonproperness/“tear” evaluator, source interpretation and controls |
| 8 | Exact eight-point characteristic-two census for the stated support, fixed collision equations, star-point and lifting tests |
| 9 | Prime survey, altitude/last-term obstructions, complete local solution lists and interpolation audit |
| 10 | Ramified lifting ladders over rings with `pi^2=2` and `pi^3=2`, toy controls and bounded follow-up |
| 11 | Numerical search network and status ledger; misses remain numerical diagnostics |
| 12 | Mate searches and exact coefficient certificates; v1 records 243 attempted P across its arms and 20 exact mates, all on certified coordinate P |
| 13 | Fibre configurations, H-screen and prestratum searches |
| 14 | Non-coordinate, gradient-unimodular prospector: 140 candidates, 90 U-passers, 79 passing non-coordinates, with individual candidate records |
| 15 | Gelfand–Leray period screen: 256 generated P, 193 NONVANISHING, 57 VANISHING, three NOT_SCREENED and three UNRESOLVED; the table distinguishes exact and numerical instruments. Bounded exact mate attempts on the 57 survivors retain their certificates |
| 16 | Exact atypical-value re-screen of those 57; all special-fibre tests still vanish, while one survivor has a generic-fibre obstruction missed by the earlier fibre selection |
| 17 | Inverted residue search solving for P; genus-zero residues versus higher-genus de Rham obstruction kept separate |
| 18 | Symbolic family mate systems over rational function fields, kernel obstruction and chart coverage |
| 19 | All-degree mateless family `gamma*x*y^2+c*y`, rational-mate pole mechanism, transport under polynomial symplectic changes, exact finite-degree regression checks |
| 20 | Shift to gradient-unimodular, non-coordinate P with all fibres irreducible and generic positive genus |
| 21 | Rational-mate pole theorem, polynomialization under irreducible-fibre hypotheses, mixed-isobaric barrier |
| 22 | Explicit degree-ten Briançon profiles; bounded exact mate exclusions through degree 30, component-pole mismatch, and the distinction between pointwise periods and generic algebraic exactness |
| 23 | Briançon infinity charts and the holomorphic Gelfand–Leray obstruction; source for Astra's independent replay |
| 24 | Cusp-preserving family closure through elliptic de Rham and pole mismatch; positive controls and manifests |
| 25 — recovered | Two faithful degree-two primitive models excluded by the quadratic Galois obstruction; triangular quotient controls explicitly distinguished from faithful realizations |
| 26 — recovered | Prime-degree audit, genus-one degree-six primitive `t=r^2+2u^2r, R=r^3`, field/volume identities, toric and regular-chart obstructions; its GO recommendation is now superseded by the pure-power obstruction below |

This table records what each lane did, not an assertion that every historical
claim has been independently re-proved in this closeout. For example, a
pointwise period measurement does not automatically produce a global
polynomial primitive, and the generic leading-field calculations must not be
identified with the unrelated degree-1144 artifact without proof.

## 8. The final Claude handoffs, source/target work and organization

PR #22 assembled the unified hunt plan, target interpretation, audit gates,
bounded attempts and stop rules. It corrected a mismatch between the claimed
164-variable asset and the actual saturated export, removed a refuted
truncation strategy, and separated a certificate of containment from an
identity proving 1 belongs to an ideal.

PR #23 executed direct attempts. Its fast exact extractor, torus-chart
reducer and branching linear-chain eliminator yielded 25 exact monomial
certificates on generated strata; twelve lie above the previous bound.
The lower-corner and `c'` provenance problem prevents transferring those
twelve automatically to published cases. One `(9,27)` compiler stratum dies
at depth six, but it is not the paper's entire `(9,27)` polygon. Segfaults,
OOMs and timeouts remain explicit walls.

PR #24 traced clues across branches, recognized that the existing thin grading
was better suited to the quadrilateral than the proposed y-adic continuation,
found missing positive-control coverage, reconciled vertex degenerations,
and recorded the stale B=16 summaries. Its later target-side work enumerated
bounded curve/cover configurations using braid monodromy, group actions,
Euler conditions, staying and escaping sheets, dicritical constraints and
line tests. The A5-on-six-sheets near-miss and related A8 configurations
are abstract data; no polynomial realization resulted.

The source-side archive generated 11,465 boundary-tree records through six
blowups, originally with restrictive coordinate-horizontal choices. Astra 1
reused the exact tree list but replaced those choices with the complete
complementarity solve needed for H3. See the inherited
[target report](docs/plans/audit/vitushkin/RESULT_2026-09-04.md) and Astra's
scope correction below.

PR #25 repaired routing and the branch map. Its proposed entry-point fixes
were not merged at the cutoff, so `main` still carried stale text. PR #26 is
a closed, superseded mailbox prototype; the record preserves its status and
does not activate it. The older Codex/Claude mailbox branch is explicitly
marked **DO NOT MERGE**. This closeout sends no messages and merges no
historical research PRs.

## 9. Astra 1 — reconciliation, source/target bridges and controls

Commits
[`4f917d0`](https://github.com/git-df-scott/jacobian_planar/commit/4f917d0)
and [`9331941`](https://github.com/git-df-scott/jacobian_planar/commit/93319412545e84d1093d79c5b59cb87731eec4a9).
Full record: [ASTRA_RECONCILIATION.md](ASTRA_RECONCILIATION.md),
[ASTRA_RUN_LOG.md](ASTRA_RUN_LOG.md),
[TARGET_SOURCE_COMPATIBILITY.md](TARGET_SOURCE_COMPATIBILITY.md).

Astra first reconciled the target and field interpretations. It did not
accept conflicting historical characteristic-zero claims about the
quadrilateral; its status remained UNKNOWN until the next run. It stopped
the degree-144 compiler route at the unverified lower-corner gate.

The exact new bridge for a generic resolved dicritical component E is
`r_E=1-k_E`, with cycle counts `c_i=sum d_E`, escape counts
`e_i=sum d_E(1-k_E)`, and coordinate horizontal degrees determined by the
target parametrization and tangential degree. Adjunction gives

\[
\chi(P^{-1}(c))=\sum_E(k_E-1)d_E^P.
\]

After subtracting escape contributions, the remaining horizontal components
have weighted budget D, and similarly for Q. H3 requires a +6 budget in
each coordinate.

The H3-specific complementarity solve checked all 11,465 archived trees,
both tangential partitions, and target bidegrees `(3,5)` and `(3,6)` without
the inherited horizontal-degree/support cap. There were zero compatible
P-coordinate or Q-coordinate assignments. This is an exact **bounded**
exclusion through six blowups, not a theorem covering arbitrary boundary
depth.

Independent H3 enumeration found 45 double transpositions, 16 labelled
triples after fixing one generator, one conjugacy orbit and group order 60;
its Euler/escape deficit is exact. The abstract target screen reproduced
5,261 rows and 635 basic signatures, which remain shapes only. Identity-map
controls, five exact Poisson witnesses and the two Briançon gradient/period
checks passed. The full inherited GAP enumeration was not replayed here.

## 10. Astra 2 — exact quadrilateral exclusion

Research commit
[`1e05b08`](https://github.com/git-df-scott/jacobian_planar/commit/1e05b08a6a9ade28949d7c0be74548c36e569b45),
report commit
[`e479477`](https://github.com/git-df-scott/jacobian_planar/commit/e479477263c1f4176b287309dda2dcb4213fcb84).
Proof: [ASTRA_2_CASE2_EXACT_DESCENT.md](ASTRA_2_CASE2_EXACT_DESCENT.md).

Starting directly from Proposition 4.3(2), Astra reconstructed the complete
thin support and the five graded equations. The top equation is
`2CG'-3C'G=T^2`. Five explicit leading solutions live in an irreducible
quintic field after normalization.

The missing completeness argument came from a degree-21 Belyi passport.
Its dessins reduce to the five rooted plane full binary trees with three
internal vertices. Five constructed normalized solutions meet that upper
bound, so no leading orbit or `C_2=0` chart is missing. This does not rely on
the discovery solver's completeness wording.

A complete lower parametrization and exact rank calculation produce the
remaining equations. Twenty-six explicit multipliers, including saturation
of the required corner, sum to 1 over the quintic field. A separate FLINT
checker reconstructs the system and multiplies the identity; all four
verification groups and altered-certificate controls pass. The identity
survives all five embeddings, excluding the quadrilateral in characteristic
zero.

Direct leading Gröbner attempts and an auxiliary chart certificate lift timed
out. Their inputs and logs are preserved in
[case2_run_manifest.json](astra/artifacts/case2_run_manifest.json); none is
used as an emptiness proof. The older degree-1144 object's provenance remains
unresolved and is not needed.

## 11. Astra 3 — pentagon and projective boundary

Commit
[`64e925e`](https://github.com/git-df-scott/jacobian_planar/commit/64e925e320afb74f1dcf285fee0803d6a6c2b659).
Proof: [ASTRA_3_PENTAGON_PROJECTIVE.md](ASTRA_3_PENTAGON_PROJECTIVE.md).

The complete support has 60 P and 124 Q nonconstant monomials, including
negative grading levels. The highest-x edge forces a square/cube relation;
an explicit residual scaling normalizes its nonzero parameter. Every kernel
in the linear descent is retained. The necessary prefix reduces to five
parameters of weights `(1,2,3,3,4)`.

Three direct characteristic-zero eliminations timed out. A smaller quintic
field and scaling were constructed and checked exactly, but the successful
argument took a different route: restore the edge parameter t, producing a
weighted homogeneous system of weights `(1,2,3,3,4,1)`.

At `p=32003`, nine equations in the `t=1` chart have an explicit unit
certificate. At `t=0`, fourteen equations have certificates for
`u1^9,u2^5,u3^3,u4^2,u5^3`. Thus the entire projective special fibre is empty.
The checker reconstructs both charts from one system, multiplies all six
identities and verifies good reduction of every exact coefficient operator.

The written valuation argument rescales any hypothetical characteristic-zero
point to an integral projective point with a nonzero reduction, contradicting
those certificates. With Astra 2's leading completeness, this excludes the
pentagon. This is **not** an inference from affine modular emptiness alone.

All four verification groups pass. The complete record, including parser
failures and compressed exact inputs from the timed-out runs, is in
[pentagon_run_manifest.json](astra/artifacts/pentagon_run_manifest.json).
The published tree was checked against the clean local tree. Neither Astra
proof claims literature priority, external peer review or formalization in
a proof assistant.

## 12. Closeout recovery and the new night26 correction

Two completed Codex commits were found outside the remote history:
`5a0592b31d127a6b9ea0d6050801dda96d6092c4` and
`b07d9e9153a926014af67ad1a892c944f00485b0`. Their twelve files are now restored
byte-for-byte under [night25/](night25/) and [night26/](night26/), with source
checksums, an original patch and a verified Git bundle. Another older
checkout's 89 existing changed-file contents were already present in remote
history; its missing working files were not treated as lost research.

The recovered night26 “GO” model has a short fatal obstruction. Faithfulness
puts r in `C(x,y)`, while polynomiality requires `Q=r^3` in `C[x,y]`.
Integral closure forces r itself to be polynomial. Then
`J(P,Q)=3r^2 J(P,r)` cannot be a nonzero constant. The intended model is
therefore impossible, even allowing arbitrary faithful rational plane
charts. Its old exact curve identities can still be correct; they did not
address this necessary condition. The original files are preserved unchanged,
with the full superseding proof in
[RECORD_CORRECTIONS.md](RECORD_CORRECTIONS.md).

## 13. What remains open and what should not be repeated

| Lane | Current boundary |
|---|---|
| Above-125 chain `(8,28)->(7/4,3)`, `(m,n)=(3,4)` | Derive the missing lower corner and correct c' range from primary definitions before solving. The matching `(8,28)` label does not transfer Astra's `(2,3)` proof. |
| Actual `(9,27)`/Corollary 5.7 issue | Resolve the disputed source step and complete support translation; do not substitute a smaller compiler stratum. |
| Corrected B=16 frontier | Reconcile exact corrected inputs and certificates before reopening cells. Old printed-system and cannot-fail-rank evidence are void. |
| H3 source geometry | Derive a forced boundary-depth/intersection obstruction or a realizable larger skeleton; six-blowup emptiness is bounded. |
| Positive-genus mate construction | Find a faithful polynomial-plane realization with exact Gelfand–Leray primitive; the two checked Briançon targets and recovered `R=r^3` model are closed. |
| Height `(4,6)` collision-first and kernel strata | Formal jets and finite grids are insufficient; retain all kernels and enforce the final polynomial degree boundaries. |

Do not restart either Proposition 4.3 polygon without a concrete defect in
Astra 2 or 3. Do not rescan generic coefficient boxes or requeue a timeout
under a new name. Do not promote an affine modular verdict, a collapsed
vertex, an ambient map, a quotient control, or a formal jet to a JC2 result.

## 14. Reproduction and navigation

The latest scoped algebraic results replay from this branch with Python and
python-flint 0.9.0:

```bash
python astra/verify_case2_certificate.py
python astra/verify_pentagon_projective.py
```

Each command prints four PASS lines. The mathematical completeness,
normalization and valuation arguments live in the accompanying proof files.
The additional exact small-field pentagon reconstruction uses
`python astra/verify_pentagon_descent.py --constraints-only`; its default
direct-certificate mode expects a certificate that the timed-out route did
not produce.

For the complete history, use [record/README.md](record/README.md), then the
[branch index](record/BRANCHES.md), [commit chronology](record/CHRONOLOGY.md),
[report index](record/REPORT_INDEX.md) and [PR archive](record/PULL_REQUESTS.md).
The machine-readable catalog preserves the exact path, object and branch
mapping for every file occurrence. The archive's integrity checks are in
[INVENTORY_VERIFICATION.json](record/INVENTORY_VERIFICATION.json).

This closeout preserves the work and makes its evidence reviewable. It does
not claim that the counterexample objective has been achieved.
# September 5 continuation: global potential strike

The frozen September 4 archive is followed by
`ASTRA_6_GLOBAL_POTENTIAL_STRIKE.md`, with exact scripts and certificates in
`astra6/`. Its verdict is OPEN; the new obstructions and two surviving
degree-14 systems are distinguished explicitly from the historical record.
