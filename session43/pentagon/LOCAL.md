# Local structure at the two families

Tangent spaces computed from the exact Jacobian of the 66 conditions (each
partial derivative obtained by exact univariate interpolation, not finite
differences), at points verified to lie on the variety.

| point | rank J | dim tangent space | dim of the known family |
|---|---|---|---|
| family A, two random `(a,b,c,d)` | 51 | **8** | 4 |
| family B, `lambda = 1` and `7` | 31 | **28** | 1 |

Both points are therefore **very singular**: the tangent space is much larger
than the family through them (8 vs 4, and 28 vs 1).

## What the tangent space at family B contains

Of the 47 variables carrying a nonzero component across the 28-dimensional
kernel, **32 have x-degree `i >= 2`**.  So first-order deformations out of the
affine-in-x locus do exist, which is exactly what the earlier one-coefficient
sweep could not have detected — that sweep moved a single coordinate, and these
directions move many at once.  Recorded as a genuine gap in the earlier
evidence.

Two things are true nonetheless:

1. **`p_16_8` does not appear in the tangent space at all.**  No first-order
   deformation of family B reaches the pentagon vertex that the saturation
   requires.
2. **None of the 28 directions gives a line inside the variety.**  Testing
   `pt + t v` at `t = 1,2,3` for each basis direction: 0 of 28 keep all 66
   conditions vanishing.

## How much this is worth

Statement 2 is weaker than it looks and should not be read as "obstructed at
second order" in the deformation-theory sense.  It shows only that no *straight
line* in those directions lies in the variety; a curved arc tangent to one of
them could still exist, and a proper test would compute the formal obstruction
order by order.  So this is **evidence, not proof**.

Taken together with statement 1, the picture is that the families sit at deeply
singular points with a large but almost entirely obstructed tangent cone, and
that the saturation vertex is not reachable to first order.  That is consistent
with the saturated system being EMPTY, which is the outcome the campaign was
originally trying to establish — but by a completely different route from the
one it attempted, and it is not established here.

`NO VERDICT` on the saturated question.
