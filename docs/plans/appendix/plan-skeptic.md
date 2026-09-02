```json
{
  "angle": "Adversarial audit-first replan. I assume JC2 is TRUE, so the only defensible deliverables are (a) certified exclusion theorems in characteristic zero and (b) corrections to the literature's exclusion chain. Every lead is scored on whether it produces a citable artifact even when the answer is EMPTY, because EMPTY is the overwhelmingly likely answer.",
  "thesis": "This campaign is not blocked by mathematics or by RAM. It is blocked by a broken bookkeeping layer: the same shape is filed under three different labels, the same region under five different cardinalities (429/464/804/474/24), the flagship asset in the README (164/288/6821) does not exist on disk, the #1-ranked lead in the current queue (the W=19 pentagon truncation ladder) was proved NON-EMPTY by a witness function that has been sitting in the repo the whole time, and the campaign's own two authoritative sources disagree on whether GGHV Cor 5.7 kills (9,27) or is invalid. Meanwhile the genuinely valuable target — an exact characteristic-zero closure — is repeatedly deferred in favour of new mod-p sweeps that the campaign's own rule forbids promoting. Roughly 40% of the residual compute queue is provably vacuous, and of the rest, the honest verdict-bearing surface is three objects, not thirty. The single highest-value thing on this board is not a solver run at all: it is that GGHV Thm 2.1 imports its ten-case table wholesale from [5]'s Algorithms 1-9, and the campaign's own independent re-implementation already found chains that [5]'s printed tables omit. If the sub-125 enumeration has a hole, the '(72,108) is the only survivor' premise — the premise the entire campaign is built on — is false, and that is checkable in a day with no Groebner basis.",
  "waste": [
    {
      "item": "The W=19 pentagon truncation ladder is still ranked #1 in the live queue despite being refuted inside the repo. trackB1_pentagon.py:432 witness() gives an exact rational point satisfying all equations and side conditions for W=12..19, so every truncation in that range is certifiably NON-EMPTY and can never yield an EMPTY. Two weeks were spent at W=19, which is underdetermined by 6; msolve OOM'd because its default parametrisation mode requires dimension 0. CATCHES.md says 'P0 IS FUTILE' and withdraws the plan; the open-queue reader nevertheless ranks it rank 1 with the reasoning 'every failure so far was memory, not mathematics'. That reasoning is wrong: the failure is targeting.",
      "evidence_path": "wt/canon/CATCHES.md ('P0 IS FUTILE', 'PENTAGON TRUNCATION', 'FOUND IN PLAIN SIGHT'); wt/pq/trackB1_pentagon.py:432; wt/canon/WEEKEND_PLAN.md §P0",
      "action": "Delete the truncation ladder from every queue and register. Add the eqs-minus-vars pre-flight gate as a hard scheduler check: refuse to launch any emptiness run with excess <= 0."
    },
    {
      "item": "Verdict inflation on the B=16 chart-Z ladder. STATE_FULL §A records d=8 EMPTY at 2 primes and d=9,10,11 EMPTY at a single prime as if these were cell closures. They are not: (i) mod-p is never char 0 by the campaign's own rule; (ii) chart N of the same cells was never run, so the cell is not covered; (iii) a large part of that work was done on the misprinted GGV (1.2), which makes it a statement about V_true intersect ({mu3=0} union {q1''(0)=0}), a proper subvariety — void as a statement about B=16.",
      "evidence_path": "wt/canon/STATE_FULL.md §A; wt/canon/OPEN_ITEMS.md header; wt/canon/CATCHES.md ('GGV (1.2) ROW 3 IS MIS-PRINTED', 'THE DAMAGE, EXACTLY')",
      "action": "Re-label every pre-correction B=16 row VOID in one pass, and forbid the word EMPTY on any cell where a chart was never run. Report cells, not charts."
    },
    {
      "item": "Regions already excluded by literature, or vacuous by a known theorem, still being swept. The 1728-shape plane sweep produced maps of total degree <= 32 against Moh's floor of 100 — zero information by construction. The rank/bifurcation criterion was run at d=3..15,18,20,27 and headlined as DECIDED; it is a can't-fail certifier (6*mu0 - 2*a2*mu2 = 0 with a2 = mu2 = 0 at the base point forces the reported answer), and WEEKEND_PLAN still proposes extending it to d=48 and d=75.",
      "evidence_path": "wt/canon/CATCHES.md ('TWO CATCHES ON MY OWN PLANE-SWEEP SEARCH', 'THE RANK / BIFURCATION CRITERION IS A CAN'T-FAIL CERTIFIER'); wt/canon/WEEKEND_PLAN.md §P2; wt/canon/OPEN_ITEMS.md §4",
      "action": "Retire the rank criterion entirely (including d=48/75). Install the Moh/GGV/GGHV pre-flight degree gate in the ansatz scheduler so no search can start below max degree 100."
    },
    {
      "item": "Numbers that do not reconcile, and two figures that exist nowhere. 429 = NO-CHAIN records in frontier_151_300_map.json (432 records total, max 156-300); 464 = admissible pairs in [125,300] from the queue-coverage audit; 474 = the independent gghv_audit re-derivation at max<=300; 804 = Session 41, explicitly disavowed by FABLE-006 as coming from lost Sessions 19-38 with no supporting artifact; 34/24 = the actual published enumeration (arXiv:1708.07936 §6, 34 cases at max<=150, 10 discarded below 125, 24 untouched). These are five different objects treated as one frontier. The '189 non-closing records' and '184 new tail hashes' figures match nothing: grep finds 184 only as the count of active pentagon unknowns and 189 only as a row index and a memory figure.",
      "evidence_path": "wt/canon/wave6/frontier_151_300_map.json; wt/canon/STATE_FULL.md §C; wt/canon/41.md; wt/hunt/41.md; wt/mailbox/AGENT_MAILBOX.md:3909-3985 (FABLE-006); wt/canon/CROSSDOOR.md §5",
      "action": "Publish one census table with a generating script per row, each row carrying its region definition and orientation convention. Mark 804, 189 and 184 NONEXISTENT in the record so they stop propagating."
    },
    {
      "item": "The README's flagship asset cannot be found. README.md:19-20 on main claims 'the reconstructed characteristic-zero bottom-seed target over Q(alpha), degree five: 164 variables, 288 quadratic equations, 6,821 terms' with 'an independently reproduced unit Groebner basis' at p=1000003. No such file exists in main, docs/, archives/transfer/state_transfer.tgz, or any of the seven worktrees. The nearest real object is trackB1_sat_Q.ms at 166 vars / 284 eqs / 8,774 coefficients / total degree 5 — different numbers, and 'degree five' there means polynomial degree, not a field degree. The claimed unit GB is corroborated by nothing: the local p=1000003 runs on the closest system are a 5400 s timeout with a 0-byte output and a four-row NO VERDICT ledger.",
      "evidence_path": "/home/user/jacobian_planar/README.md:19-20; wt/mailbox/AGENT_MAILBOX.md:246-260, 1419-1432; wt/p11/wave6/pentseed/seed0.log",
      "action": "Either fetch wave6/frontier/ from the campaign branch and count the file header directly, or amend the README. A claimed unit Groebner basis with no artifact is exactly the proxy-trust failure mode (M2) the campaign already documented."
    },
    {
      "item": "The (8,28)/(3,4) corner is being handled as if it sat below 125. In the campaign's own reproduction, A0=[8,1,28] with (m,n)=(3,4), final [7,4,3] gives the degree pair (108,144), max 144 — an above-125, never-searched case. The sub-125 survivor from that same corner is the (m,n)=(3,2) row giving (108,72). Mixing them misroutes compute between a region with a literature exclusion and a region with none.",
      "evidence_path": "wt/canon/gghv_audit/all_cases_max_le_150.json; wt/mailbox/AGENT_MAILBOX.md:3909-3985",
      "action": "Make (corner, (m,n), orientation, max) the primary key of every record. No degree pair may be filed without all four."
    },
    {
      "item": "Redundancy and double counting across branches. p108_821326 and p108_843700 are md5-identical and their EMPTY was double-counted; 49 TIMEOUT records collapse to 16 unique systems by tail hash; a sweep was re-running its own four-minute-old TIMEOUT under a new tag. Separately, 'Route 1 / Route 2' for case (2) are advertised as independent confirmation but are only file-level disjoint — both descend from the same GGHV polygon derivation, so a derivation error is invisible to both.",
      "evidence_path": "wt/canon/CATCHES.md §1, §2.3; wt/canon/STATUS.md §7 pitfalls",
      "action": "Content-hash every export before scheduling; store a unique-system map; stop calling code-disjoint routes independent."
    },
    {
      "item": "Unproved literature steps treated inconsistently — as kills in one file and as live in another, simultaneously. GGHV Cor 5.7 is recorded as verified against the PDF (lines 982-996) and killing the (9,27)/(2,3) shape in the mailbox lineage, and as having an invalid step at gghv.txt:1430-1433 with 51 of 66 conditions unsupported in CATCHES.md. FABLE-004 goes further and says the campaign's '(9,27)' label names a case the paper already discarded, so the compute spent on p108_* may be aimed at the wrong shape. Similarly, GGHV's '[4] discarded (80,112)' is a sloppy citation: the d=3 cell is solved in GGV but d>=4 was open and lies above 125.",
      "evidence_path": "wt/canon/CATCHES.md ('GGHV COROLLARY 5.7 IS UNPROVEN'); wt/mailbox/campaign/mod3_828/jc2_literature_sweep_partial.md:65-66,311; wt/mailbox/AGENT_MAILBOX.md:3676-3801 (FABLE-004); wt/canon/ADJUDICATION.md §2, §3",
      "action": "Resolve to ONE position before any further p108 compute. This is audit gate G1 and it is paper work, not solver time."
    },
    {
      "item": "The Z/N chart split and prime-size tuning are known-unnecessary work still present in plans. Seeding the row-0 root covers the whole cell (the relation is mu-free), and prime size buys nothing because the bottleneck is Groebner structure, not coefficient arithmetic. WEEKEND_PLAN §P1 still describes per-root seeding after OPEN_ITEMS §2 supersedes it.",
      "evidence_path": "wt/canon/MORNING_SUMMARY.md ('Two structural wins'); wt/canon/OPEN_ITEMS.md §2; wt/canon/WEEKEND_PLAN.md §P1",
      "action": "Regenerate exports with a_{2d} unseeded, one run per cell, primes chosen only so that 12d is a square."
    }
  ],
  "weakest_exclusions": [
    {
      "item": "The premise itself: '(72,108) is the only surviving pair below max 125'. GGHV Thm 2.1 does not derive the degree pairs; it imports a ten-case table from [5] (arXiv:1708.07936) Algorithms 1-9. The campaign's own independent re-implementation found two extra length-1 and four extra length-2 chains that [5]'s printed tables omit, and [5] §5's own prose says '2 admissible complete chains of length 2' while its table lists seven.",
      "why_weak": "If the enumeration behind the ten-case table is incomplete, then a sub-125 pair exists that nobody has ever looked at, and every downstream closure is a closure of the wrong set. This is the only place on the board where the campaign could be searching an empty room while the counterexample sits in the next one. It is also the only weakness that is pure combinatorics — no Groebner, no memory ceiling, no prime hygiene.",
      "evidence_path": "READER_MAP literature and tail-census sections citing wt/canon/gghv_audit/ggv_algorithms.py, all_cases_max_le_150.json; wt/canon/HUNT2_REPORT.md (T1)",
      "how_to_harden": "Re-derive the full max<=150 enumeration from [5]'s Algorithms in the existing re-implementation, with every divergence from the printed tables traced to its exact step and each extra chain carried forward to a degree pair or explicitly shown to produce none. Then compare against the paper's own §6 table page by page from the PDF, not from a text extraction."
    },
    {
      "item": "GGHV Corollary 5.7 as the sole kill of the (9,27)/(2,3) shape.",
      "why_weak": "One un-refereed preprint, one corollary, one step, and the campaign has a localised objection to it: after translation the bracket is 1/2 + (lambda/2)x^{-1/2}, not in K^x, so [1, Cor 7.2] does not apply, leaving 51 of 66 asserted coefficient conditions unsupported. Nobody has re-derived it. The two independent tests the campaign launched are both NO VERDICT: p108_525122 has 2 of 5 leaves unresolved, p108_192622 has 1 unresolved leaf of 139 equations in 38 variables, and their earlier timeouts were structural (grading-torus rank 5, positive-dimensional, so msolve solve mode could never terminate).",
      "evidence_path": "wt/canon/CATCHES.md ('GGHV COROLLARY 5.7 IS UNPROVEN'), gghv.txt:1412-1433; wt/mailbox/wave6/frontier/P108_RESULTS.md:11-26; wt/mailbox/AGENT_MAILBOX.md:1597-1680",
      "how_to_harden": "Re-derive (5.12) by hand and either repair it or write the counterexample to the step. If it does not repair, the shape reopens and the two sliced systems must be finished in Groebner-only mode (-g 2), never solve mode."
    },
    {
      "item": "(72,108) case (2): EMPTY mod p only, never char 0, and the campaign proved modular emptiness unsound for contradictions using its own tool.",
      "why_weak": "Three primes is evidence, not proof — and trackA_eliminator.py demonstrably closes a branch with a genuine rational solution (x-3y=0, x+4y-z=0 has (3,1,7) over Q but closes mod 7, and --verify replays it clean, exit 0). Two of the three quoted primes (32003, 65537) are 2 mod 3, violating the campaign's own hygiene rule. The 13-variable residual over the degree-1144 field K=Q[theta]/(f) — the thing that would actually settle it — was planned and never executed (MISS-4).",
      "evidence_path": "wt/canon/OPEN_ITEMS.md §5; wt/canon/CATCHES.md ('MODULAR ELIMINATION IS UNSOUND FOR CONTRADICTIONS'); wt/canon/STATE_FULL.md §B (MISS-4); wt/canon/STATUS.md §2.5",
      "how_to_harden": "Execute the char-0 residual. The irreducibility of the degree-1144 eliminant over Q is already PROVED-exact and independently re-verified at a 9th prime (100153), so all 1144 edge points are Galois-conjugate and the Q-bar question is a single yes/no — this is the one hard exclusion on the board that is genuinely within reach."
    },
    {
      "item": "Pentagon case (1) — the only branch with NO VERDICT of any kind, by any method, ever.",
      "why_weak": "It is not weak because an exclusion is shaky; it is weak because there is no exclusion. Both engines OOM (msolve pent_L23 exit 137 at 13.9 GB with a 0-byte output; Singular slimgb on L18 exit 137; monolithic measured >40 GB). The seeded extension run timed out at 5400 s / 9.5 GB with a 0-byte output. The bottom-edge Galois structure was claimed, then retracted at the fifth prime (admissible counts 1,1,0,2,3), so testing one seed may decide only its own orbit and the 'four invisible seeds' gap is open. And the witness at trackB1_pentagon.py:432 shows the truncations are non-empty, so no truncation can kill it.",
      "evidence_path": "wt/canon/STATUS.md §3; wt/canon/wave1/L23_VERDICT.txt; wt/p11/CATCHES.md:2037-2065; wt/p11/wave6/pentseed/seed0.log",
      "how_to_harden": "Stop feeding 186 variables to Groebner. FABLE-003's reduction — Q linear and redundant, pentagon as a 57-variable rank-drop on a 303x124 structured matrix with exactly one inhomogeneous equation — turns the object into linear algebra over a small parameter space, which fits in memory."
    },
    {
      "item": "Closures resting on un-re-derived external inputs and on can't-fail checks.",
      "why_weak": "The (108,72) closure is adjudicated SOUND-BUT-OVERSTATED: the THEOREM-2 removal holds on one leg only, and the residual-gap leg rests on an underived beta=6 plus two can't-fail checks at w3_10872_and_legs_audit.py:110 and :125. 45 hardcoded-True checks exist tree-wide, 19 of them inside inherited campaign certifiers. The deck-group result relies on Bayle-Beauville and Ramanujam/Morrow, neither re-derived. GGHV's [6, Prop 2.5] was never re-derived. [5]'s A'_t=(1,0) for the (10,40) chain is an unprinted assumption carried as a literature fact.",
      "evidence_path": "wt/canon/ADJUDICATION.md §1, §4.3, §7; wt/canon/CATCHES.md §32; wt/canon/STATE_FULL.md:43",
      "how_to_harden": "Every load-bearing external step gets an anchor-by-exact-quotation record or the label UNVERIFIED-HERE. Every certifier a lead depends on must be shown to FAIL on a planted negative before its PASS counts."
    },
    {
      "item": "GGV (1.2)-derived B=16 exclusions and the d>=7 ladder.",
      "why_weak": "The printed row 3 carried a spurious -2*mu3*q1''(0) term; both published worked examples have q1''(0)=0, so the control suite was structurally incapable of catching it, and everything built on the printed system is void as a statement about B=16. On the corrected system d<=7 is char-0 EMPTY, but d=7 is single-prime in the later record and STALLED-OOM in the earlier one; d=8 chart N was exported and never launched; d=9,10,11 chart N never run; d=12 chart N seed 1/20 required and never run (its export was already on disk, unrun); d=12 unsaturated is UNDECIDED after two kill attempts even though the d=3 analogue solves instantly; d=27 (resonant, both roots rational, 12*27 a square) is untouched. GGV's own conjecture that all solutions have mu_1 = mu_2 = 0 is unattempted — a refutation of it would BE a constructive counterexample.",
      "evidence_path": "wt/canon/CATCHES.md ('GGV (1.2) ROW 3 IS MIS-PRINTED'); wt/canon/STATE_FULL.md §A; wt/canon/OPEN_ITEMS.md §1-§4; wt/canon/ADJUDICATION.md §2, §6",
      "how_to_harden": "Rebuild every cell on the corrected system with a_{2d} unseeded, two primes minimum plus a char-0 attempt, and treat the d=12 unsaturated anomaly as the priority cell rather than an afterthought."
    },
    {
      "item": "The above-125 region: no exclusion theorem exists anywhere, published or campaign-side.",
      "why_weak": "GGHV's elimination stops strictly below 125; [5] enumerates to 150 and discards nothing above the frontier; the campaign's own above-125 EMPTYs are 20 shapes across 6 chains at a single prime (F_65521), and one of those chains has 115 surviving shapes so the chain is not closed. The 41 TIMEOUT shapes are aggregated in prose and enumerated in no file. Above-125 Newton polygons are published nowhere, and the chain compiler that would generate them is unwritten.",
      "evidence_path": "wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md; wt/canon/STATE_FULL.md §C; wt/pq/RESUME_STATE.md (queue table P3)",
      "how_to_harden": "Do not chase 429 uncompilable records. Attack the 24 cases the literature actually enumerates at max<=150 — a finite, checkable list — starting with (8,28)/(3,4) at max 144, which reuses the pentagon machinery unchanged."
    }
  ],
  "audit_gates_before_compute": [
    {
      "test": "G1 — Cor 5.7: kill or gap? One position, not two.",
      "how": "Read gghv.txt:1412-1433 and recompute the bracket [psi phi P, psi phi Q] by hand and in sympy; cross-read wt/mailbox/campaign/mod3_828/jc2_literature_sweep_partial.md:65-66,311 which records the corollary as verified against PDF lines 982-996. Write one page: the step, the computation, and the verdict.",
      "pass_criterion": "A single recorded position with the bracket reproduced symbolically, and every file in the tree asserting the other position amended or marked superseded. FAIL if two live records still disagree."
    },
    {
      "test": "G2 — Label integrity: every shape keyed by (corner, (m,n), orientation, max).",
      "how": "Rebuild the register from wt/canon/gghv_audit/all_cases_max_le_150.json. Assert that (9,27)/(2,3) and (8,28)/(3,2) are distinct rows, that (8,28)/(3,4) is recorded at max 144, and that L is not treated as a function of the degree pair ((72,108) gives L=3, (108,72) gives L=4).",
      "pass_criterion": "Zero rows with a missing (m,n) or missing orientation; the (8,28)/(3,4) row filed above 125. FAIL if any queued compute target cannot be resolved to exactly one row."
    },
    {
      "test": "G3 — Census reconciliation: one number per defined region, each with a generating script.",
      "how": "Recount frontier_151_300_map.json (expect 432 records: 429 NO-CHAIN, 1 0-blocked, 2 with L-values); re-run gghv_audit at M=100 (expect 474 at max<=300); recount the [125,300] coverage audit (464); locate any artifact for 804.",
      "pass_criterion": "Every circulating figure either has a script and a region definition, or is written into the record as NONEXISTENT. 804, 189 and 184 must end this gate labelled unsupported. FAIL if any number survives without provenance."
    },
    {
      "test": "G4 — Void ledger: which EMPTY rows are statements about B=16 and which are not?",
      "how": "Grep every B=16 verdict row for whether its export descends from the printed or the corrected (1.2). Tag each CORRECTED or VOID.",
      "pass_criterion": "Zero B=16 rows with unknown provenance; every void row visibly labelled in the file a future reader will open. FAIL if any headline count of 'cells closed' still includes void rows."
    },
    {
      "test": "G5 — The README asset: count it or retract it.",
      "how": "Fetch wave6/frontier/ from claude/opus-5-counterexample-plan-sep6yk and count trackB1_sat_Q.ms's header directly (vars, equations, terms, degree, characteristic). Search the campaign branch for any p=1000003 run producing a unit Groebner basis on it.",
      "pass_criterion": "Either the file exists with header counts matching a corrected README, or README.md:19-20 is amended to the real object (166/284/8774, total degree 5) with the unit-GB claim removed. FAIL if the claim stands uncorroborated."
    },
    {
      "test": "G6 — Queue sanity: excess and vacuity pre-flight on every queued system.",
      "how": "For each queued emptiness run compute eqs minus vars and the grading-torus rank; run wave2/w2_cantfail_audit.py over every certifier a queued lead depends on; re-run trackB1_pentagon.py:432 witness().",
      "pass_criterion": "Zero queued emptiness runs with excess <= 0; zero queued runs against positive-dimensional input in solve mode; zero literal-True check conditions in any dependent certifier; the truncation ladder removed. FAIL on any one."
    },
    {
      "test": "G7 — Engine provisioning plus the two poisoned-input controls.",
      "how": "apt-get install Singular 4.3.2 and build msolve 0.10.1 (a fresh container has neither). Then run the known traps: an export with a constant generator that is a nonzero multiple of the characteristic, and a planted-root system at the same unknown count as the target.",
      "pass_criterion": "The harness classifies the poisoned input as FAILURE (not EMPTY) with stderr captured, and recovers the planted root — or declares the numerical lane inadmissible for that size. FAIL if any '[-1]' is read without stderr."
    },
    {
      "test": "G8 — Prime hygiene and lucky-prime certification.",
      "how": "For every mod-p verdict in the register, record the prime list and assert p = 1 mod 3 and good reduction; compare the mod-p GB leading-term ideal against the majority over a batch and discard minority primes.",
      "pass_criterion": "Every EMPTY-mod-p row carries >= 2 hygiene-compliant primes and a recorded majority leading-term signature. FAIL for the case-(2) 32003/65537 rows unless the re-run at 65539/65599 is attached."
    },
    {
      "test": "G9 — Infrastructure floor: can a run actually finish?",
      "how": "Measure container uptime, cgroup cap and disk headroom; confirm the marker-resumable pipeline resumes correctly after a forced restart; confirm push-after-every-commit.",
      "pass_criterion": ">= 8 h uninterrupted process lifetime and >= 32 GB RAM available, or every scheduled run is marker-resumable at <= 20-minute granularity. FAIL means no monolithic run may be scheduled at all — which has been the true state for the entire campaign."
    }
  ],
  "leads": [
    {
      "id": "L1",
      "title": "Re-derive the sub-125 enumeration from [5]'s Algorithms, end to end, including the omitted chains and the A'_t assumption",
      "target": "The premise that (72,108)/(108,72) is the only surviving pair below max 125",
      "premise_with_citations": "GGHV Thm 2.1 imports its ten-case table from [5] (arXiv:1708.07936) Algorithms 1-9 rather than deriving degree pairs itself; the campaign's own independent re-implementation reproduces 34/34 published cases and 10/10 GGHV rows but ALSO finds two extra length-1 and four extra length-2 chains that [5]'s printed tables omit, and [5] §5's prose contradicts its own table (2 vs 7 length-2 chains). Separately [5] assumes A'_t=(1,0) for the (10,40) chain without printing the derivation (wt/canon/AUDIT_EOD.md §4 item 3; wt/canon/CATCHES.md:32; wt/canon/STATE_FULL.md:43). Vehicle already exists: wt/canon/gghv_audit/ggv_algorithms.py with four negative controls.",
      "method": "Run the re-implementation to max<=150 with all filters exposed. For every divergence from the printed table, trace the exact algorithm step and carry the extra chain forward to either a degree pair or a proof that it produces none. Enumerate the admissible A'_t for the (10,40) chain from the algorithm's own filters rather than importing (1,0). Verify the result against the published PDF by page image, not text extraction (the current extraction is flagged by its own author as unverified, and three claims from that class were retracted the same session).",
      "agent_roles": ["enumeration engineer (runs and instruments ggv_algorithms.py)", "paper reader (page-image verification of §6 and §5 family definitions)", "adversary (must try to produce a chain the enumerator misses)"],
      "inputs": ["wt/canon/gghv_audit/ggv_algorithms.py", "wt/canon/gghv_audit/all_cases_max_le_150.json", "wt/canon/papers/ (1708.07936, 2204.14178 PDFs)"],
      "outputs_with_labels": ["ENUMERATION-RE-DERIVED [PROVED-exact] or ENUMERATION-INCOMPLETE [PROVED-exact] with the missed rows", "A'_t (10,40): DISCHARGED or CENSUS-EXPANDED", "a table of divergences from [5]'s printed tables, each with its algorithm step"],
      "stop_rule": "Stop when every max<=150 row is reproduced or its divergence explained. If a new sub-125 pair appears, halt everything else and route it to the polygon builder immediately.",
      "cost": "2-4 agent-days, negligible CPU. No Groebner, no memory ceiling, no prime hygiene.",
      "p_hit": 0.03,
      "why_not_already_closed": "The campaign audited the survivor rather than the exclusions for 40 sessions; OPUS43-012 explicitly asked for exactly this audit and it was never reported back (wt/mailbox/AGENT_MAILBOX.md:1597-1680)."
    },
    {
      "id": "L2",
      "title": "Exact characteristic-zero closure of (72,108) case (2)",
      "target": "A publishable certified exclusion: case (2) EMPTY over Q-bar",
      "premise_with_citations": "The degree-1144 edge eliminant over Q exists, is squarefree, and is PROVED irreducible over Q by a Dedekind subset-sum sieve at 8 primes with a 9th (100153) independently confirming in adjudication, so all 1144 edge points are Galois-conjugate and the Q-bar question is one yes/no (wt/canon/STATUS.md §2.5; wt/canon/ADJUDICATION.md §1). What is missing is the 13-variable residual over K=Q[theta]/(f) — planned, never executed (MISS-4, wt/canon/STATE_FULL.md §B). The mod-p evidence at 65521/32003/65537 cannot be promoted, and the campaign proved its own eliminator closes branches with genuine rational solutions mod p.",
      "method": "Run trackB_exactQ.py (marker-resumable, QELIM_TIMEOUT, JCLEAF leaf selection) on a persistent machine. Prefer modular-GB + CRT + rational reconstruction through lift/lift_pipeline.py over a monolithic char-0 Groebner, and accept a PROVED-exact row only when the reconstructed basis verifies by exact substitution. Route every export through wave4/w4_msformat.py as a hard gate.",
      "agent_roles": ["solver operator (persistent machine, resumable staging)", "certifier author (negative controls, exact back-substitution)", "auditor (prime hygiene, leading-term majority)"],
      "inputs": ["wt/pq/trackB_exactQ.py", "wt/pq/trackB_Q_elim.sing", "wt/canon/wave1/edgeQ_eliminant.txt", "wt/canon/lift/lift_pipeline.py", "wt/canon/wave4/w4_msformat.py"],
      "outputs_with_labels": ["CASE-2 EMPTY over Q [PROVED-exact] with certifier triple, or NON-EMPTY -> HIT protocol H1-H6", "a reusable modular-GB + CRT + reconstruction wrapper labelled [CERTIFIED]"],
      "stop_rule": "Abandon after 40 uninterrupted machine-hours with no stage progress, or immediately if the residual proves reducible in a way that breaks the single-yes/no reduction.",
      "cost": "Days of wall time on a >= 32 GB persistent machine; low agent time.",
      "p_hit": 0.02,
      "why_not_already_closed": "It needs > 2.5 h of uninterrupted uptime and the container dies every ~30 minutes; the 6 h fallback timeouts configured in the script can never be reached (wt/pq/RESUME_STATE.md)."
    },
    {
      "id": "L3",
      "title": "Pentagon case (1) as linear algebra, not Groebner",
      "target": "The only branch on the board with no verdict of any kind",
      "premise_with_citations": "FABLE-003 reports Q is linear and redundant and the pentagon is a 57-variable rank-drop on a 303x124 structured matrix with exactly one inhomogeneous equation, against the 186-unknown/302-equation Groebner formulation everyone has been feeding to solvers (wt/mailbox/AGENT_MAILBOX.md:3562-3675; wt/canon/campaign/audit_tracks/trackA_report.md:65). Every pentagon failure so far is memory or targeting, never mathematics: L23 OOM at 13.9 GB, L18 slimgb exit 137, monolithic >40 GB, seeded run exit 124 at 5400 s. Structure is certified: rank 60 of 61 at two primes, 58 essential parameters against 60 conditions.",
      "method": "Build the 303x124 matrix explicitly and decide the rank-drop locus exactly over Q (minors, or a stratification by rank), never through a saturated Groebner. Independently: complete the exact coupled level ladder from level 16 downward with all kernel constants retained (W9 = g9 - (3c1/2c0)z^4 h5, W8 = g8 - (3c1/2c0)z^4 h4) and the bounded-support end check, both of which the earlier ladder dropped and thereby manufactured a false obstruction. Do NOT restart the truncation ladder.",
      "agent_roles": ["linear-algebra lead (rank stratification over Q)", "ladder continuer (levels 15 and below, exceptional strata a0=0 and F3=0)", "adversary (must reproduce the false level-16 wall to confirm the coupling is retained)"],
      "inputs": ["wt/mailbox/AGENT_MAILBOX.md:3562-3675 (FABLE-003)", "wt/l16/breakthrough/pentagon_level16.py", "wt/l16/breakthrough/PENTAGON_LEVEL15_BRANCH2.md", "wt/canon/wave1/pent_L23.ms (reference only)"],
      "outputs_with_labels": ["PENTAGON CASE (1) EMPTY over Q [PROVED-exact] via rank-drop, or a surviving stratum with its defining equations", "a corrected level ladder to level <= 8 [CERTIFIED] with the coupling and end-check controls"],
      "stop_rule": "Stop if the rank-drop locus is positive-dimensional and resists stratification after two independent formulations, or if the ladder produces a branch requiring the unbuilt rational-function cascade — that is a build task, not a solve.",
      "cost": "1-2 agent-weeks; modest CPU if the reformulation holds.",
      "p_hit": 0.03,
      "why_not_already_closed": "Nobody acted on FABLE-003; the mailbox thread ends with FABLE-006 unanswered and no reply from Sol, Codex or Opus 5 exists in the archive."
    },
    {
      "id": "L4",
      "title": "Certified B=16 ladder on the corrected system: d=8 chart N, d=12 unsaturated, d=12 chart N seed 1/20",
      "target": "A char-0 or two-prime closure of the frontier ladder cells, and the d=12 anomaly",
      "premise_with_citations": "GGV 2013 Thm 1.2 is an iff and discards nothing at B=16; it stalls at deg(q1)=5, and GGV 2017 calls B=16 'still within reach'. On the corrected system d<=7 is EMPTY in char 0 (d=7: 26 eq/20 unk, 1345 s, 6.67 GB, with a positive control). The frontier cell d=8 chart N is 30 eq / 23 unknowns, exported and NEVER LAUNCHED (MISS-2); d=12 chart N seed 1/20 is required and never run with its export already on disk (MISS-3); the d=12 unsaturated family is UNDECIDED after two kill attempts even though the d=3 analogue solves instantly — the campaign's own biggest anomaly. d=12 is resonant (12*12 = 144 a square, both roots rational).",
      "method": "Regenerate exports with a_{2d} unseeded so one run covers both roots; pick primes where 12d is a square; two primes minimum, then attempt char 0. Every run passes the msolve trap harness (stderr captured, no constant generators, all coefficients reduced mod p) and the excess pre-flight. Treat the d=12 unsaturated cell as the priority, not the leftover.",
      "agent_roles": ["export engineer (corrected system, sanitiser gate)", "solver operator", "control author (positive control per cell showing the pipeline can return non-empty)"],
      "inputs": ["wt/canon/OPEN_ITEMS.md §1-§3", "wave6/w6_seed_d8.py", "wave5/ms/m16_d8_*.ms", "wt/canon/wave4/w4_msformat.py"],
      "outputs_with_labels": ["d=8 cell EMPTY [EMPTY-mod-p(p1,p2)] or [PROVED-exact]", "d=12 unsaturated: DECIDED or MEASURED-RESISTANCE (explicitly not EMPTY)", "per-cell positive control logs"],
      "stop_rule": "Two failed formulations per cell at the measured resistance level ends that cell; record MEASURED RESISTANCE, never EMPTY. Do not launch d=9,10,11 before d=8 completes — cost scales ~32x per level (d=6: 42 s, d=7: 1345 s).",
      "cost": "Hours to days per cell on a >= 32 GB machine.",
      "p_hit": 0.01,
      "why_not_already_closed": "MISS-1/2/3: confirming primes died in container restarts, an export was never launched, and a required seed was never run despite its file sitting on disk."
    },
    {
      "id": "L5",
      "title": "Resolve Cor 5.7 and finish the two sliced p108 systems in Groebner-only mode",
      "target": "The (9,27) shape — either the literature's kill is repaired, or the shape reopens as live territory below 125",
      "premise_with_citations": "The proof of (5.12) applies [1, Cor 7.2] (standing hypothesis [P,Q] in K^x) to (psi phi P, psi phi Q) whose bracket is 1/2 + (lambda/2)x^{-1/2}, not in K^x, with lambda != 0 forced by (0,18) in N(P); 51 of 66 asserted conditions are unsupported (wt/canon/CATCHES.md; gghv.txt:1430-1433). The literature is silent — no erratum, no follow-up, no independent re-derivation. The campaign's two test systems are grading-torus rank 5 hence positive-dimensional, so their 1800 s solve-mode timeouts were structural; outstanding are 2 of 5 leaves on p108_525122 and 1 leaf (139 eq / 38 vars) on p108_192622.",
      "method": "Paper work first (this is audit gate G1 promoted to a lead): re-derive (5.12) or write the explicit counterexample to the step. Only then finish the sliced systems with msolve -g 2 (Groebner-only decides emptiness at any dimension; solve mode cannot terminate on positive-dimensional input), with the gauge admissibility proof recorded (weight-minor determinants -1/24 and -1/14) and the pre-registered verdict standard enforced: EMPTY at one prime is replication-grade only; non-empty needs the full prime tower plus a char-0 lift before the word 'refutation'.",
      "agent_roles": ["proof auditor (re-derives 5.12)", "solver operator (-g 2 only)", "label auditor (settles the (9,27) vs (8,28)/(3,2) naming dispute)"],
      "inputs": ["wt/canon/gghv.txt:1412-1433", "wt/mailbox/wave6/frontier/P108_RESULTS.md", "wave6/ms/p108_192622.ms", "wave6/ms/p108_525122.ms"],
      "outputs_with_labels": ["COR 5.7 REPAIRED [PROVED-exact] or COR 5.7 REFUTED [PROVED-exact] with the counterexample to the step", "p108 leaves EMPTY [EMPTY-mod-p] or NON-EMPTY -> HIT protocol", "one authoritative label mapping for the (72,108) shapes"],
      "stop_rule": "If the step repairs, close the shape and stop all p108 compute. If it does not, the shape is live and inherits L3's machinery rather than getting its own indefinite solver budget.",
      "cost": "3-5 agent-days for the derivation; hours to days of solver time after.",
      "p_hit": 0.01,
      "why_not_already_closed": "Two files in the same repository hold opposite positions on it and nobody adjudicated; OPUS43-012 said both systems were 'running now' and no verdict was ever reported."
    },
    {
      "id": "L6",
      "title": "The 24 published-enumerated open cases at max <= 150, starting with (8,28)/(3,4) at max 144",
      "target": "The only above-125 territory that is finite, enumerable today, and needs no unbuilt compiler",
      "premise_with_citations": "arXiv:1708.07936 §6 enumerates 34 possible counterexamples with max <= 150; only the 10 below 125 were ever discarded, leaving 24 untouched, of which (8,28) with (m,n)=(3,4), final [7,4,3], degree pair (108,144) shares the campaign's own corner and would reuse the existing machinery unchanged (wt/mailbox/AGENT_MAILBOX.md:3909-3985; wt/canon/gghv_audit/all_cases_max_le_150.json). This replaces the 429-case NO-CHAIN frontier, which is blocked on a compiler nobody has written and on Newton polygons published nowhere.",
      "method": "Verify the 24-case table against the published PDF by page image (the current list comes from a text extraction its own author flagged). Derive the GGHV Prop 4.3 analogue — reduced polygons plus bracket exponent — for (8,28)/(3,4). Run the existing x-column descent and determinantal rank test on it. Two primes minimum, no single-prime rows.",
      "agent_roles": ["paper reader (page-image table verification, §5 family definitions)", "polygon deriver (Prop 4.3 analogue)", "solver operator"],
      "inputs": ["wt/canon/papers/1708.07936.pdf", "wt/canon/gghv_audit/all_cases_max_le_150.json", "the fable_xcol/ tooling (NOT in this worktree — must be fetched from claude/fable-counterexample-sweep-yyj5vf)"],
      "outputs_with_labels": ["24-CASE TABLE VERIFIED [LIT-READ] against the published PDF", "(8,28)/(3,4) reduced polygon pair [PROVED-exact]", "its system EMPTY [EMPTY-mod-p(p1,p2)] or NON-EMPTY -> HIT protocol"],
      "stop_rule": "Stop the whole lead if the table verification fails — then the target list itself is fiction and L1 subsumes this. Stop per case at measured resistance, recorded as such.",
      "cost": "1 agent-week for the first case; the remaining 23 only after the first proves the pipeline transfers.",
      "p_hit": 0.02,
      "why_not_already_closed": "It is the head of the mailbox thread (FABLE-006) and has no reply; the referenced artifacts (FABLE_24_OPEN_CASES.md, fable_xcol/) are on a branch not present in any local worktree."
    }
  ],
  "campaign_stop_condition": "Stop the counterexample hunt and convert to write-up when EITHER (a) L1 confirms the sub-125 enumeration is complete AND (72,108) case (2) closes over Q (L2) AND pentagon case (1) closes or is reduced to a strictly positive-dimensional stratum that is provably not a counterexample locus (L3) — at which point the sub-125 region is genuinely closed and the honest statement is 'the plane Jacobian conjecture holds below max degree 125, with the (72,108) closure now unconditional'; OR (b) two consecutive audit-gate cycles (G1-G9) produce zero new verdicts and zero corrections, meaning the campaign is only re-deriving its own retractions; OR (c) the audit gates cannot be passed at all — no persistent machine, engines unavailable, register still self-contradictory — in which case there is no basis on which any further compute could produce a defensible verdict and the correct move is to publish the correction ledger and stop. Note (c) has arguably been true for most of the campaign's life.",
  "definition_of_done": "Done is NOT a counterexample. Done is a repository in which: (1) every verdict row carries characteristic, prime list, orientation, (m,n), corner, and a certifier triple (engine input, captured output, a Python certifier that is shown to FAIL on a planted negative); (2) no EMPTY row anywhere is mod-p only without being labelled so, and no timeout or OOM appears as a verdict; (3) the census has exactly one number per defined region, each with a generating script, and 804/189/184 are recorded as unsupported; (4) every load-bearing literature step — Cor 5.7, [6, Prop 2.5], A'_t=(1,0), the [5] Algorithms enumeration, the [4] §3.5 claim for (80,112) — is either re-derived locally or explicitly labelled UNVERIFIED-HERE; (5) at least one new char-0 exclusion theorem exists that did not exist before (the strongest candidate is (72,108) case (2) over Q-bar); and (6) the README describes objects that exist. That repository is publishable as a negative result and as a correction to two preprints, which is the realistic maximum value of this work.",
  "risks": [
    "The campaign's dominant failure mode is confirmation-shaped verification (M1), and an audit-first plan is itself vulnerable to it: an auditor who wants the register to be clean will declare it clean. Every gate must have a recorded input on which it is REQUIRED to fail.",
    "L1 is the highest-value lead and also the one most likely to be declared 'reproduced 34/34' without anyone opening the published PDF. Text extraction has already produced three retractions in a single session; page-image verification is not optional.",
    "Infrastructure may make L2, L3 and L4 simply impossible: ~13.3 GiB cgroup cap, ~30-minute restarts, a measured ~2.5 h process ceiling, a git tree that rolled back twice, 37+ unpushed commits lost to credential death, and fresh containers with neither Singular nor msolve installed. If the gate G9 fails, four of six leads are unrunnable and saying so is the honest output.",
    "Key artifacts live on branches absent from every local worktree (wave6/frontier/, fable_xcol/, FABLE_24_OPEN_CASES.md, session43/LEADS.md). Plans built on them are plans built on prose.",
    "A HIT, if one occurs, will most likely be a gauge artefact — it happened twice already, both caught pre-commit only because someone looked. The HIT protocol H1-H6 (exactness, Keller, non-injectivity, an independent resultant route, gauge invariance under random affine changes on BOTH source and target, and non-vacuity) must run in full, with H6 shown to have fired, before the word counterexample is written anywhere.",
    "Prior probability. JC2 has survived since 1939, Moh cleared max <= 100 by hand, and the dimension-3 counterexample explicitly does not transfer. My honest p(this campaign produces a genuine JC2 counterexample) is well under 1%. Every lead above is priced accordingly, and any plan whose value depends on a HIT is a plan with negative expected value."
  ],
  "what_would_change_my_mind": "Four things, in descending order of force. (1) L1 finding a degree pair below max 125 that [5]'s printed tables omit and that carries through to a real polygon pair — that would mean the campaign has been searching the wrong room, would multiply the value of every solver hour, and would be a publishable correction on its own. (2) L3's rank-drop reformulation producing a low-dimensional surviving stratum with explicit defining equations rather than a rank-deficiency that resists stratification — a pentagon that is 57 structured variables instead of 186 unknowns is a tractable object and would justify a real compute budget. (3) A repair of GGHV Cor 5.7 that FAILS — i.e. a genuine counterexample to the step, not just an unsupported inference — which reopens a shape below 125 with no literature exclusion at all. (4) Any NON-EMPTY that survives the full HIT protocol including H5 gauge invariance on both source and target. Conversely, what would harden my scepticism further: L2 closing case (2) over Q cleanly, plus L1 confirming the enumeration is complete. At that point the sub-125 region is genuinely closed, the only remaining territory is above 125 where no exclusion theorem exists and no polygons are published, and the correct action is to write up the exclusion theorems and the correction ledger and stop — not to start a 429-case sweep behind a compiler nobody has written."
}
```