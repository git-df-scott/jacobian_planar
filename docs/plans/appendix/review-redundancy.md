```json
{
  "merged_leads": [
    {
      "name": "PLANT — provisioned pinned CAS image, persistent 128 GB host, restart-resilient one-verdict-per-commit runner",
      "proposed_by": ["engineering ENV-1", "skeptic G7 + G9", "structural A5", "enumerated-corners audit_gates_before_compute (ENGINES)"],
      "score": 9,
      "justification": "Every solver-shaped lead in all four plans is unrunnable without it: fresh container has neither Singular nor msolve, 13.3 GiB cap, ~2.5 h process ceiling, and every heavy termination on record is memory or restart. Two agent-days buys the entire compute half of the campaign. Zero p_hit by itself, which is why it must be done by engineers in parallel and never allowed to consume the mathematicians.",
      "prerequisite": "None. This is the root of the dependency graph. If the 128 GB host cannot be obtained in 3 days (engineering ENV-1 stop_rule), every heavy lead re-scopes to <12 GB staged probes and must be re-priced downward on the spot."
    },
    {
      "name": "LEDGER — content-hash verdict schema, gate.py as blocking CI, census reconciliation (34/24 vs 429/432/464/474/804)",
      "proposed_by": ["engineering LEDGER-1 + SCHED-1 refusal list", "skeptic G2/G3/G4/G5 + waste items 4,6,7", "enumerated-corners audit gates (CONTENT-HASH DEDUP, CAN'T-FAIL SCAN, LITERATURE ANCHORING)", "structural A6/A8/A9 + risk 'count drift is endemic'"],
      "score": 9,
      "justification": "The single most consistently supported item across all four plans, and the cheapest. Without it a fleet of 6-8 agents multiplies the archive's documented failure mode — 49 TIMEOUTs that were 16 systems, an EMPTY double-counted from two md5-identical files, 45 hardcoded-True checks, five incompatible cardinalities for one region. All four plans independently reached 'policy without an enforcer' as the diagnosis. Note the honest cost: re-keying will make the verdict count go DOWN.",
      "prerequisite": "None; runs day 1 alongside PLANT. gate.py must be wired into the exporter before any export is written, not after."
    },
    {
      "name": "TABLE-VERIFY — page-image verification of arXiv:1708.07936 §6 against gghv_audit/all_cases_max_le_150.json",
      "proposed_by": ["enumerated-corners L1 step 1 + what_would_change_my_mind #5", "skeptic L6 method + risk 2", "structural A2 (hard gate on L6)", "engineering TAIL-1 step 6"],
      "score": 9,
      "justification": "One agent-day. It is the load-bearing input for the 24-case closure (three plans' main above-125 lead), it has never been done, the current list comes from a text extraction its own author flagged after retracting three claims in the same session, and poppler/pypdf are absent so it needs a page render. A mismatch invalidates the largest block of new territory in the whole campaign. Highest verified-value-per-hour item on the board.",
      "prerequisite": "poppler-utils in provision.sh (engineering TAIL-1 step 6 names this as exactly why the check failed before)."
    },
    {
      "name": "ENUM-AUDIT — re-derive the sub-125 enumeration from [5] Algorithms 1-9 inside ggv_algorithms.py; discharge A'_t=(1,0)",
      "proposed_by": ["skeptic L1 (its #1 lead)", "enumerated-corners L7", "engineering TAIL-1 step 5", "structural A2 partially"],
      "score": 8,
      "justification": "The only lead that can make the search space LARGER rather than smaller, and it is pure combinatorics — no Groebner, no memory ceiling. The re-implementation already reproduces 34/34 and 10/10 with four negative controls but ALSO finds two extra length-1 and four extra length-2 chains the printed tables omit, and [5] §5's prose contradicts its own table (2 vs 7). If the ten-case table has a hole, '(72,108) is the only survivor' — the premise of forty sessions — is false. Enumerated-corners prices A'_t at 10-15% not-forced; that is the highest non-trivial probability anywhere in the four plans.",
      "prerequisite": "TABLE-VERIFY, so divergences are traced against the published paper rather than against the extraction that generated them."
    },
    {
      "name": "COR-5.7 — adjudicate GGHV Cor 5.7 to ONE position, then finish p108_192622 / p108_525122 leaves with msolve -g 2",
      "proposed_by": ["enumerated-corners L3", "skeptic L5 (= gate G1 promoted to a lead)", "structural A4", "engineering HEAVY-1(c)"],
      "score": 8,
      "justification": "All four plans name it; two files in the same repo hold opposite positions and nobody adjudicated. The compute half is genuinely likely to finish — the systems are 28-40 vars, the 1800 s timeouts were STRUCTURAL (torus rank 5, positive-dimensional, msolve solve-mode cannot terminate), and the fix is a flag. Enumerated-corners' ~2-3% NON-EMPTY is the highest per-run figure in that plan. A NON-EMPTY means the published floor of 108 is not established, which is a major result with no counterexample attached.",
      "prerequisite": "Measure grading-torus rank and re-derive the rank-5 slice independently (second agent, different code path) BEFORE reusing the gauge; -g 2 mandatory. Do not requeue at a longer budget without this."
    },
    {
      "name": "CERT — certified char-0 promoter: multi-prime GB + lucky-prime majority + CRT + rational reconstruction + exact ideal-membership / Nullstellensatz certificate",
      "proposed_by": ["engineering CERT-1", "enumerated-corners L5", "skeptic L2 method", "structural L3 step 2 (lucky-prime half)"],
      "score": 8,
      "justification": "The only lead that changes the epistemic status of everything else: 46 EMPTY verdicts are permanently short of char 0 by the campaign's own (correct) rule, and the campaign proved modular elimination unsound for contradictions with a three-line witness. ~300 lines, no new mathematics, precedent on this data (the degree-5 w=-4 eliminant CRT'd from 41 of 96 primes, verified at 6 held-out primes). For EMPTY specifically the Nullstellensatz certificate is a linear solve, not a Buchberger run, and is checkable by a referee with one multiplication. p_hit ~0; that is the point.",
      "prerequisite": "Two-sided self-test firing on BOTH sides (planted-consistent must NOT certify 1; planted-inconsistent must) before it touches real data. Ship it failing rather than delete it."
    },
    {
      "name": "CASE2-Q — characteristic-zero closure of (72,108) case (2), including the 13-variable residual over K=Q[theta]/(f), deg f=1144",
      "proposed_by": ["skeptic L2 (its highest-value deliverable)", "enumerated-corners L5 target", "engineering CERT-1 first target"],
      "score": 7,
      "justification": "The one hard exclusion genuinely within reach: the degree-1144 eliminant is squarefree and PROVED irreducible over Q at 8 primes plus an independent 9th, so all 1144 edge points are Galois-conjugate and the Q-bar question is a single yes/no. MISS-4: planned, partially run four times, never finished, blocked purely on uptime against its own 10800 s timeouts. Its current EMPTY rests on 65521/32003/65537 — two of which violate the campaign's own p≡1 mod 3 rule. Expected outcome is EMPTY over Q, which is a publishable theorem, not a counterexample.",
      "prerequisite": "PLANT (>8 h uninterrupted) + CERT tool self-tested. The gcd shortcut for the residual is RETRACTED — do not re-derive it."
    },
    {
      "name": "D8N — B=16 corrected d=8 chart N: launch the export that has never been launched",
      "proposed_by": ["enumerated-corners L6", "skeptic L4", "engineering HEAVY-1(b)", "structural L2 step 1(a) as a carrier"],
      "score": 7,
      "justification": "30 eq / 23 unknowns — the smallest genuinely-new object anywhere on the board, exported and never run (MISS-2). Uniquely, GGV Thm 1.2 is an IFF, so a solution with mu_0 != 0 IS a counterexample rather than a candidate to lift; every other lead's non-empty is a necessary-condition result. Cheap enough that its low p_hit (0.5%) still clears the bar. Skeptic prices it lowest (0.01) and is not wrong; it is the cost, not the odds, that earns the slot.",
      "prerequisite": "Regenerate from wave6/w6_seed_d8.py and diff against wave5/ms/m16_d8_*.ms — OPEN_ITEMS and WEEKEND_PLAN disagree on the path — then w4_msformat sanitize. Everything descending from the PRINTED (1.2) is VOID and must not be reused."
    },
    {
      "name": "PRIME-AUDIT — adversarial/lucky-prime re-audit of every single-prime or hygiene-violating EMPTY",
      "proposed_by": ["structural L3 (cheapest lead on its board)", "engineering CERT-1 step 1 + gate 'lucky-prime-majority'", "enumerated-corners L2 step 7", "skeptic G8"],
      "score": 7,
      "justification": "~96 s per prime, embarrassingly parallel, restart-resilient by construction (reuse wave6/bottomedge/sweep.sh). Targets a real, proven failure mode (z=7y dies mod 7) that the archive used only defensively, never as a search tool. Structural prices it ~60% to retract at least one currently-quoted EMPTY to NO VERDICT — reopening territory at negligible cost — and a cross-prime disagreement is the single most informative cheap event available. Covers the 20 above-125 F_65521 shapes, ladder d=7, chart Z d=9/10/11, F3 x2, case (2)'s non-compliant pair.",
      "prerequisite": "Content-hash dedup FIRST (p108_821326 == p108_843700), and the selector must reject control primes 5/11/17 or it is itself a can't-fail certifier."
    },
    {
      "name": "PENT-RANK — pentagon case (1) as a 57-variable rank-drop on a 303x124 structured matrix, not a 186-variable Groebner",
      "proposed_by": ["skeptic L3", "enumerated-corners L4(b)", "structural L2 step 1(b) as a carrier", "engineering CASC-1 step 5 (coupling guards)"],
      "score": 6,
      "justification": "Pentagon case (1) is the only branch with NO VERDICT of any kind by any method anywhere, and FABLE-003's reduction (Q linear and redundant, exactly one inhomogeneous equation) turns it from a memory problem into linear algebra. Nobody acted on it; the mailbox thread ends unanswered. Discounted from higher because three prior reformulation cascades all died at exactly this step and attempt #3 would have falsely killed the campaign's best lead.",
      "prerequisite": "Independent re-derivation by a second agent, with the reduction REQUIRED to reproduce both a known EMPTY and a known NON-EMPTY control before it is pointed at the pentagon. Fail either control and the lane stops."
    },
    {
      "name": "SUBCASE2 — build GGHV Prop 4.3's never-built second sub-case (70 unknowns / 92 eqs, 21 after gauge)",
      "proposed_by": ["enumerated-corners L4(a)"],
      "score": 6,
      "justification": "Best cost/novelty ratio in the entire (72,108) territory: a system GGHV printed, nobody built, and small enough that msolve -g 2 decides it in hours. Named three times in the mailbox (FABLE-004/005/006) and never built; the referenced fable_xcol/subcase2.py is on a branch in no local worktree. Only one plan raised it, which is a gap in the other three rather than a mark against it. FABLE-004 says D=1 compatibility might kill it in one line — check that first, it is nearly free.",
      "prerequisite": "Librarian verifies Prop 4.3 really has two sub-cases against 2204.14178.pdf directly, and tests D=1 compatibility, before any system is built."
    },
    {
      "name": "CASE24 — sweep the 24 published-but-untouched cases at max in [125,150], led by (8,28)/(3,4) at (108,144)",
      "proposed_by": ["enumerated-corners L1 + L2 (its whole thesis)", "skeptic L6", "structural L6 target list", "engineering TAIL-1 step 6 partially"],
      "score": 6,
      "justification": "The largest genuinely-unsearched block that needs no unbuilt tool: GGHV eliminate max<125 only, [5] enumerates to 150 and discards nothing above the frontier, and the chain to reduced-polygon map is RESOLVED below 150 with 6/6 published pairs reproduced. Honest modal outcome is 24 more EMPTYs and a paper raising the published floor from 108 toward 150. Scored 6 not 8 because the compiler is a single point of failure — a wrong reduction makes every downstream EMPTY a statement about the wrong variety, which is the GGV-(1.2) failure replayed at scale.",
      "prerequisite": "TABLE-VERIFY passes, AND record 22 alone is driven to a verdict first as a pipeline test with the eps_P+eps_Q=(r+1,1) invariant and the 6/6 regression both firing. Do not batch 24 until one case has closed end to end."
    },
    {
      "name": "SYMBOLIC-D — attack the GGV conjecture (mu_1=mu_2=0 for all d) symbolically in d instead of climbing the ladder",
      "proposed_by": ["structural L4", "enumerated-corners L6 step 9", "skeptic weakest_exclusions (notes it unattempted)"],
      "score": 6,
      "justification": "The ladder is dead by arithmetic — 32x per level, measured (d=6: 42 s, d=7: 1345 s) — so d>=8 char-0, d=12 and d=27 are unreachable by the direct route on any hardware. The symbolic ingredients exist and are exact: torus rank 1 with explicit weights, (F2) and (F3) provably d-independent, resonance law d=3k^2. A proof closes B=16 outright; a refutation at some d is a CONSTRUCTIVE counterexample. Skilled-agent-time-bound, not compute-bound, so it costs the fleet almost nothing in CPU.",
      "prerequisite": "The derivation must reproduce d=3,4,5,6,7 EMPTY as a mandatory can-fail control; a symbolic-d result that does not is WRONG and gets discarded, not patched. Re-derive from the Poisson bracket, never from the printed (1.2)."
    },
    {
      "name": "TAIL-TEST — enumerate the 41 timeout shapes mechanically and run the 20-sample tail-closure saturation test",
      "proposed_by": ["engineering TAIL-1", "enumerated-corners L7 step 3", "skeptic waste item 4", "structural L6 step 2 (count reconciliation)"],
      "score": 6,
      "justification": "Twenty compilations, not a sweep, and it is the ONLY thing licensed to authorize or refuse the multi-week chain-compiler extension for the 429 NO-CHAIN region. Assigned to Codex in OPUS43-012 and never reported back. The 41 timeout shapes exist as an aggregate in three files and are enumerated in none; expect the count to shrink materially (49 TIMEOUTs previously collapsed to 16 unique systems), which is itself a finding.",
      "prerequisite": "LEDGER content-hashing, so the 41 are deduped before anything is swept. Predictor baseline is 34 chains -> 26 distinct tails with zero violations."
    },
    {
      "name": "SWEEP-SCOPE — audit the sweep-dichotomy's exact hypothesis set, then the general division-twist side-condition system above Moh",
      "proposed_by": ["structural L1"],
      "score": 5,
      "justification": "The step-1 audit is two hours and decides the rest: the archive's headline 'the sweep mechanism is dead in the plane' is proved for S affine-linear in gamma and for ONE twist shape (w=gamma*u, C=gamma*x^s), while the same file calls the general system 'the object nobody has written down'. The only search ever launched was killed as vacuous by Moh and no verdict was recorded. Structural prices ~35% that the audit alone narrows a headline closure to a scoped one — a real deliverable at trivial cost. The full general system is speculative and is priced accordingly.",
      "prerequisite": "Gate A1 (read w6_plane_sweep.py and w6_plane_sweep_search.py in full, publish the hypothesis set verbatim). If the dichotomy is general in (C,i,j) and gamma-degree, close the lead and reallocate — that is a valid outcome."
    },
    {
      "name": "CASCADE-4 — rebuild the rational-function cascade as saturation/regular-chain branching, paper design first",
      "proposed_by": ["engineering CASC-1", "enumerated-corners L6 step 7 + L4 step 3 (as a caution)", "structural L5 (hbar variant of the same need)"],
      "score": 4,
      "justification": "It is the shared blocker for d>=8 char-0, d=12, d=27 and pentagon propagation past level 3, and the three prior failure modes are diagnosed precisely (symbolic pivot division, non-propagating substitution), which makes a fourth attempt tractable rather than reckless. But three attempts, three self-test failures, same root cause: the base rate says it fails. It earns a build slot only because the paper design was never done. Hard stop is non-negotiable — commit as FAILING, do not run it on real data 'to see'.",
      "prerequisite": "Written paper specification with a proof that the branches COVER the original variety, before any code. Then two-sided self-test including the (a=3,b=4,c=2) regression that attempt #3 killed."
    },
    {
      "name": "COLLISION — augment a pinned system with the two colliding source points as unknowns",
      "proposed_by": ["structural L2"],
      "score": 4,
      "justification": "Genuinely novel — nothing in the archive ever made non-injectivity a variable — and the only formulation where a positive passes HIT gate H3 by construction. But structural's own 4% is not comparable to other leads' numbers, and it admits the negative is nearly worthless: an augmented EMPTY says only 'no collision of this assumed shape' and is strictly WEAKER than the unaugmented verdict. Real risk of a fleet burning weeks producing augmented EMPTYs and filing them as cell verdicts. One agent-week experiment on d=8, no more.",
      "prerequisite": "Two-sided self-test on a known non-injective etale-off-a-curve map (must find the collision) and a known triangular automorphism (must be EMPTY). Use two Rabinowitsch charts, not the sum-of-squares form, which silently admits the isotropic-line degeneracy over F_p."
    },
    {
      "name": "CHI-LEDGER — Riemann-Hurwitz without properness as a solver-free char-0 filter on the 24 open cases",
      "proposed_by": ["structural L6"],
      "score": 4,
      "justification": "FABLE-002's chi(F_c) = D - 2 deg(a_0) kill test was explicitly asked for and never run; FABLE-005 then retracted the unqualified bound because the dimension-3 mechanism converts ramification into non-properness — and non-properness is precisely the crux of JC2. If the properness-free identity lands it is a cheap char-0 filter on the largest unsearched region and a targeting device for CASE24. If it does not, days are lost, not weeks. Finds no counterexamples directly; structural says so.",
      "prerequisite": "TABLE-VERIFY (structural makes A2 a hard block on any solver time here), plus a recorded domain probe on which the identity is REQUIRED to fail — quantifier-scope drift has already voided two headline results."
    },
    {
      "name": "SCHED — expected-information-per-core-hour scheduler with a pre-flight refusal list",
      "proposed_by": ["engineering SCHED-1", "enumerated-corners audit gates (MOH/EXCESS/TORUS-RANK)", "skeptic G6", "structural A7/A8/A9"],
      "score": 4,
      "justification": "The refusal list is the valuable half and it is 20 lines: refuse if max realizable degree <=100 (Moh), gcd not in {16} u (20,inf), excess <=0, solve-mode on torus rank >0, hash already terminal, criterion on the known-vacuous list. That alone would have prevented the 1728-shape sweep, the two-week W=19 run and the requeued p108 timeouts. The scoring machinery is over-engineering for a 6-8 agent fleet and its stated acceptance test is broken (see conflicts). Build the refusal list; skip the nightly re-ranking.",
      "prerequisite": "LEDGER content hashing and the torus-rank prober, both of which the refusals query."
    },
    {
      "name": "ELIMINANT-9 — factor the degree-9 bottom-edge eliminant over Q directly",
      "proposed_by": ["enumerated-corners L4 step 6"],
      "score": 3,
      "justification": "One CPU-hour, replaces a RETRACTED Chebotarev orbit story (a four-prime average falsified by the fifth: admissible counts 1,1,0,2,3) with a [PROVED-exact] statement. The char-0 bottom edge already solves in 316 s. Tiny scope, tiny value, but it closes a live retraction rather than leaving it open, and it is cheap enough to hand to whoever is idle.",
      "prerequisite": "None beyond PLANT."
    }
  ],
  "dropped": [
    {
      "name": "Pentagon truncation ladder W=12..19",
      "reason": "REFUTED INSIDE THE REPO. trackB1_pentagon.py:432 witness() certifies an exact rational point satisfying all equations and side conditions for W=12..19, so every truncation in that range is provably NON-EMPTY and can never yield an EMPTY. W=19 is additionally underdetermined by 6. skeptic waste item 1 and structural A8 both name it; enumerated-corners L4 lists it as dead. Two weeks were already spent on it. Delete it from every queue and register, and note that the open-queue reader still ranks it #1 — that ranking is the bug."
    },
    {
      "name": "Rank/bifurcation criterion, including the proposed extension to d=48 and d=75",
      "reason": "Can't-fail certifier. The system contains 6*mu0 - 2*a2*mu2 = 0 with a2 = mu2 = 0 at the quasi-homogeneous point, forcing dmu0 = 0 at every d, so 'ALWAYS OBSTRUCTED at d=3..27' is bookkeeping, not evidence. skeptic waste item 3, enumerated-corners L6 step 8, structural A6 all agree. OPEN_ITEMS §4 governs over WEEKEND_PLAN §P2."
    },
    {
      "name": "Plane-sweep shape sweeps below the Moh floor (the 1728-shape search as configured)",
      "reason": "Vacuous by construction: maps of max total degree ~32 against Moh's proven floor of 100. A negative carries exactly zero information. Killed mid-run once already. The ansatz-degree gate exists to make this structurally impossible; the general twist system above Moh (SWEEP-SCOPE) is the live version."
    },
    {
      "name": "Everything descending from GGV's PRINTED (1.2)",
      "reason": "VOID as a statement about B=16 — the spurious -2*mu3*q1''(0) term in row 3 means those runs describe V_true intersect ({mu3=0} u {q1''(0)=0}), a proper subvariety. Both published worked examples have q1''(0)=0, so the control suite was structurally incapable of catching it. Only corrected m16_* artefacts count. Re-label in one pass (skeptic G4) rather than re-litigating case by case."
    },
    {
      "name": "Z/N chart splitting and prime-size tuning on the B=16 ladder",
      "reason": "Known-unnecessary and superseded. Seeding the row-0 root covers the whole cell because the relation is mu-free, so a_{2d} unseeded gives one run per cell; F2 (mu0 = a2*mu2/3) proves chart Z contains no counterexample; and prime size buys nothing because the bottleneck is Groebner structure, not coefficient arithmetic. OPEN_ITEMS §2 supersedes WEEKEND_PLAN §P1, which still describes the old way."
    },
    {
      "name": "Monolithic 186-variable / 166-variable pentagon Groebner as a scheduled critical-path job",
      "reason": "DEFERRED to a zero-priority background slot, not a lane. Four attempts, four NO VERDICT; msolve is structurally excluded above ~180 variables by a hard 2^25 hash-table ceiling, leaving Singular as a single engine, which weakens any verdict it produces. Its NO VERDICT carries no information about emptiness and has never carried any. Run PENT-RANK instead; if the heavy host is otherwise idle, let one 18 h run go in the background and treat a second no-progress run as a shape problem (engineering's own HEAVY-1 stop_rule)."
    },
    {
      "name": "Chain-compiler extension to the 429 NO-CHAIN records at max 156-300",
      "reason": "DEFERRED behind TAIL-TEST. Above-125 Newton polygons are published nowhere, GGHV gives polygons for only four chains hand-derived with no general recipe, and naive pattern-fitting provably fails — (9,27) has A0 = n*(3,9) exactly while (8,28) is not n*(lattice point), and fitting a rule to those two produced three retracted results. Multi-week against unpublished data. Only the saturation test (>=15 of 20 samples reusing an existing tail) may authorize starting it."
    },
    {
      "name": "B=16 ladder cells d=9, 10, 11 before d=8 completes",
      "reason": "Cost scales ~32x per level, measured. Launching d=9 before d=8 has a verdict is spending 32 units to learn what 1 unit would have told you. engineering HEAVY-1 stop_rule and skeptic L4 both say this explicitly."
    },
    {
      "name": "d=27 by direct Groebner",
      "reason": "114 eq / 85 unknowns, out of reach by the direct route on any hardware given the measured scaling. Reachable only behind CASCADE-4 or SYMBOLIC-D, both of which are themselves gated. Do not schedule it as a solver job."
    },
    {
      "name": "Weyl-algebra / Dixmier hbar cascade (structural L5)",
      "reason": "DEFERRED past week one. Genuinely interesting — the hbar filtration is linear per rung with an explicit obstruction, unlike the y-adic filtration where three cascades died — but it needs the JC_2n <=> DC_n dictionary re-derived, has no artefact of any kind in the archive, and lands in exactly the register (symbolic ladders) where this campaign has failed repeatedly. Revisit only if CASCADE-4 fails its self-test and the pentagon still has no verdict."
    },
    {
      "name": "Re-running any content-hash that already carries a terminal verdict",
      "reason": "Already closed and double-counted once: p108_821326 and p108_843700 are md5-identical and their EMPTY was counted twice; a paused sweep re-ran its own four-minute-old TIMEOUT under a new tag. A TIMEOUT/OOM record is NOT terminal and may be rescheduled — but only after the torus rank is re-measured."
    },
    {
      "name": "Citing multi-start Newton misses as evidence of anything",
      "reason": "Negative result carries no information: planted roots at residual exactly 0 were not found at 25 or 165 unknowns. Numerical lanes are finders only. A hit goes to the HIT protocol; a miss may not be cited at all."
    },
    {
      "name": "The figures 804, 189 and 184",
      "reason": "NONEXISTENT. 804 is explicitly disavowed by FABLE-006 as coming from lost Sessions 19-38 with no supporting artifact; two independent readers grepped the tree and found nothing matching 189 non-closing records or 184 new tail hashes (189 appears only as a row index and a memory figure, 184 only as the count of active pentagon unknowns). Write them into the record as unsupported so they stop propagating."
    },
    {
      "name": "README.md:19-20's flagship asset (164 vars / 288 quadratic eqs / 6,821 terms with an independently reproduced unit Groebner basis)",
      "reason": "No such file exists in main, docs/, the state transfer tarball, or any of the seven worktrees. The nearest real object is trackB1_sat_Q.ms at 166/284/8774 — different numbers — and the claimed unit GB is corroborated by a 5400 s timeout with a 0-byte output. Either fetch and count the header or amend the README. Do not plan around it."
    }
  ],
  "conflicts": [
    {
      "topic": "Pentagon: 186-variable Groebner on 128 GB, or FABLE-003's 57-variable rank-drop?",
      "positions": "engineering HEAVY-1 step 3 says run the all-vertex-saturated deg-2 form (186 vars) in Singular on the persistent host for 18 h, because the deg-2 forms merely TIME OUT at 1.5-2.3 GB while the eliminated deg-22 form OOMs — i.e. they are time-bound and time is what the host buys. skeptic L3 and enumerated-corners L4 both say STOP FEEDING 186 VARIABLES TO GROEBNER and reformulate as a rank condition on a 303x124 structured matrix. structural L2 step 1(b) agrees: pentagon augmentation is worth attempting only on the reduced form.",
      "adjudication": "Three plans to one; the reformulation is the critical path. Assign two agents to PENT-RANK with mandatory two-sided controls. Engineering's argument is not wrong, though — the deg-2 form has never had 18 uninterrupted hours and 100 GB, and agent cost is zero once the plant exists. So: run it ONCE, in the background heavy slot, at lowest priority, with engineering's own stop_rule enforced (no degree progress across two successive 18 h runs = shape problem, kill the lane). It is not a deliverable and no schedule may depend on it. If PENT-RANK's controls fail, the whole pentagon lane stops rather than falling back to the monolith."
    },
    {
      "topic": "Is the truncation ladder the #1 lead or a refuted zombie?",
      "positions": "The live open queue (quoted in engineering SCHED-1) ranks pentagon W=19 first on HIT-chance per compute-hour, reasoning 'every failure so far was memory, not mathematics'. skeptic waste item 1 says that reasoning is wrong: the failure is targeting, witness() has certified W=12..19 NON-EMPTY over Q inside the repo the whole time, and CATCHES.md already withdrew the plan as 'P0 IS FUTILE'.",
      "adjudication": "skeptic wins outright and it is not close — an in-repo exact rational witness beats a heuristic ranking. Two consequences the fleet must absorb. (1) Delete the ladder from every queue. (2) engineering SCHED-1's stated stop_rule — 'stop building when the scheduler reproduces the open-queue reader's hand ranking (pentagon 1, d=8 2, ...)' — is now a broken acceptance test that would hard-code a refuted lead into the scheduler. Replace it: the scheduler is correct when it REFUSES the truncation ladder on the excess<=0 gate and independently surfaces D8N, COR-5.7 and the p108 leaves. Note the general pattern for the fleet: 'every failure was memory, never mathematics' appears in engineering's thesis too, and it is true for the pentagon deg-2 forms and false for the truncation ladder and for the p108 solve-mode timeouts. Do not apply it as a slogan."
    },
    {
      "topic": "Are the 24 above-125 cases compilable today, or blocked on unpublished polygon data?",
      "positions": "enumerated-corners L2 says compilable TODAY: the chain data is printed, TRACKD_CHAIN_MAP.md derives the reduction from GGHV Sec 4 + [C] Thm 2.20 and reproduces 6/6 published reduced pairs, and ABOVE_125_STATUS.md says 'Status: RESOLVED'. engineering TAIL-1 says above-125 Newton polygons are published NOWHERE and naive pattern-fitting provably fails, producing three retracted results.",
      "adjudication": "Both are right about different regions and the confusion is doing damage. The chain -> reduced polygon map is RESOLVED for max<=150, which covers all 34 published cases; the 'published nowhere' problem is the 156-300 census where the chain library stops. So CASE24 is unblocked and the 429-case frontier is not. Enforce the boundary: no CASE24 work touches anything above 150, and TAIL-TEST is the only thing allowed to probe past it. Guardrails on the compiler stand regardless — eps_P+eps_Q=(r+1,1) on every output and the 6/6 regression before any new pair is trusted, because a wrong reduction makes 24 EMPTYs statements about the wrong variety."
    },
    {
      "topic": "Trust the extracted 34-case table now, or verify before building on it?",
      "positions": "enumerated-corners L1/L2 build the campaign's largest new block directly on gghv_audit/all_cases_max_le_150.json (and its author verified record 22 by hand). skeptic risk 2, structural A2 and engineering TAIL-1 step 6 all say the table is unverified against the published PDF, its own author flagged the extraction, and three claims from that class were retracted in one session.",
      "adjudication": "Verify — but in parallel, not in series. TABLE-VERIFY is one agent-day on day 1 and blocks the batch of 24, not the single-case pipeline build for record 22. Compiler work on record 22 proceeds simultaneously; if the row turns out wrong, one agent-week of pipeline is lost and the pipeline itself survives. Making 6-8 agents idle for a day behind a PDF render would be its own waste."
    },
    {
      "topic": "Audit first or build the plant first?",
      "positions": "skeptic: the campaign is blocked by a broken bookkeeping layer, ~40% of the residual queue is provably vacuous, and the highest-value item is not a solver run at all. engineering: nothing died to mathematics, build a provisioned persistent plant and re-run the whole undecided set through it.",
      "adjudication": "False dichotomy, and both plans state it as an either/or only because each was written by a single specialist. They consume disjoint resources — the plant is engineer-time and money, the audits are mathematician-time — and both are prerequisites for different halves of the board. Run them as parallel day-1 lanes. The one real ordering constraint is that no solver hour may be spent before gate.py is green on the export and the refusal list is live, because unaudited compute is what produced the queue that skeptic is complaining about."
    },
    {
      "topic": "Which region is the real target: sub-125 exclusions, the 24 above-125 cases, or B=16?",
      "positions": "skeptic assumes JC2 is TRUE and targets certified exclusions plus literature corrections, ranking the sub-125 enumeration re-derivation first. enumerated-corners targets the 24-case closure to raise the published floor from 108 toward 150. structural targets mechanism-first routes and rates B=16 as the only door where the implication runs the right way (Thm 1.2 is an iff). engineering ranks by expected information per core-hour and lands on pentagon + d=8.",
      "adjudication": "No adjudication needed on targets — the four sets are nearly disjoint and a 6-8 agent fleet can run all of them. Adjudicate the FRAMING instead: skeptic is right that expected value is dominated by certified exclusions and corrections, structural is right that B=16 is the only iff on the board, and both are consistent. The plan's headline deliverable is a certified exclusion ledger; the counterexample is the low-probability tail of doing that honestly. Any agent whose lane depends on a HIT for its value is mis-scoped."
    },
    {
      "topic": "Do the four plans' hit probabilities mean the same thing?",
      "positions": "structural L2 quotes 4% (the highest single figure anywhere) for collision-first; enumerated-corners quotes ~0.1-0.5% for a counterexample after conditioning on lift and H1-H6; skeptic prices everything under 1% and says any plan whose value depends on a HIT has negative expected value.",
      "adjudication": "The numbers are not commensurable and must not be summed or ranked against each other. structural's 4% is P(the augmented system has a solution), enumerated-corners' figures are P(a verified counterexample survives H1-H6). Adopt enumerated-corners' convention fleet-wide: every p_hit is quoted as P(verified counterexample) with the conditioning chain stated. Under that convention the whole board is ~1-2% and skeptic's warning stands."
    },
    {
      "topic": "Is EMPTY-mod-p worth producing at all?",
      "positions": "enumerated-corners and engineering both queue large mod-p sweeps (24 cases, 41 timeout shapes) at 2-3 primes. skeptic says the campaign repeatedly defers the genuinely valuable char-0 closure in favour of new mod-p sweeps its own rule forbids promoting.",
      "adjudication": "skeptic's objection dissolves once CERT exists — a mod-p EMPTY becomes a staged intermediate rather than a dead end. So the ordering rule is: CERT is built in week one, and any sweep producing EMPTY-mod-p must enqueue a CERT job for each row rather than filing it as a verdict. A sweep that outruns CERT's throughput is manufacturing stranded verdicts and must slow down."
    }
  ],
  "first_week": [
    {
      "day": "Day 1",
      "work": "PLANT: provision.sh (Singular 4.3.2p16, msolve 0.10.1 from source NOT apt 0.6.5, sympy/flint/gmpy2/PARI pinned, poppler-utils), engines.json, engine_guard.py; request the 16-core/128 GB persistent host. LEDGER: job.json / verdict.json schema, content_hash over canonicalized generators (not file text), verdict label vocabulary. TABLE-VERIFY: render §6 of 1708.07936 as page images and diff row-for-row against all_cases_max_le_150.json. ENUM-AUDIT: instrument ggv_algorithms.py, expose all filters, begin the divergence trace. COR-5.7: begin the line-by-line re-derivation of (5.12) from gghv.txt:1412-1433, recomputing the bracket by hand and in sympy.",
      "roles": ["2x infrastructure engineer (PLANT)", "1x registrar (LEDGER)", "1x librarian (TABLE-VERIFY)", "1x enumeration engineer (ENUM-AUDIT)", "1x proof auditor (COR-5.7)"],
      "deliverable": "engines.json with binary sha256s; the two schemas committed; a §6 verification verdict (CERTIFIED or a discrepancy list); the first divergence table from the re-implementation; a one-page written statement of where Cor 5.7's proof stands. If TABLE-VERIFY fails, CASE24 is suspended and ENUM-AUDIT absorbs the fleet."
    },
    {
      "day": "Day 2",
      "work": "PLANT: runner.sh generalizing wave6/bottomedge/sweep.sh — one verdict per commit, stdout and stderr tee'd separately, /usr/bin/time -v, cgroup MemoryMax per job, single-slot FIFO for the heavy lane (a queue file, not a policy), disk AND inode watcher, pkill -f banned in a pre-commit hook. LEDGER: gate.py implementing the export sanitizer, no-verdict-from-empty-output, stderr-clean, excess>0, torus-rank routing, content-hash dedup, orientation-in-the-key; wired into exporter, runner and CI. AST scan for literal-True check conditions (expect ~45). COR-5.7 continues. CASE24: begin compiling record 22 (8,28)/(3,4) via TRACKD_CHAIN_MAP, with the 6/6 published-pair regression run FIRST.",
      "roles": ["2x infrastructure engineer", "1x registrar", "1x proof auditor", "1x compiler/polygon deriver", "1x auditor-skeptic (AST scan, gate negative controls)"],
      "deliverable": "Smoke suite passing across a deliberate container restart; gate.py green or red with a triage list; the 45-finding AST report; the 6/6 regression reproduced or the compiler declared untrusted."
    },
    {
      "day": "Day 3",
      "work": "LEDGER: re-key the whole tree by content hash, publish RECONCILIATION.md (429/432/464/474/804/34-with-24-open — one object per number, a generating script per row, 804/189/184 marked NONEXISTENT), backfill prime lists, demote un-audited EMPTYs. SCHED: the pre-flight refusal list only (Moh degree, gcd, excess<=0, solve-mode on positive-dimensional input, terminal hash, vacuous criteria). PRIME-AUDIT: build the single-prime register (20 above-125 F_65521 shapes, ladder d=7, chart Z d=9/10/11, F3 x2, case (2)'s 32003/65537) deduped by content hash. CERT: lucky-prime certifier with controls 5/11/17 REQUIRED to be rejected. COR-5.7 verdict due: one position, every contradicting file amended.",
      "roles": ["1x registrar", "1x scheduler engineer", "1x prime auditor", "1x certifier author", "1x proof auditor", "1x compiler"],
      "deliverable": "RECONCILIATION.md; REFUSED.json listing what will never be scheduled and why; the single-prime register with its true deduplicated count; a lucky-prime selector that demonstrably rejects the control primes; ONE recorded position on Cor 5.7."
    },
    {
      "day": "Day 4",
      "work": "Heavy host live. D8N: regenerate from w6_seed_d8.py, diff against wave5/ms/m16_d8_*.ms, sanitize, launch chart N at two primes with 96 a square, a_16 free. COR-5.7 compute arm: measure torus rank on p108_192622 and p108_525122, independently re-derive the rank-5 slice, launch the 3 unresolved leaves under -g 2 at 8 h. PRIME-AUDIT: sweep begins on the light box, ~96 s per prime, one verdict per commit. CERT: multi-prime GB batches on case (2) both charts. PENT-RANK: independent re-derivation of FABLE-003's reduction begins (two agents, separate code paths). CASCADE-4: paper design begins, design only, no code.",
      "roles": ["1x solver operator (heavy)", "1x solver operator (light/prime sweep)", "1x certifier", "2x reduction auditors (PENT-RANK)", "1x cascade designer", "1x registrar"],
      "deliverable": "First verdict from the corrected d=8 chart N export in the history of the campaign, or a labelled TIMEOUT with peak RSS and D-ceiling; p108 leaves running under the correct engine mode for the first time; the first batch of prime-audit rows."
    },
    {
      "day": "Day 5",
      "work": "CERT: CRT + rational reconstruction with the stability rule (stable across two successive prime additions or STOP), exact ideal-membership verification, Nullstellensatz linear-algebra route, two-sided self-test — planted-consistent must NOT certify 1, planted-inconsistent must. TAIL-TEST: mechanical scan of every log and RUNLOG for exit 124 / 0-byte output / TIMEOUT, emit TIMEOUT_SHAPES.json with torus rank and orientation per row, reconcile 33 vs 36 vs 41. ENUM-AUDIT: A'_t re-derivation for the (10,40) chain from the algorithm's own filters. SUBCASE2: librarian verifies Prop 4.3 has two sub-cases and tests D=1 compatibility. SWEEP-SCOPE: the two-hour gate-A1 audit of w6_plane_sweep*.py.",
      "roles": ["1x certifier", "1x lifter", "1x librarian/enumeration engineer", "1x scope auditor", "1x solver operator", "1x registrar"],
      "deliverable": "CERT tool with both self-test sides firing, or committed as FAILING; the 41 timeout shapes enumerated for the first time (expect fewer); A'_t DISCHARGED or new census rows; a verbatim scope statement for the sweep dichotomy; a go/no-go on SUBCASE2."
    },
    {
      "day": "Day 6",
      "work": "CERT applied to case (2) both charts on the persistent host, marker-resumable so a restart costs a stage. TAIL-TEST: the 20-sample tail-closure saturation test across (150,300], counting new tails against the 34->26 baseline. CASE24: record 22 driven to a verdict end to end at three compliant primes — the pipeline test that gates the other 23. PENT-RANK: the reduction must reproduce a known EMPTY and a known NON-EMPTY control today or the lane stops. Background heavy slot: the one 186-var pentagon deg-2 run, lowest priority. Idle capacity: ELIMINANT-9, one CPU-hour.",
      "roles": ["1x certifier", "1x solver operator (heavy)", "1x compiler", "2x reduction auditors", "1x tail engineer"],
      "deliverable": "Case (2) char-0 attempt with a stage reached or a certificate; TAIL_SATURATION.json — the go/no-go that decides the chain-compiler question and nothing else does; record 22 with a labelled row; PENT-RANK certified or quarantined; the degree-9 eliminant factored over Q, replacing a retracted claim."
    },
    {
      "day": "Day 7",
      "work": "MIDPOINT AUDIT, mandatory, and read the ledger rather than the plan. Confirm: no TIMEOUT or OOM has drifted into prose as 'probably empty'; the AST scan is at zero; no verdict lacks a prime list or stderr digest; the contradiction linter is green; every count in RECONCILIATION.md still holds. Re-cost every family from measured data — a TIMEOUT raises its family's cost model, an OOM raises its memory model. Then re-rank week two on measurements, not on the day-1 guesses in any of these four plans. Adversarial red-team pass: one agent whose ONLY job is to try to break every EMPTY produced this week.",
      "roles": ["1x auditor-skeptic (owns the audit)", "1x red-team adversary", "1x registrar", "remaining agents finish or cap their day-6 jobs"],
      "deliverable": "A week-1 verdict table where every row carries a label from the vocabulary and no row is blank; a re-costed queue for week two; a written list of what is still TIMEOUT/OOM/NOT RUN with its measured resource wall. Undecided stays undecided, in writing."
    }
  ],
  "definition_of_done": "Done is NOT a counterexample, and any lane whose value depends on one is mis-scoped — all four plans price a verified counterexample at ~1-2% for the whole campaign. Done is a repository in which: (1) every verdict row carries characteristic, prime list, corner A0, (m,n), orientation, content hash, engine + version, stderr digest, and a certifier triple whose negative control was OBSERVED to fail — no timeout, OOM, parse error or empty output appears anywhere as a verdict; (2) at least one new characteristic-zero exclusion theorem exists that did not exist before, carrying a certificate a referee can re-check by polynomial multiplication (the leading candidates are (72,108) case (2) over Q-bar and the promotion of the 46 stranded EMPTY-mod-p rows via CERT); (3) the sub-125 enumeration has been re-derived from [5]'s Algorithms rather than imported, with every divergence traced to its algorithm step, A'_t=(1,0) either discharged or replaced by new census rows, and the §6 table verified against the published PDF by page image; (4) every one of the 34 published cases at max<=150 carries a labelled row — [PROVED-exact], EMPTY-mod-p with its prime list, or NO VERDICT with its measured torus rank, eqs/vars, wall time, RSS and stderr hash — and no row is blank; (5) every load-bearing external step is either re-derived locally or labelled UNVERIFIED-HERE: GGHV Cor 5.7, [6, Prop 2.5], A'_t, the [5] enumeration, the [4] §3.5 claim for (80,112), Bayle-Beauville and Ramanujam/Morrow behind the deck-group theorem, and the JC_2n <=> DC_n dictionary if it is ever used; (6) the census carries exactly one number per defined region, each with a generating script, with 804, 189 and 184 recorded as unsupported and the README describing objects that exist; (7) the enumerable list of resisters exists as a file rather than as folklore, each with the measured reason it resisted, so the next campaign inherits a queue instead of a rumour; and (8) if any candidate ever appears, H1-H6 has run in full with H6 shown to have fired and H5 gauge invariance tested under random affine changes on BOTH source and target — the step both prior false 'hits' would have failed — before the word counterexample is written anywhere. That repository is publishable as a negative result, as a raised floor from 108 toward 150, and as a correction to two preprints. It is the realistic maximum value of this work, and all four plans say so in their own words."
}
```