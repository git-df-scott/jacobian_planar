# Plane Jacobian campaign — certified record

This branch carries the wave-2 and wave-3 audit of the campaign's own results: what was
found to be wrong, what replaced it, and the machinery that now makes those classes of
error hard to commit and easy to catch.

```
python3 wave2/run_all.py        # runs every certifier; exit 0 iff all pass
```

Requires `sympy` and PARI/GP (`gp`) on `PATH`.

**11/11 certifiers, 227/227 individual checks, 0 rigged checks in tree, 0 ledger lint findings.**

---

## Read in this order

| document | what it is |
| --- | --- |
| [`WAVE2_FINDINGS.md`](WAVE2_FINDINGS.md) | the H1c refutation and the five approved tasks |
| [`WAVE3_FINDINGS.md`](WAVE3_FINDINGS.md) | the repairs, the Session 38 refutation, Path A's A1 and A2 |
| [`STATUS_CORRECTION.md`](STATUS_CORRECTION.md) | every wave-1 error, its correction, and the current label |
| [`FAILURE_ANALYSIS.md`](FAILURE_ANALYSIS.md) | why the failures happen, and the guard for each |

## Results

| | statement | evidence |
| --- | --- | --- |
| **W2-1** | `(v+1)^k(3v(v+1)R' − DR) = −c` has a rational solution **iff** `D ∉ {3,6,…,3k}` | `wave2/w2_h1c_refutation.py` |
| **W3-1** | the endgame admits a degree-`D` realization **iff** `3 ∤ D` and `k = D`; for `3 ∤ D` the solution is unique of degree `k` | `wave3/w3_endgame_degree_obstruction.py` |
| **W3-2** | a plane weighted-homogeneous Keller map with **mixed-sign** weights is linear, at every degree | `wave3/w3_weighted_homogeneous_theorem.py` |
| **W3-3** | same-sign weights break it: `(x, y+x^m)` | same |
| **W3-4** | `(det JG)∘π · D = (det JF) · (D'∘F)` | `wave3/w3_descent_jacobian_formula.py` |
| **W3-4a** | `D = x^{a₁+a₂−1}y^{b₁+b₂−1}z^{c₁+c₂−1}`, so `k = deg p₁ + deg p₂ − 3` | same |
| **W3-5** | Alpöge's class: `G = (A²(u²E+vH), A(uB+vC))`, `det JG = det JF·A²`, `f₃ = xA` | same |

## Refuted

- **H1c §2.1** (`k ≥ 1` leg, over rational `R`) — `D = 6, k = 1, R = c/(6(v+1)²)`.
- **Session 38's collapse** as stated — `(x, y + x²)`.
- **The transfer conjecture's mechanism** — backwards for rational `R`.
- **"The square is forced"** — `k = 0` and `k = 1` both occur.

## Verdicts

- **First Framework (99,66): DEAD**, and no longer conditional on the pole-fiber step.
- **Second Framework (`D = 23`): DEAD** for every endgame exponent `k ≠ 23`.
- **Path A, A1 + A2: answered.** Every weight class whose descent is Keller *is* the plane
  problem; Alpöge is a genuine `C³` counterexample precisely because its descent is not.
- **No hit.** Nothing in this repository passes the HIT gate, which is validated against
  eight known negatives and a positive control before it is allowed to certify anything.

## Still open

- §2.5 irreducibility — `UNVERIFIED-HERE`; the sieve is built and validated, the eliminant
  artifact is absent from this repository.
- The essential-parameter count — `ASSERTED`; needs an explicit gauge enumeration.
- The pentagon bound — withdrawn; needs a validated sparsity model.
- The conjecture.

## Discipline

- No check condition may be a compile-time constant (`wave2/w2_cantfail_audit.py`, AST scan).
- Every certifier carries a **negative control** — an input on which it must fail.
- Every `PROVED` claim carries a **domain probe** — an input just outside its stated domain
  on which it must fail (`wave3/w3_claim_ledger.py`, 7 lint rules, self-tested).
- Load-bearing quotations are anchored by exact substring match against the file on disk.
- Absent artifacts are `UNVERIFIED-HERE`; claims retracted on external authority are
  `WITHDRAWN`, never `REFUTED`.
