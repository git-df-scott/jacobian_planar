# GGHV Corollary 5.7 — independent adjudication

Source: `wt/canon/papers/2204.14178.pdf`. **pdfinfo Title: `arXiv:2204.14178v1 [math.AG] 29 Apr 2022`**,
25 pages, CreationDate 2022-05-02. **No v2, no erratum, no corrigendum, no journal ref in the local PDF**
(grep for erratum/corrigendum/v2 returns nothing; the only arXiv stamp is `arXiv:2204.14178v1`).
Reference [1] = `wt/canon/papers/1401.1784.pdf` (GGV, J. Algebra 471 (2017) 13–74).

Extraction: `pdftotext -layout` (poppler). `pypdf` is broken in this env (`_cffi_backend` missing →
`pyo3_runtime.PanicException`); `pdftotext` worked, so no fallback was needed.
Text files: `gghv_layout.txt`, `gghv_raw.txt`, `ggv1401_layout.txt`.

## VERDICT: **BROKEN**

The step as printed is invalid. The obstruction is explicit, structural and quotable.
(The *statement* of Cor 5.7 may still be true; what fails is its only published proof.)

---

## 1. The statement (PDF p. 20, `gghv_layout.txt:982-985`), verbatim

> **Corollary 5.7.** There exist no P, Q ∈ K[x, y] with [P, Q] = x and
> N (P ) = {(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)}
> N (Q) = {(0, 0), (1, 0), (9, 24), (9, 27), (0, 27)}

## 2. The whole proof (PDF p. 20, `gghv_layout.txt:986-996`), verbatim

> *Proof.* We claim that ℓ0,1 (P ) = λp y^18 (x − λ)^6 for some λp , λ ∈ K^× . If the claim is true, take
> φ ∈ Aut(K[x, y]) with φ(y) = y and φ(x) = x + λ. Then
> &nbsp;&nbsp;&nbsp;&nbsp;Succ_{φ(P)} (1, 0) ≥ (−1, 1) and Succ_{φ(Q)} (1, 0) ≥ (−1, 1).  (5.12)
> Since [φ(P ), φ(Q)] = x + λ, the polynomials φ(P ), φ(Q) satisfy the conditions of Theorem 5.1,
> a contradiction which concludes the proof.
> &nbsp;&nbsp;&nbsp;&nbsp;In order to prove the claim and (5.12), consider the map ψ : K[x, y] → L^(2) given by ψ(x) =
> x^{1/2} and ψ(y) = y. Then (ψ(P ), ψ(Q)) is an m, n-pair for (m, n) = (2, 3) (see [1, Definition
> 4.3]), and en_{1,0}(F ) = 1/2 · 1/m en_{1,0}(P ) for F as in [1, Theorem 2.6]. Hence q = 3 in [1, Corollary
> 7.2] and so ℓ0,1 (ψ(P )) is a sixth power, hence so is ℓ0,1 (P ). **By the same argument, for (ρ, σ) =
> Succ_{ψ(φ(P))} (0, 1) we also have that ℓ_{ρ,σ} (ψ(φ(P ))) is a sixth power**, and since st_{ρ,σ}(ψ(φ(P ))) =
> (6, 18), we know that (ρ, σ) ∈ {(−1, 1), (−2, 1), (−3, 1)}, which proves (5.12).

(The `y^18` is typeset in the PDF text layer as `y 1 8`, a well-known pdftotext superscript artifact.)

## 3. The hypotheses that "the same argument" needs, verbatim from [1]

`ggv1401_layout.txt:2007-2014` (Corollary 7.2), condition printed on its own line:

> **Corollary 7.2.** Let m, n ∈ N be coprime with m, n > 1 and let P, Q ∈ L^(l) with
> &nbsp;&nbsp;&nbsp;&nbsp;**[P, Q] ∈ K^×**  and  v1,1(P)/v1,1(Q) = v1,0(P)/v1,0(Q) = m/n.

`ggv1401_layout.txt:721-726` (Definition 4.3), same requirement:

> **Definition 4.3.** ... A pair (P, Q) of elements P, Q ∈ L^(l) ... is called an (m, n)-pair in L^(l) ... if
> &nbsp;&nbsp;&nbsp;&nbsp;**[P, Q] ∈ K^×**, v1,1(P)/v1,1(Q) = v1,0(P)/v1,0(Q) = m/n and v1,−1(en1,0(P )) < 0.

`ggv1401_layout.txt:366-367` (Theorem 2.6, which produces the F the proof invokes):

> **Theorem 2.6.** Let P ∈ L^(l) and let (ρ, σ) ∈ V>0 be such that vρ,σ (P ) > 0. **If [P, Q] ∈ K^× for
> some Q ∈ L^(l)** , then there exists G0 ∈ K[P, Q] \ {0} and a (ρ, σ)-homogeneous element F ∈ L^(l) ...

All three routes into the argument require `[·,·] ∈ K^×`. `L^(l) := K[x^{±1/l}, y]` (`ggv1401_layout.txt:29,133`).

## 4. The bracket, recomputed independently in sympy

Script `run/bracket_check.py`. Two computations, both using the paper's own bracket conventions:
the chain rule [1, Proposition 3.10] (`ggv1401_layout.txt:675-677`)

> [φ(P ), φ(Q)] = φ([P, Q])[φ(x), φ(y)]   (3.3)

and its explicit L^(l) form, also from Prop. 3.10's proof: identifying L^(l) with K[z, z^{-1}, y]
via z = x^{1/l}, `[P,Q] = (P_z Q_y − P_y Q_z) · 1/(l z^{l−1})`.

**First application (the claim) — VALID.**
`[ψP, ψQ] = ψ([P,Q]) · [ψ(x),ψ(y)] = x^{1/2} · (1/2)x^{−1/2} = 1/2 ∈ K^×`.
sympy, generic form and concrete witness (P = x²/2, Q = y, [P,Q] = x): `[psi P, psi Q]_{L(2)} = 1/2`.

**Second application (the load-bearing sentence) — INVALID.**
`[φP, φQ] = φ([P,Q])·[φ(x),φ(y)] = x + λ`, hence
`[ψφP, ψφQ] = ψ(x+λ)·(1/2)x^{−1/2} = (x^{1/2}+λ)/(2x^{1/2})`.
sympy output:

```
[psi phi P, psi phi Q] = lambda_/(2*z) + 1/2   ->  in x:  1/2 + (lambda/2) x^(-1/2)
is it in K^x (constant in z)?  False
equals 1/2 + (lam/2) z^-1 :    True
```

Same answer from the abstract chain rule, from the explicit L^(2) Jacobian formula, and from two
concrete pairs (P = x²/2, Q = y and P = x²/2 + y³, Q = y). So

> **[ψφP, ψφQ] = 1/2 + (λ/2)·x^{−1/2} ∉ K^×.**

It *is* in L^(2) (x^{−1/2} = z^{−1} is a Laurent monomial there), so the objects are in the right ring —
it is precisely and only the K^× condition that fails.

**λ ≠ 0 is forced**, so the failure is never vacuous: the claim itself writes λ ∈ K^×; independently,
(0,18) ∈ N(P) forces the constant term of ℓ0,1(P)/y^18 = λp(x−λ)^6 to be λp λ^6 ≠ 0. (And if λ were 0,
φ = id and (5.12) would assert Succ_P(1,0) ≥ (−1,1), which is false for the given N(P).)

## 5. (5.12) is load-bearing, not decorative — recomputed

Theorem 5.1 (PDF p. 14, `gghv_layout.txt:659-663`) hypothesis (2) demands `st_{−1,1}(P) = (6,18)`.
v_{−1,1}(a,b) = b − a on the given polygons (sympy):

```
v_(-1,1) on N(P): {(0,0):0, (1,1):0, (6,16):10, (6,18):12, (0,18):18}  max 18 at [(0,18)]
v_(-1,1) on N(Q): {(0,0):0, (1,0):-1, (9,24):15, (9,27):18, (0,27):27}  max 27 at [(0,27)]
```

So st_{−1,1}(P) = (0,18) ≠ (6,18) and st_{−1,1}(Q) = (0,27) ≠ (9,27): Theorem 5.1 is **not** applicable
to the untranslated pair, and is reachable only through φ + (5.12). CATCHES.md is right on this.

## 6. Size of the hole — recomputed

(5.12) forces v_{−1,1}(φP) = 12 and v_{−1,1}(φQ) = 18, i.e. vanishing of every x^a y^b with b − a
above those, inside [0,6]×[0,18] and [0,9]×[0,27]. sympy count:

```
(5.12) conditions: P: 21   Q: 45   total: 66
delivered by the claim (top rows b=18, a=0..5 ; b=27, a=0..8): 15   unsupported: 51
```

Confirms CATCHES.md exactly: **15 of 66 conditions are delivered by the valid first half; 51 rest on
the invalid step.**

## 7. Is there a repair by the same device? — checked, no

Ask for ξ with ξ(y)=y, ξ(x)=h(x) making the translated pair's bracket constant:
`[ξ(φP), ξ(φQ)] = (h+λ)h' = c`. sympy `dsolve`:

```
h(x) = -lambda ± sqrt(C1 + 2*c*x + lambda**2)
```

so ξφ sends x ↦ ±√(2cx + C1 + λ²). Two cases, both dead:
* C1 + λ² = 0: ξφ(x) = ±√(2c)·x^{1/2}, i.e. ξ∘φ **is ψ up to scaling** — it undoes the translation and
  hands back the ORIGINAL polygon, so it proves nothing about N(φP).
* C1 + λ² ≠ 0: √(2cx+d) with d ≠ 0 is **not** an element of L^(2) = K[x^{±1/2}, y] (it is only a formal
  series in K((x^{−1/2}))), so [1, Cor 7.2] / Def 4.3 / Thm 2.6, all stated for L^(l), do not apply.

The x^{1/2} trick works only because [P,Q] is the variable x itself. Structural, not a typo.

## 8. What is NOT wrong

The claim (first half of the proof) is fine — there the bracket really is 1/2 ∈ K^×. Theorem 5.1's
own proof, Prop. 4.1, and everything else in §5 were not re-audited here but nothing in this audit
touches them. The defect is localised to one sentence, `gghv_layout.txt:993-994`.

## 9. Reconciliation with the mailbox sweep

`mailbox/campaign/mod3_828/jc2_literature_sweep_partial.md:66` says
"Independently verified `Corollary 5.7` ... [VERIFIED: gghv2022 PDF, lines 982-996]". Read literally,
that verified **the statement's existence and wording** at those lines — which is correct, and which
this audit reproduces. It did **not** audit the proof. So the two records are not in direct
contradiction; the sweep's "VERIFIED" tag is scoped to the quotation, and its stronger implicature
("closed via Theorem 5.1") is what fails. Separately, line 66 misattributes Cor 5.7 to the
"(9,24)/(66,99) shape"; line 311 of the same file has it right — Cor 5.7 is the **(9,27) → (72,108)**
case. Line 66 should be corrected on both counts.
