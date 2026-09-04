# T5 — Gao family mechanism table (arXiv:2608.00222v1)

Source: `papers/2608.00222.pdf`, sha256 in `papers/SHA256SUMS`.
Certifier: `gao/run_gao.py` (17/17 checks, log `gao/gao_audit.log`, data
`gao/family.json`). The paper's own AI-disclosure note says the write-up was
machine-assisted, so nothing in it is used as a premise: every dimension-3 map
is re-expanded from the printed components, cross-checked against the paper's
own §3.3 recipe, and verified in exact rational arithmetic.

## Dimension 3 — computed

| member | ref | d (component degrees) | det J F | C*-weights | invariants π | k (W3-4a) | k (det J of descent) | h | geom. degree (printed) | sweep-form | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F (Alpöge, as Gao prints it) | §3.4, p.6, Thm 3.3 | (7,6,4) | **−2** (computed, matches) | (1,−1,−2) | (xy, x²z) | **2** | **2** | 3u+v−2 | 3 | yes (tangent sweep, deg p = 2) | — |
| G (new degree-four map) | §3.5, p.7, Thm 3.5 | (4,11,12) | **2** (computed, matches) | (1,−1,−2) | (xy, x²z) | **2** | **2** | 4u+v−2 | 4 | yes (tangent sweep, deg p = 3) | — |

The two k-routes are independent: the first is `k = deg p₁ + deg p₂ − 3` from
LEMMA W3-4a (2 + 3 − 3 = 2), the second is the exponent of the non-constant
factor of det J of the explicitly constructed descent. **They agree on both
maps.** That agreement is this audit's control; a weight class where they must
give a different answer (weights (1,−1,0), k = 0) is exercised as a negative
control and both routes return 0 there.

Non-injectivity witnesses, both verified by exact substitution:

* F: `(0, 0, −1/4)`, `(1, −3/2, 13/2)`, `(−1, 3/2, 13/2)` all map to `(−1/4, 0, 0)`
  — the paper's printed triple, re-verified.
* G: **found by exact search in this audit** (the paper prints none):
  `(−3/2, 2/3, 8/3)` and `(0, −2/3, −4)` both map to `(0, −4/3, 0)`.

## Dimension > 3 — recorded and skipped, per the brief

| member | ref | dim | component degrees | det J | geom. degree | direction field |
|---|---|---|---|---|---|---|
| F4 | §4.4.1, p.13–14, Thm 4.3 | 4 | (4,11,12,21) | −44/9 | 5 | (1, w₁, w₁²)ᵀ |
| F5 | §4.4.2 | 4 | — | — | 10 | (1, w₁, w₂)ᵀ |
| F6 | §4.5 | 5 | — | −290 | 6 | (1, w₁, w₁², w₂)ᵀ, bottom (L₁-)branch |
| F7 | §4.6 and the table on p.15 | 5 | — | det J(F₀) = γ² | 12 | (1, w₁, …, w₁ⁿ⁻²)ᵀ |

## PORT-CANDIDATE flags

**None.** Both computed members sit at k = 2, the Alpöge pattern. Nothing with
k = 0 or with a structure off that pattern appears among the dimension-3
members. Per W3-4's own Corollary A1b the k = 0 class is where a C³ Keller map
*is* a plane Keller map with a factored first coordinate; no Gao member lands
there.

## Controls (all in `gao/gao_audit.log`)

* the printed components of both maps equal the §3.3 recipe run at deg p = 2 and 3;
* det J and the component degrees match the printed values exactly;
* the weight finder recovers (1,−1,−2) without being told it;
* NEGATIVE: one corrupted coefficient makes det J non-constant;
* NEGATIVE: in the k = 0 class both k-routes give 0, so the exponent is not
  hard-wired to 2;
* NEGATIVE: the witness verifier rejects a non-witness.
