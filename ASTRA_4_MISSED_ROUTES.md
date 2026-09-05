# Astra 4 — missed routes and exact repairs

September 5, 2026. Audited base:
[`efff2dc5c31a71030ccf931d22b9cd2047c0e172`](https://github.com/git-df-scott/jacobian_planar/commit/efff2dc5c31a71030ccf931d22b9cd2047c0e172),
the head of `astra/jc2-complete-record-2026-09-04` when checked.
Work branch: `astra/jc2-missed-routes-2026-09-05`.

I found a false localization assertion, a missing justification in the
target-cover screen, an exact simplification of the collision subalgebra,
and an all-degree obstruction for a family that had remained live. None of
the pairs examined has both a nonzero constant Jacobian and a verified
failure of invertibility. This is a research audit with new scoped proofs,
not a resolution of the planar Jacobian conjecture.

## 1. The findings that change the search

| Finding | Evidence | Consequence |
|---|---|---|
| Full monic y-height (4,6) family is impossible, with arbitrary x-degrees | Three exact algebraic integrals plus an exhaustive leading-degree proof | Stop all shooting in that family, including omitted initial-value charts |
| Rational mate and generic regular primitive were incorrectly distinguished in night21 | General whole-fibre denominator-clearing proof; explicit counteridentity | Replace that false obstruction with the correct torsion-versus-zero question |
| The target code counts every fixed sheet as staying | Direct code inspection; exact non-Keller geometric control; marked Euler formulas | Universal exclusions need an extra Keller theorem or explicit boundary marks |
| The x=1 collision subalgebra has an exact conductor/parity description | Exact normalization identities and C* restriction calculation | Replace redundant target projections by a complete two-variable membership condition |
| Cubic x=1 target projections were already below known degree bounds | Degree of each restricted generator is at most four | The purported first cubic frontier is closed without a solve |
| H3 is already topologically excluded, including the new marking relaxation | Its marked Euler equation forces the old marking | Greater H3 source-tree depth cannot rescue the same group/curve class |

The detailed proofs and their limitations are in
[RIBBON46_ALL_DEGREES.md](astra4/RIBBON46_ALL_DEGREES.md),
[LOCALIZATION_AND_CONDUCTOR.md](astra4/LOCALIZATION_AND_CONDUCTOR.md), and
[TARGET_MARKING_AUDIT.md](astra4/TARGET_MARKING_AUDIT.md).

## 2. The complete height-(4,6) obstruction

Suppose P,Q have y-degrees 4,6 and constant nonzero leading y coefficients.
After scaling and a polynomial symplectic shear,

\[
P=(Y^2+a(x)/2)^2+b(x)Y+d(x).
\]

I derived the upper Q coefficients directly from the original bracket,
retaining all six constants of integration. The lower equations have three
polynomial integrals H2,H1,H0 satisfying

\[
\{P,Q\}=H_2'(Y^2+a/4)+H_1'Y+H_0'.
\]

Thus the entire family requires H2,H1 constant and H0 affine linear with
nonzero slope. Comparing degrees in a,b,d exhausts the constants in the
integrals and rules this out. In the three nondegenerate cases the possible
degree of H0 is respectively at least 16,12,8; the final degenerate case
reduces H0 to a cube or a constant. The proof includes a constant a.

This addresses the real omissions in the old bounded searches: it frees p0,
keeps all initial coefficients, places no x-degree cutoff, and imposes no
fixed collision. It does not cover nonconstant leading y coefficients or
general JC2 pairs. No novelty priority or external peer review is claimed.

Historical inputs are the branch-head versions of
`session43/lane7/SOL5_COLLISION_FIRST.md`,
`session43/lane6/SOL6_COLLISION_FIRST.md`, and
`session43/lane6/lane6_report.md`, with respective Git blobs
`98a7d59d4d6e2e3b3f43118baf1b22c246b7f2a9`,
`98f920efde9a3c22e991fdd5158f30b9471ace45`, and
`ff8bf96474625a5c5046072c4a0f219bfd89696c`. Their location across refs is
recorded in `record/FILES.jsonl`; no missing file in the current checkout
was interpreted as missing historical work.

## 3. A concrete remaining polynomial construction problem

The strongest new explicit formulation comes from the x=1 subalgebra. Put

\[
a=-cv^3+v^2+v,\quad b=-3cv^2+4v+2,\quad
\Delta=(3cv-2)^2-9c.
\]

Then B=C[a,b,c] is precisely the set of f in C[v,c] whose restriction
to Delta=0 is even in the C* parameter r=3cv-2. Equivalently, every member
has the form `F(b,c)+Delta U(v,c)`.

Every P,Q in B identifies the distinct points `(-1/3,4)` and `(2/3,4)`.
Therefore the equation

\[
\{F(b,c)+\Delta U,\ G(b,c)+\Delta V\}_{v,c}=1
\]

is a direct counterexample construction problem with its collision already
built in. This presentation is complete for this particular subalgebra,
and its conductor is exactly Delta*C[v,c]. It does not parametrize every
possible JC2 counterexample.

There is an exact first normal jet satisfying the bracket modulo Delta.
Its full residual is nonzero, and its fixed degree-three Q cannot produce
a counterexample. It serves only to check that the first conductor jet
does not itself force impossibility. No finite polynomial termination was
obtained. The old cubic target projection suggestion was already excluded:
its resulting plane degrees are at most 12. Even target degree 26 is below
the published bound 108 for plane counterexamples, since 4*26=104.
See the cited [GGHV degree theorem](https://arxiv.org/abs/2204.14178).

## 4. The target gap does not resurrect the retained examples

The audited target code replaces staying counts by fixed-point counts
without encoding whether a fixed sheet might escape unramified. A general
polynomial A2 map can have that behavior; the report gives an exact example
and explicitly checks its nonconstant Jacobian. Whether a Keller-specific
theorem forbids it remains a missing justification in this audit. The cited
[Borisov framework paper](https://arxiv.org/html/1901.04073v2) only asserts
that at least one dicritical component is ramified.

I re-screened 163 complete printed Euler-stage rows from 21 retained logs,
which reduce to 39 distinct numerical signatures of degree at least six.
Allowing fixed-sheet escape gives one arithmetic survivor, the degree-six
cusp-plus-tangent-line S4 cover. It then fails a local node-incidence bound:
the required loss of two staying points exceeds the one marked branch's
capacity. Zero remain within that stated coverage.

H3 itself is not reopened: its marked Euler equation is `3u+s=1`, forcing
u=0,s=1 and the same chi(R)=0 contradiction. The September 4 recommendation
to rank deeper H3 source trees first is therefore stale for that class.

The gap still matters for a universal census: rows filtered before Euler
data were printed, other targets, and full peripheral marking choices were
not enumerated by this check. The original GAP code is preserved as
historical code, not silently rewritten into a purported complete marked
enumerator.

## 5. What survived the audit

The independent Astra 2 and Astra 3 verifiers were replayed on this base.
Both produced their four PASS verdicts after using the existing FLINT
dependency directory. The initial import failure without that directory
was an environment issue, not mathematical evidence. No concrete flaw in
those two certified Proposition 4.3 exclusions was found here.

The following obstructions also remain intact:

- The two degree-ten Briançon targets have a nonzero holomorphic generic
  differential, so neither admits a rational mate. Correcting localization
  does not change that obstruction.
- The recovered model `t=r^2+2u^2r, R=r^3` cannot polynomialize faithfully as
  a Keller pair. The integral-closure obstruction extends to any R=H(t,r)
  monic in r of degree greater than one, with coefficients polynomial in t.
- A bracket x or x^2 in a reduced Newton system still needs a faithful
  polynomial reverse lift. None examined here provides one.
- The above-125 (108,144) chain's lower-corner and c' provenance gap remains
  unresolved. It has not been closed by certificates for a different ratio.

## 6. Reproduction and actual coverage

Run from the repository root:

```
python astra4/verify_missed_routes.py
python astra4/rescreen_marked_logs.py
```

The first independently checks the original bracket reduction, the three
integrals, sheared polynomial controls, leading noncancellation identities,
the localization control, conductor identities, collision, first jet and
boundary example. It produces four PASS groups in
[verification.json](astra4/verification.json). The second records log hashes
and the rejected marked candidate in
[marked_log_rescreen.json](astra4/marked_log_rescreen.json).

The all-degree exhaustiveness, normalization/membership, and geometric
incidence arguments are written mathematics, not machine-formalized proofs.
The tests check their exact algebra and the stated finite re-screen.

For the wider review I indexed and searched 750 distinct historical
report/text blobs, read the closeout synthesis and corrections, the current
Astra proofs/state, and the relevant older reports and implementations for
these routes. I did not independently read and reverify every line of all
1,289 catalogued commits, regenerate every historical search, or establish
that these are all remaining errors. The corrected claims here have explicit
identities or scoped arguments; a request to find everything cannot justify
claiming exhaustive mathematical coverage that was not achieved.

## 7. Revised frontier

The remaining explicit algebra is the high-degree conductor problem above
and the generic exactness/polynomialization problem for a new, appropriately
chosen gradient-unimodular P. The latter now has the correct equivalence
between rational and generic regular primitives; irreducible pole-bearing
fibres remove the remaining polynomialization obstruction.

The target route first needs its fixed/staying distinction resolved at the
theorem or marked-peripheral-data level. Existing unmarked global-exclusion
wording should not be used to discard a new marked candidate. The separate
above-125 route still needs derivation of its actual support before further
solver work.

There is no reason from this audit to repeat monic (4,6) shooting, low-degree
x=1 projections, the closed H3 class, or either certified Proposition 4.3
polygon without a specific new flaw. No explicit counterexample was found.
