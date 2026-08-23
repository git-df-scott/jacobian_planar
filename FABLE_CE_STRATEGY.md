# CE acquisition: a measured obstruction, and the three strategies ranked

Fable, 2026-08-23. Code: `fable_xcol/deform.py`, `sweepcheck.py`, `sc2desc.py`,
`determinantal.py`, `verify.py`. Everything below is measured or derived, and
where a result is invalid I say so.

---

## NEW RESULT (item 5): the degenerate families are a FIRST-ORDER DEAD END

This is the question that decides whether local search can ever work, and it had
never been computed. Using the determinantal form: at a family-A point
(`P = x + f(y)`, `deg f <= 5`) the kernel `ker(L'_P)` is 1-dimensional, and the
rank-drop locus persists along `P_1` exactly when

    L'_{P0} Q_1 + L'_{P1} Q_0 = 0

has a solution — one linear system, because `L'` is linear in `P`. Solving it
mod `p = 2^31-1` and projecting to `P`-space gives the tangent space to the
rank-drop locus. Result for the **pentagon**:

    tangent space dimension: 11  (of 60 P-coordinates)

    p_8_0   : CAN be switched on
    p_14_8  : ***PINNED AT ZERO by every tangent direction***
    p_16_8  : ***PINNED AT ZERO by every tangent direction***
    directions turning on all vertices at once: 0

**So family A is not a limit of nondegenerate solutions, to first order.** Two of
the three required `P`-vertices cannot be switched on by any first-order
deformation. This explains, structurally, why every numerical search in this
campaign collapses onto the degenerate families and cannot escape — it is a
first-order obstruction, not bad luck or bad optimisation.

Scope, honestly: **first order only.** The rank-drop locus could be singular at
these points, with a genuine branch reachable at second order. Testing that is
a concrete follow-up (compute the quadratic term of the obstruction map). But
the practical consequence is immediate: **stop running local searches seeded
near the degenerate families; they are provably going nowhere at first order.**

### Invalid half, flagged

I ran the same computation for sub-case (2) and got "tangent space = all 24
dimensions, both vertices can be switched on". **That result is worthless and I
am discarding it.** In sub-case (2) the column `a_0` is empty (P is divisible by
x), so my "family A" base point degenerated to `P = x`, `Q = x^2 y` — a valid
but maximally degenerate solution, at which the linearisation is uninformative.
Sub-case (2) needs a nontrivial base point before this test means anything.

---

## Answers to the specific questions asked

**Can a degree-8-in-x sweep produce the pentagon?** Not ruled out — and I was
too quick to dismiss it. A degree-`k` sweep gives `deg_x P <= k`, so `k = 8` is
the first degree that *can* reach the pentagon. What I proved is only that
linear and quadratic sweeps cannot (`FABLE_CONSTRUCTIVE.md`).

**Are the edge relations a signature of a hidden construction?** There is real
evidence. The quadratic sweep exists iff `mu^3 = 2E/(V'E - 3VE')` is a perfect
**cube**, where the combination `V'E - 3VE'` pairs a first derivative against a
third multiple. Independently, I showed today that **both** Newton edges satisfy
`B^2 = c A^3` (the campaign had only the upper edge — `FABLE_XCOLUMN.md`). The
same 2:3 resonance appears in the sweep condition and in both edge relations.
That is the strongest hint available that the pentagon is the polygon shadow of
a sweep-type construction.

**Verified solution of `{P,Q} = x^2` from the construction:**
`P = y + mu x`, `Q = P^3 - x^3/3`, `mu^3 = 1/3` — degenerate (P linear in x),
but it confirms the recipe works.

---

## THE THREE STRATEGIES, RANKED

### 1. Finish sub-case (2) to a certificate — highest probability, lowest cost

The only genuinely unexplored branch of the only open case below 125, and it is
small: 70 unknowns / 92 equations against the pentagon's 184/302, overdetermined
by 22 rather than 118. The determinantal form is `111 x 46` with only **24
P-variables (21 after gauge)** — Gröbner in 21 variables is routine; 186 is what
has been OOM-ing for weeks.

My x-column descent there is running **50x faster** than the pentagon (rung 10
in 87 s vs 2231 s), with zero branch points, denominators confined to the
forced-nonzero vertices, and **zero free parameters left at rung 10** — it is
tightening fast toward a pure-condition block of roughly 33 conditions in ~11
parameters. That is directly solvable.

- **Cost:** hours, on one core.
- **Delivers:** a certificate either way — an explicit point, or EMPTY with a
  planted control. Both are results; EMPTY here plus the pentagon **discards
  (72,108) and raises the bound from 108 to 125** by GGHV Theorem 2.1.
- **P(counterexample):** low, but strictly the highest of the three, because it
  is the only place nobody has looked.
- **Next action:** let the descent reach the pure-condition block, then Gröbner
  the residual system; in parallel find a nontrivial base point and redo the
  deformation test properly.

### 2. Degree-8 jet-along-a-curve ansatz — medium probability, low cost

Not "another sweep" — a structured ansatz. Write `P, Q` as degree-8 and
degree-12 jets in `gamma` whose coefficients are built from **one** curve `K(w)`
and its derivatives. This is a far smaller family than the full pentagon system,
and the 2:3 resonance above says it is the right shape to try.

- **Cost:** low. Setting up the degree-8 sweep and imposing `{P,Q} = x^2` is a
  few hundred lines and a modest symbolic solve.
- **Delivers:** either an explicit structured solution (which then goes straight
  to the verifier), or a proof that no sweep of any degree carries the pentagon
  polygon — which would be a clean structural theorem in its own right.
- **P(counterexample):** genuinely unknown, but this is the only route whose
  mechanism has actually produced counterexamples (in `n >= 3`, five weeks ago).
- **Why it is not rank 1:** it may simply reproduce the degenerate stratum again,
  as the quadratic case did.

### 3. Above 125, ranked by cheapness rather than by degree — medium-low
### probability, medium cost

Theorem 2.1 constrains nothing at or above 125, and the campaign's enumeration
artifacts for that region are lost. The user's instinct is right: **do not
assume the smallest degree is easiest.** Rank candidate pairs by

- support count (this is what actually drives solver cost),
- number of Newton-polygon *vertices* (fewer vertices = fewer nonvanishing
  constraints = a larger solution locus, exactly as sub-case (2) is easier than
  sub-case (1)),
- the exponent `k` in `[P,Q] = x^k` (larger `k` concentrates the ramification,
  which by the corrected Riemann–Hurwitz identity changes the fibre topology),
- `gcd(m,n)`, via the perfect-power filter (`A` must be an `(m/g)`-th power),
  which needs only the polygon.

- **Cost:** medium — the enumeration must be rebuilt before anything is solved.
- **Delivers:** a ranked target list, which the campaign has never had. Every
  target to date was inherited, not chosen.
- **P(counterexample):** unknown but over a far larger space than (8,28).

---

## Critical audit checklist (item 6) — binding before any claim

1. `{P,Q} - x^2 == 0` exactly over `Q` **and** at two large primes.
2. All six Newton vertices nonzero — `q_21_12` is now automatic given
   `p_14_8 != 0` (`FABLE_XCOLUMN.md`), the other five must be checked.
3. `N(P)`, `N(Q)` exactly the target polygons — no vertex lost, nothing outside.
4. **Polynomiality after the Laurent chain.** GGHV's `phi(x)=x^{-1}, phi(y)=x^3y`
   is an automorphism of `K[x,x^{-1},y]` and **not** of `K[x,y]`. A point of the
   pentagon is a point in `L(1)`; converting it to a genuine degree-(72,108)
   counterexample requires inverting `psi_1, psi_2, psi_3, phi` and proving the
   result is polynomial. **This derivation does not exist and is load-bearing.**
5. **No hidden division.** Log every parameter ever appearing in a denominator
   and fork `u = 0` versus saturate `u != 0`. The campaign lost the `g9_8 = 0`
   chart to exactly this.
6. **No properness assumption.** The July 2026 counterexamples are non-proper by
   construction; any argument assuming places at infinity map to infinity —
   including my own retracted Riemann–Hurwitz bound — excludes precisely the
   configurations where counterexamples live.

Items 1–3 are implemented and controlled in `fable_xcol/verify.py`. Items 4–6
are open.

---

## Status

No counterexample. Pentagon and sub-case (2): **NO VERDICT**. The one new hard
result this round is negative but load-bearing: **the degenerate families are a
first-order dead end for the pentagon**, which redirects effort away from local
search and toward strategies 1 and 2.
