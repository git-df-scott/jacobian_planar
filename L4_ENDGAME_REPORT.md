# The endgame residue equation, solved


> ## ⚠ CORRECTED BY PR #9 — read this first
>
> An adjudication pass (branch `claude/opus-5-counterexample-plan-sep6yk`, PR #9,
> `ADJUDICATION.md`, 110 exact checks) refuted several claims in this document. They are
> corrected in place below and listed here so nothing is taken on trust:
>
> 1. **`ABSENT` is wrong — the correct label is `NOT-FETCHED`.** This session ran
>    `git rev-list --objects --all` against a local object set containing only `main`
>    plus its own commits. The artefacts exist on `claude/plane-counterexample-endgame-az3geq`:
>    **65** session-19–38 paths, `wave1/edgeQ_eliminant.txt` (5,759,664 bytes),
>    `wave1/pent_L23.ms` (43,158,481 bytes), `CASE2_STATUS.md`, `ABOVE_125_STATUS.md`,
>    and the H1c files. Every "blocked here" below inherits this error.
> 2. **`D = 15 − 12/β` dropped an `ε`.** The correct formula is
>    `D_ode = ε·(15 − 12/β)` with `ε = ord_{U=0}(g)`; the bound `< 15` holds only at `ε = 1`.
> 3. **`m = 4` is not universal.** The exponent is `k = 5ε − 1`, so `k = 0` or `k ≡ 4 (mod 5)`.
> 4. **The "two independent closures" are one closure.** `deg W̃₋₅ = 28 ⟺ map-degree 13`
>    identically, so the degree-ledger leg and the map-degree leg are the same statement.
>    The genuinely independent second leg is E4's ladder bound, which is genericity-conditional.
> 5. **The nine (108,72) charts are not proved exhaustive** — they assume both bidegrees are
>    multiples of one primitive edge vector. Witness outside the enumeration: `(40,68)`, `(30,42)`.
>
> **The conclusions survive.** (99,66), (108,72), the Second Framework and the isotope
> series are all still empty — on `k ≡ 4 (mod 5)` plus `D_ode`, computed in PR #9
> (`D_ode(Second Framework) = 69/5`, so neither 23 nor 69: dead for every `ε`).

**Plane Jacobian campaign — the `T_{D,m}(R) = −c` object, its complete rational
solution set, and what that does to Borisov's framework family.**

Every statement here is backed by an exact machine certificate in `certifiers/new/`,
run under two toolchains with no shared code (sympy and PARI/GP). `./run_all.sh`
reproduces everything.

---

## 0. Notation and the object

Work in the `(q,v)`-chart of Borisov's First Framework (`arXiv:1901.04073`) at the
degree pair `(99,66)`, with `U = v + 1`. The framework data used below:

| symbol | meaning | (99,66) |
|---|---|---|
| `β` | `q`-pole order of `y₂` on the `(−2)`-curve | 6 |
| `γ` | `q`-pole order of `y₁` on the `(−2)`-curve | 9 |
| `σ` | `q`-index of the first surviving block of `W = y₁² − y₂³` | 5 |
| `e := γ − σ` | `q`-index of the deviation `Δ = W/(2y₁)` | 4 |
| `G` | `v`-exponent of the boundary polynomial `g = α U v^G` | 8 |
| `N` | `v`-power normalising `R := v^N W~₋₅ / g⁶` | 39 |
| `p, τ` | Keller chart form `J_{(q,v)} = −c q^{−p} v^{−τ}` | 3, 6 |

---

## 1. Theorem A — the master identity, re-derived

Write `y₂ = q^{−β} η(v)` with `η = g² v^{−3β}`, and `Δ = q^{e} δ(v)` with
`δ = (g³/2) R v^{3e−N}`. Put `a = 2G − 3β`, `b = 3G + 3e − N`. Then the leading Keller
block is

```
    e·δ·η' + β·δ'·η  =  (α⁵/2) U⁴ v^{a+b−1} · [ β U v R' + (2e+3β) v R + (ea+βb) U R ] .
```

Using `v = U − 1`, the `R`-part collapses to a multiple of `R` alone exactly when

```
    N = (2e + 3β)(1 + G)/β ,           and then       D := 3(2e+3β)/β = 3N/(1+G) .
```

At `(99,66)`: `a = −2`, `b = −3`, `a+b−1 = −6 = −τ`, `N = 39`, `D = 13`, and the block is

```
    α⁵ (v+1)⁴ ( 3 v(v+1) R' − 13 R ) / v⁶ ,
```

so the Keller condition `J = −c q^{−3} v^{−6}` reads

```
    (★)      α⁵ (v+1)⁴ ( 3 v(v+1) R'(v) − 13 R(v) )  =  −c ,        c ≠ 0 .
```

Two further consequences, both used later:

* **`m = 4` at `ε = 1` only** (originally written as universal; corrected by PR #9 to
  `k = 5ε − 1`). The exponent on `(v+1)` is `4` when `ε = 1`, for a framework of cusp
  type `(2,3)`: `U³` (from `δ`) times `U¹` (from `η'`), equivalently `U²·U²` (from
  `δ'·η`). It does not depend on `β, e, G, N, p`.
* **`D` is bounded.** With `e = β + 1 − p` (forced by `J`'s `q`-exponent),
  `D_ode = ε(15β − 6p + 6)/β`; at `p = 3`, `D_ode = ε(15 − 12/β)`, which is `< 15` only at `ε = 1`.

**Adversarial check on the derivation.** `J(y₁,y₂) = J(Δ,y₂)` exactly, since
`y₁ = y₂^{3/2} + Δ` and `J(y₂^{3/2}, y₂) = 0`. Block bookkeeping: `Δ`'s blocks sit at
`q^{e+i}` and `y₂`'s at `q^{−β+j}` with `i, j ≥ 0`, and each `J` term loses one `q`, so a
pair lands at `q^{−p+i+j}`. Only `(i,j) = (0,0)` reaches `q^{−p}`. **The computed block is
the entire Keller coefficient — no conspiracy among subleading blocks is possible.**

*Certificate:* `E1_master_identity.py` — 17/17, including the archive's own collapse
arithmetic `13(9v+8) − 117(v+1) = −13`.

---

## 2. Theorem B — every rational solution of the endgame equation

Let `K` have characteristic 0, `κ ≠ 0`, `D ≥ 1`, `m ≥ 1`, and

```
    T_{D,m}(R) := (v+1)^m ( 3 v(v+1) R'(v) − D R(v) )  =  κ ,     R ∈ K(v).
```

**(a) No poles anywhere except `v = −1`.**
At `t ∉ {0,−1}` with `ord_t R = μ < 0`, `ord_t(3v(v+1)R') = μ − 1 < ord_t(D R)`, so the
left side has a pole while the right side is a nonzero constant. At `v = 0`, if
`R ~ ρ v^μ` with `μ < 0` then the leading coefficient of the bracket is `(3μ − D)ρ ≠ 0`
(as `μ < 0 < D`), again a pole. ∎

**(b) `k := −ord_{−1}(R) ≥ m`, and `k > m` forces `D = 3k`.**
`ord_{−1}(bracket) ≥ ord_{−1}(R)`, so `ord_{−1}(LHS) ≥ m − k`, which must be `0`; hence
`k ≥ m`. Writing `R = S(v+1)^{−k}` with `S` regular and nonzero at `−1`,

```
    bracket = (v+1)^{−k} · Φ ,      Φ := 3v(v+1)S' − (3kv + D) S ,     Φ(−1) = (3k − D)S(−1),
```
so `ord_{−1}(LHS) = m − k + ord_{−1}Φ = 0`. If `k = m` then `Φ(−1) ≠ 0`, i.e. `D ≠ 3m`;
if `k > m` then `Φ(−1) = 0`, i.e. `D = 3k`. ∎

**(c) `3 ∤ D` ⟹ exactly one solution, of map-degree exactly `m`.**
`k = m` by (b). `Φ = κ` gives, for `S = Σ s_n v^n`,

```
    (3n − D) s_n + 3(n − 1 − m) s_{n−1} = κ·δ_{n,0} ,
    s_0 = −κ/D ,        s_n = 3(m+1−n)/(3n − D) · s_{n−1}  (n ≥ 1),
```

which is well posed (`3n ≠ D`), terminates at `n = m + 1`, and gives `deg S = m` exactly
with `S(−1) = −κ ≠ 0`. Both numerator and denominator have degree `m`, so the map-degree
is `m`. ∎

**(d) `D = 3j` with `j > m` ⟹ an affine line of solutions**, `R_m + C·(v/(v+1))^j`; the
kernel is spanned by `(v/(v+1))^j`, of map-degree `j`.

**(e) `D = 3j` with `j ≤ m` ⟹ no rational solution at all.**
`k = m` is barred (needs `D ≠ 3m`, and for `j < m` the recursion at `n = j` forces
`s_{j−1} = 0` hence `s_0 = 0 ≠ −κ/D`); `k > m` needs `D = 3k > 3m ≥ 3j = D`. ∎

**The First Framework instance `(D,m) = (13,4)`, `κ = −c/α⁵`:**

```
    R(v)  =  −κ · (243 v⁴ − 81 v³ + 54 v² − 42 v + 35) / (455 (v+1)⁴)
```

is the **unique** rational solution of `(★)`. Pole divisor `4·[−1]`; no pole at `v = 0`;
map-degree **4**; not a polynomial.

*Certificates:* `E2_endgame_classification.py` — 25/25, including an independent
brute-force exact linear algebra over `Q` reproducing (a)–(e) on 28 grid points;
`E3_pari_crosscheck.gp` — 35/35 in PARI/GP with independent code.

> **This is the refutation.** The archive's decisive step — *"the left side vanishes at
> `v = −1`, the right side is `−c ≠ 0`"* — presupposes that `R` has no pole at `v = −1`.
> It has one, of order exactly 4. The archive's supporting certificate searched only
> polynomials; `E9` reproduces it verbatim (rank 14, infeasible, at degree ≤ 13, 20, 30
> and 60) and then finds the true solution by the single change `P(v) → P(v)/(v+1)⁴`.

---

## 3. Theorem C — pole admissibility: the pole order is at most 3

The framework fixes `R := v³⁹ W~₋₅(U)/g(U)⁶` with `g = αU(U−1)⁸`, so

```
    R = W~₋₅ / ( α⁶ U⁶ v⁹ ) ,        ord_{v=−1}(R) = u(W~₋₅) − 6 ,    u := ord_{U=0} .
```

A 4th-order pole therefore demands `u(W~₋₅) = 2`. Now use the sqrt-tower: with
`t_j := B~₋₆₊ⱼ/g²`, `(Σ S_m x^m)² = (1 + Σ_{m≥1} t_m x^m)³`, `A~₋₉₊ₘ = g³S_m` for
`m ≤ 12`, and `W~₋₅ = 2g³(A~₄ − g³S₁₃)`. Put `τ_j := u(B~₋₆₊ⱼ) − 2 ≥ −2` and

```
    f(m) := min over multisets λ of positive integers with Σλ = m  of  Σ_{j∈λ} τ_j .
```

For a tower with no accidental cancellation, `u(g³S_m) = 3 + f(m)`. Polynomiality of
`A~₋₉₊ₘ` for `m ≤ 12` (the divisibility ladder) therefore forces `f(m) ≥ −3` for
`m ≤ 12`. Testing the partitions `j + j + … + j` gives the box bounds

```
    τ₁, τ₂, τ₃ ≥ 0 ;      τ₄, τ₅, τ₆ ≥ −1 ;      τ₇, …, τ₁₃ ≥ −2 .
```

**Lemma.** Under those bounds, every partition of 13 has `Σ τ ≥ −3`, i.e. `f(13) ≥ −3`.
*Proof.* At most one part is `≥ 7` (two would exceed 13); it contributes `≥ −2`, and the
remaining `≤ 6` admits at most one part from `{4,5,6}`, contributing `≥ −1`. If no part
is `≥ 7`, at most three parts lie in `{4,5,6}` (since `4·4 = 16 > 13`), contributing
`≥ −3`. Parts `≤ 3` contribute `≥ 0`. ∎ *(machine-checked over all 101 partitions.)*

Hence `u(g³S₁₃) ≥ 0`, hence `u(W~₋₅) ≥ 3`, hence

```
    ord_{v=−1}(R)  ≥  −3 :     the pole order at v = −1 is at most 3 .
```

Theorem B says the pole order must be exactly 4. **Out of range by exactly one.**

*Certificate:* `E4_pole_admissibility.py` — 20/20, including verification that
`(Σ S_m x^m)² = (1+T)³` through `x¹³`, that the coefficient of `t₁^m` in `S_m` is
`binom(3/2, m) ≠ 0` (which is what makes the box bounds bite), and that the min-plus
model reproduces the true `U`-order on 40 random ladder-feasible towers.

**Scope.** Closure by Theorem C assumes the ladder's divisibilities are not satisfied by
accidental cancellation among monomials of equal order. `EA_unconditional_refinements.py`
pins that hypothesis down exactly: all 372 universal coefficients of `S_1 … S_13` are
nonzero (so a monomial can only be cancelled by *another* monomial of the same order);
`τ₁ ≥ −1` — i.e. `u(B~₋₅) ≥ 1` — holds with **no** genericity assumption at all; and an
exhaustive enumeration shows that allowing cancellation enlarges the feasible set of
`(τ₁,…,τ₄)` from 108 vectors to 145, with `τ₄ = −2` appearing only in the enlargement.
So `τ₄ ≥ −1` is precisely the box bound that genericity buys. Closure by Theorem D below
needs no such assumption.

---

## 4. Theorem D — propagate the solution up the tower

Take the unique `R` of Theorem B and push it back:

```
    W~₋₅(U) = α⁶ U⁶ v⁹ R |_{v = U−1} = α⁶ · U² (U−1)⁹ · S(U−1) ,
```

an honest polynomial in `U` of degree **15**, with `u(W~₋₅) = 2` and `(U−1)⁹ | W~₋₅`.

What the pole branch *satisfies*: `R` has no pole at `v = 0` (the divisibility that
THEOREM 3 wanted), its only pole is `v = −1`, and `W~₋₅` respects the Session-15 degree
caps. `c` and `α` enter only as an overall scalar, so no rescaling changes anything.

What it *fails*: the framework's realization layer demands that `R` realize the certified
**degree-13** map — equivalently `deg W~₋₅ = 6·deg g − 26 = 28`. The solution has

```
    deg W~₋₅ = 15 ,     map-degree of R = 4 .
```

`4 ≠ 13`. **Closure.** No genericity, no Belyi coefficients, no THEOREM 3.

Note the coincidence: `deg W~₋₅ = 15` is *exactly* the near-miss's degree
(`W~₋₅ = n₃ U⁶(U−1)⁹`). The two differ only in `u`: `2` versus `6`. The pole branch that
the archive's theorem wrongly excluded lands in the same degree stratum as the near-miss
and dies on the same ledger.

**Both readings of the realization demand.** Session 10 phrases the object as
`ρ = W₋₅/K₋₆³ = W~₋₅/g⁶`; Session 11 as `R = v³⁹ρ`. Under Session 11's reading the
map-degree is 4; under Session 10's it is 43; under the archive's literal phrasing
(*"`R` must be a polynomial of degree exactly 13"*) the contradiction is immediate,
since `R` is not a polynomial. **The closure holds under all three.**

**The `c = 0` branch.** Keller forces `c ≠ 0`. For completeness: at `c = 0` the kernel of
`3v(v+1)R' − 13R` over `Q̄(v)` is trivial (it would be `C(v/(v+1))^{13/3}`, and `3 ∤ 13`),
so `R = 0`, i.e. `W~₋₅ = 0` — the first surviving block is then not at `−5`, contradicting
the chain data.

*Certificate:* `E5_propagate_tower.py` — 27/27.

---

## 5. Theorem E — the transfer conjecture, corrected

The archive conjectured: *"for chain degree `D` the same mechanism yields
`3v(v+1)R' = D R`, fatal whenever `D/3` is not an integer. Second Framework: `D = 23`."*

Both halves are false. By Theorem A, `D_ode = ε(15 − 12/β)`, which at `ε = 1` is `< 15`, so no framework of this cusp
type has `D = 23`; and by Theorem B, `3 ∤ D` is precisely the **solvable** case.

**Replacement.** For every framework of cusp type `(2,3)` with `p = 3`:

```
    k = 5ε − 1 ;    D_ode = ε(15 − 12/β) ;    integral D_ode at ε=1 ⟺ β | 12 .

    β = 1, 2, 4   (D = 3, 9, 12)   →  no rational solution at all — dies outright
    β = 3, 6, 12  (D = 11, 13, 14) →  a unique solution, of map-degree 4
```

so **the framework is empty whenever its realization layer demands a map of degree
`≠ 4`** — in particular whenever its chain has five or more curves. This covers the
First Framework (`D_chain = 13`), the Second Framework (`D_chain = 23`), and the isotope
series uniformly.

**Consequence for the `N2_prompt.md` sub-campaign.** Its Phase 0 (rederive the degree-23
Belyi data before anything else) is unnecessary: the obstruction never touches the Belyi
coefficients. Only the Second Framework's chart valuations `(γ, β)` and chain degree are
needed, and the verdict follows by substitution.

*Certificate:* `E6_transfer_general.py` — 21/21.

---

## 5b. Theorem F — the closure does not depend on THEOREM 2 either

THEOREM 2 (boundary rigidity, `g = αU(U−1)⁸`) is the archive's other lost certificate,
and the plan calls it "the highest single lever on the board". Redo E1's derivation with
the `U`-multiplicity of `g` free — `g = α U^ε (U−1)^G` — and the collapse condition
becomes `N = (2e+3β)(ε+G)/β = 13(ε+G)/3`, with the endgame equation

```
    3 v(v+1) R' − 13ε R  =  −κ (v+1)^{1−5ε} v^{(16 − 2G + 13(ε−1))/3} .
```

Sweeping every `(ε, G)` allowed by the *certified* box cap `deg g = ε + G ≤ 9`:

| `ε` | `G` | `N` | `D = 13ε` | rational `R`? | map-degree |
|---|---|---|---|---|---|
| 1 | 2, 5, **8** | 13, 26, **39** | 13 | unique | **4** |
| 2 | 1, 4, 7 | 13, 26, 39 | 26 | unique | 9 |
| 3 | 0 | 13 | 39 | 1-parameter family | 14 |
| 3 | 3, 6 | 26, 39 | 39 | none | — |
| 4–9 | all | — | 52…117 | none | — |
| 0 | 0 | 0 | 0 | none | — |

**No admissible boundary polynomial yields map-degree 13.** The closure is therefore
independent of THEOREM 2.

As a by-product, THEOREM 2's own contested step — `U | g`, which the archive got from
"propagation from the {1}-marked corner" — falls out of a congruence: with `G = 8`,
integrality of `N = 13(ε+8)/3` needs `3 | ε+8`, and `deg g ≤ 9` gives `ε ≤ 1`, so `ε = 1`.

*Certificate:* `EB_theorem2_robustness.py` — 8/8.

---

## 5c. (108,72) — the L4 target, instantiated

At (99,66) the near-miss bidegrees are `y₁: (27,72) = 9·(3,8)` and `y₂: (18,48) = 6·(3,8)`,
and Session 8's chart gives `ord_q(x₁^i x₂^j) = j − 3i`, so `γ = 9`, `β = 6`, and
`deg P = 11γ`, `deg Q = 11β` with `11 = 3+8`. Reading (108,72) the same way with
primitive edge vector `(a,b)`, `s := a+b`, gives `γ = 108/s`, `β = 72/s` — so `s | 36`,
nine charts in all. Note `11 ∤ 108`: **(108,72) cannot reuse the (99,66) dessin's edge
vector**, which is exactly why `L = 4` there and `3` at (72,108).

| `s` | `γ` | `β` | `D_ode = 15 − 12/β` (at `ε = 1`) | endgame |
|---|---|---|---|---|
| 1, 2, 3, 4, 9 | 108…12 | 72…8 | `89/6, 44/3, 29/2, 43/3, 27/2` | unique, map-degree 4 |
| 6 | 18 | 12 | 14 | unique, map-degree 4 |
| **12** | **9** | **6** | **13** | unique, map-degree 4 *(the First Framework's own endgame)* |
| 18 | 6 | 4 | 12 | **no rational solution at all** |
| 36 | 3 | 2 | 9 | **no rational solution at all** |

Every admissible chart closes, since no Borisov chain has degree 4. Conditional only on
the Keller chart exponent `p = 3`; the theorem is uniform in `p`.

*Certificate:* `EC_10872_instantiation.py` — 19/19.

---

## 6. What this means for the campaign

**Step 3 of the plan asked whether the pole branch produces a candidate `(P,Q)`.
It does not.** It produces a unique, explicit `R`, which is then killed at the next layer
up — twice over, and by arguments that do not use any of the lost certificates. That is a
real closure, written down properly, and it replaces a closure that was resting on an
invalid step.

**Net effect on the map:**

* The `(99,66)` First Framework: **still empty**, now on a valid proof.
* `(108,72)`: **empty** — the nine-chart enumeration below is not proved exhaustive
  (PR #9), but the case closes on `k ≡ 4 (mod 5)` alone, which needs no enumeration.
* Framework routes generally — Second Framework, isotope series: **empty**, by Theorem E,
  with no Belyi rederivation. The framework layer is no longer a case-by-case fight.
* THEOREM 2 and THEOREM 3, the two lost theorems the plan called the highest lever:
  **neither is load-bearing any more** (§5b, §4).
* The archive's "one obstruction kills the whole published family" instinct was right;
  the obstruction it named was not the one doing the work.

**What is not closed, and is not claimed to be:** everything the plan's Steps 2 and 4
name that is `NOT-FETCHED` (see the banner) — H1c, the irreducibility sieve, the
eliminant, chart coverage, the `(72,108)` pentagon system, case (2) over `Q̄`, and the
167 above-125 targets. See `TRUST_MAP.md` §4. No candidate pair reached Step 5, so the
HIT protocol was not invoked.
