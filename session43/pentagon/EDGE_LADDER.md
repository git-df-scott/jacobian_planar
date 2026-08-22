# The edge ladder: vertex pinning on the pentagon, with no solver

Derived from `GENERAL_LADDER.md` by running the x-expansion at the pentagon's
own degrees.  **No Groebner basis is involved anywhere in this document.**

## Setup

`m = x-deg P = 8` and `n = x-deg Q = 12`, from the Newton polygons Codex
reconstructed and I audited (`WITNESS.md`):

    N(P): (0,0), (1,0), (8,14), (8,16), (0,8)
    N(Q): (0,0), (2,1), (12,21), (12,24), (0,12)

so, writing `P = sum a_i(y) x^i` and `Q = sum q_k(y) x^k`, the supports are

    a_i = y^(2i-2) A_i,  deg A_i <= 10-i   (i = 1..8)
    q_k = y^(2k-3) B_k,  deg B_k <= 15-k   (k = 2..12)

The six vertices a genuine candidate must keep nonzero are
`p_8_0, p_14_8, p_16_8, q_12_0, q_21_12, q_24_12`, which in edge coordinates is

    alpha := p_16_8 != 0,  A_8(0) = alpha r^2 = p_14_8 != 0  (so r != 0),
    beta  := q_24_12 != 0, B_12(0) = -beta r^3 = q_21_12 != 0.

## The rungs separate

The general ladder's rung `d` is `sum_{i+k=d+1} [i a_i q_k' - k a_i' q_k] = delta_{d,2}`.
Substituting the supports, **every term of rung `d` carries the same power
`y^(2d-4)`, for `d = 19` down to `d = 12`** — the y-exponents come out
`35, 33, 31, ..., 21`, an exact arithmetic progression.  Below `d = 12` the
`i = 0` and `k <= 1` rows join in and the uniformity breaks, exactly as the
polygon's other edge predicts.  So the top eight rungs form a **self-contained
sub-ladder on the edge polynomials alone**:

    sum_{i+k=d+1} { (2k-3i) A_i B_k + y [ i A_i B_k' - k A_i' B_k ] } = 0

Note `2k - 3i` vanishes exactly on the edge slope `k/i = 3/2`, which is why the
top rung is purely differential.

**CONTROL.**  `raw rung == y^(2d-4) * edge rung` checked symbolically with all
`A_i, B_k` free functions of `y`, at every `d = 12..19`: **PASS** (`edgeladder.py`).
The rung formula itself was re-checked against the direct bracket expansion at
`m=8, n=12`: **PASS** (`toprung.py`).

## What the descent forces

Each rung `d` is *linear* in the new unknown `B_{d-7}`.  Consistency is decided
by `rank(Mat) == rank([Mat|vec])`, and the residual minors are conditions on the
`A_i`.  **`sp.solve` returning `[]` here means "generically inconsistent", i.e.
that conditions exist — not that the system is empty.  Every rung below is done
as a rank computation for that reason.**

### Rung 19 — `disc(A_8) = 0`

Only `(i,k) = (8,12)` contributes: `8 A_8 B_12' - 12 A_8' B_12 = 0`, i.e.
`B_12^2 = zeta A_8^3`.  With `deg A_8 = 2` and `deg B_12 = 3`, a nonzero cubic
`B_12` exists **iff** the 4x4 coefficient determinant vanishes, and that
determinant is exactly

    2304 * (4 p_14_8 p_16_8 - p_15_8^2)^2 .

So the pentagon's top P-row is forced:

    **p_15_8^2 - 4 p_14_8 p_16_8 = 0** ,   A_8 = alpha (y-r)^2 ,  B_12 = beta (y-r)^3 .

*Controls.*  NEGATIVE: `A_8 = (y-1)(y-3)` (disc != 0) forces `B_12 = 0`, killing
the vertex `q_21_12`.  POSITIVE: `A_8 = (y-1)^2` gives `B_12 = b3 (y-1)^3`, a
genuine 1-parameter family with `B_12^2/A_8^3` constant.  Both **PASS**.

The y-exponent bookkeeping is an independent check on the whole configuration:
`q_12^8` and `a_8^12` both land on `y^168`, and the top rung divides down by
`y^35` exactly.

### Rung 18 — no condition, and a closed form

7 equations, 5 unknowns, consistent, unique:

    **B_11 = (3 beta / 2 alpha) (y - r) A_7** .

### Rung 17 — `A_7(r) = 0`

8 equations, 6 unknowns, `rank(Mat) = 6` (full column rank), `rank([Mat|vec]) = 7`.
All three nonzero 7x7 minors of the augmented matrix share the factor

    A_7(r)^2  =  (a7_0 + a7_1 r + a7_2 r^2 + a7_3 r^3)^2 ,

with the remaining factors `alpha^5 beta r^k`, all nonzero by non-degeneracy.
So **`(y - r)` divides `A_7` as well**.

### Rung 16 — no new condition.

### Rung 15 — `A_7'(r)^2 = 4 alpha A_6(r)`

10 equations, 8 unknowns, `rank(Mat) = 7`.  The rank drop is the ODE's **free
constant of integration**; it is carried as a symbol from here down, never chosen
(lesson A3).  Only the `(i,k) = (8, d-7)` term carries the new unknown, so `Mat`
depends on `A_8` alone and the residual conditions are exactly
`{ n . vec = 0 : n in leftnull(Mat) }` — one nullspace instead of 405 dense
symbolic minors.  Left-null dimension 3, and all three collapse to the single

    **A_7'(r)^2 = 4 alpha A_6(r)** .

This is why the hypothesis `A_6(r) = 0` failed under test: the condition is a
**coupling** between `A_6` and `A_7`, not a vanishing.  Five hypotheses of the
form "`A_i(r) = 0` for various i" were each refuted at three independent random
points before the nullspace computation gave the true condition.

### Rung 14 — no new condition.

### Rung 13 — one cubic relation

12 equations, 11 unknowns, rank 10.  One new condition, a cubic coupling
`A_5(r)`, the `A_6` coefficients, `A_7'(r)` and `alpha`:

    4 alpha^2 sum_j a5_j  -  2 alpha (sum_j j*a6_j)(sum_j c7_j)  +  (cubic in c7) = 0

(written out in full in `rung14.log`; `sum_j a5_j = A_5(r)` at the gauge `r = 1`).

### Rung 12 — no new condition.  **The descent terminates.**

With all four conditions imposed, rungs 17, 16, 15, 14, 13 and 12 are each
consistent with no further condition.  Below `d = 12` the edge ladder no longer
closes (the `i = 0` and `k <= 1` rows join in), so this is the whole of it.

## The interpretation: the edge polynomial of P must have a regular square root

The top rung gave `B_12^2 = zeta A_8^3`, i.e. `Q ~ P^{3/2}` along the edge.  So
write the reversed edge polynomial `Psi(z) = sum_i A_{8-i} z^i` and expand

    sqrt(Psi)  =  s (y - r) * sqrt(1 + u),   u = (Psi - A_8)/A_8,   alpha = s^2,
               =  c_0 + c_1 z + c_2 z^2 + c_3 z^3 + ...

Each `c_i` may acquire a pole at `y = r`.  **Requiring no pole reproduces the
descent exactly, condition for condition:**

| rung | descent condition | square-root statement |
| --- | --- | --- |
| 19 | `disc(A_8) = 0` | `c_0 = s(y-r)` exists at all |
| 17 | `A_7(r) = 0` | `c_1` regular |
| 15 | `A_7'(r)^2 = 4 alpha A_6(r)` | `c_2` regular |
| 13 | the cubic above | `c_3` regular |
| 18, 16, 14, 12 | none | (no `c_i` at even rungs) |

The `c_2` match is exact.  For `c_3` the *leading* Laurent coefficient factors as
`A_7'(r) x (rung-15 condition)` and so dies automatically once rung 15 holds; the
genuine condition is the **subleading** coefficient, and with rung 15 imposed it
equals the rung-13 condition **on the nose, ratio exactly 2**.

So the entire edge ladder is one statement:

> **The pentagon's edge polynomial for `P` must admit a square root regular at
> `y = r`, through order `z^3`.**

This is GGV's shape analysis at `(72,108)`, obtained mechanically from the
bracket rather than by case analysis — which is precisely what Path D's D1 asks
for ("implement the shape analysis as a program rather than a case analysis").

## Controls

* **Reduction.** `raw rung == y^(2d-4) * edge rung`, symbolically, all `A_i, B_k`
  free functions of `y`, every `d = 12..19`: **PASS**.
* **Rung formula.** Re-checked against the direct bracket expansion at `m=8,
  n=12`: **PASS**.
* **Rung 19, negative.** `A_8 = (y-1)(y-3)` (disc != 0) forces `B_12 = 0`, killing
  the vertex `q_21_12`: **PASS**.
* **Rung 19, positive.** `A_8 = (y-1)^2` gives `B_12 = b3 (y-1)^3`, a genuine
  1-parameter family with `B_12^2/A_8^3` constant: **PASS**.
* **Sufficiency (positive, end-to-end within the edge).**  With the four
  conditions imposed and all remaining `A_i` left free and symbolic, the descent
  runs 17 -> 12 with **zero** further conditions.  So the four are sufficient for
  the edge ladder, not merely necessary.
* **Necessity (negative).**  Each condition arose as a nonzero left-null pairing,
  and the "impose nothing" control is inconsistent at rung 15 at three
  independent random points.
* **Independent cross-check.**  The square-root criterion was derived without
  reference to the descent and reproduces conditions 3 and 4 exactly.
* **Not available:** an end-to-end positive control on a genuine map with this
  Newton polygon, because no such map is known — that is the open question
  itself.  Every step is controlled; the composite is not, and cannot be.

## What this buys the search

Each of the four conditions is **rationally solvable**, so they reduce the
pentagon's parameter space with no algebraic extension:

    disc(A_8) = 0        ->  p_16_8 = alpha, p_15_8 = -2 alpha r, p_14_8 = alpha r^2
                             (3 coefficients -> 2 parameters)
    A_7(r) = 0           ->  solves linearly for one A_7 coefficient
    rung 15              ->  solves linearly for one A_6 coefficient
    rung 13              ->  solves linearly for one A_5 coefficient

That is **four dimensions removed** from every downstream solver target, plus
closed forms for `B_12, B_11, B_10, B_9, B_8, B_7`, obtained with no Groebner
basis at all — in a search where four Groebner attempts across two
representations have returned NO VERDICT, two of them on genuine memory ceilings.

## Status

**The edge descent is complete.**  It yields four necessary conditions and no
more.  It does **not** decide the pentagon: these constrain the leading edge
only, and the pentagon remains **NO VERDICT**.

Scope caveat carried from `GENERAL_LADDER.md`: polynomial `Q` is assumed, which a
genuine counterexample satisfies and the truncated 66-condition export does not.
