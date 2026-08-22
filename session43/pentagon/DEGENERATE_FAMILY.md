# The pentagon system's solution set contains a 4-parameter degenerate family

Verified symbolically and numerically.  This supersedes the single witness in
`WITNESS.md`: that point is one member of a whole family.

## Statement

For **any** polynomial `f(y)` with `deg f <= 5`,

    P(x,y) = x + f(y)
    Q(x,y) = integral_0^y ( x + f(y) - f(s) )^2 ds

satisfies

    {P,Q} = P_x Q_y - P_y Q_x = x^2        (symbolic, exact)

and `Q` has y-degree `2 deg f + 1 <= 11 < 13`, so **every** condition
`Q[j][i] = 0` for `j = 13..23` holds identically.  With the campaign gauge
`p_1_0 = 1`, i.e. `f(y) = y + a y^2 + b y^3 + c y^4 + d y^5`, this is a
**4-parameter family of solutions** of `wave1/pent_L23.ms`.

Mechanism: `u = P = x + f(y)` is a first integral, and in coordinates `(u,y)`
the equation collapses to `Q_y|_u = (u - f(y))^2`, which integrates for any `f`.
The Newton-polygon conditions never bite because Q dies at y-degree `2 deg f+1`.

## Confirmations

| check | result |
|---|---|
| random `a,b,c,d`, all 66 conditions, 3 trials | **66/66 vanish every time** |
| same but with `y^6` added (`p_6_0 != 0`) | 65/66 -- exactly one condition breaks |
| symbolic `{P,Q}` for general `f` of degree 5 | **`x^2`** |
| y-degree of Q | 11, as predicted by `2 deg f + 1` |

The `y^6` boundary is not a coincidence: `deg f = 6` gives Q y-degree 13, which
is precisely the first constrained level.  The one condition that breaks is the
level-13 one.

## Why this closes the interpretation of every prior pentagon run

The variety is **nonempty and at least 4-dimensional**, before even counting the
rank-2 grading torus.  msolve's solve mode requires a zero-dimensional input.
So the recorded pentagon failures were not close calls:

    pent_L18_g3.ms   exit -9 (OOM)   1798.9 s   6.2 GB
    pent_L18_g2.ms   TIMEOUT         3600.1 s
    wave1 L23        exit 137        13.9 GB
    job #1, job #2   90 min timeout, OOM at 3.5 / 5.0 GiB

Every one is **NO VERDICT**, and no budget would have changed that.

## The oracle now has a real-data positive control

`oracle.py` reports **consistent** at points of this family (rank 13 = 13),
recovers a late-block solution, and the recovered point satisfies all 66
conditions with zero residual.  So the instrument has now returned YES on real
data, not only on a planted right-hand side -- the campaign's planted-witness
rule is satisfied for it.

The recovered solutions all have `p_16_8 = 0`: the family stays degenerate.

## The corrected target

The campaign wants solutions where the pentagon Newton polygon is genuinely
attained.  `P = x + f(y)` has **no x-dependence beyond the linear term** -- every
`p_{j,i}` with `i >= 1` vanishes on the family -- so it is nowhere near a
(72,108) configuration.  The export must be saturated, in Rabinowitsch form
(`z * p_corner - 1 = 0`), after first searching the file for saturation rows
already present.  The natural corner is `p_16_8`, the vertex that fixes the
degree ratio.

**Until that is added, both EMPTY and NONEMPTY on `pent_L23.ms` answer the wrong
question.**

## First evidence on the corrected question

400 early points taken one coordinate off the family (perturbing a single
`p_{j,i}` with `i >= 1`) gave **0 consistent**.  That is evidence, not a proof --
random perturbations miss measure-zero loci, which is the same objection I raised
against the r=45 slice search, and it applies to me here.  Recorded as
`NO VERDICT` on the saturated question.
