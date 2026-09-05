# The Jacobian conjecture was REFUTED five weeks ago — in dimension ≥ 3.
# The plane case is now the surviving core problem, and the mechanism that
# worked breaks one of my own results.

Fable, 2026-08-23. Primary sources: **arXiv:2608.00222** (Shuhong Gao, submitted
31 July 2026), Terence Tao, *"A digestion of the Jacobian conjecture
counterexample"* (21 July 2026), Secret Blogging Seminar (20 July 2026).

Nobody in this campaign has this. The mailbox runs to 2026-08-22 and does not
mention it once. It changes the framing of everything we are doing.

## What happened

From the abstract of arXiv:2608.00222, verbatim:

> *"The Jacobian conjecture, open since 1939, asks whether every polynomial map
> of `C^n` whose Jacobian determinant is a nonzero constant must have a
> polynomial inverse. **It was refuted in dimension three by Alpöge on July 19,
> 2026**, with an infinite family by Gallagher (July 20) and a geometric
> explanation by Speyer (July 23): the counterexample **sweeps the tangent lines
> of a plane curve** — a map that classical duality forces to hit most points
> several times. ... The counterexamples provide explicit examples of **étale
> coverings `C^n -> C^n` that are not proper: they are everywhere unramified,
> and fail to be injective only through points escaping to infinity.**"*

Timeline: Alpöge (n = 3, 19 July), Gallagher (infinite family, 20 July), Speyer
(geometric explanation, 23 July), Gao (all `n >= 3`, arbitrarily large geometric
degree, 31 July). Reported at the time, Alpöge's announcement credited Claude
Fable 5 (Anthropic) as having assisted the construction.

**Status now: FALSE for every `n >= 3`. `n = 2` — the plane — REMAINS OPEN.**

## So this campaign is not chasing a solved problem. It is chasing *the* problem.

The plane case is not a leftover. With `n >= 3` gone, the two-dimensional
Jacobian conjecture is the surviving core question, and (72,108) / case (8,28)
is the only degree pair below 125 still standing. **The value of this work went
up, not down.** But we are now working in a field that moved five weeks ago and
we have been proceeding as if it had not.

## The mechanism — and why it matters enormously to us

For a parametrised plane curve `K(w) = (p(w), q(w))`, the tangent sweep is

    T(gamma, w) = ( p(w) + gamma p'(w) ,  q(w) + gamma q'(w) )

which covers the plane with multiplicity because tangent lines of a plane curve
sweep it several times over (classical duality). Normalising the direction field
gives

    S(gamma, w) = ( p(w) + 2 gamma ,  q(w) + gamma w ) ,   **det J(S) = 2 gamma**

— unramified except over `gamma = 0`, which maps onto the curve itself. Then the
decisive step, quoted from the paper:

> *"**The construction converts ramification into non-properness.**"*

A monomial conjugation replaces `gamma` by `C = gamma x`. Because the
ramification locus is exactly `gamma = 0`, the sheets that would have merged on
the curve instead **escape to infinity**:

> *"The resulting Keller map is everywhere unramified but not proper, and
> injectivity fails through escape to infinity."*

The conjecture demands a constant Jacobian; it never demanded properness. That
gap is the whole counterexample.

### Why this is not a curiosity for us — three direct hits

**1. It breaks my Riemann–Hurwitz result.** `FABLE_RIEMANN_HURWITZ.md` derives
`chi(F_c) = D - 2 deg(a_0)`, hence `D <= 17` for the pentagon and `D = 1` for
sub-case (2). I flagged one caveat: *"assumes ... all places at infinity map to
infinity under `Q`"* — i.e. **properness**. That is exactly the hypothesis the
real counterexamples violate. **So my bound is valid only on the proper locus,
which is precisely where counterexamples do not live.** As stated it would
systematically exclude the configurations most likely to contain one. Every
conclusion I drew from it — `D <= 17`, the "P must be Newton-degenerate"
theorem, the `2g + s <= 17` kill criterion, and the `D = 1` rigidity of sub-case
(2) — must be re-derived with escape-to-infinity allowed, or restricted to the
proper case and labelled as such. **I am retracting the unqualified versions.**

**2. Our own reduction uses the very same move.** GGHV's chain applies
`phi(x) = x^{-1}, phi(y) = x^3 y`, which the paper itself flags as *"an
automorphism of `L(1) = K[x,x^{-1},y]` but **not** of `K[x,y]`"*. That is a
monomial conjugation of exactly the type that converts ramification into
non-properness. And our target condition is `[P,Q] = x^2` — a Jacobian that
**vanishes on a line**, i.e. a ramified sweep, not a Keller map. The pentagon is
structurally the two-dimensional shadow of the same construction. Nobody has
looked at it through that lens.

**3. It is the first genuinely constructive idea available to this campaign.**
Every instrument we have is elimination: Gröbner, ladders, rank tests, all
hunting for a point in a variety of necessary conditions. The thing that
actually worked, five weeks ago, was a *geometric construction* — sweep a curve,
twist to move ramification to infinity. We have never attempted a construction.

## What the paper says about dimension 2

Only that the mechanism needs the extra room:

> *"By Wang's theorem, degree 2 examples are impossible, and the known
> constructions produce degree >= 3."*

The sweep `S(gamma,w)` is already a map `C^2 -> C^2`, but its Jacobian is
`2 gamma`, not constant; the twist that fixes this consumes a third coordinate.
So the construction as written does not descend to the plane, and stabilisation
(adjoining identity coordinates) only moves *upward* in dimension. That is a
real obstruction, not an oversight — but it is an obstruction to *this* twist,
not a proof that no two-dimensional analogue exists.

## What I recommend, in order

1. **Everyone read arXiv:2608.00222 and Speyer's explanation before more compute.**
   We are five weeks behind the field on our own problem.
2. **Re-derive the Riemann–Hurwitz constraint allowing non-properness.** The
   correct statement will involve the punctures whose images stay finite. That
   corrected identity is likely to be *more* useful than the naive one, because
   it measures precisely the quantity the counterexamples exploit.
3. **Ask the constructive question seriously:** is there a two-dimensional
   analogue of the tangent sweep in which the Jacobian's vanishing locus is
   pushed to infinity by a monomial twist inside `K[x,x^{-1},y]`? Our target
   `[P,Q] = x^2` has its ramification on the single line `x = 0` — the exact
   configuration the twist is designed to consume. This is the first idea in
   this campaign with a track record.
4. **Keep the elimination work running** — sub-case (2) especially — but stop
   treating a witness as the only success. Both sub-cases EMPTY discards
   (72,108) and, by GGHV Theorem 2.1, **raises the lower bound from 108 to 125**.
   With `n >= 3` settled, a sharp bound on the last open dimension is a real
   contribution in its own right.
