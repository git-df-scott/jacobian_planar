# Round 2: certified separators for bounded plane automorphisms

## Task 1 — certificate logic

### Verdict: UNCLEAR as proposed; SOUND after exact symbolic certification

The implication used at the final gate is valid:

\[
[P,Q]=1,\quad h(P,Q)\ne0,\quad h|_{\operatorname{Aut}_d}=0
\quad\Longrightarrow\quad (P,Q)\notin\operatorname{Aut}_d.
\]

There is no appeal to `Aut_d=K_d` here. The entire burden is proving the universal
vanishing statement over characteristic zero.

### Exact certification protocol

Let `c` be the `N(d)=(d+1)(d+2)` coefficient variables of a polynomial pair of degree
at most `d`.

1. **Discovery only.** Compute modular nullspaces at several primes. Fix a canonical monomial
   order and normalize every vector by a specified pivot coefficient. Match pivots/supports across
   primes. A relation seen at two primes remains only `MODULAR-INTERPOLATED`.
2. **Lift.** CRT the matched coefficients and perform rational reconstruction. This is unique only
   with a proved numerator/denominator height bound and modulus exceeding twice the relevant bound.
   Without such a bound, add primes but keep the status conjectural. Alternatively, solve the
   resulting exact rational linear system directly; this avoids an unjustified reconstruction claim.
3. **Enumerate the required automorphism strata.** For every polydegree sequence whose product is
   at most `d`, use the Jung–van der Kulk/Furter alternating affine–triangular factorization. For
   exact degree `m`, Furter proves that fixed-polydegree loci are the irreducible components. For
   degree at most `d`, do **not** silently identify all maximal polydegrees with components in
   general: Furter's general component statement is a conjecture, proved in that paper only through
   `d=27`. Sampling every stratum is safe; declaring component completeness above 27 is not.
4. **Use dominant universal charts, not samples.** For each stratum `s`, define an exact rational
   parameterization `phi_s`. Include every affine/triangular parameter needed for a dense image and
   record the open-chart product `Delta_s` (nonzero determinants and leading coefficients). Substitute
   the lifted `h` into the coefficient functions of `phi_s`.
5. **Identity check.** Clear denominators and verify

   \[
   \Delta_s^{e_s}(h\circ\phi_s)=0
   \]

   coefficientwise in `Q[parameters]`. Equivalently prove `h` lies in the kernel of the pullback map
   to the localized parameter ring, or provide a Gröbner normal-form certificate in the saturated
   chart ideal. The checker must independently expand the composition and compare every coefficient.
6. **Closure step.** Because the chart image is dense in its irreducible stratum closure and `h` is
   polynomial, the identity extends to that closure. Repeat over all strata (or over a proved complete
   list of component-dense charts). This yields `h|Aut_d=0` over `C`.
7. **Candidate gate.** Evaluate `h` exactly on the original-coordinate rational/number-field candidate,
   obtain a nonzero exact value, and separately run the full Keller/collision/nonmembership protocol.

Steps 4–6, not CRT, turn an interpolant into a certificate. If symbolic substitution is too large,
one may certify by elimination from bounded inverse equations, but a probabilistic identity test is
not a proof.

### What modular sampling can leak

- `F_p`-points are not Zariski dense in an affine parameter space over `F_p-bar`; `z^p-z` is the
  standard false identity on all base-field samples.
- Even when the candidate feature degree is two in coefficient variables, its pullback through a
  tame composition can have parameter degree at least `p`, invalidating a naive full-grid argument.
- Special fibers can acquire extra relations, components, inseparability, or rank drops. Furter's
  characteristic-zero closure arguments explicitly use divisions by polydegrees, so primes dividing
  those integers are bad.
- Random samples may remain in a proper subfamily because affine factors, orientations, leading
  coefficients, or degeneration charts were omitted.
- Rank saturation and held-out samples measure stability of the chosen distribution; they do not
  prove density or universal vanishing.
- Sampling each *labelled* polydegree does not prove that the sampler is dominant on that stratum.

### Citations/checkable statements

Furter records that the Jacobian-one degree-bounded automorphism locus is closed and states that
`J_{2,n}=G_{2,n}` is exactly the degree-`n` Jacobian conjecture:
[Furter 1997, pp. 14–18](https://www.math.u-bordeaux.fr/~jpfurter/onTheVarietyOfAutomorphismsOfTheAffinePlane.pdf).

Furter proves fixed-polydegree strata smooth and locally closed, exact-degree components indexed by
polydegrees of product `m`, but presents the degree-`<=m` component description as Conjecture 7.3 and
proves it only for `m<=27`:
[Furter 2009, Theorems A–C and §7.3](https://www.math.u-bordeaux.fr/~jpfurter/planePolynomialAutomorphismsOfFixedMultidegree.pdf).

## Task 2 — degree-<=2 separator counts frozen before computation

Let the ambient affine coefficient space have dimension

\[
N(d)=2\binom{d+2}{2}=(d+1)(d+2).
\]

The vector space of coefficient polynomials of total degree at most two has dimension

\[
M(d)=\binom{N(d)+2}{2}.
\]

For the Jacobian-one automorphism locus, the maximum component dimension is `m=d+5` for `d>=2`.
**Dimension does not determine the number of quadratic relations.** The exact number is

\[
q_d=M(d)-H_{\operatorname{Aut}_d}(2),
\]

where `H_X(2)` is the affine Hilbert function: the rank of restriction of degree-`<=2`
coefficient polynomials to `X`. Varieties of the same dimension can have different `H(2)`, and a
reducible union generally has a larger restriction space than any one component. Consequently no
honest numerical prediction follows from Furter's dimension formulas alone.

The requested dimension-only number can only be supplied as a **generic affine-plane benchmark**:
pretend the entire locus were one generic affine `m`-plane, so `H(2)=binom(m+2,2)`. This is not a
prediction for `Aut_d` and a mismatch does not diagnose either pipeline.

| d | N(d) | M(d) | m=d+5 | generic-plane H(2) | benchmark separators | known Jacobian coefficient quadrics |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 20 | 231 | 8 | 45 | 186 | 15 |
| 4 | 30 | 496 | 9 | 55 | 441 | 28 |
| 5 | 42 | 946 | 10 | 66 | 880 | 45 |
| 6 | 56 | 1,653 | 11 | 78 | 1,575 | 66 |
| 7 | 72 | 2,701 | 12 | 91 | 2,610 | 91 |
| 8 | 90 | 4,186 | 13 | 105 | 4,081 | 120 |
| 9 | 110 | 6,216 | 14 | 120 | 6,096 | 153 |
| 10 | 132 | 8,911 | 15 | 136 | 8,775 | 190 |

The last column is `d(2d-1)`, the number of coefficient equations in
`[P,Q]-1=0`, whose output degree is at most `2d-2`. These are explicit degree-`<=2` polynomials
vanishing on `Aut_d`, but they vanish on **all** of `K_d` and therefore can never certify escape.
The useful measured quantity is not total nullity; it is

\[
\dim\bigl(I(\operatorname{Aut}_d)_{\le2}/I(K_d)_{\le2}\bigr).
\]

This quotient cannot be predicted from dimension. It may be zero.

## Task 3 — scaling wall at d=125

At `d=125`, `N=126*127=16,002` and

\[
M=\binom{16004}{2}=128,056,006.
\]

A dense sample-by-feature matrix is therefore disqualified before algebra begins.

### Ranked reductions

1. **Eliminate a bounded inverse, using sparsity and block structure — highest plausibility.**
   In the plane, an automorphism of degree at most `d` has inverse of degree at most `d`.
   Introduce inverse coefficients `z` and impose `G(F)=id` and `F(G)=id`. These equations are
   linear in `z` when `F` is fixed and sparse by monomial support. Eliminate `z` from the universal
   composition ideal. Closedness ensures the elimination variety is `Aut_d`; radicalization may
   still be required for the reduced ideal. This replaces blind `1.3e8`-feature interpolation by
   structured sparse composition matrices, rank conditions, and selected minors. It is exact but
   may still be huge.

2. **Reductive symmetry decomposition — high mathematical value, medium implementation risk.**
   `Aut_d` is stable under left and right composition by determinant-one affine automorphisms.
   The linear `SL_2`/torus parts act on coefficient space, hence the quadratic feature space splits
   into weight spaces and `SL_2` isotypic blocks. Kernel computations can be performed blockwise.
   Translations are non-reductive and mix homogeneous degrees, so first split under source/target
   tori and linear groups; impose translation stability afterward with locally nilpotent Lie
   operators. Campaign `mu`-actions are useful only when the target family is proved stable under
   them. This reduction preserves the ideal because it uses actual group actions.

3. **Symbolic pullback on dense tame charts — medium/high plausibility for certification, lower for
   discovery.** Furter's precise decomposition gives explicit affine–triangular parameter maps.
   Instead of evaluating all quadratic features, compute the kernel of the pullback map one weight
   block at a time. This proves universal vanishing directly. The obstacle is the number of strata
   and parameter-monomial explosion. For `d>27`, component closure incidence is not fully classified
   in Furter 2009, so use every polydegree stratum of product `<=d`, not an asserted component list.

4. **Newton/degree-pair support restriction plus collision normalization — medium plausibility and
   directly relevant to escape search.** Necessary support theorems and affine normalization of a
   collision can shrink coefficient space before evaluating a separator. This is honest only as a
   union over every proved admissible chart, including exceptional and boundary charts.

5. **Per-stratum separators — useful locally, dangerous globally.** A polynomial in
   `I(overline{G_delta})` need not vanish on another automorphism component. Products of one
   separator per component vanish globally but multiply degrees; intersections of stratum ideals
   are the correct operation. Per-stratum work accelerates pullback verification but cannot by
   itself certify global escape.

6. **Invariant coordinates — low plausibility as a complete reduction.** The large affine action
   has few useful low-degree scalar invariants; translations destroy most naive homogeneous
   invariants. Relative invariants/covariants and highest-weight coordinates are more realistic than
   passing to a small invariant quotient, which can identify automorphisms with non-automorphisms.

7. **Assumed sparsity or numerical low rank — speculative.** The known Jacobian relations are sparse,
   but elimination can create dense high-degree polynomials. Low rank observed at small `d` is not a
   theorem and cannot justify a degree-125 certificate.

Checker for the feature count:

```python
from math import comb
assert (126*127, comb(126*127+2,2)) == (16002, 128056006)
```

## Task 4 — known explicit separators

### Published objects found

1. **Universal but useless:** the coefficient equations of `[P,Q]-1=0` are explicit quadrics
   vanishing on `Aut_d`. They vanish on all Keller pairs and cannot separate a Keller candidate.

2. **Furter's length-one equations:** if `P_i,Q_i` are homogeneous pieces of an automorphism,
   Furter Proposition 8 proves that length at most one is equivalent to
   `Jac(P_i,Q_j)=0` for all `i,j>=2`, equivalently the nonlinear parts are linearly dependent.
   These are explicit coefficient equations for the length-one closed subvariety, not for all
   `Aut_d`.

3. **Furter's degree-four component equation:** Proposition 12 proves every element of the closure
   `W_(2,2)` satisfies

   \[
   \operatorname{Jac}(P_2P_3-2P_1P_4,\;Q_2Q_3-2Q_1Q_4)=0.
   \]

   This separates that component from some elements of `W_(4)`, so it emphatically does **not**
   vanish on global `Aut_4`. It is a valuable control for a per-stratum interpolator, not an escape
   certificate.

Source and checker-by-substitution instructions are in
[Furter 1997, Propositions 8 and 12](https://www.math.u-bordeaux.fr/~jpfurter/onTheVarietyOfAutomorphismsOfTheAffinePlane.pdf).

4. **A global small-degree separator:** for `d=3`, Proposition 8 gives
   `h=p20*q11-p11*q20`, since `2h` is the `x^2` coefficient of `Jac(P_2,Q_2)` and every
   degree-at-most-three automorphism has length at most one.  The exact checker is
   `certify_separator_d3.py`.  This proves the protocol at small degree but supplies no equation
   for `d=125`.

### What was not found

No located Furter, Kambayashi, or Wright source prints a non-Jacobian polynomial in the global
ideal `I(Aut_125)` that is known not to vanish on `K_125`. Kambayashi constructs the ind/pro-affine
framework rather than usable finite-degree coefficient generators. Bass–Connell–Wright/Furter
closedness proves that a finite generating set exists, but existence is not an explicit separator.

There is nevertheless a completely explicit **algorithmic source**: eliminate degree-`<=d` inverse
coefficients from the two composition identities. This skips sampling but not elimination. Any
reported generator must ship with its elimination/Gröbner certificate and an exact test showing it
is not already in the radical of the Keller equations.

## Task 5 — honest escape-search family

### Ranked design

1. **Collision-first, union over all proved Newton/degree charts.** Any noninjective Keller map has
   two distinct points `a,b` with equal image. Over the coefficient field containing those points,
   affine source and target changes normalize

   \[
   a=(0,0),\quad b=(1,0),\quad F(a)=F(b)=(0,0).
   \]

   Impose these incidence equations together with `[P,Q]=1`, then intersect with every necessary
   degree-pair/Newton chart supplied by the proved GGHV-type classification. This preserves every
   counterexample only if the union is complete and all exceptional charts are retained. If a
   rational-coefficient counterexample has non-rational collision points, the normalized map may
   live over a number field; the exporter must allow algebraic point variables rather than silently
   demand rational collisions.

2. **Use affine symmetry only as a proved gauge.** Translations and determinant-one linear changes
   preserve the Keller condition and invertibility. Normalize constants, selected linear terms,
   and the collision pair on explicit nonzero minors, with separate charts for every vanishing
   pivot. This removes genuine redundancy without assuming special symmetry.

3. **Apply the separator as an inequation, not an objective.** Add `z*h(c)-1=0` (or the relevant
   number-field norm inequation) to the exact system. Maximizing `|h|` is scale-dependent and
   numerically meaningless unless a compact normalization is imposed. Saturation by `h` is the
   algebraically honest escape test.

4. **Deformation families only after a separator is built into the equations.** A deformation
   chart is acceptable if its parameterization is proved to contain a complete collision/Newton
   chart or is explicitly labeled a non-exhaustive probe. Formal depth alone remains irrelevant.

5. **Symmetric ansatz last.** No general theorem says a JC2 counterexample can be made symmetric,
   equivariant, or sparse by affine conjugacy. Such ansätze are exploratory subfamilies and cannot
   close or represent the full search.

The campaign-supplied count of `804` admissible degree-pair/shape cases must be accompanied by its
enumerator and a theorem-to-code coverage checker before it can serve as a complete union. The
number itself is not used here as an independently verified theorem.

## Round-2 conclusion

**Does the pivoted strategy have a valid escape certificate now? No.** It has a logically valid
certificate *format*, but no explicit non-Jacobian `h in I(Aut_d)` has yet been produced and
certified over `Q`.

**Strongest remaining objection:** degree-two interpolation will automatically rediscover the
Jacobian equations, while neither dimension nor finite-field sampling gives any reason that a
quadratic relation exists which vanishes on all bounded automorphisms but not on all Keller maps.
