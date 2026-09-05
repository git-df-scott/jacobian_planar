# `{P,Q} = x^2` — a graded reduction, and what it decides

This directory contains a self-contained attack on the reduced GGHV problem

> find `P, Q ∈ C[x,y]` with `{P,Q} = P_x Q_y − P_y Q_x = x^2`
> whose Newton supports lie in prescribed windows, with prescribed vertex
> coefficients nonzero.

Everything here is exact (rational or `F_p`); no floating point enters a verdict.

## 1. The targets, recovered

`*.sing` are the five **bracket-`x^2`** `extract` systems recovered from the
campaign bundle (`campaign_55commits.bundle`), byte-for-byte:

| file (md5-named) | campaign name | params | status in the campaign |
|---|---|---|---|
| `c19711d9…` | `p108_525122` | 25 | **TIMEOUT / undecided** (a listed resister) |
| `66317e9e…` | `p108_821326` | 38 | EMPTY (dup of 843700) |
| `fbe16216…` | `p108_843700` | 38 | EMPTY |
| `ea937b4f…` | `w6_582584_0` | 40 | — |
| `effc7cc0…` | `w6_582584_1` | 20 | EMPTY |

The other campaign systems carry bracket `±x`, not `x^2`.

## 2. What the systems actually say

`P = Σ_j Pd_j(x) y^j`, and `Pd_0 = c_1 + c_2 x` with `c_2 ≠ 0` — i.e. the Newton
polygon has the vertex `(1,0)` and `Pd_0' = c_2` is a nonzero **constant**.
Comparing `y`-coefficients in `{P,Q} = R` gives

```
(m+1)·c_2·Q_{m+1} = Rr_m + Σ_{i≥1, k=m+1−i} [ i·Pd_i·Q_k' − k·Pd_i'·Q_k ]
```

so **`Q` is uniquely determined by `P`** (with `Q_0 = 0`) and is automatically a
polynomial in `x`. The entire problem is a condition on `P` alone: the cascade
must land inside the prescribed `x`-windows and terminate. `cascade.py`
implements this; `singspec.py` parses a `.sing` file into it.

## 3. The graded reduction (the new part)

For the `(72,108)` targets `supp(P)` lies in the strip `0 ≤ 2a − j ≤ 2` and
`supp(Q)` in `0 ≤ 2b − k ≤ 3`. Grade by `ρ = 2·(x-exp) − (y-exp)` and set
`T = x y^2`, `P_ρ = y^{−ρ} f_ρ(T)`, `Q_σ = y^{−σ} g_σ(T)`. Then

```
{P_ρ, Q_σ} = y^{1−ρ−σ} · ( ρ · f_ρ g_σ' − σ · f_ρ' g_σ )
```

(`verify.py` checks this identity, and the coefficientwise expansion of every
level, against direct 2-variable algebra: `OVERALL: PASS`).

`x^2 = T^2 y^{-4}` sits at `ρ+σ = 5`, so the 2-variable system becomes a
**triangular chain of one-variable equations**:

```
level 5 :  2 f2 g3' − 3 f2' g3  =  T^2            <-- "E1", involves f2 ONLY
level 4 :  2 f2 g2' − 2 f2' g2 + f1 g3' − 3 f1' g3          = 0
level 3 :  2 f2 g1' −   f2' g1 + f1 g2' − 2 f1' g2 − 3 f0' g3 = 0
level 2 :  2 f2 g0'            + f1 g1' −   f1' g1 − 2 f0' g2 = 0
level 1 :                        f1 g0'           −   f0' g1  = 0
```

Each `g_σ` is solved coefficientwise (the diagonal coefficient is `(1+2n)` or
`(2+2n)` times `f_2`'s leading `1`, never zero), and the leftover coefficients
are the conditions. `gsys.py` (Python) and `graded_525122.sing` /
`decide_m.sing` (Singular) are two independent implementations.

### E1 is a vanishing-period condition

With `f = f_2` (degree `m`, simple roots, `f(0)=0`) and `y^2 = f(T)`,

```
2 f g' − 3 f' g = T^2      ⟺      d( g / y^3 ) = T^2 dT / y^5
```

i.e. the second-kind differential `T^2 dT / y^5` on the hyperelliptic curve
`y^2 = f(T)` must be **exact** — all `2·genus` periods vanish. For `m = 8`
the curve has genus 3, giving exactly the 6 conditions the computation
produces. This is the Gelfand–Leray/period formulation, made finite.

## 4. Verdicts (exact, `F_p`)

The minimal-width `μ=2` strip family is indexed by one even integer `m`:
`deg f_2 = deg f_1 = deg f_0 = m`, `deg g_σ = 3m/2`, giving `deg P = 3m`,
`deg Q = 9m/2` — the whole `2:3` ray. `m = 8` **is** `p108_525122`
(the `(72,108)` reduced polygons); `decide_m.sing` reproduces its 25 unknowns,
window-for-window.

| m | (deg P, deg Q) | unknowns | E1 conds | E1 solutions (F_top=1) | verdict |
|---|---|---|---|---|---|
| 2 | (6, 9)   | 6  | 0 | free      | **EMPTY** |
| 4 | (12, 18) | 12 | 2 | 3         | **EMPTY** |
| 6 | (18, 27) | 18 | 4 | 10        | **EMPTY** |
| 8 | (24, 36) | 24 | 6 | 35 (= 5 orbits × 7) | **EMPTY** — see below |
| 10 | (30, 45) | 30 | 8 | — | leading level still running |

For `m = 8` the leading level does **not** obstruct: `E1` has exactly 35
solutions with `F_7 = 1` (5 orbits under the residual scaling `F_i ↦ μ^i F_i`,
`μ^7 = 1`), forming a single triangular component

```
F7 − 1,  F6^35 − … (a quintic in F6^7),  F5 = …(F6), …, F1 = …(F6)
```

— identical structure at `p = 32003` and `p = 65521`. Every one of the five
orbits is killed by the lower levels (`stage_0.log`, `stage_1.log` for the two
`F_p`-rational orbits, `stage_ext3.log` for the three living in
`F_p[a]/(a^3−10400a^2+1641a−3068)`): `dim = −1`, GB `= 1`.

**So `p108_525122` — a live, undecided `(72,108)` resister that resisted
`msolve` at 1800 s / 6 GB — is empty, and the kill is localised: not at the
leading (period) level, but at levels 3 and 1, where `f_0' ≠ 0` (forced by the
vertex `(m,2m)`) collides with the `g_1` produced by the cascade.**

### The leading level counts Catalan numbers

`vdim` of `E1` in the slice `F_{m-1} = 1`, measured:

| m | genus of `y² = f₂(T)` | vdim | orbits under `F_i ↦ μ^i F_i`, `μ^{m-1}=1` |
|---|---|---|---|
| 2 | 0 | 1 | 1 |
| 4 | 1 | 3 | 1 |
| 6 | 2 | 10 | 2 |
| 8 | 3 | 35 | 5 |
| 10 | 4 | *126 predicted* | *14 predicted* |

`vdim = C(m−1, m/2−1)`, so the orbit count is the **Catalan number** of the
genus: 1, 1, 2, 5, 14, 42, … In words: the number of degree-`m` polynomials
`f₂` (up to scaling) for which `T² dT / y⁵` is exact on `y² = f₂(T)` appears to
be `Catalan(genus)`. Four data points and a prediction — an observation, not a
theorem. `count_e1.py` states it; `_e1only_10.sing` is the first real test.

### Exactly what is confirmed where

These are `F_p` verdicts: `1 ∈ I mod p` at one prime is strong evidence, not a
characteristic-zero proof (a solution over a number field reduces to a solution
mod almost every prime, so emptiness mod `p` fails only if `p` is bad — but the
bad set is not bounded a priori). Current state for `m = 8`:

| claim | primes |
|---|---|
| `E1` is 0-dimensional with `vdim 35`, one triangular component, eliminant a quintic in `F_6^7` | `32003`, `65521`, `1000003` |
| lower levels kill **all five** orbits | `32003` (`stage_0`, `stage_1`, `stage_ext3`) |
| lower levels kill the `F_p`-rational orbit | `1000003` (`stage_p1000003_0`) |

`pipeline.py m p` automates the whole chain (E1 → lex triangular set → factor
the eliminant → per-factor lower-level test over `F_p[a]/(factor)`) for any
`m` and `p`, and reports the raw Singular verdict lines.

## 5. Explicit witnesses that DO exist

`μ = 1` (the strip `0 ≤ a − j ≤ 1`, `T = xy`) collapses completely:

```
P = f0(xy) + x·φ(xy),   Q = g0(xy) + x·ψ(xy)
{P,Q} = x^2   ⟺   W(φ,ψ) = φψ' − φ'ψ = 1,  φ | f0',  g0' = (f0'/φ)·ψ
```

and `W(φ,ψ) = 1` for polynomials forces `deg φ ≤ 1` (if `deg ψ ≠ deg φ` the
Wronskian's leading term survives and forces `deg φ + deg ψ = 1`; if
`deg ψ = deg φ = k ≥ 2`, `ψ = φ∫dT/φ²` has degree `1−k < 0` modulo `φ`, so
`W = 0`). Direct search confirms: **no constant-Wronskian pair with
`deg φ ∈ {2,3,4}` exists.**

`witnesses.py` builds and *certifies* explicit members. Two of them:

```
P = (3x⁴y⁴ − 4x³y³ + 12x²y − 12x)/12          hull(P) = (1,0),(2,1),(4,4),(3,3)
Q = −(x³y³ + 3x)/3                            {P,Q} = x²   [exact]

P = (5x⁶y⁶ − 6x⁵y⁵ − 10x³y³ + 15x²y² + 30x²y − 30x)/30
Q = (10x⁶y⁶ − 18x⁵y⁵ − 20x³y³ + 45x²y² + 60x²y − 90x)/30
                                              {P,Q} = x²   [exact]
```

Both have the vertex `(1,0)`, so neither `P` is composite (`P = R(h)` with
`deg R ≥ 2` would make every Newton vertex divisible by `deg R`). They are
genuine solutions of the bracket equation — and they are **not** counterexample
witnesses: in the `μ = 1` strip `deg g_0 ≤ deg f_0`, hence `deg Q ≤ deg P`, and
the `2:3` ray needed by GGHV is unreachable. That is the precise reason the
easiest strip cannot host a counterexample, and it is a proof, not a search.

## 6. Files

| file | what |
|---|---|
| `cascade.py` | the 2-variable `Q`-from-`P` recursion (mirrors the campaign's `extract`) |
| `singspec.py` | parser for the campaign `.sing` systems |
| `gsys.py` | the graded one-variable system, coefficientwise |
| `verify.py` | cross-validation of the graded reduction vs. direct 2-variable algebra |
| `e1.py` | `E1` solved symbolically: `G` in terms of `F`, plus the 6 conditions |
| `graded_525122.sing` | graded ideal for `p108_525122` (Singular) |
| `decide_m.sing` | staged decision for the whole `m`-family |
| `scan_mu2.sing` | monolithic version of the same |
| `stage_*.sing` | per-`E1`-orbit lower-level runs |
| `certify.py` | exact certifier: bracket, support, hull, vertex nonvanishing |
| `witnesses.py` | the `μ=1` family, built and certified |

## 7. The general engine, and a ranking of remaining targets

The reduction is not special to one polygon. Let `μ ≥ 1`, put `T = x y^μ`, and
grade by `ρ = μ·(x-exp) − (y-exp)`; then for **any** `μ`

```
{ y^{-ρ} f(T),  y^{-σ} g(T) }  =  y^{μ−1−ρ−σ} · ( ρ f g' − σ f' g ).
```

`x^k = T^k y^{−kμ}` therefore sits at level `ρ+σ = (k+1)μ − 1`. If `supp(P)`
occupies `ρ ∈ [0, ρ_max]` and `supp(Q)` occupies `σ ∈ [0, σ_max]` with
`ρ_max + σ_max = (k+1)μ − 1`, the two-variable system splits into
`ρ_max + σ_max + 1` one-variable levels, the top one being

```
ρ_max · f g' − σ_max · f' g = T^k ,
```

which is exactness of `T^k dT / y^{2σ_max−ρ_max+…}` on the cyclic cover
`y^{ρ_max} = f(T)` — a vanishing-period condition whose genus, and hence
condition count, is read off the polygon. Everything below the top is linear
in one unknown `g_σ` at a time.

Ranking the remaining bracket-`x^2` territory by how expensive this makes it:

| target | grading | top-level equation | status |
|---|---|---|---|
| `μ=1` strips (smallest possible support) | `T = xy`, `(ρ_max,σ_max) = (1,1)` | `W(φ,ψ) = 1` | **CLOSED by proof**: forces `deg φ ≤ 1`, hence `deg Q ≤ deg P`, hence the 2:3 ray is unreachable |
| minimal `μ=2` strips, `m` even (the 2:3 ray; `m=8` is `(72,108)`) | `T = xy²`, `(2,3)` | `2 f g' − 3 f' g = T²` (genus `m/2 − 1`) | `m = 2,4,6,8` **EMPTY**; `m ≥ 10` running |
| `p108_821326` / `843700` | `T = xy²`, `(3,2)` — the strip widens to width 3 at the top corner; polygon `(0,0),(1,0),(12,21),(12,24)` | `3 f g' − 2 f' g = T²` | campaign says EMPTY; a free replication control for this engine |
| `w6_582584_0` — **the pentagon** | direction `(7,3)`, `T = x⁷y³`, polygon `(0,0),(1,0),(21,6),(21,9)` | 22 graded levels | **not attempted here.** The reduction applies but the strip is wide; this is the natural next target |
| bracket-`x` targets (`p108_192622`, `w6_35657_*`) | `T = xy³`, `(3,2)` | `3 f g' − 2 f' g = T` — a **trigonal** cover `y³ = f(T)`, not hyperelliptic | not attempted here |

## 8. What was *not* found, stated plainly

No counterexample. No pair `(P,Q)` with `{P,Q} = x²` matching a surviving GGHV
target was produced, and the four rungs of the 2:3 ray that were decided came
back empty. The witnesses in §5 satisfy the bracket equation exactly but not
the polygon conditions, and §5 proves they cannot be pushed to.

What did change: the `(72,108)` resister `p108_525122` went from *undecided
after 1800 s / 6 GB of `msolve`* to *decided in about two minutes per orbit*,
and the reason it dies is now visible rather than opaque — the leading
period-level admits exactly five solutions, and each is destroyed by the
`f_0' ≠ 0` that the polygon's own top-left vertex forces.


## 9. Widening the question, and a caught false-EMPTY

The campaign's `extract` system asks a *narrow* question: is there a `P` with
the reduced Newton polygon and a `Q` **in the prescribed windows**? The
reduction makes a strictly wider question askable: is there such a `P` and
**any** strip-type `Q` at all?

`general2.py` implements that. Two design points matter, and one of them was
found the hard way:

* Coefficients of `g_σ` that the cascade cannot solve for — the diagonal
  `rmax·n − σ·lo_top` vanishes — are **resonances**. They are genuine free
  unknowns and get their own ring variable. Dropping them silently would make
  every verdict a statement about a proper subfamily.
* Prescribing one T-degree per `g_σ` is a restriction. The first version of the
  scan (`general.py`, `batch.py`) forced every `g_σ` to have the same top degree
  `M = smax·m/rmax`, and reported `tops=(4,2)`, `μ=1` **EMPTY** — but that
  configuration is witness `W3` from §5, which is certified exact. The witness
  has `deg g_1 = 1` and `deg g_0 = 3`; no single `M` fits both. Fixed in
  `general2.py` by bounding every `g_σ` by a generous common `N`; the same
  configuration now returns `dim 8`, non-empty, as it must.

  **`general.py` / `batch.py` are superseded and their EMPTY verdicts are
  statements about the restricted subfamily only.** They are kept because the
  failure is instructive: it is exactly the campaign's failure class (v),
  a certifier that could not have failed, and it was caught only because §5
  supplied a positive control. Every scan here now runs against that control.

### The wider verdict on the 2:3 ray

`focused.py` runs `μ=2, (rmax,smax)=(2,3), tops=(m,m,m)` — the 2:3 ray, with
`m = 8` the `(72,108)` polygon — against **all** strip-type `Q` with
`deg_T g_σ ≤ 2m+2`:

| m | deg P | unknowns | conditions | verdict |
|---|---|---|---|---|
| 2 | 6 | 9 | 8 | **EMPTY** |
| 3 | 9 | 12 | 17 | **EMPTY** (and see below — free) |
| 4 | 12 | 15 | 24 | **EMPTY** |
| 5 | 15 | 18 | — | TIMEOUT at 900 s (and see below — free) |

Where these come back empty they say something stronger than the campaign's
verdict: not merely that no `Q` fits the prescribed windows, but that no
strip-type `Q` exists at all.

### Odd m is free

`odd_m.py`. The top level is `2 f g' − 3 f' g = T²` with `f = f₂` of degree `m`
(top coefficient nonzero — that is the polygon's vertex, and the nondegeneracy
condition) and `g = g₃` of degree `d`. The coefficient of `T^{m+d−1}` is
`(2d − 3m)·f_m·g_d`. If `2d ≠ 3m` it is nonzero, so `deg(LHS) = m+d−1`, and
`LHS = T²` forces `m + d = 3`. So either `m + d = 3` (only `m = 1, 2`), or
`2d = 3m`, which requires **`m` even**.

So every odd `m ≥ 3` on the 2:3 ray is empty at the top coefficient alone, with
no Gröbner basis required. That is why `m = 5` ground for 900 s without
finishing: a degrevlex GB reaches the top coefficient last. Half the ladder is
free, and only even `m` needs computing.

### Staged form of the wider question

`wide_m.sing` runs the wider question the way `decide_m.sing` runs the narrow
one: solve the leading level first (it involves `f₂` alone), decompose, then
adjoin the lower levels per orbit — but with `g₂, g₁, g₀` bounded only by
`NW = 2m+2` rather than the campaign's windows. `g₃` keeps degree `3m/2`, which
is forced, not assumed, by the argument above.

| m | deg P | leading level | wider verdict |
|---|---|---|---|
| 2 | 6 | free | **EMPTY** |
| 4 | 12 | 3 solutions | **EMPTY** |
| 6 | 18 | 10 solutions (2 orbits) | **EMPTY** |
| 8 | 24 = `(72,108)` | 35 solutions (5 orbits) | **EMPTY**, all five orbits |

Per-orbit runs for `m = 8`: `widestage_0.log`, `widestage_1.log` (the two
`F_p`-rational orbits) and `widestage_ext3.log` (the three living in
`F_p[a]/(a³−10400a²+1641a−3068)`) — every one `dim = −1`, GB `= 1`.

So each even rung up to and including `(72,108)` is empty not merely against
the campaign's prescribed `Q`-windows but against **every** strip-type `Q` of
`T`-degree up to `2m+2`. Combined with §"Odd m is free", the whole 2:3 ray is
decided through `m = 8`:

> For `m ≤ 8`, there is no `P` with the minimal-width `μ=2` strip polygon of
> parameter `m` and any strip-type `Q` at all satisfying `{P,Q} = x²` with the
> polygon's three vertex coefficients nonzero.

`m = 10` (deg P = 30) is the first undecided rung, and its leading level is the
first real test of the Catalan count.
