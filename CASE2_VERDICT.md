# Case (2) of GGHV Prop 4.3 — the decision

**Verdict: case (2) admits no realization with its stated Newton polygons.**
Complete and certified at three independent primes — `65521`, `32003`, `65537`
— covering *every* point of the edge variety at each. The reduction from "the
computation says `B = 0`" to "the polygons are wrong" is an elementary
characteristic-free lemma, so only the `B = 0` input is machine-checked.

## 0. Setup

Case (2) is
```
N(P) = {(0,0), (1,0), (8,14), (8,16)}          N(Q) = {(0,0), (2,1), (12,21), (12,24)}
```
with `[P,Q] = x²` — case (1) minus the vertices `(0,8)` and `(0,12)`. It is
one of the two shapes of the `(72,108)` degree pair, the only open shape below
max degree 125.

In the grading `w := j − 2i` both polygons are *thin*: `N(P)`'s edges are
`j = 2i` and `j = 2i − 2`, so `P` carries only weights `0, −1, −2`; `N(Q)`'s
are `j = 2i` and `j = 2i − 3`, so `Q` carries only `0, −1, −2, −3`. Writing
`t := x y²`,

```
P = A(t) + B(t)/y + C(t)/y²          Q = D(t) + E(t)/y + F(t)/y² + G(t)/y³
```

and coefficient counts match the lattice points exactly: `A 9, B 8, C 8`
(= 25 = `N(P)`) and `D 13, E 12, F 12, G 11` (= 48 = `N(Q)`). For these forms

```
[ φ(t) y^{−a} , ψ(t) y^{−b} ]  =  ( a φ ψ' − b φ' ψ ) y^{1−a−b}
```

exactly, so `[P,Q] = x² = t² y^{−4}` splits by weight into **five** equations
(the weight-1 part `[A,D]` vanishes identically, `a = b = 0`):

```
(w= 0)   B D' = A' E
(w=−1)   −2 A'F + B E' − B'E + 2 C D' = 0
(w=−2)   −3 A'G + B F' − 2 B'F + 2 C E' − C'E = 0
(w=−3)   B G' − 3 B'G + 2 C F' − 2 C'F = 0
(w=−4)   2 C G' − 3 C'G = t²
```

The polygon *vertices* require `a₀, c₁, c₈, a₈ ≠ 0` and `d₀, g₂, g₁₂, d₁₂ ≠ 0`.
Vertex `(8,16)` is `a₈`; vertex `(12,24)` is `d₁₂`. These are the two that die.

## 1. The reduction lemma (characteristic-free, no computer)

> **Lemma.** If `B = 0` then `a₈ = 0` and `d₁₂ = 0`.
>
> *Proof.* With `B = 0`, `(w=0)` reads `0 = A'E`.
> If `E ≠ 0` then `A' = 0`. If `E = 0` then `(w=−2)` reads `−3A'G = 0`, and
> `G ≠ 0` because `(w=−4)` gives `2CG' − 3C'G = t² ≠ 0`; hence `A' = 0` again.
> So `A` is constant and `a₈ = 0`. Then `(w=−1)` reads `2CD' = 0` with `C ≠ 0`,
> so `D` is constant and `d₁₂ = 0`. ∎

Contrapositive, which is how it gets used:

> **`a₈ ≠ 0  ⟹  B ≠ 0`.**

So the whole case reduces to one scalar question: *can `B` be nonzero?*

## 2. The computation: `B ≡ 0` on every branch

`(w=−4)` is self-contained in `(C,G)`. With the normalization `c₁ = c₈ = 1`
(legitimate: the two scalings `t ↦ λt` and `(C,G) ↦ (μC, G/μ)` move
`(c₁,c₈)` by `(μλ, μλ⁸)`, so both can be set to 1 up to a residual `μ₇`) it is
zero-dimensional of **vdim 35**, with a shape-lemma RUR in the primitive
element `θ = g₁₂`. The eliminant factors over `F_65521` into four irreducibles

```
(θ⁷ + 7766) (θ⁷ − 30040) (θ⁷ − 9260) (θ¹⁴ + 13055 θ⁷ − 23589)      7+7+7+14 = 35
```

(irreducibility of each verified independently). So the four residue fields
`F_{p⁷}, F_{p⁷}, F_{p⁷}, F_{p¹⁴}` cover **all 35 points** of the edge variety —
nothing is missed.

On each branch the remaining chain is linear in blocks:

| step | shape | result |
|---|---|---|
| `(w=−3)` | homogeneous linear in `(B,F)` | solution space **dim 3**: `(B,F) = Σ βᵢ vᵢ` |
| `(w=−2)` | linear in `(A,E)`, matrix **independent of `(B,F)`** | fixed kernel **dim 3**: `(A,E) = P₂(β) + Σ αⱼ kⱼ`, `P₂` quadratic in `β` |
| `(w=−1)` | linear in `D` with image `C·{deg ≤ 11}` | solvable iff `C ∣ (−2A'F + BE' − B'E)`: **8 conditions**, degree ≤3 in `β`, ≤1 in `α` |
| `(w= 0)` | division-free `B(2A'F − BE' + B'E) = 2C·A'E` | **28 conditions**, degree ≤4 in `β`, ≤2 in `α` |

Both condition sets were interpolated **exactly** in their fixed monomial
bases (80 and 350 monomials) and handed to Singular. Result, identical on all
four branches:

```
VERDICT: dim = 2
components: 1
  comp 1: dim 2 = (al(3), al(2), b(3), b(2))
```

A single minimal prime, and it is *linear*: `β₂ = β₃ = α₂ = α₃ = 0`, with `β₁`
and `α₁` free.

### What that 2-fold is

Direct reconstruction at those points (no interpolants involved —
`_c2_verify.py` rebuilds `A…G` from scratch and brackets the assembled
two-variable polynomials) gives, on every branch and for every `(β₁, α₁)`:

```
B ≡ 0,   D ≡ 0,   E ≡ 0,   A = const,   F = λC
a₈ = 0,   d₀ = 0,   d₁₂ = 0
[P,Q] = x²  exactly
```

So the surviving family is real but degenerate: `Q = λ(P − a₀) + G/y³`, and the
bracket reduces to the edge equation alone. The two free parameters are pure
gauge — `β₁` is the weighted scaling `(B,F) ↦ ν(B,F)`, `(A,E) ↦ ν²(A,E)`,
`D ↦ ν³D`, and `α₁` is the additive constant of `A` (every equation sees `A`
only through `A'`).

The Newton polygons collapse: `deg P` drops `24 → 22` and `deg Q` drops
`36 → 21`. This is not case (2).

Combined with the Lemma: `B ≡ 0` on all solutions ⟹ `a₈ = 0` always ⟹ the
vertex `(8,16)` of `N(P)` is absent. **Case (2) is not realizable over
`F̄_65521`.**

## 3. Leading coefficients: the cusp structure, by hand

Independently of the elimination, the `t¹⁹` coefficient of each equation
(taking `deg A = deg B = deg C = 8`, `deg D = deg E = deg F = deg G = 12`) gives

```
(w=−3)   f₁₂ = (3/2) b₈ g₁₂
(w=−2)   16 e₁₂ = 24 a₈ g₁₂ + 6 b₈² g₁₂
(w=−1)   24 d₁₂ = 16 a₈ f₁₂ − 4 b₈ e₁₂
(w= 0)   3 b₈ d₁₂ = 2 a₈ e₁₂
```

Eliminating `d₁₂, e₁₂, f₁₂` leaves `b₈⁴ − 8a₈b₈² + 16a₈² = 0`, that is

> **`(b₈² − 4a₈)² = 0`.**

With `c₈ = 1` this is `disc(a₈z² + b₈z + c₈) = 0`; writing `b₈ = 2s`,

```
(a₈, b₈, c₈)         = (s², 2s, 1)         = (s + z)²
(d₁₂, e₁₂, f₁₂, g₁₂) = g₁₂(s³, 3s², 3s, 1) = g₁₂ (s + z)³
```

The rightmost column of `N(P)` is forced to be a perfect square and that of
`N(Q)` the matching cube — cusp type `(2,3)`, recovered here independently of
the case-(1) analysis where it first appeared. This is *consistent*, not
contradictory: the leading data admits `b₈ ≠ 0`. The obstruction is therefore
genuinely deeper than the leading edge, which is why `B ≡ 0` needed the full
elimination. It also rules out the cheapest possible hand proof.

## 4. Scope, honestly stated

The Lemma of §1 is characteristic-free. Its input — `B ≡ 0` — is a Gröbner
computation over a finite field, and emptiness mod a *single* prime does not
imply emptiness in characteristic 0 (`(px − 1)` is empty mod `p` and nonempty
over `ℚ`). So the computation was repeated at three primes, each time
recomputing the edge RUR from scratch rather than reusing the `65521` table —
`g₂ = 1` was a derived fact at `65521` and is read off the fresh RUR at the
other primes:

| prime | vdim | eliminant degree | factor degrees | branches run | verdict |
|---|---|---|---|---|---|
| 65521 | 35 | 35 | 7, 7, 7, 14 | 4/4 | `dim 2`, component `(b₂,b₃,α₂,α₃)` |
| 32003 | 35 | 35 | 1,1,2,2,2,2,2,2,3,6,6,6 | 12/12 | same |
| 65537 | 35 | 35 | 1, 4, 6, 12, 12 | 5/5 | same |

The eliminant has degree 35 at every prime, and the factor *patterns* differ
completely (65521 has the `μ₇` splitting because `7 ∣ p−1`; 32003 has genuine
`F_q`-rational branch points), yet the verdict, the dimension, the number of
components, and the component's *generators* are identical every time. That is
the good-reduction signature: if the characteristic-0 variety had a point with
`a₈ ≠ 0`, it would have to reduce badly at all three.

This is strong evidence, not a proof. The honest statement:

* **Closed over `F̄_q` for `q ∈ {65521, 32003, 65537}`** — every branch point.
* **Characteristic 0: not yet proved.** `_c2_oneshot.py` puts the whole
  five-equation system plus the Rabinowitsch equation `w·a₈ = 1` into one
  ideal (68 unknowns) and asks whether it is the unit ideal over `ℚ`; that run
  has not terminated. Until it does, "case (2) is closed" is a
  three-prime statement.

## 5. What this does and does not settle

It settles case (2) of Prop 4.3 (mod the char-0 caveat). It does **not** settle
case (1) — the full pentagons `N(P) = {(0,0),(1,0),(8,14),(8,16),(0,8)}`,
`N(Q) = {(0,0),(2,1),(12,21),(12,24),(0,12)}` — which is a genuinely different
system: with the extra vertices `(0,8)` and `(0,12)` the grading `w = j − 2i` is
no longer thin and the reformulation above does not apply. Case (1) is tracked
separately (`trackB1_*`, grading `w = j − i`), where the remaining gap is
whether support/vanishing/(C4) force `P^{1/2}` to terminate.

## Files

| file | role |
|---|---|
| `trackB1_case2_edge.py` | the `w = j−2i` reformulation; the five equations; the edge solve |
| `trackB1_case2_extend.py` | `K`-arithmetic, RUR, `(w=−3)/(w=−2)/(w=−1)` systems; `set_modulus` for a general minimal polynomial |
| `trackB1_case2_final.py` | `(w=−1)` interpolation (80 monomials) |
| `_w0.py`, `_w0np.py` | `(w=0)` interpolation (350 monomials); `_w0np` uses `F_p` sample points + numpy |
| `_c2_branch.py` | the whole chain on one branch of the eliminant |
| `_c2_verify.py` | direct reconstruction and bracket, bypassing every interpolant |
| `_c2_oneshot.py` | the single-system char-0 attempt |
| `_c2_rur.py` | edge solve + shape-lemma RUR extraction at an arbitrary prime |
| `_c2_multiprime.py` | the whole decision at a fresh prime, from a fresh RUR |

### A note on the interpolation

Sampling `β, α` in `F_p ⊂ K` rather than in all of `K` makes the *monomial
values* land in `F_p`, so the interpolation matrix is an `F_p` matrix even
though the unknown coefficients stay in `K`; writing each unknown in the
`θ`-basis decouples the system into `[K:F_p]` independent `F_p` systems sharing
one matrix. That replaced a 370×350 Gaussian elimination over `F_{p⁷}` in
Python (~25 min) with one numpy RREF (~1 s). It is valid because individual
monomial degrees are `≤ 4 ≪ p`; and it is *checked* rather than assumed —
every interpolant is verified against fresh points with full `K`-random
coordinates before use.
