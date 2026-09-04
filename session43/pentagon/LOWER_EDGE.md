# The lower edge, exactly — and a VERDICT

## The relation

Grade by `v(x^i y^j) = 2i - j`.  The maximum of `v` on `N(P)` is **2**, attained
on the edge `(1,0)-(8,14)`; on `N(Q)` it is **3**, on `(2,1)-(12,21)`.  The
bracket satisfies `v({f,g}) <= v(f) + v(g) - 1`, and

    v(x^2) = 4 = 2 + 3 - 1   EXACTLY.

So — unlike the upper edge, where the top term vanishes identically — **here the
top `v`-piece of the bracket IS `x^2`**.  The lower edge is therefore governed by
an **inhomogeneous** relation, which is strictly more restrictive.

With `r := x y^2`, every `v`-homogeneous piece is `y^a F(r)`, and

    { y^a F(r), y^b G(r) } = y^(a+b+1) ( b F'(r) G(r) - a F(r) G'(r) )   [CONTROL: PASS]

`In_v(P) = y^-2 Ah(r)` and `In_v(Q) = y^-3 Qh(r)` give `y^(a+b+1) = y^-4` and
`x^2 = r^2 / y^4`, hence

    **2 Ah Qh' - 3 Ah' Qh = r^2** ,

    Ah = r + p_2_2 r^2 + ... + p_14_8 r^8        (p_0_1 = 1, gauge; deg 8)
    Qh = r^2 + q_3_3 r^3 + ... + q_21_12 r^12    (q_1_2 = 1, gauge; deg 12)

The homogeneous part `2 Ah Qh' = 3 Ah' Qh` is `(Qh^2/Ah^3)' = 0`, the same shape
as the upper edge — but the `r^2` on the right is what makes this one bite.

**The gauges make the inhomogeneous term automatic**: the lowest order is
`2*r*(2r) - 3*1*r^2 = r^2`, exactly.  So the content is the vanishing of the
`r^3 .. r^19` coefficients: **16 equations in 17 unknowns**.

## VERDICT: NONEMPTY

Saturating both mutable Newton vertices (`p_14_8 != 0`, `q_21_12 != 0`) and
running msolve `-g 2` (Groebner-only, decides emptiness at any dimension):

    POSITIVE run : basis of **282 elements**, 5.588 s   -> ideal proper -> **NONEMPTY**
    NEGATIVE ctl : same system plus the contradictory row `zp*p_14_8 - 2`
                   -> basis **[1]**, 0.005 s            -> correctly EMPTY

The timing matters: the positive run took 5.6 s, not 0 s, so this is **not** the
A16 parenthesis parse artefact (the input is paren-free and was checked).

**So the lower edge does NOT kill the pentagon.**  It admits solutions with both
vertices nonzero, and with 16 equations in 17 unknowns the solution set is at
least one-dimensional.

## What this does and does not say

* It is a verdict on a **necessary condition**, not on the pentagon.  NONEMPTY
  here is not a counterexample and not a witness.
* Both edges are now decided in the same direction: the upper edge admits the
  3-parameter family `A = c0(t-tau)^m`, `Qh = c1(t-tau)^n`; the lower edge admits
  an at-least-1-parameter family.  **Neither edge is where a counterexample dies.**
  Any obstruction is in the interior — the levels 9..16 gap.

## Status

Pentagon **NO VERDICT**.  Lower-edge relation: **NONEMPTY** (controlled).
