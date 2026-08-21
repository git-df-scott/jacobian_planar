# Bottom-edge sweep audit (session: jacobian-planar-sweep)

## Uniform re-census — one instrument, all archived primes

`analyse.py` (tip version) re-run on every archived `be_p*.out`. All seeds
verify against all 17 equations at all primes (verify_fail=0 throughout).

| p       | rational/9 | admissible | degenerate |
|---------|-----------|------------|------------|
| 999961  | 4         | 0          | 4          |
| 999979  | 5         | 1          | 4          |
| 999983  | 4         | 2          | 2          |
| 1000003 | 5         | 1          | 4          |
| 1000033 | 4         | 0          | 4          |
| 1000039 | 5         | 1          | 4          |
| 1000081 | 7         | 3          | 4          |

Admissible: sum 8 over 7 primes, mean 1.14. Degenerate: mean 3.71.

## Findings

1. **The retraction-era count list is CONFIRMED as a multiset.** The commit
   8492a76 list "1,1,0,2,3" and this re-census "{1,2,0,1,3}" over the same five
   primes are equal as multisets; the apparent per-prime mismatch was ordering,
   not measurement. No instrument drift between eras.
2. **Degenerate seeds have BOTH c8=0 AND d12=0 at every prime examined**
   (999961, 999979, 999983, 1000039 checked seed-by-seed), consistent with the
   original ce3143b claim. An intermediate report here to the contrary was a
   display bug in an ad-hoc audit script (operator precedence swallowed the
   d12 flag), not in `analyse.py`.
3. **analyse.py's admissibility test adds c1≠0** beyond the documented side
   conditions (c8≠0, d12≠0). At every prime checked seed-by-seed, c1 never
   vanishes, so the published counts are unaffected — but the definition in
   the ledger and the code should be reconciled explicitly.
4. **The p=999983 anomaly (degenerate=2, not 4) is the open structural fact.**
   No multiple roots mod 999983 (all roots simple), so it is not visibly bad
   reduction of the eliminant. If the degenerate locus were 4 rational
   Q-points it would count 4 at every good prime. Best fit consistent with the
   data: degenerate locus = 2 rational points + one irreducible quadratic
   orbit (counts 2 or 4; observed six 4s, one 2 — small-sample), admissible
   locus = one irreducible quintic (mean 1.14 ≈ 1). NOT asserted — the
   char-0 rational parametrization (msolve -P 2 on `be_c2is1_q.ms`, in
   flight as `be_c2is1_q_param.out`) decides this exactly by factoring the
   degree-9 eliminant over Q. Per the standing rule, no orbit claim is made
   until that factorisation lands.
5. Mean admissible 1.14 over 7 primes leans single-quintic-orbit (predicts
   1.0) over two orbits (predicts 2.0), but 7 primes is still inside the
   error-bar regime the 8492a76 retraction warned about.

## Instrument notes

- msolve here is 0.6.5 (apt), not necessarily the sibling worker's build;
  p=999979 re-analysis reproduced the committed census line byte-for-byte.
- This session cannot push to the campaign branch; sweep continues on
  `claude/jacobian-planar-sweep-iajyma` in REVERSE prime order so a surviving
  sibling walking forward and this worker meet in the middle. The resume
  script refetches the campaign branch's orbit_data.txt before each prime and
  skips primes censused on either branch.
