# HUNT_REPORT — the four-item queue

Branch `claude/opus-hunt-territories`, off `claude/plane-counterexample-endgame-az3geq`.
Every verdict below rests on a certifier in this branch with at least one
negative control that is required to fail. No prior campaign result is used as a
premise. The AST can't-fail scanner (`wave2/w2_cantfail_audit.py`, errors branch)
is clean on every file added here.

Toolchain built from source per `BUILD.md` on the toolchain branch:
msolve 0.10.1, Singular 4.3.2p16. Primes: **p ≡ 1 (mod 3) only**, and the three
used for item 1 (1000003, 1000033, 1000039) are fresh — they appear nowhere in
the campaign record.

---

## Table

| item | what ran | artifact | verdict class |
|---|---|---|---|
| **1. Case (2) over ℚ̄ — chart d_3_3 = 1** | system rebuilt from `trackA_system_case2.json`; structure certified; w=−4 block solved (eliminant degree 5) at 3 fresh primes; residual collapsed by exact elimination over F_p[w]/(g) to 27 conditions in 6 parameters; solved over **every** Galois orbit of the eliminant | `wave4/artifacts/item1_cascade_results.json`, `wave4/w4_c2_cascade_solve.py`, `wave4/w4_case2_selftest.py` (13/13) | **EMPTY** at 1000003, 1000033, 1000039 — every orbit, mutant and pin controls pass in every cell |
| **1b. Complementary chart d_3_3 = 0** | stated and tested: the chart split is exhaustive because d_3_3 is not a nonzero condition and the gauge subgroup fixing (d_2_1, c_8_16) moves d_3_3 with weight 2; the w=−4 block itself was solved in that chart | same JSON, keys `w4_zero_p*` | **EMPTY** at all three primes, controls pass |
| **1c. Direct 71-variable route** | all 92 equations, all variables, one msolve call, chart d_3_3=1 | `wave4/artifacts/c2_full_*`, kernel log | **STALLED — OOM at 10 GB RSS** (recorded, not a verdict) |
| **1d. Edge-count reconciliation** | 5 (here) vs 1144 (`wave1/edgeQ_input.ms`) | `wave4/w4_edge_reconciliation.py` (7/7) | **consistent, different normalisations** — see below |
| **2a. Pentagon hit detector v3** | all three gauges fixed, absolute normalisation, O(1)-allowed as an acceptance condition; float Newton from random starts; exact mod-p slice search at 3 compliant primes | `pent/w5_pent_hitdetector_v3.py`, `pent/pent_slice.py`, `pent/pent_v3_results.json`, `pent/pent_v3.log` | **see log** — controls 9/9 |
| **2b. msolve on the pentagon exports** | graded prefix ladder L18…L23 from `pent_L23.ms`, each run twice (2 gauges as exported, and with the third gauge `p_1_0 − 1` added), peak RSS and exit code recorded | `pent/RUNLOG.tsv`, `pent/RUNLOG_NOTES.md`, `pent/pent_msolve.log` | **STALLED, stall points named**: `L18` with 3 gauges → **OOM**, exit −9, peak RSS 6,238,548 kB after 1798.9 s; `L18` with 2 gauges → **TIMEOUT** at 3600 s. Higher rungs continue |
| **3. H2 above-125 sweep** | the shipped positive control was found **vacuous** and replaced (5/5); the queue re-run at a 900 s cap per prime, two compliant primes; then a **second engine** (msolve F4/FGLM) put on the targets Singular cannot decide | `h2/w5_h2_controls.py`, `h2/h2_state.json`, `h2/h2_sweep_900.log`, `h2/h2_changelog.json`, `h2/w5_h2_msolve_escalate.py`, `h2/h2_msolve.log` | **NO VERDICT CHANGE at the 900 s cap**: the two targets re-run stayed TIMEOUT; 0 LIVE, 0 DISAGREE anywhere. Second engine: parser and cross-engine controls pass (msolve reproduces Singular's EMPTY on a decided target in 0.07 s), targets in progress |
| **4. H4 deg_y = 3 slice** | the staged msolve escalation continued, ladder extended past the four recorded OOM cells, each cell at **two** compliant primes with disagreement reported not averaged | `h4/w5_h4_escalate.py`, `h4/h4_escalate.log`, `h4/INTERVENTION_NOTE.md` | **STALLED — OOM, at both primes, on every cell reached**: k=4 deg≤6, k=5 deg≤4, k=5 deg≤5, k=6 deg≤4, k=4 deg≤7. msolve's parser and cross-engine controls pass, so the OOMs are the engine's limit, not a misread. One cell's second prime was hand-terminated to free memory and is marked UNKNOWN, not OOM |

No CANDIDATE-UNVERIFIED was produced by any item. Nothing looked live.

---

## Item 1 — the input artifact is certified, not assumed

Everything in Item 1 rests on `campaign/audit_tracks/trackA_system_case2.json`.
That file carries a content hash, but a hash only says the bytes have not
changed. `wave4/w4_case2_json_audit.py` (7/7) checks the thing that matters:
taking its 25 c-variables and 47 d-variables at face value as the supports of P
and Q, expanding `[P,Q] − x²` symbolically over ℚ, and comparing coefficient by
coefficient.

* **all 92 equations are exactly the corresponding coefficients**, and
* **every one of the 92 nonzero bracket monomials has an equation** — nothing
  is missing;
* the polygon vertices in the meta are genuine extreme points of the supports,
  and the support sizes match `SP_size`/`SQ_size`;
* NEGATIVE: perturbing one equation breaks the match, and comparing against
  `[Q,P] − x²` instead disagrees on **all 92**, so the orientation is pinned
  rather than accidental.

## Item 1 — what was actually established

The case-(2) system is 72 coefficient variables and 92 equations, and in the
grading `w = j − 2i` it splits into blocks that are **certified**, not assumed
(`wave4/w4_case2_selftest.py`, 13/13 with negative controls):

```
w = -4 : 17 equations in (C,G) only          <- self-contained
w = -3 : 18 equations, linear in (B,F)
w = -2 : 19 equations, linear in (A,E)
w = -1 : 19 equations, linear in D           <- the 13-variable D block
w =  0 : 19 equations, no new unknowns
```

The gauge is three-dimensional — `P' = a P(mu x, nu y)`, `Q' = b Q(mu x, nu y)`,
`b = 1/(a mu^3 nu)` — and this is verified as an exact symmetry of all 92
equations at random points (S2), with a wrong-exponent negative control (S2n).
Two of the three parameters are fixed by `d_2_1 = 1` and `c_8_16 = 1`, both of
which are in the JSON's own `nonzero` list, so those are gauge fixings and never
case splits; `d_3_3` is **not** in that list, which is why `d_3_3 = 1` versus
`d_3_3 = 0` is the genuine, exhaustive chart split. The rigidification
determinants are computed: 2 in the first chart, −1 in the second (with
`d_12_24 = 1` supplying the third fixing there).

Above a w=−4 solution the rest is linear, so the residual does not need a
Gröbner engine at all. The brute-force route was tried and **OOM-killed at 10 GB**;
the elimination route collapses the residual to 27 conditions in 6 parameters and
is decided in hundredths of a second. Working in `F_p[w]/(g)` for each
irreducible factor `g` of the eliminant covers **every root, including those in
extensions of F_p** — not only the F_p-rational ones.

## Item 1 — the edge variety over ℚ, exactly

Beyond what the queue asked for (mod p), the eliminant of the w=−4 block in the
chart d_3_3 = 1, with all gauges fixed and the vertex conditions saturated, was
reconstructed **over ℚ**:

* at **96** primes ≡ 1 (mod 3) msolve returns a rational parametrisation whose
  eliminant has degree **5**, at every one of them
  (`wave4/w4_edge_eliminant_Q.py`, 5/5);
* CRT + rational reconstruction over 41 of them gives an explicit degree-5
  polynomial with coefficients of up to 122 digits, and that polynomial
  **reproduces msolve's eliminant at 6 primes that were not used to build it**;
  a single corrupted coefficient fails the same check;
* the reconstructed polynomial is **squarefree, irreducible over ℚ, has no
  rational root, and its Galois group is S5**
  (`wave4/w4_edge_eliminant_structure.py`, 6/6, with a D5 quintic as the
  negative control on the Galois call).

So the five edge points of the fully rigidified case-(2) w=−4 block form a
single Galois orbit with full symmetric group, and none of them is rational.
**Standing: reconstructed and verified at held-out primes, not a char-0 Gröbner
proof** — the exact char-0 solve (`msolve -P 1` on the same system over ℚ) was
launched alongside and is reported separately with its own outcome.

Artifacts: `wave4/artifacts/edge_eliminant_Q_one.json`,
`wave4/artifacts/edge_eliminant_structure.json`, `wave4/elimQ.log`.

## Item 1d — the 5-versus-1144 reconciliation

Rebuilt from the JSON, the w=−4 block with all gauges fixed has eliminant degree
**5**. `wave1/edgeQ_input.ms` has degree **1144**. Both reproduce. They are not
in conflict:

* the 5 is not an artefact of the c-elimination — the untouched 19-variable block
  handed straight to msolve also gives 5;
* a point of the derived variety satisfies **all six** of the campaign's edge
  polynomials once its gauge is normalised to `d_3_3 = 1`;
* the derived system is invariant under the residual gauge `g_j -> kappa^(j-3) g_j`;
  the campaign's six polynomials are **not** — restricted to the orbit through
  that point their gcd is `kappa^2 (kappa − 1)`. Moving to `kappa = 2` keeps the
  derived system satisfied and breaks all six campaign generators.

So `edgeQ_input.ms` is a differently, more rigidly normalised object and its 1144
counts points of that normalisation. **Neither number is wrong; they must not be
quoted as if they measured the same variety.**

## Item 2 — the 43 MB export is now cross-validated

`wave1/pent_L23.ms` is the object every pentagon msolve run in this campaign is
about, and it had never been checked against a second implementation.
`pent/w5_pent_export_check.py` (4/4) does that: it evaluates all 66 exported
generators at random points over a compliant prime and compares them, generator
by generator, with the forbidden coefficients produced by the y-adic recursion
in the v3 detector, which shares no code with the exporter.

**All 66 match, up to a nonzero constant per generator, at 3 independent random
points** — a constant per generator is a cleared denominator and does not change
the variety. The variable sets agree exactly. Negative controls: perturbing one
coordinate changes all 66 values, and comparing generator *k* against generator
*k+1* does not match, so the agreement is not vacuous.

## Item 2 — a well-posedness finding about the pentagon detector

STATUS §6's standing requirement is an **absolute** normalisation, and v3
implements it. Building it surfaced a constraint that has to be stated with any
number the detector produces: the y-adic recursion amplifies, so at a random
parameter point the levels-13..23 coefficients run past 1e10, and **float64
cannot resolve an absolute 1e-9 there at all**. The acceptance band (allowed
coefficients O(1)) is precisely the region where an absolute test is meaningful.
So the search's residual numbers are only interpretable together with the
allowed scale at the point that produced them, and v3b records both for every
start. The planted positive control is drawn from inside the band for the same
reason — outside it, the control would fail for a floating-point reason and say
nothing about the detector.

Second change in v3b: Newton's Jacobian is computed **exactly**, over
C[eps]/(eps^2), instead of by a finite difference with h = 1e-7 (which caps a
Newton step at about 1e-8 accuracy and could stall a search near 1e-5 without
that being a fact about the system). On the planted control the exact version
reaches 1.29e-11.

## Tooling findings recorded this session

Two silent lies in msolve 0.10.1, each found by minimal reproduction, each
documented with the reproduction in `wave4/w4_msformat.py`:

* **L1** — a constant generator whose terms sum to a multiple of the
  characteristic is read as nonzero and the system is declared `[-1]` (EMPTY).
  Written as the single token `p` it produces a **zero-byte output file**.
* **L2** — repeated monomials inside one generator are not combined:
  `a + a + 1000001` is solved as `a + 1000001`, while `2*a + 1000001` gives a
  different answer. No diagnostic either way.

Every input this branch generates now passes a sanitiser and a validator.
The campaign's own `.ms` files were scanned and are **clean** of both.

A third finding, in the H2 engine: `trackD_twoprime.py::control()` builds its
"unsaturated" variant by deleting lines containing `sat` or beginning `ideal N`,
and the generated source contains neither — the variant is byte-identical to the
real system, so the control reports FAIL for a reason unrelated to the engine.
Corrected controls are in `h2/w5_h2_controls.py` and pass 5/5.
