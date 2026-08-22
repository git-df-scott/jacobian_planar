# The x-degree <= 2 target (bilinear, saturated)

Both known families have P **affine in x**.  The natural next question is whether
any solution has genuine x-degree 2.  This is that target.

Restrict `P` to `p_{j,i} = 0` for `i >= 3` and build the system in **bilinear**
form (Q kept as unknowns).  Comparison of the two representations of the same
restriction:

| form | size |
|---|---|
| eliminated (degree 22) | 26 vars, 66 conditions, **17.6 MB** |
| **bilinear (degree 2)** | 147 vars, 184 equations, 2,585 terms, **47 KB** |

Saturation excludes the known families by requiring genuine x-degree 2:
`zs * p_10_2 - 1` (and a `p_9_2` variant), on top of the gauge `p_1_0 = 1`.

## Control

Family B at `lambda = 1` lies in this stratum (it has x-degree 1), so it must
satisfy the core equations and must fail the saturation row:

    core equations vanishing : 185/185
    saturation row satisfied : 0/1     (correct - family B has p_10_2 = 0)

**CONTROL PASS.**

## Status

Queued to run when the box frees (Codex's all-vertex-saturated system has it).
`NO VERDICT` until then.  A NONEMPTY here would still have to pass the full
six-vertex non-degeneracy test of `WITNESS.md` before being called a candidate.
