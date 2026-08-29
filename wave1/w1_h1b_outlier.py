#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 3c -- the 1.70e-09 outlier: RESOLVED as an
ARTEFACT of an unfixed gauge.  Not carried forward.

THE GAUGE GROUP ON P IS 3-DIMENSIONAL, not 2:

  g0  translation       P -> P + const                        (p_00 free)
  g1  overall scale     P -> cP,  Q -> Q/c                    (p_{j,i} -> c p_{j,i})
  g2  coordinate scale  (x,y) -> (lam x, lam^-3 y)            (p_{j,i} -> lam^{i-3j} p_{j,i})

g2 is forced by the bracket: [P.s, Q.s] = lam*mu*[P,Q].s and [P,Q] = x^2 give
lam^3 mu = 1.  It maps solutions to solutions, because each forbidden
coefficient is multiplied by a NONZERO power of lam, so zero stays zero.

WHY IT BROKE v2's OBJECTIVE.  Composing g2 with the g1 that restores p_10 = 1,
the coefficient of x^i in Q_j is multiplied by lam^{i-3j+1} -- an exponent that
DEPENDS ON i.  The forbidden coefficients are the LOW-i ones (i < j-12) and the
allowed ones are HIGH-i, so growing lam inflates the denominator of
   max_j ( max|forbidden| / max|allowed| )
relative to its numerator.  v2's objective is invariant under g1 but NOT g2.

MEASURED, on a random point (nothing solved anywhere along the path):

    lam      ratio            max|allowed|    max|forbidden|
    0.50     8.775618e+10     1.5469e+19      1.3575e+30
    1.00     8.317105e+07     1.0075e+05      8.9274e+09
    2.00     1.419786e+05     3.7918e-07      1.5478e-07
    4.00     7.394608e+02     5.6613e-18      5.4294e-19
    8.00     1.328516e+01     9.0506e-28      1.9752e-30
   16.00     9.777527e-01     8.4291e-37      7.1857e-42

The ratio falls monotonically by eleven orders of magnitude while the whole
configuration degenerates.

VERDICT ON THE OUTLIER: ARTEFACT.  Same disease as v1, one gauge deeper --
v1 collapsed the numerator, v2's outlier inflated the denominator.  The point
had max|allowed| = 2.16e+09 against max|forbidden| = 1.44, i.e. a nine-order
separation manufactured by drifting along g2, not by approaching a solution.

CONSEQUENCES, both corrections to earlier claims in this campaign:

 1. ESSENTIAL PARAMETER COUNT IS 58, not 60 (step 1b) or 59 (step 3 v2).
    61 lattice coefficients minus THREE gauge directions.  Against 60
    independent conditions, the pentagon system is OVERDETERMINED BY 2 modulo
    gauge -- before the 314 surplus conditions.

 2. ANY FUTURE DETECTOR must fix all three gauges (p_00 = 0, plus two
    coefficients of DIFFERENT weight i-3j, which pins g1 and g2 separately) and
    must impose an absolute normalisation, not a ratio.  A ratio objective is
    breakable from either end.

This file records the resolution; it is not a search.  See
w1_h1b_gauge_resolution.py for the executable checks.
"""
print(__doc__)
