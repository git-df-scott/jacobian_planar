# Search record and proof audit

This run follows Astra 9, after the full prescribed collision subalgebra was
closed. It does not regard finite conductor compatibility as evidence, and
does not revisit degrees 15, 16, or higher in that algebra.

## Primary-source search

- [Dimca–Sticlaru, *Minimal plus-one generated curves and Briançon-type
  polynomials*, arXiv:2406.19795v1, Section 4](https://arxiv.org/html/2406.19795v1#S4) supplies the higher-degree
  Briançon template. This prompted the arbitrary-exponent calculation in
  Theorem 1. The paper's curve and freeness results are not assertions that
  these polynomials have Keller mates.
- [Bustinduy–Giraldo–Muciño-Raymundo, *Jacobian mates for non-singular
  polynomial maps*, Journal of Singularities 9 (2014)](https://www.journalofsing.org/volume9/bustiunduy-giraldo-mucino-raymundo.pdf)
  distinguishes exact time forms and the role of irreducible fibres in
  global polynomial integration. Its rational-mate examples reinforce the
  need to check polynomial realization separately. We do not infer a
  polynomial mate merely from zero residues.
- [Sijsling–Voight, *On computing Belyi maps*, 2014](https://www.numdam.org/item/10.5802/pmb.5.pdf), introduction, gives the
  correspondence between three-point covers and permutation triples.
  Only its fixed-degree finiteness consequence is used in Theorem 2;
  the argument is also supplied in the proof.
- [Poonen, *Computational aspects of curves of genus at least 2*](https://math.mit.edu/~poonen/papers/ants2.pdf) was consulted for the
  standard smooth-model conventions for hyperelliptic curves. Infinity
  orders used here are explicitly derived from local parameters.

Searches for hyperelliptic Jacobian mates were noisy, often confusing
Jacobians of curves with the Jacobian conjecture. Search results claiming
proofs or higher-dimensional counterexamples were not treated as planar
certificates. The previously used three-dimensional derivation was not
reused to assert a two-dimensional Keller condition.

## Mathematical audit

1. **Full function field.** The rational chart (s,p) has an explicit inverse;
   the hyperelliptic models are birational to the generic fibres. No cover
   is replaced by a quotient while claiming faithfulness.
2. **Generic squarefreeness.** Both arguments prove it over C(t), for all
   coefficient choices in their stated scopes. A single good specialization
   is not used as a substitute for this proof.
3. **Exceptional parameters.** Theorem 1 treats A(0)=0 separately. Its
   singular-gradient case excludes polynomial mates only. Theorem 2 excludes
   a=0,1 explicitly and requires deg D0>=3. Its polynomial corollary imposes
   the exact divisibility condition at p=1.
4. **Poles of a primitive.** Pole orders of dQ are exactly one more than
   those of Q in characteristic zero. There are no additional finite poles
   available to cancel periods. The odd-degree and even-degree infinity
   cases are both covered.
5. **Isotriviality step.** Finite degree implies finitely many monodromy
   triples, not that every curve has no Belyi map. Normalization of branch
   values is allowed after specialization. The cross-ratio argument concerns
   the source curves' isomorphism classes, so changing the primitive or a
   target scaling does not evade it.
6. **Exact control.** The isotrivial degree-six twist is accepted by the
   differential test. Its failure occurs only at faithful polynomial
   realization. This prevents overclaiming that all positive-genus exact
   primitives are impossible.
7. **All birational charts.** The mixed-power obstruction uses integral
   closure in C[x,y] and a differential identity, so it applies to any chart
   where the proposed P,Q are polynomial and the field identification is
   faithful. A finite quotient is not a faithful chart.
8. **No global JC2 reduction.** Multiple pole locations, other pencil
   coefficients, different primitive identities, and the universal
   two-point collision problem are not covered. No irreducibility claim is
   made for their combined unresolved parameter space.

## Verification limits

The verifier checks nine groups of exact identities and controls, including
the complete k=4 quartic residual equations and an explicit degree-six
primitive. Theorems 1–3 use additional written arguments about compact
curves, covers, and integral closure. The script is not a proof assistant;
these new written arguments have not received external peer review.

No numerical search, finite-order lifting, modular exclusion, or generic
degree sweep was performed in this run. The resulting verdict is OPEN,
with new scoped obstructions and no counterexample.
