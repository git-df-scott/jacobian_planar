# A topological constraint on the pentagon nobody has computed

> # ⚠ RETRACTION NOTICE (2026-08-23)
> The unqualified conclusions below (`D <= 17`, "P must be Newton-degenerate",
> the `2g + s <= 17` kill criterion, and the `D = 1` rigidity of sub-case (2))
> **assume properness** — that every place at infinity of `F_c` maps to infinity
> under `Q`. The Jacobian conjecture counterexamples announced in July 2026
> (arXiv:2608.00222) work by **violating exactly that hypothesis**: they are
> everywhere unramified but not proper, and injectivity fails only through
> points escaping to infinity. So this identity is valid **only on the proper
> locus, which is precisely where counterexamples do not live.**
> See `FABLE_STATE_OF_THE_ART.md`. Re-derive before using.


Fable, 2026-08-22. Code: `fable_xcol/rh.py` (controls included and passing).

Every instrument in this campaign is algebraic: Gröbner bases, rank tests,
level ladders. **Nobody has computed the topology of the fibration.** Doing so
takes about ten lines and yields a necessary condition that is completely
independent of every ladder, chart and gate.

## The identity

`{P,Q} = x^2` says `dP ∧ dQ = x^2 dx ∧ dy`. Restrict to a generic fibre
`F_c = {P = c}`: there `dP = 0`, so `dQ|_{F_c}` vanishes **exactly** on
`F_c ∩ {x = 0}`, and to order 2. So `Q|_{F_c} : F_c -> C` is ramified exactly
there, with ramification index 3 at each such point.

Compactify: `Q` extends to `Qbar : Fbar_c -> P^1` of degree `D` (the
topological degree of `Phi = (P,Q)`), with the `s` places at infinity going to
infinity. Riemann–Hurwitz:

    2 - 2g = 2D - [ramification over C] - [ramification over infinity]
           = 2D - 2 * #(F_c ∩ {x=0}) - (D - s)

and since `chi(F_c) = 2 - 2g - s`, everything collapses to

    **chi(F_c)  =  D  -  2 * deg(a_0)** ,     a_0(y) := P(0,y)

## Controls (both pass exactly)

| pair | `{P,Q}` | `deg a_0` | `D` | predicted `chi` | actual fibre | `chi` |
|---|---|---|---|---|---|---|
| `P = x^3/3 + y,   Q = y` | `x^2` | 1 | 3 | **1**  | graph `y = c - x^3/3` ≅ `C` | **1** |
| `P = x^3/3 + y^2, Q = y` | `x^2` | 2 | 3 | **-1** | elliptic curve minus 1 point | **-1** |

Two independent nontrivial checks, exact agreement. The identity is sound.

## Applied to the pentagon

`deg a_0 = 8` exactly, because `p_8_0 != 0` is one of the six mutable vertices.
So

    **chi(F_c) = D - 16.**

Now compare against what the Newton polygon predicts for a **nondegenerate**
`P`. With `2*Area(N(P)) = 94`:

    fibre inside the torus      chi = -94
    plus F_c ∩ {x=0}: a_0(y)=c has 8 roots          +8
    plus F_c ∩ {y=0}: P(x,0) = x (the vertex (1,0))  +1
    -------------------------------------------------
    chi(F_c) = -85   =>   D = chi + 16 = -69   <  0

**Impossible.** A topological degree cannot be negative. Therefore:

> **THEOREM (necessary condition).** Any pentagon solution has `P` **Newton-
> degenerate**: some face polynomial of `N(P)` has a critical point in the torus.

This is consistent with — and independently re-derives — the campaign's edge
results: `a_8 = alpha W^2` is a perfect square, i.e. the right vertical edge
polynomial has a double root. That *is* Newton degeneracy. Two unrelated routes
to the same structural fact.

## The quantitative version — and a kill criterion

`D >= 1` forces

    **chi(F_c) >= -15** ,  i.e.  **2g + s <= 17**  for the generic fibre,

against `2g + s = 87` in the nondegenerate case. The generic fibre of `P` must
be *enormously* more degenerate than a curve with that Newton polygon generically
is — its geometric genus plus punctures must drop by 70.

### The sharpest form: **D <= 17**

Run the identity the other way. `F_c` is a connected affine curve, so
`chi(F_c) <= 1` (with equality iff `F_c ≅ C`; `chi = 0` iff `F_c ≅ C*`).
Since `chi(F_c) = D - 16`,

    **D <= 17** — the topological degree of the pentagon map is at most 17.

and the two classically expected fibre types pin it exactly:

    F_c ≅ C   (chi = 1)  =>  **D = 17**
    F_c ≅ C*  (chi = 0)  =>  **D = 16**

Worth flagging: GGV's admissible-`B` list is `{16} ∪ {20+}`, and 16 falls out
here from pure topology. That may be a coincidence; it may not, and it is
cheap to find out. For comparison the BKK bound is `MV(N(P), N(Q)) = 141`, so
topology is roughly **eight times sharper than Bezout/BKK** on this map.

Any independent computation of `D` that returns a value above 17 — from the
polygon, from the fibration, or from a resultant — is an immediate **EMPTY**
for the pentagon.

That gives a concrete, cheap, solver-free kill criterion:

> Compute the maximum `chi(F_c)` achievable subject to the *forced* edge
> structure (`a_8 = alpha y^7(y-r))^2`, `b_12 = beta (y^7(y-r))^3`, the six
> nonzero vertices, and the rung 19/17/15/13 conditions). If that maximum is
> `< -15`, **the pentagon is EMPTY** — with no Gröbner basis, no chart, no
> branch, and no dependence on any descent.

Concretely: the degeneracy budget is the sum of delta-invariants of the
singularities forced on `Fbar_c` plus the drop in the number of places at
infinity. Each is computable from the edge data by standard toric/Puiseux
methods. This is a genus-drop bookkeeping problem, not a computation that can
OOM.

## Why this is worth doing before anything else

- It is **independent of every existing instrument**. It cannot inherit the
  deleted-stratum bug, the `g8_6 = g8_7 = 0` inheritance, the `z = s - tau`
  reduction, or any chart or branch choice. If it fires, it kills the pentagon
  outright, in all charts at once.
- It is **cheap** — hours of careful bookkeeping, no solver.
- It **transfers**: the same identity applied to a general admissible degree
  pair `(m,n)` gives `chi(F_c) = D - 2 deg a_0` with `deg a_0` read off the
  polygon. That is a **new degree-pair filter**, and unlike the perfect-power
  filter it constrains the *interior*, not just the edges. It is directly
  applicable to the 804 pairs above 125 (task D3) and needs no `L`.
- If instead the bookkeeping shows `chi >= -15` is *achievable*, it tells us
  the exact genus and puncture count of the fibre a counterexample must have —
  which is a **construction blueprint**, far more specific than anything the
  campaign currently has.

## Caveats, stated honestly

- The derivation assumes the generic fibre is irreducible and that all places
  at infinity map to infinity under `Q`. Both are generic expectations and both
  hold in the controls, but for a rigorous kill each needs a proof for the
  pentagon (a reducible generic fibre would mean `P` is a composite, which is
  its own strong structural statement and worth chasing either way).
- `D >= 1` is all I use. Sharper input (`D >= 2`, since `D = 1` plus Keller
  would force an automorphism) tightens the bound to `chi >= -14`.
- Nothing here produces a counterexample, and nothing here is an emptiness
  verdict yet. Pentagon remains **NO VERDICT**.
