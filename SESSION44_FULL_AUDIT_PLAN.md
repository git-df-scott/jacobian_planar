# Session 44 — FULL AUDIT PLAN: where a missed counterexample would hide

Date: 2026-08-27. Branch `claude/past-code-session-8mdjqn`. Status: PLAN,
per instruction — audit and design, execution only where already launched.
Binding gate unchanged: a CE is explicit char-0 `P,Q`, exact `[P,Q]=1`
coefficientwise, and two distinct points with one image. Everything below is
about *finding* that object or the crack that hides it.

---

## Part 0 — The ten lenses, mapped onto THIS campaign's data

Each lens names a concrete target in our own artifacts. This is the audit's
organizing table; Part 1 turns it into a sweep.

| # | Lens | What it points at here | State |
|---|------|------------------------|-------|
| 1 | Blue LED | The 24 published never-attacked shapes (FABLE_24), esp. (8,28)/(3,4)/144; and *representations we never built* — the topological/monodromy representation (built this session), construction-from-tear at d≥6 | sieve built + run |
| 2 | O-rings | Exceptional loci of our own parameterizations: the u=0 chart of the (4,6) ribbon (found: quartic 2v⁴+3vw²+18w=0, ~20 free kernels); sol5's "exceptional shear locus where Macaulay rank drops"; Sol-4 pentagon strata a₀=0, F₃=0 never decomposed | u=0 found this session; rest queued |
| 3 | Penicillin | The anomaly register: d=12 unsaturated cell ("degenerate family?", uniquely resistant); the 0.95-residual polygon wall; deep-depth scan points; (9,27) Cor 5.7 independent test whose outcome was never recorded | register drafted below |
| 4 | Neptune | Residuals as data: the degree-144 reverse-lift defect (~2.5e3, structured); the obstruction polynomials O₁,O₂,… of the (u,v,w) hunter — solve them, don't sample them | hunter built + calibrated |
| 5 | H. pylori | Assumptions shared by ALL lanes: vertex-nonvanishing; GGV/GGHV shape classification itself (two adjacent papers already yielded a misprint + a gap); "char p is uninformative" (tested this session: refined invariant, still negative in box); "tear irreducible" | audit steps below |
| 6 | Apollo 13 | Adapters: numeric→modular→Hensel→exact as a standing certified pipeline (interval-Newton/alpha certifier on python-flint arb); staged linear eliminator to replace OOM-bound monolithic Gröbner (msreduce exists, cascade unbuilt — the campaign's own P2) | design below |
| 7 | Kepler | When a family leaves the same structured obstruction, derive it and change geometry: the (2,3) ribbon died this way; the (4,6) obstruction tower is next; the polygon wall (vertices) is the standing Kepler residual of four independent routes | partially executed |
| 8 | AlphaFold | Mine every recorded kill/survivor for structure before eliminating: needs the artifact consolidation in Part 2 (sessions 19–38 restoration) | blocked on Part 2 |
| 9 | PageRank | The survival graph over shape families (nodes = corners/chains, edges = degenerations/shears); tells us which of the 24+41+429 unexplored families neighbor survivors | blocked on Part 2 |
| 10 | Einstein | New normalizations where noninjectivity is automatic: collision-first (exists), slice/Path-S (Session 43), monodromy-first (this session: prescribe the covering, derive the map), quotient/involution-first (dead in char 0 — LND argument — recorded so nobody retries) | one new rep built |

## Part 1 — The evidence-grade audit (the "results came too fast" sweep)

The single highest-value audit: **classify every EMPTY verdict in the
campaign by the strength of its certificate.** Session 43 found ten bugs, one
of which (chi inclusion–exclusion) *wrongly rejected 55 real candidates*; the
mailbox ledger inventories 45+22 can't-fail checks and a rank criterion that
cannot fail; OPEN_ITEMS records that a misprinted GGV (1.2) voided a whole
day of B=16 artifacts. The same class of failure may guard a live cell.

Grades: **A** char-0 certificate replayed · **B** ≥2 independent primes +
controls · **C** single prime · **D** numerical only · **E** verdict relies
on a can't-fail check or a since-corrected system/import.

Known demotions to chase first (from STATE_FULL/OPEN_ITEMS/LIVE_MAP):
- B=16 d=7 chart N: EMPTY at p=1000003 only [MISS-1] — grade C.
- B=16 d=9,10,11 chart N: never run at all (only Z) — not even C.
- F3 x2: single prime 65521 [MISS-6] — grade C.
- (72,108) case (2): three primes, char-0 never done — grade B, and it is
  one of two shapes of the last pair below 125. The campaign's own P4.
- The legacy 180-target trackD queue: disposition "semi-superseded", never
  finished [MISS-5] — every non-EMPTY row there is an unexamined lead.
- Every verdict that imported Żołądek Lemma 4.10, GGHV Cor 5.7, or Prop 6.1
  without independent re-derivation (Cor 5.7's independent test was IN
  msolve on Aug 21 — find its output; if it was never read, that is
  Session 43's process failure repeating at the ledger level).

Deliverable: `TRUST_LEDGER.md` — one row per kill, grade, artifact path,
re-verification cost. Anything guarding live territory at grade C/D/E goes
to the re-run queue. Estimated: one session to build from the existing
ledgers; the 55-commit bundle in this repo root carries most artifacts.

## Part 2 — Restore and consolidate the record (prerequisite for lenses 8–9)

- The sessions 19–38 artifacts (804-pair enumeration, 167 targets, ~150
  never run) are NOT in any branch — LIVE_MAP names this the blocker for
  the only genuinely unsearched region. The `campaign_55commits.bundle` in
  this repo root restores `claude/opus-5-counterexample-plan-sep6yk`
  (verified: bundle is okay). Action: restore, index, and build the
  PageRank-style survival graph over every family ever touched.
- 254/478 vertex-LIVE entries are orphaned; dedup-by-hash was "pending
  morning" and never recorded. Reconcile.

## Part 3 — The anomaly register (each gets its own investigation)

1. **144 = 144 = 144.** The genuine degree-144 reduced component
   (residual 1e-14), the B=16 resonant cell d=12 (12d=144=12², rational
   roots −1/12, 1/20), and the d=12 *unsaturated* anomaly (undecided after
   2 kills while d=3 analogue is instant). Test whether these are one
   object; run d=12 unsaturated to verdict WITHOUT saturating — the
   "degenerate family" is the find, not the noise.
2. **The u=0 chart of the (4,6) ribbon** (NEW, this session). On u=0 the
   kernel-consuming coefficient (n+1)u/4 vanishes identically; rung 2
   becomes the exact quartic `2v⁴ + 3vw² + 18w = 0`, and on that curve the
   branch retains ~20 free kernel parameters. Mod-29 scan: the only
   survivors of the whole grid live here. sol6 worked only on u≠0. The
   symbolic descent (`session44/u0_descent.py`, running) maps which rungs
   bind the kernels; endgame = a small exact subsystem for the entire
   degenerate stratum of the campaign's live frontier.
3. **The polygon wall.** Four independent routes: `[P,Q]=x` solvable only
   with Newton vertices vanishing (residual pinned at 0.95 otherwise).
   Kepler reading: solutions want polygons OUTSIDE the assumed shape class
   ⇒ audit the discard steps of the shape classification itself (Part 4).
4. **(9,27)/Cor 5.7 test outcome** — locate or re-run; a non-empty reopens
   (72,108)'s second branch.
5. **Deep-depth points from the (u,v,w) scan** (any point at two primes
   surviving ≥3 obstructions past random expectation) — Hensel candidates.

## Part 4 — Attack the canon (H. pylori, full protocol)

The campaign found errors in two adjacent papers (GGV (1.2) misprint;
Żołądek 4.10 gap) but never audited the discard machinery it builds on:
- Re-derive GGHV Cor 5.7 (kills (9,27)) independently — already staged.
- Re-derive Prop 6.1 (kills F22 (2,3)).
- Verify the FABLE_24 extraction against the published PDF (their own
  caveat) and derive the Prop-4.3 analogue for the eight length-1 cases,
  starting with (8,28)/(3,4)/max-144 — same corner as the ground-out case,
  never opened. This is simultaneously lens 1 and lens 5.
- Vertex-nonvanishing discards: for ONE published shape, redo the corner
  analysis allowing a vanishing vertex and see whether the chain argument
  actually breaks or was merely convenient.

## Part 5 — New-representation program (Blue LED / Einstein, designed)

1. **Monodromy-first construction** (built this session,
   `session44/sieve_d6.py`, validated on trefoil covers, reproduces the
   entire literature floor d=2..5 from pure topology): for irreducible
   one-Puiseux-pair tears the floor extends — d=6,7,8 all EMPTY (p,q ≤ 30
   at d=6). Consequence: any CE of geometric degree ≤ 8 must have a
   reducible tear, deeper strata, or a multi-cusp/iterated-Puiseux tear.
   NEXT: extend the sieve to (a) reducible tears (2 components), (b)
   deeper-strata configurations (7 of Session 43's 83), (c) general
   one-place-at-infinity groups via Eisenbud–Neumann splice presentations.
   Survivors, if any, are construction targets with cusp data pinned — the
   first existence-side structural signal the campaign would ever have.
2. **Certified-existence adapter** (Apollo 13): an interval-Newton/alpha
   certifier over python-flint arb, so any numeric near-hit anywhere in
   the campaign can be *proved* to be a complex solution of its reduced
   system. The campaign has emptiness machinery only; this is the missing
   half. One day to build; calibrate on the degree-144 reduced point.
3. **Staged eliminator** for the three OOM-walled frontier systems (B=16
   d=8 chart N 30/23; pentagon seed-extension 241/123; p11zero 186/306):
   msreduce + block cascade + evaluation-interpolation, never monolithic
   Gröbner. This is the campaign's own P2, still the shared blocker.

## Part 6 — Session 44 evidence already in hand (calibrated instruments)

- `session44/uvw_hunt.py` — (u,v,w) obstruction hunter, exact + mod-p,
  calibrated to sol6's planted seed (reproduces the forbidden p3[22]
  exactly, via kernel coefficient 23/4). Result so far: p=29 full grid,
  generic chart u≠0: **zero survivors** of six stacked obstructions;
  p=31 running. The generic chart of the live frontier is closing; the
  degenerate chart opened (Part 3.2).
- `session44/sieve_d6.py` — topological sieve; floor reproduced 2–5,
  extended 6–8 EMPTY for the model tear class.
- `session44/mondello_sweep.py` — refined char-p transfer: 510 prime-to-p
  hits at p=2, 143 at p=3 (including geometric-degree-2 étale noninjective
  Keller maps in char 3 — new small objects worth recording), 0 at p=5,
  no cross-prime shape in the box: evidence the char-p door thins out,
  with the *right* invariant this time.
- `session44/u0_descent.py` — exact u=0 chart descent (running).

## Part 7 — Priority queue (when execution resumes)

| P | Item | Cost | Why first |
|---|------|------|-----------|
| 1 | Finish u=0 chart descent → exact subsystem → solve | hours | only live structured family on the frontier |
| 2 | TRUST_LEDGER + re-run every C/D/E-grade kill guarding live cells | 1 session | the "too fast" audit, systematized |
| 3 | (8,28)/(3,4) Prop-4.3 analogue + x-column run | 1–2 sessions | best untouched published territory |
| 4 | Sieve extension (reducible tears, splice groups) | 1 session | either a floor theorem at 6–8, or first construction targets |
| 5 | d=12 unsaturated to verdict, unsaturated form | hours–1 session | biggest recorded anomaly, 144-coincidence |
| 6 | Case (2) char-0 confirmation | cheap | last sub-125 pair; their own P4 |
| 7 | Staged eliminator → the three OOM systems | 1–2 sessions | unlocks pentagon seed + B=16 frontier |
| 8 | Restore 19–38 bundle → survival graph → rank 429+41 | 1 session | lenses 8–9 become possible |

## Honest posture

Every mainstream signal says JC2 is true; every session that "found" a CE so
far found a bug instead, and Session 43's audit shows the failure mode runs
in both directions — kills can be wrong too. This plan is built so that each
step either surfaces a candidate with a certificate attached, or upgrades a
soft kill to a hard one. Both outcomes move the campaign; only unread
verdicts and unexamined anomalies do not.
