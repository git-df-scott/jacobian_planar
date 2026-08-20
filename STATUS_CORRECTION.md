# STATUS — Correction Record (Waves 2–3)

> **Wave 3 supersedes two wave-2 labels.** Item 11's First Framework label is no longer
> conditional on the pole question, and item 13's Second Framework label moves from
> OPEN to DEAD. Both changes are recorded in the wave-3 section at the bottom, which is
> the current state; the wave-2 entries are left in place as the record of how it moved.

This file supersedes the corresponding wave-1 STATUS entries. Each item states the
**erroneous claim**, the **correction**, and the **evidence or standing obligation**.
Items 1–3 and 5–12 come from the wave-1 record; items 1–3 were confirmed
independently this session by the certifiers in `wave2/`.

Standing rule adopted for this and every later wave:

> **No check condition may be a compile-time constant. Every certifier must contain at
> least one negative control — an input on which it is required to fail — so that
> "all checks passed" carries information.**
> Enforced mechanically by `wave2/w2_cantfail_audit.py` (AST scan, exits nonzero on a hit,
> self-tested against a synthetic rigged/honest pair).

---

## 1. H1c §2.1 — the headline `[PROVED-exact]` result is **FALSE as stated**

**Was:** for `T_{D,k}(R) = (v+1)^k (3v(v+1)R' − D R) = −c`, `c ≠ 0`, no rational `R`
exists when `k ≥ 1`; proved by evaluating at `v = −1`.

**Correction:** the `v = −1` evaluation silently assumes `R` is regular there, but the
statement quantifies over rational `R`, which may have a pole. Explicit counterexample,
certified exactly with `c` symbolic:

```
D = 6, k = 1, R = c/(6(v+1)^2)   ⟹   T_{6,1}(R) = −c
```

**Replacement (proved, machine-checked on 150 cells by two independent code paths):**

> **THEOREM W2-1.** `T_{D,k}(R) = −c` has a rational solution **iff** `D ∉ {3, 6, …, 3k}`.

The original statement is true only under the added hypothesis **"`R` polynomial"**, which
must now be written into the theorem and discharged explicitly at every use.

**Evidence:** `wave2/w2_h1c_refutation.py` — 11/11, includes negative controls.
**Label:** `[REFUTED-exact]` for the old statement; `[PROVED-exact]` for THEOREM W2-1.

---

## 2. `w1_h1c_endgame_closed_form.py:89` — rigged certifier

**Was:** `check("k >= 1 forces c = 0...", True, ...)` — the condition is a literal `True`.

**Correction:** the check could never fail, and it "certified" precisely the statement
refuted in item 1. It certified nothing. Removed from the evidence base; the claim it
carried is withdrawn.

**Evidence:** `wave2/w2_cantfail_audit.py`.

---

## 3. `w1_h1e_d_crossfire.py:58` and `:88` — two more hardcoded `True` checks

**Was:** same pattern, wrapping prose claims.

**Correction:** lower stakes, same disease. Both withdrawn as evidence. The prose claims
they wrapped are downgraded to `[ASSERTED]` until a real check exists.

**Evidence:** `wave2/w2_cantfail_audit.py`.

---

## 4. The char-0 eliminant claim — trusted a filename over the artifact

**Was:** believed a five-day-old claim that the characteristic-0 eliminant existed; the
cited file was msolve real-solution boxes, not an eliminant.

**Correction:** the claim was false and is withdrawn. **Rule adopted:** a file is evidence
only after its *contents* have been read and matched to the claim. `wave2/w2_pole_admissibility.py`
implements this literally — every load-bearing quotation is located by exact substring
match against the file on disk, and the certifier fails if an anchor is missing.

**Standing consequence:** the wave-1 §2.5 eliminant is **not present in this repository**
(`w1_h1c_endgame_closed_form.py`, `eliminant.txt`, `eliminant_char0.txt`, `certifiers/`,
`wave1/`, `artifacts/` — all absent). §2.5 is therefore recorded as **`UNVERIFIED-HERE`**:
neither confirmed nor refuted. See item 13.

---

## 5. "Nguyen 104 is unverified" — false

**Was:** claimed unverified on the strength of three failed web searches.

**Correction:** the result is real and refereed. The claim is withdrawn.
**Rule adopted:** failed searches are evidence about the search, not about the literature.
A negative literature claim requires a positive source (a retraction, an erratum, or a
specific refereed contradiction), never an absence of hits.

---

## 6. Prime hygiene violated — two of three primes broke the `p ≡ 1 (mod 3)` rule

**Was:** the campaign's own hygiene rule was violated in a modular run.

**Correction:** all modular work in wave 2 uses eight primes `≡ 1 (mod 3)`:
`7, 13, 31, 43, 61, 73, 97, 103`. The rule is enforced *in code*, not by discipline:
primes failing `p ≡ 1 (mod 3)` are discarded with a printed reason, and control primes
`5, 11, 17` are deliberately fed in and must all be rejected. Good reduction is additionally
required (`p ∤ lc(E)`, `E mod p` squarefree), with discards reported rather than silent.

**Evidence:** `wave2/w2_irreducibility_sieve.py` — 20/20.

---

## 7. Two false-positive "hits" — gauge artifacts from broken normalization

**Was:** two claimed hits, both artifacts of broken normalization in the detectors.

**Correction:** both withdrawn. **Rule adopted:** no candidate is reported as a hit until
it has been through the §7 HIT protocol with no step skipped, and no detector is trusted
until it is shown to *reject* a known-negative input. Every wave-2 certifier now carries
such a negative control.

---

## 8. Fabricated citation — "Compositio Math 160 (2024)" for an unrefereed preprint

**Was:** a journal, volume and year attached to a preprint that has none.

**Correction:** the citation is withdrawn. The work is an unrefereed preprint and must be
cited as such (arXiv identifier only). **Rule adopted:** no venue, volume, or year is ever
written unless it has been read off the published record; "arXiv:NNNN.NNNNN, unrefereed"
is the correct default and is never an embarrassment.

---

## 9. Essential-parameter count wrong twice (60 → 59 → 58) — missed gauges

**Was:** the count was corrected twice, each time because a gauge freedom had been missed.

**Correction:** both earlier numbers are withdrawn; the count stands at the last value only
as `[ASSERTED]`, not `[PROVED]`. **Rule adopted:** a parameter count is reported only
together with an *explicit enumeration of the gauge group* and a rank computation of the
group action on the parameter space. A count without that enumeration is not evidence.

**Obligation:** re-derive the count with the gauge enumeration written down before the
number is used in any argument.

---

## 10. "Pentagon conditions cannot be written down" — bound off by eleven orders of magnitude

**Was:** an infeasibility claim resting on a dense bound that was wrong by ~10¹¹.

**Correction:** the claim is withdrawn. A dense bound proves nothing about a sparse,
structured system. **Rule adopted:** an infeasibility claim requires either (a) an actual
attempted construction that failed with the failure diagnosed, or (b) a bound whose
sparsity model has been validated against a measured instance. Neither existed here.

---

## 11. The standing contradiction — resolved

**Was:** two mutually exclusive labels left standing in the same STATUS:

- (i) First Framework **"PROVEN dead, unconditional"**
- (ii) First Framework **"conditional on unreproduced THEOREM 2/3"**

**Correction: (ii) is correct; (i) is false.** Settled from the primary artifact, not from
memory. `Sessions 1-18 status reports`, under *SCOPE AND HONEST LABELS*, records its own
**Dependence** clause on the campaign's formalization of layers 1–3, the realization theory
and the rigidity theorem — and states that *"A referee-grade writeup of the Y-side geometry
is owed before public claims."* Both sentences are located by exact match by the certifier.

**The single label that STATUS now carries:**

> **First Framework (99,66): CONDITIONALLY dead.** Conditional on the campaign's own
> formalization of layers 1–3, the realization theory (Sessions 13–14) and the rigidity
> theorem (Session 13), none of which has been independently reproduced.
> The endgame step is sound **only** because Theorem 3 (pole-fiber) pins `R` polynomial —
> **not** because of the `v = −1` evaluation, which is invalid for rational `R` (item 1).

**Evidence:** `wave2/w2_pole_admissibility.py` — 10/10.

---

## 12. Shell killed four times by `pkill -f`, once losing an uncommitted document

**Correction / rule adopted:** `pkill -f` is banned. Long-running jobs are launched as
tracked background tasks and stopped individually by their own handles. Documents are
committed before any long-running command is started, so a lost shell can never cost work.
This session ran every long job under an explicit timeout and committed the deliverables in
one push at the end, with no process-wide kills.

---

## 13. **New this wave** — the transfer conjecture is blocked

Not a wave-1 error, but a direct consequence of item 1, recorded here because it changes a
STATUS verdict.

**Was:** *"TRANSFER CONJECTURE. For chain degree `D` the same mechanism yields
`3v(v+1)R' = D R`, fatal whenever `D/3` is not an integer. Second Framework: `D = 23`."*

**Correction:** for rational `R` the stated mechanism is **exactly backwards**. By
THEOREM W2-1, `D/3` not an integer is precisely the condition under which a rational
solution **exists**. Explicit solutions at both live `D`, verified through the operator:

```
D = 13, k = 1:   R = c (10 − 3v) / (130 (v+1))
D = 23, k = 1:   R = c (20 − 3v) / (460 (v+1))
D = 13, k = 4:   R = c (243v⁴ − 81v³ + 54v² − 42v + 35) / (455 (v+1)⁴)
D = 23, k = 4:   R = c (243v⁴ − 891v³ + 2079v² − 3927v + 6545) / (150535 (v+1)⁴)
```

**Label:** **Second Framework (`D = 23`): OPEN.** It cannot be closed by the transfer
argument as written. Closing it requires first re-deriving the analogue of Theorem 3
(pole-fiber / polynomiality of `R`) at `D = 23`. The same obligation applies to every
member of the isotope series.

**Evidence:** `wave2/w2_money_cells.py` — 31/31, with negative controls at
`D ∈ {3, 6, 9, 12}`.

---

## Verifications that came back clean

| claim | status | evidence |
| --- | --- | --- |
| `det JF ≡ −2` on the Alpöge map | **CONFIRMED** (symbolic, 25 exact rational points, 5 primes) | `wave2/w2_alpoge_detjf.py` |
| `C*`-equivariance, weights `(1,−1,−2)` → `(−2,−1,1)` | **CONFIRMED** | `wave2/w2_alpoge_detjf.py` |
| Path A descent: `det JG = −2(3u+v−2)²`, `deg G = (6,4)` | **CONFIRMED** (rebuilt from scratch) | `wave2/w2_irreducibility_sieve.py` |
| Alpöge geometric degree `d = 3` | **CONFIRMED** (degree-3 core eliminant at 4 targets) | `wave2/w2_irreducibility_sieve.py` |
| Census monodromy `S₃` | **CONFIRMED** (non-square discriminant at 4 targets) | `wave2/w2_irreducibility_sieve.py` |
| §2.5 irreducibility sieve | **`UNVERIFIED-HERE`** — eliminant artifact absent | `wave2/w2_irreducibility_sieve.py` |

---

## Reproduce

```
python3 wave2/run_all.py
```

Exit code 0 iff every certifier passes. Requires `sympy` and PARI/GP (`gp`) on `PATH`.
State after wave 2: 6/6 certifiers, 82/82 individual checks, 0 rigged checks in tree.
**Current state (wave 3): 11/11 certifiers, 219/219 individual checks, 0 rigged checks,
0 ledger lint findings.**


---
---

# Wave 3 additions and supersessions

## 11′. First Framework (99,66) — the conditionality is REMOVED

**Wave-2 label:** *CONDITIONALLY dead* — conditional on the campaign's formalization of
layers 1–3, the realization theory and the rigidity theorem, because the endgame step was
sound only via Session 13's pole-fiber THEOREM 3.

**Wave-3 correction.** THEOREM 3's decisive move — *"only the 1-point fiber fits a
≤2-point pole set, so the pole fiber is the order-13 point at `v = ∞`"* — never excludes
the other candidate that fits the same fiber count: `R` totally ramified over `∞` at
`v = −1`, i.e. `R = N(v)/(v+1)^13`. The text closes `v = 0` explicitly and is silent on
`v = −1`. That gap is real.

**THEOREM W3-1** closes it without THEOREM 3. For `T_{D,k}(R) = −c`, `c ≠ 0`:

- `3 ∤ D` → the rational solution is **unique**, of degree exactly `k` as a map `P¹→P¹`;
- `3 | D`, `D ≤ 3k` → no rational solution;
- `3 | D`, `D > 3k` → a one-parameter family of degrees `k` and `D/3`.

**Corollary: the realization demand `deg R = D` is met iff `3 ∤ D` and `k = D`.**

At `D = 13`, `k = 4` the solution is unique with pole order exactly **4** (numerator at
`v = −1` is 455 ≠ 0), so the `N(v)/(v+1)^13` branch does not exist.

**The label STATUS now carries:**

> **First Framework (99,66): DEAD.** Established from the chain degree `D = 13`, the
> endgame exponent `k = 4`, and the realization demand `deg R = 13`. It uses **no**
> `v = −1` evaluation, **no** pole-fiber count, and **no** polynomiality hypothesis for
> `R`. The remaining dependence is on the campaign's formalization of the framework's
> layers producing `D = 13` and `k = 4` — narrower than before, and stated.

**Evidence:** `wave3/w3_endgame_degree_obstruction.py` — 32/32.

---

## 13′. Second Framework (D = 23) — OPEN → DEAD

**Wave-2 label:** OPEN. Wave 2 showed the transfer conjecture's mechanism is backwards
for rational `R` and exhibited explicit solutions at `D = 23`, leaving the framework
unclosable by that argument.

**Wave-3 correction.** The transfer argument is still wrong, but the framework dies
anyway — for a different and better reason. `23` is not a multiple of 3, so by W3-1 the
endgame solution is unique of degree `k`; the realization demand needs degree 23. At
`k = 4` the solution is

```
R = c(243v⁴ − 891v³ + 2079v² − 3927v + 6545) / (150535 (v+1)⁴),   deg R = 4 ≠ 23.
```

**The label STATUS now carries:**

> **Second Framework (D = 23): DEAD for every endgame exponent `k ≠ 23`.** It survives
> only if its rigidity layer produces exponent exactly 23. Nothing in this repository
> suggests it does; the First Framework's analogous layer produces 4.

**Evidence:** `wave3/w3_endgame_degree_obstruction.py` — 32/32.

---

## 14. **New** — Session 38's weighted-homogeneous collapse is FALSE as stated

**Was:** *"plane: weighted-homogeneous forces diagonal linear"* — recorded in file `39`
as "the shape of a separator", carrying the whole Path B argument.

**Correction.** Session 38's sweep had `a > 0 > b` built into its grid (*"11 weight pairs
`(a,b)` with `a > 0 > b`"*). The summary dropped that hypothesis. Counterexample, one
line:

```
weights (1, m), m >= 2:   (P, Q) = (x, y + x^m)
  weighted-homogeneous:  yes      det J = 1      linear: NO
```

This is the **same failure mechanism as H1c** (item 1): a theorem proved under an
implicit hypothesis and recorded without it. Second occurrence in three sessions.

**Replacement (proved, degree-uniform, no bound):**

> **THEOREM W3-2.** A plane Keller map whose components are weighted-homogeneous for
> integer weights `(a,b)` with `a·b < 0` is linear — `(c₁x, c₂y)` or `(c₁y, c₂x)`.

This meets Path B's own stated success criterion (*"the weighted-homogeneous collapse is
upgraded to a theorem, a separator, no more caveats"*) — while narrowing the separator
to the mixed-sign case, which is where Alpöge's `(1,−1,−2)` actually lives.

**Labels:** `[REFUTED]` for the unrestricted claim; `[PROVED-exact]` for W3-2.
**Evidence:** `wave3/w3_weighted_homogeneous_theorem.py` — 66/66.

---

## 15. **New** — Path A's item A1 is ANSWERED: the square is NOT forced

**Was:** open. File `39` calls A1 *"the central question"* and rates a `k = 0` weight
system *"the single highest-value outcome available anywhere in the campaign."*

**THEOREM W3-4.** The maximal-minor vector of a quotient map `π` is `m(π) = D·ξ` (Euler
relation: `ξ` spans `ker Jπ`), and for an equivariant `F` with descent `G`:

```
(det JG)∘π · D  =  (det JF) · (D'∘F).
```

Verified in three weight classes with three different contents (`D = x²`, `x`, `1`), each
with a negative control. On Alpöge it reproduces `det JG = −2h²`, `h = f₃/x`, exactly.

**LEMMA W3-4a (closed form).** With `e₁, e₂` the exponent vectors of the two invariant
generators, `e₁ × e₂ = λ·w` (`λ = ±1`), so `D` is the **monomial**
`x^{a₁+a₂−1} y^{b₁+b₂−1} z^{c₁+c₂−1}` and `k = deg D = deg p₁ + deg p₂ − 3`. Hence `D = 1`
iff `e₁ + e₂ = (1,1,1)`, which has exactly three splittings — a proof for **all** weights,
not a box observation.

**Enumeration** over all 144 `C*`-weight systems on `C³` with a free rank-2 invariant ring:
`D = 1` (so `k = 0`) occurs, **exactly** for weights `(±1, ∓1, 0)` up to permutation;
`deg D = 1` (`k = 1`) also occurs; Alpöge's `(1,−1,−2)` gives `D = x²`.

**So the square is not forced.** But the `k = 0` class is degenerate: there
`F = (xA(u,v), yB(u,v), C(u,v))`, `G = (u·A·B, C)`, and `det JG = det JF` **identically**.
A `C³` counterexample with those weights *is* a plane counterexample with a factored first
coordinate.

**The label STATUS now carries:**

> **A1: ANSWERED — not forced, and not a recipe.** The exponent `k` measures how far a
> weight class is from being the plane problem; `k = 0` is where the distance is zero,
> which is precisely why nothing lives there. Alpöge sits at `k = 2` because the gap must
> be positive for the `C³` problem to be strictly weaker than the plane one. This is a
> sharper separator statement than "the square is forced", and unlike that one it is true.

**Evidence:** `wave3/w3_descent_jacobian_formula.py` — 27/27.

---

## 7′. The HIT protocol is now an executable gate

Item 7 (two false-positive hits from gauge artifacts) is closed operationally. The gate
runs six steps — exactness, Keller, non-injectivity, an *independent* generic-fiber
count, **gauge independence under random affine changes on source and target**, and
non-vacuity — and **refuses to certify anything** unless it has first rejected eight
known negatives and accepted the Alpöge positive control.

Run against this repository: **no hit.** The Path A descent is correctly rejected at H2
(`det JG = −2h²`, not constant).

**Evidence:** `wave3/w3_hit_protocol.py` — 12/12.

---

## 11″. The contradiction class is now mechanically closed

Item 11 was one contradiction that survived because prose has no key to collide on.
`wave3/w3_claim_ledger.py` stores every claim as a record with a stable key, an explicit
**quantifier domain**, a label, an evidence pointer, dependencies, and — for anything
`PROVED` — a **domain probe**: an input just outside the intended domain on which the
claim is *required* to fail. Seven lint rules, self-tested (exactly seven violation codes
on a synthetic ledger, zero on a clean one).

It caught a live one immediately: `NGUYEN-104` was labeled `REFUTED` with no evidence
pointer. A claim retracted on external authority is `WITHDRAWN`, not machine-refuted, and
the linter now demands the distinction plus a recorded reason.

**Current campaign ledger: 16 claims, 0 lint findings.**

---

## Reproduce (updated)

```
python3 wave2/run_all.py
```

Runs all eleven certifiers across `wave2/` and `wave3/`. Exit code 0 iff every one passes.
Requires `sympy` and PARI/GP (`gp`) on `PATH`.

**11/11 certifiers, 219/219 individual checks, 0 rigged checks in tree, 0 ledger lint
findings.**
