# Does Valqui–Ramírez 2025 attack the open (8,28) sub-case? — Verified findings

**Scope.** This note answers the five questions about the 2025 Ramírez/Valqui Gröbner-basis
paper, tagging every claim `[VERIFIED: source]` (I fetched/read the primary text myself),
`[SECONDARY: source]` (read a source once removed — abstract page, citing summary), or
`[MEMORY, unverified]`. Nothing here is inferred from the paper's title alone; every
substantive claim about its content comes from a direct read of the cached full text
(arXiv `.txt` from `pdftotext`) or a live re-fetch.

**Bottom line up front: NO.** The paper is real, it exists, it is exactly what the sweep
found — but it does not attack, mention, or bear technically on the open `(8,28)` /
`(72,108)` sub-case of GGHV `arXiv:2204.14178`. It is a self-contained computational-algebra
exercise on a *different, much smaller* member of the same abstract family, and its own
"Final Remark" (published-version only) states that its result was already classically known.
**This paper does not shorten the path to deciding `(8,28)`.**

---

## 0. Paper identity (two co-existing versions, same content + one added remark)

| | arXiv preprint | Journal version |
|---|---|---|
| Title | "The Groebner basis and solution set of a polynomial system related to the Jacobian conjecture" | identical |
| Authors | Valeria Ramírez, Christian Valqui | Christian Valqui, Valeria Ramírez |
| ID | `arXiv:2506.05697` [math.AG, math.AC] | *Pro Mathematica* **33**(65) (2024/2025 issue), pp. 50–67 |
| Submitted / published | 6 Jun 2025, **v1 only** (checked live; no v2 exists) | Received Mar/Jun 2025, **accepted October 2025**, published online **5 Nov 2025** |
| DOI | none (arXiv only) | `10.18800/promathematica.202401.003` |
| Length | 9 pages | ~17 pages (journal typesetting) |
| Cached at | `.../scratchpad/ramirez_valqui_2025.{pdf,txt}` = `ramirez_valqui_2506.05697.{pdf,txt}` (byte-identical, MD5 `be10e1e2283f5672654fbfef03c4b32c`) | `.../scratchpad/valqui_ramirez_2024.{pdf,txt}` |

[VERIFIED: both files read in full; arXiv abstract page and the PUCP *Pro Mathematica* journal
page (`revistas.pucp.edu.pe/.../view/32277`) fetched live 2026-08-12 and cross-checked against
the cached PDFs — title, authors, page numbers, and DOI all match.]

**Important: the two versions are not textually identical.** The mathematical content
(theorems/propositions/proofs) is the same, just renumbered (arXiv Thm 1.1 → journal Thm 2.1,
arXiv Prop 2.1 → journal Prop 3.1, etc.). But the **journal version adds one paragraph — a
"Final Remark" — that is absent from the arXiv v1 text.** That paragraph turns out to contain
the single most important sentence in the whole paper (§2 below). Anyone working only from the
arXiv PDF will miss it.

Reference [2]/[5] cited throughout (for the general framework and Theorem 1.1/2.1) is
**Guccione–Guccione–Valqui, "A system of polynomial equations related to the Jacobian
conjecture," `arXiv:1406.0886`** (2014) — **not** the 2022 GGHV paper. The 2025 paper's entire
bibliography is two items (arXiv version: Cox–Little–O'Shea's textbook, and 1406.0886) or ten
items (journal version, adding Abhyankar, Formanek, Heitmann, Keller, Moh, Solórzano–Valqui,
Zannier). **`arXiv:2204.14178` (GGHV 2022) appears in neither reference list, in either
version.** [VERIFIED: full reference lists read in both files.]

---

## 1. Does it attack the open (8,28) sub-case? — **No**

Grepped the complete text of both versions for every marker of the (8,28) problem as GGHV 2022
states it: `72`, `108`, `125`, `Newton`, `polygon`, `shape`, `corner`, `bracket`, `[P,Q]`, and
the specific case labels `(7,21)`, `(9,27)`, `(8,28)`, `(9,24)`, `(8,24)`, `(8,32)`, `(5,20)`.

**Zero matches, in either version, for any of these.** [VERIFIED: `Grep` over both cached
`.txt` files] The only "matches" are false positives (`(C 3 )−1` numbering, page-footer numbers
like "Pro Mathematica, 33, 65 (2024), 50-67").

What the paper actually studies is a narrower slice of the *general* framework already stated
in the 2014 Guccione–Guccione–Valqui paper (`1406.0886`, their Theorem 1.9), which the 2025
paper restates as its own Theorem 1.1/2.1:

> "The Jacobian conjecture in dimension two is false if and only if there exist P, Q ∈ K[x, y]
> and C, F ∈ K[y]((x⁻¹)), n, m ∈ ℕ such that n ∤ m and m ∤ n, νᵢ ∈ K (i = 0,...,m+n−2) with
> ν₀ = 1, such that C has the form C = x + C₋₁x⁻¹ + C₋₂x⁻² + ⋯ with each C₋ᵢ ∈ K[y], gr(C) = 1
> and gr(F) = 2 − n, ... F₊ = x¹⁻ⁿy, ... and Cⁿ = P and Q = Σᵢ νᵢCᵐ⁻ⁱ + F. Furthermore, under
> these conditions (P, Q) is a counterexample to the Jacobian conjecture."
> — [VERIFIED, `ramirez_valqui_2025.txt` lines 18–29]

The 2025 paper then explicitly restricts to one tiny corner of this family:

> "In this paper we compute such a Groebner basis of (1.1) in a very particular case: we
> assume **n = 3, m = 3r + 1 or m = 3r + 2 for some integer r > 0, and νᵢ = 0 for i > 0**.
> Moreover we consider D = ℂ[y] and F₁₋ₙ = y, as in Theorem 1.1."
> — [VERIFIED, `ramirez_valqui_2025.txt` lines 107–109]

Because `Cⁿ = P` with `gr(C) = 1`, **n here is literally `deg(P)`** — not a reduced/coprime
abstraction of a large degree pair. `n = 3` means the hypothetical counterexample this family
could produce has `deg(P) = 3`. That is a different universe of scale from `deg(P) = 72`
(or `108`). The journal version's own concluding remark makes this explicit and is the
decisive piece of evidence (§2, `[VERIFIED]`, quoted in full there).

The journal-version introduction independently states what this method *has* been used for
historically, and it is not `(72,108)`:

> "The usefulness of this method is shown in the last section of [5], where the method is
> illustrated with the case (n, m) = (50, 75), showing—via a degree-reduction technique as
> in [4]—that no counterexample arises."
> — [VERIFIED, `valqui_ramirez_2024.txt` lines 70–73]

`(50, 75)` is one of **T. T. Moh's original four exceptional pairs** (`(48,64), (50,75),
(56,84), (66,99)`, all below degree 101) — already resolved decades ago, and moreover this
sentence describes what the *2014* paper [5] did, not new work in the 2025 paper itself. The
2025 paper's own novel content is the deg-P=3 Gröbner computation, not a new attack on any
Moh-era or GGHV-era hard case.

**Corroboration:** an earlier, independent sweep already run in this repo (see
`jc2_literature_sweep_partial.md`, three merged sub-reports) reached the identical conclusion
via the same grep-based method, and this note reaches it a second, independent way (via the
Final Remark, §2, and via the direct (n,m)-role bookkeeping, §5). Three independent
readings agree.

---

## 2. The decisive sentence — the paper's own verdict on its result

This is the single most important quote in this investigation, and it exists **only in the
journal version** (not the arXiv preprint):

> **"Final Remark.** The solution sets arising in the four cases reveal that no solution
> exists in K[y], whereas all solutions lie in K(y^{1/(m+2)}). This, in turn, implies that
> there is no counterexample (P, Q) to the Jacobian Conjecture with deg(P) = 3 and
> 3 ∤ deg(Q). **Although this fact is already known**—for instance, because no counterexample
> can occur when gcd(deg(P), deg(Q)) = 1—a more detailed analysis of the corresponding
> Gröbner bases in broader settings may still yield new insights toward a proof or disproof
> of the Jacobian Conjecture."
> — [VERIFIED, `valqui_ramirez_2024.txt` lines 824–834]

Three things follow directly from this, in the authors' own words:

1. **Every solution the paper's method actually finds requires adjoining a `(m+2)`-th root of
   `y`** (fractional/multi-valued), i.e. is *not* an honest element of `D = K[y]` as
   Theorem 1.1/2.1 requires for a genuine counterexample. This matches what a term-by-term
   read of Propositions 3.2/3.4/3.5/3.6 already shows (every explicit solution is of the form
   `C₋₁ = (−y/λ)^{1/j}` or similar, `j ≥ 2` for every `m > 3` in the family) — I derived this
   independently before finding the remark that confirms it.
2. **The one number this paper's method rules out (`deg P = 3`) is a case the authors
   themselves say was already excluded by classical means** (elementary: `deg(P) = 3` forces
   `gcd(deg P, deg Q) = 1` whenever `3 ∤ deg Q`, and it is classical, decades-old folklore
   that a coprime-degree Jacobian pair cannot be a counterexample). The paper does not claim a
   new non-existence result, and explicitly disclaims novelty for the one number-theoretic
   consequence it does draw.
3. The forward-looking sentence — "a more detailed analysis... in broader settings may still
   yield new insights" — is an aspiration for future work, not a claim that this paper, or any
   sequel, has done that broader analysis. No sequel exists (checked; see §6 below).

---

## 3. Does it write down a polynomial system for (8,28), or a general one usable by a Gröbner engine? — Partially; general, but not (8,28)-specific, and only half-solved

It writes down, precisely, the **general system** `S(n, m, (νᵢ), F₁₋ₙ)` from the 2014 paper —
this is the "form that could be handed to a Groebner engine" in the abstract sense the task
asks about — then a fully-explicit specialization at `n = 3, νᵢ = 0 (i>0), F₁₋ₙ = y`. Transcribed
exactly [VERIFIED, `ramirez_valqui_2025.txt` lines 93–104, 122–138]:

```
E_k   := (C^n)_{-k} = 0,                              for k = 1, ..., m-1,
E_{m-1+k} := ( Σ_{i=0}^{m+n-2} ν_i C^{m-i} )_{-k} = 0, for k = 1, ..., n-2,
E_{m+n-2} := ( Σ_{i=0}^{m+n-2} ν_i C^{m-i} )_{1-n} + F_{1-n} = 0
```
with `m+n-2` equations in `m+n-2` unknowns `C_{-1}, ..., C_{-(m+n-2)}`. Specialized to
`n=3, ν_i=0 (i>0), F_{1-n}=y`, this becomes (their eq. 2.1, `E_1` through `E_{m+1}`, `m+1`
equations in `C_{-1},...,C_{-(m+1)}, y`):

```
E_1  = 3C_{-1}^2 + 3C_{-3}
E_2  = 6C_{-1}C_{-2} + 3C_{-4}
E_3  = C_{-1}^3 + 3C_{-2}^2 + 6C_{-1}C_{-3} + 3C_{-5}
E_4  = 3C_{-1}^2 C_{-2} + 6C_{-2}C_{-3} + 6C_{-1}C_{-4} + 3C_{-6}
E_5  = 3C_{-1}C_{-2}^2 + 3C_{-1}^2 C_{-3} + 3C_{-3}^2 + 6C_{-2}C_{-4} + 6C_{-1}C_{-5} + 3C_{-7}
  ...  [recursive closed form given for general E_k, eq. (2.3)-(2.4)]
E_{m-1} = (C^3)_{1-m}
E_m     = (C^m)_{-1}
E_{m+1} = (C^m)_{-2} + y
```
Ideal `I = ⟨E_1,...,E_{m+1}⟩ ⊂ ℂ[C_{-1},...,C_{-(m+1)}, y]`. This is exact and fully general
for the `n=3, ν_{>0}=0` slice, for **any** `m` not divisible by 3.

**What is NOT provided:** a system for `(8,28)` itself. As GGHV 2022 states it (Proposition 4.3,
transcribed in full in §5 below), the `(8,28)` case requires `[P,Q] = x²` (not the implicit
`[P,Q]=1↦` bracket structure this paper's `F₁₋ₙ=y, ν_{>0}=0` slice encodes) and a Newton
polygon with *extra* corners that force **nonzero intermediate `νᵢ`'s and a non-trivial
`F₁₋ₙ`** (not just `y`) — exactly the generality this paper explicitly declines to treat. No
transcription of an `(8,28)`-specific system exists anywhere in either version of this paper.

**And even for its own chosen slice, the system is only half-solved.** The paper proves a
Gröbner basis in fully explicit recursive form only for the **sub-ideal**
`I_{m-1} = ⟨E_1,...,E_{m-1}⟩` (Proposition 2.1/3.1: each reduced basis element has the closed
shape `Ẽ_k = C_{-(k+2)} + R_k(C_{-1}, C_{-2})`, a polynomial in only two variables) — and even
there, **no closed formula for `R_k` at general `k` is given**; only `R_1,...,R_5` are computed
explicitly [VERIFIED, lines 245–261]:
```
Ẽ_1 = C_{-3} + C_{-1}^2
Ẽ_2 = C_{-4} + 2C_{-1}C_{-2}
Ẽ_3 = C_{-5} + C_{-2}^2 - (5/3)C_{-1}^3
Ẽ_4 = C_{-6} - 5C_{-1}^2 C_{-2}
Ẽ_5 = C_{-7} + (10/3)C_{-1}^4 - 5C_{-1}C_{-2}^2
```
The last two equations `E_m, E_{m+1}` (the ones that actually encode "`Q` is a polynomial," the
substantive constraint) are *not* put through Buchberger's algorithm to a basis — they're
reduced modulo the `I_{m-1}` basis to two bivariate equations in `C_{-1}, C_{-2}` (eq. 3.7–3.8),
and the paper then solves *those* by case-splitting (zero/nonzero, parity of `m`) rather than by
further Gröbner elimination.

---

## 4. Does it publish the (9,27)-style reduction technique in reusable general form? — **No**

This is the sharpest "no" of the five questions. The technique GGHV 2022 §5 actually uses to
**close** the sibling `(9,27)` case (verbatim, closed sub-case) — quoted here to show exactly
how much heavier it is than anything in the 2025 paper:

- Build `C` with `C² = P` by an **inductive construction controlled by two different,
  simultaneously-tracked valuations** (`v₋₁,₁` embedding `K[y,C₃⁻¹] ⊂ K((y⁻¹))` and `v₃,₋₁`
  embedding it in `K((y))`) — needed because the relevant series lives on *both* ends of the
  Newton polygon at once. [VERIFIED, `gghv2022.txt` lines 667–757, Proposition 5.2]
- Use the **actual bracket relation `[P,Q]=x`** (not just leading-term combinatorics) to force
  an auxiliary function `f₁ := C₃³F₋₄` to satisfy an honest **ODE**:
  `y⁹(y+1)² = 6y(y+1)f₁′ − 10(9y+8)f₁`, stated to have "a unique solution that can be found
  using a CAS" [VERIFIED, lines 791–819].
- Transform the (non-polynomial) `Cₖ` into genuine polynomials `Dₖ := Cₖ C₃^{5−2k} ∈ K[y]`
  (Proposition 5.5), apply a **second** automorphism `φ(x) = x − D₂`, and only then arrive at a
  9-equation system in variables `d₋₁₀,...,d₁`, of which the paper says: "using a CAS (for
  example Mathematica) we eliminate the variables `d₋₁₀, d₋₈,...,d₋₂`, obtaining" a single
  equation (5.9). [VERIFIED, lines 892–913]
- Close the contradiction via **two-sided degree/valuation bounds** (Proposition 5.6:
  `v₋₁₃,₋₁(D)=−39`, `v₁₇,₁(D)=51`) forcing a divisibility argument that cannot be satisfied
  (lines 914–981).

**None of this — two-sided valuations, the bracket-derived ODE, the second automorphism shift,
the `Dₖ`/`dₖ` transform, the final valuation-bound contradiction — appears anywhere in the 2025
paper.** Grepped for "differential equation," "ODE," "valuation," "bracket," `[P,Q]`: zero hits
in either version [VERIFIED]. The 2025 paper's own technique is much simpler *because* it
chose the `νᵢ=0` slice specifically: with all intermediate `νᵢ` zero, each `Eₖ`'s leading
monomial is a single new variable `C_{-(k+2)}`, so pairwise leading terms are automatically
coprime, and the S-polynomial criterion (Cox–Little–O'Shea Prop. 2.9.4) discharges the whole
Gröbner-basis proof by a one-line divisibility argument [VERIFIED, lines 211–226]. That
shortcut is *exactly* unavailable for `(8,28)`, whose Newton polygon (extra corners at
`(8,14)/(8,16)` for `P` and `(12,21)/(12,24)` for `Q`, plus the `[P,Q]=x²` bracket) forces
nonzero `νᵢ`'s and hence a genuinely entangled leading-term structure — the situation the
`(9,27)` proof needed the heavy machinery above to handle.

This repo's own prior analysis of GGHV 2022 (`jc2_gghv_system.md`, written before this task)
reaches the same conclusion about the *source* paper independently: "That five-page reduction
has no analogue anywhere in the paper for Case (8,28)." The 2025 paper does not fill that gap
either — it is not a generalization of the §5 technique at all, it is an application of a much
older, simpler technique (Buchberger + S-polynomial coprimality) to a family where that
simpler technique happens to suffice.

---

## 5. Groebner tooling, orderings, field, system sizes, timings — reported: **none computational**

**This is a pen-and-paper Gröbner basis, not a computer-algebra-system run.** Grepped both
versions for `Singular|Macaulay|Magma|CoCoA|Maple|Mathematica|CAS|computation time|seconds|
minutes|CPU|memory|runtime`: **zero hits** in either version (the only "CAS" substring matches
are inside the word "CASE") [VERIFIED]. Compare this to GGHV 2022 §5, which explicitly invokes
"a CAS (for example Mathematica)" *twice* for its elimination steps — the 2025 paper contains no
such invocation anywhere. Proposition 2.1/3.1's Gröbner basis is derived by citing three
general theorems from Cox–Little–O'Shea (*Ideals, Varieties, and Algorithms*, their
Propositions 2.9.4, 2.7.6, Theorem 2.9.3 — the standard S-polynomial/Buchberger-criterion
machinery) and applying them symbolically. No software is named, run, or benchmarked.

What *is* specified precisely:
- **Field**: `D = ℂ[y]` (`K[y]` for general characteristic-0 `K` in the abstract statement);
  the explicit small-`k` coefficients (`R_1,...,R_5`) are rational (`Q[C_{-1},C_{-2}]`,
  stated explicitly in the proof of Prop. 2.1/3.1).
- **Monomial order**: weighted degree-reverse-lexicographic, with weight `w(C_{-i}) = i+1`,
  `w(y) = m+2`, given as an explicit `(m+2)×(m+2)` order matrix on the variables
  `C_{-(m+1)}, C_{-m}, ..., C_{-1}, y` [VERIFIED, lines 176–197].
- **System size**: parametric in `m` — `m+1` equations, `m+1` unknowns (plus `y`), for
  arbitrary `m ≢ 0 (mod 3)`. No concrete `m` is ever instantiated numerically in the paper
  (everything stays symbolic in `m`); there is no worked example at, say, `m=100` to gauge
  actual coefficient blow-up.
- **Timings: none reported, at any system size.** There is nothing here that "tells us what is
  actually feasible" computationally — the whole point of the paper's chosen slice is that it's
  provably tractable *by hand*, precisely because it avoids needing a computer at all.

---

## 6. Does it move the degree bound, or report new excluded families? — **No, and it says so itself**

No mention of `100`, `108`, `125`, or any Moh/GGHV degree-pair ladder rung anywhere in either
version [VERIFIED, full-text grep]. The one number-theoretic consequence it draws — "no
counterexample with `deg(P)=3` and `3 ∤ deg(Q)`" — is explicitly self-flagged by the authors as
**already known** (§2 above, verbatim). No new excluded family, no bound movement, no claim of
either. This is, by the authors' own words, a methodology/machinery paper, not a results paper
in the degree-bound sense the task cares about.

---

## 7. Any OTHER 2023–2026 paper publishing a usable general form of the (9,27)-style reduction?

Checked systematically (arXiv author-listing enumeration for Guccione/Guccione/Horruitiner/
Valqui — 39 hits for Valqui alone, manually reviewed; Semantic-Scholar citation graph for
`2204.14178`; targeted greps of every cached 2023–2026 JC-adjacent paper in the scratchpad for
"Groebner," "72,108," "(8,28)," "Guccione," "Horruitiner," "Valqui," "125"). **Found nothing
that publishes a general/reusable form of the bracket→ODE→eliminate technique.** Specifically:

- **Solórzano & Valqui, "The Groebner basis of a polynomial system," Pro-Mathematica 28 (2014),
  25–40 (`arXiv:1409.6390`)** — cited by the 2025 paper itself as reference [9]/prior work,
  doing the analogous `n=2` case. Pre-dates the task's 2023–2026 window by nearly a decade;
  same limitation (no engagement with `(72,108)`/`(8,28)`).
- **T. Shaska, "Graded Keller maps and the Jacobian Conjecture," `arXiv:2607.20210`** (Jul 2026)
  — [VERIFIED: cached text grepped] zero mentions of Groebner bases, `(72,108)`, or any GGHV
  citation; a structural symmetry result on an unrelated axis.
- **Nguyen, `arXiv:1902.05923`, v5 (2025), *Quaestiones Mathematicae*** — [VERIFIED] cites
  GGHV 2022 in its bibliography but its own method is classical Newton–Puiseux/gcd arguments,
  not Gröbner bases; reaches a *weaker* bound (degree ≤ 104) and does not engage `(72,108)`.
- **Guccione, Guccione, Valqui, "The lower side of the Newton polygon of hypothetical
  counterexamples to the plane Jacobian conjecture," *Quaestiones Mathematicae*, published
  online 28 Jul 2026, DOI `10.2989/16073606.2026.2701437`** — genuinely on-topic by title and
  authorship (three of the four GGHV-2022 authors, missing Horruitiner), but **paywalled; only
  the abstract could be retrieved** [SECONDARY: abstract via publisher page, full text not
  accessible]:
  > "We prove that if the Jacobian conjecture in two variables is false and (P, Q) is a
  > counterexample that is a standard (m, n)-pair, then the Newton polygon HH(P) of P must
  > satisfy several restrictions that had not been found previously. This allows us to discard
  > some of the corners found in [16, Remark 7.9]..., together with some of the infinite
  > families found in [9, Theorem 2.25]."

  Two red flags argue this is **not** new 2026 work and **not** Gröbner-based: (1) it does not
  cite `arXiv:2204.14178` anywhere in its reference list (implausible for genuinely new work by
  three of that paper's own four authors, extending exactly this line); (2) its abstract is a
  near-verbatim match for the much older `arXiv:1605.09430` ("The two-dimensional Jacobian
  conjecture and the lower side of the Newton polygon," 2016) — "the Newton polygon HH(P) of P
  must satisfy several restrictions that had not been found previously" appears in both. This
  looks like a decade-delayed journal publication of 2016-vintage structural work, not a fresh
  attack — but this is inference from metadata, **not confirmed against the paywalled body**.
  **Flagging as the one open lead worth institutional-access follow-up**, while noting it is
  explicitly *not* Gröbner-basis machinery (no "Groebner" in title/abstract/keywords) even in
  the best case.

**No other candidate surfaced.** No SAT/computer-algebra attack on JC2 was found anywhere in
the 2023–2026 literature searched.

---

## 8. Why (8,28) structurally falls outside this paper's chosen slice [my own analysis, not stated by either paper]

GGHV 2022 Proposition 4.3 fixes the reduced shape for `(8,28)` with exponent pair
`(m,n)_{§4} = (3,2)` (`P` associated to the local exponent `3`, `Q` to `2`) — matching the
sibling `(9,27)` case's `(m,n)_{§4} = (2,3)` with the roles of `P,Q` swapped. Carried into the
2025 paper's own `Theorem 1.1` letters (`Cⁿ=P`, so `n_{Thm1.1}` is `P`'s exponent; leading term
of `Q` is `C^m`, so `m_{Thm1.1}` is `Q`'s exponent), this gives:

| Case | `n_{Thm1.1}` (P's exponent) | `m_{Thm1.1}` (Q's exponent) |
|---|---|---|
| `(9,27)` — **closed**, via the heavy §5 machinery, `[P,Q]=x` | 2 | 3 |
| `(8,28)` — **open**, Prop. 4.3 only, `[P,Q]=x²` | **3** | **2** |

So `(8,28)` really would sit at `n=3` in this paper's own notation — but at `m=2`, squarely
**outside** the paper's stated range `m = 3r+1` or `3r+2` for `r > 0` (i.e. `m ≥ 4`; `m=2`
would need `r=0`, explicitly excluded). Even setting that boundary case aside, the `(8,28)`
system needs nonzero intermediate `νᵢ`'s and a non-trivial `F₁₋ₙ` (its Newton polygon has extra
corners the `Q = Cᵐ + F` shape with `F₁₋ₙ=y` cannot produce) — a second, independent reason the
2025 paper's `νᵢ=0` slice cannot reach it, on top of the `m` boundary. Both obstructions would
need to be separately re-derived to adapt this paper's method to `(8,28)`; neither adaptation
exists in the literature.

---

## 9. Context found along the way (does not change the verdict above)

**A completely different, dimension-≥3 result exists and is unrelated to JC2.** Multiple
independent sources (Terence Tao's blog, `arXiv:2608.00222` Shuhong Gao, `arXiv:2607.20210`
Shaska) report that the **general** (`n≥3`-dimensional) Jacobian conjecture was refuted in
July 2026 (Alpöge, with follow-ups by Gallagher and Speyer), with AI assistance credited to a
model referred to as "Claude Fable 5." I independently pulled and read the abstract of
`arXiv:2608.00222` via `pdftotext`: it states the construction exists "only in dimension ≥ 3"
and explicitly disclaims relevance to the plane case. **This has zero bearing on JC2/`(72,108)`
either way** — every primary source checked (including this paper's own §2) says the
two-dimensional case is untouched and still open. One note of caution surfaced by a sibling
sweep in this repo: the arXiv identifier `2608.00222` (month prefix "08") combined with a
stated "31 Jul 2026" submission date is an internal inconsistency worth a raised eyebrow (arXiv
IDs' `YYMM` prefix should reflect the actual submission month) — though this is also explainable
by ordinary lag between a PDF's "date written" and its actual arXiv submission, so it is not
dispositive either way. **I did not audit this claim further — it is out of scope for this
task and irrelevant to the verdict regardless of its ultimate disposition**, since even the
"fully verified real" reading of events leaves JC2 exactly as open as GGHV 2022 left it.

**This repo already has an independent, unpublished, in-progress attempt at `(8,28)` itself.**
The shared scratchpad contains Singular scripts (`gghv_open1.sing`, `gghv_open2.sing`) and a
reduction log (`reduce.log`) explicitly labeled `"CASE open2: open case (2) [Prop 4.3, sub-case
2; no y-axis edge]"` — i.e., a direct, from-scratch attempt to build the actual `(8,28)`
coefficient system (72 unknowns / 92 equations for one sub-case) and run Buchberger's algorithm
on it over `GF(32003)`, plus a partial hand-reduction (monomial kills / linear solves through
step `r11`). This is **this campaign's own unpublished work, not literature**, its completion
status is unclear (the captured log shows only the setup header, no completed run), and I did
not attempt to continue or verify it — it is out of scope for this literature-verification task,
but it means the team does not need the 2025 paper's machinery to already be pursuing a direct
Gröbner attack on the real system; that attack is already independently underway and is not
what this paper offers.

---

## Sources consulted directly (all cached under
`/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/`)

| File | What it is | How used here |
|---|---|---|
| `ramirez_valqui_2025.txt` = `ramirez_valqui_2506.05697.txt` | arXiv:2506.05697 v1, full text | primary source, §§1–6 |
| `valqui_ramirez_2024.txt` | *Pro Mathematica* 33(65) published version, full text | primary source; source of the decisive Final Remark, §2 |
| `gghv2022.txt` = `gghv_2204.14178.txt` = `main_2204.14178.txt` | arXiv:2204.14178 (GGHV 2022), full text | source of Prop. 4.1/4.3, Thm 5.1, the "couldn't solve" quote |
| `jina_newton2026.txt` | Publisher abstract page, DOI 10.2989/16073606.2026.2701437 | §7 (paywalled 2026 paper) |
| `gao_2608.00222.txt` / direct `pdftotext` re-extraction | arXiv:2608.00222, Shuhong Gao | §9 (dimension≥3 context, verified out-of-scope) |
| `valqui_all.xml` | Live arXiv API author listing for "Valqui", 39 entries | §7 (author-exhaustive check) |
| Live fetches 2026-08-12: `arxiv.org/abs/2506.05697`, `arxiv.org/abs/2204.14178`, `doi.org/10.18800/promathematica.202401.003` → `revistas.pucp.edu.pe/.../32277` | version/publication confirmation | §0 |

Also cross-checked against this repo's own prior work: `jc2_literature_sweep_partial.md`
(three merged sub-reports, independently reaching the same "no" on Q1/Q5) and
`jc2_gghv_system.md` (independently reaching the same "no" on Q3, for the source 2022 paper).
