# TRUST MAP — plane Jacobian campaign


> ## ⚠ CORRECTED BY PR #9 — read this first
>
> An adjudication pass (branch `claude/opus-5-counterexample-plan-sep6yk`, PR #9,
> `ADJUDICATION.md`, 110 exact checks) refuted several claims in this document. They are
> corrected in place below and listed here so nothing is taken on trust:
>
> 1. **`ABSENT` is wrong — the correct label is `NOT-FETCHED`.** This session ran
>    `git rev-list --objects --all` against a local object set containing only `main`
>    plus its own commits. The artefacts exist on `claude/plane-counterexample-endgame-az3geq`:
>    **65** session-19–38 paths, `wave1/edgeQ_eliminant.txt` (5,759,664 bytes),
>    `wave1/pent_L23.ms` (43,158,481 bytes), `CASE2_STATUS.md`, `ABOVE_125_STATUS.md`,
>    and the H1c files. Every "blocked here" below inherits this error.
> 2. **`D = 15 − 12/β` dropped an `ε`.** The correct formula is
>    `D_ode = ε·(15 − 12/β)` with `ε = ord_{U=0}(g)`; the bound `< 15` holds only at `ε = 1`.
> 3. **`m = 4` is not universal.** The exponent is `k = 5ε − 1`, so `k = 0` or `k ≡ 4 (mod 5)`.
> 4. **The "two independent closures" are one closure.** `deg W̃₋₅ = 28 ⟺ map-degree 13`
>    identically, so the degree-ledger leg and the map-degree leg are the same statement.
>    The genuinely independent second leg is E4's ladder bound, which is genericity-conditional.
> 5. **The nine (108,72) charts are not proved exhaustive** — they assume both bidegrees are
>    multiples of one primitive edge vector. Witness outside the enumeration: `(40,68)`, `(30,42)`.
>
> **The conclusions survive.** (99,66), (108,72), the Second Framework and the isotope
> series are all still empty — on `k ≡ 4 (mod 5)` plus `D_ode`, computed in PR #9
> (`D_ode(Second Framework) = 69/5`, so neither 23 nor 69: dead for every `ε`).

**Step 1 of the plan: which doors are actually locked, and which were only claimed locked.**

Produced by re-running every executable artefact in this repository from scratch and
re-deriving every load-bearing identity independently. Everything below is either
`CERTIFIED HERE` (an exact machine check in `certifiers/`, reproducible with
`./run_all.sh`), `TRUE BUT SCOPE-LIMITED`, `REFUTED`, `UNCERTIFIED` (a claim whose
statement is in the repo but which has no executable certificate anywhere), or
`NOT-FETCHED` (a claim whose artefacts exist on a branch this session never fetched — originally and wrongly labelled `ABSENT`; see the banner).

Toolchains: **sympy 1.14 / Python 3.11** and **PARI/GP**, no shared code between them.
All arithmetic exact — rationals, `Q(sqrt(-3))`, or symbolic. No floating point is
load-bearing anywhere in the new work.

---

## 0. What is physically in the repository

`git rev-list --objects --all` shows the entire history: four documents
(`39`, `40.md`, `41.md`, `42.md`, `Sessions 1-18 status reports`) and one deleted
prompt. **Sessions 19–38 are not in this repository in any form**, neither as files
nor as deleted blobs. That fact alone determines a large part of the trust map.

---

## 1. Verdicts on the load-bearing claims named in the plan

| Claim | Verdict | Where |
|---|---|---|
| Alpöge map: `det JF = -2`, three rational points collide | **CERTIFIED HERE** (two toolchains) | `E7`, `E8` |
| Alpöge map: `C*`-equivariance, weights `(1,-1,-2) -> (-2,-1,1)` | **CERTIFIED HERE** (two toolchains) | `E7`, `E8` |
| Session 39 descent: `deg G = (6,4)`, `det JG = -2 h^2`, collision survives | **CERTIFIED HERE** (two toolchains) | `E7`, `E8`, `S14` |
| Session 39: `h = f_3/x`; the colliding point `(-3/2,13/2)` lies on `h = 0` | **CERTIFIED HERE** — and it was *never checked* by Session 39's own script | `E7` |
| Session 39: `h^2` is intrinsic under coordinate change | **CERTIFIED HERE** — also not checked by its own script | `E7` |
| Session 7 Belyi data, `deg(p^2 - w r^3) = 3`, `h = h0` constant | **CERTIFIED HERE** (archive script re-runs clean) | `S06`, `E9` |
| Cross-epoch identity `h0 = -13 n3` | **CERTIFIED HERE**, re-derived independently | `E9` |
| Session 8 layer-1 chart, pole conditions, near-miss saturation | **CERTIFIED HERE** (archive script re-runs clean) | `S07` |
| Session 10 chain-miracle unification, 13 block vanishings | **CERTIFIED HERE** (archive script re-runs clean) | `S09` |
| Sessions 16–18 **master identity** `block = α⁵(v+1)⁴(3v(v+1)R' − 13R)/v⁶` | **CERTIFIED HERE — re-derived from scratch with symbolic framework data.** The archive's certificate for it was lost; the identity is nonetheless **true**, and now has a proof that does not depend on the lost run. | `E1` |
| Sessions 16–18 endgame LA certificate (`T(R)=1` infeasible, rank 14) | **TRUE BUT SCOPE-LIMITED** — reproduced exactly, and shown to search a space of *polynomials* that provably cannot contain the actual solution | `E9` |
| Sessions 16–18 **conclusion** "(99,66) First Framework is empty" | **CONCLUSION SURVIVES, PROOF REFUTED AND REPLACED.** See §2. | `E2`–`E6` |
| Sessions 16–18 **transfer conjecture** ("fatal whenever `D/3 ∉ ℤ`", "Second Framework: `D=23`") | **REFUTED — both halves.** Replaced by a proved statement. See §3. | `E6` |
| THEOREM 1 (sqrt-reduction) | **UNCERTIFIED in the archive; the two identities it is used for are CERTIFIED HERE** (`(ΣS_m x^m)² = (1+T)³` through `x¹³`, and `W~₋₅ = 2g³(A~₄ − g³S₁₃)`) | `E4` |
| THEOREM 2 (total rigidity, `g = αU(U−1)⁸`) | **UNCERTIFIED** — statement present, certificate lost. Used as a hypothesis by closure 1; **not needed** by closure 2 | — |
| THEOREM 3 (pole-fiber ⇒ `R` polynomial) | **UNCERTIFIED, AND NO LONGER NEEDED.** Both repaired closures avoid it entirely | `E5` |
| Session 11 degree ledger `deg W~₋₅ = 6·deg g − 26 = 28` | **CERTIFIED HERE** (arithmetic and the `R`-degree bookkeeping both re-derived) | `E5` |
| Session 14/15 box caps, branch valuations, cusp discovery | **UNCERTIFIED** — `print(__doc__)` only | — |
| **H1c** | **NOT-FETCHED** — `wave0/w0_h1c_borisov_belyi.py`, `wave1/H1C_VERDICT.md`, `w1_h1c_endgame_closed_form.py` exist on `az3geq`. Its §2.1 theorem is **REFUTED** by PR #9 (159/210 cells) | `w3_odequation_adjudication.py` |
| **the irreducibility sieve** | **NOT-FETCHED** (no path matched on `az3geq` either; still unlocated) | — |
| **the eliminant** | **NOT-FETCHED** — `wave1/edgeQ_eliminant.txt`, 5,759,664 bytes | — |
| **chart coverage** | **NOT-FETCHED** — and the Second Framework's chart is certified by `campaign/d23_borisov/d23_phase1_chart.py`: `γ=15, β=10, p=3` | — |
| §2.1 theorem and its certifier | **NOT-FETCHED, then REFUTED** — `w1_h1c_endgame_closed_form.py:89` is `check(..., True, ...)` | `w3_odequation_adjudication.py` |
| pentagon system; case (2) over `Q̄`; the 167 above-125 targets | **NOT-FETCHED** — `wave1/pent_L15..L23.ms` (`pent_L23.ms` is 43,158,481 bytes; every `.out` is 0 bytes, so those runs never produced output), `CASE2_STATUS.md`, `ABOVE_125_STATUS.md` | — |

### Which archive scripts actually certify anything

| file | executable content |
|---|---|
| Session 1, 2, 3, 4, 5, 6, 7, 8, 10, 39 | **real computation**, re-runs clean |
| Session 9 (layer 2), 11, 12–14, 15, **16–18** | **`print(__doc__)` only** — no computation at all |

The `[PASS]` marks in the Sessions 16–18 ledger are **prose inside a docstring**, not
outputs of a check. That is the mechanical form of "the certificates are lost".

---

## 2. The headline result: (99,66) First Framework

**What the archive proved.** The chain layer, boundary rigidity and the Keller chart
reduce the whole framework to one equation in one unknown rational function `R(v)`:

```
    alpha^5 (v+1)^4 ( 3 v (v+1) R'(v) - 13 R(v) ) = -c ,      c != 0 .
```

This reduction is **correct** — `E1` re-derives it from scratch, and the archive's own
collapse arithmetic `13(9v+8) − 117(v+1) = −13` checks out.

**What the archive then did, and why it is invalid.** It argued: *"The left side
vanishes at `v = -1`; the right side is `-c != 0`. Contradiction."* That step evaluates
`(v+1)^4 · (…)` at `v = -1` and concludes it is zero. **That is only true if `R` has no
pole at `v = -1`.** Polynomiality of `R` was supplied by THEOREM 3, whose certificate is
lost, and the supporting linear-algebra certificate searched **only polynomials** — so it
could not have found a pole solution even if the theorem were dropped.

**The pole solutions exist.** `E2` (sympy) and `E3` (PARI/GP, independent code) prove:

> `(v+1)^4(3v(v+1)R' − 13R) = κ ≠ 0` has **exactly one** solution in `Q̄(v)`:
> ```
> R(v) = − κ (243 v^4 − 81 v^3 + 54 v^2 − 42 v + 35) / (455 (v+1)^4),
> ```
> with a pole at `v = −1` of order **exactly 4**, no other poles, and map-degree 4.

So the archive's decisive step is refuted, and its certificate's scope limitation is
exactly one Laurent shift wide (`E9` finds the solution by changing `P(v)` to
`P(v)/(v+1)^4` in the archive's own code).

**The conclusion nevertheless survives.** Two closures are recorded below; PR #9 shows closure 2 is the *same statement* as the degree ledger rather than independent of it, so the independent pair is closure 1 (genericity-conditional) and closure 2:

* **Closure 1 — pole admissibility (`E4`).** The framework's own divisibility ladder
  forces `ord_{U=0}(W~₋₅) ≥ 3`, i.e. `ord_{v=−1}(R) ≥ −3`: **the pole order can be at
  most 3.** The unique solution needs exactly 4. *Out of range by exactly one.*
  (Proved for towers with no accidental cancellation in the ladder; the bound reduces to
  a finite partition statement, `f(13) ≥ −3`, checked over all 101 partitions of 13.)
* **Closure 2 — degree ledger (`E5`).** Propagating the unique `R` up the tower gives
  `W~₋₅ = α⁶ U²(U−1)⁹ S(U−1)`, an honest degree-15 polynomial. The framework's
  13-realization needs `deg W~₋₅ = 28`, equivalently `deg R = 13`; the solution has
  map-degree **4**. This closure uses **no** genericity, **no** Belyi coefficients, and
  **not** THEOREM 3.

Striking detail: the pole branch has `deg W~₋₅ = 15` — *exactly the near-miss's degree*.
The branch Opus's theorem wrongly excluded lands in the same degree stratum as the
near-miss and dies on the same ledger.

**Verdict: the door is locked, but it was locked with the wrong key.** The emptiness of
Borisov's First Framework at (99,66) stands; its published proof does not.

---

## 3. The transfer conjecture: refuted and replaced

The archive's closing conjecture is wrong in both halves (`E6`):

1. **`D` is not the chain degree.** From the framework data alone,
   `D = 3(2e+3β)/β = 9 + 6e/β = 3N/(1+G)`, and with the Keller chart exponent `p = 3`,
   `D_ode = ε·(15 − 12/β)`. Hence **`D_ode < 15` at `ε = 1`** (the `ε` was dropped here originally): the
   Second Framework cannot have `D = 23`. `D = 13` at (99,66) only because `β = 6`.
2. **The fatality criterion is exactly backwards.** `3 ∤ D` is precisely the case where
   the equation **is** solvable (uniquely). The fatal case is `3 | D` with `D/3 ≤ m`.

**Replacement (proved):** the exponent `m` on `(v+1)` is **4 for every framework of cusp
type (2,3)** — it is `U³` from the deviation block times `U¹` from `η'`, equivalently
`U²·U²` from `δ'·η`, independently of `β, e, G, N, p`. Therefore the endgame equation has
**at most one** rational solution and that solution **always has map-degree 4**. A
framework whose realization layer demands a degree-`D_chain` map with `D_chain ≠ 4` is
**empty**. At `p = 3`, integral `D` forces `β | 12`:

| `β` | `D_ode = 15 − 12/β` (at `ε = 1`) | endgame verdict |
|---|---|---|
| 1 | 3 | **no rational solution at all** — framework dies outright |
| 2 | 9 | **no rational solution at all** |
| 3 | 11 | unique solution, map-degree 4 |
| 4 | 12 | **no rational solution at all** |
| 6 | 13 | unique solution, map-degree 4  ← First Framework |
| 12 | 14 | unique solution, map-degree 4 |

So the transfer conjecture's *conclusion* — "the entire published framework family dies
to the one obstruction" — is **true**, and now has a valid proof covering the Second
Framework and the isotope series uniformly, with no Belyi rederivation required for
either. The `N2_prompt.md` sub-campaign (Phase 0: rederive the degree-23 Belyi data) is
**unnecessary**: the obstruction never touches the Belyi coefficients.

---

## 4. Reopened / still-open territory

* **(108,72) framework route. CLOSED (`EC`).** `11 ∤ 108`, so (108,72) cannot reuse the
  (99,66) edge vector; its admissible charts are indexed by `s = a+b | gcd(108,72) = 36`,
  nine in all. Seven give a unique endgame solution of map-degree 4; two (`s = 18, 36`,
  i.e. `D = 12, 9`) give no rational solution at all. No chain degree is 4, so every
  admissible chart closes. Conditional only on the Keller chart exponent `p = 3`, and
  the theorem is uniform in `p`.
* **(72,108) pentagons, case (2) over `Q̄`, the 167 above-125 targets, H1c, the
  irreducibility sieve, the eliminant, chart coverage.** `NOT-FETCHED` — see the banner; they exist on `az3geq`.
  No verdict is possible and none is claimed. These need their session 19–38 artefacts
  restored before Step 4 of the plan can run at all.
* **Paths A–E (sessions 39–42).** Only Path A's descent computation exists as code; it
  is now fully certified plus its three unchecked claims. A1 ("is the `h²` square
  forced?"), B1–B4, C1–C4, D1–D2, E1–E4 remain untouched.

---

## 5. Reproduce

```
./run_all.sh          # every certifier, archive and new; nonzero exit on any failure
```

Current status: **all 15 archive re-runs clean; all 12 new certifiers pass** —
193 exact checks under sympy and 47 under PARI/GP, no shared code between them.

| certifier | checks | subject |
|---|---|---|
| `E1_master_identity.py` | 17 | re-derives the Sessions 16-18 master identity from symbolic framework data |
| `E2_endgame_classification.py` | 25 | complete rational solution set of `T_{D,m}(R) = κ` |
| `E3_pari_crosscheck.gp` | 35 | the same, in PARI/GP, independent code |
| `E4_pole_admissibility.py` | 20 | the ladder bound `u(W~₋₅) ≥ 3` |
| `E5_propagate_tower.py` | 27 | propagation of the unique `R` up the tower; both closures |
| `E6_transfer_general.py` | 21 | the corrected transfer theorem |
| `E7_alpoge_audit.py` | 23 | Alpöge map + Session 39 descent, incl. its three unchecked claims |
| `E8_pari_alpoge.gp` | 12 | the same, in PARI/GP, independent code |
| `E9_archive_certificate_audit.py` | 24 | reproduces the archive's own certificates; `h0 = −13 n₃` |
| `EA_unconditional_refinements.py` | 9 | exactly where genericity enters Theorem C |
| `EB_theorem2_robustness.py` | 8 | the closure holds for every admissible boundary polynomial `g` |
| `EC_10872_instantiation.py` | 19 | the (108,72) instantiation: all 9 admissible charts close |
