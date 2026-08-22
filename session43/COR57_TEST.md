# The independent test of GGHV Corollary 5.7 — status

## Why this target

`AUDIT_EOD.md` §9: the two `p108` sliver shapes **are** GGHV Prop 4.1's reduced
(9,27) polygons, and their emptiness **is** Corollary 5.7 — which the campaign's
own ledger records as *"proved there via the Sec 5 / Thm 5.1 degree apparatus
that was never re-derived by anyone."*  The audit (`EXCLUSION_AUDIT_SUMMARY.md`)
confirms: statement and proof architecture verified, but Cor 5.7 rests on an
imported Corollary 7.2 from GGV 2017 that nobody re-checked, and there is **no
third-party replication and no erratum anywhere**.

Pre-registered standards (from the campaign, unchanged):
EMPTY at one prime = replication-grade evidence, not a char-0 proof.
Non-empty = needs the full tower and a char-0 lift before the word refutation.

## Finding 1: the recorded TIMEOUTs were structural

    wave6/ms/p108_192622.ms : 40 vars, grading-torus rank 5
    wave6/ms/p108_525122.ms : 28 vars, grading-torus rank 5

Both **positive-dimensional**.  msolve's solve mode requires a zero-dimensional
input, so the 1800 s TIMEOUTs logged against them ("UNDECIDED, requeue
overnight") could never have resolved, at any budget — the same diagnosis as the
pentagon.  This is worth having independently of the verdict: it means the
existing `SLIVER_STATUS.txt` entries are non-verdicts for a structural reason,
not a resource one.

## Finding 2: slicing was necessary but NOT sufficient here

Sliced both along the torus, with gauge validity checked (weight-minor
determinants `-1/24` and `-1/14`, both nonzero, so setting those variables to 1
is a legitimate chart):

| system | engine | budget | outcome |
|---|---|---|---|
| `p108_192622_sliced` | msolve `-t 2` | 1500 s | exit 124, 0 bytes — **NO VERDICT** |
| `p108_525122_sliced` | msolve `-t 2` | 1500 s | exit 137 (OOM) at 715 s, 0 bytes — **NO VERDICT** |

Last night the rank-5 *resister* systems decided **instantly** once sliced.
These did not.  Recorded plainly: the rank-5 diagnosis explains why the original
runs could not terminate, but removing five dimensions does not by itself make
these two decidable.  They are simply bigger objects (1.6 MB and 1.4 MB).

Singular on the sliced shape 2 (28 vars, the smaller one, and the one msolve
OOM'd on):

| system | engine | budget | outcome |
|---|---|---|---|
| `p108_525122_sliced` | Singular `slimgb` | 2400 s | exit 124, "halt 1", 0 bytes — **NO VERDICT** |

So **both engines, on the sliced system, at 25–40 minute budgets**: undecided.
Peak memory stayed at ~320 MB, so this is a time wall, matching every other
degree-2 system today.

Still untried: `msolve -g 2` (Groebner-only), which decides emptiness at *any*
dimension and is cheaper than solve mode — the right tool given that Cor 5.7's
claim IS emptiness.  Also untried: the `v = 0` strata, which a single chart does
not cover.

## Status

`VERDICT: NO VERDICT` on Cor 5.7's independent test.  It remains the single
highest-value unverified exclusion in the campaign, and it is now at least
correctly posed.
