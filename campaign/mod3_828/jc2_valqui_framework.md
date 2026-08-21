# Does arXiv:1409.6390 (Valqui–Solórzano) bear on the open (8,28) sub-case?

**Scope.** Primary target: arXiv:1409.6390, "The Groebner basis of a polynomial
system" (Christian Valqui, Marco Solórzano, 2014) — never previously examined in
this repo. Secondary task: re-confirm `jc2_ramirez_valqui_2025.md` (arXiv:2506.05697)
is internally consistent and that its stated greps were actually performed.
Every claim below is tagged `[VERIFIED: source]` (I fetched/read/grepped the
primary text myself, this session), `[SECONDARY: source]` (one step removed —
citation text, abstract page), or `[MEMORY, unverified]`.

---

## 0. Bottom line

**arXiv:1409.6390 does not touch, generalize to, or provide a usable system for
the (8,28) sub-case.** It computes a closed-form Gröbner basis for exactly one
narrow, fully specified corner of the general framework — `n = 2` fixed,
`m` any odd number `≥ 3`, and the "homogeneous" restriction `λᵢ = 0` for `i > 0`
— and states this scope explicitly in its own text. Neither of the two possible
readings of "(n,m)" that could connect it to (72,108)/(8,28) lines up: taken as
the paper's own literal `n = deg(P)`, `m = deg(Q)`, `n=2` is nowhere near `72` or
`108`; taken as GGHV22's internal corner-table label `(m,n)=(3,2)` for the (8,28)
row, that label denotes a different, already-reduced object (see §3) that the
paper's own Theorem 1.1 doesn't describe in the first place, and — new finding,
§4 — is not even the template GGHV22's *own* successful (9,27) reduction
literally instantiates. The paper reports **zero** computational tooling and
**zero** timings anywhere (§6); its tractability comes entirely from a structural
sparsity (`λᵢ=0`) that this repo's own prior analysis of GGHV22 (`jc2_gghv_system.md`,
`jc2_ramirez_valqui_2025.md`) has already shown Proposition 4.3's Newton polygon
does **not** have. GGHV22 (arXiv:2204.14178) does not cite it, and it cannot cite
GGHV22 (predates it by 7.5 years) — checked directly in both bibliographies (§5).

**This paper does not change the current direct attack on (8,28), does not
validate it beyond what was already known, and sits essentially orthogonal to
it** — full verdict restated at the end.

---

## 1. Paper identity — verified metadata

| Field | Value | Source |
|---|---|---|
| Title | "The Groebner basis of a polynomial system" | [VERIFIED: arXiv abstract page, live fetch; PDF title line] |
| Authors | Christian Valqui, Marco Solórzano | [VERIFIED: same] |
| arXiv ID | 1409.6390, **v1 only** (no v2 exists) | [VERIFIED: live arXiv abstract page + arXiv API author-listing XML `valqui_all.xml`, both fetched this session] |
| Submitted | 23 Sep 2014 | [VERIFIED: PDF header "arXiv:1409.6390v1 [math.AC] 23 Sep 2014"; arXiv submission history] |
| Subject | math.AC (Commutative Algebra) | [VERIFIED: arXiv abstract page] |
| MSC | Primary 14R15; Secondary 13F20, 11B99 | [VERIFIED: arXiv abstract page] |
| Comment | "From the Magister Thesis of Marco Solorzano" | [VERIFIED: arXiv abstract page] |
| Journal ref | *Promathematica* Vol. 28, No. 55, p. 24–40 (2014) | [VERIFIED: arXiv abstract page] |
| Abstract | "We compute the Groebner basis of a system of polynomial equations related to the Jacobian conjecture using a recursive formula for the Catalan numbers." | [VERIFIED: arXiv abstract page + PDF] |
| Semantic Scholar citationCount | **0** | [VERIFIED: live S2 Graph API query, `arXiv:1409.6390`, cached at `scratchpad/s2_1409_6390.json`] |

Downloaded PDF and ran `pdftotext -layout`; both cached at
`/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/solorzano_valqui_1409.6390.{pdf,txt}`
(9 pages, 653 text lines).

**Where it sits in the lineage** (all directly verified this session):

```
1406.0886 (Guccione, Guccione, Valqui, Jun 2014, v1)
  "A system of polynomial equations related to the Jacobian Conjecture"
  -> Theorem 1.9: defines the general system St(n,m,(λi),F1-n)
  -> Section 3: "The homogeneous system S(n,m,F1-n)" (λi=0 case), qualitative
     study only — existence/finiteness, no Gröbner basis computed
        |
        | cited as [2] (Theorem 1.1 restated verbatim)
        v
1409.6390 (Valqui, Solórzano, Sep 2014)  <-- TARGET
  "The Groebner basis of a polynomial system"
  -> computes an EXPLICIT closed-form Gröbner basis for the homogeneous
     system at n=2, any odd m, via a Catalan-number recursion
        |
        | cited as [9] (journal version only)
        v
2506.05697 / Pro Mathematica 33(65) (Ramírez, Valqui, 2025)
  "The Groebner basis and solution set of a polynomial system..."
  -> does the analogous computation at n=3 (weaker: no closed formula for
     general k, only R1..R5 computed by hand) — already read, see
     jc2_ramirez_valqui_2025.md
```

1406.0886's own text confirms the "homogeneous system" is where 1409.6390 picks
up:

> "...we call the homogeneous system, giving a very detailed description of its
> solutions." — [VERIFIED: `valqui_1406v1.txt` line 33]
>
> "3   The homogeneous system S(n, m, F1−n)" — [VERIFIED: `valqui_1406v1.txt` line 611, section heading]

Neither v1 nor the 2024 v3 revision of 1406.0886 cites 1409.6390 anywhere
[VERIFIED: `grep -i "1409\|solorzano\|solórzano"` on both `valqui_1406v1.txt` and
`valqui_1406v3.txt` — zero hits, both files]. Not asked for by the task, but
noted since it's directly adjacent: even the parent paper's own decade-later
revision (Apr 2024, after GGHV22 existed) doesn't engage with either the 2014
follow-up or GGHV22 — I did not investigate why, per the "don't speculate"
instruction.

---

## 2. Q1 — which (n,m) does 1409.6390 actually compute? Verbatim.

> "In this paper we compute such a Groebner basis of (1.3) in a very particular
> case: we assume **n = 2, m = 2r + 1 for some r > 0, and λi = 0 for i > 0**.
> Moreover we consider **D = ℂ[y] and F1−n = y**, as in Theorem 1.1."
> — [VERIFIED: `solorzano_valqui_1409.6390.txt`, lines 101–103]

Restated as the actual computed object (§2, eq. 2.1–2.2 and Theorem 3.5):
`n=2` fixed for the *entire* paper; `m` ranges over **all odd integers ≥ 3**
(`r=1,2,3,...`); the only nonzero `λ_i` is `λ_0=1`; the base ring is
`D=ℂ[y]`, field is characteristic-0 (stated generally, line 14), specialized to
ℂ for the actual computation. This is the full scope — there is no other `(n,m)`
instance computed anywhere else in the 9-page paper (verified by reading it in
full, reproduced in Read output above).

### Does this match, generalize, or bear on (8,28)? Checked against the paper's own definitions, not assumed.

The task flags exactly the right trap: **do not assume GGHV22's corner-table
`(m,n)=(3,2)` label for the (8,28) row is the same symbol as this paper's
`(n,m)`.** Tracing each definition directly:

1. **1409.6390 / 1406.0886's `(n,m)`** (Theorem 1.1, quoted at
   `solorzano_valqui_1409.6390.txt` lines 17–27): for an *honest* pair
   `P,Q ∈ K[x,y]` with **`[P,Q] ∈ K^×`** (a nonzero constant — a genuine
   Jacobian pair), `C^n = P` and `Q = Σλ_iC^{m-i}+F` with `gr(C)=1`. Since `C`
   has leading term `x`, `C^n` has leading term `x^n`, so **`n = deg(P)`,
   `m = deg(Q)`, literally, for the full original counterexample.** This is
   confirmed independently in 1406.0886's own introduction: "T. T. Moh...
   finds four exceptional cases (m, n) = (48, 64)... where **(n, m) =
   (deg(P), deg(Q))**." [VERIFIED: `valqui_1406v1.txt` lines 21–22]

   Under this reading, the (72,108)/(108,72) top-level pair would give
   `(n,m)=(72,108)` or `(108,72)` — nowhere near the paper's fixed `n=2`.

2. **GGHV22's corner-table `(m,n)=(3,2)`** for the (8,28) row is a *different*
   notion entirely: it is the `(m,n)`-pair valuation ratio of
   `[1]=1401.1784, Def. 4.3` — `v_{1,1}(P)/v_{1,1}(Q) = v_{1,0}(P)/v_{1,0}(Q) =
   m/n` — applied to a **reduced pair `(P,Q) ∈ L^{(1)}`** (already transformed
   by a chain of automorphisms away from the actual counterexample), and that
   Def. 4.3 *also* requires `[P,Q] ∈ K^×` [VERIFIED, quoted in
   `jc2_gghv_system.md` §2 from `paper2_1401.1784.txt`].

3. **Proposition 4.3's actual `(P,Q)`** (the open case's real data) have
   **`[P,Q] = x²`** — not a unit. So on the letter of Def. 4.3's own
   requirement, Proposition 4.3's pair is not even literally an "(m,n)-pair"
   in that sense; it is a further-reduced object still. **Three distinct
   technical notions of "(n,m)"/"(m,n)" are in play across this literature
   (Theorem-1.1 top-level degree pair; Def-4.3 valuation-ratio label for a
   unit-bracket reduced pair; Proposition-4.3's own non-unit-bracket object),
   and none of the source papers asserts any two of them coincide.**

**Verdict on Q1: does not match** (neither reading of "(n,m)" lands anywhere
near 1409.6390's `n=2`); **does not generalize** (the paper proves a result for
one fixed `n=2`, not a method stated to work for general `n` — the sequel paper
had to redo the whole argument by hand for `n=3` and got a strictly weaker,
non-closed-form result, see §4); **bears on it only methodologically** — as one
data point showing this general lineage of systems *can* yield a hand-provable
closed-form Gröbner basis in a sufficiently degenerate corner, which is a
technique precedent, not a lookup-table hit.

---

## 3. Q2 — is the method adaptable to (8,28)? Concrete, not hand-wavy.

**Short answer: no, not as a drop-in template.** The paper's entire technique
depends on two structural facts that Proposition 4.3's own shape is already
known (from this repo's prior work) to lack, plus a third gap newly confirmed
this session.

**Why the method works for `n=2`, `λᵢ=0` (mechanism, verified by reading the
proofs):**

* With `λᵢ=0` for `i>0`, each even-indexed equation `E_{2j}` has the form
  `C_{-2j-1} + (lower stuff already in the ideal)` — i.e. **each equation
  contributes exactly one new "pivot" variable that appears nowhere else at
  that stage** (Proposition 2.2, eq. 2.7: `C_{-2j-1}+λ_jC_{-1}^{j+1} - E_{2j}
  ∈ Ĩ_{2j-1}`). This is what makes every S-polynomial reduce to zero by a
  one-line argument (Proposition 2.4's proof: `S(Ẽ_{2s-1},Ẽ_{2t}) =
  -λ_tC_{-1}^{t+1}Ẽ_{2s-1}`, etc. — divisibility, not a real Buchberger
  search).
* The **closed-form** part (the paper's actual novel contribution beyond
  1406.0886, via Lemma 3.1/Proposition 3.2) is a bijection between the `λ_j`
  recursion and the **Catalan-number** recursion `c_r = Σc_jc_{r-1-j}` — a
  fact that is special to squaring (`n=2`; `(C²)_{-k}` is literally a
  self-convolution). This lets the paper state the Gröbner basis for **every**
  odd `m` at once, in one formula, with zero computation blow-up as `m` grows.

**What (8,28) needs instead, per this repo's own already-verified findings:**

1. **Nonzero intermediate coefficients are forced.** `jc2_ramirez_valqui_2025.md`
   §3 (independently re-confirmed this session, §6 below) already establishes
   that Proposition 4.3's extra Newton-polygon vertices (`(8,14)` *and*
   `(8,16)` for `P`; `(12,21)` *and* `(12,24)` for `Q`) "force nonzero
   intermediate `νᵢ`'s and a non-trivial `F₁₋ₙ`... exactly the generality this
   paper explicitly declines to treat." Without `λᵢ=0`, the isolated-pivot
   structure above **does not exist**; S-polynomials no longer divide out for
   free, and a real Buchberger computation — with the usual risk of
   coefficient/degree blow-up — would be required instead of a hand proof.
2. **The bracket is `x²`, not a unit.** Theorem 1.1's whole system (eq.
   1.1–1.3) is derived from `[P,Q]∈K^×` (1406.0886's proof of Theorem 1.9,
   not re-derived in 1409.6390). Nobody in this literature has published the
   analogous derivation for `[P,Q]=x²`. This is the same gap
   `jc2_gghv_system.md` §6 already identified from the GGHV22 side; it is now
   corroborated from the 1406.0886/1409.6390 side as well — the S(n,m,...)
   system's construction simply presupposes a different kind of object than
   Proposition 4.3 hands us.
3. **New, sharper finding this session: GGHV22's own successful (9,27)
   reduction does not literally instantiate Theorem 1.1's system either**, so
   there is no existing "worked example at larger scale" to imitate. GGHV22
   writes, twice (once for (9,27)/(9,24) in §5, once for (7,21) in §6, in
   near-identical language):
   > "The equalities `C² = P` and `Q = C³ + λC⁻¹ + F` yield a system of
   > polynomial equations for `Ck`, **similar to** the systems of [3]..."
   > — [VERIFIED: `gghv2022.txt` line 826 (§5) and line 1132 (§6), essentially
   > verbatim in both places]

   "Similar to," not "an instance of" — and checking the indices confirms why
   that phrasing is exactly right: Theorem 1.1's sum `Σ_{i=0}^{m+n-2}λ_iC^{m-i}`
   bottoms out at `C^{m-(m+n-2)} = C^{2-n}`; for `n=2` (which `C²=P` forces)
   that floor is `C^0` — **`C^{-1}` is not a term the `n=2` template allows at
   all.** Yet GGHV22's own closed (9,27) system explicitly has a nonzero
   `λC^{-1}` term (their `α_{-1}`, surviving Remark 5.3's normalization, and
   feeding directly into equation `(D_3)_{-3}+λC_3^{20}=0`). **Even the case
   GGHV22 successfully closed falls outside the literal template 1409.6390
   computes.** This is a bespoke, self-contained derivation (Propositions
   5.2–5.6), not a citation-based reuse of Theorem 1.9's system at specific
   parameters — confirming, independently of the λ-sparsity argument above,
   that "adapt 1409.6390's result" and "redo GGHV22 §5's derivation" are not
   the same task even for the case already closed, let alone the open one.

**What would concretely have to change**, restated as a checklist (each item
independently blocking):

| # | Requirement in 1409.6390 | What (8,28) actually has | Consequence |
|---|---|---|---|
| 1 | `λᵢ=0` for `i>0` (sparsity) | Forced nonzero (extra polygon vertices) | Loses the one-line S-polynomial argument; real Buchberger needed |
| 2 | `[P,Q]∈K^×` (unit bracket, baked into the system's construction) | `[P,Q]=x²` | The system (1.1)–(1.3) itself would need re-derivation from scratch; not published anywhere checked |
| 3 | `n=2` exactly (source of the Catalan closed form) | Unconfirmed, plausibly 2 or 3 by analogy (`jc2_gghv_system.md` point 1; not stated in GGHV22) | Even `n=3` (2506.05697) loses the closed form — only `R_1..R_5` computed by hand, no general `R_k` |
| 4 | — | GGHV22's own bracket-`x` template for the closed sibling *already* falls outside the `n=2` index range (`C^{-1}` term) | No literal worked example at any scale to imitate |

**Is it "a reusable template we should be using instead of the from-scratch
reduction currently underway"?** No. The repo's current attack
(`jc2_reduction_828.py`/`.md`) is already doing the thing `jc2_gghv_system.md`
§5.5 identified as the right target — **redoing GGHV22's own §5-style bespoke
construction** (auxiliary series `C`, `D_k` transform, degree bounds) **for
bracket `x²`**, not invoking 1406.0886/1409.6390's general `S(n,m,...)`
machinery. That existing effort has already reached "8 shallow unknown
polynomials, reduced to 5," with a Singular Gröbner engine and sympy both
pointed at the remainder without finishing (`jc2_reduction_828.md`, its own
stated bottom line). 1409.6390 offers no shortcut past that point: its own
shortcut mechanism is precisely the one ingredient (`λᵢ=0`) this problem is
already known not to have.

---

## 4. Q3 — citation direction, checked both ways directly

**Does GGHV22 (arXiv:2204.14178) cite 1409.6390? No.**

GGHV22's complete bibliography — read in full, all 13 entries, `[1]`–`[13]` —
contains no Valqui–Solórzano paper and no reference to *Promathematica* 28 or
arXiv:1409.6390:

> `[3]         , A system of polynomial equations related to the Jacobian Conjecture, available at arXiv:1406.0886.`
> `[4]         , A Differential Equation for Polynomials related to the Jacobian Conjecture, Pro Mathematica 27, Num 53-54 (2013), 83–98.`
> — [VERIFIED: `gghv2022.txt` lines 1256–1282, full reference list]

Note explicitly: GGHV22 **does** cite a different *Pro Mathematica* paper
co-authored by (a subset of) the same author group — reference `[4]`, *A
Differential Equation for Polynomials related to the Jacobian Conjecture*,
*Pro Mathematica* **27** (2013) — which is not 1409.6390 (*The Groebner basis
of a polynomial system*, *Pro Mathematica* **28**, 2014): different title,
different volume, different year, no arXiv id given for `[4]`. Flagging this
explicitly since it is the one plausible way to misread this check —
GGHV22 does cite *a* Pro Mathematica paper from this circle, just not this one.
A direct text search confirms no occurrence of "Solorzano," "Solórzano," or
"1409.6390" anywhere in GGHV22's 1282-line extracted text
[VERIFIED: `grep -ni` over `gghv2022.txt`, `main_2204.14178.txt`,
`gghv_2204.14178.txt` — zero hits, all three cached copies].

**Does 1409.6390 cite GGHV22? Structurally impossible, and confirmed absent.**
1409.6390 was submitted 23 Sep 2014; GGHV22/arXiv:2204.14178 was submitted Apr
2022 (~7.5 years later — the arXiv ID's `2204` prefix is itself dispositive).
1409.6390's complete bibliography has exactly **3** entries — Cox–Little–O'Shea's
textbook, 1406.0886, and Koshy's *Catalan Numbers with Applications* — read in
full [VERIFIED: `solorzano_valqui_1409.6390.txt` lines 636–642]. GGHV22 is
absent, as it must be.

**External corroboration:** Semantic Scholar reports **citationCount = 0** for
1409.6390 [VERIFIED: live API query this session] — i.e., by S2's index, no
paper at all cites it, not just "not GGHV22." (S2 reports `referenceCount=4`
against my own direct count of 3 in the printed bibliography — a minor
S2-parsing discrepancy, noted rather than silently smoothed over; it does not
change the citation-direction conclusion either way.)

**So: 1409.6390 predates GGHV22 by 7.5 years and is not cited by it.** Per the
task's instruction, I report this as a plain citation fact and do not
speculate about whether GGHV22's authors considered-and-rejected it or simply
didn't encounter it (Valqui is a common author across nearly this whole
literature, so either is possible; nothing in either paper's text settles it).

---

## 5. Q4 — tooling, system sizes, orderings, field, timings

**1409.6390 reports zero computational tooling and zero timings, anywhere.**
Checked precisely (not just "no hits for 'Mathematica'" — that string is a
substring of nothing relevant here, see the false-positive discussion in §6 for
why this needs care in the *companion* paper): a targeted grep for
`mathematica|singular|macaulay|magma|cocoa|maple|" cas "|computation time|N
seconds|N minutes|cpu time|runtime|memory usage` returns **zero genuine
matches** in `solorzano_valqui_1409.6390.txt`
[VERIFIED, re-run this session with word-bounded patterns to exclude the
"Matemáticas"/"Universidad" false-positive class discovered along the way].
Every Gröbner basis in the paper is derived **by hand**, via induction on `r`
(Propositions 2.2, 2.4, 3.2, 3.3, Theorem 3.5) — this is a pen-and-paper proof
that a specific family of S-polynomials all reduce to zero, not a machine run.

What **is** specified precisely:

* **Field**: general characteristic-0 `K` in the setup (line 14); specialized
  to **`D = ℂ[y]`** for the actual computation (lines 102, 107) — complex
  coefficients, not a finite field.
* **Monomial order**: explicit **lexicographic** order,
  `C_{-2r-1} > C_{-2r} > ... > C_{-3} > C_{-2} > C_{-1} > y`
  [VERIFIED: Proposition 2.4 and Theorem 3.5, `solorzano_valqui_1409.6390.txt`
  lines 295, 560].
* **System size**: parametric, not a fixed numeric instance —
  **`2r+1` equations in `2r+1` unknowns** (`C_{-1},...,C_{-(2r+1)}`, plus `y`
  as a parameter) for **any** `r>0`, i.e. any odd `m=2r+1≥3`. The paper never
  instantiates a specific large `m` numerically; the whole point is a
  closed-form basis valid uniformly in `r`. This means the paper's notion of
  "computationally realistic" is not about keeping `m` small — it's that the
  `λᵢ=0` sparsity keeps the leading-term structure trivial **regardless of
  size**. That specific escape hatch is unavailable for (8,28) (§3).
* **Timings**: none, at any size — consistent with a fully symbolic, hand-checked
  induction.

For completeness on "either paper" (Q4's phrasing): the companion
arXiv:2506.05697/journal paper's tooling situation was already characterized in
`jc2_ramirez_valqui_2025.md` §5 as "none computational," and I independently
re-ran the same style of check this session — see §6 immediately below, where
I both confirm and slightly correct that section's phrasing.

---

## 6. Internal-consistency re-check of `jc2_ramirez_valqui_2025.md` (as requested)

Per the task: re-confirm this document (already read, not re-derived) is
internally consistent and that its stated greps were actually performed. I
spot-checked file existence, several verbatim quotes against their claimed
line numbers, and re-ran its key greps independently.

**Confirmed accurate:**

* All three source files it cites exist and are non-trivial
  (`ramirez_valqui_2025.txt` 35,598 bytes; `valqui_ramirez_2024.txt` 37,002
  bytes; `gghv2022.txt` 82,053 bytes) [VERIFIED: `ls -la`].
* Every verbatim quote I spot-checked reproduces **exactly**, modulo a small
  (~3-line) offset in the claimed line numbers for one quote (Theorem 1.1,
  claimed lines 18–29, actually at lines 15–32 in my fresh read of the same
  cached file — the quoted *text* is character-for-character correct, only
  the line-number pointer drifted slightly):
  - Theorem 1.1 statement — verbatim match [VERIFIED: `ramirez_valqui_2025.txt` lines 15–32].
  - "n = 3, m = 3r + 1 or m = 3r + 2..." — verbatim match at the *exact*
    claimed lines [VERIFIED: `ramirez_valqui_2025.txt` lines 104–112].
  - The "Final Remark" (the decisive quote) — verbatim match, full paragraph,
    at the exact claimed lines [VERIFIED: `valqui_ramirez_2024.txt` lines
    818–838].
  - The "(n,m)=(50,75)" quote — verbatim match at the exact claimed lines
    [VERIFIED: `valqui_ramirez_2024.txt` lines 66–76].
* The grep for GGHV22 degree/shape markers (`72`,`108`,`125`,`Newton`,
  `polygon`, case-label tuples) in both versions of the 2025 paper: I
  independently re-ran it. Result: **same conclusion, different specific
  false positives** than the ones the document names. My re-run's only hits
  are "Newton**s** binomial theorem" (twice, in `ramirez_valqui_2025.txt`)
  and, additionally, a bibliography page range "35–72" from the cited
  Heitmann paper (in `valqui_ramirez_2024.txt`) — genuinely unrelated to
  `deg=72`. Zero substantive hits either way; **the document's "no attack on
  (8,28)" conclusion is reconfirmed**, independently, this session.
* The `(m,n)_{§4}=(3,2)` reading for the (8,28) row (§8 of the document)
  matches this repo's own `jc2_gghv_system.md` corner table exactly
  (`(8, 28)   *(3,2)   108`) — internally consistent across the two documents.
  Both flag the exponent-vs-label identification as "plausible by analogy,
  not confirmed in the source paper," which is the same caveat, not a
  contradiction, despite being stated with slightly different emphasis in
  each file.
* The 1409.6390 identification in the document's §7 ("Solórzano & Valqui...
  Pro-Mathematica 28 (2014), 25–40 (arXiv:1409.6390) — cited by the 2025 paper
  itself as reference [9]") is **exactly right**: `valqui_ramirez_2024.txt`
  line 863 reads `[9] Solorzano, M. & Valqui, C. The Groebner basis of a
  polynomial system related to the Jacobian conjecture. Pro-Mathematica. 28
  (2014) 25–40.` [VERIFIED, re-confirmed this session] — a trivial page-number
  discrepancy (24 vs 25 for the opening page) against the arXiv metadata's
  "24-40," not worth flagging as an error either way.

**One real, if minor, imprecision found — flagged per "precision over
reassurance":**

§5 of `jc2_ramirez_valqui_2025.md` states: *"Grepped both versions for
`Singular|Macaulay|Magma|CoCoA|Maple|Mathematica|CAS|...`: **zero hits in
either version**"*. Re-running this literally: `ramirez_valqui_2025.txt`
(arXiv preprint) does have zero hits, confirmed. But `valqui_ramirez_2024.txt`
(the journal version) has **~20 raw hits for "Mathematica"**
[VERIFIED, this session] — every single one is part of the repeated running
page header/footer **"Pro Mathematica, 33, 65 (2024), 50-67, issn 1012-3938"**
(the journal's own name, stamped on every page) or the bibliography citation
of 1409.6390 itself ("Pro-Mathematica. 28..."), not a reference to Mathematica
the software. So **the substantive conclusion is still correct** — no CAS
tool is named or used anywhere in either version — but the sentence "zero hits
... in either version" does not survive a literal re-run against the journal
file; it should read "zero hits for the *software*; ~20 hits for the
*journal's own name* in running headers, which is not a tooling mention."
This does not change any downstream conclusion in that document or in this
one, but it is exactly the class of small, checkable overclaim the task asked
me to watch for, so I am reporting it plainly rather than smoothing it over.

**Conclusion of the re-check: the document's methodology was genuinely
executed (not fabricated), its quotes are accurate, and its central
conclusions all reproduce independently. One phrasing overclaim (the
"Mathematica" grep sentence) is noted above; it is cosmetic, not substantive.**

---

## 7. What this means for the repo's current (8,28) work

* `jc2_gghv_system.md` (Prop. 4.3 documentation, the "naive system," and the
  §5.5/§6 recommendation to redo GGHV22 §5's bespoke technique for bracket
  `x²`) — **unaffected**. Nothing here contradicts or extends it; if anything
  §3–4 above independently re-derive, from the 1406.0886/1409.6390 side, the
  same "this is new mathematics, not extraction" conclusion that document
  already reached from the GGHV22 side.
* `jc2_ramirez_valqui_2025.md` — reconfirmed accurate (§6 above), one cosmetic
  phrasing note.
* `jc2_reduction_828.py`/`.md` (the live from-scratch attempt) — **this is
  already the right kind of approach** relative to what 1409.6390 offers; nothing
  here suggests switching strategies. It is *not* an application of the general
  `S(n,m,(λᵢ),F_{1-n})` framework at literal parameters (that system, at
  `(n,m)=(72,108)`, would have `m+n-2=178` unknowns — `jc2_gghv_system.md` §7,
  independently re-confirmed arithmetically here: `72+108-2=178` — and
  1406.0886's own abstract already disclaims tractability at far smaller sizes
  like `(50,75)` without a further case-specific reduction). It is a redo of
  GGHV22's own bespoke §5-style construction for bracket `x²`, which is the
  correct target per both this document and `jc2_gghv_system.md`.

---

## File manifest

* `/home/user/jacobian_planar/jc2_valqui_framework.md` — this file.
* Fetched/extracted this session, cached under
  `/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/`
  (not in the repo, no PDFs committed):
  - `solorzano_valqui_1409.6390.{pdf,txt}` — primary target, full text, 9pp/653 lines.
  - `abs_1409.6390.html` — live arXiv abstract page (metadata, journal ref, MSC).
  - `s2_1409_6390.json` — live Semantic Scholar Graph API record (citationCount=0).
* Already cached from prior sessions, re-read/re-grepped for this task (not
  re-fetched, per the task's "don't redo that read" instruction where
  applicable):
  - `gghv2022.txt` = `main_2204.14178.txt` = `gghv_2204.14178.txt` — GGHV22 full
    text, 1282 lines; bibliography (lines 1256–1282) and both `[3]`-citation
    contexts (lines 826, 1132) re-read directly this session.
  - `valqui_1406v1.txt`, `valqui_1406v3.txt` — 1406.0886 v1 (Jun 2014) and v3
    (Apr 2024) full text; re-read for the "homogeneous system" provenance and
    the citation-direction side-check against 1409.6390/GGHV22.
  - `ramirez_valqui_2025.txt`, `valqui_ramirez_2024.txt` — arXiv preprint and
    journal version of 2506.05697; re-grepped and quote-checked in §6.
  - `valqui_all.xml` — arXiv API author listing for "Valqui" (39 entries),
    used to independently confirm 1409.6390's identity/date/abstract.

---

## Verdict

**Arxiv:1409.6390 is a real, narrowly-scoped, hand-proved result (Gröbner basis
of the `n=2`, odd-`m`, homogeneous slice of the Guccione–Guccione–Valqui
`S(n,m,(λᵢ),F₁₋ₙ)` framework, via a Catalan-number recursion, zero computer
tooling, zero timings) that neither matches (8,28)'s parameters under either
plausible reading of "(n,m)," nor generalizes to them, nor is cited by or cites
GGHV22 (confirmed directly in both bibliographies, and impossible in one
direction on dates alone); its one substantive contribution to this campaign is
negative-but-useful confirmation that the tractability trick it demonstrates —
isolate one pivot variable per equation via forced coefficient sparsity — is
exactly the trick Proposition 4.3's Newton polygon is already known to foreclose
(nonzero intermediate coefficients are forced by its extra vertices), and that
this holds even for the *closed* (9,27) sibling, whose own bracket-`x` system
GGHV22 explicitly built by hand rather than by invoking this framework's
theorem at specific parameters. Net effect: this paper sits **orthogonal** to
the current direct (8,28) attack — it neither changes nor validates it, and the
from-scratch redo of GGHV22 §5's own bespoke construction already underway in
`jc2_reduction_828.py`/`.md` remains the correct strategy, with no shortcut
handed to it by this literature.**
