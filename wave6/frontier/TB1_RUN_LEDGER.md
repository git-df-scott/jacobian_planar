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
| 3 | Singular `slimgb` block `(dp51,dp115)` | 1000003 | root, c eliminated | 5 GB / 3600 s | **NO VERDICT** — `exit=124`, clean timeout |
| 4 | Singular `slimgb` 3-block `c>d>s` | 1000003 | root | 4 GB / 3300 s | **retired at 20 min**, flat at 1165 MB; elimination orders on 166 vars least likely to terminate |
| 5 | Singular `slimgb` dp | 65521 | root 166v | 6 GB / 3600 s | **NO VERDICT** — `exit=124` |
| 6 | Singular `std` degBound 6→16 | 65521 | root | 5 GB / 3300 s | **NO VERDICT** — `exit=124`, and **not one rung completed**: even `degBound=6` on 166 vars did not finish. The cheap one-sided proof is not cheap at this size. |
| 7 | Singular `stdhilb` | 65521 | root | 5 GB / 3000 s | **NO VERDICT** — `exit=124` |
| 8 | Singular `slimgb` dp | 65521 | s-fixed slice, 162v deg ≤2 + quartic sat row | 5 GB / 3000 s | running |
| 9 | Singular `slimgb` dp | 65521 | s-fixed + linear reduction, **148v deg 3** | 4 GB / 2700 s | running |
| 10 | Singular `slimgb` dp | 65521 | second s (seed 777), 148v deg 3 | 4 GB / 2700 s | running |

## Every full-root attack has now failed

Seven attempts, two engines, two primes, four monomial orders (dp, block
`(51,115)`, 3-block `c>d>s`, Hilbert-driven), degree-bounded and unbounded,
4–13 GB, 50–60 minutes each. **All NO VERDICT.**

**Correction — my first diagnosis of msolve was wrong.** I wrote that msolve
"fails structurally on variable count", its hash table being dense in nvars.
That is not what the data says. msolve aborts with the *same* ceiling,
`esz = 33554432` = 2²⁵, at **166, 148 and 61 variables alike**. The variable
count is not what saturates it — the **monomial count generated during F4** is,
and 2²⁵ is where its hash table gives up.

What that changes: the remedy is **more memory, not fewer variables**, which is
the opposite of what I concluded and the opposite of what I acted on. At 61
variables the table needs 2²⁵ × 61 × 4 B ≈ 8.2 GB, and it was capped at 6 GB —
so the cap was the binding constraint, and shrinking the system from 166 to 61
variables never addressed it. Retried at 9 GB.

Singular fails on *time*: every run was still computing when killed, none
crashed and none exhausted memory.

The conclusion to draw is not "try harder on the root". It is that **the
unreduced 166-variable root is out of reach of the available tooling**, and the
route forward is decomposition into pieces that terminate.

## The subsystem route

`w6_tb1_subsystem.py` / `w6_tb1_square.py`. Emptiness is monotone: any subset of
the equations that is empty proves the whole system empty.

- **No overdetermined block exists** (max surplus 0 over greedy walks from all
  283 seeds). Heuristic only — 283 greedy paths do not survey 2¹⁶⁵ subsets, and
  that exact overclaim was made and retracted earlier in this campaign.
- A **square block** does exist: 60 equations over 60 variables, max degree 4,
  **533 terms** against the root's 8,774.
- Decisively, **all four saturation variables** `c_1_0, c_8_14, d_12_21, s_4_8`
  lie inside it, so the block can carry the full nondegeneracy condition as a
  **61×61 saturated system**.

| outcome | meaning |
|---|---|
| saturated block **EMPTY** | every trackB1 solution restricts to a solution of this block with those four variables nonzero. None exists ⟹ **trackB1 EMPTY. A real verdict.** |
| saturated block **NONEMPTY** | inconclusive for trackB1 — a subset having solutions says nothing about the superset — but gives a small solution set to test against the remaining 224 equations, which is a complete decision procedure. |

Both branches terminate. Expectation recorded before the result: the block is
probably NONEMPTY, since 60 equations in 60 variables is not overdetermined.

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

## msolve: a hard 2²⁵ ceiling — and I misdiagnosed it twice

msolve aborts with `Enlarging exponent vector for hash table failed for
esz = 33554432` on every hard target here. The constant never moves:

| target | vars | memory cap | result |
|---|---|---|---|
| root | 166 | 13 GB | `esz = 33554432` |
| linred slice | 148 | 6 GB | `esz = 33554432`, `exit=139` |
| saturated block | 61 | 6 GB | `esz = 33554432`, `exit=139` |
| saturated block | 61 | **9 GB** | `esz = 33554432`, `exit=139` |

**My first diagnosis** — "fails structurally on variable count, the hash table
is dense in nvars" — is refuted by rows 3 and 4: the same ceiling at 61
variables as at 166.

**My second diagnosis** — "it is monomial count, so the fix is more memory" —
is refuted by row 4: 9 GB dies exactly like 6 GB.

**What is actually true.** msolve is working correctly here; on tiny systems it
returns a parametrization, `[-1]` for an empty one, and `[1, n, -1, []]` for a
positive-dimensional one. It has a **hard internal ceiling of 2²⁵ hash-table
entries**. Any system whose F4 needs more monomials than that is out of reach
for this build, *independent of variable count and independent of available
memory*. Nothing but a system generating fewer monomials will help.

So the original conclusion — msolve is ruled out for these targets — stands, but
it stood for the wrong reason, and the wrong reason is what drove the hunt for
ever-smaller subsystems. That hunt produced the 61×61 decisive block, so it was
not wasted; but it was undertaken on a false premise and should be recorded that
way.

**Everything from here is Singular.**

## A real, if modest, quantitative result: no certificate below degree 6

Degree-bounded ladders (`degBound = d; std(I)`) on the saturated blocks, at both
primes:

| block | prime | D=4 | D=5 | D=6 |
|---|---|---|---|---|
| 61×61 saturated | 1000003 | no unit | no unit | OOM at 3.5 GB, retried at 5 GB |
| 97×97 saturated | 1000003 | no unit | no unit | OOM at 3.5 GB, then at 4.5 GB, retried at 6.5 GB |
| 97×97 saturated | **65521** | no unit | no unit | pending |

Three ladders, two block sizes, two independent primes, all agreeing. So:

> **If these blocks are empty, any Nullstellensatz certificate has degree ≥ 6.**

The cross-prime agreement matters: it makes this a statement about the integer
system rather than a mod-p artifact. Both primes would have to conspire for a
low-degree certificate to be hidden.

Stated carefully, because the direction is easy to get backwards: this is **not**
evidence that the blocks are nonempty. A degree ladder is one-sided — a unit
proves EMPTY, its absence proves only that the bound was too low. What the
result does is *bound the search*: degrees 4 and 5 are now closed off, and the
question lives at degree ≥ 6.

That is also exactly where the memory wall sits. Every ladder clears 4 and 5
cheaply and dies at 6. The Macaulay matrices at degree 6 are large for these
blocks, and 3.5 GB and 4.5 GB were both insufficient — those deaths are
`halt 14`, a cap I set, not a property of the problem.

## The decisive block has only TWO nonlinear variables

Measured on `tb1_sq_sat.sing` (61 vars, 61 eqs, 535 terms, p=1000003):

| | root | 61-block |
|---|---|---|
| c-block | 51 | **23** |
| d-block | 110 | **35** |
| s-block (all the nonlinearity) | 4 | **2** |
| affine-linear in c | 283/284 | 60/61 |
| affine-linear in d | 284/284 | 61/61 |
| terms | 8,774 | **535** |
| max degree | 5 | 5 |

The block inherits the root's structure but far more sharply. Degree histogram:
one linear row, 44 quadrics, 10 cubics, 5 quartics, one quintic.

**CORRECTION — I overstated this within minutes of measuring it.** I wrote that
eliminating c and d would leave "a system in 2 remaining variables", making a
23×23 Cramer determinant an ordinary two-variable object. **That is false.**

The block is affine-linear in c *and* affine-linear in d, but it is not
*jointly* linear in (c,d) — it is **bilinear**. The two eliminations cannot be
composed:

- eliminate c (23 vars) → the result is rational in d, so clearing denominators
  leaves **38 variables** (35 d + 2 s + 1 sat), and it is **no longer linear in
  d**, so the d-elimination that was available before is gone;
- eliminate d (35 vars) first → leaves **26 variables** (23 c + 2 s + 1 sat),
  same problem in the other direction.

Neither order reaches 2 variables. The "2 nonlinear variables" figure describes
which variables carry nonlinearity, **not** how many survive elimination, and I
conflated the two. This is the same class of error as the earlier
`rank[A|b] = rank A + 1` reading: taking a structural quantity to mean something
it does not.

**What is actually true and still useful.** The block is far smaller than the
root in every dimension (23/35/2 against 51/110/4, 535 terms against 8,774), and
for *fixed* s it is a bilinear system in 58 unknowns. Since s-space here is only
**2-dimensional**, sweeping it is a far more realistic proposition than sweeping
the root's 4-dimensional s-space — but each sample still requires solving a
58-unknown bilinear system, so it is not free, and an EMPTY at fixed s carries
the same weak-direction caveat recorded for the root's slices.

Honest status: a smaller and better-understood target, not a shortcut to a
verdict.

## Process error, repeated: `pkill -f` matching its own shell

Twice tonight `pkill -f '<pattern>'` killed the shell running it, because that
shell's command line contained the pattern. The first time it suspended a
status command harmlessly. The second time it killed the running degree-6 job
*and* died before reaching the relaunch line, leaving **nothing running for four
minutes** while the logs looked like a normal shutdown.

Fix: kill by PID, or keep the pattern out of the command that greps for it. The
failure is silent and looks exactly like a clean process exit, which is what
makes it worth writing down rather than just not repeating.
