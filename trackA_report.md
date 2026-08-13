# Track A report — reconstruction of the GGHV (8,28) open system + sound eliminator

STATUS: COMPLETE (2026-08-13, Wave 1).
A1 reconstruction DONE (case-2 counts match handoff 72/92; case-1 gap found).
A2 normalization PROVED. A3 sound eliminator DONE (selftests + certificate
replay). A4 elimination DONE for case (2) (2 open leaves; verified); case (1)
partially reduced (see A4). A5 = this report.

HEADLINE FOR TRACK B: the lost session's entire r0-r6 campaign lived in the
d_2_2 = 0 SLICE (leaf 1) of case (2) of Prop 4.3. Certificates show d_3_5 = 0
is forced globally, so Sol(case 2) = Sol(leaf 2) and leaf 1 = leaf 2 ∩
{d_2_2 = 0}: the never-explored generic locus d_2_2 != 0 of leaf 2 is new
ground, and closing LEAF 2 closes case (2). Case (1) (pentagons, 186/302 —
absent from the handoff) must ALSO die before any (8,28) closure claim.
Nonzero_exprs in the JSON are mandatory constraints (transferred vertex
nonvanishing) on every verdict.

## A1. What the paper actually says (quotes)

Source: arXiv:2204.14178 (GGHV), text extraction in scratch dir.

- Abstract: "We list all the pairs (deg(P), deg(Q)) with max{deg(P), deg(Q)} < 125 for any
  hypothetical counterexample to the plane Jacobian Conjecture and discard them all, except
  the pair (72, 108) (and the symmetric pair (108, 72))".
- Introduction (line 81-82 of extraction): "For the other case with (deg(P), deg(Q)) =
  (72, 108) we couldn't solve the corresponding system of polynomial equations, thus it is
  left open."
- The open shape is the table row "A0 = (8, 28), (m,n) = *(3,2), max = 108" (line 123);
  the closed (72,108) shape is "(9, 27), (2,3), 108" (line 126), discarded in section 5.
- Proposition 4.3 (Case (8,28)), lines 492-495: "If there is a counterexample to the
  Jacobian Conjecture in the case (8, 28), then there exist P, Q in L(1) with [P, Q] = x^2
  and one of the following cases holds:
  (1) N(P) = {(0,0),(1,0),(8,14),(8,16),(0,8)}, N(Q) = {(0,0),(2,1),(12,21),(12,24),(0,12)}.
  (2) N(P) = {(0,0),(1,0),(8,14),(8,16)},       N(Q) = {(0,0),(2,1),(12,21),(12,24)}"

The paper does NOT print an explicit coefficient system for (8,28) (its section 5 prints
systems only for (9,24)/(9,27), section 6 for (7,21)). The "corresponding system" is the
coefficient system of the bracket condition [P,Q] = x^2 on the Prop 4.3 supports.
Reconstruction below is from Prop 4.3 alone.

Ambient ring: L(1) = K[x, x^-1, y] (paper line 339). The stated Newton polygons confine
all support to the nonnegative quadrant, so P, Q are honest polynomials supported on the
polygon lattice points; a counterexample of this shape yields a solution of our system
with the vertex coefficients nonzero (solutions with smaller support are points with
extra zeros — automatically covered). Direction of use is closure-sound: closing BOTH
cases of the system closes the (8,28) shape.

Bracket right-hand side: [P,Q] = x^2 — verbatim from Prop 4.3 ("there exist P, Q in
L(1) with [P, Q] = x2"), NOT x (which is the (9,24)/(9,27)/(7,21) normalization) and
not a plain constant. Independently confirmed by Track E's literature verification
(orchestrator cross-check mid-run): no conflict.

## A1. Reconstructed system — counts vs the lost session

Built by trackA_gghv_system.py (exact Fractions, dict-of-monomials convolution).
Unknowns: c_i_j on lattice(N(P)), d_k_l on lattice(N(Q)); equations: every coefficient
of [P,Q] - x^2 (one bilinear equation per bracket lattice point; the (2,0) equation
carries the constant -1).

RESULT (verified by run):

| | supp P | supp Q | unknowns | equations | degree | hash (sha256) |
|---|---|---|---|---|---|---|
| case (2) quadrilaterals | 25 | 47 | **72** (70 active + inert c_0_0, d_0_0) | **92** | all 2 | f27a28a21a9bc6e615109a81ef93b578d6ffa6e09f373cbe7dc8b819ee98ab30 |
| case (1) pentagons | 61 | 125 | **186** (184 active + 2 inert) | **302** | all 2 | 49d28a2fd7ca72eb4064564d02084b2fab1612222d0c2c86b22ee1fe4702be9a |

VERDICT: the lost session's "72 unknowns / 92 quadratic equations" is EXACTLY
Prop 4.3 **case (2)** (including the two Jacobian-inert origin constants in the count).
Reconstruction MATCHES the handoff for case (2).

**PROMINENT DISCREPANCY / GAP:** Proposition 4.3 is a disjunction of TWO cases.
The lost session's 72/92 system covers only case (2). Case (1) — proof-branch c),
pentagon polygons with the extra vertices (0,8) and (0,12) — is a second, LARGER
system: 186 unknowns / 302 equations. No trace of it in the handoff. Even a complete
closure of every branch of the 72/92 system does NOT close the (8,28) shape; case (1)
must be closed too. Track B must know this.

Vertex-nonvanishing side conditions (polygon = exactly the stated hull):
case (2): c_1_0, c_8_14, c_8_16, d_2_1, d_12_21, d_12_24 all nonzero;
case (1): those plus c_0_8, d_0_12 nonzero.

Structural facts falling out of the reconstruction (useful downstream):
- The bracket point (2,0) equation is c_1_0*d_2_1 - 1 = 0 (single product pair), so
  c_1_0 * d_2_1 = 1 is forced; with the A2 normalization d_2_1 = 1 this gives c_1_0 = 1.
- The slope-2 edge subsystem: on the direction (2,-1) both polygons have their long
  edge (P: (1,0)->(8,14); Q: (2,1)->(12,21)) and v(P)+v(Q)-v(xy) = 2+3-1 = 4 =
  v(x^2), so the edge leading forms satisfy the INHOMOGENEOUS relation
  [x f(z), x^2 y g(z)] = x^2 with z = x y^2, i.e.  f g + z(2 f g' - 3 f' g) = 1,
  deg f = 7, deg g = 10, f(0) g(0) = 1 (f_k = c_{1+k,2k}, g_k = d_{2+k,1+2k}).
  This is precisely the "slope-2 Newton edge of Q, line j = 2i-3 from (2,1) to
  (12,21)" locus the lost session's 7-var/6-eq subsystem lived on (d_9_15 = g_7).

## A2. Scaling normalization d_2_1 = 1 — verdict: SOUND (nothing lost)

Executable proof in trackA_gghv_system.py --check-normalization; run output: all
claims PROVED for both cases.

Torus action exhibited: (P,Q) -> (a P(sx,ty), b Q(sx,ty)), acting on coefficients by
c_ij -> a s^i t^j c_ij, d_kl -> b s^k t^l d_kl.
- Equivariance proved exhaustively per term: every term of the (alpha,beta) bracket
  equation scales by the same factor a b s^(alpha+1) t^(beta+1) (index identity
  i+k-1 = alpha, j+l-1 = beta checked for all terms of all 92 resp. 302 equations);
  the unique inhomogeneous equation is (2,0), preserved iff a b s^3 t = 1.
- Which solutions does d_2_1 = 1 lose? NONE: d_2_1 != 0 is forced by the Prop 4.3
  polygon hypothesis (vertex (2,1) of N(Q)), and the explicit witness scaling
  (a,b,s,t) = (d_2_1, 1/d_2_1, 1, 1) satisfies the constraint and maps any solution
  to one with d_2_1 = 1. The locus d_2_1 = 0 is excluded by the side condition,
  not by the normalization — no separate branch needed.
- Residual freedom: the stabilizer of {d_2_1 = 1} is the 2-torus
  (a,b,s,t) = (1/s, 1/(s^2 t), s, t) — two more normalizations remain available
  downstream (consistent with the lost session's "after one more normalization" at
  the 7-var subsystem).
- Exact numeric equivariance spot check with random rationals: PASS (both cases).

## A3. Eliminator soundness design (trackA_eliminator.py)

- R1 on a single-monomial equation first divides out variables already known
  nonzero; empty remainder => contradiction (branch closed); one variable left =>
  deterministic v := 0; two or more => **or-branching: one child per variable**
  (u*w = 0 => u = 0 OR w = 0). No silent choice — the audit-item-#1 bug is
  structurally impossible. (Selftest 1 asserts a 2-child branch on u*w = 0.)
- R2 pivots only when the FULL coefficient of v in the equation is one term
  c*m with c in Q^x and m a monomial all of whose variables are known nonzero,
  AND m divides every monomial of the remainder B — divisibility checked at pivot
  SELECTION (the Session-20 infinite-loop fix; selftest 2). Then v := -B/(c*m)
  stays polynomial.
- If an eliminated variable was subject to a nonvanishing side condition, the
  condition transfers: the replacement polynomial is recorded in nonzero_exprs and
  a branch closes if such an expression becomes identically 0. States are
  dedup-merged ONLY when equations, nonzero set AND nonzero_exprs all agree
  (merging on equations alone would be unsound: a representative could close via
  a path-provenance constraint the merged path does not share).
- Sound enrichment: c*m + c0 = 0 with c, c0 nonzero constants forces every
  variable of m nonzero.
- Every closed branch emits a machine-replayable certificate; `--verify` replays
  certificates AND open-leaf states step-by-step against the root system with
  independent validation of each pivot/branch/contradiction.
- Exact Q (Fraction) primary; optional --mod P scouting (refuses P != 1 mod 3).
- 7 selftests cover: or-branching, divisibility-at-selection, pivot firing,
  nonzero-forced-zero, constant contradiction, cascade+sound dedup, enrichment.
- Semantics disclosure: the engine reasons at the level of SOLUTION SETS
  (varieties over Q-bar): v^e = 0 forces v = 0 and equation sets are dedup'd.
  This is exactly right for counterexample hunting and closure, but scheme
  multiplicities (e.g. the handoff's "multiplicity 10" at r0) are not tracked.

## A4. Elimination outcome (case (2), normalized d_2_1 = 1)

Run: `python3 trackA_eliminator.py --system trackA_system_case2.json
--normalize d_2_1=1 --out trackA_reduced_system.json` (20 s, exact Q).
Verified: `--verify` replays 2/2 open-leaf reduced systems exactly; rerun is
bit-identical (deterministic rule order).

- Root deterministic cascade: 43 R2 eliminations + 5 R1-det zeros
  (48 of 69 active vars eliminated; c_1_0 = 1 forced immediately from the (2,0)
  bracket equation c_1_0*d_2_1 = 1). Vertex variables c_8_14, c_8_16, d_12_21
  (and in leaf 1 also d_12_24) were R2-eliminated; their nonvanishing became
  recorded nonzero_exprs constraints — not dropped.
- Then exactly ONE R1 or-branch at the root, on  -2/3 * d_2_2^2 * d_3_5 = 0:
  - **Leaf 1 (d_2_2 := 0): 41 equations / 20 variables — EXACTLY the lost
    session's "20 vars / 41 eqs" state.** The 20 vars are the d-variables on the
    three lattice lines j = 2i-3, 2i-2, 2i-1 (i = 3..9). Inside it sits a closed
    subsystem of exactly 6 equations (indices 34-39) in exactly the 7 variables
    d_3_3, d_4_5, d_5_7, d_6_9, d_7_11, d_8_13, d_9_15 — the interior lattice
    points of Q's slope-2 edge j = 2i-3 from (2,1) to (12,21) (d_10_17 and
    d_11_19 having been R2-eliminated at the root). **The handoff's 7-var/6-eq
    edge subsystem claim is independently REPRODUCED.**
  - **Leaf 2 (d_3_5 := 0, d_2_2 free): 44 equations / 22 variables — NO
    counterpart in the handoff.** This is a branch the unsound "R1 forces a
    variable zero" eliminator silently dropped: audit item #1 is not just a
    theoretical bug, it lost a real branch at the very first fork. Track B must
    close leaf 2 as well before any (8,28)-case-(2) closure claim.
  - Branch containment (read off the certificates): inside leaf 1 the cascade
    subsequently FORCES d_3_5 = 0 (R1-det). Hence Sol(case 2) = Sol(leaf 2
    hypothesis), and Sol(leaf 1) = Sol(leaf 2) ∩ {d_2_2 = 0}. So **closing
    leaf 2 alone closes case (2)**; closing leaf 1 (where the lost session's
    whole r0-r6 campaign lived) only ever closed the d_2_2 = 0 slice. The lost
    branches are not a corner case — they are the generic (d_2_2 != 0) locus.
- Cap sensitivity: with --max-repl-terms unbounded, leaf 1 is unchanged and
  leaf 2 reduces one more step (43 eqs / 21 vars, eliminating vertex var d_12_24
  at the cost of a ~300-term transferred nonzero_expr). Official file keeps the
  44/22 form (cleaner vertex condition for saturation work).
- Residual scaling freedom for Track B: stabilizer torus acts by
  d_kl -> s^(k-2) t^(l-1) d_kl; on the edge subsystem it factors through
  u = s t^2 (one further normalization — consistent with the handoff's "after
  one more normalization" step), with an independent second direction scaling
  the j = 2i-2 line by t and j = 2i-1 by t^2.
- Case (1) (pentagons, 186/302): two runs.
  - Tight-pivot run (--max-repl-terms 25): TERMINATED, verified (1/1 leaf replay
    OK). Result: a single open leaf, **261 equations / 142 variables**, no
    or-branch reachable at this pivot size. File:
    trackA_reduced_system_case1_tight.json.
  - Default run (cap 400, 45-min time cap): the cascade eliminates ~1 var per
    rule application but total term count grows geometrically (~1.6x per 5
    eliminations: 19k terms at 35 apps, 213k at 60, 339k at 65) — naive
    substitution will not finish case (1); the run self-caps and dumps a valid
    intermediate state (trackA_reduced_system_case1.json). Instrumented, not
    guessed (per the "instrument before calling it hard" rule).
  - RECOMMENDATION for case (1): do not push plain R1/R2 further. The pentagon
    top edges (0,8)-(8,16) of P and (0,12)-(12,24) of Q sit at bracket level
    v_{-1,1}(P)+v_{-1,1}(Q)-v_{-1,1}(xy) = 20 > v_{-1,1}(x^2) = -2, so their
    leading forms must satisfy [lP, lQ] = 0, i.e. lP = a S^2, lQ = b S^3 for a
    single slope-1 form S with 5 coefficients ((0,4)..(4,8)). That factorization
    structure (invisible to R1/R2 pivots) is the natural entry point — Track
    B-style ideal decomposition or a parametrization by S.

## A5. Discrepancy ledger + confidence

| # | Handoff claim (Sessions 19-20, lost) | Verdict tonight |
|---|---|---|
| 1 | Prop 4.3 yields 92 quadratic equations in 72 unknowns | **REPRODUCED — but only for case (2)** of Prop 4.3 (72 = 25+47 lattice points incl. 2 inert constants; 92 bracket points; all equations bilinear). |
| 2 | (whole (8,28) shape = one 72/92 system) | **WRONG BY OMISSION: case (1) pentagons give a second system, 186 unknowns / 302 equations.** Closing case (2) does not close the shape. |
| 3 | scaling symmetry permits d_2_1 = 1 | **PROVED** (executable; loses nothing; d_2_1 != 0 is a polygon side condition; residual 2-torus remains). |
| 4 | iterated elimination reaches 20 vars / 41 eqs | **REPRODUCED as ONE OF TWO branches** (d_2_2 := 0). The sibling d_3_5 := 0 (22 vars / 44 eqs) was silently dropped by the unsound R1 — audit item #1 CONFIRMED in the wild. |
| 5 | closed 7-var/6-eq subsystem on interior points of Q's slope-2 edge j = 2i-3, (2,1)-(12,21) | **REPRODUCED exactly** (6 equations, 7 edge variables, inside leaf 1). |
| 6 | "one more normalization" available there | CONSISTENT (residual torus factors through u = s t^2 on the edge vars). |
| 7 | dim 0, vdim 1144, degree-43 eliminant in d_9_15, 7 branch factors r0-r6 | NOT CHECKED HERE — that is Track B's job, now with sound inputs. |

Cross-checks performed on the reconstruction itself:
- Bracket RHS is x^2 (Prop 4.3 verbatim; independently confirmed by Track E's
  literature pass — no conflict).
- Edge-ODE cross-check: the 18 system equations on the bracket line 2a-b = 4
  equal, term by term, the coefficients of f g + z(2 f g' - 3 f' g) - 1 for the
  edge sections f (deg 7), g (deg 10) — re-derived by hand calculus, PASS for
  both cases (function check_edge_ode in trackA_gghv_system.py).
- Content hashes (sha256) pin both systems; the eliminator refuses to verify a
  tree against a system with a different hash.

Confidence: HIGH on the reconstruction (counts + independent edge cross-check +
Track E corroboration), HIGH on eliminator soundness for the properties tested
(or-branching, pivot discipline, certificate replay), MEDIUM-HIGH that leaf 1 +
leaf 2 exhaust case (2) after normalization (rests on the engine's rule
completeness, exercised by selftests and full leaf replay). The case-(1) gap is
the dominant strategic fact.

## Files

- trackA_gghv_system.py — builder + A2 normalization proof + edge cross-check
  (sha256 1f274a54...)
- trackA_eliminator.py — sound branching eliminator + verifier + selftests +
  mod-p scouting mode (sha256 bb77c201...)
- trackA_system_case2.json (72/92, system hash f27a28a2...),
  trackA_system_case1.json (186/302, system hash 49d28a2f...),
  trackA_system_summary.json
- trackA_reduced_system.json — OFFICIAL Track-B input: case-(2) branch tree +
  reduced leaves + machine-replayable certificates + meta.trackB_annotations
  (verified 2/2 leaf replays)
- trackA_reduced_system_case1_tight.json — case-(1) tight-pivot reduction,
  single open leaf 261 eqs / 142 vars (verified 1/1)
- trackA_reduced_system_case1.json — case-(1) deeper cascade, time-capped
  intermediate state (valid resumable state; see log for growth data)
- trackA_elim_case2.log / trackA_elim_case1.log / trackA_elim_case1_tight.log
- Scouting smoke test: mod 65521 reproduces the exact-Q case-(2) tree shape
  (5 R1-det, 43 R2, 1 or-branch, leaves 41/20 and 44/22); p not = 1 mod 3 is
  refused. Scouting is evidence only, never proof; exact Q is the standard.

Reproduce everything:
  python3 trackA_gghv_system.py                  # build + counts + hashes + A2
  python3 trackA_eliminator.py --selftest
  python3 trackA_eliminator.py --system trackA_system_case2.json \
      --normalize d_2_1=1 --out trackA_reduced_system.json
  python3 trackA_eliminator.py --verify trackA_reduced_system.json \
      trackA_system_case2.json
