# Why the failures happen, and what now stops them

Twelve recorded errors. They are not twelve independent slips. Sorted by mechanism
rather than by symptom, they collapse to **three**, and the three have one thing in
common: *nothing executable stood between the claim and the record.*

---

## The three mechanisms

### M1 — Confirmation-shaped verification
**The check was written after the conclusion, so it encodes the conclusion.**

- #2 `w1_h1c_endgame_closed_form.py:89` — `check("k >= 1 forces c = 0...", True, ...)`.
  The condition is a literal `True`. It was written to record a conclusion already
  reached, not to test it.
- #3 two more of the same in `w1_h1e_d_crossfire.py`.
- #7 two false-positive "hits" from detectors that had never been shown to reject a
  known negative. A detector validated only on things it should accept is a
  rubber stamp.

The tell: **a certifier that has never failed on anything has never been tested.**
`PASS` is only information if `FAIL` was reachable.

### M2 — Proxy trust
**Metadata was substituted for the artifact.**

- #4 believed a filename and a summary said "char-0 eliminant"; the file was msolve
  real-solution boxes.
- #5 concluded "Nguyen 104 is unverified" from three *failed searches*. Absence of hits
  is evidence about the search, not about the literature.
- #8 attached "Compositio Math 160 (2024)" to an unrefereed preprint — venue metadata
  invented to make a citation look finished.
- #12 `pkill -f` four times, once losing an uncommitted document: trusting a process
  name pattern instead of a handle to the process actually meant.

The tell: **the thing consulted was a label about the object, not the object.**

### M3 — Quantifier-scope drift *(the deep one)*
**A statement was proved under an implicit hypothesis and recorded without it.**

- #1 H1c. The proof evaluates at `v = −1`, which is legal only for *polynomial* `R`.
  The statement was recorded for *rational* `R`. One counterexample —
  `D = 6, k = 1, R = c/(6(v+1)²)` — and the headline `[PROVED-exact]` result is gone.
- **New this wave, same bug:** Session 38's collapse. Its sweep had `a > 0 > b`
  written into the search grid; the summary says "weighted-homogeneous forces
  diagonal linear". `(x, y + x^m)` with weights `(1, m)` is weighted-homogeneous,
  has Jacobian 1, and is not linear. The claim was true on its grid and false as
  stated. (`wave3/w3_weighted_homogeneous_theorem.py`.)
- #9 parameter count 60 → 59 → 58: counted a space while quietly assuming a gauge
  had been fixed. The domain of the count was never written down, so nothing
  could catch that it had moved.
- #10 "pentagon conditions cannot be written down": a *dense* bound applied to a
  *sparse* system, off by eleven orders of magnitude. The bound was true in its
  own domain and irrelevant in the one it was applied to.
- #6 running primes that violate the campaign's own `p ≡ 1 (mod 3)` rule is the same
  shape: the protocol's domain of validity was left implicit, so it could be
  stepped outside without anything registering.
- #11 the standing contradiction — "PROVEN dead, unconditional" beside "conditional on
  unreproduced THEOREM 2/3" — is M3's end state. Two labels for one claim survived
  in two files because prose has no key to collide on.

The tell: **the theorem's hypotheses live in the experiment, not in the sentence.**
M3 is the expensive one, because the result is genuinely *true* under the hypothesis
that got dropped. Nothing looks wrong. It only surfaces when someone downstream uses
the sentence outside the domain the proof covered — which is exactly what the
transfer conjecture did with H1c.

---

## The one-line root cause

> **Failures cluster where a claim was recorded without an executable, falsifiable
> check bound to it — and the certifier culture made `PASS` available without
> evidence.**

The mechanical computation was almost always sound. Every one of the twelve is an
error of *bookkeeping about what had been established*, not of algebra.

---

## What now stops each one

| mech. | guard | where | can it fail? |
| --- | --- | --- | --- |
| M1 | **No check condition may be a compile-time constant.** AST scan of the whole tree; exits nonzero on a hit. | `wave2/w2_cantfail_audit.py` | self-tested on a synthetic file with 1 rigged + 2 honest checks; must find exactly the rigged one |
| M1 | **Every certifier carries a negative control** — an input on which it is *required* to fail. | all of `wave2/`, `wave3/` | each control is itself a check that fails if the control passes |
| M1 | **The HIT gate must reject 8 known negatives and accept a positive control before it may certify anything.** | `wave3/w3_hit_protocol.py` | refuses to certify if H6 validation did not fire |
| M2 | **Anchor-by-exact-quotation.** Every load-bearing sentence is located by exact substring match against the file on disk; a missing anchor fails the run. | `wave2/w2_pole_admissibility.py` | two anchors were wrong on first run and the certifier failed — see the run log |
| M2 | **Absent artifacts are labeled `UNVERIFIED-HERE`,** never confirmed. §2.5 is on record as neither confirmed nor refuted. | `wave2/w2_irreducibility_sieve.py` | checks that the artifact really is absent |
| M2 | **`WITHDRAWN` is a distinct label** from `REFUTED`, and the linter demands a reason for it. A claim retracted on external authority may not be dressed as machine-refuted. | `wave3/w3_claim_ledger.py` | linter L7; the campaign ledger tripped L2 on this exact claim before the label existed |
| M2 | **`pkill -f` banned;** background jobs get handles, documents get committed before long runs. | working practice | — |
| M3 | **Every claim carries an explicit `domain`** — the exact quantifier range — in a structured ledger with stable keys. | `wave3/w3_claim_ledger.py` | linter L3 |
| M3 | **Every `PROVED` claim carries a domain probe:** a recorded input just *outside* the intended domain on which the claim is required to fail. | `wave3/w3_claim_ledger.py` | linter L3; e.g. W3-2's probe is `(x, y+x^m)` |
| M3 | **Contradiction linter:** two records under one key with incompatible labels is a hard error. Item #11 could not recur. | `wave3/w3_claim_ledger.py` | linter L1, self-tested |
| M3 | **Protocols encoded in code, not discipline.** `p ≡ 1 (mod 3)` is enforced by the sieve, with `5, 11, 17` fed in and required to be rejected. | `wave2/w2_irreducibility_sieve.py` | control primes must appear in the discard list |
| M3 | **Dependency edges are explicit** and no claim may depend on a `REFUTED` one. | `wave3/w3_claim_ledger.py` | linter L4 |

Every guard above is itself tested — the linter has a self-test that must produce
exactly seven violation codes on a synthetic ledger and **zero** on a clean one; the
AST scanner has a self-test that must find exactly the one rigged check. A guard
with no failing test is M1 all over again.

---

## The domain probe, in one paragraph

It is the generalisation of a negative control from *inputs* to *hypotheses*. A
negative control asks: does this certifier fail on a wrong input? A domain probe
asks: **does this theorem fail just outside its stated domain?** If it does not, the
domain is either wrong or wider than stated — and the sentence should say so. Both
of this session's live theorems carry one:

- **W3-2** (mixed-sign weights ⟹ linear): probe `(x, y + x^m)` at weights `(1,m)`.
  Same-sign, and the conclusion fails. The hypothesis `ab < 0` is exactly right, not
  an artifact of the search grid.
- **W3-1** (endgame realization ⟺ `3∤D` and `k = D`): probes `k = D` with `3 | D`
  (blocked) and `k = D` with `3 ∤ D` (available). Both boundaries checked.

Had H1c carried a domain probe, the counterexample would have been part of writing
it down.

---

## What is honestly still unfixed

- **#9 (the parameter count)** cannot be recomputed here — the artifact is not in this
  repository. It stands as `ASSERTED` with the obligation attached: no count is
  reportable without an explicit enumeration of the gauge group and a rank
  computation of its action.
- **#10 (the pentagon bound)** likewise: the claim is withdrawn, and re-making it
  requires either a failed construction with the failure diagnosed, or a bound whose
  sparsity model has been validated against a measured instance.
- **§2.5** is `UNVERIFIED-HERE`. The sieve machinery is built and validated; it needs
  the eliminant file.

Those three are recorded as open rather than quietly closed. That is the point of the
ledger.
