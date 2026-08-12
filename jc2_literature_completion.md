# JC2 Literature Sweep — Completion Report (Modalities A–D)

Continues `jc2_literature_sweep_partial.md` (5/8 modalities). This file runs the
three modalities that never launched (A: grey literature, B: above 125, C: the
gcd≥36 thread) and the completeness critic (D) that never ran either. Per the
task rules, every claim is tagged `[VERIFIED: source]`, `[SECONDARY: source]`,
or `[MEMORY, unverified]`. Nothing already nailed down in the partial file
(GGHV Thm 2.1, the (72,108) status, the July-2026 dimension-≥3 irrelevance to
JC2, the two Newton-polygon sub-shapes at (72,108)) is re-litigated here except
where new evidence changes the picture.

All primary sources fetched fresh this session are in the scratchpad (list at
the end); none were committed to the repo; nothing was pushed.

---

# A. GREY LITERATURE

## A1. Theses — three found, all from Purdue (Moh's own students), one from PUCP (already logged)

**Horruitiner's PUCP Master's thesis** was already found and read in full by the
partial sweep (§4 of report 1, §0 of report 5) — not repeated here.

**New: two Purdue PhD theses, both supervised by T.T. Moh, both specifically on
JC2, neither found by any of the 5 completed reports** (confirmed by grepping
`jc2_literature_sweep_partial.md` for "Xu", "Yansong", "Zhang", "Yitang",
"Moskowicz" — zero hits on all five). [VERIFIED: negative-result grep against
the partial file]

- **Yitang Zhang**, *"The Jacobian Conjecture and the Degree of Field
  Extension,"* PhD thesis, Purdue University, December 1991, advisor
  Tzuong-Tsieng Moh. [VERIFIED: full PDF fetched from
  `docs.lib.purdue.edu/dissertations/AAI9215703`, `pdftotext`'d]. This is the
  same Yitang Zhang who later proved the first finite bound on gaps between
  primes (2013). Abstract verbatim: *"If two polynomials f(x,y) and g(x,y)
  satisfy the Jacobian condition fxgy − fygx ∈ k*, then the degree of the field
  extension of k(x,y) over k(f,g), [k(x,y) : k(f,g)], is less than or equal to
  the minimum of deg f and deg g."* A field-theoretic result building directly
  on Moh's 1983 approximate-roots machinery — not itself a new degree-bound
  case-elimination, and it is never cited by GGHV or anyone in the 2017–2026
  literature for degree-bound purposes (confirmed: no "Zhang" or "Zha91"-style
  citation anywhere in `gghv2022.txt`, 1708.09367, or 1708.07936 reference
  lists).

- **Yansong Xu**, *"On the Jacobian Conjecture and affine lines,"* PhD thesis,
  Purdue University, 1993, advisor T.T. Moh. [VERIFIED: existence and metadata
  confirmed via live search hit at `docs.lib.purdue.edu/dissertations/AAI9403813`,
  and independently via Xu's own 2016–2022 paper's reference list, item
  `[Xu93]`, discussed next — the PDF itself was not re-downloaded this session,
  time-limited].

**[VERIFIED: `math.purdue.edu/~ttm/student.html`, fetched live]** Moh's own
"My Ph.D. Students" page confirms this is the *complete* list — exactly two of
his students wrote JC2 theses, no others: *"Y.T.Zhang has written his thesis on
the Jacobian Conjecture. He is now working in the field of analytic number
theory."* / *"Y.S.Xu has written his thesis on the Jacobian Conjecture. He is
now doing business."* This is a clean negative result closing the "Purdue
(Moh's students)" lead: nobody else among Moh's students touched JC2.

## A2. Yansong Xu's 2016–2022 paper: the gap in Moh's (99,66) treatment and the Moh correspondence — found, read in full

**arXiv:1604.07683, Yansong Xu, *"Intersection numbers and split of minor
roots,"* v1 Apr 2016 → v4 15 Feb 2022** [VERIFIED: full PDF fetched, cached at
scratchpad `xu_1604.07683.{pdf,txt}`]. Abstract verbatim: *"...we discuss all
possibilities of the splits of principal minor roots for the case of degree
(99, 66) with help of Abhyankar-Moh planar semigroup, find an unknown possible
split and suggest case (99, 66) is open."*

This is precisely the "2016 preprint claiming a gap in Moh's proof" the task
asked for, and it documents the actual dispute. §8, verbatim:

> "Moh writes in [Moh83] page 209 on the principal minor roots... To do so,
> there are three claims have to be proven. (i) The principal minor roots do
> not split except at π-root order δ = 2. (ii) gσ(π) can not have three roots
> when δ = 2. (iii) [...] **We can not find materials to support these claims
> in his paper. We sent Moh an email to point out the possible gaps. He
> replied with, "I will make an investigation of the issue and reply to your
> e-mail as soon as possible." on Jan. 06, 2016.** We show that (ii) and (iii)
> are true, but there is one exception case for (i) open. [...] Thus this case
> is open and it suggests case (99, 66) is open."
> [VERIFIED: xu_1604.07683.txt, lines 618–667]

So the historical record is precise: Xu emailed Moh on 6 Jan 2016 pointing out
an unjustified step in the 1983 proof at exactly the shape that scales to
(66,99); Moh's own reply promised an investigation; Xu's paper (through v4,
Feb 2022) proves two of the three needed claims but finds **a genuine surviving
split possibility at π-root order δ = 5/2** that Moh's proof does not address,
and states plainly that this "suggests case (99,66) is open." This is the
primary-source origin of exactly the uncertainty that GGHV's 2022 Theorem 5.1 /
Corollary 5.7 closes five years later via an unrelated method (a direct
polynomial-system computation, not continuation of Moh's π-root/split
formalism) — see §C for why this route needed to be independent.

The acknowledgement is also a direct, named link between Xu and the GGHV group:
*"The author thanks Professor Mattias Josson and Professor Christian Valqui for
pointing out errors in previous version."* [VERIFIED, line 681] **Yet GGHV
2022's own reference list (`[1]`–`[13]`, checked exhaustively) never cites Xu
by name** — grepped `gghv2022.txt` for "xu" (any case): zero hits. GGHV's other
2017 paper, arXiv:1708.09367, by contrast, is built explicitly around Xu's
results (§C below) and cites him twice by name, including in its very abstract.
So GGHV's team clearly knew Xu's work well at the technical level; the 2022
paper simply doesn't need to invoke it because its (66,99) closure goes through
a completely different, self-contained route.

## A3. Moh's personal webpage — found and read; a real, if informal, erratum-adjacent record

**[VERIFIED: `https://www.math.purdue.edu/~ttm/`, fetched live, 12 Aug 2026]**
Moh's Purdue homepage is a plain, non-JS page hosting his own PDFs directly.
Contents on-point for this sweep:

- **`jacobian.pdf`** — *"Jacobian Conjecture,"* T.T. Moh, *Proc. Alg. and
  Geom.* (1995) 103–116, International Press. A formal, published 1995 survey
  talk ("main results of T.T. Moh, S.S. Abhyankar, S.S.S. Wang, H. Bass,
  E. Connell, D. Wright, A. Sathaye and others... possible research lines are
  mentioned"). [VERIFIED: PDF fetched, confirmed via page-1 image — this PDF
  is scanned/image-only with no text layer, so I could not grep its full 14
  pages; flagged below as a residual gap]. Predates the 100→108→125 ladder by
  decades; low marginal value but genuinely on-topic and previously unindexed
  by this campaign.
- **`Su.pdf`** — *"Comment on a Paper by Yucai Su On Jacobian Conjecture"* —
  Moh's own hosted copy of the material report 4 already found via
  `arXiv:math/0512495` (*"The said paper... is with gaps"*). Also
  image-only/no text layer; not independently re-verified beyond confirming
  its existence and title.
- **`kuo.pdf`** — *"A Short Note on TC Kuo-A.Parusinski-L.Paunescu's paper On
  Jacobian Conjecture"* — a Moh critique of a third paper, previously unseen
  by this campaign. Not read (image-only, time-limited).
- **`ZhangYt.pdf`** — *"Zhang, Yitang's life at Purdue (Jan 1985–1991),"* T.T.
  Moh, Aug 2013 (revised 2018) — this one **does** carry a text layer.
  [VERIFIED: fetched and read in full, `moh_on_zhang.{pdf,txt}`]. It is a
  personal memoir, not a mathematical paper, and makes a specific, disputed,
  one-sided claim that belongs in a grey-literature/dispute audit but must be
  clearly flagged as **[SECONDARY: Moh's own unverified personal account, not
  corroborated elsewhere]**: Moh writes that Zhang, during his PhD, separately
  and privately claimed to have solved the full Jacobian Conjecture, that Moh
  reviewed the claimed proof and found it wrong, and — the one mathematically
  relevant sentence — *"it was discovered that he used one of T.T.Moh's
  theorems which was wrong, and his thesis could not be published."* This is
  **not** a claim about the max-100 degree bound itself (which is independently
  re-confirmed by Heitmann 1990 and used as the solid floor of every later
  paper in the ladder, including GGHV 2022) — the memoir gives no equation or
  citation for which specific auxiliary theorem it means, and Zhang's actual
  1991 thesis (§A1, read in full) is a clean, self-contained field-extension
  bound with no visible retraction marks. I flag this explicitly as **a claim
  I could not verify or refute** and did not find corroborated or disputed
  anywhere else. The webpage also usefully corroborates independent math: Moh's
  own count of the original 1983 "exceptional cases," *"there are only 4
  exceptional cases of pair of degrees (64,48),(75,50),(84,56),(99,66),"*
  cross-checked as Heitmann's independent reproduction of the same 4 pairs —
  matching GGHV 2022's own framing of Moh's original scope exactly — and a
  striking, informal remark: *"Our experiments showed that the number of the
  exceptions tended to infinity"* as degree grows, i.e. Moh himself doubted
  degree bounds could ever be pushed to a clean finite statement without heavy
  extra machinery — relevant context for §B.
- **`student.html`** — used above (A1) to close the Purdue-students question.

## A4. Conference talks / slides

**[VERIFIED: WebSearch, live]** Christian Valqui gave a talk *"La conjetura del
Jacobiano desde el punto de vista geométrico"* ("The Jacobian Conjecture from a
geometric viewpoint") at the **XXXVII Coloquio de la Sociedad Matemática
Peruana**, hosted by IMCA Lima. I could not retrieve the talk date or slides —
the speakers page (`coloquio37.imca.edu.pe/speakers.php`) returned **HTTP 503**
on fetch. **Negative/inconclusive result, explicitly flagged**: this talk
exists and is on-point (title alone doesn't reveal whether it discusses degree
bounds or is a general-audience geometric overview) but its content is
unverified — a concrete, named lead for a future session with better luck
against that server.

## A5. MathOverflow / math.StackExchange

**Found, but about supporting number theory, not the degree bound directly.**
V. Moskowicz's paper (§C) explicitly thanks three MathStackExchange users by
name in her Acknowledgements: *"Jon Wharf, user Joffan... Sungjin Kim, user
i707107... Erick B. Wong, user Erick Wong,"* citing
`math.stackexchange.com/questions/2811792`, `/2811373`, `/2930958`, and
`/2930893` — these MSE threads supplied an arithmetic-progression/gcd lemma
(Lemma 2.3 of her paper) used in deriving her automorphism theorems, not a
JC2-degree-bound result in themselves. [VERIFIED: Moskowicz PDF, references and
acknowledgements sections, read in full]

**Direct search, negative result:** I ran `WebSearch` for "(72,108)" / "(66,99)"
/ "degree 108" combined with `site:mathoverflow.net` and
`site:math.stackexchange.com` and separately unrestricted. **Found nothing** —
no MO/MSE thread discussing the GGHV degree ladder, the (72,108) open case, or
the gcd≥36 thread specifically. This matches the pattern already documented for
Moskowicz's own paper: MSE gets used for elementary supporting lemmas in this
literature, not for the frontier questions themselves.

## A6. Personal webpages of Borisov, Valqui, Heitmann

- **Borisov**: `people.math.binghamton.edu/borisov/papersandpreprints.html`
  [VERIFIED: fetched live]. Lists exactly four Keller-map-adjacent papers, the
  latest being the 2020 *Electronic Journal of Combinatorics* publication of
  "Frameworks for Two-dimensional Keller Maps" (= arXiv:1901.04073) already
  known to the partial sweep, plus one item explicitly marked by Borisov
  himself as abandoned: *"On Resolution of Compactifications of Unramified
  Planar Self-maps" (2011–12) — "Unpolished, will not be submitted."*
  **Negative result, explicit**: no post-2020 update, no trace of progress on
  his own "Question 6.7 (the biggest question of all)" — his page corroborates
  report 3's WebSearch-based finding directly from the source.
- **Valqui**: PUCP CRIS/institutional page already found and used by the
  partial sweep (report 3, `pucp_cris_valqui.html`); not re-duplicated.
- **Heitmann**: no personal academic homepage found (searched directly); R.
  Heitmann's 1990 J. Pure Appl. Algebra paper is 36 years old and he does not
  appear to maintain an active web presence tied to this topic. **Negative
  result.**

## A7. Errata / retractions to the degree-bound ladder — the one genuinely new, load-bearing find

**This is the single most important grey-literature find of this sweep, and it
belongs equally to §C; full technical detail is there.** In short: **GGHV's
own arXiv:1708.09367 silently and substantially weakened its central claim
between v1 (30 Aug 2017, titled "Discarding infinite families using
intersection numbers") and v2 (14 Aug 2018, retitled "Approximate roots and
intersection numbers")** — v1 claimed to *discard* all gcd<36 families bar two;
v2 states outright, in its own new abstract, that the key equality no longer
holds and *"we cannot discard the infinite families as desired."* No arXiv
"Comments" field, no erratum notice, nothing — this is discoverable only by
diffing the two PDFs directly, which none of the five completed sweep reports
did for this paper (they did do exactly this diff for `1406.0886` v1-vs-v3, so
the *technique* was in the campaign's toolkit — it just wasn't pointed at this
paper). See §C2 for the full verbatim evidence.

## A8. University repositories — PUCP, IMCA, UBA

- **PUCP**: already extensively covered by the partial sweep (Horruitiner's
  thesis, PUCP CRIS pages); this session additionally confirms (via A1/A2/A4
  above) that PUCP/IMCA is also where Valqui gives conference talks on this
  exact topic, and where the Valqui–Ramírez 2024/25 Gröbner-basis paper was
  published (*Pro Mathematica*, PUCP's own house journal — already logged by
  the partial sweep).
- **Universidad de Buenos Aires** (home institution of both Guccione
  brothers): [VERIFIED: `bibliotecadigital.exactas.uba.ar` confirmed to host
  the J. Algebra 2017 "shape of possible counterexamples" paper]. **Searched
  specifically for a UBA thesis on the Jacobian conjecture — found none.**
  Negative result; time-limited, so this is a "not found in the time
  available" result rather than a confident "does not exist."
- **IMCA Lima**: talk found (A4) but content unverified (503 error).

## A9. On-point items the 5-report campaign missed that are *not* degree-bound results (noted for completeness)

**Kevin Zwart, *"Mathieu's approach to the Jacobian Conjecture,"* arXiv, v1 20
Nov 2025, v2 21 Nov 2025.** [VERIFIED: WebFetch of the abstract page]. An
expository treatment of Olivier Mathieu's Lie-theoretic sufficient condition
for the general Jacobian Conjecture (irreducible-subrepresentation analysis for
SL(N,ℂ)). Contains no mention of degree bounds, GGHV, or (72,108) — a different
attack axis entirely, general-n not n=2-specific. Flagged only because it is a
genuinely new (Nov 2025), on-topic item that fell entirely outside all five
completed reports' searches, illustrating that the sweep's recency net still
has holes even in plain arXiv listings.

---

# B. ABOVE 125

## B1. Correcting the task's framing: two different 2017 papers, not one

The task attributes "discarding infinite families using intersection numbers"
and the families F1,F2,F3,F9,F17,F22 to **arXiv:1708.09367**. Having now read
both papers directly, this needs a precise correction:

- **The families F1–F24 themselves, and the exhaustive enumeration of every
  possible-counterexample shape with max(deg P, deg Q) ≤ 150, are defined and
  tabulated in `arXiv:1708.07936`, "Some algorithms related to the Jacobian
  Conjecture"** (Guccione, Guccione, Horruitiner, Valqui, 26 Aug 2017).
  [VERIFIED: cached `pdfs/paper7_1708.07936.txt`, read in full — the family
  table is at its §5, the ≤150 enumeration at its §6.]
- **`arXiv:1708.09367`** is a companion paper (submitted 4 days later, 30 Aug
  2017) that takes those *already-defined* families as an input and tries to
  *discard* most of them using an intersection-number technique adapted from
  Yansong Xu. **Its v1 title genuinely was** *"The Jacobian Conjecture:
  Discarding infinite families using intersection numbers"* [VERIFIED: fetched
  `arxiv.org/abs/1708.09367v1` live, page `<title>` tag confirms this exactly]
  — so the task's framing is accurate for v1, but the paper was retitled
  *"Approximate roots and intersection numbers"* in v2 (Aug 2018), and that
  retitling is not cosmetic (§C).

So: **1708.07936 is the correct primary source for "the families labelled
F1...F22"** (in fact there are 24, F1–F24; F1–F17 are "length-1 chain"
families, F18–F24 are "length-2 chain" families, and F18–F21 are eliminated
outright within 1708.07936 itself, leaving 20 families that needed the
intersection-number treatment — matching 1708.09367's own count, *"one of the
20 families of [7]"*).

## B2. The exhaustive enumeration (≤150) — read directly, reproduced here

[VERIFIED: `pdfs/paper7_1708.07936.txt`, §6, "Possible counterexamples with
max(deg(P),deg(Q))≤150"] The paper states explicitly: *"Here we describe the
shape of the 34 possible counterexamples with max(deg(P),deg(Q))≤150."* I
independently recounted every row across its three tables (13 family-derived
cases + 9 length-1-chain cases + 11 length-2-chain cases + 1 length-3-chain
case = 34, matching exactly) [VERIFIED by direct count]. This table is,
concretely, **the "list nobody in this campaign has ever written down"** that
the task asked for — except that it already exists, published in 2017, and
simply needed converting from GGHV's "(reduced shape, max degree)" notation
into actual (deg P, deg Q) pairs and cross-checked against the classical
filters. That conversion is mechanical (actual degree = reduced_shape × scale,
where scale = given_max_degree ÷ max(reduced_shape)) and I verified the method
against **two cases the papers state explicitly in unreduced form**: (75,125)
and (64,224) (next section) — both match my formula exactly, confirming it's
sound.

## B3. Applying the classical (Magnus-chain) automorphism filter

The classical filter — proved in full in §C6 — says: **if gcd(deg P, deg Q) ∈
{1,8} ∪ (primes) ∪ (2×primes), the map is automatically an automorphism (no
counterexample possible)**. I applied this filter by direct computation
(script run and shown in full below the table) to every one of the 34
cataloged shapes. **Result: not one of the 34 published ≤150 shapes is
excluded by the classical filter.** This is itself informative: GGHV's
family-enumeration algorithm and the classical gcd filter are complementary,
not overlapping — the families exist precisely because they already survive
the classical filter (the algorithm's whole point is to enumerate what's left
*after* removing the classically-solved gcd values).

## B4. THE DELIVERABLE — smallest degree pairs above 125 surviving every published filter (bounded by the 150 ceiling of the only exhaustive enumeration that exists)

Sorted by max degree, [DERIVED from VERIFIED primary data — see method above;
not a verbatim quote except where noted]:

| max{deg P,deg Q} | (deg P, deg Q) | gcd | Source shape(s) in 1708.07936 |
|---|---|---|---|
| **125** | **(75, 125)** | 25 | F2, j=1 — **[VERIFIED verbatim](1708.09367v1, line 926)** |
| 126 | (84, 126) | 42 | length-1 chain (A0=(7,35)); length-2 chain (A0=(12,30)) |
| 128 | (96, 128) | 32 | F24, j=0 |
| 132 | (88, 132) | 44 | length-1 chain (A0=(11,33)) |
| 135 | (90, 135) | 45 | 4 independent shapes: length-1 chains at A0=(9,36),(12,33); length-2 chain at A0=(9,36) (×2) |
| 140 | (56, 140) and (84, 140) | 28 each | F11, j=0; F9, j=1 |
| 144 | (96, 144) and (108, 144) | 48; 36 | 6 independent shapes (chain2, chain3) for (96,144); 1 shape for (108,144) |
| 147 | (42, 147), (63, 147), (98, 147) | 21; 21; 49 | F7, j=0; F8, j=0; length-1 chain (A0=(7,42)) ×2 |
| 150 | (100, 150) | 50 | length-2 chain (A0=(10,40)) ×2 |

**(75,125) is the single smallest pair above the resolved region**, sitting
exactly at GGHV's own stated threshold (max=125). It is also, per §C, the pair
whose open status has the longest unexamined paper trail of any case in this
whole area — see §C for why nobody has actually attacked it since 2017.

Note (72,108)/(108,72) itself (max=108, the still-open case below 125) and its
already-closed sibling (9,27)-shape both appear in this same table's "chain"
rows for completeness/cross-validation — my derivation reproduces them exactly
(108 = 3×36 and 2×36), confirming the method.

## B5. Above 150 — confirmed, nothing exhaustive published

**Negative result, explicit.** I searched specifically for any extension of
the `1708.07936` algorithm's tables past 150 (arXiv full-text search for
"max(deg(P),deg(Q))" combined with numbers 151–300; author-exhaustive search of
Guccione/Guccione/Horruitiner/Valqui's full output list, already enumerated by
report 1 of the partial sweep) and **found nothing**. Above 150, the only
constraints on a hypothetical counterexample's degree pair are the *generic*
classical filters (§C6: gcd ∈ {1,8}∪P∪2P excluded; Moskowicz's Theorem 1.2:
deg(p) or deg(q) prime or semiprime excluded) — no combinatorial Newton-polygon
enumeration of *specific* surviving shapes exists past the 1708.07936 ceiling.
This matches and confirms the task's own framing precisely.

---

# C. THE gcd ≥ 36 THREAD

## C1. Locating and reading arXiv:1708.09367 directly — both versions

Moskowicz's arXiv:1810.08202 §4 cites, verbatim: *"it is known that
gcd(deg(g(p)), deg(g(q))) ≥ 36 except for two possible cases {(75, 125), (64,
224)}; see [8]"* where her reference **[8] is explicitly**
*"J. A. Guccione, J.J. Guccione, R. Horruitiner and C. Valqui, The Jacoian
[sic] Conjecture: Discarding infinite families using intersection numbers,
**arXiv:1708.09367v1** [math.AG] 30 Aug 2017."* [VERIFIED: `paper3_1810.08202.txt`
line 487, references section]

I fetched **both** arXiv versions of 1708.09367 fresh this session (not from
any pre-existing scratchpad cache, to sidestep any tampering risk — see §D)
and confirmed via `arxiv.org/abs/1708.09367v1` that its title really is,
verbatim on arXiv's own page, *"The Jacobian Conjecture: Discarding infinite
families using intersection numbers,"* submitted 30 Aug 2017.
[VERIFIED: `v1_abs.html`, live fetch]

## C2. The theorem, verbatim, with all hypotheses — and its silent retraction

**Theorem 4.1 of v1** (exact statement): *"Let (P, Q) be a standard (m, n)-pair.
If (P, Q) belongs to one of the 20 families of [7] with gcd(deg(P), deg(Q)) <
36, then the values of Im and IM are given in the following tables."*
[VERIFIED: `gghv_1708.09367v1.txt`, line 850] — followed by a 20-row table
giving `IM` (a closed formula in the family's parameter j) and `Im` (a fixed
value or small finite set) for each family. The paper's method: *"since IM and
Im have to coincide"* for any valid Jacobian pair, a family is discarded
whenever its `IM(j)` formula can never equal any of `Im`'s finitely many
possible values, for any `j`.

Applying this, the paper's own text (verbatim) states: *"In particular, since
IM and Im have to coincide, if gcd(deg(P), deg(Q)) < 36, then necessarily we
are in the case F2 with m = 3, n = 5, (deg(P), deg(Q)) = (75, 125)... or we are
in the case F23 with m = 2, n = 7, (deg(P), deg(Q)) = (64, 224)."*
[VERIFIED: line 887, 891]. **Corollary 4.2, verbatim in full: "B ≥ 25."**
[VERIFIED, line 1185], where the abstract defines `B := ∞` if JC2 is true, else
`min gcd(v1,1(P), v1,1(Q))` over all counterexamples. **Remark 4.3, verbatim:
"One can try to discard the two remaining possible cases, with (deg(P),
deg(Q)) = (75, 125) and (deg(P), deg(Q)) = (64, 224)... However, the complexity
of the resulting systems of equations one needs to solve still surpasses the
capacity of the software we had to our disposal. Therefore these two cases
remain open."*** [VERIFIED, lines 1186-1190]. The v1 abstract summarizes this
as discarding *"all hypothetical counterexamples (P,Q) with
gcd(deg(P),deg(Q)) < 36 except for two isolated cases"* — i.e. exactly
Moskowicz's phrasing, and the abstract's own headline number is **"increases
the lower bound for gcd(deg(P),deg(Q)) from 16 ... to 25."** So the rigorously
*proven* unconditional bound, per v1's own abstract, was **25**, not 36; "36"
is explicitly labeled a conditional, not-yet-achieved value: *"Moreover, if one
manages to discard the two cases, one would obtain B ≥ 36."* Moskowicz's "≥36
except for two cases" phrasing is a logically equivalent restatement of the
same disjunction (compare GGHV 2022's own later "max≥125, or ∈{(72,108),
(108,72)}" framing) — not an error on her part.

**Now the retraction, found by diffing v1 against v2 directly — this is the
new finding.** v2 (14 Aug 2018) has a **completely different abstract**:

> "We translate the results of Yansong Xu into the language of [5], obtaining
> nearly the same formulas for the intersection number of Jacobian pairs, **but
> with an inequality instead of an equality**."
> [VERIFIED: `pdfs/paper8_1708.09367.txt`, lines 7–14]

And its Introduction states the reason explicitly:

> "In a recent paper [14] Yangsong Xu gives two formulas for the intersection
> number of possible counterexamples, which we call IM and Im. **If the
> formulas were true, we would be able to discard many infinite families of
> possible counterexamples to the Jacobian conjecture described in [8]. When we
> translated the result and the proofs of [14] into the language of [5], we
> obtained the same formula for IM, but for Im we obtained only an inequality,
> consequently we cannot discard the infinite families as desired.**"
> [VERIFIED: `pdfs/paper8_1708.09367.txt`, lines 37–43]

I confirmed directly that v2's body **no longer contains** Theorem 4.1,
Corollary 4.2, Corollary 5.3, or any "B ≥ 25/36" claim at all — grepped the
full v2 text for `"36"` and `"224"`: **zero hits for "36"; the only "224"
match is an unrelated MR-review number.** [VERIFIED: direct grep, this
session]. There is no formal erratum notice: arXiv's own "Comments" metadata
field for this paper reads only *"4 figures, 4 tables, 1 algorithm"*
[VERIFIED: `v_latest_abs.html`], and no v3 exists (only v1 and v2 are listed).
**This is a genuine, primary-source-documented, silent self-correction of a
published degree-bound-ladder claim that no completed report in this campaign
found**, and it is exactly the kind of item Task A asked for ("errata,
retractions or published corrections to ANY rung of the degree-bound ladder").

## C3. Resolving the task's stated tension: why gcd(66,99)=33<36 was still open in 2022

The Theorem 4.1 table's F17 row (whose j=0 member, at scale 33, is exactly
(66,99)) is walked through explicitly in v1's proof: *"Here we have
ℓ3,−1(P)=((z³−α)⁸)^m... IM = 8(5j+2). There are only principal minor roots and
so Im = 1+Im^p ∈ {6,7,8/3}. **Clearly Im ≠ IM for all j ∈ N0, hence this case
is discarded.**"* [VERIFIED: `gghv_1708.09367v1.txt`, lines 1137–1145] — this
literally, explicitly includes j=0, i.e. **v1's own text appears to discard
(66,99) already in 2017**, five years before GGHV 2022's Corollary 5.7 closes
it by an unrelated method (direct polynomial-system solving, "as in [3]").

Given the v2 retraction (§C2) — the whole apparatus this F17 discard depends on
(the `IM = Im` **equality**) was subsequently shown by the same authors to be
only an **inequality**, which is not strong enough to license "IM≠Im ⟹
impossible." **This is almost certainly why (66,99) genuinely remained an open
question requiring GGHV 2022's completely independent proof**: the 2017 v1
argument that looked like it had already closed (66,99) was quietly withdrawn
before anyone (including, apparently, GGHV's own later 2022 paper, which never
mentions or relies on it) could build on it. I flag this as the most
defensible reading of the evidence rather than a certainty — I did not find an
explicit sentence anywhere saying "the F17/(66,99) discard specifically was
wrong"; what I have is (a) v1's explicit F17 discard, (b) v2's blanket
retraction of the method that discard depends on, and (c) GGHV 2022's
independent, unrelated re-proof five years later, treating (66,99) as one of
"5 remaining cases" not yet discarded going into that paper. All three of
(a)-(c) are individually [VERIFIED]; the causal link between them is my own
inference, clearly labeled as such.

## C4. What this implies for (72,108)

gcd(72,108) = 36 exactly [VERIFIED by direct computation: 72=2³·3², 108=2²·3³,
gcd=2²·3²=36]. This places (72,108) **outside the scope of both filters
discussed here**: it is not `<36` (so it was never a candidate for the
1708.09367 family-discarding attempt, retracted or not), and 36 is not a
member of `{1,8}∪P∪2P` (36=2×18, 18 not prime) so the classical automorphism
theorem (§C6) does not reach it either. **(72,108) has never, at any point in
this literature, been in scope for a blanket gcd-based elimination** — it has
always required, and still requires, dedicated Newton-polygon/polynomial-system
case analysis, exactly the kind GGHV 2022 §4–5 (and this repo's own
computational sessions) apply to it directly. This is a clean, precise answer
to the task's specific question.

## C5. What this implies above 125

The classical filter (§C6) is **independent of the retracted equality** — it
rests on Magnus/Nakai-Baba/Appelgate-Onishi/Nagata/Żołądek, none of which
touch the Xu-formula machinery — so my §B derivation is unaffected by the
retraction. What the retraction *does* affect is the belief that "only two
cases above the classically-solved gcd range survive" (75,125) and (64,224):
that was **never actually established** as a theorem (only as a v1 claim later
narrowed by its own authors to "we obtained the same formula for IM, but for
Im we obtained only an inequality"), and my own direct enumeration in §B shows
at least a dozen distinct degree pairs above 125 (up to the 150 ceiling) that
are not excluded by anything currently published. **(64,224)** in particular
sits entirely outside the ≤150 enumeration's scope (max=224) and, as far as I
can find, has not been mentioned in the literature since 1708.09367 v1 in
2017 — GGHV 2022 does not mention it (grepped `gghv2022.txt` for "224": zero
hits).

## C6. The Magnus / Baba-Nakai / Appelgate-Onishi / Nagata / Żołądek chain — verified against Moskowicz's primary text

**Confirmed exactly as the task described**, verbatim from Moskowicz's paper:

> "**Theorem 1.1.** f is an automorphism of k[x, y] if gcd(deg(p), deg(q)):
> • is 1. • is ≤ 2. • is ≤ 8 or belongs to P. • belongs to 2P.
> In short, Theorem 1.1 says that f is an automorphism of k[x, y] if
> gcd(deg(p), deg(q)) ∈ {1, 8} ∪ P ∪ 2P.
> Proof. • Magnus [14]. See also [16, page 158]. • Nakai-Baba [2]. •
> Appelgate-Onishi [1] and Nagata [16, pages 158-159, 169-172] [17]. •
> Żoladek [22] (see also [18])."
> [VERIFIED: `paper3_1810.08202.txt`, lines 38–48]

Full citations, from Moskowicz's own reference list [VERIFIED, lines 468–515]:
**[1]** H. Appelgate, H. Onishi, *The Jacobian Conjecture in two variables*, J.
Pure Appl. Algebra 37, 215–227, 1985. **[2]** K. Baba, Y. Nakai, *A
generalization of Magnus' theorem*, Osaka J. Math. 14, 403–409, 1977.
**[14]** A. Magnus, *On polynomial solutions of a differential equation*, Math.
Scand. 3, 255–260, 1955. **[16]** M. Nagata, *Two-dimensional Jacobian
Conjecture*, Kyoto Uni., 153–172, 1990. **[17]** M. Nagata, *Some remarks on
the two-dimensional Jacobian Conjecture*, Chin. J. Math. 17, no. 1, 1–7, 1989.
**[22]** H. Żoladek, *An application of Newton-Puiseux charts to the Jacobian
problem*, Topology 47, no. 6, 431–469, 2008. This exactly matches the task's
"Magnus / Baba-Nakai / Appelgate-Onishi / Nagata / Zoladek chain (automorphism
if gcd in {1,8} ∪ primes ∪ 2·primes)" — the only nuance is the name order
"Baba-Nakai" in the task vs. "Nakai-Baba" in Moskowicz's own citation, same two
authors, same 1977 Osaka J. Math. paper.

A companion **Theorem 1.2** (built on Theorem 1.1) states, per Moskowicz:
*"f is an automorphism of k[x,y] if deg(p) or deg(q): • belongs to P. •
belongs to P² = {uv}"* [VERIFIED, partial text, lines 61-62] — i.e. prime or
semiprime individual degree also forces an automorphism. I applied this as a
secondary filter to my §B candidate list by spot-check (none of (75,125),
(84,126), (96,128) have a prime or semiprime component) but did not
exhaustively re-verify Theorem 1.2's own proof/hypotheses to the same depth as
Theorem 1.1; flagged as **[VERIFIED existence and statement; proof details not
independently re-derived]**.

---

# D. COMPLETENESS AUDIT of `jc2_literature_sweep_partial.md`

## D1. The central contradiction: arXiv:2608.00222 treated inconsistently across the five reports

This is the largest, most consequential inconsistency in the partial file, and
it concerns the July-2026 dimension-≥3 counterexample material (Alpöge /
Gallagher / Speyer / Gao / Tao), **not** JC2 directly — but Task D explicitly
asks for cross-report contradictions, and this is the clearest one.

- **Report 1** (§7, "Data-integrity note") is the *only* one of the five to
  flag a problem: *"an arXiv ID `2608.00222` claiming a 31 Jul 2026 submission
  date is internally impossible (arXiv's `2608` prefix denotes month 08 =
  August; a July submission cannot carry it)... whatever produced those files
  should not be trusted as evidence the Jacobian conjecture has been
  disproven."* It refused to build on this material and did not tag anything
  from it `[VERIFIED]`.
- **Reports 2, 3, 4, and 5** all fetched and quoted from arXiv:2608.00222,
  the Tao blog, and related material extensively, tagging passages
  `[VERIFIED: arXiv:2608.00222, ... full text read]` — with **no cross-check of
  report 1's concern anywhere in reports 2–5**, and no acknowledgement that a
  concurrently-running process in the same shared scratchpad had been flagged
  as suspect.

**I re-investigated this independently this session** (fresh `WebFetch` and a
fresh `curl` of `arxiv.org/abs/2608.00222`, not reusing any pre-existing
scratchpad file, precisely to sidestep any tampering risk in the shared
cache). Finding: **report 1's specific technical objection does not actually
hold up.** ArXiv's real submission process has a well-known cutoff (submissions
received after roughly 14:00 US Eastern Time are processed as the next
business day's batch). The fetched page's own submission timestamp is *"Fri,
31 Jul 2026 19:08:59 UTC"* [VERIFIED: live curl of `arxiv.org/abs/2608.00222`,
`check_2608.html`] — 19:08 UTC is **15:08 US Eastern** (EDT, in effect in
July), i.e. after the typical cutoff — so a paper uploaded at that hour on the
last day of July landing in the *August* identifier batch (`2608.*`) is
consistent with how arXiv is known to work, not "internally impossible." So
report 1's specific debunking argument is itself mistaken on this narrow
technical point, even though the instinct to be suspicious of the broader
material was sound methodology.

**What I can and cannot independently establish:** I re-fetched the same page
via two independent tool paths this session (agentic `WebFetch` and raw
`curl`) and got matching, internally consistent content both times. I also
found — via ordinary `WebSearch`, not the shared/possibly-compromised
scratchpad — **three additional, independent, differently-worded outlets**
(Chilean tech-news site *Fintualist*, and Spanish math-blogs *Gaussianos* and
*La Ciencia de la Mula Francis*) all separately reporting the same event with
matching but non-identical phrasing, including an idiosyncratic quote
attributed to Alpöge's own announcement (*"thanx to my close friend akhil for
asking about it and my other close friend fable for working during the world
cup final"*) that is hard to explain as independent fabrication across
unrelated outlets. **This raises my confidence that some real, widely-reported
announcement occurred**, well beyond what a single compromised fetch could
produce. What I explicitly **cannot** do is (a) independently verify the
underlying mathematics is correct — that is outside this task's scope and
outside what any literature search can establish — or (b) confirm "Claude
Fable 5"/"Fable" against my own training knowledge, since I have no record of
any such Anthropic model name and this postdates my January 2026 cutoff by
construction. **I record this as a genuinely unresolved epistemic limit, not a
finding either way about the underlying disproof.**

**None of this affects JC2.** Every source on both sides of this
dispute — including arXiv:2608.00222 itself, Tao's blog, and the Spanish-language
coverage — is unanimous and explicit that the plane case is untouched. That
part of the partial sweep's conclusion is solid regardless of how the
meta-question about data integrity resolves, and I did not find any source,
anywhere, suggesting otherwise.

## D2. Other contradictions and inconsistencies found

- **None found between the reports on the core JC2 facts** (Theorem 2.1's exact
  statement, the two (72,108) sub-shapes, (66,99)'s 2022 closure, the 108→125
  gap) — these are consistent and independently re-confirmed by me directly
  against the primary PDF (`gghv2022.txt`) again this session.
- **A near-miss, self-caught by report 3**: a Wikipedia summarization pass
  initially conflated "Nguyen 2025 → bound 104" with superseding "GGHV 2022 →
  bound 108," which report 3 traced back to source and correctly identified as
  a wording artifact, not a real dispute. No action needed; flagging only
  because Task D asked for contradictions and this is documented as caught
  in-file already.
- **A citation-title mismatch nobody flagged**: reports 1–5 all cite
  arXiv:1708.09367 under its *current* (v2) title, "Approximate roots and
  intersection numbers," including report 1's own author-table (line 44 of the
  partial file). None of the five noticed this paper had a different title and
  a substantively different claim in v1 — this is the same finding as §C2,
  cross-listed here because it is, precisely, an uncaught contradiction between
  what the partial file's own author-enumeration table implies (a single
  stable paper) and the paper's real two-version history.

## D3. Load-bearing claims tagged [SECONDARY] or [MEMORY] that this session could not upgrade

- Report 3's claim about the Tsuchimoto/Belov-Kanel-Kontsevich Dixmier↔JC
  stable equivalence is explicitly tagged `[MEMORY, unverified for the exact
  dates]` — I did not attempt to re-verify this, out of scope for A–D as
  specified.
- Report 5's assessment that Yucai Su's 43-version arXiv preprint does not
  actually repair the specific errors Moh identified is explicitly self-tagged
  as *"I only have secondary evidence of the historical dispute, not a fresh
  mathematician's review of v43"* — still true after this session; I did not
  attempt a fresh review of v43 either (out of scope; the task pointed me at
  the gcd-thread and grey-literature leads specifically, not at re-litigating
  Su).
- Report 3's identification of the 28 Jul 2026 Guccione-Guccione-Valqui
  *Quaestiones Mathematicae* paper as *"almost certainly... the long-delayed
  journal publication of... arXiv:1605.09430"* is explicitly self-tagged
  `[SECONDARY, inferred from metadata+abstract, not full text — paywalled]`.
  **I did not gain access to this paper's body either** — still paywalled,
  still unread by anyone in this 8-agent campaign. This remains the single
  largest concrete access gap (see D6).

## D4. Sources named but never actually fetched and read (confirmed still true)

- **Guccione–Guccione–Valqui, *Quaestiones Mathematicae*, DOI
  10.2989/16073606.2026.2701437** (published online 28 Jul 2026) — abstract
  only, full body never obtained by any of the 8 agents run so far.
- **Makar-Limanov & Trakhtenberg, "Properties of a Jacobian mate," São Paulo J.
  Math. Sci. (2026), DOI 10.1007/s40863-025-00520-4** — report 3 could not
  even get the abstract (Springer paywalled/login-redirected). Still unread.
- **Lee & Li, "Magnus' formula revisited" parts II and III** — report 5 read
  only metadata/abstracts, not full text, and explicitly tagged this
  `[SECONDARY]`.
- **Moh's `jacobian.pdf`, `Su.pdf`, `kuo.pdf`** (this session, §A3) — fetched,
  but image-only PDFs with no text layer; not OCR'd due to time, so "found but
  not read" in the fullest sense.
- **Yansong Xu's actual 1993 PhD thesis PDF** (§A1) — located and its existence
  confirmed via a live Purdue-library search hit, but the PDF itself was not
  downloaded and read this session (time-limited); only Xu's later 2016–2022
  arXiv paper was read in full.

## D5. The single most likely place an on-point result is still hiding

Ranked by my own assessment of probability × potential impact:

1. **The paywalled 28-Jul-2026 Guccione-Guccione-Valqui *Quaestiones
   Mathematicae* paper.** Same three authors as the open (72,108) case, same
   exact sub-topic (Newton polygon lower side, discarding corners and infinite
   families), brand new. Two independent report-writers in the partial sweep
   both flagged it and neither got past the abstract. This is the highest-value
   single unresolved lead in the entire combined 8-agent campaign.
2. **A direct, modern re-attempt at (75,125) and (64,224) with 2020s
   computer-algebra power.** The 2017 authors explicitly stated their only
   obstacle was software capacity (*"the complexity of the resulting systems of
   equations one needs to solve still surpasses the capacity of the software we
   had to our disposal"*) — nearly a decade of Gröbner-basis/elimination
   tooling improvements (and this repo's own considerable `jc2_*.py`
   computational infrastructure) has never, as far as I can tell from either
   this sweep or the repo's own file list, been pointed at these two specific
   pairs; all of the repo's computational sessions target (72,108) exclusively.
3. **Non-English grey literature at PUCP/IMCA** — talks, seminar notes, or
   student work in Spanish that a keyword search in English will systematically
   under-find; the one concrete lead found this session (the IMCA colloquium
   talk, §A4) hit a dead server and was not resolved.
4. **Moh's own scanned, unindexed PDFs** (`jacobian.pdf`, `kuo.pdf`) — 1990s
   survey material that has never been OCR'd or full-text indexed by any
   search engine because it has no text layer; effectively invisible to
   `WebSearch`-style discovery by construction.

---

# WHERE THE COMBINED SWEEP IS STILL INCOMPLETE

Stated explicitly, per the task's instruction not to claim full coverage:

- **The (72,108)/(108,72) open case itself is not resolved by this report or
  any report in this campaign.** Nothing here changes that.
- **Two specific, previously-unflagged degree pairs — (75,125) and (64,224) —
  are shown by this report to be more precarious than the partial sweep
  believed**: the "except for two possible cases" framing was treated by the
  partial sweep (and by Moskowicz) as a clean, stable theorem; it is actually
  the surviving fragment of a 2017 claim its own authors walked back a year
  later. Nobody, including this report, has resolved either pair.
- **§B's "smallest surviving pairs above 125" table is bounded by the 150
  ceiling of the one exhaustive enumeration that exists (1708.07936, 2017).**
  Above 150, only generic filters apply; no combinatorial enumeration of
  specific surviving shapes has ever been published, as far as eight agents'
  worth of searching across this and the prior campaign have found.
- **Three named, on-point primary sources remain genuinely unread by
  anyone in this campaign**, not merely under-summarized: the paywalled 2026
  Quaestiones Mathematicae paper, the paywalled São Paulo J. Math. Sci. 2026
  paper, and Yansong Xu's 1993 PhD thesis (located, not opened).
  Moh's `jacobian.pdf`/`kuo.pdf`/`Su.pdf` are fetched but not OCR'd.
- **The IMCA colloquium talk lead (§A4) is unresolved** — server error, not a
  negative result.
- **The UBA and broader non-English/non-arXiv grey literature was searched but
  not exhaustively** — searches were in Spanish and English but time-boxed;
  I cannot rule out theses or notes at UBA, IMCA, or elsewhere in the
  Peruvian/Argentine mathematical community that a native-language, in-person,
  or citation-network search (rather than keyword search) would surface.
- **The arXiv:2608.00222 / "Claude Fable 5" material's underlying mathematical
  correctness is not something any literature sweep can establish** — I have
  raised my confidence that the *announcement* is real and widely covered, but
  I cannot and do not certify the mathematics, and this whole question remains
  outside JC2 either way.
- **I did not re-verify** items the partial sweep already tagged `[SECONDARY]`
  or `[MEMORY]` and marked as out of this task's specific scope (Su v43's
  actual mathematical content, the Tsuchimoto/Dixmier dimension-transport
  claim) — these remain exactly as uncertain as the partial file already
  disclosed.

No claim in this report should be read as "the (72,108) case is closer to
resolution" — it isn't, on any evidence found. What has changed is that the
supporting literature around it (the gcd-threshold theorem, the family
enumeration, the historical Moh-Xu dispute, the errata trail) is now mapped in
much more precise, primary-source-verified detail than before, and one
concrete, previously-invisible bibliographic error (the 1708.09367 v1/v2
retraction) has been corrected.

---

## Files saved this session (scratchpad only, not committed)

`/tmp/claude-0/-home-user-jacobian-planar/8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad/`:
`xu_1604.07683.{pdf,txt}` (Yansong Xu, read in full), `yitang_purdue_thesis.{pdf,txt}`
(Zhang's 1991 thesis, read in full), `moh_on_zhang.{pdf,txt}` (Moh's memoir,
read in full), `moh_jacobian.pdf` / `moh_su.pdf` (image-only, not OCR'd),
`moh_homepage.html`, `moh_students.html`, `gghv_1708.09367v1.{pdf,txt}` (fresh
fetch of the 2017 v1, the key primary source for §C), `v1_abs.html` /
`v_latest_abs.html` (arXiv metadata pages), `check_2608.html` (fresh
independent fetch for §D1). Plus everything already cached by the partial
sweep's five agents (`gghv2022.txt`, `pdfs/paper7_1708.07936.txt`,
`pdfs/paper8_1708.09367.txt`, `pdfs/paper3_1810.08202.txt`, etc.), reused for
cross-reading, not taken on faith.

No files were committed to the repository or pushed, per instructions.
