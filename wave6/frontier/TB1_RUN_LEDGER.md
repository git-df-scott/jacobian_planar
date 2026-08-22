# trackB1 tier-1 run ledger — night of 2026-08-22

Every attempt on the tier-1 target, with its honest outcome. A run that hit its
wall-clock limit is **NO VERDICT** — not EMPTY, not a hit.

## The target

`wave6/frontier/trackB1_sat_p1000003.ms` — 166 vars, 284 eqs, degree 5, 8,774
terms. Saturated on `c_1_0, c_8_14, d_12_21, s_4_8`. A solution is an
admissible point of pentagon case (1). **NONEMPTY here is the counterexample
candidate.**

Second prime: `campaign/audit_tracks/trackB1_case1_full_p65521.ms`, verified the
same integer system (284/284 equations, all 8,774 coefficients a common lift).
Characteristic zero: `wave6/frontier/trackB1_sat_Q.ms`, verified to reduce to
both primes.

## Earlier attempts, on the WRONG object

The forced chain trades variables for degree, and Gröbner cost is doubly
exponential in degree. Every "deeper" reduction was strictly harder:

| export | vars | max deg | terms | outcome |
|---|---|---|---|---|
| root | 166 | **5** | **8,774** | see below |
| `reduced_tb1deep_99v` | 100 | 19 | 414,175 | OOM, `halt 14` — NO VERDICT |
| `reduced_tb1deep_82v` | 83 | — | ~1.5 M | `halt 1` — NO VERDICT |
| `reduced_tb1deep_60v` | 61 | — | ~5.3 M | 240 MB, cannot load — NO VERDICT |

The root was never given a budget until tonight: `w6_branch_solve.py` defaults
to `LEAF_MEM=4000000` (4 GB) and `LEAF_T=120` (2 min).

## Tonight's runs on the root

| # | engine | prime | form | budget | outcome |
|---|---|---|---|---|---|
| 1 | msolve `-t 4` | 1000003 | root 166v | 13 GB / 3600 s | **NO VERDICT** — hash table abort at 3 min, `esz = 33554432`. 2²⁵ monomials × 166 dense exponent slots ≈ 22 GB. Structural: msolve cannot ingest 166 vars on this box, no tunable exists. |
| 2 | Singular `slimgb` dp | 1000003 | root 166v | 13 GB / 3600 s | **NO VERDICT** — ran the full 3600 s to 2060 MB, killed by `timeout` (`halt 1`). Not a crash; it was still computing. |
| 3 | Singular `slimgb` block `(dp51,dp115)` | 1000003 | root, c eliminated | 5 GB / 3600 s | running |
| 4 | Singular `slimgb` 3-block `c>d>s` | 1000003 | root | 4 GB / 3300 s | **retired at 20 min**, flat at 1165 MB; elimination orders on 166 vars least likely to terminate |
| 5 | Singular `slimgb` dp | 65521 | root 166v | 6 GB / 3600 s | running |
| 6 | Singular `std` degBound 6→16 | 65521 | root | 5 GB / 3300 s | running — **one-sided**: a unit at any rung proves EMPTY, no unit proves nothing |
| 7 | Singular `stdhilb` | 65521 | root | 5 GB / 3000 s | running |
| 8 | Singular `slimgb` dp | 65521 | s-fixed slice, 162v deg ≤2 + quartic sat row | 5 GB / 3000 s | running |
| 9 | Singular `slimgb` dp | 65521 | s-fixed + linear reduction, **148v deg 3** | 4 GB / 2700 s | running |
| 10 | Singular `slimgb` dp | 65521 | second s (seed 777), 148v deg 3 | 4 GB / 2700 s | running |

## Non-Gröbner results (these DID complete)

- **Variable projection, c-block.** 283 of 284 equations are affine linear in
  the 51-variable c-block: `A(d,s)·c = b(d,s)`. At both primes and every random
  `(d,s)`: `rank A = 51`, `rank[A|b] = 52` — **inconsistent**.
- **Variable projection, d-block.** All 284 equations affine linear in the
  110-variable d-block. Every random `(c,s)`: `rank M = 110`, `rank[M|n] = 111`
  — **inconsistent**.
- **Coordinate subspaces.** 11 sparse patterns, including all free `s` and all
  free `d` zeroed. All inconsistent; `rank A` stays 51 throughout.
- **Planted-solution control** (`w6_tb1_control.py`): passes all three legs, so
  the above are measurements, not a broken instrument.

**None of this is emptiness.** Consistency is a proper closed condition and
random points miss proper closed subvarieties by construction. What it
establishes is that the projection is not dominant in either direction.

## Errors found tonight, all mine

1. **Sign error in solution recovery** — `c = +v/v[n]` instead of `-v/v[n]`, in
   both `w6_tb1_rank.py` CHECK 3 and the control. Caught by the control's
   recovery leg. **Only executes on a hit**, so it would have corrupted exactly
   the counterexample point and nothing else.
2. **Silent variable drop** — parameter block built from an explicit prefix
   list, so `w_sat` (p=65521's saturation variable, named `zsat` at the other
   prime) fell out of it entirely. Harmless only by accident of where that
   variable occurs.
3. **False homogeneity claim** — asserted the system was homogeneous in `c`; the
   assertion fired, eq 8 has a c-free term. It is affine, not homogeneous.
4. **"Purely bilinear" overstatement** — claimed the s-slice was all bidegree
   (1,1) degree 2. Measured: 21 rows degree 1, 262 degree 2, one degree 4.
5. **Meaningless exit codes** — runner printed `exit=$?` after a pipeline,
   reporting `tail`'s status. Printed `msolve exit=0` for a segfault.
6. **`pkill -f` self-match** — the pattern matched its own shell and suspended it.
7. **Read significance into a forced quantity** — nearly wrote up
   `rank[A|b] = rank A + 1` as a "minimal obstruction". One extra column can
   only raise rank by one; it means nothing.

The pattern that keeps repeating: **the saturation variable is the one that gets
forgotten, and it is the one carrying the nondegeneracy conditions.**
