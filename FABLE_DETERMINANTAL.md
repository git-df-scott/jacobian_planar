# The pentagon is a 57-variable rank-drop problem, not a 186-variable Gröbner problem

Fable, 2026-08-23. Code: `fable_xcol/determinantal.py`, `codim.py`, `varpro2.py`
(all with measurements reproduced below).

This is the biggest computational lever I have found in this campaign, and I
believe it explains why every previous attack stalled.

## The observation

`{P,Q} = x^2` is `X_P(Q) = x^2` where `X_P = P_x d/dy - P_y d/dx`. **For fixed
`P` this is LINEAR in `Q`.** The campaign noticed the system is bilinear
(CLAUDE-001 point 2) and responded by *keeping* `Q` as unknowns, giving a sparse
degree-2 system in 186 variables. That was the wrong direction. `Q` enters
linearly and should be *eliminated*.

## Measurement 1 — exactly one term is inhomogeneous

Which `(P-coeff, Q-coeff)` pairs feed the target monomial `x^2 y^0`? Requires
`i + k = 3` and `ja + jb = 1`. Against the polygon's valuations
(`val a_i = 2(i-1)`, `val b_k = 2k-3`) only `(i,k) = (1,2)` with
`(ja,jb) = (0,1)` survives — the other three splittings need `ja+jb >= 3`.
So the whole inhomogeneous content of the pentagon is

    **p_{0,1} * q_{1,2} = 1**

which the campaign's own normalisation already satisfies. **All 303 remaining
equations are homogeneous.** The pentagon is a *bihomogeneous* system on
`P^59 x P^123` intersected with `p_{0,1} q_{1,2} != 0` — a fact worth having on
its own, because multihomogeneous Bezout and determinantal resolutions apply to
such systems and to nothing the campaign has been running.

## Measurement 2 — the rank, and the reformulation

Let `L'_P` be the `303 x 124` matrix of the homogeneous rows, entries **linear**
in `P`'s 60 coefficients. Then

> **The pentagon is nonempty iff there is an admissible `P` with
> `ker(L'_P) != 0`, i.e. iff the structured matrix `L'_P` drops rank.**

and `Q` is then that kernel vector — **uniquely determined by `P` up to scale**.

Measured over `F_p`, `p = 2^31 - 1`:

    generic P                                  rank(L'_P) = 124 of 124  (full)
    P with the forced a_8 = alpha y^14 (y-r)^2 rank(L'_P) = 124 of 124  (full)

So the kernel is trivial away from a special locus, and a pentagon point
requires a genuine rank drop.

## Why this matters

**The true unknown count is 60, or 57 after the gauge — not 186.** Gröbner
complexity is doubly exponential in the number of variables, so removing 126 of
them is not an optimisation, it is a different problem. Every OOM and timeout in
the campaign ledger (msolve at 13.9 GB, the `esz = 2^25` ceiling, Singular's
expired clocks) was incurred on a system three times larger than the one that
actually needs solving.

It also explains the failure mode of the campaign's earlier eliminations: they
eliminated `Q` by substituting the recursion, producing degree-22 systems with
1,080,147 monomials (ERRATA: "the reductions were de-optimisations"). The
*linear* elimination of `Q` is the one that is free.

## Measurement 3 — how special must P be?

The obstruction is the projected residual `r(P) = P_perp(x^2)` in the
`304 - 124 = 180`-dimensional cokernel. Measured at random `P`:

    ||r(P)|| = 1.000            (= ||x^2||: the projection captures nothing)
    rank(dr/dP) = 57 of 57      (full -- the obstruction map is an immersion)
    span of r(P) over 30 random P: 30 dimensions, still growing

So `P`-space maps into the cokernel as a 57-dimensional immersed submanifold of
a 180-dimensional space, and we need it to pass through the origin:
**expected codimension 123**. That is a strong structural reason to expect
EMPTY — but it is *expected* codimension for a generic linear family, and
`L'_P` is highly structured, so it is not a proof. The determinantal variety
could be far from generic; that is exactly what a rank-drop computation on
`L'_P` would settle.

## Measurement 4 — a variable-projection search, and what it found

Because `Q` is determined by `P`, the right numerical search optimises 57 real
parameters with an exact inner linear solve (VARPRO / Kaufman), not 184
parameters jointly. Over 12 random starts with the gauge `alpha = r = 1`:

    best  || L_P Q - x^2 ||  =  0.719      (against ||x^2|| = 1)

i.e. the best real `P` found leaves 72% of the target unexplained, and the
optimiser consistently drives `Q`'s vertices toward 0 (collapsing onto the known
degenerate families A/B/C). **Evidence toward emptiness over the reals in this
gauge, and nothing more** — local optimisation proves nothing, and the campaign
has correctly retracted numerics as evidence before (P15). It is recorded as a
search result, not a verdict.

## What to do with it

1. **Run the rank-drop computation on `L'_P`.** All `124 x 124` minors of a
   `303 x 124` matrix with linear entries in 57 variables. Do not expand minors —
   use the standard determinantal machinery (Eagon–Northcott / a resolution, or
   a Gröbner basis of the rank-`<=123` locus computed via the Kronecker/
   eliminant route on 57 variables). A 57-variable determinantal ideal is inside
   the reach of the tools that OOM'd on 186 general variables.
2. **Impose the forced edge structure first.** `a_8 = alpha y^14 (y-r)^2` is
   proved (rung 19, exact and global) and the gauge kills `alpha, r`, so 3 of
   the 60 coefficients are already fixed before the determinantal computation
   starts.
3. **Then the six vertex conditions and the rung 17/15/13/11 gates** cut further.

## Honest scope

Nothing here is a counterexample or an emptiness verdict. Pentagon: **NO
VERDICT**. What is established is a reformulation with measurements behind it —
the problem has 57 essential unknowns rather than 186, `Q` is redundant, the
system is bihomogeneous but for one normalisation, and the solvable locus is a
rank-drop locus of expected codimension 123 in a 57-dimensional space.
