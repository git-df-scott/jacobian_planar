# H1b task 2 — reformulation via the affine reduction (approach (b))

**Chosen over (a)** because it attacks the measured obstruction directly and
rests on something proved by exact test this session rather than ported by
analogy. Outcome: the reduction is only *partial*, but pursuing it **overturned
a load-bearing assumption** and opened an export path the campaign did not have.

## 1. The affine reduction is partial, not total

Step 2b proved each level `j = 13..17` is affine in its **own** newest slice.
That is not the same as the block being **jointly** affine in the 13 late
parameters `P_12..P_16` — `xy` is affine in `x` and in `y` and not in `(x,y)`.
Measured jointly, by degree along a random line inside the 13-dimensional late
subspace:

| levels | degree in the late block |
|---|---|
| 13, 14, 15 | **0** — the late parameters *do not appear at all* |
| 16, 17 | 0, 1 |
| 18 … 24 | 1 |
| ≥ 25 (termination) | **2, 3** |

So the system is affine in the late block **through level 24 only**; the
termination conditions are quadratic and cubic in it. A clean linear elimination
of all 13 late parameters is therefore **not** available for the whole system.

This also sharpens step 2b's wording: at levels 13–15 the conditions are not
merely *affine* in the newest slice, they are **independent** of it — exactly
what `trackB1_yadic_rank.py` warned about ("the i = 0 condition at j = 13 is
untouched by P_12, because N(P) forces P_12 to have i ≥ 4").

And the reduction does not pay for itself: the surviving conditions have degree
**10 … 21+ in the early parameters, with 45 of them above degree 30**. Removing
13 variables raises the degree in the 45 that remain.

## 2. The finding that matters: the conditions are SPARSE

Step 2c concluded — and this session's earlier commit and PR body both asserted
— that a degree-12 form in 61 variables admits ~10¹⁴ monomials, so *"these
conditions cannot be written down."* **That was wrong.** It used the *dense*
bound as if it were the actual count. Measured, by running the recursion
symbolically over `F_p[parameters]` with the gauges `p_00 = 0`, `p_10 = 1` (so
no denominators appear):

| level j | max monomials in one x-coefficient | total |
|---|---|---|
| 13 | **686** | 3,394 |
| 17 | 4,585 | 26,115 |
| 20 | 17,134 | 107,690 |
| 23 | 59,626 | 411,878 |
| 26 | 199,017 | 1,474,753 |

Growth is ~1.5× per level. At level 13 the true count is **686**, eleven orders
of magnitude below the dense bound. The whole build to level 26 takes 148 s.

**The conditions can be written down.** The obstruction the campaign has treated
as structural — and which I repeated before measuring — is not there.

## 3. What that unlocks: a sound route to EMPTY

Emptiness is **monotone**: if any *subset* of the conditions has no common zero,
the full system has none. So exporting levels 13..J for increasing J and testing
each is a sound path to a verdict, and the smallest J that closes is the cheapest
verdict available.

Exported (`w1_h1b_export.py`, reproducible):

| file | conditions | monomials | size | build |
|---|---|---|---|---|
| `pent_L15.ms` | 6 | 7,581 | 0.3 MB | <1 s |
| `pent_L17.ms` | 15 | 38,734 | 1.4 MB | 1 s |
| `pent_L18.ms` | 21 | 75,382 | 2.7 MB | 2 s |
| `pent_L23.ms` | **66** | **1,080,147** | 43.2 MB | 30 s |

`pent_L23.ms` is the near-square subsystem: 66 conditions against 58 essential
parameters (61 lattice coefficients minus the three gauges).

**Calibration so far.** msolve on the small subsystems is the wrong shape —
6 conditions in 59 variables is a ~53-dimensional variety, and msolve ran past
10 minutes without returning. Only the near-square system can plausibly close.
`pent_L23.ms` is running under a bounded budget; its result is recorded
separately.

## 4. Gauge caveat, stated not absorbed

The export imposes `p_00 = 0` and `p_10 = 1`. The second encodes `p_10 ≠ 0`,
which the y-adic recursion requires anyway (it divides by `p_10`). **An EMPTY
verdict from these files therefore covers the `p_10 ≠ 0` chart only.** The
`p_10 = 0` locus is a separate branch and must be closed on its own before any
claim about the pentagons as a whole. Recorded, not silently absorbed.

A third gauge (the coordinate scale `(x,y) → (λx, λ⁻³y)`, found in step 3c)
remains unfixed in the export. That costs nothing for an EMPTY verdict — a
residual gauge only means solutions come in orbits — but it means the exported
system is not as tight as it could be.

## 5. Status

Approach (b) did **not** deliver the clean linear elimination it promised. It
delivered something more useful: the measurement that the conditions are
writable, and the first exportable pentagon systems in the campaign's history.
Whether any engine closes them is now an experiment rather than an assumption.
