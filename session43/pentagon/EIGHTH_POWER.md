# The eighth-power theorem: A(t) = c0 (t - tau)^8

The sharpest pin on the pentagon so far, and the first to **link the two Newton
edges to each other**.  No Groebner basis is involved.

## The argument

`R := Q^2 - c P^3`.  Its top-y row (y-degree `24+k` at x-exponent `k`) is
annihilated — that row *is* the upper-edge theorem `Qh^2 = c A^3`
(`UPPER_EDGE.md`).  The residual ladder's own solutions land exactly 17 rows
lower:

    deg_y r_7 = 14 = 7+7 ,   deg_y r_6 = 13 = 7+6 ,

with y-**orders** 8 and 6, which `N(Q^2) = N(P^3)` predicts independently.  So
`R`'s top-y row sits at y-degree `7+k`, and we may run the upper-edge trick again
on `{P,R} = 2 x^2 Q`:

    LHS term (i,k) lands at y-degree (i+8) + (7+k) - 1 = d+15, uniform in d;
    RHS 2 q_{d-2}  lands at y-degree 12 + (d-2) = d+10 < d+15.

The LHS top-y coefficient therefore **vanishes at every rung**, giving

    sum_{i+k=d+1} (7i - 8k) ahat_i rhat_k = 0 ,

whose generating form is `7 A' Rh = 8 A Rh'`, i.e. `(Rh^8 / A^7)' = 0`:

    **Rh^8 = c A^7** ,   deg A = 8 , deg Rh = 7 ,  8*7 = 56 = 7*8 .

Combined with the upper edge `A = c0 G^2`, `deg G = 4`: every root of `G` has
multiplicity `e` with `8 | 14 e`, i.e. `4 | 7e`, i.e. `4 | e`.  `G` is a quartic,
so `e = 4`:

    **G = g (t - tau)^4 ,   A(t) = c0 (t - tau)^8 ,   Rh = c (t - tau)^7 ,
      Qh = c1 (t - tau)^12 .**

## tau is determined, and it ties the edges together

From the explicit residual solutions,

    rhat_7 = 2048 beta / (3315 alpha rho^5) ,
    rhat_6 = 1792 beta c7_2 / (3315 alpha^2 rho^5) ,   ratio = 7 c7_2 / (8 alpha),

and `Rh = c(t-tau)^7` forces `rhat_6/rhat_7 = -7 tau`, so

    **tau = - c7_2 / (8 alpha) = - p_15_7 / (8 p_16_8) .**

Self-consistent: `ahat_7 = -8 alpha tau = c7_2 = p_15_7`, which is exactly the
leading coefficient of `a_7 = y^12 (y-rho) C_7`.  **This is the first relation
connecting the upper edge to the lower edge's data** — `c7_2` lives in `A_7`,
which the lower-edge and residual ladders constrain, while `alpha = p_16_8` is
the shared corner vertex.

## What it determines

    p_{i+8,i} = p_16_8 * binom(8,i) * tau^(8-i) ,     i = 0..8   (nine coefficients)
    q_{12+k,k} = c1 * binom(12,k) * tau^(12-k) ,      k = 0..12  (thirteen)

**Twenty-two coefficients from three parameters** (`p_16_8`, `tau`, `c1`) — 19
conditions, up from the 16 that `A = c0 G^2` gave.  Three further dimensions
removed, and every vertex stays nonzero automatically since `tau != 0`
(`p_8_0 = p_16_8 tau^8 != 0`).

## Controls

* top-y coefficient of the raw rung vs the `(7i-8k)` anti-diagonal sum, every
  `d = 0..14`: **PASS** — this control **failed first**, at `d+14`, and caught my
  own arithmetic: the correct top degree is `(i+8)+(7+k)-1 = d+15`.  The
  coefficient formula was unaffected.
* generating-function identity `7A'Rh - 8A Rh'`: **PASS**
* POSITIVE: `A = c0(t-tau)^8`, `Rh = cR(t-tau)^7` satisfies every rung: **PASS**
* NEGATIVE: `A = G^2` with `G` having four *distinct* roots forces `Rh = 0`,
  killing `deg_x R = 7`: **PASS**
* Independent arithmetic check, done before the general argument: the top-y rung
  `d = 13`, `8 ahat_8 rhat_6 - 7 ahat_7 rhat_7 = 0`, holds **identically** on the
  explicitly computed `r_6, r_7`.

## Caveat, stated plainly

The step "`R`'s top-y row sits at `7+k` for **every** `k`" is verified at `k = 7`
and `k = 6`, where the ladder determines `r_k` uniquely, and is consistent with
`deg_x R = 7`.  It is not yet proved for `k <= 5`.  If some `r_k` had a higher
top-y row the uniformity would break and this theorem would need restating.
Computing `r_5, r_4, r_3` and checking `deg_y r_k = 7+k` is the outstanding
verification.

## Status

Pentagon still **NO VERDICT**.  Solver-free conditions now: four on the lower
edge, nineteen on the upper edge and top rows, and the residual cascade
`(y-rho)^2 | A_7`, `A_6(rho) = 0`.
