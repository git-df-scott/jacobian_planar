# Handoff to the Counter-example Audit session

From: the Opus 5 session executing `OPUS_PLAN.md`'s priority queue
Branch: `claude/opus-plan-priority-queue-0pultj` (PR #4, based on
`claude/counter-example-audit-dnu9l9` so the diff is only this session's work)
Window: 2026-08-13 22:00Z - 2026-08-14 04:30Z

Read this in the order given. Item 1 bears directly on the "polygon recipe
gate" your last status line mentions, and item 6 is the one that changes what
can be claimed about (72,108).

Verdict vocabulary throughout is OPUS_PLAN rule 6: EMPTY / ALIVE / STALLED,
nothing else. **No counterexample. No non-EMPTY verdict anywhere. Nothing
reached the gate.**

---

## 1. P3 is blocked: the above-125 Newton polygons are not published anywhere

This is a hard escalation (OPUS_PLAN §E, "any shape-derivation ambiguity in
P3a") and it is probably the most useful thing in this document for you.

- `trackE_literature_verified.md` §E6 extracts 1708.07936 §6 verbatim. Those
  tables give **chain data only**: A0, A1, ..., (m,n), and max degree. Example
  rows: (75,125) is family F2 with (m,n) = (3,5); (84,126) is the length-1
  chain A0 = (7,35), A1 = (19/7,5), (m,n) = (2,3); (126,84) is the length-2
  chain (12,30)/(16/3,10)/(11/6,3) with (m,n) = (3,2). **No Newton polygon
  appears in those tables at all.**
- The polygons the campaign uses come from GGHV arXiv:2204.14178 Prop 4.3,
  which states N(P), N(Q) for the (8,28) shape explicitly.
  `trackA_gghv_system.py` is built on that verbatim statement.
- Checked against the full text this session (ar5iv): §4 contains
  Prop 4.1 (case (9,27)), 4.2 (case (9,24), three subcases), 4.3 (case (8,28),
  two subcases), 4.4 (case (7,21)) — **only below-125 shapes**. The paper gives
  **no explicit polygons for any pair above 125**.
- §4's derivations are explicitly case-by-case by hand, with automorphisms
  chosen per case: "In this section we apply some automorphisms reminiscent of
  the procedure in section 8 of the ArXiv version of [6] ... to the Newton
  Polygons in order to greatly reduce their sizes." **There is no general
  recipe** from chain data to a polygon pair.

Consequence: P3b-P3d (generalize the builder over vertex lists, eliminate,
close, verdict) are mechanical and ready — the builder already takes vertex
lists — but their input does not exist in the literature. Producing it means
redoing GGHV's §4 geometry for chains they never treated. A guessed polygon
gives a system that is not the case in question, and an EMPTY verdict on it
would read as a bound improvement while being worthless.

**Engine calibration, done anyway, and it is informative.** msolve on the RAW
case-(2) system (`trackA_system_case2.json`, hash f27a28a2..., 72 unknowns /
92 equations, plus one Rabinowitsch tie = 73 vars / 93 polys) grew past 10GB
in ~8 minutes and was killed without a verdict. Under an explicit
address-space cap it dies inside monomial hash-table growth instead.
**Conclusion for any above-125 plan: assume the elimination-first pipeline,
not a direct GB, whatever the engine.**

## 2. P0 pentagon endgame: STALLED, with numbers

`--tower-check` had been dead since the pause commit — appending `tower_lift`
overwrote `tower_check`'s `def` line, leaving its body as unreachable code
after a `return`, so the entry point raised NameError. Header restored, no
logic touched. **T1 now PASSES** (raw-vs-assembled residual agreement on 5
random full assignments; level-20 equation count 19).

Per-sample cost, p = 65521, sample a = 8806, b = 37304,
S = [1, 55537, 52577, 50054, 4136], ntau = 53, kernel dims
9,9,8,8,6,5,4,3,1 then 0 (reproducing the report's profile exactly):

| level | std | slimgb |
|---|---|---|
| 19 | 0 s, 2 MB | 0 s, 2 MB |
| 18 | 0 s, 2 MB | 0 s, 2 MB |
| 17 | 79 s, 150 MB | 172 s, 524 MB |
| 16 | >1400 s, 1.8 GB, unfinished | killed after losing level 17 |

Nine levels lie below 16, and Structure Theorem 1 puts any kill below all of
them. So T2's ">= 10k samples" is off by ~4 orders of magnitude and T4's
4.47M-sample sweep by three more. T5's tickets both lost: slimgb is worse than
std (above), and msolve on the full 166-variable pentagon system dies in
hash-table growth. Engine is now switchable via `JCENGINE=std|slimgb`.

**Why it is expensive, structurally** (offered as input, not a result). The
level-w map is (A,B) |-> 3bS^2[A,S] + 2aS[S,B] = S*[S, 2aB - 3bSA], so its
kernel is {(A,B) : 2aB - 3bSA in Cent(S)} — the new P-component A is
unconstrained at its own level. That is why ntau = 53 = the number of
P-coefficients below the top, and why the obstruction ideal stays far from 1
through the whole upper tower. The cost driver is the 53 free A-directions
carried as ring variables. Whether the right fix is the deviation coordinate
G := b^2 P^3 - a^3 Q^2 (leading form cancels by construction; the pentagon
analogue of the cusp function c2 = y1^2 - y2^3 that carried Sessions 16-18) is
a Fable-grade call, recorded only because it is cheap to say.

**No verdict on case (1).**

## 3. P1 exact-Q: STALLED, but the blockage is now ONE identified computation

Both routes P1 specifies were run to exhaustion. The ladder:

| what | engine | outcome |
|---|---|---|
| per-branch closure, mod p | Singular std, staged | **works** — seconds to minutes per branch |
| char-0 edge eliminant | groebner + eliminate + factorize | no output in >1h, twice |
| char-0 edge eliminant | modStd | no output in 10 min |
| monolithic chart, char 0 | groebner | no output in ~55 min |
| monolithic chart, char 0 | modStd | no output |
| **monolithic chart, mod p** | groebner | **no output in 10 min** |

The last row is the diagnostic one: the monolithic chart is hard *even mod p*,
so P1's prescribed fallback was never going to work over Q. Its difficulty is
the undecomposed system, not coefficient growth. What makes case (2) tractable
is the staged decomposition (pin an edge point, close a small residual), and
the exact-Q analogue needs the same. Its gate is one computation:

> **the char-0 edge eliminant: 7 variables, 6 equations plus d_3_3 = 1, with
> coefficients like 1094125239/455785946.**

**msolve cracks its first phase.** Exported with denominators cleared per
generator (`trackB_edgeQ.ms`), msolve reports
`Elimination polynomial has degree 1144` and enters multi-modular
reconstruction at ~170 MB. **Degree 1144 is your own number** — RESUME_STATE
records "their vdim 1144 / deg-43 eliminant story lived in this slice", so the
two epochs agree on the size of the object. Status at handoff: still
reconstructing (prime count doubling, {3}...{513}). If it lands, the
per-branch exact-Q route it gates becomes viable.

**A shortcut rejected as unsound.** Every branch is EMPTY mod three primes and
it is tempting to promote that to a Q-statement. It does not follow:
I = (p*x - 1) is (1) mod p while V(I_Q) = {1/p} is nonempty. mod-p stays
scouting.

**A route left implemented but unevaluated.** `trackB_certsupport.py`: use mod
p to find which handful of generators carry nonzero cofactors in
1 = sum h_i f_i (the *support*), then run the char-0 lift on that subset alone
— a verified certificate is a proof however it was found. Note the cofactors
themselves cannot be CRT-reconstructed across primes: `lift`'s output depends
on the computation path and is not canonical, so only the index set carries
over. It could not be evaluated because its own first step is the monolithic
mod-p GB in the table; it needs the staged decomposition applied first.

**Case (2) is closed mod p at three primes and STALLED over Q. Not certified.**

## 4. P2 leaf 1: 21 branches EMPTY across three primes, in flight

Leaf 1 (d_2_2 = 0) is the slice the Sessions 19-20 hunt actually lived in,
closed by them mod 65521 only and through the unsound R1 pipeline. Our staged
pipeline is now leaf-parametrized (`JCLEAF`, default 2) and **derives** the
Newton-edge equation indices from the equations rather than hardcoding
[38..43]; leaf 2's indices are pinned by assertion as a regression check.
Leaf 1's indices are [34..39] — the same six equations, so the edge subsystem
is shared. Leaf 1's eliminant reproduces **ELIMDEG 43**, matching leaf 2 and
the handoff's deg-43 story: an independent cross-check.

State at handoff: p=65521 complete; p=65539 all but its terminal r0b branch;
p=65599 through rk0-rk3 and the r0a branches; 21 EMPTY total. The terminal
branch is re-running under a 9000 s budget. Then leaf-1 exact-Q.

## 5. P4 / C2: the handoff's D(k) is wrong, and it manufactures a death

C2 is COMPLETE (`python3 trackC_phase4.py c2`, 5 PASS 0 FAIL, artifact
`trackC_c2_tenR.json`).

- D(k) DERIVED from C1's q-order matching: **D = (a+b)k + 1 - s = 5k - 2** in
  the handoff frame. **The handoff's D = 3k+4 is wrong.** It agrees at k = 3
  (13 = 13) and diverges from k = 4 on (18 vs 16). Not cosmetic: under the
  guessed D the k = 4 slice returns `DEAD_resonance`, i.e. **the wrong relation
  manufactures a spurious death** where the derived one gives a forced R. Any
  handoff statement about k >= 4 that leaned on D = 3k+4 must be re-read.
- All ten slices k = 3..12 carry a forced R, deg S = 4, each passing the exact
  block check, each unique up to a scalar absorbed by alpha^(a+b).
- Pole order p = (a+b)m - 1 = 4 is EXACT, not an upper bound: S(-1) != 0 for
  all ten, via E(-1) = -(Dm - kp)S(-1) = -c.
- k = 3 cross-check: our forced S is **identical** to the handoff's
  243v^4 - 81v^3 + 54v^2 - 42v + 35. |c| = 455 agrees; the sign does not (ours
  +455 in the C1e-verified convention, handoff -455). Convention, not
  mathematics — but pin it before comparing any c across epochs.

The full table of ten (k, D, S, c) is in `trackC_report.md` §C2.

## 6. C3: layer 1 certified and anchored — and a GAP that limits every (72,108) claim

**Certified** (`trackC_c3_ladder.py`, 13 PASS; `trackC_c3_anchor.py`, 5 PASS):

- L1 the formal (b/a)-th root exists and is unique with S_0 = 1, verified to
  order 8 with generic T for (2,3), (2,5), (3,5), (4,7). The (2,3) case is
  Sessions 12-14's THEOREM 1, independently re-derived.
- L2 chain <=> square-root agreement: all W-blocks below the deviation order
  vanish iff Delta = O(x^D).
- L3 the first surviving block is **2 g^6 delta** — the deviation enters
  LINEARLY, which is the structural reason the endgame is an ODE in R.
- L4 a ladder operator deciding "g^b S_m polynomial" per (g, tower). Sanity
  check: perturbing level 2 off the divisibility breaks the ladder first at
  **level 4**, correct because g^3 g^-2 is still polynomial and the pole only
  bites once T_2^2 brings g^-4.
- **Anchor against certified data**: on the Session-7/10 near-miss,
  B~_-6 = U^2 (U-1)^16 exactly, so g = **U (U-1)^8** — Sessions 12-14's
  THEOREM 2 boundary form falls out DERIVED, on the near-miss. And
  **A~_{-9+m} == g^3 S_m for every m = 0..12**, all thirteen levels: the
  S-side from this session's generic engine, the A-side from Session 10's
  certified Belyi expansion. Two independent code paths, different epochs,
  exact agreement — a cross-epoch validation of the same kind as h0 = -13 n3.

**NOT certified, and both load-bearing:**

- **THEOREM 2 at general parameters.** The anchor confirms g = U(U-1)^8 *on the
  near-miss*. The theorem claims every framework solution has this boundary
  polynomial up to one scalar, via the Taylor-pin argument. One worked point
  is not a rigidity proof.
- **THEOREM 3 (pole-fiber => R is a polynomial).** Not reproduced at all. C1
  forces the pole *order*; the fiber-counting step that makes R a *polynomial*
  is missing, and its argument runs on D = 13's Belyi fiber sizes (13/9/5/1),
  which (72,108) does not share.

> **Every (72,108) statement that assumes a polynomial R inherits this gap —
> the C2 table of ten forced R's included.** That table is correct *given*
> polynomiality; it is not independent of it.

Sessions 11-14's executable engines died with the transcripts, which is why
this had to be re-derived rather than imported. Session 10 is executable and
Track-F-certified and was the only inherited input.

## 7. C4 refined sweep: the ODE layer does not discriminate

`trackC_c4_refined_sweep.py` runs the framework's own obstruction chain over
every refined slice (rho(s-1) = 1 mod 5, rho,s <= 12) for m = 1..8, k = 1..14.
**22 of the 23 slices carry a forced R.** The only death is (1,2), precisely
the sigma = 0 slice where k*t + D*sigma = 0 forces c = 0.

So C4 cannot be settled by the forced-R machinery; the discrimination must
come from the realization/boundary layer — which is C3 layer 2, gated by the
THEOREM 2/3 gap above. A useful negative rather than a narrowing.

Bookkeeping worth having: the 23 slices contain the baseline **(3,3)** (the
handoff frame is rho = s = 3) and the degenerate **(1,2)**. "22 unexamined"
from `trackC_phase4.py c4` means 23 minus the baseline, keeping (1,2). A list
of 22 that keeps (3,3) and drops (1,2) is a different set. **(3,1) is not a
slice at all** — rho = 3 forces s = 3 (mod 5).

Three further filters were proposed to us and are documented as assessed and
NOT applied, because none follows from the C1 relations: a (72,108)
integer-combination match on (D, sigma) — ill-posed, since D = 5k+1-s varies
with k inside a slice, and measured to discard 58% of live instances;
sigma <= 0 with c > 0 — sigma <= 0 holds lattice-wide so it filters nothing,
and c's sign is convention-dependent (our +455 vs the handoff's -455 for the
same S); and integrality of primitive S — vacuous, since S is fixed only up to
a scalar that alpha^(a+b) absorbs. The framework's real arithmetic
obstructions, already in the chain, are the divisibility sieve k | D(m+sigma)
and the resonance test.

## 8. Environment facts that will cost you time if you rediscover them

- **The container can come up with no Singular.** `apt-get install -y singular`
  (4.3.2); `apt-get install -y msolve` adds msolve. Every campaign script
  assumes Singular on PATH. After a *restart* both survive; a *fresh container*
  has neither.
- **Container lifetime ~1-2.5h, measured** (two restarts this session). Any
  monolithic Groebner run budgeted beyond ~2h cannot land, whatever timeout it
  carries. Prefer marker-resumable per-branch pipelines: a restart costs one
  stage there and the whole run otherwise.
- **modStd forks one worker per prime and ignores `system("--cpus", n)`** —
  measured 15 Singulars on a 4-core box. Pin with `taskset` or it starves
  everything else.

## 9. Bugs found and fixed (all were failures that printed as successes)

1. `tower_check` overwritten by `tower_lift`'s append — entry point raised
   NameError while the report claimed PASS.
2. **`echo "$(date ...) exit=$?"` masks the exit code.** The command
   substitution runs first, `date` succeeds, so `$?` is *date's* status. A
   sweep that died on TimeoutExpired logged `exit=0`. Every exit code those
   chain scripts ever logged was `date`'s. Fixed by capturing `rc=$?` first.
3. `trackB_exactQ.py` cached an **empty** factor list when the eliminant timed
   out; on rerun that skipped every rk-branch and would have read as a
   closure. Now refuses to write the marker.
4. `trackB_leaf1_sweep.py` wrote its eliminant cache but never read it,
   recomputing the factorization on every restart.
5. Stage timeouts were hardcoded; a branch needing longer silently lost its
   verdict. Now `JC_ST1_TIMEOUT` / `JC_ST2_TIMEOUT`.
6. Editing a shell script while bash is executing it can make bash resume
   mid-command (it reads by byte offset). Two scripts were retired rather than
   trusted after in-place edits.

## 10. What I would do next, in order

1. **Rule on the polygon question (item 1).** Everything in P3 waits on it and
   nothing else in the queue does. If reproducing GGHV §4 for new chains is in
   scope, say so and name the method; if not, P3's CPU should go elsewhere.
2. **Finish the msolve edge eliminant (item 3)** and, if it lands, rebuild the
   per-branch exact-Q route on top of it. That is the shortest path to a
   theorem-grade case-(2) closure.
3. **Decide THEOREM 3 (item 6).** It is a mathematical argument, not a machine
   check, and it currently limits what the entire (72,108) line may claim.
4. Leaf-1 exact-Q, once its three primes finish.
5. P0 only after a reformulation that removes the 53 free A-directions before
   the GB. Re-running the tower as specified will reproduce the same wall.

## 11. Where things are

Branch `claude/opus-plan-priority-queue-0pultj`, PR #4 (draft, based on your
branch). Key documents: `FABLE_REVIEW.md` (the three escalations),
`AUDIT_REPORT.md` (session addendum), `trackC_report.md` (C2/C3/C4),
`trackB1_report.md` §B1d (pentagon verdicts), `RESUME_STATE.md` (resume
commands and environment gotchas). New code: `trackB_leaf1_sweep.py`,
`trackB_leaf1_driver.sh`, `trackB_exactQ_fallback.py`,
`trackB_certsupport.py`, `trackB1_msolve_export.py`,
`trackC_c4_refined_sweep.py`, `trackC_c3_ladder.py`, `trackC_c3_anchor.py`,
`trackW_formulation.md`.
