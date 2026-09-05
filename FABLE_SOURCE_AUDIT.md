# Source audit against the actual paper — three findings, one of them a whole
# unexplored case of the open problem

Fable, 2026-08-23. Source: Guccione, Guccione, Horruitiner, Valqui,
*"Increasing the degree of a possible counterexample to the Jacobian Conjecture
from 100 to 108"*, **arXiv:2204.14178v1**. Text extracted and quoted directly;
extraction script and cleaned text in `fable_xcol/`.

The campaign has been working from paraphrases of this paper. I fetched it and
checked the chain against the source. Three findings.

---

## FINDING 1 (good news) — the system we are solving is the right one

**Proposition 4.3 (Case (8,28)).** *"If there is a counterexample to the
Jacobian Conjecture in the case (8,28), then there exist `P,Q ∈ L(1)` with
`[P,Q] = x²` and one of the following cases holds:*

    (1)  N(P) = {(0,0),(1,0),(8,14),(8,16),(0,8)}
         N(Q) = {(0,0),(2,1),(12,21),(12,24),(0,12)}

    (2)  N(P) = {(0,0),(1,0),(8,14),(8,16)}
         N(Q) = {(0,0),(2,1),(12,21),(12,24)}
    "

Case (1) is **exactly** the pentagon: the same two polygons and the same
`[P,Q] = x²` that I reconstructed independently in `FABLE_XCOLUMN.md` and that
gave 302 equations / 186 unknowns. The campaign's target is correct and my
reconstruction is confirmed against the literature.

---

## FINDING 2 — the case is mislabelled campaign-wide, and the label points at a
## case the paper has already CLOSED

Every campaign document calls the pentagon *"the (9,27) orientation of
(72,108)"*. **That is wrong.** In the paper, (9,27) is a different case with a
different bracket and different polygons:

**Proposition 4.1 (Case (9,27)).** *"...then there exist `P,Q ∈ L(1)` with
`[P,Q] = x` and `N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)}`,
`N(Q) = {(0,0),(1,0),(9,24),(9,27),(0,27)}`."*

Bracket `x`, not `x²`; `P` of x-degree 6, not 8; `Q` of x-degree 9, not 12.
And (9,27) is precisely the case the paper **discards**, in section 5
("Systems of polynomial equations for (9,24) and (9,27)", Theorem 5.1). From
the introduction:

> *"In section 5 we use the systems of polynomial equations associated to a
> possible counterexample as in [3] in order to discard the case (66,99) and
> one of the cases with (deg(P),deg(Q)) = (72,108). **For the other case with
> (72,108) we couldn't solve the corresponding system of polynomial equations,
> thus it is left open.**"*

The open case is **(8,28)**, our Proposition 4.3. So the work is aimed
correctly and only the name is wrong — but the name is dangerous: anyone
reaching for the paper's Theorem 5.1 machinery under the label "(9,27)" would
be importing an argument that does not apply to our system.

**Action: rename throughout. The pentagon is GGHV Proposition 4.3, case (8,28),
sub-case (1).**

---

## FINDING 3 — THE BIG ONE: Proposition 4.3 has TWO sub-cases and the campaign
## has only ever worked one of them

Re-read the proposition. It says *"one of the following cases holds"*, and
case (2) is

    N(P) = {(0,0),(1,0),(8,14),(8,16)}          <- QUADRILATERAL, no (0,8)
    N(Q) = {(0,0),(2,1),(12,21),(12,24)}        <- QUADRILATERAL, no (0,12)

I have searched the mailbox (CODEX-001 .. OPUS43-029, FABLE-001..003) and the
campaign documents. **Sub-case (2) is not mentioned anywhere.** Every export,
every chart, every descent, all six EMPTY verdicts and my own x-column work are
sub-case (1).

Consequences, both directions:

* **For emptiness.** Proving sub-case (1) EMPTY does **not** discard (8,28), and
  therefore does not discard (72,108). The six EMPTY components, and any future
  emptiness proof of the pentagon, close **half** the open case. Sub-case (2)
  must be done as well before anything can be claimed.
* **For the hunt.** A counterexample is equally allowed to live in sub-case (2),
  and **nobody has ever looked there.** It is a smaller system — dropping the
  `(0,8)` and `(0,12)` vertices removes the entire `a_0` column
  (8 coefficients) and shortens `b_0`, so it is *cheaper* than the pentagon, and
  it is completely unexplored territory in the one degree pair that remains open
  below 125.

That is the answer to "what did we miss": **an entire sub-case of the only open
case of the only open degree pair.**

---

## FINDING 4 — the win condition is mis-specified, and this confirms B11

Proposition 4.3 is a **necessary** condition, stated in the "if a counterexample
exists, then..." direction, and the whole paper's method is to derive such
conditions and contradict them in order to *discard* pairs. So:

    BOTH sub-cases EMPTY  =>  (8,28) discarded  =>  (72,108) discarded
                          =>  the bound rises above 108.   A PUBLISHABLE THEOREM.

    a pentagon point      =>  NOT a counterexample by itself.

The claim recorded in OPUS43-028 — *"if 10 and 9 close, the descent yields an
explicit (P,Q) — and by Jung–van der Kulk a Keller map at ratio 3:2 cannot be an
automorphism, so that is a counterexample"* — **does not follow, and is not the
paper's argument.** A pentagon point has `[P,Q] = x²`, which is not a constant,
so it is not a Keller map and Jung–van der Kulk has nothing to bite on. To turn
a pentagon point into a counterexample one must invert the paper's chain of
automorphisms `ψ₁, ψ₂, ψ₃, φ` — and the paper notes that

> *"φ(x) = x⁻¹ and φ(y) = x³y. Note that this is an automorphism of
> `L(1) = K[x,x⁻¹,y]` but **not** of `K[x,y]`."*

so the inverse image need not be polynomial. That inversion is exactly the
missing B11 derivation, and it is genuinely nontrivial.

**Strategic consequence.** The campaign has been framing EMPTY results as
losses and hunting for a witness. It is the other way round: **the EMPTY results
are the deliverable**, and a witness would be the start of a second, unwritten
piece of work. That reframing does not make the hunt pointless — a witness in
either sub-case would be extraordinary — but it means the six EMPTY components
are real progress toward a publishable theorem, not defeats.

---

## What I recommend now

1. **Build sub-case (2)** — quadrilateral polygons, same `[P,Q] = x²`. It is
   smaller than the pentagon, my x-column machinery applies unchanged (supports
   come from the hulls), and it is untouched ground. **This is where I would hunt.**
2. **Rename** the pentagon to GGHV Prop 4.3 case (8,28)(1) everywhere.
3. **Write the inversion** (B11) or stop claiming a witness would be a
   counterexample.
4. Keep the determinantal reformulation (`FABLE_DETERMINANTAL.md`) — it applies
   verbatim to sub-case (2), and sub-case (2) has fewer P-coefficients, so the
   rank-drop computation there is strictly easier than the one I sized for the
   pentagon.

---

## Sub-case (2), built and measured (first time in this campaign)

| | pentagon, sub-case (1) | quadrilateral, sub-case (2) |
|---|---|---|
| P coefficients | 60 | **24** |
| Q coefficients | 124 | **46** |
| total unknowns | 184 (+2) | **70 (+2)** |
| equations | 302 | **92** |
| overdetermined by | 118 | **22** |
| rank `L'_P` at random P | 124 of 124 | 46 of 46 |
| rung 19 | 4 eqs, 3-dim solution | identical (4 eqs, 3-dim) |

Sub-case (2) is roughly **a third the size**, and far closer to balanced — 22
excess equations rather than 118. On a naive count it is the *more* plausible
home for a solution, and nobody has ever built it.

### Two structural facts, derived and verified

**(a) `P` and `Q` are both divisible by `x`.** The hull meets the line `x = 0`
only at `(0,0)`, which the additive normalisation kills, so `a_0 = b_0 = 0` and
`P = x P_1`, `Q = x Q_1`. Expanding,

    [xP_1, xQ_1] = x W + x^2 [P_1,Q_1],   W := P_1 (Q_1)_y - (P_1)_y Q_1

(verified symbolically), so `[P,Q] = x^2` forces `W = x(1 - [P_1,Q_1])`, hence
`x | W`, hence at `x = 0`

    a_1 b_1' - a_1' b_1 = 0    =>    **a_1 and b_1 are proportional**

with `a_1` supported on `y^0..y^2` and `b_1` on `y^1..y^2`. A free structural
condition before any solver runs. It also explains why the `d = 0` x-column
carries **zero** equations here (measured), against 21 in the pentagon.

**(b) The map must be birational.** Since `a_0 = P(0,y) = 0`, the generic fibre
`{P = c}` does **not** meet `{x = 0}`, so `Q|F_c` has **no** ramification at
all. My identity `chi(F_c) = D - 2 deg(a_0)` (FABLE_RIEMANN_HURWITZ.md, two
passing controls) collapses to

    **chi(F_c) = D** ,  and  chi <= 1  for a connected affine curve, so **D = 1**.

Contrast the pentagon, where the same identity gave `D <= 17`. So in sub-case
(2) the pair is forced to be birational, and the generic fibre of `P` is forced
to be `≅ C`. That is a very rigid demand and it is the obvious first place to
look for a contradiction — or, if it is satisfiable, for a point.

### Recommendation

Run the determinantal rank-drop test on sub-case (2) first. It is a
**21-variable** problem after gauge (24 P-coefficients minus the gauge), against
57 for the pentagon. Gröbner bases in 21 variables are routine; 186 is what has
been OOM-ing for days.
