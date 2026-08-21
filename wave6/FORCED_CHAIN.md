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

---

# v2: exploit EVERY hypothesis (`w6_forced_chain2.py`)

Two things v1 left on the table, both from being too conservative:

**(a) `eq41` is `−1 + c_1_0 = 0`, i.e. `c_1_0 = 1` exactly** — a gauge
normalisation in plain sight. v1's pivot rule *skipped* any variable listed as
nondegenerate, so it refused to solve for it. Correct rule: eliminate it and
carry the condition forward in discharged form. Here the value is `1`, so
`c_1_0 ≠ 0` is discharged outright.

**(b) Common monomial factors.** `eq282 = 12·c_8_15·s_4_8³ − 8·d_12_23·s_4_8²`
has every term divisible by `s_4_8²`, and `s_4_8 ≠ 0` is required — so it
divides out, giving `d_12_23 = (3/2)·c_8_15·s_4_8`. v1 never looked for common
factors at all.

| | original | v1 | **v2** |
|---|---|---|---|
| equations | 283 | 229 | **212** |
| variables | 165 | 111 | **95** |
| pivots | – | 52 | **67** |

## A redundant equation, predicted then observed

`eq278 = 57·c_8_15·s_3_7·s_4_8² − 38·d_12_23·s_3_7·s_4_8`. Dividing by
`s_3_7·s_4_8` gives `d_12_23 = (57/38)·c_8_15·s_4_8`, and **57/38 = 3/2
exactly** — the same relation `eq282` gives. So `eq278` carries no independent
information.

This shows up in the bookkeeping: 70 variables were removed (3 zeros + 67
pivots), which should leave 213 equations, but **212** remain. One equation went
trivial beyond the accounting.

**CORRECTION (self-caught).** I first wrote that this makes the true
overdetermination "117, not 118". That is imprecise and the 118 stands. An
exact rank computation of the 283 x 8727 coefficient matrix mod (2^61-1) gives
**rank exactly 283, with ZERO linearly dependent equations**. `eq278` is *not*
a linear combination of the others — it becomes redundant only after dividing
by `s_3_7 . s_4_8`, which is a non-linear step licensed by the nondegeneracy
hypotheses. So there are two different, both-correct counts:

  * **un-localized**: 283 linearly independent equations, overdetermination
    **118** — the campaign's number, confirmed;
  * **localized at the nondegeneracy conditions** (i.e. inverting the required-
    nonzero variables): one equation becomes redundant, giving **117**.

The seed-pinned system independently lands on the same 117 after the same
localization (194 equations in 77 variables), which is why the two agree.

## Honest limits of v2

- When a nondegenerate variable is eliminated with a *polynomial* right-hand
  side (`c_8_14`, `d_12_21`), the condition "that polynomial ≠ 0" should be
  carried forward. v2 drops it. This **weakens** the hypotheses, so it can never
  manufacture a false contradiction — any contradiction found under weaker
  hypotheses is still valid — but it does lose forcing power.
- One **unused case-split** remains: `s_3_7` appears as a common factor but is
  not known nonzero, so `s_3_7 = 0` OR the reduced equation holds. Branching on
  it is the obvious next cheap move.
- Densification again stops the run (4.3M terms), not a fixed point.

# The certificate ladder: rung 0 established rigorously

**Degree 0: NO CERTIFICATE**, proved by exact Gaussian elimination over ℚ on the
full 283-equation system (8,727 distinct monomials, 283 multiplier unknowns).
The campaign had only the weaker statement "no equation collapses to a nonzero
constant" from its linear loop; this is the real degree-0 Nullstellensatz test.

**Degree 1 is precisely scoped but out of reach this session**: 283 × 166 =
**46,978** multiplier unknowns against ~10⁶ sparse monomial equations
(≈1.6M nonzeros). Dense elimination on 47k columns is ~10¹⁴ operations. It needs
either a sparse/iterative method over F_p or a smarter support restriction.

# Why the Challenger move does not apply here

Searching for a **small overdetermined closed subsystem** — a set of variables
`S` such that the equations entirely inside `S` already outnumber `S` — found
**none**. Every small variable set carries fewer equations than variables.

That is a real structural fact and it is worth stating plainly: **the pentagon's
overdetermination by 117 is global, not localised.** There is no small piece
whose behaviour decides the question, so the O-ring strategy — isolate the
smallest decisive component — provably cannot be applied by subsystem
extraction here. Any proof of emptiness must be global, which is exactly what a
Nullstellensatz certificate is. This explains why 42 sessions never found a
cheap kill: there isn't one to find.

## The `s_3_7` case split: both branches survive

| branch | equations | variables | overdetermined by | verdict |
|---|---|---|---|---|
| `s_3_7 = 0` | 211 | 93 | 118 | alive |
| `s_3_7 ≠ 0` | 214 | 97 | 117 | alive |

Neither branch reaches a contradiction; both stop on densification rather than
at a fixed point. So the split narrows nothing yet — but it is now set up, and
`w6_forced_chain2.py` takes `zero:VAR` / `nonzero:VAR` to branch on any variable.

**Net position on case (1): still alive, from every direction tried.** No
counterexample, and no proof of emptiness.

---

# The Euler measurement: the load is uniformly distributed

An exact rank computation of the constraint system (283 x 8727 monomial
coefficient matrix, mod 2^61-1):

| quantity | value |
|---|---|
| nominal equations | 283 |
| **true rank** | **283** |
| linearly dependent equations | **0** |
| constant monomial in the row space | **NO** |

**Not one equation is slack.** Every constraint carries independent load — the
overdetermination by 118 is distributed uniformly across all 283, exactly like
compression across every cross-section of an Euler column. This is the precise
sense in which there is no weak notch to find, and it is the same fact the
closed-subsystem search reported from the other side: no small piece decides
anything, because the load is everywhere.

It also re-derives the degree-0 Nullstellensatz result by a second independent
route (rank over F_p, versus exact Gaussian elimination over Q): the constant
is not in the row space, so no constant-coefficient certificate exists.

## What Euler actually tells us to compute

Euler's column does not fail from a crack; it fails when a **global threshold**
is crossed and the structure's mathematics changes character. The analogue for
a polynomial system is exact and classical: the **degree of regularity** -- the
degree D at which the Macaulay matrix `M_D` (rows `x^alpha . F_k`, columns
monomials of degree <= D) first has the constant in its row space. Below that
degree nothing is decided; at it, infeasibility appears all at once.

That is the same ladder as the Nullstellensatz certificate, but the reframing
says what to measure: not "can I find lambda", but **the rank of `M_D` as D
increases, and the codimension of the constant**. D = 0 is done (rank 283, not
reached). D = 1 is 46,978 rows against ~10^6 monomial columns with ~1.6M
nonzeros; a row-subset restriction is sound for a NEGATIVE answer (inconsistency
on a subset implies inconsistency overall), which is the tractable direction and
the recommended next computation.
