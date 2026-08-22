# TRACK E — Literature Verification Net

**Status: COMPLETE** (2026-08-13; all eight items verified; web sweep done; bottom line at end of file)

One-line verdicts: E1 VERIFIED · E2 VERIFIED · E3 VERIFIED · E4 VERIFIED · E5 VERIFIED · E6 VERIFIED (+1 shape addendum) · E7 VERIFIED (incl. the negative Belyi-polynomial claim) · E8 PREMISES STAND.

Sources (extracted text in scratchpad):
- `arxiv_2204.14178.txt` — GGHV (Guccione, Guccione, Horruitiner, Valqui), 2022
- `arxiv_2608.00222.txt` — Gao, 2026
- `arxiv_1708.09367v1.txt` / `arxiv_1708.09367v2.txt` — (v1 vs v2 diff)
- `arxiv_1708.07936.txt` — admissible pairs / §6
- `borisov1901.txt` — Borisov frameworks paper (arXiv:1901.04073)

Verdict key: **VERIFIED** = exact supporting quote found; **REFUTED** = text contradicts the claim; **NOT FOUND** = no supporting text located (claim may still be true but is unsupported by these sources); **PARTIAL** = some sub-claims verified, others not.

---

## E1. GGHV: counterexample ⇒ max degree ≥ 125 or pair (72,108)/(108,72)

**Verdict: VERIFIED**

Exact quote (Theorem 2.1, `arxiv_2204.14178.txt` lines 97–98, paper §2, p. 2):

> "Theorem 2.1. If (P, Q) is a counterexample to the Jacobian Conjecture, then we have either
> max{deg(P ), deg(Q)} ≥ 125, or (deg(P ), deg(Q)) ∈ {(72, 108), (108, 72)}."

Abstract (lines 8–11) agrees: "We list all the pairs (deg(P ), deg(Q)) with max{deg(P ), deg(Q)} < 125 for any hypothetical counterexample to the plane Jacobian Conjecture and discard them all, except the pair (72, 108) (and the symmetric pair (108, 72)), thus we confirm the lower bound of 100 obtained by Moh and raise it up to 108."

Caveat for downstream use: Theorem 2.1 is stated as the *aim* of §2 ("The aim is to prove the following result"), and its proof is distributed over §§2–6 relying on prior papers [1]–[7] of the same group and on Moh [10]. Within this paper the only fully self-contained discards are §3 (84 and 120), §5 ((66,99) and the (9,27) shape of (72,108)) and §6 (another proof of (56,84)). The pair list itself (10 cases, 5 previously solved) is imported from [5] (arXiv:1708.07936, see E6). So the theorem's strength is conditional on that chain of prior work — same caution as any single-group serial literature.

## E2. (66,99) excluded outright by GGHV

**Verdict: VERIFIED**

Exact quote (introduction, lines 79–82):

> "In section 5 we use the systems of polynomial equations associated
> to a possible counterexample as in [3] in order to discard the case (deg(P ), deg(Q)) = (66, 99) and
> one of the cases with (deg(P ), deg(Q)) = (72, 108)."

Mechanics verified in the text: (66,99) is the shape named "(9,24)" (table, line 125: corner A0 = (9,24), (m,n) = (2,3), max deg 99 — 9+24 = 33, so (deg P, deg Q) = (2·33, 3·33) = (66,99)). Proposition 4.2 ("Case (9,24)", lines 348–352) reduces it to three Newton-polygon possibilities with N(P) ⊇ {(1,1),(6,16),(6,18)}, N(Q) ⊇ {(1,0),(9,24),(9,27)}; §5's Theorem 5.1 (lines 658–663: "There exist no pair of polynomials P, Q ∈ K[x, y] such that (1) [P, Q] = x + g(y) … (2) en3,−1(P) = st1,0(P) = 2(3, 8) = (6, 16) and st−1,1(P) = en1,0(P) = 2(3, 9) = (6, 18), (3) en3,−1(Q) = st1,0(Q) = 3(3, 8) = (9, 24) and st−1,1(Q) = en1,0(Q) = 3(3, 9) = (9, 27)") kills exactly this configuration, by contradiction completed at "This contradiction concludes the proof of Theorem 5.1."

Nuance (does not change the verdict): the table row for (9,24)/99 says "no detail in [10]" — i.e. Moh (1983) already *claimed* max deg 99 impossible but published no detailed proof; GGHV's §5 is the first complete published discard. "Excluded outright by GGHV" is therefore accurate in the strong sense: GGHV do not lean on Moh's undetailed claim for this case.

## E3. (72,108) → two shapes; one closed, one explicitly left open

**Verdict: VERIFIED**

**The verbatim open-case sentence** (introduction, lines 80–82):

> "In section 5 we use the systems of polynomial equations associated
> to a possible counterexample as in [3] in order to discard the case (deg(P ), deg(Q)) = (66, 99) and
> one of the cases with (deg(P ), deg(Q)) = (72, 108). For the other case with (deg(P ), deg(Q)) =
> (72, 108) we couldn’t solve the corresponding system of polynomial equations, thus it is left open."

Reinforced at lines 87–90: "we have to combine these techniques in order to be able to increase the lower bound of 100 … up to 108. With enough computing power we would be able to raise it up from 108 to 125, since there is only one case left." (Note the paper's own framing: the missing ingredient is *computing power* for one polynomial system.)

**How the paper names/defines the two shapes.** They are named by the corner A0 of the reduced Newton polygon together with a multiplier pair (m,n); the underlying polygon has corners {(0,0),(1,0),A0,(0,b)} scaled by (m,n). From the case table (§2, lines 113–126), the two max-deg-108 rows are:

| A0 | (m,n) | max{deg P, deg Q} | previously discarded? |
|---|---|---|---|
| (8, 28) | *(3,2) | 108 | – |
| (9, 27) | (2,3) | 108 | – |

(Degrees: 8+28 = 36 = 9+27; (3,2)·36 → (108,72), (2,3)·36 → (72,108).) The asterisk on "(3,2)" appears in the extracted text without an explanation; the paper says solved cases are highlighted in red (color lost in extraction), and the asterisk plausibly flags the one case left open. Not load-bearing.

- **Closed shape = "Case (9,27)"**: Proposition 4.1 (lines 228–231) reduces it to N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)}, N(Q) = {(0,0),(1,0),(9,24),(9,27),(0,27)} with [P,Q] = x; killed by Corollary 5.7 (which reduces to Theorem 5.1).
- **Open shape = "Case (8,28)"**: Proposition 4.3 (lines 492–495) states: "If there is a counterexample to the Jacobian Conjecture in the case (8, 28), then there exist P, Q ∈ L(1) with [P, Q] = x2 and one of the following cases holds: (1) N (P ) = {(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)}, N (Q) = {(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)}. (2) N (P ) = {(0, 0), (1, 0), (8, 14), (8, 16)}, N (Q) = {(0, 0), (2, 1), (12, 21), (12, 24)}". **No section of the paper attacks the resulting polynomial system** — (8,28) appears only in §§2–4 (last substantive occurrence is Prop 4.3's proof); §5 handles (9,24)/(9,27), §6 handles (7,21). This confirms the open case is exactly the (8,28) shape.
- Note the bracket normalization differs between the shapes: [P,Q] = x for (9,27)/(9,24)/(7,21) but **[P,Q] = x²** for (8,28).
- Corroboration of the Track A/B handoff geometry: Prop 4.3's N(Q) contains the corners (2,1) and (12,21) — the endpoints of the slope-2 line j = 2i−3 that the lost session's 7-variable edge subsystem lived on ((12,21) is a *corner* of N(Q); (12,24) is the top corner). Consistent, not proof.

## E4. Gao 2608.00222 — what is actually proved; plane-case disclaimer; mechanism; transfer-to-dim-2

**Verdict: VERIFIED** (all handoff sub-claims check out; details below)

**Paper:** Shuhong Gao, "Counterexamples to the Jacobian conjecture in dimensions greater than two", arXiv:2608.00222v1 [math.AG], dated July 31, 2026. (Footnote: "AI disclosure: The main idea and framework are due to the author, and Claude Fable 5 assisted in the proofs and in the writing up of the paper.")

**Exactly what is proved (dimension / field / degrees).** Everything is over **C**. Context established by the paper (lines 14–17, 47–52 and refs [11]–[15]): the Jacobian conjecture was **refuted in dimension three by L. Alpöge on July 19, 2026** (announcement; ref [11]), with an infinite family by A. Gallagher (July 20, Zenodo doi:10.5281/zenodo.21479195, "every generic fiber degree n ≥ 3 occurs" — ref [12]) and the geometric "tangent sweep" explanation by D. E. Speyer (July 23 — ref [14]); exposition by Tao (July 21 — ref [15]). Alpöge's map F: C³→C³ has component degrees 7, 6, 4, det J(F) ≡ −2, generic fiber exactly 3 points (Theorem 3.3), with full fiber stratification {3,1,0} and image C³ \ C (Theorem 3.4). Gao's own contributions: a general construction ("sweeping tangent direction fields on parametrized hypersurfaces") valid **in every dimension n > 2**, producing counterexamples of **arbitrarily large geometric degree in each fixed dimension** (abstract, lines 18–22; lines 101–106), with five new explicit maps: G (3-dim, geometric degree 4), F4 (4-dim, degree 5, det ≡ −44/9), F5 (4-dim, degree 10), F6 (5-dim, degree 6, det ≡ −290), F7 (5-dim, degree 12); plus a propagation principle n ↦ n+3 (counterexamples in n−3 variables can serve as transverse data). All maps are étale (everywhere unramified) and non-proper; "All identities were verified in exact rational arithmetic"; Appendix A gives Gröbner-basis fiber certificates for F and G (complete stratifications of F4–F7 deferred to a subsequent version).

**The explicit plane-case disclaimer** — verbatim, §2, lines 121–124:

> "In dimension two, Moh [8] verified the
> conjecture for maps of degree at most 100; the two-dimensional case remains open and is untouched
> by the counterexamples discussed here, which exist only in dimension ≥ 3 (by Wang’s theorem,
> degree 2 examples are impossible, and the known constructions produce degree ≥ 3)."

**Mechanism summary (half page).** Two structural facts frame everything (§2, lines 125–135): (i) Bialynicki-Birula–Rosenlicht — an injective polynomial map Cⁿ→Cⁿ is an automorphism, so a Keller counterexample must be non-injective; (ii) a Keller map is étale, so distinct preimages can never collide over a target point — non-injectivity can only arise through **failure of properness** ("they can only escape to infinity"), and Jelonek's theorem says the non-properness locus is empty or a hypersurface. The construction realizes exactly this loophole:

1. *Sweep.* Take a parametrized plane curve K(w) = (p(w), q(w)) with deg q ≤ deg p + 1, normalized so the tangent direction field is δ = (2,w)ᵀ, i.e. q′ = w²p′ (eq. (1)). The tangent sweep S(γ,w) = (p(w)+2γ, q(w)+γw) sends (point of curve, position along its tangent line) to the plane; det J(S) = 2γ. By projective duality the sweep is unavoidably many-to-one: fibers of S biject with roots of the univariate **tangency polynomial** W_{X,Y}(w) = q(w) + w²(X−p(w)) − Y (eq. (2)), of degree d+1 for d = deg p (d+1 = the class of K, by Plücker). The exact identity W′_{X,Y}(w) = γ (eq. (3)) makes multiple roots ⟺ γ = 0 ⟺ target on the swept curve: the discriminant locus is the curve itself (envelope of its tangents).
2. *Monomial twist.* S is not Keller (det = 2γ). Pad to three variables and conjugate: with γ = γ₀ + axy + bx²z, u = 1+xy, w = γu, C = γx, the composite (C, P/C, Q/C²) (P = p(w)+2γ, Q = q(w)+γw) has constant Jacobian −2b, **provided** the divisibilities C | P and C² | Q hold — finitely many linear "side conditions" on the coefficients of p. The twisted coordinate C = γx degenerates exactly on the sweep's ramification locus γ = 0, so the composite is everywhere unramified; sheets that would have merged over the curve now **escape to infinity**. "The construction converts ramification into non-properness" (§3.3). Varying d gives Gallagher's family — "which defeats all approaches to the conjecture through degree bounds."
3. *Generalization (§4).* Replace the plane curve by a parametrized hypersurface X: Cⁿ⁻² → Cⁿ⁻¹ carrying a prescribed tangent direction field Δ (unimodular component row); tangency is an exterior-product criterion; the twist's side conditions become "discrete data and stage equations" (§4.3); different direction fields (curve-type (1,w₁,…,w₁ⁿ⁻²)ᵀ vs mixed) select different escape branches, some rigid (Problem 4.8, open), some flexible. The curve-type field admits a uniform reduction (Theorem 4.9): prescribing a w₁-family of constant-Jacobian maps of Cⁿ⁻³ plus one free potential — this is what lets counterexamples propagate n ↦ n+3 and gives arbitrarily large geometric degree via the degree of the univariate fiber polynomial (Prop 4.11).

**Transfer-to-dim-2 assessment.** Direct transfer is structurally impossible, for reasons visible in the construction itself:

- *Dimension count of the architecture.* The framework needs a positive-dimensional swept object: a hypersurface of dimension n−2 ≥ 1 in Cⁿ⁻¹ (so n ≥ 3), plus one multiplier variable γ, plus the twist variable(s). For n = 2 the "swept object" would be 0-dimensional (a point of C¹) — there is no 1-parameter family of tangent objects, hence no duality-forced many-to-oneness. Equivalently: the plane sweep S(γ,w) already uses two variables and has non-constant Jacobian 2γ; laundering γ into a constant requires the monomial conjugation to act on a third variable (C = γx needs an x that is itself a coordinate of the source). There is no room in two variables.
- *The escape divisor.* The mechanism's non-properness lives over the Jelonek hypersurface {c₃ = 0} (codim 1 in C³). In dim 2 a Keller map's Jelonek set would be a plane curve; nothing in the paper's machinery produces the required étale non-proper structure with constant Jacobian in two variables — and Pinchuk's map (cited §2) shows only the *real, nonconstant-Jacobian* analogue in dim 2.
- *Degree obstruction from the plane theory.* The plane structure theory (Moh; GGHV, E1) forces any 2-dim counterexample to have max degree ≥ 125 or degree pair (72,108) with rigid Newton-polygon shape — while Gao's mechanism produces low-degree components from small curve data. Any dim-2 analogue would have to thread the Newton-polygon/approximate-root constraints that the dim-3 construction simply never meets (its components are not subject to the two-variable Abhyankar–Moh machinery).
- *The paper's own verdict* is the disclaimer quoted above: dim 2 "remains open and is untouched by the counterexamples discussed here."

What *is* potentially transferable technology (assessment, not a paper claim): (a) the discipline of hunting for **non-properness/escape-to-infinity** rather than ramification — any JC2 counterexample must also be étale non-proper with escape over a Jelonek curve, which is exactly the "boundary/valuation at infinity" structure the (8,28) system and the Phase-4 chart analysis already encode; (b) the **tangency-polynomial** pattern — one univariate resolvent whose derivative is the sweep multiplier — as a model for how a putative plane counterexample's fiber structure would organize; (c) the exact-arithmetic + graph-ideal Gröbner certification methodology (Appendix A) matches Track F's gate philosophy (G3 fiber counts).

## E5. 1708.09367 v1 vs v2 — retracted gcd theorem

**Verdict: VERIFIED** (every sub-claim; silent-retraction picture confirmed by diff)

**v1 (30 Aug 2017)** — title: "THE JACOBIAN CONJECTURE: DISCARDING INFINITE FAMILIES USING INTERSECTION NUMBERS" (same four authors as GGHV 2204.14178). Abstract (lines 12–15):

> "We translate the important result of Yansong Xu into the language of [4]. We apply this result to the lists of [7] and are able to discard all hypothetical counterexamples (P, Q) with gcd(deg(P ), deg(Q)) < 36 except for two isolated cases. This result increases the lower bound for gcd(deg(P ), deg(Q)) from 16 (see [8] or [4]) to 25."

- **gcd ≥ 25 theorem**: §4 "Intersection numbers of the families with gcd(deg(P ), deg(Q)) < 36" (line 844); Theorem 4.1 (line 850, tables of Im and IM for "the 20 families listed in [7]" — 17 families of chain length 1, 3 of length 2); **Corollary 4.2 (line 1185): "B ≥ 25."** where B := min gcd(v₁,₁(P), v₁,₁(Q)) over counterexamples (∞ if JC true) — intro lines 44–47.
- **Discarded infinite families**: Theorem 4.1's per-family discards (Im and IM computed per family; "Since IM ≠ Im for all j ∈ N0, this family is discarded" — repeated per family) plus §5's Theorem 5.2 (line 1272) for "the additional 15 families listed in section 6 of [7]" (F25–F39; note families F28/F29 have corner A0 = (8,28) and F34 has A0 = (9,27)). §5's title (line 1193): "**Increasing the bound of Moh from 100 to 125**"; intro (lines 50–52): "This also proves that for a counterexample (P, Q) necessarily max(deg(P ), deg(Q)) ≥ 125, thus increasing the bound of 100 attained by Moh in [11]."
- **The "36" claim**: intro lines 40–50: "we can discard nearly all families with gcd(deg(P ), deg(Q)) < 36, and are left with only two possible cases, with (deg(P ), deg(Q)) = (75, 125) and (deg(P ), deg(Q)) = (64, 224) respectively… Moreover, if one manages to discard the two cases, one would obtain B ≥ 36." Remark 4.3 (lines 1186–1191): the two cases "remain open" — the systems' "complexity … surpasses the capacity of the software we had to our disposal". (Note gcd(75,125) = 25, gcd(64,224) = 32 — the two exceptions below 36.)

**v2 (14 Aug 2018)** — **retitled**: "THE JACOBIAN CONJECTURE: APPROXIMATE ROOTS AND INTERSECTION NUMBERS". **Inequality-only abstract** (lines 6–9):

> "We translate the results of Yansong Xu into the language of [5], obtaining nearly the same formulas for the intersection number of Jacobian pairs, but with an inequality instead of an equality."

Intro (lines 38–43): "In a recent paper [14] Yangsong Xu gives two formulas for the intersection number … which we call IM and Im. **If the formulas were true**, we would be able to discard many infinite families … When we translated the result and the proofs of [14] into the language of [5], we obtained the same formula for IM, but **for Im we obtained only an inequality, consequently we cannot discard the infinite families as desired**." The surviving results are Theorem 3.15 (IM = I(P,Q)) and **Theorem 3.25: "Im ≤ I(P, Q)"** — an inequality, which destroys the discard mechanism (v1 discarded a family exactly when IM ≠ Im, requiring both *equalities*).

**Absent theorems, confirmed by diff**: v2 (1078 lines / 10203 words) vs v1 (1593 / 15757); only 62 identical lines shared (essentially boilerplate/addresses) — a near-total rewrite. v2 contains **zero** occurrences of "B ≥ 25", "≥ 36", or "125"; its only two occurrences of "discard" are the intro sentences saying they **cannot** discard. v1's §§4–5 (Theorem 4.1, Corollary 4.2, Remark 4.3, Theorem 5.2) have no counterpart in v2; v2's table of contents ends at §3.3.

**No erratum**: v2 contains no occurrence of "erratum", "withdraw", "retract", "correction", "previous version", or "first version" (case-insensitive grep). The retraction of v1's Corollary 4.2 (B ≥ 25), of the 35 family discards, and of the max ≥ 125 bound is entirely **silent** — signaled only by the retitle and the weakened abstract. Anyone citing 1708.09367v1's bounds without checking v2 is relying on withdrawn mathematics.

**Operative consequences (unchanged from handoff):** (i) never use the gcd ≥ 25 / conditional ≥ 36 filter; (ii) the 100→125 bound claim of 2017-v1 is dead — the operative published bound chain is Moh 100 → GGHV 2204.14178's 108 with only (72,108) open below 125 (E1); (iii) (75,125) — gcd 25 — was one of v1's two undiscardable exceptions and remains a legitimate above-125 frontier case (Track D).

## E6. 1708.07936 §6 — admissible pairs 125 < max ≤ 150

**Verdict: VERIFIED** (verbatim tables extracted; handoff's "smallest admissible pairs" list confirmed, with one shape-level addendum)

Source: "SOME ALGORITHMS RELATED TO THE JACOBIAN CONJECTURE" (same four authors), §6 "Possible counterexamples with max(deg (P ), deg (Q)) ≤ 150" (lines 1467–1560). Framing quote: "Here we describe the shape of the 34 possible counterexamples with max(deg(P ), deg(Q)) ≤ 150. We only list the cases satisfying equality (3.17). The other cases (satisfying (3.18)) can be obtained by swapping m with n." (13 family members + 9 length-1 chains + 11 length-2 chains + 1 length-3 chain = 34. Count checks.)

**Verbatim rows with max ≥ 125** (boundary note: GGHV's Theorem 2.1 leaves max ≥ 125 admissible, so max = 125 itself is included). Degree pairs in the last column are **computed** by me as (m·(a+b), n·(a+b)) for A0 = (a,b) — the paper prints only max{deg(P),deg(Q)}; family A0's are from §5's tables (F2: A0 = (5,20); F7, F8: (6,15); F9: (7,21); F11: (7,21); F24: (8,24)).

From the family table (paper prints: Family, (m,n), max{deg(P),deg(Q)}):

| Family | (m,n) | max (verbatim) | degree pair (computed) |
|---|---|---|---|
| F2 | (3,5) | 125 | (75, 125) |
| F7 | (2,7) | 147 | (42, 147) |
| F8 | (3,7) | 147 | (63, 147) |
| F9 | (3,5) | 140 | (84, 140) |
| F11 | (2,5) | 140 | (56, 140) |
| F24 | (3,4) | 128 | (96, 128) |

From the length-1 chain table (paper prints: A0, A1, (m,n), max):

| A0 | A1 | (m,n) | max (verbatim) | degree pair (computed) |
|---|---|---|---|---|
| (7,35) | (19/7,5) | (2,3) | 126 | (84, 126) |
| (7,42) | (13/7,6) | (3,2) | 147 | (147, 98) |
| (7,42) | (13/7,6) | (2,3) | 147 | (98, 147) |
| (8,28) | (7/4,3) | (3,4) | 144 | (108, 144) |
| (9,36) | (17/9,4) | (3,2) | 135 | (135, 90) |
| (9,36) | (17/9,4) | (2,3) | 135 | (90, 135) |
| (11,33) | (19/4,8) | (2,3) | 132 | (88, 132) |
| (12,33) | (11/3,8) | (2,3) | 135 | (90, 135) |

(The 9th length-1 row, (8,28)/(11/4,7)/(3,2)/max 108, is the open (108,72) case — below 125, listed here only for completeness of the table's provenance.)

From the length-2 chain table, rows with max ≥ 125:

| A0 | A1 | A2 | (m,n) | max (verbatim) | degree pair (computed) |
|---|---|---|---|---|---|
| (8,40) | (8,28) | (11/4,7) | (3,2) | 144 | (144, 96) |
| (9,36) | (9,24) | (11/3,8) | (2,3) | 135 | (90, 135) |
| (10,40) | (16/5,6) | (23/10,3) | (3,2) | 150 | (150, 100) |
| (10,40) | (18/5,8) | (8/5,3) | (3,2) | 150 | (150, 100) |
| (12,30) | (16/3,10) | (11/6,3) | (3,2) | 126 | (126, 84) |
| (12,36) | (12,33) | (11/3,8) | (2,3) | 144 | (96, 144) |
| (12,36) | (9,24) | (11/3,8) | (2,3) | 144 | (96, 144) |
| (12,36) | (21/4,9) | (19/4,8) | (2,3) | 144 | (96, 144) |
| (12,36) | (21/4,9) | (12/4,5) | (2,3) | 144 | (96, 144) |

(Excluded from this table, max < 125: (8,32)/(8,28)/(11/4,7)/(3,2)/120 — killed by GGHV §3 — and (9,27)/(9,24)/(11/3,8)/(2,3)/108 — the closed (72,108) shape.)

Length-3 chain (the paper's single entry):

| A0 | A1 | A2 | A3 | (m,n) | max (verbatim) | degree pair (computed) |
|---|---|---|---|---|---|---|
| (12,36) | (12,30) | (16/3,10) | (11/6,3) | (3,2) | 144 | (144, 96) |

**Distinct degree pairs with 125 ≤ max ≤ 150, sorted by max** (each row also represents its m↔n mirror): (75,125); (84,126) and (126,84) [two different shapes]; (96,128); (88,132); (90,135) [4 shapes: (9,36)·(3,2), (9,36)·(2,3), (12,33)·(2,3), (9,36)-chain²·(2,3)]; (84,140); (56,140); (108,144); (96,144) and (144,96) [6 shapes total at max 144]; (42,147); (63,147); (98,147)/(147,98); (100,150) [2 shapes].

**Cross-check vs handoff list** ("smallest admissible pairs (75,125), (84,126), (96,128), (88,132), (90,135)"): **CONFIRMED** — these are exactly the pairs with the five smallest maxes 125, 126, 128, 132, 135. Addendum: at max 126 there is a *second* shape with reversed degree order, (126,84) (chain (12,30)·(3,2)) — anyone enumerating "all shapes with max ≤ 135" must include it, and the four distinct shapes at (90,135).

Caveats: (i) this list is the 2017 state — GGHV 2204.14178 (2022) then killed everything below 125 except (72,108) but did **not** prune anything at or above 125; no later pruning of the ≥125 list exists in the sources held here (see E8 for the web check); (ii) the list's completeness rests on the paper's algorithm (Algorithms 8/9 + PLLC restrictions); F22-style discards (Prop 6.1) show the same paper occasionally removes its own entries; (iii) v11(A0) ≤ 35 bounds §5's family generation — §6's "all pairs with max ≤ 150" claim is the operative completeness statement.

## E7. Borisov 1901.04073 — Second Framework (435,290); D=23 ramification; Belyi polynomials; Questions 6.1/6.7

**Verdict: VERIFIED** (all four sub-claims, including the negative one)

Source: A. Borisov, "FRAMEWORKS FOR TWO-DIMENSIONAL KELLER MAPS", arXiv:1901.04073v2 [math.AG], 4 Aug 2019. Second Framework = §4 (line 816).

**(a) Second Framework degree pair (435,290): VERIFIED.** Lines 1015–1025:

> "Recon-
> structing the curves numbered 2, 10, and 1 on Figure 21, we get the
> following orders of poles: (165,110), (270,180), and, finally, (435, 290).
> So with the suitable choice of coordinates on the source and the target
> planes, our map ϕ should be given by a pair of polynomials of degrees
> (435, 290)."

**(b) D=23 ramification data: VERIFIED, exactly as in the handoff.** "Belyi map of (-2)-curves, the Second Framework" (lines 1055–1066):

> "The degree of the map is 23. The map is ramified above three points.
> They correspond to the branches that end with the 0-curve with the
> self-intersection (-2), with the 0-curve with the self-intersection (-1),
> and with the forked (-5)-curve. We will identify them as {0}, {1}, and
> {∞} respectively. On the (-2)-curve on Z we will identify with {∞}
> the unique point that is sent to {∞}, so that the Belyi map is given by
> a polynomial. Then above {0} we have one point of order 1, 4 points of
> order 3, and 2 points of order 5. Above {1} we have one point of order
> 7 and 16 points of order 1."

Checks: above {0}: 1·1 + 4·3 + 2·5 = 23 ✓; above {1}: 1·7 + 16·1 = 23 ✓; unique preimage of ∞ (polynomial Belyi map) ✓. (The companion (-5)-curve Belyi map of the Second Framework has degree 28: above {0} 14×2, above {∞} 9×3 + 1×1, above {1} 1×23 + 5×1 — lines 1028–1037.)

**(c) Explicit Belyi polynomials for the Second Framework (-2)-curve map: NOT PUBLISHED — handoff's "NO" confirmed** (verification by exhaustive absence). For the degree-23 Second-Framework map the paper gives only the ramification data and a dessin d'enfant ("A corresponding dessin d'enfant (unique as a graph, but not as a dessin) is the following" — Fig. 28); same for the degree-28 map (Fig. 27, "not unique, there are some options"). A scan of every "given by"/"Maple"/"explicit" occurrence in the paper finds explicit Belyi formulas ONLY for: (i) First Framework (-5)-curves, degree 16: w ↦ p²(w)/(w·r³(w)) with p, r written out in full over Q(√−3) (lines 587–608, "thanks to Maple"); (ii) First Framework (-2)-curves, degree 13: t ↦ (1/3¹⁵)·t(35t⁴−182t³+390t²−455t+455)³ (lines 636–638); (iii) the k=6 isotope's degree-13 map t ↦ t¹³+1 (line 1147); (iv) the Three-dessin Framework's degree-5 map t ↦ (1/108)x³(x−5)² (line 1239). Nothing for either Second Framework Belyi map. Any Track wanting to realize the Second Framework must first CONSTRUCT the degree-23 (and degree-28) Belyi polynomials from the dessins.

**(d) Questions 6.1 and 6.7: VERIFIED, verbatim** (§6, lines 1467–1499):

> "Question 6.1. Is there a simple reason why in the First Framework
> there is no map ϕ? If so, it would be really helpful, as it might help pre-
> screen any further framework examples, before embarking on tedious
> and time-consuming computer calculations."

> "Question 6.7. (The biggest question of all). Can one actually use
> our frameworks to contruct a Keller map? If you have some time and
> knowledge in computing, I am very open to collaboration, and will be
> glad to share with you many further details beyond the discussion at
> the end of section 3." ["contruct" sic]

**Campaign-relevant bonus findings (context, beyond the assigned claims):**

1. *First Framework is (probably) dead, without a proof.* Lines 688–694: "my own calculations, using Maple, based on the ideas below, led to the same result: no map. So, in all likelihood, there is no map ϕ that satisfies our framework, but we currently do not have a simple reason for this." — and Borisov's honesty caveat (lines 800–806, paraphrasing exactly): after reducing hundreds of linear equations to "just a dozen or so coefficients" he concluded no map exists, but "one careless mistake anywhere in the process would likely lead to a missed solution, and I cannot trust my own bookkeeping abilities to claim that I actually have a proof that no ϕ exists." The First Framework closure is therefore NOT certified even by its author.
2. *The Session-7 near-miss pair is Borisov's.* Lines 807–815 print exactly the pair Track F must reject: y1 = x1³x2⁸·p((1/x2)(x1x2³−1)³), y2 = x1²x2⁵·(x1x2³−1)·r((1/x2)(x1x2³−1)³) with p, r from the degree-16 Belyi map; "It has a rather simple Jacobian, a constant multiple of x1⁴x2¹²" [hence NOT Keller]; "generically 16:1"; not proper; "Unfortunately, there does not seem to be a way to modify it to get a Keller map."
3. *The First Framework's degree pair is (99,66)* (lines 664–676: y1 of separate degrees 27/72, total 99; y2 separate 18/48, total 66) — Moh's last troublesome case (Remark 3.1), i.e. Track C's (99,66) specialization has this as its source. The isotope family (k ∈ {2,…,6}, lines 1137–1155) generalizes it: y1 degrees 9k+9 (in x1) and 27k+18 (in x2), y2 degrees 6k+6 and 18k+12; k=2 recovers (99,66).
4. *The Three-dessin Framework's hypothetical Keller map has degree pair (108, 72)* (line 1241: "it is not hard to figure out the pair of degrees of the possible Keller map: (108, 72)") — **the same degree pair as GGHV's open (8,28) case**. Two independent approaches (GGHV Newton-polygon elimination; Borisov Picard-graph frameworks) converge on (108,72) as the live small case. Its three Belyi maps: the degree-16 and degree-13 maps of the First Framework plus an explicit degree-5 map (given, line 1239).
5. *Moh (99,66) history* (lines 679–689): Moh's published proof for (99,66) is "sketchy"; Xu's 2016 patch attempt "had a mistake, that he acknowledged (cf. [7])" (per Valqui — consistent with E5's v2 story); "Rodrigo Horruitiner essentially proved it in his Master's thesis."

## E8. Web sweep 2024–2026

**Verdict: COMPLETE — no premise-changing news for the plane case; one new relevant paper found (Valqui–Ramírez 2025, does not touch (8,28)).**

Sweep performed 2026-08-13 (UTC), via arXiv API listing (40 most recent "Jacobian conjecture" papers), arXiv abs pages, Semantic Scholar citations, and general web search.

**(a) The July 2026 dimension-3 refutation wave (context the handoff already had, now independently confirmed):**
- JC refuted in **dimension 3** by Levent Alpöge, announced July 19, 2026 on X; found using Anthropic's Claude Fable 5 model (per phys.org, The Conversation, ScienceDaily coverage); verified rapidly by the community — "the brevity of the counterexample made it easy for other mathematicians to verify"; Gallagher published exact symbolic verification scripts (jacobianfun.org, curated by Gallagher, updated 2026-07-22).
- A. Gallagher: infinite family, every geometric degree ≥ 3 in dim 3 (July 20, Zenodo doi:10.5281/zenodo.21479195). D. E. Speyer: tangent-sweep explanation (July 23). T. Tao: expository "digestion" (July 21). S. Gao: arXiv:2608.00222 (July 31) — every dimension n > 2 (see E4).
- **Every credible source states dim 2 remains open.** jacobianfun.org verbatim: "These three-variable constructions do not settle the separate two-variable case."

**(b) Status of (72,108) and GGHV 2204.14178:**
- arXiv:2204.14178 is still **v1 (29 Apr 2022)** — no v2, no erratum, no journal reference on the abs page. The (72,108) gap announced there is unmodified at the source.
- No 2024–2026 paper closing (72,108), raising 108→125, or otherwise pruning the below-125 or ≥125 admissible lists was found (targeted searches + 40-paper recent arXiv listing).
- Semantic Scholar's citation list for 2204.14178 surfaced only T. Nguyen, "Some classes satisfying the 2-dimensional Jacobian conjecture and a proof of the complex conjecture until degree 104" (arXiv:1902.05923, v5 Mar 2025, published Quaestiones Mathematicae 48(2), 2025) — a *weaker* bound (104 < 108), fully consistent with GGHV; no conflict, no premise change.
- arXiv:1708.09367 confirmed at **two versions exactly** (v1 2017-08-30, v2 2018-08-14), no erratum, no journal ref — E5's silent-retraction picture holds at the arXiv-metadata level too.

**(c) GGHV authors' later output:** Valqui's most recent Jacobian item is **C. Valqui & V. Ramírez, "The Groebner basis and solution set of a polynomial system related to the Jacobian conjecture", arXiv:2506.05697 (6 Jun 2025)** — downloaded and read (now in scratch as arxiv_2506.05697.pdf/.txt). It studies the *Laurent-series (C-series) system* of GGHV's arXiv:1406.0886 formulation (JC2 false ⟺ ∃ C = x + C₋₁x⁻¹ + … with Cⁿ = P etc.), computes a Gröbner basis for the truncated system in the special case n = 3, νᵢ = 0 (i>0), D = C[y], F₁₋ₙ = y, and parametrizes its solution set (Prop 3.6: ≤ 2·s·(m+2) solutions, explicit). **It is NOT the (8,28) coefficient system and says nothing about (72,108)** — different attack line entirely (truncated solutions exist; obstructions live at higher order, which the paper does not reach). Signal: the group is still active on JC2 as of June 2025; no degree-bound progress published since 2022.

**(d) Claimed proofs / counterexamples in dim 2 (credibility check):**
- Yucai Su, "Generalizations of local bijectivity of Keller maps and a proof of 2-dimensional Jacobian conjecture", arXiv:1603.01867, **v43** (11 May 2024), 43 versions since 2016, two withdrawn versions, never published, not accepted by the community. Not evidence in either direction for the campaign.
- Lee–Li, "On the two-dimensional Jacobian conjecture: Magnus' formula revisited, IV" (arXiv:2408.01279, Aug 2024) — approach development (Newton polygon / Magnus expansion), no closure claim.
- Moskowicz, "There are no Keller maps having prime degree field extensions" (arXiv:2407.13795, Jul 2024) — unrefereed; even if correct it does not close (72,108) (the geometric degree of the hypothetical map is not forced prime).
- No claimed *counterexample* in dimension two found anywhere 2024–2026.
- Follow-on wave applying the dim-3 counterexample elsewhere (none touching JC2): weak Markus–Yamabe fails in dim ≥ 14 (2608.05392); Hessian conjecture false n ≥ 5 (2607.22198); characteristic-2 separable JC counterexamples (2608.02634, 2607.20968); Gaussian Moments Conjecture counterexamples (2607.18186); Jelonek on generic Jacobian-one mappings (2607.20597); Shaska graded Keller maps (2607.20210 — in the graded setting dim 2 admits no counterexample signature); real-JC degree bounds (2605.12302: real plane JC holds through degree 6, sharp; 2608.12294: real JC degree 7 special case).

Sources: [arXiv 2204.14178 abs](https://arxiv.org/abs/2204.14178), [arXiv 1708.09367 abs](https://arxiv.org/abs/1708.09367), [arXiv API recent "Jacobian conjecture" listing](http://export.arxiv.org/api/query?search_query=all:%22Jacobian+conjecture%22&start=0&max_results=40&sortBy=submittedDate&sortOrder=descending), [arXiv 2506.05697](https://arxiv.org/abs/2506.05697), [arXiv 2608.00222](https://arxiv.org/abs/2608.00222), [arXiv 1902.05923](https://arxiv.org/abs/1902.05923), [arXiv 1603.01867](https://arxiv.org/abs/1603.01867), [jacobianfun.org explainer](https://jacobianfun.org/jacobian-explained), [Semantic Scholar citations of 2204.14178](https://api.semanticscholar.org/graph/v1/paper/arXiv:2204.14178/citations), [The Conversation coverage](https://theconversation.com/hello-there-the-jacobian-conjecture-is-false-thanx-why-a-tiny-social-media-post-has-mathematicians-rethinking-ai-283883), [phys.org coverage](https://phys.org/news/2026-07-tiny-social-media-mathematicians-rethinking.html), [ScienceDaily coverage](https://www.sciencedaily.com/releases/2026/08/260804034634.htm), [Tao's digestion post](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/) (403 to our fetcher; content corroborated via search snippets and Gao's citations), [Secret Blogging Seminar post](https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/) (403; same).

---

## BOTTOM LINE

**PREMISES STAND.** Specifically:

1. The plane (dimension-2) Jacobian conjecture is **open** as of 2026-08-13. The July 2026 refutations live strictly in dimension ≥ 3 and their authors say so explicitly (E4, E8).
2. GGHV 2204.14178's Theorem 2.1 is the operative bound: any JC2 counterexample has max degree ≥ 125 or degree pair (72,108)/(108,72); of the two (72,108) shapes, "(9,27)" is closed and **"(8,28)" is exactly the shape left open** ("we couldn't solve the corresponding system of polynomial equations, thus it is left open") — unchanged on arXiv since April 2022, no erratum, no superseding work found (E1–E3, E8).
3. The 2017 gcd ≥ 25 theorem, its conditional "≥ 36" strengthening, and 2017-v1's claimed 125 bound are **silently retracted** in 1708.09367v2 (inequality-only) and must not be used; (75,125) and (64,224) were the two exceptions and remain legitimate frontier cases (E5).
4. The above-125 admissible list of 1708.07936 §6 stands as extracted (E6); smallest maxes: 125, 126 (two shapes), 128, 132, 135 (four shapes). No later pruning found.
5. Borisov's frameworks paper checks out on all four handoff claims; bonus corroborations: the Session-7 near-miss pair is Borisov's own (his Jacobian is const·x1⁴x2¹², non-Keller), the First Framework's "no map" conclusion is explicitly uncertified by its author, and Borisov's Three-dessin Framework independently lands on degree pair **(108,72)** — the same pair GGHV leave open (E7).
6. **Premise changed (context only, already known to the handoff):** the ambient conjecture is dead in every dimension ≥ 3 (July 2026), which raises the stakes on dim 2 and supplies a proven mechanism (étale non-properness, escape to infinity) that any JC2 counterexample must also exhibit — but no new mathematics closing or opening the dim-2 attack surface has appeared.
7. New minor item the handoff lacked: Valqui–Ramírez arXiv:2506.05697 (June 2025) — Gröbner analysis of the truncated C-series system; unrelated to (8,28); no impact (E8c).
