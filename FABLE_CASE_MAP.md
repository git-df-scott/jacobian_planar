# The complete case map, and two corrections to my own earlier claims

Fable, 2026-08-23. Source: arXiv:2204.14178v1, section 2 table + Theorem 2.1,
extracted verbatim (`fable_xcol/ggh_paper_text.txt`).

Asked whether I was sure nothing else was missed, I went back to the paper's own
table instead of any summary. Here is the complete landscape, and two errors of
mine that the exercise caught.

## Theorem 2.1 (verbatim)

> *"If (P,Q) is a counterexample to the Jacobian Conjecture, then we have either
> max{deg(P),deg(Q)} >= 125, or (deg(P),deg(Q)) in {(72,108),(108,72)}."*

## The ten cases, and their disposition

| `A_0` | `(m,n)` | max deg | discarded by | replicated here? |
|---|---|---|---|---|
| (4,12) | (3,4) | 64 | [4 §3.5], [10], [7] | no |
| (4,12) | (5,7) | 112 | [4 §3.5] | no |
| (5,20) | (2,3) | 75 | [3 §5] | no |
| (5,20) | (3,2) | 75 | [3 §5] | no |
| (7,21) | (2,3) | 84 | this paper §3 (via [6 Thm 7.3]); second proof §6 | no |
| (8,24) | (2,3) | 96 | [5 Prop 6.1] | no |
| **(8,28)** | **(3,2)** | **108** | **NOTHING — LEFT OPEN** | **our target** |
| (8,32) | (3,2) | 120 | this paper §3 (via [2 Rmk 3.31, Prop 3.29]) | no |
| (9,24) | (2,3) | 99 | this paper §5, Theorem 5.1 | attempted, NO VERDICT |
| (9,27) | (2,3) | 108 | this paper §5, **Corollary 5.7** | attempted, NO VERDICT |

So the landscape is exactly:

* **Below 125:** one open case, **(8,28)**, with **two sub-cases** (Prop 4.3).
  Sub-case (1) is the pentagon. Sub-case (2) is the quadrilateral, which nobody
  had built before today (`FABLE_SOURCE_AUDIT.md`).
* **At or above 125:** entirely open — Theorem 2.1 says nothing there. This is
  the 804-pair territory whose enumeration artifacts (Sessions 19–38) are lost.
* **Everything else below 125** is closed only by literature this campaign has
  never replicated.

**That is the whole map. There is no third sub-case of (8,28) and no eleventh
case below 125.** Within the paper's framework the enumeration is now complete.

## CORRECTION 1 — I repeated a false claim about Corollary 5.7

`FABLE_SWEEP_REPORT.md` item B9 says *"GGHV Cor 5.7 is refuted (line-by-line),
so (9,27) is live in the literature."* **That is wrong, and it is my error.** I
took it from a summary rather than the primary document. The primary source,
`session43/COR57_TEST.md`, says the opposite:

> *"`VERDICT: NO VERDICT` on Cor 5.7's independent test. It remains the single
> highest-value unverified exclusion in the campaign."*

and `EXCLUSION_AUDIT_SUMMARY.md` records *"statement and proof architecture
verified, but Cor 5.7 rests on an imported Corollary 7.2 from GGV 2017 that
nobody re-checked."* So Corollary 5.7 is **unreplicated, not refuted**, and
(9,27) is **closed in the literature**, not live.

This matters in both directions: (9,27) is not a second open case to hunt in,
and the campaign has not overturned anything in the literature. It is also
exactly the failure mode this campaign keeps logging — trusting a summary over
the primary source — and I committed it myself within hours of writing it up as
someone else's problem.

For the record, the paper's Corollary 5.7 reads:

> *"There exist no P,Q in K[x,y] with [P,Q] = x and
> N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)}, N(Q) = {(0,0),(1,0),(9,24),(9,27),(0,27)}"*

and its proof reduces to Theorem 5.1 by an automorphism `tau(x) = x + lambda`.
The campaign's "sliver" / `p108` systems are exactly these polygons.

## CORRECTION 2 — my VARPRO search result was a scaling artifact

I reported the variable-projection search reaching `||L_P Q - x^2|| = 2.6e-02`
over 300 starts, down from 0.719. **That improvement is not real.** Inspecting
the best point:

    Q vertices  ~ 3e-07   (all three)
    ||Q||       ~ 1e-02
    max |Q_k| for x-degree k >= 3  ~ 3e-04

The system is bihomogeneous apart from the single normalisation
`p_{0,1} q_{1,2} = 1` (`FABLE_DETERMINANTAL.md`), so `(lambda P, mu Q)` with
`lambda mu = 1` is a symmetry, and the optimiser exploited it by sending
`P -> large`, `Q -> 0`. My reciprocal barrier slowed that but did not stop it.
The point is a collapse onto the degenerate families, not an approach to a
solution. **The correct fix is to normalise scale explicitly** (fix
`q_24_12 = 1` and optimise the rest) rather than to penalise it. Until that is
rerun, the only honest numerical statement remains the 12-start result
(`residual ~ 0.72`), and even that is a search outcome, not evidence.

## What I still cannot certify

I am not able to say "nothing else was missed" and mean it. What I can say
precisely:

1. **Within the paper's enumeration, the map above is complete** — I read the
   table and Theorem 2.1 directly.
2. **The literature closures are unreplicated.** Nine of the ten cases rest on
   [2],[3],[4],[5],[6],[7],[10] plus this paper's §3, §5, §6. This campaign has
   re-derived none of them, and has already found one genuine misprint in GGV
   (1.2) row 3, which invalidated a batch of its own verdicts. If any closure is
   wrong, a case reopens.
3. **Above 125 is untouched and the enumeration artifacts are lost.**
4. **My own two errors above were caught only by going to primary sources.** The
   rate at which that keeps finding things is the honest measure of how much
   confidence to place in any summary here, including mine.
