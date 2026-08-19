# Opus 5 Session Report — Sessions 19–20

**Plane Jacobian conjecture (JC2).** Handoff document. Written to be picked up
cold by someone who was not here.

**Bottom line: no counterexample was found.** What was produced is (a) a
corrected answer to the Session-19 mod-3 question, (b) a literature correction
that relocates the entire campaign's target, (c) six of seven branches closed at
the one degree pair still open below 125, and (d) a large pile of retractions,
because most of what broke tonight was my own code looking like mathematics.

---

## 0. The one-paragraph version

Session 19 asked whether the `3` in `3v(v+1)R' = D·R` is fundamental. It is
**`k`, the primitive multiplicity of the boundary valuation** — verdict **(c)**,
neither of the offered options. Session 20 then tried to find an actual
counterexample, discovered that the campaign's target degree pair `(66,99)` had
been closed in the literature since 2022, retargeted to `(72,108)` — the unique
admissible pair below 125 — reduced its open Newton-polygon shape from 72
unknowns to 20, decomposed that into 7 branches along a Newton-polygon edge, and
killed 6 of them. The 7th is still running. Nothing is proven: everything is mod
`p`, and a soundness audit of the reduction has not returned.

---

## 1. State of the field (verified against primary sources)

| fact | status |
|---|---|
| JC2 open since 1939 | — |
| Counterexample ⇒ `max(deg P, deg Q) ≥ 125`, **or** pair is `(72,108)/(108,72)` | GGHV, arXiv:2204.14178, Thm 2.1, **[VERIFIED verbatim]** |
| `(66,99)` excluded outright | GGHV Thm 5.1/Cor 5.7, 2022 **[VERIFIED]** |
| `(72,108)` splits into two shapes; `(9,27)` closed, `(8,28)` **open** | GGHV Prop 4.1 / Prop 4.3 **[VERIFIED]** |
| GGHV never write the `(8,28)` system down | **[VERIFIED]** — "we couldn't solve the corresponding system of polynomial equations, thus it is left open" |
| arXiv:2204.14178 is v1 only, never superseded | **[VERIFIED]** |
| Nobody 2022–2026 has closed `(72,108)` | **[VERIFIED]** across 5 independent sweep modalities |
| July 2026 dim-≥3 counterexample does **not** touch the plane case | **[VERIFIED]** — Gao arXiv:2608.00222 says so explicitly |
| Smallest survivors above 125: `(75,125)`, `(84,126)`, `(96,128)`, `(88,132)`, `(90,135)` … to 150 | from arXiv:1708.07936 §6 |
| Above 150: nothing exhaustive exists | — |

**The campaign's own premise was three years stale.** Sessions 7–19 targeted
`(66,99)`, closed in 2022 by a general argument. The Session 16–18 emptiness
theorem is correct but strictly weaker than the published result.

### 1a. A silent retraction found (worth propagating)

`arXiv:1708.09367` **v1** (2017) proved `gcd ≥ 25` and discarded infinite
families. **v2** (2018) was retitled and its abstract says, verbatim:

> "we obtained the same formula for IM, but for Im we obtained only **an
> inequality**, consequently **we cannot discard the infinite families as
> desired**."

v2's body no longer contains Theorem 4.1, Corollary 4.2, Corollary 5.3, or any
"36" claim (grep: zero hits). **No erratum notice.** Discoverable only by diffing
the PDFs. Moskowicz arXiv:1810.08202 propagates the retracted v1 claim. **The
`gcd ≥ 36` filter must not be used.**

---

## 2. Session 19 result — the mod-3 question

**Verdict (c).** The coefficient is `k`, the primitive multiplicity of the
boundary valuation vector `(val_E y1, val_E y2) = −k·(b,a)`. In Borisov's
framework `(9,6) = 3·(3,2)`, so `k = 3` — colliding with the cusp exponent `b=3`
and the chart slope `ρ=3`. It is neither.

Master identity, all inputs free, **two independent derivations plus a third in
concrete rational arithmetic**:

```
[q^D] K  =  g0^(a+b) · ( k·R'  +  D·R·(log g0)' )
```

`ρ` is provably **absent** — the identity is chart-independent. With
`g0 = α(v+1)^m v^σ`:

```
α^(a+b) (v+1)^((a+b)m−1) v^((a+b)σ−1) [ k·v(v+1)R' + D((m+σ)v+σ)R ] = −c·v^(ρ−ρ²)
```

Order matching: `D = (a+b)k + 1 − ρ` and `(a+b)σ = 1 + ρ − ρ²`. Specializing
reproduces `α⁵(v+1)⁴(3v(v+1)R′ − 13R) = −c` exactly, and *derives* `σ = −1`,
`e = 8` (i.e. the certified `g = αU(U−1)⁸`) rather than assuming them.

**Corollaries.** `k = (D+ρ−1)/(a+b)` is determined, not free — so D=23 gives
`k=5`, D=28 gives `k=6`, and the campaign's "the 3 transfers to all D" was wrong
(verdicts unaffected). The real universal obstruction is the **corner lemma**
`m ≥ 1`, forced only by `y1` being a polynomial with a pole along `E`.

**Also closed independently:** the cusp type is not a free parameter at all.
`J(P̄,Q̄)=0 ⇒ P̄^d₂ = cQ̄^d₁ ⇒ (a,b) = (d₂/n, d₁/n)`. `(99,66) → (2,3)`.
Choosing a cusp type *is* choosing a degree pair.

**Jung–van der Kulk collapse.** Every automorphism of ℂ² is tame and has one
degree dividing the other ⇒ the entire search target is `J(P,Q)=1` with
non-dividing degrees. No automorphism test needed anywhere.

---

## 3. Session 20 — what worked

### 3.1 The reduction pipeline (the thing that actually worked)

```
72 unknowns, 92 quadratic equations          (Prop 4.3, jc2_gghv_system.py)
  → 71   normalize d_2_1 = 1                 (scaling symmetry, PROVED)
  → 20 vars / 41 eqs   triangular elimination, exact over ℚ, 3 seconds
  → 7 vars / 6 eqs     closed subsystem on a Newton-polygon EDGE
  → dim 0, vdim 1144   after one more normalization
  → degree-43 eliminant, factors into 7 branches
  → 13 vars per branch after fixing the edge point
  → 6 of 7 branches DEAD
```

Two elimination rules, iterated to a fixed point: **R1** a single-monomial
equation forces a variable to zero; **R2** an equation linear in a variable with
an invertible monomial coefficient is solved and substituted.

**The structural discovery:** the 7-variable subsystem is exactly the interior
lattice points of the slope-2 edge of `N(Q)` from `(2,1)` to `(12,21)`, the line
`j = 2i−3`. The elimination rediscovered a Newton-polygon edge unprompted. That
is why the literature attacks this problem through Newton polygons.

### 3.2 Branch verdicts (GF(65521), `p ≡ 1 mod 3`)

| branch | `d_9_15` | edge | verdict |
|---|---|---|---|
| r1 | 28232 | vdim 1 | **DEAD** |
| r2 | 21444 | vdim 1 | **DEAD** |
| r3 | 16066 | vdim 1 | **DEAD** |
| r4 | quadratic | vdim 2 | **DEAD** |
| r5 | 19859 | vdim 2 | **DEAD** |
| r6 | 796 | vdim 2 | **DEAD** |
| r0 | 0 (mult 10) | vdim 280 | **running** |

Each run pins the solved edge basis, adds the residual, forces all four vertex
coefficients nonzero via Rabinowitsch `w·(c_8_14·c_8_16·d_12_21·d_12_24) − 1`,
**and prints a containment sanity check** (`I₀ ⊆ sat`), because a saturation
failing that is the bug that voided the first attempt.

### 3.3 Phase 4 — the direct attack

Phase 1 **cannot** produce a counterexample: a solution is a *reduced* pair,
related to a real Keller pair by an automorphism chain that must be inverted
(`jc2_gghv_system.md` §9). Phase 4 is direct — there `y₁,y₂` **are** `P,Q`.

The Session-19 escape (`R` with a pole of order exactly `p = (a+b)m−1` at
`v=−1`) is **inhabited**. At `(72,108)`, ten chain degrees remain open, each with
`R = S(v)/(v+1)⁴` **forced uniquely up to one scalar**:

```
k= 3, D=13: S = 243v⁴ −  81v³ +  54v² −  42v +  35,  c = −455
k= 4, D=18: S = 128v⁴ −  64v³ +  48v² −  40v +  35,  c = −630
k= 5, D=23: S = 625v⁴ − 375v³ + 300v² − 260v + 234,  c = −5382
...
k=12, D=58:                                          c = −1247290
```

Forced chain block: `W̃_n0 = α⁶·S(v)·(v+1)²·v^(3k)`, degree `3k+6`, against a box
cap of `18k`. **The cap never binds** — box combinatorics obstructs none of them.
Any obstruction must come from the realization layer.

**Refinement of my own Session-19 criterion:** `k·p ≠ D·m` is necessary but
**not sufficient** — the ODE's forced constant can vanish anyway, giving `c = 0`.
`k=1` satisfies `4 ≠ 3` and still dies.

### 3.4 The bulletproof gate (`jc2_bulletproof.py`)

Written **before** any candidate existed so it could not be tuned. Default
verdict is rejection; an errored gate counts as failure.

- **G0** char 0, exactly rational (JC is *false* in char `p`)
- **G1** bracket `= 1`, **two independent ways** — sympy expansion *and* a dict
  convolution sharing no code, so a shared bug cannot pass both
- **G2** non-dividing degrees (= "not an automorphism", by Jung–van der Kulk)
- **G3** interpolation **proof**, not a probabilistic test
- **G4–G6** leading forms, non-degeneracy, multi-prime

Validated against four known non-counterexamples including `(y³+x, y²+x)`, which
has non-dividing degrees and passes G2 *and* G4 — and dies at G1. All rejected.

---

## 4. What did NOT work — and every retraction

**This is the most important section for a handoff.** Six of my own conclusions
were withdrawn tonight. Each initially looked like mathematics.

| # | What I claimed | What was true |
|---|---|---|
| 1 | "All attacks fail to expression swell; probably the same wall GGHV hit" | **False.** Instrumentation showed max 21 terms, 706 total. Polynomials were tiny. The stall was an `O(eqs×vars×terms)` search loop. Inference withdrawn. |
| 2 | (implicit) the reduction is just slow | **Infinite loop.** On an undividable pivot my code did `eqs = [x for x in eqs if x is not src] + [src]; continue` — reordering the list, then reselecting the same pivot forever. Burned >1h of wall clock across two runs. Fixed by checking divisibility during pivot *selection*. |
| 3 | mod-`p` results are reliable | **False closure caught.** The residual's 2-variable equation has discriminant `−1/3`; branches exist iff `p ≡ 1 (mod 3)`. At `p = 32003` it forces `d_3_4 = d_4_7 = 0` — a spurious closure. Verified across 5 primes; matches the `p mod 3` rule exactly. |
| 4 | "vdim 3 ≠ 0, solutions exist" | **Degenerate.** The point satisfied all 92 equations (T1 PASS) but `c_8_16 = 0` and `d_12_24 = 0` — two Newton-polygon *vertices* collapse. Not a valid configuration. Exposed that the entire branch analysis was under-constrained. |
| 5 | Three branches closed via `sat()` | **Void.** Containment check showed `dim 0 → dim 19` with 20 of 21 generators falling out. Saturation must satisfy `I ⊆ sat(I,f)`. Discarded and redone with Rabinowitsch. |
| 6 | "Eleven open chain degrees"; "20 of 40 escape points open" | **Wrong counts.** Forced-constant bug not back-ported. True: **ten**, and **13 of 40**. Independently reproduced before accepting the audit's claim. |

**Also did not work:**

- **Direct Gröbner on the raw systems.** Singular OOM'd at 6GB on 71 variables
  and again on the 21-variable saturated residual. Even a degree-`(5,4)` *toy*
  Keller system (23 unknowns) does not finish. General-purpose elimination is
  useless here at any relevant size; this is why the field uses Newton polygons.
- **Exhaustive small-degree search.** `jc2_exhaustive_search.py` /
  `jc2_modular_search.py` decided only **4 degree pairs** — `(3,2)`, `(4,3)`,
  `(5,2)`, `(5,3)`, all EMPTY — before coefficient blowup. Pipeline validation
  only, **no mathematical content**.
- **Branches without a pinned edge.** `r0/r4/r5/r6` would not converge when only
  the `d_9_15` equation was imposed. Feeding the *solved edge basis* made three
  of them finish in ~1 minute each.
- **`n = b·k + H` is not general.** `G = b·k` holds only because `ρ = b` **and**
  `m+σ = 0` coincide in Borisov's construction. At other admissible `ρ` it fails.
  The `D = 13/23/28` retrodiction survives (it follows from relation (Q) alone),
  but the finite 12-point bound rests on **one data point**. So Phase 4's ten
  chain degrees are **one `(ρ=3, m=1)` slice**, not the admissible space.
- **Ramirez–Valqui 2025 / Valqui–Solórzano 2014.** Both checked, both
  **orthogonal**. The latter's tractability needs a sparsity condition
  (`λᵢ = 0`) that Prop 4.3's shape provably lacks.

---

## 5. File inventory

**Session 19 — the endgame derivation**
| file | contents |
|---|---|
| `session19_general_endgame.py` | master identity, two independent routes, 32/32 |
| `session19_parameter_lattice.py` | admissible lattice, `k` determined not free, 18/18 |
| `session19_self_audit.py` | leak detection, third concrete route, 14/14 |
| `session19_general_chart.py` | general monomial chart factor, `A = ε(Q′−P′)−1`, 9/9 |
| `session19_report.md` | full write-up, verdict (c), confidence MEDIUM |

**Session 20 — the hunt**
| file | contents |
|---|---|
| `jc2_cusp_from_degrees.py` | cusp type = `(d₂/n, d₁/n)`; Jung–van der Kulk, 10/10 |
| `jc2_escape_hatch.py` | escape inhabited; **fixed** to 13/40, 22/22 |
| `jc2_target_72_108.py` | **superseded in part** — annotated, stale count |
| `jc2_phase4_direct.py` | the ten forced `R`; use **this**, not the above |
| `jc2_gghv_system.py/.md` | Prop 4.3 system, 72 vars / 92 eqs; §9 = what solving proves |
| `jc2_gghv_modp.py` | GF(p) triangular reduction (fixed) |
| `jc2_gghv_exact.py` | same over ℚ, 3 seconds |
| `jc2_gghv_normalize.py` | scaling symmetry proof, `d_2_1 = 1` WLOG |
| `jc2_reconstruct.py` | push a point back up the chain; T1/T2 tests |
| `jc2_bulletproof.py` | **the gate** — run before claiming anything |
| `jc2_reduction_828.py/.md` | GGHV §5 redone for `(8,28)`; new ODE |
| `jc2_phase4_audit.py/.md` | adversarial audit, 33 checks, found 4 defects |
| `jc2_literature_*.md`, `jc2_valqui_framework.md`, `jc2_ramirez_valqui_2025.md` | literature |
| `jc2_status.html` | published visual |

**New mathematics believed correct and not in the literature:** the `(8,28)`
analogue of GGHV Prop 5.4 —

```
y⁸(y+1)² = 8y(y+1)·f₁′ − 14(8y+7)·f₁
f₁ = −y⁸(y+1)²(2048y⁴ − 512y³ + 320y² − 240y + 195)/6630
```

Independently verified in the main session: residual exactly 0, degree 14,
divisible by `y⁸(y+1)²`, cofactor coprime to `y(y+1)`, **solution space
1-dimensional** so `f₁` is unique.

---

## 6. Open at handoff

1. **`r0`** — last branch, running, near its memory cap. If it OOMs, decompose
   its 280-point edge into sub-branches (the move that rescued r4/r5/r6).
2. **Phase 0 soundness audit** — **the long pole.** Does rule R1 branch
   correctly? `u·w = 0` means `u = 0` **or** `w = 0`. If the code silently takes
   one, "all branches dead" covers only part of the tree and **every closure
   collapses.** Six closures are provisional until this returns.
3. **Characteristic zero.** Everything is mod 65521. Mandatory, given item 3 in
   the retraction table.
4. **`(8,28)` is not closed.** No counterexample found.

### Next steps, ranked

1. Finish `r0`; then redo all seven branches over ℚ.
2. If it closes → **bound moves 108 → 125**, a real result, *not* a
   counterexample.
3. Phase 4 on one forced `R` — the only route that outputs an actual map. Start
   with `k=3, D=13` (smallest, and the D=13 tower machinery exists from Sessions
   10–13).
4. Enumerate the `ρ ≠ 3` slices Phase 4 does not currently cover.
5. Above 125: `(75,125)` first — its `gcd = 25` was an exception in the
   *retracted* gcd theorem, so it may be softer than it looks.

### Standing rules for whoever picks this up

- A mod-`p` empty ideal is **evidence**, never proof. Use `p ≡ 1 (mod 3)`.
- A mod-`p` solution proves **nothing** — JC is false in characteristic `p`.
- Any saturation must print its containment check.
- Any candidate must pass `jc2_bulletproof.py` **and** have all Prop 4.3 vertex
  coefficients nonzero.
- A solution to the Phase 1 system is **not** a counterexample until GGHV's
  automorphism chain is inverted.
- Every "it's slow, must be hard mathematics" hypothesis tonight was a bug.
  Instrument before concluding.
