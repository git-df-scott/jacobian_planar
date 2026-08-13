# Track A report — reconstruction of the GGHV (8,28) open system + sound eliminator

STATUS: IN PROGRESS (skeleton created at start; updated incrementally).
Steps: A1 system reconstruction [RUNNING], A2 normalization [PENDING],
A3 eliminator [PENDING], A4 elimination run [PENDING], A5 this report [PENDING].

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

## A3. Eliminator soundness design

[PENDING]

## A4. Elimination outcome

[PENDING]

## A5. Discrepancy ledger + confidence

[PENDING]
