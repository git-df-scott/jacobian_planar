# Chain data → reduced polygon pair: the map, derived and validated

`ABOVE_125_STATUS.md` recorded this as *"not started, and deliberately not
faked"* — the blocker being that GGHV §4's reduction "does not pattern-match
from the two published examples". It is now derived from the definitions and
validated against **every** reduced pair the papers print (6/6), not fitted to
two of them.

## Sources

Both papers are held locally as full text; line numbers are cited in
`trackD_chain_map.py`'s docstring.

| ref | paper | what is used |
|---|---|---|
| [C] | arXiv:1708.07936, *Some algorithms related to the Jacobian Conjecture* | Thm 2.20 (the chain attached to a standard `(m,n)`-pair); §5 (the 17 length-1 + 7 length-2 **families**, each printed as `A₀, A'₀, A₁[, A'₁, A₂], k, m(j), n(j)`); §6 (the 34 shapes with max ≤ 150) |
| [G] | arXiv:2204.14178, *Increasing the degree … from 100 to 108* | §4 *Reducing the size of the Newton polygon*: Prop 4.1 (9,27), Prop 4.2 (9,24), Prop 4.3 (8,28) |

## What Theorem 2.20 pins down

`A₀ = (1/m) en₁,₀(P)`, `A'ᵢ = (1/m) st_{ρᵢ,σᵢ}(P)`, and `A_{i+1} = A'ᵢ` at
type-II.a corners. Points print as `(a∣l, b)` = `(a/l, b)`, and by item (13)
the corners with `l = 1` are **exactly** the regular corners of `(P,Q)`. So
the pre-reduction base polygon is

```
B = conv{ (0,0), A'_t, A_t, …, A₀, (0, c) }
```

with `N(P) = m·B`, `N(Q) = n·B`. This already gives the degree pair
`(m·v₁₁(A₀), n·v₁₁(A₀))`, which **agrees with [C] §6's own max column on all
34 rows** — an independent check that the chain table is transcribed correctly.

## What §4 does, and where the bracket exponent comes from

The reduction is `φ₁: x ↔ y`, then shears `φ(y) = y + λx^{σ/ρ}` that cut an
edge whose leading form is a power of `(x^a y^b − λ)`, then a monomial twist

```
ϕ(x) = x⁻¹,   ϕ(y) = x^{c_t} y
```

— an automorphism of `L⁽¹⁾ = K[x, x⁻¹, y]` but not of `K[x,y]`. Shears are
volume preserving and the swap contributes `−1`, so with
`[ϕ(P),ϕ(Q)] = ϕ([P,Q])·[ϕ(x),ϕ(y)]` and `[x⁻¹, x^{c_t}y] = −x^{c_t−2}`:

> **`r = c_t − 2`.** The bracket right-hand side `x^r` is *not* a free choice.

Tracking where `ϕ` sends the swapped top corner gives `c_t = (a + b_t)/a_t`,
where `A_t = (a_t, b_t)` is the last chain corner with `l = 1`. This
reproduces `[P,Q] = x, x, x²` for (9,27), (9,24), (8,28) — matching Props 4.1,
4.2, 4.3 exactly.

## The map

Chain `A₀, …, A_{j+1}`, `Aᵢ = (aᵢ/lᵢ, bᵢ)`; `A_t` = last corner with `l = 1`;
`A'_t = (a', 0)` the last lower corner.

```
a  = l_{j+1}                      b  = b_{j+1} + 1
B' = {(0,0), (a, b−1), (a, b), (0, c′)}
(m′, n′) = sorted(m, n)
N(P) = conv(m′B′ ∪ {ε_P})         N(Q) = conv(n′B′ ∪ {ε_Q})
{ε_P, ε_Q} = {(1,0), (r,1)}       r = (a + b_t)/a_t − 2
c′ ∈ { c_pre, c_pre − a, c_pre − 2a, … ≥ 0 },  c_pre = b₀ − (q−1)a₀,  q = b_t/(a_t − a′)
```

The `c′` ladder is precisely what produces Prop 4.2's **three** cases and Prop
4.3's **two**.

## The ε invariant is a consequence, not an axiom

Write `P = p₀₀ + y P₁(x) + O(y²)` and `Q = q₀₀ + q_{k0}x^k + y Q₁(x) + O(y²)`.
The `y⁰` part of `[P,Q]` is `−k q_{k0} x^{k−1} P₁(x)`, so the surviving
monomial sits at `(i_P + i_Q − 1, 0)` and `[P,Q] = x^r` forces

> **`ε_P + ε_Q = (r+1, 1)`.**

Every emitted shape satisfies it by construction; `check_eps()` re-derives it
*from the emitted polygons* so a construction bug cannot pass, and it also
enforces the row-0 shape the y-adic engine needs (one polygon's `j=0` row
exactly `{(0,0),(1,0)}`, the other's exactly `{(0,0)}`).

## Validation

| check | result |
|---|---|
| Prop 4.1 (9,27) | reproduced exactly, `(a,b,c′,r) = (3,9,9,1)` |
| Prop 4.2 cases (1)(2)(3) — (9,24) | reproduced exactly, `c′ = 6, 3, 0`, `r = 1` |
| Prop 4.3 cases (1)(2) — (8,28) | reproduced exactly, `c′ = 4, 0`, `r = 2` |
| degree pairs vs [C] §6 max column | all 34 rows agree |
| engine regression on the 3 hand-entered shapes | 61/110/60/1, 25/188/24/1, 172/103/103/69 — unchanged |
| F22 | falls out as *"twist does not close"* — independently the family [C] discards in its own Prop 6.1 |

**Honest limit.** All six published pairs come from only two `(a,b)`
configurations, `(3,9)` and `(4,8)`. The rules could still be incomplete for
other configurations. That is why chains whose rules fail to close (non-integer
`c_t`, unknown `A'_t`, `ε` absorbed into the base) are **not** reported as
discarded: they are re-run in *superset mode* with `r` and `c′` enumerated over
bounded ranges. A missed shape costs a counterexample; a spurious shape costs
one machine run.

## Pipeline result

866 ε-passing shapes (134 from the derived rules, 732 from superset mode for
the 8 chains that did not close), each run through the y-adic recursion and the
exact dual-number Jacobian.

`dim_bound = 1` is the **baseline, not a survival**: the `p₀₀` Jacobian column
is identically zero in every shape (adding a constant to `P` changes no
bracket), and both open (8,28) cases sit at exactly 1. Only `≥ 2` means the
polygon conditions left real freedom.

Over the 572 runs completed at the time of writing (sorted by size, so the
largest shapes were still queued):

- **21 of 34 chains have every shape cut to `dim ≤ 1`** — the same strength as
  the two open (8,28) cases, i.e. finitely many points modulo the additive
  constant. These are ready for the elimination machinery that closed case (2).
- 13 chains have at least one loose shape. The genuinely weak ones are
  `F1(3,4)` and `(8,28)/(7/4,3)(3,4)` (dim 13–14, identical because both have
  terminal corner `(7/4,3)` and the same sorted `(m,n)` — a consistency check),
  and `F1(5,7)` (dim 26–27). These sit where `(9,27)` sits (dim 69): the
  polygons alone are not enough, exactly as GGHV's own §5 needed more than the
  polygons to close `(9,27)`.
- On the **≥ 125 frontier**: 470 of 492 runs at `dim ≤ 1`, 22 loose.

**No counterexample.** What changed is that the frontier is now mapped rather
than blocked: every one of the 34 shapes has explicit coordinates, and most are
reduced to finite point sets awaiting the same Gröbner/elimination pass that
decided (8,28) case (2).

## Files

| file | role |
|---|---|
| `trackD_chain_map.py` | chain tables, the map, `check_eps`, `validate()` |
| `trackD_pipeline.py` | chain → ε filter → y-adic + dual-number Jacobian |
| `trackD_summary.py` | triage table from `trackD_results.json` |
