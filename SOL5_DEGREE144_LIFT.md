# Sol 5: degree-144 simultaneous-shear lift intersection

Date: 2026-08-25. Branch: `codex/sol5-counterexample-hunt`.

## Binding counterexample gate

A point of the reduced equation `[P,Q]=x^2` is not a plane Jacobian
counterexample. It must reverse through the Laurent chain to two polynomials,
retain every required Newton vertex, have exactly constant nonzero original
Jacobian, and then be proved noninjective. Nothing in this note passes that
gate. Numerical output is reconnaissance only.

## Sol 4 recovery

There was no newer Sol 4 ref or artifact on the remote. The newest pushed hunt
tip was `3567fb3` on `codex/sol3-all-five`. Its two exact degree-144 closures
replay:

* the `(lambda_2,lambda_3,lambda_4)=(0,0,1)` intersection has the stated
  three-generator rational Nullstellensatz certificate;
* the opposite epsilon orientation generates row 12 only through x-degree 15,
  so its required `(16,12)` vertex is identically zero.

Those closed charts were not reopened.

## The real reduced point is reproduced

`degree144_numeric.py --case Q-drives --real-only --free-other-vertices`
reproduces the full 209-equation reduced recurrence point:

    support norm             1.043366033381e-14
    support max coefficient  5.329070518201e-15
    generated vertices       0.6258768827, 1.1172207541

The point is saved as `sol3/degree144_reduced_seed.npz`. This confirms the
reduced component, but its raw reverse-lift defect at `(0,0,1)` is
`2.574710518122e3` (maximum coefficient `2.490193862992e3`).

## Simultaneous-shear continuation

`degree144_lift_continuation.py` frees `lambda_2,lambda_3`, fixes
`lambda_4=1`, preserves all 209 support equations, and includes all 64 pole
coefficients. It uses fixed row scaling only for conditioning and reports the
unscaled norms after every stage. Its fast multinomial lift matrix is checked
term-for-term against the independent `lift_x4.reverse` implementation.

The continuation reduced the raw lift defect substantially, but only by
leaving the support variety:

| lift weight | support norm | raw lift norm | generated vertices |
|---:|---:|---:|---:|
| `1e-6` | `1.18e-7` | `2.556e3` | `0.626, 1.114` |
| `1e-4` | `7.64e-5` | `2.308e3` | `0.626, 1.024` |
| `1e-2` | `1.48e-3` | `8.148e1` | `0.624, 0.0525` |
| `1` | `2.68e-2` | `2.532` | `0.691, 0.542` |

This is not an intersection.

## Lift-kernel formulation: 49 variables become 17

`degree144_lift_kernel_search.py` removes the continuation tradeoff entirely.
For each `(lambda_2,lambda_3,1)` it computes the complete pole matrices and
parameterizes both polynomials directly in their kernels:

    driver: 51 coefficients - rank 40 = 11 dimensions
    partner: 31 coefficients - rank 24 = 7 dimensions

The three nonzero driver vertices are set identically to 1 using the three
available torus/scaling gauges, reducing the driver kernel from 11 to 8 free
coordinates. Thus the simultaneous support/lift search is a 17-variable system
(8 + 7 + 2 shears) with:

* all 64 Laurent-pole equations zero by construction;
* all three driver gauges exact by construction;
* the full 106 coefficient equations of `[P,Q]-x^2` as the only core residual;
* a small search-only barrier keeping the three partner vertices away from the
  deleted boundary. The barrier is excluded from the reported raw residual.

Controls independently verify both lift nullspaces and the tensor bracket
builder against `lift_x4.bracket`.

Ten gauged starts found no numerical intersection. The best raw point has:

    lambda_2, lambda_3, lambda_4  -0.05866037, 0.06079895, 1
    full bracket norm             1.057211683686
    full bracket max coefficient  0.927646801788
    full lift norm                1.042421502260e-12
    driver gauges                 1, 1, 1
    partner vertices              0.0723532, 0.0445204, 0.0445204

The best point is saved as `sol3/degree144_lift_kernel_best.npz`. It is useful
as a negative diagnostic, not as an emptiness certificate.

## Exact generic-chart edge consequence

The highest pole equations are independent of `lambda_2,lambda_3`. Exact
rational row reduction in `degree144_lift_edge_certificate.py` proves that
every point on the simultaneous-shear lift locus must have

    driver x^16 row  = A y^12 (1+y)^4,
    partner x^12 row = B y^9  (1+y)^3.

The script verifies the one-dimensional kernels exactly as coefficient vectors
`(1,4,6,4,1)` and `(1,3,3,1)`. This does not itself contradict the bracket—the
highest Wronskian vanishes automatically—but it is an exact reduction that an
eliminator can impose before touching lower rows.

## Verdict and next exact step

**No counterexample.** The genuine reduced degree-144 component still has no
observed intersection with the generic simultaneous-shear polynomiality locus.
The generic chart is **NO VERDICT**, not closed: numerical nonintersection is
not an emptiness proof.

The next decisive computation is to export the 17-variable lift-kernel bracket
system over a finite field with the two exact binomial edge rows substituted,
then compute either a saturated modular point (for Hensel/reconstruction) or a
unit-ideal certificate. This is strictly smaller and better conditioned than
the 47-driver/209-support/64-pole penalty formulation.
