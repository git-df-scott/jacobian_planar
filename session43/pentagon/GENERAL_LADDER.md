# The general ladder: {P,Q} = x^2 as a coupled system of first-order linear ODEs

This supersedes the x-degree-specific reductions.  It needs no completing the
square, no first integral, and no algebraic extension — so it holds at **any**
x-degree, including the pentagon's `m = 8`.

## Statement

Write `P = sum_i a_i(y) x^i`, `Q = sum_k q_k(y) x^k`.  Then

    {P,Q} = P_x Q_y - P_y Q_x = sum_{i,k} [ i a_i q_k' - k a_i' q_k ] x^{i+k-1}

so `{P,Q} = x^2` is exactly, for every `d >= 0`:

    **sum_{i+k = d+1} [ i a_i q_k' - k a_i' q_k ]  =  delta_{d,2}**

## Control

Verified symbolically at `m = 3, n = 4` with all `a_i, q_k` free functions of `y`:
the direct expansion of the bracket and the rung formula agree at **every**
coefficient `x^0 .. x^6`.  **PASS.**

## What it gives

**1. The leading relation, immediately.**  At `d = m+n-1` only `(i,k) = (m,n)`
contributes:

    m a_m q_n' - n a_m' q_n = 0    =>    q_n^m = const * a_m^n

recovering by a third independent route what I first derived by degree counting
(`STRUCTURE.md` §2) and then again from the x-degree-2 ladder
(`XDEG2_CLOSED_FORM.md`).  Three derivations, one relation.

**2. Every rung is a first-order LINEAR ODE.**  Rung `d` involves `q_k'` only
through `i a_i q_k'`, so given the `q` of higher index it determines the next one
by an integrating factor.  The system is **triangular**, and each step's
polynomiality is one explicit condition — exactly the shape that settled
x-degree <= 1 (`sigma R' - 2 sigma' R = 1`) and x-degree 2.

**3. It is the cascade the campaign needed, in correct form.**  `OPEN_ITEMS.md`
calls the "rational-function cascade" *"the single blocker shared by almost
everything else"*, and three attempts at it were retracted with manufactured
contradictions.  The reason is now visible: those attempts treated the levels as
**rank tests on numeric data**.  The levels are not rank conditions — they are
**ODEs**, and the free constants of integration are precisely the kernel freedom
that a greedy numeric choice destroys.  That is the same failure that broke my
own order-by-order lift last night, diagnosed there and confirmed here.

## Why this is the right object for the pentagon

For the pentagon the `a_i` are known explicitly: `a_i(y) = sum_j p_{j,i} y^j`
over the pentagon support.  So the ladder is a triangular system of first-order
linear ODEs with **polynomial coefficients in y**, and requiring each `q_k` to be
polynomial converts it into explicit algebraic conditions on the `p_{j,i}` —
without any Groebner basis.

That is the route to `m = 8`, which is what a genuine solution needs
(`p_16_8 != 0` forces it), and it is reachable in a way the eliminated
degree-22 export never was.

## Status

Framework: **controlled and exact**.  Not yet run at `m = 8`.  Scope caveat
carried from `STRUCTURE.md`: polynomial `Q` is assumed, which a genuine
counterexample satisfies and the truncated 66-condition export does not.
