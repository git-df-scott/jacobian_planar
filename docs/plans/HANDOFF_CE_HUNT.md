# Handoff: JC2 counterexample hunt, direct attempts

Written 2026-09-03 for a fresh session. Read this file first, then `docs/plans/groundcover/GROUND_COVER_2026-09-02.md`, then `docs/plans/CE_HUNT_PLAN.md`. Everything below was verified in the previous session; nothing below is a counterexample.

## 1. Where things are

| Item | Location |
|---|---|
| This branch | `claude/jc2-handoff-audit-hartnc`, draft PR [#22](https://github.com/git-df-scott/jacobian_planar/pull/22) against `main`, head 3da2603 plus this file |
| The plan | `docs/plans/CE_HUNT_PLAN.md` (leads A to I, audit gates, fleet design, verdict labels, HIT protocol H0 to H6) |
| Plan provenance | `docs/plans/appendix/` (nine reader reports, five planner outputs, three adversarial reviews) |
| Ground-cover report | `docs/plans/groundcover/GROUND_COVER_2026-09-02.md` with scripts and outputs in `docs/plans/groundcover/artifacts/` |
| Canonical campaign branch | `claude/opus-5-counterexample-plan-sep6yk` at 24a06fc (STATUS.md, OPEN_ITEMS.md, CATCHES.md, wave*/ , certifiers/) |
| Pentagon system over Q | `codex/claude-opus5-mailbox` at 156ba7a, path `wave6/frontier/trackB1_sat_Q.ms` (166 vars, 284 eqs), twins `trackB1_sat_p1000003.ms` and, on canon, `campaign/audit_tracks/trackB1_case1_full_p65521.ms` |
| (9,27) test systems | `codex/pentagon-p11-zero-search` at e4fa5ce, paths `wave6/ms/p108_525122.ms` (28 vars, 140 eqs) and `wave6/ms/p108_192622.ms` (40 vars, 139 eqs); results ledger on mailbox at `wave6/frontier/P108_RESULTS.md` |
| d=8 chart N exports | canon `wave5/ms/m16_d8_p1000003.ms`, `m16_d8_p1000033.ms`, `m16_d8_q.ms` (23 vars including the Rabinowitsch t, 30 eqs, excess 7); generator `wave6/w6_seed_d8.py` |
| Bottom-edge residual | `docs/plans/groundcover/artifacts/resid6.ms` (6 eqs in c3..c8 after the exact triangular elimination) and `resid6_P1.out` (msolve RUR with the degree-9 eliminant) |
| Case (2) eliminants | canon `wave1/edgeQ_eliminant.txt` (degree 1144, squarefree PROVED-exact), `wave4/artifacts/edge_eliminant_Q_one.json` (w = -4 quintic, irreducible, S5) |
| System register | `docs/plans/groundcover/artifacts/REGISTER.json` (455 distinct systems by content hash; excess and torus rank per system; torus ranks on large systems are upper bounds), `TIMEOUT_SHAPES.json`, `REGISTER_SUMMARY.md` |
| Papers | canon `papers/` (GGV 2013 journal, arXiv:1708.07936, arXiv:2204.14178, others); arXiv:1310.8249v3 was fetched to the scratchpad and is not committed |

## 2. Re-creating the working environment

The previous session's worktrees and engine builds lived in an ephemeral scratchpad and are gone. Recreate them:

```
cd /home/user/jacobian_planar
git fetch origin claude/opus-5-counterexample-plan-sep6yk codex/claude-opus5-mailbox codex/pentagon-p11-zero-search codex/pentagon-level16-exact
git worktree add /tmp/wt/canon   origin/claude/opus-5-counterexample-plan-sep6yk
git worktree add /tmp/wt/mailbox origin/codex/claude-opus5-mailbox
git worktree add /tmp/wt/p11     origin/codex/pentagon-p11-zero-search
git worktree add /tmp/wt/l16     origin/codex/pentagon-level16-exact
export DEBIAN_FRONTEND=noninteractive
apt-get install -y -q singular msolve poppler-utils libflint-dev libgmp-dev libmpfr-dev autoconf automake libtool build-essential
git clone --depth 1 --branch v0.10.1 https://github.com/algebraic-solving/msolve.git /tmp/msolve-src
cd /tmp/msolve-src && ./autogen.sh && ./configure --prefix=/tmp/msolve-0.10.1 && make -j4 && make install
```

Facts about the box: 4 cores, 15 GB, no swap, no `/usr/bin/time` (use the shell timer), PARI/GP 2.15.4 without `galdata` (`polgalois` up to degree 7), `pypdf` broken (use `pdftotext`). The apt msolve is 0.6.5; use the source build (`/tmp/msolve-0.10.1/bin/msolve`) for anything that matters, since the campaign's certifiers pin 0.10.1. Smoke tests that must pass before any run: the bottom-edge chart c2 = 0 at p = 1000003 (`canon/wave6/bottomedge/be_c2is0_p1000003.ms`) returns `[-1]` in about 2 s; the chart c2 = 1 returns a parametrization; a file with a constant generator equal to a multiple of p must produce a parse error, never `[-1]`.

## 3. What is verified, in one screen

- The search space below max degree 125 is exactly GGHV's ten cases, re-derived from the algorithms; the only survivor is (72,108)/(108,72). The 34 published cases at max 150 match the campaign's reproduction row for row; 24 are untouched above 125, including (75,125) at exactly 125.
- GGHV Corollary 5.7, the only published kill of the (9,27) orientation with (m,n) = (2,3), is broken as printed (bracket leaves K^x; 51 of 66 conditions unsupported; no repair by the same device). Both orientations of (72,108) are open.
- GGV Theorem 1.2 is a genuine iff with mu0 nonzero as its only inequality; the reconstruction of (P,Q) from a solution is explicit in the paper (section 3, integrate (3.2) and (3.3)); the row-3 misprint is in the authors' source. On the corrected system d = 3..7 are EMPTY over Q. d = 8 chart N was launched once in Groebner-only mode and was killed at 13.7 GB: measured resistance, not a verdict.
- Pentagon case (1): the system is 166 variables, 284 equations, bilinear in the c and d blocks apart from the saturation row and a third s-block of four variables; the 51 c-variables are uniquely determined by (d, s) (generic rank 51, augmented rank 52); no torus grading exists on the saved file; the free branch (d_0_1 = d_1_1 = 0) reduces to 269 equations in 151 variables and stays undecided. Every truncation of weight at least 8 is alive by an exact witness, so the truncation ladder cannot kill it. The bottom-edge eliminant factors 1 + 1 + 2 + 5 over Q (two rational roots, a quadratic orbit, an S5 quintic), so admissible seeds fall into at most four Galois classes.
- Case (2): EMPTY at five primes, never over Q; the degree-1144 edge eliminant is squarefree (exact) with irreducibility strongly supported modulo 15 primes; the w = -4 quintic is irreducible with group S5.
- The chain compiler does not factor through the tail; compiling by tail drops shapes. The (10,40) lower corner is forced to (2,0), not the default (1,0).
- 455 distinct exported systems; 88 have non-positive excess (vacuous for emptiness); 262 have positive torus rank (solve mode cannot terminate; use `-g 2` or a gauge); 27 duplicate groups were re-run under different names.

## 4. The four direct attempts, in order

Each attempt has a gate, a command shape, a stop rule and a label. Do not skip the gate. Never report a timeout, an OOM, a segfault or an empty output as a verdict.

### Attempt 1: the (9,27) leaves in Groebner-only mode

Why first: the only published kill of this orientation is invalid, the systems are small (28 and 40 variables), and their earlier 1800 s timeouts were structural (torus rank 5, solve mode on positive-dimensional input), not budget.

1. Gate: measure the grading-torus rank of `p108_525122.ms` and `p108_192622.ms` (exponent-difference nullspace; `docs/plans/groundcover/artifacts/register_build.py` has the routine). Re-derive the rank-5 slice independently with a proof that every orbit meets it, not just a nonzero weight-minor (the recorded gauge minors are -1/24 and -1/14). Quotient by the torus to remove the parameters exactly; check with a planted point that the quotient preserves the solution set.
2. Sanitize the export (coefficients in [0, p), no zero terms, no constant generators, round-trip re-parse).
3. Run the three unresolved leaves (two on 525122, one on 192622 with 139 equations in 38 variables) with `msolve -g 2 -t 2` at three primes p = 1 mod 3, 8 h cap each, memory watched. Then Singular `facstd` in parallel on the leaf structure.
4. Verdict standard, pre-registered both ways: EMPTY at one prime is replication-grade only; EMPTY at three compliant primes is EMPTY-mod-p and goes to the certificate step; a non-empty zero-dimensional output freezes everything, goes to Hensel lift (`canon/lift/lift_pipeline.py`), exact substitution, gate H0 (reconstruct explicit P, Q with the right degrees), then H1 to H6. The word "refutation" about GGHV section 5 is not used before a char-0 lift.

### Attempt 2: d=8 chart N by routes that fit in 15 GB

Why: the frontier cell of the one door where a solution promotes by an iff; the direct Groebner route needs more than 14 GB.

1. Gate: regenerate from `wave6/w6_seed_d8.py` and diff against the exports; confirm provenance is the corrected row 3 (mu3 A''(0) = -6 mu1). Add, alongside the mu0 t - 1 saturation, a saturation pinning the cell (leading coefficient of q1 nonzero) and run both charts of any split.
2. Route A, Singular over Q with a degree bound ladder: `option(redSB); degBound = 5; ideal G = std(I);` then 6, 7, 8; a unit at any rung is a genuine 1 in the ideal; then `matrix M = lift(I, ideal(1));` to extract cofactors. Note `option(degBound, D)` is not valid syntax and fails silently; set `degBound` as a variable. Each rung is a separate process under 25 minutes.
3. Route B, the graded cofactor certificate: build the linear system for 1 = sum h_i f_i at degree D from maxdeg + 1 upward, rank-test mod p first, solve exactly with python-flint or by CRT and rational reconstruction, then verify the identity by exact expansion against the saturated generators. Failure at every D up to 12 is "no certificate at D", not evidence.
4. Route C, modular sanity: msolve `-g 2` at primes where 96 is a quadratic residue and p = 1 mod 3, with a 6 GB memory cap, two agreeing primes before quoting anything.
5. Stop: three routes at 8 h each; if all fail, record "exact elimination cannot decide d=8 chart N on this hardware" and do not queue d = 9..11 (cost scales about 32 times per level). A NON-EMPTY is a lift target: H0 (integrate (3.2) and (3.3) to get P, Q of degrees 16(3d-2), 16(2d-1)) then H1 to H6.

### Attempt 3: the pentagon with the c-block eliminated

Why: the only branch with no verdict by any method, and the previous session established that the c-variables are determined by the rest.

1. Gate: reproduce the bilinearity and rank facts from `docs/plans/groundcover/artifacts/PENTAGON_STRUCTURE.md` on the file (`msparse.py`, `analyze_final.py`). Do not use any claimed torus grading; there is none.
2. Elimination: for the c-linear system M(d,s) c = b(d,s) (283 rows, 51 unknowns), pick a rank-51 row subset R, solve c symbolically over Q(d,s) (or over F_p for the first pass), and substitute into the remaining 232 rows to get the compatibility ideal in the 114 (d, s) variables plus the saturation. Do not enumerate 52 by 52 minors.
3. Seeds: the bottom-edge eliminant splits 1 + 1 + 2 + 5; map msolve's separating-form roots in `resid6_P1.out` back to the named (c, d) coordinates, one representative per Galois class (two rational, one quadratic, one quintic), and pin each seed exactly (over Q for the rational ones, over the quadratic field, over the quintic field) before extension. The prior seed-pinned run (`canon/wave6/pentseed/seed0_p1000003.ms`, 267 eqs, 148 unknowns, timeout at 5400 s and 9.5 GB) pinned one seed at one prime only.
4. Alternative reformulation to audit in parallel: FABLE-003's 57-variable rank-drop on a 303 by 124 matrix (`mailbox/AGENT_MAILBOX.md:3562-3675`), required to reproduce a known EMPTY and a known NONEMPTY control before it is trusted.
5. Stop: if the compatibility ideal exceeds about 120 variables after elimination and no further exact reduction is available, record the size and stop; do not fall back to the 186-variable monolith on this box.

### Attempt 4: the first untouched published case, (8,28) with (m,n) = (3,4) at (108,144)

Why: the largest region with no published exclusion that needs no unbuilt compiler.

1. Gate: compile through `canon/campaign/audit_tracks/trackD_chain_map.py` with the corrected key (add cmax = min(int(b0 - (b_t/(a_t - a') - 1) a0), b) so the c' ladder is fully determined) and check the invariant eps_P + eps_Q = (r + 1, 1) and the six published reduced pairs as a regression.
2. Compute excess and torus rank; refuse emptiness runs with excess at most 0; route positive-rank systems to `-g 2`.
3. Two compliant primes at 1800 s, then the certificate step. Only after this one case closes end to end, batch the other 23.

## 5. Guardrails that were load-bearing last session

- Read stderr on every solver call; ignore exit codes. A verdict is read only from a non-empty output matching a documented pattern.
- Every export goes through the sanitizer (coefficient range, no zero terms, no constant generators, round-trip re-parse). The msolve 0.10.1 parse error on a bad constant is the correct behavior; the silent `[-1]` mode is documented in `canon/CATCHES.md` and was not reproduced, so stay defensive.
- Excess above zero and torus rank measured before every emptiness run.
- EMPTY over Q is certified only by explicit cofactors 1 = sum h_i f_i against the saturated generators, verified by an independent checker. The reduce-to-zero-plus-Buchberger check certifies containment and is a NONEMPTY certifier only. Lucky-prime majority voting is a search heuristic with no evidential weight.
- Any non-empty point on a reduced-polygon system is ADMISSIBLE-SHAPE, not a candidate, until H0 produces explicit P, Q in Q[x,y] with the right degrees. H2 is a global symbolic identity (det J minus c expands to zero), H3 uses exact algebraic points, H4 is the field degree [C(x,y) : C(P,Q)] by resultants, H5 is invariance under random affine changes on source and target. Both historical false hits were gauge artefacts H5 would have caught.
- No numerical multi-start as evidence at any size. No `pkill -f`. Push after every result; the campaign's tree rolled back twice.
- PARI: put every `for` body on one line in `gp -q -f` scripts; any output line reading `p=p` is a symbolic-loop artefact and must be rejected.

## 6. Probability, stated once

The reviewers' campaign-level estimate of a verified plane counterexample is of order one in a thousand; no attempt above exceeds about half a percent. The guaranteed product of the four attempts is a first verdict on the (9,27) orientation, a first characteristic-zero statement past d = 7 on the B=16 ladder or a measured wall, a first verdict of any kind on the pentagon or a precise statement of why not, and one closed case above 125. Report every outcome with its label and its resource wall.
