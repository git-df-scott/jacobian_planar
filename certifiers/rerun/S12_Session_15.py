"""
Plane Jacobian campaign - Session 15
Box-cap verification (user-gated) + three structural results.

VERIFICATION (transcript inline run, exact):
  - per-block caps: deg B~_{-6+m} <= min(18, floor((54-m)/3)), so
    deg sigma_m <= -ceil(m/3), shown for m = 1..13;
  - all 101 partitions of 13 enumerated: max of 39 - sum ceil(m_i/3)
    equals 34, floored by superadditivity sum ceil >= ceil(13/3) = 5;
  - extremal-data PER-TERM check: every partition term of v^39 S_13
    has degree <= 34, max exactly 34 - no reliance on cancellation;
  - A~_4 reach: i <= (72-4)/3 = 22, reach 15 + 22 - 3 = 34.
The Session-14 claim stands, now shown rather than asserted.

RESULT 1 (affine-u tightening).  Theorem 3 puts R's pole fiber at the
order-13 point, so u^{-1}(inf) = inf and the target Moebius u is
AFFINE:
    R(v) = lambda * B13((v - v0)/sigma) + nu,
a 4-parameter family.  Realization cost, corrected: membership of
R's 14 coefficients in this family (10 conditions) + U^3-polynomiality
(3 conditions) ~ 13 conditions total against 190 parameters.

RESULT 2 (branch valuations explained and saturated).  The long-
mysterious (45,30) 0-curve valuation is nu(q) = 5 over the marked
point v = b (the simple {0}-fiber point of R): 45 = 5*9, 30 = 5*6,
matching BOTH the paper's stated valuations and the pullback formula
phi*(F0) = 5 E0 + (2 E_-1 + E_-3) + (2 E1 + E3); the branch (-1)
carries 2*(9,6) = (18,12) likewise.  Every branch pole-inequality is
exactly SATURATED by the q^-9 / q^-6 leading terms: the inequalities
are automatic and impose nothing.  The branch layer's true content is
second-order.

RESULT 3 (the cusp discovery).  Every Y-side boundary valuation
outside the line-side chain is proportional to (3,2): the clusters
(-3,-2), (-6,-4), (-9,-6).  Hence y1^2/y2^3 == 1 along the ENTIRE
outer boundary, and the whole outer framework - chain, realization,
and now the branch layers - is governed by the contact geometry of
the single cusp function
    c2 := y1^2 - y2^3
against the boundary configuration.  The branch conditions are
second-order JET conditions of c2 at the marked points of R (and of
the (-5)-side Belyi map); Borisov's (e1, e2) are the free jet moduli
at the order-5 point v = a of the long branch.  Session 16 derives
the required contact orders of c2 along the {0}/{1}-branch curves and
imposes the jet conditions - the layer where the surviving family
should finally shrink to Borisov's dozen, with Keller behind it.
"""
print(__doc__)
