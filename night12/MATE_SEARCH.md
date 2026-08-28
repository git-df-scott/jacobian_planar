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
