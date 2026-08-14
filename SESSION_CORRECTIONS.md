# Session corrections — GGHV Prop 4.3 case (1), pentagons

Date 2026-08-14 (Opus-5 block). This session **retracted three previously
recorded results** and replaced them with proved ones. Nothing here claims a
counterexample, and case (1) is **not** closed. Read this file before
`trackB1_THEOREM_S_square.md`, whose headline is superseded.

## Summary table

| claim | status now | why |
|---|---|---|
| "S must be a perfect square" | **RETRACTED**, replaced by an exact two-component classification | inferred from 40-random-sample tables per stratum; missed a codim-1 component *inside* the `A^2*B` stratum |
| ladder death spiral (OBSTRUCTED at 4, then 7; forced `P_7 = c S^2`) | **RETRACTED** as an artifact | the level↔variable pairing was off by one |
| the polynomial-`W` proof (`wtop(W) = 2`) | **REFUTED** as a proof | Theorem B below proves `wtop(W) >= 5` |
| the stated "gauge caveat" | **RESOLVED** | it only ever affected the polynomial-`W` route; the formal-`F` route needs no gauge |
| `cascade()`'s C4 test | **FIXED** (was scale-strict) | `kappa x^2`, `kappa != 0`, is an equally good Keller pair; no verdict changed |

## 1. The exact classification of S (replaces the perfect-square theorem)

The bottom criterion is `2 S R' + S' R = 2 z^2 S` with `R` rational. Writing
`S = S1 S2^2` with `S1` squarefree and `U := R S2` turns it into
`2 S1 U' + S1' U = 2 z^2 S1 S2` with `U` **always** a polynomial, so only
`deg S2 in {0,1,2}` occur:

- **`deg S2 = 0` (S squarefree): NO SOLUTIONS.** Three explicit conditions on
  S; the Gröbner basis eliminates to degree 5 and all five solutions have
  discriminant zero. The sampled `0/40` row is now an exact finite computation.
- **`deg S2 = 1`: COMPONENT II (new).**
  `S = c A^2 B`, `B = z^2 + u z + v`, `A = 2(5u^2-4v) z + u(7u^2-12v)`.
- **`deg S2 = 2`: COMPONENT I.** Every perfect square.

Both components are 3-dimensional, so the operative consequence survives
unchanged: **S's freedom drops from 5 parameters to 3.** In particular S always
has a repeated root.

Verified three independent ways (`trackB1_component2_verify.py`): the raw
bracket via `slice_bracket()`, the polynomial-`W` criterion, and a brute-force
mod-p linear solve using none of the derivation — component II 25/25 solvable,
random squarefree 0/25, random `A^2 B` off the component 0/25, perfect squares
25/25.

Component II was then searched for the first time (`trackB1_divisor_grid.py`):
component I reproduces the published spiral exactly, and component II behaves
identically. No survivors.

## 2. The off-by-one, and what the ladder really is

In `S^3 | N_m`, the terms carrying the two newest slices are
`3 P_8^2 P_{8-m} = 3a^2 S^4 P_{8-m}` and `6 P_8 P_7 P_{9-m} = 6a S^2 P_7 P_{9-m}`;
with `S | P_7` (level 3) both are `S^3`-divisible and drop. So **level m
constrains `P_{10-m}`**, not `P_{9-m}`. The measured kernel profile said so
(`free == nun` at every level = rank zero) and was misread.

Consequences, all verified:

- **Level 4 is quadratic in `P_6` and never obstructs.** Its whole condition
  sits in S-adic digit 2, the quadratic part is exactly `(3/4)(X^2 mod S)`, the
  linear part is multiplication by a fixed `beta in F_p[z]/(S)`, and completing
  the square gives `D = (4/9)beta^2 - (4/3)gamma` **identically zero**. So it is
  `(X + (2/3)beta)^2 = 0`, always solvable. Constructed `P_6` verified against
  `build_N` directly: **60/60 on both components**.
- **Level 4 is the perfect-square condition on P.** `-(2/3)beta == M^2/(4a)
  mod S` exactly, i.e. `T_2 = (P_6 - T_3^2)/(2T_4)` is a polynomial, `T = P^{1/2}`.
  Generally **level m ⟺ `T_{6-m}` is a z-polynomial**: level 5's codimension
  equals the slack dimension exactly (2 on component I, 1 on component II), it
  holds identically when the slack is zero for arbitrary `z` and `P_5` (10/10)
  and fails for random slack (0/10), and with `P = T^2` an exact square levels 6
  and 7 hold 8/8 while perturbing `P_5` breaks level 6 8/8.
- **The levels are coupled.** For generic level-4 free directions level 5 is
  empty (8/8), yet the joint variety is **DIM 13** (of 15 on component I, of 14
  on component II). Solving level by level with earlier directions frozen finds
  nothing where solutions exist — that is exactly what produced the retracted
  spiral.

`trackB1_rational_cascade.py` rebuilds the cascade with rational slices
`(num, e)` meaning `num/S^e`, so every condition is a polynomial identity
defined at **every** parameter point (the exact-division cascade is only defined
where earlier levels already hold). Witness anchor: `P = Stilde^2` violates no
ladder or vanishing condition and fails only the bottom bracket, exactly 0.

## 3. Two unconditional theorems from x = 0

With `u = P(0,y)`, `v = Q(0,y)`, `U = P_x(0,y)`, `V = Q_x(0,y)`, the polygons
give `deg u = 8`, `deg v = 12`, `u(0), v(0), U(0) != 0`, and `V(0) = 0` (since
`(1,0)` is not in `N(Q)`). `[P,Q] = x^2` at `x = 0` reads

        U v' = u' V,          hence  v'(0) = 0.

With `E := W(0,y) = v^2 - gamma u^3`, the identity (verified 25/25)

        u E' - 3 u' E = v ( 2 u v' - 3 u' v )

gives:

- **THEOREM A: `E != 0`.** If `E = 0` then `v^2 = gamma u^3` forces `u = h^2`,
  `v = ±sqrt(gamma) h^3`, and `U v' = u' V` reduces to
  `±3 sqrt(gamma) U h = 2 V`, nonzero at `y = 0` on the left, zero on the right.
- **THEOREM B: `deg E >= 5`, hence `wtop(W) >= 5`.** The left side has degree
  exactly `7 + deg E` (the leading coefficient carries `deg E - 24 != 0`), the
  right side is `v` times something with `deg v = 12`; and
  `2 u v' - 3 u' v = 0` would give `v^2 = c u^3`, so `E = (c-gamma)u^3` of
  degree 24 unless `E = 0`, excluded by Theorem A.

**Theorem B refutes the polynomial-`W` proof**: the descent on `W` can never
reach weight 2, so the `[P_8,.]`-kernel is *necessarily* nontrivial. The gauge
cannot repair it — `Q -> Q + lambda P` is unavailable (it would create the
monomial `x`, and `(1,0)` is not in `N(Q)`). The formal-`F` route is unaffected:
it absorbs kernel terms into `F`, and its descent was verified airtight
(kernel description 75/75 cells; absorber `[P, P^{3/2}] = 0` 88/88 slices).

## 4. A third engine: the y-adic recursion

Expanding in powers of `y`, `[P,Q] = x^2` at order `y^0` is
`P_0' Q_1 - P_1 Q_0' = x^2`. `N(Q)`'s `j = 0` row is `{(0,0)}` alone, so `Q_0`
is a constant and `Q_0' = 0`; with `P_0 = p_00 + p_10 x`,

        Q_1 = x^2 / p_10     exactly,

forcing `q_01 = q_11 = 0` and `q_21 = 1/p_10` — independently reproducing
`v'(0) = 0` and `V'(0) = 0`. Since `P_0' = p_10` is a nonzero constant, every
higher order solves for `Q_{k+1}`: **Q is entirely determined by P**, with no
square roots, no `S`-denominators and no formal series. The degree bound
`deg Q_j <= (j+3)/2` propagates automatically, so the live conditions are
`N(Q)`'s upper edge (`i >= j-12` for `j > 12`) and termination (`Q_j = 0` for
`j > 24`). P carries 61 lattice-point coefficients. Anchored on `P = x`,
`Q = x^2 y`; self-checked on random P, 5/5.

## What would close case (1)

If `P` were a perfect square **of a polynomial**, case (1) dies at once:
`N(P) = 2N(T)` forces even vertex coordinates but `(1,0)` is a vertex;
equivalently `P^(0)(x) = p_00 + p_10 x` with `p_10 != 0` is not a square in
`C[x]`. The ladder forces `P` to be a square in the *graded z-polynomial* sense
only down to a finite weight, and `P^{1/2}` always exists in the graded
completion as an infinite series — its `y^0` component is the power series
`sqrt(p_00 + p_10 x)`, infinite precisely because `p_10 != 0`. So case (1)
closes iff the support, vanishing and (C4) conditions force that series to
terminate.

## Reproduce

    python3 trackB1_elliptic_locus.py       # the three squarefree conditions
    python3 trackB1_elliptic_solve.py       # five solutions, all disc = 0
    python3 trackB1_star_full.py            # component II
    python3 trackB1_component2_verify.py    # three independent checks
    python3 trackB1_offbyone_check.py       # the pairing bug
    python3 trackB1_level4.py 20 1          # the ring quadratic, D == 0
    python3 trackB1_level4_solve.py 10 1    # constructive P_6 vs build_N
    python3 trackB1_gauge_resolve.py        # kernel 75/75, absorber 88/88
    python3 trackB1_rational_cascade.py     # globally-defined conditions
    python3 trackB1_x0_theorem.py           # Theorems A and B
    python3 trackB1_yadic.py                # the y-adic engine

(`trackB1_level4.py` and `trackB1_level4_solve.py` take a sample count and a
seed; the defaults 150/60 run for many minutes. `trackB1_level4.py` reports
"D degenerate at a factor" for every sample — that is the *expected* outcome and
the point of the section: `D` is not merely a non-unit, it is identically zero
in `F_p[z]/(S)`, which is why level 4 always has a solution. The constructive
consequence is what `trackB1_level4_solve.py` verifies against `build_N`.)

---

## 5. The y-adic verdict engine: N(Q)'s upper edge alone makes case (1) FINITE

`trackB1_yadic_verdict.py` is a complete verdict engine that uses **none** of the
weight grading, the square root `T = P^{1/2}`, the cusp parametrization
`P_8 = a S^2`, the S-classification, or the cascade — only `[P,Q] = x^2` and the
two polygons. Since `Q` is a function of `P`, the live conditions are

    coefficient of x^i in Q_j must vanish for i < j - 12,   13 <= j <= 24,

which is `1+2+...+12 = 78` conditions against P's 61 lattice-point
coefficients (plus 2 more "above N(Q)" conditions at j = 23, 24, and the
termination conditions `Q_j = 0` for `j > 24`, none of which are used below).

**Sanity:** a random P dies at `j = 13`, the very first condition, 150/150.

**A trap avoided.** The natural move — "solve the order-j condition for the
newest slice `P_{j-1}`" — is wrong and reports spurious inconsistency 60/60: the
`i = 0` condition at `j = 13` is *untouched* by `P_12`, because N(P) forces
`P_12` to have `i >= 4`, so it can only contribute to `Q_13` at `i >= 5`. The
low-i conditions are driven by the low-i COLUMNS of P. (Same class of mistake as
the retracted off-by-one: guessing which unknown a condition constrains instead
of measuring it.)

**The measurement.** `trackB1_yadic_jac.py` runs the whole recursion over dual
numbers `F_p[eps]/(eps^2)` to get the EXACT Jacobian — a finite difference over
`F_p` is a secant, not a derivative, and its rank is meaningless for a nonlinear
map. (The conditions reach degree 11 in a single parameter already at `j = 14`,
which is why a 6-point interpolation cross-check fails spuriously; with 26
points the dual-number derivative matches the interpolated linear term exactly.)

| conditions imposed | # | Jacobian rank | dim bound |
|---|---|---|---|
| j = 13..16 | 10 | 10 | 51 |
| j = 13..18 | 21 | 21 | 40 |
| j = 13..21 | 45 | 45 | 16 |
| j = 13..22 | 55 | 55 | 6 |
| j = 13..23 | 66 | **60** | 1 |
| j = 13..24 | 78 | **60** | 1 |

The rank saturates at 60, and the deficiency is completely explained: the ONLY
identically-zero Jacobian column is the parameter `(j,i) = (0,0)`, i.e. `p_00`.
That is exact, not accidental — `Q` does not depend on P's constant term at all,
because `P -> P + nu` leaves `[P,Q] = x^2` and hence `Q` unchanged. On the other
**60 parameters the rank is full**.

> **Consequence.** At any solution where the Jacobian has full rank, the solution
> is ISOLATED modulo the trivial shift `P -> P + nu`. So N(Q)'s upper edge alone
> cuts case (1) from a 61-parameter family down to at most a finite set of
> points — before the termination conditions `Q_j = 0` (j > 24) are imposed at
> all, and with 78 conditions against 60 essential parameters.

Honest labels: the rank is measured at random points, so it bounds the dimension
only where it is attained; the rank can drop on the solution locus itself, and
"78 conditions vs 60 parameters" is strong evidence of emptiness but not a
proof. Deciding emptiness needs elimination, which is out of reach directly
(degree ~24 polynomials in 61 variables).

Reproduce:

    python3 trackB1_yadic_verdict.py scan 150 1    # random P dies at j = 13
    python3 trackB1_yadic_jac.py 2 1               # exact Jacobian ranks
