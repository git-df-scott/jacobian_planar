# night11 -- numeric net (v0): PAUSED

State at pause. Nothing here is a result; the search itself has not been run.

## What is built and in the tree

- `polykit.py` -- float64 polynomial kernel: FFT convolution/correlation, the
  Keller residual `R = P_x Q_y - P_y Q_x - 1` and its exact analytic gradient
  (one fused routine, 4 forward + 5 inverse real FFTs per objective+gradient
  call), the tear proxy `E_T` and its gradient, and a post-hoc Sylvester
  singular-value diagnostic.
- `supports.py` -- support design and the swappable objective
  `E = E_K + lambda_T * E_T`.
- `controls.py` -- controls N1 / N2 / N3.
- `net.py` -- the many-restart driver (multiprocessing over 4 cores).

## Measured / derived before the pause

1. **Timing.** One objective+gradient call at degrees (84,126) costs ~11 ms
   before the FFT fusion (18 transforms); the fused path uses 9. A single
   2000-iteration L-BFGS-B restart took 99 s unfused.

2. **A support-design error was found and corrected by measurement.** The first
   design put both `P` and `Q` in the sublattice `L_t = {i-j = 0 mod t}`
   (t = 16, 745 parameters). Every seed run in that support drove `E_K` to
   `1.0000000` with `||P_x Q_y - P_y Q_x|| ~ 2e-4`. Reason: the (0,0)
   coefficient of the Jacobian is exactly `P[1,0] Q[0,1] - P[0,1] Q[1,0]`, and
   `(1,0)`, `(0,1)` are not in `L_16`, so the constant 1 is unreachable and
   `E_K >= 1` identically on that support.

3. **Corrected design: torus grading by cosets.** `P` and `Q` are taken
   semi-invariant of weights `aP`, `aQ` under `(x,y) -> (zeta x, zeta^-1 y)`,
   `zeta^t = 1`, with `aP + aQ = 0 (mod t)`. The Keller constant forces
   `aP = 1`, `aQ = -1 (mod t)`.

4. **Grading arithmetic (recorded as a derivation, not a result).** If the
   leading forms are additionally to have the `(H^2, H^3)` shape, one needs a
   weight `w` with `2w = aP`, `3w = aQ (mod t)`; with `aP = 1`, `aQ = -1` this
   forces `t | 5`. So `t = 5` (`w = 3`) is the only nontrivial torus grading
   carrying both conditions. Its parameter count is 2357, above the 300-800
   band that was asked for; `t = 15` (`aP = 1`, `aQ = 14`) lands in the band at
   788 parameters but cannot support the `(H^2, H^3)` shape.

   | arm | t | aP,aQ | params (P + Q) | residual cells | top-form dims |
   |---|---|---|---|---|---|
   | GRADED-5  | 5  | 1, 4  | 731 + 1626 = 2357 | 4389 | 17, 26 |
   | GRADED-15 | 15 | 1, 14 | 245 + 543 = 788 | 1463 | 6, 8 |
   | FULL (controls only) | 1 | - | 3655 + 8128 = 11783 | 21945 | 85, 127 |

   Unknowns / equations is ~0.537 in every arm: both counts scale like 1/t, so
   the grading is a resolution knob only, not a knob on over-determination.

5. **Degree shape (84,126) carries no automorphism.** By Jung-van der Kulk the
   two degrees of a planar polynomial automorphism are divisibility-ordered,
   and 84 does not divide 126 nor conversely. Control N2 is therefore run at
   (84,168), the nearest same-scale shape that does carry one.

## Not yet done

- Controls N1/N2/N3 have not completed a clean run (last attempt died on a
  slicing bug in the N1 fused-vs-reference comparison, now fixed; not re-run).
- The net itself has not been run: no seeds, no classification tally, no stall
  histogram. `stalls/` is empty and there is no `NUMERIC_NET.md`.
