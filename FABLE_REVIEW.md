# FABLE REVIEW — escalations from the Opus 5 priority-queue session

Written per OPUS_PLAN.md §E. Two items. Item 1 is a hard escalation trigger
("any shape-derivation ambiguity in P3a") and blocks P3 as written. Item 2 is
a measured infeasibility that turns T2/T4 of P0 into STALLED-with-data rather
than a verdict; it is reported now so the next session does not re-spend the
same CPU discovering it.

Nothing here is a non-EMPTY verdict. No candidate has reached the gate. No
suspicion of unsoundness in the reduction machinery has arisen.

---

## Item 1 (BLOCKING, P3a) — the above-125 Newton polygons are not published anywhere

**The plan's premise.** P3a says: "derive the GGHV-style shape (Newton
polygons, bracket RHS) FROM 1708.07936's tables — document the derivation in
trackD_<pair>.md; this step is judgment-adjacent: if the shape derivation is
ambiguous, ESCALATE rather than guess."

**What the sources actually contain.**

- `trackE_literature_verified.md` §E6 extracts 1708.07936 §6 verbatim. Those
  tables give, per admissible pair, only the **chain data**: A0, A1, ... and
  (m, n), plus max{deg P, deg Q}. Example rows: (75,125) is family F2 with
  (m,n) = (3,5); (84,126) is the length-1 chain A0 = (7,35), A1 = (19/7,5),
  (m,n) = (2,3); (126,84) is the length-2 chain (12,30)/(16/3,10)/(11/6,3)
  with (m,n) = (3,2). **No Newton polygon appears in those tables at all.**
- The polygons the campaign works with come from the *other* paper:
  GGHV arXiv:2204.14178 Proposition 4.3 states N(P) and N(Q) for the (8,28)
  shape explicitly, and `trackA_gghv_system.py` is built on that verbatim
  statement ("reconstruct, from GGHV arXiv:2204.14178 Proposition 4.3 ALONE").
- Checked against the paper this session (full text, ar5iv):
  - §4 contains Propositions 4.1 (case (9,27)), 4.2 (case (9,24), three
    subcases), 4.3 (case (8,28), two subcases), 4.4 (case (7,21)) — i.e.
    **only below-125 shapes**.
  - The paper gives **no explicit Newton polygons for any pair with max degree
    above 125** — not (75,125), (84,126), (96,128), (88,132), (90,135).
  - §4 derives its polygons **case by case, by hand**, with automorphisms
    chosen per case: "In this section we apply some automorphisms reminiscent
    of the procedure in section 8 of the ArXiv version of [6] ... to the
    Newton Polygons in order to greatly reduce their sizes." There is **no
    general recipe** taking chain data to a polygon pair.

**Why this blocks P3 rather than slowing it.** Steps P3b-P3d (generalize
`trackA_gghv_system.py` over polygon vertex lists, eliminate, close, verdict)
are mechanical and ready — the builder already takes vertex lists. The input
they need does not exist in the literature. Producing it means redoing GGHV's
§4 geometry for chains they never treated: choosing the automorphism sequence
that shrinks each chain's polygon, and proving the reduction is
emptiness-sound. That is exactly the Fable-grade derivation P3a says not to
guess at. A guessed polygon yields a system that is *not* the case in
question, and an EMPTY verdict on it would be worthless — worse, it would read
as a bound improvement.

**What is safely available without a ruling.** The degree-pair list, the chain
data, and the ordering of targets are all verified and on disk (E6). The
system builder, eliminator, staged closure, and now an msolve route are all
pair-agnostic. The moment a polygon pair is fixed for (75,125), the rest is
CPU.

**Ask.** Either (a) a ruling that reproducing GGHV's §4 reduction for the
above-125 chains is in scope, with the intended method; or (b) redirect P3's
CPU to the tracks that still have well-posed inputs (P1/P2 exact-Q work, and
the pentagon endgame's bottom-weight structure, item 2).

**Engine calibration (P3's first step) — done, and it says something useful.**
P3 says to benchmark the new engine on the known-EMPTY (8,28) case-(2) system
before starting. msolve was installed and pointed at exactly that: the RAW
hash-pinned case-(2) system (`trackA_system_case2.json`, f27a28a2..., 72
unknowns / 92 equations, plus one Rabinowitsch tie for the six vertex
conditions = 73 vars / 93 polys), p = 65521, DRL, 2 threads. It grew past
10 GB in about 8 minutes and was killed by the kernel without producing a
basis or a verdict. Under an explicit address-space cap it instead dies inside
its monomial hash-table growth. Conclusion for planning: **msolve is not
usable on the raw, un-eliminated systems of this family on this box** — the
campaign's elimination-first pipeline (sound or-branching, edge eliminant,
per-branch staged closure) is not an accident of taste, it is what makes these
systems finite. Any above-125 plan should assume the same pipeline, not a
direct GB, whatever the engine.

---

## Item 2 (measured, P0/T2 and P0/T4) — per-sample tower cost is 4-6 orders of magnitude off

**Status of the machinery.** T1 is green. `--tower-check` had been lost — the
pause commit's append of `tower_lift` overwrote its `def` line and left the
body as dead code after a `return`, so the entry point raised NameError. The
header is restored and the check PASSES (raw-vs-assembled residual agreement
on 5 random full assignments; level-20 equation count 19). The tower is
validated against the raw hash-pinned system, as the plan requires.

**The measurement** (p = 65521, sample a = 8806, b = 37304,
S = [1, 55537, 52577, 50054, 4136], ntau = 53, kernel dims
9,9,8,8,6,5,4,3,1,0,...  — reproducing the report's profile exactly):

| level | engine std | engine slimgb |
|---|---|---|
| 19 | 0 s, 2 MB | 0 s, 2 MB |
| 18 | 0 s, 2 MB | 0 s, 2 MB |
| 17 | 79 s, 150 MB | 172 s, 524 MB |
| 16 | > 20 min, 1.5 GB, unfinished | (killed after the level-17 loss) |

Nine more levels lie below 16, and Structure Theorem 1 says the kill — if
there is one — lives at weight <= 7, i.e. below *all* of them.

**Consequences for the plan as written.**

- T2 (">= 10k random samples") at even 25 min/sample is ~170 CPU-days, and
  sample 0 does not finish in 25 min. Not viable.
- T4 (exhaustive p = 31: 5 x 31^3 x 30 = 4,468,650 samples) is out by a
  further three orders of magnitude. The report already flagged this and made
  it conditional on "a shallow closed-form death criterion"; that criterion
  does not exist yet, and finding one is Fable-grade.
- T5's engine idea was tried in both available forms. slimgb is worse than std
  (table above). msolve (F4, installed this session) was pointed at the full
  normalized pentagon system (284 polys / 166 vars, source hash 094bcd93) and
  died in its hash-table growth; a calibration run on the *known-EMPTY*
  case-(2) system (73 vars) is the honest test of whether msolve is usable on
  this family at all, and is in flight as of writing.

**The structural reason, stated plainly** (offered as input, not as a
conclusion). The level map at weight w is
(A, B) |-> 3bS^2[A,S] + 2aS[S,B] = S*[S, 2aB - 3bSA]. Its kernel is therefore
{(A,B) : 2aB - 3bSA in Cent(S)} — i.e. A (the new P-component) is
unconstrained at its own level and only bites lower down. That is why ntau
equals the number of P-coefficients below the top (53) and why the obstruction
pile stays far from 1 through the whole upper tower: the GB is being asked to
work hard on an ideal that is not close to collapsing until the bottom
levels. Any reformulation that removes the free A-directions before the GB
(rather than carrying them as 53 ring variables) would attack the actual cost
driver. Whether the right such move is the deviation coordinate
G := b^2 P^3 - a^3 Q^2 — whose leading form cancels by construction, and which
is the pentagon analogue of the cusp function c2 = y1^2 - y2^3 that carried
Sessions 16-18 — is a Fable-grade call, not mine, and is offered here only
because it is cheap to say and expensive to rediscover.

**What was NOT concluded.** No verdict on case (1). The pentagon system is
neither EMPTY nor ALIVE on this evidence; it is STALLED, with the
instrumentation above.

---

## Item 3 (measured, P1) — exact-Q closure is blocked at one identified computation

P1's own instruction was to run `trackB_exactQ.py`, and if the char-0 eliminant
factorization exceeded ~3h, to fall back on per-chart closure without the
eliminant. Both routes were run. Neither lands, and the reason is now precise
enough to hand to whoever picks it up.

**The measurement ladder** (leaf 2, case (2), 44 equations / ~24 variables):

| what | engine | outcome |
|---|---|---|
| per-branch closure, mod p | Singular std, staged | **works** — seconds to minutes per branch; this is what closed case (2) at p = 65521, 65539, 65599 |
| char-0 edge eliminant (the per-branch route's gate) | groebner + eliminate + factorize | no output in >1h, twice |
| char-0 edge eliminant | modStd (modular + rational reconstruction) | no output in 10 min |
| monolithic chart, char 0 | groebner | no output in ~55 min, killed by container restart |
| monolithic chart, char 0 | modStd | no output |
| **monolithic chart, mod p** | groebner | **no output in 10 min** |

The last row is the diagnostic one. The monolithic chart is hard *even mod p*,
so the fallback route was never going to work over Q — its difficulty is not
coefficient growth, it is the undecomposed system. What makes case (2)
tractable mod p is the staged decomposition: pin an edge point first, then
close a small residual system. The exact-Q analogue needs the same
decomposition, and its gate is a single computation:

> **the char-0 edge eliminant: 7 variables, 6 equations plus the
> normalization d_3_3 = 1, with coefficients like 1094125239/455785946.**

Everything downstream of that is small and already written. That one
elimination is the whole blockage.

**A route that was considered and rejected as unsound.** Since every branch is
EMPTY mod three primes, it is tempting to promote that to a Q-statement. It
does not follow: I = (p*x - 1) is the standard counterexample — it is (1) mod
p while V(I_Q) = {1/p} is nonempty. The campaign's rule that mod-p is scouting
only is correct and was not bent.

**A route that remains open and is probably the right one.** `trackB_certsupport.py`
implements it: use mod p to find which handful of generators carry nonzero
cofactors in the certificate 1 = sum h_i f_i (the *support*), then run the
char-0 lift on that subset alone. A certificate that verifies over Q is a
proof however it was found, and the mod-p step contributes only a hint about
where to look. Note that the cofactors themselves cannot be CRT-reconstructed
across primes — lift's output depends on the computation path and is not
canonical — so only the index set is carried over. The script could not be
evaluated here because its own first step is the monolithic mod-p GB in the
table above; it needs the staged decomposition applied to it first, which is
the natural next build.

**Verdict vocabulary.** Case (2) is closed **mod p at three primes** and
**STALLED over Q**. It is not certified. The AUDIT_REPORT reflects this.
