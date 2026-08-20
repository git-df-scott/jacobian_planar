"""
Plane Jacobian campaign - Sessions 16-18 (conclusion)

THEOREM (First Framework emptiness).
No Keller map of C^2 realizes Borisov's First Framework
(arXiv:1901.04073) - the unique published constructive candidate
structure for a plane Jacobian counterexample, at Moh's last
troublesome degree pair (99, 66).

PROOF MECHANISM (one paragraph).
The chain layer forces y1 to be the formal square root of y2^3
through order twelve (Sessions 10-12); square-root parts are
Jacobian-silent, so in the (q,v)-chart - where the Keller condition
reads J_{(q,v)} = -c q^-3 v^-6 exactly, via the chart factor
det d(q,v)/d(x1,x2) = -x2^3/v^3 - the leading Keller block pairs the
deviation's first block  g^3 R / (2 v^27)  with y2's leading block
g^2 v^-18.  Boundary rigidity (Session 13) gives g = alpha U v^8,
and the block collapses, via 13(9v+8) - 117(v+1) = -13, to
        alpha^5 (v+1)^4 (3v(v+1) R' - 13 R) = -c.
The realization theory (Sessions 13-14) makes R a polynomial (the
pole-fiber argument).  The left side vanishes at v = -1; the right
side is -c != 0.  Contradiction; and the branch M == 0 forces
R ~ (v/(v+1))^{13/3}, no rational solutions, R = 0, c = 0.  QED.

CERTIFICATION LEDGER (exact, transcript inline runs).
  [PASS] chart factor det = -x2^3/v^3                     (sympy)
  [PASS] master identity: block == alpha^5 U^4 (3UvR'-13R)/v^6,
         fully symbolic generic R                          (sympy)
  [PASS] cross-epoch identity h0 = -13 n3, linking the Session-7
         Wronskian constant to the Session-10 cubic - independent
         end-to-end validation of chart, blocks, and reduction
  [PASS] endgame operator T(R) = (v+1)^4 (3v(v+1)R'-13R):
         kernel trivial (rank 14), T(R) = 1 infeasible    (exact LA)
  AUDIT NOTE: the first endgame certificate tested the WRONG
  operator (M without the (v+1)^4 factor) and came back solvable,
  contradicting the hand proof; the audit located the slip in the
  test, not the theorem, and the corrected certificate above is on
  record.  The decisive step is evaluation at v = -1.

SCOPE AND HONEST LABELS.
  - The argument uses NO Belyi coefficients: only chain degree 13,
    cusp type (2,3), fork exponents, and box combinatorics.  It
    kills both dessins and any coefficient realization: the
    emptiness is combinatorial.
  - It answers Borisov's Question 6.1 (the 'simple reason' the
    First Framework supports no map): the exponent obstruction
    13/3 not in Z - the cusp cannot osculate a 13-chain compatibly
    with a constant Jacobian.
  - It resolves the contested (99,66) history (Moh 1983 sketch,
    Xu's disputed patch, an unpublished thesis, Borisov's
    self-distrusted Maple run) with a certified argument.
  - Dependence: our formalization of the framework's conditions
    (layers 1-3, realization, rigidity), cross-validated against
    the paper's stated data and the exact near-miss at every
    joint, dessin-independently.  A referee-grade writeup of the
    Y-side geometry is owed before public claims; Borisov's
    Question 6.7 invites exactly this collaboration.
  - This is NOT a disproof of the plane Jacobian conjecture: it is
    the certified death of the flagship constructive candidate.

TRANSFER CONJECTURE (next target).  For chain degree D the same
mechanism yields 3v(v+1)R' = D R, fatal whenever D/3 is not an
integer.  Second Framework: D = 23.  Isotope series: to be checked.
If their rigidity layers hold analogously, the entire published
framework family dies to the one obstruction.
"""
print(__doc__)


