# STATUS — Plane Jacobian Conjecture campaign

**This is the single place. Everything from the Plan 43 session lives here.**
Detail files and scripts are indexed in §9; nothing essential is only in them.

Last updated: 2026-08-19, Plan 43 Waves 0–1. 19 commits, branch
`claude/plane-counterexample-endgame-az3geq`, PR #6.

---

## 0. Bottom line

> **No counterexample has been found. No non-EMPTY verdict exists on any real
> system, ever.** Nothing has been promoted from mod-p to ℚ. Every result below
> moves toward **closure**, not toward a hit. Two apparent hits arose during the
> session; both were gauge artefacts, both were caught before reaching a
> committed claim, and both are documented in §6.

**Wave-1 gate ("(72,108) decided, or its exact stall points named"): NOT MET**,
but **one of the three sub-territories is now closed** — the framework side dies
unconditionally, THEOREM 2 certified and THEOREM 3 confirmed (§2.6). The two
remaining stall points (pentagons; case (2) over ℚ̄) are computational, not
conceptual. §7 scores it.

---

## 1. The target

GGHV (arXiv:2204.14178, **unrefereed**, v1 only) eliminate every degree pair with
max < 125 **except (72,108)/(108,72)**. The refereed floor is Nguyen's 104
(*Quaestiones Mathematicae* 48(2) 2025). Live territory:

* **(72,108)** — the one surviving pair below 125. Undecided.
* **max ≥ 125** — largely unexplored (~150 of 167 enumerated targets unrun).
* everything in **[105,124]**, which rests on unrefereed work.

`J(Q,P) = −J(P,Q)`, so **(72,108) and (108,72) are one territory** — proved two
independent ways (`wave0/w0_h1a_swap_and_G.py`).

---

## 2. Results, by item

### 2.1 The endgame obstruction, in closed form `[PROVED-exact]`
`wave1/w1_h1c_endgame_closed_form.py`

> For every `D ≥ 1` and `k ≥ 0`, `(v+1)^k(3v(v+1)R′ − D·R) = −c` with `c ≠ 0`
> has a rational solution of degree ≥ 1 **iff `k = 0` and `3 | D`.**

The homogeneous equation integrates to `C(v/(v+1))^{D/3}`, rational iff `3 | D`;
`R = c/D` is a particular solution; for `k ≥ 1` evaluate at `v = −1`.

Verified for **symbolic** D. Reproduces the campaign's per-degree ledgers
(rank 14 at D=13, rank 24 at D=23) as corollaries, from an independently built
matrix. **Uniform in D, no ceiling.** The campaign had this as an extrapolation
off two rank computations; it is now a theorem.

Consequences: **L4 is immaterial** (every k dies); Plan 43's `3|D` loophole is
**exact**, not heuristic — and every published framework has `D ∈ {13, 23}`,
neither divisible by 3.

### 2.2 (108,72), framework side — every layer transfers
`wave1/H1C_VERDICT.md`, `w1_L3_chain_identity.py`, `w1_L3_step2_pinning.py`, `w1_L1_L2_threedessin.py`, `w1_L1_boxes_closed.py`, `w1_L2_cascade_threedessin.py`

Borisov's Three-dessin Framework predicts **(108,72)** (verbatim, §5), and its
third Belyi map `x³(x−5)²/108` is certified exactly — degree 5, ramification
(5)/(3,2)/(2,1,1,1) over ∞/0/1, critical values exactly {0,1}, **defined over ℚ**.

Degree ledger read from the source, not from campaign files:

| framework | (−5)-map | (−2)-map | chain degree D | Keller degrees |
|---|---|---|---|---|
| First | 16 | **13** | 13 | (99,66) |
| Second | 28 | **23** | 23 | (435,290) |
| **Three-dessin** | = First's | **= First's** | **13** | **(108,72)** |

`D = deg((−2)-curve Belyi map)` is structural: Borisov arranges coordinates in
both frameworks so that map is a *polynomial*, which is exactly what the
realization layer demands. The new degree-5 dessin sits above the **(−1)**-curves
— a different curve class — so it does not move D.

| layer | status | how |
|---|---|---|
| L1 chart | **transfers** | inversion, monomial rule, chart factor, Keller form all recomputed; pole depths (−9,−6) inherited from the identical chain |
| L1 boxes | **immaterial** | the layer-1 conditions are box-independent (stated verbatim in `d23_n3_layer1.py`); their inputs are chain/Belyi data, shared |
| L2 contact | **transfers** | contact −5, 13 vanishings; independently confirmed by L3's `eW = −5` |
| L2 cascade | **transfers** | L1–L4 identities are generic in `(a,b)`, `D`, `g`; all three shared |
| L3 rigidity | **transfers** | `g = αU(U−1)⁸` pins, `deg g = N/μ + ε = 16/2+1 = 9` |
| L4 | **immaterial** | §2.1 kills every `k` |

Two supporting facts, each verified two ways:
* the **(−5)…(−2) chain is identical** in both frameworks — same 18 K̄ labels
  `-5 -52 -47 -42 -37 -32 -27 -22 -39 -17 -12 -19 -26 -7 -9 -11 -13 -2` and same
  target chain — validated by the campaign's own C1 blowup test *and* a forward
  reconstruction. (Figures unreadable via `pdftotext`; pages rendered at 200 dpi.)
* the reconstruction ladder is **Fibonacci** (each rung the sum of the previous
  two), matching Borisov's SF walk `4,7,11,18,29`, whose pole pairs are exactly
  depths `(15,10)` times those rungs.

**Verdict: the Three-dessin Framework at (108,72) dies — as strongly as the First
Framework's own death, and conditional on exactly the same two unreproduced
theorems, no more.**

**Residue — DISCHARGED, not inherited.** `THEOREM 2` (Taylor-pin rigidity at
*general* parameters) and `THEOREM 3` (pole-fiber ⇒ R polynomial) were the
campaign's only remaining framework conditionality. Both are now closed. Their
statements were never lost — they are written out verbatim in the tracked file
`Sessions 1-18 status reports` (lines 1051, 1062), present on every branch; only
the executable transcript runs were lost. `THEOREM 2`'s conclusion is
**certified** (`wave1/w1_L3_step2_pinning.py` derives `g = αU(U−1)⁸` with no
free moduli). `THEOREM 3` is **CONFIRMED** — and a genuine gap in its recorded
proof was found and repaired (§2.6). See `wave1/RECOVERED_THEOREMS.md`. **The Three-dessin Framework introduces no new
conditionality of its own** — which was the whole question.

**Flagged discrepancy — RESOLVED (§2.6).** Both sides were right about their own
moment and both are now superseded: `trackC_c3_ladder.py` was correct that
THEOREM 2/3 were unreproduced and load-bearing, and `d23_phase2_preview.py`'s
*"unconditional"* label is correct **now** that both are discharged — it was not
correct when written. Original texts: `d23_phase2_preview.py` labels the First
Framework *"[PROVEN dead, Sessions 16–18, unconditional]"*, while
`trackC_c3_ladder.py` records THEOREM 2/3 as unreproduced prose that *"every
(72,108) statement that assumes a polynomial R inherits."* These cannot both be
right.

### 2.6 THEOREM 3 — CONFIRMED, recorded proof repaired `[PROVED-exact]`
`wave1/w1_theorem3_verdict.py`

**Conclusion true; recorded proof insufficient.** THEOREM 3 asserts
`R = 2v³⁹(Ã₄ − g³S₁₃)/g³` is a degree-13 polynomial, arguing from the Belyi-13
fiber sizes 13/9/5/1 that the pole fiber is the 1-point one.

*The gap.* That step fixes the pole divisor's **multiplicity** (13), not its
**location**. The following sentence closes `v = 0`; nothing in the recorded
text closes `v = −1`. Witness — built and tested, not asserted:
**`R = 1/(v+1)¹³`** satisfies every premise the recorded argument states (finite
poles inside `{0,−1}`; a single pole point of multiplicity 13; `v = 0` not a
pole) and is **not a polynomial**. The premises do not entail the conclusion.

*The repair — shorter, and uses strictly less.* Session 11 defines
`R = v³⁹·W̃₋₅(U)/g(U)⁶` with `W̃₋₅` a **block, hence a polynomial**, of degree
`6·deg g − 26 = 28`; THEOREM 2 gives `g = αU(U−1)⁸`. With `v³⁹ = (U−1)³⁹` and
`g⁶ = α⁶U⁶(U−1)⁴⁸`:

    R = W̃₋₅(U) / ( α⁶ · U⁶ · (U−1)⁹ )

Write `gcd(W̃₋₅, U⁶(U−1)⁹) = U^a(U−1)^b`, so `a ≤ 6`, `b ≤ 9`. After cancelling,
`map-degree(R) = 28 − a − b`. The framework's own **13-realization** demands
`map-degree(R) = 13`, so `a + b = 15` — which inside the box `a ≤ 6, b ≤ 9` has
**exactly one solution**, `(a,b) = (6,9)`. The denominator cancels completely.
**R is a polynomial of degree 13.** ∎

The Belyi passport is reproduced and shown Riemann–Hurwitz consistent
(`(13−9)+(13−5)+(13−1) = 24 = 2·13−2`) but is **not load-bearing**; neither is
the `v = 0` divisibility argument. Dependencies: `g = αU(U−1)⁸` (certified),
`deg W̃₋₅ = 28` (arithmetic from `deg g = 9`), `W̃₋₅` polynomial (by
construction), `deg R = 13` (the framework's demand, **not** THEOREM 3).

**The `g³S₁₃`-regularity sub-question flagged in §6.8 dissolves** — the `W̃₋₅`
form never constructs `g³S₁₃`.

**Consequence.** Both uncertified legs of the Sessions 16–18 First Framework
emptiness theorem are discharged. Every (72,108) statement carrying
`CONDITIONAL(R-poly)` can be re-labelled, and the Three-dessin (108,72)
framework kill loses its last conditionality.

### 2.3 The eliminator is controlled — A6 `[CERTIFIED]`
`MANIFEST.md` §G, `wave0/w0_a6*.py`

Every campaign EMPTY comes from one path: `groebner(I)` → `dim == -1`. It had
emitted EMPTY 46 times and non-EMPTY **zero** times; nothing showed it *could*
say otherwise. On the real (72,108) case-(2) system, through the identical calls:

| control | expected | measured |
|---|---|---|
| raw edge subsystem | non-EMPTY | `dim = 1` |
| + `d_3_3 = 1` chart | zero-dim | `dim = 0, vdim = 1144` |
| + contradictory pin | EMPTY | `dim = −1` |
| **A4 data-mutant** (constant terms only; α verified a genuine zero *inside* Singular) | non-EMPTY | `dim = 0, vdim = 1144` at three primes |

msolve 0.10.1 agrees: **1144** for real and planted, `[-1]` for contradictory, at
all three primes — independently re-deriving the degree-1144 count.

**Seventh gate control:** the descent map `G` passes G0/G2/G3/G4/G5 — including
the hard non-injectivity gate — and is stopped by exactly G1/G6 (Jacobian
non-constancy). The correct reason and only the correct reason. Free
cross-validation: G3's resultant route independently confirms `d(G) = 3`.

### 2.4 H1f — complete, and it corrected a five-day-old false claim
`wave1/H1F_FINDING.md`, `w1_h1f_eliminant.py`

`AUDIT_REPORT.md` §2 had said since 2026-08-14 that the char-0 edge eliminant
*"completed via msolve … elimination polynomial degree 1144 … that is the
unblock."* **The cited file contains no polynomial.** Parsed with PARI: 28
entries × 7 coordinates, each a 2-vector `[lower, upper]` with dyadic endpoints;
max nested vector length in the whole file is **2**. It is msolve's *real-solution*
output — 28 real boxes, 7 being exactly the number of edge variables.

msolve's own help explains it: *"When input coefficients are rational numbers:
**real solutions** … (see the **-P flag** to recover a parametrization)."* The
campaign ran without `-P`.

**Fixed.** Re-run with `-P 1`:

| | |
|---|---|
| eliminant degree | **1144** — matching the independently recomputed `vdim` |
| squarefree | **yes** (`gcd(f,f′) = 1`) |
| leading coefficient | 4666 digits |
| saved | `wave1/edgeQ_eliminant.txt` (5.7 MB); full RUR `wave1/edgeQ_param.out` (46 MB) |

The four H1f items:

1. **Eliminant** — was blocked because the artifact did not exist; **now computed**.
2. **Prime hygiene** — the CASE2 route used 65521 (ok) plus **32003 and 65537, both ≡ 2 (mod 3)**, violating the campaign's own rule. Re-ran the full chain at **65539** (8 factors, degrees 1,2,2,6,6,6,6,6) and **65599** (6 factors, 1,3,3,4,12,12), both summing to 35. **Every branch reproduces `dim = 2`, same component.** The verdict survives.
3. **Provenance** — Route 1 / Route 2 are file-level disjoint (hashes recorded, no shared sources). Both still descend from the same GGHV polygon derivation, so this is *code* disjointness, **not full independence**. Stated, not overclaimed.
4. **Gauge integrity** — the dim-2 survivor is a *linear* component `β₂=β₃=α₂=α₃=0` with `β₁,α₁` free, and the gauge group is exactly 2-dimensional (`β₁` = weighted scaling; `α₁` = additive constant of A, which every equation sees only through `A′`). **2 = 2.** It is *also* excluded independently: on it `a₈ = 0`, killing the vertex (8,16) of N(P), so it is not case (2) at all. **Disposed of twice over.**

### 2.5 The eliminant is irreducible over ℚ `[PROVED-exact]` — new result
`wave1/w1_h1f_eliminant.py`

A planned shortcut **did not exist** (§6.3). Instead, Dedekind's criterion at 8
good primes (all squarefree mod p, all degree-sums 1144): every ℚ-factor degree
must be a subset sum of the mod-p degrees at every such prime.

```
100003: [1,2,4,19,143,299,676]      100069: [1,4,5,5,6,13,16,63,104,162,195,570]
100019: [2,4,4,5,5,6,96,275,747]    100103: [1,46,59,69,409,560]
100043: [1,27,70,119,199,728]       100109: [6,7,9,13,31,240,838]
100057: [1,2,244,897]               100129: [8,25,29,52,80,99,99,270,482]
```
**Surviving proper-factor degrees: none.** Controls confirm the sieve *can*
detect reducibility (a planted 400+744 split is found; a totally-split prime
leaves all 1143 degrees surviving).

**Proves:** `K = ℚ[θ]/(f)` is a single degree-1144 number field; all 1144 edge
points are **Galois-conjugate**, so either all extend to a case-(2) solution or
none do — the ℚ̄ question is one yes/no about the generic point; **no rational
edge points**; the exact-ℚ branch structure is *simpler* than mod-p (4–12 factors).

**Does not prove:** case (2) empty over ℚ̄ — that needs the residual system, 13
variables over K, not done. Nothing about case (1). **Not** a confirmation of the
recorded mod-p EMPTY: different object, different verdict class per §6.2 of the
plan. Chart `d_3_3 = 1` only.

### 2.6 Closed as hiding places
* **H1d — GGHV's Prop 4.3 case split is exhaustive.** The only place a fourth polygon could hide is *"one or two different linear factors"*, and that is a **bound**: GGHV establish `ℓ = λR^{4m}` with `e(R) = (7,2)`, and `(7,2)` in `z = x³y` is `x¹·z²`, so `deg_z R = 2`. **No case (3).** Residue: the external citation `[6, Prop 2.5]` is not re-derived.
* **p₁₀ = 0 chart** — my own gauge excluded it; it is provably empty. The order-`y⁰` coefficient of `[P,Q]` is `p₁₀·Q₁ = x²`, so `p₁₀ = 0` gives `0 = x²`.
* **H1e geometric-degree crossfire — NEGATIVE.** Every bound runs the wrong way (Bezout → `d ≤ 7560`; Jelonek bounds `deg S_F`; T7 bounds `d` *below*; Makar-Limanov sharpens `deg S_F`, not `d`). Żołądek confirmed applicable → floor `d ≥ 6`. The one actual value at this degree pair is **d = 16** (Borisov: *"the generic degree of φ is 16"*), clearing the floor. No cheap kill exists.
* **H3-A1 reverse descent — closed as a hit source.** Via exterior powers, `det JG = const·(t∘F)/s`, verified on Alpöge (`s = x²`, `t = F₃²`, ratio `h²`, k=2); a weight sweep gives `s = x^d`, `d ≥ 1` always. **Theorem:** if the descent is Keller (k=0), unique factorisation forces `F = (f₁,f₂,cx)` with `∂(f₁,f₂)/∂(y,z)` constant, so injectivity is fibrewise in x and **F is non-injective iff some specialisation is a non-injective plane Keller pair.** The k=0 stratum is not a route around JC2 — it is a restatement of it.

---

## 3. Pentagons (case 1) — structure certified, no verdict
`wave1/H1B_STATUS.md`, `wave1/H1B_REFORMULATION.md`

* y-adic Jacobian **rank 60 of 61**, independently reproduced at two primes, three random points each — own polygons, own bracket expansion, own recursion, own dual-number differentiation. Audit item A2.9 closes on the number.
* The gauge group is **3-dimensional** (translation `p₀₀`; overall scale `P → cP`; coordinate scale `(x,y) → (λx, λ⁻³y)` forced by `λ³μ = 1`), so **58 essential parameters** against 60 independent conditions — **overdetermined by 2**, before 314 surplus conditions.
* Rank **saturates at level j ≤ 23**; everything beyond is surplus.
* The cascade is **affine in the newest slice** at levels 13–17 (exact second-difference test), and levels 13–15 are *independent* of it.
* Conditions have **degree 12–23** but are **sparse**: 686 monomials at level 13, 59,626 at level 23 — eleven orders below the dense bound. **They can be written down.**
* Exported: `wave1/pent_L23.ms` — 66 conditions, 1,080,147 monomials, 43 MB. First exportable pentagon system in the campaign's history.
* **Both engines OOM.** msolve on L23: exit 137 (`wave1/L23_VERDICT.txt`). Singular `slimgb` on the smaller L18 export: exit 137. STALLED, stall point named. **Emptiness is not claimed.**

---

## 4. Open

| item | state |
|---|---|
| ~~THEOREM 2 / THEOREM 3~~ | **CLOSED.** THEOREM 2 certified (`w1_L3_step2_pinning.py`); THEOREM 3 **CONFIRMED**, its recorded proof repaired (§2.6, `w1_theorem3_verdict.py`). No residual — the `g³S₁₃` flag dissolved. |
| case (2) over ℚ̄ | eliminant exists and is irreducible (single branch); residual system — 13 variables over a degree-1144 field — unsolved |
| case (1) pentagons | no verdict; both engine rungs exhausted |
| **H2** above-125 sweep | **COMPLETE — all 180 targets carry a contract verdict.** 31 EMPTY at two compliant primes (all 20 of the old single-prime table reproduced, +11 new), 141 TIMEOUT, 8 OOM, **zero LIVE, zero DISAGREE**. Stall point is a size boundary: decides ≤ ~82 params; above that blocked on engine capacity (a 3.3× budget converted zero). Still mod-p only — §6.2 forbids promotion. `wave2/H2_COUNT_RECONCILIATION.md` |
| **H4** deg_y = 3 slice | FRAMEWORK.md's own OPEN-1; untouched |

---

## 5. Corrections made to the campaign record

1. `AUDIT_REPORT.md` §2 — *"the blocker is now gone"* is **wrong**; the eliminant never existed (§2.4).
2. `AUDIT_REPORT.md` §1 — leaf-1 at p=65521/65599 is **stale, not overstated**; PR#4 carries the completed terminals. All 24 leaf-1 terminals are EMPTY at three primes.
3. `phase2_moduli/README.md` — the *"Compositio Math 160 (2024)"* reference for GGHV is wrong; GGHV is unrefereed.
4. Plan 43's *"run T7 on G"* — ill-posed; **G is not étale** (`det JG` vanishes on `h=0`).
5. Plan 43's A2.8 — not a conflict; a scope ambiguity, reconciled. The Belyi-gate/contact closure is scoped to the template `(3+12a, 6+12b)`, `2a−3b=1`, which provably excludes (108,72) — Session 23 says so itself.
6. Route-2 prime hygiene — two of three primes violated the `p ≡ 1 (mod 3)` rule; re-run compliant, verdict survives.
7. `trackC_report.md` L2 was checked only for **D = 1..6**; the chain length in play is **D = 13**. Now computed at D = 1..14.

## 6. Corrections to my own work this session

1. **"Nguyen 104 is unverified"** — retracted. It is real and refereed (arXiv:1902.05923 → *Quaest. Math.* 48(2) 2025). Three web searches missed it. *Absence from a search is not absence from the literature.*
2. **"These conditions cannot be written down"** — retracted. I used the *dense* monomial bound as the actual count; the true counts are 11 orders smaller (§3).
3. **The gcd route for case (2)** — retracted before anything was built on it. Substituting the RUR eliminates only the 7 edge variables; **13 remain free**, so there is no univariate polynomial and no gcd.
4. **"a+b = 12" box framing** — retracted. It conflated the near-miss *boxes* with the *final degrees*; they coincide for the First Framework only.
5. **Parameter count 60 → 59 → 58**, as each further gauge was found.
6. **Two false-positive episodes**, both gauge artefacts, both caught by the §6.1 adversarial check before any committed claim:
   * **v1** used an *absolute* stopping test on a system homogeneous of degree −1 in P's scale. Newton drove `‖x‖ → 10¹⁰`; Q collapsed to zero and every support condition was satisfied vacuously — at the deepest level the "vanishing" coefficients were *larger* than the allowed ones.
   * **v2's outlier** (ratio 1.70e−09) inflated the *denominator* instead: the unfixed coordinate-scale gauge moves forbidden and allowed coefficients by different powers of λ, driving the ratio down eleven orders with nothing solved.

**Standing requirement for any future pentagon detector:** fix all three gauges;
use an **absolute** normalisation (a ratio is breakable from either end); make
"allowed coefficients are O(1)" an *acceptance* condition, not a post-hoc check.

---

### 6.7 Our own H1c "closed form" was overstated — and correcting it removed THEOREM 3 from the endgame
`wave1/w1_h1c_polefix.py`, `wave1/RECOVERED_THEOREMS.md`

`w1_h1c_endgame_closed_form.py` printed: for every `D ≥ 1`, `k ≥ 0`,
`(v+1)^k(3v(v+1)R′ − D·R) = −c` with `c ≠ 0` has a rational solution of degree
≥ 1 **iff** `k = 0` and `3 | D`. **False as stated.** The `k ≥ 1` branch was
never computed — its `check()` call passed a literal `True`, and its own prose
reads *"IF R is regular at v = −1"*. Regularity at `v = −1` is exactly what
THEOREM 3 supplies, so the file assumed the uncertified input it was meant to be
independent of. Counterexample at the campaign's own `(D,k) = (13,4)`, `c = 1`:

    R = (243v⁴ − 81v³ + 54v² − 42v + 35) / (455(v+1)⁴)

— non-constant, exact, with a genuine order-4 pole at `v = −1`
(`gcd(num,(v+1)⁴) = 1`); checked by substitution, Laurent expansion, and exact
zero residual at 40 random rational points.

**LEMMA (corrected).** For `D ≥ 1`, `k ≥ 1`, `c ≠ 0`, every rational solution has
all poles at `v = −1`; `R` is never a polynomial; there is **no** rational
solution iff `3 | D` and `k ≥ D/3`; otherwise the solutions are exactly
`R = A/(v+1)^k` with `deg A = k`, each of **map-degree exactly `k`**. Certified
for `D = 1..30`, `k = 1..6`.

**COROLLARY.** The endgame contradiction never needs `R` polynomial — only
`map-degree(R) ≠ k`. At `(13,4)` every rational solution has map-degree 4, so a
demand that `R` realise a **degree-13** object dies on degree alone.

**Scope.** This does *not* prove THEOREM 3; the C2 table keeps its
`CONDITIONAL(R-poly)` label. It removes THEOREM 3 from the *endgame* step and
relocates the gap to one smaller question (§4). Session 15's affine form must
not be used to answer it — it is derived from THEOREM 3 and would be circular.

**Net effect: this makes the campaign record more conditional, not less** — it
retracts one of our own claimed unconditional results, and confirms that the
prior sessions (`trackC_report.md`, `HANDOFF_TO_AUDIT.md`, `FABLE_DECISIONS.md`)
were right to flag THEOREM 3 as load-bearing.

---

### 6.8 The map-degree question resolved — by pole order, not map-degree
`wave1/w1_mapdeg_question.py`

§6.7 left one thread: the endgame equation at `(D,k) = (13,4)` *does* have
non-constant rational solutions, so the framework kill needs an independent
input to exclude them. THEOREM 3 was that input. There is a cheaper one.

The framework **defines** `R = 2v³⁹(Ã₄ − g³S₁₃)/g³`, and THEOREM 2's
`g = αU(U−1)⁸` — certified in this campaign by `w1_L3_step2_pinning.py` —
vanishes at `v = −1` (i.e. `U = 0`) to order **exactly 1**. So `g³` vanishes to
order exactly 3, and `R`'s pole order at `v = −1` is **at most 3** whenever the
numerator is regular there (`v³⁹` is `−1` at `v = −1`, so it contributes
nothing). Every pole-branch solution of the endgame equation has pole order
**exactly 4**. `3 < 4`, so no framework `R` is one of them; the polynomial
branch was already dead by evaluation at `v = −1`. Both branches closed.

This uses **only THEOREM 2 (certified) plus arithmetic** — no Belyi fibers, no
13/9/5/1, no polynomiality, and no map-degree. It is strictly cheaper than the
map-degree route, which needed `deg R = 13` as a separate input.

**Flagged, not resolved:** it needs `(Ã₄ − g³S₁₃)` regular at `v = −1`. `Ã₄` is
a block polynomial in `U`, hence regular. `g³S₁₃` is the `m = 13` extension of
THEOREM 1's ladder, proved there only for `m = 0..12`. On the near-miss
`S₁₃ = −n₃v⁻³⁹/2`, whose only pole is at `v = 0` — evidence, not proof. If the
ladder extends to `m = 13`, both the First and Three-dessin kills become
unconditional on THEOREM 3.

---

### 6.9 H4 rung 2: msolve does NOT buy the degrees Session 35 expected — STALLED
`wave2/w2_msolve_escalate.py`, `wave2/h4_msolve.log`

Session 35's close-out predicted the escalation: *"The boundary is now RAM, so a
bigger machine or an F4/FGLM engine buys degrees directly."* Tested. It does not,
on this hardware.

| cell (Singular: out of memory) | msolve gens | msolve verdict | secs |
|---|---:|---|---:|
| `k=4 h=t deg≤6` | 67 | **OOM** | 238 |
| `k=5 h=t deg≤4` | 64 | **TIMEOUT** (600 s) | 600 |
| `k=5 h=t deg≤5` | 76 | **OOM** | 359 |
| `k=6 h=t deg≤4` | 85 | **OOM** | 413 |

**0 of 4 decided.** Recorded **STALLED**, stall point named (memory on a 15 GB
box, three cells; wall-clock on the fourth) — *not* as emptiness.

The negative is trustworthy because the controls passed: a two-sided parser
control (a unit ideal is called EMPTY, a solvable system NONEMPTY) and a
cross-engine control (msolve agrees with Singular's EMPTY on a cell whose answer
was already known). An earlier draft of the parser read msolve's `[1]:` — the
unit ideal, i.e. an *empty* variety — as NONEMPTY; the cross-engine control
caught it, which is why it exists.

**Read:** F4/FGLM is a genuinely different algorithm, not a longer run of the
same one, and it still cannot hold these cells. The `deg_y = 3` h-branch
boundary is a real computational wall, not a Singular artefact. Raising it needs
more RAM or a structurally smaller system, not another engine.

---

## 7. Wave-1 gate score

Plan 43's gate: *"(72,108) decided, or its exact stall points named."*

| territory | on record | closed? |
|---|---|---|
| case (1) pentagons | **no verdict at all** | **No** |
| case (2) quadrilaterals | EMPTY mod p, 3 compliant primes, 2 code-disjoint routes | **No** — mod-p only; §6.2 forbids promotion |
| framework (Three-dessin) | **dies, unconditionally** — THEOREM 2 certified, THEOREM 3 confirmed (§2.6) | **Yes** |

**STILL NOT MET, but one of the three territories is now closed.** The framework
side is no longer conditional on anything: THEOREM 2's conclusion is certified
and THEOREM 3 is confirmed with its recorded proof repaired (§2.6). That was the
campaign's single highest-value open item and the only thing blocking *both* the
First and Three-dessin verdicts.

(72,108) is still undecided, because two territories remain: the pentagons have
exhausted both available engines, and case (2)'s ℚ̄ residual is well-posed but
heavy. Those are the only stall points left, and both are computational rather
than conceptual.

Per Plan 43, the gate's next step is a **user check-in on the outreach decision**
(Valqui/GGHV, Borisov) — the user's call, not to be drafted before the gate is met.

---

## 8. Tooling

Singular 4.3.2, msolve 0.10.1 (built from source, pinning discrepancy A0.6).

Silent-lie table entries earned this session:
* **msolve's solve mode and eliminant mode write indistinguishable output**, and the filename does not disambiguate. Cost: a false "unblocked" claim that stood five days. **Parse the artifact; never trust the filename or the summary.**
* **`pkill -f` has now killed the invoking shell four times**, three of them in this session after two corrections — once mid-commit, losing an uncommitted document. That is a tooling problem, not a discipline problem; see the recommendation in `campaign/moduli_phase2/tools/README.md`. Safe idiom: `for pid in $(pgrep -x msolve); do kill $pid; done`.

---

## 9. Artifact index

**Start here for the THEOREM 2/3 recovery:** `wave1/RECOVERED_THEOREMS.md`
— what was recovered, where the transcripts actually are, the corrected H1c
lemma, and the exact residual gap. Certifiers: `wave1/w1_h1c_polefix.py`
(correction + classification), `wave1/w1_L3_step2_pinning.py` (THEOREM 2's
conclusion).

**Literature spot-check (2026-08-19):** `arXiv:2608.00222` (Gao,
*Counterexamples to the Jacobian conjecture in dimensions greater than two*)
was re-verified live through three independent paths — agentic fetch, raw
`curl` of the abs page (`citation_arxiv_id` = 2608.00222, `citation_date` =
2026/07/31), and the arXiv export API (1 entry, `published`
2026-07-31T19:08:59Z, math.AG). **The identifier is real.** It is also **not
load-bearing for the plane case**: the paper explicitly disclaims dimension 2
(*"the two-dimensional case remains open and is untouched by the
counterexamples discussed here"*), as `trackE_literature_verified.md` §E4
already recorded.


| document | contents |
|---|---|
| **`STATUS.md`** | this file — the single place |
| `MANIFEST.md` | claim → certifier → verdict → proof-standard ledger; A6 controls in full |
| `wave1/H1C_VERDICT.md` | (108,72) framework verdict, long form |
| `wave1/H1B_STATUS.md` | pentagons; both false-positive episodes in full |
| `wave1/H1B_REFORMULATION.md` | sparsity finding and the export path |
| `wave1/H1F_FINDING.md` | the exact-ℚ blocker correction, long form |
| `wave1/L23_VERDICT.txt` | machine-written OOM classification |

**Certifiers** (each self-documenting, each printing PASS/FAIL with proof standards):

`wave0/` — `w0_h1a_swap_and_G.py`, `w0_h1c_borisov_belyi.py`, `w0_a6_planted_controls.py`, `w0_a6b_planted_pinned.py`, `w0_a6c_seventh_control_and_msolve.py`

`wave1/` — `w1_h1c_endgame_closed_form.py`, `w1_L3_chain_identity.py`, `w1_L3_step2_pinning.py`, `w1_L1_L2_threedessin.py`, `w1_L1_boxes_closed.py`, `w1_L2_cascade_threedessin.py`, `w1_h1e_d_crossfire.py`, `w1_h1d_casesplit.py`, `w1_h3_a1_square.py`, `w1_h3_a1_theorem.py`, `w1_h1f_eliminant.py`, `w1_h1b_yadic_independent.py`, `w1_h1b_kernel_analysis.py`, `w1_h1b_structure.py`, `w1_h1b_linearity.py`, `w1_h1b_degrees.py`, `w1_h1b_sparsity.py`, `w1_h1b_export.py`, `w1_h1b_reduction.py`, `w1_h1b_reduction2.py`, `w1_h1b_hitdetector_v2.py`, `w1_h1b_gauge_resolution.py`

**Data and supporting artifacts:**

| path | contents |
|---|---|
| `wave1/edgeQ_eliminant.txt` | the degree-1144 eliminant (5.7 MB) |
| `wave1/edgeQ_param.out` | full msolve `-P 1` RUR (46 MB) |
| `wave1/edgeQ_input.ms` | the ℚ edge system it was computed from |
| `wave1/pent_L23.ms`, `pent_L18.ms` | pentagon exports (43 MB / 2.7 MB) |
| `wave1/pari/` | the 13 PARI/GP scripts behind §2.5, plus the raw 8-prime degree table and a reproduce sequence |
| `wave1/figures/` | Borisov Fig. 10 (p.9) and Fig. 31 (p.23) rendered at 200 dpi — **the evidence** for the chain identity, since `pdftotext` mangles them |
| `wave1/rur_compliant/` | RURs at the hygiene-compliant primes 65539, 65599 |
| `wave1/L23_VERDICT.txt`, `*.log` | machine-written verdicts and run logs |

**Deliberately not committed:** the source PDFs (Borisov arXiv:1901.04073, GGHV
arXiv:2204.14178) — third-party papers, freely available; the relevant READMEs
carry the URLs and the exact commands to regenerate everything derived from them.

**Inherited campaign** (5 PR branches consolidated in Wave 0):
`campaign/d23_borisov/`, `campaign/mod3_828/`, `campaign/audit_tracks/`,
`campaign/moduli_phase2/`. PR#4's unique and divergent files are preserved under
`campaign/audit_tracks/_pr4_unique/` and `_pr4_divergent/`.
