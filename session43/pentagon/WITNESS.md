# The exported pentagon system is NONEMPTY, with an exact rational witness

**VERDICT: NONEMPTY.**  Verified against the original `wave1/pent_L23.ms`
polynomials, not merely against my own evaluator, and then in exact
characteristic-zero arithmetic.

## The witness

    p_1_0 = 1,   every other p_{j,i} = 0

i.e.

    P(x,y) = x + y
    Q(x,y) = 1 + x^2 y + x y^2 + y^3/3

Checks, all exact:

- `{P,Q} = P_x Q_y - P_y Q_x = (x^2+2xy+y^2) - (2xy+y^2) = x^2`  **exactly, over Q**.
- `Q` terminates at `y^3`, so `Q_j = 0` for every `j >= 4`.  Hence every
  condition `Q[j][i] = 0` for `j = 13..23` holds trivially.
- Substituted into the 66 exported degree-22 polynomials of `pent_L23.ms` at
  p = 1000003: **66/66 vanish.**
- `p_1_0 = 1` is *exactly* the campaign's third gauge (`p_1_0 - 1`), the one
  added in the `g3` exports to make the system "rigid".

## What this means

**"Prove pentagon case (1) EMPTY" is, as exported, false.**  The system is not
empty; it has this solution and, by the torus action (rank 1 after the single
gauge), a positive-dimensional family through it.  Two consequences:

1. Every prior Groebner attack on the pentagon was aimed at a system that is
   **nonempty and positive-dimensional**.  That compounds the rigidity finding
   in `PENTAGON_RIGIDITY.md`: msolve's solve mode needs a zero-dimensional
   input, and here the input is not only positive-dimensional but genuinely
   has solutions.  The recorded OOMs and timeouts
   (`pent_L18_g3` -9 at 1798.9 s / 6.2 GB; `pent_L18_g2` TIMEOUT 3600 s; wave1
   L23 exit 137 at 13.9 GB; the two 90-minute jobs) were never going to
   terminate in a useful state.

2. **The export is missing its non-degeneracy conditions.**  The bottom-edge
   work (`wave6/bottomedge/analyse.py`) is careful about exactly this: it
   classifies seeds by the side conditions `c1, c8, d12 != 0` and discards the
   degenerate ones.  The `pent_L23` export carries no analogue.  Without
   saturation, the variety contains degenerate points like `P = x + y` that are
   nowhere near a (72,108) Newton polygon.

**This is not a counterexample** and must not be read as one.  `P = x + y` has
degree 1; it is the trivial solution of `{P,Q} = x^2`, and its Q terminates long
before the levels the conditions constrain.  It satisfies the exported system
only because that system does not say what it was intended to say.

## What the target should be

The question the campaign wants is the *saturated* one: a solution in which the
pentagon's Newton polygon is genuinely attained.  That needs the corner
coefficients kept nonzero, in the Rabinowitsch form `z * p_corner - 1 = 0`
(your Example 8), with a prior search of the file for saturation rows already
present.  Until that is fixed, both EMPTY and NONEMPTY on `pent_L23.ms` are
answers to the wrong question.

Note also that the witness has `p_1_1 = 0`, so it lies *outside* the rigid chart
`{p_1_0 != 0, p_1_1 != 0}` of `PENTAGON_RIGIDITY.md` and inside the `p_1_1 = 0`
stratum.  The rigid chart may still be empty; that is a separate question and is
still `NO VERDICT`.

## Reproduction

    python3 session43/pentagon/pentev.py      # evaluator, controls in control.py
    # or directly, with no dependence on my code:
    #   substitute p_1_0 = 1 and all other p_{j,i} = 0 into wave1/pent_L23.ms
