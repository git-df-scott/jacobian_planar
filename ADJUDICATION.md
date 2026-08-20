# ADJUDICATION — the night's three reports, refereed

Branch `claude/opus-5-counterexample-plan-sep6yk`. Everything below is produced by
`wave3/run_all.sh` (5 python certifiers + 1 PARI/GP cross-check, 110 checks, all pass,
0 can't-fail checks in tree). Two toolchains, no shared code.

**Headline: two of the three reports contain a refuted claim, one of them is mine — and
the one number that was missing has now been computed. `D_ode(Second Framework) = 69/5`.
The Second Framework is DEAD outright.**

---

## Task 1 — Provenance

`git fetch origin` brings back **12 branches**. The audit turns on one fact:

```
git merge-base origin/claude/opus-errors-false-proofs-820rmd  61fbde3  ->  c72e7e4  (main)
git merge-base origin/claude/jacobian-conjecture-search-om7slv 61fbde3  ->  c72e7e4  (main)
```

**Neither the errors branch nor my branch descends from the recon snapshot.** Both fork
from `main`, which carries only the five archive documents. Only
`claude/plane-counterexample-endgame-az3geq` (and the two `opus-support-*` branches)
contains `campaign/`, `wave0/`, `wave1/`, `STATUS.md`, `MANIFEST.md`.

### Provenance table

| report | branch | head | commits since `61fbde3` | files touched | STATUS/MANIFEST writes |
|---|---|---|---|---|---|
| **R1** STATUS.md §0–§2 ("H1c PROVED-exact", THEOREM 2/3) | `plane-counterexample-endgame-az3geq` | `2815abb` | 7 | `STATUS.md`, `wave1/RECOVERED_THEOREMS.md`, `w1_h1c_endgame_closed_form.py`, `w1_h1c_polefix.py`, `w1_mapdeg_question.py`, `w1_theorem3_verdict.py`, `wave2/*`, `campaign/audit_tracks/*` | **3 commits** — `b08fb76`, `443ef2b`, `000da9c` |
| **R2** `WAVE2_FINDINGS.md` | `opus-errors-false-proofs-820rmd` | `55417d0` | forked from `main`, 4 commits | `wave2/*`, `STATUS_CORRECTION.md` | 0 (writes `STATUS_CORRECTION.md`, not `STATUS.md`) |
| **R3** `WAVE3_FINDINGS.md` | same branch, later commits | `55417d0` | — | `wave3/*` | 0 |
| **R4** `TRUST_MAP.md` / `L4_ENDGAME_REPORT.md` (PR #8, mine) | `jacobian-conjecture-search-om7slv` | `721aad6` | forked from `main`, 3 commits | `certifiers/*`, 4 md files | 0 |

R2 and R3 are the **same session superseding itself**, not two conflicting sessions.
R1 is the only report that edited the shared record; it is also the only one that could,
since it is the only branch that has it.

### The "ABSENT" claim (mine) — adjudicated mechanically

`TRUST_MAP.md` states sessions 19–38 and seven named systems are *"not in this repository
in any form, checked against the full git object list."* `git ls-tree` on both trees:

| artifact | on `main` (what R4 ran against) | on `az3geq` |
|---|---|---|
| sessions 19–38 material | 0 paths | **65 paths** (`campaign/mod3_828/session19_*`, `moduli_phase2/.../session19..38_*`) |
| H1c | 0 | 4 (`wave0/w0_h1c_borisov_belyi.py`, `wave1/H1C_VERDICT.md`, …) |
| the eliminant | 0 | 3 — `wave1/edgeQ_eliminant.txt` is **5,759,664 bytes** |
| pentagon exports | 0 | 6 — `wave1/pent_L23.ms` is **43,158,481 bytes** |
| case (2) | 0 | `campaign/audit_tracks/CASE2_STATUS.md` |
| above-125 / 167 targets | 0 | `campaign/audit_tracks/ABOVE_125_STATUS.md` |

**Verdict: R4's ABSENT finding is REFUTED.** It was true of the object set my session had
(`main` + my own commits) and false of the campaign. The sentence *"not in this repository
in any form"* over-claimed: the check was run against a tree that had never fetched the
work. **The correct label is `NOT-FETCHED`, not `ABSENT`, and every downstream "blocked
here" in `TRUST_MAP.md` §4 and `LIVE_MAP.md` §1–§3 inherits that error.**

---

## Task 2 — The linchpin: the endgame ODE

`wave3/w3_odequation_adjudication.py` — my own rank/consistency solver over ℚ(c), no line
reused. Grid `D = 1…30`, `k = 0…6`, 210 cells. Poles at `v = 0` allowed and **never
needed** (checked, not assumed).

| claim | source | violated cells | verdict |
|---|---|---|---|
| **[A]** solution of degree ≥ 1 exists **iff `k = 0` and `3 \| D`** | R1, STATUS §2.1, tagged `[PROVED-exact]` | **159 / 210** | **REFUTED** |
| **[B]** solution exists **iff `D ∉ {3,6,…,3k}`** | R2, THEOREM W2-1 | **0 / 210** | **CONFIRMED** |
| **[C]** `3∤D` unique deg `k`; `3\|D, D/3≤k` none; `3\|D, D/3>k` line | R3 (W3-1) and R4 (E2) | **0 / 210** | **CONFIRMED** |

Minimised witness against [A], the smallest cell with `k ≥ 1`:

```
D = 1, k = 1 :   R = c(3v+2) / (2(v+1))       T(R) + c = 0   exactly
```

R1's own §2.1 justification — *"for `k ≥ 1` evaluate at `v = −1`"* — is the identical
quantifier error the campaign has now made three times. Its certifier
`w1_h1c_endgame_closed_form.py:89` reads `check("k >= 1 forces c = 0...", True, ...)`.

R2's explicit seed `c₀ = (−1)^k c k! / (3∏_{i=0}^{k}(D/3−i))` also **checks out**, once you
notice it indexes the Laurent expansion in `U = v+1`, not the numerator: 7/7 cells.

Six cells re-run in PARI/GP (`w3_pari_crosscheck.gp`, 10/10): `(13,4)`, `(23,4)`, `(12,4)`,
`(15,4)`, `(1,1)`, `(13,13)` — all agree.

**Both [B] and [C] survive. [A] is dead.** Note `(13,13)` and `(23,23)` *do* have solutions
of map-degree 13 and 23 — the `k = D` cells are live, which is what makes Task 4 non-trivial.

---

## Task 3 — THEOREM 3's repair is **circular**

`wave3/w3_theorem3_repair_audit.py`, 24/24.

R1's `w1_theorem3_verdict.py` correctly finds the gap in the *recorded* proof (the fiber
count fixes the pole divisor's multiplicity, not its location; `1/(v+1)^13` satisfies every
stated premise and is not a polynomial). That part stands. **Its repair does not.**

The repair runs: `R = W~₋₅/(α⁶U⁶(U−1)⁹)`, **`deg W~₋₅ = 28`**, `gcd = U^a(U−1)^b` with
`a ≤ 6, b ≤ 9`, map-degree `= 28 − a − b = 13` ⟹ `a+b = 15` ⟹ `(a,b) = (6,9)` ⟹ polynomial.

It lists `deg W~₋₅ = 28` as *"Session 11 ledger, arithmetic from deg g = 9"*. Session 11
line 998 reads verbatim:

> **"STRATEGIC THEOREM (degree ledger): the 13-realization FORCES deg W~₋₅ = 6·deg(g) − 26 = 28"**

And `R = v³⁹W~/g⁶` makes `39 + deg W~ = 54 + 13` ⟺ `deg W~ = 28` ⟺ *R is a polynomial of
degree 13*. **The degree input is the conclusion.** The 13-realization is used to get the
input and then again to force `a+b = 15`.

Drop only that, keep everything else the repair uses — **including the `v = 0` divisibility
it calls "NOT load-bearing"** — and non-polynomial `R` survives:

```
witness B:   W~ = (U−1)^9 (U^13 + 5U^7 − 3U + 11)      deg 22, ord_0 = 0, ord_1 = 9
             R  = (U^13 + 5U^7 − 3U + 11) / U^6
             map-degree 13 · only pole v = −1 · v = 0 closed · NOT a polynomial
```

**Verdict: THEOREM 3 → `UNVERIFIED`.** R1's `CONFIRMED` label must come down, and with it
the STATUS §0 line *"THEOREM 2 certified and THEOREM 3 confirmed"*.

Dependency audit of the rest of the chain:

| link | status |
|---|---|
| `g = αU(U−1)⁸` | **PROVED** — `w1_L3_step2_pinning.py` computes `L2 = (U(U−1)⁸)²` from the chart, not assumed |
| `deg W~₋₅ = 6·deg g − 26 = 28` | **circular** — equivalent to the conclusion (above) |
| `deg R = 13` (13-realization) | framework demand, not certified in-repo; used twice |
| box bounds `a ≤ 6, b ≤ 9` | **PROVED** — multiplicities of `U⁶(U−1)⁹`, computed |
| `(a,b) = (6,9)` | follows only from the circular input |

**None of this moves (99,66).** The endgame independently gives map-degree `k = 4 ≠ 13`.
THEOREM 3 is not merely unproved — it is **not needed**.

---

## Task 4 — Second Framework: who erred, and where

`wave3/w3_second_framework_verdict.py`, 17/17.

### The two `D`s are different objects that coincide at one value of β

```
D_chain = 2γ − σ = 3β − σ                (number of vanishing blocks)
D_ode   = 3(2e+3β)/β = 18 − 6σ/β         (coefficient in the endgame operator)
D_ode − D_chain = −(β − 6)(3β − σ)/β
```

They agree **identically in σ exactly when β = 6**, and (99,66) has β = 6. So the
agreement at 13 is a property of that one framework. R1's *"`D` = deg((−2)-curve Belyi map)
is structural"* is true of `D_chain` by definition and **false of `D_ode` away from β = 6**:
`UNVERIFIED`.

### My own claim is worse — I withdraw it

`D = 15 − 12/β < 15, so D = 23 is unreachable` (R4, PR #8, THEOREM E) uses
`e = β + 1 − p` with `p = 3`. In general `D_ode = 15 + 6(1−p)/β`, and at `p = 0` that is
**16 > 15**. `p = 3` is the (99,66) chart's Keller exponent; nothing in the record proves
`p ≥ 1` for another framework. **WITHDRAWN as stated.** It was also never the load-bearing
argument, which makes stating it as the transfer theorem's headline a second error.

### What actually closes both frameworks, with no `β`, no `p`, no Belyi data

The deviation block carries `g³` and the `y₂` block carries `g²`, so with
`ε := ord_{U=0}(g)` the Keller block carries `U^{5ε−1}` — machine-verified for `ε = 0…7`
with symbolic `a, b, e, β`. Hence

```
k = 5ε − 1   (ε ≥ 1),      k = 0   (ε = 0)      ⟹   k ∈ {0, 4, 9, 14, 19, …}
```

so **`k ≡ 4 (mod 5)` or `k = 0`**. The realization demands map-degree `= D_chain`; the
unique-solution branch delivers map-degree `= k`; and

```
13 mod 5 = 3        23 mod 5 = 3
```

**Neither 13 nor 23 is an admissible `k`, for any `ε`.** Both frameworks die on that alone.

### The escape nobody closed

When `3 | D_ode` and `D_ode/3 > k`, the solution set is a **line** whose generic member has
map-degree `D_ode/3` — which meets the realization demand exactly when `D_ode = 3·D_chain`.

```
First  (99,66)  D_ode = 13, k = 4, D_chain = 13  ->  unique, deg 4    DEAD
First  if D_ode were 39   , k = 4, D_chain = 13  ->  line,   deg 13   WOULD SURVIVE
Second          D_ode = 23, k = 4, D_chain = 23  ->  unique, deg 4    DEAD
Second if D_ode were 69   , k = 4, D_chain = 23  ->  line,   deg 23   WOULD SURVIVE
```

(99,66) is closed because its `D_ode = 13 ≠ 39`. **The Second Framework's `D_ode` has never
been computed by anyone.**

### Verdict

* **R2 (`OPEN`) vs R3 (`DEAD`): R3 is right in direction**, and its supersession of R2 is
  legitimate — the same session correcting itself, recorded properly.
* **R1 erred** by transporting `D_chain` as if it were `D_ode`.
* **R4 (mine) erred** by dropping an `ε` from `D_ode` and calling the result
  cusp-intrinsic — see §4b, where the formula is repaired rather than restored.
* The missing number is now computed. **§4b.**

---

## Task 4b — `D_ode` for the Second Framework, computed

`wave3/w3_second_framework_Dode.py`, 31/31. **The data was on
`claude/d23-borisov-transfer-test-vpr3m6` and in `campaign/d23_borisov/` the whole
time** — the same NOT-FETCHED failure as everything else in Task 1.

`campaign/d23_borisov/d23_phase1_chart.py` (re-run: 5/5 of its own checks pass, and
re-derived by hand here) certifies for the Second Framework:

```
same chart   v = x1 x2^3 - 1,  q = x2/v^3
pole depths  val_{(-2)mf}(y1, y2) = (-15, -10)        [FF: (-9, -6)]
Keller form  J_{(q,v)} = -c q^-3 v^-6                  [identical to FF]
```

so `γ = 15`, `β = 10`, `p = 3`. Then `D_chain = 2γ − σ` (FF check: `2·9 − 5 = 13`)
gives `σ = 7`, hence `e = γ − σ = 8` — which the independent chart relation
`e = β + 1 − p = 10 + 1 − 3` reproduces exactly. Two routes, same answer.

```
D_ode = 3 ε (2e + 3β)/β          ε := ord_{U=0}(g)
SF:   3ε(16 + 30)/10 = 69ε/5             FF:  3ε(8 + 18)/6 = 13ε
```

Built from scratch symbolically at `(ε,G,N) = (1,14,69)` — not substituted into my own
formula — the SF Keller block is

```
(α⁵/2)(β/3) U⁴ v⁻⁶ [ 3v(v+1)R′ − (69/5) R ]
```

with the same construction at the FF numbers returning `13` as a control.

**`D_ode(SF) = 69/5 = 13.8`. Not 23. Not 69.** Both escape routes are shut, for every `ε`:

| `ε` | `D_ode` | `k = 5ε−1` | branch | survives realization `23`? |
|---|---|---|---|---|
| 1 | 69/5 | 4 | unique, map-degree 4 | no |
| 2 | 138/5 | 9 | unique, map-degree 9 | no |
| 3 | 207/5 | 14 | unique | no |
| 4 | 276/5 | 19 | unique | no |
| **5** | **69** | **24** | **none** — `D_ode/3 = 23 ≤ 24` | no |
| … | | | `23m ≤ 25m−1` for all `m ≥ 1` | no |

`ε` not a multiple of 5 → `D_ode` isn't an integer, so `3 ∤ D_ode`, so the solution is
unique of map-degree `5ε−1 ≡ 4 (mod 5) ≠ 23`. `ε = 5m` → `D_ode/3 = 23m ≤ 25m−1 = k`,
so **no rational solution at all**. Two disjoint mechanisms, no gap between them.

> **SECOND FRAMEWORK: `DEAD-CONDITIONAL` → `DEAD`.**

The First Framework and the Three-dessin (108,72) case have the identical structure at
`D_ode = 13ε`, `D_chain = 13`: `ε = 3` gives no solution (`13 ≤ k = 14`), every other `ε`
gives map-degree `5ε−1 ≠ 13`. **(108,72)'s residual gap `D_ode ≠ 39` is closed the same
way** — at `ε = 3`, `D_ode` *is* 39, and that cell has no solution at all.

### My withdrawn claim, repaired

The correct formula carries an `ε` I had dropped:

```
D_ode = ε · (15 − 12/β)          at p = 3.
```

At `ε = 1` that is my `15 − 12/β`, and the bound `D_ode < 15` holds **only at `ε = 1`**.
What is now certified rather than assumed is `p = 3` for **both** published frameworks
(`d23_phase1_chart.py` L1c) — the input the bound always needed. So the claim is not
restored as written; it is restored with the `ε` and with its hypothesis discharged.

### And the transfer conjecture's premise, at its sharpest

The Second Framework's chain degree is **23**; its endgame operator's coefficient is
**69/5 — not even an integer**. *"For chain degree `D` the same mechanism yields
`3v(v+1)R′ = D R`"* is false here as loudly as it can be.

Two further claims in `campaign/d23_borisov/d23_phase1_endgame.py` fall with it:

* **E3** — *"for every `k ≥ 1`: infeasible outright (evaluation at `v = −1` … an identity
  argument covering ALL `k ≥ 1`)"* — refuted by the same witness as R1 §2.1
  (`D = 1, k = 1`, verified exactly).
* **E5** — the "rigidity collapse identity" `23(15v+14) − 345(v+1) = −23`. It is an
  instance of `D((deg g)v + deg g − 1) − D·deg g·(v+1) = −D`, which holds for **every**
  `D` and every `deg g`, so it cannot determine `D`. It assumes what it appears to show.
  (Verified, with a negative control that breaks on a perturbed middle term.)

---

## Task 5 — my (108,72) closure and the "two legs"

`wave3/w3_10872_and_legs_audit.py`, 13/13.

**The two legs are one leg.** `R = v³⁹W~/g⁶` with `deg g = 9` gives
`map-degree(R) = max(deg W~, 15) − a − b`. So `deg W~ = 28 ⟺ map-degree 13` and
`deg W~ = 15 ⟺ map-degree 4` (recomputed from the actual solution: `deg W~ = 15`,
`ord_0 = 2`, `ord_1 = 9`, map-degree 4). Presenting *"deg W~ = 15 vs 28"* and
*"map-degree 4 vs 13"* as two independent closures **overstates the evidence**. The genuine
second leg is E4's ladder pole bound, which E4 itself labels genericity-conditional.

**The nine charts are not proved exhaustive.** The enumeration assumes both bidegrees are
integer multiples of one primitive edge vector — verified at (99,66)
(`(27,72) = 9(3,8)`, `(18,48) = 6(3,8)`), **assumed** at (108,72). Explicit witness outside
the enumeration: bidegrees `(40,68)` and `(30,42)` sum to `(108,72)` and are not
proportional. Label: **CONDITIONAL, not exhaustive.**

**(108,72) still closes** — on `k ≡ 4 (mod 5)` alone, with no chart enumeration, no `β`,
no `p`, and no `D = 15 − 12/β`. Same residual gap as the Second Framework: `D_ode ≠ 39`.

**Can't-fail scan of my own tree:** the scanner (self-tested) found **4** — three in my
PR #8 certifiers (`E2:100`, `E5:144`, `E5:146`) and one in my own new script. All four are
now replaced with computed conditions; `E2` 25/25 and `E5` 27/27 still pass. **Current
count: 0.**

---

## Claim ledger

| # | claim | report | verdict | artifact |
|---|---|---|---|---|
| 1 | endgame solvable iff `k=0 ∧ 3\|D` | R1 §2.1 `[PROVED-exact]` | **REFUTED** (159/210) | `w3_odequation_adjudication.py` |
| 2 | solvable iff `D ∉ {3,…,3k}` | R2 W2-1 | **VERIFIED-HERE** | same |
| 3 | unique/none/line trichotomy, degree `k` | R3 W3-1, R4 E2 | **VERIFIED-HERE** | same + PARI |
| 4 | R2's seed formula | R2 W2-1 | **VERIFIED-HERE** | same |
| 5 | THEOREM 3's recorded proof has a gap | R1 | **VERIFIED-HERE** | `w3_theorem3_repair_audit.py` |
| 6 | THEOREM 3 CONFIRMED by the repair | R1 | **REFUTED** (circular; witness B) | same |
| 7 | `g = αU(U−1)⁸` (THEOREM 2) | R1 | **VERIFIED-HERE** (computed, not assumed) | `w1_L3_step2_pinning.py`, re-read |
| 8 | `D = deg((−2)-Belyi)` is structural | R1 §2.2 | **UNVERIFIED** (true of `D_chain`, false of `D_ode`) | `w3_second_framework_verdict.py` |
| 9 | `D = 15 − 12/β < 15`, so `D=23` unreachable | R4 | **REPAIRED** → `D_ode = ε(15 − 12/β)`; `p = 3` now certified for both frameworks | `w3_second_framework_Dode.py` |
| 10 | Second Framework OPEN | R2 | superseded | — |
| 11 | Second Framework DEAD | R3 | **VERIFIED-HERE** — `D_ode = 69/5`; dead for every `ε` | `w3_second_framework_Dode.py` |
| 11a | `D_ode(SF) = 69ε/5`, `γ=15, β=10, σ=7, e=8` | new here | **VERIFIED-HERE** (two independent routes to `e`) | same |
| 11b | d23 `E3` (`v=−1` covers all `k≥1`) | `d23_phase1_endgame.py` | **REFUTED** | same |
| 11c | d23 `E5` collapse identity determines `D` | `d23_phase1_endgame.py` | **REFUTED** — holds for every `D` | same |
| 12 | `k = 5ε − 1`, so `k ≡ 4 (mod 5)` | new here | **VERIFIED-HERE** | same |
| 13 | (99,66) empty | R1, R3, R4 | **VERIFIED-HERE** — via map-degree `4 ≠ 13`, needing neither THEOREM 3 nor `D_ode` | `w3_odequation_adjudication.py` |
| 14 | (108,72) closes over nine exhaustive charts, two legs | R4 | **REFUTED as stated**; closes on `k ≡ 4 (mod 5)`, and its `D_ode ≠ 39` gap is closed at §4b | `w3_10872_and_legs_audit.py`, `w3_second_framework_Dode.py` |
| 15 | sessions 19–38 etc. ABSENT | R4 | **REFUTED** — `NOT-FETCHED`; 65 paths + a 43 MB export exist on `az3geq` | Task 1 |

---

## What I have not touched

PR #6's body is R1's; **I have not edited it.** Claims 1, 6 and 8 above are the ones a
reader of that PR would take away and which this adjudication refutes — flagged for you,
not acted on.

## The board

**Live, and now actually reachable** (the artifacts exist, they were never fetched):
`wave1/edgeQ_eliminant.txt` (5.7 MB), `wave1/pent_L23.ms` (43 MB, `.out` is 0 bytes — the
run never produced output), `campaign/audit_tracks/CASE2_STATUS.md`,
`ABOVE_125_STATUS.md`, and 65 session-19–38 paths.

**The framework route is closed.** `D_ode(SF) = 69/5` was the last number, and it kills
the Second Framework for every `ε`; the same computation closes (108,72)'s residual gap.
First Framework, Second Framework, Three-dessin (108,72), and the isotope series all die,
and none of it needs THEOREM 3, the Belyi coefficients, or the `v = −1` evaluation.

Reproduce: `./wave3/run_all.sh`
