# Wave 3 — Findings

**Branch:** `claude/opus-errors-false-proofs-820rmd`

Wave 2 broke a theorem. Wave 3 does the follow-through the plan called for: work out
whether the break is load-bearing, repair what can be repaired, and find the next
thing that is wrong. Two new theorems, one of them a genuine counterexample to a
claim the campaign has been leaning on since Session 38.

```
python3 wave2/run_all.py        # runs all ten certifiers, exit 0 iff all pass
```

**10/10 certifiers, 192/192 individual checks, 0 rigged checks in tree, 0 ledger lint
findings.**

| certifier | checks | verdict |
| --- | --- | --- |
| `wave3/w3_endgame_degree_obstruction.py` | 32/32 | **THEOREM W3-1** — repairs the First Framework proof outright |
| `wave3/w3_weighted_homogeneous_theorem.py` | 66/66 | **THEOREM W3-2 / W3-3** — Session 38's collapse, made a theorem *and* refuted as stated |
| `wave3/w3_hit_protocol.py` | 12/12 | HIT gate implemented and validated; no hit in this repository |
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

## 3. The HIT gate

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

## 4. The claim ledger

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

## 5. On finding a counterexample

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
4. **Detector discipline: closed.** The HIT gate cannot certify without first rejecting
   known negatives.
5. **Record discipline: closed.** Contradictions and dropped hypotheses are now lint
   errors, not prose.

## Still open, honestly

- **§2.5 irreducibility** — `UNVERIFIED-HERE`; machinery ready, artifact absent.
- **#9 parameter count** — `ASSERTED`; needs an explicit gauge enumeration and a rank
  computation before it may be used.
- **#10 pentagon bound** — withdrawn; needs a validated sparsity model or a diagnosed
  failed construction.
- **The conjecture itself.** Unchanged, and no session of this kind is going to change it.
