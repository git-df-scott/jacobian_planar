# night8 — census of the F_2 points on the E1 enlarged support

Scope note. Measurements only. Every characteristic-2 quantity is labelled as
such. Nothing here says what any of it means.

Scripts: `night8/e1_enumerate.py` (enumeration + its E0 control),
`night8/e1_census.py` (per-point census and ladders).
Data: `night8/e1_points.json`, `night8/e1_census.json` (full per-point table).
Prior files: `MONDELLO_LIFT.md`, `STAR_POINT.md`, `LADDER_8.md`,
`ALL_EIGHT.md` (the E0 census).

## 0. Support and coordinate order

E1 = all lattice points of the convex hulls of the two exact supports:

* `P` (9 monomials): `(1,0) (2,0) (2,1) (3,0) (3,1) (4,0) (4,1) (5,1) (6,2)`
* `Q` (13 monomials): `(0,1) (1,1) (2,1) (3,1) (4,1) (4,2) (5,0) (5,1) (5,2)
  (6,1) (6,2) (7,2) (8,3)`

Coordinate order for every 22-bit string below:

```
a_1_0 a_2_0 a_2_1 a_3_0 a_3_1 a_4_0 a_4_1 a_5_1 a_6_2
b_0_1 b_1_1 b_2_1 b_3_1 b_4_1 b_4_2 b_5_0 b_5_1 b_5_2 b_6_1 b_6_2 b_7_2 b_8_3
```

System: 22 unknowns, 34 equations — (K) every coefficient of
`P_x Q_y - P_y Q_x - 1`, plus (C2) `P(0,1)-P(1,0)=0`, `Q(0,1)-Q(1,0)=0`.

## 1. Exhaustive enumeration over F_2^22

`det J = P_x Q_y - P_y Q_x` is bilinear in `(a,b)` and (C2) is linear, so every
equation has the shape

```
e(a,b) = const + sum_m alpha_m a_m + sum_n beta_n b_n + sum_{m,n} c_{mn} a_m b_n .
```

Those coefficients were extracted once symbolically; then for each of the
`2^9 = 512` choices of `a` the entire system is an affine linear system in the
13 unknowns `b` over `F_2`, solved exactly by Gaussian elimination and its
solution set enumerated in full. This covers all `2^22 = 4194304` points of
`F_2^22` — every point is decided, none is sampled.

* `a`-vectors giving a consistent linear system: **16 of 512**.
* **Total `F_2` points of (K)+(C2) on E1: 144.**
* Every one of the 144 was re-substituted into the 34 equations and verified.

**Control.** The identical routine run on the E0 support returns exactly the
8 points, and the set matches the independent brute-force enumeration of
`night8/verify_lift.py` element for element.

## 2. Universal checks (all 144 points)

* `det J = 1` exactly in `F_2[x,y]`, by direct expansion: **144 / 144**.
* `F(0,1) = F(1,0) = (0,1)`: **144 / 144**.
* No failures of either check (`universal_checks_failures` is empty).
* `F(1,1)` in the same fibre as `F(0,1)`: 36 of 144.

## 3. Class counts

| class | count (of 144) |
|---|---|
| additive-type (char-2 screen) | **2** |
| proper non-additive | **142** |
| tear EMPTY (char 2) | 86 |
| **tear NONEMPTY (char 2)** | **58** |
| E0 points embedded in E1 | 8 |
| ladders run (NONEMPTY and not an E0 point) | **55** |

The two additive-type points (screen: `P` free of `y` and `Q - y` free of `y`,
or the `x <-> y` mirror) are

| bits | `P` | `Q` | tear | E0 point? |
|---|---|---|---|---|
| `1000010001000001000000` | `x + x^4` | `y + x^5` | EMPTY | yes, the star point `101011000` |
| `1100000001000001000000` | `x + x^2` | `y + x^5` | EMPTY | no (uses `a_2_0`, outside E0) |

Both are TEAR-EMPTY, so neither is laddered under rule (4).

The 8 embedded E0 points were located inside E1 by coefficient embedding and
are marked in `e1_census.json` (`is_an_E0_point`, `E0_bits`). Their tear
classification here reproduces the E0 census exactly: NONEMPTY for
`101011010`, `111111100`, `111111111`; EMPTY for the other five. Their ladders
are on record in `ALL_EIGHT.md` and were not re-run; note that an E0 point sits
in a *larger* deformation problem inside E1 (22 unknowns, 34 equations), so its
E1 ladder is a different computation, not performed here.

## 4. Ladders

Rule (4): every TEAR-NONEMPTY point that is not one of the 8 embedded E0
points — **55 points** — was climbed with the derivation of
`MONDELLO_LIFT.md` §5, `J` recomputed at each point, carrying **all** lifts at
every level, ceiling mod 64. A carry cap of 200000 points per level was armed;
**it was never reached**.

Ranks at the laddered points: `rank(J mod 2)` is 13, 14 or 15 (nullity 9, 8, 7)
— 14 points of nullity 9, 28 of nullity 8, 13 of nullity 7.

| outcome | count |
|---|---|
| die at mod 4 (no mod-4 lift at all) | **53** |
| reach mod 4, die at mod 8 | **2** |
| reach mod 8 or higher | 0 |
| **survive to the mod-64 ceiling** | **0** |

The two that reach mod 4 each have `rank(J mod 2) = 15`, nullity 7, and
**128** solutions mod 4 (a coset of dimension 7); all 128 fail the mod-8 step
in both cases:

| bits | `P` | `Q` | product of tear leading coefficients | obstruction rows at a representative mod-8 death |
|---|---|---|---|---|
| `1001001001010101011011` | `x + x^3 + x^4 y` | `y + x^2 y + x^4 y + x^5 + x^5 y^2 + x^6 y + x^7 y^2 + x^8 y^3` | `u^9 + u^8 v + u + v` | `K(11,3)`, `K(3,1)` |
| `1101011001010111011111` | `x + x^2 + x^3 + x^4 + x^4 y` | `y + x^2 y + x^4 y + x^4 y^2 + x^5 + x^5 y^2 + x^6 y + x^6 y^2 + x^7 y^2 + x^8 y^3` | `u^8 + u^4 + 1` | `K(11,3)`, `K(7,1)`, `K(5,1)`, `K(3,1)` |

In every death, at every level, `rank([J | s_k] mod 2) = rank(J mod 2) + 1`,
and the obstruction rows listed are rows whose gradient vanishes identically
mod 2 while the right-hand side is 1, so the congruence reads `0 = 1 (mod 2)`.

Frequency of obstruction rows across the 53 mod-4 deaths (first representative
death of each point): `K(5,1)` 26, `K(6,1)` 16, `K(7,1)` 16, `K(1,1)` 12,
`K(5,2)` 9, `K(9,2)` 6, `K(7,2)` 6, `K(10,1)` 5, `K(9,1)` 5, `K(11,2)` 4,
`K(12,3)` 1.

### Full ladder listing (55 points)

| point (22 bits) | death level | nullity of `J mod 2` | obstruction rows at a representative death |
|---|---|---|---|
| `1001001001010101011011` | 8 | 7 | `K(11, 3),K(3, 1)` |
| `1101011001010111011111` | 8 | 7 | `K(11, 3),K(7, 1),K(5, 1),K(3, 1)` |
| `1000010001000001000100` | 4 | 9 | `K(6, 1)` |
| `1000010001000001000110` | 4 | 9 | `K(7, 1),K(6, 1)` |
| `1000010001000001010000` | 4 | 8 | `K(5, 1)` |
| `1000010001000001010010` | 4 | 8 | `K(7, 1),K(5, 1)` |
| `1000010001000001010100` | 4 | 8 | `K(6, 1),K(5, 1)` |
| `1000010001000001010110` | 4 | 8 | `K(7, 1),K(6, 1),K(5, 1)` |
| `1000010001000011000000` | 4 | 9 | `` |
| `1000010001000011000010` | 4 | 9 | `K(7, 1)` |
| `1000010001000011000100` | 4 | 9 | `K(6, 1)` |
| `1000010001000011000110` | 4 | 9 | `K(7, 1),K(6, 1)` |
| `1000010001000011010000` | 4 | 8 | `K(5, 1)` |
| `1000010001000011010010` | 4 | 8 | `K(7, 1),K(5, 1)` |
| `1000010001000011010100` | 4 | 8 | `K(6, 1),K(5, 1)` |
| `1000010001000011010110` | 4 | 8 | `K(7, 1),K(6, 1),K(5, 1)` |
| `1000010011000011000010` | 4 | 9 | `K(12, 3),K(10, 1),K(7, 1),K(5, 2)` |
| `1001001001010101001000` | 4 | 8 | `K(9, 1),K(5, 1)` |
| `1001001001010101011111` | 4 | 7 | `` |
| `1001001001010111001000` | 4 | 8 | `K(9, 1),K(5, 1)` |
| `1001001001010111001100` | 4 | 8 | `K(9, 2),K(9, 1),K(5, 1)` |
| `1001001001010111011011` | 4 | 7 | `` |
| `1001001001010111011111` | 4 | 7 | `` |
| `1010010001000011001000` | 4 | 8 | `K(1, 1)` |
| `1010010011000011001000` | 4 | 8 | `K(11, 2),K(5, 2),K(1, 1)` |
| `1010010011000011001100` | 4 | 8 | `K(11, 2),K(7, 2),K(5, 2),K(1, 1)` |
| `1011000001010101000000` | 4 | 7 | `K(5, 1),K(1, 1)` |
| `1011000011010111000000` | 4 | 7 | `K(10, 1),K(9, 2),K(7, 2),K(5, 2),K(5, 1),K(1, 1)` |
| `1011000011010111000100` | 4 | 7 | `K(10, 1),K(9, 2),K(5, 2),K(5, 1),K(1, 1)` |
| `1100000001000001000010` | 4 | 9 | `K(7, 1)` |
| `1100000001000001000100` | 4 | 9 | `K(6, 1)` |
| `1100000001000001000110` | 4 | 9 | `K(7, 1),K(6, 1)` |
| `1100000001000001010000` | 4 | 8 | `K(5, 1)` |
| `1100000001000001010010` | 4 | 8 | `K(7, 1),K(5, 1)` |
| `1100000001000001010100` | 4 | 8 | `K(6, 1),K(5, 1)` |
| `1100000001000001010110` | 4 | 8 | `K(7, 1),K(6, 1),K(5, 1)` |
| `1100000001000011000000` | 4 | 9 | `` |
| `1100000001000011000010` | 4 | 9 | `K(7, 1)` |
| `1100000001000011000100` | 4 | 9 | `K(6, 1)` |
| `1100000001000011000110` | 4 | 9 | `K(7, 1),K(6, 1)` |
| `1100000001000011010000` | 4 | 8 | `K(5, 1)` |
| `1100000001000011010010` | 4 | 8 | `K(7, 1),K(5, 1)` |
| `1100000001000011010100` | 4 | 8 | `K(6, 1),K(5, 1)` |
| `1100000001000011010110` | 4 | 8 | `K(7, 1),K(6, 1),K(5, 1)` |
| `1101011001010101011011` | 4 | 7 | `` |
| `1101011001010101011111` | 4 | 7 | `` |
| `1101011001010111001000` | 4 | 8 | `K(9, 1),K(5, 1)` |
| `1101011001010111001100` | 4 | 8 | `K(9, 2),K(9, 1),K(5, 1)` |
| `1101011001010111011011` | 4 | 7 | `` |
| `1110000001000001001100` | 4 | 8 | `K(7, 2),K(1, 1)` |
| `1110000001000011001100` | 4 | 8 | `K(7, 2),K(1, 1)` |
| `1110000011000011001000` | 4 | 8 | `K(11, 2),K(5, 2),K(1, 1)` |
| `1110000011000011001100` | 4 | 8 | `K(11, 2),K(7, 2),K(5, 2),K(1, 1)` |
| `1111010011010111000000` | 4 | 7 | `K(10, 1),K(9, 2),K(7, 2),K(5, 2),K(5, 1),K(1, 1)` |
| `1111010011010111000100` | 4 | 7 | `K(10, 1),K(9, 2),K(5, 2),K(5, 1),K(1, 1)` |

## 5. Summary

| quantity | value |
|---|---|
| search space | `2^22 = 4194304`, exhaustively decided |
| `F_2` points of (K)+(C2) on E1 | **144** |
| `det J = 1` exact / collision verified | 144 / 144 |
| additive-type | 2 |
| proper non-additive | 142 |
| tear NONEMPTY (char 2) | 58 |
| embedded E0 points | 8 |
| ladders run | 55 |
| deaths at mod 4 / mod 8 | 53 / 2 |
| points surviving to mod 64 | **0** |
| carry cap (200000) reached | never |
