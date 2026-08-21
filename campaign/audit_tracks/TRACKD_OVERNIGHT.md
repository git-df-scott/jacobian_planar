# Overnight state — what is running and how to read it in the morning

## Running (pure compute, no token use)

| job | log | what it decides |
|---|---|---|
| `trackD_solve.py 420 167` | `$SCRATCH/solve.out` | the 167 tight, ≥125, twice-surviving shapes, one Singular `facstd` each, 420 s cap |
| `trackD_extract.py case2_quad case1_pent` | `$SCRATCH/facstd_cal.out` | calibration: case (2) must come back EMPTY, case (1) must not |
| `_c2_oneshot.py 0` | `$SCRATCH/oneshot_q.out` | the characteristic-0 attempt on case (2) |

Read the solver with:

```
grep -c 'VERDICT: EMPTY' $SCRATCH/solve.out     # shapes killed
grep -B4 'live component' $SCRATCH/solve.out    # anything that SURVIVED
```

**A surviving component is the only thing that matters.** `live component: dim 0,
vdim N` on a target means a finite, non-degenerate point set exists for that
reduced polygon pair — the first genuine counterexample candidate the pipeline
has produced. Everything so far is EMPTY.

## Status at hand-off

- 20 / 167 decided, **20 EMPTY, 0 live**.
- The remainder are larger; the 420 s cap means some will TIMEOUT rather than
  answer. A timeout is *not* a verdict.

## The retraction that matters

The previous report said full Gröbner extraction "times out at 240 s even on
case (2)" and concluded brute force does not scale. **That run was buggy, not
hard.** The condition loop used `deg(t)`, which in Singular is the *total*
degree, so it overran `coeffs(t,x)` (exactly `deg_x(t)+1` rows) and Singular
errored on every row past the end. Driving the loop off `nrows(coeffs(t,x))`
fixes it, and the smallest targets then decide in ~0 s. Case (2) itself is
still slow under `facstd`, so the corrected statement is narrower: *the small
shapes are easy; case (2) is not.*

## Why not triangular decomposition

Considered and rejected on the merits, not skipped. `triangMH` (and the regular
-chains route generally) needs a **lex Gröbner basis of a zero-dimensional
ideal as input** — which is the expensive step that was the wall in the first
place. It reorganises the answer after the hard work is done. `facstd`
(factorizing Gröbner) attacks the actual cost: it splits the ideal into
components as it goes, so a system collapsing to `(1)` on every branch never
builds one dense basis. That is what made the targets tractable.

## Not delivered

No counterexample. Nothing has reached the lifting or packaging stage, because
nothing has survived elimination. If the overnight run turns up a live
component, the next steps are in order: exact ℚ-lift of that point set, the
`ε_P + ε_Q = (r+1,1)` check (automatic by construction, so a bug-catcher), and
assembly of explicit `P, Q` with a direct `[P,Q] = x^r` verification.
