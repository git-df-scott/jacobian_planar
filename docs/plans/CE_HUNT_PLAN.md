# JC2 counterexample hunt: unified fleet plan

Status: plan, not result. Prepared 2026-09-02 on branch `claude/jc2-handoff-audit-hartnc` from a nine-reader audit of the canonical campaign branch (`claude/opus-5-counterexample-plan-sep6yk` at 24a06fc), the Codex branches (`codex/claude-opus5-mailbox` 156ba7a, `codex/pentagon-p11-zero-search` e4fa5ce, `codex/pentagon-level16-exact` 1e3ac1f), and the support branches (`opus-hunt-territories`, `opus-plan-priority-queue`, `opus-errors-false-proofs`). Five independent planning angles were generated, judged, and merged; each load-bearing premise was then checked against the files and the mathematics by adversarial reviewers. Supporting material is in `docs/plans/appendix/`.

Every path below is relative to the checkout of the branch named in the citation; `canon/` means the canonical campaign branch, `mailbox/` the Codex mailbox branch, `p11/` and `l16/` the two pentagon Codex branches, `pq/` the priority-queue branch.

## 0. Honest framing

The plane Jacobian conjecture is widely believed true. Moh (1983) excluded max degree at most 100. Guccione, Guccione, Horruitiner and Valqui (GGHV, arXiv:2204.14178, unrefereed) exclude every degree pair with max below 125 except (72,108) and its mirror. Tao's July 2026 digestion of the dimension-3 counterexample states explicitly that the plane case remains open. Forty-plus sessions of this campaign produced zero non-EMPTY verdicts on any real system; both apparent hits were gauge artefacts caught before commit (`canon/STATUS.md` section 6.6).

The plan therefore has two products. The primary product, which it will almost certainly deliver, is a set of certified characteristic-zero exclusions and corrections to the literature's exclusion chain. The secondary product, which it is designed to maximize but cannot promise, is a genuine counterexample. The honest probability that this program produces a verified JC2 counterexample is of order one in a thousand for the whole campaign, decomposed below; no single lead exceeds about half a percent. Any plan whose value depends on a HIT has negative expected value; this one does not.

Campaign-level probability, decomposed. P(HIT) = P(JC2 is false) times P(a minimal counterexample lies in the region this campaign can reach) times P(a verdict rather than a timeout is obtained there) times P(the non-empty point survives reconstruction, lifting and the HIT protocol). Charitable values: 5 to 10 percent; 10 to 20 percent (the enumerated region stops at max 150 while the frontier extends past 300); 20 to 40 percent even on a 128 GB host (the archive records 49 timeouts, OOM at 13.9 GB on the live cells, and zero non-empty verdicts across about 46 decided systems); at most 50 percent. The product is about 0.001. Per-lead figures below are P(a verified counterexample) conditioned on that lead's own chain; they are strongly positively correlated through the single question of whether JC2 fails at these degrees and must never be summed. The soundness reviewer's figures are used; the planners' original numbers were 10 to 40 times higher and are recorded in the appendix.

| Lead | p(HIT) | Guaranteed product |
|---|---|---|
| A. Re-derive the enumeration; adjudicate Cor 5.7 | 0 directly; 10 to 15 percent that the search space grows | Verified or expanded search space |
| B. Compute plant and ledger | 0 | Every later verdict becomes checkable |
| C. B=16 ladder, corrected system, d=8 chart N first | 0.1 to 0.2 percent | First char-0 verdict past d=7 |
| D. Certified char-0 promoter; case (2) over Q | under 0.1 percent | The campaign's central verdict becomes a theorem |
| E. (9,27) leaves and Cor 5.7 repair | at most 0.5 percent | Independent test of a published kill |
| F. Pentagon case (1) by reformulation | at most 0.3 percent | First verdict of any kind on the pentagon |
| G. The 24 published cases at max 125 to 150 | about 0.3 percent | A publishable closure toward 150 |
| H. Structural routes (twisted sweep, Weyl cascade, chi filter) | at most 0.5 percent; the Weyl route yields "JC2 false" without an explicit map | Scoped theorems, char-0 kill certificates |
| I. Tail: 41 timeout shapes, compiler factorization audit, A'_t | under 0.1 percent | The frontier becomes a list instead of folklore |

## 1. State of play

All entries below are quoted from the reader audit with file citations. Labels follow the campaign's own vocabulary: PROVED-exact and CERTIFIED are characteristic-zero results; EMPTY-mod-p is evidence and is never promoted; TIMEOUT, OOM and FAILURE are not verdicts.

| Territory | Verdict | Label | Source |
|---|---|---|---|
| (72,108) and (108,72) as one territory | J(Q,P) = -J(P,Q); both orientations are one object | PROVED-exact | `canon/STATUS.md` section 1; `wave0/w0_h1a_swap_and_G.py` |
| (72,108) case (2) quadrilaterals | EMPTY mod p on both charts at 65521, 32003, 65537 (two of these violate the p = 1 mod 3 rule), re-run compliantly at 65539, 65599; edge eliminant degree 1144, squarefree, irreducible over Q by Dedekind sieve at 8 primes plus an independent 9th | EMPTY-mod-p; irreducibility PROVED-exact; residual over Q never executed (MISS-4) | `canon/STATUS.md` sections 2.4, 2.5, 4; `canon/STATE_FULL.md` B; `canon/campaign/audit_tracks/CASE2_VERDICT.md` |
| (72,108) case (1) pentagon, corner (8,28) with (m,n)=(3,2) | NO VERDICT by any method. msolve on `wave1/pent_L23.ms` exit 137 at 13.9 GB, 0-byte output; Singular slimgb on L18 exit 137; seed-pinned twin exit 124 at 5400 s, 9.5 GB, 0-byte output. Every normalized weight truncation W at least 8 is certified alive by an exact rational witness in the repo, so the truncation ladder cannot kill it | NO VERDICT | `canon/STATUS.md` section 3; `canon/pent/RUNLOG.tsv`; `canon/CATCHES.md` "P0 IS FUTILE"; `pq/trackB1_pentagon.py:432` (witness: P = S^2, Q = S^3, S = y^4 (1 + (xy)^4) + x^4 y^7) |
| (9,27) orientation with (m,n)=(2,3) | Killed in print only by GGHV Cor 5.7; the campaign's line-by-line audit finds the step at `gghv.txt:1430-1433` invalid (bracket leaves K^x; 51 of 66 conditions unsupported). The two independent test systems are positive-dimensional (torus rank 5); p108_525122 has 2 of 5 leaves unresolved, p108_192622 has 1 leaf (139 eq / 38 vars) unresolved | OPEN; literature silent | `canon/CATCHES.md` "GGHV COROLLARY 5.7 IS UNPROVEN"; `mailbox/wave6/frontier/P108_RESULTS.md`; `mailbox/AGENT_MAILBOX.md:1597-1680` |
| Borisov framework family (First, Second, Three-dessin, (108,72) charts) | Closed by exact endgame obstruction for all reachable admissible charts; the (108,72) closure is adjudicated sound but overstated on one leg | PROVED-exact / CERTIFIED with a named caveat | `canon/TRUST_MAP.md` sections 2 to 5; `canon/ADJUDICATION.md` sections 1, 7 |
| B=16 ladder (GGV Thm 1.2, an iff) on the corrected system | d=3..7 EMPTY over Q (d=7: 26 eq / 20 unk, 1345 s). Everything built on the misprinted printed row 3 of (1.2) is VOID. d=8 chart N (30 eq / 23 unk) exported and never launched. d=9..11 chart N never run. d=12 unsaturated undecided. d=27 untouched | d<=7 PROVED-exact; rest NOT RUN or TIMEOUT | `canon/OPEN_ITEMS.md` sections 1 to 4; `canon/CATCHES.md` "GGV (1.2) ROW 3 IS MIS-PRINTED" |
| Rank/bifurcation criterion | A can't-fail certifier; its "always obstructed" rows are bookkeeping, not evidence | RETIRED | `canon/OPEN_ITEMS.md` section 4 |
| Numerical multi-start lanes | Planted roots not recovered at 25 and 165 unknowns; all empty-floor evidence VOID | RETRACTED as evidence | `canon/CATCHES.md` "RETRACTION (05:45Z)" |
| Published enumeration to max 150 | `canon/gghv_audit/all_cases_max_le_150.json` reproduces 34 cases, 10 with max below 125. The corner A0=[8,1,28] appears twice: (m,n)=(3,2) gives (108,72), the sub-125 survivor; (m,n)=(3,4) gives (108,144), an above-125 case. The reproduction has never been checked row for row against the published section 6 | LIT-READ, reproduction unverified against the PDF | `canon/gghv_audit/`; `mailbox/AGENT_MAILBOX.md:3909-3985` (FABLE-006) |
| Above-125 frontier | `canon/wave6/frontier_151_300_map.json`: 432 records, 429 NO-CHAIN (no compilable chain, hence no system). 20 shapes across 6 chains EMPTY at the single prime 65521. Counts 429 / 464 / 474 / 804 are five different objects and are unreconciled; 804 is disavowed by FABLE-006 | mostly NOT RUN; 20 single-prime EMPTY | `canon/STATE_FULL.md` C; `canon/campaign/audit_tracks/ABOVE_125_STATUS.md`; `canon/CROSSDOOR.md` section 5 |
| "41 timeout shapes" | Referenced as an aggregate in three files; enumerated in none. Components 33 or 36 virgin, 5 orphan, 3 above-125; the arithmetic is the reader's inference | TIMEOUT, unenumerated | `canon/OPEN_ITEMS.md` section 7; `canon/AUDIT_EOD.md` section 3 |
| README "strongest inherited asset" (164 vars, 288 quadrics, 6,821 terms over Q(alpha), unit GB at p=1000003) | No file with these dimensions exists in any local checkout. The nearest real object is `mailbox/wave6/frontier/trackB1_sat_Q.ms` (present on disk on the mailbox branch; there is no `canon/wave6/frontier/` directory) at 166 vars / 284 eqs / degree 5 / 8,774 coefficients, reconstructed from two primes, with four Groebner attempts all NO VERDICT and no recorded unit GB | UNVERIFIED; README numbers contradict the mailbox record | `README.md:19-20` on main; `mailbox/AGENT_MAILBOX.md:246-260, 1419-1432`; `mailbox/wave6/frontier/` |
| Tail-closure test, rank-five Cor 5.7 slices, provenance audit of the 184 hashes / 189 nonclosing cases | The tail test was assigned to Codex in OPUS43-012 and never reported. The figures 184 and 189 match nothing in any checkout | UNRUN; 184/189 are non-facts | `mailbox/AGENT_MAILBOX.md:1597-1680`; reader grep |
| Environment | 4 cores, 15 GB, no swap; container restarts every 30 to 50 minutes; measured 2.5 h process ceiling; Singular and msolve absent from a fresh container; git tree rolled back twice | infrastructure | `canon/MANIFEST.md` C; `pq/RESUME_STATE.md`; `which Singular msolve` |

Disagreements between the repository and the literature that the plan must respect:

- The (8,28) corner with (m,n)=(3,4) sits at max degree 144, above 125. Any file treating it as part of the sub-125 frontier is misrouting effort. Every record must carry corner, (m,n), orientation and max degree.
- The literature reader could not locate the Nguyen 2025 paper cited as the refereed floor of 104. Cite GGHV's 108 until it is found.
- No published bound of 150 exists; 150 is the enumeration horizon of arXiv:1708.07936, and that paper discards nothing above 125.

## 2. Audit gates before compute

Each gate is a pass/fail test an agent can run in under a day. No solver time is spent on a lead until its gates pass. The gates encode the campaign's own failure catalogue (`canon/CATCHES.md`, `errors/FAILURE_ANALYSIS.md` mechanisms M1 to M3).

| Gate | Test | Pass criterion |
|---|---|---|
| G1 Engines | `which Singular msolve`; build msolve 0.10.1 from source and Singular 4.3.2; write `engines.json` with versions and hashes | Both present and pinned; the runner exits with a MISSING-ENGINE status otherwise |
| G2 Cor 5.7 position | Recompute the bracket by hand and in sympy from the self-contained argument in `canon/CATCHES.md:517-604` (the cited `gghv.txt` is in no local checkout, so its line numbers cannot be inspected here); reconcile with `mailbox/campaign/mod3_828/jc2_literature_sweep_partial.md:65-66,311`, which records the corollary as verified | One recorded position; every file asserting the other amended or marked superseded |
| G3 Label integrity | Rebuild the case register from `canon/gghv_audit/all_cases_max_le_150.json` keyed by (corner, (m,n), orientation, max) | Zero rows missing a key; (8,28)/(3,4) filed above 125 |
| G4 Census reconciliation | Recount 432/429 from the frontier map, 474 from `gghv_audit`, 464 from the coverage audit; search for any artifact behind 804, 189, 184 | Every count has a script and a region definition, or is recorded as NONEXISTENT |
| G5 Void ledger | Tag every B=16 verdict row by provenance: corrected (m16_*) or printed | Zero rows with unknown provenance; no headline count includes void rows |
| G6 README asset | Count the header of `mailbox/wave6/frontier/trackB1_sat_Q.ms` (it is on disk on the mailbox branch, not the canonical branch); search for any p=1000003 unit-GB artifact | Either the file matches a corrected README or the claim is struck |
| G7 Excess and torus rank | For every queued emptiness run compute equations minus variables and the grading-torus rank | No run with excess at most 0; no solve-mode run on positive-dimensional input; truncation ladder removed from every queue |
| G8 Can't-fail scan | Run `wave2/w2_cantfail_audit.py` over every certifier a lead depends on | Zero literal-True check conditions (45 exist today) |
| G9 Export sanitizer | Route every `.ms` through `canon/wave4/w4_msformat.py`: coefficients in [0,p), no zero terms, no constant generator, round-trip re-parse | Poisoned-input controls classified FAILURE, never EMPTY |
| G10 Prime hygiene | Every mod-p verdict carries its prime list; p = 1 mod 3; for ladder cells 12d a square mod p; control primes 5, 11, 17 must be rejected | Every EMPTY-mod-p row has at least two compliant primes |
| G11 Infrastructure floor | Measure uptime, cgroup cap, disk headroom; confirm marker-resumable resume after a forced restart; push after every commit | At least 8 h uninterrupted and 32 GB, or every run is resumable at 20-minute granularity |
| G12 Sweep dichotomy scope | Read `canon/wave6/w6_plane_sweep.py` and `w6_plane_sweep_search.py`; state verbatim whether the twist rebuttal is proved for general (C,i,j) or only for w = gamma u, C = gamma x^s | A scope statement anchored by exact quotation |

## 3. Leads, ordered by expected value per agent-week

Each lead names its target, its premise with citations, the method, the agent roles, inputs, outputs with labels, the stop rule, cost, and the honest p(HIT). Leads A and B are prerequisites for everything else and cost no solver time.

### Lead A. Re-derive the sub-125 enumeration and adjudicate GGHV Corollary 5.7

Target. The premise that (72,108)/(108,72) is the only surviving pair below max 125, and the single literature step that closes one orientation of it.

Premise. GGHV Theorem 2.1 imports its ten-case table from arXiv:1708.07936 Algorithms 1 to 9 rather than deriving degree pairs itself. The campaign's independent re-implementation `canon/gghv_audit/ggv_algorithms.py` reproduces 34 of 34 published cases and 10 of 10 GGHV rows, but also finds two extra length-1 and four extra length-2 chains that the printed tables omit, and section 5 of that paper contradicts its own table on the number of length-2 chains (`canon/HUNT2_REPORT.md` T1). One kill inside the 105 to 124 window, (80,112), rests on a citation to GGV 2013 section 3.5 with no argument of its own. The (10,40) chain rests on an unprinted assumption A'_t = (1,0) (`canon/AUDIT_EOD.md` section 4 item 3; `canon/CATCHES.md:32`). Cor 5.7 is recorded as verified in one file and as broken in another (gate G2).

Method.
1. Run the re-implementation to max 150 with every filter exposed. For each divergence from the printed tables, trace the exact algorithm step and carry the extra chain to a degree pair or to a proof that it produces none.
2. Enumerate the admissible A'_t for the (10,40) chain from the algorithm's own filters instead of importing (1,0). This is the same pattern the campaign used for the F6 gcd discrepancy.
3. Verify the section 6 table of arXiv:1708.07936 against the published PDF by page image (install poppler-utils in the provisioning script; text extraction produced three retractions in one session).
4. Attempt to repair Cor 5.7: either establish that the translated bracket lies in K^x by another route, or supply the missing 51 of 66 coefficient conditions, or construct a counterexample to (5.12) as stated. Read `canon/papers/2204.14178.pdf` section 5 in full.
5. Locate the Nguyen 2025 reference or downgrade the cited floor to 108.

Agent roles. Enumeration engineer; paper reader (page-image verification); proof auditor for Cor 5.7; adversary whose only job is to produce a chain the enumerator misses.

Inputs. `canon/gghv_audit/ggv_algorithms.py`, `canon/gghv_audit/all_cases_max_le_150.json`, `canon/papers/1708.07936.pdf`, `canon/papers/2204.14178.pdf`, `canon/gghv.txt`.

Outputs. ENUMERATION-RE-DERIVED [PROVED-exact] or ENUMERATION-INCOMPLETE with the missed rows; A'_t DISCHARGED or CENSUS-EXPANDED; COR 5.7 REPAIRED, REFUTED, or UNVERIFIED-HERE; a divergence table with the algorithm step for each.

Stop rule. Stop when every max-150 row is reproduced or its divergence explained. If a new sub-125 pair appears, halt everything else and route it to the polygon builder. Paper lane for Cor 5.7: four agent-days, then write up whatever state it is in.

Cost. Two to four agent-days for the enumeration; four agent-days for Cor 5.7; negligible CPU.

p(HIT). Zero directly. The probability that the enumeration is incomplete below 125 or that A'_t is not forced is perhaps 10 to 15 percent, and that is the only outcome in this plan that can make the search space larger. Cor 5.7 refuted as stated would reopen a whole orientation of the last surviving sub-125 pair.

### Lead B. The compute plant, the ledger, and the gates as code

Target. Make any run over 20 minutes or 12 GB finish at all, and make every verdict machine-checkable.

Premise. Nothing on the board died to mathematics. The open queue died to a 4-core, 15 GB container with 30-minute restarts and no engines, to msolve modes that write `[-1]` and exit 0 on parse errors, to three cascades that failed their own self-tests, and to a ledger without prime lists or content hashes (49 TIMEOUT records collapsed to 16 unique systems; two md5-identical p108 systems double-counted). The working pattern already exists in `canon/wave6/bottomedge/sweep.sh`: solve, analyse, commit, push, one prime per commit, so a restart costs one job.

Method.
1. `provision.sh`: idempotent install of Singular 4.3.2, msolve 0.10.1 from source, python-flint, gmpy2, PARI/GP, poppler-utils; emit `engines.json`.
2. One persistent heavy host (16 cores, 128 GB, 500 GB disk, no restart policy) for the memory-bound cells; the ephemeral box stays the light lane.
3. `runner.sh` generalizing the sweep script: skip if the content hash has a terminal verdict; run under `timeout` and `/usr/bin/time -v`; tee stdout and stderr separately; classify; write one verdict JSON; commit and push. Single-slot FIFO for the heavy lane with explicit cgroup memory limits. Watch disk and inodes as well as RSS. Ban `pkill -f` in a pre-commit hook.
4. `job.json` and `verdict.json` schemas (section 4). Content hash is over the canonicalized generator list, not the file text.
5. `gate.py` implementing every gate in section 4 as a blocking check in the exporter, the runner and CI.
6. Re-key the historical record by content hash; publish `RECONCILIATION.md` for the counts 429 / 432 / 464 / 474 / 804 / 34; backfill prime lists; demote any EMPTY without recoverable stderr to EMPTY-mod-p-UNAUDITED and re-queue it.
7. Scheduler: the pre-flight refusal list is the valuable half and is about twenty lines (refuse if max realizable degree is at most 100, gcd not 16 or above 20, excess at most 0, solve mode on positive-dimensional input, known terminal hash, or a can't-fail criterion); build that first. Score admissible jobs by expected information per core-hour, break ties by size ascending, publish `queue.json` and `REFUSED.json`, and skip nightly re-ranking machinery for a fleet this size.
8. Smoke suite on every wake: known-EMPTY returns EMPTY in both engines, known-NONEMPTY returns non-empty, malformed input returns FAILURE, a 3-second job survives a simulated restart.

Agent roles. Librarian; exporter/sanitizer; auditor.

Outputs. Infrastructure artifacts; `RECONCILIATION.md`; the first verdict landed committed and pushed unattended.

Stop rule. Smoke suite passes twice across a deliberate restart. If the persistent host cannot be obtained within three days, re-scope every heavy lead to staged degree-bounded probes under 12 GB and say so.

Cost. About five agent-days; roughly 350 to 500 USD of commodity cloud for two weeks of the heavy host.

p(HIT). Zero. Everything else depends on it.

### Lead C. The B=16 ladder on the corrected system: d=8 chart N, then d=12 unsaturated, then d=27

Target. GGV Pro Mathematica 27 (2013) Theorem 1.2 systems (1.2)+(1.3) on the corrected row 3, cell deg(q1)=d, degree pair (16(3d-2), 16(2d-1)).

Premise. Theorem 1.2 is stated in the campaign's record as an iff: B=16 holds iff a solution with mu0 nonzero exists. The exact wording has not been re-read from the page image here, and the campaign was already burned once by a printed GGV equation, so the iff is LIT-READ until re-read. Even granting it, a solution is leading-form data (a_i, b_j, mu_k) for a cell, not a pair (P,Q); reconstructing polynomials of the stated degrees is a separate step that no artifact in the archive has performed, and the solution must also pin the cell (the leading coefficient of q1 nonzero) or it belongs to a lower cell with a different degree pair. GGV discard nothing at B=16 and stall at d=5 (`canon/ADJUDICATION.md` sections 2, 3). On the corrected system d=3..7 are EMPTY over Q. d=8 chart N is 30 equations in 23 unknowns (the 23rd unknown is the Rabinowitsch variable t and the 30th equation is mu0 t - 1), exported as `canon/wave5/ms/m16_d8_p1000003.ms`, `m16_d8_p1000033.ms` and `m16_d8_q.ms`, regenerable by `canon/wave6/w6_seed_d8.py`, and never launched (MISS-2). Chart Z contains no counterexample by F2 (mu0 = a2 mu2 / 3), so chart N is the only chart. Seeding the row-0 root covers the whole cell; the roots are sqrt(12d)-irrational so modular work needs primes where 12d is a square; prime size buys nothing (`canon/MORNING_SUMMARY.md`). Direct Groebner scales about 32 times per level (d=6: 42 s; d=7: 1345 s), so d at least 9 is unreachable by the direct route. d=12 and d=27 are resonant (12d a perfect square, both row-0 roots rational). The corrected unsaturated form is EMPTY at d=3..6 and was never tried at d=12. The rank criterion must not be cited for anything.

Method.
1. Re-read Theorem 1.2 from the page image of GGV Pro Mathematica 27 (2013) and record its exact hypotheses and constructive content. Regenerate the d=8 export from the generator and diff against the on-disk file; confirm provenance is corrected (gate G5); sanitize (gate G9). Add, alongside the mu0 saturation (which F2 makes a genuine saturation rather than a free side condition), a saturation pinning the cell (leading coefficient of q1 nonzero), and run both charts of any resulting split.
2. Three disjoint routes in parallel on d=8 chart N over Q: msolve `-g 2` (Groebner-only; solve mode is invalid on non-rigid input) with an 8 h budget; Singular over Q with a degBound ladder 5, 6, 7, 8 (a unit at any rung is a genuine 1 in the ideal; note `option(degBound,D)` is not valid syntax and errors silently) followed by `lift(I, ideal(1))`; and the graded certificate machine of Lead D.
3. Modular sanity only at primes p = 1 mod 3 where 96 is a quadratic residue, two agreeing primes before quoting anything.
4. d=12 unsaturated (mu0 free, mu2 gauged to 1, a_{2d} unseeded so one run covers both rational roots) by the same three routes, 24 h budget.
5. d=27 (114 eq / 85 unk) only via the certificate route, 40 CPU-hours, then stop.
6. In parallel, a symbolic-in-d attempt on the GGV conjecture (all solutions have mu1 = mu2 = 0): re-derive the system with d symbolic from the Poisson bracket (`canon/wave6/w6_ggv12_rederivation.py`), classify each row family as d-independent or not (F2 and F3 are d-independent for d at least 4), solve the d-dependent rows as recurrences using the rank-1 torus grading with weights wt(a_i)=2d-i, wt(b_j)=d-j, wt(mu3)=d, wt(mu2)=2d-1, wt(mu1)=3d-2, wt(mu0)=4d-3, and reduce the ladder to a finite condition set in d. The derivation must reproduce d=3..7 EMPTY or be discarded.
7. Any NON-EMPTY at a screened prime is a lift target and nothing more. Freeze, Hensel-lift with `canon/lift/lift_pipeline.py`, exact substitution, then gate H0 (reconstruct explicit P, Q in Q[x,y] with verified degrees 16(3d-2), 16(2d-1)), then the full HIT protocol.

Agent roles. Export verifier; solver runner; certificate engineer; symbolic-d algebraist; control author (a planted algebraic solution per cell, never numerical); lifter and HIT-gate operator.

Outputs. d=8 chart N: [PROVED-exact] EMPTY, or EMPTY-mod-p(p1,p2), or CANDIDATE-UNVERIFIED. d=12 unsaturated: DECIDED or MEASURED-RESISTANCE. d=27: certificate or NO VERDICT. GGV conjecture: THEOREM, or OPEN with the finite condition set recorded.

Stop rule. d=8: three routes at 8 h each; if all fail, record that exact elimination cannot decide d=8 chart N on this hardware and do not queue d=9..11. Symbolic-d: three agent-weeks, then OPEN.

Cost. Hours to days per cell on the heavy host; the symbolic-d work is agent time.

p(HIT). 0.1 to 0.2 percent for d=8, lower for d=12 and d=27: d=3..7 are all EMPTY over Q and the excess of conditions over unknowns grows with d, so conditional emptiness increases up the ladder. This is the one lead where a non-empty verdict is the candidate whose promotion path is an iff rather than a necessary condition; it is not itself a counterexample until H0 and H1 to H6 pass. Perhaps 15 to 20 percent that the symbolic-d attempt proves the GGV conjecture instead, which closes the door.

### Lead D. The certified characteristic-zero promoter, and case (2) over Q

Target. Convert EMPTY-mod-p into checkable char-0 proofs; first application (72,108) case (2).

Premise. Weak Nullstellensatz: an ideal I in Q[x] has no zero over the algebraic closure iff 1 lies in I, iff there are cofactors h_i over Q with 1 = sum h_i f_i. Finding cofactors of bounded degree D is a linear system over Q, and under the L = 2 alpha - beta torus grading that system is block-diagonal by weight because the constant 1 sits in a single weight (`p11/CATCHES.md:1600-1604`). The certificate is verified by one exact polynomial identity and is immune to every failure mode in the catalogue: it cannot time out into a fake EMPTY, cannot be a parse artefact, cannot be a bad-prime artefact, and cannot be a can't-fail certifier. A mod-p unit basis can be an artefact (the ideal (p x - 1) is empty mod p and has the solution 1/p over Q), and the campaign has a live witness that its own modular eliminator closes branches with genuine rational solutions (`canon/CATCHES.md` "MODULAR ELIMINATION IS UNSOUND FOR CONTRADICTIONS"). Good-prime selection is unjustified in the record (`canon/MANIFEST.md` D item 2). Case (2) is EMPTY at five primes and the 13-variable residual over the degree-1144 field was never run; but the w = -4 block of the 72-variable, 92-equation edge system has a degree-5 eliminant over Q reconstructed by CRT from 41 primes and verified at 6 held-out primes, and its residual collapses to 27 conditions in 6 parameters (`canon/HUNT_REPORT.md` items 1, 1b, 1c). The tools already present and unused are python-flint 0.9.0 and gmpy2 2.3.1; Singular's `lift(I, ideal(1))` is never invoked anywhere in the tree.

Method.
1. Build `cert_find.py`: compute the weight of every generator and monomial; for target degree D, emit the graded linear system A x = e_1 restricted to the contributing weight block; solve exactly with flint, or by multi-prime solve plus CRT plus rational reconstruction when a block exceeds about 40,000 unknowns.
2. Degree ladder: rank-test mod p at D = maxdeg + 1, +2, ... up to 12. The smallest consistent D is the working degree. Failure at every D up to 12 is "no certificate at D", never evidence of non-emptiness (the effective Nullstellensatz bound is far beyond reach); record it and hand the object to Lead F as a live target.
3. Verify: expand sum h_i f_i in exact rational arithmetic and assert it equals 1. Store the certificate with a hash and the expansion log. A referee can re-check it by one multiplication.
4. Independent route on the same object: Singular `degBound` ladder then `lift`, verified the same way.
5. Lucky-prime screen, as a search heuristic only: GB at 12 or more primes p = 1 mod 3 across bit sizes; majority leading-term signature; discard minority primes; record the batch. Control primes 5, 11, 17 must be rejected by the selector. This step carries no evidential weight. The acceptance criterion for EMPTY over Q is exactly one thing: explicit cofactors h_i in Q[x] with 1 = sum h_i f_i, verified by exact expansion against the original saturated generator list (the Rabinowitsch variables inside the f_i) by an independent checker. The check "every input generator reduces to zero modulo a lifted basis G and G passes Buchberger's criterion" establishes only that the ideal generated by G contains I; it is vacuous when G = {1} and certifies the opposite verdict: if that check passes and 1 is not in the ideal generated by G, then I is proper and its variety is non-empty. Keep it, labelled as a NONEMPTY certifier, and never use it for EMPTY.
6. Two-sided self-test before any real data: a planted-consistent system must not certify 1 at any D up to the bound; a planted contradiction must. Ship the tool failing rather than delete it.
7. Case (2): promote the w = -4 degree-5 eliminant to PROVED-exact by an exact char-0 elimination on the block; prove irreducibility exactly with `factorize` or PARI `polisirreducible`; run the 27 conditions in 6 parameters over K = Q[t]/(g) in a Singular algebraic-extension ring; extract cofactors; repeat for every open w-block on both charts. Fall back to the certificate form over the degree-1144 field only if this stalls. Re-run the modular verdict at two more compliant primes.
8. Apply the promoter to every EMPTY produced by Leads C, E, F, G and to the 20 single-prime above-125 shapes and the F3 result (MISS-6).

Agent roles. Certificate engineer; lucky-prime certifier; structurist (weights, blocks); number-field specialist; adversarial verifier who re-expands every certificate in a second CAS and owns the controls; ledger scribe.

Inputs. `canon/lift/lift_pipeline.py`, `pq/trackB_exactQ.py`, `pq/trackB_Q_elim.sing`, `canon/wave1/edgeQ_eliminant.txt`, `canon/wave1/edgeQ_param.out`, `canon/HUNT_REPORT.md`.

Outputs. A reusable certified promoter [CERTIFIED only with both self-tests firing]; case (2) over Q [PROVED-exact] or NO VERDICT with the stage reached; per-system prime batches and majority signatures; an explicit list of EMPTYs that could not be promoted.

Stop rule. Per object: abandon when the graded block exceeds 200,000 unknowns, or D reaches 12 without consistency, or after 8 CPU-hours; label NO VERDICT. Case (2): 24 h on the extension ring, then the certificate form, then NO VERDICT at 200 CPU-hours. A system gets at most 12 primes and one lift attempt. Never let a failed certificate search become "probably empty" prose. Unstable reconstruction across primes on case (2) is a finding that the mod-p EMPTYs may be reduction artefacts; stop and report it.

Cost. Three agent-days of build; case (2) tens of CPU-hours; the promoter itself runs inside the light lane because every stage checkpoints by weight block.

p(HIT). About 0.2 percent, and only in the sense that a five-prime modular EMPTY turning out non-empty over Q would be extraordinary. This is the lead that changes the epistemic status of everything else.

### Lead E. The (9,27) leaves in Groebner-only mode after a torus quotient

Target. `p11/wave6/ms/p108_525122.ms` (28 vars, 140 eqs, 5 leaves, 3 EMPTY, 2 unresolved) and `p11/wave6/ms/p108_192622.ms` (40 vars, 1 unresolved leaf of 139 equations in 38 variables): the first independent test of GGHV Cor 5.7. The files are on the pentagon Codex branch, not the canonical branch.

Premise. OPUS43-012 showed both systems have grading-torus rank 5, hence are positive-dimensional, so their 1800 s solve-mode timeouts were structural; both were sliced with a validated gauge (weight-minor determinants -1/24 and -1/14) and reported "running now", and no verdict was ever harvested (`mailbox/AGENT_MAILBOX.md:1597-1680`; `mailbox/wave6/frontier/P108_RESULTS.md`). Cor 5.7 is unproven by local audit and the literature is silent. FABLE-004 argues the campaign's "(9,27)" label named a case the paper already discarded; every artifact must carry (m,n).

Method.
1. Re-derive the rank-5 grading independently, with a proof that every orbit meets the slice, not just a nonzero minor.
2. Quotient by the torus to remove 5 parameters exactly, checking with a planted point that the quotient preserves the solution set.
3. Re-export, sanitize, hash, register.
4. msolve `-g 2` on the three unresolved leaves at three compliant primes, 6 to 8 h each, in parallel with Singular `facstd`, on the heavy host.
5. Pre-registered verdict standard both ways: EMPTY at one prime is replication-grade only; NON-EMPTY needs the full prime tower and a char-0 lift before the word "refutation" is used about GGHV section 5.
6. Promote any EMPTY with Lead D.

Agent roles. Grading auditor; solver runner; certificate engineer; lifter; adversary.

Outputs. Per-leaf EMPTY-mod-p(p1,p2,p3) or NON-EMPTY to the lift queue; with all leaves EMPTY and certified, an independent non-Cor-5.7 closure of the orientation.

Stop rule. Per leaf three primes at 8 h; any zero-dimensional non-empty parametrization freezes the fleet.

Cost. About 9 CPU-hours if the leaves decide; 50 to 100 with resisters.

p(HIT). One to two percent of a NON-EMPTY on some leaf, the highest per-run figure on the board because the only thing that ever closed this orientation is a proof with a hole; conditional on NON-EMPTY, perhaps one in four that it is a real point rather than a slice or gauge artefact, and then still a necessary-condition system.

### Lead F. Pentagon case (1) by reformulation, plus the collision-first search

Target. Case (1) of (72,108) at corner (8,28) with (m,n)=(3,2): the only branch with no verdict of any kind.

Premise. Both engines OOM on the 186-variable form; msolve is structurally excluded above about 180 variables (2^25 hash-table ceiling, segfaults; `mailbox/AGENT_MAILBOX.md:1053,1233`). Every truncation of weight at least 8 is certified alive by `pq/trackB1_pentagon.py:432 witness()` (an exact rational point over Q), so the truncation ladder is futile and any kill of case (1) must use equations of weight at most 7; W=19 is also underdetermined by 6. Three rational-function cascades failed their own two-sided self-tests; attempt 3 would have falsely killed this lead. Three reformulations exist on paper and none was executed: FABLE-003's reduction (Q is linear and redundant; the pentagon is a 57-variable rank-drop condition on a 303 by 124 structured matrix with exactly one inhomogeneous equation; `mailbox/AGENT_MAILBOX.md:3562-3675`); the bilinear split into c-block and d-block variables (`wave6/frontier/tb1_square_block.json`), under which for each fixed d-block the system is linear in the c-block and existence becomes a rank condition on M(d); and the exact coupled level ladder from level 16 downward with the W-variable coupling and bounded-support end conditions retained (`l16/breakthrough/PENTAGON_LEVEL16.md`, `PENTAGON_LEVEL15_BRANCH2.md`). The bottom-edge Galois structure was claimed and retracted at the fifth prime, so it is unknown how many independent admissible seeds must be tested. The seed-pinned, linearly reduced twin (241 eq / 123 unk) survives every linear consequence, a weak positive signal. The deck-group result says a plane counterexample must be a non-Galois covering of degree at least 3, resting on un-re-derived inputs (Bayle-Beauville; Ramanujam-Morrow).

Method.
1. Gate G6 first: count the header of `mailbox/wave6/frontier/trackB1_sat_Q.ms` and verify the char-0 lift at a third prime never used in the reconstruction (it was lifted from 1000003 and 65521 and verified only by re-reduction to those two).
2. Factor the degree-9 bottom-edge eliminant over Q directly (the char-0 bottom edge solves in 316 s) to settle the orbit structure exactly.
3. Independently re-derive FABLE-003's reduction with a second agent; require it to reproduce a known EMPTY and a known NON-EMPTY control before it is trusted. If it holds, attack the rank-drop locus with modular rank profiles across many primes and exact minor certificates, never a monolithic Groebner basis.
4. Bilinear projection: verify every one of the 284 equations is bilinear in the c/d split; apply the free branch (c_1_0 d_0_1 = 0 and c_1_0 d_1_1 = 0 with c_1_0 saturated nonzero); build M(d), compute its generic rank at random points, form the minor ideal, and run the d-block-only system (tens of variables) in msolve `-g 2` and Singular `facstd` at three primes. Planted-solution control: plant a c-solution over a random d-point and confirm the minor formulation recovers it.
5. Continue the exact level ladder to levels 14 and below on both branches, retaining every kernel constant and the coupling W9 = g9 - (3c1/2c0) z^4 h5, W8 = g8 - (3c1/2c0) z^4 h4, and the end condition [z^19]K16; decompose the a0 = 0 and F3 = 0 strata.
6. Collision-first augmentation, used only as an interpretation tool on a cell that has already returned NON-EMPTY on its base system, never as a primary search: the augmented variety projects onto the base variety by forgetting the two points, so it can never hit where the base is empty, and its probability is bounded by the base cell's. Add unknown source points p, q with P(p) = P(q), Q(p) = Q(q); saturate distinctness in two charts t (x1 - x2) = 1 and t (y1 - y2) = 1, with EMPTY requiring both charts (the sum-of-squares form deletes the isotropic lines y1 - y2 = plus or minus i (x1 - x2) over C, which is an unsoundness for EMPTY, not a modular nuisance); normalize det J = 1 or saturate the constant, since the component det J = 0 satisfies the collision block vacuously; add leading-coefficient saturations pinning deg P and deg Q; and add a characteristic-p negative control that Artin-Schreier and Frobenius-type non-injective Keller maps are excluded by the shape equations, since over F_p such maps are abundant and a modular NON-EMPTY is close to noise. A solution over C with these guards is a genuine counterexample (a non-injective Keller map of C^2). Two-sided self-test on a known non-injective map and a known automorphism before real data. One agent-week cap.
7. Any candidate: Hensel lift, exact substitution, bijectivity check with `wave6/w6_bijcheck.py`, then H1 to H6.

Agent roles. Reconciler; structurist; reduction auditor (two-sided controls); rank-profile specialist; ladder mathematician; search engineer (exact only; no floating point in the tool allowlist); witness auditor with veto.

Outputs. Orbit structure [PROVED-exact]; a rank-drop or bilinear reformulation [CERTIFIED only after both controls fire, else shipped as FAILING]; a first verdict on the pentagon, most likely still NO VERDICT, said plainly; any candidate CANDIDATE-UNVERIFIED until H1 to H6 pass.

Stop rule. Kill the bilinear lead if any equation is not bilinear or the minor ideal exceeds about 120 variables. Kill the ladder when a level branches without closing twice in a row. Absolutely no numerical multi-start at any size.

Cost. About two agent-weeks; 60 to 120 hours on the heavy host for the reduced systems.

p(HIT). At most 0.3 percent across the reformulations; the pentagon has resisted only on memory, so the resistance carries no information about emptiness, but nothing in the archive is evidence that the cell is non-empty either.

### Lead G. The 24 published cases at max degree 125 to 150, starting with (8,28)/(3,4)

Target. The records of `canon/gghv_audit/all_cases_max_le_150.json` with max at least 125, including the boundary case (75,125) that GGHV's strict inequality does not cover, and GGHV Proposition 4.3's second sub-case (70 unknowns, 92 equations, 21 variables after gauge; FABLE-004).

Premise. GGHV eliminate max below 125 only; arXiv:1708.07936 enumerates to 150 and discards nothing above 125. These 24 cases have printed chain data, so they need no chain-compiler extension; the sub-150 chain-to-polygon map is resolved in `canon/campaign/audit_tracks/TRACKD_CHAIN_MAP.md` and reproduces all six published reduced pairs. The invariant eps_P + eps_Q = (r+1, 1) is a gate on any candidate reduced pair. Naive pattern-fitting from (9,27) and (8,28) provably fails and produced three retractions. FABLE-006, the unanswered head of the mailbox, names (8,28)/(3,4) at (108,144) as the first new target; its artifacts live on `claude/fable-counterexample-sweep-yyj5vf`, which is not in any local worktree.

Method.
1. Lead A step 3 must pass first (the table verified against the PDF).
2. Register one row per case keyed by (corner, (m,n), orientation, max).
3. Compile record 22, (8,28)/(3,4), first and drive it to a labelled verdict end to end as the pipeline test; only then compile the other 23 through the resolved chain map with the six-pair regression and the eps invariant as gates. No work under this lead touches anything above max 150; that region belongs to Lead I.
4. Content-hash and dedupe before scheduling.
5. Sweep smallest first at 900 s and two compliant primes; escalate resisters to 1800 s and the second engine; run the cheap torus-rank probe before any budget extension; try a degree-3 Nullstellensatz certificate on one resister to decide feasibility of that route for the class.
6. Build Prop 4.3 sub-case (2) from the polygons and test whether D = 1 is compatible with its polygon at all (FABLE-004 suggests this may kill it in one line); run it at three primes.
7. Bridge the 20 existing single-prime above-125 EMPTYs to two more primes, then to Lead D.

Agent roles. Librarian; compiler; registrar; scheduler; solver runners; Nullstellensatz specialist; adversary.

Outputs. A 24-row closure table with no blank rows; sub-case (2) verdict; the enumerable resister list.

Stop rule. Per case two primes at 1800 s plus one torus probe plus one certificate attempt, then NO VERDICT. Fleet-wide 200 CPU-hours.

Cost. Compiler build about one agent-week; 24 to 200 CPU-hours.

p(HIT). Roughly one percent that some case returns NON-EMPTY and about 0.3 percent that one survives lifting and the HIT protocol. The dominant value is a publishable closure from 125 toward 150.

### Lead H. Structural routes with a hard cheap gate each

Three items, each gated so that a two-hour audit decides whether the rest is launched.

H1. The twisted plane sweep above Moh. The dimension-3 mechanism (tangent sweep, arXiv:2608.00222) is already a plane map whose only defect is det J = 2 gamma. The archive proved no polynomial conjugation repairs it and wrote the general division-twist identity C{P,Q} - j Q{P,C} + i P{Q,C} = kappa C^(i+j+1), calling it "the object nobody has written down" (`canon/CATCHES.md`). The only search on it produced maps of total degree at most 32 and was killed as vacuous by Moh; the dichotomy's twist rebuttal appears to be proved only for w = gamma u, C = gamma x^s. Gate G12 decides. If the dichotomy is not general: generalize the ansatz to degree 2 in the sweep parameter and to monomial reparametrizations in K[x, x^-1, y] (FABLE-005's unanswered ask), write the general system with cofactor unknowns for the divisibilities, apply the Moh and gcd pre-flight gate, solve surviving shapes at two primes then char 0, and label negatives with their degree scope. p(HIT) about 3 percent conditional on the gate opening; about 35 percent that the gate alone narrows the "sweep is dead in the plane" headline to a scoped statement.

H2. Weyl-algebra deformation cascade. The known implications are DC_n implies JC_n, and JC_2n implies DC_n (Tsuchimoto 2005; Belov-Kanel and Kontsevich 2005 to 2007). The lead uses the contrapositive of JC_2 implies DC_1: a pair X, Y in A_1(C) with [X,Y] = 1 generating a proper subalgebra refutes DC_1 and hence JC_2. That passage runs through reduction mod p and is not known to be effective, so a DC_1 witness yields the statement "JC2 is false" without an explicit plane map, and the HIT protocol cannot be run on it; this must be stated in any write-up. Prerequisite before any hbar work: the quasi-classical shadow of a Weyl pair with [X,Y] = 1 is a Poisson-commuting pair, whereas the archive's pinned systems satisfy {P,Q} = x^r; prove or refute that the pinned systems are the associated-graded shadow of the Weyl problem, or the tower is built over the wrong base point. Set the deformation up as a filtered (Rees) deformation of a fixed-degree pair so the tower is finite. Each rung is linear over a branching lower-order solution variety, not a single obstruction class, so the same branch-covering discipline and coverage proof demanded of the cascades applies. Two-sided self-test and the vacuity pre-check before real data. p(HIT) at most 0.3 percent; an obstruction at finite order would be a char-0 kill on a cell Groebner cannot reach.

H3. Euler-characteristic additivity over the fibration P = const as a targeting device (not Riemann-Hurwitz, which is the properness-dependent statement FABLE-005 already retracted). For a polynomial P on C^2 with bifurcation set B(P) of size k, 1 = chi(C^2) = (1 - k) chi(F_gen) + sum over c in B(P) of chi(F_c), valid with no properness assumption. The content sits in the corrections at infinity (vanishing cycles at infinity, as in Broughton's x + x^2 y), which can be read from the Newton polygon only when P is convenient and Newton-nondegenerate (Kouchnirenko; Nemethi and Zaharia); FABLE-002's own conclusion was that the constraint forces P Newton-degenerate, so the read-off is inadmissible on exactly the shapes of interest unless a degeneracy audit says otherwise. Per shape: check nondegeneracy first; if degenerate, the ledger entry is NO VERDICT, not a kill; a kill requires an inequality-form bound on the at-infinity term valid in the degenerate case. Consistency is never a verdict. Read Nguyen Van Chau, Orevkov and Suzuki-type chi formulas first so the identity is labelled LIT-READ or genuinely new. Record a domain probe on which the identity is required to fail (linter rule L3). p(HIT) zero directly; expect it to void most targets rather than kill them.

### Lead I. The tail: enumerate the 41 shapes, run the tail-closure test, discharge A'_t

Target. Turn the two largest "unsearched" regions from folklore into lists.

Premise. The 41 timeout shapes are listed in no file. The 429 NO-CHAIN records need a compiler extension against polygons published nowhere. The tail-closure predictor (last two segments plus shape index to system hash) has zero violations across 16 groups and the library is 34 chains to 26 distinct tails (`canon/CROSSDOOR.md` section 5); the 20-sample saturation test assigned in OPUS43-012 was never run.

Method.
1. Scan every log for exit 124, 0-byte outputs and TIMEOUT rows; hash each system; emit `TIMEOUT_SHAPES.json` with size, torus rank, keys, budget, engine and stderr digest. Expect the count to shrink.
2. Sweep the deduplicated list smallest first at 1800 s and two primes, with the torus-rank probe before any escalation.
3. Audit the compiler for factorization: read the chain-to-reduced-system construction and determine, as a proof or a refutation, whether the extracted coefficient system depends on chain entries before the tail. This is cheaper than sample compilations and actually settles the question; the 34-to-26 zero-violation figure is a fit on the same data the predictor was read from and is not a test. Keep a 20-sample count only as a corroborating measured number and hold the saturation claim at CONJECTURE regardless of the rate. Tail-closure deduplicates compute and has no evidential effect on any verdict; a shared tail system still needs per-chain lifting because the degree pairs differ. Authorize the compiler extension only if the factorization audit proves the tail dependence.
4. Discharge A'_t for (10,40) inside `ggv_algorithms.py` (Lead A step 2).

Outputs. `TIMEOUT_SHAPES.json`; a factorization proof or refutation for the compiler, plus `TAIL_SATURATION.json` as a measured corroboration only; A'_t PROVED-exact or a new census row.

Stop rule. The factorization audit alone decides the compiler question.

Cost. About 1.5 agent-days plus 120 core-hours in the light lane.

p(HIT). Under 0.1 percent.

### Leads dropped or deferred, with reasons

- The pentagon truncation ladder (W=19 and every truncation of weight at least 8): refuted by `witness()` in `pq/trackB1_pentagon.py:432`; W=19 is also underdetermined by 6. Remove from every queue. The open-queue file still ranks it first; that ranking is the bug.
- The rank/bifurcation criterion and its extension to d=48, 75: a can't-fail certifier.
- Any numerical multi-start lane as evidence: retracted; a HIT would be real, a MISS says nothing.
- Direct Groebner on d=9, 10, 11: 32 times per level; blocked until a self-tested cascade or the certificate route works at d=8.
- Monolithic Groebner on the 186-variable pentagon as a scheduled job: four attempts, four NO VERDICT, and msolve is excluded above about 180 variables. Permitted once as a lowest-priority background run in the heavy slot (the degree-2 saturated form timed out at 1.5 to 2.3 GB, so it is time-bound, and the heavy host buys time); a second run with no degree progress ends the lane. No schedule may depend on it.
- The Weyl-algebra cascade in week one: deferred until the base-point question is settled and the fourth cascade has passed or failed its self-test.
- The 429 NO-CHAIN frontier as a search target: blocked on the compiler; gated by the compiler factorization audit in Lead I.
- Anything built on the printed GGV (1.2).

## 4. Fleet design

Roles and contracts.

| Role | Contract |
|---|---|
| Librarian | Owns provenance: exact-quotation anchors for every literature step (file:line), the case register, the reconciliation of counts; labels absent artifacts UNVERIFIED-HERE, never confirmed |
| Generator / compiler | Builds systems from chain data through the resolved map; gates every output on the six-pair regression and the eps invariant |
| Exporter / sanitizer | Every `.ms` passes `w4_msformat.py`; coefficients in [0,p), no zero terms, no constant generators, round-trip re-parse; records the gauge with its admissibility proof and torus rank |
| Prover / solver runner | Runs only jobs the scheduler admits; stdout and stderr teed; exit codes ignored; a verdict read only from a non-empty output matching a documented pattern |
| Certificate engineer | Produces cofactor or lifted-basis certificates; never the same agent that produced the verdict |
| Lifter | Hensel to p^(2^K), rational reconstruction, exact substitution; labels CANDIDATE-UNVERIFIED and nothing stronger |
| Witness auditor | Owns H1 to H6; has unilateral veto; fixes all three gauges and uses an absolute normalization before evaluating anything |
| Adversary | For every new tool, builds the two-sided self-test and the negative control; for every claim, tries to refute it; may void |
| Ledger scribe | One verdict per commit, pushed immediately; the contradiction linter runs on every commit |

Job schema (`job.json`): content hash of the canonicalized generators; n_vars, n_eqs, max degree, term count, excess, torus rank; characteristic and prime list; engine, engine hash, exact flags; wall, memory and disk budgets; orientation key (degree pair ordered, corner, (m,n), chart, gauge with proof reference); provenance (generator script, corrected or printed, parent hash); lane; score.

Verdict labels: PROVED-exact (char 0 with a certificate a third party can re-check; for EMPTY this means explicit cofactors with 1 = sum h_i f_i against the saturated generators); CERTIFIED (engine input, captured output, and an independent certifier with a negative control observed to fail); EMPTY-mod-p(p1, p2, ...) (at least two compliant primes; never promotable without Lead D); TIMEOUT; OOM; FAILURE (parse error, missing engine, ENOSPC, segfault, empty output, or `[-1]` with any parse error); ADMISSIBLE-SHAPE (a non-empty point on a reduced-polygon coefficient system, i.e. admissible leading data only, not yet completed to polynomials); CANDIDATE-UNVERIFIED (explicit P, Q in Q[x,y] exist but H1 to H6 have not passed); HIT (H0 and H1 to H6 all passed with H6 shown to have fired).

Gates as code (`gate.py`), each blocking: no verdict from empty output; stderr captured and clean; export sanitizer; no constant generators; excess above zero for emptiness runs; torus-rank routing (solve mode forbidden on positive-dimensional input); degree bound bites (D above max input degree; gbsize equal to the input count is a no-op sentinel); prime hygiene with control primes rejected; lucky-prime majority; modular verdicts never stand alone; two-sided self-test on every reducer, including the (a=3, b=4, c=2) regression; planted-root control for any numerical lane; AST scan for literal-True checks; certifier negative control observed to fail; content-hash dedup; ansatz degree gate (max degree above 100, gcd 16 or above 20, below 125 only (72,108)); engine present and pinned; disk and inode headroom; PID-verified running claims; no `pkill -f`; orientation in the key; contradiction linter; HIT protocol complete.

HIT protocol (`canon/reruns2/w3_hit_protocol.py`, also on `p11/reruns2/`), with the reviewer's sharpenings: H0 exact reconstruction, added ahead of the file's gates: an exact characteristic-zero point (modular points carry no information, since JC fails in characteristic p), completed to explicit P, Q in Q[x,y] with verified degrees; failure to complete leaves the record at ADMISSIBLE-SHAPE. H1 exact rational coefficients, no floats on the decision path. H2 Keller constancy as a global symbolic identity: det J(P,Q) minus c expands to the zero polynomial with c in Q*, never sampled. H3 non-injectivity by two distinct exact algebraic points with P(p) = P(q) and Q(p) = Q(q) verified in an exact number-field representation. H4 the field degree [C(x,y) : C(P,Q)] at least 2 by exact resultants, an independent route. H5 invariance under random affine coordinate changes on source and on target (the step both historical false positives would have failed). H6 the gate rejects the known negatives and accepts the positive control before it runs. H2 and H3 alone constitute the proof; the rest are hygiene and corroboration. Any single failure reports the failing step and claims nothing.

Scheduler policy. Refuse vacuous jobs; score expected information per core-hour (1.0 for a cell with no verdict by any method; 0.6 for single-prime to multi-prime; 0.5 for EMPTY-mod-p to PROVED-exact; 0.1 for re-confirming a multi-prime EMPTY; 0 for a can't-fail criterion); ties by size ascending; two lanes (light: under 15 minutes and 8 GB per sibling run, one verdict per commit; heavy: single slot, 18 h and 100 GB caps, checkpointed); re-cost after every verdict; publish `queue.json` and `REFUSED.json`. The scheduler is accepted when it refuses the truncation ladder on the excess gate and independently surfaces d=8 chart N, the p108 leaves and case (2) over Q; it must not be tuned to reproduce the open-queue file's hand ranking, which puts a refuted lead first.

## 5. Milestones and stop conditions

Two-week schedule for a fleet of six to eight agents.

| Day | Work | Deliverable |
|---|---|---|
| 1 | Lead B: provisioning, engine guard, schemas, content hashing; Lead I step 1 scan; Lead A steps 1 to 3 begin | `engines.json`, first hashed register, timeout list draft |
| 2 | Lead B: runner, serial heavy queue, watchers, gate.py in CI; smoke suite across a forced restart; gate G2 (Cor 5.7 position) | First verdict committed unattended; one Cor 5.7 position |
| 3 | Lead B: re-key the tree, `RECONCILIATION.md`, scheduler; AST scan triage; gates G3 to G6 | Reconciled counts; README asset located or struck |
| 4 | Heavy host live. Lead C: d=8 chart N launched by three routes; Lead I: smallest-first sweep starts; Lead F step 2 (eliminant factorization); Lead H gate G12 | d=8 in flight; orbit structure exact; sweep-dichotomy scope statement |
| 5 | Lead D: lucky-prime screen and multi-prime batches on case (2); Lead I compiler factorization audit and A'_t; Lead A enumeration divergences traced; Lead G sub-case (2) D = 1 compatibility check | Factorization proof or refutation; A'_t discharged or expanded; go or no-go on sub-case (2) |
| 6 | Lead D: CRT, reconstruction, exact verification, certificate self-test; Lead F: reformulation audits begin; Lead A step 3 PDF check | Promoter passing both self-tests |
| 7 | Midpoint audit: read the ledger, not the plan; confirm no TIMEOUT drifted into prose; AST scan at zero; every verdict has a prime list | Audit note |
| 8 to 9 | Lead D on case (2) to completion; Lead E leaves with torus quotient in `-g 2` mode; Lead G record 22 driven to a verdict, then the other 23 compiled behind the regression gates | Case (2) over Q or a recorded stage; leaf verdicts; record 22 labelled |
| 10 | Lead F reformulation acceptance (controls) or FAILING commit; Lead C d=12 unsaturated; Lead H1 if the gate opened | Reformulation status |
| 11 to 12 | Lead D on d=7 and chart Z d=8..12; Lead G smallest-first sweep; Lead C symbolic-d attempt continues | Promotions or explicit non-promotions |
| 13 | Lead C d=27 by certificate only; Lead H2 cascade self-test verdict | Cell verdicts or NO VERDICT with D-ceiling |
| 14 | Freeze. Every job carries a label from the vocabulary. Publish reconciled counts, the enumerated timeout list, the compiler factorization verdict, every char-0 promotion with its certificate, and the honest list of what is still TIMEOUT, OOM or NOT RUN with its measured wall | Write-up |

Candidate escalation. Any NON-EMPTY on any system freezes all other lanes; the lifter and the witness auditor take over; nothing is said aloud until H1 to H6 pass with H6 shown to have fired. Both historical false positives were gauge artefacts that H5 would have caught.

Campaign stop condition. Stop the hunt and convert to write-up when any of the following holds: (a) Lead A confirms the sub-125 enumeration is complete, case (2) closes over Q, and the pentagon closes or reduces to a positive-dimensional stratum provably not a counterexample locus, at which point the honest statement is that the plane conjecture holds below max degree 125 with the (72,108) closure unconditional; (b) two consecutive audit cycles produce zero new verdicts and zero corrections; (c) the gates cannot be passed at all (no persistent host, engines unavailable, register still self-contradictory), in which case no further compute can produce a defensible verdict and the correct move is to publish the correction ledger.

Definition of done. Not a counterexample. A repository in which every verdict row carries characteristic, prime list, orientation, (m,n), corner and a certifier triple; no EMPTY is mod-p only without the label; no timeout or OOM appears as a verdict; the census has one number per region with a generating script and 804, 189, 184 recorded as unsupported; every load-bearing literature step is re-derived or labelled UNVERIFIED-HERE; at least one new char-0 exclusion theorem exists; and the README describes objects that exist.

## 6. Open questions the fleet must resolve first

1. What exactly does GGV Theorem 1.2 say on the page? The reviewer could not verify the iff from any artifact here, and the plan already adds the cell-pinning saturation and the reconstruction gate H0 in anticipation; the page-image read is Lead C step 1.
2. Resolved by the soundness review: the reduce-to-zero-plus-Buchberger check certifies containment and hence NONEMPTY when 1 is absent; EMPTY over Q is certified only by explicit cofactors. Lead D now says so.
3. Resolved in direction (the contrapositive of JC_2 implies DC_1 is correct) but not in effectivity, and the base-point question (Poisson-commuting versus {P,Q} = x^r) is open; see Lead H2.
4. Is the sweep dichotomy proved for general (C, i, j) and general gamma-degree? Gate G12.
5. Does the truncate(W) closure lemma matter anymore, given the witness makes every truncation non-empty? It does not for kills; it still matters for any future claim that a truncation constrains the full system.
6. Which (8,28) row does each existing artifact belong to? Gate G3.
7. Where are the FABLE artifacts (`FABLE_24_OPEN_CASES.md`, `fable_xcol/`, `session43/LEADS.md`) and `gghv.txt`? They are referenced in the record and present in no local worktree. (`trackB1_sat_Q.ms` was found: it is on the mailbox branch under `wave6/frontier/`.)
8. Is the Nguyen 2025 floor of 104 a real refereed result? One reader found it, one could not.
9. Resolved: it does, and Lead F step 6 now normalizes det J, pins the degrees, uses two distinctness charts, and adds a characteristic-p negative control; the augmentation is demoted to an interpretation tool.
10. What is the true Nullstellensatz degree for the small live objects? If it exceeds about 12, the certificate route returns "no certificate at D" and the objects stay EMPTY-mod-p; no other route promotes them, since the lucky-prime pipeline is a heuristic with no evidential weight.
11. Are the archive's pinned bracket systems {P,Q} = x^r the associated-graded shadow of the Weyl problem, whose shadow is a Poisson-commuting pair? Lead H2 cannot start until this is settled.
12. Which of the 24 above-125 shapes are Newton-nondegenerate? Lead H3 is admissible only on those.

## Appendix: provenance

- `docs/plans/appendix/READER_MAP.md`: the nine reader reports (verdict map, open queue, failure catalogue, pentagon route, bottom-seed asset, tail census, mailbox thread, toolchain, literature), each with file citations.
- `docs/plans/appendix/plan-*.md`: the five planner outputs (enumerated corners, characteristic-zero verdicts, structural routes, fleet engineering, skeptic).
- `docs/plans/appendix/review-*.md`: the three adversarial reviews (premise file-check, mathematical soundness, redundancy and ordering).
