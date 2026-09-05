# night13 stage 2 — the unavoidable-singleton screen over all H-supports

Scope note. Measurements only. Every count below says what was computed, in
which ring and characteristic. The stage-1 object and notation are in
`night13/PRESTRATUM.md`; this file generalises its section 5.

---

## 1. What is being screened

For an H-support `E` (the set of x-exponents of the degree-`m` form `H`, all
in one residue class mod 3, coefficients generic with the smallest one pinned
to 1 by the chart):

```
supp(H^2) = { (s, 2m-s) }   leading form of P = A·H^2,  deg P = 2m
supp(H^3) = { (s, 3m-s) }   leading form of Q = B·H^3,  deg Q = 3m
NP(P) = conv( supp(H^2) ∪ {(0,0), (1,0)} )
NP(Q) = conv( supp(H^3) ∪ {(0,0), (0,1)} )
```

and the **maximal lower pools** are all lattice points of those polygons with
the required residue and total degree `< 2m` resp. `< 3m`, with `(0,0)`
dropped from the Q pool (identically zero bracket column).

**Route.** At a bracket row key `k`, a route is a pair `(p, a)` with
`p + a = k + (1,1)`, `p` in the P support pool (leading ∪ lower), `a` in the Q
one, and `p1 a2 − p2 a1 ≠ 0`. It is **adjustable** when at least one member is
a lower monomial; pure leading × leading contributions cancel key by key
because `[A·H^2, B·H^3] = 6·A·B·H^3·(H_x H_y − H_y H_x) = 0` identically.

**Normalization-forced row.** The constant row `(0,0)` has the single route
`x = (1,0)` × `y = (0,1)`, so `a_(1,0)·b_(0,1) = 1` and both are nonzero at
every point of the stratum. A mandatory row `k ≠ (0,0)` is normalization-forced
when *every* adjustable route at `k` pairs one of those two forced monomials
with a **leading-form** monomial. Its equation is then

```
(a coefficient that cannot vanish) × (an expression in the top parameters) = 0
```

with no lower coefficient available to absorb it.

```
F1 : exactly one such route   -> a single top monomial is forced to vanish
F2 : exactly two such routes  -> one nontrivial relation among the top parameters
```

There can never be more than two: a route with `a = (0,1)` determines
`p = k + (1,0)`, and a route with `p = (1,0)` determines `a = k + (0,1)`.

**A support SURVIVES the screen iff it has no F1 and no F2 row.**

For ranking, a **near-singleton row** is a mandatory row with exactly two
adjustable routes (full census, computed only for survivors).

Cross-check: run on the stage-1 support `E = {2,14,29,41}` at `m = 42`, the
screen returns exactly `F1 = {(3,80), (123,2)}` and `F2 = {}` — the two
unrepairable rows of `PRESTRATUM.md` §5, reproduced by an independent code
path that never builds a carrier.

---

## 2. The mu_3 residue convention is forced

With `supp(H) ⊂ {i ≡ r mod 3}`, `supp(P)` sits in `2r` and `supp(Q)` in
`3r ≡ 0`. The constant bracket row needs a pair summing to `(1,1)`, i.e.
`P·(1,0) × Q·(0,1)` (needs `1 ≡ 2r` and `0 ≡ 0`, so `r = 2`) or
`P·(0,1) × Q·(1,0)` (needs `0 ≡ 2r` and `1 ≡ 0`, impossible).

| arm | H residue `r` | P residue | Q residue | constant row reachable |
|---|---|---|---|---|
| `r2_P1_Q0` | 2 | 1 | 0 | **yes** (the convention of stage 1) |
| `r0_P0_Q0` | 0 | 0 | 0 | **no** |
| `r1_P2_Q0` | 1 | 2 | 0 | **no** |

Checked, not assumed, at all three H-degrees (`h_screen_m*.json`, field
`constant_row_reachable_by_residue`). The two unreachable arms are not swept:
with no route to `(0,0)` the bracket's constant coefficient is structurally 0
and can never equal 1, for every support and every lower carrier. Varying the
residue convention therefore does not change the polygon extremes — it
removes the equation's right-hand side.

---

## 3. Tally, characteristic 0 (and every characteristic dividing neither row factor)

All subsets of size 3..6 of the exponent set `{i ≤ m : i ≡ 2 mod 3}`.

### m = 42, degree pair (84, 126)

| support size | supports | with F1 | with F2 | **survivors** |
|---|---|---|---|---|
| 3 | 364 | 364 (all with exactly 2 F1 rows) | 0 | **0** |
| 4 | 1001 | 1001 | 0 | **0** |
| 5 | 2002 | 2002 | 0 | **0** |
| 6 | 3003 | 3003 | 0 | **0** |
| **total** | **6370** | **6370** | **0** | **0** |

### m = 45, degree pair (90, 135)

| support size | supports | survivors |
|---|---|---|
| 3 / 4 / 5 / 6 | 455 / 1365 / 3003 / 5005 | 0 / 0 / 0 / 0 |
| **total** | **9828** | **0** |

### m = 48, degree pair (96, 144)

| support size | supports | survivors |
|---|---|---|
| 3 / 4 / 5 / 6 | 560 / 1820 / 4368 / 8008 | 0 / 0 / 0 / 0 |
| **total** | **14756** | **0** |

Every one of the 30 954 supports has the F1 count exactly 2 and the F2 count
exactly 0.

### Degree pairs and divisibility

| m | (deg P, deg Q) | `3m mod 2m` | `2m mod 3m` | divisibility-ordered |
|---|---|---|---|---|
| 42 | (84, 126) | 42 | 84 | **no** |
| 45 | (90, 135) | 45 | 90 | **no** |
| 48 | (96, 144) | 48 | 96 | **no** |

All three profiles keep the 2:3 shape and none is divisibility-ordered, so
Jung–van der Kulk excludes an automorphism of each of these degree shapes.

---

## 4. The mechanism: the two extreme-ray rows

Let `e0 = min E`, `e1 = max E`, and put

```
phi(v) = e1·v2 − (m−e1)·v1        (zero on the lower extreme ray)
psi(v) = (m−e0)·v1 − e0·v2        (zero on the upper extreme ray)
```

* Over `NP(Q)` the minimum of `phi` is 0 (the ray runs from `(0,0)` to the
  extreme `H^3` monomial `(3e1, 3(m−e1))`; `(0,1)` and all of `supp(H^3)` lie
  on or above it). Over `NP(P)` the minimum is `−(m−e1)`, attained **only** at
  `x = (1,0)`.
* For the row `k = (3e1, 3(m−e1) − 1)` one has `phi(k + (1,1)) = −(m−e1)`, and
  `phi` is additive, so every route must have `phi(p) = −(m−e1)` and
  `phi(a) = 0`: `p = x` and `a` the extreme `H^3` monomial. The row is F1.
* Symmetrically the minimum of `psi` over `NP(P)` is 0 and over `NP(Q)` it is
  `−e0`, attained only at `y = (0,1)`; the row `k = (2e0 − 1, 2(m−e0))` is F1
  with the extreme `H^2` monomial.

The two equations, with the constant row `a_(1,0)·b_(0,1) = 1`:

| row | route | equation |
|---|---|---|
| `(2e0 − 1, 2(m−e0))` | leading `(2e0, 2(m−e0)) = A·h_(e0)^2` × `y` | `2·e0·A·b_(0,1) = 0` |
| `(3e1, 3(m−e1) − 1)` | `x` × leading `(3e1, 3(m−e1)) = B·h_(e1)^3` | `3·(m−e1)·a_(1,0)·B·h_(e1)^3 = 0` |

`m − e1 ≥ 1` always (`m ≡ 0 mod 3` at all three degrees while `e1 ≡ 2 mod 3`),
and `e0 ≥ 2`, so both integer factors are nonzero over `Z`.

**Verification.** For each of the 30 954 supports the screen's F1 row list was
compared with this prediction: `6370/6370`, `9828/9828`, `14756/14756`
matched, with `n_F1 = 2` and `n_F2 = 0` in every case (`screen.verify`).
The stage-1 support `{2,14,29,41}` gives `2e0 − 1 = 3`, `2(m−e0) = 80` and
`3e1 = 123`, `3(m−e1) − 1 = 2` — the rows `(3,80)` and `(123,2)` of
`PRESTRATUM.md` §5.

---

## 5. Small characteristics: where the screen's verdict does not apply

The two row factors are `2·e0` and `3·(m − e1)`. In a characteristic `p`
dividing only one of them the other row still bites; only `p` dividing
`g = gcd(2 e0, 3(m − e1))` can make both vacuous. The two working primes of
the lane, 999983 and 1000003, divide neither factor at any of these degrees
(both factors are at most `3m ≤ 144`), so the §3 tally holds verbatim in
**char 0, char 999983 and char 1000003**.

| m | supports | with `g > 1` | primes occurring (support counts) |
|---|---|---|---|
| 42 | 6370 | 2541 | 2: 2478, 5: 176, 7: 56, 11: 3 |
| 45 | 9828 | 4006 | 2: 3892, 5: 285, 7: 98, 11: 7, 13: 1 |
| 48 | 14756 | 6132 | 2: 5936, 5: 445, 7: 164, 11: 15, 13: 3 |

Those supports were re-screened with a characteristic-aware route test (a
route contributes only when `p1 a2 − p2 a1 ≠ 0 mod p`, which can also promote
*further* rows to normalization-forced), and with characteristic-aware
leading supports: in char 2 the cross terms of `H^2` die
(`H^2 = Σ h_e^2 x^(2e) y^(2m−2e)`, Frobenius) and in char 3 those of `H^3` do,
which shrinks the leading supports — though not the Newton polygons, since
`2e0, 2e1, 3e0, 3e1` survive in every characteristic.

| m | (support, char) pairs re-screened | survivors |
|---|---|---|
| 42 | 2713 | **2713** |
| 45 | 4283 | **4283** |
| 48 | 6563 | **6563** |

So the screen has survivors, and all of them are small-characteristic
survivors. Control: the stage-1 support `{2,14,29,41}` has `g = gcd(4,3) = 1`
and is not among them; re-screened at char 2 it keeps the row `(123,2)` and
at char 3 the row `(3,80)`, so it fails in every characteristic.

---

## 6. The surviving H-supports, ranked

Ranking as specified: fewest near-singleton rows (mandatory rows with exactly
two adjustable routes over the maximal pools, computed in the characteristic
of survival), ties by fewest one-route rows, then lexicographic.

At `m = 42`, char 2 (the largest survivor family): **2478 survivors** —
161 of size 3, 420 of size 4, 791 of size 5, 1106 of size 6. These are exactly
the supports whose largest exponent is even (then `m − e1` is even, so
`3(m−e1) ≡ 0 mod 2`, while `2 e0 ≡ 0 mod 2` always).

Top of the ranking (full list in `rank_char2.json`):

| rank | support `E` | 2-route rows | 1-route rows | rows total | pools P / Q |
|---|---|---|---|---|---|
| 1 | `{5, 8, 11, 17, 29, 32}` | 14 | 15 | 3527 | see JSON |
| 2 | `{5, 8, 11, 23, 29, 32}` | 14 | 15 | 3527 | |
| 3 | `{5, 8, 11, 26, 29, 32}` | 14 | 15 | 3527 | |
| 4 | `{5, 8, 14, 17, 29, 32}` | 14 | 15 | 3527 | |
| 5 | `{5, 8, 17, 20, 29, 32}` | 14 | 15 | 3527 | |

All five have `e0 = 5`, `e1 = 32`, hence `2e0 = 10`, `3(m−e1) = 30` and
`g = 10`: they survive the screen in **char 2 and char 5**.

---

## 7. Carrier build and probe for the top two survivors

Deviation, recorded. The probe of `PRESTRATUM.md` §7 runs at 999983 and
1000003. At both of those primes these supports fail the screen exactly as the
stage-1 support did (§5), so running the probe there would only re-measure the
two-row obstruction. Each of the top two supports is therefore probed in both
characteristics in which it survives, 2 and 5 — the analogue of the dual-prime
discipline. A further loss in char 2: every nonzero coefficient of `F_2` is 1,
so the top parameters are not free and the top chart is a single point; over
`F_5` each has 4 admissible values. A char-2 probe with a large top-parameter
space would need `F_(2^k)`, which was not built.

Everything else is unchanged from stage 1: the same greedy (net-singleton
score, rank-gain tie-break, cap 8), the same 96 + 256 stop, the same controls
and the same halt protocol.

<!--RESULTS-->

---

## 8. File index

| file | content |
|---|---|
| `screen.py` | the screen: char-aware leading supports, fast lattice pools, route analysis, `verify` against the extreme-ray prediction |
| `h_screen_m42.json`, `h_screen_m45.json`, `h_screen_m48.json` | the per-degree sweeps and the residue arms |
| `char_arm.py`, `char_arm.json` | the small-characteristic re-screen |
| `rank.py`, `rank_char2.json` | vectorised near-singleton census and the survivor ranking |
| `survivor_probe.py`, `survivor_*.json` | carrier build and probe for the top two survivors |
| `screen4*_log.txt`, `char_arm_log.txt`, `rank_log.txt`, `survivor_log.txt` | raw run logs |
