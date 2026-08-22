# The residual ladder: R = Q^2 - c P^3, and the cascade the edge ladder missed

## The object

The edge theorems make the leading forms of `Q^2` and `c P^3` cancel — the upper
edge gives `Qh^2 = c A^3` (`UPPER_EDGE.md`) and the x-ladder's top rung gives
`q_12^2 = zeta a_8^3` (`EDGE_LADDER.md`).  So

    **R := Q^2 - c P^3**

is genuinely smaller than either term, and `R != 0`: from `Q^2 = c P^3` one gets
`2 Q Q_x = 3c P^2 P_x` and likewise in `y`, hence `{P,Q} = 0`, contradicting
`{P,Q} = x^2`.

Two identities follow from the bracket, both **controlled symbolically**:

    {P,R} = {P,Q^2} - c{P,P^3} = 2 Q {P,Q} = 2 x^2 Q          PASS
    {Q,R} =        - 3c P^2 {Q,P}        = 3c x^2 P^2          PASS

(the second is not independent: `c{P^3,R} - {Q^2,R} = {-R,R} = 0`.)

Matching x-degrees in the first, `7 + deg_x R = 14`, so **`deg_x R = 7`** — down
from `deg_x Q^2 = 24`.

## The ladder

Rung `d` of `{P,R} = 2 x^2 Q` is

    sum_{i+k=d+1} [ i a_i r_k' - k a_i' r_k ]  =  2 q_{d-2} ,

a triangular system with a **nonzero right-hand side at every rung** — strictly
more constrained than the homogeneous edge ladder.

Crucially, every input is **exact**, not an edge approximation: the pentagon's
supports are short enough that the edge results pin the whole polynomial.

    a_8  = alpha y^14 (y-rho)^2                 (support j in [14,16], disc = 0)
    a_7  = y^12 (y-rho) C_7 , deg C_7 = 2       (support j in [12,15], A_7(rho) = 0)
    q_12 = beta y^21 (y-rho)^3                  (support j in [21,24])
    q_11 = y^19 (3 beta/2 alpha)(y-rho)^2 C_7

### Rung 14 — `r_7` is unique

`8 a_8 r_7' - 7 a_8' r_7 = 2 q_12`.  A polynomial solution exists **only** at
degree 14, and is unique:

    r_7 = beta y^8 (y-rho)^2 (195 rho^4 + 240 rho^3 y + 320 rho^2 y^2
                              + 512 rho y^3 + 2048 y^4) / (3315 alpha rho^5)

**Independent check.**  The ODE produces y-order exactly **8**, and `N(Q^2) =
N(P^3)` independently predicts the support `j in [8,31]` at x-exponent 7.  Two
unrelated computations, same number.

### Rungs 13 and 12 — `r_6`, `r_5` unique, no conditions

Both consistent with zero residual conditions and **no free parameters**, and
both come out with the y-order the polygon predicts (6 and 4).

### Rung 11 — the cascade

Two residual conditions.  Their combination is the result:

    **cond2 - 3*cond1  =  16 * C_7(rho)^3**

so `C_7(rho) = 0`, i.e. `A_7'(rho) = 0`, i.e.

    **(y - rho)^2 divides A_7.**

Combined with the edge ladder's rung 15, `A_7'(rho)^2 = 4 alpha A_6(rho)`:

    **A_6(rho) = 0.**

This is exactly the cascade I hypothesised from the edge ladder and then
**refuted** — five variants of "`A_i(rho) = 0`" were tested at three random
points each and all failed (`EDGE_LADDER.md`).  The edge ladder alone genuinely
does not force it.  The residual ladder does, because its right-hand side is
nonzero.  The earlier refutation was correct about the edge ladder and wrong as a
guess about the geometry; the two together settle it.

The remaining piece of `cond1`, with `C_7(rho) = 0` imposed, is a second
independent condition:

    alpha [ 6 A_5(rho) - rho A_5'(rho) ]  =  (explicit bilinear in A_6, C_7)

## Where this points

`(y-rho)^2 | A_8` and `(y-rho)^2 | A_7`, and `A_6(rho) = 0`.  If the cascade
continues, `a_i(rho) = a_i'(rho) = 0` for every `i >= 1`, whence `P(x,rho)` is
constant in `x` and `P_y(x,rho)` is constant in `x`.  Then `{P,Q} = x^2` on the
line `y = rho` reads `P_y(x,rho) Q_x(x,rho) = -x^2`, forcing

    Q(x,rho) = q_0(rho) + q_3(rho) x^3 ,  q_3(rho) != 0 ,  q_k(rho) = 0 otherwise.

Already consistent with what is known: `q_12(rho) = 0` and `q_11(rho) = 0` both
hold identically from the edge results.  Whether the full prediction is
satisfiable is the next computation.

## Errata generated here

* The `{Q,R}` control failed on first run — my **test** had the sign wrong
  (`+3cP^2{P,Q}` where the identity needs `-`); the residual `6cP^2{P,Q}` is
  exactly twice the correct term, confirming the identity as stated.  Claim
  unchanged, test corrected.
* Rung 13 first reported "8 residual conditions" because the loop broke at the
  first degree that produced any — `D = 6`, far below the polygon's allowed
  support `[6,30]`.  Those were **truncation artefacts**, discarded; at the full
  support the rung is consistent with none.
* `sp.sympify` again produced symbols distinct from the assumption-carrying ones,
  so `factor` displayed `16*C_7(rho)^3` while the equality test returned False.
  Re-run with an explicit `locals` table: **True**.  Same root cause as A16.

## Status

The pentagon remains **NO VERDICT**.  What is now solver-free: four lower-edge
conditions, four upper-edge conditions, and the residual-ladder cascade forcing
`(y-rho)^2 | A_7` and `A_6(rho) = 0`.
