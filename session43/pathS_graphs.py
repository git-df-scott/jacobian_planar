"""*** WITHDRAWN -- SUPERSEDED, DO NOT TRUST THE NUMBERS IN THIS FILE ***

This module ran on the pre-audit chi machinery, which carried three bugs:
  BUG 5  pairwise-only inclusion-exclusion (a point on >=3 components is
         over-subtracted), so chi(A_W) came out too SMALL, hence chi(S) too
         LARGE -- it wrongly REJECTED genuine candidates.
  BUG 6  points at infinity counted over Q instead of over C.
  BUG 7  a component dividing B is a 1-dimensional centre (S reducible), not
         an ordinary hit.
The fibre counts at special values also used mod-p majority voting rather than
exact arithmetic, and were simply wrong in places (the non-linear family was
reported as chi = -167, -258; the exact values are -3, -4, -5).

Replaced by chi_exact.py (25/25 calibrations), pathS_scan2.py and
pathS_graphs2.py.  Kept only so the corrected results can be diffed against the
wrong ones.
"""

"""Session 43, Path S, stage 2 — NON-LINEAR slices Sigma = C^2.

Plane slices are exhausted (pathS_scan.py: 7992 scanned, 0 survivors).  But the
Euler formula  chi(S) = 3 - 2 chi(A_Sigma) - #C_Sigma  used only chi(Sigma) = 1,
so it holds for EVERY Sigma = C^2 -- an infinitely bigger family.  Graphs

    Sigma_g = { w2 = g(w1,w3) }   ( = C^2 for every polynomial g )

are the natural next class, and the constraints pin g down almost completely.

DERIVATION (worked out by hand, checked by machine below).  Put v = w1 w3.  On
Sigma_g, with w2 = g,

    Delta|_Sigma = (9v + h)^3 w3 - 216 v^2 - 36 v h - h^2 + 16 w1,   g =: 9 v + h

(the 9v is forced: on C_sing = (4/27t^2, 4/3t, t) one has w2 = 4/(3t) and
9 w1 w3 = 4/(3t), so the term 9 w1 w3 is exactly what cancels the pole and lets
Sigma MISS C_sing.)  Then:

  * #C_Sigma = 0  <=>  h(4/27t^2, t) is a nonzero monomial in t, which forces all
    monomials of h onto one line j - 2i = m with sum h_ij (4/27)^i != 0;
  * chi(A_Sigma) = 1 needs ONE place at infinity, hence the top form of
    (9v+h)^3 w3 must be a power of a single linear form.  Writing d = deg h:
        d <  2 : top = 729 w1^3 w3^4          -> 2 points at infinity   FAIL
        d =  2 : top = w3^4 (9w1 + c w3)^3    -> 2 points at infinity   FAIL
        d >  2 : top = h_d^3 w3, so need h_d = c w3^d, and the single-weight-line
                 condition j-2i = d with i+j <= d forces i = 0, j = d exactly.
    So the ONLY graphs of this form that can work are

        *** Sigma_{d,c} = { w2 = 9 w1 w3 + c w3^d },   d >= 3,  c != 0 ***

    and there #C_Sigma = 0 (the difference on C_sing is c t^d != 0) and the top
    form is c^3 w3^(3d+1): exactly ONE point at infinity.

This module builds A_Sigma for that family and decides chi exactly.  A hit needs
chi(A_Sigma) = 1 AND no component = A^1; then S = F^{-1}(Sigma) = {Q = 9PR + cR^d}
is the candidate and goes to the full gate.
"""
import sympy as sp

import pathS_chi as CH

w1, w3, t, c = sp.symbols('w1 w3 t c')
u, v = CH.u, CH.v
DELTA = CH.DELTA
W1, W2, W3 = sp.symbols('w1 w2 w3')


def A_sigma(g):
    """The tear cut Delta|_Sigma in coordinates (w1,w3) -> (u,v)."""
    expr = sp.expand(DELTA.subs(W2, g))
    return sp.expand(expr.subs({W1: u, W3: v}))


def n_Csing_graph(g):
    """#(Sigma_g n C_sing): distinct nonzero roots of g(4/27t^2, t) - 4/(3t)."""
    e = sp.together(sp.expand(g.subs({W1: sp.Rational(4, 27)/t**2, W3: t})
                              - sp.Rational(4, 3)/t))
    num = sp.expand(sp.numer(e))
    if num == 0:
        return sp.oo
    p = sp.Poly(num, t)
    if p.degree() < 1:
        return 0
    sq = sp.Poly(sp.quo(p, sp.gcd(p, p.diff(t))), t)
    n = sq.degree()
    if sq.eval(0) == 0:
        n -= 1
    return n


def report(g, label):
    print("\n" + "=" * 72)
    print("Sigma : w2 =", g, "   [%s]" % label)
    nC = n_Csing_graph(g)
    cut = A_sigma(g)
    d, top, npts = CH.leading_form_places(cut, u, v)
    print("   #C_Sigma        =", nC)
    print("   deg A_Sigma     =", d, "   top form =", sp.factor(top),
          "  -> distinct points at infinity =", npts)
    fl = [b for b, _m in sp.factor_list(cut)[1] if b.free_symbols]
    print("   components      =", len(fl))
    chiA = CH.chi_curve(cut)
    print("   chi(A_Sigma)    =", chiA)
    if chiA is None or nC is sp.oo:
        print("   VERDICT: degenerate")
        return None
    chiS = 3 - 2*chiA - nC
    print("   chi(S)          =", chiS, "   (need 1)")
    if chiS != 1:
        print("   VERDICT: EULER-FAIL")
        return False
    bad = [f for f in fl if CH.is_isomorphic_to_A1(f, u, v)]
    if bad:
        print("   VERDICT: CHAU-FAIL, component = A^1:", bad)
        return False
    print("   *** VERDICT: SURVIVES chi AND Chau -- CANDIDATE ***")
    return True


if __name__ == '__main__':
    print("controls: the two shapes the derivation says must FAIL")
    report(9*W1*W3 + 1, "d=0: expect 2 points at infinity")
    report(9*W1*W3 + W3**2, "d=2: expect 2 points at infinity")

    print("\n\n" + "#" * 72)
    print("# THE DERIVED FAMILY:  w2 = 9 w1 w3 + c w3^d,  d >= 3")
    print("#" * 72)
    hits = []
    for dd in [3, 4, 5, 6, 7]:
        for cc in [1, -1, 2, sp.Rational(1, 2), -3]:
            g = 9*W1*W3 + cc*W3**dd
            r = report(g, "d=%d, c=%s" % (dd, cc))
            if r:
                hits.append((dd, cc))
    print("\n\nCANDIDATES from the derived family:", hits)
