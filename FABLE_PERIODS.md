# The period criterion: what a counterexample must look like, exactly

Fable, 2026-08-23. Code: `fable_xcol/periods.py` (verified).

A reformulation this campaign has never used, and it localises the hunt to a
single thin, classifiable phenomenon.

## The criterion

`{P,Q} = x^2` is `X_P(Q) = x^2`, with `X_P` the Hamiltonian vector field of `P`.
So the entire problem is:

> **For which `P` does `x^2` lie in the image of `X_P`?**

(This is the same fact the determinantal reformulation measured from the matrix
side: `Q` is determined by `P`, here visibly up to `Q -> Q + h(P)`, which is the
kernel of `X_P`.)

Solvability is classical. `Q` exists iff the Gelfand–Leray form

    omega  =  x^2 dx ^ dy / dP

has **vanishing period on every cycle of every generic fibre** `F_c = {P = c}`.
The number of independent conditions per fibre is the first Betti number

    b_1(F_c)  =  1 - chi(F_c) .

## Consequence 1 — why every search collapses to the degenerate families

Any `P` with `P_x = x^2` solves the problem instantly with `Q = y`, since
`{P, y} = P_x`. Verified for `P = x^3/3 + g(y)` at `g = y, y^2, y^5`. The fibres
of such a `P` are **graphs** — simply connected, **no cycles at all** — so every
period vanishes trivially.

That is the structural reason the numerical searches collapse there, and it
matches the first-order obstruction measured in `FABLE_CE_STRATEGY.md`: the
degenerate stratum is where the period conditions are vacuous, and it is
separated from the nondegenerate locus at first order. **Two independent routes
to the same conclusion: local search near the degenerate families cannot work.**

## Consequence 2 — `P` CANNOT be composite. Verified.

If `P = R(h)` with `deg R = d >= 2`, then `N(P) = d · N(h)`, so **every vertex of
`N(P)` must have both coordinates divisible by `d`**. Checked:

| polygon | vertices | `d >= 2` dividing all vertices |
|---|---|---|
| pentagon `N(P)` | (0,0),(1,0),(8,14),(8,16),(0,8) | **NONE** |
| quadrilateral `N(P)` | (0,0),(1,0),(8,14),(8,16) | **NONE** |
| pentagon `N(Q)` | (0,0),(2,1),(12,21),(12,24),(0,12) | **NONE** |

The vertex `(1,0)` alone forces `d = 1` — and `(1,0)` is exactly the
normalisation `p_{0,1} != 0` that the campaign has always imposed. So in **both**
sub-cases, `P` is not a composite polynomial.

## Consequence 3 — this localises the counterexample precisely

Classical tangential-centre / polynomial-moment theory says that in a wide range
of families, the *only* mechanism making all periods vanish is that `P` is
composite with the form aligned to the composition (the "composition
conjecture"). Here composition is **impossible**. Therefore:

> **A nondegenerate solution must exhibit vanishing periods WITHOUT
> composition.**

The composition conjecture is known to be **false in general** — Pakovich and
collaborators constructed counterexamples — so this is *not* an emptiness proof.
But it is the sharpest localisation the campaign has: a counterexample must sit
in the non-composite vanishing-period locus, which is a thin phenomenon with an
existing classification literature.

## Why this is worth pursuing before more elimination

1. **It eliminates `Q` honestly.** The determinantal form showed `Q` is
   redundant; the period criterion says *why*, and replaces 124 unknowns with a
   condition on `P` alone.
2. **It gives a finite condition count.** `b_1(F_c) = 1 - chi(F_c)` conditions
   per fibre, computable from the Newton polygon and the forced edge
   degeneracies — no solver.
3. **It has a literature.** Non-composite vanishing periods are studied
   (Christopher, Pakovich, Muzychuk, Roytvarf). The known counterexamples to the
   composition conjecture have specific shapes; checking whether any is
   compatible with the pentagon's polygon is a bounded literature-plus-algebra
   task, and either outcome is decisive — a match is a **construction
   blueprint**, a mismatch across the classification is strong evidence of
   emptiness.
4. **It is independent** of the descent, the charts, the gates, the determinantal
   rank test, and of any properness assumption.

## Where this sits in the ranked strategies

This upgrades what was "angle 3" into a concrete fourth strategy, and on
present evidence I would rank it **second**, above the degree-8 jet ansatz:

1. Finish sub-case (2) to a certificate (cheapest, gives a verdict either way).
2. **Non-composite vanishing periods** — localises where a CE must live, has a
   literature, needs no solver.
3. Degree-8 jet-along-a-curve ansatz.
4. Above-125 targets ranked by support count and vertex count.

## Status

No counterexample. Pentagon and sub-case (2): **NO VERDICT**. What is new is a
correct reformulation, a verified proof that `P` cannot be composite in either
sub-case, and a second independent confirmation that the degenerate families are
a dead end for local search.
