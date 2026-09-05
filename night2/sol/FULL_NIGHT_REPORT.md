# JC2 separator pivot — full-night report

## Bottom line

The escape implication is logically valid **only after** a characteristic-zero
universal vanishing proof for the separator.  Finite-field interpolation, rank
saturation, and held-out samples do not provide that proof.  This run produced
one exact small-degree separator and a controlled modular grid, but no separator
at degree 125 and no counterexample candidate.

**Current answer: no, the pivot does not yet possess a usable degree-125 escape
certificate.**  It possesses a sound certificate format and a verified `d=3`
demonstration of that format.

## 1. Certificate logic

**VERDICT: UNCLEAR as proposed; SOUND with exact symbolic certification.**

For a characteristic-zero polynomial `h`, the implication

\[
[P,Q]=1,\quad h(P,Q)\ne 0,\quad
h|_{\operatorname{Aut}_{\le d}(\mathbf C)}=0
\Longrightarrow (P,Q)\notin\operatorname{Aut}_{\le d}
\]

is elementary and noncircular.  It never assumes `Aut_d=K_d`.  The third
hypothesis is the entire burden.

An honest certificate must contain:

1. a fixed coefficient/feature ordering and normalized modular vectors;
2. CRT and rational reconstruction with a proved height bound, or an exact
   rational nullspace computation;
3. a proved complete family of dominant rational charts for all required
   automorphism strata;
4. exact substitution `h o phi_s`, denominator clearing, and coefficientwise
   zero over `Q` on every chart;
5. the density/closure argument extending chart identities to `Aut_d`;
6. exact evaluation `h(candidate) != 0` in original coordinates.

Vanishing on samples can leak through finite-field polynomial identities,
special-fiber rank drops, bad characteristic, missing orientations or affine
factors, and nondominant sampling distributions.  The pipeline controls detect
several engineering failures but do not replace item 4.

There is also a component-coverage trap: Furter's description of the components
of the degree-at-most-`m` variety is **Conjecture 7.3 in general**, proved there
only for `m <= 27`.  Thus the component claim is safe for this run (`d <= 10`),
not for `d=125`.  [Furter 2009, Conjecture 7.3 and Proposition
7.2](https://www.math.u-bordeaux.fr/~jpfurter/planePolynomialAutomorphismsOfFixedMultidegree.pdf).

## 2. Count prediction audit

With `N=(d+1)(d+2)`, the full affine degree-at-most-two feature space has

\[
M=\binom{N+2}{2}.
\]

Furter's dimension `dim Aut_d^Jac=1=d+5` does **not** determine the quadratic
Hilbert function.  The exact count is `M-H_Aut(2)`.  The table's “prediction” is
therefore only the deliberately naive benchmark obtained by replacing `Aut_d`
with a generic affine `(d+5)`-plane.  It was frozen before computation.

| d | N | M | generic-plane benchmark | known Keller quadrics |
|---:|---:|---:|---:|---:|
| 3 | 20 | 231 | 186 | 15 |
| 4 | 30 | 496 | 441 | 28 |
| 5 | 42 | 946 | 880 | 45 |
| 6 | 56 | 1,653 | 1,575 | 66 |
| 7 | 72 | 2,701 | 2,610 | 91 |
| 8 | 90 | 4,186 | 4,081 | 120 |
| 9 | 110 | 6,216 | 6,096 | 153 |
| 10 | 132 | 8,911 | 8,775 | 190 |

Every measured count is expected to mismatch this benchmark because a nonlinear,
reducible variety is not a generic affine plane.  Such mismatch is not a pipeline
error.  Treating it as an independent predicted count would be mathematically
false.

## 3–4. Pipeline and modular run

`separator_pipeline.py` implements finite-field bivariate polynomial arithmetic,
full alternating affine-triangular tame sampling, quadratic feature evaluation,
incremental modular row reduction, nullspace extraction, and held-out tests using
only the standard library and NumPy.

The first sampler version was rejected during the run: it fixed too many affine
parameters, sampled a proper subfamily, and created spurious coefficient
relations.  All its counts were withdrawn.  The shipped implementation uses
general affine factors, general exact-degree triangular factors, nontriangular
interior affine factors, and chooses the last determinant to make the Jacobian
one.

The controls mean precisely:

- `S1`: each generated map has Jacobian exactly one modulo `p`;
- `S2`: every proven maximal polydegree label for `d<=10` is sampled;
- `I1`: the observed rank is unchanged for three further batches;
- `I2`: every computed nullspace vector vanishes on fresh sampler outputs;
- `I3`: every nullspace vector is nonzero on at least one random ambient vector.

`S2` is coverage of labels plus the standard alternating factorization chart; it
is not a machine proof of chart dominance.  All numeric results remain explicitly
**MODULAR-EMPIRICAL**.

The definitive table is `separator_counts.csv`.  Cross-prime equality is a strong
control against accidental bad-prime rank loss, but not a characteristic-zero
certificate.

| d | samples/prime | rank at both primes | modular nullity | generic benchmark | mismatch |
|---:|---:|---:|---:|---:|:---:|
| 3 | 384 | 174 | 57 | 186 | **YES** |
| 4 | 768 | 395 | 101 | 441 | **YES** |
| 5 | 1,024 | 588 | 358 | 880 | **YES** |
| 6 | 1,920 | 1,228 | 425 | 1,575 | **YES** |
| 7 | 2,560 | 1,558 | 1,143 | 2,610 | **YES** |
| 8 | 4,224 | 2,976 | 1,210 | 4,081 | **YES** |
| 9 | 5,632 | 3,918 | 2,298 | 6,096 | **YES** |
| 10 | 8,320 | 5,998 | 2,913 | 8,775 | **YES** |

Every mismatch is flagged, but none is evidence of a defect because the benchmark
was explicitly derived from a false generic-plane model.  The valuable empirical
cross-check is instead the exact equality of ranks across the two primes.

## 5. One separator certified end-to-end

At `d=3`, write `P_2=p20*x^2+p11*x*y+p02*y^2` and similarly for `Q_2`.
The shipped certificate is

\[
h=p20q11-p11q20.
\]

The independent checker derives

\[
[x^2]\,[P_2,Q_2]=2h.
\]

Furter's Proposition 8 says that for length-at-most-one plane automorphisms,
`Jac(P_i,Q_j)=0` for every `i,j>=2`; every degree-at-most-three automorphism has
length at most one.  Hence `h` vanishes on `Aut_{<=3}(C)`.  The script checks the
two modular residues, held-out samples, ambient nontriviality, and that `h` is not
in the linear span of the universal Jacobian coefficient equations.

Primary source: [Furter 1997, Proposition
8](https://www.math.u-bordeaux.fr/~jpfurter/onTheVarietyOfAutomorphismsOfTheAffinePlane.pdf).

This is a proof-of-protocol separator, not a degree-125 escape tool.  No candidate
was produced: `CANDIDATE-UNVERIFIED: none`.

## 6. Scaling wall and published equations

At `d=125`, `N=16,002` and `M=128,056,006`; dense quadratic interpolation is
already disqualified.  Ranked alternatives:

1. **Bounded-inverse elimination.**  Introduce coefficients of a degree-at-most
   `d` inverse and eliminate them from both composition identities.  This is exact,
   sparse before elimination, and targets closedness directly.
2. **Reductive symmetry blocks.**  Decompose features under source/target tori and
   `SL_2`; handle translations afterward through their locally nilpotent operators.
3. **Exact pullback on tame charts.**  Compute kernels blockwise in parameter
   rings instead of building the full sample-feature matrix.  Above `d=27`, use
   all polydegree strata rather than an unproved component list.
4. **Complete Newton/collision charts.**  Restrict supports only through proved
   necessary conditions and retain all boundary charts.
5. **Per-stratum work.**  Useful for calculation, unsafe as a global certificate
   unless ideals are intersected (or component relations combined correctly).
6. **Invariant coordinates.**  Limited by translations and by loss of orbit
   separation; covariants are more plausible than a tiny invariant quotient.
7. **Assumed sparsity/low rank.**  Unsupported; elimination can densify equations.

Published explicit equations do exist in restricted settings.  Furter Proposition
8 supplies length-one equations; Proposition 12 supplies an equation on the
degree-four component `W_(2,2)` and explicitly exhibits an automorphism in the
other component violating it.  Thus Proposition 12 is a component control, not a
global separator. [Furter 1997, Propositions 8 and
12](https://www.math.u-bordeaux.fr/~jpfurter/onTheVarietyOfAutomorphismsOfTheAffinePlane.pdf).

Kambayashi builds the pro-affine/ind-affine framework and warns that the relevant
inverse-limit reduction map need not be surjective; it does not print usable
finite-degree global generators. [Kambayashi 2003, Introduction and Theorem
1.3.1](https://ir.library.osaka-u.ac.jp/repo/ouka/all/8490/1578ojm.pdf).

No primary source located in this review supplies a non-Keller global separator
for `Aut_{<=125}`.  Closedness is existence, not a tractable formula.

## 7. Honest escape design

1. Normalize a collision by affine changes on a finite union of nonzero-minor
   charts; retain algebraic collision-point variables when rationality is absent.
2. Intersect with the complete, checker-backed union of all proved admissible
   degree/Newton cases.  The campaign's number `804` is not accepted without its
   enumerator and theorem-to-code coverage proof.
3. Impose escape algebraically by `z*h-1=0`, not by maximizing `|h|`, which is
   scale-dependent.
4. Use deformation families only as labeled nonexhaustive probes unless their
   union is proved to cover the normalized cases.
5. Put symmetric ansatzes last: no theorem says a counterexample can be made
   symmetric by the permitted group actions.

Any escape below degree 125 is a negative-control failure, not a discovery.

## Recommended order for the next joint session

1. Re-run the shipped grid and certificate checker verbatim.
2. Independently verify the full affine-triangular sampler is dominant on each
   `d<=10` stratum and audit the component enumerator against Furter.
3. Compute the quotient of modular quadrics by the full Keller-quadrics span,
   block by symmetry weight, rather than comparing raw nullities.
4. Reproduce the `d=3` exact separator by a second symbolic pullback path.
5. Prototype bounded-inverse elimination at `d=3,4` and compare its radical
   degree-two piece with the interpolation output.
6. Only after these agree, design a degree-125 sparse/block computation.

**Strongest remaining objection:** no theorem or experiment here shows that a
computable low-degree polynomial exists in `I(Aut_{<=125})` but outside the
radical of the Keller equations; without such an `h`, the escape search has no
gate to optimize.
