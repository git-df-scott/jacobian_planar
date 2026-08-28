# night8 — JOB 2: the 2-adic ladder over the distinguished F_2 point

Scope note. Measurements only. The file records at which level lifts exist and
the linear-algebra evidence; it says nothing about what that means.

Script: `night8/ladder.py`. Data: `night8/ladder.json`.
The level of death is **8**, hence the file name.

## 0. Coordinate order and the point

Order (same as everywhere in night8):

```
( a_1_0 , a_2_1 , a_4_0 , a_6_2 , b_0_1 , b_5_0 , b_6_1 , b_7_2 , b_8_3 )
```

Star point `(1, 0, 1, 0, 1, 1, 0, 0, 0)`, i.e. `P* = x + x^4`, `Q* = y + x^5`
(identified in `night8/STAR_POINT.md`).

System over `Z`: the E0 system of `night8/MONDELLO_LIFT.md` — 9 unknowns,
15 equations: (K) every coefficient of `P_x Q_y - P_y Q_x - 1`, and (C2)
`P(0,1) - P(1,0) = 0`, `Q(0,1) - Q(1,0) = 0`.

Integer residual of the star point: `K(3,0) = 4`, `C2_P = -2`, all other
thirteen equations exactly `0`; all residuals even, so the star point is a
mod-2 solution.

## 1. The Jacobian at the star point, recomputed

`J` was recomputed at the star point, not reused from the base point.

* `rank(J mod 2) = 5`, `nullity = 4`, 10 rows identically zero mod 2
  (`K(13,4) K(12,3) K(11,2) K(10,1) K(9,3) K(9,0) K(7,1) K(5,2) K(3,0)
  K(1,1)` — the same ten labels as at the base point).
* **`J mod 2` at the star point is NOT equal to `J mod 2` at the base point**
  (same rank and nullity, different matrix). Nonzero rows at the star point,
  columns in the order above:

```
K(8,2) : 0 0 0 0 0 0 0 0 1
K(6,0) : 0 1 0 0 0 0 1 0 0
K(0,0) : 1 0 0 0 1 0 0 0 0
C2_P   : 1 0 1 0 0 0 0 0 0
C2_Q   : 0 0 0 0 1 1 0 0 0
```

## 2. The step

Identical derivation to `night8/MONDELLO_LIFT.md` §5: `r` is quadratic, so for
`x_{k+1} = x_k + 2^k d` and `r(x_k) = 2^k s_k`,

```
r(x_k + 2^k d) ≡ 2^k ( s_k + J d )   (mod 2^{k+1}),      J = Dr(star) mod 2,
```

the step being the `F_2` linear system `J d = s_k` (`-s_k = s_k` over `F_2`),
solvable iff `rank(J) = rank([J | s_k])`, with solution set a coset of
`ker(J)` of dimension `nullity = 4`.

All lifts are carried forward: at each level the complete set of solutions mod
`2^{k+1}` lying over the star point is enumerated, not a single representative.
The ceiling set for this job was mod 64.

## 3. Survivor table

| step | points in | of which the linear step is solvable | dim of the linear-step solution space | solutions out | verdict |
|---|---|---|---|---|---|
| mod 2 → mod 4 | 1 | 1 | 4 | **16** | EXISTS |
| mod 4 → mod 8 | 16 | **0** | — | **0** | **DOES-NOT-EXIST** |
| mod 8 → mod 16 | — | — | — | — | not reached |
| mod 16 → mod 32 | — | — | — | — | not reached |
| mod 32 → mod 64 | — | — | — | — | not reached |

Highest level reached: **4**. Level of death: **8**. All 16 of the mod-4 lifts
die at the mod-8 step; none survives.

Verification control at level 4: every one of the 16 solutions was re-evaluated
and has all 15 residuals `≡ 0 mod 4`.

## 4. Obstruction rows at the deaths

For each of the 16, `rank(J mod 2) = 5` while `rank([J | s_2] mod 2) = 6`. In
each case the inconsistency is visible in rows whose gradient mod 2 vanishes
while the right-hand side is 1, i.e. the congruence reads `0 ≡ 1 (mod 2)`.
Three representative deaths, verbatim from `night8/ladder.json`:

| mod-4 point | rows with `s_2 = 1` | obstruction rows (zero gradient, rhs 1) |
|---|---|---|
| `(1,0,3,0,1,1,0,0,0)` | `K(3,0) C2_P` | **`K(3,0)`** |
| `(1,0,3,0,1,1,0,2,0)` | `K(7,1) K(3,0) C2_P` | **`K(7,1)`, `K(3,0)`** |
| `(1,2,3,0,1,1,2,0,0)` | `K(3,0) K(1,1) C2_P` | **`K(3,0)`, `K(1,1)`** |

`K(3,0)` is an obstruction row for the first representative and appears in all
three; `C2_P` has a nonzero gradient mod 2 and is not itself an obstruction row.

## 5. Controls

* The 16 mod-4 solutions produced by the ladder coincide exactly, as residues
  mod 4, with the 16 found by the exhaustive `(Z/4)^9` search of
  `night8/verify_lift.py` (which searched all 262144 points): **match**.
* Exhaustive mod-8 brute force over every point congruent to one of those 16
  solutions mod 4 — `16 * 2^9 = 8192` candidates, all evaluated — found
  **0** solutions mod 8. This agrees with the linear-algebra verdict.

## 6. Summary

| quantity | value |
|---|---|
| `rank(J mod 2)` / nullity at the star point | 5 / 4 |
| `J mod 2` equal to the base point's | no |
| mod-4 lifts of the star point | 16 (EXISTS, step dimension 4) |
| mod-8 lifts | 0 (DOES-NOT-EXIST; 0 of 16 solvable) |
| mod 16 / 32 / 64 | not reached |
| exhaustive mod-8 control | 8192 candidates tested, 0 solutions |
