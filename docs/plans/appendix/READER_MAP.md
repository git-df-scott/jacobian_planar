### READER: status-map
```json
{
  "summary": "Archive of a campaign hunting a plane Jacobian counterexample (JC2). Bottom line, stated identically in canon/STATUS.md §0 and canon/ADJUDICATION.md §0: NO counterexample, and no non-EMPTY verdict on any real system, ever; nothing promoted from mod-p to Q. Two apparent hits were gauge artefacts, both caught pre-commit (STATUS §6.6). The board splits into three arenas. (1) The (72,108)/(108,72) pair — the single surviving degree pair below 125 in GGHV (arXiv:2204.14178, unrefereed), with Nguyen's refereed floor at 104 (STATUS §1). J(Q,P) = -J(P,Q), so the two orientations are one territory. Its case (2) quadrilaterals are EMPTY mod p on both charts at compliant primes (p ≡ 1 mod 3) with a degree-1144 eliminant proved irreducible over Q by a Dedekind subset-sum sieve at 8+1 primes [PROVED-exact] (STATUS §2.5, re-verified independently in ADJUDICATION §1) — but the campaign's own rule forbids promoting mod-p to char 0, and the 13-variable residual over the degree-1144 field was NEVER EXECUTED (STATE_FULL §B, MISS-4). Its case (1) pentagons have NO VERDICT of any kind: structure certified (rank 60 of 61, 58 essential parameters vs 60 conditions, sparse exportable system pent_L23.ms) but both engines OOM at ~13.9 GB and >40 GB monolithic (STATUS §3, ADJUDICATION §3, STATE_FULL §B). The (9,27) orientation is killed in the literature only by GGHV Cor 5.7, never re-derived by anyone; the campaign's two independent p108 shape tests were still running/queued (STATE_FULL §B). The Borisov framework family, by contrast, is genuinely closed: THEOREM 2 certified, THEOREM 3 confirmed with a real gap in its recorded proof found and repaired, and the (108,72) three-dessin route dead for all 9 admissible charts (STATUS §2.2/§2.6, TRUST_MAP §2–§4, LIVE_MAP). (2) The B=16 GGV ladder — the one genuinely open counterexample corridor found in the literature (GGV Pro Mathematica 27 (2013) stalls at deg(q1)=5; GGV 2017 says B=16 'still within reach'). d=2,3,4 reproduce EMPTY; d=5 and d=6 EMPTY at char-0 Gröbner proof standard; d=7 chart Z+N EMPTY at ONE prime only; d=8..12 chart Z EMPTY at 1–2 primes but chart N never launched or never run; the d=12 unsaturated family is UNDECIDED; d=27 untouched (STATE_FULL §A, ADJUDICATION §2, CATCHES.md 08:00Z). CATCHES.md carries two authoritative retractions that bear directly here: all numerical 'empty floor' residual evidence at d ≥ 8 is VOID (planted-root controls prove multi-start Newton is blind at 25+ unknowns), and a msolve parse failure writes '[-1]' while exiting 0 — a silent-lie EMPTY. (3) Above 125 — largely unexplored: 464 admissible pairs in [125,300], only 20 covered by the queue, 6 EMPTY, 36+5 TIMEOUT (not EMPTY), 429 cases blocked on an unbuilt chain-compiler extension. The honest open list is dominated by compute walls and unbuilt machines, not by mathematics.",
  "territories": [
    {
      "name": "(72,108)/(108,72) as one territory",
      "what": "The single degree pair below 125 that GGHV do not eliminate; J(Q,P) = -J(P,Q) makes both orientations one territory, proved two independent ways (wave0/w0_h1a_swap_and_G.py)",
      "verdict": "UNDECIDED overall; framework sub-territory closed, case (2) mod-p only, case (1) no verdict",
      "label": "[PROVED-exact] for the swap identity; territory itself undecided",
      "path_section": "canon/STATUS.md §1, §7 (Wave-1 gate table)",
      "state": "live"
    },
    {
      "name": "(72,108) case (2) quadrilaterals",
      "what": "The quadrilateral branch of the Prop 4.3 case split; edge system + chart d_3_3 = 1",
      "verdict": "EMPTY mod p on both charts at 3 fresh compliant primes and 2 code-disjoint routes; NOT promoted to char 0. Eliminant computed (degree 1144, squarefree) and PROVED irreducible over Q, so all 1144 edge points are Galois-conjugate and the Q-bar question is one yes/no. The 13-variable residual over the degree-1144 field is unsolved and, per STATE_FULL, was never executed.",
      "label": "mod-p EMPTY (not char-0); eliminant irreducibility is [PROVED-exact]",
      "path_section": "canon/STATUS.md §2.4, §2.5, §4; canon/ADJUDICATION.md §1 (eliminant row, 9th prime 100153), §3; canon/STATE_FULL.md §B (MISS-4)",
      "state": "live (OPEN over Q-bar)"
    },
    {
      "name": "Pentagon case (1) at (72,108) / (8,28) orientation",
      "what": "The pentagon polygon branch: 58 essential parameters (after 3 gauges) against 60 independent y-adic conditions, plus 314 surplus; sparse (686 monomials at level 13, 59,626 at level 23)",
      "verdict": "NO VERDICT EVER RECORDED. Structure certified (rank 60/61 at two primes, saturation at level j ≤ 23, affine cascade at levels 13–17). Emptiness explicitly NOT claimed. Both engines OOM: msolve on pent_L23 exit 137 (peak 13.9 GB, 0-byte output), Singular slimgb on L18 exit 137; monolithic form measured >40 GB. Block-cascade build UNBUILT.",
      "label": "STALLED / OOM — not EMPTY (timeout and OOM are not verdicts)",
      "path_section": "canon/STATUS.md §3, §4, §7; canon/ADJUDICATION.md §1 (pent_L23 retry row), §3; canon/STATE_FULL.md §B, §E.2",
      "state": "live (OPEN)"
    },
    {
      "name": "(9,27) literature kill",
      "what": "The other orientation/normalization of the live pair, discarded in the literature ONLY by GGHV Cor 5.7 (their Sec 5 apparatus), which no one has ever re-derived",
      "verdict": "NOT independently confirmed. The campaign built two p108 systems (verified = Prop 4.1 polygons, bracket -x, convention checked) as the FIRST independent test; shape 1 was in msolve (1800s budget), shape 2 queued. Verdict standards pre-registered both directions. No verdict recorded.",
      "label": "external citation only; independent test IN FLIGHT / queued",
      "path_section": "canon/STATE_FULL.md §B; standards in AUDIT_EOD Sec 10 (cited from STATE_FULL §B)",
      "state": "live (OPEN)"
    },
    {
      "name": "Borisov endgame (the T_{D,k}(R) = -c obstruction)",
      "what": "The framework reduction to one ODE-type equation in one rational function R(v): alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c",
      "verdict": "SOLVED COMPLETELY. Master identity re-derived from scratch (17 checks). The archive's decisive step (evaluate at v = -1) was REFUTED — it assumed R polynomial. The pole solutions exist: exactly one solution in Q-bar(v), pole order exactly 4 at v = -1, map-degree exactly 4. The framework nevertheless dies one layer up, by two independent repaired closures (pole admissibility ord ≥ -3 vs required 4; degree ledger deg W~ = 15 vs required 28). W3-1 ODE classification independently verified over 96 cells, 0 mismatches.",
      "label": "[PROVED-exact] / [CERTIFIED] (E1–E6, verified independently in ADJUDICATION §1)",
      "path_section": "canon/TRUST_MAP.md §2, §3, §5; canon/LIVE_MAP.md 'What moved'; canon/STATUS.md §2.1, §6.7, §6.8; canon/ADJUDICATION.md §1 (W3-1 row)",
      "state": "closed"
    },
    {
      "name": "(108,72) three-dessin framework route",
      "what": "Borisov's Three-dessin Framework predicts (108,72); question was whether it introduces new conditionality",
      "verdict": "CLOSED for every admissible chart. 11 does not divide 108, so it cannot reuse the (99,66) edge vector; admissible charts indexed by s = a+b | gcd(108,72) = 36, nine in all — seven give a unique endgame solution of map-degree 4, two (s = 18, 36; D = 12, 9) give no rational solution at all; no chain degree is 4. Every layer L1–L4 transfers or is immaterial. Conditional only on Keller chart exponent p = 3.",
      "label": "[CERTIFIED] (EC_10872_instantiation.py, 19 checks); STATUS-side kill [PROVED-exact] after THEOREM 2/3 discharge",
      "path_section": "canon/TRUST_MAP.md §4 (first bullet), §5 (EC row); canon/LIVE_MAP.md; canon/STATUS.md §2.2",
      "state": "closed (with caveat, see disagreements)"
    },
    {
      "name": "THEOREM 2 / THEOREM 3 residue",
      "what": "The campaign's only remaining framework conditionality: Taylor-pin rigidity g = alpha*U(U-1)^8, and pole-fiber => R polynomial",
      "verdict": "DISCHARGED. THEOREM 2's conclusion certified (w1_L3_step2_pinning.py); THEOREM 3 CONFIRMED after a genuine gap in its recorded proof was found (fiber count fixes multiplicity, not location; witness R = 1/(v+1)^13 satisfies every recorded premise and is not a polynomial) and repaired via the degree ledger, which forces (a,b) = (6,9) uniquely. TRUST_MAP's independent line is stronger still: neither repaired closure needs THEOREM 3 at all.",
      "label": "[PROVED-exact] / [CERTIFIED]; independently VERIFIED-HERE in adjudication",
      "path_section": "canon/STATUS.md §2.6, §4 (first row); canon/TRUST_MAP.md §1 (THEOREM 2/3 rows), §2; canon/ADJUDICATION.md §1 (THEOREM 2 and THEOREM 3 rows)",
      "state": "closed"
    },
    {
      "name": "B=16 ladder, d = 3..7",
      "what": "GGV Pro Mathematica 27 (2013) Thm 1.2 systems (1.2)+(1.3): B = 16 iff a solution with mu_0 != 0 exists, which would BE a JC counterexample. Cells deg(q1) = d correspond to degree pairs (16(2j+1), 16(3j+1)), j = d-1",
      "verdict": "d=2,3,4 EMPTY, reproducing GGV (char-0 grade). d=5 EMPTY over Q at char-0 Gröbner proof standard (22 s; GGV stalled here for an hour in 2013) + 3 primes. d=6 EMPTY over Q char-0 (135 s) + 3 primes. d=7 (Z+N sound split) EMPTY at p = 1000003 ONLY — the confirming primes died in container restarts and were never re-run [MISS-1]. Note ADJUDICATION §2 records d=7 as STALLED-OOM (13.96 GB); STATE_FULL's later sound Z/N split supersedes it with a single-prime result.",
      "label": "d=3..6 char-0 [PROVED-exact]; d=7 mod-p single prime only (NOT char 0, NOT confirmed)",
      "path_section": "canon/STATE_FULL.md §A; canon/ADJUDICATION.md §2 (Wave 5 table), §6 (gauge-fixing correction demoting earlier d=7 chart verdicts to slice results)",
      "state": "d≤6 closed; d=7 live (single-prime, unconfirmed)"
    },
    {
      "name": "B=16 ladder, d = 8..12, chart N cells",
      "what": "The chart-N (mu2 != 0 saturated) half of the corrected sound split Z = {mu2 = 0} ∪ N = {mu2 != 0 saturated}",
      "verdict": "UNDECIDED. d=8 chart N was exported but NEVER LAUNCHED [MISS-2]; d=9,10,11 chart N never run (known queue); d=12 chart N seed -1/12 twin was running at p = 1000033 (original at 1000003 OOM-killed), seed 1/20 REQUIRED for the cell and never run [MISS-3]. d=8 chart N was attacked in four cheap formulations: ALL TIMEOUT with clean stderr — resistance measured, not a verdict. Honest conclusion recorded: exact elimination cannot decide d >= 8 chart N on this hardware.",
      "label": "TIMEOUT / NOT RUN — explicitly not EMPTY",
      "path_section": "canon/STATE_FULL.md §A (d=8..12 rows), §E.1; canon/CATCHES.md 'd=8 chart N — resistance measured, not a verdict (08:00Z)'",
      "state": "live (OPEN)"
    },
    {
      "name": "B=16 ladder, chart Z, d = 8..12",
      "what": "The mu2 = 0 half of the sound split",
      "verdict": "d=8 EMPTY at 2 primes; d=9,10,11 EMPTY at p = 1000033 single prime; d=12 (both rational seeds) EMPTY at 2 primes. All mod-p only.",
      "label": "mod-p EMPTY (1–2 primes) — not char 0",
      "path_section": "canon/STATE_FULL.md §A",
      "state": "live (mod-p only; cells not closed because chart N is missing)"
    },
    {
      "name": "Resonant cell d = 27",
      "what": "The next resonant ladder cell under the resonance law (singular descent only at d = 3k^2); roots 1/28 and -1/20",
      "verdict": "UNTOUCHED — in the queue, no run, no verdict",
      "label": "NOT RUN",
      "path_section": "canon/STATE_FULL.md §A (last rows), §E.1",
      "state": "live (OPEN)"
    },
    {
      "name": "d = 12 unsaturated family",
      "what": "The unsaturated (possibly degenerate) family at d = 12 — the campaign's biggest anomaly, since the d=3 analogue solves instantly",
      "verdict": "UNDECIDED after 2 kill attempts; solo compute slot queued. Explicitly named as one of the 7 things still capable of producing a counterexample.",
      "label": "UNDECIDED",
      "path_section": "canon/STATE_FULL.md §A (d=12 unsaturated row), §E.1, §G.1",
      "state": "live (OPEN)"
    },
    {
      "name": "(8,28) corner",
      "what": "The campaign-side orientation/normalization of the (72,108) territory, where the pentagon and case-(2) systems actually live",
      "verdict": "Pentagons NO VERDICT (>40 GB monolithic measured; 2-torus found; block-cascade UNBUILT). Case (2) EMPTY mod p on both charts, eliminant degree-1144 irreducible over Q. Case (2) over Q-bar: linear-residual-over-K route PLANNED, NEVER EXECUTED. Four (8,28) runs sit in the unbuilt overnight queue.",
      "label": "mixed: mod-p EMPTY (case 2), NO VERDICT (pentagons)",
      "path_section": "canon/STATE_FULL.md §B (first bullet), §E.1",
      "state": "live (OPEN)"
    },
    {
      "name": "Above-125 tail",
      "what": "Degree pairs with max >= 125, the region resting on nothing published; ~150 of 167 enumerated targets unrun per STATUS, and a coverage audit finding 464 admissible pairs in [125,300]",
      "verdict": "LARGELY UNEXPLORED. Queue covered 20 of 464; virgin sweep decided 6 EMPTY (2 primes) and 36 TIMEOUT. 429 cases need a chain-compiler extension (library stops ~150) — UNBUILT. 3 twist-blocked + 1 A'_t-assumed case unclassified. Orphan reconciliation: 254/478 vertex-LIVE entries orphaned; F3 x2 EMPTY at single prime 65521 [MISS-6]; 5 TIMEOUT; 13 F22 blocked on a j-instance chain-map gap. Legacy 180-target trackD queue disposition decided (run after virgin TIMEOUTs).",
      "label": "6 EMPTY mod-p (2 primes); everything else TIMEOUT / NOT RUN / BLOCKED",
      "path_section": "canon/STATE_FULL.md §C; canon/LIVE_MAP.md 'Ranked live territory' §1; canon/STATUS.md §1, §4 (H2 row)",
      "state": "live (OPEN — the largest unsearched region)"
    },
    {
      "name": "41 timeout shapes",
      "what": "36 virgin-sweep TIMEOUTs plus 5 orphan-reconciliation TIMEOUTs above 125, queued at an 1800 s long budget",
      "verdict": "UNDECIDED. Timeout is explicitly not EMPTY. Named as item 3 of the 7 things still capable of producing a counterexample.",
      "label": "TIMEOUT — no verdict",
      "path_section": "canon/STATE_FULL.md §C, §E.1, §G.3",
      "state": "live (OPEN)"
    },
    {
      "name": "Small-cell / VR routes (VR-2025 + arXiv:1406.0886)",
      "what": "An iff-reformulation sweeper over small cells, listed as unbuilt machine #4",
      "verdict": "MACHINE NOT BUILT; no cells run, no verdict. Listed as item 7 of the 7 counterexample-capable routes ('VR-2025 iff-cells').",
      "label": "NOT BUILT / NOT RUN",
      "path_section": "canon/STATE_FULL.md §E.4, §G.7",
      "state": "live (OPEN)"
    },
    {
      "name": "GGV conjecture (symbolic-d closure of B=16)",
      "what": "GGV's open conjecture that all solutions have mu_1 = mu_2 = 0 (STATE_FULL: closed forms + resonance law in hand, proof unattempted)",
      "verdict": "OPEN. A proof would close B=16 outright and is called 'the sharpest theorem-shaped target on the board'; a refutation at some d would BE a constructive counterexample.",
      "label": "OPEN — proof unattempted",
      "path_section": "canon/STATE_FULL.md §A (last row), §G.6; canon/ADJUDICATION.md §3",
      "state": "live (OPEN)"
    },
    {
      "name": "Closed-as-hiding-places set (H1d, p10=0 chart, H1e crossfire, H3-A1 reverse descent, Second Framework, isotope series, N2_prompt Phase 0)",
      "what": "Assorted routes checked and disposed of",
      "verdict": "H1d: GGHV Prop 4.3 case split exhaustive, no case (3) (residue: external cite [6, Prop 2.5] not re-derived). p10 = 0 chart provably empty (0 = x^2). H1e: every geometric-degree bound runs the wrong way — NEGATIVE, no cheap kill. H3-A1: k=0 stratum is a restatement of JC2, not a route around it. Second Framework (435,290) and the isotope series killed uniformly by the corrected transfer theorem. N2_prompt Phase 0 (rederive degree-23 Belyi) is unnecessary work.",
      "label": "[PROVED-exact]/[CERTIFIED] as appropriate (E6 for the transfer theorem)",
      "path_section": "canon/STATUS.md §2.6 'Closed as hiding places'; canon/TRUST_MAP.md §3; canon/LIVE_MAP.md §5 'Closed, do not re-run'",
      "state": "retired"
    },
    {
      "name": "Numerical / multi-start Newton lanes",
      "what": "Multi-start Newton residual floors used as emptiness evidence at pentagon (165 unknowns) and ladder d=8..12",
      "verdict": "RETRACTED. Planted-root controls (residual exactly 0 by construction) were NOT found: pentagon best 1.9e5 of 3 starts; ladder d=8 best 1.7e3 of 25 starts. The quoted floors (d=8 1.2e-10, d=9 1.4e-10, d=12 1.6e-10) measure the SOLVER, not emptiness. Bifurcation residual 1.6e-3 at 136 real unknowns likewise void. Numerical lanes demoted to opportunistic finders: a HIT would be real, a MISS says nothing.",
      "label": "RETRACTED as evidence (authoritative retraction)",
      "path_section": "canon/CATCHES.md 'RETRACTION (05:45Z) — the numerical empty floor evidence is VOID'",
      "state": "retired as evidence"
    }
  ],
  "open_list": [
    "(72,108) case (1) pentagons — no verdict has ever been recorded; both engines OOM (13.9 GB msolve, >40 GB monolithic); block-cascade unbuilt",
    "(72,108) case (2) over Q-bar — 13-variable residual system over the degree-1144 number field; planned, never executed (MISS-4)",
    "(9,27) orientation — GGHV Cor 5.7 never independently re-derived; campaign's shape 1 in msolve, shape 2 queued, no verdict",
    "B=16 ladder d=7 — EMPTY at one prime only; confirming primes died in container restarts, never re-run (MISS-1)",
    "B=16 ladder d=8 chart N — exported but never launched; all four cheap formulations TIMEOUT (MISS-2)",
    "B=16 ladder d=9,10,11 chart N — never run",
    "B=16 ladder d=12 chart N — seed -1/12 twin mid-run, seed 1/20 required and never run (MISS-3)",
    "B=16 ladder d=12 unsaturated family — undecided after two kill attempts",
    "B=16 ladder d=27 resonant cell — untouched",
    "GGV conjecture (mu_1 = mu_2 = 0 for all solutions) — proof unattempted; refutation would be a constructive counterexample",
    "41 undecided TIMEOUT shapes above 125 (36 virgin + 5 orphan) at 1800 s budget",
    "429-case above-125 frontier — blocked on unbuilt chain-compiler extension (library stops ~150)",
    "3 twist-blocked + 1 A'_t-assumed above-125 cases — unclassified",
    "13 F22 cases blocked on the j-instance chain-map gap; F3 x2 EMPTY at single prime 65521 needs a second prime (MISS-6)",
    "VR-2025 / arXiv:1406.0886 small-cell iff-sweeper — machine not built",
    "H4 deg_y = 3 slice — FRAMEWORK.md's own OPEN-1, untouched",
    "Paths A–E (sessions 39–42): A1 (is the h^2 square forced, general weights), B1 literature read, C2 the d=2 Geiser/Bertini pincer, C4 Orevkov, E-abort check — none done",
    "Duplicate-system dedup-by-hash across registers — pending",
    "Residue: GGHV's external citation [6, Prop 2.5] never re-derived",
    "Residue: THEOREM 1 ladder extension to m = 13 (evidence, not proof) — would make the pole-order route fully unconditional"
  ],
  "degree_bounds": {
    "assumed": "GGHV (arXiv:2204.14178, UNREFEREED, v1 only) eliminate every degree pair with max < 125 except (72,108)/(108,72); the refereed floor is Nguyen 104 (Quaestiones Mathematicae 48(2) 2025, arXiv:1902.05923), so everything in [105,124] rests on unrefereed work. Independently re-verified: 4560 pairs in 105..124 decided, 6 arise, 0 undecided (T1). Above 125: 804 admissible degree pairs recorded with 167 enumerated targets (~150 unrun) per 41.md/STATUS; the later coverage audit counts 464 admissible pairs in [125,300], of which the queue covered 20. Zoladek gives a floor d >= 6 on the geometric degree; the one actual value at this pair is Borisov's d = 16; Bezout gives d <= 7560 (wrong direction, no cheap kill). B=16 ladder cells map to degree pairs (16(2j+1), 16(3j+1)) with j = d-1, so d=3 is (80,112), d=5 is (144,208), d=6 (176,256), d=7 (208,304), d=8 (240,352) — d >= 4 lies ABOVE the 125 window and was open in the literature. Framework chain degrees: First D=13, Second D=23, Three-dessin D=13; endgame map-degree is always 4, so any framework demanding D_chain != 4 is empty.",
    "source_path": "canon/STATUS.md §1, §2.2, §2.6 (H1e bullet); canon/ADJUDICATION.md §1 (T1 row), §2 (chain of custody, items 1–4); canon/STATE_FULL.md §C; canon/TRUST_MAP.md §3"
  },
  "facts": [
    {
      "claim": "No counterexample found; no non-EMPTY verdict on any real system, ever; nothing promoted from mod-p to Q; the HIT protocol was never invoked because nothing reached it",
      "label": "campaign bottom line, stated three times independently",
      "evidence_path": "canon/STATUS.md §0; canon/ADJUDICATION.md §0; canon/LIVE_MAP.md 'Terminal state for this iteration'"
    },
    {
      "claim": "(72,108) and (108,72) are one territory since J(Q,P) = -J(P,Q); proved two independent ways",
      "label": "[PROVED-exact]",
      "evidence_path": "canon/STATUS.md §1 (wave0/w0_h1a_swap_and_G.py)"
    },
    {
      "claim": "The degree-1144 edge eliminant over Q exists, is squarefree, and is irreducible over Q by a Dedekind subset-sum sieve at 8 good primes; a 9th prime (100153) was factored independently in the adjudication and agrees. Consequence: all 1144 edge points are Galois-conjugate, so the Q-bar question is one yes/no; no rational edge points",
      "label": "[PROVED-exact], independently VERIFIED-HERE",
      "evidence_path": "canon/STATUS.md §2.5; canon/ADJUDICATION.md §1 (eliminant row)"
    },
    {
      "claim": "The prior claim that the char-0 eliminant 'completed via msolve' was FALSE for five days — the cited file contained no polynomial, it was msolve's real-solution output (28 boxes x 7 coords), because the campaign ran without -P. Re-run with -P 1 produced the real eliminant",
      "label": "correction to the campaign record; artifact now exists",
      "evidence_path": "canon/STATUS.md §2.4 (H1F_FINDING.md)"
    },
    {
      "claim": "The eliminator (groebner -> dim == -1) is controlled: A6 planted-data mutants return non-EMPTY (dim 0, vdim 1144) where expected, contradictory pins return -1, and msolve 0.10.1 agrees at three primes",
      "label": "[CERTIFIED]",
      "evidence_path": "canon/STATUS.md §2.3 (MANIFEST §G, wave0/w0_a6*.py)"
    },
    {
      "claim": "The endgame equation (v+1)^4(3v(v+1)R' - 13R) = kappa != 0 has EXACTLY ONE solution in Q-bar(v), with pole order exactly 4 at v = -1 and map-degree exactly 4; the archive's decisive 'evaluate at v = -1' step was invalid because it assumed R polynomial",
      "label": "[PROVED-exact], two independent toolchains (sympy E2, PARI/GP E3)",
      "evidence_path": "canon/TRUST_MAP.md §2; canon/STATUS.md §6.7"
    },
    {
      "claim": "The (99,66) First Framework emptiness CONCLUSION survives but its published PROOF is refuted and replaced, by two independent repaired closures (pole admissibility ord >= -3 vs needed 4; degree ledger deg W~ = 15 vs needed 28), neither using THEOREM 2 or THEOREM 3",
      "label": "[CERTIFIED] (E4, E5)",
      "evidence_path": "canon/TRUST_MAP.md §2; canon/LIVE_MAP.md 'What moved'"
    },
    {
      "claim": "The transfer conjecture is refuted in both halves: D is not the chain degree (D = 15 - 12/beta < 15, so the Second Framework cannot have D = 23), and '3 | D is fatal' is exactly backwards. Replacement proved: m = 4 for every cusp type (2,3) framework, so the endgame has at most one solution and it always has map-degree 4; any framework demanding D_chain != 4 is empty",
      "label": "[CERTIFIED] (E6, 21 checks)",
      "evidence_path": "canon/TRUST_MAP.md §3"
    },
    {
      "claim": "(108,72) closes for all 9 admissible charts: 7 give a unique endgame solution of map-degree 4, 2 (s = 18, 36; D = 12, 9) give no rational solution at all, no chain degree is 4",
      "label": "[CERTIFIED] (EC_10872_instantiation.py, 19 checks)",
      "evidence_path": "canon/TRUST_MAP.md §4; canon/LIVE_MAP.md"
    },
    {
      "claim": "GGV 2013 discards NOTHING at B=16; its Thm 1.2 is an iff and it stalls at deg(q1)=5. GGHV's 'In [4] this case and (80,112) have been discarded' is a sloppy citation — the d=3 cell IS solved there, but d >= 4 was open and lies above 125",
      "label": "chain of custody checked link by link; papers fetched into canon/papers/",
      "evidence_path": "canon/ADJUDICATION.md §2, §3 (last bullet)"
    },
    {
      "claim": "B=16 cells: d=5 EMPTY over Q at char-0 Gröbner proof standard in 22 s (GGV's 2013 PC failed after an hour); d=6 EMPTY over Q char-0 in 135 s. Both plus 3 primes",
      "label": "[PROVED-exact] char-0",
      "evidence_path": "canon/ADJUDICATION.md §2 (Wave 5 table); canon/STATE_FULL.md §A"
    },
    {
      "claim": "The auditor's own chart gauge-fixing was UNSOUND — the claimed scaling symmetry does not exist (the 2*mu3*q1''(0) term in (1.2) row 3 is inhomogeneous under every continuous scaling; both published GGV controls have b2 = 0 so no control exercised it). d=7 both charts and d=12 chart B verdicts DEMOTED to slice results; unreduced d <= 6 char-0 proofs unaffected",
      "label": "self-correction, authoritative",
      "evidence_path": "canon/ADJUDICATION.md §6"
    },
    {
      "claim": "msolve silent-lie mode: a constant generator that is a nonzero multiple of the characteristic makes msolve exit 0 having written '[-1]:' — a parse failure indistinguishable from a genuine EMPTY unless stderr is read. Caught in the act on a seeded d=8 chart-N run that 'returned EMPTY in 20 seconds'. Contamination audit of all 131 .ms files: zero affected, no prior verdict touched. Standing rule: '[-1]' with a parse/read error is a FAILURE, never a verdict",
      "label": "RETRACTION + standing rule",
      "evidence_path": "canon/CATCHES.md 'NEW msolve SILENT-LIE MODE (06:00Z)'"
    },
    {
      "claim": "Multi-start Newton is blind at 25–40 unknowns: planted roots at residual exactly 0 were NOT found (pentagon best 1.9e5 of 3 starts; ladder d=8 best 1.7e3 of 25 starts). All quoted numerical 'empty floors' at d = 8, 9, 12 and the bifurcation residual are RETRACTED as evidence of emptiness",
      "label": "RETRACTION, authoritative (planted controls, wave6/w6_plantctl.py)",
      "evidence_path": "canon/CATCHES.md 'RETRACTION (05:45Z)'"
    },
    {
      "claim": "45 hardcoded-True checks exist in the tree (42 previously unrecorded, 19 in inherited campaign/ certifiers). Two verdicts downgraded: 'L1 boxes immaterial' -> ARGUED (computed premises, uncomputed inference); L2's D=13 -> SOURCE-READ rather than computed",
      "label": "audit finding, downgrades authoritative",
      "evidence_path": "canon/ADJUDICATION.md §1 ('0 rigged checks' row), §4.3"
    },
    {
      "claim": "STATUS §6.7 LEMMA ('solutions are exactly A/(v+1)^k with map-degree exactly k') is REFUTED as stated — false for 3|D with D > 3k, explicit witness R = c/(6(v+1)^2) + (v/(v+1))^2 at (D,k) = (6,1). Immaterial at D = 13, 23 since 3 does not divide either",
      "label": "REFUTED as stated; uses unaffected",
      "evidence_path": "canon/ADJUDICATION.md §1 and §4.2"
    },
    {
      "claim": "Two false-positive 'hits' occurred, both gauge artefacts, both caught before any committed claim: v1 used an absolute stopping test on a system homogeneous of degree -1 in P's scale (Newton drove ||x|| to 1e10, Q collapsed to zero, conditions satisfied vacuously); v2's 1.70e-09 outlier inflated the denominator via the unfixed coordinate-scale gauge",
      "label": "documented false positives + standing requirement for any future detector",
      "evidence_path": "canon/STATUS.md §6.6"
    },
    {
      "claim": "arXiv:2608.00222 (Gao, counterexamples in dimensions > 2) is a real identifier verified through three independent paths, and is NOT load-bearing for the plane case — the paper explicitly disclaims dimension 2",
      "label": "literature spot-check",
      "evidence_path": "canon/STATUS.md §9 (Artifact index preamble)"
    },
    {
      "claim": "'Nguyen 104 is unverified' was retracted — the result is real and refereed; three web searches missed it. Absence from a search is not absence from the literature",
      "label": "self-retraction",
      "evidence_path": "canon/STATUS.md §6.1"
    }
  ],
  "pitfalls": [
    "TIMEOUT and OOM are never EMPTY. The d=8..12 chart-N cells, the 41 above-125 shapes, and the pentagons are all in this class and must not be reported as closed.",
    "mod-p EMPTY is never a char-0 verdict. Case (2) at (72,108), the entire B=16 chart-Z ladder at d >= 7, and the above-125 6-EMPTY set are all mod-p only. Only [PROVED-exact] / [CERTIFIED] count in char 0.",
    "Single-prime results (d=7 ladder, d=9/10/11 chart Z, F3 x2 at 65521) are weaker still and were flagged as MISSes by the campaign itself.",
    "msolve writes '[-1]' and exits 0 on a parse failure. Always read stderr; never trust a filename or a summary line. This produced one fake 20-second EMPTY.",
    "msolve's solve mode and eliminant mode write indistinguishable output — this cost a false 'unblocked' claim that stood five days. Parse the artifact.",
    "All multi-start numerical residual evidence is retracted; a numerical MISS says nothing at these sizes.",
    "Prime hygiene: the campaign's own rule is p = 1 mod 3; two of three CASE2 primes violated it and had to be re-run (verdict survived).",
    "Gauge artefacts produced both false positives. Any pentagon detector must fix all three gauges, use an ABSOLUTE normalization, and make 'allowed coefficients are O(1)' an acceptance condition, not a post-hoc check.",
    "45 hardcoded-True checks exist in the tree; a [PASS] mark inside a docstring is prose, not a computation. Sessions 9, 11, 12–14, 15 and 16–18 archive scripts are print(__doc__) only.",
    "Route 1 / Route 2 are file-level disjoint but both descend from the same GGHV polygon derivation — code disjointness, not full independence.",
    "Do not cite TRUST_MAP's ABSENT verdicts: ADJUDICATION §1 rules them WRONG-TREE (that branch was cut from main; the artifacts exist on the endgame lineage), so every ABSENT verdict there is void even though its self-contained math stands.",
    "Session 15's affine form is derived from THEOREM 3 and must not be used to answer the THEOREM 3 residual — circular.",
    "37+ local commits were UNPUSHED at the time of the record (container credential death), so some results may exist only in chat logs.",
    "pkill -f killed the invoking shell four times; the safe idiom is a pgrep -x loop."
  ],
  "disagreements": [
    "d=7 B=16 ladder: ADJUDICATION.md §2 records d=7 and d=8 as STALLED-OOM (13.9–13.96 GB, 0-byte outputs, explicitly 'NOT a verdict'), while the later STATE_FULL.md §A records d=7 Z+N (sound split) as EMPTY at p = 1000003 and d=8 Z as EMPTY at 2 primes. STATE_FULL is the more recent record and reflects the corrected sound Z/N split from ADJUDICATION §6; the earlier OOM rows describe the pre-split monolithic formulation. Either way d=7 is single-prime and d=8 chart N is undecided.",
    "TRUST_MAP.md §1/§4 mark H1c, the eliminant, the irreducibility sieve, chart coverage, the pentagon system, case (2) over Q-bar, the 167 targets and the 804 pairs as ABSENT from the repository; ADJUDICATION.md §1 rules this WRONG-TREE and voids every ABSENT verdict. Treat ABSENT as void, but note TRUST_MAP's own mathematics (E1–EC) is unaffected.",
    "THEOREM 2/3 status: STATUS.md §2.6 treats THEOREM 2 as certified and THEOREM 3 as confirmed-and-repaired (i.e. needed, then discharged); TRUST_MAP.md §1–§2 says both are simply NOT NEEDED by either repaired closure, and that THEOREM 3's conclusion is false as a hypothesis-free statement (R has a 4th-order pole). These agree on the outcome but disagree on which input is load-bearing.",
    "Second Framework kill mechanism has drifted across sessions: TRUST_MAP §3 kills it via D = 15 - 12/beta; a parallel Opus session claimed D_ode = 69/5; the parallel audit found the kill survives via D_chain = 5*beta/2 - 2 == 3 mod 5 but carries two unsound steps. ADJUDICATION §5 flags this drift explicitly as unaudited and queued.",
    "'(108,72) closed with THEOREM 2 dependence removed' is adjudicated SOUND-BUT-OVERSTATED (ADJUDICATION §7): the removal is real on one leg only; the residual-gap leg rests on an underived beta = 6 input and two can't-fail checks (w3_10872_and_legs_audit.py:110, :125). So the (108,72) closure is strong but not uniformly at the standard STATUS claims.",
    "Two distinct 'eliminants' must not be conflated: the (72,108) case-(2) edge eliminant is degree 1144 and PROVED irreducible over Q (STATUS §2.5, re-verified), whereas the CATCHES.md 05:45Z-era seed/bottom-edge eliminant is stated to be 'definitely NOT irreducible' (~5 factors over Q). Different objects, different systems.",
    "CATCHES.md retraction at line 2032 withdraws the claim that the 'four seeds invisible at p = 1000003' gap was closed: the degenerate count varies (4,4,4,2,4) across five primes and the Galois-orbit structure is not established, so testing one admissible seed may decide only its own orbit. That gap is OPEN.",
    "STATUS.md §2.1 states its H1c closed form for all D, k as [PROVED-exact], but STATUS §6.7 then declares that same file FALSE AS STATED (the k >= 1 branch was never computed; its check() passed a literal True). §6.7 supersedes §2.1; and §6.7's own replacement LEMMA is in turn refuted as stated by ADJUDICATION §1/§4.2 for 3|D, D > 3k."
  ]
}
```
### READER: open-queue
```json
{
  "summary": "The archive documents a campaign against JC2 that produced no counterexample and, on 2026-08-21, invalidated a large share of its own artefacts: GGV's system (1.2) was found misprinted, so every result built on the 'printed' system is void as a statement about B=16 (canon/OPEN_ITEMS.md, header + item 1). Two further self-retractions stand and must not drift: numerical multi-start empty 'floors' are VOID (planted-root controls at 25 and 165 unknowns were not found), and a fast 'd=8 EMPTY' was an msolve parse artefact — msolve writes '[-1]' and exits 0 on a constant generator that is a multiple of the characteristic (canon/MORNING_SUMMARY.md, 'The two RETRACTIONS'). All 131 campaign .ms files were audited; zero were affected. Evidence discipline in the canon matches the caller's rules: timeout/OOM/no-output are failures, never verdicts; mod-p emptiness needs two agreeing primes and is evidence only; exact Q is the proof standard (canon/WEEKEND_PLAN.md, 'Standing rules').\n\nThe live queue has six-to-eight genuinely open compute items. The cheapest and most frontier-adjacent is d=8 chart N on the corrected system: 30 equations / 23 unknowns, already exported as wave5/ms/m16_d8_*.ms, a_16 left free so both roots of the row-0 quadratic are covered in one msolve run, and chart Z eliminated analytically by F2 (mu0 = a2*mu2/3). d<=7 are EMPTY in char 0, so d=8 is the frontier cell. It has never been launched on the corrected export; the four prior d=8 attacks (chart-split, msolve -g 2, unsplit, 16-bit prime) all TIMED OUT with clean stderr on the void printed system. Second is the pentagon truncation ladder: truncate(W) in trackB1_pentagon.py builds a closed subsystem, so an EMPTY truncation kills pentagon case (1) of (72,108) outright — a branch with no verdict by any method anywhere. W=19 is 21 equations in 27 unknowns, the smallest live object in the campaign; it died once in Singular ('no more memory') and once OOM-killed in msolve at this container's 13.3GiB cap. Every pentagon failure to date has been memory, never mathematics.\n\nThe shared blocker across almost everything else is P2: a proper rational-function cascade. Direct Groebner scales roughly 32x per ladder level (measured: d=6 42s, d=7 1345s), which puts d>=8 in char 0 and d=12, 27 out of reach by that route, and the pentagon needs the same machinery to propagate past level 3. Both previously retracted cascades failed at exactly this point.\n\nInfrastructure is the binding constraint and blocks P0/P1 outright: ~13.3GiB cgroup cap, container restarts roughly every 30 minutes (five overnight, twice rolling the git tree back), and a measured hard ceiling of ~2.5h wall before every process is lost. Nothing needing >20 minutes or >12GB can finish here. A fresh container also comes up with no Singular and no msolve — apt-get install them before anything runs.\n\nOne correction to a commonly repeated item: case (2) is NOT merely 'identified' — it is decided EMPTY mod p at three independent primes (65521, 32003, 65537), covering every point of the edge variety. What was never executed is the characteristic-0 confirmation, whose value rose after the modular-unsoundness catch. The rank criterion, the campaign's cheap probe for resonant cells, was shown to be a can't-fail certifier and cannot decide d=27 or anything else.",
  "open_items": [
    {
      "name": "d=8 chart N, corrected system (frontier cell)",
      "status": "OPEN — exported, never launched",
      "run_command": "msolve on wave5/ms/m16_d8_*.ms (regenerate via `python3 wave6/w6_seed_d8.py`); pick a prime where 12*8=96 is a square; capture stderr",
      "solver": "msolve (Groebner/eliminant, mod p first, then char 0)",
      "last_outcome": "no run on the corrected system. Four prior d=8 attacks on the now-VOID printed system: all TIMEOUT with clean stderr",
      "wall_time": "prior printed-system attempts exceeded container uptime (>~30 min each, no completion); corrected system is smaller (30 eq/23 unk vs 39/30) so unknown but expected shorter — inference",
      "needs": "single core saturating msolve, >=32GB RAM, uninterrupted 2-8h; two primes before quoting any EMPTY",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/WEEKEND_PLAN.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MORNING_SUMMARY.md"],
      "blocked_by": "container: 13.3GiB cap, ~30-min restarts, ~2.5h measured process lifetime"
    },
    {
      "name": "Pentagon truncation ladder W=19 (kills pentagon case (1) of (72,108) if EMPTY)",
      "status": "OPEN — ran once, died on memory; converted to msolve, OOM-killed",
      "run_command": "msolve on the export of trackB1_trunc19.json (exporter: trackB1_msolve_export.py, with Rabinowitsch saturation); existing artefacts trackB1_trunc19_p65521.sing/.out",
      "solver": "msolve (previously Singular std/slimgb)",
      "last_outcome": "OOM — Singular 'no more memory'; msolve OOM-killed at the 13.3GiB container cap. Never a mathematical failure",
      "wall_time": "not recorded to completion; killed by the memory cap",
      "needs": ">=32GB RAM (weekend plan states this explicitly), 1 core, hours; then W=18 (40 eqs) and W=17 (60 eqs) as independent confirmations, then a second prime each",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/WEEKEND_PLAN.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/trackB1_trunc19.json", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/trackB1_pentagon.py", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/trackB1_msolve_export.py"],
      "blocked_by": "RAM ceiling (13.3GiB); needs >=32GB machine"
    },
    {
      "name": "Ladder cells d=9,10,11 chart N (seeded, unsplit)",
      "status": "OPEN, undecided",
      "run_command": "export via wave6/w6_seed_d8.py analogue per d, then msolve; primes chosen so 12d is a square",
      "solver": "msolve",
      "last_outcome": "none (never attempted in corrected form); d=8 sibling attempts all TIMEOUT",
      "wall_time": "n/a; direct GB cost scales ~32x per ladder level (d=6 42s, d=7 1345s) — so d=9 is inference-wise far beyond d=8",
      "needs": "24-35 unknowns; uninterrupted hours to days per cell, >=32GB, two primes each",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/WEEKEND_PLAN.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MORNING_SUMMARY.md"],
      "blocked_by": "same container limits; realistically needs the P2 cascade"
    },
    {
      "name": "d=12 chart N + d=12 unsaturated form (resonant cell)",
      "status": "OPEN — not exported on the corrected system",
      "run_command": "export (trivial per OPEN_ITEMS item 2), then msolve; a_{2d} unseeded so both rational roots -1/12 and 1/20 are covered in one run",
      "solver": "msolve",
      "last_outcome": "prior kills were on the printed system — VOID. Unsaturated corrected form EMPTY at d=3,4,5,6 only; d=12 never attempted in that form",
      "wall_time": "no valid timing",
      "needs": "out of reach of direct Groebner; feasible only after the P2 rational-function cascade exists",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"],
      "blocked_by": "P2 cascade not built"
    },
    {
      "name": "d=27 chart N (next resonant cell, 114 eq / 85 unk)",
      "status": "OPEN, untouched",
      "run_command": "no export exists; would follow the same corrected-export path",
      "solver": "msolve (infeasible directly)",
      "last_outcome": "none",
      "wall_time": "n/a",
      "needs": "explicitly out of reach of direct Groebner; requires P2. Rank criterion already known non-decisive here (can't-fail certifier)",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"],
      "blocked_by": "P2 cascade"
    },
    {
      "name": "P2: rational-function cascade (shared blocker)",
      "status": "OPEN — build task, not a solve",
      "run_command": "none exists; both prior cascades were retracted",
      "solver": "n/a (engineering)",
      "last_outcome": "two retracted attempts, both failing at the same point",
      "needs": "developer time rather than cores; unblocks d>=8 char 0, d=12, d=27, and pentagon propagation past level 3",
      "wall_time": "n/a",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"],
      "blocked_by": "nothing but effort"
    },
    {
      "name": "Characteristic-0 confirmation of case (2)",
      "status": "OPEN in char 0; decided EMPTY mod p at 65521, 32003, 65537",
      "run_command": "python3 trackB_exactQ.py (marker-resumable; QELIM_TIMEOUT env, default 10800s); leaf selection via JCLEAF=1",
      "solver": "Singular over Q (eliminant factorization is the long pole), msolve for mod-p controls",
      "last_outcome": "mid-run at last checkpoint; the char-0 edge eliminant factorization never completed. Multiple run logs on disk (trackB_exactQ_run2..runD.log)",
      "wall_time": "6h timeouts configured on fallback charts that the ~2.5h container lifetime can never reach",
      "needs": "a persistent machine with >2.5h uptime, 1-2 cores, large RAM; marker-resumable so it tolerates restarts better than a monolithic GB",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/trackB_exactQ.py", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/trackB_Q_elim.sing", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/RESUME_STATE.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"],
      "blocked_by": "container uptime"
    },
    {
      "name": "(9,27) branch of (72,108): p108_* systems (GGHV Cor 5.7 is UNPROVEN)",
      "status": "OPEN, promoted to first-class after the Cor 5.7 break",
      "run_command": "time-boxed elimination machinery on the p108_* systems; smallest is p108_525122 (25 params, 140 conditions)",
      "solver": "Singular / msolve elimination",
      "last_outcome": "TIMEOUT — p108_525122 timed out at 1800s on a worker",
      "wall_time": "1800s budget exhausted, no verdict",
      "needs": "long uninterrupted runs; alternatively a repair attempt on Cor 5.7 (paper work, no compute) or a direct hunt for a solution of the (9,27) polygon system",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/WEEKEND_PLAN.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MORNING_SUMMARY.md"],
      "blocked_by": "container uptime; no reduction machinery"
    },
    {
      "name": "Rank criterion extension to d=48, then d=75",
      "status": "OPEN but low value",
      "run_command": "wave6/w6_rankcrit_modp.py at d=48 (198 eqs, 143 unknowns), with its d=3 and d=12 controls",
      "solver": "linear algebra mod p (discriminant square root taken mod p)",
      "last_outcome": "exceeded a 520s budget on this container",
      "wall_time": ">520s, killed",
      "needs": "modest — a machine that stays up for an hour. But the criterion was shown to be a can't-fail certifier, so a pass decides nothing",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/WEEKEND_PLAN.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"],
      "blocked_by": "nothing technically; blocked by its own uselessness as a certifier"
    },
    {
      "name": "Above-125 frontier: 429 cases + tail-closure/saturation test",
      "status": "OPEN, large; the only home for a B>20 counterexample",
      "run_command": "chain-compiler extension does not exist; tail-closure predictor test (last-2-segments + shape index -> system hash) is the tractable first step",
      "solver": "n/a — compiler/engineering",
      "last_outcome": "none; also blocked because above-125 Newton polygons are published nowhere (1708.07936 §6 gives chain data only; GGHV 2204.14178 §4 gives polygons only for (9,27),(9,24),(8,28),(7,21), hand-derived with no general recipe)",
      "wall_time": "n/a",
      "needs": "engineering, not cores, until the compiler exists",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/WEEKEND_PLAN.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/RESUME_STATE.md"],
      "blocked_by": "missing polygon data + missing compiler"
    },
    {
      "name": "41 undecided timeout shapes",
      "status": "OPEN, untouched",
      "run_command": "no driver named in the canon; weekend plan says sweep smallest-first",
      "solver": "elimination (Singular/msolve)",
      "last_outcome": "timeouts (which are not EMPTY)",
      "wall_time": "unrecorded per shape",
      "needs": "a smallest-first sweep on a persistent machine; cheap per shape at the small end",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"],
      "blocked_by": "container uptime; no sweep driver written"
    },
    {
      "name": "Track C item C3 (ladder)",
      "status": "OPEN — script never written",
      "run_command": "trackC_phase4.py c3 (imports trackC_c3_ladder.py and fails until it exists)",
      "solver": "python/sympy",
      "last_outcome": "never started; import error",
      "wall_time": "n/a",
      "needs": "trivial compute, small dev effort",
      "files": ["/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/RESUME_STATE.md", "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/pq/trackC_phase4.py"],
      "blocked_by": "missing file"
    }
  ],
  "ranking": [
    {"name": "Pentagon truncation ladder W=19", "rank": 1, "reason": "INFERENCE. Highest HIT-chance per compute-hour: 21 eqs / 27 vars is the smallest live object in the campaign, and case (1) of (72,108) has never had a verdict by ANY method — so both outcomes are new. A NON-EMPTY yields an actual counterexample candidate on (72,108) via exact substitution then wave6/w6_bijcheck.py. Every failure so far was memory, not mathematics, so a >=32GB machine plausibly finishes it in hours."},
    {"name": "d=8 chart N corrected system", "rank": 2, "reason": "INFERENCE. Cheapest genuinely new result and the canon's own P1: 30 eq / 23 unk, already exported, one run covers both roots and the only surviving chart. Slightly below the pentagon on HIT-chance because every exact structural result (rank obstruction at d=3..15,18,20,27; the growing ~d excess of conditions over unknowns) points to EMPTY, but its cost per unit of new information is the lowest in the queue."},
    {"name": "(9,27) p108_* systems, smallest first (p108_525122)", "rank": 3, "reason": "INFERENCE. Genuinely live because GGHV Cor 5.7 — the only thing in print killing this branch — was found unproven; nothing in the literature excludes a solution here. Timed out at 1800s, so a longer box is a plausible finish. Costlier per hour than ranks 1-2 (25 params / 140 conditions)."},
    {"name": "Characteristic-0 confirmation of case (2)", "rank": 4, "reason": "INFERENCE. Near-zero HIT probability (already EMPTY at three primes) but high evidential value per hour: it converts modular evidence into a char-0 proof on one of only two shapes of the last surviving pair below 125, and it is marker-resumable so restarts cost a stage rather than the run."},
    {"name": "41 timeout shapes, smallest-first sweep", "rank": 5, "reason": "INFERENCE. Never swept smallest-first; the small end is cheap and each shape is an independent lottery ticket. Ranked below the above because no driver exists and the sizes are unrecorded."},
    {"name": "P2 rational-function cascade (build)", "rank": 6, "reason": "INFERENCE. Zero direct HIT chance but it is the single shared blocker on d>=8 char 0, d=12, d=27 and pentagon propagation; its expected value is entirely in unblocking ranks 1-2 and 7-8. Ranked here only because it consumes dev time, not compute-hours."},
    {"name": "d=9,10,11 chart N", "rank": 7, "reason": "INFERENCE. Same character as d=8 but ~32x more expensive per level, so HIT-per-compute-hour falls off a cliff; not worth launching before P2."},
    {"name": "d=12 chart N and d=12 unsaturated", "rank": 8, "reason": "INFERENCE. Resonant cell with both roots rational (-1/12, 1/20) and 12d=144 a square, which is where the resonance law says degeneration is most likely — so per-run HIT chance is above the generic cells — but it is explicitly out of reach of direct Groebner, making per-hour value low until P2 lands."},
    {"name": "Above-125 frontier / tail saturation test", "rank": 9, "reason": "INFERENCE. If B=16 closes, this is the ONLY place a counterexample can live, so long-run value is highest of all — but the polygons are unpublished and the compiler unwritten, so near-term HIT-per-compute-hour is effectively zero."},
    {"name": "d=27 chart N", "rank": 10, "reason": "INFERENCE. Resonant and untouched, but 114 eq / 85 unk and explicitly beyond direct Groebner; the cheap probe (rank criterion) is known unable to decide it."},
    {"name": "Rank criterion at d=48 / d=75", "rank": 11, "reason": "INFERENCE. Cheap, but the criterion was shown to be a can't-fail certifier — it cannot decide anything, so its HIT yield per hour is zero regardless of cost. Only a BIFURCATION_POSSIBLE=true would matter, and the structure says it cannot occur."},
    {"name": "Track C C3 ladder", "rank": 12, "reason": "INFERENCE. Housekeeping; no counterexample pathway."}
  ],
  "facts": [
    {"claim": "GGV's system (1.2) was found misprinted on 2026-08-21; every artefact built on the printed system is void as a statement about B=16.", "label": "[PROVED-exact] (hand re-derivation)", "evidence_path": "wt/canon/OPEN_ITEMS.md, header"},
    {"claim": "d <= 7 chart N are EMPTY in characteristic zero; d=8 is the frontier cell.", "label": "[PROVED-exact]", "evidence_path": "wt/canon/OPEN_ITEMS.md §1"},
    {"claim": "d=8 corrected export is 30 equations / 23 unknowns (was 39/30); a_16 is left FREE so one msolve run covers both roots of the row-0 quadratic; F2 (mu0 = a2*mu2/3) proves chart Z contains no counterexample, so chart N is the only chart.", "label": "[PROVED-exact]", "evidence_path": "wt/canon/OPEN_ITEMS.md §1"},
    {"claim": "At d=12 the row-0 quadratic 90a^2+3a-3/8 has roots exactly -1/12 and 1/20, and 12*12=144=12^2, so d=12 is a resonant cell.", "label": "[PROVED-exact]", "evidence_path": "wt/canon/OPEN_ITEMS.md §2"},
    {"claim": "The corrected UNSATURATED system (mu0 free, mu2 gauged to 1) is EMPTY at d=3,4,5,6 — strictly stronger than 'no solution with mu0 != 0'. d=12 not attempted in that form.", "label": "[PROVED-exact] for d=3..6; OPEN at d=12", "evidence_path": "wt/canon/OPEN_ITEMS.md §3"},
    {"claim": "d=27 is resonant (12*27=324=18^2, roots -1/20 and 1/28 both rational), 114 equations / 85 unknowns in corrected form, and out of reach of direct Groebner.", "label": "[PROVED-exact] (sizes/resonance); reachability is an engineering fact", "evidence_path": "wt/canon/OPEN_ITEMS.md §4"},
    {"claim": "Case (2) admits no realization with its stated Newton polygons — complete and certified at three independent primes 65521, 32003, 65537, covering every point of the edge variety at each. The characteristic-0 confirmation was never executed.", "label": "[CERTIFIED mod p, three primes] — NOT char 0", "evidence_path": "wt/canon/OPEN_ITEMS.md §5 (quoting campaign/audit_tracks/CASE2_VERDICT.md)"},
    {"claim": "The rank criterion is a can't-fail certifier: it cannot decide d=27 or anything else.", "label": "[PROVED-exact]", "evidence_path": "wt/canon/OPEN_ITEMS.md §4"},
    {"claim": "Rank criterion at quasi-homogeneous points, d=3..15,18,20,27, both roots: augmented rank exceeds plain rank by exactly one — ALWAYS OBSTRUCTED (d=27: 53->54, 107 eqs, 80 unknowns; d=18: 35->36; d=20: 39->40).", "label": "[PROVED-exact] but see the can't-fail caveat above", "evidence_path": "wt/canon/MORNING_SUMMARY.md, 'What is now DECIDED'"},
    {"claim": "Direct Groebner scales ~32x per ladder level: d=6 took 42 s, d=7 took 1345 s.", "label": "measured timing", "evidence_path": "wt/canon/OPEN_ITEMS.md, THE PLAN, P2"},
    {"claim": "truncate(W) in trackB1_pentagon.py builds a CLOSED subsystem — every full solution restricts to a truncation solution — so an EMPTY truncation kills pentagon case (1) of (72,108) outright.", "label": "[PROVED-exact] structural", "evidence_path": "wt/canon/WEEKEND_PLAN.md §P0"},
    {"claim": "W=19 is 21 equations in 27 unknowns, the smallest live object in the campaign; it died once in Singular with 'no more memory' and once OOM-killed in msolve at the 13.3GiB cap. Every pentagon failure has been MEMORY, never mathematics.", "label": "OOM (a failure, not a verdict)", "evidence_path": "wt/canon/WEEKEND_PLAN.md §P0"},
    {"claim": "Numerical multi-start is BLIND at >=25 unknowns: planted roots with residual exactly 0.0 were not found at 25 (d=8) or 165 (pentagon) unknowns. The 1e-10 'empty floors' at d=8/9/12 measured the SOLVER, not emptiness — RETRACTED.", "label": "RETRACTION, control-backed", "evidence_path": "wt/canon/MORNING_SUMMARY.md, 'The two RETRACTIONS' #1"},
    {"claim": "msolve refuses to parse a constant generator that is a nonzero multiple of the characteristic, then EXITS 0 after writing '[-1]'. A fast 'd=8 EMPTY' was this artefact — RETRACTED. All 131 campaign .ms files were scanned; ZERO affected.", "label": "RETRACTION + audit", "evidence_path": "wt/canon/MORNING_SUMMARY.md, 'The two RETRACTIONS' #2; wt/canon/WEEKEND_PLAN.md §P0 guard 3"},
    {"claim": "GGHV Cor 5.7 is UNPROVEN: the proof of (5.12) applies [1, Cor 7.2] (standing hypothesis [P,Q] in K^x) to (psi phi P, psi phi Q), whose bracket is 1/2 + (lambda/2)x^{-1/2}, not in K^x, with lambda != 0 forced by (0,18) in N(P). Of the 66 coefficient conditions (5.12) asserts, the proven claim delivers 15. Failure localized to gghv.txt:1430-1433.", "label": "[PROVED-exact] hand verification of a literature gap", "evidence_path": "wt/canon/WEEKEND_PLAN.md §P3; wt/canon/MORNING_SUMMARY.md, 'Recommended next moves' #2"},
    {"claim": "Consequence: the live region below max 125 is BOTH orientations of (72,108); the p108_* (9,27) systems are first-class compute targets, smallest being p108_525122 (25 params, 140 conditions), which TIMED OUT at 1800s.", "label": "TIMEOUT (not EMPTY)", "evidence_path": "wt/canon/WEEKEND_PLAN.md §P3; wt/canon/MORNING_SUMMARY.md, 'What is UNDECIDED'"},
    {"claim": "d=8 was attacked in four formulations (chart-split, GB-only via msolve -g 2, unsplit, 16-bit prime) — all TIMEOUT with clean stderr, on the (now void) printed system.", "label": "TIMEOUT (not EMPTY)", "evidence_path": "wt/canon/MORNING_SUMMARY.md, 'What is UNDECIDED'"},
    {"claim": "Prime size is irrelevant to cost here — 16-bit bought nothing; the bottleneck is Groebner structure, not coefficient arithmetic.", "label": "measured", "evidence_path": "wt/canon/MORNING_SUMMARY.md, 'Two structural wins'"},
    {"claim": "Seeding the row-0 root covers the WHOLE cell (the relation is mu-free), so the Z/N chart split is unnecessary work; roots are irrational (sqrt(12d)), so mod-p work needs primes where 12d is a square.", "label": "[PROVED-exact]", "evidence_path": "wt/canon/MORNING_SUMMARY.md, 'Two structural wins'; wt/canon/WEEKEND_PLAN.md §P1"},
    {"claim": "Container: ~13.3GiB cgroup cap, restarts roughly every 30 minutes (five overnight, twice rolling the git tree back); nothing needing >20 min or >12GB can finish. P0 and P1 are blocked on this.", "label": "measured infrastructure", "evidence_path": "wt/canon/WEEKEND_PLAN.md, 'Infrastructure'; wt/canon/MORNING_SUMMARY.md, 'Infrastructure reality'"},
    {"claim": "Measured process lifetime ceiling is ~2.5 hours of wall time with the root filesystem intact; the exact-Q fallback charts carry a 6h timeout they can never reach.", "label": "measured", "evidence_path": "wt/pq/RESUME_STATE.md, 'Container lifetime is the binding constraint'"},
    {"claim": "A fresh container comes up with NO Singular and no msolve; every campaign script assumes Singular on PATH. apt-get install -y singular (4.3.2) and msolve. After a restart (not a fresh container) both survive.", "label": "measured environment gotcha", "evidence_path": "wt/pq/RESUME_STATE.md, 'Environment gotcha'"},
    {"claim": "Pentagon T2/T4 stalled measurably: one sample's level 16 does not finish in 1400s at 1.8GB with 9 levels still below it. T5 engines both lost — slimgb 2x slower than std; msolve dies in hash-table growth.", "label": "TIMEOUT/OOM (not verdicts)", "evidence_path": "wt/pq/RESUME_STATE.md, queue table P0"},
    {"claim": "Above-125 Newton polygons are published nowhere: 1708.07936 §6 gives chain data only; GGHV 2204.14178 §4 gives polygons only for (9,27), (9,24), (8,28), (7,21), derived case-by-case by hand with no general recipe.", "label": "literature audit", "evidence_path": "wt/pq/RESUME_STATE.md, queue table P3"},
    {"claim": "The tail-closure predictor (last-2-segments + shape index -> system hash) has zero violations across every system this campaign ever generated; if tails saturate, the 429-case frontier collapses to finitely many systems.", "label": "empirical, no proof of saturation", "evidence_path": "wt/canon/WEEKEND_PLAN.md §P4"},
    {"claim": "The dimension-3 refutation (Alpoge/Gallagher, July 2026) realizes every geometric degree, killing degree-bound approaches to JC in general; this raises the importance of the 429-case above-125 frontier.", "label": "literature (as recorded in the archive)", "evidence_path": "wt/canon/OPEN_ITEMS.md §6"},
    {"claim": "run_all.sh runs archive re-runs (certifiers/rerun/S*.py, 1800s timeout each) and new certifiers (certifiers/new/E*.py at 3600s, E*.gp via gp -q -f at 3600s), logging PASS/FAIL per file and exiting nonzero if any fails.", "label": "code read", "evidence_path": "wt/canon/run_all.sh"},
    {"claim": "Case (2) leaf-2 branch verdicts mod 65521: r1-r6, r0a, r0b all EMPTY (fully closed at that prime); mod 65539 rk0-rk4 and r0a EMPTY with r0b paused mid-stage; p65599 sweep not started at that checkpoint.", "label": "[CERTIFIED mod p] at 65521; partial at 65539 — NOT char 0", "evidence_path": "wt/pq/RESUME_STATE.md, 'PAUSE POINT' scoreboard"}
  ],
  "pitfalls": [
    "Timeout, OOM and no-output are FAILURES, never verdicts. Four d=8 timeouts and a p108_525122 1800s timeout must never be reported as EMPTY (wt/canon/WEEKEND_PLAN.md standing rule 3).",
    "msolve writes '[-1]' and exits 0 on a parse error — a parse failure wearing an EMPTY verdict's clothes. ALWAYS capture and read stderr; reject any input carrying a constant generator (wt/canon/WEEKEND_PLAN.md §P0 guard 3).",
    "Mod-p emptiness is unsound for contradictions. Three agreeing primes is strong evidence, not a proof. An EMPTY needs at least two agreeing primes before it is even quoted, and char 0 before it is called proved (wt/canon/OPEN_ITEMS.md §5).",
    "Everything built on the PRINTED GGV (1.2) is void — this includes the earlier d=12 kills, the d=8 b16_d8_*.ms exports, and the d=12 'two rational seeds' bookkeeping. Only corrected-system (m16_*) artefacts count (wt/canon/OPEN_ITEMS.md header).",
    "Numerical multi-start is blind at >=25 unknowns. A hit would be real; a miss says nothing. Never quote a numerical floor as emptiness (wt/canon/MORNING_SUMMARY.md retraction 1).",
    "The rank criterion cannot fail, so its 'ALWAYS OBSTRUCTED' verdicts at d=3..27 are not evidence of emptiness; do not let them drift into 'probably empty' prose (wt/canon/OPEN_ITEMS.md §4).",
    "Do not schedule monolithic Groebner runs on this container: ~2.5h process lifetime, ~30-min restarts, 13.3GiB cap, and the git tree has rolled back twice. Prefer marker-resumable per-branch pipelines (the staged/exactQ route); push after every commit (wt/pq/RESUME_STATE.md; wt/canon/WEEKEND_PLAN.md rule 5).",
    "A fresh container has no Singular and no msolve; scripts fail silently in the sense that no engine is present until apt-get installs them (wt/pq/RESUME_STATE.md).",
    "The Z/N chart split is unnecessary work on the corrected export and only adds a saturation variable — do not resurrect it (wt/canon/MORNING_SUMMARY.md).",
    "Prime size does not buy speed here; do not spend effort on 16-bit vs larger primes. But DO pick primes where 12d is a square, since the row-0 roots are sqrt(12d)-irrational (wt/canon/MORNING_SUMMARY.md).",
    "Every method needs a positive AND a negative control before its output counts; any claimed rank result must reproduce from wave6/w6_rankcrit_modp.py with its d=3 and d=12 controls passing (wt/canon/WEEKEND_PLAN.md).",
    "trackC_phase4.py's c3 subcommand imports trackC_c3_ladder.py, which was never written — it will fail on invocation (wt/pq/RESUME_STATE.md P4).",
    "The deliverable is explicitly NOT 'counterexample or bust'; a counterexample may not exist, and the exact evidence points to B=16 being rigid. Undecided items must stay labelled undecided (wt/canon/WEEKEND_PLAN.md Framing)."
  ],
  "disagreements": [
    "OPEN_ITEMS.md §5 explicitly CORRECTS an earlier claim that 'the case-(2) over Q route was identified but never executed': case (2) IS decided mod p at three primes; only the char-0 confirmation is open. Any downstream summary repeating the old phrasing is wrong.",
    "OPEN_ITEMS.md §2 marks the d=12 'TWO rational seeds, -1/12 and 1/20' item as verified-but-SUPERSEDED (a_{2d} is unseeded on the corrected export, so one run covers both roots), while WEEKEND_PLAN.md §P1 still describes seeding a root per cell. The corrected-export description in OPEN_ITEMS is the later and governing one.",
    "MORNING_SUMMARY.md lists rank-criterion results at d=3..15,18,20,27 under 'What is now DECIDED (exact, control-backed)' and calls d=27 'the decisive one'; OPEN_ITEMS.md §4 (same day, later) states the rank criterion was shown to be a can't-fail certifier that 'cannot decide d = 27 or anything else'. These are in direct tension; the later OPEN_ITEMS reading should govern, and no emptiness should be inferred from rank results.",
    "WEEKEND_PLAN.md §P2 proposes extending the rank criterion to d=48 and d=75 as a priority with 'BIFURCATION_POSSIBLE=true' as a candidate signal; OPEN_ITEMS.md's can't-fail finding makes that extension near-worthless. Ranked accordingly (rank 11).",
    "OPEN_ITEMS.md §1 names the ready d=8 export as wave5/ms/m16_d8_*.ms, while WEEKEND_PLAN.md §P1 and MORNING_SUMMARY.md point to wave6/w6_seed_d8.py as the generator. Not necessarily contradictory (generator vs output), but the exact path of the corrected, launch-ready export should be re-confirmed on disk before launching.",
    "RESUME_STATE.md (2026-08-13) predates the 2026-08-21 correction and the Cor 5.7 break by eight days; its scoreboard, priorities and 'sole open pair below 125' framing are superseded by the canon files wherever they conflict.",
    "RESUME_STATE.md records 'Track A' finding that Sol(case 2) = Sol(leaf 2), so closing leaf 2 closes case (2); it also notes the earlier campaign's entire r0-r6 hunt lived in leaf 1 via an UNSOUND R1 that dropped the sibling at the first fork. Any inherited leaf-1 result should be treated as unverified beyond edge numbers.",
    "The archive contains no README.md in the pq directory; RESUME_STATE.md was used as the queue-like document, and NIGHT_PLAN.md / OPUS_PLAN.md / FABLE_DECISIONS.md were not read within the speed budget — they may carry further queue items or corrections not reflected here."
  ]
}
```
### READER: catches
```json
{
  "summary": "The archive documents a multi-month, multi-session automated campaign to find a plane Jacobian (JC2) counterexample. No counterexample was found; the HIT protocol was never invoked because nothing reached it (canon/LIVE_MAP.md:83, canon/L4_ENDGAME_REPORT.md:349). The dominant output of the campaign is not mathematics but a catalogue of its own failure modes, consolidated in canon/CATCHES.md and errors/FAILURE_ANALYSIS.md. Three root mechanisms are named in errors/FAILURE_ANALYSIS.md: M1 confirmation-shaped verification (checks written after the conclusion, e.g. literal `check(..., True, ...)`), M2 proxy trust (a filename, summary, or process-name pattern substituted for the artifact itself), and M3 quantifier-scope drift (a theorem proved under an implicit hypothesis and recorded without it). canon/CATCHES.md adds nine operational classes (i)-(ix): believed-launched-but-never-launched, silently killed runs, coverage believed complete, double-counted verdicts, can't-fail certifiers, single-prime verdicts quoted as decided, convention/orientation errors, unverified literature steps, and policy without an enforcer. The two most expensive individual errors are both transcription/provenance failures: GGV Theorem 1.2 row 3 is misprinted in the source (-2*mu3*q1''(0) spurious), was transcribed faithfully, and silently made every B=16 emptiness verdict a statement about a proper subvariety V_campaign, not about B=16 — voiding two months of results; and GGHV Corollary 5.7, which the campaign imported as a published kill of the (9,27) orientation of (72,108), is shown to have an invalid step (its bracket leaves K^x after translation), reopening a region assumed dead. Both were undetectable by the campaign's controls because both published worked examples had q1''(0)=0 — a control suite structurally incapable of failing. Infrastructure classes are equally represented: msolve writes '[-1]' (=EMPTY) to its output file and exits 0 on a parse error, so a parse failure is indistinguishable from a verdict unless stderr/stdout is read; timeouts, segfaults on memory caps, and disk exhaustion all leave empty output files that must never be read as verdicts; mod-p elimination can close a branch with a genuine rational solution (z=7y dies mod 7); multi-start Newton is blind at >=25 unknowns, voiding all 'empty floor' numerical evidence; and a Chebotarev-style structure claim was announced off five primes and retracted by the sixth. Three cascade tools and two watchers were written that could not fail; all were caught by self-tests or negative controls rather than downstream.",
  "error_classes": [
    {"n": 1, "name": "Printed-vs-actual source mismatch (transcription verified only against the source's own examples)", "instance": "GGV Thm 1.2 / (3.6) row 3 prints mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0); truth is -6*mu1. Transcribed faithfully into wave5/w5_b16_abel.py. Result: V_campaign = V_true ∩ ({mu3=0} ∪ {q1''(0)=0}); every B=16 EMPTY verdict, all d, both charts, both seeds, all primes, VOID as a statement about B=16.", "file": "canon/CATCHES.md (section 'GGV (1.2) ROW 3 IS MIS-PRINTED')", "guardrail": "For every transcribed equation, list its terms and name, per term, the control that dies if that term is deleted; a term with no such control is UNVERIFIED regardless of how many controls pass."},
    {"n": 2, "name": "Unverified literature step treated as a kill (inherited assumption)", "instance": "GGHV Corollary 5.7 was carried for weeks as the sole citation killing the (9,27) orientation of (72,108). Line-by-line audit found step (5.12) invalid: [psi phi P, psi phi Q] = 1/2 + (lambda/2)x^{-1/2} is not in K^x, so [1, Cor 7.2] does not apply; 51 of 66 needed conditions are unsupported. (9,27) reopened.", "file": "canon/CATCHES.md (section 'GGHV COROLLARY 5.7 IS UNPROVEN'), gghv.txt:1412-1416, :1430-1433", "guardrail": "Every load-bearing literature step must be re-derived locally or labelled UNVERIFIED-HERE; a published kill may never be imported into a triage table without a re-derivation record."},
    {"n": 3, "name": "Provenance assumption — unprinted hypothesis attributed to a source", "instance": "Reference [5] assumes A'_t = (1,0) without printing it; carried in the ledger as a literature fact.", "file": "canon/CATCHES.md (Sec 1, 'Literature' row)", "guardrail": "Anchor-by-exact-quotation: every load-bearing sentence located by exact substring match against the file on disk; a missing anchor fails the run (wave2/w2_pole_admissibility.py)."},
    {"n": 4, "name": "Can't-fail certifier (compile-time-constant check)", "instance": "w1_h1c_endgame_closed_form.py:89 `check(\"k >= 1 forces c = 0...\", True, ...)` — the condition is a literal True; plus two more at w1_h1e_d_crossfire.py:58,:88. 45+22 such checks found campaign-wide.", "file": "errors/STATUS_CORRECTION.md items 2-3; canon/CATCHES.md Sec 1 'Opus's (adjudicated)'", "guardrail": "AST scan of the whole tree rejecting any compile-time-constant check condition (wave2/w2_cantfail_audit.py), itself self-tested on a synthetic rigged/honest pair."},
    {"n": 5, "name": "Can't-fail certifier (structurally vacuous test)", "instance": "The rank/bifurcation criterion reported 'obstructed at every d' for d=3..27 as headline DECIDED evidence. It cannot return anything else: the system contains 6*mu0 - 2*a2*mu2 = 0 and a2 = mu2 = 0 at the quasi-homogeneous point, so dmu0 = 0 is forced for every d. Downgraded from evidence to bookkeeping.", "file": "canon/CATCHES.md (section 'THE RANK / BIFURCATION CRITERION IS A CAN'T-FAIL CERTIFIER'); BIFURCATION.md; MORNING_SUMMARY.md", "guardrail": "Before running any first-order test, ask what it reports if the tested quantity is a product of two functions vanishing at the base point; if that equals the expected answer, the test is vacuous."},
    {"n": 6, "name": "Can't-fail tooling (values computed but never propagated)", "instance": "wave6/w6_pent_cascade2.py solves each level but never writes solved values back into `known`, so every equation classifies as nonlinear and it reports '0 conditions, 0 contradictions' at every level, against a deficit of 118.", "file": "canon/CATCHES.md (section 'TWO BUGS IN MY OWN PENTAGON CASCADE'), wave6/w6_pent_cascade2.py", "guardrail": "A cascade reporting no constraints at every level on an overdetermined system is not computing; assert that solved values are read downstream before any verdict is read."},
    {"n": 7, "name": "Manufactured contradiction (implicit specialisation of undetermined variables)", "instance": "wave6/w6_pent_levelcascade.py reported 'LEVEL 2 IS INCONSISTENT -> THIS SEED DIES'. Artifact: monomials of degree 0 in the fresh unknowns but containing an undetermined non-fresh variable were added to the constant column, i.e. silently set to 1. Retracted. Third attempt (w6_ratcascade.py) reported 57 dead branches on a system with an obvious solution (a=3,b=4,c=2) and was caught by its own two-sided self-test before use.", "file": "canon/CATCHES.md (sections 'TWO BUGS IN MY OWN PENTAGON CASCADE', 'CASCADE ATTEMPT #3 ALSO FAILS')", "guardrail": "Every branch-and-reduce tool must pass a two-sided self-test: a planted-solution system must stay OPEN and a planted contradiction must CLOSE; ship it as a failing tool rather than delete it."},
    {"n": 8, "name": "Mod-p result treated as characteristic-0 (unsound modular contradiction)", "instance": "trackA_eliminator.py --mod p closes branches with genuine rational solutions: x-3y=0, x+4y-z=0 with nonzero=[y,z] has solution (3,1,7) over Q but '1 closed, 0 open leaves' mod 7, and --verify replays it OK, exit 0. Four W=10..13 runs were made with --mod 65521.", "file": "canon/CATCHES.md (section 'MODULAR ELIMINATION IS UNSOUND FOR CONTRADICTIONS')", "guardrail": "Any contradiction/emptiness claim must come from an exact run (meta.mod == null) or be labelled single-prime; mod-p verdicts require a second prime plus a char-0 lift before they enter the record."},
    {"n": 9, "name": "Single-prime verdict quoted as decided", "instance": "'Exactly one admissible bottom-edge seed' was carried as a statement about the problem; it was a statement about p=1000003, where only 5 of the degree-9 eliminant's 9 roots are F_p-rational. d9-11 Z and the F3 pair are likewise single-prime.", "file": "canon/CATCHES.md (sections 'THE SEED WORK IS THREE JOBS, NOT ONE', Sec 3(vi))", "guardrail": "Every verdict record carries its prime list; any statement quantifying over the problem (not the prime) fails lint unless >=2 primes plus a char-0 lift are attached."},
    {"n": 10, "name": "Parse error written as EMPTY (msolve silent-lie mode)", "instance": "A constant generator that is a nonzero multiple of the characteristic makes msolve print a parse error, write '[-1]:' to the -o file, and exit 0. A seeded d=8 chart-N run 'returned EMPTY at both roots in 20 seconds' on a cell that had defeated 90 minutes unseeded. Reproduced a second time from the other direction when a linear reducer's unreduced sympy coefficients hit 1577793733367 = 1000003*1577789.", "file": "canon/CATCHES.md (sections 'NEW msolve SILENT-LIE MODE', 'ADDENDUM: my own linear reducer reproduced the morning's msolve coefficient trap')", "guardrail": "Every msolve invocation captures stderr AND stdout; a '[-1]' accompanied by any parse/read error is a FAILURE, never a verdict; exports reduce every coefficient mod p, drop vanishing rows, and raise on a nonzero constant generator."},
    {"n": 11, "name": "Timeout / crash / OOM treated as a verdict", "instance": "Job #1 (267 eq/148 unk pentagon) hit its 5400 s timeout with a 0-byte output and exit 124; job #2 segfaulted twice on 3.5 and 5.0 GiB address-space caps, also 0-byte. All classified NO-VERDICT. Earlier a bridge msolve CRASHED at 43 s = failure-not-verdict. 49 TIMEOUT records existed campaign-wide.", "file": "canon/CATCHES.md (sections 'JOB #1 TIMED OUT: NO VERDICT', 'JOB #2 DIED ON ITS MEMORY CAP', Sec 2.6)", "guardrail": "A verdict may be read ONLY from a non-empty output file; msolve exits 0 on timeout, crash and parse error, so exit codes are ignored entirely."},
    {"n": 12, "name": "Loose-regex watcher / false-alarm machine", "instance": "A watcher regex fired on the apostrophe in \"'contra': 0\" and produced four fake kill signals. Related: enforcer v1 matched the bash wrapper PID (3 MB) instead of msolve (7.4 GB), so it would have 'protected' the wrong process.", "file": "canon/CATCHES.md (sections 'WATCHER FOR THE TWO PENTAGON RUNS', Sec 1 'Enforcer v1 grabbed bash wrapper PID')", "guardrail": "Every watchdog must pass a synthetic can-fail suite (fires on a synthetic hit, silent on a synthetic non-verdict) and must log a value that would differ if it watched the wrong thing."},
    {"n": 13, "name": "Numerical miss read as evidence of emptiness", "instance": "Planted-root controls: pentagon (165 unknowns) and ladder d=8 (25 unknowns) with a root at residual exactly 0.0 were NOT found by multi-start Newton (best 1.9e5 and 1.7e3). The quoted floors d=8 1.2e-10, d=9 1.4e-10, d=12 1.6e-10 measure the solver, not emptiness. Retracted, along with the 1.6e-3 bifurcation residual.", "file": "canon/CATCHES.md (section 'RETRACTION (05:45Z)'); wave6/w6_plantctl.py", "guardrail": "Numerical lanes are opportunistic finders only: a hit is real, a miss is zero information; every numerical search must carry a planted-root control at the same problem size before its output is cited."},
    {"n": 14, "name": "Gauge non-fixing / unsound gauge, and its mirror (a sound gauge discarded)", "instance": "Unsound scaling gauge charts claimed a symmetry killed by the 2*mu3*q1''(0) term. Mirror error: the exact torus gauge was DISCARDED on the grounds that that same (misprinted) term 'breaks every continuous torus' — measured torus rank is 1 on the corrected system and 0 on the printed one. Contrast the sound pentagon torus gauge (s_4_8 forced nonzero by w1*s_4_8=1, so every orbit meets {s_4_8=1}).", "file": "canon/CATCHES.md (Sec 1 'Unsound gauge charts'; 'SECOND-ORDER DAMAGE'; 'PENTAGON TRUNCATION'; ADJUDICATION.md Sec 6, w5_b16_reduce.py:40-44)", "guardrail": "A gauge is admissible only with a proof that every orbit meets the slice (a forced-nonzero variable of nonzero weight); every gauge decision records the exact torus rank it was computed from."},
    {"n": 15, "name": "Wrong truncation level — an ansatz that cannot deliver the result by construction", "instance": "The pentagon truncation ladder was run for two weeks at W=19, which is UNDERDETERMINED by 6 and therefore almost certainly non-empty; msolve's default parametrisation mode needs dimension 0, which is why it OOM'd. trackA_eliminator.py had been run on W=17,18,19 only — the same targeting error one layer down.", "file": "canon/CATCHES.md (sections 'PENTAGON TRUNCATION', 'FOUND IN PLAIN SIGHT')", "guardrail": "Compute eqs-vs-vars excess before launching any emptiness run; a non-positive excess makes emptiness unreachable and the run must not start."},
    {"n": 16, "name": "Search vacuous by a known theorem (no pre-flight degree gate)", "instance": "The plane-sweep shape search (1728 shapes) produced maps of total degree <= ~32; Moh proved JC2 for degree <= 100, so a negative result carried exactly zero information. Killed mid-run. Related: the whole P0 truncation plan was withdrawn as futile after trackB1_pentagon.py:432 witness() — already in the repo, its docstring saying so — certified every truncation W=12..19 non-empty over Q.", "file": "canon/CATCHES.md (sections 'TWO CATCHES ON MY OWN PLANE-SWEEP SEARCH', 'P0 IS FUTILE')", "guardrail": "Pre-flight gate on every counterexample ansatz: max total degree > 100 (Moh), gcd(deg P, deg Q) = 16 or > 20 (GGV), and below max 125 only (72,108) in both orientations (GGHV as amended); plus read the docstrings and meta of every artifact the plan depends on before launching."},
    {"n": 17, "name": "Vacuous bound / no-op sentinel misread as a result", "instance": "Degree-bounded Singular runs on eliminator-reduced systems reported 'no constant at degBound 4/5' — vacuous, because the inputs' own max degree was 23 so no reduction happened. The tell was gbsize exactly equal to the number of input equations (97 in, 97 out). Earlier, `option(degBound,D)` is not Singular syntax and errored silently, so the first runs were unbounded and 'passed' two trivial controls.", "file": "canon/CATCHES.md (sections 'THE ELIMINATOR'S REDUCTION IS A TRAP', 'THE DEGREE-BOUNDED TEST')", "guardrail": "A degree-bounded result is meaningful only when D exceeds the max degree of the input generators; report both, and treat gbsize == number-of-inputs as a no-op sentinel. The bound must be shown to BITE (a third control)."},
    {"n": 18, "name": "Verdict double-counting / no dedup by content hash", "instance": "p108_821326 and p108_843700 are md5-identical and their EMPTY was double-counted; 49 TIMEOUT records reduced to 16 unique systems by tail-hash; the paused pair108 sweep was re-running its own 4-minutes-earlier TIMEOUT under a different tag (621292 == 671059).", "file": "canon/CATCHES.md (Sec 1, Sec 2.3)", "guardrail": "Hash every exported system by content before scheduling; verdicts transfer by hash identity, and the register stores the unique-system map, not the tag count."},
    {"n": 19, "name": "Multi-parameter re-verification of a parameter-independent object", "instance": "(F2) mu0 = a2*mu2/3 and (F3) mu0*mu3 + mu1*mu2 = 0 were reported 'verified for d = 3,4,5,6,7,8,10,12', reading as eight confirmations. The y^3 row of (1.3) caps every index at 3, so for d >= 4 it is literally d-independent: H(d=5) == H(d=7) == H(d=9) as expressions. One identity, not a pattern.", "file": "canon/CATCHES.md (section 'BLINDSPOT 1')", "guardrail": "Before reporting 'verified for d = ...', check whether the object depends on d; if not, report it as one check and say why."},
    {"n": 20, "name": "Statistical structure announced off too few samples", "instance": "On four primes the nine bottom edges were declared '4 degenerate over Q + 5 admissible forming one Galois orbit', closing the 'four seeds invisible at p=1000003' gap. A fifth prime (1000081) falsified both: degenerate counts 4,4,4,2,4 and admissible counts 1,1,0,2,3 (avg 1.40) distinguish one orbit (1.0) from two (2.0) not at all. Both retracted; the gap reopened.", "file": "canon/CATCHES.md (section 'RETRACTION, 15 MINUTES OLD')", "guardrail": "A Chebotarev-style average needs enough primes for its own error bar before it is quoted as structure — especially when the conclusion would close a gap or retire planned work."},
    {"n": 21, "name": "Quantifier-scope drift (proof's hypothesis lives in the experiment, not the sentence)", "instance": "H1c: the proof evaluates at v = -1, legal only for polynomial R; the statement quantified over rational R. Counterexample D=6, k=1, R = c/(6(v+1)^2). Headline [PROVED-exact] gone. Same bug recurred in Session 38's 'weighted-homogeneous forces diagonal linear', whose grid had a > 0 > b written into it — (x, y+x^m) at weights (1,m) refutes the claim as stated.", "file": "errors/STATUS_CORRECTION.md item 1; errors/FAILURE_ANALYSIS.md M3", "guardrail": "Every claim carries an explicit `domain` and a domain probe: a recorded input just outside the intended domain on which the claim is REQUIRED to fail (wave3/w3_claim_ledger.py linter L3)."},
    {"n": 22, "name": "Proxy trust — metadata substituted for the artifact", "instance": "A five-day-old claim that a char-0 eliminant existed was believed from a filename and summary; the cited file was msolve real-solution boxes. Related: 'Nguyen 104 is unverified' concluded from three failed web searches; 'Compositio Math 160 (2024)' venue metadata fabricated for an unrefereed preprint; `pkill -f` used four times, once losing an uncommitted document.", "file": "errors/STATUS_CORRECTION.md items 4, 5, 8, 12; errors/FAILURE_ANALYSIS.md M2", "guardrail": "A file is evidence only after its contents have been read and matched to the claim; a negative literature claim requires a positive source (retraction/erratum/refereed contradiction), never absent hits; no venue/volume/year unless read off the published record; `pkill -f` banned."},
    {"n": 23, "name": "Convention / orientation / sign and unit errors", "instance": "(13,4) sign error; Sec 6.7 lemma false as stated; the (108,72) closure OVERSTATED on an underived beta=6; L is not a function of the degree pair — (72,108) gives L=3, (108,72) gives L=4. Unit slip: `ps -o rss` read as 8.37 GB when it reports KiB (= 7.98 GB), nearly producing a false imminent-OOM alarm.", "file": "canon/CATCHES.md (Sec 1, Sec 3(vii), 'MEASUREMENT NOTE'); errors/41.md Blocker 1", "guardrail": "Orientation is part of the record key: every degree-pair claim names its orientation. Every measurement states its unit and is re-sampled before a trend is revised."},
    {"n": 24, "name": "Policy without an enforcer; contradictory labels left standing", "instance": "The concurrency tripwire was policy-only and two OOM kills followed, including the original chart-N run at 83 min; the 'one-heavy' rule stayed manual. Separately, STATUS carried both 'First Framework PROVEN dead, unconditional' and 'conditional on unreproduced THEOREM 2/3' in two files at once.", "file": "canon/CATCHES.md (Sec 1, Sec 2.1, Sec 3(ix)); errors/STATUS_CORRECTION.md item 11", "guardrail": "Every policy has a live enforcer process (wave5/tripwire_enforcer.sh) or is made structural (a serial queue runner); a contradiction linter makes two records under one key with incompatible labels a hard error (w3_claim_ledger.py L1)."},
    {"n": 25, "name": "Run believed launched but never launched; coverage believed complete", "instance": "MISS-1 d7 confirm primes lost; MISS-2 d8-N never launched; MISS-3 d12-N-1/20 required and never run (its export b16seed2_d12_N_p1000003.ms was already on disk, unrun); MISS-4 case-2 Q-bar route never executed; MISS-6 F3 single-prime; 444/464 coverage hole. Container restarted 4x in one night, twice rolling the working tree back to an older commit.", "file": "canon/CATCHES.md (Sec 1 'Write-out finds', Sec 3(i), 'INFRASTRUCTURE NOTE')", "guardrail": "ps-verify every claimed-running job; the coverage register lists known holes rather than asserting closure; push every result immediately since the working tree can roll back."},
    {"n": 26, "name": "Resource exhaustion outside the monitored dimension (disk, not memory)", "instance": "A routine sweep found the container at 98% disk / 1.1 GB free — the same condition that killed the W=10 eliminator mid `json.dump` with OSError Errno 28. Neither job monitor would have caught it: both Groebner runs were healthy on memory and CPU.", "file": "canon/CATCHES.md (section 'SWEEP, 18:47. Disk was the real risk, not memory')", "guardrail": "Sweep DISK as well as memory before and during any long run; memory pressure announces itself, disk exhaustion corrupts a write at an arbitrary moment."},
    {"n": 27, "name": "Reporting/verification layer unsound even when the engine is sound", "instance": "trackA_eliminator.py's exact-Q reduction was fuzzed on ~1900 planted-solution systems with ZERO false closures, but: a CAPPED run reports '0 open leaves' and exits 0 with checkpoint done: True unconditionally; --verify skips branched/merged/capped nodes, does not check that a branch's children cover all cases, and reads nonzero hypotheses from the TREE's own meta (the artifact asserts its own hypotheses); load_system silently overwrites repeated monomials and stores zero coefficients; the '(SCOUTING ONLY)' warning reaches neither the JSON, --verify, nor the exit code.", "file": "canon/CATCHES.md (section 'MODULAR ELIMINATION IS UNSOUND', 'Related weaknesses in the same tool')", "guardrail": "A replay that shares the engine's arithmetic is not an independent check; capped runs must be a distinct label from completed, and every warning must survive into the artifact a later reader will open."}
  ],
  "hit_protocol": {
    "steps": [
      "H1 EXACTNESS. P, Q in Q[x,y] have exact rational coefficients. No floats anywhere in the decision path.",
      "H2 KELLER. det J(P,Q) = P_x Q_y - P_y Q_x is a NONZERO CONSTANT. Checked symbolically, at random exact rational points, and modulo several primes.",
      "H3 NON-INJECTIVITY. Two distinct points of C^2 with the same image, given exactly and substituted back. (Equivalently deg_geom > 1.)",
      "H4 NOT AN AUTOMORPHISM, independently. The generic fiber has more than one point, computed by resultant elimination with exact back-substitution -- a different computation from H3, not a restatement of it.",
      "H5 GAUGE INDEPENDENCE. H2-H4 survive random invertible affine changes of coordinates on the source AND on the target. This is the check the two wave-1 false positives would have failed.",
      "H6 NON-VACUITY. The gate itself must reject every known negative and accept the positive control. Enforced below; the module refuses to run otherwise.",
      "A candidate is reported as a HIT only if H1-H5 all pass and H6 held. Any single failure is reported with the step that failed, and NOTHING is claimed."
    ],
    "source_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/p11/reruns2/w3_hit_protocol.py (module docstring, 'THE GATE'; same module cited as wave3/w3_hit_protocol.py in errors/FAILURE_ANALYSIS.md guard table and invoked as '§7 HIT protocol' at canon/39:38, canon/40.md:70, canon/42.md:60)"
  },
  "guardrails": [
    {"test": "No verdict from an empty output file", "how_to_check": "Fail any pipeline step that reads a solver verdict when the -o file is 0 bytes. msolve exits 0 on timeout, segfault, OOM and parse error, so exit codes must be ignored entirely. Classification must match documented outputs exactly: '[-1]:' EMPTY, '[1,n,-1,[]]' POSITIVE-DIMENSIONAL, '[0,...' ZERO-DIM/HIT, anything else reported verbatim as UNRECOGNISED."},
    {"test": "stderr and stdout captured and clean for every solver invocation", "how_to_check": "Tee both streams; grep for 'Error when parsing'/'Error when reading'/'cannot be 0 modulo'. Any '[-1]' co-occurring with a parse or read error is a FAILURE record, never an EMPTY verdict."},
    {"test": "No constant generators and no coefficient >= p or ≡ 0 mod p in any exported .ms", "how_to_check": "Pre-flight scan of every export: reduce all coefficients mod p, drop vanishing terms, raise on a genuinely nonzero constant generator; assert count(|c| >= p) == 0 and count(c ≡ 0 mod p) == 0."},
    {"test": "Every certifier contains a negative control and no compile-time-constant check", "how_to_check": "AST scan of the tree (wave2/w2_cantfail_audit.py) exits nonzero on any literal-True check condition; each certifier must additionally carry an input on which it is REQUIRED to fail, and the scanner itself must be self-tested against a synthetic rigged/honest pair."},
    {"test": "Two-sided self-test on every branch-and-reduce or cascade tool before any real data", "how_to_check": "Run a planted-solution system (must stay OPEN) and a planted contradiction (must CLOSE); a tool that closes branches on a satisfiable system is quarantined. Verify solved values are actually read downstream (a cascade reporting 0 constraints at every level on an overdetermined system is not computing)."},
    {"test": "Emptiness search is targeted at an overdetermined level", "how_to_check": "Compute eqs - vars before launch; refuse to schedule an emptiness/parametrisation run when excess <= 0, since the variety is positive-dimensional and cannot be empty."},
    {"test": "Degree-bounded results bite", "how_to_check": "Report D and the max degree of the input generators together; fail the result if D <= max input degree, and treat gbsize == number-of-input-equations as a no-op sentinel, not evidence of non-emptiness."},
    {"test": "Modular verdicts never stand alone", "how_to_check": "Contradiction/emptiness claims require meta.mod == null (exact) or >= 2 primes plus a char-0 lift; assert the prime satisfies the campaign's hygiene rule (p ≡ 1 mod 3, good reduction) with control primes 5, 11, 17 fed in and required to be rejected."},
    {"test": "Ansatz pre-flight degree gate", "how_to_check": "Compute the max total degree the ansatz can produce; abort if <= 100 (restates Moh). Also assert gcd(deg P, deg Q) ∈ {16} ∪ (20,∞) and, below max 125, that the pair is (72,108) in one of its two orientations."},
    {"test": "Transcription term-by-term control map", "how_to_check": "For each transcribed equation, enumerate its terms and require a named control that fails if that term is deleted; a term with no such control is labelled UNVERIFIED. Reproducing the source's own worked examples does not count as verification."},
    {"test": "Every claim carries an explicit domain plus a domain probe", "how_to_check": "Structured ledger with stable keys (wave3/w3_claim_ledger.py): linter L3 rejects a PROVED claim lacking a recorded input just outside its domain on which it is required to fail; L1 rejects two records under one key with incompatible labels; L4 rejects any claim depending on a REFUTED one; L7 demands a reason for WITHDRAWN and forbids dressing it as machine-refuted."},
    {"test": "Anchor-by-exact-quotation for every literature dependency", "how_to_check": "Locate each load-bearing sentence by exact substring match against the file on disk (file:line); a missing anchor fails the run. Absent artifacts are labelled UNVERIFIED-HERE, never confirmed. A negative literature claim needs a positive source, never failed searches."},
    {"test": "Gauge admissibility proof recorded with every gauge", "how_to_check": "Require a forced-nonzero variable of nonzero weight proving every orbit meets the slice, plus the computed torus rank of the exact system the gauge is applied to."},
    {"test": "First-order/vacuity pre-check on any local criterion", "how_to_check": "Before running a rank or bifurcation test, ask what it reports if the tested quantity is a product of two functions vanishing at the base point; if that equals the expected answer, mark the test vacuous and do not cite it as evidence."},
    {"test": "Numerical lanes are finders, never evidence", "how_to_check": "Require a planted-root control at the same unknown-count; if the planted root is not recovered, no MISS from that lane may be cited. Only a HIT is admissible, and it goes to the HIT protocol."},
    {"test": "Content-hash dedup before scheduling", "how_to_check": "md5/tail-hash every exported system; refuse to schedule a hash already in the register, and store the unique-system map so verdicts are not counted per tag."},
    {"test": "Watchdogs and enforcers must self-identify their target", "how_to_check": "Every watcher passes a synthetic suite (fires on a synthetic hit, silent on empty/non-verdict files) and logs a value (e.g. /proc cmdline, RSS) that would visibly differ if it watched the wrong process; no regex-only matching."},
    {"test": "Claimed-running jobs are ps-verified; policy has an enforcer", "how_to_check": "Every 'running' claim carries a live PID check; concurrency/one-heavy rules are enforced by a serial queue runner or a live tripwire process, not by prose. `pkill -f` banned; jobs stopped by handle."},
    {"test": "Disk headroom swept alongside memory", "how_to_check": "Poll free disk before and during every long run and abort/free at a threshold; memory pressure announces itself, disk exhaustion corrupts a write mid-dump."},
    {"test": "Parameter counts ship with a gauge enumeration", "how_to_check": "No count is reportable without an explicit enumeration of the gauge group and a rank computation of its action on the parameter space."},
    {"test": "d-independence check before claiming multi-d verification", "how_to_check": "Compare the object as an expression across two values of d; if identical, report one check and state the structural reason rather than presenting N confirmations."},
    {"test": "Sampling adequacy for Chebotarev-style structure claims", "how_to_check": "Compute the error bar of the statistic over the primes sampled; refuse to quote it as structure — and especially to close a gap or retire planned work — until the sample separates the competing hypotheses."},
    {"test": "Read the artifact before building on it", "how_to_check": "Before launching a plan that depends on an existing script or JSON, read its docstring, meta and declared side conditions; the P0 truncation plan and the eliminator targeting were both settled by artifacts already in the repo."},
    {"test": "No candidate is called a counterexample without the full HIT protocol", "how_to_check": "H1-H6 in w3_hit_protocol.py, no step skipped, with H6 validation shown to have fired (rejects 8 known negatives, accepts the positive control); the module refuses to certify otherwise."}
  ],
  "facts": [
    {"claim": "No counterexample to JC2 was found; the HIT protocol was never invoked because nothing reached it.", "label": "ESTABLISHED", "evidence_path": "canon/LIVE_MAP.md:75-83; canon/L4_ENDGAME_REPORT.md:349"},
    {"claim": "GGV Theorem 1.2 / (3.6) row 3 is misprinted; the correct relation is mu3*A''(0) = -6*mu1, and the printed -2*mu3*q1''(0) term is spurious. Confirmed on four independent legs: the printed offprint p.85/p.93 renders, arXiv 1310.8249v3 eq (3.9), a re-derivation from GGV's own bracket ODEs, and an explicit numerical instance with q1''(0)=6, mu3=5.", "label": "ESTABLISHED", "evidence_path": "canon/CATCHES.md sections 'GGV (1.2) ROW 3 IS MIS-PRINTED' and 'BLINDSPOT 2'; wave6/w6_ggv12_rederivation.py"},
    {"claim": "Every B=16 emptiness verdict produced before the correction is VOID as a statement about B=16: V_campaign = V_true ∩ ({mu3=0} ∪ {q1''(0)=0}), a proper closed subvariety.", "label": "ESTABLISHED", "evidence_path": "canon/CATCHES.md, 'THE DAMAGE, EXACTLY' / 'WHAT IS VOID'"},
    {"claim": "On the corrected system the B=16 ladder is EMPTY in characteristic zero for d = 3..7 (d=7: 26 eq/20 unk, 1345 s, 6.67 GB, [-1], mod p agrees), with a positive control showing the pipeline can return non-empty.", "label": "ESTABLISHED (char-0, with positive control)", "evidence_path": "canon/CATCHES.md sections 'WHAT I RE-RAN TODAY ON THE CORRECTED SYSTEM' and 'B=16 LADDER: d = 7 IS EMPTY'"},
    {"claim": "GGHV Corollary 5.7's proof has an invalid step at gghv.txt:1430-1433 — after translation the bracket is 1/2 + (lambda/2)x^{-1/2}, not in K^x, so [1, Cor 7.2] does not apply; 51 of 66 required conditions are unsupported. The (9,27) orientation of (72,108) is therefore NOT killed by the literature.", "label": "ESTABLISHED (local line-by-line audit; not independently refereed)", "evidence_path": "canon/CATCHES.md section 'GGHV COROLLARY 5.7 IS UNPROVEN'"},
    {"claim": "d >= 8 chart N cannot be decided by exact elimination on this hardware: four formulations (25/24 unknowns, 16- and 20-bit primes, GB-only) all timed out with clean stderr. d = 8..12 chart N remain UNDECIDED.", "label": "MEASURED RESISTANCE, NOT A VERDICT", "evidence_path": "canon/CATCHES.md section 'd=8 chart N — resistance measured, not a verdict'"},
    {"claim": "The pentagon truncations W=12..19 are certifiably NON-EMPTY: trackB1_pentagon.py:432 witness() gives an exact rational point satisfying all equations and side conditions. The entire P0 plan is futile and withdrawn. W=10/11 fail only c_1_0 != 0, so they are neither certified alive nor killed.", "label": "ESTABLISHED", "evidence_path": "canon/CATCHES.md section 'P0 IS FUTILE'"},
    {"claim": "The witness admits no first-order correction: 283 eqs/165 vars, 7 nonzero residuals, rank J = 163, Jv = -F infeasible, with two independently verified obstruction certificates (one supported on the single weight-7 equation at bracket point (1,8), where F = -16 and all 165 partials vanish).", "label": "ESTABLISHED (local statement only; does not prove case (1) empty)", "evidence_path": "canon/CATCHES.md section 'FIRST DIRECT ATTACK ON THE BOTTOM-VERTEX PROBLEM'"},
    {"claim": "A plane Keller counterexample cannot have geometric degree 2 and cannot be a Galois covering; it must be a non-Galois covering of degree mu >= 3.", "label": "ESTABLISHED, RELYING ON UNRE-DERIVED INPUTS (Bayle-Beauville classification of birational involutions of P^2; Ramanujam/Morrow rationality of boundary components)", "evidence_path": "canon/CATCHES.md section 'A COMPLETELY DIFFERENT HUNT: CLASSIFY BY THE DECK GROUP'"},
    {"claim": "No plane tangent sweep is a counterexample: det J(S) = det(Delta,X') + gamma*det(Delta,Delta'); branch (a) is not Keller and cannot be repaired by a divisional twist, branch (b) forces a triangular automorphism, hence injective.", "label": "ESTABLISHED", "evidence_path": "canon/CATCHES.md section 'THE SWEEP MECHANISM IS DEAD IN THE PLANE'"},
    {"claim": "(F1)-(F4): mu0 occurs linearly in exactly one row of (1.3); on the normalized locus that row is mu0 = a2*mu2/3, so a counterexample requires a2 != 0 AND mu2 != 0 and the chart mu2 = 0 contains no counterexample at any d; (F3) mu0*mu3 + mu1*mu2 = 0; the corrected system is weighted-homogeneous with exact torus rank 1 (printed system: rank 0).", "label": "ESTABLISHED, BUT ONE IDENTITY EACH, NOT A PATTERN ACROSS d", "evidence_path": "canon/CATCHES.md sections 'THE B=16 LADDER, RE-READ' and 'BLINDSPOT 1'"},
    {"claim": "(1.3) is CORRECT: its residual factors exactly as -6*y^3*(p1*q0' - p0'*q1 - mu0), remainder 0, so (1.3) <=> p1*q0' - p0'*q1 = mu0, a Wronskian-type condition.", "label": "ESTABLISHED", "evidence_path": "canon/CATCHES.md section 'WE AUDITED (1.2) AND NEVER AUDITED (1.3)'"},
    {"claim": "The (72,108) pentagon bottom edge is completely classified: 17 equations = coefficients of 2fg' - 3f'g = w^2; chart c_2=0 EMPTY, chart c_2=1 zero-dimensional with a degree-9 eliminant; every extracted seed verifies 17/17 at every prime tested. Whether the admissible seeds form one Galois orbit is NOT established (retracted at the fifth prime), so testing one seed does not decide the family.", "label": "PARTLY ESTABLISHED; ORBIT STRUCTURE RETRACTED", "evidence_path": "canon/CATCHES.md sections 'THE (72,108) PENTAGON BOTTOM EDGE IS COMPLETELY CLASSIFIED' and 'RETRACTION, 15 MINUTES OLD'"},
    {"claim": "JC was refuted in dimension 3 (Alpöge 2026-07-19), with an infinite family of every geometric degree >= 3 (Gallagher), the mechanism named the tangent sweep (Speyer), generalized to all n > 2 (Gao, arXiv:2608.00222). n = 2 explicitly remains open, and Gao gives no reason the plane fails beyond Wang's degree-2 theorem.", "label": "LITERATURE, READ LOCALLY FROM papers/2608.00222.pdf", "evidence_path": "canon/CATCHES.md section 'A NEW DOOR: THE PLANE TANGENT SWEEP'"},
    {"claim": "THEOREM W2-1 replaces the refuted H1c result: T_{D,k}(R) = -c has a rational solution iff D ∉ {3,6,...,3k}; the old statement holds only under the added hypothesis 'R polynomial'. Consequently the transfer conjecture is exactly backwards and Second Framework (D=23) moves from DEAD to OPEN.", "label": "ESTABLISHED (machine-checked on 150 cells by two independent code paths)", "evidence_path": "errors/STATUS_CORRECTION.md items 1 and 13; wave2/w2_h1c_refutation.py, wave2/w2_money_cells.py"},
    {"claim": "First Framework (99,66) is CONDITIONALLY dead — conditional on the campaign's own unreproduced formalization of layers 1-3, the realization theory and the rigidity theorem. The 'PROVEN dead, unconditional' label is false.", "label": "CORRECTED LABEL, settled from the primary artifact", "evidence_path": "errors/STATUS_CORRECTION.md item 11; wave2/w2_pole_admissibility.py"},
    {"claim": "Current certifier state: 11/11 certifiers, 227/227 individual checks, 0 rigged checks in tree, 0 ledger lint findings (python3 wave2/run_all.py, exit 0 iff all pass).", "label": "REPORTED BY THE ARCHIVE, NOT RE-RUN HERE", "evidence_path": "errors/README.md; errors/STATUS_CORRECTION.md 'Reproduce'"},
    {"claim": "Three items are recorded as honestly unfixed: the essential-parameter count (#9, artifact absent, stands as ASSERTED), the pentagon infeasibility bound (#10, withdrawn), and §2.5 (UNVERIFIED-HERE, eliminant artifact absent).", "label": "OPEN BY THE ARCHIVE'S OWN RECORD", "evidence_path": "errors/FAILURE_ANALYSIS.md 'What is honestly still unfixed'"}
  ],
  "disagreements": [
    {"item": "Scope of the task instruction vs. the archive's layout", "detail": "The task named 'errors/false-proofs/Path A' as the two most relevant files; no such subdirectory exists. The two most relevant files by content are errors/FAILURE_ANALYSIS.md (mechanisms M1-M3 and the guard table) and errors/STATUS_CORRECTION.md (13 numbered errors with corrections and labels); errors/40.md-42.md are forward-looking session plans (Paths C, D, E), and Path A appears inside WAVE3_FINDINGS.md, which was not read. Read those two instead."},
    {"item": "HIT protocol numbering", "detail": "The canon files invoke it as '§7 HIT protocol' (canon/39:38, canon/40.md:70, canon/42.md:60) but no §7 section text exists anywhere in canon/. The only definition on disk is the executable one in p11/reruns2/w3_hit_protocol.py (H1-H6), which errors/FAILURE_ANALYSIS.md's guard table cites as wave3/w3_hit_protocol.py. The steps quoted above are from that module's docstring; the prose '§7' section itself may have been lost with the session 19-38 artefacts (canon/TRUST_MAP.md §4)."},
    {"item": "Whether the (72,108) admissible-seed gap is open", "detail": "canon/CATCHES.md contains both a section closing the 'four seeds invisible at p=1000003' gap by a Galois-orbit argument and, later in the same file, an explicit retraction of that closure on a fifth prime. The retraction is the later record and governs; a reader taking the earlier section alone would carry a withdrawn claim."},
    {"item": "Rank/bifurcation results still present in other canon files", "detail": "BIFURCATION.md and MORNING_SUMMARY.md report the rank criterion as a headline DECIDED result; canon/CATCHES.md downgrades it to bookkeeping and forbids citing it as evidence. Those files were not read here and may not carry the downgrade inline — treat CATCHES.md as authoritative."},
    {"item": "Not independently verified in this pass", "detail": "Every claim above is quoted from the archive's own record; no solver, certifier, or script was run (read-only budget). The GGV misprint, the GGHV Cor 5.7 defect, the deck-group result, and the sweep dichotomy are internally argued and internally cross-checked but have had no external referee, and the archive says so for the last two (it names Bayle-Beauville and Ramanujam/Morrow as un-re-derived inputs)."}
  ]
}
```
### READER: pentagon
```json
{
  "summary": "PENTAGON CASE 1 (bottom edge + level ladder). The bottom edge is completely classified (canon/OPEN_ITEMS.md §7): ungauged it is dim 1; chart c2=0 is EMPTY (wave6/bottomedge/be_c2is0_p1000003.out returns [-1]); chart c2=1 is zero-dimensional with a degree-9 eliminant both mod p and in char 0. The edge system itself is small and explicit (wave6/bottomedge/analyse.py): f = sum_{i=1..8} c_i w^i, g = w^2 + sum_{j=3..12} d_j w^j, single relation 2 f g' - 3 f' g = w^2, expanded into 17 coefficient equations in 18 unknowns. A seed is 'admissible' iff c1, c8, d12 are all nonzero; otherwise 'degenerate'. Nine geometric seeds exist; only F_p-rational ones are visible at each prime, so the census sweeps primes near 10^6. Earlier five-prime data gave admissible counts 1,1,0,2,3 (avg 1.40) and forced an explicit retraction (p11 commit 8492a76) of both the 'exactly one admissible seed' and the '4 degenerate over Q + one Galois orbit of 5' story: p=1000081 has 7/9 rational with 3 admissible, p=999983 has only 2 degenerate, so the degenerate part is NOT four rational seeds and the single-orbit claim is unestablished. The restart-resilient sweep (one prime per commit, canon HEAD = 24a06fc, p=1000171) adds eight more primes (orbit_data.txt): 999979 5/9 adm1, 999961 4/9 adm0, 1000117 5/9 adm1, 1000121 3/9 adm1, 1000133 3/9 adm1, 1000151 2/9 adm0, 1000159 5/9 adm1, 1000171 6/9 adm2 — elim_deg=9 and verify_fail=0 at every prime, cost ~96 s per prime end-to-end. Established: the eliminant is definitely NOT irreducible; every extracted seed verifies against all 17 equations. The 'four invisible seeds' gap is explicitly NOT closed. EXTENSION RUNS: job #1 (does the admissible seed at p=1000003 extend?) timed out — exit 124, 5400.63 s, 9.53 GB RSS, 0-byte output = NO VERDICT by the standing rule; job #2 (reduced 241 eq / 123 unk) died three times on address-space caps (3.5 GiB, 5.0 GiB, then stopped deliberately), relaunched uncapped 19:33:28, no verdict recorded. Both pentagon msolve exports also fail: L23 OOM exit 137 at 13.9 GB, L18_g3 SIGKILL at 6.2 GB/1799 s, L18_g2 TIMEOUT at 3600 s. LEVEL 16 (l16/breakthrough/PENTAGON_LEVEL16.md): the proposed 'sigma^6 | h7' multiplicity wall is WRONG. With z = s - tau, complete level 16 in the chart c0*c1 != 0 is solvable iff F0 = a0^2 - 4 c0 b0 = 0, F1 = a0 a1 - 2 c0 b1 = 0, a0^3*lambda = 0, and a4^2 - 4 c0 b8 = 0 — a joint condition on h7, h6 and the level-19 kernel constant lambda, not a divisibility on h7 alone. Two branches: (i) a0 = b0 = b1 = 0, (ii) lambda = 0 with h6 matching (h7/z^4)^2/(4 c0) in its constant and linear coefficients. The earlier ladder was wrong because it dropped the coupling: the true level-17 unknown is W9 = g9 - (3c1/2c0) z^4 h5 (and W8 = g8 - (3c1/2c0) z^4 h4 at level 16), leaving h5, h4 free; using g9 alone manufactures a false resonant obstruction. A separate bounded-support end condition ([z^19]K16 = 3c1(a4^2-4c0 b8)^2/(4c0^3)) supplies the fourth equation; omitting it yields spurious solutions with an illegal z^12 term. Level 15 on branch 2 branches again (C3 = 33 a0 c1 F2^2/(32 c0^4), F2 = 2a0a2 + a1^2 - 4c0b2), so no kill. RESIDUAL TORUS PARAMETER t is the affine edge coordinate on the chosen Newton face: A(t), B(t) leading-edge polys of exact degrees m, n; m A B' = n A' B gives B^m = c A^n, hence A = alpha G^a, B = beta G^b with g = gcd(m,n); the primitive residual R = Q^a - lambda P^b exposes H(t) of degree m-1 with (m-1)A'H = m A H', i.e. H^m = d A^{m-1} (at (m,n)=(8,12): H^8 = d A^7), forcing A = alpha (t-rho)^m, B = beta (t-rho)^n. This is a necessary-condition theorem only — NO VERDICT, including for (72,108). COUPLED-EDGE ESCAPE (p11 e4fa5ce): with T = y^4 S(xy) + lambda x^4 y^7, the minimal ansatz P = (x+y) + T^2, Q = B + T^3 is EMPTY (coefficient -8 s0^2 at x^0 y^9, char 0, s0 != 0), and the pure-high-block first-order subsystem is EMPTY; escape requires a same-order subtop Q line with G10' = 12, i.e. q_11_1 = 12 turned on at first order. CASE 2 char 0: eliminant computed (deg 1144, squarefree, irreducible over Q by Dedekind at 8 primes) so all 1144 edge points are Galois-conjugate; the residual system is 13 variables over the degree-1144 field K and is unsolved. No char-0 verdict anywhere; nothing here is EMPTY in char 0.",
  "systems": [
    {
      "name": "Pentagon bottom edge, chart c2=1",
      "path": "wt/canon/wave6/bottomedge/be_c2is1_p1000003.ms, analyse.py",
      "variables": "18 (c1..c8, d3..d12) minus the c2=1 gauge",
      "equations": "17 (w-coefficients of 2fg' - 3f'g - w^2)",
      "degree": "eliminant degree 9; system degree 2 in the c,d bilinear form",
      "field": "F_p (13 primes near 10^6) and char 0 (be_c2is1_q)",
      "verdict": "zero-dimensional, 9 geometric seeds; solved",
      "label": "[PROVED-exact] for dim/eliminant degree; per-prime seed census is mod-p"
    },
    {
      "name": "Pentagon bottom edge, chart c2=0",
      "path": "wt/canon/wave6/bottomedge/be_c2is0_p1000003.out",
      "variables": "same edge variables with c2=0",
      "equations": "17",
      "degree": "2",
      "field": "F_1000003",
      "verdict": "EMPTY ([-1] output), 1.67 s",
      "label": "mod-p only"
    },
    {
      "name": "Pentagon bottom edge, ungauged",
      "path": "wt/canon/wave6/bottomedge/be_free_p1000003.out",
      "variables": 18,
      "equations": "17",
      "degree": "2",
      "field": "F_1000003",
      "verdict": "dim = 1 (gauge orbit), 30 s",
      "label": "mod-p"
    },
    {
      "name": "Seed-extension job #1 (does the admissible seed extend?)",
      "path": "wt/canon/wave6/pentseed/seed0.log",
      "variables": "full pentagon late system",
      "equations": "full",
      "degree": "n/a",
      "field": "F_1000003",
      "verdict": "TIMEOUT exit 124, 5400.63 s, 9.53 GB RSS, 0-byte output = NO VERDICT",
      "label": "no verdict (timeout is not EMPTY)"
    },
    {
      "name": "Seed-extension job #2, reduced system",
      "path": "wt/canon/wave6/pentseed/lin.log, lin2.log, lin3.log, lin_queued.log, watch.log",
      "variables": 123,
      "equations": 241,
      "degree": "n/a",
      "field": "F_p",
      "verdict": "three deaths on address-space caps (3.5 GiB, 5.0 GiB, manual stop), empty output each time; relaunched uncapped 19:33:28, no recorded verdict",
      "label": "no verdict"
    },
    {
      "name": "Pentagon L23 export",
      "path": "wt/canon/wave1/pent_L23.ms, wave1/L23_VERDICT.txt",
      "variables": "58 essential (61 params, 3 gauges)",
      "equations": "66 conditions, 1,080,147 monomials, 43 MB",
      "degree": "12-23",
      "field": "F_p",
      "verdict": "msolve OOM exit 137 at 13.9 GB peak",
      "label": "no verdict"
    },
    {
      "name": "Pentagon L18 exports",
      "path": "wt/canon/pent/RUNLOG.tsv, pent_L18_g2.ms, pent_L18_g3.ms",
      "variables": "58 essential",
      "equations": "L18 subset (2.7 MB export)",
      "degree": "12-18",
      "field": "F_p",
      "verdict": "g3: SIGKILL/OOM, 1798.9 s, 6.24 GB; g2: TIMEOUT 3600.1 s; Singular slimgb also exit 137",
      "label": "no verdict"
    },
    {
      "name": "Case (2) edge variety, d_3_3=1 chart",
      "path": "wt/canon/STATUS.md §2.4-2.5, wave1/edgeQ_eliminant.txt, wave1/edgeQ_param.out",
      "variables": "7 edge variables",
      "equations": "edge system",
      "degree": "eliminant degree 1144, squarefree, irreducible over Q",
      "field": "Q (RUR via msolve -P 1)",
      "verdict": "dim 0, vdim 1144; single Galois orbit, no rational edge points",
      "label": "[PROVED-exact]"
    },
    {
      "name": "Case (2) char-0 residual system",
      "path": "wt/canon/STATUS.md §2.5 and §4",
      "variables": 13,
      "equations": "not recorded in the audited files",
      "degree": "not recorded; coefficients live in K = Q[theta]/(f), [K:Q] = 1144",
      "field": "K, degree-1144 number field",
      "verdict": "UNSOLVED — no char-0 verdict for case (2)",
      "label": "open"
    },
    {
      "name": "p11-zero full saturated bilinear chart (p_1_1=0, p_1_0!=0)",
      "path": "wt/p11/codex_p11zero/STATUS.md, p11zero_full_sat_p1000003.ms",
      "variables": 186,
      "equations": 306,
      "degree": "<= 2 (6,924 terms, 125,784 bytes)",
      "field": "F_1000003",
      "verdict": "generated and hash-pinned (SHA-256 f8fe18...6195d); NOT solved — no solver installed",
      "label": "no verdict"
    },
    {
      "name": "Pentagon level 16/15 exact ladder",
      "path": "wt/l16/breakthrough/pentagon_level16.py, pentagon_level15_branch2.py",
      "variables": "a0..a4, b0..b8, c0, c1, lambda, kappa, h5, h4 kernels",
      "equations": "4 at level 16 (F0, F1, a0^3 lambda, a4^2-4c0b8); 4 carried coefficients C3..C6 at level 15",
      "degree": "2-3 in the edge coefficients",
      "field": "char 0, symbolic (sympy), exact",
      "verdict": "NO VERDICT — branching condition, not emptiness; explicit char-0 witness for branch 1",
      "label": "[PROVED-exact] for the conditions; NO VERDICT for the pentagon"
    }
  ],
  "facts": [
    {"claim": "Complete pentagon level 16 in the chart c0*c1 != 0 is solvable iff F0 = a0^2 - 4c0b0 = 0, F1 = a0a1 - 2c0b1 = 0, a0^3*lambda = 0, and a4^2 - 4c0b8 = 0; equivalently branch (i) a0=b0=b1=0 or branch (ii) lambda=0 with h6 matching (h7/z^4)^2/(4c0).", "label": "[PROVED-exact]", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL16.md §Verdict"},
    {"claim": "Level 16 is NOT equivalent to (s-tau)^6 | h_7; the proposed level 16/15/14 quick-kill multiplicity wall does not continue.", "label": "[PROVED-exact] (retraction)", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL16.md §Verdict"},
    {"claim": "The sigma^6|h7 ladder was wrong because the complete level-17 unknown is W9 = g9 - (3c1/2c0) z^4 h5 (level 16: W8 = g8 - (3c1/2c0) z^4 h4). Dropping this coupling — treating g9 as the unknown — manufactures a false resonant obstruction; h5 and h4 stay arbitrary.", "label": "[PROVED-exact]", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL16.md §Independent diagonal derivation"},
    {"claim": "Triangular carried coefficients: [z^3]K16 = -9c1F0^2/(4c0^3); [z^4]K16 = -33c1F0F1/(4c0^3); [z^5]K16 mod F0 = -15c1F1^2/(2c0^3); [z^6]K16 mod (F0,F1) = -693 a0^3 lambda/(1024 c0^3); [z^19]K16 = 3c1(a4^2-4c0b8)^2/(4c0^3).", "label": "[PROVED-exact]", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL16.md"},
    {"claim": "The bounded-support end condition (allowed deg W8 <= 11, so the formal inverse's z^12 term must vanish) is essential; omitting it yields a spurious solution with an illegal z^12 term in g8.", "label": "[PROVED-exact]", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL16.md; l16 commit 1e3ac1f"},
    {"claim": "Branch 1 is genuinely alive: explicit char-0 witness c0=c1=lambda=1, a4=2, b8=d7=1, all other a_i,b_i,d_i and both earlier kernel constants zero, giving h7=2z^8, h6=z^8, h5=z^7 and making complete levels 19,18,17,16 vanish with exact degrees retained.", "label": "[CERTIFIED] (symbolic verification)", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL16.md §Sharpness and scope"},
    {"claim": "Level 15 on branch 2 requires C3=C4=C5=C6=0 with C3 = 33 a0 c1 F2^2/(32c0^4), F2 = 2a0a2 + a1^2 - 4c0b2; on the open chart a0*F3 != 0 (F3 = a0a3 + a1a2 - 2c0b3), C5 determines kappa uniquely and C6 determines d0 uniquely, so the generic part of branch 2 survives level 15.", "label": "[PROVED-exact]", "evidence_path": "wt/l16/breakthrough/PENTAGON_LEVEL15_BRANCH2.md"},
    {"claim": "Residual-edge theorem in the torus coordinate t: m A B' = n A' B gives B^m = c A^n and A = alpha G^a, B = beta G^b (g = gcd(m,n), a=m/g, b=n/g); the primitive residual R = Q^a - lambda P^b exposes H of exact degree m-1 with (m-1)A'H = m A H', i.e. H^m = d A^{m-1} (H^8 = d A^7 at (m,n)=(8,12)); since gcd(m,m-1)=1 this forces A = alpha (t-rho)^m and B = beta (t-rho)^n.", "label": "[PROVED-exact], necessary condition only", "evidence_path": "wt/l16/breakthrough/GENERIC_RESIDUAL_EDGE.md"},
    {"claim": "The residual-edge filter has NO EMPTY output for any degree pair, including (72,108); tame controls P = x + y^m, Q = y + P^k at (1,2),(2,4),(2,6) are NONEMPTY and survive the full-power conclusion.", "label": "NO VERDICT (explicitly stated)", "evidence_path": "wt/l16/breakthrough/GENERIC_RESIDUAL_FILTER_STATUS.md"},
    {"claim": "Coupled-edge: with T = y^4 S(xy) + lambda x^4 y^7, the minimal ansatz P = (x+y) + T^2, Q = B + T^3 is EMPTY in char 0 because the x^0 y^9 coefficient of {A,T^3}+{T^2,B} is exactly -8 s_0^2 and the lower-left vertex forces s_0 != 0.", "label": "[PROVED-exact] for that ansatz only", "evidence_path": "wt/p11/codex_p11zero/EDGE_STRUCTURE.md §Exact obstruction"},
    {"claim": "Escape condition: with F_8 = a S_0^2, G_12 = b S_0^3 and no same-order subtop Q line, weight-13 gives -G_12' = 0 and weight-11 gives F_8' + 12 G_12 + u G_12' = 0, a contradiction in char 0 (EMPTY). Retaining a subtop term t y^10 G_10(u) changes weight 11 to F_8' + 12G_12 + uG_12' - G_10' = 0, forcing G_10 = 12u + const, i.e. q_11_1 = 12 must turn on at first order. This subsystem does not decide the full all-vertex chart.", "label": "[PROVED-exact] for the subsystem; NO VERDICT overall", "evidence_path": "wt/p11/codex_p11zero/EDGE_STRUCTURE.md §Exact first-order escape condition"},
    {"claim": "Bottom-edge seed census: 9 geometric seeds; admissible = c1,c8,d12 all nonzero. Sweep primes and (rational/9, admissible): 999979 (5,1), 999961 (4,0), 1000117 (5,1), 1000121 (3,1), 1000133 (3,1), 1000151 (2,0), 1000159 (5,1), 1000171 (6,2); elim_deg = 9 and verify_fail = 0 at every prime. Earlier primes 1000003, 999983, 1000033, 1000039, 1000081 gave admissible 1,1,0,2,3.", "label": "mod-p census, not char 0", "evidence_path": "wt/canon/wave6/bottomedge/orbit_data.txt, sweep.log, analyse.py; p11 commits 24a06fc..fb936be"},
    {"claim": "RETRACTED: 'exactly one admissible bottom-edge seed' and '4 degenerate over Q + one Galois orbit of 5 admissible'. p=1000081 gives 7/9 rational with 3 admissible; p=999983 has only 2 degenerate. Admissible average 1.40 fits neither one orbit of 5 (avg 1.0) nor two orbits (avg 2.0). The four-invisible-seeds gap is NOT closed.", "label": "retraction, recorded", "evidence_path": "wt/p11 git commit 8492a76"},
    {"claim": "What survives the retraction: the degree-9 eliminant is definitely NOT irreducible (total rational counts averaging ~5 over the first five primes), and every extracted seed verifies against all 17 bottom-edge equations at every prime.", "label": "mod-p evidence", "evidence_path": "wt/p11 git commit 8492a76; wt/canon/wave6/bottomedge/orbit_data.txt"},
    {"claim": "Prime-sweep cost: ~96 s wall per prime for solve + analyse + commit (e.g. 20:25:25 solve 999979 -> 20:27:01 committed), one prime per commit, restart-resilient. The original bottom-edge char-0 run (be_c2is1_q) took 316 s / 141 MB; the p=1000003 modular run 156 s / 189 MB.", "label": "measured", "evidence_path": "wt/canon/wave6/bottomedge/sweep.log, be.log"},
    {"claim": "Case (2) eliminant is degree 1144, squarefree, irreducible over Q (Dedekind at 8 primes 100003..100129, all degree-sums 1144, no surviving proper-factor degree; controls detect a planted 400+744 split). Hence all 1144 edge points are Galois-conjugate and the Q-bar question is one yes/no about the generic point.", "label": "[PROVED-exact]", "evidence_path": "wt/canon/STATUS.md §2.5"},
    {"claim": "A char-0 verdict for case (2) requires solving the 13-variable residual system over K = Q[theta]/(f) with [K:Q] = 1144; it is unsolved. The gcd shortcut was retracted (substituting the RUR eliminates only the 7 edge variables, leaving 13 free, so there is no univariate polynomial and no gcd).", "label": "open; retraction recorded", "evidence_path": "wt/canon/STATUS.md §4 and §6 item 3"},
    {"claim": "Recorded case-(2) EMPTY is mod-p only, at primes 65521, 32003, 65537, two of which violate the p = 1 (mod 3) hygiene rule; the chain was re-run compliantly at 65539 and 65599 and every branch reproduces dim = 2, same component. STATUS.md forbids promoting this to char 0.", "label": "mod-p only", "evidence_path": "wt/canon/STATUS.md §2.4 item 2, §7 table; wt/canon/OPEN_ITEMS.md §5"},
    {"claim": "Pentagon parameter budget: y-adic Jacobian rank 60 of 61 (two primes, three random points each), gauge group 3-dimensional (translation p_00, overall scale, coordinate scale (x,y)->(lam x, lam^-3 y)), so 58 essential parameters against 60 independent conditions — overdetermined by 2, plus 314 surplus conditions. Rank saturates at level j <= 23.", "label": "[CERTIFIED]", "evidence_path": "wt/canon/STATUS.md §3"},
    {"claim": "Pentagon conditions are sparse, not un-writable: 686 monomials at level 13 (total 3,394) up to 199,017 at level 26 (total 1,474,753), ~1.5x growth per level; whole build to level 26 takes 148 s. The earlier 'cannot be written down' claim used the dense bound and is retracted.", "label": "measured; retraction recorded", "evidence_path": "wt/canon/wave1/H1B_REFORMULATION.md §2; STATUS.md §6 item 2"},
    {"claim": "The pentagon late block (13 late parameters P_12..P_16) is affine only through level 24 — levels 13-15 do not involve it at all, levels 18-24 are degree 1, and the termination conditions are degree 2 and 3 — so a clean linear elimination of the late block is unavailable, and eliminating it raises degrees (45 surviving conditions above degree 30).", "label": "[PROVED-exact] (measured by degree along a random line)", "evidence_path": "wt/canon/wave1/H1B_REFORMULATION.md §1"},
    {"claim": "p11-zero chart searches found no witness: 1,764 sparse F_43 choices (+42 perturbations) all rank 14/15; all 29^3 = 24,389 square-top-edge slices over F_29 rank 9/10; kernel-aware order-two gate exhausted 917,969 coordinates at F_43 and 591,041 at F_31 with no obstruction-zero jet. The earlier greedy-arc slice-exclusion interpretation was retracted (corrections defined only modulo a 34-dimensional kernel).", "label": "NO VERDICT; retraction recorded", "evidence_path": "wt/p11/codex_p11zero/STATUS.md; p11 commit 9abca1f"}
  ],
  "open_items": [
    {"name": "Does the admissible bottom-edge seed extend to a full pentagon solution?", "status": "NO VERDICT — job #1 timed out (exit 124, 5400.63 s, 9.53 GB, 0-byte output); job #2 (241 eq/123 unk) died three times on caps and was relaunched uncapped with no recorded verdict", "what_it_would_take": "either the rational-function cascade (P2) to propagate past level 3, or a solver run that completes on the reduced 241/123 system; plus a second prime, since modular emptiness was shown unsound for contradictions", "compute_estimate": ">90 min and >10 GB RSS already spent with no verdict; job #2 was growing 0.63 GB/min", "files": ["wt/canon/wave6/pentseed/seed0.log", "wt/canon/wave6/pentseed/lin.log", "wt/canon/wave6/pentseed/lin2.log", "wt/canon/wave6/pentseed/lin3.log", "wt/canon/wave6/pentseed/watch.log", "wt/canon/wave6/pentseed/lin_queued.log"]},
    {"name": "Four invisible bottom-edge seeds / Galois structure of the degree-9 eliminant", "status": "OPEN — gap explicitly NOT closed after the 5-prime retraction; 13 primes censused so far", "what_it_would_take": "factor the degree-9 eliminant over Q directly (char-0 factorization), rather than inferring orbit structure from Chebotarev averages", "compute_estimate": "cheap — the char-0 bottom edge already solves in 316 s; the sweep costs ~96 s/prime", "files": ["wt/canon/wave6/bottomedge/orbit_data.txt", "wt/canon/wave6/bottomedge/be_c2is1_q.ms", "wt/canon/wave6/bottomedge/elim_roots.json", "wt/canon/wave6/bottomedge/analyse.py"]},
    {"name": "Pentagon level 16 branches 1 and 2 — descend further", "status": "branch 2 survives level 15 generically (kappa and d0 determined); branch 1 alive with an explicit char-0 witness; exceptional subbranches a0=0 and F3=0 undecomposed", "what_it_would_take": "continue the exact coupled ladder (W-variables, all kernel constants retained, bounded-support end checks) to levels 14 and below, and decompose the a0=0 / F3=0 strata from the four emitted polynomials", "compute_estimate": "symbolic, per-level; the levels done so far are minutes of sympy", "files": ["wt/l16/breakthrough/PENTAGON_LEVEL16.md", "wt/l16/breakthrough/PENTAGON_LEVEL15_BRANCH2.md", "wt/l16/breakthrough/pentagon_level16.py", "wt/l16/breakthrough/pentagon_level15_branch2.py", "wt/l16/breakthrough/PENTAGON_LEVEL17.md"]},
    {"name": "Case (2) characteristic-0 confirmation (plan item P4)", "status": "OPEN — eliminant exists and is irreducible; residual system unsolved", "what_it_would_take": "solve the 13-variable residual system over K = Q[theta]/(f), deg 1144 (or equivalently decide the single generic point); NOT reachable by gcd (retracted)", "compute_estimate": "unknown; the RUR alone is 46 MB and the eliminant 5.7 MB with a 4666-digit leading coefficient", "files": ["wt/canon/STATUS.md", "wt/canon/wave1/edgeQ_eliminant.txt", "wt/canon/wave1/edgeQ_param.out", "wt/canon/wave1/H1F_FINDING.md", "wt/canon/OPEN_ITEMS.md"]},
    {"name": "Pentagon full-system solve (L18/L23 exports)", "status": "STALLED — both engines exhausted: msolve L23 OOM exit 137 at 13.9 GB, Singular slimgb on L18 exit 137, L18_g2 TIMEOUT 3600 s. Emptiness is NOT claimed.", "what_it_would_take": "the rational-function cascade (three attempts, three failures, all caught by self-tests; attempt #3 reported 57 dead branches of 61 on a consistent system) — the vanishing-symbolic-pivot case must be designed on paper first", "compute_estimate": "beyond 15 GB / 1 h with current engines", "files": ["wt/canon/wave1/pent_L23.ms", "wt/canon/wave1/L23_VERDICT.txt", "wt/canon/pent/RUNLOG.tsv", "wt/canon/pent/RUNLOG_NOTES.md", "wt/canon/wave1/H1B_STATUS.md"]},
    {"name": "p11-zero chart (p_1_1=0, p_1_0!=0) full saturated bilinear system", "status": "exported, hash-pinned, never solved — no compatible solver installed in that environment", "what_it_would_take": "run msolve/Singular on p11zero_full_sat_p1000003.ms (186 vars, 306 eqs, degree <= 2), then lift any modular witness to char 0", "compute_estimate": "unknown; file is only 126 KB", "files": ["wt/p11/codex_p11zero/STATUS.md", "wt/p11/codex_p11zero/bilinear_full.py", "wt/p11/codex_p11zero/kernel_order2.py"]},
    {"name": "41 undecided timeout shapes; H2 above-125 sweep; H4 deg_y=3", "status": "OPEN, untouched (H2: ~150 of 167 targets unrun; 429 above-125 cases blocked on the chain compiler)", "what_it_would_take": "chain-compiler extension; sweep the frontier smallest-first (plan P6)", "compute_estimate": "large", "files": ["wt/canon/OPEN_ITEMS.md", "wt/canon/STATUS.md"]}
  ],
  "pitfalls": [
    "Timeout is not EMPTY: job #1's 0-byte output after exit 124 was correctly classified NO VERDICT; the same rule applies to L18_g2's 3600 s timeout and to every empty file from a killed process (wt/canon/pent/RUNLOG_NOTES.md).",
    "OOM rows in wt/canon/pent/RUNLOG.tsv were measured with other solvers resident on a 15 GB box, so they mean 'did not fit in the memory available then', not a hard memory bound. Only the L23 figure (exit 137, 13.9 GB, box to itself) is quotable.",
    "Two different objects are both described as '13 variables': the case-(2) char-0 residual over the degree-1144 field, and the pentagon's 13 late parameters P_12..P_16. They are unrelated.",
    "Dropping the coupling (using g9/g8 instead of W9 = g9 - (3c1/2c0)z^4 h5 and W8 = g8 - (3c1/2c0)z^4 h4) manufactures a false level-16 resonant obstruction — this is exactly how the sigma^6|h7 wall arose.",
    "Omitting the bounded-support end check (deg W8 <= 11, z^12 term must vanish) yields spurious solutions that pass every divisibility and resonance test.",
    "Chebotarev averages over four or five primes are not structure: the 5th prime falsified two just-made claims. A recorded method note says four primes read as a pattern only because a pattern was wanted.",
    "Pentagon detectors must fix all three gauges and use an ABSOLUTE normalization — two false-positive episodes were gauge artefacts (v1 drove ||x||->1e10 with a relative stopping test; v2's 1.70e-09 outlier inflated the denominator via the unfixed coordinate-scale gauge).",
    "The residual-edge collapse A = alpha(t-rho)^m is a necessary condition under stated Newton-face hypotheses; it has no EMPTY output, and one may NOT declare a pair empty merely because H vanishes or has lower degree — those are separate strata.",
    "The recorded case-(2) EMPTY used primes 32003 and 65537, both = 2 (mod 3), violating the campaign's own hygiene rule; the re-run at 65539/65599 preserves the verdict but it is still mod-p only.",
    "Route 1 / Route 2 for case (2) are file-level (code) disjoint but both descend from the same GGHV polygon derivation — not full independence.",
    "Three rational-function cascade attempts all failed their own self-tests; attempt #3 would have falsely killed the campaign's best lead had it been run on the pentagon."
  ],
  "disagreements": [
    "wt/canon/OPEN_ITEMS.md §7 still records 'exactly ONE of the five F_p-rational seeds admissible' as the pentagon bottom-edge state; the later p11 retraction (commit 8492a76) and the 8-prime orbit_data.txt (admissible counts 0,1,2 varying by prime) supersede it. Treat OPEN_ITEMS §7 as stale on this point.",
    "OPEN_ITEMS.md §5 asserts case (2) 'IS DECIDED ... complete and certified at three independent primes', while STATUS.md §7 lists case (2) as mod-p only and explicitly forbids promotion. STATUS.md is the later and stricter record.",
    "wt/canon/wave6/bottomedge/be.log's truncated line for be_c2is1_p1000003 shows '19, 1144' where analyse.py and orbit_data.txt consistently report elim_deg = 9. The 1144 coincides with the case-(2) eliminant degree and the be.log line is truncated mid-output; I could not resolve which quantity it names within the tool budget. Do not quote 1144 for the bottom edge without re-checking be_c2is1_p1000003.out.",
    "STATUS.md §2 records that AUDIT_REPORT.md §2's claim 'the eliminant was completed, that is the unblock' was false — the cited file held only 28 real-solution boxes (msolve run without -P). Any downstream text citing the old AUDIT_REPORT is void on that point."
  ]
}
```
### READER: bottom-seed
```json
{
  "summary": "TARGET NOT LOCATED AS A FILE in any locally available checkout. The claim about it exists in exactly one place on disk: the `main` branch README of the archive repo, /home/user/jacobian_planar/README.md, lines 19-20 (section 'Cross-chat JC2 handoff audit'): 'The strongest inherited asset is the reconstructed characteristic-zero bottom-seed target over Q(alpha), degree five: 164 variables, 288 quadratic equations, 6,821 terms. It has NO VERDICT in characteristic zero.' and 'The specialized reduction at p=1000003 has an independently reproduced unit Groebner basis and is EMPTY mod-p only; that does not prove characteristic-zero emptiness.' No system file with those dimensions exists in main, docs/, archives/transfer/state_transfer.tgz (124 files, only wave5 .ms/.out), or in any of the six local worktrees (canon = claude/opus-5-counterexample-plan-sep6yk, p11 = codex/pentagon-p11-zero-search @ e4fa5ce, mailbox = codex/claude-opus5-mailbox @ 156ba7a, l16, pq, hunt, errors). Greps for '164 variables', '288 equations', '6821' across all worktree .md/.log/.txt returned nothing; the only 6821/1000003 hits are unrelated numeric data in campaign/d23_borisov/d23_PR_data/*.txt.\n\nTwo concrete nearby assets were found and are almost certainly what the README paraphrases (with drifted numbers).\n(A) The reconstructed char-0 export `wave6/frontier/trackB1_sat_Q.ms` — 'the exact characteristic-zero system (166 vars, degree 5, max integer coefficient 468)', reconstructed by common-integer-lift from two primes (p=1000003 and campaign/audit_tracks/trackB1_case1_full_p65521.ms), 284/284 equations matching monomial-for-monomial, all 8,774 coefficients sharing a common lift, verified by re-reduction to both primes. Documented in mailbox/AGENT_MAILBOX.md lines 236-260. 'Tier 1 had no char-0 form before this.' Its Groebner ledger (AGENT_MAILBOX.md ~1419) is four attempts / four NO VERDICT: 60 vars deg 22 p_16_8-sat -> OOM at 13.9 GB in 18 min; 186 vars deg 2 all-vertex-sat -> timeout at 2.3 GB (40 min, then again at 3 h); 148 vars deg 2 p_10_2-sat -> timeout, 1.5 GB, 50 min. msolve is excluded (2^25 hash-table ceiling; segfaults above ~180 vars).\n(B) The pentagon bottom-edge seed-pinned system in the p11 worktree: wave6/pentseed/seed0_p1000003.ms (147 KB, msolve format, mod 1000003) and its linearly reduced twin seed0_p1000003_lin.ms (188 KB). Sizes: 267 eq/148 unk unreduced, 241 eq/123 unk after a sound constant-coefficient linear fixed point. seed0.log records exit 124, TIME 5400.63 s, RSS 9,992,824 KB (~9.5 GB), 'DONE -> []' with a 0-byte .out — a TIMEOUT, not EMPTY. The 'degree five / Q(alpha)' language is the degree-9 bottom-edge eliminant splitting as 4 degenerate + 5 admissible conjugate seeds over a degree-5 number field (CATCHES.md ~1990); that Galois-orbit claim was then RETRACTED 15 minutes later by a fifth prime p=1000081 (counts 1,1,0,2,3, avg 1.40 — one orbit averages 1.0, two average 2.0).\nSo: no local file, no recorded char-0 unit GB, and the README's 'unit Groebner basis at p=1000003' is not reproduced by anything on disk here (the local p=1000003 pentseed runs are timeouts). The asset, if it exists, lives on the campaign branch (claude/opus-5-counterexample-plan-sep6yk, head 24a06fc, path wave6/frontier/) and/or the mailbox branch codex/claude-opus5-mailbox (README names remote mailbox snapshot 7db7ff2, handoff reaching OPUS43-012); large .ms/.gens files were explicitly excluded from the transfer archive as 'regenerable'.",
  "location": {
    "branch": "claimed on main README; artifact itself named on claude/opus-5-counterexample-plan-sep6yk (head 24a06fc) and referenced from codex/claude-opus5-mailbox (head 156ba7a; README cites remote mailbox snapshot 7db7ff2)",
    "path": "claim: /home/user/jacobian_planar/README.md:19-20. Nearest real artifact: wave6/frontier/trackB1_sat_Q.ms (char-0), with mod-p twins wave6/frontier/trackB1_sat_p1000003.ms and campaign/audit_tracks/trackB1_case1_full_p65521.ms. Pentagon seed twin: wave6/pentseed/seed0_p1000003.ms and seed0_p1000003_lin.ms (present locally in the p11 worktree).",
    "format": "msolve .ms text export (variable list line, characteristic line, then comma-separated polynomials); char-0 version has characteristic 0",
    "size": "trackB1_sat_Q.ms not on disk locally (large .ms excluded from state_transfer.tgz as regenerable); seed0_p1000003.ms = 146,851 bytes, seed0_p1000003_lin.ms = 187,977 bytes",
    "found": false
  },
  "generation": {
    "script": "not located. Provenance chain for the char-0 form is common-integer-lift reconstruction from two modular exports (p=1000003 and p=65521), verified by re-reduction; pentagon seed pinning + sound linear reduction is wave6/w6_pent_lineloop.py (degree-1, constant-coefficient equations only, coefficients reduced mod P by redp()).",
    "provenance": "mailbox/AGENT_MAILBOX.md:246-260 (reconstruction of trackB1_sat_Q.ms, 284/284 equations, 8,774 coefficients, max integer coefficient 468, verified by reducing back to both primes 284/284 each). Pentagon seed provenance: p11/CATCHES.md:1600-1700 and 1930-2065.",
    "alpha_minpoly": "NOT RECORDED anywhere on disk. The only degree-5 algebraic object is the degree-5 factor of the degree-9 bottom-edge eliminant of the c_2=1 chart (9 = 4 degenerate + 5 admissible); its irreducibility over Q was inferred by Chebotarev from 4 primes and then RETRACTED after p=1000081 (p11/CATCHES.md:2037-2065). The eliminant was never factored over Q; CRT reconstruction from the modular runs is listed as the cheap alternative and remains owed."
  },
  "attempts": [
    {"solver": "Singular std/slimgb, eliminated p_16_8-saturated form (60 vars, deg 22)", "characteristic": "p=1000003", "outcome": "OOM", "wall_time": "18 min", "memory": "13.9 GB", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1419-1432 (Groebner ledger)"},
    {"solver": "Singular slimgb, all-vertex-saturated (186 vars, deg 2)", "characteristic": "p=1000003", "outcome": "timeout / NO VERDICT", "wall_time": "40 min", "memory": "2.3 GB", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1419-1432"},
    {"solver": "Singular slimgb, all-vertex-saturated (186 vars, deg 2), extended budget", "characteristic": "p=1000003", "outcome": "timeout / NO VERDICT", "wall_time": "3 h", "memory": "not recorded", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1419-1432, 1406"},
    {"solver": "Singular, x-degree<=2 p_10_2-saturated (148 vars, deg 2)", "characteristic": "p=1000003", "outcome": "timeout / NO VERDICT", "wall_time": "50 min", "memory": "1.5 GB", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1419-1432"},
    {"solver": "msolve -g 2 on 43 MB z*p_16_8-1 saturated export", "characteristic": "p=1000003", "outcome": "killed (memory)", "wall_time": "13 min", "memory": "13 GB of ~14 GB", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:413-415"},
    {"solver": "msolve -t 2 bilinear form", "characteristic": "p=1000003", "outcome": "exit 124, 0-byte output = NO VERDICT", "wall_time": "110 s budget", "memory": "n/a", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:415, 566"},
    {"solver": "msolve, seed-pinned pentagon system (267 eq/148 unk)", "characteristic": "p=1000003", "outcome": "TIMEOUT (exit 124, empty .out) - explicitly NOT empty", "wall_time": "5400.63 s (90 min)", "memory": "9,992,824 KB (~9.53 GB)", "evidence_path": "wt/p11/wave6/pentseed/seed0.log"},
    {"solver": "msolve, linearly reduced seed-pinned system (241 eq/123 unk)", "characteristic": "p=1000003", "outcome": "no verdict recorded; seed0_lin.out is 0 bytes", "wall_time": "capped ~50 min, 3.5 GiB address-space cap, oom_score_adj=1000", "memory": "capped 3.5 GiB", "evidence_path": "wt/p11/wave6/pentseed/seed0_lin.out, wt/p11/CATCHES.md:1690-1700"},
    {"solver": "any char-0 solver on the 164/288/6821 Q(alpha) target", "characteristic": "0", "outcome": "NONE recorded; NO VERDICT", "wall_time": "n/a", "memory": "n/a", "evidence_path": "/home/user/jacobian_planar/README.md:19"}
  ],
  "structure": [
    "Quadratic (degree-2) in the saturated/all-vertex formulation; the alternative eliminated formulation trades 60 variables for degree 22 and OOMs.",
    "Bilinear: 'the L = 2*alpha - beta grading and the bilinearity of every monomial' is listed as INTACT and independently verified (wt/p11/CATCHES.md:1600-1604). A separate 'bilinear form' export exists and was run under msolve.",
    "Torus/level grading L = 2*alpha - beta with a level census (deficits +1,+2,+3,+3,+1 then negative from Lambda = -1) - a genuine torus weight structure driving a level cascade.",
    "Block structure: square subsystem blocks indexed in wave6/frontier/tb1_square_block.json; c-block and d-block variables (c_i_j, d_i_j naming visible in seed0_p1000003.ms header).",
    "Galois symmetry: the system is defined over Q, so solvability is Gal(Qbar/Q)-invariant across the conjugate admissible seeds - this was the basis of an 'all five extend or none' argument that was later RETRACTED as not established.",
    "Side conditions / saturation: nonzero constraints on vertex coordinates c_1_0, c_8_14, d_12_21 (also c_8_16, d_12_24 in case 2); saturation variables z*p_16_8-1, p_10_2, all-vertex.",
    "After pinning the admissible seed: exactly the 17 L=4 equations satisfied, no nonzero constant row, 266-267 eq in 147-148 unknowns, 22 linear; sound linear fixed point -> 241 eq / 123 unknowns with degrees {2:72, 3:54, 4:115}. No linear obstruction kills the seed."
  ],
  "ideas_recorded": [
    {"idea": "Degree-bounded Singular ladder: degBound = 7 then 8 with std(I) on the saturated system; a unit at either rung is a real EMPTY verdict (mod p) - explicitly requested as a handoff because the container kept restarting every ~15 min.", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:236-250"},
    {"idea": "Independent rebuild/verification of the char-0 system trackB1_sat_Q.ms by common integer lift from two primes and re-reduction back to each (already done once: 284/284 both ways).", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:250-260"},
    {"idea": "Stop feeding saturated systems to Groebner; push closed-form reduction to x-degree 2 and use Groebner only on the small blocks it produces. Obstacle named precisely: for x-degree<=1, u=P is a first integral and Q is quadratic in u giving three x-slots; at x-degree 2, x is algebraic of degree 2 over u so the trick does not transfer.", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1455-1470"},
    {"idea": "The level cascade (propagating past level 3) is the only route that reaches this system by the author's own assessment - but it needs rational-function arithmetic over F_p implemented properly and it failed three self-tests; must be designed on paper before a fourth attempt.", "evidence_path": "wt/p11/CATCHES.md:1614-1620, 1930-1936"},
    {"idea": "Factor the degree-9 bottom-edge eliminant over Q (char-0 run produced it; CRT reconstruction from modular runs is the cheap alternative) to settle the Galois orbit structure and hence how many independent admissible seeds must be tested.", "evidence_path": "wt/p11/CATCHES.md:2028-2036"},
    {"idea": "Multi-prime seed extraction + Chebotarev to count Q-irreducible factors instead of inferring orbit structure from one prime (run at 1000003, 1000039, 1000033, 999983, 1000081).", "evidence_path": "wt/p11/CATCHES.md:1980-2050"},
    {"idea": "Second/independent prime for the admissible seed itself, guarding against bad reduction ('JOB 3'), plus exact lifting before any char-0 claim.", "evidence_path": "wt/p11/CATCHES.md:1962-1968"},
    {"idea": "Sound linear-only reduction (constant-coefficient degree-1 equations, iterated to fixed point) as a cheap preconditioner that shrinks 267/148 to 241/123 and is strictly better input for the Groebner run.", "evidence_path": "wt/p11/CATCHES.md:1622-1645"}
  ],
  "facts": [
    {"claim": "The strongest inherited asset is described as the reconstructed characteristic-zero bottom-seed target over Q(alpha), degree five: 164 variables, 288 quadratic equations, 6,821 terms, with NO VERDICT in characteristic zero.", "label": "NO VERDICT (char 0)", "evidence_path": "/home/user/jacobian_planar/README.md:19"},
    {"claim": "Its specialization at p=1000003 is claimed to have an independently reproduced unit Groebner basis, EMPTY mod-p ONLY; this does not prove char-0 emptiness.", "label": "EMPTY mod-p only", "evidence_path": "/home/user/jacobian_planar/README.md:20"},
    {"claim": "No file with 164 vars / 288 equations / 6,821 terms exists in main, docs/, archives/transfer/, or any of the six local worktrees; greps for those numbers return nothing relevant.", "label": "verified absent locally", "evidence_path": "grep over /home/user/jacobian_planar and wt/{canon,mailbox,p11,l16,pq,hunt,errors}"},
    {"claim": "An exact char-0 system trackB1_sat_Q.ms does exist on the campaign branch: 166 vars, degree 5, max integer coefficient 468, 284 equations, 8,774 coefficients, reconstructed by common integer lift from p=1000003 and p=65521 and verified by reduction back to both.", "label": "[CERTIFIED] reconstruction (verified 284/284 both primes); solver verdict still NO VERDICT", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:250-260"},
    {"claim": "Four Groebner attempts on the corrected target across two representations and a 10x budget range all ended NO VERDICT (one OOM at 13.9 GB, three timeouts including a 3-hour run).", "label": "NO VERDICT", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1419-1432"},
    {"claim": "The local p=1000003 pentagon seed run ended exit 124 at 5400.63 s with 9.53 GB RSS and a 0-byte output - a timeout, explicitly not an EMPTY.", "label": "TIMEOUT (not EMPTY)", "evidence_path": "wt/p11/wave6/pentseed/seed0.log"},
    {"claim": "The single admissible bottom-edge seed survives every purely linear consequence (fixed point 241 eq/123 unknowns, no inconsistent linear block, no equation collapsing to a nonzero constant). This cannot prove survival, only absence of a linear obstruction.", "label": "weak positive signal, mod p", "evidence_path": "wt/p11/CATCHES.md:1622-1650"},
    {"claim": "The degree-9 bottom-edge eliminant does NOT split as one degree-5 Galois orbit; that claim was retracted after p=1000081 gave admissible counts 1,1,0,2,3 (avg 1.40).", "label": "RETRACTED", "evidence_path": "wt/p11/CATCHES.md:2037-2065"},
    {"claim": "msolve is structurally excluded for this target: hard 2^25 hash-table ceiling and segfaults above roughly 180 variables.", "label": "tool limit", "evidence_path": "wt/mailbox/AGENT_MAILBOX.md:1053, 1233"},
    {"claim": "Large .ms/.gens solver files were deliberately excluded from archives/transfer/state_transfer.tgz as 'regenerable', which is why the target file is absent from the archive.", "label": "archive policy", "evidence_path": "/home/user/jacobian_planar/archives/transfer/README.md"}
  ],
  "pitfalls": [
    "msolve exits 0 on a coefficient-parse failure and writes an EMPTY output file: an empty .out is never an EMPTY verdict. Standing rule - read msolve's text output, never the exit code, and check the file is non-empty AND stdout/stderr clean (wt/p11/CATCHES.md:1655-1680).",
    "The msolve coefficient trap: substitutions done in plain sympy grow coefficients past P; 3921 of 8264 coefficients had |c| >= P and 8 were exactly 0 mod P, triggering 'coefficient cannot be 0 modulo 1000003'. Fix: reduce every coefficient mod P and drop vanishing terms before export.",
    "The same bug hid mathematics: with proper reduction the linear elimination goes further (245/127 -> 241/123 instead of 244/126).",
    "Unit slip: ps -o rss reports KiB. 8,371,388 is 7.98 GB, not 8.37 GB; a false OOM alarm was nearly reported. Always divide by 1048576 and re-sample before revising a trend.",
    "A mod-p unit Groebner basis at a single prime is EMPTY mod p only; contradictions do not lift without an exact certificate. Modular emptiness was proven unsound for contradictions in this campaign.",
    "One-prime seed censuses were repeatedly mistaken for statements about the problem; five primes were needed to break the orbit-count inference.",
    "A char-0 msolve real-root-isolation parse suggesting 2 of 9 seeds are real was explicitly recorded as PROVISIONAL AND NOT USED (37 box endpoints do not divide by 18 coordinates).",
    "The pentagon was never rigid: msolve solve mode needs zero-dimensional input, so prior solve-mode runs on it are NO VERDICT by construction; only Groebner-only mode (-g 2) decides emptiness at any dimension."
  ],
  "disagreements": [
    "Dimensions conflict: README main says 164 variables / 288 quadratic equations / 6,821 terms; the mailbox record for the reconstructed char-0 system says 166 vars / 284 equations / 8,774 coefficients / max integer coefficient 468. These are not the same numbers and no file reconciles them.",
    "'degree five' is ambiguous and probably conflated in the README: the mailbox says 'degree 5' meaning total polynomial degree of trackB1_sat_Q.ms, while README reads it as the degree of the field Q(alpha). The only degree-5 field object is the (retracted) degree-5 factor of the bottom-edge eliminant.",
    "'quadratic equations' (README) vs 'degree 5' (mailbox) for the same claimed system - mutually inconsistent unless these are two different exports.",
    "README asserts an 'independently reproduced unit Groebner basis' at p=1000003; nothing in any local worktree records a unit GB at that prime for this system - the local p=1000003 runs on the closest system are a timeout (5400 s, 9.5 GB, 0-byte out) and an OOM/timeout ledger of four NO VERDICTs. The unit-GB claim could not be corroborated from the material available here.",
    "The claimed asset may not exist as a single file at all; it may be a summary of the two-prime reconstruction (trackB1_sat_Q.ms) plus the pentagon seed narrative, merged during the cross-chat handoff audit. Treat the numbers as unverified until the campaign branch wave6/frontier/ is fetched and the file's header counted directly."
  ]
}
```
### READER: tail-census
```json
{
  "summary": "The 'above-125 tail census' in this archive is the frontier map at canon/wave6/frontier_151_300_map.json: a flat list of 432 records, each [max_degree, chain-string, status], covering max degree 156-300 (one orientation), generated by the trackD chain generator / chain-compiler pipeline (trackD_generate.py + TRACKD_CHAIN_MAP.md's GGHV-Sec-4 reduction, validated 6/6 on published reduced pairs). Status counts are exactly: 429 'NO-CHAIN', 1 '0-blocked' ((10,40)/18/5,8 at max 250), and 2 records carrying a numeric L-like value (4 at (8,28)/7/4,3 max 252; 2 at (12,30)/16/3,10/11/6,3 max 294). 'NO-CHAIN' is the archive's exact meaning of the recurring '429 cases requiring a chain-compiler extension' (STATE_FULL.md C; OPEN_ITEMS.md 6; AUDIT_EOD.md 4.1): the chain library / GGV shape classification stops around max 150, so for those 429 records no A0-chain, hence no reduced Newton-polygon pair, hence no system, can be compiled. They are enumerated but unsearched. A separate, smaller [125,300] coverage audit (STATE_FULL.md C) found 464 admissible pairs, of which the queue covered 20, a virgin sweep decided 6 EMPTY at two primes and left 36 TIMEOUT. Session 41 (canon/41.md, hunt/41.md) reports a different count, 804 admissible pairs with max in [125,300], and states none can be assigned an L, i.e. they can be listed but not ranked. These three counts (429 / 464 / 804) are different objects and are not reconciled anywhere in the archive.\n\nI could not find, anywhere in the worktree, the specific figures '189 non-closing records' or '184 new tail hashes'. Exhaustive grep over canon/, hunt/, p11/, pq/, mailbox/ (.md/.json/.log/.tsv) returned only unrelated hits (189 conditions in trackD_twoprime_state.json; 184 in CATCHES.md truncation tables). What the archive does contain on tails is CROSSDOOR.md section 5, 'Tail-closure (frontier finiteness)': dedup found reduced systems depend only on the chain TAIL; the predictor (last-2-segments, shape index) -> system hash has zero violations across 16 groups; the current library is 34 chains -> 26 distinct tails; the conjecture is that the tail set saturates, so the 429-case frontier collapses to finitely many tail-systems. The proposed test is exactly 'extend compiler on 20 sample cases across (150,300], count new tails vs reused'. That test appears to be UNRUN in this archive: no results file, no tail-hash counts. So 189/184 should be treated as either from a session not in this worktree or as an unverified premise.\n\nThe A'_t assumption: AUDIT_EOD.md section 4 item 3 and CATCHES.md line 32 record that for the (10,40) case, source [5] (arXiv:1708.07936) ASSUMES A'_t = (1,0) without printing the derivation. STATE_FULL.md C classifies it as '3 twist-blocked + 1 A'_t-assumed case: unclassified'. Discharging it requires re-deriving that step from [5]'s Algorithms; the gghv_audit re-implementation (HUNT2_REPORT T1) already reproduces 34/34 published cases and 10/10 GGHV rows, so it is the natural vehicle.\n\nThe '41 timeout shapes' are named in OPEN_ITEMS.md 7, STATE_FULL.md G3 and P6 but are NOWHERE enumerated as a list. Their components across the record are 33 virgin TIMEOUT shapes (AUDIT_EOD.md 3), 5 orphan TIMEOUTs (STATE_FULL.md C), 3 above-125 timeouts at 420s then 120s (ABOVE_125_STATUS.md), plus 4 (8,28) shapes at max 144 TIMEOUT in both engines; the arithmetic is not stated and 33+5+3 = 41 is my inference, not the archive's. Per the evidence rules every one of these is NO VERDICT, not EMPTY.\n\nExact system families newly found: the certification log in ABOVE_125_STATUS.md certifies 20 shapes across 6 chains EMPTY at max 126-147, single prime F_65521 only. HUNT2_REPORT adds T2 (378 Keller branches over 230 weight cells, all automorphisms, exact over Q) and T3 (1140 mu_n cells, all killed). Nothing char-0 solved above 125.",
  "census": {
    "region": "max degree 156-300 (one orientation), the above-125/above-150 frontier; the companion coverage audit covers max in [125,300] and Session 41 quotes max in [125,300] as 804 admissible pairs",
    "shapes": "records are keyed by chain string, i.e. GGV/[5] admissible complete chain data A0/A1/.../final-corner with cusp pair (m,n) (e.g. '(13,39)/25/13,3', '(8,24)/14/4,6/5/4,2', '(12,30)/16/3,10/11/6,3'); degree pair = (m(a+b), n(a+b)) for A0=(a,b). Reduced Newton-polygon pairs (the actual solvable object) exist only for chains the compiler can reduce via GGHV Sec 4 / TRACKD_CHAIN_MAP.md; for 429 of 432 records they do not.",
    "generator": "trackD chain generator (trackD_generate.py) extending [C]/[5] Sec 6 families past its max<=150 horizon, tier 'gen>150', pushed through four gates: compiler -> epsilon filter -> vertex probe -> trackB1 sweep; independent re-derivation of the same enumeration exists as gghv_audit/ggv_algorithms.py (M=100 -> 474 cases with max<=300)",
    "total_targets": "432 records in frontier_151_300_map.json (156-300). Related but distinct counts in the same archive: 464 admissible in [125,300] from the queue-coverage audit; 804 admissible pairs in [125,300] per Session 41; 474 possible counterexamples max<=300 from the independent gghv_audit re-derivation; 167/180 legacy trackD targets below that.",
    "unsearched": "429 of 432 are NO-CHAIN (no compilable chain -> no system -> never searched); 1 is 0-blocked; 2 carry an L-value. On the [125,300] coverage audit side: 20 covered by the queue, 6 EMPTY (2-prime), 36 TIMEOUT, 429 needing the compiler extension. Certified EMPTY anywhere above 125: 20 shapes across 6 chains, single prime only.",
    "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave6/frontier_151_300_map.json; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md#C"
  },
  "a_t_assumption": {
    "statement": "For the (10,40) case, source [5] (arXiv:1708.07936, 'Some Algorithms Related to the Jacobian Conjecture') assumes A'_t = (1,0) without printing the derivation; the archive records it verbatim as \"(10,40) case: [5] assumed A'_t=(1,0) unprinted -- re-derive\" and classifies the case in STATE_FULL.md as '3 twist-blocked + 1 A'_t-assumed case: unclassified'.",
    "why_load_bearing": "A'_t is a corner of the chain's terminal polygon data; it determines the final corner and hence which (m,n)/degree pairs the chain admits, which is what the enumeration of possible counterexample degree pairs above 125 rests on. If A'_t=(1,0) is not forced, the (10,40) chain may admit degree pairs the census does not list, so the frontier enumeration is not provably complete there. It is currently the one case in the census whose classification rests on an unprinted step of a source rather than on anything re-derived in this campaign.",
    "how_to_discharge": "Re-derive the step inside the existing independent re-implementation of [5]'s Algorithms 1-9 (gghv_audit/ggv_algorithms.py), which already reproduces 34/34 published cases at max<=150 and 10/10 rows of GGHV's own Sec 2 table with four negative controls: enumerate the admissible A'_t for the (10,40) chain from the algorithm's own filters rather than importing (1,0), and check whether any alternative A'_t survives and whether it produces a degree pair. If none survives, the case is closed by re-derivation; if one does, the census gains rows. Same pattern already used for the F6 gcd(m,n)=2 discrepancy (D7). Cost: small, hours of CPU at most; the work is reading plus re-running the existing enumerator.",
    "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/AUDIT_EOD.md (section 4, item 3); /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/CATCHES.md:32; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md:43"
  },
  "timeout_shapes": [
    {
      "shape": "NOT ENUMERABLE FROM THIS ARCHIVE: the '41 undecided TIMEOUT shapes' are referenced as an aggregate in OPEN_ITEMS.md item 7 / P6, STATE_FULL.md section G item 3, and wave6/CERTIFICATE_ROUTE.md, but no file in the worktree lists the 41 individually.",
      "last_outcome": "TIMEOUT (NO VERDICT; explicitly not EMPTY)",
      "wall_time": "unstated for the aggregate",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md:60,85; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md:87"
    },
    {
      "shape": "33 virgin TIMEOUT shapes (main virgin sweep of the [125,300] coverage audit); STATE_FULL.md quotes the same block as '36 TIMEOUT' from the virgin sweep, so 33 vs 36 is itself inconsistent in the record",
      "last_outcome": "TIMEOUT — facstd and msolve both stall at short budgets; queued for an overnight 1800 s long-budget run whose completion is not recorded",
      "wall_time": "short budgets (unspecified, < 1800 s); requeued at 1800 s",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/AUDIT_EOD.md:38,69; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md#C"
    },
    {
      "shape": "5 orphan-reconciliation TIMEOUT shapes (from the 254/478 orphaned vertex-LIVE entries)",
      "last_outcome": "TIMEOUT",
      "wall_time": "unstated",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md#C"
    },
    {
      "shape": "3 above-125 certification-sweep targets (from the 21 attempts of the ephemeral overnight run)",
      "last_outcome": "TIMEOUT — explicitly 'a timeout is not a verdict; those shapes are neither confirmed nor ruled out'",
      "wall_time": "420 s, then retried at 120 s",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md (Scope section)"
    },
    {
      "shape": "the 4 (8,28) shapes at max = 144",
      "last_outcome": "TIMEOUT in both engines; queued overnight",
      "wall_time": "unstated; requeued at 1800 s",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/AUDIT_EOD.md:38-40"
    },
    {
      "shape": "the two (9,27) 'sliver' p108 shapes (= GGHV Prop 4.1's reduced (9,27) polygons)",
      "last_outcome": "TIMEOUT — the first independent test of the orientation GGHV closes only via Cor 5.7",
      "wall_time": "shape 1 in msolve at 1800 s; shape 2 queued",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/AUDIT_EOD.md:96; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md#B"
    },
    {
      "shape": "H2 above-125 queue targets re-run at a 900 s cap, two compliant primes, then escalated to a second engine (msolve F4/FGLM)",
      "last_outcome": "NO VERDICT CHANGE — the two targets re-run stayed TIMEOUT; 0 LIVE, 0 DISAGREE; cross-engine controls pass (msolve reproduces Singular's EMPTY on a decided target in 0.07 s)",
      "wall_time": "900 s per prime",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT_REPORT.md (item 3 row; h2/h2_sweep_900.log, h2/h2_msolve.log)"
    }
  ],
  "families": [
    {
      "name": "Above-125 certification log: 6 chains / 20 reduced-polygon shapes ruled out by exact elimination — (7,42)/13/7,6 (m,n)=2,3; (7,42)/13/7,6 (m,n)=3,2; (8,40)/8,28/11/4,7 (m,n)=3,2; F11 (m,n)=2,5; (11,33)/19/4,8 (m,n)=2,3 [15 shapes]; (7,35)/19/7,5 (m,n)=2,3",
      "size": "20 shapes, 20-38 parameters each, max degree 126-147",
      "verdict": "EMPTY over F_65521 only — no non-degenerate realization; 20 of 167 targets decided, ~147 unrun; the (11,33) chain has 115 surviving shapes so the chain is NOT closed",
      "label": "mod-p only, single prime — NOT char-0; does not count as EMPTY in characteristic zero",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md (Certification log)"
    },
    {
      "name": "T2 same-sign weighted-homogeneous sector (new exact family sweep)",
      "size": "230 cells (all weight pairs a+b<=12, all (dP,dQ), full monomial bases to total degree 20), 378 Keller branches",
      "verdict": "EMPTY of non-automorphisms — 0 non-automorphisms; every branch certified an automorphism two ways (explicit inverse over K(s,t) both directions, generic-fibre count by resultant elimination); 9/9 controls",
      "label": "PROVED-exact (exact primary decomposition over Q in Singular, no sampling) — char 0",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT2_REPORT.md (T2); samesign/sweep_results.json"
    },
    {
      "name": "T3 mu_n-restricted (72,108) slice families (n in {2,3,4,6})",
      "size": "1140 faithful cells (12+72+192+864)",
      "verdict": "EMPTY — 1140/1140 killed by mechanically detected degeneracy; largest cell per n confirmed EMPTY on msolve at 3 compliant primes; n=1 control reproduces the full 72-var/92-eq system so the screen is not vacuous",
      "label": "degeneracy screen exact; solver confirmation mod-p at 3 primes — NOT char-0 for the solver step. Scope caveat: reduced coordinates of the (8,28) polygon pair, not (72,108) directly",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT2_REPORT.md (T3); symslice/symslice_results.json"
    },
    {
      "name": "Case-(2) w=-4 edge variety over Q (new exact object, both charts d_3_3=1 and d_3_3=0)",
      "size": "72 variables / 92 equations splitting by w=j-2i into blocks; w=-4 block eliminant degree 5; residual collapses to 27 conditions in 6 parameters",
      "verdict": "EMPTY at 1000003, 1000033, 1000039 in every Galois orbit, both charts; the degree-5 eliminant over Q was reconstructed by CRT from 41 of 96 primes and reproduces msolve's eliminant at 6 held-out primes — squarefree, irreducible over Q, no rational root, Galois group S5. Direct 71-variable route OOM-killed at 10 GB (not a verdict).",
      "label": "mod-p EMPTY at 3 fresh primes (NOT char-0); the Q-eliminant is 'reconstructed and verified at held-out primes, not a char-0 Groebner proof'. Char-0 confirmation is open (OPEN_ITEMS P4).",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT_REPORT.md (Item 1, Item 1b, Item 1c, 'the edge variety over Q, exactly')"
    },
    {
      "name": "h-branch / deg_y=3 slice (OPEN-1) msolve escalation family",
      "size": "cells (k, h, D) with k=4..6, D<=4..7; first case k=5,h=t,D=4 is 46 variables / 64 equations",
      "verdict": "NO VERDICT — OOM at both primes on every cell reached (k=4 deg<=6, k=5 deg<=4, k=5 deg<=5, k=6 deg<=4, k=4 deg<=7); one 6 GB run SIGSEGV'd (input validated, so genuine memory exhaustion, not a malformed file); one cell's second prime hand-terminated and marked UNKNOWN",
      "label": "NO VERDICT in any characteristic — a SIGSEGV/OOM is never EMPTY",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT_REPORT.md (item 4); /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/wave6/frontier/README.md"
    },
    {
      "name": "B=16 ladder cells d=2..12 (GGV Thm 1.2 systems) — the second, disjoint door",
      "size": "one cell per d; d=8 chart N is 30 eq / 23 unknowns on the corrected system, d=27 is 114 eq / 85 unknowns",
      "verdict": "d=2,3,4 EMPTY (reproduces GGV); d=5,6 EMPTY with char-0 Groebner PROOF plus 3 primes; d=7 EMPTY at one prime only; d=8 chart N exported but never launched; d=9,10,11 charts N never run; d=12 partial; d=27 untouched; d=12 unsaturated UNDECIDED after 2 kills",
      "label": "d<=6 [PROVED-exact] char 0; d>=7 mod-p or unrun. Every artefact built on GGV's misprinted (1.2) is VOID.",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md#A; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md"
    }
  ],
  "territory_ranking": [
    {
      "territory": "Tier 1 — trackB1_sat_p1000003.ms, pentagon case (1) unpinned, saturated on c_1_0, c_8_14, d_12_21, s_4_8 (166 vars / 284 eqs)",
      "rank": 1,
      "reason": "the hunt branch's own stated criterion: 'A NONEMPTY on trackB1 is immediately meaningful and nothing else here is' — a solution of that system IS an admissible point of case (1), i.e. a counterexample candidate. Everything else in the queue is ground-clearing. It also branches well: c_1_0*d_0_1 = 0 and c_1_0*d_1_1 = 0 with c_1_0 saturated nonzero kills one branch instantly and forces d_0_1 = d_1_1 = 0 in the other.",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/wave6/frontier/TARGET_QUEUE.md"
    },
    {
      "territory": "Tier 2 — p108_525122 surviving leaves (the (9,27) orientation sliver)",
      "rank": 2,
      "reason": "3 of 5 leaves already EMPTY, only 2 remain, and they are closest to the main line; the (9,27) orientation is killed in the literature ONLY by GGHV Cor 5.7, whose Sec 5 apparatus nobody has re-derived, so these runs are the first independent test of that closure",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/wave6/frontier/TARGET_QUEUE.md; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/STATE_FULL.md#B"
    },
    {
      "territory": "Tier 3 — 13 sweep NO-VERDICT cells, ranked by proximity then residual size: m16_d6 (17v/22eq), m16_d7 (20v/26eq), b16r_d5_A_q (15v/20eq char 0), b16r_d6_A_q (18v/24eq char 0), b16r_d7_A_q (21v/28eq char 0), u16_d7_q (19v/25eq char 0), then c2_w4_one_real / probe_w4m4_real (20v/19eq)",
      "rank": 3,
      "reason": "small enough to actually finish; the char-0 variants convert mod-p results into proofs. Deliberately EXCLUDED: the 14 bottomedge/be_* cells — they are NO VERDICT only because they are nonempty and slow (5 F_p-rational seeds, degree-9 eliminant), and listing them as leads would count known results as discoveries.",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/wave6/frontier/TARGET_QUEUE.md"
    },
    {
      "territory": "OPEN-1 / h-branch deg_y=3 slice (k>=4) — the 'campaign's real frontier' by the endgame-tablebase ranking",
      "rank": 4,
      "reason": "the campaign named its own blocker ('memory, not time... an F4/FGLM engine such as msolve moves the line further') and never pointed msolve at it — a 'Rosetta-Stone flag'. The hunt branch did, and got SIGSEGV/OOM at both 6 GB and across the staged ladder, so the flag is now known to need more than a second engine.",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/wave6/frontier/README.md; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT_REPORT.md (item 4)"
    },
    {
      "territory": "Path D — above-125 classification door (the 429/804 unrankable pairs)",
      "rank": 5,
      "reason": "explicitly ranked last for near-term yield: 'A counterexample from Path D this session: effectively zero. This path builds the road; it does not walk it.' Two blockers must fall together — L is not a function of the degree pair (804 pairs unassignable), and the constraints turn cubic at L=5 (Groebner timed out at 1200 s; iterated resultants cleared d_-5 and d_-4 in 4 s each then stalled 16+ min on d_-3, both dying at the same place because it is a shape change, not a compute limit). But it is the only route to territory nobody has searched.",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/41.md; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/hunt/41.md"
    },
    {
      "territory": "Closed / de-prioritised: T1 GGHV enumeration audit, T4 lift pipeline, T5 Gao family",
      "rank": 6,
      "reason": "all three returned DONE with no candidate: T1 no discrepancy in the enumeration (34/34 and 10/10 reproduced; seven discrepancies found are all non-degree-producing); T4 no rational point (case-(2) mod-p points lift to p^8 and are not rationally reconstructible; H2 has 0 LIVE targets so nothing to lift); T5 no PORT-CANDIDATE (both dimension-3 Gao maps sit at k=2 by both routes)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT2_REPORT.md"
    }
  ],
  "facts": [
    {
      "claim": "The chain-compiler extension is the map from chain data (A0, A1, ..., m, n) to the reduced Newton-polygon pair N(P), N(Q) and the bracket right-hand side — i.e. GGHV Sec 4's reduction (chain data -> automorphism sequence -> reduced pair). It is needed because the verdict machine (trackB1_polygon.py + trackB1_shapes.py) VERIFIES a given reduced pair but does not guess one, and the chain library stops around max 150, so 429 of 432 above-150 census records have no system to hand any solver.",
      "label": "documented, and the sub-150 version RESOLVED (TRACKD_CHAIN_MAP.md derives the map from GGHV Sec 4 + [C] Thm 2.20 and reproduces all six published reduced pairs plus the bracket exponent; all 34 shapes have explicit coordinates)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md ('What is BLOCKED, precisely' + 'Status: RESOLVED')"
    },
    {
      "claim": "The reason a naive pattern-fit for the chain->polygon map fails: (9,27) has A0 = n*(3,9) and A1 = n*(3,8) exactly, while (8,28) is NOT n*(lattice point) (8/3 not an integer) yet its reduced polygons have base pair (4,7),(4,8). Two examples with incompatible A0-to-base relations; fitting a rule to them is the exact failure mode that produced three retracted results.",
      "label": "PROVED-exact (both reduced pairs published and reproduced)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md"
    },
    {
      "claim": "A usable invariant on any candidate reduced pair: eps_P + eps_Q = (r+1, 1) where [P,Q] = x^r. Verified: (9,27) gives (1,1)+(1,0)=(2,1) with r=1; (8,28) gives (1,0)+(2,1)=(3,1) with r=2. Any candidate violating it is wrong.",
      "label": "CERTIFIED (checked on both published reduced shapes)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/ABOVE_125_STATUS.md"
    },
    {
      "claim": "Tail-closure conjecture: reduced systems depend only on the chain TAIL. The predictor (last-2-segments, shape index) -> system hash has ZERO violations across every system ever generated in the campaign (16 groups). Current library: 34 chains -> 26 distinct tails. If tails saturate, the 429-case frontier collapses to finitely many tail-systems, most already decided, and the compiler extension only needs each case's tail, not its full chain.",
      "label": "CERTIFIED as an observed zero-violation predictor over 16 groups; the saturation claim itself is CONJECTURE and its proposed test ('extend compiler on 20 sample cases across (150,300], count new tails vs reused') has no recorded result in this archive",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/CROSSDOOR.md (section 5)"
    },
    {
      "claim": "The B=16 ladder and (72,108) are DISJOINT doors: a B=16 solution in cell deg(q1)=d has deg(P)=16(3d-2), deg(Q)=16(2d-1) with gcd(m,n)=1 always, so B=gcd=16, while (72,108) has gcd 36. A hit in either suffices. The d=5..12 EMPTY verdicts therefore eliminate the specific above-125 pairs (208,144), (256,176), ..., (544,368) — territory no published elimination covers.",
      "label": "PROVED-exact (from GGV [4] Sec 2 sixth step) for the degree map; the eliminations themselves inherit their own labels (d<=6 char-0, d>=7 mod-p or unrun)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/CROSSDOOR.md (section 1)"
    },
    {
      "claim": "Seventh GGHV discrepancy found by cross-checking the campaign's own queue: 179 of 180 trackD targets match the re-derived enumeration; the one miss is F6(j=0; m,n=4,10), because family F6's m=3j+4, n=8j+10 gives gcd(m,n)=2 at every even j while Definition 3.3 requires gcd(m,n)=1. One entry of the campaign's queue is not a possible counterexample shape.",
      "label": "CERTIFIED (h2/w5_h2_target_provenance.py, 4/4 with negative controls)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT2_REPORT.md (T1, D7)"
    },
    {
      "claim": "One kill inside the 105-124 window rests on a source the audit cannot open: (80,112) is discarded by GGHV citing only '[4, Sec 3.5]' (Pro Mathematica 27, 2013, not on arXiv), with no argument of its own.",
      "label": "LIT-READ / EXTERNAL-NOT-RE-DERIVED",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT2_REPORT.md (T1)"
    },
    {
      "claim": "Two silent-failure modes in msolve 0.10.1, each with a minimal reproduction: (L1) a constant generator whose terms sum to a multiple of the characteristic is read as nonzero and the system is declared [-1] i.e. EMPTY — written as the single token 'p' it produces a zero-byte output file; (L2) repeated monomials inside one generator are not combined, so a+a+1000001 is solved as a+1000001. The campaign's own .ms files were scanned and are clean of both.",
      "label": "PROVED-exact (minimal reproductions in wave4/w4_msformat.py)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT_REPORT.md ('Tooling findings')"
    },
    {
      "claim": "A third can't-fail control was found and fixed: trackD_twoprime.py::control() built its 'unsaturated' variant by deleting lines containing 'sat' or beginning 'ideal N', and the generated source contains neither — the variant was byte-identical to the real system. Corrected controls in h2/w5_h2_controls.py pass 5/5.",
      "label": "CERTIFIED",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT_REPORT.md"
    },
    {
      "claim": "Campaign bottom line unchanged: no counterexample found, no non-EMPTY verdict on any real system, nothing promoted from mod-p to Q. No CANDIDATE-UNVERIFIED and no PORT-CANDIDATE was produced by any of the four hunt items or five territories.",
      "label": "CERTIFIED (both hunt reports; hunt/README.md)",
      "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/hunt/README.md; /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/HUNT2_REPORT.md"
    }
  ],
  "open_items": [
    {
      "name": "Chain-compiler extension for the 429 NO-CHAIN census records",
      "status": "OPEN, large; blocker is the compiler, not the mathematics. Importance rose after the dimension-3 refutation (Alpoge/Gallagher, July 2026) realized every geometric degree, killing degree-bound approaches. If B > 20 the counterexample lives here.",
      "what_it_would_take": "Either (a) extend GGV's shape analysis past max 125 — first DIAGNOSE why the enumeration terminates (genuine finiteness theorem vs computational cutoff vs artefact of the bound being proved), a ~2-day reading task on arXiv:1401.1784 and arXiv:1605.09430 that decides whether this is a week or a year — then mechanise Cor 7.4 / Prop 8.2 / the l_{rho,sigma}/en/st apparatus; or (b) the cheap route: run the tail-closure test (extend the compiler on 20 sample cases across (150,300], count new tails vs reused) and, if tails saturate, compute only each case's tail",
      "compute_estimate": "path (a): a paper's worth of work, weeks-to-months, low CPU; path (b): the 20-case tail test is an order of magnitude cheaper — days of build, hours of CPU. Note both are gated by the L>=5 cubic wall: even with polygons, systems with L>=5 are unrunnable today."
    },
    {
      "name": "L = 5 cubic wall (Path D, D2)",
      "status": "OPEN; L=4 is the last quadratic case (constraint degrees 2,2,2,2 at L=4 vs 2,2,2,2,3 at L=5). Groebner timed out at 1200 s; iterated resultants stalled on d_-3 for 16+ minutes. Both routes died in the same place.",
      "what_it_would_take": "Five attacks in the recorded order, starting with #5: derive E(L) and the ratio r(L) analytically the way U(L) was derived (U(L) = (L+1)[(L+1)(L+2)/2 - 1] + L; U(3)=39, U(4)=74, both measured), avoiding computing the L=5 relation at all. Then: exploit quasi-homogeneity with a matching weighted ordering (the L=4 relation had a 1-dimensional weight nullspace; never tried because L=4 did not need it); eliminate the cubic LAST; msolve F4/FGLM; split by the y-grading.",
      "compute_estimate": "attack 5 is hours, not days; the whole item is estimated 3-5 days"
    },
    {
      "name": "Char-0 confirmation of case (2)",
      "status": "OPEN and higher-value than before — modular emptiness was proved unsound for contradictions, so three agreeing primes is strong evidence, not a proof, and case (2) is one of only two shapes of the sole surviving degree pair below 125",
      "what_it_would_take": "msolve -P 1 over Q on the same rigidified system; the elimination route already collapses the residual to 27 conditions in 6 parameters and decides in hundredths of a second mod p, so the char-0 run is the remaining step. Priority P4.",
      "compute_estimate": "cheap relative to its value; the brute-force 71-variable route is out (OOM at 10 GB), the cascade route is small"
    },
    {
      "name": "The 41 undecided TIMEOUT shapes",
      "status": "OPEN, untouched; never swept smallest-first (priority P6). Not enumerated as a list anywhere in the archive.",
      "what_it_would_take": "First produce the list (it does not exist as an artifact — reconstruct from the virgin-sweep, orphan, above-125 and (8,28)-max-144 registers), then sort by size and sweep smallest-first. CROSSDOOR sections 2 and 6 propose two better-than-brute-force routes: run the cheap grading/torus finder (exponent-vector linear algebra) on each resister before spending 1800 s budgets, treating resistance as a treasure map; and search degree-bounded Nullstellensatz certificates (1 = sum h_i f_i mod p), which is a LINEAR system in the h coefficients — streamable, fixed memory, parallel.",
      "compute_estimate": "one experiment at certificate degree <= 3 on a single resister decides feasibility of the whole Nullstellensatz route; the grading finder is minutes per shape; brute-force is 1800 s x 41 x 2 primes minimum"
    },
    {
      "name": "(10,40) A'_t = (1,0) re-derivation, plus the 3 twist-blocked cases (c_t non-integer)",
      "status": "OPEN MATH, unclassified — no computation exists",
      "what_it_would_take": "re-derive the A'_t step inside gghv_audit/ggv_algorithms.py (see a_t_assumption); separately decide whether the 3 twist-blocked cases form a territory or admit a closure theorem",
      "compute_estimate": "hours of CPU; the work is reading and re-running an existing enumerator"
    },
    {
      "name": "Rational-function cascade (priority P2) — the shared blocker",
      "status": "OPEN, unbuilt; both prior cascade attempts failed on exactly this point",
      "what_it_would_take": "build it properly. Direct Groebner scales ~32x per ladder level (d=6: 42 s; d=7: 1345 s), so d>=8 in char 0 and d=12, 27 are out of reach by that route, and the pentagon needs the same machinery to propagate past level 3 through its two free parameters.",
      "compute_estimate": "highest-leverage build in the plan; unlocks P3 (d=12 then d=27) and the pentagon block-cascade"
    },
    {
      "name": "d = 8 chart N on the corrected system (priority P1)",
      "status": "READY, not yet run — exported as wave5/ms/m16_d8_*.ms, 30 equations / 23 unknowns (was 39/30 on the void printed system). a_16 left FREE so msolve covers both roots of the row-0 quadratic in one run; F2 (mu0 = a2*mu2/3) proves chart Z contains no counterexample, so chart N is the only chart.",
      "what_it_would_take": "launch it mod p, then char 0 if clean. It is the frontier cell — d<=7 are now EMPTY in characteristic zero.",
      "compute_estimate": "the cheapest genuinely new result available; small system"
    },
    {
      "name": "H2 above-125 sweep completion",
      "status": "OPEN — ~147 of 167 targets unrun (STATUS.md quotes '~150 of 167 targets unrun'); the overnight container was reclaimed after 21 attempts; the chain->polygon map needs hardening; the 20 certified EMPTYs are single-prime F_65521 only",
      "what_it_would_take": "re-run on a non-ephemeral host at >= 900 s per target at two compliant primes; bridge the existing 20 EMPTYs to a second prime; harden the compiler for superset-mode chains where the enumeration is wider but not proven exhaustive",
      "compute_estimate": "147 targets x 900 s x 2 primes ~ 74 CPU-hours minimum, more for the resisters"
    },
    {
      "name": "Tail-closure test (CROSSDOOR section 5)",
      "status": "PROPOSED, no result recorded in this archive",
      "what_it_would_take": "extend the compiler on 20 sample cases across (150,300] and count new tails vs reused tails; a low new-tail rate supports saturation and makes [125,300] finite work",
      "compute_estimate": "small — 20 compiler runs; this is the single highest-leverage cheap experiment for the 429-case frontier"
    }
  ],
  "pitfalls": [
    "The requested figures '189 non-closing records' and '184 new tail hashes' do NOT appear anywhere in this worktree. Exhaustive grep over canon/, hunt/, p11/, pq/, mailbox/ for 189 and 184 in .md/.json/.log/.tsv returned only unrelated hits (189 conditions in trackD_twoprime_state.json; 184 in a CATCHES.md truncation table). Do not treat them as archive facts. The census record set is 432 with 429 NO-CHAIN; the tail library is 34 chains -> 26 tails.",
    "TIMEOUT, OOM and SIGSEGV are NEVER verdicts. The archive says so explicitly in three places ('A SIGSEGV is NO VERDICT. Never EMPTY, never a hit'; 'a timeout is not a verdict'; 'STALLED - OOM ... recorded, not a verdict'). The 41 timeout shapes, the pentagon L18 stall, the h-branch OOMs and the 71-variable case-(2) route are all undecided, not empty.",
    "mod-p EMPTY is not char-0 EMPTY. The campaign itself proved modular emptiness unsound for contradictions. The 20 above-125 EMPTYs are single-prime F_65521; case (2) is 3 primes; T3's solver confirmations are 3 primes. None of these is a characteristic-zero result. Only d<=6 of the B=16 ladder and T2's exact primary decomposition over Q are char-0.",
    "Do not quote the case-(2) edge degree 5 and edgeQ_input.ms's degree 1144 as measuring the same variety. They are differently normalised objects; both reproduce; the campaign's six edge polynomials are not invariant under the residual gauge g_j -> kappa^(j-3) g_j while the derived system is.",
    "Everything built on GGV's printed (1.2) is VOID as a statement about B=16 — the equation was found misprinted on 2026-08-21. Several OPEN_ITEMS entries are void for this reason, not resolved.",
    "The pentagon detector's numbers are only interpretable together with the allowed scale at the point that produced them: the y-adic recursion amplifies, levels 13-23 run past 1e10 at a random point, and float64 cannot resolve an absolute 1e-9 there at all. A residual quoted without its allowed scale says nothing.",
    "One target of the campaign's own 180-target queue, F6(j=0; m,n=4,10), is not a possible counterexample shape at all (gcd(m,n)=2 violates Definition 3.3). Any coverage claim built on '180 targets' is off by that one.",
    "Ruling out some shapes of a chain does not rule out the chain: (11,33)/19/4,8 has 15 shapes certified EMPTY but 115 surviving shapes, so it is open.",
    "p108_821326 and p108_843700 are md5-identical systems — the (8,28)/11/4,7 and (8,32)/8,28/11/4,7 orphans reduce to ONE system, so their two EMPTYs are one result, not two. A dedup-by-hash across registers was still pending.",
    "37+ local commits were unpushed at the time of the record (container credential death, user-parked); results may exist only in chat logs and a stale API backup branch."
  ],
  "disagreements": [
    "Count of admissible pairs above 125 is stated three incompatible ways and never reconciled: 429 needing the compiler (STATE_FULL.md C / frontier_151_300_map.json, region 156-300), 464 admissible in [125,300] (STATE_FULL.md C, queue-coverage audit), 804 admissible pairs with max in [125,300] (canon/41.md and hunt/41.md), and 474 possible counterexamples with max <= 300 from the independent gghv_audit re-derivation. Orientation conventions (one vs both) probably explain part of the 429/804 gap but nothing in the archive says so.",
    "Virgin-sweep TIMEOUT count: AUDIT_EOD.md says '33 virgin TIMEOUT shapes' and queues '33 TIMEOUT shapes at 1800s', while STATE_FULL.md section C says the virgin sweep left '36 TIMEOUT'. The aggregate '41 timeout shapes' is never derived from either.",
    "H2 unrun-target count: ABOVE_125_STATUS.md says 20 of 167 decided with ~147 unrun; canon/STATUS.md line 273 says '~150 of 167 targets unrun'.",
    "The mu_n compatibility condition: the brief for T3 specified p + q = 1 + b (mod n); the territory found the correct condition in these reduced coordinates is p + q = 3a + b (mod n), since the bracket right-hand side is x^2, not a constant. Both are enumerated and labelled in symslice_results.json rather than one being assumed away — but the brief and the implementation disagree.",
    "[5] Section 5's own text says '2 admissible complete chains of length 2' while its own table lists seven; and the independent re-implementation finds two extra length-1 and four extra length-2 chains that [5]'s printed tables omit (each traced to the exact divergent step, each shown to produce no degree pair).",
    "GGHV's Theorem 2.1 imports its ten-case table from [5] rather than deriving degree pairs itself, so 'GGHV eliminated the region' is mechanically a claim about [5]'s Algorithms 1-9, not about GGHV. The (108,72) node is left open by GGHV itself; the (72,108) node's Section 5 kill has never been re-derived by anyone.",
    "The 'resistance-is-geometry' law is labelled a campaign heuristic and has a stated counterexample within the archive (d=3 unsaturated is instant AND has a degenerate family), so it must not be quoted as a rule."
  ]
}
```
### READER: mailbox
```json
{
  "summary": "Archive = a mailbox worktree at /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox, branch codex/claude-opus5-mailbox, head 156ba7a. All inter-agent messages live in ONE file, AGENT_MAILBOX.md (3985 lines); every mailbox commit touches only that file. Participants: Claude Opus 5 (session43, OPUS43-nnn), Codex/GPT-5 (CODEX-nnn), 'Sol', and a late arrival 'Fable' (FABLE-001..006, the last six messages and the current head). No counterexample was found; every message ends 'Pentagon: NO VERDICT'. Thread arc: the campaign spent ~40 sessions on degree pair (72,108), reduced to a 'pentagon' bracket system [P,Q]=x^2 with 186 unknowns (184 active + 2 inert) / 302 equations. OPUS43-012 (2026-08-22) reported that the two systems constituting the first independent test of GGHV Corollary 5.7 (wave6/ms/p108_192622.ms, 40 vars; p108_525122.ms, 28 vars) are grading-torus RANK 5, hence positive-dimensional, so msolve solve-mode could never terminate — their 1800s TIMEOUTs were structural, not budget. He sliced both with a validated gauge (weight-minor determinants -1/24 and -1/14, nonzero) and said they were 'running now'; no later message reports a verdict, and wave6/frontier/P108_RESULTS.md still records both as NO VERDICT (525122: 5 leaves, 3 EMPTY, 2 unresolved; 192622: 1 unresolved leaf, 139 eq / 38 vars). The same message allocated the tail-saturation test to Codex — extend chain construction to ~20 sample cases above 150 and count new vs reused tails; CROSSDOOR.md §5 records the library as 34 chains -> 26 distinct tails with zero predictor violations. No answer to that task appears anywhere in the mailbox. OPUS43-013..029 are the level-by-level pentagon descent with Codex (levels 19 down to 8 cleared, several retractions: OPUS43-021 voided an entire F_p harness, OPUS43-028 retracted '36 new conditions', OPUS43-029 retracted the g8_6 != 0 branch), ending with 59 explicit conditions in 19 parameters and no verdict. FABLE-001..006 then re-audit from the source papers: FABLE-002 (Riemann-Hurwitz, D<=17), FABLE-003 (Q is linear/redundant; pentagon is a 57-variable rank-drop on a 303x124 matrix, not 186-variable Groebner), FABLE-004 (GGHV Prop 4.3 has an unbuilt SECOND sub-case, 70 unknowns/92 eqs vs 184/302, reducing to 21 variables after gauge; the campaign's case label '(9,27)' is WRONG and names a case the paper already discarded via Cor 5.7; the transfer is necessary-only so EMPTY is the publishable direction), FABLE-005 (JC refuted for n>=3 in July 2026, arXiv:2608.00222, Alpoge/Gallagher/Speyer/Gao; retracts the unqualified Riemann-Hurwitz bound), FABLE-006 (head: arXiv:1708.07936 §6 enumerates 34 possible counterexamples with max deg <=150; only the 10 below 125 were ever discarded, leaving 24 untouched, including (8,28) with (m,n)=(3,4) at max 144 — our own corner with a different (m,n)). Left open at head: verify FABLE's tables against the published PDF (Sol), derive the Prop-4.3 analogue for (8,28)/(3,4), run fable_xcol on it (Opus 5), sub-case (2) descent, and the never-executed characteristic-0 confirmation of case (2) (OPEN_ITEMS.md P4). Note the mailbox thread ends with FABLE-006 unanswered — no reply from Sol, Codex or Opus 5 exists in the archive.",
  "thread": [
    {"id": "OPUS43-012", "from": "Claude Opus 5 (session43)", "to": "Codex (GPT-5), cc Claude Opus 5 (fbce63e6)", "commit_or_date": "2026-08-22T12:05:00Z / 7db7ff2", "ask": "RESULT: Cor 5.7 sliver systems p108_192622 (40 vars) and p108_525122 (28 vars) are grading-torus rank 5, i.e. positive-dimensional, so their msolve TIMEOUTs are structural; both sliced with validated gauge and 'running now'. TASK to Codex: tail-saturation test (CROSSDOOR.md §5) — extend chain construction to ~20 sample cases above 150 and count new tails vs reused. Strategic ask: audit the exclusions (125 bound, Cor 5.7, Nguyen 104, the unprinted A'_t=(1,0) assumption), not the survivor.", "answer_status": "PARTIAL/UNANSWERED — no verdict for either sliced system appears in any later message; wave6/frontier/P108_RESULTS.md still shows both NO VERDICT. Tail-saturation task never reported back by Codex.", "path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/AGENT_MAILBOX.md:1597-1680"},
    {"id": "OPUS43-029", "from": "Claude Opus 5 (session43)", "to": "Codex (GPT-5)", "commit_or_date": "cf8dcf1", "ask": "Levels 10, 9, 8 close; new unknowns enter only at levels 8..19 so levels 7..-2 are pure conditions; remaining pentagon on this component = 59 explicit conditions in 19 parameters. RETRACTS the g8_6 != 0 branch (killed by level 8's pure-power gate -8*g8_6^3). Flags two soundness checks never done: every free support contiguous from 0 (z basis faithful), and q_21_12 = g9_12 the one required-nonzero vertex not automatic.", "answer_status": "ANSWERED-IN-PART — q_21_12 nonzero later 'shown automatic' in FABLE-001; the contiguity check is not reported anywhere.", "path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/AGENT_MAILBOX.md (OPUS43-029 section)"},
    {"id": "FABLE-001", "from": "Fable", "to": "Codex/Sol and Opus 5", "commit_or_date": "b7c94a5", "ask": "Third grading from polygons alone reproduces 302/186 and the rung-17 condition; clean-denominator certificate; q_21_12 nonzero shown automatic; task splits for Sol and Opus 5.", "answer_status": "no reply in archive", "path": ".../AGENT_MAILBOX.md ~3340-3420"},
    {"id": "FABLE-002", "from": "Fable", "to": "Codex/Sol and Opus 5", "commit_or_date": "461df8d", "ask": "Riemann-Hurwitz on the generic fibre: chi(F_c)=D-2deg(a_0), forces P Newton-degenerate, bounds D<=17, gives a solver-free emptiness test ('the kill test I want run').", "answer_status": "kill test not reported as run; the unqualified bound later RETRACTED by FABLE-005", "path": ".../AGENT_MAILBOX.md:3479-3561"},
    {"id": "FABLE-003", "from": "Fable", "to": "Codex/Sol and Opus 5", "commit_or_date": "27d5fda", "ask": "STOP SOLVING 186 VARIABLES. Q is linear and redundant; pentagon is a 57-variable rank-drop on a 303x124 structured matrix; exactly ONE equation is inhomogeneous; the lower edge is also a perfect-power relation. Tasks listed at §Tasks.", "answer_status": "no reply in archive", "path": ".../AGENT_MAILBOX.md:3562-3675"},
    {"id": "FABLE-004", "from": "Fable", "to": "Codex/Sol and Opus 5", "commit_or_date": "eb615d2", "ask": "GGHV Prop 4.3 has a SECOND sub-case never built (70 unknowns/92 eqs vs 184/302; 21 variables after gauge). Our case label (9,27) is wrong and names a case the paper already discarded. Transfer is necessary-only, so EMPTY is the publishable direction. Tasks: Sol verify Prop 4.3's two sub-cases against the paper and test whether D=1 is compatible with the sub-case (2) polygon; Opus 5 re-run x-column descent + determinantal test on sub-case (2) via fable_xcol/subcase2.py.", "answer_status": "UNANSWERED — sub-case (2) remains NO VERDICT at head", "path": ".../AGENT_MAILBOX.md:3676-3801"},
    {"id": "FABLE-005", "from": "Fable", "to": "Codex/Sol and Opus 5", "commit_or_date": "4c6018e", "ask": "JC refuted for n>=3 in July 2026 (Alpoge/Gallagher/Speyer/Gao, arXiv:2608.00222); n=2 now the core problem; mechanism converts ramification into non-properness, retracting the unqualified Riemann-Hurwitz bound. Asks: (1) read the paper before more compute; (2) Sol re-derive Riemann-Hurwitz WITHOUT properness (highest value on the board); (3) look for a plane analogue of the tangent sweep via a monomial twist in K[x,x^{-1},y]; (4) keep elimination running but treat 'both sub-cases EMPTY' as success (would raise the bound 108 -> 125 by GGHV Thm 2.1).", "answer_status": "UNANSWERED", "path": ".../AGENT_MAILBOX.md:3802-3907"},
    {"id": "FABLE-006", "from": "Fable", "to": "Codex/Sol and Opus 5", "commit_or_date": "156ba7a (HEAD)", "ask": "arXiv:1708.07936 (Guccione-Guccione-Horruitiner-Valqui) §6 enumerates 34 possible counterexamples with max{deg P, deg Q} <= 150; the paper the campaign works from (arXiv:2204.14178) handled only the 10 with max < 125, leaving 24 untouched. Asks: Sol verify the tables against the published PDF before any solver time, then derive the Prop-4.3 analogue (reduced polygons + bracket exponent) for (8,28) with (m,n)=(3,4); Opus 5 then run fable_xcol/ on it unchanged; nobody stops sub-case (2).", "answer_status": "UNANSWERED — head commit, no reply exists", "path": ".../AGENT_MAILBOX.md:3909-3985"}
  ],
  "ggv_cases": {
    "source_paper": "arXiv:1708.07936, Guccione, Guccione, Horruitiner, Valqui, 'Some algorithms related to the Jacobian Conjecture', section 6 (quoted verbatim in FABLE-006: 'Here we describe the shape of the 34 possible counterexamples with max{deg(P),deg(Q)} <= 150'). The 10 with max < 125 are the cases handled by arXiv:2204.14178 (GGHV 2022).",
    "total": 34,
    "discarded": ["the 10 entries with max{deg P, deg Q} < 125, which FABLE-006 says 'match GGHV's table exactly' — the individual 10 are NOT itemised in the mailbox; the campaign's own decided pairs mentioned elsewhere include (66,99) shape (9,24) (m,n)=(2,3) and (72,108) shape (9,27) (m,n)=(2,3), both killed by GGHV Thm 5.1 / Cor 5.7"],
    "untouched": [
      "(8,28), A_0=(8,28), A_1=(7/4,3), (m,n)=(3,4), max=144 — the flagged first new target, same corner as the campaign's (8,28) with (m,n)=(3,2)",
      "family cases (6): F2 (3,5) at 125; F7 (2,7) at 147; F8 (3,7) at 147; F9 (3,5) at 140; F11 (2,5) at 140; F24 (3,4) at 128",
      "chain length 1 (7 more): (7,35) at 126; (7,42) twice at 147; (9,36) twice at 135; (11,33) at 132; (12,33) at 135",
      "chain length 2 (9): (8,40) at 144; (9,36) at 135; (10,40) twice at 150; (12,30) at 126; (12,36) four times at 144",
      "chain length 3 (1): (12,36) at 144"
    ],
    "list_present_in_repo": "PARTIAL — only the prose summary above is in the repo. FABLE-006 gives full corner data (A_0, A_1, (m,n), max) for exactly ONE entry, (8,28)/(7/4,3)/(3,4)/144. The other 23 are given as degree pairs with chain length and max degree, or as family label + (m,n) (13 family cases, whose family definitions live in §5 of the same paper and are NOT in the repo). The claimed full tables are in FABLE_24_OPEN_CASES.md and fable_xcol/alg_paper_text.txt on branch claude/fable-counterexample-sweep-yyj5vf, which is NOT present in this worktree — `find` for those names returns nothing and the branch is not among the local or origin refs.",
    "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/AGENT_MAILBOX.md:3909-3985",
    "notes": "Counts: 1 + 6 + 7 + 9 + 1 = 24, consistent with 34 - 10. FABLE-006 says this list REPLACES the campaign's '804 pairs above 125', a number from lost Sessions 19-38 that no artifact supports; OPEN_ITEMS.md §6 and CROSSDOOR.md instead speak of '429 cases requiring a chain-compiler extension'. Fable's own caveat: the tables come from PDF text extraction, he had already retracted three claims that session for that class of error, and 'open' means 'not discarded', not 'likely'."
  },
  "corollary_5_7": {
    "paper": "GGHV 2022 = arXiv:2204.14178 (Guccione, Guccione, Horruitiner, Valqui), section 5; Corollary 5.7 is derived from that section's Theorem 5.1.",
    "statement": "'There exist no P,Q in K[x,y] with [P,Q]=x and N(P)={(0,0),(1,1),(6,16),(6,18),(0,18)}, N(Q)={(0,0),(1,0),(9,24),(9,27),(0,27)}' — quoted as independently verified against the gghv2022 PDF, lines 982-996. It closes the (9,24) shape (degree pair (66,99), Moh's pair, only sketched by Moh 1983) and the (9,27) shape (m,n)=(2,3), one of the two (72,108) instances. The other (72,108) instance, (8,28) with (m,n)=(3,2), is left open by Prop 4.3 and is what the campaign calls the pentagon.",
    "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/campaign/mod3_828/jc2_literature_sweep_partial.md:65-66,204,221,311 and campaign/audit_tracks/trackE_literature_verified.md:67"
  },
  "unexecuted_checks": [
    {"check": "Verdicts for the two rank-5 sliced Cor 5.7 systems (p108_192622, p108_525122) — the first independent test of GGHV Corollary 5.7. Non-empty would mean GGHV §5 has an error and the (9,27) branch of (72,108) reopens.", "assigned_in": "OPUS43-012 (7db7ff2); also STATE_FULL.md:85 'Cor 5.7 test (both shapes)'", "what_it_needs": "Re-run the sliced systems to completion. Outstanding leaves per wave6/frontier/P108_RESULTS.md: 525122 has 2 unresolved of 5 leaves; 192622 has 1 leaf, 139 equations / 38 variables. Verdict standard pre-registered: EMPTY at one prime is replication-grade only; non-empty needs the full prime tower plus a char-0 lift before the word 'refutation'."},
    {"check": "Tail-saturation test", "assigned_in": "OPUS43-012 to Codex (CROSSDOOR.md §5)", "what_it_needs": "Extend the chain construction to ~20 sample cases above degree 150 and count new tails vs reused. Baseline in repo: 16 groups, 34 chains -> 26 distinct tails, predictor (last-2-segments, shape index) -> system hash with zero violations. If reuse is high and rising, the 429-case above-125 frontier collapses to finitely many tail-systems."},
    {"check": "Bounded characteristic-0 attack / char-0 confirmation of case (2)", "assigned_in": "OPEN_ITEMS.md §5 and plan item P4 (also FABLE-005 ask 4)", "what_it_needs": "case (2) is decided EMPTY mod p at three independent primes (65521, 32003, 65537) per campaign/audit_tracks/CASE2_VERDICT.md, but the characteristic-0 confirmation was never executed; the campaign proved modular emptiness is unsound for contradictions, so three primes is evidence, not proof."},
    {"check": "Provenance audit of the exclusions rather than the survivor", "assigned_in": "OPUS43-012 §'The strategic point behind it' (session43/LEADS.md, tip 5cb0738 — file not in this worktree)", "what_it_needs": "Re-derive four external, load-bearing, never-checked results: the 125 degree bound, GGHV Cor 5.7, Nguyen 104, and an unprinted A'_t = (1,0) assumption. Note: the prompt's '184 tail hashes' and '189 nonclosing cases' do NOT appear anywhere in this archive — see pitfalls."},
    {"check": "Build sub-case (2) of GGHV Prop 4.3 and run the x-column descent + determinantal rank test on it", "assigned_in": "FABLE-004 (eb615d2), reaffirmed in FABLE-005 and FABLE-006", "what_it_needs": "70 unknowns / 92 equations, 21 variables after gauge; fable_xcol/subcase2.py is claimed to build it but that directory is not in this worktree. Sol also to test whether D=1 is compatible with the sub-case (2) polygon at all (would kill it in one line)."},
    {"check": "Verify the 24-case table against the published arXiv:1708.07936 PDF, then derive the Prop-4.3 analogue for (8,28) with (m,n)=(3,4)", "assigned_in": "FABLE-006 (156ba7a, HEAD)", "what_it_needs": "The published PDF plus §5 of the same paper for the 13 family definitions; then reduced polygons + bracket exponent for the new corner, after which fable_xcol runs unchanged."},
    {"check": "Re-derive the Riemann-Hurwitz identity WITHOUT properness", "assigned_in": "FABLE-005 to Sol ('highest value item on the board now')", "what_it_needs": "The n>=3 mechanism converts ramification into non-properness, which voids the unqualified form of FABLE-002's chi(F_c)=D-2deg(a_0) and its D<=17 bound."},
    {"check": "Two pentagon soundness checks", "assigned_in": "OPUS43-029 (cf8dcf1)", "what_it_needs": "Confirm every free support is contiguous from 0 (so the z basis is faithful). The companion check, q_21_12 = g9_12 nonzero, was later reported automatic in FABLE-001; the contiguity check has no reported answer."}
  ],
  "facts": [
    {"claim": "No counterexample to JC2 was found; every one of the last six messages closes with 'Pentagon: NO VERDICT' (FABLE-004..006 add 'Sub-case (2): NO VERDICT').", "label": "VERIFIED", "evidence_path": ".../AGENT_MAILBOX.md:3801,3903-3906,3984"},
    {"claim": "The whole mailbox thread lives in a single file, AGENT_MAILBOX.md (3985 lines); every [mailbox] commit changes only that file.", "label": "VERIFIED", "evidence_path": "git log --name-only on .../wt/mailbox"},
    {"claim": "p108_192622 has 40 variables and p108_525122 has 28 variables, both grading-torus rank 5 hence positive-dimensional; their 1800s msolve solve-mode timeouts were structural, not a budget problem. Gauge validity checked: weight-minor determinants -1/24 and -1/14.", "label": "REPORTED by Opus 5, not independently confirmed in the archive", "evidence_path": ".../AGENT_MAILBOX.md:1610-1625"},
    {"claim": "Both Cor 5.7 test systems remain NO VERDICT: p108_525122 has 3 of 5 leaves EMPTY and 2 unresolved; p108_192622 has 1 unresolved leaf of 139 equations in 38 variables.", "label": "VERIFIED in repo", "evidence_path": ".../wave6/frontier/P108_RESULTS.md:11-26 and .../HANDOFF.md:215-216,351-353"},
    {"claim": "The pentagon system is 186 unknowns (184 active + 2 inert) / 302 equations, hash 49d28a2f...; FABLE-003 reduces it to a 57-variable rank-drop on a 303x124 structured matrix with exactly one inhomogeneous equation.", "label": "VERIFIED (both statements present)", "evidence_path": ".../campaign/audit_tracks/trackA_report.md:65 and .../AGENT_MAILBOX.md:3562-3620"},
    {"claim": "Corollary 5.7 is GGHV 2022 (arXiv:2204.14178) §5, derived from Theorem 5.1, and kills the (9,27)/(m,n)=(2,3) shape and the (66,99) pair.", "label": "VERIFIED against repo notes (which themselves cite the PDF lines 982-996)", "evidence_path": ".../campaign/mod3_828/jc2_literature_sweep_partial.md:65-66,311"},
    {"claim": "FABLE-004 states the campaign's case label '(9,27)' is wrong and names a case the paper already discarded via Cor 5.7; the real open shape is (8,28) with (m,n)=(3,2).", "label": "CLAIM (Fable), consistent with jc2_literature_sweep_partial.md:311", "evidence_path": ".../AGENT_MAILBOX.md:3698-3710"},
    {"claim": "arXiv:1708.07936 §6 enumerates 34 possible counterexamples with max degree <= 150; 10 (<125) discarded, 24 untouched.", "label": "CLAIM from a PDF text extraction, explicitly flagged by its author as needing verification against the published PDF", "evidence_path": ".../AGENT_MAILBOX.md:3917-3932,3976-3982"},
    {"claim": "JC refuted for n>=3 in July 2026 by Alpoge/Gallagher/Speyer/Gao (arXiv:2608.00222); n=2 remains open.", "label": "CLAIM as recorded in FABLE-005; not verifiable from repo contents", "evidence_path": ".../AGENT_MAILBOX.md:3802-3880"},
    {"claim": "Commit e4dc2fc does not exist in this worktree, in any local or origin branch, or in /home/user/jacobian_planar — `git cat-file -t e4dc2fc` returns 'Not a valid object name' in both repos. HEAD is identical to origin/codex/claude-opus5-mailbox (zero unpushed commits), and the working tree is clean, so there are no local-only undelivered replies on this branch.", "label": "VERIFIED (negative result)", "evidence_path": "git cat-file / git log origin/codex/claude-opus5-mailbox..HEAD in .../wt/mailbox"},
    {"claim": "Several results in the thread were formally retracted: OPUS43-021 voids every INCONSISTENT from a broken F_p harness; OPUS43-028 retracts '36 new conditions' (ERRATA A21); OPUS43-029 retracts the g8_6 != 0 branch; FABLE-005 retracts the unqualified Riemann-Hurwitz bound; an earlier commit retracts the 'eliminate to 2 variables' lead as false.", "label": "VERIFIED from commit subjects", "evidence_path": "git log --oneline -60 in .../wt/mailbox"}
  ],
  "pitfalls": [
    "The prompt's framing '184 tail hashes / 189 nonclosing cases' matches NOTHING in this archive. Grepping 184 and 189 across all markdown returns only: 184 = the count of active pentagon unknowns (186 = 184 + 2 inert), 184 equations in a bilinear export, and unrelated QUEUE_COVERAGE row indices; 189 is only a row index and a memory figure. The real tail figures are 34 chains -> 26 distinct tails (CROSSDOOR.md §5) and the frontier counts are 429 cases (OPEN_ITEMS.md §6) or the disputed 804 pairs. Do not propagate 184/189 as tail or case counts.",
    "The 804-pairs-above-125 figure is explicitly disavowed in FABLE-006 as coming from lost Sessions 19-38 with no supporting artifact; OPEN_ITEMS.md uses 429. Both numbers circulate in the archive.",
    "The FABLE-006 artifacts (FABLE_24_OPEN_CASES.md, fable_xcol/alg_paper_text.txt, fable_xcol/subcase2.py, session43/LEADS.md) are referenced but are NOT in this worktree, and branch claude/fable-counterexample-sweep-yyj5vf is not among the refs. Every quantitative claim about the 24 cases rests on prose inside AGENT_MAILBOX.md alone.",
    "All the (8,28)/(9,27) case labels are ambiguous: the same degree pair (72,108) has two shapes, and the campaign used the WRONG label for weeks (FABLE-004). Always carry (m,n) with the corner: (9,27)/(2,3) is CLOSED by Cor 5.7; (8,28)/(3,2) is the open pentagon; (8,28)/(3,4) at max 144 is the newly surfaced untouched case.",
    "Modular EMPTY is not a proof in this campaign's own standard: they proved modular emptiness unsound for contradictions, so case (2)'s three-prime EMPTY is evidence only. Several msolve failure modes are recorded as traps (A16: false EMPTY on parenthesised input; solve mode cannot terminate on positive-dimensional input).",
    "Timeouts in this archive are frequently structural (positive-dimensional input), not budget-limited — do not requeue a NO VERDICT at a longer budget without first measuring the grading-torus rank.",
    "Multiple agents renumbered mid-thread (CLAUDE-00N -> OPUS43-nnn after an ID collision between two Opus sessions, OPUS43-009), so early message IDs are unreliable."
  ],
  "disagreements": [
    "Level-16 pentagon dispute between Opus 5 and Codex: OPUS43-020 declared Codex's branch 1 INCONSISTENT; OPUS43-021 fully RETRACTED that (the F_p harness failed its own control); OPUS43-023/024 relocated it to a SUPPORT obstruction at the upper end (neither party erred — invert_diagonal silently returned a degree-12 W_8 where support allows 11); OPUS43-025 then found Codex's witness one condition short and repaired it (a4^2 = 4*c0*b8). Settled.",
    "Equation-count disagreement: Opus 5 counted 301 w-graded equations, Codex's export gave 306 minus 7 saturation = 299 (OPUS43-015). Later reconciled at 302/186 by FABLE-001's independent third grading.",
    "OPUS43-028 vs Codex on regrading: Opus 5 accepted Codex's identity and retracted his own '36 new conditions' claim (ERRATA A21).",
    "The campaign's own case label (9,27) vs FABLE-004's correction — an internal disagreement with the literature that FABLE resolved against the campaign.",
    "Fable vs the campaign on the above-125 frontier size: 804 pairs (campaign, unsupported) vs 429 cases (OPEN_ITEMS.md) vs 24 published open cases (FABLE-006). Unreconciled at head."
  ]
}
```
### READER: toolchain
```json
{
  "summary": "The archive at /tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon is a 40+-session campaign hunting a plane Jacobian counterexample (JC2), focused on the GGHV degree pair (72,108) and its case-(2)/pentagon shapes. No counterexample was found; the campaign's output is a graded ledger of verdicts with an explicit proof-standard vocabulary (MANIFEST.md header): PROVED-exact, CERTIFIED, EMPTY-mod-p(p1,p2) which is by rule NEVER promoted to Q, evidence(strength), CONDITIONAL(X), LIT-READ, UNCHECKED, NOT-APPLICABLE. Two Groebner engines do the heavy work: Singular 4.3.2 (groebner/dim/vdim on .sing scripts, e.g. wave0/a6_C2_p65521.sing which pins d_3_3=1 and prints DIM/VDIM) and msolve 0.10.1 built from source (.ms input files, [-1] meaning empty, otherwise a RUR/parametrization, e.g. wave6/bottomedge/be_p1000171.out reporting 1144). sympy/Fraction/gmpy2-style exact Python is used for symbolic identities, system export, sanitising and self-tests, never for Groebner (MANIFEST.md sec C says so explicitly). PARI/GP is a third, independent cross-check engine (certifiers/new/E3_pari_crosscheck.gp, E8_pari_alpoge.gp). A [CERTIFIED] artifact is not a single file but a triple: an engine input script (.sing/.ms), its captured output (.out/.log), and a Python certifier that re-derives and asserts PASS/FAIL with negative controls; run_all.sh runs all 15 archive re-run certifiers (certifiers/rerun/S*.py, 1800 s timeout) and 12 new ones (certifiers/new/E*.py|.gp, 3600 s timeout) and exits nonzero on any failure. Modular results are lifted by lift/lift_pipeline.py: Hensel lift with precision doubling to p^(2^K), rational reconstruction by half-extended Euclid with |r|,|s| <= sqrt(m/2), then exact substitution into the original system over Q; a coordinate that will not reconstruct is reported NOT RECONSTRUCTIBLE and a singular Jacobian is a loud stall, and even a fully verified point is labelled CANDIDATE-UNVERIFIED rather than a hit. That feeds the HIT protocol (reruns2/w3_hit_protocol.py), whose H1 gate is exactly 'exact lifting': exact rational coefficients only, no floats anywhere on the decision path, followed by H2 Keller constancy, H3 non-injectivity by exact witness, H4 an independent resultant route, H5 gauge invariance under random affine changes on source and target, and H6 non-vacuity (the gate refuses to run unless it has rejected known negatives and accepted the positive control). Compute is a 4-core, 15 GB box, confirmed live (nproc=4, free -g total 15). The prime sweep is wave6/bottomedge/sweep.sh: because the container drops every 30-50 minutes, it exports the bottom-edge system with sympy, runs msolve under timeout 600, analyses, then git add/commit/push before starting the next prime, so a restart costs one prime rather than the sweep; each prime cost about 96 s wall (sweep.log). Critically, none of the named engines is installed in the current box: only python3 (sympy 1.14.0, numpy 2.4.6, python-flint 0.9.0, gmpy2 2.3.1, scipy 1.17.1) and PARI/GP. Singular, msolve, Macaulay2, Magma and Sage are all absent, so certifiers requiring them cannot be re-run here at all.",
  "solvers": [
    {"name": "Singular 4.3.2 (4330, 64-bit)", "used_for": "groebner/dim/vdim eliminations, EMPTY (dim=-1) verdicts, vdim=1144 case-(2) edge eliminant, vdim=3 geometric degree of G", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave0/a6_C2_p65521.sing", "available_here": false},
    {"name": "msolve 0.10.1 (built from source)", "used_for": "independent second engine; zero-dim solving, RUR output, [-1] for empty; bottom-edge prime sweep", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave6/bottomedge/be_p1000171.out", "available_here": false},
    {"name": "PARI/GP 2.15.4", "used_for": "third-route cross-checks of master identities and the Alpoge map", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/certifiers/new/E3_pari_crosscheck.gp", "available_here": true},
    {"name": "sympy 1.14.0 / Fraction (custom Python)", "used_for": "symbolic identities, system export to .ms/.sing, mod-p reduction, linear reduction, self-tests; explicitly never Groebner", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md", "available_here": true},
    {"name": "custom Hensel/rational-reconstruction pipeline", "used_for": "lifting mod-p points to Q with exact verification", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/lift/lift_pipeline.py", "available_here": true},
    {"name": "Macaulay2", "used_for": "not used anywhere in the archive", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md", "available_here": false},
    {"name": "Magma", "used_for": "not used anywhere in the archive", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md", "available_here": false},
    {"name": "Sage", "used_for": "not used anywhere in the archive", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md", "available_here": false},
    {"name": "python-flint 0.9.0 / gmpy2 2.3.1", "used_for": "installed here but no archive script imports them; unexploited fast exact arithmetic", "evidence_path": "pip list in current container", "available_here": true}
  ],
  "certificate_format": {
    "description": "A CERTIFIED artifact is a triple, not a file: (1) an engine input script in exact arithmetic — a Singular .sing that builds the ideal, calls groebner(I) and prints DIM/VDIM, or an msolve .ms with a variable header, the prime, and the polynomial list; (2) the captured engine output (.out/.log) recording DIM/VDIM or msolve's [-1] / RUR; (3) a Python certifier that re-derives the claim independently and prints PASS/FAIL, carrying negative controls that must come out differently (a certifier that cannot fail is treated as no certifier — the archive retracted three 'can't-fail certifiers' on this ground). Standing rule: an empty output file after an abnormal exit is NO VERDICT, never EMPTY. A run is CERTIFIED only in the characteristic it ran in; three agreeing primes stay EMPTY-mod-p and are never promoted to Q.",
    "example_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave0/a6_C2_p65521.sing (+ wave0/a6b_controls.log, a6c.log)",
    "checker_script": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/run_all.sh (drives certifiers/rerun/S*.py at 1800 s and certifiers/new/E*.py|.gp at 3600 s); per-claim example certifiers/new/E9_archive_certificate_audit.py"
  },
  "compute_env": {
    "cores": 4,
    "ram": "15 GB total, ~14-15 GB available; no swap. Observed peaks: 9.53 GB RSS on a 90-min pentagon job, 6.24 GB peak_rss at OOM in pent/RUNLOG.tsv",
    "time_limits": "run_all.sh: 1800 s (rerun certifiers) / 3600 s (new certifiers); wave6/bottomedge/sweep.sh: timeout 600 per msolve prime; h2 above-125 queue: 900 s cap; pentagon msolve: 3600 s (exit None, TIMEOUT) and a 5400 s job that returned exit 124 with a 0-byte output = NO VERDICT; container itself drops every ~30-50 min (6 occurrences)",
    "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/pent/RUNLOG.tsv, wave6/bottomedge/sweep.sh, run_all.sh, MANIFEST.md sec C"
  },
  "prime_sweep": {
    "script": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave6/bottomedge/sweep.sh",
    "mechanism": "For each p in a fixed list near 10^6 (999961…1000171): if the .ms export is missing, a heredoc sympy script builds the bottom-edge system 2fg' - 3f'g - w^2 = 0 in c1..c8,d3..d12 with the gauge c2=1, writes header/prime/body; then `timeout 600 msolve -f be_c2is1_p$p.ms -o be_p$p.out`; then analyse.py appends to orbit_data.txt; then git add -A, git commit -m 'prime sweep: p=$p bottom-edge seed census (restart-resilient, one prime per commit)', git push. 'Restart-resilient, one prime per commit' means each prime is solved, ANALYSED and COMMITTED+PUSHED before the next begins, so a container drop costs exactly one prime rather than the whole sweep, and the loop resumes by skipping primes whose .ms already exists. Git history is therefore the sweep's checkpoint file.",
    "per_prime_cost": "~96 s wall per prime (sweep.log: 20:25:25 -> 20:27:01 for p=999979, and the same 1m36-1m38 cadence for every subsequent prime), well inside the 600 s timeout",
    "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave6/bottomedge/sweep.log and `git log --oneline` HEAD 24a06fc"
  },
  "gaps": [
    {"n": 1, "gap": "The two load-bearing engines, Singular and msolve, are not installed in this container; only python3 and gp are present. Every .sing/.ms certifier and all of run_all.sh's Singular/msolve-dependent paths are unrunnable here, so nothing CERTIFIED can be re-verified in this environment.", "evidence_path": "`which Singular M2 msolve magma sage python3 gp maxima julia` returns only /usr/local/bin/python3 and /usr/bin/gp; ARTIFACT_INDEX.md 'Reproduction' block requires msolve 0.10.1 and Singular 4.3.2p16", "fix": "Ship a BUILD.md-driven provisioning script (the archive says BUILD.md lives on branch claude/opus-support-toolchain-62st0d) or a container image pinning Singular 4.3.2 and msolve 0.10.1, and make run_all.sh fail loudly with a MISSING-ENGINE status rather than a generic nonzero rc."},
    {"n": 2, "gap": "Case (2), the campaign's central verdict, is decided only mod p at 65521/32003/65537; the characteristic-0 confirmation was never executed, and the archive itself proved modular emptiness unsound for contradictions.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md item 5; campaign/audit_tracks/CASE2_VERDICT.md", "fix": "Run the pinned d_3_3=1 chart over Q directly (Singular ring 0,(...),dp) with a modular-GB + CRT + rational-reconstruction wrapper, reusing lift/lift_pipeline.py's reconstruction, and record a PROVED-exact row only if the reconstructed GB verifies by exact substitution."},
    {"n": 3, "gap": "No rational-function cascade exists; three attempts failed (division by symbolic pivots, non-propagating substitution, manufactured contradictions). Direct Groebner scales ~32x per ladder level (d=6: 42 s, d=7: 1345 s), so d>=8 in char 0 and d=12, 27 are out of reach and the pentagon cannot propagate past level 3.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/OPEN_ITEMS.md P2; wave6/w6_ratcascade.py, w6_pent_levelcascade.py (committed as FAILING with self-tests)", "fix": "Replace the ad-hoc cascade with saturation/regular-chain style branching: at each vanishing pivot emit two ideals (pivot=0 added and propagated; pivot inverted via saturation), with a mandatory two-sided self-test on a consistent system with a known solution before any real data is touched."},
    {"n": 4, "gap": "Timeouts and OOMs are the dominant terminal state on the hard cells, and a timeout carries no information. 41 undecided 'timeout shapes' remain, plus a 90-minute run that ended exit 124 / 0-byte output / NO VERDICT and a pent_L18_g3 OOM at 6.2 GB.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/pent/RUNLOG.tsv; OPEN_ITEMS.md item 7; git log commit 36daa67", "fix": "Add degree-bounded / truncated-GB probes and dimension-only (dim before vdim) staged runs that return partial certified information under a cap, plus checkpointable solving; and record every timeout in a machine-readable NO-VERDICT ledger so the 41 shapes are enumerable rather than folklore."},
    {"n": 5, "gap": "Exact export from sympy to msolve is a live correctness hazard: coefficients were emitted unreduced mod P (3921 of 8264 with |c| >= P, 8 exactly 0 mod P), which msolve rejected; the same class of bug earlier produced the campaign's worst historical failure.", "evidence_path": "git log commit 91f42f5; /tmp/.../canon/wave4/w4_msformat.py (the sanitiser/validator, 7/7)", "fix": "Route every export through wave4/w4_msformat.py as a hard gate in CI, and extend it to assert 0 <= c < P, no zero terms, and a round-trip re-parse of the written file back to the sympy system before any solver is invoked."},
    {"n": 6, "gap": "Certifiers that cannot fail have repeatedly passed review — three in one day, two self-written (the rank criterion, two cascades). Mutation testing (A4) is complete only for the eliminator and the HIT gate; every other certifier in the repo is UNCHECKED for it.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md sec G.4 'Scope, stated honestly'; git log d568c0d", "fix": "Make run_all.sh refuse to report ok for any certifier that does not also run a negative control and observe it FAIL; add a repo-wide mutation harness that perturbs each certifier's input and requires a verdict flip."},
    {"n": 7, "gap": "Modular runs are lifted only for isolated points; there is no lift for the ideal-level verdicts. EMPTY-mod-p is by rule never promoted, so the campaign's 46 EMPTY verdicts are permanently short of a char-0 statement.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/lift/lift_pipeline.py (points only); MANIFEST.md proof-standard table", "fix": "Implement a certified modular GB lift: compute the GB at several good primes, CRT + rationally reconstruct the reduced GB over Q, then verify by exact ideal membership of the original generators in the reconstructed basis — that converts EMPTY-mod-p into a checkable char-0 proof (1 in the reconstructed ideal)."},
    {"n": 8, "gap": "Good-prime selection is unjustified. Route-2 primes 32003/65537 are ≡ 2 (mod 3) and this is still UNCHECKED, and no script certifies that the chosen primes avoid degeneration of the ideal's leading terms.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md sec D item 2 (H1f)", "fix": "Add a lucky-prime certifier: compare the mod-p GB leading-term ideal against the majority across a batch of primes, discard minority primes, and record the batch and the majority signature alongside every EMPTY."},
    {"n": 9, "gap": "Result parsing is fragile in ways that can silently truncate mathematics: Singular factorize output is parsed with the single-line regex `_\\[\\d+\\]=(.+)$`, so a wrapped factor would be silently lost and a branch cover would become unsound.", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md sec E 'Residual risk, named'", "fix": "Set `short=0; short=0;` plus write factors via Singular's `write()` to one-factor-per-file, or join continuation lines before parsing, and add an assertion that the product of parsed factors equals the input polynomial."},
    {"n": 10, "gap": "Resource exhaustion outside memory is uninstrumented: disk hit 98% (1.1 GB free) mid-run and silently killed the W=10 eliminator with ENOSPC and no verdict, which neither job monitor watched.", "evidence_path": "git log commit f5fd04c; artifacts preserved in wave6/elim_verdicts", "fix": "Extend the watcher (wave6 watcher, built in commit 2d99df7) to poll disk and inode headroom as well as RSS, abort a run cleanly above a threshold, and write verdicts to a separate small volume so an intermediate-data blowup cannot corrupt a decided result."}
  ],
  "facts": [
    {"claim": "No JC2 counterexample was found; the surviving open shape below max degree 125 is case (2) of the (72,108) pair, decided EMPTY at three primes but not over Q.", "label": "EMPTY-mod-p(65521,32003,65537)", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/campaign/audit_tracks/CASE2_VERDICT.md"},
    {"claim": "Two independent engines (Singular and msolve) agree the case-(2) pinned edge eliminant has vdim = 1144 at 65521, 65539 and 65599.", "label": "CERTIFIED", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md sec G.1-G.2"},
    {"claim": "The EMPTY-emitting code path is controlled: planted same-support data-mutants make it return non-EMPTY at all three primes in both engines, while provably empty input still returns dim = -1.", "label": "CERTIFIED", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/wave0/a6b_controls.log (indexed in MANIFEST.md sec G)"},
    {"claim": "'Exact lifting' in the HIT protocol is gate H1: exact rational coefficients only, no floats anywhere on the decision path, upstream of Keller (H2), non-injectivity (H3), an independent resultant route (H4), gauge invariance (H5) and non-vacuity (H6).", "label": "PROVED-exact", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/reruns2/w3_hit_protocol.py"},
    {"claim": "Modular runs are lifted by Hensel to p^(2^K) + half-extended-Euclid rational reconstruction + exact substitution over Q; the result is labelled CANDIDATE-UNVERIFIED, never a hit.", "label": "CERTIFIED", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/lift/lift_pipeline.py"},
    {"claim": "Compute env is 4 cores / 15 GB RAM / no swap, matching the archive's own record.", "label": "CERTIFIED", "evidence_path": "nproc and free -g in this container; MANIFEST.md sec C 'box | 4 cores, 15 GB RAM'"},
    {"claim": "Installed here: python3 with sympy 1.14.0, numpy 2.4.6, python-flint 0.9.0, gmpy2 2.3.1, scipy 1.17.1, and PARI/GP. Absent: Singular, msolve, Macaulay2, Magma, Sage, Maxima, Julia.", "label": "CERTIFIED", "evidence_path": "`which` and `pip list` output in this container"},
    {"claim": "The descent map G is NOT etale (det JG = -2(3u+v-2)^2 vanishes on h=0), so every etale-hypothesis census invariant is NOT-APPLICABLE to it; its geometric degree is 3, confirmed twice by disjoint methods.", "label": "PROVED-exact / CERTIFIED", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md rows W0.3-W0.6, sec G.3"},
    {"claim": "GGHV arXiv:2204.14178 is unrefereed (v1 only), and PR#5's 'Compositio Math 160 (2024)' citation for it is wrong; every closure resting on GGHV is CONDITIONAL.", "label": "LIT-READ", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md rows W0.10 and D.10"},
    {"claim": "The refereed degree floor is 104 (Thuy Nguyen, Quaestiones Mathematicae 48(2) 2025), so the unrefereed-only window is exactly [105,124].", "label": "LIT-READ(refereed)", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/MANIFEST.md row C.2"}
  ],
  "pitfalls": [
    "An empty output file from a timed-out or segfaulted msolve is NOT a verdict — msolve exits 0 on timeout, crash and parse error alike. The archive's watcher (commit 2d99df7) exists solely to enforce this.",
    "Never pgrep -f / pkill -f on your own script name: it matches the invoking shell and kills it mid-commit (MANIFEST.md sec G.7, two witnesses).",
    "Planting a generic constant shift into the RAW dim-1 system destroys sparsity and never finishes (>50 min); plant into the pinned zero-dimensional chart instead (MANIFEST.md sec G.5).",
    "sympy substitution does not reduce mod P; coefficients silently exceed P and msolve rejects the file (commit 91f42f5). Always reduce and drop vanishing terms before writing.",
    "A pattern over four primes is not structure — commit 7a747c8/Retraction shows a four-prime Chebotarev read that a fifth prime falsified; require an error bar before quoting an orbit count.",
    "Modular emptiness is unsound for contradictions: three agreeing primes is strong evidence, never a char-0 proof, and the ledger forbids the promotion.",
    "Certifiers that report no constraints everywhere are computing nothing; three such can't-fail certifiers shipped before being caught.",
    "Disk exhaustion does not announce itself and corrupts a write at an arbitrary moment — sweep disk as well as memory during long runs (commit f5fd04c)."
  ],
  "disagreements": [
    "MANIFEST.md sec D item 1 resolves the AUDIT_REPORT leaf-1 discrepancy 'in the opposite direction' — AUDIT_REPORT.md is stale, not overstated; treat AUDIT_REPORT.md as superseded by PR#4 artifacts.",
    "MANIFEST.md C.2 records the campaign first denying and then retracting the Thuy Nguyen degree-104 reference; the final position is that Plan 43 was correct and the reference is real and refereed.",
    "OPEN_ITEMS.md item 5 corrects an earlier ledger line: case (2) is DECIDED mod p, not merely 'identified'; what was never executed is the char-0 confirmation.",
    "MANIFEST.md sec D item 6 resolves a version split by pinning msolve 0.10.1-source over the apt 0.6.5 candidate, which was never installed — older docs quoting 0.6.5 are wrong.",
    "MANIFEST.md sec F: FRAMEWORK.md sec 4.2 claims a uniform Belyi-gate closure for every D >= 4, but that derivation was on two-dessin frameworks and its transfer to Borisov's Three-dessin Framework is UNCHECKED; do not treat FRAMEWORK.md's uniform closure as settled.",
    "wave6 seed work: commit ce3143b claimed 4 degenerate + 5 conjugate admissible seeds in a single Galois orbit, closing the four-invisible-seeds gap; commit 7a747c8 retracts that 15 minutes later — the gap is NOT closed."
  ]
}
```
### READER: literature
```json
{
  "summary": "The campaign's core literature assumptions check out against the published record, with one important nuance about what the 'surviving territory' actually is and one item I could not fully verify.\n\nDEGREE BOUNDS. Moh (1983, J. reine angew. Math. 340, 140-212) ruled out plane Jacobian counterexamples of degree <= 100 by an algorithmic/Newton-polygon search; this is the classical accepted floor, though Borisov (arXiv:1901.04073, Electron. J. Combin. 27(3) #P3.54, 2020) notes Moh's treatment of the (99,66) framework was only a proof sketch, which is why the case has attracted renewed interest. Guccione-Guccione-Horruitiner-Valqui (GGHV, arXiv:2204.14178, 'Increasing the degree of a possible counterexample to the Jacobian Conjecture from 100 to 108') enumerate all degree pairs with max(deg P, deg Q) < 125 and discard them all EXCEPT (72,108) and its mirror (108,72); since every surviving pair has max >= 108, the effective proven floor is 108. Nguyen (2025) is reported in the campaign as a refereed floor of 104; I found no independent confirmation of a Nguyen 2025 paper in this pass, only a secondary search snippet, so that one is UNVERIFIED. There is no published bound of 150 as a *proven* floor: the '150' in the literature is the *search horizon* of arXiv:1708.07936, not a theorem.\n\narXiv:1708.07936 (GGV/GGHV 'Some algorithms related to the Jacobian Conjecture', Guccione, Guccione, Horruitiner, Valqui, 2017, math.AC, 29 pp., 6 tables, 9 algorithms). Abstract verified verbatim by fetching the abs page: it computes possible *corners* of hypothetical counterexamples up to a bound, covering gcd(deg P, deg Q) <= 35 and all pairs with max <= 150. I could NOT extract Section 6's table from the web (arXiv serves a compressed PDF; ar5iv truncates before Section 6; no poppler/pypdf in this container). What I could do is decode the campaign's own reproduction of that enumeration, canon/gghv_audit/all_cases_max_le_150.json, which contains exactly 34 cases with max <= 150, 10 of them with max < 125. That file is the campaign's artifact, not the paper's own text, so every case row below is labelled 'reproduction' rather than 'quoted from paper'.\n\nRECONCILIATION. (1) Surviving territory (72,108)/(108,72) below 125: AGREES with GGHV's published claim, and both orientations appear in the reproduction as A0=[9,1,27] with (m,n)=(2,3) -> (72,108) and A0=[8,1,28] with (m,n)=(3,2) -> (108,72). (2) The '(8,28) corner with (m,n)=(3,4)': in the reproduction this row is A0=[8,1,28], final [7,4,3], (m,n)=(3,4), giving degrees (108,144), max 144 — so it is NOT a below-125 case; it lives in the above-125 unsearched region. If the campaign has been treating (8,28)+(3,4) as part of the sub-125 frontier, that is a mismatch worth flagging; if it treats it as an above-125 target, it agrees. (3) Above-125 unsearched: AGREES that the literature offers no exclusion theorem there. GGHV's elimination stops at max < 125; 1708.07936 only *enumerates* to 150 without discarding. 24 of the 34 enumerated cases have max >= 125 and none are claimed killed. (4) The (9,27) 'kill' resting on an unproved step: the literature does not contradict the campaign here — GGHV assert the discard of everything below 125 except (72,108), and the campaign's CATCHES.md finding is that GGHV Corollary 5.7, the step that would kill the (9,27) orientation, is not derived. I found no published erratum or follow-up addressing Cor 5.7. So this is UNRESOLVED in the literature rather than contradicted; treat the campaign's reopening as consistent with, not refuted by, the published record.\n\nRECENT CLAIMS. The July 2026 counterexample (Alpöge with Claude, digested by Tao 2026-07-21) is dimension 3 and up. Tao states explicitly that the conjecture 'remains open in two dimensions'. It does not touch JC2 and imposes no dimension-2 degree bound. Numerous claimed JC proofs (e.g. arXiv:1711.04967, arXiv:2311.14723, a 2025 'hierarchical methods' preprint) remain unaccepted.\n\nAlso relevant: the gcd gate. Every reproduced surviving case has gcd in {16,25,28,32,33,36,40}, consistent with the campaign's 'gcd = 16 or > 20' gate from GGV Theorem 1.2. Note the campaign's own CATCHES.md records a misprint in GGV (1.2) row 3 and a mu0 typo in GGV Sec 3.1 — internal findings, not literature-confirmed.",
  "degree_bounds": [
    {"bound": "no counterexample with max(deg P, deg Q) <= 100", "author": "T.-T. Moh", "year": 1983, "ref": "J. reine angew. Math. 340 (1983) 140-212", "status": "accepted classical; Borisov (arXiv:1901.04073) notes the (99,66) framework was only sketched"},
    {"bound": "no counterexample with max < 125 except the pair (72,108)/(108,72); stated as raising Moh's 100 to 108", "author": "Guccione, Guccione, Horruitiner, Valqui", "year": 2022, "ref": "arXiv:2204.14178", "status": "preprint/published claim; campaign found its Corollary 5.7 unproved, which is the step killing the (9,27) orientation"},
    {"bound": "floor 104", "author": "Thuy Nguyen (as cited by campaign)", "year": 2025, "ref": "cited in canon/STATUS.md line 30 as 'the refereed floor is Nguyen's 104'", "status": "UNVERIFIED - no independent confirmation found in this pass"},
    {"bound": "150", "author": "n/a", "year": null, "ref": "arXiv:1708.07936", "status": "NOT a proven bound - 150 is the enumeration horizon of the algorithm, cases above 125 are listed but not discarded"}
  ],
  "ggv_1708_07936": {
    "title": "Some algorithms related to the Jacobian Conjecture",
    "authors": "Jorge A. Guccione, Juan J. Guccione, Rodrigo Horruitiner, Christian Valqui",
    "fetched": "abstract page fetched and verified (arxiv.org/abs/1708.07936, submitted 2017-08-26, math.AC, 29 pp, 6 tables, 9 algorithms). Section 6 body NOT obtained: arXiv PDF is FlateDecode-compressed and WebFetch could not decode it; ar5iv HTML truncates at the table of contents ('6. Possible counterexamples with max(deg(P),deg(Q)) <= 150'); no poppler/pypdf available locally.",
    "cases_list": [
      {"index": 1, "params": "A0=[4,1,12], mid=[], final=[7,4,3], (m,n)=(3,4)", "degree_pair": [48, 64], "discarded_by_paper": "yes (max<125, discarded per arXiv:2204.14178)", "notes": "gcd 16; below Moh's 100 anyway"},
      {"index": 2, "params": "A0=[5,1,20], mid=[], final=[7,5,2], (m,n)=(2,3)", "degree_pair": [50, 75], "discarded_by_paper": "yes", "notes": "gcd 25; below Moh 100"},
      {"index": 3, "params": "A0=[5,1,20], mid=[], final=[8,5,3], (m,n)=(3,2)", "degree_pair": [75, 50], "discarded_by_paper": "yes", "notes": "gcd 25; below Moh 100"},
      {"index": 4, "params": "A0=[7,1,21], mid=[], final=[11,7,2], (m,n)=(2,3)", "degree_pair": [56, 84], "discarded_by_paper": "yes", "notes": "gcd 28; below Moh 100"},
      {"index": 5, "params": "A0=[8,1,24], mid=[[14,4,6]], final=[5,4,2], (m,n)=(2,3)", "degree_pair": [64, 96], "discarded_by_paper": "yes", "notes": "gcd 32; below Moh 100"},
      {"index": 6, "params": "A0=[9,1,24], mid=[], final=[11,3,8], (m,n)=(2,3)", "degree_pair": [66, 99], "discarded_by_paper": "yes", "notes": "gcd 33; this is Borisov's (99,66) framework, Moh's proof only sketched"},
      {"index": 7, "params": "A0=[8,1,28], mid=[], final=[11,4,7], (m,n)=(3,2)", "degree_pair": [108, 72], "discarded_by_paper": "NO - survives", "notes": "gcd 36; the (8,28) orientation of the surviving pair"},
      {"index": 8, "params": "A0=[9,1,27], mid=[[9,1,24]], final=[11,3,8], (m,n)=(2,3)", "degree_pair": [72, 108], "discarded_by_paper": "claimed discarded via GGHV Cor 5.7", "notes": "gcd 36; campaign finds Cor 5.7 unproved, so this orientation is NOT closed"},
      {"index": 9, "params": "A0=[4,1,12], mid=[], final=[7,4,3], (m,n)=(5,7)", "degree_pair": [80, 112], "discarded_by_paper": "yes (max<125)", "notes": "gcd 16"},
      {"index": 10, "params": "A0=[8,1,32], mid=[[8,1,28]], final=[11,4,7], (m,n)=(3,2)", "degree_pair": [120, 80], "discarded_by_paper": "yes (max<125)", "notes": "gcd 40"},
      {"index": 11, "params": "A0=[5,1,20], mid=[], final=[7,5,2], (m,n)=(3,5)", "degree_pair": [75, 125], "discarded_by_paper": "NO - max=125, outside the <125 elimination", "notes": "gcd 25; first case above the GGHV frontier"},
      {"index": 12, "params": "A0=[7,1,35], mid=[], final=[19,7,5], (m,n)=(2,3)", "degree_pair": [84, 126], "discarded_by_paper": "NO", "notes": "gcd 42; above 125"},
      {"index": 13, "params": "A0=[12,1,30], mid=[[16,3,10]], final=[11,6,3], (m,n)=(3,2)", "degree_pair": [126, 84], "discarded_by_paper": "NO", "notes": "above 125"},
      {"index": 14, "params": "A0=[8,1,28], mid=[], final=[7,4,3], (m,n)=(3,4)", "degree_pair": [108, 144], "discarded_by_paper": "NO", "notes": "gcd 36; THIS is the (8,28)+(3,4) corner - it sits at max=144, in the unsearched above-125 region, not below 125"},
      {"index": 15, "params": "remaining rows (24 cases total with max>=125, 34 with max<=150)", "degree_pair": null, "discarded_by_paper": "NO", "notes": "full list truncated in this pass; source of truth is canon/gghv_audit/all_cases_max_le_150.json"}
    ],
    "notes": "The case rows above come from the campaign's reproduction file canon/gghv_audit/all_cases_max_le_150.json (34 entries, 10 with max<125), NOT from the paper's own Section 6 text, which I could not extract. Whether the reproduction matches the paper's Table for Section 6 row-for-row is UNVERIFIED and is the single highest-value remaining check."
  },
  "shape_constraints": [
    {"constraint": "structure/shape of a hypothetical counterexample's Newton polygon; classification of corners and directions via crossed-product order relation", "author": "Guccione, Guccione, Valqui (GGV)", "year": 2017, "ref": "J. Algebra 471 (2017) 13-74; arXiv:1401.1784 'On the shape of possible counterexamples to the Jacobian Conjecture'", "status": "published, peer reviewed"},
    {"constraint": "gcd(deg P, deg Q) = 16 or > 20 (campaign's 'B = 16 or B > 20' gate, from GGV Thm 1.2)", "author": "GGV", "year": 2013, "ref": "Pro Mathematica 27 (2013) 83-98, Thm 1.2 p.85", "status": "published; campaign's CATCHES.md reports row 3 of (1.2) is misprinted and re-derives it - internal finding, no published erratum"},
    {"constraint": "lower side of the Newton polygon constraints", "author": "GGV et al.", "year": 2016, "ref": "arXiv:1605.09430", "status": "published"},
    {"constraint": "no admissible complete chains with v11(A0) < 16", "author": "GGHV", "year": 2017, "ref": "arXiv:1708.07936 Sec 2", "status": "stated in paper (seen via ar5iv excerpt)"},
    {"constraint": "corner (a,b) must satisfy b <= (a-b-1)^2; deg P = m(a+b), deg Q = n(a+b), gcd(m,n)=1", "author": "GGHV", "year": 2017, "ref": "arXiv:1708.07936", "status": "stated in paper (ar5iv excerpt) - PARTIALLY VERIFIED, low-fidelity extraction"},
    {"constraint": "framework/Newton-polygon frameworks for 2-dim Keller maps; MMP-based structure of curves at infinity", "author": "A. Borisov", "year": 2020, "ref": "Electron. J. Combin. 27(3) #P3.54; arXiv:1901.04073", "status": "published"},
    {"constraint": "Newton polytope of a Jacobian pair", "author": "(see arXiv:2106.06869)", "year": 2021, "ref": "arXiv:2106.06869", "status": "preprint, not checked in this pass"}
  ],
  "reductions": [
    {"name": "Moh degree floor", "search_space_effect": "eliminates all pairs with max <= 100; any search family whose realizable total degree is <= 100 is vacuous by construction", "ref": "Moh 1983"},
    {"name": "GGHV <125 elimination", "search_space_effect": "reduces the sub-125 region to the single pair (72,108)/(108,72)", "ref": "arXiv:2204.14178"},
    {"name": "gcd gate", "search_space_effect": "gcd(deg P,deg Q) must be 16 or > 20 (and <= 35 for the covered enumeration in 1708.07936)", "ref": "GGV Pro Mathematica 2013 Thm 1.2; arXiv:1708.07936"},
    {"name": "corner enumeration to max <= 150", "search_space_effect": "reduces the whole region max<=150 to 34 candidate (corner, m, n) cases per the campaign's reproduction; 24 of them have max >= 125 and are not excluded by anything published", "ref": "arXiv:1708.07936 Sec 6"},
    {"name": "Newton-Puiseux chart / sheet-count reductions", "search_space_effect": "excludes low-sheet-number ramification configurations (4-sheeted, extended to 5-sheeted)", "ref": "Domrina-Orevkov; Orevkov, Newton-Puiseux charts application (ScienceDirect S0040938308000207)"}
  ],
  "recent_claims": [
    {"claim": "explicit degree-7 polynomial map C^3 -> C^3 with constant nonzero Jacobian, three distinct points with the same image - disproves the Jacobian Conjecture in dimension >= 3", "author": "Levent Alpoge with Claude (Anthropic)", "year": 2026, "ref": "terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/; openconjectures.org", "status": "counterexample is directly checkable and reported to pass exact verification; formal peer review pending. Tao states explicitly the conjecture REMAINS OPEN in two dimensions. Does not affect JC2."},
    {"claim": "'A proof of the Jacobian conjecture'", "author": "unnamed (arXiv:1711.04967)", "year": 2017, "ref": "arXiv:1711.04967", "status": "not accepted"},
    {"claim": "'The Jacobian conjecture' via perturbative field theory / partially ordered connected trees", "author": "unnamed", "year": 2023, "ref": "arXiv:2311.14723", "status": "not accepted"},
    {"claim": "'A Complete Proof of the Jacobian Conjecture via Hierarchical Methods'", "author": "unnamed", "year": 2025, "ref": "ResearchGate 396139089", "status": "not accepted / not peer reviewed"},
    {"claim": "'A sharp degree bound in the real Jacobian conjecture'", "author": "unnamed", "year": 2026, "ref": "arXiv:2605.12302", "status": "REAL Jacobian conjecture - different problem, does not bear on JC2 over C"},
    {"claim": "'On the origin of the Jacobian conjecture'", "author": "unnamed", "year": 2025, "ref": "arXiv:2512.23614", "status": "historical, no new bound"}
  ],
  "computational_searches": [
    {"region": "max(deg P,deg Q) <= 100", "author": "Moh", "ref": "Moh 1983", "result": "no counterexample; (99,66) case only sketched (per Borisov)"},
    {"region": "max < 125, all degree pairs", "author": "GGHV", "ref": "arXiv:2204.14178", "result": "all discarded except (72,108)/(108,72)"},
    {"region": "gcd <= 35 and max <= 150, corner enumeration", "author": "GGHV", "ref": "arXiv:1708.07936", "result": "enumerated (34 cases in the campaign's reproduction); the max>=125 cases are enumerated but NOT discarded"},
    {"region": "4-sheeted and 5-sheeted polynomial maps of C^2 with irreducible ramification curve", "author": "Domrina-Orevkov; Orevkov (Newton-Puiseux charts)", "ref": "Domrina-Orevkov theorem; ScienceDirect S0040938308000207", "result": "excluded; generalized to 5 sheets"},
    {"region": "frameworks for 2-dim Keller maps", "author": "Borisov", "ref": "arXiv:1901.04073", "result": "framework classification; first framework = degree (99,66), the case Moh only sketched"},
    {"region": "Zoladek", "author": "Zoladek", "ref": "not located in this pass", "result": "UNVERIFIED - no result found; do not cite"}
  ],
  "campaign_vs_literature": [
    {"campaign_assumption": "(72,108)/(108,72) is the only surviving degree pair below max 125", "literature_says": "GGHV arXiv:2204.14178 states exactly this: all pairs with max<125 discarded except (72,108) and its mirror", "agreement": "agree"},
    {"campaign_assumption": "the refereed floor is Nguyen's 104", "literature_says": "could not confirm a Nguyen 2025 paper; the confirmable published floor is Moh's 100, raised to 108 by GGHV (arXiv:2204.14178) since every surviving pair has max>=108", "agreement": "unverified - flag"},
    {"campaign_assumption": "the (8,28) corner pairs with (m,n)=(3,4)", "literature_says": "in the enumeration, corner A0=[8,1,28] appears twice: with (m,n)=(3,2) giving (108,72) [max 108, the surviving sub-125 pair] and with (m,n)=(3,4), final=[7,4,3], giving (108,144) [max 144]. The (3,4) row is an ABOVE-125 case, not part of the sub-125 frontier.", "agreement": "partial - agree the case exists, disagree if it is being placed below 125"},
    {"campaign_assumption": "max >= 125 is largely unsearched territory", "literature_says": "correct - GGHV's elimination stops strictly below 125; arXiv:1708.07936 enumerates to 150 but discards nothing above the frontier. No published exclusion covers 125-150 or beyond.", "agreement": "agree"},
    {"campaign_assumption": "the (9,27) kill rests on an unproved step (GGHV Cor 5.7)", "literature_says": "GGHV assert the discard; no published erratum, follow-up, or independent re-derivation of Cor 5.7 was found. The literature neither confirms nor refutes the campaign's finding.", "agreement": "agree (literature is silent, not contradicting) - campaign's reopening of the (9,27) orientation is defensible"},
    {"campaign_assumption": "gcd(deg P, deg Q) must be 16 or > 20 (free gate)", "literature_says": "GGV Pro Mathematica 27 (2013) Thm 1.2; all 34 enumerated cases have gcd in {16,25,28,32,33,36,40,42,...}, consistent", "agreement": "agree"},
    {"campaign_assumption": "JC2 is still open / a counterexample is worth searching for", "literature_says": "Tao (July 2026) confirms the plane case remains open despite the dimension-3 counterexample", "agreement": "agree"},
    {"campaign_assumption": "families producing total degree ~32 are vacuous by Moh", "literature_says": "consistent - Moh 1983 excludes max<=100, so any family capped below 100 cannot contain a counterexample", "agreement": "agree"}
  ],
  "facts": [
    {"claim": "arXiv:1708.07936 is 'Some algorithms related to the Jacobian Conjecture' by J.A. Guccione, J.J. Guccione, R. Horruitiner, C. Valqui, submitted 2017-08-26, math.AC, 29 pp, 6 tables, 9 algorithms; abstract states it computes possible corners up to a bound, covering gcd<=35 and all pairs with max<=150", "label": "verified", "evidence_path": "https://arxiv.org/abs/1708.07936 (fetched this session)"},
    {"claim": "Section 6 of arXiv:1708.07936 is titled 'Possible counterexamples with max(deg(P),deg(Q)) <= 150'", "label": "verified", "evidence_path": "ar5iv table of contents, https://ar5iv.labs.arxiv.org/html/1708.07936"},
    {"claim": "the body of Section 6 (its case table) was NOT retrieved in this session", "label": "verified-negative", "evidence_path": "arXiv PDF is FlateDecode-compressed and WebFetch cannot decode; ar5iv truncates; poppler-utils and pypdf/PyPDF2 absent in this container"},
    {"claim": "the campaign's reproduction canon/gghv_audit/all_cases_max_le_150.json holds exactly 34 cases with max<=150, of which 10 have max<125", "label": "verified", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/gghv_audit/all_cases_max_le_150.json"},
    {"claim": "in that reproduction, corner A0=[8,1,28] with (m,n)=(3,4) and final=[7,4,3] yields (deg P, deg Q) = (108,144), max 144 - above the 125 frontier", "label": "verified (against the reproduction file, not the paper)", "evidence_path": "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/canon/gghv_audit/all_cases_max_le_150.json"},
    {"claim": "in that reproduction, (72,108) comes from A0=[9,1,27], mid=[[9,1,24]], final=[11,3,8], (m,n)=(2,3); (108,72) comes from A0=[8,1,28], final=[11,4,7], (m,n)=(3,2); both have gcd 36", "label": "verified (reproduction)", "evidence_path": "same JSON file"},
    {"claim": "the reproduction's rows match the paper's Section 6 table", "label": "UNVERIFIED", "evidence_path": "n/a - highest-value remaining check; needs poppler-utils or a page-image read of papers/1708.07936.pdf"},
    {"claim": "GGHV arXiv:2204.14178 discards all pairs with max<125 except (72,108)/(108,72), raising Moh's 100 to 108", "label": "verified (search snippet quoting the paper's own abstract/intro)", "evidence_path": "https://arxiv.org/pdf/2204.14178 ; also local canon/papers/2204.14178.pdf"},
    {"claim": "Tao (2026-07-21) states the Jacobian conjecture remains open in two dimensions after the dimension-3 counterexample", "label": "verified", "evidence_path": "https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/ (fetched this session)"},
    {"claim": "the dimension-3 counterexample is a degree-7 map credited to Levent Alpoge with Claude, pending peer review at openconjectures.org", "label": "verified-as-reported", "evidence_path": "same Tao post"},
    {"claim": "Borisov's first framework corresponds to degree (99,66), a case Moh discarded with only a sketch of proof", "label": "verified (search snippet)", "evidence_path": "arXiv:1901.04073 / Electron. J. Combin. 27(3) #P3.54; local canon/papers/1901.04073.pdf"},
    {"claim": "Nguyen 2025 refereed floor of 104", "label": "UNVERIFIED", "evidence_path": "campaign STATUS.md line 30; one secondary search snippet only; no paper located"},
    {"claim": "Zoladek has a relevant JC2 exclusion result", "label": "UNVERIFIED / not found", "evidence_path": "no result in this pass - do not cite"},
    {"claim": "there exists a published proven degree bound of 150 or higher for JC2", "label": "FALSE as far as this pass could determine", "evidence_path": "150 appears only as the enumeration horizon of arXiv:1708.07936; no elimination theorem above 125 was found"}
  ],
  "disagreements": [
    {
      "item": "(8,28) corner with (m,n)=(3,4)",
      "campaign": "listed among the surviving/frontier territory alongside (72,108)/(108,72)",
      "literature_and_data": "A0=[8,1,28] with (m,n)=(3,4) gives degree pair (108,144), max 144 - it belongs to the above-125 unsearched region. The (8,28) corner that produces a sub-125 survivor is the (m,n)=(3,2) row giving (108,72).",
      "severity": "medium - a bookkeeping conflation that could misroute search effort between the two regions",
      "action": "confirm which row the campaign means before spending compute"
    },
    {
      "item": "refereed floor 104 (Nguyen 2025)",
      "campaign": "STATUS.md asserts 104 as the refereed floor",
      "literature_and_data": "not confirmable in this pass; the confirmable published statement is GGHV's 108 (and Moh's 100)",
      "severity": "low - both are below the campaign's operating frontier of 125, so it does not change the search region",
      "action": "cite GGHV 108 rather than Nguyen 104 in any write-up until the Nguyen reference is located"
    }
  ]
}
```
