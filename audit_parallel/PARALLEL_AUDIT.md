# PARALLEL_AUDIT — soundness audit of the parallel Opus session's wave3 claims

Auditor: independent session, branch `claude/opus-5-counterexample-plan-sep6yk` (HEAD `e0c0fdb`).
Scope: `wave3/ADJUDICATION_PARALLEL_OPUS.md` and the certifiers it cites, plus
`certifiers/new/E2_endgame_classification.py`, `E5_propagate_tower.py`, `EC_10872_instantiation.py`.
Nothing outside `audit_parallel/` was edited. No msolve, no Singular. All re-runs are `python3` /
`gp` on existing files, plus four probe scripts written for this audit (contents reproduced inline).

---

## 0. Re-run log (b)

Every certifier reproduces its advertised count. Exit codes are as designed
(`raise SystemExit(1 if bad else 0)` / `assert`).

| file | exit | checks |
|---|---|---|
| `wave3/w3_odequation_adjudication.py` | 0 | 15/15 |
| `wave3/w3_second_framework_Dode.py` | 0 | 31/31 |
| `wave3/w3_second_framework_verdict.py` | 0 | 17/17 |
| `wave3/w3_10872_and_legs_audit.py` | 0 | 13/13 |
| `wave3/w3_theorem3_repair_audit.py` | 0 | 24/24 |
| `wave3/w3_pari_crosscheck.gp` | 0 | PASS 10, FAIL 0 |
| `certifiers/new/E2_endgame_classification.py` | 0 | 25/25 |
| `certifiers/new/E5_propagate_tower.py` | 0 | 27/27 |
| `certifiers/new/EC_10872_instantiation.py` | 0 | 19/19 |

100 python + 10 PARI = the advertised **110 checks, all pass**. That part of the headline is
accurate. The rest of this document is about what the 110 checks are checks *of*.

---

## 1. The headline that is false on inspection: "0 can't-fail checks in tree"

`ADJUDICATION_PARALLEL_OPUS.md:5` claims "110 checks, all pass, **0 can't-fail checks in tree**",
and §Task 5 claims "Current count: **0**" after four replacements.

The scanner backing that claim is `wave3/w3_10872_and_legs_audit.py:50-61`. It flags a check only
when the condition is a literal `ast.Constant` equal to `True`/`1`, or a `BoolOp(Or)` containing
literal `True`. That is a very narrow detector: it does not fire on `True is not False`
(a `Compare`), on `True if x is not None else False` (an `IfExp`), or on any arithmetic over
literals such as `6*9 - 26 == 28`.

I re-ran the scan with a stricter, still-mechanical rule — *a check whose condition contains no
`Name`, `Call`, `Attribute`, `Subscript` or comprehension node, i.e. is fully determined at parse
time* (`scratchpad/scan.py`, reproduced in §7). Over `wave3/*.py` + `certifiers/new/*.py`:

```
total check()/chk()/rec() calls scanned : 260
parse-time-constant conditions         : 22
```

Six of the 22 are inside the parallel session's own new wave3 files:

| site | condition | label it stands in for |
|---|---|---|
| `w3_10872_and_legs_audit.py:72` | `True if findings is not None else False` | "scan completed over my own tree" |
| `w3_10872_and_legs_audit.py:107` | `(27,72)==(9*3,9*8) and (18,48)==(6*3,6*8)` | the (99,66) read-off |
| `w3_10872_and_legs_audit.py:110` | `True is not False` | **"HYPOTHESIS H-PROP … ASSUMED at (108,72)"** |
| `w3_10872_and_legs_audit.py:125` | `13 % 5 == 3` | **"(108,72) Three-dessin chain degree is 13"** |
| `w3_second_framework_Dode.py:88` | `9-5 == 4 == 6+1-3` | "FF cross-check: both routes give e = 4" |
| `w3_theorem3_repair_audit.py:69,71,89,133` | `39+28==6*9+13`, `6*9-26==28`, `28-2-0!=13`, `13>6` | ledger arithmetic |

and sixteen more in `certifiers/new/` (`E4:157,158,159`, `E5:69`, `E6:121,122,133`,
`EC:43,44,45,47,53,101`). Note `E5:69` — `chk("Session-11 ledger … deg W~_-5 = 28", 6*9-26 == 28)` —
is exactly the kind of check the adjudication's Task 3 correctly convicts as *circular*, still live
in the tree the same document declares clean.

Two further can't-fail sites that even my stricter scanner misses because they read module-level
literals: `E5_propagate_tower.py:156` — `chk("R = 0 means W~_-5 = 0, contradicting the framework's
13 chain vanishings", sp.simplify(alpha**6*U**6*(U-1)**9*sp.Integer(0)) == 0)` — the condition is
`0 == 0`, and the label it certifies is unrelated to it; and in
`w3_second_framework_Dode.py` the whole of sections 1–2 (lines 71–88, plus 114 and 117), where the
conditions are arithmetic on constants assigned two lines above (see §3).

**Finding A. "0 can't-fail checks in tree" is false under any definition broad enough to be
meaningful, and the two checks standing in for the load-bearing hypotheses of the (108,72) closure
(`:110`, `:125`) are themselves in the list.** The self-scan passed because the detector was
narrower than the phenomenon.

---

## 2. CLAIM 1 — "(108,72) closed with the THEOREM 2 dependence removed"

Sources: `ADJUDICATION_PARALLEL_OPUS.md` Task 5 and §4b (lines 298–322, 262–265);
`wave3/w3_10872_and_legs_audit.py` (13/13); `certifiers/new/EC_10872_instantiation.py` (19/19);
`E5_propagate_tower.py` (27/27).

### (a) Line-by-line: constants, prose inputs, unverified dependencies

`w3_10872_and_legs_audit.py`:

* `:45` globs `certifiers/new/*.py` and `wave3/*.py` with **relative** paths — the file silently
  scans nothing if run from anywhere but the repo root. Not a soundness bug, a reproducibility one.
* `:71` scanner self-test — genuine.
* `:72-73` `rec(..., True if findings is not None else False)` — **can't-fail**.
* `:81-83` `legs()` arithmetic — genuine and correct; the leg-equivalence finding (that
  "deg W~ = 15 vs 28" and "map-degree 4 vs 13" are one statement) is right, and is a real
  self-correction of the parallel session's own PR #8.
* `:85-96` recomputes deg W~ = 15, ord₀ = 2, ord₁ = 9, map-degree 4 from the explicit endgame
  solution — genuine computation, reproduced.
* `:106-108` nine divisors of 36, and the (99,66) read-off — arithmetic on literals, true.
* `:110-111` **`rec("HYPOTHESIS H-PROP: both bidegrees are integer multiples of one primitive
  (a,b). Verified at (99,66); ASSUMED at (108,72)", True is not False)`** — the load-bearing
  exhaustiveness hypothesis of the nine-chart enumeration is entered into the pass count as a
  tautology. The label is honest ("ASSUMED"); the mechanism is not.
* `:114-117` the non-proportional witness (40,68)/(30,42) — genuine, and the conclusion
  "CONDITIONAL, not exhaustive" is correct and is a real finding against the session's own PR #8.
* `:123-128` **`rec("(108,72) Three-dessin chain degree is 13 (az3geq STATUS 2.2 table)",
  13 % 5 == 3)`** — the label asserts the chain degree of (108,72); the condition tests a modular
  arithmetic fact about the literal 13. The chain degree 13 for (108,72) is **prose, taken from a
  STATUS table on another branch, never computed anywhere in this tree.** It is the single input on
  which the entire "closes on k ≡ 4 (mod 5)" argument turns.

`EC_10872_instantiation.py`: `:43,44,45,47,53,101` are all parse-time constants; `:53` certifies
that **(108,72) cannot reuse the (99,66) edge vector** (11 ∤ 108). The per-chart verdicts use
`D_of(beta,p=3) = (15β−6p+6)/β = 15 − 12/β`, i.e. the ε-free formula that
`w3_second_framework_verdict.py` withdraws; the audit file notes this (`:25-29` of its docstring),
correctly.

Unverified dependencies inherited: (i) the E2/W3-1 trichotomy (empirical, see §4); (ii)
"the realization layer demands map-degree equal to the chain degree" — prose in every file that
uses it; (iii) `k = 5ε − 1`, which rests on the assumed block shapes (deviation block carries `g³`,
`y₂` block carries `g²`) transported to (108,72) without derivation; (iv) for the §4b gap closure,
`D_ode(108,72) = 13ε`, which is asserted, never derived for (108,72).

### (c) PROVES vs ASSERTS

**Proves** (recomputed by me, independently):
1. `max(deg W~,15) − a − b` reproduces both "legs"; they are one leg. Correct.
2. From the explicit (99,66) endgame solution: deg W~ = 15, ord₀ = 2, ord₁ = 9, map-degree 4.
3. The nine-chart list is `s | 36`, and the enumeration is not exhaustive without H-PROP; the
   witness (40,68)+(30,42) is genuinely outside it.
4. `EC`: for each of the nine charts, the endgame equation has either no rational solution or a
   unique one of map-degree 4 (all nine verified by explicit substitution).
5. `k = 5ε−1` for ε = 0…7 as an algebraic identity of the assumed block shapes
   (`w3_second_framework_verdict.py:93-109`) — I re-derived this with `a,b,e,β` symbolic and it is
   a theorem of those shapes, not a coincidence.

**Asserts**:
1. (108,72)'s Three-dessin chain degree is 13.
2. The realization layer demands map-degree = chain degree.
3. H-PROP (nine-chart exhaustiveness) — flagged by the file itself.
4. That (108,72) has the First Framework's block structure at all (`g³`/`g²`, ε = ord_{U=0}(g)),
   despite `EC:53` certifying that its chart is *not* the (99,66) chart.
5. `D_ode(108,72) = 13ε` — the input that closes the ε = 3 residual gap (§4b, lines 262-265).

### Is the THEOREM 2 dependence actually removed?

Partly, and less than advertised.

* **Yes** for the `k ≡ 4 (mod 5)` leg: `ε := ord_{U=0}(g)` is carried free, so `g = αU(U−1)⁸`
  (THEOREM 2) is not used. That is a real improvement over `E5`, whose closure 2 uses `deg g = 9`
  at `E5:68-71`.
* **No** for the residual-gap leg. Closing "D_ode ≠ 39" at ε = 3 requires `D_ode(108,72) = 13ε`,
  i.e. `β = 6, e = 4, p = 3` — the (99,66) chart data. The certifier does not derive them, and
  `EC:53` says (108,72) does not share (99,66)'s edge vector. Substituting one chart-transport
  assumption for another is not removal.
* I checked whether the missing derivation is *recoverable*: under the framework's own relations
  (`γ = 3β/2`, `e = β+1−p`, `p = 3`, `D_chain = 2γ−σ`, `e = γ−σ`) one gets
  `D_chain = γ + e = 5β/2 − 2`, so `D_chain = 13 ⟹ β = 6 ⟹ D_ode = 13ε`. So the assertion is
  **reconstructible but not certified**; the reconstruction is nowhere in the tree, and it silently
  singles out the s = 12 chart out of the nine.

### (e) VERDICT — Claim 1: **SOUND-BUT-OVERSTATED**

The conclusion "(108,72) closes" survives, and the two genuine self-corrections in the file (one
leg not two; nine charts conditional not exhaustive) are correct and creditable. But:

* the two hypotheses the closure actually rests on are recorded as passing checks that cannot
  fail — **`wave3/w3_10872_and_legs_audit.py:110`** (H-PROP) and
  **`wave3/w3_10872_and_legs_audit.py:125`** (chain degree 13);
* "the THEOREM 2 dependence removed" is true of one leg and false of the other:
  **`ADJUDICATION_PARALLEL_OPUS.md:262-265`** closes the residual gap on `D_ode(108,72) = 13ε`,
  which is (99,66) chart data asserted for a chart `EC:53` certifies is different.

Nearest thing to an unsound step, stated precisely:
`ADJUDICATION_PARALLEL_OPUS.md:262-265` — asserted input, not derived, and in tension with
`certifiers/new/EC_10872_instantiation.py:53`.

---

## 3. CLAIM 2 — "Second Framework: D_ode = 69/5, it dies outright"

Source: `wave3/w3_second_framework_Dode.py` (31/31), `w3_second_framework_verdict.py` (17/17),
`ADJUDICATION_PARALLEL_OPUS.md` §4 / §4b.

### (a) Line-by-line

Sections 1–2 (`:57-88`, 11 of the 31 checks) contain **no computation from data**. `GAM, BET, PP =
15, 10, 3` are hard-coded at `:71`; every subsequent check in those sections is arithmetic on those
literals:

| line | condition | status |
|---|---|---|
| `:63,:67,:69` | chart inversion, `det = −x2³/v³`, `= −q³v⁶ ⟹ p = 3` | **genuine sympy computation** — this is the only part of §1 that computes anything, and it does establish `p = 3` |
| `:72` | `(GAM,BET) == (15,10)` with `GAM,BET = 15,10` at `:71` | **tautology**; the label ("SF pole depths give gamma = 15, beta = 10") is the prose input |
| `:75` | `Rational(3*BET,2) == GAM` | constants; a real consistency test of two prose numbers, but parse-time determined |
| `:80` | `Dchain(9,5) == 13` | constants |
| `:82` | `SIG == 7` where `SIG = 2*GAM - 23` | constants; **the 23 is prose** (the SF's chain degree) |
| `:84,:85,:87` | `e = γ−σ = 8`, `e = β+1−p = 8`, "the two routes agree" | constants; the agreement `23−15 = 10+1−3` is a genuine numerical coincidence among four prose inputs, and is the strongest single piece of corroboration in the file |
| `:88` | `9-5 == 4 == 6+1-3` | pure literals — flagged by my scanner |
| `:96,:97,:98,:100,:102` | `D_ode(SF) = 69ε/5`, `D_ode(FF) = 13ε`, etc. | sympy, but they re-evaluate the file's **own** one-line formula `D_ode(e,b) = 3ε(2e+3b)/b` at the hard-coded numbers. They confirm arithmetic, not the formula |
| `:114` | "collapse condition N = (2e+3β)(ε+G)/β gives N = 69 at (ε,G) = (1,14)" | `NV = 69` is assigned at `:112` with the comment *"N from collapse"*. **The value is defined by the condition it is then checked against** |
| `:117` | `a = 2G−3β = −2`, `b = 3G+3e−N = −3`, `a+b−1 = −6 = −τ` | constants |
| `:124` | SF block `== (α⁵/2)(β/3)U⁴v⁻⁶[3v(v+1)R′ − (69/5)R]` | **genuine symbolic derivation** at that one instance |
| `:131` | FF control returns 13 | **genuine**, and a real negative control |
| `:153-163`, `:171-174` | the per-ε table | computed, but from the file's own `verdict()` encoding of the trichotomy (see §4) |
| `:182,:187,:189,:192` | refutations of d23 `E3` and `E5`, with a NEG control | **genuine and correct** — I reproduced both. `E5`'s "collapse identity" really does hold for every `D`, and `E3`'s `v = −1` argument really is refuted by `D=1,k=1` |

Provenance of the only numerical inputs: the docstring (`:8-9`) says γ = 15, β = 10 are
"certified by `campaign/d23_borisov/d23_phase1_chart.py` (re-run here by hand, 5/5 of its own
checks pass)". I read that file. It certifies **only** the chart algebra (L1a inversion, L1b
monomial rule, L1c Jacobian factor); the pole depths appear at `d23_phase1_chart.py:21-22` as
narrative — *"certified boundary data, C6/C7"* — a pointer, not a computation, and C6/C7 are not
in this tree. The file also has **four** boolean checks, no pass counter, and no nonzero exit path:
"5/5 of its own checks pass" is not a statement that file can support.

**So: `γ = 15, β = 10` — the sole framework-specific inputs to 69/5 — are prose in every file in
the chain.** `p = 3` is genuinely computed. `σ = 7` and `e = 8` are computed *from* the prose
inputs plus the prose `D_chain = 23`.

### (d) What is `D_ode`, where does 69/5 come from, is the fraction a unit error?

**Definition actually used.** The Keller block is `e·δ·η′ + β·δ′·η` with
`η = α²U^{2ε}v^a`, `δ = ½α³U^{3ε}Rv^b`, `U = v+1`. I re-derived this symbolically with
`a, b, e, β` all free (probe 3, §7): the block equals

```
(α⁵/2) U^{5ε−1} v^{a+b−1} [ β v(v+1) R′ + ε(2e+3β) v R + (ea+βb) U R ].
```

The `R`-coefficient is constant iff **`ea + βb = −ε(2e+3β)`** (the "collapse"), and then the
bracket is `β·v(v+1)R′ − ε(2e+3β)R`. Forcing the derivative term into the First Framework's
normalisation `3v(v+1)R′` pulls out `β/3` and *defines*

```
D_ode := 3λ,        λ := ε(2e+3β)/β.
```

I verified the collapse identity holds for ε = 1…6 with `a,b,e,β` symbolic — so the formula is a
theorem of the assumed block shapes, not an instance fit. (It also means the `(ε,G,N) = (1,14,69)`
"built from scratch" check at `:112-126` adds nothing beyond one instance: `G` enters only through
`a,b`, which are free in the general identity. `G = 14` is in fact forced by `a+b−1 = −τ = −6`
together with `a = 2G−3β`, so it is not arbitrary; the file just does not show that.)

**Where 69/5 comes from.** Substituting `e = γ−σ` and `γ = 3β/2` gives `2e + 3β = 2D_chain`, hence
the clean form the certifiers never state:

```
D_ode = 6 ε D_chain / β .
```

FF: `6·13/6 = 13`. SF: `6·23/10 = 69/5`. So the entire content of "69/5 ≠ 23" is the single
inequality `β ≠ 6ε` — i.e. the SF's pole depth β = 10 differs from the FF's 6. Everything else is
bookkeeping.

**Is the fraction a unit/convention error?** No — but it carries far less rhetorical weight than
the adjudication gives it (`ADJUDICATION:245`, `:280-284`, "not even an integer … false as loudly
as it can be").

* `D_ode` is not a count of anything. It is `3×` the Euler exponent `λ` of the homogeneous solution
  `R = C(v/(v+1))^λ`. Nothing in its definition forces `λ ∈ ℤ` or `3λ ∈ ℤ`. Fractional values are
  structurally admissible.
* The factor `3` is **inherited from the First Framework**, where `β/3 = 2` absorbs cleanly. The
  convention-free invariant is `λ = ε(2e+3β)/β = 2εD_chain/β` (SF: 23/5; FF: 13/3). All the
  classification depends on is `λ ∈ ℤ` or not.
* Decisive against the rhetoric: **this lineage's own earlier certifier already produced fractional
  `D_ode` routinely.** `EC_10872_instantiation.py` prints, for seven of the nine (108,72) charts,
  `D = 89/6, 44/3, 29/2, 43/3, 27/2` and handles them with the same non-integer branch. A
  fractional `D_ode` was normal in this framework three files ago; the "not even an integer" flourish
  presents the generic case as an anomaly.

So: consistent with the definition, **not** a unit error — but also not the sharp kill it is sold
as. The sharp statement is `λ ∉ ℤ`, and that only ever meant "β ∤ 2εD_chain".

### The definition of `D_ode` is not stable across the suite

* `w3_second_framework_verdict.py:60` — `D_ode = 3(2(γ−σ)+3β)/β`, **no ε**.
* `w3_second_framework_Dode.py:93` — `D_ode = 3ε(2e+3β)/β`, **with ε**.

Both files are in the same suite, same commit pair (`aa5ad56`, `be027ec`), and
`ADJUDICATION_PARALLEL_OPUS.md` quotes both (§4 line 150 without ε, §4b line 232 with ε) without
reconciling them. The consequence is a false check: `w3_second_framework_verdict.py:66-70` certifies
that `D_ode` and `D_chain` "agree identically in σ **exactly when β = 6** … and at no other beta",
testing β ∈ {2,3,4,5,7,8,12}. Under the ε-carrying definition established by the *same file's*
§3 (which proves ε is free), they agree whenever **β = 6ε**, e.g. (ε,β) = (2,12) — one of the very
values the check tests as a negative. The check passes only because ε was silently 1.

**This is the third distinct form of the kill in this lineage** — `D = 15 − 12/β` (PR #8),
`D_ode = 18 − 6σ/β` (verdict.py), `D_ode = 69ε/5` (Dode.py) — and the second and third are not the
same function of the framework data.

### The trichotomy is applied entirely outside the region where it was verified

`w3_odequation_adjudication.py` verifies the trichotomy on the grid **D = 1…30, k = 0…6** (210
cells, integer D). `E2` adds a grid topping out at (24,4) and (23,6). Every downstream application
in the Claim-2 argument is outside both:

| use | cell | in any verified grid? |
|---|---|---|
| SF, ε = 1 | `D = 69/5`, k = 4 | no — **D not an integer** |
| SF, ε = 2,3,4 | `D = 138/5, 207/5, 276/5`, k = 9,14,19 | no |
| SF, ε = 5 | `D = 69`, k = 24 | no |
| FF/(108,72), ε = 3 | `D = 39`, k = 14 | no |

`w3_second_framework_Dode.py:137-144` re-implements the trichotomy as a bare python `verdict()`
function and applies it at those cells. Nothing in the tree verifies that the classification proved
on integers ≤ 30 extends to non-integer `D` or to `k > 6`.

I closed this gap myself (probes 1 and 4, §7) — exact rank/consistency solves over ℚ(c):

```
D=69/5  k=4  : unique, map-degree 4     T(R)+c = 0 verified
D=138/5 k=9  : unique, map-degree 9     verified
D=69/5  k=9  : unique, map-degree 9     verified
D=39    k=14 : NO SOLUTION
D=39    k=13 : NO SOLUTION
D=42    k=14 : NO SOLUTION
D=69    k=24 : NO SOLUTION          (box m=24, numerator deg ≤ 28)
```

All four load-bearing cells behave as the certifier assumes. **The extrapolation is true; it was
simply never checked by the party making it.** That is a gap I have now filled, not a gap they had
filled.

### The conclusion is right, and the number 69/5 is not what makes it right

Working the framework's own relations through (probe 2, §7):

1. With `γ = 3β/2`, `e = β+1−p`, `p = 3`: `D_chain = γ + e = 5β/2 − 2`. Since β is even,
   **`D_chain ≡ 3 (mod 5)` for every framework in the class** — 13 and 23 are not special, they are
   forced. The "kill" `k ≡ 4 (mod 5) ≠ D_chain ≡ 3 (mod 5)` therefore cannot fail *for any chain
   degree whatsoever*.
2. The family-branch escape (`3 | D_ode` and `D_ode/3 > k`) is closed **universally**:
   `D_ode/3 = 5ε − 4ε/β`, so integrality needs `β | 4ε`, which forces `4ε/β ≥ 1`, hence
   `D_ode/3 ≤ 5ε−1 = k` — the "no solution" branch. Exhaustive scan ε ≤ 59, β ≤ 398 even: zero
   cases where the escape opens.

So the Second Framework's death does **not** require γ = 15, β = 10, σ = 7, e = 8 or the number
69/5. It follows from `p = 3`, `γ = 3β/2`, `e = β+1−p`, `k = 5ε−1` and the trichotomy alone —
for every framework of this type, every chain degree, every ε.

That robustness is good news for the conclusion and bad news for the presentation. An argument that
kills an infinite class in two congruences, with no framework-specific input surviving, should be
labelled as such; instead §4b sells a specific computed number as "the last number", when the number
is decorative. It also means the "proves too much" test is now live: the entire weight rests on two
uncertified structural inputs — `k = 5ε−1` (from the assumed `g³`/`g²` block shapes) and "the
realization layer demands map-degree = chain degree". If either is wrong, nothing in §4b survives;
if both are right, every framework in the class was already dead before the SF chart data was
fetched.

### (c) PROVES vs ASSERTS — Claim 2

**Proves**:
1. `J_{(q,v)} = −c q⁻³v⁻⁶`, i.e. `p = 3`, for the SF chart (genuine sympy, and independently in
   `d23_phase1_chart.py`).
2. Given the block shapes and the collapse, `D_ode = 3ε(2e+3β)/β`; and at (e,β) = (8,10), ε = 1
   the SF block is `(α⁵/2)(β/3)U⁴v⁻⁶[3v(v+1)R′ − (69/5)R]`, with the FF control returning 13.
3. `d23_phase1_endgame.py`'s **E3** ("v = −1 covers all k ≥ 1") is refuted by the exact witness
   `D=1, k=1`.
4. `d23_phase1_endgame.py`'s **E5** "rigidity collapse identity" holds for every `D` and every
   `deg g`, so it determines nothing — with a working negative control.
5. Arithmetic: 3·(2·8+3·10)/10 = 69/5, and the per-ε table given the trichotomy.

**Asserts**:
1. `γ = 15`, `β = 10` (SF pole depths) — prose in every file; the "certified boundary data C6/C7"
   is not in this tree.
2. `D_chain(SF) = 23` — prose; `σ = 7` and `e = 8` are derived from it.
3. `e = β + 1 − p` — an unproved chart relation used as one of the "two independent routes".
4. `N = 69`, i.e. that the SF Keller block **collapses to an Euler operator at all**
   (`w3_second_framework_Dode.py:112`, "N from collapse"). If the SF's true `N` differs, the
   endgame is not of the form `T_{D,k}` and the trichotomy does not apply.
5. The trichotomy at non-integer `D` and at `k > 6` (true — I verified it — but asserted there).
6. `k = 5ε − 1` for the SF, from FF block shapes.
7. "The realization layer demands map-degree = chain degree."

### (e) VERDICT — Claim 2

Split, because the claim has two halves:

* **"The Second Framework dies": SOUND-BUT-OVERSTATED.** The conclusion holds, and holds more
  robustly than claimed — I verified it survives dropping γ = 15 and β = 10 entirely. The
  overstatement is "computed": the specific headline number rests on inputs no certifier in this
  tree computes, and the kill does not need it.
* **"`D_ode(SF) = 69/5`, computed": CANNOT-DETERMINE.** Its two framework-specific inputs
  (γ = 15, β = 10) are prose sourced to `campaign/d23_borisov/d23_phase1_chart.py:21-22`, which
  does not certify them, and whose "5/5 of its own checks pass" (`w3_second_framework_Dode.py:9`)
  is not a claim that file can support — it has four boolean prints, no counter, no failure exit.
  Nothing in this repository lets me confirm or refute 15 and 10.
* **Unsound-as-certified steps**, precisely:
  * **`wave3/w3_second_framework_Dode.py:112-115`** — `NV = 69` is assigned with the comment "N
    from collapse" and then checked against the collapse condition. The value is defined by the
    condition it is presented as satisfying. This is structurally the same circularity the same
    suite convicts THEOREM 3's repair of in Task 3 (`ADJUDICATION:99-125`).
  * **`wave3/w3_second_framework_verdict.py:66-70`** — certifies "they agree identically in σ
    exactly when β = 6 … and at no other beta"; false under the ε-carrying definition of `D_ode`
    that the same suite adopts at `w3_second_framework_Dode.py:93` (they agree whenever β = 6ε).
    The check passes only because ε is silently fixed to 1, in a file whose §3 proves ε is free.
  * **`wave3/w3_second_framework_Dode.py:71-73`** — the framework's only numerical inputs entered
    as a hard-coded tuple and then "checked" against themselves.

---

## 4. Cross-cutting findings

**F1.** The trichotomy [C]/`E2`/`W3-1` is **empirically verified, never proved**. `E2`'s docstring
states it "for arbitrary integer D ≥ 1 and m ≥ 1" and calls the case analysis "implemented as
executable checks", but §3's structural lemmas are checked at sampled values
(`E2:97` is `all((3m−D) != 0 for m in −12..−1, D in 1..39)`, true by sign for all m<0<D but tested
on a box; `E2:111` samples three poles and three orders) and §4 is a 28-point grid. Everything
downstream in both claims is an extrapolation. Verified-on-a-grid is being reported as
`VERIFIED-HERE` in the claim ledger (`ADJUDICATION:331`), which a reader will take as proved.

**F2.** `D_ode` is defined three different ways across the lineage — `15 − 12/β` (PR #8),
`18 − 6σ/β` (`verdict.py:60`), `3ε(2e+3β)/β` (`Dode.py:93`) — and the middle and last are not the
same function. The "repair" narrative (`ADJUDICATION:267-278`) presents this as recovering a dropped
ε, but the ε-free version is still live in the companion certifier and still generating a passing
check that the ε-version falsifies.

**F3.** Sole surviving quantitative content of the SF computation: `D_ode/D_chain = 6ε/β`. Neither
certifier states it in that form, which is why "69/5" reads as a discovery rather than as
"β = 10 ≠ 6".

**F4.** Two of the wave3 refutations are solid and I confirmed them independently: the d23 `E3`
witness and the d23 `E5` "collapse identity" (`ADJUDICATION:286-294`). Likewise Task 3's circularity
finding against THEOREM 3's repair, and Task 5's two self-corrections (one leg, not two; nine charts
conditional). This session's negative results against *other* sessions' work are the best-supported
material in the file. Its positive claim (69/5) is the least-supported.

**F5.** Reproducibility: `wave3/run_all.sh` `cd`s to the repo root, so the relative globs in
`w3_10872_and_legs_audit.py:45` work there and only there. A direct `python3 wave3/w3_10872_and_legs_audit.py`
from any other directory scans zero files and still prints 13/13.

---

## 5. Verdict table

| # | claim | verdict | reason |
|---|---|---|---|
| 1 | "(108,72) closed with the THEOREM 2 dependence removed" | **SOUND-BUT-OVERSTATED** | conclusion holds; THEOREM 2 removed from one leg only — the residual-gap leg substitutes an underived (99,66) chart transport (`ADJUDICATION:262-265`) against `EC:53`; the two load-bearing hypotheses ride on can't-fail checks at `wave3/w3_10872_and_legs_audit.py:110` and `:125` |
| 2a | "Second Framework dies" | **SOUND-BUT-OVERSTATED** | true, and more robustly than claimed (survives dropping γ=15, β=10 — see §3); "computed" is the overstatement |
| 2b | "`D_ode(SF) = 69/5`" as a computed number | **CANNOT-DETERMINE** | γ = 15, β = 10 are prose; `d23_phase1_chart.py` does not certify them; "5/5 of its own checks pass" (`Dode.py:9`) misdescribes a file with four prints and no failure exit |
| 2c | the derivation as presented | **UNSOUND-STEP-AT** `wave3/w3_second_framework_Dode.py:112` (N defined by the collapse it is then checked against) and **`wave3/w3_second_framework_verdict.py:68`** (β = 6 uniqueness, false under the suite's own ε-carrying `D_ode`) | — |
| 3 | "0 can't-fail checks in tree" (`ADJUDICATION:5`, Task 5) | **UNSOUND** | 22 parse-time-constant conditions across the scanned tree, 6 in wave3 itself; the self-scan's detector cannot see `Compare`/`IfExp`/literal-arithmetic conditions, including two in its own file |
| 4 | "fractional D_ode makes the transfer premise false as loudly as possible" | **OVERSTATED** | fractional `D_ode` is generic in this formula and already appeared for 7 of 9 charts in the lineage's own `EC_10872_instantiation.py` (89/6, 44/3, 29/2, 43/3, 27/2) |

**Base-rate note.** The brief said one recorded error per session for this lineage. I found more
than one, but the largest is not in the mathematics: the conclusions of both target claims survive
audit. The failures are of *certification discipline* — hypotheses and prose inputs entered into
pass counts as tautologies, a self-scan narrower than the property it certifies, an unreconciled
change of definition inside one commit pair, and a headline number whose inputs no file in the tree
computes.

---

## 6. What I verified that the parallel session did not

1. The trichotomy at **non-integer D** — `(69/5, 4)`, `(138/5, 9)`, `(69/5, 9)`: unique, map-degree
   k, verified by substitution.
2. The trichotomy at **k > 6** — `(39,14)`, `(39,13)`, `(42,14)`, `(69,24)`: no rational solution.
   These are the exact cells on which both claims' residual-gap closures depend.
3. The collapse identity with `a, b, e, β` **all symbolic** for ε = 1…6 — the `D_ode` formula is a
   theorem of the assumed block shapes, and independent of `G`.
4. `D_chain = 5β/2 − 2` under the framework relations, hence `D_chain ≡ 3 (mod 5)` **always** — the
   mod-5 kill cannot fail for any member of the class.
5. The family-branch escape is closed **universally** (`β | 4ε ⟹ D_ode/3 ≤ k`), exhaustively for
   ε ≤ 59, β ≤ 398. The SF conclusion needs neither 69/5 nor the SF chart data.

---

## 7. Probe scripts (reproduce)

All were run from the repo root under `python3` with sympy; each finishes in well under five
minutes. Written to a scratch directory, not to the repository.

**probe 1 — trichotomy off-grid** (rank/consistency over ℚ(c), `R = N(v)/((v+1)^m v^l)`):
`solve_box(D,k,m,l,n)` builds `T(R,D,k)+c`, clears denominators, takes `Poly(...).all_coeffs()`,
compares `rank(A)` to `rank(A|b)`; reports nullity and map-degrees of the representatives.
Cells run: `(69/5,4)`, `(138/5,9)`, `(69/5,9)`, `(39,14)`, `(39,13)`, `(42,14)`.

**probe 2 — the framework relations**: substitute `γ = 3β/2`, `σ = γ−β−1+p`, `p = 3` into
`D_chain = 2γ−σ` and `D_ode = 3ε(2e+3β)/β`; print `D_chain = 5β/2−2`, `D_ode = ε(15−12/β)`,
`D_ode/3 = 5ε−4ε/β`; scan ε ≤ 59, β ≤ 398 even for any case with `D_ode/3 ∈ ℤ` and `> 5ε−1`.

**probe 3 — the collapse identity, fully symbolic**: for ε = 1…6, with `a,b,e,β` symbolic, solve
`ea+βb = −ε(2e+3β)` for `b` and check
`e·δ·η′ + β·δ′·η == (α⁵/2)(β/3)U^{5ε−1}v^{a+b−1}[3v(v+1)R′ − D_ode·R]`. Also prints the
uncollapsed bracket, showing the `R`-coefficient is `v`-dependent without the collapse.

**probe 4 — the ε = 5 cell**: `(D,k) = (69,24)`, box `m = 24`, numerator degree ≤ 28 — rank test
only. Result: inconsistent system, no rational solution.

**scan.py — strict can't-fail scanner**: flags any `chk`/`check`/`rec` call whose second argument
contains no `Name`, `Call`, `Attribute`, `Subscript` or comprehension node, and evaluates it in an
empty namespace to record its constant truth value.
