# night10 — the ramified ladder over `O = Z[pi]`, `pi^2 = 2` (and `pi^3 = 2`)

Scope note. Measurements only. Every quantity is labelled with the ring it was
computed in. Nothing here says what any of it means.

Scripts (all in `night10/`): `system.py` (the map `r`), `ram.py` (the rings and
`F_2` linear algebra), `ladder.py` (the ladder engine), `controls.py` (STEP 0),
`toy_ladder.py` (R0 through the engine itself), `run.py` (STEP 1 + STEP 2),
`detail.py` (per-level census + STEP 3), `o3_probe.py` (bounded STEP-3
follow-up).
Data: `ramified_O2.json`, `ramified_detail.json`, `ramified_O3_probe.json`.

## 0. The map `r`, rebuilt in lane

Coordinate order, as in `night8/all_eight.json`:

```
( a_1_0 , a_2_1 , a_4_0 , a_6_2 , b_0_1 , b_5_0 , b_6_1 , b_7_2 , b_8_3 )
```

```
P = a_1_0 x + a_2_1 x^2 y + a_4_0 x^4 + a_6_2 x^6 y^2
Q = b_0_1 y + b_5_0 x^5 + b_6_1 x^6 y + b_7_2 x^7 y^2 + b_8_3 x^8 y^3
```

`r : Z^9 -> Z^15` — every coefficient of `P_x Q_y - P_y Q_x - 1` over `Z`
(13 rows), then `C2_P = P(0,1)-P(1,0)` and `C2_Q = Q(0,1)-Q(1,0)`.
Base ring of the system: **Z**.

| row | expression (over `Z`) | row | expression (over `Z`) |
|---|---|---|---|
| `K(13,4)` | `2 a_6_2 b_8_3` | `K(7,1)` | `2 a_1_0 b_7_2 - 4 a_2_1 b_6_1` |
| `K(12,3)` | `-2 a_6_2 b_7_2` | `K(6,0)` | `a_1_0 b_6_1 - 5 a_2_1 b_5_0` |
| `K(11,2)` | `12 a_4_0 b_8_3 - 6 a_6_2 b_6_1` | `K(5,2)` | `6 a_6_2 b_0_1` |
| `K(10,1)` | `8 a_4_0 b_7_2 - 10 a_6_2 b_5_0` | `K(3,0)` | `4 a_4_0 b_0_1` |
| `K(9,3)` | `-2 a_2_1 b_8_3` | `K(1,1)` | `2 a_2_1 b_0_1` |
| `K(9,0)` | `4 a_4_0 b_6_1` | `K(0,0)` | `a_1_0 b_0_1 - 1` |
| `K(8,2)` | `3 a_1_0 b_8_3 - 3 a_2_1 b_7_2` | `C2_P` | `-a_1_0 - a_4_0` |
| | | `C2_Q` | `b_0_1 - b_5_0` |

Ten rows have identically-vanishing gradient mod 2 (`K(13,4)`, `K(12,3)`,
`K(11,2)`, `K(10,1)`, `K(9,3)`, `K(9,0)`, `K(7,1)`, `K(5,2)`, `K(3,0)`,
`K(1,1)`) — the same ten `night8/LADDER_8.md` lists, reproduced here from an
independent construction.

`r` is quadratic: `r(v) = c + L v + Q2(v)`, with `Q2` the vector of pure
quadratic forms. Two derived objects, both extracted programmatically from the
coefficient dictionaries in `system.py`:

* `Dr(x)` — the Jacobian, `Dr(x)_{k,i} = L_{k,i} + d/dx_i Q2_k(x)`.
* `Bpol(d,d') := Q2(d+d') - Q2(d) - Q2(d')` — the **integral** polarization
  (equal to `2 B_sym(d,d')`; this is the cross term that actually appears in
  the expansion, and it stays in `Z`, unlike `B_sym`).

### Step calculus

For a scalar `e` and vectors `x, d`, exactly (no error term):

```
r(x + e d) = r(x) + e Dr(x) d + e^2 Q2(d)                     (*)
```

Multi-level version, used by the ladder. With `x = x_0 + sum_{k>=1} pi^k d_k`
and `d_k` integer vectors, `Q2` quadratic gives
`Q2(sum u_k) = sum_k Q2(u_k) + sum_{i<j} Bpol(u_i,u_j)`, so

```
r(x_0 + sum_{k>=1} pi^k d_k)
   = r(x_0) + sum_{m>=1} pi^m * T_m ,

   T_m = Dr(x_0) d_m
       + [m even] Q2(d_{m/2})
       + sum_{i<j, i+j=m} Bpol(d_i, d_j)                      (**)
```

`(**)` is the general recursion. Note it is stated over `Z` before any
reduction — the `pi`-adic bookkeeping (`2 = pi^e`) then happens inside the
ring, which is why the engine works verbatim for `pi^2 = 2` and `pi^3 = 2`.

### CONTROLS (STEP 0), `night10/controls.py` — all passed

* **C1** `(*)` verified on 200 random integer `(x, d, e)` against direct
  expansion of `r`. Base ring `Z`.
* **C2** `Bpol` extracted from the coefficient dictionaries equals the direct
  `Q2(d+d') - Q2(d) - Q2(d')` on 200 random integer pairs. Base ring `Z`.
* **C3** ring control for `O2 = Z[pi]/(pi^2-2)` and `O3 = Z[pi]/(pi^3-2)`:
  associativity, distributivity, `pi^e = 2`, `w(uv) = w(u)+w(v)`, and
  `div_pi(mul_pi(u)) = u`, on 300 random elements each.
* **C4** `(**)` assembled term-by-term equals `r` evaluated by exact
  arithmetic in `O2` (and in `O3`) on 60 random `(x_0, d_1..d_4)`.

### Ring arithmetic

`O_e = Z[pi]/(pi^e - 2)`, elements are integer tuples `(c_0,...,c_{e-1})`
meaning `sum c_k pi^k`. For `e = 2` this is the pair `(a,b) = a + b pi` with
`(a,b)(c,d) = (ac+2bd, ad+bc)` as prescribed. Integer valuation `w`,
`w(pi)=1`, `w(2)=e`: for `u = sum c_k pi^k`, `w(u) = min_k (k + e*v_2(c_k))`
(the `k + e v_2(c_k)` are pairwise distinct mod `e`, so the minimum is exact).
Residue field `O/(pi) = F_2`; digits `{0,1}` give a unique `pi`-adic expansion,
so taking every `d_k` in `{0,1}^9` is a canonical and complete parametrisation
— no two distinct digit strings give the same point, hence no duplicate states
to prune.

### The ladder step, and why `J` is constant along it

Truncate `x_m = x_0 + sum_{k=1}^{m-1} pi^k d_k` with the invariant
`w(r(x_m)_j) >= m` for every component `j`. Let
`rho = residue_{F_2}( r(x_m) / pi^m )`. Adding `pi^m d_m` changes `r` by
`pi^m Dr(x_m) d_m + pi^{2m} Q2(d_m)` by `(*)`, and `2m > m`, so the level-`m`
condition is

```
   Dr(x_0) d_m  ==  rho   (mod 2)
```

— `Dr(x_m) = Dr(x_0) mod pi` because `x_m = x_0 mod pi`. So the matrix is the
**fixed** `J2 := Dr(x_0) mod 2`. The level is passable iff `rho` lies in the
`F_2`-column space of `J2`; the solution set is then a coset of
`ker(J2 mod 2)`, of size `2^nullity = 16` at every one of the 8 points.

Specialising `(**)` at the first two levels over `O2` (`2 = pi^2`, and
`r(x_0) = 2 s = pi^2 s`):

* level 1: `w(r(x_0)) >= 2`, so `rho = 0` and the condition is
  `J2 d_1 = 0`, i.e. `d_1 in ker(J2)` — **16** vectors.
* level 2: `r(x_0 + pi d_1) = pi^2 (s + Q2(d_1)) + pi^3 t` where
  `J d_1 = 2 t`, so the condition is
  **`J2 d_2 = (s + Q2(d_1)) mod 2`**, passable iff
  `(s + B(d_1,d_1)) mod 2` lies in `Im(J2)`. This is STEP 1.

Over `O3` (`2 = pi^3`, `r(x_0) = pi^3 s`) the quadratic term lands one level
earlier relative to the constant:

* level 1: `rho = 0`, `d_1 in ker(J2)` — 16 vectors.
* level 2: `r(x_0 + pi d_1) = pi^2 Q2(d_1) + pi^3 (s + t)`, so the condition
  is **`J2 d_2 = Q2(d_1) mod 2`** — the vector `s` does **not** appear.

Both closed forms are cross-checked inside `run.py` / `detail.py` against the
`rho` produced by exact `O`-arithmetic, at every point and every `d_1`
(assertions; all passed).

### Independent check at every accepted level

Whenever a `d_m` is accepted, the truncated point is substituted back into `r`
and evaluated by exact arithmetic in `O_e`, and every one of the 15 components
is asserted to have `w > m`. No level in any run below was accepted without
this check.

## R0 — the toy

`f(x) = x^2 - 2`, base point `x = 0 mod 2`.

* over `Z`: squares mod 4 are `{0,1}`; `2` is not among them. The unramified
  step `x = 0 + 2 d` gives `f = 4d^2 - 2`, and `4d^2 - 2 = 0 (mod 4)` has
  **no** solution. Unramified step **FAILS**.
* over `O2`: `x = pi d_1` gives `f = 2 d_1^2 - 2`; `d_1 = 0` leaves `w = 2`,
  `d_1 = 1` gives `f = 0` exactly. Ramified step **SUCCEEDS with `d_1 = 1`**.

Run through the ladder engine unchanged (`toy_ladder.py`, `n = 1`,
`J2 = [0]`, rank 0, kernel `{0,1}`): level 1 admits both `d_1`; at level 2 the
branch `d_1 = 0` has `rho = [1]` with `rank J2 = 0`, `rank [J2|rho] = 1` and
**dies**, while `d_1 = 1` climbs to the level-12 ceiling with residual
identically `0`. Matches the required outcome; no hard exit.

## STEP 1 — first ramified obstruction test over `O2`, at the 8 census points

For each point: `r(x_0)` is even componentwise (checked), `s = r(x_0)/2`,
`J2 = Dr(x_0) mod 2` has **rank 5, nullity 4** at all 8 (reproducing night8),
so `ker(J2)` has 16 elements. Test: is `(s + B(d,d)) mod 2 in Im(J2)`?

| # | point | `s` (over `Z`, nonzero rows) | STEP 1 pass count |
|---|---|---|---|
| 1 | `101011000` | `K(3,0)=2`, `C2_P=-1` | **16 / 16** |
| 2 | `101011010` | `K(10,1)=4`, `K(7,1)=1`, `K(3,0)=2`, `C2_P=-1` | **0 / 16** |
| 3 | `101111000` | `K(10,1)=-5`, `K(5,2)=3`, `K(3,0)=2`, `C2_P=-1` | **0 / 16** |
| 4 | `101111010` | `K(12,3)=-1`, `K(10,1)=-1`, `K(7,1)=1`, `K(5,2)=3`, `K(3,0)=2`, `C2_P=-1` | **0 / 16** |
| 5 | `111011100` | `K(9,0)=2`, `K(7,1)=-2`, `K(6,0)=-2`, `K(3,0)=2`, `K(1,1)=1`, `C2_P=-1` | **0 / 16** |
| 6 | `111011111` | `K(11,2)=6`, `K(10,1)=4`, `K(9,3)=-1`, `K(9,0)=2`, `K(7,1)=-1`, `K(6,0)=-2`, `K(3,0)=2`, `K(1,1)=1`, `C2_P=-1` | **0 / 16** |
| 7 | `111111100` | `K(11,2)=-3`, `K(10,1)=-5`, `K(9,0)=2`, `K(7,1)=-2`, `K(6,0)=-2`, `K(5,2)=3`, `K(3,0)=2`, `K(1,1)=1`, `C2_P=-1` | **0 / 16** |
| 8 | `111111111` | `K(13,4)=1`, `K(12,3)=-1`, `K(11,2)=3`, `K(10,1)=-1`, `K(9,3)=-1`, `K(9,0)=2`, `K(7,1)=-1`, `K(6,0)=-2`, `K(5,2)=3`, `K(3,0)=2`, `K(1,1)=1`, `C2_P=-1` | **0 / 16** |

Point 1 — all sixteen `d_1 in ker(J2)` pass:

```
000000000  000100000  101011000  101111000  010000100  010100100  111011100  111111100
000000010  000100010  101011010  101111010  010000110  010100110  111011110  111111110
```

(these are the 16 elements of `ker(J2)` itself; at this point the pass set is
the whole kernel).

Points 2–8 — the pass set is empty. For every one of the 16 `d`, the failure
is `rank(J2) = 5` vs `rank([J2 | rho]) = 6`, where `rho = (s + Q2(d)) mod 2`.
Representative failing `rho` rows at `d = 0`:

| # | `rho` rows at `d = 0` |
|---|---|
| 2 | `K(7,1)`, `C2_P` |
| 3 | `K(10,1)`, `K(5,2)`, `C2_P` |
| 4 | `K(12,3)`, `K(10,1)`, `K(7,1)`, `K(5,2)`, `C2_P` |
| 5 | `K(1,1)`, `C2_P` |
| 6 | `K(9,3)`, `K(7,1)`, `K(1,1)`, `C2_P` |
| 7 | `K(11,2)`, `K(10,1)`, `K(5,2)`, `K(1,1)`, `C2_P` |
| 8 | `K(13,4)`, `K(12,3)`, `K(11,2)`, `K(10,1)`, `K(9,3)`, `K(7,1)`, `K(5,2)`, `K(1,1)`, `C2_P` |

Cross-reference. At `d_1 = 0` the level-2 condition reads `J2 d_2 = s mod 2`,
which is exactly the unramified mod-2 -> mod-4 step of `night8/LADDER_8.md`.
The `d_1 = 0` column above therefore reproduces night8's mod-4 verdict
(point 1 passes, points 2–8 fail) from an independently rebuilt system; the
`d_1 = 0` row of point 8 reproduces night8's eight obstruction rows for the
base point exactly. The ramified freedom is the extra term `Q2(d_1)` for the
other 15 kernel vectors, and at points 2–8 none of the 15 moves `rho` into
`Im(J2)`.

## STEP 2 — the `pi`-ladder over `O2`, ceiling `w`-level 12

Full breadth-first census, all digit choices carried, `d_k in {0,1}^9`.

| # | point | branches by level (`in -> out`) | outcome |
|---|---|---|---|
| 1 | `101011000` | L1 `1->16`, L2 `16->256`, L3 `256->512` (224 died), L4 `512->0` (512 died) | all branches dead at **w-level 4** |
| 2–8 | (the other seven) | L1 `1->16`, L2 `16->0` (16 died) | all branches dead at **w-level 2** |

**No branch reached the level-12 ceiling over `O2` at any of the 8 points.**
Every death, at every level and every point, has `rank(J2) = 5` and
`rank([J2 | rho]) = 6`.

Representative deaths (full trees in `ramified_detail.json`,
`ramified_O2.json`):

* point 1, first death, **w-level 3**: `d_1 = 000100000`, `d_2 = 001000000`;
  residual valuation before the step `w = 3`; failed condition
  `J2 d_3 = rho` with `rho` supported on `K(10,1)`, `K(5,2)`;
  `rank 5` vs `rank_aug 6`.
* point 1, terminal deaths, **w-level 4** (all 512 surviving branches):
  e.g. `d_1 = 000000000`, `d_2 = 001000000`, `d_3 = 000000000`;
  `w = 4` before the step; `rho` supported on `K(3,0)`, `C2_P`;
  `rank 5` vs `rank_aug 6`.
* points 2–8, **w-level 2**: the STEP 1 table above is the death record — all
  16 branches fail the level-2 condition, `rank 5` vs `rank_aug 6`.

For scale: `w`-level 12 over `O2` is `pi^13`, i.e. comparable with `Z/2^6`.
Point 1 reaches `w = 4` (comparable with `Z/4`); the unramified ladder of
night8 for the same point reached `Z/4` and died into `Z/8`.

## STEP 3 — first obstruction test over the ramified cubic `O3`, `pi^3 = 2`

Step calculus as derived above: level 1 gives `d_1 in ker(J2)` (16 vectors),
and the level-2 condition is `J2 d_2 = Q2(d_1) mod 2`, with `s` absent.
Checked against exact `O3` arithmetic at all 8 points and all 16 `d_1`.

| # | point | `w(r(x_0))` over `O3` | STEP 3 pass count |
|---|---|---|---|
| 1 | `101011000` | 3 | **16 / 16** |
| 2 | `101011010` | 3 | **16 / 16** |
| 3 | `101111000` | 3 | **16 / 16** |
| 4 | `101111010` | 3 | **16 / 16** |
| 5 | `111011100` | 3 | **16 / 16** |
| 6 | `111011111` | 3 | **16 / 16** |
| 7 | `111111100` | 3 | **16 / 16** |
| 8 | `111111111` | 3 | **16 / 16** |

All 16 pass at every point. The level-2 test over `O3` does not see `s` at
all, which is what the derivation predicts.

### Bounded follow-up over `O3` (`o3_probe.py`)

Since everything passed and the test was cheap, the `O3` ladder was run
depth-first to the same level-12 ceiling under a 300 000-node budget. **The
budget was not reached at any point — every search terminated by exhausting
its tree, so these counts are complete, not sampled.**

| # | point | nodes | deaths | death `w`-levels | reached level 12 |
|---|---|---|---|---|---|
| 1 | `101011000` | 28 945 | 27 136 | 4, 5, 6 | no |
| 2 | `101011010` | 273 | 256 | 3 | no |
| 3 | `101111000` | 273 | 256 | 3 | no |
| 4 | `101111010` | 273 | 256 | 3 | no |
| 5 | `111011100` | 273 | 256 | 3 | no |
| 6 | `111011111` | 273 | 256 | 3 | no |
| 7 | `111111100` | 273 | 256 | 3 | no |
| 8 | `111111111` | 273 | 256 | 3 | no |

Representative deaths over `O3`:

* point 1, **w-level 4**: `d_1 = 000100000`, `d_2 = 0`, `d_3 = 001000000`;
  `rho` rows `K(10,1)`, `K(5,2)`; `rank 5` vs `rank_aug 6`.
* points 2–8, **w-level 3** with `d_1 = d_2 = 0`: `rho` rows are exactly the
  point's night8 mod-4 obstruction rows plus `C2_P` (row lists in the STEP 1
  failure table above); `rank 5` vs `rank_aug 6`. With `d_1 = d_2 = 0` the
  `O3` level-3 condition coincides with the unramified mod-2 -> mod-4 step,
  so this row agrees with night8.

**No branch reached the level-12 ceiling over `O3` either.** Every death
recorded in this file, in both rings, has the same shape: `rank(J mod 2) = 5`,
augmented rank 6.
