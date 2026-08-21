# Track F — Sessions 1-18 regression report

Date: 2026-08-13. Source: `/home/user/jacobian_planar/Sessions 1-18 status reports`
(a single Python file of alternating module docstrings and code, 14 blocks).

Method: split into per-session blocks (split verified LOSSLESS — concatenation of the
14 blocks is byte-identical to the source), each block executed with `timeout 900`
(15-min cap), stdout/stderr captured, printed output compared line-by-line against the
block's docstring claims. Artifacts: scratch `regress/` (sXX.py / sXX.out / sXX.err /
sXX.status). All 14 blocks exited 0; no timeouts; slowest block 15.3 s (S6).

## Per-session verdict table

| Session | Block | Runnable? | Elapsed | Verdict | Key evidence |
|---|---|---|---|---|---|
| S1 | s01 | yes | 1.4s | PASS | (1) pencil `F == v*z + w`: True; (2) twisted-cubic direction field: True; (3) `c2 = 0, c1 = 0, c0 = -2` exactly as claimed; (4) fiber sizes recorded below |
| S2 | s02 | yes | 1.4s | PASS | J = c symbolically; inverse identities True; L1 nullspace = span{a^2}, L2 = 2ab + kappa*a (checked by hand against printed tuples), L3 remainder = -c_s; 200/200 random inverse checks True; PART4 leading nullspace = span{x^3}; all 4 cuspidal P probes: no Keller partner |
| S3 | s03 | yes | 4.1s | PASS | (1,3)/(1,4) homogeneous dims 4/5 as expected; (2,3) cascade [y^4],[y^3],[y^2] all 0; C1 repeated-root branch all infeasible; C2 free-lead FEASIBLEs are the documented degenerate phantoms — PART D pinned-lead re-sweeps all infeasible; phantom check True (P = y^2+x has the deg_y<=1 partner Q = y, Session-2 family) |
| S4 | s04 | yes | 4.1s | PASS | (2,4) leading nullspace = span{A^2} (tuple = B_4*A^2 verified); J(y^2+x, tau*P^2+y) = 1, reduction = y; (2,5) cascade identities 0, C3 residue divisibility "divisible"; all (2,5)/(2,7) pinned-lead sweeps infeasible |
| S5 | s05 | yes | 0.0s | PASS | `all admissible templates obstructed: True`; 15 (n,k) templates each print OBSTRUCTED; normalized constants k-independent: True for every n (values below) |
| S6 | s06 | yes | 15.3s | PASS | PART 1 all infeasible (binomial slice theorem); PART 2 matches "feasible iff a0 affine" on all 5; PART 3 LIVE count = 0 (see below) |
| S7 | s07 | yes | 3.7s | PASS | all 7 checks `[PASS]`; degrees y1: (27,72), y2: (18,48) |
| S8 | s08 | yes | 0.1s | PASS | supports 1144/523 (boxes 2044/931); 108/51 pole conditions, exact ranks 108/51; dims 1036+472 = 1508 of 2975; near-miss saturation 9/9 and 6/6; violations 0 + 0; G1 == p(w)/w^2 and G2 == r(w)/w both True |
| S9 | s09 | PROSE-ONLY | 0.0s | N/A (no checks exist) | block is docstring + `print(__doc__)`; the layer-2 executable checks lived in the lost transcript. Nothing rerun, nothing fabricated |
| S10 | s10 | yes | 0.2s | PASS | all 8 checks `[PASS]` including the four surviving W-blocks and cascade C2 <=> 2p7 = 3r4; n3 printed = (-128 + 64*sqrt(-3))/3 |
| S11 | s11 | PROSE-ONLY | 0.0s | N/A (no checks exist) | cascade-engine claims; executable run was "inline in transcript" (lost) |
| S12-14 | s12_14 | PROSE-ONLY | 0.0s | N/A (no checks exist) | Theorems 1-3 + census; "executable checks recorded in the transcript inline runs" (lost) |
| S15 | s15 | PROSE-ONLY | 0.0s | N/A (no checks exist) | box-cap verification lived in a transcript inline run (lost) |
| S16-18 | s16_18 | PROSE-ONLY | 0.0s | N/A (no checks exist) | First-Framework emptiness theorem + certification ledger; ledger's four `[PASS]` items were transcript inline runs (lost). One arithmetic consequence IS re-checkable today: h0 = -13*n3, verified exactly below |

PASS means: every quantitative claim printed by the block matches the docstring's
stated expectation, and no assertion failed. PROSE-ONLY sessions (9, 11, 12-14, 15,
16-18) contain no executable checks in the repo — their certifications existed only in
lost session transcripts. We state this explicitly and did NOT fabricate reruns; their
mathematical claims remain unverified by this regression except where noted (h0/n3).

## S1 generic fiber sizes (RECORDED, as demanded)

The Session-1 map F (reverse-engineered "Alpoge" C^3 -> C^3, det JF = -2):

| target tau | type | #preimages found (certified back-substitution, tol 1e-8/1e-7) |
|---|---|---|
| (3, 5, 2) | generic | **3** |
| (7, -2, 11) | generic | **3** |
| (-4, 9, 6) | generic (Part 2 rerun) | **3** |
| (1/2, 3, 0) | fold-image point | **3** total = 1 (branch x=0, exact point (0, 3, -71/2)) + 2 (branch F3/x=0) |

So the recorded generic fiber cardinality is 3 on every target tested — geometric
degree 3, non-injective, consistent with claim (4). (Numeric root-finding with
certified back-substitution; not exact-Q, as in the original session.)

## S6 PART 3 LIVE-template list (RECORDED, as demanded)

`swept 22 P-candidates x 2 partner degrees; live templates found: 0`

LIVE list: **EMPTY**. The m=3 frontier sweep (nonconstant cusp x^3*y^3 + a2*y^2 +
a1*y + a0, a2 in {0,x,x^2,x^3}, a1 in {0,x,x^2}, a0 in {x, x^2+x}, binomials excluded,
partner degrees n = 4 with lead x^4 and n = 5 with lead x^5) produced NO live
templates: no "rung-2 signal" reproduces. Note the docstring frames PART 3 as "the
first slice the collapse machinery does not decide" — the machinery still returned
infeasible on every probe in this rerun; the docstring itself asserts no nonzero count,
so this is recorded as PASS with the empty list called out prominently.

## h0 = -13 * n3 cross-check (S7's h0 vs S10's n3) — computed ourselves, exact

Over Q(sqrt(-3)), written a + b*sqrt(-3):

    h0  = 1664/3 - (832/3)*sqrt(-3)     (Session 7 Wronskian constant)
    n3  = -128/3 + (64/3)*sqrt(-3)      (Session 10 leading cubic coefficient, printed by s10 run)
    -13 * n3 = 1664/3 - (832/3)*sqrt(-3)  ==  h0   EXACT (Fraction arithmetic)

The Sessions 16-18 ledger's "cross-epoch identity h0 = -13 n3" is CONFIRMED by
independent exact arithmetic (13*128 = 1664, 13*64 = 832, matching signs). This is the
one piece of the prose-only S16-18 ledger that is re-checkable from surviving data.

## Divergences

**NONE.** Every executable block (S1-S8, S10) reproduced its docstring's quantitative
claims exactly; no assertion tripped; no timeouts; empty stderr on all 14 blocks.

Caveats, for honesty:
1. S1's fiber counts are floating-point root-finding with certified back-substitution
   (tolerances 1e-8/1e-7, separation 1e-6) — evidence, not exact-Q proof. That is what
   the original session did too; the regression reproduces it faithfully.
2. S3 PART C2's three "FEASIBLE" lines are expected output (degenerate free-lead
   phantoms), resolved inside the same block by the pinned-lead PART D — not a
   divergence.
3. The prose-only sessions' theorems (notably the Sessions 16-18 First-Framework
   emptiness "theorem") are NOT re-certified by this regression. Their only surviving
   machine-checkable artifact re-verified today is h0 = -13*n3 (above). Treat the rest
   as claims pending Track C's re-derivation (master identity, chart factor, endgame
   operator).
4. Runtime environment: python3 + sympy available in-container; sympy version noted in
   scratch regress logs' environment (runs completed 2026-08-13 04:29 UTC).
