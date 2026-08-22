# What the eighth-power theorem says: P and Q are powers of a single cubic

## The grading

The upper edge of `N(P)` runs `(0,8) -> (8,16)`, so `j - i = 8` is constant along
it.  Grade monomials by

    w(x^i y^j) := j - i .

Then `w = 8` is the **maximum** of `w` on `N(P)` and `w = 12` the maximum on
`N(Q)`, and the `w`-initial forms are `y^8 A(xy)` and `y^12 Qh(xy)`.  Feeding in
`EIGHTH_POWER.md`'s `A(t) = c0 (t-tau)^8`, `Qh(t) = c1 (t-tau)^12`:

    **In_w(P) = c0 u^8 ,   In_w(Q) = c1 u^12 ,   u := y (x y - tau) = x y^2 - tau y .**

`u` is `w`-homogeneous of weight 1 (both monomials have `j - i = 1`) and is a
**cubic**.  All three identities are controlled: `In_w(P) = c0 u^8` PASS,
`In_w(Q) = c1 u^12` PASS, `{In_w(P), In_w(Q)} = 0` PASS.

That last one is the point.  The bracket's `w`-degree is at most `8 + 12 = 20`,
while `{P,Q} = x^2` has `w = -2`.  The top graded piece must therefore vanish
identically — and it does, automatically, because both leading forms are
functions of the same `u`.

## So the object is a deformation of one cubic

To leading order in this grading the pentagon is not two independent polynomials.
It is

    P ~ c0 u^8 ,   Q ~ c1 u^12 ,   u a single cubic,

and `u = y(xy - tau)` is **reducible**: a line `y = 0` and a hyperbola
`xy = tau`.  Worth flagging against Path C: the hyperbola is isomorphic to `C*`,
not to `C`, and Chau / Abhyankar-Moh forbids a component of the non-properness
set isomorphic to `C`.  A `C*` component is not forbidden.

## The next order is determined

Write `P = c0 u^8 + ptilde + ...`, `Q = c1 u^12 + qtilde + ...` with
`w(ptilde) = 7`, `w(qtilde) = 11`.  Level 19 of the bracket reads

    8 c0 u^7 {u, qtilde} - 12 c1 u^11 {u, ptilde} = 0 ,

and since `{u, u^4 ptilde} = u^4 {u, ptilde}` (CONTROL: PASS) this is
`{u, 2 c0 qtilde - 3 c1 u^4 ptilde} = 0`.  A `w`-homogeneous polynomial killed by
`{u, -}` is a polynomial in `u`, so

    **qtilde = ( 3 c1 u^4 ptilde + lambda u^11 ) / (2 c0)** ,  lambda a constant.

Q's next order is determined by P's, up to one constant.

## Why this reframes the whole problem

`w` runs from `8` down to `-1` on `N(P)` (minimum at the vertex `(1,0)`) and from
`12` down to `-1` on `N(Q)` (minimum at `(2,1)`).  So the bracket's levels run
from `20` down to `-2`, and

    **levels 20 down to -1 must all vanish -- 22 conditions -- and level -2 is x^2.**

Each level is one first-order equation `{u, X} = known`.  So the pentagon becomes
**22 sequential linear steps against a single explicit operator `{u, -}`**, whose
kernel on `w`-homogeneous polynomials is the polynomials in `u` and whose
cokernel is the obstruction.

This is exactly the "rational-function cascade" `OPEN_ITEMS.md` calls *"the single
blocker shared by almost everything else"* — three attempts at which were
retracted with manufactured contradictions — now in correct form and with `u`
explicit.  `GENERAL_LADDER.md` diagnosed why those attempts failed (the levels
are ODEs, and the constants of integration are the kernel freedom a greedy
numeric choice destroys).  Here the kernel is named: it is `C[u]`.

## Verification status of the input

`EIGHTH_POWER.md` rests on `R`'s top-y row sitting at `y`-degree `7+k`.  Now
confirmed at **k = 7, 6, 5** — `deg_y r_k = 14, 13, 12` — each with the `y`-order
`N(Q^2) = N(P^3)` predicts independently (8, 6, 4).  `r_4` requires the rung-11
conditions imposed first and is outstanding.

## Status

Pentagon **NO VERDICT**.  But it is no longer a 186-variable Gröbner problem; it
is a 22-level cascade against `{u, -}` with `u = xy^2 - tau y`.
