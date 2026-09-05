### 4.1 Per support: system size, solution structure, survivors

| support | shape | unknowns | residue equations | solution structure | instances | survivors |
|---|---|---|---|---|---|---|
| H1 | HE(G=0,H=1,K=2) | 6 | -4*g0*k2 + h1**2 | proper ideal (Groebner basis of 1 elements); solvable with h1 nonzero | 2 | 0 |
| H2 | HE(G=0,H=3,K=6) | 12 | -4*g0*k2 + 2*h0*h2 + h1**2; -4*g0*k3 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 + 2*h1*h3 + h2**2 ... (5 total) | Groebner not attempted (12 unknowns, 5 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g_ | 1 | 0 |
| H3 | HE(G=1,H=1,K=1) | 6 | -4*g1*k1 + h1**2 | proper ideal (Groebner basis of 1 elements) | 1 | 1 |
| H4 | HE(G=1,H=2,K=3) | 9 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h1*h2; -4*g1*k3 + h2**2 | proper ideal (Groebner basis of 7 elements) | 1 | 1 |
| H5 | HE(G=1,H=3,K=5) | 12 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h1*h3 + h2**2 ... (5 total) | Groebner not attempted (12 unknowns, 5 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g_ | 1 | 1 |
| H6 | HE(G=1,H=5,K=9) | 18 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h0*h4 + 2*h1*h3 + h2**2 ... (9 total) | Groebner not attempted (18 unknowns, 9 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g_ | 1 | 0 |
| H7 | HE(G=1,H=8,K=15) | 27 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h0*h4 + 2*h1*h3 + h2**2 ... (15 total) | Groebner not attempted (27 unknowns, 15 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g | 1 | 1 |
| H8 | HE(G=1,H=15,K=29) | 48 | -4*g0*k2 - 4*g1*k1 + 2*h0*h2 + h1**2; -4*g0*k3 - 4*g1*k2 + 2*h0*h3 + 2*h1*h2; -4*g0*k4 - 4*g1*k3 + 2*h0*h4 + 2*h1*h3 + h2**2 ... (29 total) | Groebner not attempted (48 unknowns, 29 equations); structure read off directly: every equation is LINEAR in the k_j with triangular leading term -4 g | 1 | 1 |
| H9 | HE(G=2,H=2,K=2) | 9 | g2; -4*g0*k2 - 4*g1*k1 - 4*g2*k0 + 2*h0*h2 + h1**2; -4*g1*k2 - 4*g2*k1 + 2*h1*h2 ... (4 total) | UNIT IDEAL with g2 nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| H10 | HE(G=0,H=0,K=2) | 5 | -4*g0*k2 | proper ideal (Groebner basis of 1 elements); solvable with k2 nonzero | 0 | 0 |
| E1 | SE(m=2;3) | 4 | none (every point of the support solves) | no equations: the whole support solves | 2 | 2 |
| E2 | SE(m=2;2) | 4 | 1 | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E3 | SE(m=2;4) | 4 | -alpha | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E4 | SE(m=2;5) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| E5 | SE(m=2;9) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| E6 | SE(m=3;2) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E7 | SE(m=3;4) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| E8 | SE(m=3;3) | 4 | 1 | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E9 | SE(m=2;2,3) | 5 | 1 | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| E10 | SE(m=2;3,3) | 5 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E11 | SE(m=3;5,4) | 5 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E12 | SE(m=2;27) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E13 | SE(m=4;3) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| E14 | SE(m=5;3) | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| V1 | v-power  P = h0 y + c x^1 y^2 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V2 | v-power  P = h0 y + c x^2 y^3 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V3 | v-power  P = h0 y + c x^2 y^5 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V4 | v-power  P = h0 y + c x^3 y^4 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 1 |
| V5 | v-power  P = h0 y + c x^4 y^2 | 4 | none (every point of the support solves) | no equations: the whole support solves | 1 | 0 |
| V6 | v-power  P = h0 y + c x^2 y^4 | 4 | -alpha | UNIT IDEAL with alpha c nonzero adjoined: NO SOLUTIONS | 0 | 0 |
| M1 | shear image | 10 | none (every point of the support solves) | shear image of a solved support; Jacobian-1 shears preserve eta and all periods (control G3) | 1 | 1 |
| M2 | shear image | 15 | none (every point of the support solves) | shear image of a solved support; Jacobian-1 shears preserve eta and all periods (control G3) | 1 | 1 |
| M3 | shear image | 6 | none (every point of the support solves) | shear image of a solved support; Jacobian-1 shears preserve eta and all periods (control G3) | 1 | 1 |

### 4.2 Per instance: certificates and mate verdicts

| support | id | deg | deg_y | screen | genus | punctures | Bezout | SY | survivor | mate | NUM-MONO rel |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | `1e8144b39dbd` | 2 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | COORDINATE | no | - | 4.6e-16 |
| H1 | `05448ae01b6d` | 2 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | COORDINATE | no | - | 4.8e-16 |
| H2 | `f9c3e6131ab8` | 6 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | COORDINATE | no | - | 1.1e-15 |
| H3 | `d37142063698` | 3 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=3:EMPTY_over_Q;D=5:EMPTY_over_Q;D=6:EMPTY_over_Q | 2.0e-13 |
| H4 | `431f3f1966ca` | 3 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=3:EMPTY_over_Q;D=5:EMPTY_over_Q;D=6:EMPTY_over_Q | 3.6e-15 |
| H5 | `9667585bcb72` | 5 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 5.8e-14 |
| H6 | `fb63dd1ccaec` | 9 | 2 | PERIODS_VANISH | 0 | - | NOT_CERTIFIED (None) | NON_COORDINATE | no | - | 3.4e-15 |
| H7 | `2c6dbb9e3815` | 15 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=15:EMPTY_over_Q;D=23:EMPTY_over_Q | - |
| H8 | `02299003cb19` | 29 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=29:EMPTY_over_Q | - |
| E1 | `4b3d403b5051` | 5 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 6.9e-14 |
| E1 | `e57028c3921e` | 5 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 5.4e-15 |
| E4 | `168e0b30d46b` | 7 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 4.3e-14 |
| E5 | `65551d9727e7` | 11 | 2 | PERIODS_VANISH | 0 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=11:EMPTY_over_Q;D=17:EMPTY_over_Q;D=22:EMPTY_over_Q | 1.3e-13 |
| E6 | `b520c37ad02b` | 5 | 3 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 2 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 1.5e+00 |
| E7 | `f2782c9f083f` | 7 | 3 | PERIODS_VANISH | 0 | 4 | OK residual 0 (LINALG) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 6.9e-14 |
| E10 | `5ba43826fa42` | 8 | 2 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 1.4e+00 |
| E11 | `e507bc4e8db0` | 12 | 3 | UNDECIDED_BY_RESIDUES_genus>=1 | 2 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | - |
| E12 | `13aa79d7382f` | 29 | 2 | PERIODS_VANISH | 0 | 3 | NOT_CERTIFIED (None) | NON_COORDINATE | no | - | - |
| E13 | `462652ead2a6` | 7 | 4 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 3 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 2.0e+00 |
| E14 | `5497083f3554` | 8 | 5 | UNDECIDED_BY_RESIDUES_genus>=1 | 2 | 2 | OK residual 0 (LINALG) | NON_COORDINATE | no | - | 2.1e+00 |
| V1 | `2f401c620811` | 3 | 2 | PERIODS_VANISH | 0 | 2 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=3:EMPTY_over_Q;D=5:EMPTY_over_Q;D=6:EMPTY_over_Q | 8.9e-15 |
| V2 | `977aeb39d938` | 5 | 3 | PERIODS_VANISH | 0 | 3 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 2.1e-14 |
| V3 | `3d71c055f95f` | 7 | 5 | PERIODS_VANISH | 0 | 3 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 1.8e-15 |
| V4 | `8cf19228f363` | 7 | 4 | PERIODS_VANISH | 0 | 4 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=7:EMPTY_over_Q;D=11:EMPTY_over_Q;D=14:EMPTY_over_Q | 1.2e-13 |
| V5 | `e1961840267e` | 6 | 2 | UNDECIDED_BY_RESIDUES_genus>=1 | 1 | 3 | OK residual 0 (EUCLID) | NON_COORDINATE | no | - | 1.6e+00 |
| M1 | `2d9fa751f027` | 5 | 2 | PERIODS_VANISH | 0 | - | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | 2.0e-13 |
| M2 | `97e25aa31406` | 6 | 6 | PERIODS_VANISH | 0 | 2 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=6:EMPTY_over_Q;D=9:EMPTY_over_Q;D=12:EMPTY_over_Q | - |
| M3 | `61cc00cd7420` | 5 | 5 | PERIODS_VANISH | 0 | 2 | OK residual 0 (EUCLID) | NON_COORDINATE | yes | D=5:EMPTY_over_Q;D=8:EMPTY_over_Q;D=10:EMPTY_over_Q | - |

### 4.3 The synthesised P (survivors)

* `d37142063698`  (support H3, degree 3) — `P = 1*x*y^2 + 1*x*y + (1/4)*x + 1*y`
* `431f3f1966ca`  (support H4, degree 3) — `P = (1/4)*x^3 + 1*x^2*y + 1*x*y^2 + (3/4)*x^2 + 1*x*y - 1*y^2 + (3/2)*x + 1*y + (7/4)`
* `9667585bcb72`  (support H5, degree 5) — `P = (1/8)*x^5 + (1/4)*x^4 + 1*x^3*y + (1/8)*x^3 + 1*x^2*y + 2*x*y^2 + (1/4)*x^2 + (1/4)*x + 1*y + (-3/8)`
* `2c6dbb9e3815`  (support H7, degree 15) — `P = (1/4)*x^15 + (1/2)*x^14 + (1/4)*x^13 + (1/2)*x^12 + (1/2)*x^11 + (3/4)*x^9 + 1*x^8*y + (1/2)*x^8 + 1*x^7*y + (1/2)*x^7 + 1*x^6 + 1*x^5*y + (1/2)*x^4 + (1/4)*x^3 + 1*x^2*y + 1*x*y^2 + (1/2)*x + 1*y + (-1/4)`
* `02299003cb19`  (support H8, degree 29) — `P = (1/4)*x^29 + (1/2)*x^28 + (1/4)*x^27 + 1*x^15*y + 1*x^14*y + (1/2)*x^14 + (1/2)*x^13 + 1*x*y^2 + 1*y + (-1/4)`
* `4b3d403b5051`  (support E1, degree 5) — `P = 1*x^3*y^2 + 1*x`
* `e57028c3921e`  (support E1, degree 5) — `P = 3*x^3*y^2 - 9*x^2*y^2 + 9*x*y^2 - 3*y^2 + 2*x + 1`
* `168e0b30d46b`  (support E4, degree 7) — `P = 1*x^5*y^2 + 1*x`
* `65551d9727e7`  (support E5, degree 11) — `P = 1*x^9*y^2 + 1*x`
* `f2782c9f083f`  (support E7, degree 7) — `P = 1*x^4*y^3 + 1*x`
* `2f401c620811`  (support V1, degree 3) — `P = 1*x*y^2 + 1*y`
* `977aeb39d938`  (support V2, degree 5) — `P = 1*x^2*y^3 + 1*y`
* `3d71c055f95f`  (support V3, degree 7) — `P = 1*x^2*y^5 + 1*y`
* `8cf19228f363`  (support V4, degree 7) — `P = 1*x^3*y^4 + 1*y`
* `2d9fa751f027`  (support M1, degree 5) — `P = 1*x^5 + 2*x^4 + 2*x^3*y + 2*x^3 + 2*x^2*y + 1*x*y^2 + 2*x^2 + 1*x*y + (5/4)*x + 1*y`
* `97e25aa31406`  (support M2, degree 6) — `P = 1*y^6 + 3*x*y^4 + 2*y^5 + 3*x^2*y^2 + 4*x*y^3 + 2*y^4 + 1*x^3 + 2*x^2*y + 3*x*y^2 + 1*y^3 + 1*x^2 + 1*x*y + (5/4)*y^2 + (5/4)*x + 1*y`
* `61cc00cd7420`  (support M3, degree 5) — `P = 1*x^3*y^2 + 3*x^2*y^3 + 3*x*y^4 + 1*y^5 + 1*x + 1*y`
