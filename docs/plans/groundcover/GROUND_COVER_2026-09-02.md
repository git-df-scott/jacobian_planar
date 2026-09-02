# Ground cover, 2026-09-02

Purpose: cover as much ground as possible with solver-free audits and cheap exact checks, so that the next session's direct attempts are aimed at verified targets. Nothing here is a counterexample and nothing here changes a verdict in the archive. Every item below was produced by an agent working read-only on the campaign worktrees, with scripts and outputs in `docs/plans/groundcover/artifacts/`.

Worktrees audited: `canon` = `claude/opus-5-counterexample-plan-sep6yk` at 24a06fc; `mailbox` = `codex/claude-opus5-mailbox` at 156ba7a; `p11` = `codex/pentagon-p11-zero-search` at e4fa5ce; `l16` = `codex/pentagon-level16-exact` at 1e3ac1f; `hunt`, `pq`, `errors` = the corresponding `claude/opus-*` branches.

## 1. Plant

| Item | Result |
|---|---|
| Singular 4.3.2 | installed from apt; smoke test `dim(std(x^2-1, y-x, x+y)) = -1` passes |
| msolve 0.6.5 (apt) | installed; returns `[-1]` on the known-EMPTY bottom-edge chart c2=0 at p=1000003 in 2 s; returns a parametrization on the known-NONEMPTY chart c2=1 in 271 s; segfaults on a poisoned input (constant generator equal to a multiple of p) rather than lying |
| msolve 0.10.1 (built from source, `scratchpad/msolve-0.10.1/bin/msolve`) | the version the campaign's certifiers pin; same EMPTY and NONEMPTY results; on the poisoned input it exits 1 with `Error when parsing term ... coefficient cannot be 0 modulo`, the documented silent-lie mode was not reproduced with this input; `-g 2` Groebner-only mode works (bottom-edge c2=1 basis in 9 s, 1,085 generators) |
| poppler `pdftotext` | installed; read every page of all three papers cleanly. `pypdf` is installed but broken by a cffi issue in the system `cryptography` package |
| `/usr/bin/time` | absent; use the shell timer |

Anomaly to settle: msolve's parametrization header for the bottom-edge chart c2=1 at p=1000003 reads `[0, [1000003, 19, 1144, ...]`, i.e. 19 variables and degree 1144, while the campaign's `analyse.py` and `orbit_data.txt` report an eliminant of degree 9. The PARI check in section 8 addresses this.

## 2. Published enumeration verified against the PDFs (Lead A step 3): DISCHARGED

Agent output: `artifacts/TABLE_VERIFY.md`.

- arXiv:1708.07936 section 6 lists 13 family rows, 9 length-1 rows, 11 length-2 rows and 1 length-3 row, 34 in all. The campaign's `canon/gghv_audit/all_cases_max_le_150.json` matches 34 of 34 on (A0, mid, final, m, n), with zero missing, zero extra, and zero value discrepancies; deg_P = m v11(A0) and deg_Q = n v11(A0) hold in every record.
- The 10 rows with max below 125 match GGHV 2022 section 2 row for row. GGHV discard all ten except the starred (8,28) with (m,n)=(3,2), which is (108,72), the campaign's own case.
- The corner A0=[8,1,28] appears as a first corner exactly twice: (m,n)=(3,2) giving (108,72) at max 108, and (m,n)=(3,4) giving (108,144) at max 144. It also appears as a mid corner in two other records.
- The unique record with max exactly 125 is F2 with j=1, (75,125), (m,n)=(3,5). GGHV's bound is strict, so this row is on the untouched side. The split is 10 below, 1 at, 23 above.
- arXiv:1708.07936 discards nothing above max 100; its only original discard is F22 with (m,n)=(2,3) at max 96. "34 enumerated" is right; "34 open" is wrong.
- FABLE-006's 24-case list reconciles completely; its ask to verify the table before spending solver time is discharged.

## 3. Enumeration re-derived from the algorithms (Lead A steps 1 and 2): NO NEW SUB-125 CASE

Agent output: `artifacts/ENUMERATION_AUDIT.md`, `artifacts/gc_enum_audit.py`, `artifacts/gc_all_cases_max_le_300.json`.

- The campaign's re-implementation `canon/gghv_audit/ggv_algorithms.py` has no CLI; its driver `w5_gghv_certifier.py` re-ran in 4.8 s, 19 of 19 checks, and regenerated `all_cases_max_le_150.json` and `rerun_105_124.json` byte-identical to the committed files. A fresh run at M=100 gives 474 cases at max 300, set-identical to the committed file.
- The six unprinted chains the archive reports were all found and traced. The two length-1 extras die at Definition 3.3 (gcd(6,10)=2 and gcd(6,9)=3, so no (m,n) family). The four length-2 extras do not die: they diverge at Algorithm 2 line 7 and rejoin the printed F18-F21 route at the same A1, emitting real degree pairs (48,168), (72,168), (60,210), (90,210), all far above 125 and adding no new pair.
- Degree pairs with max below 125 at both M=50 and M=100 are exactly GGHV's ten. The search space below 125 is not larger.
- A'_t for the (10,40) chain: the code contains no such assumption; the (1,0) default lives in `canon/campaign/audit_tracks/trackD_chain_map.py:105,229` because section 6's table has no A' column. Enumerating Algorithm 2's own filters for A0=(10,1,40) gives 58 starting edges, of which exactly one carries admissible complete chains: A'_0=(2,0), mu=4, direction (5,-1), 41 complete and 25 admissible. The point (1,0) is not among the 58 at all. So A'_t is forced to (2,0), the campaign's default is wrong for this case, and nothing opens: the minimum degree-pair max over the 25 admissible chains is 150.
- The F6 coprimality discrepancy (D7) holds in the code; the queue entry F6(j=0; m,n=4,10) is not a possible counterexample shape.

Compiler correction for tomorrow: any (10,40) shape compiled with A'_t=(1,0) sits on the wrong lower corner, which changes the Newton polygon and the slope q = b_t/(a_t - a').

## 4. GGHV Corollary 5.7 (gate G2): BROKEN as printed

Agent output: `artifacts/COR57_ADJUDICATION.md`, `artifacts/run/bracket_check.py`.

- The local `2204.14178.pdf` is v1 only (April 2022), with no v2, erratum or journal reference in the file.
- Every quotation in `canon/CATCHES.md:517-604` checks against the PDF text layer. The three arithmetic claims were recomputed independently in sympy. Using the paper's own chain rule and its explicit L^(2) bracket, the first application gives [psi P, psi Q] = 1/2, in K^x, valid; the second gives [psi phi P, psi phi Q] = 1/2 + (lambda/2) x^(-1/2), not in K^x, with lambda nonzero forced by the claim itself and independently by (0,18) in N(P). The standing hypothesis [P,Q] in K^x is printed on its own line in [1, Cor 7.2] and required by [1, Def 4.3] and [1, Thm 2.6], so all three routes into "the same argument" are blocked.
- (5.12) is load-bearing: v_(-1,1) is maximal on N(P) at (0,18), not (6,18), and on N(Q) at (0,27), not (9,27), so Theorem 5.1 hypothesis (2) fails on the untranslated pair and Theorem 5.1 is reachable only through phi and (5.12). Condition count 21 on P plus 45 on Q is 66; the valid claim delivers 15; 51 are unsupported.
- No repair by the same device: solving (h + lambda) h' = c gives h = -lambda plus or minus sqrt(C1 + 2cx + lambda^2), so the composite either undoes the translation or leaves L^(2).
- The mailbox sweep's "VERIFIED" at line 66 is scoped to the wording of the statement, not the proof, so the two records do not directly contradict; line 66 also misattributes the corollary to the (9,24)/(66,99) shape, which line 311 of the same file has right.

Consequence: the (9,27) orientation of (72,108), with (m,n)=(2,3), is unclosed by the literature. The statement may still be true; its only published proof is not valid. The campaign's two independent test systems (Lead E) are the first test.

## 5. GGV Theorem 1.2 verbatim (Lead C step 1): a genuine iff; the misprint is in the source

Agent output: `artifacts/GGV_THM12_VERBATIM.md`, `artifacts/run/row3_check.py`, `artifacts/GGV_ARXIV_DIFF.md`.

- Theorem 1.2 (journal p. 85) reads: B = 16 if and only if there exist A, q1 in K[y] and mu0, mu1, mu2, mu3 in K with mu0 nonzero, A(0) = -(1/4) mu3^2, A'(0) = mu2, and mu3 A''(0) = -6 mu1 - 2 mu3 q1''(0), such that (1.3) holds. It is a genuine iff.
- The equivalent object is the reduced datum (A, q1, mu0..mu3) with A = y p1 - q1 p2 + (3/4) q1^2 relative to the ansatz P = x^3 y + x^2 p2 + x p1 + p0, Q = x^2 y + x q1 + q0. Full P, Q are recoverable: p2 and F from q1, p1 from A, then q0 and p0 by integrating (3.2) and (3.3); (1.2) is exactly the condition making those integrals polynomial. So a solution is not Newton-polygon leading data, and the reconstruction to (P,Q) is explicit. This settles open question 1 of the plan and defines gate H0 for this lead concretely.
- mu0 nonzero is the only inequality in the statement. No deg(q1) = d condition is part of Theorem 1.2; the cell index j enters only through Theorem 1.1. The reviewer's suggested cell-pinning saturation remains a sensible export choice but is not a hypothesis of the theorem.
- Row 3 of (1.2) is printed with the -2 mu3 q1''(0) term twice in the journal (p. 85 and p. 93) and twice in arXiv:1310.8249v3 (equations (2) and (3.9), fetched today), so the error is in the authors' source, not a typesetting slip. The sympy re-derivation from the polynomiality of (3.2) and (3.3) gives mu3 A''(0) = -6 mu1 identically; the campaign's correction is confirmed. Scope: the derivation divides by mu3, so on the mu3 = 0 slice both forms coincide and prior verdicts restricted to that slice are unaffected.
- The arXiv text also states the GGV conjecture explicitly (in the case mu1 = mu2 = 0 with q1 of arbitrary degree, any solution of (3.8) satisfying (3.9) has mu0 = 0; the general conjecture that the only solutions satisfying (3.9) are those with mu0 = 0).

## 6. Sweep dichotomy scope (gate G12): narrower than its headline, but the headline survives one degree higher

Agent output: `artifacts/SWEEP_SCOPE.md`, `artifacts/sweep_gamma2.py`.

- The hypothesis at `canon/CATCHES.md:1382` is S(gamma, w) = X(w) + gamma Delta(w), affine-linear in gamma; every code path agrees.
- Branch (a)'s twist rebuttal is not general: it is conditional on w = gamma u, and the searched family fixes C = gamma x^s with all exponents at most 2 and four inconsistent short (i,j) lists across the tree. A general divisor C is untested at every gamma-degree.
- The general side-condition identity is present, and the archive itself already retracted its content (CATCH 2: it reduces to {A,B} = kappa, the original problem). No system above Moh's bound was ever built; the only run had max total degree about 32 and was killed at 501 of 1,728 shapes.
- New: at gamma-degree 2, det J is cubic in gamma with coefficients det(D,X'), det(D,D') + 2 det(E,X'), det(D,E') + 2 det(E,D'), 2 det(E,E'). The branch (b) collapse fails verbatim, but running the conditions top-down forces E = (0, c D1^2), D2 = D1 (2c X1 + e), D1 constant, and the surviving map satisfies S2 - c S1^2 - e S1 = G(w), gamma-free, so S is triangularizable after an elementary quadratic target shear, hence injective. The correct general form of branch (b) is "triangularizable after a target shear of degree equal to the gamma-degree". Gamma-degree 3 and above is untested; a general C is the real gap.

## 7. Chain-compiler factorization (Lead I): REFUTED

Agent output: `artifacts/COMPILER_FACTORIZATION.md`, `artifacts/tailtest.py`.

- `trackD_chain_map.reduced_candidates` (`canon/campaign/audit_tracks/trackD_chain_map.py:208-263`) is the only reader of chain corners. Given (tail, c', swap) the polygons are tail-determined (proved from lines 251-257). But the c' ladder at lines 232-243 computes c_pre = b0 - s a0 from A_0 = corners[0], a pre-tail entry, so the enumeration of c' is not tail-determined. 21 of 29 in-scope chains are A_0-live.
- Concrete pair in the library: X = "(8,28)/11/4,7 (m,n)=3,2" (corners [(8,28),(11/4,7)]) and Y = "(8,32)/8,28/11/4,7 (m,n)=3,2" have identical tails, A_t, A'_t, (m,n), a, b, r, but c_pre 4 versus 8, so X emits c' in [4,0] and Y emits [8,4,0]. Y carries a shape X does not, with different Newton polygons, parameter count and dimension bound. X is exactly the published GGHV Proposition 4.3 (8,28) case.
- Why "zero predictor violations" was still true: shorter ladders are suffixes of longer ones, so shared shapes share hashes, and a shape that is never generated cannot violate a hash comparison. Four of the six multi-chain tail groups agree only because A_0 is clamped, an arithmetic accident.
- Repair: extend the key by one integer, cmax = min(int(b0 - (b_t/(a_t - a') - 1) a0), b), one rational evaluation from A_0 plus tail data. The 26 tails become 27 keys and the saturation conjecture survives as (tail, cmax)-closure. As written, `canon/CROSSDOOR.md:78`'s "compute each case's tail, not its full chain" silently drops shapes.

## 8. Pentagon case (1) structure (Lead F): the file is real, the README numbers are not, the c-block is eliminable, the grading claim fails

Agent output: `artifacts/PENTAGON_STRUCTURE.md`, `artifacts/msparse.py`, `artifacts/analyze_*.py`.

- `mailbox/wave6/frontier/trackB1_sat_Q.ms` is 166 variables, 284 generators, 8,774 terms, max total degree 5, max coefficient 468, all integral. This matches the mailbox record to the digit. The README's "164 variables, 288 quadrics, 6,821 terms over Q(alpha)" matches nothing: the file is over Q, has no alpha, and is not quadratic. Variable families: 51 c, 110 d, 4 s (s_1_5, s_2_6, s_3_7, s_4_8), and one saturation variable zsat that occurs only in generator 283.
- Third-prime check: reduced mod 1000003 the file agrees with `trackB1_sat_p1000003.ms` on all 284 generators; mod 65521 it agrees with `trackB1_case1_full_p65521.ms` on all 284, the only difference being the saturation variable's name (w_sat there).
- Bilinearity: 283 of 284 generators have degree at most 1 in the c-block and at most 1 in the d-block; the sole exception is the Rabinowitsch row. The s-block is a genuine third block (degree up to 3, 990 c s^3 monomials). `tb1_square_block.json` is not a c/d split; it defines a 60 by 60 square subsystem.
- Torus grading: refuted for the saved file. Over 7,358 primitive monomial-difference rows the constraint matrix has rank 166, so the torus rank is 0; excluding the saturation row it is 1, supported only on zsat. The L = 2 alpha - beta grading fails on 207 of 283 generators; breakage starts at generator 21 and the derived row c_1_0 = 1 is the likely gauge culprit. The system register's rank 22 for this file used a 4,000-row cap and is a sampling artifact; treat all register torus ranks on large systems as upper bounds.
- Free branch (d_0_1 = d_1_1 = 0) followed by a sound constant-coefficient linear fixed point: 15 variables eliminated in 14 rounds, leaving 269 equations in 151 variables, max degree 4, no nonzero constant. UNDECIDED, not empty. Case (1) still has no verdict.
- The c-linear system M(d,s) c = b(d,s) is 283 rows in 51 unknowns with generic rank 51 and augmented rank 52 at random points: c is uniquely determined by (d,s), the generic fibre is empty as expected, and the projection to the (d,s)-block is well posed. Do not enumerate 52 by 52 minors; solve c from a rank-51 row subset and substitute into the remaining 232 rows.

## 9. System register and timeout enumeration (Lead B step 6, Lead I step 1)

Agent output: `artifacts/REGISTER.json`, `artifacts/TIMEOUT_SHAPES.json`, `artifacts/REGISTER_SUMMARY.md`, `artifacts/register_build.py`.

| Quantity | Value |
|---|---|
| `.ms` files across the seven worktrees | 1,489 |
| genuine input systems (8 are msolve outputs misfiled as `.ms`) | 1,481 |
| distinct content hashes | 455 |
| files over 5 MB, header-only (no torus scan) | 38 |
| cross-name duplicate groups (same mathematics, different name) | 27 |
| unique systems with excess at most 0 (emptiness runs vacuous) | 88 (371 files) |
| unique systems with torus rank above 0 (solve mode cannot terminate) | 262 (895 files), ranks are upper bounds |
| machine-identifiable timeout shapes | 18, of which 7 resolve to a file |

- Verified: `p108_821326.ms` and `p108_843700.ms` are byte-identical, one system not two. Also `p108_192622.ms` equals `w6_35657_0.ms`; `pent_L18.ms` equals `pent_L18_g2.ms`; eighteen `sym_n4_a2_b1` and `sym_n6_a2_b5` pairs across three primes are the same systems re-exported under a second parameter label and re-run.
- The entire pentagon truncation ladder (pent_L14 through pent_L19, slice_ctl_pin, slice_ctl_pos) has 59 variables against 2 to 29 equations, excess -57 to -30, and torus rank 22 to 23: every pentagon OOM or timeout in the run log was on a system that is both underdetermined and graded. This is the family that consumed two weeks.
- The "41 timeout shapes" is not reconstructible from any artifact: 36 is the above-125 virgin sweep, 33 the same minus three later-decided cases, 49 to 16 is the wave6 hash dedup, and 41 has no derivation anywhere. 33 plus the separately listed (8,28) four is 37.
- Smallest undecided systems with positive excess are the B=16 controls and small ladder cells (7 to 8 variables); the register lists the twenty smallest.

## 10. Exact checks in PARI (Lead D steps 1 and 7, Lead F step 2)

Agent output: `artifacts/PARI_EXACT_CHECKS.md`, `artifacts/check*.gp`, `artifacts/resid6.ms`.

- Bottom-edge eliminant, pentagon case (1). `canon/wave6/bottomedge/be_c2is1_q.out` does not contain an eliminant; it is msolve's real-root-isolation output (three boxes of 18 coordinate intervals). Direct characteristic-zero regeneration timed out at 300 s in both msolve `-P 1` and Singular. The system is triangular in the d-variables: after the gauge c1 = c2 = 1, ten of the sixteen remaining equations are linear in a fresh d-variable with a nonzero integer constant pivot (3, 5, 7, ..., 21), so solving for d3..d12 is an invertible change of variables over Q. The residual is 6 equations in c3..c8 (degrees 5, 6, 6, 6, 6, 6); msolve `-P 1` solves it in 30 s and returns a degree-9 eliminant with coefficients up to 108 digits, matching the degree recorded mod p at all twelve archive primes. PARI factors it as 1 + 1 + 2 + 5: exactly two rational roots (x, and 4100x - 771 for msolve's separating form), one quadratic orbit, one quintic orbit with `polgalois` S5, squarefree. The retracted "4 rational plus one degree-5 orbit" story is refuted with a concrete replacement, and the twelve archive prime counts (5, 4, 5, 4, 5, 4, 5, 3, 3, 2, 5, 6) are consistent with this pattern (expected 4, minimum 2, maximum 6) and impossible under the old one (minimum 4). Label: PROVED-exact for the derived residual, with an independent direct char-0 confirmation on the 18-variable system still outstanding. Consequence for Lead F: the admissible seeds fall into at most four Galois classes (two rational, one quadratic, one quintic), so testing one seed per class decides the family; mapping the roots back to named (c, d) coordinates was not done.
- Case (2), w = -4 quintic (`canon/wave4/artifacts/edge_eliminant_Q_one.json`): degree 5, content 1, squarefree, irreducible over Q, hence no rational root, discriminant of 806 digits positive and non-square, Galois group S5; both negative controls fire. PROVED-exact for the polynomial as written; its identity with the true w = -4 eliminant remains as strong as the six held-out primes and no stronger.
- Case (2), degree-1144 edge eliminant (`canon/wave1/edgeQ_eliminant.txt`): gcd(f, f') over Q has degree 0, computed exactly in 72 ms, so squarefreeness is PROVED-exact; three modular certificates agree. Seven fresh primes (100169 to 100237) give multiplicity-free factor patterns, and the Dedekind subset-sum sieve on the fresh primes alone closes to zero surviving proper-factor degrees by p = 100193; the archive's eight old primes close independently with no prime shared. Irreducibility is reported as strengthened modular evidence, not claimed.
- Tooling gotcha to propagate: `gp -q -f` parses multi-line `for` bodies line by line and can silently execute the body at top level with a symbolic loop variable, printing plausible but meaningless output; every loop body must be on one line, and any output line reading `p=p` must be rejected. `polrootsQ` does not exist in PARI 2.15.4; `galdata` is not installed, so `polgalois` is limited to degree 7 (this did not bind).

On the msolve header anomaly from section 1: the modular parametrization of the c2 = 1 chart reports 1144 in the degree field while the distinct-point count is 9 at every prime and over Q. Whether that field is the quotient dimension (multiplicity 1144 over 9 points) or an artifact of the separating form was not settled today and is a one-line question for tomorrow; it does not affect the factorization above, which is computed on the reduced residual.

## 11. d=8 chart N, corrected system (Lead C step 2)

`canon/wave5/ms/m16_d8_p1000003.ms`: 23 variables (including the Rabinowitsch variable t), 30 generators, excess 7, no constant generators, all coefficients in range. Launched with msolve 0.10.1 in Groebner-only mode (`-g 2 -t 2`) at p=1000003 with a 90-minute cap on the 4-core, 16 GB container. Memory grew from 215 MB at 266 s to 7.8 GB at 586 s and 9.1 GB at 715 s; the memory cgroup killed the process at 737 s with 13.7 GB resident (exit 137, empty output, empty stderr).

Label: OOM, not a verdict. This is the first launch of the corrected d=8 chart N export in the campaign's history, and it establishes that the direct Groebner route on this cell needs more than 14 GB even in Groebner-only mode at a single prime. The measured growth rate suggests a 64 to 128 GB host might finish it, but that is an extrapolation. The alternative routes in the plan (Singular degBound ladder with `lift`, and the graded cofactor certificate) are the ones to try before renting memory.

## 12. What this changes for tomorrow

- Lead A (enumeration and Cor 5.7) is done except the paper-repair attempt on Cor 5.7 by a different argument. The search space below 125 is verified: (72,108)/(108,72), with both orientations now open, since the (9,27) kill has no valid published proof.
- Lead C's premise is verified from the page: Theorem 1.2 is an iff, mu0 nonzero is the only inequality, the reconstruction to (P,Q) is explicit, and the row-3 misprint is in the source. The d=8 chart N cell is the frontier and its resistance is now being measured on a real engine.
- Lead E (the (9,27) leaves) is upgraded from "test of a published kill" to "the only thing standing between the (9,27) orientation and the open list".
- Lead F has a concrete reformulation target: eliminate the 51 c-variables exactly and work in the (d,s)-block of 114 variables with 232 compatibility rows; the grading claim must not be used.
- Lead I: do not compile by tail. Add cmax to the key first.
- Lead B: the plant exists; the register exists; 88 vacuous systems and 27 duplicate groups are now known by hash.

## Addendum

All items reported above are complete. The only computations that ended without a verdict are the direct characteristic-zero regenerations of the bottom-edge eliminant on the full 18-variable system (both engines, 300 s) and the d=8 chart N Groebner run (OOM at 13.7 GB).
