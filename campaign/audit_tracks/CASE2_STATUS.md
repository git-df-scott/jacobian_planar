# Case (2) of GGHV Prop 4.3 — the (72,108) window below degree 125

Case (2): `N(P) = {(0,0),(1,0),(8,14),(8,16)}`, `N(Q) = {(0,0),(2,1),(12,21),(12,24)}`,
`[P,Q] = x^2`, degrees (72,108).

## The reformulation that made it tractable (verified, not assumed)

Grade by `w := j - 2i`. N(P)'s slanted edges are `j = 2i` and `j = 2i-2`, so **P
has only weights 0, -1, -2**; N(Q)'s are `j = 2i` and `j = 2i-3`, so **Q has only
weights 0, -1, -2, -3**. With `t := x y^2` each weight piece is a function of `t`
times a power of `y`:

    P = A(t) + B(t)/y + C(t)/y^2,   Q = D(t) + E(t)/y + F(t)/y^2 + G(t)/y^3.

For such forms the bracket is exactly (machine-verified, 8/8 random trials)

    [ phi(t) y^-a , psi(t) y^-b ]  =  ( a phi psi' - b phi' psi ) y^(1-a-b),

so `[P,Q] = x^2 = t^2 y^-4` splits by weight into FIVE equations (the weight-1
part vanishes identically since `a = b = 0`), and the five pieces reconstruct
`[P,Q]` exactly (machine-verified):

    (w= 0)   B D' = A' E
    (w=-1)   -2 A' F + B E' - B' E + 2 C D' = 0
    (w=-2)   -3 A' G + B F' - 2 B' F + 2 C E' - C' E = 0
    (w=-3)   B G' - 3 B' G + 2 C F' - 2 C' F = 0
    (w=-4)   ***  2 C G' - 3 C' G = t^2  ***

Coefficient counts match the lattice points exactly: A 9, B 8, C 8 (= 25 = N(P))
and D 13, E 12, F 12, G 11 (= 48 = N(Q)).  So the whole of case (2) is five ODEs
in seven UNIVARIATE polynomials — against 25 parameters in the raw formulation.

## The lowest-weight equation is self-contained, and solved

`2 C G' - 3 C' G = t^2` involves only `C` and `G`.  Vertex conditions pin
`C = c_1 t + ... + c_8 t^8` with `c_1, c_8 != 0` (`c_0 = 0`, as `(0,-2)` is not a
lattice point) and `G = g_2 t^2 + ... + g_12 t^12` with `g_2, g_12 != 0`.

**Structure, by hand.** At a root `rho` of `C` of multiplicity `m` where `G` has
order `n`, the left side has order `m+n-1` with leading coefficient
proportional to `2n - 3m`.  For `rho != 0` the right side is nonzero, forcing
`m = 1, n = 0`.  So **`C` is squarefree of degree 8** and `G` vanishes at none of
its nonzero roots.  Setting `u^2 = C`, the equation is exactly

        t^2 dt / u^5  =  d( 2 G / u^3 ),

i.e. a specific differential is EXACT on the genus-3 hyperelliptic curve
`u^2 = C(t)`.  Also, `W := G^2 - kappa C^3` (with `kappa` cancelling the degree-24
terms) satisfies `C W' - 3 C' W = t^2 G`, and comparing degrees gives
**`deg W = 7` exactly**; `W = 0` is impossible since it would force
`2CG' - 3C'G = 0`, not `t^2`.

**Solved exactly (Singular, F_65521).**  Two scalings act — `t -> lambda t` and
`(C,G) -> (mu C, G/mu)`, i.e. `c_i -> mu lambda^i c_i`, `g_i -> g_i lambda^(i-3)/mu`
— so `c_1 = c_8 = 1` is attainable over the algebraic closure (it needs a 7th
root of `c_1/c_8`).  In that normalization, 17 unknowns and 17 equations:

| | result |
|---|---|
| raw ideal | **dim 0, vdim 35** |
| with `g_2, g_12 != 0` imposed by Rabinowitsch (`w g_2 g_12 = 1`) | **dim 0, vdim 35** |

so no solution is lost to the vertex conditions.  The univariate eliminants
(`finduni`) are decisive:

- `g_2` has eliminant of degree **1**: `g_2 = 1` is FORCED.
- `g_9` has eliminant of degree **5**, factoring as three linear factors
  (`g_9 = -4723, -17368, -24930` mod 65521) and one irreducible quadratic.
- EVERY other coordinate has eliminant of degree 35, factoring as
  `(deg 7)(deg 7)(deg 7)(deg 14)` **in the 7th power of the variable**.

That 7-fold structure is exactly the residual 7th-root-of-unity symmetry left
over from the normalization, and `g_9` is invariant under it.  Hence

> **The lowest-weight edge equation of case (2) has exactly FIVE essentially
> distinct solutions** (35 = 5 orbits x 7), three of them rational over F_65521
> and two conjugate over a quadratic extension.

Note the saturation route reported `dim = 16` here, which is impossible for a
subvariety of a 0-dimensional scheme: loading `primdec.lib` on top of `elim.lib`
redefines `sat`.  The Rabinowitsch form needs no library and is what the table
above uses.

## Status of the three-stage pipeline

1. **Elimination.** Done for the self-contained lowest-weight subsystem:
   dim 0, vdim 35, five essentially distinct solutions, coordinates as above.
   NOT yet done for the remaining four equations.
2. **Rational lifting.** NOT started — it is premature until a branch is known
   to extend.  (The repo's `tower_lift()` belongs to the old case-(1)
   tau-system and is itself unfinished, so lifting will be implemented against
   whatever stage 1 produces.)
3. **Bracket check.** NOT started.

**No counterexample is claimed and case (2) is not closed.**  What is
established is that the top-edge data is a finite, explicitly computed list of
five candidates, and that the remaining question is whether any of them extends
to `A, B, D, E, F` through the other four equations — which, with `C` and `G`
numeric, is largely LINEAR algebra: `(w=-3)` is linear homogeneous in `(B,F)`,
and `(w=-2)`, `(w=-1)`, `(w=0)` are then linear in `(A,E)` and `D`.

---

## Stage 3 attempted: do the edge solutions extend?

Working in `K = F_p[th]/(th^7 + 7766) = F_{p^7}` (and likewise for the other two
rational factors), the RUR gives `C` and `G` explicitly, and

    EDGE EQUATION 2 C G' - 3 C' G = t^2 HOLDS OVER K,  deg C = 8, deg G = 12

so the stage-1 output is confirmed by independent arithmetic.  The remaining
four equations are then linear algebra over `K`:

| equation | role | result |
|---|---|---|
| `(w=-3)` `B G' - 3B'G + 2C F' - 2C'F = 0` | linear homogeneous in `(B,F)`, 20 unknowns | **solution space dim 3** |
| `(w=-2)` `-3A'G + BF' - 2B'F + 2CE' - C'E = 0` | linear in `(A,E)` given `(B,F)` | always consistent, **kernel dim 3** |
| `(w=-1)` `-2A'F + BE' - B'E + 2CD' = 0` | linear in `D`; its image is `C * {deg <= 11}` | consistency is EXACTLY **`C | (-2A'F + BE' - B'E)`**, 8 conditions |
| `(w=0)` `B D' = A' E` | no new unknowns | not reached |

The `(w=-1)` condition is LINEAR in the three `(w=-2)` kernel coefficients, so it
is SOLVED rather than sampled (sampling it first gave 0/60, which proves
nothing -- the same freezing mistake as the retracted case-(1) spiral).  Solving:

| branch | edge holds | `(B,F)` dim | `(w=-2)` | `(w=-1)` after solving for the kernel |
|---|---|---|---|---|
| `th^7 = 57755` | yes | 3 | consistent | **inconsistent 60/60** |
| `th^7 = 30040` | yes | 3 | consistent | **inconsistent 25/25** |
| `th^7 = 9260`  | yes | 3 | consistent | **inconsistent 25/25** |

**Counting.** For fixed `(B,F)` the `(w=-1)` condition is 8 equations in the 3
kernel coefficients, leaving 5 residual conditions on the 3 parameters of the
`(B,F)` space -- overdetermined by 2.  So emptiness is the expected outcome and
every sample agrees.

**Honest status: NOT a proof.** The three `(B,F)` parameters are still SAMPLED
(over `K`, so random sampling cannot see a positive-codimension locus), and the
two branches conjugate over the quadratic factor have not been run at all.  To
close case (2) this last step must be solved, not sampled: 8 polynomial
equations of degree <= 4 in the 6 parameters (3 for `(B,F)`, 3 for the `(w=-2)`
kernel) over `K` -- a small system, but one that needs Singular over the
algebraic extension `F_p(a)`, `a^7 = -7766`, because the kernel BASIS depends on
`(B,F)` and so the conditions cannot simply be interpolated in a fixed
parametrization.

**No counterexample, and case (2) is not closed.**
