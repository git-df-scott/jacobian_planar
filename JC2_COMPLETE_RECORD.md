# JC2 — complete Claude, Codex/Sol and Astra campaign record

**Updated September 5, 2026, through Astra 13. No explicit planar Jacobian
counterexample has been produced. The general conjecture remains unresolved.**

This is the mass report: the September 4 campaign synthesis, followed by the
complete September 5 continuation, corrections, exact results, failed
attempts, and stopping point. All Astra 4–13 reports, scripts, and saved
certificates are included on this branch. Start with sections 15–20 for the
latest work; sections 1–14 preserve the earlier campaign and its evidence.

The strongest collision result is the arbitrary-degree obstruction in
[Astra 9](ASTRA_9_FULL_COLLISION_ROUTE_CLOSURE.md): the specified collision
subalgebra contains no polynomial pair with nonzero constant Jacobian.
It supersedes the OPEN collision verdicts in Astra 5–8. It does not close
other approaches to JC2.

Outside that algebra, [Astra 11](ASTRA_11_CORRECTED_DEGREE144.md) repairs a
lost-support error and classifies 17 marked leading solutions for the
separate degree-(108,144) case. [Astra 12](ASTRA_12_GLOBAL_DIFFERENTIAL_DESCENT.md)
forces one entire next row to vanish and reduces the following row to one
scalar for the rational leading solution. That scalar survives the next
necessary test; no finite Keller pair has been reconstructed.

[Astra 13](ASTRA_13_SHIFTED_CHART_CONSTRUCTION.md) gives a written additional-
root argument excluding twelve of the seventeen marked leading solutions,
under the recorded standard-pair assumptions. It also restores a possible
extra fractional shift. Astra 12's p11=0 statement is valid in its stated
direct terminal chart; the expanded necessary system permits a nonzero p11.
Exact coupled row families survive, but no full Keller pair has been obtained.

**Archive boundary:** the frozen inventory in section 1 has cutoff
September 4, Astra 3 commit `64e925e320afb74f1dcf285fee0803d6a6c2b659`,
plus the two recovered local commits. Its counts have not been relabeled
as September 5 totals. The separate [continuation inventory](record/CONTINUATION_INDEX.md)
catalogs the subsequent reports and exact artifacts. “Complete” means the
preserved repository work and recorded explorations, not a reconstruction
of unavailable conversations or an independent audit of every old proof.

Repository: [git-df-scott/jacobian_planar](https://github.com/git-df-scott/jacobian_planar).

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

## 13. September 4 frontier — historical, superseded where noted

The table records the September 4 stopping point. Astra 4 closes the monic
height-(4,6) lane, Astra 9 closes the prescribed collision algebra, and
Astra 11–12 revise the above-125 lane. See section 18 for current status.

| Lane | September 4 boundary |
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

The September 4 scoped algebraic results replay from this branch with Python and
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

## 15. September 5 — missed routes through collision-route closure

### Astra 4: audit and all-degree monic height obstruction

[Astra 4](ASTRA_4_MISSED_ROUTES.md) revisited missed routes without treating
bounded coefficient searches as complete. The [monic height-(4,6) proof](astra4/RIBBON46_ALL_DEGREES.md)
excludes that class with unrestricted degree in the other variable and
retains the required kernel charts. The [localization audit](astra4/LOCALIZATION_AND_CONDUCTOR.md)
corrects the alleged rational-mate obstruction: a regular primitive on the
generic fibre must be handled by clearing whole-fibre denominators, rather
than by the earlier unsupported localization assertion. It also identifies
the collision algebra by its conductor and parity condition.

The [target-marking audit](astra4/TARGET_MARKING_AUDIT.md) separates a fixed
sheet from the stronger absence of boundary marking, gives an explicit
non-Keller control, and rescreens marked Euler data. The H3 obstruction
survives the stated relaxation. This does not turn a finite boundary-tree
census into a theorem about all larger source configurations.

### Astra 5: formal compatibility is not termination

[Astra 5](ASTRA_5_CONDUCTOR_STRIKE.md) proves an all-order formal correction
criterion in terms of trace derivatives generating the unit ideal in the
Laurent ring. The old trace fails an exact residue comparison: `-8/3`
versus the required `4/3`. More significantly, an explicit deceptive family
passes arbitrary finite conductor orders but its limit obeys
`c(Q+v)^2=1`, which is impossible in the rational function field by the odd
valuation at `c`. A target shear makes both coordinates vary without
removing that obstruction.

The [termination report](astra5/CONDUCTOR_TERMINATION.md) also closes the
stated unrestricted families with a component in `C[c,cv]` and introduces
a global potential gate. Formal lifting was thereby retired as a route to
polynomial existence. Its apparent success remains a negative control,
not evidence toward a counterexample.

### Astra 6: an exact global potential criterion

Write `r=3cv-2`, `Delta=r^2-9c`, `b=-3cv^2+4v+2`, and
`B=C[b,c]+Delta*C[v,c]`. For a polynomial potential `H`, set

\[
A_H=H_v,\quad C_H=H_c+v,\quad
 g=\gcd(A_H,C_H),\quad X_H=C_H\partial_v-A_H\partial_c.
\]

The [global theorem](astra6/GLOBAL_POTENTIAL_THEOREM.md) gives the exact
criterion, with its normalizations and nonzero-gcd convention:

\[
H+\tfrac23r\in B,\qquad g\in B,\qquad X_H(g)=g.
\]

These conditions reconstruct `P=g` and a polynomial `Q` from the closed
form `(H_v/g)dv+((H_c+v)/g)dc`; the trace condition places `Q` in `B`.
The reverse implication supplies necessity. [Astra 6](ASTRA_6_GLOBAL_POTENTIAL_STRIKE.md)
excludes potential degree in `v` at most 13 with unrestricted `c` degree,
and extracts the first residual systems `(4,10)` and `(6,8)`. Ordinary
polynomial Keller controls pass the ambient global test; collision
membership is a separate restriction. The nonterminating family fails
globally, as required.

### Astra 7: both live degree-14 systems closed

[Astra 7](ASTRA_7_LIVE_SYSTEMS_CLOSED.md) closes both complete systems,
including their exceptional coefficient choices and both leading
alternatives. For [(4,10)](astra7/OBSTRUCTION_410.md), first integrals yield
`y^2+64Z^3+AZ=B` and
`kappa=u(10yZ'+15Zy')/16`, with `y=u^2/h`. Valuations at a simple zero of
`h` force regularity and then `kappa=0`.

For [(6,8)](astra7/OBSTRUCTION_68.md), four first integrals and the
antisymmetry under the square-root field involution reduce the possible
poles. The exact resultant `-73728 A0^3 B0^9`, together with the handled
degenerate cases, gives the remaining contradiction. This involution must
not be confused with collision parity. Thus all admissible potentials of
`v` degree at most 14 are excluded. These were structural arguments, not
finite sweeps in the unrestricted coefficient variable.

### Astra 8: noncube degree-15 obstruction and genuine resonance

[Astra 8](ASTRA_8_DEGREE15_STRIKE.md) attacks `(6,9)`. The noncube leading
case is eliminated by four first integrals, pole orders, and an exact
exceptional-case resultant `567/32768` with a Bezout certificate. The
[leading-coefficient invariant](astra8/LEADING_COEFFICIENT_INVARIANT.md)
also gives the stated arbitrary-degree necessary condition: a nonconstant
leading root must be a power of one linear factor, with exponent at least
two in the normalized setting.

The resonant collision branch survives that argument. Its normalized six
fractional-power constants and all polynomiality/parity conditions are
preserved in the [exact system](astra8/RESONANT_69_SYSTEM.md) and its JSON
output. Astra 8 did not prove this system irreducible or reduce the full
route to it. Its OPEN verdict was accurate at that stage and is superseded
by the next theorem.

### Astra 9: the entire prescribed collision algebra is excluded

[Astra 9](ASTRA_9_FULL_COLLISION_ROUTE_CLOSURE.md) gives an arbitrary-degree
obstruction for

\[
a=-cv^3+v^2+v,\qquad
B=\mathbb C[a,b,c]=\mathbb C[b,c]+\Delta\mathbb C[v,c].
\]

On `Delta=0`, use `c=r^2/9`, `v=3(r+2)/r^2`. Membership in `B` is even
Laurent trace in `r`. If a component has positive mixed weight for
`wt(v)=1, wt(c)=-1`, parity forces a nonmonomial leading expression
`v^d L(vc)` with a nonzero root `lambda`. The resulting branch at infinity
of a generic fibre gives a nonzero residue `kappa*e*lambda` for `v dc`.
That contradicts the exact differential supplied by a polynomial Keller
mate. The proof connects this argument to the published prohibition on
the corresponding Newton edge. If both components have nonpositive mixed
weight, both lie in `C[c,cv]`, and their Jacobian is divisible by `c`.

The [full proof](astra9/FULL_COLLISION_OBSTRUCTION.md),
[proof audit](astra9/PROOF_AUDIT.md), and exact certificate cover these
alternatives. The closure includes the earlier resonant degree-15 system
and every higher degree in this particular algebra. It does **not** prove
the planar Jacobian conjecture. It is a written mathematical proof with
supporting exact checks, not an externally reviewed or machine-formalized
resolution of the campaign.

## 16. September 5 — work outside the closed collision algebra

### Astra 10: larger mateless families and a deceptive exact primitive

[Astra 10](ASTRA_10_OUTSIDE_COLLISION_SEARCH.md) investigates constructions
outside `B`. With `s=xy+1`, `p=xs+1`, `u=s^2+y`, it excludes polynomial
mates for every `P=p^m u+s A(p)`, `m>=1`, with arbitrary polynomial `A`.
The proof handles both the positive-genus differential case and the
exceptional residue/gradient cases.

A second theorem excludes the stated rational primitives on the varying
hyperelliptic pencil `w^2=D0(p)+4t p(p-1)`, for `deg D0>=3`, pole location
`a!=0,1`, and order `k>=1`. Odd-degree pole orders and, in the even case,
the incompatibility of the resulting isotrivial cover with varying branch
data provide the obstruction. Its hypotheses are essential; this is not
a theorem that positive genus alone prevents exact meromorphic forms.

A third rigidity theorem says that, for a polynomial Keller pair,
`P^m Q^n=f(r)` with rational `r` forces `r` polynomial and `f` a translated
pure power, whose degree divides `gcd(m,n)` in the stated setting. This
rejects an otherwise exact degree-six elliptic construction:

\[
D_*(z)=\frac{z^4-2z^3+3z^2-4z+5}{5},\quad
W^2=tD_*(z),\quad Q=\frac{(z+1)W}{3tz^3},
\]
\[
dQ=-\frac{dz}{z^4W},\qquad
tQ^2=\frac{r^6}{9}+\frac{2r^5}{15}+\frac1{45},\quad r=z^{-1}.
\]

Thus an exact curve primitive can exist and still admit no faithful
polynomial-plane Keller realization. The [proofs](astra10/PROOFS.md) and
[search audit](astra10/SEARCH_AND_AUDIT.md) preserve the construction,
its rejection, sources, and limitations. No counterexample resulted.

### Astra 11: support repair, 17 leading solutions, scoped extension closure

[Astra 11](ASTRA_11_CORRECTED_DEGREE144.md) audits the distinct published
above-125 ratio-(3,4) case. The old `trackD_chain_map.py` used terminal
height plus one to produce `(4,4)`, while its stated transformations take
`(8,28)` through `(28,8)` to `(4,8)`. No extra map justifying the smaller
support was supplied. Therefore the old small coefficient system did not
exhaust the published case. This correction does not invalidate Astra 2–3,
which address the separate ratio-(2,3) proposition.

The corrected leading root is `S=X h(XY^4)`, with
`h(T)=(T-1)^3 B(T)`, `B` a monic quartic and `B(0)B(1)!=0`.
The exact identity

\[
4Thf'+(h-3Th')f=h,\qquad \deg f\le5
\]

reduces to seven quadratic equations in seven variables. The saved
[lexicographic elimination](astra11/leading_lex.txt) classifies 17 marked
normalized leading solutions, with eliminant factor degrees `1,2,4,4,6`.
These are leading solutions, not 17 full counterexample components.
The rational solution has `B=(1+(T-1)^5)/T` and gives the transformed
leading root `c(y)=y^3(1+y^5)`.

Both normalized terminal alternatives are solved exactly in the fractional
chart. Their polynomial expressions after adjoining a fourth root have
Jacobian proportional to `t^3`, not a nonzero constant, so they are not
plane Keller maps. A separate simple-root theorem excludes the joint
slice with `P` rows `2,7,12` and `Q` rows `1,6,11,16` for all 17 leading
solutions. The full support, including the missing rows, remains open.

## 17. Astra 12 — current work, complete stopping point

The [full Astra 12 report](ASTRA_12_GLOBAL_DIFFERENTIAL_DESCENT.md) attacks
the rational leading solution without assuming the old reduced support.
Use the exact birational chart

\[
X=x^4(y+1),\qquad Y=x^{-1},\qquad J(X,Y)=x^2.
\]

All finite Laurent rows are retained. A row `x^k p_k(y)` descends to an
original polynomial precisely when `p_k` is divisible by
`(y+1)^max(0,ceil(k/4))`; the original rectangle imposes the additional
explicit degree bounds in the report. The terminal corner gives
`4k-5j<=3` for `P` and `<=4` for `Q`.

Let `h=1+y^5`, `c=y^3h`, and write
`P=c^3 x^12+sum p_k x^k`, `Q=c^4 x^16+sum q_k x^k`.
A finite mate with `J(P,Q)=kappa*x^2` forces global rational primitives
on `w^4=c(y)`. These are necessary conditions on complete algebraic
curves, extracted from the inverse expansion of `P^(1/12)`; they are
not a return to conductor jets or a claim of polynomial termination.

The entire first row satisfies

\[
\boxed{p_{11}=0.}
\]

High-coefficient polynomiality gives `p11=y^9h^2 a`, `deg a<=4`.
On `z^2=y+y^6`, exactness is equivalent to the complete finite identity
`2(y+y^6)B'-(1+6y^5)B=2a`, `deg B<=3`.
It forces `p11=lambda*y^12h^2`, whose order two at `y=-1` contradicts
the required order three unless `lambda=0`.

The next row is completely reduced to

\[
\boxed{p_{10}=\tau y^8(1+y^5)^2(3+5y^2+8y^5).}
\]

Local radical certificates first force `h^2|p10` and `h|p9`.
On `V^4=1+u^5`, with `u=1/y`, the relevant primitive is
`4*tau*(u^2-1)/V`. Its classification follows from
`4(1+u^5)B'-5u^4 B=4u^6a(1/u)`, `deg B<=2`, followed by original-plane
descent at `y=-1`. The nonzero scalar can be normalized to one; both zero
and nonzero branches remain possible at this stage.

A direct attempt to eliminate the nonzero branch failed for an exact
reason. Set `E=3+5y^2+8y^5`. The admissible row

\[
p_8=\frac{11}{24}\tau^2 y^7(1+y^5)E^2
\]

makes the next forcing numerator `24c^3p8-11p10^2` identically zero.
This is a control against an incorrect exclusion, not a full solution.
The larger next meromorphic linear problem has 11 free parameters in the
saved exploratory calculation. Lower rows, including `p9`, are unresolved.
The other 16 marked leading solutions were not classified further.

Other work recorded in the report includes a bracket-divisibility rejection
of a restricted cubic/quartic polynomial-part ansatz, a cyclic projection
strengthening the old joint slice when `P` is already in that slice, and an
uncompleted attempt to use other multiple roots in the published corner
theorem. The required root-selection hypotheses were not established, so
no elimination is claimed from that attempt.

**Exact stopping point:** solve the complete finite Laurent coefficient
identity `J(P,Q)=kappa*x^2`, `kappa!=0`, with the original-plane descent,
endpoint conditions, and the two boxed row restrictions. No full solution,
full contradiction, irreducible global-component reduction, collision, or
noninvertibility certificate has been obtained. Work stopped for the user's
requested report consolidation, not because this remaining system was
shown impossible.

## 18. Current verdicts and governing corrections

| Object | Current status and scope |
|---|---|
| Planar Jacobian conjecture | Unresolved in this campaign; no counterexample |
| Prescribed algebra `C[b,c]+Delta*C[v,c]` | Closed in arbitrary degree by Astra 9's written proof and exact supporting checks |
| Formal conductor approximations | Can persist without rational or polynomial termination; retired as an existence argument |
| Original GGHV Proposition 4.3 ratio-(2,3) polygons | Both excluded in Astra 2–3's computer-assisted record |
| Separate above-125 ratio-(3,4) degree-(108,144) case | Open; old smaller support is insufficient |
| Its corrected leading system | 17 marked normalized solutions classified; full extensions not classified |
| Rational leading solution, full Laurent support | `p11=0`, `p10` is the displayed one-parameter row; lower equations open |
| Briançon and hyperelliptic templates of Astra 10 | Closed only under the stated family hypotheses |
| Other historical geometric and corrected support frontiers | No blanket closure; retain their specific evidence limits |

The [correction ledger](RECORD_CORRECTIONS.md) governs contradictory old
claims. A historical OPEN collision verdict is superseded by Astra 9;
a historical reduced-support exclusion does not transfer to a larger
published support; and an exact rational primitive, fractional-chart
bracket, leading root, or surviving row is not a polynomial Keller pair.
There is no claim that the entire JC2 problem has been reduced to one
irreducible component.

## 19. Reproduction, inventory, and what was actually verified

The [September 5 artifact index](record/CONTINUATION_INDEX.md) lists every
Astra 4–12 report, proof, script, saved certificate, and recorded exploration
with SHA-256 hashes. The [machine-readable manifest](record/CONTINUATION_FILES.json)
is reproducible with `python record/build_continuation.py`; its scope is
separate from the immutable September 4 inventory.

| Run | Principal exact replay entry point |
|---|---|
| Astra 4 | `python astra4/verify_missed_routes.py` |
| Astra 5 | `python astra5/verify_conductor_strike.py` |
| Astra 6 | `python astra6/verify_global_potential.py`; derivation scripts and root certificate in `astra6/` |
| Astra 7 | `python astra7/verify_410_obstruction.py`; `python astra7/verify_68_obstruction.py`; input/control verifier |
| Astra 8 | `python astra8/run_certificates.py`; resonance derivation in `astra8/` |
| Astra 9 | `python astra9/verify_full_obstruction.py` |
| Astra 10 | `python astra10/verify.py` |
| Astra 11 | `python astra11/verify.py` |
| Astra 12 | `python astra12/verify.py` |

Dependencies and optional certificate regeneration flags are documented
in the individual reports/scripts. Earlier PASS records are preserved;
this closeout does not claim to have rerun every historical computation.
Astra 12's seven verification groups were run successfully against its
saved certificate. They cover the chart and positive control, high
coefficient identities and radical certificates, inverse coefficients,
both global linear classifications and descent, and the surviving next
numerator control. The exploratory scripts are preserved separately and
are not promoted to full coefficient-system certificates.

The written valuation and pole-order arguments supply mathematical
completeness within their stated hypotheses. The scripts check the exact
algebra; they do not independently formalize every geometric step. No
external peer review or proof-assistant verification is claimed. This
report records both what was achieved and the precise limitations.

## 20. Astra 13 — five leading solutions, restored shift and coupled attempt

The [review](JC2_RETHINK_AND_COUNTEREXAMPLE_PLAN.md) was pushed first in
`9e764c064b374ba6f7e4e60b2c5e346e33ff20bb`. Applying the published corner
restrictions to every eligible multiple root excludes the additional
double/quadruple-root patterns: twelve of the seventeen marked leading
solutions. The rational solution and four conjugates with two triple roots
remain. This is a written scoped argument with exact supporting checks.

The [Astra 13 continuation](ASTRA_13_SHIFTED_CHART_CONSTRUCTION.md) identifies
a possible intermediate type-III normal (2,-1), requiring the fuller chart
`X=t^4, Y=t^(-1)+eta*t^(-2)+Z`. No proof that eta vanishes had been supplied.
For the rational root the widened first row is
`p11=mu*y^8*(1+y^5)^2*(3+5y^4+8y^5)`, with `eta=-mu/12`.
The complete next necessary row has one further scalar tau and recovers
Astra 12 when mu=0. The four algebraic leading solutions also survive
the corresponding first-two-row tests over their quartic coefficient field.

On the nonzero-mu rational branch, the coupled p9,p8 global primitive test
has 21 free parameters at fixed tau. Its easiest particular section fails
the next q9 polynomiality gate for every complex tau, with a saved Bezout
certificate. Retaining the parameters gives two 17-dimensional uniform
local slices and a 13-dimensional intersection, each surviving for all tau.
Mixed choices between local factors remain unclassified. These dimensions
belong to necessary row systems, not full Keller components.

The remaining lower rows, bottom boundary, finite polynomial reconstruction
and noninvertibility witness were not obtained. No counterexample resulted.
Reproduction, exact equations and scope are in the Astra 13 report; all new
code and certificates are in `astra13/`. The earlier frozen inventory counts
and Astra 4–12 continuation manifest retain their original cutoff.
