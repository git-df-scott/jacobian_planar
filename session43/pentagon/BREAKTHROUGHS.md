# Breakthrough round — five attacks

## B1. Uniqueness of the inhomogeneous face  [PROVED]

For weights `(a,b)` on `(x,y)`, `gamma({f,g}) <= gamma(P)+gamma(Q)-a-b` and
`gamma(x^2) = 2a`, so the top graded level **carries the `x^2` iff**

    **gamma(P) + gamma(Q) = 3a + b .**

CONTROL: `w = j-i` gives `(a,b)=(-1,1)`, `20` vs `-2` -> homogeneous, as observed;
`v = 2i-j` gives `(a,b)=(2,-1)`, `5` vs `5` -> inhomogeneous, as observed.

Scanning every primitive `(a,b)` with `|a|,|b| <= 12`: many gradings satisfy the
criterion, but in **every** one except `(2,-1)` the maximising face is a single
**vertex** on both polygons — always `(1,0)` on `N(P)` and `(2,1)` on `N(Q)`,
which are exactly the two gauge-fixed monomials `p_0_1 = 1`, `q_1_2 = 1`.

    **(a,b) = (2,-1) is the ONLY grading whose inhomogeneous top level is an
    EDGE on both polygons.**

So the lower-edge relation `2 Ah Qh' - 3 Ah' Qh = r^2` is *the* unique exact
inhomogeneous edge relation of the pentagon; every other exact top relation is
homogeneous.  This also explains why the `w`-cascade's level `-2` is `x^2`
identically from those same two vertices.

Consequence: there is no second lower-edge-style relation waiting to be found.
The one we have is already decided **NONEMPTY**, so no *edge* can kill the
pentagon — any obstruction is interior.  (`edgescan.py`)

## B2. The v-cascade bottom: 45 previously unused conditions  [COMPUTED]

Descending, `v`-level `V` introduces `F_{V-2}` and `G_{V-1}`; `F` exists for
`d >= -8` and `G` for `e >= -12`, so levels `V = -12 .. -20` introduce
**nothing** and are pure conditions.  Computed: **45 bilinear conditions in 106
variables**, from `V = -20` (a single equation) up to `V = -12` (nine).

The bottom-most is clean:

    V = -20 :  2 p_8_0 q_13_1 = 3 p_9_1 q_12_0

These constrain combinations the `w`-cascade's bottom never touches — that one
clears levels `-2 .. 8` in entirely different variables.  (`vbottom.py`)

## B3. The two cascades cross-verify  [ESTABLISHED EARLIER, recorded here]

    w-cascade (w = j-i)  : 22 levels, 301 equations
    v-cascade (v = 2i-j) : 25 levels, 301 equations

Two different gradings, different level counts, different per-level splits, same
total.  Independent verification of both support reconstructions.

## B4. The level-16 discrepancy is one rational number  [LOCALISED]

See `L16_DISCREPANCY.md`.  On Codex's branch-1 witness the level-16 `z^19`
coefficient contains no unknowns and evaluates to `27/4`, checked three ways.
Sent as OPUS43-023.

## B5. Neither edge kills the pentagon  [VERDICT]

Upper edge: the 3-parameter family `A = c0(t-tau)^m`, `Qh = c1(t-tau)^n`.
Lower edge: **NONEMPTY**, 282-element basis in 5.6 s with both mutable vertices
saturated, negative control `[1]` in 0.005 s.  With B1 showing there is no other
inhomogeneous edge, **the edges are exhausted as a source of obstruction.**

## Status

Pentagon **NO VERDICT**.
