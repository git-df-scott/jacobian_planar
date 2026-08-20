# Wave 3 — Findings

**Branch:** `claude/opus-errors-false-proofs-820rmd`

Wave 2 broke a theorem. Wave 3 does the follow-through the plan called for: work out
whether the break is load-bearing, repair what can be repaired, and find the next
thing that is wrong. Two new theorems, one of them a genuine counterexample to a
claim the campaign has been leaning on since Session 38.

```
python3 wave2/run_all.py        # runs all ten certifiers, exit 0 iff all pass
```

**11/11 certifiers, 227/227 individual checks, 0 rigged checks in tree, 0 ledger lint
findings.**

| certifier | checks | verdict |
| --- | --- | --- |
| `wave3/w3_endgame_degree_obstruction.py` | 32/32 | **THEOREM W3-1** — repairs the First Framework proof outright |
| `wave3/w3_weighted_homogeneous_theorem.py` | 66/66 | **THEOREM W3-2 / W3-3** — Session 38's collapse, made a theorem *and* refuted as stated |
| `wave3/w3_hit_protocol.py` | 12/12 | HIT gate implemented and validated; no hit in this repository |
| `wave3/w3_descent_jacobian_formula.py` | 35/35 | **THEOREM W3-4 / W3-5** — Path A's items A1 **and** A2 answered |
| `wave3/w3_claim_ledger.py` | linter self-test PASS, 0 findings | contradictions and dropped hypotheses now mechanically impossible to leave standing |

---

## 1. THEOREM W3-1 — the endgame degree obstruction

### The problem wave 2 left open

Wave 2 showed the Sessions 16–18 decisive step (*"the left side vanishes at `v = −1`"*)
is invalid for rational `R`, and that the conclusion survived only because Session 13's
pole-fiber **Theorem 3** pins `R` polynomial by a separate route. That left the whole
(99,66) verdict resting on Theorem 3 — and Theorem 3's own decisive move,

> *"only the 1-point fiber fits a ≤2-point pole set, so the pole fiber is the order-13
> point at `v = ∞`"*

never rules out the other candidate. A degree-13 map totally ramified over `∞` at
`v = −1` — that is, `R = N(v)/(v+1)^13` — fits the fiber count exactly as well. The text
closes `v = 0` ("the forced divisibilities close the `v = 0` pole exactly") and says
nothing about closing `v = −1`. **That is a real gap, and it is the gap the H1c break
was pointing at.**

### The theorem that closes it

> **THEOREM W3-1.** For `T_{D,k}(R) = (v+1)^k (3v(v+1)R' − D R) = −c`, `c ≠ 0`:
>
> **(i)** `3 ∤ D` — the rational solution set is a **single function**, of degree
> exactly `k` as a map `P¹ → P¹` (pole divisor `k·[−1]`, numerator degree `k`, coprime).
> **(ii)** `3 | D` and `D ≤ 3k` — no rational solution at all.
> **(iii)** `3 | D` and `D > 3k` — a one-parameter family `R_k + C·(v/(v+1))^{D/3}`,
> whose members have degree `k` (at `C = 0`) or `D/3` (at `C ≠ 0`).
>
> **COROLLARY.** The endgame is compatible with the realization demand `deg R = D`
> **iff `3 ∤ D` and `k = D`.**

Verified on a 24 × 7 = 168-cell grid, with `D = 13` and `k = 4` themselves anchored by exact quotation from the primary artifact: solvability, nullity, degree and residual all
match, with two bogus degree rules (`deg R = D always`, `deg R = k always`) rejected by
the same grid, and both boundary witnesses checked (`k = D` with `3 ∤ D` available;
`k = D` with `3 | D` blocked).

### What it does to the frameworks

```
First Framework (99,66):  D = 13,  k = 4   (both read off the campaign's own
                          endgame identity, anchored by exact quotation)
  unique rational solution  R = c(243v⁴ − 81v³ + 54v² − 42v + 35) / (455 (v+1)⁴)
  deg R = 4;  realization demands 13.        4 ≠ 13  ⟹  DEAD

Second Framework:         D = 23,  k = 4
  unique rational solution  R = c(243v⁴ − 891v³ + 2079v² − 3927v + 6545) / (150535 (v+1)⁴)
  deg R = 4;  realization demands 23.        4 ≠ 23  ⟹  DEAD for every k ≠ 23
```

**The `R = N(v)/(v+1)^13` branch that Theorem 3 never excluded is killed directly:**
at `D = 13, k = 4` the rational solution is unique and has pole order exactly 4
(numerator at `v = −1` is 455 ≠ 0), so no solution of pole order 13 exists.

Compare the two routes:

| | wave-1 route | THEOREM W3-1 |
| --- | --- | --- |
| needs | the `v = −1` evaluation (invalid for rational `R`) **+** Theorem 3's pole-fiber count to restore it | `D`, `k`, and the demand `deg R = D` |
| uses Belyi coefficients | no | no |
| uses the pole-fiber count | **yes** | **no** |
| uses polynomiality of `R` | **yes** | **no** |
| status | CONDITIONAL | unconditional on the pole question |

So the (99,66) verdict is not merely rescued — it is now established on strictly less.
**Wave 2's `WAVE2_FINDINGS.md` said the transfer to `D = 23` was blocked and the
Second Framework was OPEN. THEOREM W3-1 closes it: `D = 23` dies too, for every `k ≠ 23`.**
That supersedes the wave-2 label, and the ledger records the change.

---

## 2. THEOREM W3-2 / W3-3 — Session 38's collapse

### The claim

Session 38 tested plane Keller maps that are `C*`-weighted-homogeneous and reported
*"22 branches with nonzero constant Jacobian, every one a diagonal linear map."*
Path B (file `39`) calls this *"the shape of a separator"* and correctly labels it
bounded-degree evidence, noting the degree-uniform proof was attempted and thrown away.
Path B's own success criterion is: *"the weighted-homogeneous collapse is upgraded to a
theorem (a separator, no more caveats)."*

### Both halves are now settled — and they point opposite ways

> **THEOREM W3-2 (degree-uniform, no bound).** Let `P, Q ∈ ℂ[x,y]` be
> weighted-homogeneous for integer weights `(a,b)` with **`ab < 0`**, and let
> `P_x Q_y − P_y Q_x = c ≠ 0`. Then `(P,Q)` is linear: `(c₁x, c₂y)` or `(c₁y, c₂x)`.

> **THEOREM W3-3 (the dropped hypothesis).** Mixed signs are **essential**. For weights
> `(1, m)`, `m ≥ 2` — same sign — the map `(x, y + x^m)` is weighted-homogeneous, has
> Jacobian `1`, and is **not linear**.

Session 38's sweep had `a > 0 > b` built into its grid — *"11 weight pairs `(a,b)` with
`a > 0 > b`"*. **The hypothesis was in the experiment and absent from the summary.**
That is mechanism M3, the same quantifier-scope drift as H1c, caught a second time in
the same repository. `(x, y+x²)` refutes the claim as stated in one line.

### The proof of W3-2 (each step machine-checked)

Write `b = −b'`, `g = gcd(a,b')`, `u = b'/g`, `w = a/g`, so `u,w ≥ 1`. Monomials with
`ai + bj = p` lie on one lattice line, so

```
P = x^α y^β A(s),   Q = x^γ y^δ B(s),   s = x^u y^w,   A,B ∈ ℂ[s].
```

**Step 1 — the `A'B'` terms cancel.** Directly,

```
P_x Q_y − P_y Q_x = x^(α+γ−1) y^(β+δ−1) · Φ(s),
Φ(s) = (αδ − βγ)AB + s[(αw − βu)AB' + (uδ − wγ)A'B].
```

Verified symbolically for generic `A, B` and symbolic `α,β,γ,δ,u,w`, plus 24 randomized
explicit-polynomial instances.

**Step 2 — only one power of `s` can survive.** `u,w ≥ 1`, so distinct powers of `s`
carry distinct `(x,y)`-exponents. `t ≥ 1` forces `α=β=γ=δ=0`, `u=w=1`, whence `Φ ≡ 0`
and `c = 0`. So `t = 0`: **`α+γ = 1` and `β+δ = 1`.** (Checked by exhausting the
exponent lattice.)

**Step 3 — four cases.** `(0,0,1,1)` and `(1,1,0,0)` give `Φ = const·s·A'B` and
`const·s·AB'`, which have no `s⁰` term, so `c = 0`: excluded. The other two give

```
Φ = ± Σ_{i,j} (1 + u·i + w·j) a_i b_j s^{i+j}.
```

**Step 4 — the top coefficient.** The `s^{degA+degB}` coefficient is
`(1 + u·degA + w·degB)·a_top·b_top`, and `u,w ≥ 1` makes that factor **strictly
positive**. So `a_top b_top = 0`; feeding back, `A` and `B` are both constant, and
`(P,Q) = (a₀x, b₀y)` or `(a₀y, b₀x)`. ∎

Corroborated independently by brute force over seven mixed-sign weight pairs at total
degree ≤ 5 — 2 Keller branches each, zero nonlinear. The boundary case `ab = 0` is
computed too (not assumed): it collapses to affine-linear.

### What this is worth

- **Path B's success criterion is met.** The separator is a theorem, at every degree,
  with no caveat left implicit.
- **And the separator is narrower than the campaign thought.** It is a statement about
  *mixed-sign* weights only. Alpöge's map has weights `(1,−1,−2)` — mixed — so the
  analogy is intact; but any future argument that quotes "weighted-homogeneous ⟹
  linear" without `ab < 0` is quoting something false.

---

## 3. THEOREM W3-4 / W3-5 — Path A's items A1 and A2, answered

File `39` calls A1 *"the central question"* and says that if the square is **not** forced,
*"there exist equivariant counterexamples whose descent is Keller. That is the construction
recipe … the single highest-value outcome available anywhere in the campaign."* It asks for
*"the general computation with symbolic weights."* Here it is.

### The formula

Every invariant `p` satisfies the Euler relation `Σ wᵢ xᵢ ∂p/∂xᵢ = 0`, so the generating
vector field `ξ = (w₀x₀, …, w_n x_n)` spans `ker(Jπ)` generically. Hence the maximal-minor
vector of `Jπ` is `ξ` times a polynomial **content**:

```
m(π) = D · ξ ,        m(π') = D' · ξ' .
```

> **THEOREM W3-4.** For an equivariant `F` with descent `G` (`G∘π = π'∘F`):
>
> ```
> (det JG)∘π · D  =  (det JF) · (D'∘F).
> ```

Verified in **three weight classes with three different contents** — `D = x²` (Alpöge),
`D = x`, `D = 1` — each with a negative control in which the wrong content breaks the
identity. On Alpöge it reproduces `det JG = −2h²` with `h = f₃/x` exactly.

So the exponent `k` in `det JG = c·h^k` is **not an accident of Alpöge's map**: it is read
off `D` and `D'`, which depend only on the weights.

### The content in closed form — a proof, not a search box

Row `i` of `Jπ` is `(aᵢpᵢ/x, bᵢpᵢ/y, cᵢpᵢ/z)`, so with `e₁, e₂` the exponent vectors of
the two invariant generators,

```
m(π) = (p₁p₂ / xyz) · (Δ₁x, Δ₂y, Δ₃z),      (Δ₁,Δ₂,Δ₃) = e₁ × e₂ .
```

Both generators are invariant, so `e₁·w = e₂·w = 0` and therefore `e₁ × e₂ = λ·w`
(verified: `λ = ±1` on every system). Hence

> **LEMMA W3-4a.** `D = x^{a₁+a₂−1} y^{b₁+b₂−1} z^{c₁+c₂−1}` — a **monomial** determined by
> the weights alone — and
> ```
> k := deg D = deg p₁ + deg p₂ − 3 .
> ```

> **Corollary.** `D = 1` ⟺ `e₁ + e₂ = (1,1,1)` ⟺ the generators are `{x, yz}`, `{y, xz}` or
> `{z, xy}` ⟺ the weight system is `(0,1,−1)`, `(1,0,−1)` or `(1,−1,0)` up to sign.
> `(1,1,1)` has exactly three splittings into two nonzero parts, so this is a **proof for
> all weights**, not an observation inside a search box.

Checked against the computed content on all 144 systems, with a negative control (the same
formula without the `−1` shift, which is rejected).

### The enumeration — the square is NOT forced

All 144 `C*`-weight systems on `C³` with `gcd = 1`, mixed signs or a zero weight, and
invariant ring free on two generators (the generator routine is validated against three
known answers and a negative control):

| `deg D` | `k` | weight systems |
| --- | --- | --- |
| 0 | **0** | exactly `(±1, ∓1, 0)` up to permutation |
| 1 | **1** | e.g. `(1,−1,−1)`, `(1,−2,0)`, `(−1,0,2)` |
| 2 | **2** | includes Alpöge's `(1,−1,−2)`, `D = x²` |

Alpöge: `p₁ = xy`, `p₂ = x²z`, so `k = 2 + 3 − 3 = 2`. `(1,−1,−1)`: `p₁ = xy`, `p₂ = xz`,
`k = 2 + 2 − 3 = 1`. `(1,−1,0)`: `p₁ = xy`, `p₂ = z`, `k = 2 + 1 − 3 = 0`.

**`k = 0` and `k = 1` both occur. A1's "not forced" branch is the live one.**

### But it is not a construction recipe — and that is the interesting part

In the `k = 0` class the equivariant maps can be written down completely. With weights
`(1,−1,0)` and invariants `u = xy`, `v = z`:

```
F = ( x·A(u,v),  y·B(u,v),  C(u,v) )        ⟹        G = ( u·A·B,  C )
```

and — proved symbolically for generic `A,B,C`, plus 8 randomized explicit instances —

```
det JG  =  det JF        identically.
```

So a `C³` Keller counterexample with these weights **is** a plane Keller counterexample
whose first coordinate factors as `u·A·B`. The `k = 0` class opens no new search space; it
is the plane problem wearing a third variable.

**Read as a separator, this is sharper than "the square is forced" — and unlike that, it
is true.** The exponent `k` measures how far a weight class is from being the plane
problem. `k = 0` is the degenerate case where the distance is zero, which is exactly why no
counterexample lives there. Alpöge sits at `k = 2` because the gap has to be positive for
the higher-dimensional problem to be strictly weaker.

A1's stated success condition — *"characterise the weight systems where `k = 0`, then search
for a `C³` counterexample with those weights"* — is answered and closed: the weight systems
are characterised, and searching them is searching the plane.

### A2 — can the square be removed? Alpöge's class, completely

Grading the components of an equivariant map by weight in the `(1,−1,−2)` class:

```
f₃ (weight +1) = x·A(u,v)
f₂ (weight −1) = y·B(u,v) + xz·C(u,v)
f₁ (weight −2) = y²·E(u,v) + z·H(u,v)
```

> **THEOREM W3-5.** `G = ( A²(u²E + vH),  A(uB + vC) )` and `det JG = det JF · A²`.

Verified on 6 random instances, both that the constructed `G` really is the descent and that
the Jacobian identity holds. Alpöge is the specialisation `f₃ = x(2 − 3u − v)`, i.e.
`A = 2 − 3u − v`, giving `det JG = −2A² = −2(3u+v−2)²` — the campaign's `h²`, exactly.

The three A2 bullets, each now *checked* rather than asserted:

- **`h²` is intrinsic.** Under 6 random invertible affine gauges on the quotient, `det JG`
  stays `(constant)·(linear)²` — the factorization type never moves.
- **`G` does not factor as `G'∘σ` with `σ` carrying the whole `h²`.** Such a `σ` would ramify
  to index 3 along `h = 0`, forcing every component of `G` to have order divisible by 3
  there. In adapted coordinates `s = 3u+v−2`, `t = u`, the `s`-exponents are `{2,3}` for `G₁`
  and **`{1,2}` for `G₂`** — order 1, not a multiple of 3. And `G` contracts the whole line
  `h = 0` to the point `(0,0)`.
- **The square vanishes only when `A` is constant.** Then
  `G = (c²(u²E + vH), c(uB + vC))` — an arbitrary plane Keller pair normalised so that
  `G(0,0) = (0,0)` and `∂G₁/∂u(0,0) = 0`, a normalisation any plane Keller map admits by a
  translation and a linear change on the target (`JG(0)` is invertible). So the `A = const`
  sub-class is the plane problem too.

### The unified answer

**Every class in which the descent is Keller turns out to be the plane problem in disguise**
— `k = 0` and `A = const` alike. Alpöge's map is a genuine `C³` counterexample *precisely
because* its descent is not Keller. The obstruction is not a defect of the descent: it is the
exact measure of how much weaker the `C³` problem is than the plane one, and it has to be
non-trivial for a `C³` counterexample to exist at all.

---

## 4. The HIT gate

Wave 1 produced two false-positive hits, both gauge artifacts of broken normalization.
`wave3/w3_hit_protocol.py` is the fix: a single executable gate with six steps —
exactness, Keller (symbolic + exact rational points + modular), non-injectivity by
explicit collision, generic-fiber count by an *independent* resultant computation,
**gauge independence under random invertible affine changes on source and target**
(the step the wave-1 false positives would have failed), and non-vacuity.

The gate refuses to certify anything unless it has first **rejected eight known
negatives** (identity, three tame automorphisms, a linear shear, and three non-Keller
maps) and the Alpöge positive control has fired. Run against everything in this
repository: the Path A descent `G` is correctly **not** a hit — non-injective but not
Keller, `det JG = −2h²`, exactly the obstruction file `39` describes. **No hit is
claimed.**

---

## 5. The claim ledger

`wave3/w3_claim_ledger.py` stores every campaign claim as a record with a stable key,
an **explicit quantifier domain**, a label, an evidence pointer into a certifier, its
dependencies, and — for anything labeled `PROVED` — a **domain probe**: a recorded input
just *outside* the intended domain on which the claim is required to fail.

The linter enforces seven rules (incompatible labels on one key; `PROVED`/`REFUTED`
without evidence; unrestricted domain without a probe; depending on a `REFUTED` claim;
`CONDITIONAL` without naming the condition; missing evidence script; `WITHDRAWN`
without a reason). It is self-tested: exactly seven violation codes on a synthetic
ledger, **zero** on a clean one.

It has already earned its keep twice. It tripped on `NGUYEN-104` labeled `REFUTED` with
no evidence — the honest label is `WITHDRAWN`, because that claim was retracted on
external authority, not by an in-repository artifact, and the two must never be
conflated. And item #11 — the "PROVEN dead, unconditional" vs "conditional on
unreproduced THEOREM 2/3" contradiction — is now a hard error under rule L1 rather than
something two files can disagree about indefinitely.

Current campaign ledger: **16 claims, 0 lint findings.**

---

## 6. On finding a counterexample

Straight answer, unchanged: no counterexample to the plane Jacobian Conjecture was
found, and the reachable search space cannot contain one. Moh closes `deg ≤ 100`; the
campaign's own bound closes every degree pair below 125; the 804 admissible pairs above
125 are unrankable and unrunnable until Path D's two blockers fall together. Any
low-degree sweep — including Path B's B2 as written, at total degree ≤ 12 — is
*provably* empty before it starts, and running it would be exactly the failure Path B's
own B1 warns about.

What *was* found is a counterexample to a claim the campaign has been standing on since
Session 38, and it took one line: `(x, y + x²)`. That is the second load-bearing
statement in three sessions to be false because its hypotheses lived in the experiment
and not in the sentence. **The productive target is not the conjecture; it is the
campaign's own record**, and the domain-probe rule now makes that class of error expensive
to commit and cheap to catch.

---

## What changed since wave 2

1. **Second Framework `D = 23`: OPEN → DEAD** (for every `k ≠ 23`), by W3-1. Wave 2's
   label is superseded.
2. **First Framework (99,66): CONDITIONAL → unconditional on the pole question.**
   The dependence on Theorem 3's pole-fiber step is removed; the branch that step never
   excluded is killed directly.
3. **Session 38's collapse: bounded-degree evidence → a theorem, with the missing
   hypothesis exhibited.** Path B's success criterion met; a false unrestricted
   version of the claim retired.
4. **Path A's A1 and A2: open → answered.** The square is not forced; the `k = 0` weight
   systems are characterised (with a proof, not a search box); Alpöge's class is described
   in closed form; and the reason none of it yields a counterexample is that every
   Keller-descent class *is* the plane problem. The campaign's "single highest-value
   outcome" is resolved in the negative, with a formula that explains why.
5. **Detector discipline: closed.** The HIT gate cannot certify without first rejecting
   known negatives.
6. **Record discipline: closed.** Contradictions and dropped hypotheses are now lint
   errors, not prose.

## Still open, honestly

- **§2.5 irreducibility** — `UNVERIFIED-HERE`; machinery ready, artifact absent.
- **#9 parameter count** — `ASSERTED`; needs an explicit gauge enumeration and a rank
  computation before it may be used.
- **#10 pentagon bound** — withdrawn; needs a validated sparsity model or a diagnosed
  failed construction.
- **The conjecture itself.** Unchanged, and no session of this kind is going to change it.
