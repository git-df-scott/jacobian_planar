# Clues audit, 2026-09-03

Scope: a read-only sweep of all 37 branches of this repository for clues, not for a counterexample. Six parallel audits (canon ledgers, codex branches, early claude workstreams, night-run tooling, session narrative and transfer archive, literature-facing claims) were run and every claim below was spot-checked against the cited file. Nothing below is a counterexample. Nothing below is a new verdict. Every item is a location in the record plus what it implies for the next session.

Branch heads read: canon `claude/opus-5-counterexample-plan-sep6yk` 24a06fc; night `claude/jc2-counterexample-hunt-handoff-w369mc` e0086a7; handoff `claude/jc2-handoff-audit-hartnc` ae58bd3; mailbox `codex/claude-opus5-mailbox` 156ba7a; pentagon branches p11 e4fa5ce, l16 1e3ac1f, l14 338eca4; plus the early claude and codex workstreams listed in the README branch map.

## 1. Findings that change what the next session should do

### 1.1 The case (2) quadrilateral has at least four independent emptiness records the night run did not know about

The night handoff's Attempt 1 plans to spend the box on `scb0881` (the paper's Prop 4.3 case (2) quadrilateral, same polygons as `p108_525122`) at depth 6 in the y-adic eliminator, where it timed out at 3000 s and has no monomial certificate to depth 24. The record already contains:

| record | formulation | verdict | primes | location |
|---|---|---|---|---|
| CASE2_VERDICT | thin-polygon grading w = j - 2i, t = x y^2, edge variety | EMPTY mod p, every point of the edge variety | 65521, 32003, 65537 | canon `campaign/audit_tracks/CASE2_VERDICT.md:1-6` |
| Poisson-bracket branch | grading rho = 2 i - j, T = x y^2, triangular chain of one-variable equations; the leading level is a vanishing-period condition on a genus-3 hyperelliptic curve with exactly 35 solutions in 5 orbits | EMPTY mod p, all five orbits killed at levels 3 and 1 | 32003 (all orbits), 1000003 (rational orbit only) | `claude/poisson-bracket-counterexample-9esk1r:x2/README.md` sections 3 to 4 |
| Session 44 sweep | independent multi-prime sweep of "subcase 2" | EMPTY mod p, 144/144 and 112/112 covers | 1000003, 1500007 and one more | `claude/past-code-session-8mdjqn:HANDOFF.md:122-157` (read its own caveat at 145-157 before quoting) |
| Fable night branch | mate-problem formulation over a degree-35 number field | claims char-0 closure, 4/4 unit ideals | char 0 | `claude/fable-6o0nqe:HANDOFF_SOL_SESSION2.md:31-32` |

None of the four cites another. Canon `OPEN_ITEMS.md` item 5 knows only the first. The night run log (10:30Z) says the five-prime EMPTY "is neither confirmed nor contradicted here". The fable-6o0nqe char-0 claim names a degree-35 field while canon's case (2) residual is a degree-1144 eliminant; whether they are the same object is not established and must be checked before the char-0 claim is quoted.

Implication: the y-adic driver formulation is the wrong instrument for case (2). The thin-polygon grading turns it into a chain of one-variable equations that Singular decides in seconds per orbit. The right Attempt 1 is to reproduce the Poisson-bracket branch pipeline (`x2/pipeline.py m p`) at two more primes and then run its stage systems over Q, not to push the eliminator harder. The same grading applies to the (8,32) and (8,40) twins that survived the night's monomial scan.

### 1.2 The night's eliminator has no positive control at depth 6

The eliminator (`lincascade3.py` + `decide_ends.py`) produced the session's headline EMPTY (the (9,27) c' = 0 eps-swap stratum dying at depth 6) and 20 of 35 EMPTY branches on `sab7d9e`. The positive controls `posctl_a`, `posctl_b` were run through the extractor and the monomial scan (run log 05:22Z, 08:50Z) but never through the eliminator and `decide_ends.py`. The one cross-check at 08:30Z compares two paths through the same formulation. The depth-6 death was also confirmed by direct substitution of the depth-4 family into the recursion, so that particular verdict has a second route; the `sab7d9e` branch verdicts do not.

Also: the controls have a single Q-row above j = 0, so they exercise only 2 support conditions each (run log 05:22Z admits this). A control with several Q-rows is needed. The Poisson-bracket branch's certified mu = 1 witnesses (`x2/README.md` section 5, e.g. P = (3x^4y^4 - 4x^3y^3 + 12x^2y - 12x)/12, Q = -(x^3y^3 + 3x)/3 with {P,Q} = x^2) are exact realizable pairs with multi-row polygons and can serve.

### 1.3 The mailbox already contained the night's two headline corrections, plus one structural fact the night did not use

`codex/claude-opus5-mailbox:AGENT_MAILBOX.md`:

- FABLE-004 (line 3676) states that the campaign's "(9,27)" label is wrong, that (9,27) is Prop 4.1 with bracket x, and that the open case is (8,28) sub-case (1) pentagon and sub-case (2) quadrilateral. The night run rediscovered this at 05:10Z and 05:20Z.
- FABLE-006 (line 3909) lists the 24 published cases above 125 from arXiv:1708.07936 section 6 and names (8,28) with (m,n) = (3,4) at 144 as the obvious first target. The night run's Attempt 4 sizing (06:10Z) is that case.
- FABLE-004 section 3 derives two structural facts for sub-case (2) that no later document uses: (a) after a_0 = b_0 = 0 both P and Q are divisible by x, and [P,Q] = x^2 forces a_1 and b_1 proportional before any solver runs; (b) the generic fibre of P never meets x = 0, so Q restricted to it is unramified and chi(F_c) = D forces D = 1: the pair must be birational in sub-case (2). FABLE-005 later restricts (b) to the proper locus (line 3848-3853). These are cheap necessary conditions to impose on any case (2) system, in any formulation.
- The last mailbox item OPUS43-029 (line 3210) reports an explicit 59-condition, 19-parameter endgame system with no verdict and no reply. Nobody answered it. The README's statement that Codex reply e4dc2fc was never delivered is confirmed: the object does not exist in any fetched branch.

### 1.4 STATE_FULL.md and ADJUDICATION.md still carry the voided B = 16 ladder

`CATCHES.md:655-665` voids every B = 16 EMPTY row built on the misprinted GGV row 3: "Not 'unconfirmed': VOID". Under the corrected system only d = 2..5 were re-established (CATCHES.md ~691-706). Yet `STATE_FULL.md:6-19` still lists d = 6..12 EMPTY rows and `ADJUDICATION.md:82` still says "the B=16 corridor is now closed further than any published source". Both files predate the retraction and were never revisited. `STATUS.md`, `LIVE_MAP.md`, `TRUST_MAP.md` do not mention B = 16 at all: the ladder fell out of tracking rather than being reconciled. `WEEKEND_PLAN.md:46-50` still directs extending the rank criterion to d = 48, 75 after `OPEN_ITEMS.md:39-40` recorded that criterion as a can't-fail certifier.

The transfer tarball `archives/transfer/state_transfer.tgz` has CATCHES.md at 125 lines against canon's 2073 and BIFURCATION.md missing its last 200 lines. Restoring from it silently reintroduces claims canon retracted.

## 2. Results on side branches that never reached canon

| branch | result | where | in canon |
|---|---|---|---|
| `codex/pentagon-level14-rational-obstruction` | branch 2 of the pentagon descent dies at level 14 on an exact rational constant -63/32, asserted in code | `breakthrough/pentagon_level14_rational_obstruction.py:60-73` | no |
| `codex/pentagon-level16-exact` | explicit char-0 witness c_0 = c_1 = lambda = 1, a_4 = 2, b_8 = d_7 = 1 keeping branch 1 alive at level 16; joint condition F_0 = F_1 = a_0^3 lambda = 0 | `breakthrough/PENTAGON_LEVEL16.md:17-21, 96-100` | README only |
| `work` | pentagon descent solved through level 17 with kernel constant retained; still NO VERDICT | `breakthrough/PENTAGON_LEVEL17.md`, `GENERIC_RESIDUAL_EDGE.md:91-93` | no |
| mailbox `wave6/bottomedge/ORBIT_VERDICT.md` | bottom-edge degree-9 eliminant factors over Q as (57x+179)(285000x+769477)(quadratic)(quintic); admissible locus is the single quintic Galois orbit, so one admissible seed decides the bottom edge | lines 1-30 | partially (OPEN_ITEMS item 7 has the count, not the factorization) |
| `codex/sol-session3-pole` | cusp-preserving Briancon family closed exactly at all degrees by an elliptic de Rham argument | `night24/CUSP_CLOSURE.md` | no |
| `codex/sol6-collision-first` | fully rational planted seed (u = 1, v = w = 0, A_1 = -1, A_2 = -1/2, A_3 = -1/3, A_5 = -1/5) survives exactly through x^21 and dies at x^22 on an explicit rational obstruction | `SOL6_COLLISION_FIRST.md` | no |
| `claude/mod-3-keller-pair-obstruction-oceq9z` | session 20: a mod-65521 point satisfying all 92 original (8,28) equations, rejected only because vertex coefficients c_8_16 = d_12_24 vanish | `jc2_reconstruct.py:1-40`, commit a87af7d | no |
| same branch | the escape-hatch solution R(v) = S(v)/(v+1)^4, S = -243v^4 + 81v^3 - 54v^2 + 42v - 35, is byte-for-byte the polynomial canon `TRUST_MAP.md:88-93` presents as a fresh derivation; the branch's general lattice criterion (`jc2_escape_hatch.py:190-217`) is more general than canon's | `jc2_escape_hatch.py:1-35` | uncredited |
| `claude/counter-example-audit-dnu9l9` | `trackD_targets.json` and `trackD_vertex.json` (about 13,500 lines) are the above-125 enumeration data canon `TRUST_MAP.md` marks ABSENT | branch root | no |
| `claude/d23-borisov-transfer-test-vpr3m6` | explicit polynomial near-miss for D23/N3, stopped before "the surgery" | `d23_n3_layer1_nearmiss.py`, commit 7296164 | no |
| `claude/opus-worker-resisters` | resister IDs `w6_35657_1-7`, `w6_79970_0-3`, `orph_345092`, `p108_638901` have no later mention anywhere | `wave6/ms_opus/` | no |

## 3. A pattern worth naming: every near-miss is a vertex degeneration

Four independent searches ended at the same wall:

- session 20's mod-p candidate passes all 92 equations and fails only vertex nonvanishing (`jc2_reconstruct.py`);
- the fable numerical sweep finds [P,Q] = x solvable to machine precision "ONLY with the Newton vertices vanishing" (`claude/fable-counterexample-sweep-yyj5vf` commit e9a65be);
- sol3-all-five's degree-144 reduced hit at residual 1e-14 fails only the reverse lift (`rundown.md`);
- the night run's block 0 on both (72,108) charts forces c_4 = c_5 = 0 and leaves a positive-dimensional family that only deeper rows kill (run log 06:55Z, 07:45Z).

The reductions are saturated against the vertex coefficients, so a solver that ignores saturation lands on the degenerate locus every time. This is consistent with emptiness of the saturated systems and is not evidence either way, but it means any future numerical or modular "hit" should be checked for vertex vanishing before anything else, and it suggests the shape constraints, not the bracket, are the binding ones.

## 4. Tool hygiene items (no verdict changes found)

- All 25 monomial kills in `sweep_table.md` have `exactQ: CERTIFIED` entries in `certified.json`, and by construction (`fastx.py:15-16, 54-58`) every free parameter is a driver-polygon coefficient, so the nonzero-set filter cannot admit a stray variable. Twelve of the 25 kills are above max degree 125 and carry the compiler's unverified A'_t = (1,0) and fallback c' ladder; 110 of 134 `library.json` entries carry the "falling back to the full ladder 0..b" note, confirming the ground-cover cmax correction is not yet in the compiler.
- `decide_ends.py:8` declares only `c_\d+` variables; a surviving w, u or x would produce a parse error (a WALL), not a silent verdict.
- `torus_charts.py:48-59` recognizes Rabinowitsch rows only when they have exactly two terms after reduction; under-detection falls through to a chart split, which is sound but slower.
- `lincascade3.py:183-200` restarts non-monomial pivot branches from the full system; branch-limit hits are labelled, not folded into EMPTY.
- The night handoff's guardrails (section 5) cover the msolve pipeline mechanics only. `claude/opus-errors-false-proofs-820rmd:FAILURE_ANALYSIS.md` classifies the campaign's false proofs into three mechanisms (can't-fail certifiers, metadata trusted over artifacts, quantifier-scope drift) and none of the three is covered by those guardrails. Its `wave2/w2_cantfail_audit.py` and `wave3/w3_claim_ledger.py` were never carried forward.

## 5. Literature state, checked today

- arXiv:2608.00222 (Gao, 31 July 2026) and Tao's post of 21 July 2026 confirm the refutation of the Jacobian conjecture in every dimension above two (Alpoge 19 July, Gallagher 20 July, Speyer 23 July). The plane case is open. `OPEN_ITEMS.md` item 6 cites this correctly.
- arXiv:2204.14178's abstract confirms (72,108) and (108,72) are the only surviving pairs below 125. The campaign's finding that its Cor 5.7 proof of the (9,27) orientation is broken (`CATCHES.md:517-609`, `COR57_ADJUDICATION.md:12-15`, 15 of 66 conditions delivered) is internally consistent and independently re-derived; the repair attempt (CE_HUNT_PLAN Lead A) is the one ground-cover item not done.
- The paper's actual (9,27) polygon (172 driver parameters) has never been computed on in any formulation. Every "(9,27)" run in the archive is a compiler stratum that Prop 4.1 excludes.
- `GGV_ARXIV_DIFF.md` closes the version question: the GGV row-3 misprint is in both the journal and arXiv v3, so no verdict depends on edition.

## 6. What this audit did not do

No solver was run. No claim in section 1.1 was reproduced; the four case (2) records are quoted, not verified, and their formulations differ enough that "same object" must be established for each before they are counted as replications. The 1199-line `docs/history/sessions-01-18-status.md` was not read in full. `trackD_targets.json` was not diffed against the ground-cover enumeration.
