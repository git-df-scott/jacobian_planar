# The s-ladder: the pentagon in ONE variable

## The reduction

Every `w`-homogeneous polynomial of weight `a` is `y^a h(s)` with `s := x y`,
because `x^i y^(i+a) = y^a (xy)^i`.  In particular `u = y(s - tau)`.  Then

    **{ y^a h(s), y^b g(s) } = y^(a+b) ( b h'(s) g(s) - a h(s) g'(s) )**

— **CONTROL: PASS**, symbolically, for all `a, b` in `[-1,4]` with `h, g` free
functions.  So `{P,Q} = x^2` becomes, level by level in `w`,

    **sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} s^2**

a bilinear ladder in **one variable** — structurally identical to
`GENERAL_LADDER.md`'s, but with the whole two-variable problem inside it.

Supports straight from the Newton polygons:

    deg h_a : a = 8..-1  ->  8, 8, 8, 7, 6, 5, 4, 3, 2, 1
    deg g_b : b = 12..-1 ->  12,12,12,12,11,10, 9, 8, 7, 6, 5, 4, 3, 2

**CONTROL: level -2 is `s^2` exactly.**  `h_{-1} = s`, `g_{-1} = s^2` (the two
gauge-fixed vertices) give `b h' g - a h g' = s^2`, and `y^(a+b) = y^-2`, i.e.
`x^2`.  PASS.

**CONTROL: level 20** with `h_8 = c0 (s-tau)^8`, `g_12 = c1 (s-tau)^12`: PASS.
Indeed level 20 reads `12 h_8' g_12 = 8 h_8 g_12'`, i.e. `g_12^2 = c h_8^3` — the
upper-edge theorem falls straight out.

**CROSS-CHECK.**  Levels 19 and 18 reproduce the two-variable `w`-cascade
*identically* — level 19 consistent with kernel 10, level 18 giving the same
seven conditions, coefficient for coefficient.  Two independent formulations,
same output.

## Level 18 collapses to one divisibility

Level 19's 10-dimensional kernel is exactly `h_7` (9 coefficients) plus one
constant `lambda`:

    W_19 = 8 c0 g_11 - 12 c1 sigma^4 h_7 = lambda sigma^11 ,   sigma := s - tau
    =>  g_11 = (3 c1 / 2 c0) sigma^4 h_7 + (lambda / 8 c0) sigma^11 .

Substituting (**CONTROL: PASS** on the factorisation):

    11 h_7' g_11 - 7 h_7 g_11'
      = E * sigma^3 * [ (6 c1/c0) h_7 + (11 lambda/8 c0) sigma^7 ] ,
        E := sigma h_7' - 7 h_7 ,   which has **no** sigma^7 term.

Level 18 requires divisibility by `sigma^7`.  Both factors have `sigma`-order
`nu := ord(h_7)`, so the product has order `2 nu + 3`.  Measured:

    nu = 0 -> order 3    NOT divisible
    nu = 1 -> order 5    NOT divisible
    nu = 2 -> order 7    DIVISIBLE
    nu >= 3 -> divisible

So the seven messy quadrics in nine `q`-variables are exactly one statement:

    **(s - tau)^2 divides h_7 .**

Same `tau` as the eighth-power theorem.  Everything concentrates at `s = tau`.

## The pattern so far

    h_8 = c0 (s - tau)^8          (eighth-power theorem)
    (s - tau)^2 | h_7             (level 18)
    g_12 = c1 (s - tau)^12 ,  g_11 determined by h_7 and one constant

## Why the one-variable form matters

The operator `{u,-}` acts on weight-`k` pieces as `D_k(h) = k h - (s - tau) h'`,
which in the `sigma` basis is **diagonal**: `D_k(sigma^m) = (k - m) sigma^m`.
Kernel `sigma^k` (i.e. `u^k`); image everything but the `sigma^k` slot.  So each
level carries **exactly one scalar obstruction** plus a divisibility, and the
freedom is exactly one constant — the kernel `C[u]`, named at last.

## Status

Pentagon **NO VERDICT**.  The problem is now a one-variable bilinear ladder in
10 + 14 unknown polynomials of degree <= 12, descending under an explicit
diagonal operator.
