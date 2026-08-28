# night8 — census of all 8 F_2 points of the E0 system

Scope note. Measurements only. Every characteristic-2 quantity is labelled as
such. Nothing here says what any of it means.

Script: `night8/all_eight.py`. Data: `night8/all_eight.json`.
Supporting files: `MONDELLO_LIFT.md` (the system and the Hensel derivation),
`STAR_POINT.md`, `LADDER_8.md`, `verify_lift.json` (exhaustive searches).

## 0. Setup

E0 coordinate order, used in every bit-string below:

```
( a_1_0 , a_2_1 , a_4_0 , a_6_2 , b_0_1 , b_5_0 , b_6_1 , b_7_2 , b_8_3 )
```

System over `F_2` / over `Z`: (K) every coefficient of `P_x Q_y - P_y Q_x - 1`
vanishes, plus (C2) `P(0,1) - P(1,0) = 0` and `Q(0,1) - Q(1,0) = 0` with the
collision points held fixed. The system has exactly **8** `F_2`-rational
points (exhaustive enumeration, `verify_lift.py`), listed below.

Definitions used in the classification columns:

* **additive-type screen** (char 2): `P` free of `y` **and** `Q - y` free of
  `y`; or the `x <-> y` mirror, `Q` free of `x` and `P - x` free of `x`.
* **tear** (char 2): `R1 = Res_y(P-u, Q-v)` kept in `x`, `R2 = Res_x(P-u,Q-v)`
  kept in `y`, coefficients in `GF(2)[u,v]`; **EMPTY** means the product of
  the two leading coefficients is a nonzero constant, **NONEMPTY** means it is
  not. The characteristic-zero statement behind this construction is not
  claimed to apply in characteristic 2; these are char-2 measurements.
* **ladder**: the 2-adic climb of `night8/LADDER_8.md` §2, carrying **all**
  lifts at every level, ceiling mod 64. Run for every point that is
  non-additive-type **and** TEAR-NONEMPTY; the base and star points are
  recomputed here too so the census is uniform.

Universal checks, all 8 points: `det J = 1` exactly in `F_2[x,y]` and
`F(0,1) = F(1,0) = (0,1)`. Both hold for all 8 (verified pointwise by direct
expansion / substitution). All 8 have `rank(J mod 2) = 5`, nullity 4.

## 1. The eight pairs

| # | point | `P` | `Q` | `deg P` | `deg Q` |
|---|---|---|---|---|---|
| 1 | `101011000` (**star**) | `x + x^4` | `y + x^5` | 4 | 5 |
| 2 | `101011010` | `x + x^4` | `y + x^5 + x^7 y^2` | 4 | 9 |
| 3 | `101111000` | `x + x^4 + x^6 y^2` | `y + x^5` | 8 | 5 |
| 4 | `101111010` | `x + x^4 + x^6 y^2` | `y + x^5 + x^7 y^2` | 8 | 9 |
| 5 | `111011100` | `x + x^2 y + x^4` | `y + x^5 + x^6 y` | 4 | 7 |
| 6 | `111011111` | `x + x^2 y + x^4` | `y + x^5 + x^6 y + x^7 y^2 + x^8 y^3` | 4 | 11 |
| 7 | `111111100` | `x + x^2 y + x^4 + x^6 y^2` | `y + x^5 + x^6 y` | 8 | 7 |
| 8 | `111111111` (**base**) | `x + x^2 y + x^4 + x^6 y^2` | `y + x^5 + x^6 y + x^7 y^2 + x^8 y^3` | 8 | 11 |

Point 8 is the extracted Mondello pair; point 1 is the star point of
`STAR_POINT.md`.

## 2. Classification and ladder — SUMMARY TABLE

| # | point | additive-type (char 2) | tear (char 2): `lc(R1)`, `lc(R2)`, product | tear verdict | `F(1,1)` | ladder | death level | obstruction rows at the death |
|---|---|---|---|---|---|---|---|---|
| 1 | `101011000` | **YES** (forward form) | `1`, `1`, `1` | EMPTY | `(0,0)` | run (on record) | **8** | `K(3,0)`; also `K(7,1)`, `K(1,1)` for other representatives |
| 2 | `101011010` | no | `1`, `u^7`, `u^7` | NONEMPTY | `(0,1)` | run | **4** | `K(7,1)` |
| 3 | `101111000` | no | `1`, `1`, `1` | EMPTY | `(1,0)` | classification only | — | — |
| 4 | `101111010` | no | `1`, `1`, `1` | EMPTY | `(1,1)` | classification only | — | — |
| 5 | `111011100` | no | `1`, `1`, `1` | EMPTY | `(1,1)` | classification only | — | — |
| 6 | `111011111` | no | `1`, `1`, `1` | EMPTY | `(1,1)` | classification only | — | — |
| 7 | `111111100` | no | `u`, `1`, `u` | NONEMPTY | `(0,1)` | run | **4** | `K(11,2)`, `K(10,1)`, `K(5,2)`, `K(1,1)` |
| 8 | `111111111` | no | `v^2`, `1`, `v^2` | NONEMPTY | `(0,1)` | run | **4** | `K(13,4)`, `K(12,3)`, `K(11,2)`, `K(10,1)`, `K(9,3)`, `K(7,1)`, `K(5,2)`, `K(1,1)` |

**No point survives to the mod-64 ceiling.** Exactly one point (the star,
#1) reaches mod 4, with 16 solutions there, and dies at mod 8. The other seven
die at mod 4. In every death `rank(J mod 2) = 5` while
`rank([J | s_k] mod 2) = 6`, and the obstruction rows listed are rows whose
gradient vanishes identically mod 2 while the right-hand side is 1, so the
congruence reads `0 ≡ 1 (mod 2)`.

The ladder was run for #1, #2, #7, #8. For the four classification-only points
(#3, #4, #5, #6) the corresponding existence statement is nevertheless already
on record from a different computation: the exhaustive search over all
`4^9 = 262144` points of `(Z/4)^9` in `night8/verify_lift.py` found 16
solutions mod 4 in total, all of them lying over the star point, hence **0**
mod-4 lifts over each of #2 .. #8. The ladder results for #2, #7, #8 agree with
that exhaustive count, and the #8 ladder reproduces the base-point result of
`MONDELLO_LIFT.md` (death at mod 4, same eight obstruction rows).

## 3. Tear detail (characteristic-2 measurements)

| # | `deg_x R1` / Sylvester bound | `deg_y R2` / bound | flags beyond `POSITIVE_CHARACTERISTIC` |
|---|---|---|---|
| 1 | 4 / 4 | 4 / 4 | — |
| 2 | 8 / 8 | 8 / 8 | — |
| 3 | 16 / 16 | 16 / 16 | — |
| 4 | 16 / 26 | 20 / 26 | `DEGREE_DROP:R1(16<26)`, `DEGREE_DROP:R2(20<26)` |
| 5 | 10 / 10 | 10 / 10 | — |
| 6 | 20 / 20 | 16 / 20 | `DEGREE_DROP:R2(16<20)` |
| 7 | 12 / 18 | 18 / 18 | `DEGREE_DROP:R1(12<18)` |
| 8 | 18 / 34 | 19 / 34 | `DEGREE_DROP:R1(18<34)`, `DEGREE_DROP:R2(19<34)` |

No resultant was identically zero; every `det J` is `1`, so no `NOT_DOMINANT`
flag anywhere. Row 8 reproduces the values night7 recorded independently for
the same pair.

## 4. Tail profiles mod 2 (characteristic-2 measurements)

Formal-inverse recursion to `D = 2 deg F + 4`, reimplemented in-lane; the
mandatory recomposition self-check `G(F) = id` through degree `D` **passed for
all 8 points**. Profile = number of nonzero coefficients of `G^(m)`, both
components summed, for `m = deg F + 1 .. D`.

| # | `deg F` | `D` | first nonzero tail degree | profile |
|---|---|---|---|---|
| 1 | 5  | 14 | 8  | `0 0 1 0 0 0 0 0 0` |
| 2 | 9  | 22 | 12 | `0 0 1 0 0 1 1 0 1 0 1 1 0` |
| 3 | 8  | 20 | 12 | `0 0 0 1 0 1 0 0 1 1 0 2` |
| 4 | 9  | 22 | 14 | `0 0 0 0 1 1 1 0 0 0 1 1 1` |
| 5 | 7  | 18 | 8  | `1 1 1 1 1 2 1 3 0 1 0` |
| 6 | 11 | 26 | 12 | `2 1 0 4 1 1 1 2 1 3 0 1 0 2 1` |
| 7 | 8  | 20 | 9  | `1 1 1 1 2 1 3 3 2 1 1 2` |
| 8 | 11 | 26 | 13 | `0 1 0 4 3 2 1 2 1 2 1 0 0 1 0` |

No profile is identically zero. (Control on the reimplementation, recorded in
`STAR_POINT.md`: three tame automorphisms give identically zero tails.)

## 5. Collisions

All 8 points satisfy `F(0,1) = F(1,0) = (0,1)` — imposed by (C2) and verified
directly. The third Mondello collision point behaves as follows:
`F(1,1) = (0,1)` (same fibre) for #2, #7, #8; `F(1,1) = (0,0)` for #1;
`F(1,1) = (1,0)` for #3; `F(1,1) = (1,1)` for #4, #5, #6.
