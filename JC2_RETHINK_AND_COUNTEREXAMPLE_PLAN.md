# JC2 — rethink and counterexample plan

September 5, 2026. No counterexample has been constructed.

**Continuation:** [Astra 13](ASTRA_13_SHIFTED_CHART_CONSTRUCTION.md) executes the
chart check and part of this plan. It retains a previously unremoved fractional
shift, widens the rational first row to a nonzero-mu family, and records exact
coupled construction attempts. Read that report before applying the older
direct-chart row restrictions below to the full case.

**Recommendation:** continue the corrected degree-(108,144) construction, but first apply the additional-root obstruction below. Under the recorded standard-pair hypotheses, it excludes twelve of Astra 11's seventeen marked leading solutions. The five remaining marked solutions are the rational one already studied and four conjugate solutions with two triple roots. Work on the four conjugates together, enforce compatibility at both triple roots, and continue the rational branch with its previously invisible p9 row retained.

This is a strategy review with new written deductions and exact supporting calculations. It is not an independent verification of all historical proofs or a solution of the remaining coefficient system.

## 1. What I reviewed

I read the complete supplied [campaign record](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/JC2_COMPLETE_RECORD.md), including its September 5 continuation through Astra 12. I followed the correction ledger, continuation inventory, Astra 4's audit, Astra 9's full obstruction and proof audit, Astra 11's full report and saved leading certificate, Astra 12's full report, verifier and next-exactness exploration, and the localization/conductor proof. I consulted the primary corner papers for the new argument below.

The complete-record file fetched in this review has Git blob `4607d1ccea86f9d97cd13741df4f4b7d061a9ea8`. The branch name contains September 4, but its report covers work through September 5.

The archive inventories 44 branches, 1,289 catalogued commits including two recovered local commits, and 581 distinct report versions at its earlier cutoff. I did not independently read and re-prove every archived report or rerun every experiment. The synthesis supplies the campaign-wide history; the sources listed above supply the focused mathematical review.

## 2. What the campaign actually accomplished

| Workstream | Durable contribution | Consequence for the next construction |
|---|---|---|
| Early low-height and cusp cascades | Explicit Wronskian, divisibility, residue and kernel calculations | Use their scoped obstructions; do not extrapolate to arbitrary leading coefficients. |
| Borisov frameworks and Belyi reconstruction | Explicit leading data, Laurent charts and repaired pole-order obstructions | A rational solution or a monomial-Jacobian near-miss is insufficient for polynomial-plane realization. |
| B=16 and territory compiler | Substantial exact and modular infrastructure, with consequential transcription/support corrections | Reopen only a precisely identified corrected input. Historical range claims are inconsistent. |
| Proposition 4.3 quadrilateral | Astra 2's leading completeness and characteristic-zero contradiction certificate | Retire this specified polygon unless a concrete proof defect is found. |
| Proposition 4.3 pentagon | Astra 3's complete graded prefix and projective good-reduction argument | Retire this specified polygon. Affine modular emptiness alone was never sufficient. |
| Collision-first height searches | Finite jets and exact monic height-(2,3)/(4,6) exclusions | Extra degree cannot rescue an all-degree excluded class. |
| Prescribed collision subalgebra | Astra 9's arbitrary-degree parity/infinity-residue obstruction | The degree-15 resonance and all higher degrees in this algebra are dead. |
| Mate and period programme | Explicit mateless families and corrected rational-versus-polynomial distinction | Generic exactness, denominator clearing and polynomialization are separate gates. |
| Elliptic/hyperelliptic primitive constructions | Exact curve identities, plus integral-closure and faithful-realization obstructions | Exact primitives do not supply plane Keller coordinates by themselves. |
| Target monodromy/source boundary searches | Scoped cover and boundary constraints; a repaired fixed-sheet marking issue | Abstract survivors require realization. Astra 4 closes the retained H3 class even with the stated marking relaxation. |
| Corrected degree-(108,144) case | Astra 11 restores lost support and classifies 17 marked leading solutions | This is an actual untreated part of an explicit construction problem. |
| Rational leading solution | Astra 12 proves p11=0 and a one-parameter p10 under its terminal-chart assumptions | Lower rows, both parameter branches and finite termination remain unresolved. |

These conclusions follow the [complete record](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/JC2_COMPLETE_RECORD.md) and its linked corrections. A notable historical lesson is that the campaign repeatedly solved systems stronger than the actual counterexample requirements: omitted support, discarded kernels, imposed symmetries or special collision algebras made the problem smaller without proving that every desired example lay inside it.

The principal failure mode has been reaching an intermediate object and mistaking its compatibility for progress toward finite realization. Astra 5's all-order nonterminating control is an especially clear example. Conversely, the meaningful positive asset in Astra 11 is a faithfully specified finite construction problem whose missing rows have finally been restored.

## 3. New deduction: twelve marked leading solutions fail an additional-root test

### Data and scope

Work over C and assume a standard (3,4)-pair with the recorded first corner `(8,28)`, lower endpoint `(1,0)` and normal `(4,-1)`. Its leading root is

\[
S=Xh(XY^4),\qquad \ell(P)=S^3,\qquad \ell(Q)=S^4.
\]

Astra 11 classifies the normalized solutions

\[
h(T)=(T-1)^3B(T),\qquad B(0)B(1)\ne0.
\]

Its five coefficient-field factors have degrees 1,2,4,4,6 and root multiplicity patterns for h of `(3,1,1,1,1)`, `(3,4)`, `(3,2,2)`, `(3,3,1)`, `(3,2,1,1)`, respectively. These multiplicities were checked again over the exact coefficient fields in this review.

### Published facts used

The argument uses the root-shift criterion in Proposition 5.18, the termination of type-III corner changes in Proposition 5.19, and the regular-corner power/divisibility constraints in Theorem 7.6 of [Guccione–Guccione–Valqui, On the shape of possible counterexamples](https://arxiv.org/html/1401.1784v3). Proposition 5.13 describes the two noncommuting terminal types. These are statements for the indicated (m,n)-pairs, not just for a selected coefficient slice.

### Application to every eligible root

Let a nonzero root of h have multiplicity nu. In the fractional ring with `l=4`, use `z=X^(1/4)Y` and choose a fourth root lambda of that root. Its multiplicity in the leading P is `3 nu`. The root-shift threshold is

\[
3\nu\ge 3\frac{4\cdot8-28}{4-1}=4.
\]

Thus **every root of multiplicity nu>=2 qualifies**, not just the marked triple root. The resulting next corner is

\[
A_\nu=(1+\nu/4,\nu)=((4+\nu)/4,\nu).
\]

All five root patterns have multiplicities with gcd one. Therefore S is not a nontrivial power in the fractional Laurent polynomial ring: its nonzero linear factors already prohibit that. The upper leading P has maximal power exponent exactly 3, so the corresponding normalized exponent d is 1.

The corner divisibility constraints now prevent an intervening lower type-II corner: its denominator would have to divide d=1 while not dividing its own power exponent. They also prohibit additional lower regular corners. If a type-III change is necessary, its repeated removal preserves the upper leading form and stays in the same `l=4` ring. Consequently the corner A_nu must admit a noncommuting terminal form in that ring.

This is the crucial point: the argument does not assume that a chosen root is already terminal in the first simple shifted chart. It allows the required type-III changes. It also does not import an exclusion from the separate ratio-(2,3) problem.

### Terminal arithmetic

Write `a=4+nu`, `b=nu`, `l=4`. For a terminal type-I.a corner, the common normalized lower endpoint is `(j/4,0)` for a positive integer j. Equality of the leading weights and the constant-bracket weight forces

\[
j=\frac{lb-a}{(3+4)b-1}=\frac{3\nu-4}{7\nu-1}.
\]

For terminal type-I.b, the two lower endpoints are `(k/4,0)` and `(1-k/4,1)` with positive integer k. The two assignments force

\[
k=\frac{3(3\nu-4)}{7\nu-1}
\quad\text{or}\quad
k=\frac{4(3\nu-4)}{7\nu-1}.
\]

These formulae can also be obtained directly by applying the face weight to both endpoints and using `v(P)+v(Q)=rho+sigma`.

| nu | Next corner | Type-I.a j | Type-I.b k alternatives | Result |
|---:|---|---|---|---|
| 2 | (3/2,2) | 2/13 | 6/13, 8/13 | No integer terminal endpoint |
| 3 | (7/4,3) | 1/4 | 3/4, 1 | The known k=1 assignment survives |
| 4 | (2,4) | 8/27 | 8/9, 32/27 | No integer terminal endpoint |

Therefore an additional double or quadruple root cannot occur in a full standard pair with these data. The quadratic factor contributes two excluded marked solutions, the first quartic contributes four, and the sextic contributes six: **twelve in total**.

This is a new written deduction in this review, supported by exact factor and arithmetic checks. It has not received independent peer review or proof-assistant verification. Its scope is precisely this leading classification and the stated standard-pair hypotheses. It neither proves JC2 nor solves the remaining full systems.

## 4. What remains and why branch order changes

For each leading solution the auxiliary curve in the differential method is the smooth projective normalization of

\[
w^4=c(y),\qquad c(y)=y^3(y+1)B(y+1).
\]

Its degree is eight. Riemann–Hurwitz gives

\[
2g-2=-8+\sum_{c(\alpha)=0}(4-\gcd(4,\operatorname{ord}_\alpha c)),
\]

with zero ramification contribution at infinity. The simple root at -1 ensures that the cover is connected.

| Field-factor degree | Root multiplicities of h | Auxiliary genus | Status after the argument above |
|---:|---|---:|---|
| 1 | 3,1,1,1,1 | 6 | Retain rational branch |
| 2 | 3,4 | 0 | Exclude by the quadruple root |
| 4 | 3,2,2 | 2 | Exclude by either double root |
| 4 | 3,3,1 | 3 | Retain all four conjugate marked branches |
| 6 | 3,2,1,1 | 4 | Exclude by the double root |

At first the genus-zero factor looked like the obvious construction target. I explicitly rationalized it: for `b=(-6±sqrt(-3))/8`,

\[
c(y)=y^3(y+1)(y-b)^4,
\quad y=\frac1{z^4-1},
\quad w=\frac{z(1+b-bz^4)}{(z^4-1)^2}.
\]

The curve identity holds exactly, and its leading differential has a rational primitive. The additional-root obstruction nevertheless excludes its plane extension. This is a useful example of why auxiliary tractability must be checked against the full geometric requirements before committing to it.

The four remaining algebraic marked solutions are more interesting than their coefficient complexity suggests. Their auxiliary curves have genus three, compared with genus six for the rational branch. **These are genera of the auxiliary leading curves, not of the generic fibres of a hypothetical P.** No rational-fibre theorem is being applied to them.

Write their coefficient parameter as A, with

\[
3A^4+60A^3+394A^2+620A+475=0.
\]

Then

\[
h(T)=(T-1)^3(T-r)^3(T-s),
\]

where exact squarefree factorization gives

\[
r=\frac{3A^3+135A^2-851A+905}{6160},\qquad s=-A-3r.
\]

Marking the other triple root replaces A by

\[
\sigma(A)=-\frac{9A^3+195A^2+1507A+3905}{280}.
\]

Modulo the quartic, I checked `sigma(sigma(A))=A`, that sigma(A) obeys the same quartic, and that it has no fixed point. Thus the four marked leading solutions pair under re-marking. This observation can prevent duplicate work; it does not reduce the full solution scheme to two irreducible components.

The important construction requirement is simultaneous compatibility at both triple roots. The two local charts describe one global polynomial pair. Their allowable shifts, endpoint parameters, free kernels and transition map must agree.

**A chart caution:** before imposing a second copy of Astra 12's simple row bounds, derive the full shift sequence at that root. An additional fractional type-III shift cannot silently be set to zero. The root-exclusion proof above permits these shifts; a coefficient compiler must preserve them as well. The earlier support-loss error is a reason to settle this explicitly.

## 5. A specific blind spot in the rational-branch differential test

Keep Astra 12's stated chart and terminal hypotheses. Put `c=y^3(1+y^5)`, `w^4=c`, and `s=P^(1/12)`. After p11=0, define

\[
a_j=\frac{p_{12-j}}{w^{12-j}},\qquad x=(s/w)L(s^{-1}).
\]

An independent implicit inversion gives

\[
\begin{aligned}
x^3=\frac{s^3}{w^3}\bigg[1
&-\frac{a_2}{4}s^{-2}-\frac{a_3}{4}s^{-3}
+\frac{11a_2^2-24a_4}{96}s^{-4}\\
&+\frac{5a_2a_3-6a_5}{24}s^{-5}
+\frac{-7a_2^3+24a_2a_4+12a_3^2-32a_6}{128}s^{-6}
+O(s^{-7})\bigg].
\end{aligned}
\]

In particular the first p9 term is

\[
[s^0]x^3=-\frac{p_9}{4c^3}.
\]

Astra 12's forcing identity is

\[
\left.\partial_yQ\right|_P=\frac{\kappa}{36s^{11}}\partial_s(x^3).
\]

Differentiation with respect to s annihilates this entire first p9 contribution. That explains why a sequence of successful early differential tests need not decide p9. It is not a freely disposable coefficient.

The subsequent visible coefficients include

\[
[s^{-2}]x^3=\frac{5p_{10}p_9-6c^3p_7}{24w^{22}},
\]

\[
[s^{-3}]x^3=
\frac{-7p_{10}^3+24c^3p_{10}p_8+12c^3p_9^2-32c^6p_6}{128w^{33}}.
\]

These give specific coupled differential tests. If p10=0, the first displayed test no longer sees p9; the next one still sees p9 squared together with p6. Both the zero and nonzero p10 branches must be kept. This is a diagnostic and a direction for the next calculation, not an exclusion or a terminating construction.

I reran Astra 12's verifier against its saved certificate. All seven groups passed, including the nonzero-parameter survivor control. The new inverse coefficients above were derived separately by truncated implicit inversion.

## 6. Concrete execution plan

### First: establish the full charts of the five retained marked solutions

Use the published standard-pair definitions and the exact corner argument to enumerate the required root shifts, including possible type-III changes. Prove which simple charts are complete and retain parameters for any additional shifts. Keep the original rectangle bounds and the precise reverse-polynomiality map. Do this once, before a new coefficient solve.

Deliverable: a derivation of the exact finite supports and chart transition maps for the rational branch and the quartic coefficient field. This step may confirm the current chart or expose a further support correction; neither outcome should be pre-decided.

### Second: solve the double-triple-root compatibility problem

Work over the one quartic coefficient field, carrying all embeddings. Construct the complete spaces of allowed rational primitives on the genus-three auxiliary curve. Derive their allowed poles from the source support and chart bounds rather than guessing a numerator degree.

Impose the original bracket rows, global exactness, original-plane descent and the second triple-root chart together. Carry every integration constant until it is either constrained or removed by a demonstrated polynomial automorphism. Explicitly compare the two terminal data sets under re-marking.

The first substantive milestone is a complete description of the compatible upper rows and all remaining parameters. A single incompatible residue or pole order can rule out a whole coefficient-field branch. A survivor must be kept with its complete equations, not replaced by a convenient sparse representative.

### Third: continue the rational branch through the p9 coupling

Within the verified chart, retain

\[
p_{11}=0,\qquad
p_{10}=\tau y^8(1+y^5)^2(3+5y^2+8y^5).
\]

Treat tau=0 and tau!=0 separately, normalizing the latter only using the recorded allowed scaling. Solve p9, p8, p7 and p6 jointly with the new forcing coefficients. The existing p8 control only cancels one numerator; it cannot justify choosing every free p8 parameter to be zero in the full system.

Deliverable: a complete parameterization or an exact contradiction for this coupled block, including exceptional coefficient strata. A timeout remains undecided.

### Fourth: make the upper and lower constraints meet

Do not extend the upper cascade indefinitely without enforcing the other end. Write in original coordinates

\[
P=\sum_iX^iA_i(Y),\qquad Q=\sum_iX^iB_i(Y).
\]

The restriction of the Keller identity to X=0 is already

\[
A_1B_0'-A_0'B_1=\kappa.
\]

In particular `gcd(A0',B0')=1` is necessary. Higher X coefficients give further finite equations. These constrain the lower/negative Laurent rows that an upper-only treatment barely touches.

Combine the bottom equations, all remaining upper equations and original descent in a finite compatibility system. Use symbolic linear elimination where justified, preserving all kernels and splitting any branch on which a divided coefficient vanishes. A large undifferentiated Gröbner computation is not the first step.

### Fifth: reconstruct and verify an actual pair

Every retained solution must produce finite original polynomials. Expand their Jacobian directly in C[X,Y] and verify that it is a nonzero constant. Prove noninvertibility independently, preferably by an exact collision of two distinct points, or by a rigorously computed function-field degree greater than one.

An auxiliary primitive, a fractional-chart constant bracket, a finite jet, or a solution of only the necessary prefix does not satisfy this milestone.

### If these five leading branches fail

Close only this degree-(108,144) case. The next support-based task is to resolve the actual `(9,27)` provenance/Corollary 5.7 issue and identify corrected B=16 cells with valid inputs. Re-enter either only after its target has been derived. A different geometric construction would need a new realizability mechanism; increasing the depth of the already-closed H3 class or changing the degree in Astra 9's algebra cannot help.

## 7. What this plan deliberately learns from the old failures

The full collision subalgebra forced the identification of an entire curve, not merely one pair of points. Its parity condition forced a forbidden infinity edge. Its all-degree closure therefore says that this particular way of encoding a collision is too restrictive, not that all direct collision constructions fail.

The direct two-point coefficient searches already exist in the archive; rebranding them would not create a new idea. Their eventual reuse should come with a newly derived support or a new global constraint. Similarly, primitive-first geometry should only return with a faithful plane-realization mechanism and an early integrality check.

The strongest next mathematical question is now precise: **can the two triple-root terminal descriptions and the global differential conditions be realized by one finite polynomial pair, with every missing row retained?** The companion question on the rational branch is whether the p9 couplings and the lower boundary equations force a contradiction or permit actual termination.

These are opportunities to make the construction problem materially smaller. They are not evidence that a counterexample is likely to exist in it.

## 8. Verification and limitations

Performed in this review:

- Read the complete campaign synthesis and the focused source/proof files identified above.
- Replayed Astra 12's seven exact verification groups against its saved certificate.
- Recomputed the four nonrational factors' squarefree multiplicities over their exact number fields.
- Calculated the auxiliary genera, including the unramified infinity contribution.
- Checked the genus-zero parametrization and a rational leading primitive, before rejecting its plane extension by the corner argument.
- Checked the terminal fractions for multiplicities two, three and four exactly.
- Checked the surviving quartic branch's root re-marking, its involution identity and absence of fixed points.
- Derived the inverse expansion through drop six independently.

Not performed:

- A fresh audit of all 1,289 historical commits or all earlier geometry arguments.
- A full new support compiler, including every possible additional fractional shift.
- A solution of the five retained full coefficient systems, or a proof that they are irreducible.
- Construction of P,Q, a collision, or a JC2 counterexample.
- A repository push or modification of the historical record.

The additional-root exclusion is a written mathematical argument. Exact computations verify its input multiplicities and arithmetic; they do not formalize the application of every published geometric theorem. The plan keeps that distinction explicit.

Primary and campaign references:

- [Complete campaign record](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/JC2_COMPLETE_RECORD.md).
- [Astra 4: missed routes and corrected target marking](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/ASTRA_4_MISSED_ROUTES.md).
- [Astra 9: full collision obstruction](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/astra9/FULL_COLLISION_OBSTRUCTION.md).
- [Astra 11: leading classification and support repair](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/ASTRA_11_CORRECTED_DEGREE144.md).
- [Astra 12: global differential descent](https://github.com/git-df-scott/jacobian_planar/blob/astra/jc2-complete-record-2026-09-04/ASTRA_12_GLOBAL_DIFFERENTIAL_DESCENT.md).
- [On the shape of possible counterexamples](https://arxiv.org/html/1401.1784v3).
- [Some algorithms related to the Jacobian Conjecture, Section 6](https://arxiv.org/html/1708.07936v1#S6), documenting the separate `(8,28)->(7/4,3)` ratio-(3,4) chain.
