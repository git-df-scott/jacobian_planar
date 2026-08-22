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

## Why this matters

`(y-r)` divides `A_8` (twice), `B_12` (three times), `B_11`, and `A_7`.  If the
cascade continues down the edge it forces `A_i(r) = 0` for every `i >= 1`, i.e.
`P(x, r)` constant in `x` — the whole top edge degenerating on a single line.
That would be a solver-free structural obstruction on the pentagon, obtained
where four Groebner attempts across two representations returned NO VERDICT.

## Status

Rungs 19, 18, 17, 16: **done and controlled.**  Rungs 15..12: running
(`cascade.py`, log in `cascade.log`).  No verdict is claimed on the pentagon
until the cascade terminates.

Scope caveat carried from `GENERAL_LADDER.md`: polynomial `Q` is assumed, which
a genuine counterexample satisfies and the truncated 66-condition export does not.
