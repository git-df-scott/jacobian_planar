# MANIFEST — claim → certifier → verdict → proof standard → dependencies

Built in Plan 43 Wave 0. **Scope note, stated first:** this manifest covers the
claims Wave 0 actually touched, plus the inventory of every claim-bearing
artifact inherited from Sessions 1–42. It is the *skeleton* of the coverage
matrix demanded by Plan 43 §5 (exit criterion `UNCHECKED = 0`), not the
completed matrix. Wave 0 closes 12 rows and leaves the rest `UNCHECKED` **by
name**, which is the point: an unnamed unchecked claim is invisible, a named one
is work.

## Proof-standard vocabulary (Plan 43 §6.3)

| label | meaning |
|---|---|
| `PROVED-exact` | symbolic identity over ℚ, no floats, ≥2 independent routes |
| `CERTIFIED` | computed by Singular/msolve in exact arithmetic, artifact on disk |
| `EMPTY-mod-p(p₁,p₂)` | geometric emptiness (`dim = −1`) at named good primes. **Never** promoted to ℚ |
| `evidence(strength)` | stated with its exact strength, never as a verdict |
| `CONDITIONAL(X)` | holds only if X; X named |
| `LIT-READ(ref, refereed?)` | read from the source, refereed status recorded |
| `UNCHECKED` | asserted somewhere in Sessions 1–42, never re-verified |
| `NOT-APPLICABLE` | the cited theorem's hypothesis fails; recorded, not forced |

---

## A. Claims CLOSED in Wave 0

| # | claim | certifier | verdict | standard | depends on |
|---|---|---|---|---|---|
| W0.1 | `J(Q,P) = −J(P,Q)`; a (72,108) counterexample exists ⟺ a (108,72) one does | `wave0/w0_h1a_swap_and_G.py` | TRUE | `PROVED-exact` (sympy + independent dict/Fraction convolution) | — |
| W0.2 | Live-Map rows L1 and L2 are one territory, not two | W0.1 | TRUE | `PROVED-exact` | W0.1 |
| W0.3 | `det JG = −2(3u+v−2)²`, `deg G = (6,4)`, ratio 3:2 | `wave0/w0_h1a_swap_and_G.py` | TRUE | `PROVED-exact` | — |
| W0.4 | G is non-injective; the collision descends from Alpöge's F through `π=(xy,x²z)` | same | TRUE | `PROVED-exact` (recomputed from F, not copied) | — |
| W0.5 | geometric degree `d(G) = 3` | `wave0/w0_G_vdim.sing` | TRUE | `CERTIFIED` (Singular `vdim` over ℚ(a,b) = 3; was numeric-only before) | — |
| W0.6 | **G is NOT étale** — `det JG` vanishes on `h=0` | same | TRUE | `PROVED-exact` | — |
| W0.7 | ⇒ T7 and every étale-hypothesis census invariant are **NOT-APPLICABLE** to G | W0.6 + T7's proof (S37 WP-F) | — | `NOT-APPLICABLE` | W0.6 |
| W0.8 | Borisov arXiv:1901.04073v2 §5 states the Three-dessin Framework's Keller degrees are **(108,72)** | source read (`pdftotext`) | TRUE, verbatim | `LIT-READ(1901.04073v2, arXiv-unrefereed; EJC status UNCHECKED)` | — |
| W0.9 | its third Belyi map is `t ↦ x³(x−5)²/108`: degree 5, ramification (5)/(3,2)/(2,1,1,1) over ∞/0/1, critical values exactly {0,1}, **defined over ℚ** | `wave0/w0_h1c_borisov_belyi.py` | TRUE | `PROVED-exact` (ramification recomputed, not trusted) | W0.8 |
| W0.10 | GGHV arXiv:2204.14178 is **unrefereed** — v1 only (29 Apr 2022), no journal ref, no revisions | arXiv abstract page | TRUE | `LIT-READ` | — |
| W0.11 | Miyanishi arXiv:2110.06709 (**Transformation Groups**, refereed) closes **even**-order finite actions | arXiv abstract page | TRUE | `LIT-READ(refereed)` | — |
| W0.12 | the campaign's degree-1144 case-(2) edge eliminant, re-derived independently | `wave0/a6_C2_p65521.sing` | `vdim = 1144` | `CERTIFIED` (fresh Singular run, `dp`, from the JSON system) | — |

## B. Corrections Wave 0 makes to Plan 43 itself

| # | Plan 43 said | Wave 0 finds | consequence |
|---|---|---|---|
| C.1 | "run T7 on G" as a Wave-0 freebie | G is not étale, so T7's hypothesis fails | freebie **withdrawn as ill-posed** (W0.6/W0.7). The census row for G must record d=3 and stop there |
| C.2 | "The accepted refereed bound is 104 (T. Nguyen, Quaest. Math. 48(2) 2025)" | **not located** in 3 independent searches | `UNVERIFIED`. The confirmed refereed floor is **Moh's 100**, which GGHV's own abstract endorses ("we confirm the lower bound of 100 obtained by Moh"). The unrefereed-only window is therefore **[101,124]**, wider than the plan's [105,124]. §9's "max ≥ 105" filter must be weakened to "max ≥ 101" until Nguyen is found |
| C.3 | A0.1: "AUDIT_REPORT.md §1 overstates leaf 1 at p=65521 (no EMPTY line exists for the r0b terminal)" | AUDIT_REPORT is **stale, not wrong**. PR#4 carries `trackB_st2_L1_p65521_r0b_f0_f0_f0_f0.done` **and** the p=65599 twin, both `RESIDUAL DIM: -1 → EMPTY` | leaf 1 is terminal-complete at **all three** primes. See §D |
| C.4 | H1c: "derive and certify its three Belyi maps" | Borisov **gives** the third in closed form and says the other two are the First Framework's, already certified at D=13 | H1c step 1 is **done**, not a work item |
| C.5 | "five explicit maps" attributed to Gao | Gao's abstract lists 5 maps (3D d=4; 4D d=5,10; 5D d=6,12); Alpöge's d=3 F is separate | plan's table is consistent; noted to prevent a miscount in H3.2 |
| C.6 | Meng–Yang's technique unnamed | it is **"Schur descent"**, from Alpöge's map | directly relevant to H3 (the descent program) — H3 and H10 share machinery |

## C. Environment (pins A0 discrepancy #6)

| tool | version | provenance |
|---|---|---|
| Singular | 4.3.2 (4330, 64-bit) | apt |
| msolve | **0.10.1** | built from source per `tools/README.md`, `/usr/local/bin/msolve` |
| sympy / numpy | 1.14.0 / 2.4.6 | symbolic identities only, never Gröbner |
| PARI/GP | 2.15.4 | available |
| box | 4 cores, 15 GB RAM | — |

The 0.6.5-apt / 0.10.1-source split recorded in Plan 43 A0.6 is resolved by
pinning **0.10.1-source**; the apt candidate (0.6.5) was never installed here.

## D. Discrepancy ledger (Plan 43 §5 A0, items 1–10)

| # | item | status after Wave 0 |
|---|---|---|
| 1 | AUDIT_REPORT overstates leaf-1 at p=65521 | **RESOLVED — in the opposite direction.** All 24 leaf-1 terminals across p ∈ {65521, 65539, 65599} carry `RESIDUAL DIM: -1 / EMPTY`; the two the report calls stuck live on PR#4 (`_pr4_unique/`). AUDIT_REPORT.md was written before those runs landed and is **stale**, not overstated. Branch-cover argument audited in §E |
| 2 | Route-2 primes 32003/65537 ≡ 2 (mod 3) | `UNCHECKED` — still open (H1f) |
| 3 | FRAMEWORK.md uniform closure vs D=23 conditional DIES | `UNCHECKED` — the A2.8 reconciliation, now **load-bearing for H1c** (see §F) |
| 4 | stale RESUME_STATE / PR#4-body lines | `UNCHECKED` |
| 5 | trackD_state.json results undocumented | `UNCHECKED` |
| 6 | msolve version split | **RESOLVED** — pinned 0.10.1-source (§C) |
| 7 | verdict tally 45 vs 46 | `UNCHECKED` — must be regenerated mechanically from logs, not counted by hand |
| 8 | phase2_moduli/README claims S19–35, stops at S23 | `UNCHECKED` |
| 9 | FRAMEWORK.md omits tools/, predates S38 | `UNCHECKED` |
| 10 | PR#5's "Compositio Math 160 (2024) 2775–2827" reference for GGHV | **RESOLVED — the reference is wrong.** arXiv shows v1-only, no journal ref (W0.10). GGHV is unrefereed; every closure resting on it is `CONDITIONAL(GGHV unrefereed)` |

## E. The leaf-1 branch cover — audited, not assumed

The cover emitted by `trackB_leaf1_sweep.py` + `trackB_r0.py` is

```
{d_3_3 = 0}                      → r0b subtree
∪ {d_3_3 = 1, d_9_15 = 0}        → r0a subtree
∪ ⋃_k {d_3_3 = 1, f_k = 0}       → rk0 … rk{n−1},  f_k the irreducible
                                    factors of the edge eliminant E[1]
```

Soundness of the cover, as read from the code:
* `d_3_3 ≠ 0 ⇒ WLOG d_3_3 = 1` is a **gauge normalization** — `CONDITIONAL(gauge-scaling acts on d_3_3)`, which is Plan 43's A2.10 and is **still UNCHECKED**;
* branching on `E[1]` alone is **sound for covering**: `V(I)` projects into `V(elimination ideal) ⊆ V(E[1])`, so the factors of `E[1]` cover — using one generator is weaker, hence safe;
* `R0.close` is called **unconditionally** for r0a and r0b, so the cover holds whether or not `d_9_15` divides the eliminant;
* the recursive split factors a **univariate generator of the GB**, and `V(body) = ⋃ V(f_i)` over `F̄_p` — sound;
* factor counts differ per prime (6 / 5 / 4 eliminant branches at 65521 / 65539 / 65599), i.e. the trees really are **built per prime, not replayed** — this is Plan 43 §6.2's sharpest requirement, and the code satisfies it.

Residual risk, named: `factorize` output is parsed with the regex `_\[\d+\]=(.+)$`, which reads **one line**. A factor long enough for Singular to wrap would be silently truncated. Not triggered here (the split polynomials are univariate of degree ≤ 6) but it is a live latent defect for any wider use. `UNCHECKED` → filed for A4 mutation testing.

**Verdict on leaf 1:** `EMPTY-mod-p(65521, 65539, 65599)`, `CONDITIONAL(gauge normalization d_3_3=1)`. Not ℚ. Not promoted.

## F. What H1c now turns on

Borisov's Three-dessin Framework is confirmed real, its degrees are (108,72),
and its only *new* Belyi datum is rational and rigid (W0.8, W0.9). Its other two
Belyi maps are the First Framework's, which this campaign certified at D=13.

FRAMEWORK.md §4.2 claims a **uniform** framework closure: "Belyi gate closes
every D ≥ 4, uniformly in the cusp exponent, no upper bound", plus "contact
exponent derived: k = ε(m+n) − 1 ≥ 4 always ⟹ the D ≤ 3 window is empty".
Taken at face value that closes **every** framework, this one included.

It cannot be taken at face value yet, for a reason Wave 0 can state precisely:
that closure was derived on **two-dessin** frameworks. The Three-dessin
Framework has a third forked vertex and, in Borisov's words, "no curves of type
4". Whether the chain → master-equation → endgame-obstruction argument transfers
across that structural change is **exactly** the "FF-specific transfer never
performed" of Plan 43's L8, and it is now the single decisive question for
(72,108) on the framework side. It is also the same object as A2.8 (the
unreconciled uniform-closure vs D=23-conditional-DIES pair).

**Status: `UNCHECKED`, and promoted to the top of Wave 1.**
