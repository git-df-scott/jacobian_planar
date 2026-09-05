# night9 — the prime survey

Scope note. This file records measurements only. It states what was computed
and what the computations returned. It contains no assessment of what any of
these numbers mean. Every result is labelled with its characteristic.

## 0. The system

Over `F_p`, for a support pair `(S_P, S_Q)` of exponent vectors in `Z_{>=0}^2`,

```
P(x,y) = sum_{m in S_P} a_m x^{m0} y^{m1}
Q(x,y) = sum_{n in S_Q} b_n x^{n0} y^{n1}
```

with the coefficients `a_m, b_n` as unknowns. The equations are

* **(K)** every coefficient of `P_x Q_y - P_y Q_x - 1` is zero;
* **(C)** `P(0,1) = P(1,0)` and `Q(0,1) = Q(1,0)` — the two collision points
  are held fixed (Mondello-style) and the unknowns are the coefficients, with
  the convention `0^0 = 1`.

Because

```
P_x Q_y - P_y Q_x = sum_{m,n} (m0 n1 - m1 n0) a_m b_n x^{m0+n0-1} y^{m1+n1-1},
```

the (K) equations are **bilinear**: linear in `a` for fixed `b` and linear in
`b` for fixed `a`. (C) splits as `C_P` (only `a`) and `C_Q` (only `b`). The
equation index set used is `{e : some pair has nonzero integer bracket}` union
`{(0,0)}`; `(0,0)` is always present because of the `-1`.

Files: `keller_solver.py` (system, solver, verification, Hensel), `tear.py`
(tear data), `survey.py` (the sweep), `census.py` (complete solution lists),
`control_p2.py` (the positive control), `summarize.py` (tallies).

## 1. Positive control at p = 2 (run first, hard exit on failure) — PASSED

Exact Mondello support
`S_P = {(1,0),(2,1),(4,0),(6,2)}`, `S_Q = {(0,1),(5,0),(6,1),(7,2),(8,3)}`,
9 unknowns.

| method | result |
|---|---|
| (A) naive exhaustive over all `2^9 = 512` points of `F_2^9`, each point tested by **direct substitution** (`P_x Q_y - P_y Q_x - 1 = 0` in `F_2[x,y]` and both collision equalities) | **8** solutions |
| (B) the bilinear exhaustive solver used throughout this lane | **8** solutions |
| `night8/mondello_lift.json` (independent lane) | 8 |

All three agree. The base point `(1,1,1,1;1,1,1,1,1)` is among the 8. The
per-point Hensel step to `Z/4` reproduces night8's table exactly: of the 8
`F_2` points, exactly one lifts —

```
a = (1,0,1,0), b = (1,1,0,0,0)   i.e.  P = x + x^4,  Q = y + x^5
```

— and that one does not lift further to `Z/8`; the base point does not lift to
`Z/4`. Output: `night9/control_p2.json`.

## 2. Support families

**F1 — Frobenius ansatz.** The `p = 2` object reads, in terms of `p`,
`S_P = {(1,0),(p,1),(2p,0),(2p+2,2)}`,
`S_Q = {(0,1),(2p+1,0),(2p+2,1),(2p+3,2),(2p+4,3)}`. The family keeps that
shape and varies

```
S_P = {(1,0), (A,1), (2p,0), (2p+C,2)}      A in {2, p, p+1, 2p-1}, C in {0,2,3}
S_Q = {(0,1), (D,0), (D+1,1), (D+2,2), (D+3,3)}   D in {p+1, 2p, 2p+1, 2p+2}
```

4 x 3 x 4 = **48 patterns per prime**, `n = 9`, maximum degree `2p+5`.

**F2 — random sparse.** 40 pairs per prime, seed `1000003*p + 17`;
`|S_P|, |S_Q|` in `{4,...,7}`; total degrees in `{4,...,20}` and attained;
`(1,0)` always in `S_P` and `(0,1)` always in `S_Q`; each support forced to
contain a pure-`x` monomial and a mixed monomial. `n <= 14`.

**F3 — the Mondello support verbatim**, one cell per prime.

Supports are written to `night9/supports/<hash>.json`
(`hash` = first 12 hex of the SHA-1 of the sorted support pair).

## 3. Method ladder

* `exhaustive-bilinear` — **complete**. Enumerate the smaller side inside the
  affine subspace cut out by its own collision equation (`p^nfree` points,
  `nfree = |side| - 1` when that equation is nonzero mod `p`), and for each
  enumerated point solve the resulting **linear** system over `F_p` for the
  other side by batched Gauss-Jordan. Every `F_p` point is visited, so the
  reported count is exact. Used when `p^nfree <= 400000`.
* `groebner-gfp-field` — `sympy.groebner` over `GF(p)` of the system
  **together with the field equations** `z^p - z` for every unknown, so that
  the variety is exactly the set of `F_p`-rational points; `basis == [1]` iff
  EMPTY. 300 s timeout.
* `sampling-linear-fibres` — lower-bound probe only, 200000 random draws of
  the smaller side each followed by an exact linear solve, covering
  `>= 10^6` points. A miss is recorded INCONCLUSIVE, never EMPTY.

Verdicts: NONEMPTY / EMPTY / INCONCLUSIVE / TIMEOUT.

## 4. Per-hit protocol

For each solution in the recorded sample:

1. **Degeneracy screen** (cheap, applied to the effective support of the
   solution, i.e. its nonzero coefficients). DEGENERATE if `P` has no monomial
   involving `y` and `Q` has no monomial involving `y` outside its pure-`y`
   part, or the `x <-> y` mirror. DEGENERATE hits are recorded and go no
   further.
2. **Direct substitution**: `det J - 1 = 0` as a polynomial identity in
   `F_p[x,y]`, and `P(0,1) = P(1,0)`, `Q(0,1) = Q(1,0)`. The four values
   `P(0,1), P(1,0), Q(0,1), Q(1,0)` and the two images are recorded.
3. **Tear data mod p** (see §5).
4. **Hensel** to `Z/p^2`, and on success to `Z/p^3`. TEAR-NONEMPTY hits are
   lifted first (priority rule).

## 5. Tear data mod p

```
R1 = Res_y(P - u, Q - v)  in F_p[x,u,v],   R2 = Res_x(P - u, Q - v) in F_p[y,u,v]
```

Recorded: `lc_x(R1)` (coefficient of `x^{deg_x R1}`, an element of `F_p[u,v]`),
`lc_y(R2)`, and their product.

```
product a nonzero CONSTANT  ->  TEAR-EMPTY
product NONCONSTANT in u,v  ->  TEAR-NONEMPTY
```

Rationale recorded verbatim as supplied by the coordinator: *proper
(tear-empty) char-p Keller collisions can arise from additive/Artin-Schreier-type
maps, a mechanism specific to positive characteristic; non-proper
(tear-nonempty) hits are structurally closer to what characteristic zero could
support.*

Computation. Everything is done directly over `F_p` by an exact Laplace
expansion with row-subset memoisation of the Sylvester matrix, entries held as
sparse dicts. Two exact shortcuts are used:

* the two resultants play symmetric roles in the product, so whichever has the
  smaller Sylvester matrix is expanded first;
* `F_p[u,v]` is an integral domain, so if the leading coefficient of the
  cheaper resultant is **nonconstant** and the other resultant is nonzero, the
  product is nonconstant and the hit is TEAR-NONEMPTY whatever the other
  leading coefficient is. `R != 0` is certified by exhibiting numeric
  `(y0,u0,v0)` in `F_p^3` at which the Sylvester determinant is nonzero.

When the remaining Sylvester expansion exceeds the size cap (30), the state cap
(400000) or the per-call time budget (5 s), the class is recorded as
**TEAR-NOT-COMPUTED**; nothing is guessed. This happens mainly at the larger
primes, where the F1 supports have `x`-degrees of order `2p`.

Note on provenance: the tear fields inside `night9/hits/` were produced during
the sweep with the size cap at 18; the caps quoted above (30 / 400000 / 5 s)
are those used for `night9/census.csv` and `night9/hits_nondegenerate/`, which
are the authoritative tear numbers reported in §8. The classification rule and
all arithmetic are identical; only the cap at which a cell is abandoned as
TEAR-NOT-COMPUTED differs.

## 6. Hensel step (rederived in lane)

The residual map `r : Z^N -> Z^M` of (K)+(C) is quadratic, so Taylor is exact:
`r(x + h) = r(x) + Dr(x) h + B(h,h)`. If `r(x_k) = 0 mod p^k` with `k >= 1`,
write `r(x_k) = p^k s_k` and look for `x_{k+1} = x_k + p^k d`. Then

```
r(x_k + p^k d) = r(x_k) + p^k Dr(x_k) d + p^{2k} B(d,d),
```

and `2k >= k+1`, so mod `p^{k+1}` this is `p^k ( s_k + Dr(x_k) d )`. Hence a
lift exists **iff** `Dr(x_k) d = -s_k` is solvable mod `p`, and
`Dr(x_k) = Dr(x_0) mod p` since `x_k = x_0 mod p`. The condition is necessary
as well as sufficient. Each computed lift is re-checked by evaluating the
integer residual mod `p^{k+1}`.

## 7. Results — the sweep

534 cells (89 per prime x 6 primes), all completed; see
`night9/prime_survey.csv` and `night9/prime_survey_summary.json`.

| p | F1 | F2 | F3 | NONEMPTY | EMPTY | INCONCLUSIVE | TIMEOUT |
|---|---|---|---|---|---|---|---|
| 3  | 48 | 40 | 1 | 67 | 22 | 0 | 0 |
| 5  | 48 | 40 | 1 | 63 | 26 | 0 | 0 |
| 7  | 48 | 40 | 1 | 53 | 36 | 0 | 0 |
| 11 | 48 | 40 | 1 | 50 | 39 | 0 | 0 |
| 13 | 48 | 40 | 1 | 51 | 38 | 0 | 0 |
| 17 | 48 | 40 | 1 | 49 | 40 | 0 | 0 |
| **total** | 288 | 240 | 6 | **333** | **201** | **0** | **0** |

Methods used: `exhaustive-bilinear` 522 cells, `groebner-gfp-field` 12 cells,
`sampling-linear-fibres` 0 cells.

By family:

| family | p=3 | p=5 | p=7 | p=11 | p=13 | p=17 |
|---|---|---|---|---|---|---|
| F1 NONEMPTY / cells | 48/48 | 48/48 | 48/48 | 48/48 | 48/48 | 48/48 |
| F2 NONEMPTY / cells | 19/40 | 15/40 | 5/40 | 2/40 | 3/40 | 1/40 |
| F3 NONEMPTY / cells | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |

The F3 cell — the exact `p = 2` Mondello support — is EMPTY at every one of
`p = 3, 5, 7, 11, 13, 17`, by complete enumeration.

Exact `F_p` solution counts, summed over the NONEMPTY cells of that prime:
`p=3: 774`, `p=5: 748`, `p=7: 1146`, `p=11: 2200`, `p=13: 3636`, `p=17: 6928`.

## 8. Results — the non-degenerate census

`census.py` enumerates the **complete** solution set of every NONEMPTY cell
(no cell was truncated; the totals agree with the exact counts of §7, which is
an internal consistency check on the solver) and splits it by the degeneracy
screen. `night9/census.csv`, hits in `night9/hits_nondegenerate/`.

15432 `F_p` solutions in total across the 333 NONEMPTY cells: **3012
DEGENERATE**, **12420 NON-DEGENERATE**, spread over **111** cells that contain
at least one non-degenerate solution.

| family, p | cells | all solutions | DEGENERATE | NON-DEGENERATE | cells with >=1 non-deg |
|---|---|---|---|---|---|
| F1, 3  | 48 | 468  | 96  | 372  | 48 |
| F1, 5  | 48 | 368  | 192 | 176  | 6 |
| F1, 7  | 48 | 756  | 288 | 468  | 6 |
| F1, 11 | 48 | 2180 | 480 | 1700 | 6 |
| F1, 13 | 48 | 3312 | 576 | 2736 | 6 |
| F1, 17 | 48 | 6656 | 768 | 5888 | 6 |
| F2, 3  | 19 | 306  | 68  | 238  | 16 |
| F2, 5  | 15 | 380  | 148 | 232  | 11 |
| F2, 7  | 5  | 390  | 336 | 54   | 3 |
| F2, 11 | 2  | 20   | 20  | 0    | 0 |
| F2, 13 | 3  | 324  | 24  | 300  | 2 |
| F2, 17 | 1  | 272  | 16  | 256  | 1 |

Of the 48 F1 cells per prime, the ones carrying non-degenerate solutions are 48
at `p = 3` and exactly **6** at each of `p = 5, 7, 11, 13, 17`. At those primes
the six are, without exception, the cells with `D = 2p`, i.e.

```
S_Q = {(0,1), (2p,0), (2p+1,1), (2p+2,2), (2p+3,3)}
```

together with `S_P` containing `(2p,0)` and either `A = p` (any `C`) or
`C = 0` (any `A`).

Direct-substitution verification failures across the whole lane: **0** (678
non-degenerate solutions checked in the census, 444 in the sweep).

### Tear classification (characteristic p)

Counts of non-degenerate sampled solutions (up to 8 per cell) by tear class:

| p | TEAR-NONEMPTY | TEAR-EMPTY | TEAR-NOT-COMPUTED / other |
|---|---|---|---|
| 3  | 231 | 87  | 0 |
| 5  | 32  | 92  | 0 |
| 7  | 0   | 52  | 16 |
| 11 | 0   | 0   | 48 |
| 13 | 0   | 16  | 48 |
| 17 | 0   | 1   | 55 |
| **total** | **263** | **248** | **167** |

TEAR-NONEMPTY appears only at `p = 3` (F1 and F2) and `p = 5` (F2 only). Every
F1 tear class that was computed at `p >= 5` is TEAR-EMPTY. The
TEAR-NOT-COMPUTED entries are exactly the cases where the remaining Sylvester
expansion exceeded the size / state / time caps of §5; they are concentrated in
F1 at `p >= 7`, where the supports have `x`-degrees of order `2p`.

For reference, at `p = 2` on the exact Mondello support the base point
`P = x + x^2y + x^4 + x^6y^2`, `Q = y + x^5 + x^6y + x^7y^2 + x^8y^3` is
TEAR-NONEMPTY (`lc_x(R1) = v^2`), while the one point that lifts to `Z/4`,
`P = x + x^4`, `Q = y + x^5`, is DEGENERATE by the screen and TEAR-EMPTY
(`lc_x(R1) = lc_y(R2) = 1`).

## 9. Lifting

Hensel steps were attempted on every verified, non-degenerate sampled hit.

* Solutions climbing to `Z/p^2`: **8** in total, all in family **F2**, all at
  `p = 3` (6, in three cells: `3ee4c514dba8` 3, `c764f008a1a1` 2,
  `cf8c7ed97c0c` 1) and `p = 5` (2, in one cell: `e3ff048903ae`).
  None in F1 or F3, none at `p = 7, 11, 13, 17`.
* Solutions climbing to `Z/p^3`: **0**, at every prime and in every family.
* At `p = 2` (control) exactly one of the 8 `F_2` points climbs to `Z/4` and
  it does not climb to `Z/8`.

The cells with a `Z/p^2` climb are listed in `night9/census.csv`
(`climb_p2 > 0`) with the lifted coefficient vectors in
`night9/hits_nondegenerate/<hash>_p<p>.json`.

## 10. Files

```
night9/keller_solver.py        system, exhaustive solver, verification, Hensel
night9/tear.py                 tear data mod p
night9/survey.py               the 534-cell sweep
night9/census.py               complete solution lists for the NONEMPTY cells
night9/control_p2.py           the mandatory positive control
night9/summarize.py            tallies
night9/prime_survey.csv        one row per cell
night9/prime_survey_p<p>.csv   per-prime shards
night9/prime_survey_summary.json
night9/census.csv              one row per NONEMPTY cell
night9/control_p2.json
night9/supports/<hash>.json    every support pair used
night9/hits/<hash>_p<p>.json   sweep-sample solutions with verification/tear/lift
night9/hits_nondegenerate/     census-sample non-degenerate solutions
night9/log_p<p>.txt, census_log.txt
```
