# night8 — deformation space and 2-adic lift measurements for the night5/mondello object

Scope note. This file records measurements only. It states what was computed
and what the computations returned. It contains no assessment of what any of
these numbers mean.

## 0. The object and the two scripts

From `night5/mondello/mondello_map.json` (arXiv 2608.02634, Theorem 1.2), over
`F_2`:

```
P(x,y) = x + x^2 y + x^4 + x^6 y^2
Q(x,y) = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3
```

with `det J(P,Q) = 1` exactly in `F_2[x,y]` and the verified collisions
`F(0,1) = F(1,0) = F(1,1) = (0,1)`.

Scripts:

* `night8/mondello_lift.py` — builds the systems, the witness control, STEP 1
  (tangent ranks, Groebner over GF(2)), STEP 2 (smoothness mod 2) and STEP 3
  (2-adic lifting). Output: `night8/mondello_lift.json`.
* `night8/verify_lift.py` — independent controls: exhaustive brute force over
  `(Z/4)^9` and `(F_2)^9`, Groebner reduction controls, Krull dimension of the
  E0 ideal by maximal independent set, and a per-`F_2`-point table. Output:
  `night8/verify_lift.json`.
* `night8/mondello_ranks.json` — compact JSON of the matrix ranks.

## 1. Unknowns, supports, equations

Unknowns are the coefficients `a_m` (`m` in the support `E_P` of `P`) and `b_n`
(`n` in the support `E_Q` of `Q`); variables are named `a_i_j`, `b_i_j` for the
monomial `x^i y^j`.

The system, in both the char-2 and the integral setting:

* **(K)** every coefficient (as a polynomial in `x`, `y`) of
  `P_x Q_y - P_y Q_x - 1` is set to `0`;
* **(C2)** `P(0,1) - P(1,0) = 0` and `Q(0,1) - Q(1,0) = 0`. The two collision
  **points** `(0,1)` and `(1,0)` are held fixed; the unknowns are the
  coefficients. Written out on E0 these two equations are
  `-a_1_0 - a_4_0 = 0` and `b_0_1 - b_5_0 = 0`.

Every equation is a polynomial with integer coefficients, of total degree 2 in
the unknowns for (K) and degree 1 for (C2). The char-2 system is the entrywise
mod-2 reduction of the integral one, so differentiation and reduction commute
and one code path serves both settings.

### Supports

**E0 (exact supports).**

```
S_P = {(1,0), (2,1), (4,0), (6,2)}          |S_P| = 4
S_Q = {(0,1), (5,0), (6,1), (7,2), (8,3)}   |S_Q| = 5
```
Unknowns: 9.

**E1 (all lattice points of the convex hulls).** Hulls computed by exact
integer monotone-chain, lattice points by exact in-hull test.

* `conv(S_P)` vertices: `(1,0), (4,0), (6,2), (2,1)` (all four support points
  are vertices). Lattice points (9):
  `(1,0) (2,0) (2,1) (3,0) (3,1) (4,0) (4,1) (5,1) (6,2)`.
* `conv(S_Q)` vertices: `(0,1), (5,0), (8,3)` (a triangle; `(6,1)` and `(7,2)`
  are non-vertex points of `S_Q`). Lattice points (13):
  `(0,1) (1,1) (2,1) (3,1) (4,1) (4,2) (5,0) (5,1) (5,2) (6,1) (6,2) (7,2)
  (8,3)`.

E1 sizes: `|S_P| = 9`, `|S_Q| = 13`; unknowns: 22.

The base point is, in both cases, coefficient `1` on the exact support of the
extracted pair and `0` on every added monomial.

## 2. Witness control (run first; hard exit on failure)

| system | equations | of which from (K) | unknowns | base residual `= 0 mod 2` for every equation |
|---|---|---|---|---|
| E0 | 15 | 13 | 9  | **yes** |
| E1 | 34 | 32 | 22 | **yes** |

PASSED for both. (Equation count = number of monomials with a symbolically
nonzero coefficient in `P_x Q_y - P_y Q_x - 1`, plus the two (C2) equations.)

Over `Z` the base point is not a solution: the nonzero integer residuals on E0
are

```
K(13,4)=2  K(12,3)=-2  K(11,2)=6  K(10,1)=-2  K(9,3)=-2  K(9,0)=4
K(7,1)=-2  K(6,0)=-4   K(5,2)=6   K(3,0)=4    K(1,1)=2   C2_P=-2
```

all even, and `K(0,0) = 0` (the constant coefficient of
`P_x Q_y - P_y Q_x - 1` vanishes over `Z`).

## 3. STEP 1 — tangent space of the char-2 deformation space at the base point

Jacobian of the full system (K)+(C2) with respect to all coefficient unknowns,
evaluated at the base point, over `F_2`:

| system | unknowns `N` | equations `M` | rank(J mod 2) | nullity (`N - rank`) | rows identically zero mod 2 |
|---|---|---|---|---|---|
| E0 | 9  | 15 | **5**  | **4** | 10 |
| E1 | 22 | 34 | **14** | **8** | 10 |

Rows whose gradient vanishes identically mod 2 at the base point:

* E0: `K(13,4) K(12,3) K(11,2) K(10,1) K(9,3) K(9,0) K(7,1) K(5,2) K(3,0)
  K(1,1)` — the five surviving rows are `K(8,2)`, `K(6,0)`, `K(0,0)`, `C2_P`,
  `C2_Q`, and they are independent.
* E1: `K(13,4) K(11,3) K(9,3) K(9,1) K(7,2) K(7,1) K(5,2) K(5,1) K(3,1)
  K(1,1)`.

### STEP 1b — Groebner basis of the E0 ideal over GF(2)

`sympy.groebner(..., order='grevlex', modulus=2)`, timeout 600 s.
Outcome: **COMPLETED** in < 0.01 s (not TIMEOUT). 7 basis elements:

```
a_1_0 + a_4_0
b_0_1 + b_5_0
a_4_0*b_5_0 + 1
a_2_1 + a_4_0**2*b_6_1
a_2_1*b_5_0 + a_4_0*b_6_1
a_2_1*b_7_2 + a_4_0*b_8_3
b_5_0*b_8_3 + b_6_1*b_7_2
```

Controls (in `verify_lift.py`): every generator of the original system reduces
to `0` modulo this basis, and the base point satisfies every basis element.

Dimension. 2 of the 9 variables carry a pure-power leading term, so the
quotient is not finite-dimensional. By the maximal-independent-set criterion
(`dim V(I) = max |U|` with `LT(I) ∩ k[U] = 0`), the **Krull dimension of the E0
ideal over the algebraic closure of `F_2` is 4**, with `{a_2_1, a_4_0, a_6_2,
b_8_3}` one maximal independent set. (`a_6_2` occurs in no leading monomial;
it occurs in no basis element at all.)

Exhaustive count over `F_2` itself: the E0 system has **8** `F_2`-rational
points, the base point among them. All 8 have `rank(J mod 2) = 5`, nullity 4.

## 4. STEP 2 — the integral system at the base point

Same supports E0, same equations, now over `Z`, with the target
`P_x Q_y - P_y Q_x = 1` in `Z[x,y]`. Base point = the `F_2` coefficients
lifted as the integers 0/1.

* number of unknowns `N = 9`
* number of equations `M = 15`
* all residuals at the base point are even (verified above): **yes**
* `rank(J mod 2) = 5`
* **corank in the unknowns `= N - rank = 4`**
* a square minor of size `N = 9` that is odd: **does not exist** — the rank mod
  2 is 5 < 9, so every 9×9 minor is even. The base point is therefore **not a
  smooth mod-2 point** of the integral system in the full-unknown-rank sense.
* equations whose gradient vanishes identically mod 2 at the base point: the
  ten listed in §3 (`K(13,4) K(12,3) K(11,2) K(10,1) K(9,3) K(9,0) K(7,1)
  K(5,2) K(3,0) K(1,1)`).

`J mod 2` on E0, rows in the order
`K(13,4) K(12,3) K(11,2) K(10,1) K(9,3) K(9,0) K(8,2) K(7,1) K(6,0) K(5,2)
K(3,0) K(1,1) K(0,0) C2_P C2_Q`, columns in the order
`a_1_0 a_2_1 a_4_0 a_6_2 b_0_1 b_5_0 b_6_1 b_7_2 b_8_3`:

```
K(8,2) : 1 1 0 0 0 0 0 1 1
K(6,0) : 1 1 0 0 0 1 1 0 0
K(0,0) : 1 0 0 0 1 0 0 0 0
C2_P   : 1 0 1 0 0 0 0 0 0
C2_Q   : 0 0 0 0 1 1 0 0 0
```

(all other ten rows are zero).

## 5. Derivation of the Hensel step actually used

Let `r : Z^N -> Z^M` be the residual map of the system (K)+(C2); each component
is a polynomial of total degree at most 2 in the unknowns. Let `J = Dr(x_0)`,
the integer Jacobian at the base point.

Since `r` is quadratic, Taylor's formula is exact with no remainder beyond
second order: for any `h`,

```
r(x + h) = r(x) + Dr(x) h + B(h, h)
```

with `B` the (integer) quadratic form given by the second-order terms.

Suppose `x_k` satisfies `r(x_k) ≡ 0 (mod 2^k)`, `k >= 1`, and look for the next
lift in the form `x_{k+1} = x_k + 2^k d`, `d ∈ Z^N`. Then

```
r(x_k + 2^k d) = r(x_k) + 2^k Dr(x_k) d + 2^{2k} B(d, d).
```

For `k >= 1` we have `2k >= k + 1`, so the last term vanishes mod `2^{k+1}`.
Write `r(x_k) = 2^k s_k` with `s_k ∈ Z^M`. Then

```
r(x_k + 2^k d) ≡ 2^k ( s_k + Dr(x_k) d )   (mod 2^{k+1}),
```

so `r(x_{k+1}) ≡ 0 (mod 2^{k+1})` holds **iff**

```
Dr(x_k) d ≡ -s_k   (mod 2),
```

and since `x_k ≡ x_0 (mod 2)` we have `Dr(x_k) ≡ Dr(x_0) = J (mod 2)`. Over
`F_2`, `-s_k = s_k`. The step at every level is therefore the same `F_2` linear
system

```
(J mod 2) · d = (s_k mod 2)      over F_2,
```

with the same matrix at every level and only the right-hand side changing.
It is solvable iff `s_k mod 2` lies in the column space of `J mod 2`, i.e. iff
`rank(J mod 2) = rank([J | s_k] mod 2)`; when solvable, the solution set is a
coset of `ker(J mod 2)`, of dimension `N - rank(J mod 2)` over `F_2`. Existence
of a lift of `x_k` to level `2^{k+1}` is exactly this solvability — the
condition is necessary as well as sufficient, because the displayed congruence
is an equality of the two sides, not a bound.

## 6. STEP 2 (continued) — the mod-4 step

At level `k = 1`: `r(x_0) = 2 s_1` with

```
s_1 mod 2 = 1 on  K(13,4) K(12,3) K(11,2) K(10,1) K(9,3) K(7,1) K(5,2)
                  K(1,1) C2_P
          = 0 on  K(9,0) K(8,2) K(6,0) K(3,0) K(0,0) C2_Q
```

(the entries with integer residual `≡ 2 mod 4` give 1, those `≡ 0 mod 4` give
0.)

Linear algebra over `F_2`:

* `rank(J mod 2) = 5`
* `rank([J | s_1] mod 2) = 6`

The augmented rank exceeds the rank, so `J d = s_1` has **no** solution over
`F_2`. Concretely, `s_1` is 1 in row `K(13,4)` while that row of `J mod 2` is
identically zero (and likewise for `K(12,3)`, `K(11,2)`, `K(10,1)`, `K(9,3)`,
`K(7,1)`, `K(5,2)`, `K(1,1)`), so the congruence reads `0 ≡ 1 (mod 2)`.

**mod 4: DOES-NOT-EXIST.**

Independent control (`verify_lift.py`): exhaustive search over all `4^9 =
262144` points of `(Z/4)^9`. The system has 16 solutions mod 4 in total, and
**0** of them are congruent to the base point mod 2. This agrees with the
linear-algebra verdict.

Distribution of those 16 mod-4 solutions over the 8 `F_2`-points of the system
(all 8 have `rank(J mod 2) = 5`):

| `F_2` point (a_1_0 a_2_1 a_4_0 a_6_2 b_0_1 b_5_0 b_6_1 b_7_2 b_8_3) | mod-4 lifts |
|---|---|
| 1 0 1 0 1 1 0 0 0 | 16 |
| 1 0 1 0 1 1 0 1 0 | 0 |
| 1 0 1 1 1 1 0 0 0 | 0 |
| 1 0 1 1 1 1 0 1 0 | 0 |
| 1 1 1 0 1 1 1 0 0 | 0 |
| 1 1 1 0 1 1 1 1 1 | 0 |
| 1 1 1 1 1 1 1 0 0 | 0 |
| 1 1 1 1 1 1 1 1 1 | 0 (**the base point**) |

## 7. STEP 3 — mod 8 and mod 16

STEP 3 is conditional on a mod-4 lift of the base point existing. It does not
exist, so the mod-8 and mod-16 levels were not entered: **not applicable**, no
level beyond 4 was attempted. (The cap in the task was 16.)

## 8. Summary table

| quantity | value |
|---|---|
| witness control, E0 / E1 | PASSED / PASSED |
| E0: unknowns / equations | 9 / 15 |
| E0: rank(J mod 2) / nullity | 5 / 4 |
| E1: unknowns / equations | 22 / 34 |
| E1: rank(J mod 2) / nullity | 14 / 8 |
| E0 Groebner over GF(2) | COMPLETED (<0.01 s), 7 elements, Krull dim 4 |
| E0 `F_2`-rational points | 8 |
| smooth mod-2 point of the integral system (odd `N x N` minor) | NO, corank 4 |
| mod-4 lift of the base point | DOES-NOT-EXIST (rank 5 vs augmented rank 6; exhaustive `(Z/4)^9` search confirms 0) |
| mod-8, mod-16 | not attempted (conditional on mod 4) |
