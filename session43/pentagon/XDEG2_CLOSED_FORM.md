# x-degree 2 in closed form: a descending ladder of ODEs

The analogue, for `deg_x P = 2`, of the reduction that settled `deg_x P <= 1`.

## Setup

`P = a(y) x^2 + b(y) x + c(y)`.  Complete the square with `w = x + b/(2a)`:

    P = a w^2 + e ,      e = c - b^2/(4a)

`u = P` is a first integral of the bracket, so at fixed `u`

    w^2 = (u - e)/a ,     Q_y|_u = x^2/P_x = (w - b/2a)^2 / (2 a w)

which expands to

    **Q_y|_u  =  w/(2a)  -  b/(2a^2)  +  b^2/(8 a^3 w)**

Unlike the `deg_x P <= 1` case, `w` is **algebraic of degree 2** over `C(u,y)`,
so Q is not polynomial in `u` and the three-x-slot collapse does not transfer.
That was the obstacle.  The way past it is to work in `w` rather than `u`.

## The key step

`Q` is a polynomial in `(x,y)`, hence in `(w,y)` since `w = x + b/2a` is a
y-dependent shift.  Write `Q = sum_k q_k(y) w^k`.  Differentiating at fixed `u`,
with `u - e = a w^2`,

    w_y = -( a' w^2 + e' ) / (2 a w)

so

    dQ/dy|_u = sum_k [ q_k' w^k  -  k q_k ( a' w^k + e' w^{k-2} ) / (2a) ]

Matching against `Q_y|_u` power by power in `w` gives a **closed ladder**:

    w^{-1} :  q_1 e'                     = -b^2/(4 a^2)
    w^0    :  q_0' - q_2 e'/a            = -b/(2 a^2)
    w^1    :  q_1' - q_1 a'/(2a) + 3 q_3 e'/(2a) = 1/(2a)
    w^k    :  q_k' - k q_k a'/(2a) - (k+2) q_{k+2} e'/(2a) = 0   (k >= 2)

## Two things this immediately gives

**1. It reproduces the leading relation, as a consistency check.**
If `Q` has `w`-degree `N` then `q_{N+2} = 0`, so the `k = N` rung reads

    q_N'/q_N = N a'/(2a)     =>     **q_N^2 = const * a^N**

which is exactly `b_n^m = c a_m^n` at `m = 2, n = N` — derived independently in
`STRUCTURE.md` §2 from degree-counting.  The two derivations agree, which is
the check I wanted before building on either.

**2. Descending the ladder is a sequence of polynomiality conditions.**
Each rung `k` is a *first-order linear ODE* for `q_k` with a source supplied by
`q_{k+2}`, solvable by integrating factor `a^{k/2}`:

    q_k = a^{k/2} * integral [ (k+2) q_{k+2} e' / (2a) ] a^{-k/2} dy

so `q_k` is polynomial only if that integral is.  **Each rung is one explicit
condition**, exactly as `sigma R' - 2 sigma' R = 1` was the single condition at
x-degree 1.  The ladder terminates because `Q` has bounded `w`-degree.

## Status: CONTROLLED

Two planted solutions, both with `{P,Q} = x^2` verified symbolically first:

| planted point | why | result |
|---|---|---|
| `P = x^2`, `Q = xy/2` | simplest genuine x-degree 2 | all rungs OK |
| **`P = x^2 + xy`, `Q = xy/2`** | **`b = y` nonconstant, `e = -y^2/4` nonzero** | **all rungs OK** |

The second is the one that counts.  With `b` nonconstant and `e != 0`, no rung is
trivially absent — the `w^-1` rung reads `q_1 e' = -y^2/4` against
`-b^2/(4a^2) = -y^2/4`, the `w^0` rung `-y/2` against `-b/(2a^2) = -y/2`, and the
`w^1` rung `1/2` against `1/(2a) = 1/2`.  A weak control (the first row) would
have passed with most terms zero and proved nothing; that is the failure mode that
caught me on the bilinear export last night, so it was worth building the second.

**LADDER CONTROL: PASS.**  The reduction is now safe to build on.

Scope caveat, carried from `STRUCTURE.md`: this assumes **Q polynomial**, which
a genuine counterexample satisfies but the truncated 66-condition export does
not.  Fine for a witness hunt; not fine for an emptiness claim about the export.
