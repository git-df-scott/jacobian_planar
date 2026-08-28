# night8 — JOB 1: identification of the distinguished F_2 point

Scope note. Measurements only. Nothing here says what any number means.
Every characteristic-2 quantity is labelled as such.

Script: `night8/star_point.py`. Data: `night8/star_point.json`.
The formal-inverse tail recursion (method of `night4/tail.py`) and the
resultant / leading-coefficient measurement (statement used in night7's tear
evaluator) are **reimplemented in-lane** in `night8/star_point.py`; nothing is
imported from `night4/`, `night6/` or `night7/`.

## 0. Coordinate order (stated explicitly)

The E0 coordinate vector used throughout night8 is, in this order:

```
( a_1_0 , a_2_1 , a_4_0 , a_6_2 , b_0_1 , b_5_0 , b_6_1 , b_7_2 , b_8_3 )
```

where `a_i_j` is the coefficient of `x^i y^j` in `P` and `b_i_j` the
coefficient of `x^i y^j` in `Q`. In this order,

* the **star point** is `(1, 0, 1, 0, 1, 1, 0, 0, 0)`;
* the **Mondello base point** is `(1, 1, 1, 1, 1, 1, 1, 1, 1)`.

## 1. The pair

```
P*(x, y) = x + x^4
Q*(x, y) = y + x^5
```

* Coefficients present: `a_1_0, a_4_0, b_0_1, b_5_0` (all `= 1`).
* Coefficients zero: `a_2_1, a_6_2, b_6_1, b_7_2, b_8_3`.
* Support of `P*`: `{(1,0), (4,0)}`; support of `Q*`: `{(0,1), (5,0)}`.
* `deg P* = 4`, `deg Q* = 5`, `deg F* = 5`.
* `P*` involves no `y`; `Q* - y` involves no `y`.

## 2. Jacobian determinant, by direct expansion

`P*_x = 1 + 4x^3`, `P*_y = 0`, `Q*_x = 5x^4`, `Q*_y = 1`, so over `Z`

```
det J(P*, Q*) = (1 + 4x^3)(1) - 0 * (5x^4) = 4x^3 + 1
```

and reducing, **`det J(P*, Q*) = 1` exactly in `F_2[x,y]`** (verified by direct
expansion, `sp.Poly(..., domain=GF(2))`), as it must be by construction from
the (K) equations.

## 3. Images and the collision

Over `F_2`:

| point | `P*` | `Q*` | image |
|---|---|---|---|
| `(0,1)` | 0 | 1 | `(0,1)` |
| `(1,0)` | 0 | 1 | `(0,1)` |
| `(1,1)` | 0 | 0 | `(0,0)` |
| `(0,0)` | 0 | 0 | `(0,0)` |

`F*(0,1) = F*(1,0) = (0,1)`: the two-point collision imposed by (C2) holds, as
it must by construction (verified). `F*(1,1) = (0,0) ≠ (0,1)`, so the third
point of the Mondello collision is not in the same fibre for this pair;
`F*(1,1) = F*(0,0) = (0,0)`.

## 4. Relation to the Mondello base point

Base pair: `P = x + x^2 y + x^4 + x^6 y^2`, `Q = y + x^5 + x^6 y + x^7 y^2 +
x^8 y^3`.

* Equal to the base pair: **no**.
* Coordinate relation (recorded): the star point is the base point with the
  five coefficients `a_2_1, a_6_2, b_6_1, b_7_2, b_8_3` set to `0`.
* `x <-> y` swap conjugation of the base pair,
  `F^σ = (Q(y,x), P(y,x))`:
  `P = x + y^5 + x y^6 + x^2 y^7 + x^3 y^8`, `Q = y + x y^2 + y^4 + x^2 y^6`.
  Equal to the star pair: **no**.
* `x <-> y` swap conjugation of the star pair itself:
  `(x + y^5, y + y^4)`. Equal to the star pair: **no** (the star pair is not
  swap-invariant).
* Coefficientwise Frobenius squaring: over `F_2` every coefficient satisfies
  `c^2 = c`, so this operation is the identity on both pairs and relates
  nothing that was not already equal.

**Verdict: no obvious relation** under the checked symmetries (equality,
`x <-> y` swap conjugation, coefficientwise Frobenius). The only relation
recorded is the coordinate one above.

## 5. Tail recursion mod 2 — CHARACTERISTIC-2 MEASUREMENT

Linear part of `F*` is `[[1,0],[0,1]]`, invertible mod 2, so the recursion
runs. `deg F* = 5`, bound `D = 2*deg + 4 = 14`.

* Mandatory recomposition self-check `G(F*) = id` through degree `D`:
  **PASSED** (the assembled `G` is recomposed with `F*` from scratch).
* Tail profile (number of nonzero coefficients of `G^(m)`, both components
  summed), `m = 6 .. 14`:

```
degree:  6  7  8  9 10 11 12 13 14
count :  0  0  1  0  0  0  0  0  0
```

* `tail_all_zero`: **False**; first nonzero tail degree: **8**;
  `deg G` computed through `D`: 8.

Reimplementation controls (mod 2, `D = 14`): the tame automorphisms
`(x, y+x^2)`, `(x+y^3, y)` and `(x, y+x^2) o (x+y^2, y)` all have identically
zero tail and pass the self-check.

For comparison, the same char-2 measurement on the Mondello base pair
(`deg F = 11`, `D = 26`), degrees 12..26:

```
0  1  0  4  3  2  1  2  1  2  1  0  0  1  0      (first nonzero at degree 13)
```

## 6. Resultant / leading-coefficient data — CHARACTERISTIC-2 MEASUREMENT

`R1 = Res_y(P* - u, Q* - v)` kept in `x`; `R2 = Res_x(P* - u, Q* - v)` kept in
`y`; coefficients in `GF(2)[u,v]`.

| | eliminated | source var | `deg` in source var | Sylvester bound | leading coefficient |
|---|---|---|---|---|---|
| `R1` | `y` | `x` | 4 | 4 | `1` (constant) |
| `R2` | `x` | `y` | 4 | 4 | `1` (constant) |

```
R1 = x^4 + x + u
R2 = y^4 + y + v + u^5 + u^3 v + u^3 y + u v^2 + u y^2 + v^4
```

Product of the two leading coefficients: `1` — a nonzero constant. Flags:
`POSITIVE_CHARACTERISTIC` only (no degree drop, no identically zero resultant,
Jacobian determinant `1` so no `NOT_DOMINANT` flag).

The same measurement on the Mondello base pair, characteristic 2:

| | `deg` in source var | Sylvester bound | leading coefficient |
|---|---|---|---|
| `R1` | 18 | 34 | `v^2` |
| `R2` | 19 | 34 | `1` |

product `v^2`; flags `POSITIVE_CHARACTERISTIC`, `DEGREE_DROP:R1(18<34)`,
`DEGREE_DROP:R2(19<34)`. These four numbers and the two leading coefficients
agree exactly with the values night7 recorded independently for the same pair,
which is a cross-check on this in-lane reimplementation.

Reimplementation controls, characteristic 0: `(x, y+x^2)` gives constant
leading coefficients on both branches; `(x, x*y)` gives product of leading
coefficients `u`.

The characteristic-zero statement behind this construction is not claimed to
apply in characteristic 2; the entries above are recorded as characteristic-2
measurements.
