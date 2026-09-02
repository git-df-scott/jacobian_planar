```json
{
  "results": [
    {
      "id": "P1",
      "status": "VERIFIED",
      "evidence": "$WT/canon/gghv_audit/all_cases_max_le_150.json parsed with python3: top-level JSON list, len=34; sum(max<125)=10; two records have A0=[8,1,28] and the one with (m,n)=(3,4) has final=[7,4,3], deg_P=108, deg_Q=144, max=144 (the other is (m,n)=(3,2), final [11,4,7], (108,72)).",
      "correction": ""
    },
    {
      "id": "P2",
      "status": "VERIFIED",
      "evidence": "$WT/canon/wave6/frontier_151_300_map.json: list of 432 entries, each [max, label, status]; Counter of status field = {'NO-CHAIN':429, '0-blocked':1, 4:1, 2:1}. Example entry: [156, \"(13,39)/25/13,3\", \"NO-CHAIN\"].",
      "correction": ""
    },
    {
      "id": "P3",
      "status": "VERIFIED",
      "evidence": "$WT/canon/CROSSDOOR.md:69-80 (§5 'Tail-closure (frontier finiteness)'): 'ZERO violations across every system ever generated here (16 groups). Current library: 34 chains -> 26 distinct tails.' and line 80: 'Test: extend compiler on 20 sample cases across (150,300], count new tails vs reused.' `find $WT -iname '*tail*'` returns nothing — no results file for the 20-sample test exists in any checkout.",
      "correction": "Note the predictor is stated as a heuristic conjecture ('Conjecture: the tail set SATURATES'), zero-violation on already-generated systems only — not a proof."
    },
    {
      "id": "P4",
      "status": "PARTLY",
      "evidence": "$WT/canon/CATCHES.md:517-604 contains the section 'GGHV COROLLARY 5.7 IS UNPROVEN...'; lines 568-571 give the bracket computation [psi phi P, psi phi Q] = 1/2 + (lambda/2)x^{-1/2} 'NOT in K^x'; lines 591-595: '21 conditions on P and 45 on Q, 66 in all ... So 51 of the 66 conditions rest on the invalid step ... 15 delivered, 51 unsupported'; line 604: 'The failure is localised to one sentence: gghv.txt:1430-1433.'",
      "correction": "gghv.txt does NOT exist anywhere in the checkouts or in /home/user/jacobian_planar (`find ... -name 'gghv*.txt'` returns nothing), so the cited lines 1412-1433 cannot be inspected here. The line-number citation is unverifiable from disk; the CATCHES.md argument itself is self-contained and readable."
    },
    {
      "id": "P5",
      "status": "VERIFIED",
      "evidence": "$WT/canon/CATCHES.md:615 'GGV (1.2) ROW 3 IS MIS-PRINTED IN THE PAPER, AND THE CAMPAIGN COPIED IT'; :626 printed row 'mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0)'; :637 corrected 'mu3*A''(0) = -6*mu1 -- NO q1''(0) term'; :651 'printed minus truth = -4*F'(0)*mu3 = -2*mu3*q1''(0), the spurious term'; :685-688 'WHAT IS VOID. Every B=16 EMPTY row in STATE_FULL.md section A ... VOID'; :1422-1428 'd = 7 IS EMPTY IN CHARACTERISTIC ZERO ... 26 equations / 20 unknowns ... 1345.48 s, 6.67 GB. Verdict [-1] = EMPTY'; :1891 'the B = 16 ladder EMPTY in characteristic zero for d = 3..7'.",
      "correction": ""
    },
    {
      "id": "P6",
      "status": "VERIFIED",
      "evidence": "ls shows $WT/canon/wave5/ms/m16_d8_p1000003.ms, m16_d8_p1000033.ms, m16_d8_q.ms. m16_d8_q.ms line 1 (variable list) has 23 names (a3..a16, b2..b7, mu0, mu3, t); line 2 is the characteristic '0'; remaining 30 nonempty lines are the equations (last is 'mu0*t-1', the Rabinowitsch saturation). So 30 equations / 23 unknowns. $WT/canon/wave6/w6_seed_d8.py exists (3485 bytes).",
      "correction": "The 23rd unknown t and the final generator mu0*t-1 are the saturation variable/equation, not an independent chart unknown — worth noting when quoting '30/23'."
    },
    {
      "id": "P7",
      "status": "PARTLY",
      "evidence": "$WT/pq/trackB1_pentagon.py:432 `def witness():`; docstring lines 433-457: exact witness P = Stilde^2, Q = Stilde^3, Stilde = y^4*(1+(xy)^4) + t*x^4*y^7, t=1, all Fractions (file line 22: 'Everything exact over Q (fractions.Fraction); mod-p is scouting evidence only'). It certifies 'every normalized weight truncation W >= 8 is ALIVE' and that any death of case (1) must use equations of weight <= 7.",
      "correction": "The certified claim is W >= 8 alive (all truncations of weight at least 8), not specifically 'W=12..19 non-empty'. W=12..19 is a subset of what is claimed, but the file never names that range in witness(); do not cite 12..19 as the file's statement."
    },
    {
      "id": "P8",
      "status": "VERIFIED",
      "evidence": "$WT/canon/STATUS.md:206-207 'eliminant degree 1144 ... squarefree yes (gcd(f,f')=1)'; :218-235 §2.5 'The eliminant is irreducible over Q [PROVED-exact]' via Dedekind's criterion at 8 good primes (100003, 100019, 100043, 100057, 100069, 100103, 100109, 100129; all degree-sums 1144), 'Surviving proper-factor degrees: none', with reducibility-detection controls; :240 'Does not prove: case (2) empty over Qbar — that needs the residual system, 13'; :271 'residual system — 13 variables over a degree-1144 field — unsolved'. $WT/canon/STATE_FULL.md:30 'residual over K route planned, NEVER EXECUTED** [MISS-4...]' and :66 'case-2 Q-bar ranks [MISS-4]'.",
      "correction": ""
    },
    {
      "id": "P9",
      "status": "PARTLY",
      "evidence": "$WT/mailbox/wave6/frontier/P108_RESULTS.md:11 '`p108_525122` | 28 var / 140 eq | TIMEOUT | NO VERDICT — 5 leaves: **3 EMPTY**, 2 unresolved'; :12 '`p108_192622` | — | TIMEOUT | NO VERDICT — 1 leaf unresolved (139 eq / 38 var)'; :26 same figures restated; :37 'final unresolved leaves are labelled \"both engines: no verdict\"'. The .ms files exist: $WT/p11/wave6/ms/p108_525122.ms and $WT/p11/wave6/ms/p108_192622.ms (plus .gens/.out/_dump.sing/_long.* siblings, and p108_843700/p108_821326).",
      "correction": "The .ms files live under $WT/p11/wave6/ms/, NOT under canon/wave6 — there is no canon/wave6/ms copy of them and no canon/wave6/frontier directory at all."
    },
    {
      "id": "P10",
      "status": "PARTLY",
      "evidence": "Both files exist: $WT/canon/wave6/w6_plane_sweep.py (8811 B) and w6_plane_sweep_search.py (3953 B). Sweep ansatz (w6_plane_sweep.py:14-16 docstring, code lines ~50-60): S(gamma,w) = (p(w) + 2*gamma, q(w) + gamma*w) with q'(w) = (w/2)p'(w), det J(S) = 2*gamma — S is AFFINE-LINEAR in gamma. Twist ansatz (w6_plane_sweep_search.py:10-13): phi:(x,y)->(gamma,w) with gamma = c0 + a*x^al*y^be, w = gamma*u, u = 1 + b*x^mu*y^nu, C = gamma*x^s; F = (P/C^i, Q/C^j); side condition C*2*gamma*detJphi - j*Q*{P,C} + i*P*{Q,C} = kappa*C^(i+j+1) solved by Groebner over Q saturated by kappa!=0, a!=0. Its own docstring lines 21-23 disclaim: 'No solution over the searched shapes is NOT a proof that none exists; it bounds the shape family only.' CATCHES.md:1355 'THE SWEEP MECHANISM IS DEAD IN THE PLANE'; dichotomy at :1385-1405: (a) det(Delta,Delta')!=0 — the twist argument is stated only 'with w = gamma*u the twisted Jacobian is u^2 * Psi(gamma,u) * {gamma,u}'; (b) det(Delta,Delta')=0 gives a triangular automorphism.",
      "correction": "Branch (a) is NOT proved for general (C,i,j): the killing argument is written for the specific substitution w = gamma*u (implicitly C = gamma*x^s style twists), not for an arbitrary divisor C with arbitrary exponents i,j. Elsewhere CATCHES.md:827-876 treats (i,j) only as an explicit finite list — '(i,j) in {(1,2),(1,1),(0,1),(2,3)}, deg p <= 3' (line 844) and 'verified symbolically for (i,j) = (1,2),(2,1),(1,1),(2,3),(3,1)' (line 876). So 'THE SWEEP MECHANISM IS DEAD IN THE PLANE — COMPLETELY' overstates: branch (b) is general, branch (a) is shape-restricted."
    },
    {
      "id": "P11",
      "status": "CONTRADICTED",
      "evidence": "`grep -rl '164 variables' $WT` returns nothing (that part holds). But `grep -rl '\\b288\\b' $WT | wc -l` = 802 files and `grep -rl '6821' $WT | wc -l` = 733 files. And trackB1_sat_Q.ms IS present on disk: $WT/mailbox/wave6/frontier/trackB1_sat_Q.ms. The directory $WT/canon/wave6/frontier/ does not exist at all (ls: No such file or directory), so the canon-path assertion is vacuous rather than informative.",
      "correction": "Only the '164 variables' string is genuinely absent. '288' and '6821' occur in hundreds of files, and trackB1_sat_Q.ms exists under mailbox/wave6/frontier — a plan must not assume that artifact is missing. Note the two literal-number greps are string matches, not semantic checks of the intended claims."
    },
    {
      "id": "P12",
      "status": "VERIFIED",
      "evidence": "Both $WT/p11/reruns2/w3_hit_protocol.py and $WT/canon/reruns2/w3_hit_protocol.py exist. Docstring lines 1-33 list the gate: H1 EXACTNESS, H2 KELLER (det J nonzero constant), H3 NON-INJECTIVITY, H4 NOT AN AUTOMORPHISM (independent resultant route), H5 GAUGE INDEPENDENCE, H6 NON-VACUITY (must reject known negatives, accept positive control; module refuses to run otherwise). 'A candidate is reported as a HIT only if H1-H5 all pass and H6 held.'",
      "correction": ""
    },
    {
      "id": "P13",
      "status": "VERIFIED",
      "evidence": "$WT/canon/lift/lift_pipeline.py exists (8059 B). Line 2: 'T4 -- Hensel lift + rational reconstruction + exact verification.' Functions: _rref_mod (41), _is_unit (69), hensel_lift (74), rational_reconstruct (109), reconstruct_point (129), verify_exact (139), pipeline (148), controls (169). All operate on a point x0 (reconstruct_point / verify_exact substitute a point into polys); no ideal-level or Groebner-basis lifting appears.",
      "correction": ""
    },
    {
      "id": "P14",
      "status": "VERIFIED",
      "evidence": "`which Singular msolve` printed nothing, exit code 1 — neither binary is on PATH in this container.",
      "correction": ""
    }
  ],
  "overall_notes": [
    "12 of 14 premises hold as stated or nearly so; the two that must be corrected in the plan are P11 (trackB1_sat_Q.ms DOES exist, at $WT/mailbox/wave6/frontier/) and P10 (the sweep-death branch (a) is shape-restricted, not general in (C,i,j)).",
    "Path drift is systematic: several artifacts the premises attribute to canon/ actually live under mailbox/ or p11/ (P9 .ms files, P11 sat_Q.ms). canon/wave6/frontier/ does not exist; mailbox/wave6/frontier/ does.",
    "P4's external source file gghv.txt is not in any checkout, so every gghv.txt:NNNN line citation in CATCHES.md is unverifiable from this container. Same category of risk as P14 (no Singular/msolve): claims resting on external artifacts cannot be re-run here.",
    "Two premises overstate what the file certifies: P7 (witness certifies W>=8 alive, not 'W=12..19') and P10. Both are weaker-but-still-useful; quote the file's own wording.",
    "P3's tail predictor is explicitly labelled a conjecture with a proposed-but-unrun 20-sample test; no results file exists. Treat as unvalidated if a plan depends on tail-only compilation.",
    "Search coverage caveat: greps for '288' and '6821' were literal string matches across all checkouts; a semantic check of what those numbers were meant to denote was not performed."
  ]
}
```