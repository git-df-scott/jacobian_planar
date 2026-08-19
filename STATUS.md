# STATUS — Plane Jacobian Conjecture campaign

**Read this first.** Single index of where everything stands, what is certified,
and what is not. Last updated: session of 2026-08-19 (Plan 43, Waves 0–1).

> **No counterexample has been found. No non-EMPTY verdict exists on any real
> system, ever.** Nothing has been promoted from mod-p to ℚ. Everything below
> that sounds like progress is progress toward *closure*, not toward a hit.

---

## 1. Where to find things

| what | where |
|---|---|
| **This index** | `STATUS.md` (you are here) |
| Claim → certifier → verdict ledger | `MANIFEST.md` |
| Session-0 consolidation of 5 PR branches | `campaign/{d23_borisov,mod3_828,audit_tracks,moduli_phase2}/` |
| Wave-0 certifiers (swap lemma, G, Belyi, A6 controls) | `wave0/` |
| Wave-1 certifiers (endgame theorem, L1/L2/L3, H1b, H1e, H3, H1d) | `wave1/` |
| Pentagon status + the false-positive record | `wave1/H1B_STATUS.md` |
| Pentagon reformulation + sparsity finding | `wave1/H1B_REFORMULATION.md` |
| (108,72) framework verdict | `wave1/H1C_VERDICT.md` |
| **H1f: the exact-ℚ blocker correction** | `wave1/H1F_FINDING.md` |
| Engine contract + silent-lie table | `campaign/moduli_phase2/tools/README.md` |

---

## 2. The target

GGHV (arXiv:2204.14178, **unrefereed**, v1 only) eliminate every degree pair
with max < 125 **except (72,108)/(108,72)**. The refereed floor is Nguyen's 104
(*Quaestiones Mathematicae* 48(2) 2025). So the live territory is:

* **(72,108)** — the one surviving pair below 125. Undecided.
* **max ≥ 125** — mostly unexplored (~150 of 167 enumerated targets unrun).
* everything resting on unrefereed work in **[105,124]**.

`J(Q,P) = −J(P,Q)`, so **(72,108) and (108,72) are one territory** — proved two
independent ways (`wave0/w0_h1a_swap_and_G.py`).

---

## 3. Certified this session

### The endgame obstruction, in closed form
`wave1/w1_h1c_endgame_closed_form.py`

> For every `D ≥ 1` and `k ≥ 0`, `(v+1)^k(3v(v+1)R′ − D·R) = −c` with `c ≠ 0`
> has a rational solution of degree ≥ 1 **iff `k = 0` and `3 | D`.**

The homogeneous equation integrates to `C(v/(v+1))^{D/3}`, rational iff `3 | D`.
Verified for **symbolic** D; reproduces the campaign's per-degree ledgers
(rank 14 at D=13, rank 24 at D=23) as corollaries. Uniform in D, no ceiling.
Consequences: **L4 is immaterial** (every k dies); the `3|D` loophole is exact.

### (108,72), framework side
`wave1/H1C_VERDICT.md`, `wave1/w1_L3_step2_pinning.py`, `wave1/w1_L1_L2_threedessin.py`, `wave1/w1_L1_boxes_closed.py`

Borisov's Three-dessin Framework predicts **(108,72)** (verbatim from §5), and
its third Belyi map `x³(x−5)²/108` is certified exactly (degree 5, ramification
(5)/(3,2)/(2,1,1,1), defined over ℚ).

| layer | status |
|---|---|
| L1 chart | **complete** — inversion, monomial rule, chart factor, Keller form, pole depths (−9,−6) |
| L1 boxes | **complete** — not load-bearing; the layer-1 conditions are box-independent |
| L2 contact | **complete** — contact −5, 13 vanishings, confirmed independently by L3's `eW = −5` |
| L2 cascade | **UNCHECKED** — the one remaining gap |
| L3 rigidity | **complete** — `g = αU(U−1)⁸` pins, `deg g = N/μ + ε = 9` |
| L4 | **immaterial** (closed-form theorem) |

**Verdict: the Three-dessin Framework at (108,72) dies, conditional on the L2
cascade alone.** Down from three named gaps to one.

### The eliminator is controlled (A6)
`MANIFEST.md` §G. Every campaign EMPTY comes from `groebner(I)` → `dim == -1`,
which had said EMPTY 46 times and non-EMPTY **zero** times. Now demonstrated to
emit non-EMPTY on real data and on planted same-support data-mutants, at three
primes, in two engines — while still emitting EMPTY on provably empty input.
Plus the descent map **G as a seventh gate control**: it passes five gates
including the hard non-injectivity gate and is stopped by exactly G1/G6.

### Closed as hiding places
* **H1d** — GGHV's Prop 4.3 case split is **exhaustive**; "one or two linear factors" is a *bound* (`deg_z R = 2` from `e(R) = (7,2)`), not an assumption. No case (3).
* **p₁₀ = 0 chart** — provably empty; `p₁₀·Q₁ = x²` forces `p₁₀ ≠ 0`.
* **H1e geometric-degree crossfire** — NEGATIVE. Every bound runs the wrong way; the one actual value at this degree pair is `d = 16`, clearing the `d ≥ 6` literature floor.
* **H3-A1 reverse descent** — the `k = 0` stratum forces `F = (f₁,f₂,cx)` and is **equivalent to JC2 itself**, so it cannot yield a counterexample that does not already exist. Closed as a hit source.

---

## 4. H1f — COMPLETE, and it corrected the record

`wave1/H1F_FINDING.md`

**AUDIT_REPORT.md §2 claimed the exact-ℚ blocker was cleared. It was not.** The
file it cites, `trackB_edgeQ.msolve.out`, contains **28 real solution boxes**
(7 coordinates each, dyadic endpoints) — not an elimination polynomial. msolve's
own help explains why: *"When input coefficients are rational numbers: real
solutions … (see the **-P flag** to recover a parametrization)."* The campaign
ran without `-P`.

**Now fixed.** Re-run with `-P 1`:

| | |
|---|---|
| eliminant degree | **1144** — matching the independently recomputed `vdim` |
| squarefree | **yes** (`gcd(f,f′) = 1`) |
| leading coefficient | 4666 digits |
| saved | `wave1/edgeQ_eliminant.txt` (5.7 MB), full RUR in `wave1/edgeQ_param.out` (46 MB) |

The four H1f items:

1. **Eliminant** — was blocked (the artifact did not exist); **now computed**.
2. **Route-2 prime hygiene** — the CASE2 route used 65521 (ok), **32003 and 65537 (both ≡ 2 mod 3, violating the rule)**. Re-run at compliant primes **65539** (8 factors, degrees 1,2,2,6,6,6,6,6) and **65599** (6 factors, 1,3,3,4,12,12), both summing to 35: **every branch reproduces `dim = 2`, same component `(α₂,α₃,β₂,β₃)`.** The verdict survives the hygiene fix.
3. **Route-1/Route-2 provenance** — file-level disjoint (no shared source files; hashes recorded). Both still descend from the same GGHV polygon derivation, so this is *code* disjointness, not full independence. Stated, not overclaimed.
4. **Gauge-quotient integrity on the dim-2 survivor** — the survivor is a *linear* component `β₂=β₃=α₂=α₃=0` with `β₁,α₁` free, and the gauge group is exactly 2-dimensional (`β₁` = weighted scaling, `α₁` = additive constant of A, which every equation sees only through `A′`). **Dimensions match: 2 = 2.** It is also excluded independently — on it `a₈ = 0`, killing the vertex (8,16) of N(P), so it is not case (2) at all. Disposed of twice over.

### 4a. The eliminant is irreducible over ℚ — NEW RESULT
`wave1/w1_h1f_eliminant.py`

A planned shortcut **did not exist and is recorded as a plan error**: substituting
the RUR eliminates only the 7 edge variables, leaving **13 free** (leaf 1) — so
there is no univariate polynomial in θ and no gcd to take.

Instead, Dedekind's criterion, at 8 good primes (all squarefree mod p, all
degree-sums 1144). **No proper factor degree is a subset sum at every prime**, so:

> **The degree-1144 edge eliminant is irreducible over ℚ.** `[PROVED-exact]`

Controls confirm the sieve can *detect* reducibility (a planted 400+744 split is
found; a totally-split prime leaves all 1143 degrees surviving).

**Proves:** `K = ℚ[θ]/(f)` is a single degree-1144 number field; all 1144 edge
points are **Galois-conjugate**, so either all extend or none do — the ℚ̄ question
is one yes/no about the generic point; there are **no rational edge points**; the
exact-ℚ branch structure is *simpler* than the mod-p one (which splits into 4–12).

**Does not prove:** case (2) empty over ℚ̄ — that needs the residual system in 13
variables over K, not done. Nothing about case (1). And it is **not** a
confirmation of the recorded mod-p EMPTY — different object, different verdict
class per §6.2. Chart `d_3_3 = 1` only.

---

## 5. Open

| item | state |
|---|---|
| **L2 cascade** on the three-dessin chain | last framework gap; inputs identical, promotion not rebuilt |
| **H2** above-125 sweep | ~150 of 167 targets unrun; chain→polygon map needs hardening |
| **H4** deg_y = 3 slice | FRAMEWORK.md's own OPEN-1; untouched |
| **Pentagons (H1b)** | undecided; see §6 |
| exact-ℚ closure of case (2) | **still open.** The eliminant exists and is **irreducible over ℚ** (§4a), so there is a single branch — but the residual system (13 variables over a degree-1144 field) is not solved |

---

## 6. Pentagons — what is known

`wave1/H1B_STATUS.md`, `wave1/H1B_REFORMULATION.md`

* y-adic Jacobian **rank 60 of 61**, independently reproduced at two primes.
* The gauge group is **3-dimensional** (translation, overall scale, coordinate scale `(x,y) → (λx, λ⁻³y)`), so **58 essential parameters** against 60 independent conditions — overdetermined by 2, before 314 surplus conditions.
* Conditions have **degree 12–23** but are **sparse**: 686 monomials at level 13, 59,626 at level 23 — eleven orders below the dense bound. **They can be written down.**
* Exported: `wave1/pent_L23.ms` — 66 conditions, 1,080,147 monomials, 43 MB. First exportable pentagon system in the campaign's history.
* msolve on it: **OOM** at 15 GB (`wave1/L23_VERDICT.txt`). STALLED, stall point named. **Emptiness is not claimed.**

### Two false-positive episodes, both recorded in full
The Newton hit-detector reported "candidate hits" twice; **both were gauge
artefacts**, caught by the §6.1 adversarial check before reaching any committed
claim.

* **v1** used an *absolute* stopping test on a system homogeneous of degree −1 in P's scale. Newton drove `‖x‖ → 10¹⁰`; Q collapsed to zero and every support condition was satisfied vacuously.
* **v2's outlier** (ratio 1.70e−09) inflated the *denominator* instead: the unfixed coordinate-scale gauge moves forbidden and allowed coefficients by different powers of λ, driving the ratio down eleven orders with nothing solved.

**Standing requirement for any future detector:** fix all three gauges, use an
**absolute** normalisation (a ratio is breakable from either end), and make
"allowed coefficients are O(1)" an *acceptance* condition, not a post-hoc check.

---

## 7. Corrections made to the record this session

1. `AUDIT_REPORT.md` §2 — "the blocker is now gone" is **wrong**; the eliminant never existed (§4).
2. `AUDIT_REPORT.md` §1 — leaf-1 at p=65521/65599 is **stale, not overstated**; PR#4 carries the completed terminals. All 24 leaf-1 terminals are EMPTY at three primes.
3. `phase2_moduli/README.md` — the "Compositio Math 160 (2024)" reference for GGHV is wrong; GGHV is unrefereed.
4. Plan 43's "run T7 on G" — ill-posed; **G is not étale**.
5. Plan 43's A2.8 — not a conflict; a scope ambiguity, reconciled.
6. My own: the pentagon "cannot be written down" claim (retracted, §6); the "a+b=12" box framing (retracted); the parameter count 60 → 59 → **58**.

## 8. Tooling

Singular 4.3.2, msolve 0.10.1 (source). **`pkill -f` has now killed the invoking
shell four times across the campaign, three in one session after two
corrections.** That is a tooling problem, not a discipline problem — see the
recommendation in `campaign/moduli_phase2/tools/README.md` to put it out of
reach. Safe idiom: `for pid in $(pgrep -x msolve); do kill $pid; done`.
