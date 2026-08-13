# Track B1 report — case (1) pentagons of GGHV Prop 4.3 (the second virgin territory)

STATUS: IN PROGRESS (2026-08-13). Skeleton created at start per checkpoint discipline;
sections fill in as steps complete. If this file looks truncated, the container died —
resume from the last completed section.

Input (hash-pinned): trackA_system_case1.json, 186 unknowns / 302 equations,
sha256 49d28a2fd7ca72eb4064564d02084b2fab1612222d0c2c86b22ee1fe4702be9a.
Nobody — paper, lost sessions, tonight's Track B — has ever attacked this system.

## Plan of record

- B1a: derive (not assume) the top-edge structure: equations on the bracket line
  beta - alpha = 20 are exactly the coefficients of [L_P, L_Q] = 0; prove
  L_P = a*S^2, L_Q = b*S^3 for a single slope-1 form S (5 coeffs), machine-checking
  every identity that can be machine-checked and writing out the one UFD step.
- B1b: substitute the parametrization into the 186/302 system (exact Fractions),
  quotient the 4-dim gauge (A2 torus + S-rescaling mu), run the sound eliminator.
- B1c: mod-p scout (65521 first) of the reduced core via Singular, Rabinowitsch
  ties for every nonzero side condition (incl. transferred ones).
- B1d: per-branch verdicts DEAD / alive-with-structure, with certificates.

## B1a. Derivation of the pentagon top-edge parametrization — DONE, ALL CHECKS PASS

Setup. Grade monomials by the weight v(x^i y^j) = j - i (direction (-1,1)).
On N(P) = conv{(0,0),(1,0),(8,14),(8,16),(0,8)} the maximum weight is 8, attained
exactly on the top edge (0,8)-(8,16) (lattice points (i, i+8), i = 0..8); on
N(Q) the maximum is 12, attained exactly on the top edge (0,12)-(12,24)
((k, k+12), k = 0..12). Since [x^i y^j, x^k y^l] lands at (i+k-1, j+l-1), the
bracket is additive in this weight, so the weight-20 component of [P,Q] is
exactly [L_P, L_Q] where L_P, L_Q are the top-edge leading forms. [P,Q] = x^2
has weight -2, hence

    [L_P, L_Q] = 0.        (*)

Machine checks (trackB1_pentagon.py --derive, exact Q, all PASS —
trackB1_derivation.json):

- C1: the system contains exactly 19 equations at bracket points on the line
  beta - alpha = 20, namely (n, n+20), n = 0..18.
- C2: each of them is  sum_{i+k=n+1} 4(3i-2k) c_{i,i+8} d_{k,k+12} = 0 — i.e.
  writing L_P = y^8 f(xy), L_Q = y^12 g(xy) with f_i = c_{i,i+8} (deg f = 8),
  g_k = d_{k,k+12} (deg g = 12), the 19 equations are precisely the coefficients
  of 4*(3f'g - 2fg') = 0. So (*) as read off the actual system is
  3f'g - 2fg' = 0. [Derived from the equations, not assumed.]
- C3: edge*edge products occur in NO other equation (structural: weight 20 needs
  top edge x top edge). Hence substituting the edge parametrization below leaves
  every other equation with terms at most LINEAR in substituted quantities.
- C5: independent code path (derivatives, not the builder's convolution)
  confirms [y^8 f(xy), y^12 g(xy)] = 4 y^20 (3f'g - 2fg')(xy).

Structure theorem for (*). Suppose f, g in K[u], K a field of char 0, f, g != 0,
and 3f'g - 2fg' = 0. Then (f^3/g^2)' = f^2 g (3f'g - 2fg') / g^4 = 0 (numerator
identity machine-checked as C6), so the rational function f^3/g^2 has zero
derivative, hence f^3 = c g^2 for some c in K^x (char 0). K[u] is a UFD: for
every irreducible pi, 3 v_pi(f) = 2 v_pi(g), so v_pi(f) = 2 t_pi and
v_pi(g) = 3 t_pi with t_pi := v_pi(f)/2 = v_pi(g)/3 a nonnegative integer.
Put h = prod pi^{t_pi}. Then f = alpha h^2, g = beta h^3 with alpha, beta in
K^x (and alpha^3 = c beta^2). Degrees: deg f = 8 forces deg h = 4; the vertex
conditions give f(0) = c_0_8 != 0 => h(0) != 0, and lc(f) = c_8_16 != 0 is
automatic for deg h = 4. NOTE this argument needs NO algebraic closure — it
works verbatim over any char-0 field.

Consequence (the parametrization, both directions):
- Every solution of the case-(1) system with its vertex conditions has
  L_P = a S^2, L_Q = b S^3 for some slope-1 form S = sum_{p=0..4} s_p x^p y^{p+4}
  (5 coefficients, s_0 = h-const, s_4 = lc(h)), a, b, s_0, s_4 != 0
  [surjectivity: UFD argument above, with S := y^4 h(xy)].
- Conversely c_{i,i+8} := a [S^2]_i, d_{k,k+12} := b [S^3]_k satisfies all 19
  top-line equations identically (machine check C4, symbolic, exact Q).

So Sol(case 1) is EXACTLY the image of the substituted system's solution set:
the parametrization loses nothing and adds nothing. Gauge redundancy of the
parametrization: (a, b, S) -> (a mu^-2, b mu^-3, mu S) gives the same (L_P, L_Q)
— quotiented soundly in B1b.

Variable naming in code: s_p_{p+4} for the S-coefficients (lattice points
(0,4)..(4,8)); a, b exist only transiently inside --build.

## B1b. Substituted system + gauge quotient + elimination

### The substituted, gauge-fixed system (trackB1_param_system.json)

Substitution (exact Fractions, machinery of trackA_eliminator):
c_{i,i+8} := a*[S^2]_i (i = 0..8), d_{k,k+12} := b*[S^3]_k (k = 0..12),
S = sum_{p=0..4} s_p_{p+4} x^p y^{p+4}. Then four normalizations, each backed by
a gauge argument:

1. d_2_1 = 1 — the A2 torus normalization, PROVED sound for case (1) by
   trackA_gghv_system.py --check-normalization (loses nothing; d_2_1 != 0 is a
   polygon side condition).
2. s_0_4 = 1 — the parametrization gauge mu: (a,b,S) -> (a mu^-2, b mu^-3, mu S)
   changes NO c/d coordinate (every substituted equation is a polynomial in the
   mu-invariants a[S^2]_i, b[S^3]_k and non-edge vars), and s_0_4 != 0 is forced
   by c_0_8 != 0. Take mu = 1/s_0_4.
3. + 4. a = 1, b = 1 — the residual A2 2-torus (a',b',s,t) = (1/s, 1/(s^2 t), s, t)
   fixes d_2_1 (weight identity s^{2-2} t^{1-1} = 1) and fixes s_0_4 (the mu-
   corrected action multiplies s_p_{p+4} by (st)^p; p = 0 is invariant), and acts
   on (a,b) by (a,b) -> (a s^-1 t^8, b s^-2 t^11). Exponent matrix
   [[-1,8],[-2,11]] has det 5 != 0, so the action on (a,b) in (Qbar^x)^2 is
   surjective (degree-5 torus isogeny): any solution moves to one with
   a = b = 1. a != 0, b != 0 are forced by the vertex conditions
   (c_0_8 = a s_0^2, d_0_12 = b s_0^3).

All four are emptiness-sound over Qbar (the proof standard for closure): the
gauge orbits of solutions meet the normalized slice. Directions of use:
Sol(case 1) = empty over Qbar  <=>  the normalized substituted system (with its
side conditions) has no Qbar-point. Any live point lifts back explicitly.

Result of --build (all self-checks PASS):
- dropped-as-identically-zero equations = EXACTLY the 19 top-line equations;
- the (2,0) bracket equation becomes c_1_0 - 1 = 0 (forces c_1_0 = 1);
- **283 equations / 165 variables**, degree profile {1: 1, 2: 100, 3: 50, 4: 132},
  largest equation 76 terms;
- side conditions: c_1_0, c_8_14, d_12_21, s_4_8 nonzero (c_0_8, c_8_16, d_0_12,
  d_12_24, d_2_1 transferred: first pair became "1 != 0" and "s_4_8 != 0" etc.,
  see meta.vertex_conditions_transferred);
- content hash 094bcd939f0ac42620212cd091ce046a61ee0902c1f55ed8b42704a106b390bb.

Comparison: raw case (1) is 302 eqs / 186 vars (bilinear); the parametrized
system is 283/165 of degree <= 4. The 22-variable top-edge pair is replaced by
4 s-variables; 19 equations are consumed exactly.

### Sound elimination (trackA_eliminator.py, exact Q)

Tight-pivot run (--max-repl-terms 25): TERMINATED in 16.6 s, 46 R2 + 3 R1-det
eliminations, no or-branch, single open leaf **233 equations / 116 variables**
(trackB1_reduced_tight.json); certificate replay `--verify`: 1/1 leaf OK.
Remaining nonzero facts at the leaf: d_12_21, s_4_8, one 13-term transferred
nonzero_expr. 116 variables is beyond direct Grobner range, which motivates the
weight-graded attack below.

### The weight tower (new structure, exploited for the first time)

The system is graded by the (-1,1)-weight (bracket point (alpha,beta) has
weight beta - alpha; the bracket adds weights). For a threshold W, the
equations of weight >= W involve ONLY the variables on the top lattice lines
(c-lines j - i >= W - 12, d-lines l - k >= W - 8, s-vars): a CLOSED subsystem.
Any full solution restricts to a truncation solution (with the side conditions
on the variables present), so **if any truncation is empty over Qbar, case (1)
is dead**. Sizes (equations of weight >= W / variables in the tower):

| W | eqs | vars | | W | eqs | vars |
|---|-----|------|-|---|-----|------|
| 19 | 20 | 26 | | 13 | 136 | 133 |
| 18 | 40 | 48 | | 12 | 153 | 143 |
| 17 | 60 | 69 | | 11 | 169 | 151 |
| 16 | 80 | 88 | | 10 | 184 | 157 |
| 15 | 99 | 105 | | 8 | 211 | 165 |
| 14 | 118 | 120 | | -2 | 283 | 165 (full) |

Crossover to formally overdetermined at W = 13. The top level (W = 19) is the
relation S*(2[S, Q_11] - 3*S*[S, P_7]) = 0 for the first sub-top lines; the
inhomogeneous x^2 equation sits at weight -2 (bottom of the tower only).
Eliminator on the near-top truncations (exact Q, verified terminating): W=19:
20/26 -> leaf 11 eqs/18 vars; W=18: 40/48 -> 27/36; W=17: 60/69 -> 44/54 — all
still underdetermined, consistent with the witness family below. NOTE the
normalization d_2_1 = 1 injects weight-(-1) data into the truncations: a
weight-w equation may contain c-variables of weight w+1 through its
(former) d_2_1 terms; the truncations remain closed subsystems and the
soundness direction (empty truncation => case (1) dead) is unaffected.

### STRUCTURE THEOREM 1 (exact witness): where a kill can and cannot live

trackB1_pentagon.py --witness, exact Q, PASS (trackB1_witness.json):
the point corresponding to  P = Stilde^2, Q = Stilde^3,
Stilde = y^4*(1 + (xy)^4) + t*x^4*y^7  (t = 1) — supports verified inside the
pentagons, [P,Q] = 0 identically — satisfies EVERY equation of the normalized
substituted system EXCEPT exactly seven: the inhomogeneous (2,0) equation
(weight -2) and the six equations where the baked-in d_2_1 = 1 multiplies a
nonzero family coefficient ((1,8), (5,11), (5,12), (9,14), (9,15), (9,16) —
weights 5, 6, 7). Its side-condition values c_8_14 = 1, d_12_21 = 1,
s_4_8 = 1 are nonzero. Consequences, all certified:

- **Truncations W >= 8 of the normalized tower are ALIVE** — no compute needed
  there, and the formal overdetermination at W <= 13 is misleading: the
  equations are highly non-generic (the commuting family P = Stilde^2,
  Q = Stilde^3 sweeps through them).
- **Any death of case (1) must use equations of weight <= 7**, i.e. must
  engage the bottom-vertex data c_1_0 * d_2_1 = 1 (the x^2 equation and its
  weight-(-1)/(-2) neighborhood) against the top structure. On the commuting
  family c_1_0 = d_2_1 = 0 is FORCED (a nonzero (1,0)- resp. (2,1)-coefficient
  of a square resp. cube supported in N(P)/N(Q) would need x^2- resp.
  x^4y^2-support outside the polygons). This is the precise algebraic form of
  "functional dependence at the top vs [P,Q] = x^2 at the bottom" for the
  pentagon shape — localized to 7 named equations.

### STRUCTURE THEOREM 2 (tower-compare): case (1) and case (2) share their
### slope-2 tower down to level 2

trackB1_pentagon.py --tower-compare, exact term-for-term comparison of the RAW
case-(1) and case-(2) systems (both hash-pinned), PASS:

- For every (2,-1)-weight w >= 2 (w = 2alpha - beta of the bracket point), the
  equation sets are IDENTICAL — same bracket points, same terms, same
  coefficients. This includes the 18-equation inhomogeneous slope-2 edge ODE
  (f g + z(2fg' - 3f'g) = 1) at w = 4, x^2 included.
- Divergence starts exactly at w = 1 (same bracket points, different terms)
  and w <= 0 (case (1) has extra bracket points; below w = -1 only case (1)
  continues — 13..19 equations per level down to w = -8).

Consequences: (i) any closure argument that uses only slope-2-tower levels
w >= 2 would kill BOTH cases at once; (ii) conversely, everything
case-(1)-specific — the pentagon columns and the S-parametrization — lives at
(2,-1)-weight <= 1; (iii) the case-2 branch analysis (Track B leaf 2) and the
case-1 attack share their upper tower exactly, so any structure Track B proves
about the edge-ODE levels transfers verbatim.

### Shape of the reduced core (tight run)

In the normalized system every c-variable acquires a LINEAR occurrence (its
former pairing with d_2_1 becomes a c_ij-linear term), and every d_kl with
l != 0 likewise via c_1_0 = 1; the cascade therefore solves the entire c-side
in terms of the d-side. Tight-run leaf inventory: remaining variables are the
d-side almost intact (100 d-vars on lines l-k = 0..11), the 4 s-vars, and 12
straggler c-vars on lines 5..7; eliminated: 39 c-vars, 10 d-vars. The core is
"the coefficients of Q + the top form S, modulo compatibility" — favorable
shape for a GB engine (massively linear-solvable), which motivates a direct
Singular mod-p scout of the substituted system after the deeper elimination
pass completes.

### Deep elimination beyond the tight leaf: ABANDONED (measured blowup)

Both the exact cap-120 run and a mod-65521 eliminator run were killed by a
container restart while exhibiting super-exponential fill-in: largest equation
2018 -> 16534 terms between rule apps 50 and 60, total terms 75k -> 494k
(trackB1_elim_cap120.log, trackB1_elim_modp.log — identical growth mod p, so
this is structural fill-in, not coefficient swell). The eliminator's role ends
at the tight leaf (233/116); the core goes to a GB engine instead.

## B1c. mod-p scout

RESUME NOTE (2026-08-13 ~14:30 UTC, post-restart). First scout attempt before
the restart targeted the RAW W=19 truncation (26 vars + 1 Rabinowitsch var,
21 eqs) and ran out of memory at ~866MB under a 1.8GB address-space cap
(trackB1_trunc19_p65521.out) — an expensive way to learn what the witness
already certifies: truncations W >= 8 are ALIVE (high-dimensional), and GB of
a high-dimensional alive truncation is both hard and pointless. Scouting
truncations W >= 8 is hereby dropped; per Structure Theorem 1 any kill engages
weight <= 7, so the scout target is the FULL normalized substituted system
(283 eqs / 165 vars + 4 Rabinowitsch ties for c_1_0, c_8_14, d_12_21, s_4_8;
input total ~8.6k terms, far sparser than the eliminator leaf whose
substitutions inflated it to ~67k terms).

Plan of record (in flight):
1. Full system, p = 65521, dp, Rabinowitsch, option(prot), 6.2GB vmem cap,
   output streamed to trackB1_sysfull_p65521.out (survives restarts).
2. If it finishes: repeat at p = 65497, 65479 (one Singular at a time — CPU
   courtesy to the Track B/C jobs sharing this box).
3. If it blows up: weight-peeling fallback — incremental GB down the tower
   (G_{W} = groebner(G_{W+1} + level W), checkpointed per level), which
   localizes both the cost and the death level.

(running)

## B1d. Verdicts

(pending)

## Artifacts

- trackB1_pentagon.py — all derivation/build/scout code (subcommands)
- trackB1_param_system.json — substituted, normalized system (built in B1b)
- trackB1_reduced.json — eliminator output tree (B1b)
- trackB1_*.sing / *.out — Singular scout scripts and outputs (B1c)
