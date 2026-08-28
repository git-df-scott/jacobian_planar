# night9 — the redirected accumulator: votes at legal altitude

Scope note. Measurements only. Every result is labelled with its
characteristic or with the ring it was computed in. No assessment of what any
of these numbers mean is offered.

Script: `night9/altitude.py`. Raw data: `night9/altitude.csv`, per-support
JSON in `night9/altitude/`, run log `night9/altitude_log.txt`.

## 0. Scoping rationale, recorded as handed down

The sweep was restricted to supports of maximum total degree in `[126, 160]`
on the following stated ground, recorded here verbatim as the reason for the
scoping and **not** as a finding of this lane: supports of maximum degree
below 125 cannot carry a characteristic-zero object (published bound), so
multi-prime hits at those degrees are residual-divisibility coincidences;
votes at legal altitude require maximum degree at least 126.

## 1. What was swept

Sparse support pairs `(S_P, S_Q)`, generated with seed `20260830`, subject to

* `5 <= |S_P|, |S_Q| <= 8`;
* `(1,0) in S_P` and `(0,1) in S_Q`;
* each support contains at least one PURE monomial (one exponent zero) of
  total degree `>= 100` **and** at least one MIXED monomial (both exponents
  strictly positive) of total degree `>= 100`;
* the maximum total degree over both supports lies in `[126, 160]`.

**60 supports**, realised max total degree 131..160, unknown count
`n = |S_P| + |S_Q|` in 10..16. Primes: **p = 2 and p = 3 only**, so
**120 cells**.

Method: `exhaustive-bilinear` in all 120 cells — for each assignment of the
coefficients of one side (chosen as the smaller, inside its own collision
subspace) the (K) system is linear in the other side's coefficients and is
solved exactly over `F_p` by batched Gauss-Jordan. Every `F_p` point is
visited, so every count below is exact. No cell exceeded the budget; no cell
needed Groebner; no TIMEOUT occurred. All solution lists complete (no
truncation at the cap of 20000).

## 2. Verdicts

| | p = 2 | p = 3 | total |
|---|---|---|---|
| NONEMPTY | 53 | 42 | 95 |
| EMPTY | 7 | 18 | 25 |
| TIMEOUT / NOT-ATTEMPTED | 0 | 0 | 0 |

Supports NONEMPTY at **both** p = 2 and p = 3: **38** of 60.

Direct-substitution verification (`det J - 1 = 0` in `F_p[x,y]` and both
collision equalities) on the sampled non-degenerate solutions:
**624 checked, 0 failures**.

Tear classification over the same 624 sampled solutions:
TEAR-NONEMPTY 0, TEAR-EMPTY 7, TEAR-NOT-COMPUTED / other 617.
At these degrees the Sylvester matrices exceed `tear.py`'s size caps in almost
every cell, and TEAR-NOT-COMPUTED is recorded honestly rather than guessed.

## 3. The support-by-prime table

`N/<exact F_p count>/<non-degenerate count>`; `Empty` as recorded. The last
column is `<shared support patterns> / <matched (p=2,p=3) pairs examined> /
<factorisation of the integer content of the smallest-content residual>`.

| hash | max deg | n | p = 2 | p = 3 | matched-pair summary |
|---|---|---|---|---|---|
| `f4c533396b1c` | 153 | 11 | Empty | N/6/4 | 0 / 0 / - |
| `2e4c72090e2e` | 153 | 12 | N/44/42 | N/70/64 | 3 / 10 / 2*3*7^2*71 |
| `cf4ee5f59b92` | 153 | 12 | N/16/15 | N/10/4 | 0 / 0 / - |
| `d42d069ab871` | 147 | 13 | N/28/28 | Empty | 0 / 0 / - |
| `71ac15ff1c37` | 148 | 12 | N/32/31 | N/18/16 | 1 / 4 / 2^2*3 |
| `42b4233a6437` | 154 | 13 | N/16/14 | N/486/484 | 3 / 16 / 2*3 |
| `e66454742942` | 138 | 13 | N/24/23 | N/6/0 | 0 / 0 / - |
| `56b7dae5d4ab` | 156 | 10 | Empty | N/6/4 | 0 / 0 / - |
| `b42e4046989d` | 157 | 14 | N/12/8 | Empty | 0 / 0 / - |
| `fd12cbe4b429` | 148 | 11 | Empty | Empty | 0 / 0 / - |
| `0d4f9a0d7f81` | 148 | 11 | N/4/2 | Empty | 0 / 0 / - |
| `492665aa006d` | 146 | 14 | N/64/52 | N/18/18 | 2 / 6 / 2^2*3*19*61 |
| `77aa218f7917` | 154 | 14 | N/256/248 | N/54/36 | 4 / 24 / 2*3 |
| `c7ba7509d0b2` | 159 | 12 | N/4/3 | N/6/6 | 1 / 2 / 2^2*3*11^2*13 |
| `2685778ac045` | 158 | 14 | N/36/20 | N/66/48 | 0 / 0 / - |
| `6703cbfe5fe4` | 158 | 14 | N/8/5 | N/54/36 | 0 / 0 / - |
| `efae6ba71cb6` | 160 | 14 | N/640/638 | N/162/156 | 14 / 68 / 2^4*3^2*5*13 |
| `0f2efd22ee8f` | 159 | 12 | N/16/15 | N/6/4 | 1 / 2 / 2^2*3*11*13 |
| `e07f72fc152b` | 153 | 15 | N/48/44 | N/1458/1440 | 20 / 104 / 2^2*3*5*13 |
| `a0c736f067a4` | 160 | 13 | N/20/18 | N/486/480 | 8 / 36 / 2^2*3*5*7*37 |
| `abda1496949e` | 158 | 15 | N/56/54 | N/162/162 | 1 / 2 / 2*3*23*41 |
| `e600e2184b1d` | 159 | 16 | N/32/30 | N/102/96 | 1 / 4 / 2*3 |
| `405a469bffcf` | 152 | 12 | N/40/35 | N/198/132 | 5 / 26 / 2^3*3^2*103 |
| `21bd08557217` | 145 | 15 | N/32/32 | N/4374/4374 | 32 / 264 / 2*3*5*23 |
| `247c36e19dc3` | 153 | 13 | N/12/10 | Empty | 0 / 0 / - |
| `4f8445c930b0` | 139 | 12 | N/16/15 | N/18/16 | 0 / 0 / - |
| `3aa3f2d1cd2f` | 154 | 12 | N/64/60 | N/2/2 | 1 / 2 / 2^2*3*31*41 |
| `efcc92f30ccf` | 160 | 15 | N/32/30 | N/6/4 | 0 / 0 / - |
| `1d1a31e7ba9c` | 159 | 15 | N/8/4 | N/270/252 | 0 / 0 / - |
| `6b14a35869e1` | 131 | 11 | N/8/4 | Empty | 0 / 0 / - |
| `38e6cb1f6a94` | 143 | 15 | N/8/8 | Empty | 0 / 0 / - |
| `ba6b62170c52` | 153 | 12 | N/4/4 | N/1566/1548 | 2 / 6 / 2*3*7*19^2 |
| `6b2a44111074` | 144 | 13 | N/8/6 | Empty | 0 / 0 / - |
| `62fc1a178b8f` | 160 | 14 | N/32/31 | Empty | 0 / 0 / - |
| `c44d9d649a23` | 159 | 11 | N/16/15 | N/6/0 | 0 / 0 / - |
| `2db81810e7ad` | 157 | 16 | N/24/22 | N/630/608 | 3 / 10 / 2^4*3*5*17 |
| `b8cb03dd9688` | 148 | 13 | N/64/63 | N/486/486 | 16 / 96 / 2*3*5*19^2 |
| `c37a1c94c6f2` | 154 | 14 | N/160/155 | N/522/500 | 16 / 110 / 2^3*3*5*11 |
| `168b6eb04780` | 140 | 14 | Empty | Empty | 0 / 0 / - |
| `cdcf3cc59c58` | 141 | 13 | N/8/6 | Empty | 0 / 0 / - |
| `70aab4481767` | 149 | 15 | N/16/14 | N/18/16 | 0 / 0 / - |
| `5b6a8c32ede8` | 155 | 13 | N/20/12 | Empty | 0 / 0 / - |
| `ad2397183dda` | 159 | 15 | N/256/251 | N/54/52 | 7 / 34 / 2^3*3*11*17 |
| `1751cd1e2604` | 158 | 10 | Empty | N/18/0 | 0 / 0 / - |
| `41fcb750b183` | 160 | 13 | N/40/36 | N/306/288 | 4 / 12 / 2^2*3*89 |
| `6936b7b54b0c` | 159 | 12 | N/4/2 | N/6/0 | 0 / 0 / - |
| `3b714329e68e` | 154 | 14 | N/8/7 | N/2/0 | 0 / 0 / - |
| `ef38fc7d5f53` | 160 | 14 | N/64/46 | N/102/84 | 2 / 4 / 2^6*3*7 |
| `597332c0312f` | 152 | 16 | N/44/28 | Empty | 0 / 0 / - |
| `2e2bde3ebbe3` | 154 | 13 | N/40/36 | Empty | 0 / 0 / - |
| `13512b945a96` | 151 | 14 | N/4/4 | N/6/4 | 0 / 0 / - |
| `0ba45c61d577` | 148 | 16 | N/56/56 | N/954/954 | 18 / 80 / 2^2*3*17 |
| `1a08a6ed5b29` | 139 | 13 | Empty | N/6/4 | 0 / 0 / - |
| `60891c73f760` | 158 | 11 | N/8/7 | Empty | 0 / 0 / - |
| `73eb82dc7fc5` | 159 | 11 | N/4/2 | N/54/48 | 2 / 8 / 2*3 |
| `b6ef2dcad17f` | 155 | 12 | Empty | Empty | 0 / 0 / - |
| `bd0279288432` | 143 | 11 | N/3/2 | Empty | 0 / 0 / - |
| `059ba1a7ab65` | 159 | 13 | N/18/14 | Empty | 0 / 0 / - |
| `92153ee43036` | 155 | 11 | N/8/8 | N/2/2 | 1 / 2 / 2*3*5^2*59 |
| `fb644eab941d` | 155 | 14 | N/32/28 | N/30/24 | 4 / 14 / 2*3*23*41 |

## 4. The quantity of interest — exact integer residuals of matched lifts

For every support NONEMPTY at both primes, each pair `(s_2, s_3)` of
NON-DEGENERATE solutions with the **same zero/non-zero coefficient pattern**
was CRT-combined coefficient-wise to the balanced integer lift mod
`M = 6` (representatives in `(-3, 3]`), and

    R(x,y) = P_x Q_y - P_y Q_x - 1

was computed **exactly over Z** (sympy, integer arithmetic), together with the
two collision differences over Z. Every such object is filed
**CANDIDATE-UNVERIFIED**.

| quantity | value |
|---|---|
| supports contributing at least one matched pair | **26** |
| matched pairs examined | **946** (no support hit the 4000-pair cap) |
| lifts recorded in the JSONs (cap 200 per support) | 882 |
| lifts with `R` **identically zero over Z** | **0** |
| lifts whose two collision differences both vanish over Z | 876 of 882 |

Distribution of the number of **distinct** prime factors of the integer
content of `R`:

| distinct primes in content | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| lifts | 768 | 62 | 48 | 4 |

Every content recorded is divisible by `6 = 2 * 3`, which is the modulus of
the lift. Distribution of the number of monomial terms in `R` over Z:

| terms in R | 1 | 3 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| lifts | 88 | 474 | 256 | 16 | 48 |

(`R` has one term exactly when the `(0,0)` coefficient of `P_x Q_y - P_y Q_x`
is `1` over Z and all but one of the remaining monomials cancel; the content
is then the absolute value of that single coefficient.)

The lifts carrying the most distinct primes in the content:

| distinct primes | content | factorisation | terms in R | collisions hold over Z |
|---|---|---|---|---|
| 5 | 15960 | 2^3*3*5*7*19 | 1 | True |
| 5 | 15960 | 2^3*3*5*7*19 | 1 | True |
| 5 | 15540 | 2^2*3*5*7*37 | 1 | True |
| 5 | 15540 | 2^2*3*5*7*37 | 1 | True |
| 4 | 21726 | 2*3^2*17*71 | 1 | True |
| 4 | 21726 | 2*3^2*17*71 | 1 | True |
| 4 | 20874 | 2*3*7^2*71 | 1 | True |
| 4 | 20874 | 2*3*7^2*71 | 1 | True |
| 4 | 20160 | 2^6*3^2*5*7 | 1 | True |
| 4 | 20160 | 2^6*3^2*5*7 | 1 | True |
| 4 | 18876 | 2^2*3*11^2*13 | 1 | True |
| 4 | 18876 | 2^2*3*11^2*13 | 1 | True |

**No matched lift produced a residual identically zero over Z.** Recorded as
such; nothing here passed exact verification over Z or Q.

## 5. Files

* `night9/altitude.py` — the sweep (generator, method, and the exact-over-Z
  residual computation).
* `night9/altitude.csv` — one row per cell, 120 rows.
* `night9/altitude/<hash>.json` — per support: both supports, both per-prime
  records, the shared support patterns, and the matched lifts with their exact
  integer residuals, content factorisations and collision differences; every
  lift carries `"label": "CANDIDATE-UNVERIFIED"`.
* `night9/altitude_log.txt` — the run log.
