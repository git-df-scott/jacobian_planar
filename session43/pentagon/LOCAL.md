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

## Retraction: the higher-order lift test is unsound (caught by its own control)

I built an order-by-order deformation lift (`lift.py`) and ran it on all 28
tangent directions at family B.  It reported **0 of 28 surviving to order 8**,
which would have been a strong local-rigidity statement.

**That result is retracted.**  The control refutes it: the tangent direction of
family B itself — `d/dlambda` at `lambda = 1`, i.e.
`(p_1_1, p_2_0, p_3_0) -> (1, 1, 2/3)` — is by construction tangent to a curve
that lies in the variety, and the exact family points at `lambda = 2, 3, 6` do
satisfy 66/66 conditions.  The lift code nevertheless reports it **obstructed at
order 4**.

Cause: at each order the correction `w_k` solving `J w_k = -(residual)_k` is
determined only **modulo the kernel of J**, and the kernel here is
28-dimensional.  My implementation takes one particular solution greedily, and a
wrong choice at order k manufactures an obstruction at order k+1.  A correct
test has to carry that freedom forward — i.e. compute the obstruction map on the
whole tangent cone, not along one greedily-chosen lift.

**What survives, and what does not:**

- **Sound:** the order-2 test.  Checking whether the second-order term lies in
  `image(J)` is a genuine necessary condition, and it is choice-independent
  because nothing has been chosen yet.  So **23 of the 28 directions are
  genuinely obstructed at order 2**, and at most 5 can be tangent to curves.
- **Unsound:** everything the greedy lift said beyond order 2, including the
  headline "0 of 28".  At least one of the 5 (the family direction) is a real
  curve, so the true count of unobstructed directions is at least 1.
- Also **unaffected** and still standing: `p_16_8` does not appear anywhere in
  the tangent space, so no first-order deformation of family B reaches the
  saturation vertex.

Recorded rather than quietly deleted, because a lift that reports false
obstructions is exactly the kind of instrument that produces a confident wrong
answer, and the campaign's ledger exists for this class of error (`CATCHES.md`
class (v): certifiers that cannot fail — this is its mirror image, a certifier
that fails when it should not).
