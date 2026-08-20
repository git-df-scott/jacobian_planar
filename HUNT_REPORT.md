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
| **2b. msolve on the pentagon exports** | graded prefix ladder L18…L23 from `pent_L23.ms`, each run twice (2 gauges as exported, and with the third gauge `p_1_0 − 1` added), `-t` threads, peak RSS and exit code recorded | `pent/RUNLOG.tsv`, `pent/pent_msolve.log` | **see RUNLOG** |
| **3. H2 above-125 sweep** | the shipped positive control was found **vacuous** and replaced; the queue re-run at a 900 s cap per prime, two compliant primes | `h2/w5_h2_controls.py` (5/5), `h2/h2_state.json`, `h2/h2_sweep_900.log` | **see log** |
| **4. H4 deg_y = 3 slice** | the staged msolve escalation continued, ladder extended past the four recorded OOM cells, each cell at **two** compliant primes with disagreement reported not averaged | `h4/w5_h4_escalate.py`, `h4/h4_escalate.log` | **see log** |

No CANDIDATE-UNVERIFIED was produced by any item. Nothing looked live.

---

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
