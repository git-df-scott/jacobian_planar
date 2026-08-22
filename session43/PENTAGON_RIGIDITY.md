# The pentagon system was never rigid: residual torus rank 1

**Session 43, 2026-08-22. Verified by exact nullspace computation.**

## The finding

`wave1/pent_L23.ms` (59 vars, 66 conditions, p=1000003) carries a
**grading torus of rank 2**, computed as the exact rational nullspace of the
stacked matrix of monomial-exponent differences (every reported weight vector
re-verified: <w,e> is constant across the monomials of each generator).

The campaign's `gauges = 3` export adds the single generator `p_1_0 - 1`.
`pent/RUNLOG_NOTES.md` states the reason:

> Without it the variety contains a one-dimensional gauge orbit through every
> point and cannot be zero-dimensional, which is what msolve's solve mode
> needs; with it the system is rigid.

**Measured: with `p_1_0 - 1` added, the residual torus rank is 1, not 0.**

    raw pent_L23.ms                      torus rank 2
    + p_1_0 - 1        (campaign gauge)  torus rank 1   <-- NOT rigid
    + p_1_0 - 1, p_1_1 - 1               torus rank 0   <-- rigid

The residual weight vector has **all positive weights** on the other 58
coordinates (p_1_1 -> 1, p_2_0 -> 1, ... p_16_8 -> 23), with p_1_0 of weight 0.

## Consequence for every prior pentagon run

A variety invariant under a positive-dimensional torus contains a
1-dimensional orbit through every non-degenerate point, so it is **not
zero-dimensional**.  msolve's solve mode requires a zero-dimensional input.

Therefore the recorded pentagon failures

    pent_L18_g3.ms   exit -9 (SIGKILL/OOM)  1798.9 s  6.2 GB
    pent_L18_g2.ms   TIMEOUT                3600.1 s
    wave1 L23        exit 137               13.9 GB
    job #1 / job #2  90 min timeout, OOM at 3.5 / 5.0 GiB caps

were **structurally incapable of returning a solution**, independently of
memory or time budget.  They are NO VERDICT, and their cost was not evidence
about the mathematics.  This is a Challenger-class finding: one small local
misdiagnosis (one gauge believed sufficient, two required) controlled the
failure of the campaign's most promising object.

## What this does NOT claim

- It does **not** claim the pentagon variety is nonempty.  Rank 0 only makes
  the question well-posed for the solver.
- The chart `{p_1_0 != 0, p_1_1 != 0}` is one chart.  A complete decomposition
  needs the strata `p_1_1 = 0` (with p_1_0 = 1) and `p_1_0 = 0`, each of which
  must be re-profiled for its own residual torus and rigidified separately.
  Systems for all three are built (`pentA_rigid`, `pentB_p11zero`,
  `pentC_p10zero`).
- `p_1_0 = 0` in particular has **never been exported or searched** by the
  campaign; `pent/pent_slice.py` says so explicitly ("the p_10 = 0 chart is a
  different export and is not covered by this file").

## Second finding: the random-slice search cannot find a low-dimensional witness

`pent/pent_slice.py` fixes r = 45 of 58 parameters to **uniformly random**
values in F_p and solves.  A random affine subspace of codimension r meets a
variety of dimension d only if d >= r.  If the pentagon variety is
0-dimensional or of small positive dimension -- which the campaign's own
bottom-edge result (degree-9 eliminant, dim 0 in chart c2=1) makes likely --
then **no random slice at r = 45 can ever meet it**, and every EMPTY it
returns is uninformative by construction.

Its controls are sound and pass (S-POS `[1, 59, -1, []]` non-empty, S-NEG
`[-1]` empty), so the instrument is honest; it is aimed wrongly.  The
asymmetry it relies on (a point of a slice IS a point of the full system) is
correct and still worth using -- but at codimension at or below the variety's
dimension, or through a locus derived from necessary conditions, not through
uniformly random points.

## Status of the runs this finding enables

See `VERDICTS.md` for the ledger.  Verdict language: EMPTY / NONEMPTY /
NO VERDICT, with timeout, OOM, segfault and empty output all NO VERDICT.
