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

## Verdict

`Singular -q` (`slimgb`, `dp`), solo, 13 GB free, 50-minute budget:

    exit 124 (timeout at 3000 s), output "halt 1", no VERDICT line
    peak ~1.5 GB

**VERDICT: NO VERDICT.**  Like Codex's system and unlike my degree-22 saturated
run, this died on **time** with the memory ceiling nowhere in sight.

## The pattern across every saturated attempt tonight

| target | vars | degree | peak | failed on |
|---|---|---|---|---|
| eliminated, `p_16_8`-saturated | 60 | 22 | 13.9 GB | **memory**, 18 min |
| Codex all-vertex-saturated | 186 | 2 | 2.3 GB | **time**, 40 min |
| this x-degree<=2, `p_10_2`-saturated | 148 | 2 | 1.5 GB | **time**, 50 min |

Every degree-2 formulation is time-bound with 85–90% of memory unused.  So the
binding constraint on the corrected target is **Groebner time on a
150–190-variable degree-2 system**, not memory, and the useful lever is a longer
budget or a structural reduction — not a bigger box.  A 3-hour run of the
all-vertex-saturated system is under way on that reasoning.

It also means the analytic route is worth more than the solver route here: the
x-degree <= 1 stratum was settled *exactly* in minutes by reducing the 66
conditions to five explicit equations (`CLASSIFICATION.md`), while every
Groebner attack on its neighbours has returned NO VERDICT.
