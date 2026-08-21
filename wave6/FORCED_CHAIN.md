# The nondegeneracy conditions were being wasted

Certifier: `wave6/w6_forced_chain.py`. Independent verification: back-substitution
at 4 random points mod (2⁶¹−1) — **PASS**.

## The opening nobody used

The case (1) system contains **single-monomial equations**:

    eq0  :  c_1_0 · d_0_1 = 0
    eq20 :  c_1_0 · d_1_1 = 0

and `c_1_0 ≠ 0` is one of the system's **own** nondegeneracy conditions. A
product vanishes with one factor known nonzero, so

>  **d_0_1 = 0 and d_1_1 = 0, forced. No computation, no solver, no choice of
>  field.** `d_0_2 = 0` follows on the next round.

**Why this was missed for 42 sessions.** `w6_pent_lineloop.py` reduced using
"only total-degree-1 equations with constant coefficients in F_p" — these are
*degree 2*, so it structurally could not see them. The nondegeneracy conditions
`c_1_0, c_8_14, d_12_21, s_4_8 ≠ 0` were being carried as a **filter applied at
the end** (to sift candidate seeds) rather than as **hypotheses used during
reduction**. That is a reusable lesson: everywhere the campaign carries side
conditions, they should be feeding the elimination, not just screening its
output.

## Generalising the pivot: polynomial right-hand sides

The campaign's loop also required the *right-hand side* to be constant. But
`eq21: −2·c_0_1 + 2·c_1_0·d_1_2 = 0` gives `c_0_1 = c_1_0·d_1_2` — a clean
polynomial substitution with **no denominator**. The correct rule is:

> a variable occurring as a bare `constant · v` in **exactly one term** of its
> equation can be eliminated exactly over ℚ, with a polynomial RHS.

Applying it repeatedly, smallest-equation-first:

| | before | after |
|---|---|---|
| equations | 283 | **229** |
| variables | 165 | **111** |
| c-variables | 51 | **0 — all eliminated exactly over ℚ** |
| overdetermination | 118 | **118** |

**This realises the variable-projection representation change symbolically
rather than numerically.** VARPRO solves the c-block by linear algebra at every
numerical evaluation; the forced chain solves it once, exactly, over ℚ, and
hands back a system in the (d,s)-variables alone. That the overdetermination
invariant is still exactly 118 — matching both the linear-reduction count and
the Segre expected-dimension count −118 — is an independent consistency check
on the whole export chain.

## Honest cost, and no contradiction

Substitution **densifies**: 8,592 terms → 1.7M. So this is a genuine exact
reduction but **not automatically a win for downstream solving** — fewer
variables bought at the price of density is the classic elimination trade-off,
and a Gröbner run on the dense reduced system may well be worse, not better.

**No contradiction was reached.** Had some equation collapsed to `nonzero = 0`,
or had a monomial in required-nonzero variables been forced to vanish, that
would have been a *proof* that case (1) is empty — exact, over ℚ, with no solver
trusted, re-checkable by reading the chain. It did not happen. **Case (1)
remains alive.**

## Verification

Soundness of each step is provable, but the implementation is not. Checked by an
independent route: pick random values mod (2⁶¹−1) for the 111 surviving
variables, recompute the eliminated variables from their pivot expressions in
reverse order, then evaluate **all 283 original equations**. Every spent
equation vanishes identically and every live equation matches the reduced
system pointwise, on 4 independent trials.
