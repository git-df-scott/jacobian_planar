# The bilinear export: 43 MB -> 84 KB, degree 22 -> degree 2

`bilinear.py` re-exports the pentagon system keeping every Q coefficient as an
unknown instead of eliminating it through the recursion.

|  | original `pent_L23.ms` | bilinear form |
|---|---|---|
| variables | 59 | 180 |
| equations | 66 | 184 |
| max total degree | **22** | **2** |
| total monomials | **1,080,147** | **4,736** |
| file size | **43 MB** | **84 KB** |

Same mathematics, 228x fewer terms and degree 2 instead of 22.  This is
Example 14's lesson measured rather than assumed: the low-variable form is the
hard one.

## Why it is equivalent

Each recursion step

    (k+1) q_{k+1,d} = sum_a [ a*(P[a]*Q[b]')_d - (k+1-a)*(P[a]'*Q[b])_d ],  b = k+1-a

is bilinear -- every term is one p times one q.  For (k+1,d) NOT among the
Newton-polygon conditions the equation *defines* `q_{k+1,d}` (its coefficient
is k+1, a unit), so the system is triangular in the q-block and eliminating it
reproduces the original degree-22 export exactly.  For the 66 pairs
(j,i), j = 13..23, i <= j-13, the variable is substituted to zero and the same
equation becomes a *condition* -- which is where the original 66 conditions
come from.  So solutions correspond one-to-one.

## Control

`bilinear.py` runs a positive control: draw a random P, compute Q by the
recursion, and check every one of the 184 bilinear equations.  **PASS** (built
without the zero-substitution, so it tests the encoding and not the conditions).

The first version of this control FAILED with 63 violated equations, because it
imposed `q_{j,i} = 0` while checking against a random P whose recursion Q does
not satisfy those conditions.  The control caught the error in the test, not in
the export -- recorded here because a control that had been written to pass
would have hidden nothing but would also have proved nothing.

## Status

`attack.sh` runs a restart-resilient engine ladder against it: Groebner-only
emptiness (`msolve -g 2`), Singular `slimgb` (sparse low-degree is its regime,
Example 15), then full solve.  Each stage checkpoints to its own `done_*` file.

Results so far: `msolve -t 2 -f bilin_rigid.ms` at a 110 s budget returned
exit 124 with a 0-byte output -- **NO VERDICT**.  The earlier Groebner-only run
on the *original* 43 MB export reached 13 GB of the box's ~14 GB and was killed
at 13 minutes with a 0-byte output -- also **NO VERDICT**, never EMPTY.
