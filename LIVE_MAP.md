# LIVE MAP — territory after the audit


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

**Step 2 of the plan: reopen and rank. Step 6: terminal state for this iteration.**

Every claim that fails fact-check reopens a region; every claim that is repaired
re-closes one. Here is the board after `TRUST_MAP.md` and `L4_ENDGAME_REPORT.md`.

---

## What moved

| region | before this session | after |
|---|---|---|
| (99,66) First Framework | closed, by a proof whose decisive step was invalid and whose supporting certificates were lost | **closed, at proof standard** — neither closure using THEOREM 2 or THEOREM 3; PR #9 shows the two legs are one statement, and closes it on `k ≡ 4 (mod 5)` instead |
| Second Framework (435,290), `D_chain = 23` | "dies if the transfer conjecture holds"; the conjecture was unproved and its Phase-0 Belyi rederivation not started | **closed** — the corrected transfer theorem kills it without touching any Belyi data |
| isotope series | "to be checked" | **closed** by the same theorem, uniformly |
| (108,72) framework route | dead only conditionally on THEOREM 2/3, "possibly not dead at all" | **closed for every admissible chart** — 9 admissible edge vectors enumerated, 7 give a unique endgame solution of map-degree 4, 2 give none at all; no chain degree is 4 |
| THEOREM 2 (boundary rigidity) | "highest single lever on the board" | **lever removed.** The verdict is independent of it (`EB`), and its own conclusion `U \| g` follows from an integrality congruence |
| THEOREM 3 (pole-fiber ⇒ `R` polynomial) | load-bearing, certificate lost | **not needed by either closure.** Its conclusion is also *false as a hypothesis-free statement*: `R` is not a polynomial, it has a 4th-order pole |
| the `T_{D,k}(R) = −c` object | "unsolvable" verdict broken for `k ≥ 1` | **solved completely.** Unique solution, pole order exactly 4, map-degree 4. The "broken verdict" is real; the branch it opens is real; and it dies one layer up |
| Alpöge map / Session 39 descent | certified for 8 claims, 3 claims asserted but unchecked | **all 11 certified**, under two toolchains |

**Net: the framework route is now closed everywhere it was reachable, and closed by
arguments that survive the loss of the campaign's transcripts.** That is the opposite of
what the audit was expected to produce, and it is the honest result.

---

## Ranked live territory

### 1. `max ≥ 125` — the only genuinely unsearched region
`41.md` records 804 admissible degree pairs above 125 and 167 enumerated targets, of
which ~150 were never run. **Blocked here:** neither the pair list, the target list, nor
the enumeration code is in this repository. Unblocking needs the session 19–38 artefacts,
or a re-enumeration from GGV's shape analysis.

Note that Path D's two blockers are *unchanged* by this session: `L` is still not a
function of the degree pair, and the constraints still turn cubic at `L = 5`. The endgame
theorem does not touch either.

### 2. (72,108) pentagons — no verdict has ever been recorded
`41.md` and the plan both list this as open. **Blocked here:** the 58-parameter /
60-condition system is not in this repository. Its stated failure mode was RAM, not
mathematics; on this machine (15 GB, 4 cores) a sparse exact run is plausible *if the
system is supplied*.

### 3. (72,108) case (2) over `Q̄` — mod-`p` EMPTY only, promotion forbidden
13 variables over a degree-1144 number field. **Blocked here:** the system is not in this
repository. This is the one place where a mod-`p` result is standing in for a `Q̄` result,
which the campaign's own standard forbids.

### 4. Paths A–E (sessions 39–42) — only Path A has any code
* **A1 — is the `h²` square forced?** The single sharpest open question with a concrete
  object attached. Session 39's own script never checked that `h = f₃/x`, that a colliding
  point lies on `h = 0`, or that `h²` is intrinsic; all three are now certified (`E7`),
  which strengthens the case that the square is structural. The general-weights
  computation remains undone.
* **B1** (literature: is the plane weighted-homogeneous Keller case a theorem?),
  **C4** (Orevkov, before day five), **E-abort check** (does `arXiv:2608.00222` say in its
  first section that its construction is a sweep generalisation?) — three cheap reading
  tasks that each gate a multi-day path. None was done.
* **C2** — the `d = 2` pincer (Geiser/Bertini against the `S_F` enumeration) is the
  campaign's largest available single result after the bound to 125, and is untouched.

### 5. Closed, do not re-run
The whole Borisov framework family, at every degree pair, for every chain degree `≠ 4`.
This includes the `N2_prompt.md` sub-campaign in its entirety: its Phase 0 (rederive the
degree-23 Belyi map from its ramification profile) is **unnecessary work** — the
obstruction is upstream of the Belyi coefficients.

---

## Terminal state for this iteration

The loop's two honest termini are *an explicit `(P,Q)` through the HIT protocol* and
*proof-standard emptiness for a region*. This iteration reached the second, for the whole
framework family.

* **No candidate pair was produced.** The constraint stack was driven to the bottom: the
  endgame equation has exactly one solution, it is explicit, and it fails the next layer
  up by a margin (map-degree 4 against 13) that no choice of scalars, boundary polynomial,
  or chart can close.
* **The HIT protocol was not invoked**, because nothing reached it. That is recorded
  rather than glossed.
* **What is now needed to continue** is not more mathematics on this route — it is the
  restoration of the session 19–38 artefacts, without which Steps 2 and 4 of the plan
  cannot address the regions they name. The precise list is in `TRUST_MAP.md` §4.

The framework door is not merely locked. It is now locked with a key that does not depend
on anything the campaign has lost.
