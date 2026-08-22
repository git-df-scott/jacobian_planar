# New leads — thinking from different starting points

Written after the pentagon work, deliberately *not* continuing it.  Ranked by
what I think the honest expected value is, not by how attractive they sound.

---

## L1. Audit the exclusions, not the survivor  [my top pick]

Forty sessions have hammered `(72,108)` and produced no witness.  That pair is
"the sole survivor below 125" — but **every step that made it the sole survivor
rests on results this campaign has never re-derived:**

| exclusion | status in the campaign's own ledger |
|---|---|
| GGHV's `max < 125` bound | assumed |
| GGHV Cor 5.7, the `(9,27)` kill | *"never re-derived by anyone"* (`AUDIT_EOD.md` §9) |
| Nguyen 104 | *"trusted refereed, never re-derived here"* (§4.8) |
| `[5]`'s `A'_t = (1,0)` | *"assumed ... unprinted"* |

Last night I took one unverified campaign claim — "the gauge `p_1_0 - 1` makes
the system rigid" — and it was **wrong**, which invalidated the reading of about
a dozen hours of compute.  That claim was internal and load-bearing.  The four
above are external, load-bearing, and unchecked.

**The asymmetry is the point.**  Disproving a *survivor* claim costs the campaign
sessions.  Disproving an *exclusion* **adds search space** — it hands back
degree pairs that were removed from consideration on someone else's authority.
Given a 40-session drought, the probability that the counterexample is in the
searched region is now visibly low, and the cheapest way to change that is to
check whether the region was drawn correctly.

This also inverts the campaign's posture, which has been forty sessions of
trying to prove things empty.  The productive move may be to try to prove an
*emptiness claim wrong*.

**Live already:** Cor 5.7 is under direct computational test (the `p108` sliver
shapes) and those runs are TIMEOUTs, i.e. undecided.  A non-empty there means
GGHV Sec 5 has an error inside the surviving pair's own case.

---

## L2. The pentagon system never encodes non-injectivity at all

The 66 conditions are Newton-polygon and valuation data.  **Nowhere do they say
the map is not injective** — which is the entire property a counterexample must
have.  That is precisely why `P = x + y` satisfies all 66, and why a 7-parameter
degenerate locus does.

Every system in this campaign is of that shape: necessary conditions on
polygon data, with the defining property checked only *afterwards*, on candidates
that never arrive.

**The move:** carry the defining property *into* the system rather than checking
for it later — a collision `F(a) = F(b)` with `a != b` (Rabinowitsch on a
coordinate difference), or the full Keller condition on the original map, as
extra equations.  Extra equations **shrink** the variety, which is the direction
you want when the current variety is full of junk.

**Caveat, stated because it matters:** the pentagon's `(P,Q)` are the reduced
polygon data of a hypothetical counterexample, not the counterexample map
itself, so a collision condition has to be transported through that reduction
rather than written down naively.  Doing that transport correctly is the work.

---

## L3. The Dixmier route, which shares my leading relation

`JC2 <=> DC1` (Tsuchimoto; Belov-Kanel–Kontsevich): a counterexample to the
Dixmier conjecture for the Weyl algebra `A_1` gives a counterexample to plane JC.
`BIFURCATION.md` logs this as an alternate and never pursued it.

**What is new is that last night's work connects them.**  For `[P,Q] = 1` in
`A_1` with Bernstein degrees `m, n`, the symbol map gives
`{sigma(P), sigma(Q)} = 0` once `m+n-2 > 0`, hence

    sigma(Q)^m = c sigma(P)^n

— **exactly the leading-coefficient relation I derived for `{P,Q} = x^2`**.  So
the pentagon's combinatorics *is* the Dixmier combinatorics, seen commutatively.

Two consequences worth something:
- every polygon/valuation tool built here transfers to `A_1` unchanged;
- the noncommutative side carries **strictly more rigidity** — the full identity
  `[P,Q] = 1`, not just its symbol — so branches that survive commutatively may
  die there.  Rigidity is what this search has been short of.

---

## L4. Tail saturation — the cheapest large payoff

`CROSSDOOR.md` §5 records that reduced systems depend only on the **chain tail**,
with a predictor `(last-2-segments, shape index) -> system hash` showing **zero
violations across every system ever generated** (16 groups, 34 chains -> 26
tails).  The conjecture is that the tail set *saturates* as degree grows.

If true, the 429-case (and 804-pair) above-125 frontier collapses to **finitely
many tail-systems, most already decided**, and the chain-compiler extension only
needs each case's tail rather than its full chain.

**Never tested.**  The test is cheap and well-defined: extend the compiler on ~20
sample cases above 150 and count new tails versus reused.  This matters more
than it looks, because of L6.

---

## L5. The cover-degree family, and what happens at k = 0

`{P,Q} = x^k` means, with `s = x^{k+1}/(k+1)`, `det J_(s,y)(P,Q) = 1`: a Keller
map on the **(k+1)-fold cyclic cover**.  Plane JC is exactly `k = 0`.

I found explicit solution families at `k = 2` last night.  So solutions exist for
`k >= 1` and are conjectured not to for `k = 0`.  **The transition is a handle
nobody has used**: what breaks as `k -> 0`?  If the mechanism that kills `k = 0`
is visible, it is a proof strategy; if it is *not* visible, that is evidence the
plane case is not as different as assumed, and says where to look.

---

## L6. Degree is unbounded upstairs — why is the plane search degree-bounded?

Gao (`arXiv:2608.00222`) produces counterexamples in every dimension `> 2` of
**arbitrarily large geometric degree**.  The plane search here is bounded at 125
by *machinery*, not by theory — the classification simply stops there.

If the plane counterexample has large geometric degree, **every below-125 search
is looking in the wrong place by construction**, and forty sessions of EMPTY are
exactly what that would produce.  L4 is the cheap way to make above-125
tractable, and L1 is the cheap way to find out whether the boundary was even
drawn in the right place.

---

## How these differ from what has been tried

The campaign's whole method has been: *fix a degree pair, derive necessary
polygon conditions, try to prove them unsatisfiable.*  Every lead above steps
outside that loop —

- L1 attacks the boundary of the search region instead of its interior;
- L2 puts the defining property into the system instead of checking it after;
- L3 changes the category, to one with more rigidity;
- L4/L6 attack the region the machinery cannot currently reach;
- L5 studies the family the problem sits in rather than the problem.
