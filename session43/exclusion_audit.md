# Exclusion Audit: Jacobian Conjecture Degree-Pair Campaign

Status: COMPLETE (within 20-min budget)
Date: 2026-08-22
Auditor note: VERIFIED = read directly from primary source text (arXiv PDF, converted to text
with pdftotext, quotes checked against the raw extraction). PARTIALLY VERIFIED = abstract/summary
confirmed but full proof not read line-by-line. COULD NOT VERIFY = not accessed / no reliable source found.

---

## 0. Identifying "GGHV"

The campaign's "GGHV" almost certainly refers to one or both of:

- **arXiv:1708.07936**, "Some algorithms related to the Jacobian Conjecture", Jorge A. Guccione,
  Juan J. Guccione, Rodrigo Horruitiner, Christian Valqui — the actual G-G-H-V four-author paper
  (this is where the "list of possible corners of small counterexamples" comes from, per the
  paper below's own account of its history).
- **arXiv:2204.14178**, "Increasing the degree of a possible counterexample to the Jacobian
  Conjecture from 100 to 108", same four authors (Guccione, Guccione, Horruitiner, Valqui) — this
  is the paper that actually proves the "max degree < 125" statement AND contains "Corollary 5.7".

I fully fetched and text-extracted **2204.14178** (the load-bearing one for items 1 and 2) via
`pdftotext`. I did not have time to fully extract 1708.07936; where it matters I mark that.

Related earlier papers by a 3-author subset (Guccione–Guccione–Valqui, i.e. "GGV"):
- arXiv:1401.1784 = J. Algebra 471 (2017), 13–74, "On the shape of possible counterexamples to
  the Jacobian Conjecture" — published, peer-reviewed. Cited as [1] in 2204.14178.
- arXiv:1605.09430, "The Two-Dimensional Jacobian Conjecture and the Lower Side of the Newton
  Polygon" — cited as [2].
- arXiv:1406.0886, "A system of polynomial equations related to the Jacobian Conjecture" —
  cited as [3]. This is the direct source of the "systems of polynomial equations" machinery
  used in Section 5 of 2204.14178 (i.e., the machinery behind Theorem 5.1 / Corollary 5.7).

---

## 1. The "max degree < 125" bound

**VERIFIED.**

Source: arXiv:2204.14178, "Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108", J.A. Guccione, J.J. Guccione, R. Horruitiner, C. Valqui.

Exact abstract (quoted verbatim from the paper):

> "We list all the pairs (deg(P),deg(Q)) with max{deg(P),deg(Q)}<125 for any hypothetical
> counterexample to the plane Jacobian Conjecture and discard them all, except the pair
> (72,108) (and the symmetric pair (108,72)), thus we confirm the lower bound of 100 obtained
> by Moh and raise it up to 108."

Exact theorem statement (Theorem 2.1, quoted verbatim):

> "Theorem 2.1. If (P, Q) is a counterexample to the Jacobian Conjecture, then we have either
> max{deg(P), deg(Q)} ≥ 125, or (deg(P), deg(Q)) ∈ {(72, 108), (108, 72)}."

(a) **What "125" refers to**: `max{deg(P), deg(Q)}` — the LARGER of the two component degrees,
not the gcd and not the sum. So "below 125" means the larger degree is < 125.

(b) Confirmed above.

(c) **Which pairs survive, and is (72,108) really unique below 125?** The paper's own table
(Section 2) lists exactly 10 candidate "shape" cases below max-degree 125, coming from the
classification in a companion paper ([5] = arXiv:1708.07936, "Some algorithms related to the
Jacobian Conjecture" — the actual 4-author G-G-H-V paper). Reduced to `deg(P) < deg(Q)`, the
surviving degree-VALUE cases before this paper's own new work are:

  `{(56,84), (66,99), (72,108) [×2 distinct Newton-polygon shapes], (80,120)}`

The paper discards (56,84) [§6, alternate proof also given in §3 via a different route],
(80,120) [§3], (66,99) [§5], and **one of the two shape-cases with degree-pair (72,108)** [§5,
via Corollary 5.7]. This leaves **exactly one** surviving shape-case, still with degree pair
(72,108), which the authors could NOT resolve. Direct quote from the Introduction:

> "In section 5 we use the systems of polynomial equations associated to a possible
> counterexample as in [3] in order to discard the case (deg(P),deg(Q))=(66,99) and one of the
> cases with (deg(P),deg(Q))=(72,108). For the other case with (deg(P),deg(Q))=(72,108) we
> couldn't solve the corresponding system of polynomial equations, thus it is left open."

and:

> "The only exception is the case (deg P, deg Q) = (72, 108), and so, if one manages to discard
> this case, it would increase the lower bound from 108 up to 125."

So: **yes, (72,108) is genuinely the sole numerically-surviving degree pair below 125**, per this
paper — Theorem 2.1 as stated is correct and (72,108)/(108,72) is exhaustively the only
unresolved case in the max<125 range, GIVEN the correctness of the classification in [5]
(1708.07936) that produced the original list of 10 candidate shapes, and given the correctness
of the discarding arguments in §3 and §5-6 of this paper.

**Important nuance the campaign should know**: within the single numeric pair (72,108) there
are **two distinct Newton-polygon "shapes"** (the paper's table labels them by corner data
`A0=(9,27)` with `(m,n)=(2,3)` giving max-degree 108, and `A0=(8,28)` with `(m,n)=(3,2)` also
giving max-degree 108). Only the (9,27)-shape case is discarded (by Corollary 5.7). The
(8,28)-shape case is explicitly left OPEN — not proven to survive as realizable, just not yet
ruled out. This matches exactly what the campaign's own ledger says about "Corollary 5.7 kills
the (9,27) orientation" — that description is accurate. But it also means: **of the two
orientations, only one has actually been eliminated; the fact that (72,108) survives as a
degree pair rests partly on genuine unresolved difficulty (the authors couldn't solve their own
system of equations for the other shape), not just on a completed proof.** This is not a flaw in
the campaign's reasoning (both orientations still permit a counterexample logically, so (72,108)
correctly remains "admissible" either way) — but it is worth flagging that "sole survivor" does
NOT mean "every sub-case fully resolved"; one sub-case is an open problem, and if it had gone
the other way, it wouldn't have changed which degree PAIR survives.

(d) **Hypotheses / gaps, as verified from the text**:
- The whole classification chain depends on the prior classification work in [1] (1401.1784,
  published J. Algebra 2017), [2] (1605.09430), [3] (1406.0886), and especially [5] (1708.07936)
  for the list of 10 candidate shapes — I did NOT independently re-derive or fully text-extract
  [5], so the completeness of "these are the only 10 shapes below max-degree 125" is
  PARTIALLY VERIFIED only (I confirmed 2204.14178 cites and relies on it, but did not check
  1708.07936's own derivation line-by-line).
- The (8,28)-shape / other-(72,108)-case is an explicitly acknowledged OPEN problem within this
  very paper — not a gap in rigor, but a genuine incompleteness the authors state themselves.
- I found NO erratum, correction, or retraction notice for 2204.14178, 1401.1784, 1605.09430,
  or 1406.0886 in web search (see item 4 below for search details).

**VERDICT: VERIFIED** (the "< 125" bound and the "(72,108) sole survivor" claim are accurately
represented by the campaign), **with one flagged nuance**: one of the two Newton-polygon
orientations of (72,108) is not eliminated by this paper — it's simply an open problem, so
"sole surviving admissible pair" is correct but rests in part on absence-of-proof for one
sub-case, not a completed proof that this sub-case is realizable.

---

## 2. GGHV Corollary 5.7

**VERIFIED** (statement and proof sketch read directly from arXiv:2204.14178, §5).

Exact statement (quoted verbatim):

> "Corollary 5.7. There exist no P, Q ∈ K[x, y] with [P, Q] = x and
>   N(P) = {(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)}
>   N(Q) = {(0, 0), (1, 0), (9, 24), (9, 27), (0, 27)}"

Here `N(P)`, `N(Q)` denote the Newton polygon vertex sets of P and Q. This is exactly the
"(9,27)"-shape case from the Section-2 table (max{deg P,deg Q}=108, i.e. deg Q=27·... — note the
Newton polygon vertices (0,18) and (0,27) correspond, after the paper's homogeneity/scaling
conventions in earlier sections, to the degree pair (72,108); the campaign's phrase "(9,27)
orientation of (72,108)" matches this table row (`A0=(9,27), (m,n)=(2,3), max=108`) precisely.

**The proof apparatus it depends on** (verified from the text):
1. It is derived by REDUCTION to **Theorem 5.1** (same paper, §5), which rules out a closely
   related but different pair of Newton-polygon conditions (essentially the same shape without
   the extra hypothesis `[P,Q] = x + g(y)` generalized to `[P,Q] = x` via a linear shift). Exact
   quote of the reduction step: "Since [φ(P), φ(Q)] = x + λ, the polynomials φ(P), φ(Q) satisfy
   the conditions of Theorem 5.1, a contradiction which concludes the proof."
2. Theorem 5.1's own proof (which I read in full) is a long, explicit computation: it factors
   `P = C²`, `Q = C³ + α₂C² + α₁C + α₀ + α₋₁C⁻¹ + F` in a formal Laurent-series ring, derives a
   recursive system of polynomial equations for coefficients `Ck` (following the machinery of
   [3] = arXiv:1406.0886), transforms it into polynomial unknowns `Dk = Ck·C3^(5-2k)`, and
   reaches an explicit polynomial identity (eq. 5.11) that is shown to be impossible by a
   degree-count / divisibility argument (`(y+1)^k` divides both sides with an incompatible
   exponent count) for all `k`. This is a genuine, self-contained algebraic contradiction — I did
   not find any obvious gap in reading it, but I did not independently re-verify the algebra
   (i.e., I did not re-derive equations 5.7–5.11 symbolically myself; that would require a CAS
   and is beyond this budget).
3. Corollary 5.7's proof ALSO separately invokes external results from paper [1] (=1401.1784,
   published J. Algebra 2017): "Definition 4.3", "Theorem 2.6", and "Corollary 7.2" of [1], to
   establish that a certain leading coefficient `ℓ₀,₁(P)` must be a perfect sixth power. This is
   an additional, external dependency beyond Theorem 5.1 itself — i.e. Corollary 5.7 = Theorem
   5.1 (this paper) + Corollary 7.2 and related results of the 2017 J. Algebra paper. I did NOT
   fetch/verify J. Algebra 2017's Corollary 7.2 directly (paywalled ScienceDirect; arXiv version
   1401.1784 should mirror it but I did not cross-check the corollary numbering in the arXiv PDF
   in the time available).

**Independent verification / erratum**: none found (see item 4).

**VERDICT: VERIFIED** for the statement and the two-step proof architecture (Thm 5.1 + external
lemma from GGV 2017). **PARTIALLY VERIFIED** for full correctness — I read the argument but did
not symbolically re-derive it, and I did not independently check the imported Corollary 7.2 from
the 2017 paper. The campaign's characterization ("proved via the Sec 5 / Thm 5.1 degree
apparatus that was never re-derived by anyone") is essentially accurate: I found no independent
re-derivation, replication, or citation confirming/refuting Corollary 5.7 by a third party.

---

## 3. "Nguyen 104"

**PARTIALLY VERIFIED** (paper identified with high confidence; refereed publication confirmed;
full proof not read).

Source: **arXiv:1902.05923**, "Some classes satisfying the 2-dimensional Jacobian conjecture and
a proof of the complex conjecture until degree 104", author **Thuy Nguyen** (note: this appears
to be a different person from **Nguyen Van Chau**, who is a separate, prolific author on the
2D Jacobian conjecture / non-properness / Newton-polygon methods — I could not fully confirm
their distinctness with certainty from search alone, but the arXiv author-listing shows the
single name "Thuy Nguyen", and other Nguyen Van Chau papers found in search, e.g. "Pencil of
irreducible rational curves and Plane Jacobian conjecture" arXiv:0905.3939, list the author
differently. Flag: campaign should not assume "Nguyen 104" = Nguyen Van Chau without checking
further; treat as a SEPARATE, unconfirmed identity issue.)

Exact abstract (quoted verbatim):

> "We construct a non-proper set of two variables polynomial maps and study the nowhere
> vanishing Jacobian condition of the Jacobian conjecture for this set. We obtain some classes of
> polynomial maps satisfying the 2-dimensional Jacobian conjecture for both real and complex
> cases. In addition, by Newton polygon technique, we prove that the complex conjecture is true
> until degree 104, improving Moh boundary (degree 100) since 1983."

**Publication status**: The arXiv listing page shows a **journal-ref: "Quaestiones Mathematicae
48(2), 2025"** — Quaestiones Mathematicae is a legitimate, refereed Taylor & Francis journal
(South African Mathematical Society). So this result IS now peer-reviewed and published (as of
2025), confirming the campaign's "trusted refereed" characterization. However:
- v1 was posted Feb 2019; the paper went through 5 arXiv revisions (v1 2019 → v5 Mar 2025) before
  journal publication — a 6-year gap, suggesting a substantial referee process / revision.
- I did NOT read the proof itself (only the abstract) — I cannot verify the "until degree 104"
  claim's internal correctness. "Degree" here, by analogy with Moh/GGHV convention, almost
  certainly means `max{deg P, deg Q}`, but I could not confirm this from the abstract alone —
  COULD NOT VERIFY this convention-matching detail without reading the full paper.

**Notable cross-check finding**: The GGHV paper (arXiv:2204.14178, submitted April 2022 — i.e.
**after** Nguyen's 2019 v1 preprint existed) does **not cite or mention** the Nguyen 104 result
anywhere in its 13-item reference list. GGHV's own framing is "we confirm the lower bound of 100
obtained by Moh and raise it up to 108" — as if 104 were never claimed by anyone in between. This
is either (a) an oversight/non-citation by GGHV, (b) a sign that the Guccione–Guccione–
Horruitiner–Valqui group did not consider the Nguyen preprint's 2019-vintage claim reliable
enough to cite/build on at the time, or (c) simply an independent, non-overlapping research
thread. This is a **genuine, verifiable gap worth flagging to the campaign**: the two headline
numbers (104 from Nguyen, 108 from GGHV) come from apparently non-communicating lineages, and
the more citation-central paper (GGHV, which the campaign treats as authoritative for the "125"
bound) does not appear to regard the 104 paper as an established stepping stone.

**VERDICT: PARTIALLY VERIFIED.** Paper identified, refereed/published status confirmed
(Quaestiones Mathematicae 48(2), 2025). Full proof NOT read/verified — could not check the
"until degree 104" claim's correctness or its exact degree convention. Flag: possible identity
confusion with Nguyen Van Chau; flag: GGHV's own 2022 paper is silent on this result, suggesting
either a citation gap or a lack of cross-validation between the two exclusion lineages the
campaign is relying on.

---

## 4. Known errata / retractions / disputes

**COULD NOT FIND ANY**, based on web search only (I did not have time for a systematic errata
database search, e.g. Retraction Watch, MathSciNet reviews, or Zentralblatt).

Search queries run: "Jacobian conjecture degree bound paper erratum retraction correction
Guccione Valqui" and variants. Results returned only the primary papers and generic
errata-policy pages (AIP, IntechOpen, PubMed, journals' generic corrections policies) — no
specific correction notice for any of: 1401.1784/J.Algebra 2017, 1605.09430, 1406.0886,
1708.07936, or 2204.14178.

Background context (general knowledge, NOT independently re-verified in this session): it is
well known in the field that several FULL proofs of the 2-dimensional Jacobian conjecture itself
have been published and later found flawed or withdrawn over the decades (this is widely
discussed in survey literature, e.g. van den Essen's book "Polynomial Automorphisms and the
Jacobian Conjecture", cited as [12] in the GGHV paper). I did NOT verify specific instances of
this in this session — flagging it only as a reason for the campaign to remain skeptical of any
single degree-bound claim until independently checked, consistent with the campaign's own
stated caution.

**VERDICT: COULD NOT VERIFY absence of errata with high confidence** — negative result from
web search only, not from a specialist database (MathSciNet/zbMATH) which I do not have access
to in this environment. Treat as "no erratum found" rather than "no erratum exists."

---

## Summary Table

| Item | Verdict | Key risk to campaign |
|---|---|---|
| 1. max<125 bound / (72,108) sole survivor | VERIFIED (with nuance) | Relies on unverified [5]=1708.07936 classification of 10 shapes; one (72,108) sub-case is an *open problem*, not a completed exclusion |
| 2. Corollary 5.7 | VERIFIED statement/architecture; PARTIALLY VERIFIED correctness | Depends on external Cor 7.2 from GGV 2017 (J.Algebra) not independently re-checked; no third-party replication found |
| 3. Nguyen 104 | PARTIALLY VERIFIED | Now refereed (Quaestiones Math. 48(2) 2025) but proof unread; possible author-identity ambiguity (Thuy Nguyen vs Nguyen Van Chau); GGHV 2022 paper doesn't cite it at all — the two lineages may not have cross-validated each other |
| 4. Errata/retractions | COULD NOT VERIFY (none found, but search was web-only) | Field has history of withdrawn JC proofs generally; no MathSciNet/zbMATH check performed |

## Overall recommendation to the campaign

The (72,108) narrowing is **not obviously wrong** — Theorem 2.1 of arXiv:2204.14178 is a real,
specific, quotable theorem, and I read its Section 5 proof of Corollary 5.7 directly and found it
internally coherent. But the campaign's ledger entry "never re-derived by anyone" for Corollary
5.7 is literally true as far as I can find, and there are three concrete places a re-audit could
still overturn (72,108) as sole survivor:
1. Full re-derivation/verification of arXiv:1708.07936 ("GGHV" proper)'s classification of the
   10 candidate shapes below max-degree 125 (not done here — not fetched in full).
2. Full re-derivation of GGV 2017's (arXiv:1401.1784) Corollary 7.2, which Corollary 5.7 imports.
3. Symbolic re-verification of the equations 5.7-5.11 computation inside Theorem 5.1's proof
   (not done here — would need a CAS).
None of these were found to be flawed, but none were independently re-derived either — they were
read and found plausible, which is different from independently checked.
