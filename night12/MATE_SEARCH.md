# night12 -- the MATE SEARCH (v0)

Measurements only. Nothing in this file is a conclusion.

Ring labels used throughout:

- **ring: Q** -- exact arithmetic in `Q[x,y]` (python `int` / `Fraction`).
- **ring: F_p** -- the finite field `F_p`, `p = 999983` or `p = 1000003`.

---

## 1. The construction being measured

For a **fixed** `P` in `Q[x,y]`, the Keller equation

```
P_x Q_y - P_y Q_x = 1
```

is **linear** in the coefficients of `Q`. Writing `P = sum_b c_b x^b1 y^b2` and
`Q = sum_a q_a x^a1 y^a2`, the bracket expands term by term into a single
monomial per pair:

```
c_b * (b1*a2 - b2*a1) * x^(b1+a1-1) * y^(b2+a2-1)
```

so the coefficient matrix `A` (rows indexed by monomials of the bracket,
columns by the unknowns `q_a`) has at most `|supp P|` nonzeros per column, and
the system is `A q = e` with `e` the indicator of the monomial `(0,0)`.
The mate question for a fixed `P` and a fixed `Q`-support is therefore exactly
the linear-algebra question **is `e` in the column space of `A`**, i.e.
`rank(A) = rank([A|e])`.

Implemented in `matekit.py` (`build_system`, `consistency_mod_p`,
`exact_solve`, `bracket`).

### Structural row that the construction exposes

The constant row of the bracket receives contributions only from
`b + a = (1,1)` with `b1*a2 - b2*a1 != 0`. The pairs
`b=(1,1), a=(0,0)` and `b=(0,0), a=(1,1)` both carry factor `0`, so the
constant row reads exactly

```
P[1,0] * Q[0,1] - P[0,1] * Q[1,0] = 1 .
```

Two things follow mechanically and are recorded as such:
(a) any `P` with no linear term makes this row identically `0 = 1`;
(b) the monomials `(1,0)` and `(0,1)` must be present in the `Q`-support or
the system is inconsistent for support reasons rather than arithmetic ones.
Both are exercised by control C0 below. (The same row was recorded in the
night11 lane as the reason a sublattice support forced `E_K >= 1`.)

---

## 2. The Q-support (bounded, and the bound is recorded)

For each `P` of degree `d`:

```
S_full = { a in Z^2_{>=0} : |a| <= floor(3d/2) }  intersect  (3/2) * NP(P)
NP(P)  = conv( supp(P)  u  {(0,0), (1,0), (0,1)} )
```

The `3/2` scaling is done exactly on the doubled lattice: `a` lies in
`(3/2) NP(P)` iff `2a` lies in `conv(3V)` for `V` the vertex set of `NP(P)`,
so the support is computed with integer cross products only, no floating
point. The three BASE points are forced into `NP(P)` for the reason in
section 1(b) -- without them control C1 (`P = x`, `Q = y`) could not be found,
since `NP(x)` is a single point.

`|S_full|` is recorded per `P` as `n_full_support`. Two caps are applied and
both are recorded:

- `cap_full = 4000` -- the design cap.
- `cap_work = 1200` -- a further purely computational cap, since the dense
  modular elimination is `O(n^3)` and the sweep runs on 4 cores.

When the count exceeds the cap the support is **thinned to the self-similar
sublattice** `k*Z^2` (union the BASE points) for the least `k >= 2` that fits;
`thin_k` and the resulting `n_unknowns` are both recorded per `P`. Where
`thin_k > 1` the search is a search on that thinned support and on no larger
one; the recorded verdict is a verdict about that support.

---

## 3. The decision procedure

1. Build `A` and `e` over `Z` (ring: Q) -- sparse, `<= |supp P| * n` nonzeros.
2. Compress the rows by an independent random `F_p`-linear map onto
   `n + 16` rows (the row count reaches ~`10^4`; a random compression
   preserves both `rank(A)` and `rank([A|e])` with probability
   `1 - O(n/p)`). Different random maps are drawn for each prime.
3. Row-reduce `[A|e]` over **F_p** and read off `rank(A)`, `rank([A|e])`, and
   the pivot columns. `consistent` iff the last column is not a pivot.
4. Run step 2-3 independently at `p = 999983` and `p = 1000003`.
   `dual_prime_consistent` requires both.
5. **Only** on dual-prime consistency: exact rational solve (ring: Q) by
   Gaussian elimination over `Fraction`, restricted to the mod-`p` pivot
   columns when `n > 500` (the modular pivot choice is a heuristic for
   *finding* a solution and is never part of the certificate).
6. Every solution `Q` is then certified by **direct exact bracket expansion**
   over `Q`: `P_x Q_y - P_y Q_x` is expanded in `Q[x,y]` and compared to `1`.
   Only `exact_status = verified_bracket_eq_1` counts as a mate.

A modular consistency verdict is a statement about `F_p`; only step 6 is a
statement about `Q`.

---

## 4. The degree fact being tested against

Jung--van der Kulk: the two degrees of any plane polynomial automorphism are
divisibility-ordered. Per exactly verified pair `(P,Q)` this lane records
`deg P`, `deg Q`, and the boolean `div_ordered = (deg P | deg Q) or
(deg Q | deg P)`. **The recorded quantity of interest** is the count of
main-arm (`deg P in {84, 96, 108, 126}`) pairs that are exactly verified over
`Q` and whose degree pair is **not** divisibility-ordered. Any such pair is
written to `night12/HIT_<hash>/` under the halt-and-commit protocol.

---

## 5. Files

| file | contents |
| --- | --- |
| `matekit.py` | kernel: polynomial arithmetic, Newton-polygon support, sparse system build, dual-prime consistency, exact solve, bracket certificate |
| `ansatz.py` | the P families and the seed-20260831 generator |
| `sweep.py` | the driver (4-way multiprocessing) |
| `controls.py` | hard-gate controls C0/C1/C2/C4 |
| `report.py` | the tallies reproduced in section 7 |
| `controls_log.txt`, `controls.json` | control outcomes |
| `mate_search.csv`, `mate_search.json` | one row per `P` |
| `VERIFIED/` | per-pair JSON for every exactly verified mate |
| `HIT_<hash>/` | halt-and-commit directory, one per main-arm non-divisibility-ordered pair |

CSV columns: `hash, arm, tag, deg, n_supp_P, has_linear_term,
n_full_support, thin_k, n_unknowns, deg_Q_max, n_rows_nonzero,
rank_A_p999983, rank_Ae_p999983, nullity_p999983, consistent_p999983,
rank_A_p1000003, rank_Ae_p1000003, nullity_p1000003, consistent_p1000003,
dual_prime_consistent, exact_status, deg_Q, div_ordered, secs`.

---

## 6. Controls (hard gate) -- all four as designed

Reproduce with `python3 controls.py`; raw in `controls_log.txt` / `controls.json`.

| control | P | unknowns | dual-prime verdict | exact |
| --- | --- | --- | --- | --- |
| **C1** | `x` | 3 | consistent | `Q = y`, `verified_bracket_eq_1`, degree pair `(1,1)` |
| **C2** | `x + y^2` | 6 | consistent | `Q = y`, `verified_bracket_eq_1`, degree pair `(2,1)` |
| **C4** | random dense deg-5 `P`, 20 monomials, seed 20260831 | 36 | **inconsistent**; `rank(A)/rank([A|e]) = 34/35` at both `p = 999983` and `p = 1000003` | not attempted |
| **C0** | `x^2 + y^3 + xy` (no linear term) | -- | **inconsistent** | not attempted |

C0 was added during the run and it caught a real defect in the kernel: the
first version assembled the augmented column only from the *nonzero* rows of
`A`, so when `P` has no linear term -- exactly the case where the constant row
of `A` is identically zero -- the equation `0 = 1` was dropped and the system
was reported consistent. `consistency_mod_p` and `exact_solve` now force the
monomial `(0,0)` into the row set unconditionally. All the numbers in this
file are from the fixed kernel; the sweep confirms the fix at scale
(22 of the 174 `P` have no linear term, and **0** of those 22 are consistent).

C3 (the calibration arm) is section 7.3.

---

## 7. The sweep

`python3 sweep.py`, seed 20260831, 174 distinct `P` (>= the 150 asked for),
4 worker processes, 2124 s of summed per-`P` wall time.

### 7.1 P swept, and consistency tally by arm

| arm | deg P | dual-prime consistent / total |
| --- | --- | --- |
| calib | 4 | 3 / 14 |
| calib | 6 | 6 / 18 |
| calib | 9 | 3 / 14 |
| **main** | **84** | **0 / 32** |
| **main** | **96** | **0 / 32** |
| **main** | **108** | **0 / 32** |
| **main** | **126** | **0 / 32** |

By family:

| family | consistent / total |
| --- | --- |
| `A_rand_sparse_lin` (random sparse, linear term forced) | 0 / 44 |
| `B_rand_sparse_nolin` (random sparse, no linear term forced) | 0 / 22 |
| `C_struct_x` (`x` + structured monomial mixes) | 1 / 33 |
| `D_leadsq` (leading form `(H_{d/2})^2`, `H` random sparse) | 0 / 36 |
| `E_leadcube` (leading form `(H_{d/3})^3`, `H` random sparse) | 0 / 28 |
| `F_coord` (triangular compositions) | 11 / 11 |

Agreement between the two primes: **174 / 174**; zero disagreements between
`p = 999983` and `p = 1000003` on any `P`.

### 7.2 System sizes actually decided

| quantity | main arm (128 P) | calib arm (46 P) |
| --- | --- | --- |
| `n_full_support` min / median / max | 97 / 4859 / 15509 | (all <= cap) |
| `n_full_support > cap_full = 4000` | 78 of 128 | 0 of 46 |
| `thin_k` distribution | `1`: 28, `2`: 35, `3`: 54, `4`: 11 | `1`: 46 |
| `n_unknowns` min / median / max | 97 / 715 / 1200 | 6 / -- / <= 500 |
| nonzero rows min / median / max | 171 / 3342 / 8635 | -- |
| `deg Q` bound `floor(3 deg P/2)` | 126 .. 189 | 6 .. 13 |

Two recorded structural regularities:

- `rank([A|e])` never reached `n_unknowns + 1` on the main arm (0 of 128), i.e.
  the augmented matrix always had a nontrivial kernel even where the system was
  inconsistent.
- The corank `n_unknowns - rank(A)` over `F_999983` was `1` for 98 of the 174,
  `2` for 74, and `7` and `10` once each. Corank `>= 1` is forced whenever
  `supp(P)` sits inside the `Q`-support, because `[P, P] = 0` puts `P`'s own
  coefficient vector in the kernel of `A`; more generally `[P, f(P)] = 0` for
  any one-variable `f`, and the corank-2 cases are those where `P^2` also fits
  in the support.

### 7.3 C3 -- the calibration arm, exactly verified over Q

Every dual-prime-consistent case at `deg P in {4,6,9}` was solved exactly over
`Q` and then certified by direct bracket expansion. All 12 passed
(`exact_status = verified_bracket_eq_1`); there were no
`solve_did_not_verify` and no `inconsistent_exact` outcomes anywhere in the
sweep. Per-pair JSON in `VERIFIED/`.

| hash | family | P | Q | degree pair | divisibility-ordered |
| --- | --- | --- | --- | --- | --- |
| `eb6976b38508` | F_coord | `x + y^4` | `y` | (4,1) | True |
| `a4012387e160` | F_coord | `x + y^2 + 2x^2 y + x^4` | `y + x^2` | (4,2) | True |
| `fbf00970ade6` | F_coord | `y + x^2 + 2x y^2 + y^4` | `-(x + y^2)` | (4,2) | True |
| `40c3553b8128` | F_coord | `x + y^6` | `y` | (6,1) | True |
| `7d595c3bd034` | C_struct_x | `x + 2y + y^6` | `y` | (6,1) | True |
| `84d01285324b` | F_coord | `x + y^3 + 3x^2y^2 + 3x^4y + x^6` | `y + x^2` | (6,2) | True |
| `2253023eddc1` | F_coord | `y + x^3 + 3x^2y^2 + 3xy^4 + y^6` | `-(x + y^2)` | (6,2) | True |
| `6df7f7c0a35c` | F_coord | `x + y^2 + 2x^3y + x^6` | `y + x^3` | (6,3) | True |
| `241c5be4e3a9` | F_coord | `y + x^2 + 2xy^3 + y^6` | `-(x + y^3)` | (6,3) | True |
| `d9103ff114e1` | F_coord | `x + y^9` | `y` | (9,1) | True |
| `5bf4f9822cd4` | F_coord | `x + y^3 + 3x^3y^2 + 3x^6y + x^9` | `y + x^3` | (9,3) | True |
| `693586fd5f7e` | F_coord | `y + x^3 + 3x^2y^3 + 3xy^6 + y^9` | `-(x + y^3)` | (9,3) | True |

Degree pairs found: `(4,1) (4,2) (6,1) (6,2) (6,3) (9,1) (9,3)`.
Divisibility-ordered: **12 of 12**.

### 7.4 The quantity of interest

> Main-arm (`deg P in {84, 96, 108, 126}`) systems that are dual-prime
> consistent, exactly solvable over `Q`, bracket-certified, **and** whose
> degree pair `(deg P, deg Q)` is not divisibility-ordered:
>
> ## 0
>
> out of 128 main-arm `P` swept.

No `HIT_<hash>/` directory was created. The halt-and-commit protocol did not
fire.

The main-arm verdict is a verdict about the bounded `Q`-supports recorded in
7.2 (`n_full_support`, `thin_k`, `n_unknowns` per `P` in the CSV) and about
the two primes named; 78 of the 128 main-arm supports were thinned to a
sublattice `k*Z^2` with `k` in `{2,3,4}` before being decided.
