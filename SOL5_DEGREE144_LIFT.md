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

## Lift-kernel formulation: correction, 49 variables become 18

`degree144_lift_kernel_search.py` removes the continuation tradeoff entirely.
For each `(lambda_2,lambda_3,1)` it computes the complete pole matrices and
parameterizes both polynomials directly in their kernels:

    driver: 51 coefficients - rank 40 = 11 dimensions
    partner: 31 coefficients - rank 24 = 7 dimensions

The first version of this note incorrectly treated the three driver vertex
rows as three independent gauges. The exact edge calculation below shows that
the two right-edge endpoints are automatically equal on the lift kernel, so
that gauge block has rank **2**, not 3. The old 17-variable numerical chart was
therefore ill-conditioned and its numerical sweep is withdrawn.

The corrected chart sets two independent driver vertices to 1 and the third is
then 1 by the exact edge identity. This reduces the driver kernel from 11 to 9
free coordinates. Thus the simultaneous support/lift search is an 18-variable
system (9 + 7 + 2 shears) with:

* all 64 Laurent-pole equations zero by construction;
* both independent driver gauges exact by construction, with the third driver
  vertex fixed automatically by the right-edge identity;
* the full 106 coefficient equations of `[P,Q]-x^2` as the only core residual;
* a small search-only barrier keeping the three partner vertices away from the
  deleted boundary. The barrier is excluded from the reported raw residual.

Controls independently verify both lift nullspaces and the tensor bracket
builder against `lift_x4.bracket`.

The original ten-start, rank-3 gauged sweep is withdrawn because of that gauge
rank error. Its negative output was not a counterexample claim, but it is not
evidence for emptiness either. The corrected real/complex sweep is recorded in
the follow-up commit.

The old diagnostic file is retained only to reproduce the discovery of the
rank defect and must not be used as a verdict artifact.

## Corrected complex search

JC2 is over `C`, so the corrected rank-2 gauge chart was searched with 18
**complex** variables, not merely real coefficients. The lift kernels and two
independent gauges remained exact throughout.

Eight complex perturbations of the validated real near-miss all returned to
`lambda_2=lambda_3=0` and the same nonzero raw bracket floor:

    best full complex bracket norm   7.071149857399e-1
    maximum bracket coefficient      5.024073310753e-1
    partner vertices                 0.502407, 0.314447, 0.314447

The limiting chart is the already certified-empty `(0,0,1)` fibre. Thus the
real reduced component does not peel into a nearby complex lift component.
Twelve broad complex starts away from that basin also produced no hit (best raw
norm `2.6294`), with all partner vertices nonzero. These are numerical screens,
not generic emptiness proofs.

## Exact closure of the whole `lambda_2=0` divisor

`degree144_lambda2_zero_certificate.py` reconstructs the complete lift kernels
symbolically over `Q` with `lambda_2=0`, `lambda_3=t`, and `lambda_4=1`, then
forms the original full bracket. Three of its coefficient equations satisfy

    F_(2,1) - F_(2,0) - t F_(3,1) = 1.

The script verifies the identity exactly. Therefore the simultaneous-shear
support/lift system is **EMPTY over characteristic zero for every** `t` on the
entire divisor `lambda_2=0`. This strictly extends the earlier `(0,0,1)`
certificate and has no genericity or nonzero-`t` assumption.

## Exact nonzero-shear finite-field fibres

`degree144_lift_modp.py` row-reduces both lift matrices exactly over a finite
field and exports a fixed nonzero-shear fibre as 75--76 equations in 16 kernel
coordinates. `degree144_fixed_fiber_certificate.py` then performs every forced
linear elimination, leaving 69--70 quadrics in 10 variables, and extracts a
degree-4 Macaulay certificate for `1`.

The following fibres are independently re-expanded to exactly `1`; perturbing
one certificate multiplier breaks each identity:

| prime | `(lambda_2,lambda_3,lambda_4)` | reduced system | terms | verdict |
|---:|---:|---:|---:|---|
| 101 | `(1,1,1)` | 69 quadrics / 10 vars | 128 | EMPTY mod p |
| 103 | `(1,1,1)` | 69 quadrics / 10 vars | 127 | EMPTY mod p |
| 101 | `(1,2,1)` | 70 quadrics / 10 vars | 152 | EMPTY mod p |
| 101 | `(2,1,1)` | 69 quadrics / 10 vars | 153 | EMPTY mod p |
| 101 | `(2,3,1)` | 70 quadrics / 10 vars | 150 | EMPTY mod p |

These fixed-fibre modular certificates do not prove the whole
`lambda_2 != 0` characteristic-zero chart empty. They establish a reproducible
exact pipeline and give strong evidence that a witness, if any, must lie on an
exceptional shear locus where the degree-4 Macaulay rank drops.

## Exact symbolic `lambda_2=1` line and exhaustive `F_11` screen

`degree144_normalized_line.py` keeps `lambda_3=t` symbolic on the exact slice
`(lambda_2,lambda_4)=(1,1)`. It recomputes both full lift kernels over `Q(t)`,
imposes the two independent gauges, and forms all 76 bracket equations. There
are no parameter denominators. Six forced coefficient coordinates eliminate
polynomially, including at `t=0`, and exact duplicate/redundant edge equations
leave 50 equations in 10 coefficient variables plus `t`.

Specializing this symbolic system at `t=1` modulo 101 gives exactly the same 50
distinct reduced polynomials as the independently constructed fixed-fibre
system. This is a cross-implementation replay check, not just an equation
count.

`degree144_normalized_line_sweep.py` exhausts every rational value
`t in F_11`. All eleven fibres have independently replayed degree-4 unit
certificates (with a deliberately altered-certificate negative control):

* `t=0`: Macaulay rank 564, 34 certificate terms;
* `t=1,...,10`: Macaulay rank 569, 117--143 certificate terms.

This closes the **F_11-rational points of this line only**. It does not exclude
parameters in extension fields and is not a characteristic-zero certificate.

There is a tempting but invalid shortcut here. Diagonal coordinate scaling
acts on ungauged shears by `lambda_k' = B A^k lambda_k`, but on the two driver
gauge coefficients by different weights (`A` and `A^16` after preserving
`lambda_4=1`). The second driver gauge has already consumed that torus freedom.
Consequently `lambda_2=1` with both gauges fixed is a genuine slice, not a
representative of every `lambda_2 != 0` fibre. No whole-chart conclusion is
drawn from the normalized-line computation.

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

The next decisive computation is a rank-drop/elimination calculation on the
corrected two-parameter `lambda_2 != 0` plane. The exact normalized-line core
also exposes a triangular boundary subsystem (one constant driver pivot and
three ensuing equations independent of the last top-edge driver coefficient),
which is a better starting point than the raw 76 equations. Generic fibres
already have short unit certificates; only the exceptional locus can hide a
modular point for Hensel/reconstruction. This remains strictly smaller and
better conditioned than the old 47-driver/209-support/64-pole penalty system.
