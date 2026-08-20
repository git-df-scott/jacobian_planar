# HUNT2_REPORT — the five territories

Branch `claude/opus-hunt-territories`, off `claude/plane-counterexample-endgame-az3geq`.
Nothing in the campaign record is used as a premise. Every verdict rests on a
certifier in this branch carrying at least one negative control that is required
to fail; the AST can't-fail scanner (`wave2/w2_cantfail_audit.py`, errors branch)
is clean on every file added here. Toolchain rebuilt from source per `BUILD.md`
(msolve 0.10.1, Singular 4.3.2p16). Primes are p ≡ 1 (mod 3) throughout.

---

## Table

| territory | what ran | artifacts | verdict class |
|---|---|---|---|
| **T1 GGHV audit** | GGHV's Theorem 2.1 imports its ten-case table from arXiv:1708.07936 §§5–6, so the mechanical object is *that* paper's Algorithms 1–9. Re-implemented from its pseudocode alone and run to M = 50 (max ≤ 150) and M = 100 (max ≤ 300) | `gghv_audit/ggv_algorithms.py`, `case_tree.json`, `rerun_105_124.json`, `all_cases_max_le_150.json`, `all_cases_max_le_300.json`, `DISCREPANCIES.md`, `controls.log` | **DONE — no discrepancy in the enumeration.** 34/34 published cases at max ≤ 150 and 10/10 rows of GGHV's own table reproduced exactly; 19/19 checks with four negative controls |
| **T2 same-sign weighted-homogeneous sector** | exact sweep of every weight pair a+b ≤ 12, every (dP,dQ), full monomial bases to total degree 20, exact primary decomposition over ℚ in Singular — no sampling | `samesign/sweep_results.json`, `samesign/sweep.log`, `w5_samesign_sweep.py` | **EMPTY of non-automorphisms.** 230 cells, 378 Keller branches, **0** non-automorphisms; 9/9 controls |
| **T3 μ_n-restricted (72,108) slices** | every faithful (n,a,b,p,q) for n ∈ {2,3,4,6}; restricted systems built mechanically; degeneracy screen; solver confirmation on the largest cell per n at 3 compliant primes | `symslice/symslice_results.json`, `symslice/symslice.log`, `symslice/artifacts/` | **EMPTY.** 1140/1140 cells killed; n = 1 control reproduces the unrestricted system exactly (72 vars, 92 eqs) |
| **T4 lift pipeline** | Hensel lift to p^8, half-extended-Euclid rational reconstruction, exact verification over ℚ; validated on a planted rational system and an irrational-only system; applied to every real mod-p point this session produced | `lift/lift_pipeline.py`, `lift/run_lift.py`, `lift/lift_results.json` | **DONE — 3/3 controls; no rational point.** The case-(2) w=−4 mod-p points lift cleanly to p^8 and are **not** rationally reconstructible. The H2 queue has 0 LIVE targets, so nothing else to lift yet |
| **T5 Gao family audit** | both dimension-3 members re-expanded from the printed components and cross-checked against the paper's own §3.3 recipe; det J exact; descent content exponent computed two independent ways; non-injectivity witnesses | `gao/family.json`, `gao/mechanism_table.md`, `gao/gao_audit.log` | **DONE — no PORT-CANDIDATE.** 17/17 checks; both maps sit at k = 2 by both routes |

**No CANDIDATE-UNVERIFIED and no PORT-CANDIDATE was produced by any territory.**

---

## T1 — the shape of the audit, and what it found

GGHV (arXiv:2204.14178) does **not** enumerate degree pairs. §2 says so: "Based
on the tables obtained in sections 5 and 6 of [5], we begin with the study of the
cases with max < 125", and prints ten rows imported from
[5] = arXiv:1708.07936. So (b) "run the elimination over every degree pair with
105 ≤ max ≤ 124" is, mechanically, a re-derivation of [5]'s Algorithms 1–9.
That is what `gghv_audit/ggv_algorithms.py` is, written from the pseudocode and
definitions of [5] and from nothing else.

**Reproduction (positive controls, all in `controls.log`).**

* (2,1), (6,3) and (8,4) are all absent from my independently computed PLLC —
  the three exclusions [5] §6, [5] §5 and GGHV §3 respectively depend on;
* no admissible complete chain has v11(A0) ≤ 15 ([5]'s B ≥ 16);
* the 14 length-1 chains and the 7 length-2 chains F18–F24 of [5] §5;
* all three of [5] §6's tables — 13 family cases, 9 further length-1, 11 further
  length-2, 1 length-3 — **exactly 34, row for row**;
* GGHV's own ten-row §2 table equals the max ≤ 124 part of the reproduction.

**The 105 ≤ max ≤ 124 rerun, in the literal form asked for.** For an ordered
pair (d₁, d₂) the data are forced — `g = gcd(d₁,d₂) = v11(A₀)`, `m = d₁/g`,
`n = d₂/g` — so every pair in the window can be decided outright, and
`gghv_audit/w5_pairs_105_124.py` (4/4 checks) decides **all 4560 of them**:

| outcome | pairs | reason |
|---|---:|---|
| ARISES | **6** | the six orientations of (72,108), (80,112), (80,120) |
| ELIMINATED-BY-ENUMERATION | 214 | gcd forces m = 1 or n = 1 |
| ELIMINATED-BY-ENUMERATION | 4316 | no admissible complete chain has that v11(A₀) |
| ELIMINATED-BY-ENUMERATION | 24 | chains with that v11(A₀) exist but none has that (m,n) |
| NOT-ELIMINATED-BY-MY-RERUN | **0** | — |

No pair is left undecided, and no pair arises that GGHV does not list. The four
distinct nodes behind those six orientations:

| deg pair | A0 | chain | final corner | (m,n) | GGHV node | class |
|---|---|---|---|---|---|---|
| (108,72) | (8,28) | — | (11⁄4, 7) | (3,2) | **left open by GGHV itself** | OPEN-IN-SOURCE |
| (72,108) | (9,27) | (9,24) | (11⁄3, 8) | (2,3) | GGHV §5 | NOT-RE-DERIVED-HERE |
| (80,112) | (4,12) | — | (7⁄4, 3) | (5,7) | "[4, §3.5]" | EXTERNAL-NOT-RE-DERIVED |
| (120,80) | (8,32) | (8,28) | (11⁄4, 7) | (3,2) | GGHV §3 | RE-DERIVED-KEY-STEP |

**Discrepancies** (full text in `gghv_audit/DISCREPANCIES.md`): two extra
length-1 chains and four extra length-2 chains that [5]'s printed tables omit —
each traced to the exact step where the divergence happens, and each shown to
produce **no degree pair** (the extras have I(A) = ∅, or duplicate an existing
(A1, A2) with a different A'_0). [5] §5's sentence "2 admissible complete chains
of length 2" is inconsistent with its own table of seven. And one sensitivity
finding: the ϑ-filter of Algorithm 1 is load-bearing for the (6,3)/(8,4)
exclusions but not for the 34-case count, while the `v_{ρ,σ}(a,b) ≥ ρ` filter is
redundant at xmax = 60.

**One kill in the window rests on a source this audit cannot open:** (80,112) is
discarded by GGHV citing only "[4, §3.5]" (Pro Mathematica 27, 2013, not on
arXiv). GGHV gives no argument of its own for that row.

**Extension.** The same implementation, run to M = 100, gives the complete list
of **474** possible counterexamples with max ≤ 300 (one orientation),
`gghv_audit/all_cases_max_le_300.json` — a superset of the campaign's own 34,
independently derived.

## T2 — the same-sign sector

Give x weight a and y weight b. `[P,Q]` is weighted-homogeneous of degree
dP + dQ − a − b, so a nonzero constant bracket forces **dP + dQ = a + b**. That
identity is *checked on every off-shell cell*, not assumed: the constant
coefficient of `[P,Q]` is identically zero whenever dP + dQ ≠ a + b. With
a + b ≤ 12 that leaves 230 cells, each swept with its full monomial basis and
decomposed exactly. Every one of the 378 Keller branches found is an
automorphism, certified two ways per branch (explicit inverse over K(s,t),
verified in both directions, and a generic-fibre count by resultant elimination).

Controls: the sweep's Keller test accepts (x, y+x³) and rejects (x, x·y) and
((3x+y)², 3x+y); its automorphism test accepts (x, y+x³) and (x+2y, y) and
rejects (x²−y², x·y), whose generic fibre it measures at 4.

## T3 — the symmetry slices

Under `P(ζ^a x, ζ^b y) = ζ^p P`, `Q(ζ^a x, ζ^b y) = ζ^q Q`, differentiating gives
`[P,Q](ζ^a x, ζ^b y) = ζ^(p+q−a−b) [P,Q]`, and the case-(2) system's bracket
right-hand side is x² (the JSON's own `bracket_rhs`), so the compatibility
condition in these reduced coordinates is **p + q ≡ 3a + b (mod n)**, not the
brief's `p + q ≡ 1 + b` (which is the condition for a constant bracket). Both
are enumerated and labelled in `symslice_results.json` rather than one being
assumed away.

**Scope.** These are the reduced coordinates of the case-(8,28) polygon pair —
the object `trackA_system_case2.json` encodes after GGHV §4's size reduction —
not (72,108) directly, so a symmetry invisible after that reduction is outside
what this territory tests. The count 1140 is every faithful (a,b) with
gcd(a,b,n) = 1 times every (p,q): 12 + 72 + 192 + 864 for n = 2, 3, 4, 6.

Every faithful cell is killed by a mechanically detected degeneracy — a polygon
vertex coefficient that the ansatz sets to zero, or the x² equation reducing to
"−1 = 0". The n = 1 control keeps all 72 variables and all 92 equations, so the
screen is not vacuous, and the largest surviving cell for each n is confirmed
EMPTY on msolve at three compliant primes with a contradictory-pin control.

## T5 — the Gao maps

Both dimension-3 members are re-expanded and agree with the paper's own recipe
run at deg p = 2 and 3. det J is −2 and 2 exactly, component degrees (7,6,4) and
(4,11,12) exactly. The weight finder recovers (1,−1,−2) without being told, the
invariant ring is (xy, x²z), and the descent content exponent comes out **2** by
both routes — `k = deg p₁ + deg p₂ − 3` and the exponent of the non-constant
factor of det J of the explicitly constructed descent. A weight class where the
two must give something else (k = 0, weights (1,−1,0)) is run as a negative
control and both routes return 0 there.

A **new** exact non-injectivity witness was found for the §3.5 map, which the
paper does not print: `(−3/2, 2/3, 8/3)` and `(0, −2/3, −4)` both map to
`(0, −4/3, 0)`.

Dimension > 3 members (F4, F5, F6, F7) are recorded with degrees, det J,
geometric degree and direction field, and skipped, per the brief.
