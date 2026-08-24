# Sol 3: all-five counterexample sweep

Branch: `codex/sol3-all-five` from `e9a65be9be5fbb63fdc35f21ea29644bb412424f`.
The occupied `x=1` degree-3 route was deliberately excluded.

## Counterexample gate

A reduced pair satisfying `[P,Q]=x^2` is not a JC2 counterexample.  A hit must
survive the reverse Laurent chain, become two polynomials, have constant
nonzero original Jacobian, retain every required vertex, and then be shown
non-injective.  Nothing below passed that gate.  Modular hits, if any, are
labelled `CANDIDATE-UNVERIFIED`.

## 1. Correct `x^4 y` inverse-lift locus

`sol3/lift_x4.py` implements the actual final involution
`x -> x^-1, y -> x^4*y`, all three preceding Laurent shear slots, their exact
reverse, and the polynomiality matrix.  Controls recover a planted polynomial
exactly and map the five published pre-final vertices to the reduced pentagon.

Every zero/nonzero shear stratum and twelve generic points were run over
`F_2147483647`.

* On the required `lambda_4 != 0` chart, P has 61 coefficients, 12 independent
  negative-power cancellation conditions, and lift-nullity 49.  Q has 125
  coefficients (including its additive constant), 24 independent conditions,
  and lift-nullity 101.  Every polygon vertex remains live.
* On `lambda_4=0`, some strata force a required P or Q vertex to vanish.  Those
  divisor strata cannot contain the stated pentagon.

Thus the correct lift filter is substantial (36 linear conditions per pair)
but does not itself close the generic pentagon.

## 2. Proposition 4.3 sub-case (2), characteristic zero

The exact five-ODE formulation and the saturation `w*a_8-1` were replayed.
The existing complete computations over the algebraic closures of 65521,
32003, and 65537 all force the degenerate `B=0` component and kill `a_8`.
Those are strong good-reduction evidence, not a characteristic-zero proof.

The one-shot characteristic-zero `std` calculation was launched against the
full normalized ideal.  Its final transcript/verdict is recorded below when
the process terminates.

## 3. Pentagon generic divisor and omitted multi-root strata

The assumption-free, no-division descent `nodivide5.py` was resumed from its
level-13 checkpoint.  It retains divisor branches instead of assuming a pivot
nonzero.

More importantly, the load-bearing D4 degree gap is now closed.  Write
`P=sum a_i(y)x^i`, `R=sum r_k(y)x^k`, with `deg(a_i)<=i+8`.  The rung first
containing `r_k` is

    8 a_8 r_k' - k a_8' r_k + known higher-r terms = 2 q_(k+5).

If the already-known terms obey `deg(r_l)<=l+7`, their degree is at most
`k+22`.  A hypothetical term `c*y^D` of `r_k` with `D>k+7` produces the unique
higher coefficient

    8*alpha*c*(D-2k).

For `k<=6`, `D>=k+8` gives `D-2k>=8-k>0`; it cannot cancel.  Descending from
the support bound `deg(r_7)<=14` proves

    deg_y(r_k) <= k+7,  k=0,...,7.

`sol3/residual_degree_bound.py` checks the coefficient formula symbolically.
This removes the caveat in `EIGHTH_POWER.md`: no higher row appears on any
single-root or multi-root stratum.  The eighth-power conclusion may use a zero
top coefficient at an individual rung, so equality is not required.

## 4. Degree-8 jet along the two proved pentagon edges

`sol3/degree8_jet.py` uses the structured driver

    P = alpha*y^8*(x*y-tau)^8
        + alpha*x^8*y^14*((y-rho)^2-y^2) + x.

It simultaneously realizes the proved upper eighth power, the lower
`y^14(y-rho)^2` row, x-degree 8, and all five required P vertices.  For each
slice it solves the full linear equation `[P,Q]=x^2` in all 125 coefficients
of the pentagon Q.

After torus normalization `tau=rho=1`, every nonzero remaining alpha was
exhausted over both `F_101` and `F_103`: 100 + 102 slices, zero consistent.
The broader small-integer grid gave 0/432.  A planted polynomial solution of
`[P,Q]=x^2` passes the same matrix builder at both primes.

No reduced solution, hence no lift candidate, exists in this two-edge jet
family on either exhaustive finite-field normalization.

## 5. Degree 144: `(8,28)/(7/4,3)`, `(m,n)=(3,4)`

The chain map gives four exact reduced shapes (two orientations for each
`c'=0,4`).  Their exact tangent screens are unexpectedly loose:

| `c'` | orientation | params | conditions | rank | residual bound |
|---:|---|---:|---:|---:|---:|
| 0 | P has epsilon `(2,1)` | 51 | 234 | 44 | 7 |
| 0 | P has epsilon `(1,0)` | 32 | 214 | 24 | 8 |
| 4 | first orientation | 187 | 156 | 156 | 31 |
| 4 | second orientation | 110 | 78 | 78 | 32 |

This is the largest missed hiding place in the five-target list.  By
comparison, the familiar open degree-108 shapes sit much closer to tangent
isolation.

`sol3/degree144_jet.py` then pinned the common-base power and the complete
vertical edge in both `c'=0` orientations and solved for every coefficient of
the other polygon.  After normalization, all nonzero alpha values were
exhausted over `F_101` and `F_103` in both orientations (404 total normalized
slices): zero were consistent.  Planted matrix controls pass.  This kills the
most rigid common-power construction, but not the full loose varieties.

Full vertex-saturated elimination of the first `c'=0` variety was also
launched; its final transcript/verdict is recorded below when it terminates.

## Bottom line

No original constant-Jacobian counterexample has been found.  The genuinely
new theorem is the all-rung residual degree bound, which repairs the omitted
multi-root step.  The genuinely large search target is the degree-144 chain:
it leaves 7/8 dimensions already for its small quadrilaterals and 31/32 for
its pentagons, although the natural common-power jets are empty.
