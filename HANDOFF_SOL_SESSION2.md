# Handoff to Sol — JC2 campaign, end of session 2

## The reduction

The hunt is now the MATE PROBLEM: find P with
  (a) unimodular gradient — 1 in (P_x, P_y), i.e. no critical points
  (b) non-coordinate
  (c) a polynomial Q with P_x*Q_y - P_y*Q_x = 1
Any such (P,Q) is a counterexample. For fixed P, (c) is LINEAR in Q's coefficients.

## Established this session (machine-certified, in repo)

1. THEOREM (unconditional, night19). P = g*x*y^2 + c*y has NO polynomial mate of any degree.
   [P, x^i y^j] = (j-2i)*g*x^i y^{j+1} - c*i*x^{i-1} y^j, so each column meets at most two rows.
   Lambda((xy)^n) = (-1)^n c^n/((n+1) g^n), zero off-diagonal, annihilates every column and pairs
   to 1 with the target. Verified D = 2..60. Transports by a Jacobian-1 change of variables to a
   5-parameter family.

2. MECHANISM. P is isobaric for the MIXED weight w(x) = -1, w(y) = +1. The bracket raises weight
   by exactly 1, so only one monomial chain can reach the weight-0 target; the recursion never
   terminates; its formal sum is a RATIONAL mate Q = -x/(g*x*y + c) whose POLES lie on the second
   component of the REDUCIBLE zero fibre P = y*(g*x*y + c). The mate exists, it just is not polynomial.

3. THE STRUCTURAL FLAW IN THE WHOLE SEARCH. Every P tested this session was certified non-coordinate
   BY having a reducible or disconnected fibre - exactly the feature that creates that pole.
   Independently confirmed: all 57 period-survivors have reducible atypical fibres.

4. PERIOD OBSTRUCTION (night15, validated). A mate forces eta = dy/P_x = -dx/P_y to be exact on every
   fibre, so all periods vanish. Kills 193 of 256 certified P outright. Controls: 8 coordinates all
   vanishing, 3 negative exhibits, sum-of-residues identically 0.

5. ALL EMPTY. 256 screened -> 57 survivors -> 57/57 EMPTY beyond 2*deg P; 19 synthesised to satisfy
   every necessary condition -> 19/19 EMPTY; 18 targets at degree 124-132 -> 18/18 EMPTY. Hundreds of
   lambda-certificates, independently re-verified, 0 failures. Solver controls recover genuine mates
   in 1805-unknown systems at degree 84, so these are not tool weakness.

6. Also closed: subcase 2 of the (72,108) exceptional case in characteristic zero (4/4 unit ideals over
   the degree-35 number field, Bezout and inconsistency certificates verified).

## Live target (night20, running)

P unimodular with ALL FIBRES IRREDUCIBLE and generic fibre GENUS >= 1. Automatically non-coordinate
(coordinates have all fibres isomorphic to the affine line). Neumann-Norbury forces genus >= 1, since
rational irreducible fibres imply a coordinate. Generator: Newton polygons with interior lattice points
(Baker's bound gives positive genus).

## Tasks

T1 THE POLE THEOREM (crux). For P unimodular consider D_P(Q) = 1, D_P = P_x d_y - P_y d_x. Does a
   rational solution always exist, and where can its pole divisor live? On the night19 family the pole
   sat on the extra component of a reducible fibre. For P with all fibres irreducible and genus >= 1,
   is a pole still forced? Forced pole = the conjecture's mechanism, a theorem. Not forced = the
   pole-free locus is where a counterexample lives. Use ker D_P = C[P], Jelonek, Neumann-Norbury.

T2 EFFECTIVE MATE-DEGREE BOUND. Every EMPTY except night19's is carrier-relative. Mates are defined
   modulo Q + h(P), so is the MINIMAL mate degree bounded by f(deg P)? Newton-polygon similarity for
   Jacobian pairs (GGV arXiv:1401.1784 section 5), Cheng-McKay-Wang younger mates (Proc AMS 123 (1995)
   2939-2947), Bezout/geometric-degree accounting at infinity. An effective f makes every EMPTY
   unconditional and all future mate decisions decisive.

T3 THE SECOND OBSTRUCTION. By Grothendieck comparison, vanishing periods on a smooth affine fibre mean
   eta is exact in algebraic de Rham there, so a regular primitive Q_c exists fibrewise. The failure is
   assembling them: constants of integration, degree growth of Q_c in c, or torsion in the relative
   de Rham module H^1_dR(C^2/C) over C[P] (our P have no critical points but do have atypical values, so
   the fibration is not locally trivial). Give the precise obstruction and whether it is computable -
   Gauss-Manin / Griffiths-Dwork, or coker(D_P) as a D-module computation.

T4 GENERALISE THE THEOREM. Night19 rests on isobaricity for a mixed weight. Characterise all P isobaric
   for some mixed weight (w(x) < 0 < w(y)): do they all admit the analogous chain certificate, hence no
   mate? That is a theorem covering an infinite class, and it says a counterexample's P cannot be
   mixed-isobaric - another design constraint.

T5 ADVERSARIAL. Attack all of the above. One idea was already corrected: a scalar holonomy is only
   defined when every column meets exactly two rows, i.e. the acyclic case. Rank-2 supports still gave
   certificates at every carrier tested, so richer support alone is not sufficient. What else is wrong?

Format as always: verdicts first, objects with checkers or citations with quotes, holes named.
