# night11 -- NUMERIC NET (v0): landscape census

First numerical search of this campaign. Continuous optimization of
real coefficient vectors for polynomial pairs `(P, Q)` of degrees
`(2m, 3m) = (84, 126)`, `m = 42`, against

    E(c) = E_K + lambda_T * E_T,
    E_K  = sum of squares of all coefficients of P_x Q_y - P_y Q_x - 1,

with many random restarts. **v0 maps the landscape only.** Every number
below is a measurement of where an optimizer stops; nothing here is
lifted, certified, or claimed to be anything.

## 1. Parametrization

See `supports.py` for the full derivation. Summary:

* **Newton-triangle similarity.** `supp(P) subset Delta(84)`,
  `supp(Q) subset Delta(126) = 1.5 * Delta(84)` -- one Newton triangle
  and a scaled copy. On its own that is 11783 real parameters.
* **Torus grading.** `P`, `Q` are taken semi-invariant of weights
  `aP`, `aQ` under `(x,y) -> (zeta x, zeta^-1 y)`, `zeta^t = 1`; a
  monomial `x^i y^j` has weight `i - j mod t`. The Jacobian then has
  weight `aP + aQ`, so `aP + aQ = 0 (mod t)` is needed for the residual
  to stay in one class.
* **The grading is not free.** The `(0,0)` coefficient of the Jacobian
  is exactly `P[1,0] Q[0,1] - P[0,1] Q[1,0]` and nothing else, so the
  constant `1` is reachable only if `aP = 1`, `aQ = -1 (mod t)`.
  If additionally the leading forms are to have the `(H^2, H^3)` shape
  one needs `w` with `2w = aP`, `3w = aQ`, forcing `t | 5`.

  This was found by measurement, not assumed: a first design put both
  `P` and `Q` in the sublattice `{i - j = 0 mod 16}` (745 parameters),
  where `(1,0)` and `(0,1)` are absent; every seed there ran to
  `E_K = 1.0000000` with `||P_x Q_y - P_y Q_x|| ~ 2e-4`, i.e. straight
  into the degenerate locus `Jacobian = 0`, because `E_K >= 1` holds
  identically on that support.

| arm | t | aP, aQ | params (P + Q) | residual cells | unknowns/eqns | top-form dims | (H^2,H^3) shape reachable |
|---|---|---|---|---|---|---|---|
| GRADED-5 | 5 | 1, 4 | 731 + 1626 = 2357 | 4389 | 0.537 | 17, 26 | yes (w = 3) |
| GRADED-15 | 15 | 1, 14 | 245 + 543 = 788 | 1463 | 0.539 | 6, 8 | NO |
| FULL | 1 | 0, 0 | 3655 + 8128 = 11783 | 21945 | 0.537 | 85, 127 | yes |

`GRADED-15` (788 parameters) is the primary arm: it is inside the
300-800 parameter band the brief asked for. `GRADED-5` (2357
parameters) is the secondary arm; it is the only nontrivial grading
that also admits the `(H^2, H^3)` leading-form shape, and it is above
the band -- the band and that shape are not simultaneously satisfiable.
Unknowns/equations is ~0.54 in every arm because both counts scale
like `1/t`: the grading is a resolution knob, not a knob on how
over-determined the Keller system is.

## 2. What E_T measures, and what it does not

`E_T` acts on the leading homogeneous parts `P_top` (degree 84) and
`Q_top` (degree 126) only. For a pair of degrees `(2m, 3m)` the shape
wanted of the leading forms is `P_top ~ H^2`, `Q_top ~ H^3` for a
single form `H` of degree `m`; equivalently `P_top^3` and `Q_top^2`
(both of degree `6m`) are proportional. `E_T` measures exactly that
proportionality defect, as a squared sine of the angle between the two
coefficient vectors, plus a guard keeping the leading forms from
collapsing:

    A = tP*tP*tP,  B = tQ*tQ   (1D coefficient convolutions)
    E_prop = 1 - <A,B>^2 / (|A|^2 |B|^2)          in [0,1], scale free
    E_nd   = relu(tau - |tP|^2)^2 + relu(tau - |tQ|^2)^2,  tau = 1e-2
    E_T    = E_prop + E_nd

**Limitation.** This is a proxy on the leading forms, not the Jelonek
set. It says nothing about lower-order terms, and the actual
non-properness locus is cut out by the leading coefficients (in the
source variable) of `Res_y(P-u, Q-v)` and `Res_x(P-u, Q-v)`, which are
far too heavy to form symbolically at degrees (84, 126). `E_prop = 0`
is a necessary shape condition, in no way sufficient; a small `E_T`
supports no conclusion. The smallest singular value of the Sylvester
matrix of the two leading forms (the alternative the brief suggested)
is computed as a post-hoc diagnostic on the recorded stalls only -- a
210x210 SVD inside the inner loop would have cost more than the whole
objective. The objective is a swappable object (`supports.Objective`,
`tear=` argument), so a refined `E_T` drops in without touching the net.

## 3. Controls (hard gate, all run before the search)

### N1 -- symbolic vs numeric Keller residual: **PASS**

Random pair of degrees (3, 4), coefficients rounded to 6 decimals and
lifted to exact rationals in sympy; `expand(P_x Q_y - P_y Q_x - 1)`
compared cell by cell with the FFT kernel.

| quantity | value |
|---|---|
| monomials compared | 21 |
| max abs difference, all cells | 3.553e-15 |
| fused-FFT vs explicit-convolution residual | 7.105e-15 |
| direct vs FFT product, deg 39 x deg 59 | 1.636e-15 (relative) |
| analytic vs central-difference gradient (43 params, lambda_T = 0.3) | 9.748e-11 (relative) |

### N2 -- seeded at a known automorphism

Automorphisms used: `P = x + f(y)`, `Q = y + g(P)`, Jacobian identically
1, degrees `(deg f, deg f * deg g)`.

**The campaign degree shape (84, 126) admits no automorphism at all.**
By Jung-van der Kulk every planar polynomial automorphism is tame and
its two degrees are divisibility-ordered; 84 does not divide 126 and
126 does not divide 84. N2 is therefore run at (4, 8) and at (84, 168),
the nearest same-scale shape that does carry one.

| | N2a | N2b |
|---|---|---|
| degrees | (4, 8) | (84, 168) |
| parameters (full triangular support) | 60 | 18020 |
| E_K at the exact automorphism | 1.624e-29 | 1.338e-24 |
| perturbation applied | 1e-3 | 1e-8 |
| E_K at the perturbed start | 6.855e-03 | 6.025e-05 |
| E_K after descent | **6.960e-20** | **6.749e-13** |
| iterations | 528 | 4000 |

N2a reaches `6.96e-20`: the basin exists and the code finds exact
structure to the precision the brief asked for. N2b descends 8 decades
from its perturbed start but stops at `6.7e-13` within its 4000-iteration
budget. Recorded as measured: at 18020 parameters the Keller variety is
positive-dimensional, so the Hessian is singular along the automorphism
group directions and L-BFGS-B converges linearly, not quadratically.
`E_K = 1.3e-24` at the exact point shows the floor is not a kernel
accuracy limit.

### N3 -- random seeds at small degree

| degrees | shape | params | seeds | reached E_K < 1e-18 | best | median |
|---|---|---|---|---|---|---|
| (2, 4) | d, 2d | 21 | 12 | 9/12 | 7.217e-32 | 2.128e-29 |
| (4, 8) | d, 2d | 60 | 12 | 0/12 | 2.434e-10 | 1.424e-07 |
| (4, 6) | 2m, 3m (m=2) | 43 | 12 | 1/12 | 3.713e-19 | 6.657e-09 |

`(2,4)` and `(4,8)` are shapes `d | 2d`, where automorphisms are
abundant. `(4,6)` is the mission shape `(2m, 3m)` at `m = 2`, where
the same divisibility obstruction as at (84,126) applies, and it is
reported alongside as the small-degree image of the mission problem.

N3 reads as follows. At `(2,4)` -- 21 parameters -- random seeds do
reach machine precision (9 of 12, best `7.22e-32`), which is the check the
brief asked for. At `(4,8)` -- 60 parameters -- they do not inside a
2000-iteration budget (best `2.43e-10`), even though N2a shows that same
shape's automorphism basin is reachable to `6.96e-20` when the descent
starts near it. So the `(4,8)` shortfall is a reach-from-random-start
and budget effect, not a defect in the residual or its gradient, which
N1 pins to `4e-15`. This is recorded as the state of the gate, not
argued away: the net's own stall values below have to be read knowing
that random-start descent already fails to find known exact structure
at 60 parameters in this budget.

Controls wall time: 57.9 s.

## 4. The net

| | |
|---|---|
| degrees | (84, 126) |
| optimizer | scipy L-BFGS-B, `ftol = gtol = 0` (relative stopping tests OFF) |
| iteration budget | 4000 per seed, re-launched from the end point on early stop (up to 4 passes, total capped at the budget) |
| seeds | 300 total |
| initialisation | coefficients `~ N(0, decay^(i+j))` on the masked support, then a global rescale `P,Q -> sP,sQ` making `\|P_x Q_y - P_y Q_x\| = 1`; four decay families `flat`=1.00, `mild`=0.96, `steep`=0.90, `vsteep`=0.82 |
| parallelism | 4 cores, `multiprocessing.Pool` |
| wall time | 4595 s (76.6 min) |

`ftol = gtol = 0` matters: with scipy's defaults the descent halts on a
relative test around `1e-11` and every "plateau" would be a tolerance
artefact. Here a run ends only on the iteration budget or on a genuine
line-search failure.

### Classification tally

* `CONVERGED-AUTOMORPHISM-LIKE` -- `E_K < 1e-18`.
* `STALLED-COLLAPSED` -- `|E_K - 1| < 1e-6` with
  `||P_x Q_y - P_y Q_x|| < 1e-3`: the degenerate attractor where the
  Jacobian is driven to zero and the residual is just the missing
  constant. `E_K = 1` is exactly the value of that locus.
* `STALLED` -- everything else that stayed finite; the interesting class.
* `DIVERGED` -- non-finite, or `E_K > 1e6`.

| arm | seeds | CONVERGED-<br>AUTOMORPHISM-<br>LIKE | STALLED | STALLED-<br>COLLAPSED | DIVERGED | min E_K | median E_K |
|---|---|---|---|---|---|---|---|
| `G15_lamT0` | 120 | 0 | 120 | 0 | 0 | 2.119e-09 | 6.414e-06 |
| `G15_lamT1e-3` | 120 | 0 | 120 | 0 | 0 | 2e-09 | 6.626e-06 |
| `G5_lamT1e-3` | 60 | 0 | 60 | 0 | 0 | 4.043e-06 | 4.792e-05 |
| **all** | 300 | 0 | 300 | 0 | 0 | 2e-09 | 1.489e-05 |

### Histogram of final E_K

| bin | `G15_lamT0` | `G15_lamT1e-3` | `G5_lamT1e-3` | all |
|---|---|---|---|---|
| `[1e-12, 1e-08)` | 5 | 6 | 0 | 11 |
| `[1e-08, 1e-06)` | 28 | 28 | 0 | 56 |
| `[1e-06, 1e-04)` | 60 | 62 | 38 | 160 |
| `[1e-04, 1e-03)` | 18 | 16 | 3 | 37 |
| `[1e-03, 1e-02)` | 7 | 3 | 0 | 10 |
| `[1e-01, 5e-01)` | 1 | 2 | 0 | 3 |
| `[5e-01, 9e-01)` | 1 | 2 | 0 | 3 |
| `[9e-01, 1e+00)` | 0 | 1 | 1 | 2 |
| `[1e+00, 2e+00)` | 0 | 0 | 15 | 15 |
| `[1e+01, 1e+02)` | 0 | 0 | 3 | 3 |

**Stall count: 300** of 300 seeds in the `STALLED` class
(0 more sat in the degenerate `E_K = 1` collapse, 0 converged, 0 diverged).

Reading of the tally, kept to what was measured:

* **The classification is degenerate: every one of the 300 seeds landed
  in the single class `STALLED`.** Nothing converged, nothing collapsed
  onto the `E_K = 1` degenerate locus, nothing diverged. The four-way
  classification therefore separated nothing in this run, and the
  informative object is the `E_K` distribution, not the class labels.
* The `STALLED-COLLAPSED` count being `0` is the one thing the labels do
  say: the corrected support fixed the failure mode recorded in
  `STATUS.md`, where every seed on the old `aP = aQ = 0` support ran to
  `E_K = 1`. Here the median `||P_x Q_y - P_y Q_x||` is `1`, i.e. the
  Keller constant is being fitted rather than the Jacobian being killed.
* The whole distribution sits between `2e-09` and `39`. The smallest
  `E_K` reached anywhere in 300 seeds x 4000 iterations is `2e-09`, which is
  about 9 decades above the `1e-18` bar this campaign set for
  `CONVERGED-AUTOMORPHISM-LIKE`.
* That gap has to be read against control N3, which is the reason the
  bar is not the interesting quantity here: at **60** parameters and the
  same budget, random starts already failed to find known exact
  structure, bottoming out at `2.4e-10`. A floor at 788 parameters is
  consistent with that and carries no information about whether
  anything exists at degrees (84, 126).
* Every seed in every arm used its full 4000-iteration budget in a single
  L-BFGS-B pass (median passes 1, median iterations 4000): no run stopped
  early on a line-search failure, so these are budget-limited end
  points, not points where the descent demonstrably ran out of
  descent direction. The gradient norms in the stall table (`~1e-4`)
  say the same thing.

### Plateau by initialisation family

| family | decay | seeds | median E_K | min E_K |
|---|---|---|---|---|
| `flat` | 1.00 | 75 | 0.0002831 | 5.995e-06 |
| `mild` | 0.96 | 75 | 5.426e-06 | 1.769e-07 |
| `steep` | 0.90 | 75 | 1.033e-05 | 4.314e-08 |
| `vsteep` | 0.82 | 75 | 5.985e-07 | 2e-09 |

### The tear proxy, by arm

| arm | lambda_T | median E_prop | min E_prop | median E_T | min E_T |
|---|---|---|---|---|---|
| `G15_lamT0` | 0 | not computed | not computed | not computed | not computed |
| `G15_lamT1e-3` | 0.001 | 1 | 1 | 1 | 1 |
| `G5_lamT1e-3` | 0.001 | 0.0001244 | 8.181e-06 | 0.0003244 | 0.0002082 |

`E_T` and `E_prop` are only evaluated when `lambda_T != 0`; the
`G15_lamT0` records carry `0.0` in those fields because the term was
never formed, not because the proxy vanished. Read those two cells as
*not computed*, and the same applies to the `E_T` / `E_prop` columns of
the `G15_lamT0` rows in the stall table below.

On the arms where it was computed the proxy behaves exactly as the
grading arithmetic predicts, which is the one place in this run where a
derivation made a numerical prediction and the numbers met it:

* `G15_lamT1e-3` (`t = 15`): `E_prop = 1` at **every one of the 120**
  seeds, minimum and median alike -- the maximum the proxy can take.
  `t = 15` admits no weight `w` with `2w = aP`, `3w = aQ`, so the
  `(H^2, H^3)` shape is not in the support at all and `E_prop` cannot
  descend. It did not.
* `G5_lamT1e-3` (`t = 5`): `E_prop` reaches `8.18e-06` (median `0.000124`),
  four to five decades below `1`. `t = 5` is the grading that does carry
  the shape (`w = 3`), and the optimizer finds the direction.

That contrast is a check on the parametrization, not evidence about the
Jacobian conjecture: `E_prop` small is a necessary shape condition on the
leading forms and nothing more, and the `t = 5` arm's `E_K` is the
*worst* of the three (median `4.79e-05` against `6.41e-06` on `G15_lamT0`).

## 5. The ten deepest stalls

Coefficient vectors are in `night11/stalls/*.npz` (keys: `c`, `dP`,
`dQ`, `t`, `aP`, `aQ`, `EK`, `ET`, `arm`, `seed`). No lifting was
attempted, per the v0 brief.

| # | arm | seed | family | E_K | E_T | E_prop | grad norm of E_K | Jacobian norm | passes/iters |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `G15_lamT1e-3` | 110043 | vsteep | **1.99963e-09** | 1 | 1 | 0.000185 | 1 | 1/4000 |
| 2 | `G15_lamT0` | 110043 | vsteep | **2.11917e-09** | 0 | 0 | 0.000121 | 1 | 1/4000 |
| 3 | `G15_lamT0` | 110095 | vsteep | **2.42779e-09** | 0 | 0 | 0.000203 | 1 | 1/4000 |
| 4 | `G15_lamT1e-3` | 110015 | vsteep | **3.14047e-09** | 1 | 1 | 0.000327 | 1 | 1/4000 |
| 5 | `G15_lamT1e-3` | 110095 | vsteep | **3.44462e-09** | 1 | 1 | 0.000161 | 1 | 1/4000 |
| 6 | `G15_lamT1e-3` | 110019 | vsteep | **3.94275e-09** | 1 | 1 | 0.000268 | 1 | 1/4000 |
| 7 | `G15_lamT0` | 110015 | vsteep | **4.20802e-09** | 0 | 0 | 0.000476 | 1 | 1/4000 |
| 8 | `G15_lamT0` | 110091 | vsteep | **5.12565e-09** | 0 | 0 | 0.000146 | 1 | 1/4000 |
| 9 | `G15_lamT1e-3` | 110091 | vsteep | **5.83003e-09** | 1 | 1 | 0.000552 | 1 | 1/4000 |
| 10 | `G15_lamT0` | 110107 | vsteep | **7.56109e-09** | 0 | 0 | 0.000365 | 1 | 1/4000 |

Profiles (all post-hoc; none of this is in the objective):

| # | residual constant `R[0,0]` | \|P_top\| | \|Q_top\| | Sylvester log10 cond | max abs coeff | total degrees carrying most residual mass |
|---|---|---|---|---|---|---|
| 1 | -8.793e-07 | 4.243e-05 | 2.671e-06 | 295.82 | 1.008 | 170 (8.3e-11), 161 (7.7e-11), 153 (7.3e-11), 156 (7.3e-11) |
| 2 | 4.238e-07 | 1.248e-05 | 2.395e-06 | 295.29 | 1.008 | 164 (1.2e-10), 163 (1e-10), 168 (8.8e-11), 158 (8.4e-11) |
| 3 | -1.305e-06 | 4.834e-05 | 1.576e-06 | 295.95 | 1.159 | 149 (1.8e-10), 157 (1.4e-10), 141 (1.3e-10), 161 (1.3e-10) |
| 4 | 1.964e-07 | 1.878e-05 | 2.909e-06 | 295.57 | 1.103 | 139 (1.6e-10), 144 (1.4e-10), 145 (1.3e-10), 158 (1.3e-10) |
| 5 | -2.484e-06 | 3.826e-05 | 2.059e-06 | 295.84 | 1.159 | 157 (1.9e-10), 163 (1.7e-10), 147 (1.5e-10), 149 (1.4e-10) |
| 6 | 3.226e-06 | 8.945e-05 | 8.831e-07 | 296.03 | 1.025 | 149 (1.8e-10), 146 (1.5e-10), 151 (1.4e-10), 156 (1.2e-10) |
| 7 | -8.908e-07 | 2.719e-05 | 2.02e-06 | 295.46 | 1.1 | 145 (2e-10), 155 (1.8e-10), 136 (1.6e-10), 144 (1.6e-10) |
| 8 | 6.507e-07 | 3.042e-05 | 2.065e-06 | 295.63 | 1.016 | 169 (2.6e-10), 170 (2.3e-10), 171 (2.1e-10), 161 (2.1e-10) |
| 9 | -3.827e-07 | 2.99e-05 | 3.608e-06 | 295.58 | 1.016 | 174 (4.8e-10), 167 (3.1e-10), 161 (2.3e-10), 169 (2.2e-10) |
| 10 | 4.218e-07 | 7.36e-05 | 3.657e-06 | 295.89 | 1.192 | 171 (3.5e-10), 172 (3.2e-10), 160 (3.1e-10), 146 (2.9e-10) |

`R[0,0]` is the residual in the constant coefficient: a value near 0
means the seed did fit the Keller constant `1`; a value near `-1` means
it did not and the pair sits at or near the degenerate `Jacobian = 0`
locus.

## 6. Post-hoc diagnostics on the five deepest stalls

Run by `diag.py` after the net, on the saved `.npz` vectors only.
Neither experiment feeds back into the search.

### D1 -- Sylvester singular values of the two leading forms

Sylvester matrix of `P_top`, `Q_top` dehomogenised in one variable;
a small `sigma_min` relative to `sigma_max` would be the numerical
shadow of a common root of the two leading forms.

| # | file | E_K | Sylvester dim | sigma_max | sigma_min | log10 cond | five smallest sigma |
|---|---|---|---|---|---|---|---|
| 1 | `stall_01_G15_lamT1e-3_seed110043.npz` | 1.99963e-09 | 195 | 6.634e-05 | 0 | 295.82 | 0, 0, 0, 0, 0 |
| 2 | `stall_02_G15_lamT0_seed110043.npz` | 2.11917e-09 | 195 | 1.97e-05 | 0 | 295.29 | 0, 0, 0, 0, 0 |
| 3 | `stall_03_G15_lamT0_seed110095.npz` | 2.42779e-09 | 195 | 8.877e-05 | 0 | 295.95 | 0, 0, 0, 0, 0 |
| 4 | `stall_04_G15_lamT1e-3_seed110015.npz` | 3.14047e-09 | 195 | 3.679e-05 | 0 | 295.57 | 0, 0, 0, 0, 0 |
| 5 | `stall_05_G15_lamT1e-3_seed110095.npz` | 3.44462e-09 | 195 | 6.861e-05 | 0 | 295.84 | 0, 0, 0, 0, 0 |

**The diagnostic is void on the primary arm, and the null model is
what shows it.** Running the same diagnostic at *random* points of
the same graded support gives:

| arm grading | Sylvester dim | `sigma_min` at 5 random points | `x^k` dividing `P_top`, `Q_top` | `y^k` dividing `P_top`, `Q_top` |
|---|---|---|---|---|
| `t = 15` (aP=1, aQ=14) | 195 | 0, 0, 0, 0, 0 | 5, 10 | 4, 11 |

On `t = 15` the grading puts `P_top` on exponents `i = 5, 20, ..., 80`
and `Q_top` on `i = 10, 25, ..., 115`, so `x^5 | P_top` and
`x^10 | Q_top` **for every point of that support**. The two leading
forms therefore share the factor `x` identically on the whole arm,
the dehomogenised Sylvester matrix is exactly singular everywhere on
it, and `sigma_min = 0` at the stalls is a property of the
parametrization, not of the stalls. The `log10 cond ~ 296` column is
just `log10(sigma_max / 1e-300)` from the divide-by-zero guard and
should be read as `infinity`, not as a large finite number.

So D1 as posed measures nothing on the primary arm. Recorded as a
negative result about the diagnostic. On `t = 5` the shared factor is
`y` rather than `x`, which the one-variable dehomogenisation absorbs
as a degree drop, and `sigma_min` there is nonzero at random points;
no `t = 5` seed reached the ten deepest stalls, so no `t = 5` stall
was available to run it on. A diagnostic that would carry information
here has to divide out the forced monomial factors first, or work
with the homogeneous resultant of the two forms directly.

### D2 -- rational-reconstruction experiment (labelled experiment)

**This is an experiment, not a lifting step, and its expected
outcome is a nonzero exact residual.** For each stall the six
dominant coefficients (largest `|c|`) were passed through
`sympy.nsimplify(..., rational=True, tolerance=1e-6)`; any
reconstruction with denominator `<= 1e6` was substituted back. Every
remaining coefficient was taken as the exact dyadic rational the
float already is, so the whole vector is exactly rational and the
bracket `B = P_x Q_y - P_y Q_x` was formed exactly over `Q` by
`Fraction` convolution. The table records the exact residual
`B - 1`.

| # | dominant coeffs attempted | substituted | exact residual: nonzero cells | exact `R[0,0]` | max abs exact coeff | identically zero? |
|---|---|---|---|---|---|---|
| 1 | 6 | 6 | 1463 | `-206657/235014334152` | 6.574e-06 | no |
| 2 | 6 | 6 | 1463 | `32845/77497549916` | 9.128e-06 | no |
| 3 | 6 | 6 | 1463 | `-526720/403658681613` | 9.731e-06 | no |
| 4 | 6 | 6 | 1463 | `50888/259090176265` | 1.162e-05 | no |
| 5 | 6 | 6 | 1463 | `-812069/326903412444` | 1.014e-05 | no |

Reconstructions attempted, per stall:

| # | coefficient index | float value | nsimplify output | \|error\| | substituted |
|---|---|---|---|---|---|
| 1 | 245 | 1.00775696638 | `970995/963521` | 2.6e-12 | yes |
| 1 | 5 | 0.992301868433 | `726103/731736` | 4.56e-13 | yes |
| 1 | 254 | -0.0427428473964 | `-29068/680067` | 5.04e-13 | yes |
| 1 | 11 | 0.0420872674982 | `6967/165537` | 8.61e-13 | yes |
| 1 | 263 | 0.0225096853129 | `3736/165973` | 2.59e-12 | yes |
| 1 | 17 | -0.0203793639914 | `-15929/781624` | 4.94e-13 | yes |
| 2 | 245 | 1.00767159469 | `627201/622426` | 6.4e-13 | yes |
| 2 | 5 | 0.992387231201 | `864927/871562` | 5.03e-13 | yes |
| 2 | 254 | -0.0427470248588 | `-38237/894495` | 1.18e-12 | yes |
| 2 | 11 | 0.0420989015024 | `24102/572509` | 3.92e-13 | yes |
| 2 | 263 | 0.0225535786941 | `10311/457178` | 4.53e-13 | yes |
| 2 | 17 | -0.02042546279 | `-17855/874154` | 3.22e-13 | yes |
| 3 | 5 | -1.15930599662 | `-624619/538787` | 1.71e-14 | yes |
| 3 | 245 | -0.862583906278 | `-646247/749199` | 8.09e-13 | yes |
| 3 | 11 | 0.396732369557 | `396413/999195` | 5.2e-13 | yes |
| 3 | 254 | -0.295189594684 | `-166765/564942` | 1.93e-13 | yes |
| 3 | 263 | -0.124050180052 | `-15950/128577` | 4.14e-12 | yes |
| 3 | 23 | -0.0811718631937 | `-32769/403699` | 1.42e-12 | yes |
| 4 | 245 | -1.10279959846 | `-346053/313795` | 2.83e-13 | yes |
| 4 | 5 | -0.906783243125 | `-748701/825667` | 1.67e-12 | yes |
| 4 | 272 | -0.201300130351 | `-11891/59071` | 9.49e-13 | yes |
| 4 | 23 | 0.166431880544 | `126887/762396` | 7.99e-13 | yes |
| 4 | 263 | -0.11529546035 | `-94354/818367` | 8.29e-14 | yes |
| 4 | 17 | 0.0947812831674 | `11876/125299` | 3.28e-12 | yes |
| 5 | 5 | -1.15902600394 | `-822650/709777` | 1.43e-12 | yes |
| 5 | 245 | -0.862791268247 | `-794755/921144` | 1.62e-12 | yes |
| 5 | 11 | 0.396246297914 | `351203/886325` | 1.33e-12 | yes |
| 5 | 254 | -0.294970399052 | `-293815/996083` | 1.1e-12 | yes |
| 5 | 263 | -0.123921470083 | `-66081/533249` | 2.99e-13 | yes |
| 5 | 23 | -0.0810627003217 | `-80933/998400` | 1.24e-12 | yes |

Stalls whose exact residual is identically zero over `Q`: **0**.

That is the expected outcome and it is the only thing the
experiment establishes: these float points are not exact
solutions, and nothing about the size of `E_K` at them says
otherwise. `nsimplify` at tolerance `1e-6` will return *some*
small-denominator rational for almost any float, so a successful
reconstruction of an individual coefficient is not a signal.

## 7. Files

| file | contents |
|---|---|
| `polykit.py` | float64 polynomial kernel: FFT product/correlation, Keller residual and its exact analytic gradient (4 forward + 5 inverse real FFTs per objective+gradient call), tear proxy and gradient, Sylvester diagnostic |
| `supports.py` | support design and the swappable objective |
| `opt.py` | descent driver (L-BFGS-B with relative tolerances off, restarts; Adam fallback) |
| `controls.py`, `controls.json`, `controls_log.txt` | N1/N2/N3 |
| `net.py`, `net_results.json`, `net_log.txt` | the search; one record per seed |
| `stalls/*.npz` | coefficient vectors of the ten deepest stalls |
| `report.py` | builds this file |
| `diag.py`, `diag_results.json` | post-hoc D1/D2 diagnostics on the deepest stalls |

