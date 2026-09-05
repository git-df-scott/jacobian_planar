# night9 — the cross-prime experiment

Scope note. Measurements only. Every result is labelled with its
characteristic. No assessment of what any of these numbers mean is offered.

Twelve distinguished supports, each run at **every** prime in
`{2, 3, 5, 7, 11, 13, 17, 19, 23}` — 108 cells. Selection:

* **(a)** the four supports whose solutions climbed to `Z/p^2` in the sweep:
  `3ee4c514dba8`, `c764f008a1a1`, `cf8c7ed97c0c` (found at `p = 3`) and
  `e3ff048903ae` (found at `p = 5`);
* **(b)** eight further cells that were TEAR-NONEMPTY *and* carried
  non-degenerate solutions, chosen for enumerability — smallest
  `min(|S_P|,|S_Q|)` and lowest total degree first — and spread over the two
  families and over the primes at which they were found.

Method and standards are exactly those of `night9/README.md` §3–§6:
complete `exhaustive-bilinear` enumeration when `p^nfree <= 10^7`, otherwise
Groebner over `GF(p)` **with the field equations** `z^p - z` (300 s timeout,
a timeout recorded as TIMEOUT and never as EMPTY); on NONEMPTY the complete
solution set is enumerated (cap 60000) and split by the additive-type
degeneracy screen; up to 8 non-degenerate solutions per cell are verified by
direct substitution, tear-classified mod `p`, and pushed through the Hensel
steps to `Z/p^2` and then `Z/p^3`, TEAR-NONEMPTY first.

Raw data: `night9/cross_prime.csv`, per-cell JSON in `night9/cross_prime/`.


## 1. The twelve supports

| hash | origin | S_P | S_Q | n |
|---|---|---|---|---|
| `3ee4c514dba8` | climb to Z/p^2 | (0,2) (0,3) (1,0) (1,2) (1,3) (2,1) (4,0) | (0,1) (0,9) (1,8) (3,4) (3,5) (6,0) | 13 |
| `c764f008a1a1` | climb to Z/p^2 | (1,0) (4,6) (7,3) (8,0) (9,0) (9,2) | (0,1) (0,12) (1,2) (4,14) (8,0) (8,9) | 12 |
| `cf8c7ed97c0c` | climb to Z/p^2 | (0,4) (1,0) (1,1) (1,4) (1,6) (3,3) (6,1) | (0,1) (3,0) (11,3) (12,2) | 11 |
| `e3ff048903ae` | climb to Z/p^2 | (0,5) (1,0) (1,5) (2,0) (3,2) (4,2) (5,1) | (0,1) (1,7) (2,11) (5,4) (7,6) (10,0) | 13 |
| `4ed4abb6f5df` | TEAR-NONEMPTY, non-degenerate | (1,0) (4,4) (5,3) (6,0) | (0,1) (0,6) (1,3) (2,0) | 8 |
| `9fad1aac9556` | TEAR-NONEMPTY, non-degenerate | (0,10) (1,0) (2,1) (3,0) | (0,1) (2,1) (3,10) (4,0) | 8 |
| `1c4afff29879` | TEAR-NONEMPTY, non-degenerate | (1,0) (2,4) (3,4) (5,0) (6,0) | (0,1) (1,0) (1,8) (3,6) | 9 |
| `184a36732588` | TEAR-NONEMPTY, non-degenerate | (1,0) (2,8) (4,2) (5,0) (9,0) | (0,1) (2,7) (8,0) (8,3) | 9 |
| `2b796756e70e` | TEAR-NONEMPTY, non-degenerate | (1,0) (2,1) (6,0) (8,2) | (0,1) (4,0) (5,1) (6,2) (7,3) | 9 |
| `252ffcaec0dc` | TEAR-NONEMPTY, non-degenerate | (1,0) (2,1) (6,0) (9,2) | (0,1) (6,0) (7,1) (8,2) (9,3) | 9 |
| `36b363c5d338` | TEAR-NONEMPTY, non-degenerate | (1,0) (3,1) (6,0) (9,2) | (0,1) (6,0) (7,1) (8,2) (9,3) | 9 |
| `6c5a7dd8e3e9` | TEAR-NONEMPTY, non-degenerate | (1,0) (1,1) (1,4) (5,0) (5,1) (6,0) | (0,1) (1,0) (1,1) (1,5) (3,3) | 11 |

## 2. The support-by-prime matrix

Cell legend. `EMPTY` / `TIMEOUT` as recorded. For a NONEMPTY cell:
`N/<non-degenerate count>/<tear tally>` where the tear tally counts the
sampled non-degenerate solutions as `NE` = TEAR-NONEMPTY, `E` = TEAR-EMPTY,
`?` = TEAR-NOT-COMPUTED (caps of `README.md` §5); `/c2=..,c3=..` is appended
when any solution climbed to `Z/p^2` resp. `Z/p^3`.

| hash | p=2 | p=3 | p=5 | p=7 | p=11 | p=13 | p=17 | p=19 | p=23 |
|---|---|---|---|---|---|---|---|---|---|
| `3ee4c514dba8` | N/13/E8/c2=1,c3=0 | N/12/E8/c2=3,c3=0 | E | E | E | E | E | E | E |
| `c764f008a1a1` | N/14/NE5E3/c2=2,c3=0 | N/16/NE4E4/c2=2,c3=0 | E | E | E | E | E | E | E |
| `cf8c7ed97c0c` | N/2/E2/c2=1,c3=0 | N/18/NE3E5/c2=1,c3=0 | E | E | E | E | E | E | E |
| `e3ff048903ae` | N/9/NE5E3 | E | N/20/E8/c2=2,c3=0 | E | E | E | E | E | E |
| `4ed4abb6f5df` | N/2/E2 | N/12/NE3E5 | E | E | E | E | E | E | E |
| `9fad1aac9556` | N/3/NE1E2/c2=1,c3=1 | N/4/NE2E2 | N/20/NE1E7 | E | E | E | E | E | E |
| `1c4afff29879` | N/7/NE6E1 | N/4/NE4 | N/0/- | E | E | E | E | E | E |
| `184a36732588` | E | N/4/NE4 | N/0/- | E | E | E | E | E | E |
| `2b796756e70e` | N/7/NE4E3/c2=1,c3=0 | N/4/NE4 | E | E | E | E | E | E | E |
| `252ffcaec0dc` | N/3/NE1E2 | N/16/NE6E2 | E | E | E | E | E | E | E |
| `36b363c5d338` | N/1/NE1 | N/52/NE6E2 | E | E | E | E | E | E | E |
| `6c5a7dd8e3e9` | N/0/- | N/4/NE4 | N/32/NE8 | E | E | E | E | E | E |

## 3. Tallies

Cells run: **108**. Verdicts: NONEMPTY 27, EMPTY 81.

Methods: `exhaustive-bilinear` 108.

Direct-substitution verification failures: **0**.

### Per-support totals

| hash | NONEMPTY primes | primes with >=1 non-degenerate solution | TEAR-NONEMPTY primes | primes with a Z/p^2 climb | Z/p^3 climbs |
|---|---|---|---|---|---|
| `3ee4c514dba8` | 2, 3 | 2, 3 | none | 2, 3 | 0 |
| `c764f008a1a1` | 2, 3 | 2, 3 | 2, 3 | 2, 3 | 0 |
| `cf8c7ed97c0c` | 2, 3 | 2, 3 | 3 | 2, 3 | 0 |
| `e3ff048903ae` | 2, 5 | 2, 5 | 2 | 5 | 0 |
| `4ed4abb6f5df` | 2, 3 | 2, 3 | 3 | none | 0 |
| `9fad1aac9556` | 2, 3, 5 | 2, 3, 5 | 2, 3, 5 | 2 | 1 |
| `1c4afff29879` | 2, 3, 5 | 2, 3 | 2, 3 | none | 0 |
| `184a36732588` | 3, 5 | 3 | 3 | none | 0 |
| `2b796756e70e` | 2, 3 | 2, 3 | 2, 3 | 2 | 0 |
| `252ffcaec0dc` | 2, 3 | 2, 3 | 2, 3 | none | 0 |
| `36b363c5d338` | 2, 3 | 2, 3 | 2, 3 | none | 0 |
| `6c5a7dd8e3e9` | 2, 3, 5 | 3, 5 | 3, 5 | none | 0 |

## 4. The quantity of interest

Does any single support show **non-degenerate NONEMPTY at three or
more distinct primes**? Recorded without interpretation:

* `3ee4c514dba8`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `c764f008a1a1`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `cf8c7ed97c0c`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `e3ff048903ae`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=5
* `4ed4abb6f5df`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `9fad1aac9556`: non-degenerate NONEMPTY at 3 prime(s) — p=2, p=3, p=5
* `1c4afff29879`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `184a36732588`: non-degenerate NONEMPTY at 1 prime(s) — p=3
* `2b796756e70e`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `252ffcaec0dc`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `36b363c5d338`: non-degenerate NONEMPTY at 2 prime(s) — p=2, p=3
* `6c5a7dd8e3e9`: non-degenerate NONEMPTY at 2 prime(s) — p=3, p=5

Supports reaching three or more: **1** — `9fad1aac9556` (3 primes).
