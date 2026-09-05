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

"""Session 43, Path S — the EXACT Euler filter on the slice family.

From pathS_tear.py / strata.py, the fibre structure of Alpoge's map F is
completely determined by ONE depressed cubic:  the x-coordinates of F^{-1}(w)
are exactly the roots of

    h(x;w) = Delta(w) x^3 + (4 - 3 w2 w3) x - 2 w3,
    Delta  = 27 w1^2 w3^2 - 18 w1 w2 w3 + w2^3 w3 + 16 w1 - w2^2   (irreducible quartic)

and (all verified exactly in strata.py):

    Delta != 0                          ->  fibre = 3 points
    Delta  = 0, w not in C_sing         ->  fibre = 1 point
    w in C_sing                         ->  fibre = 0 points   (outside the image)

    C_sing := Sing(Delta) = {Delta = 0} n {E = 0} = {Delta = 0} n {4-3w2w3 = 0}
            = the rational curve  ( 4/(27 t^2), 4/(3 t), t ),  t != 0,
    E := 27 w1 w3^2 - 9 w2 w3 + 8,   disc_x(h) = -4 E^2 Delta.

(E = 0 is NOT part of the tear: there the fibre still has 3 points, two of which
share an x-coordinate.  So the x-projection of S is 2:1 over E=0 and the
hypersurface {h=0} is singular there while S is smooth -- S is not {h=0}.)

Since chi is motivic, for a target plane W (= C^2) the slice S = F^{-1}(W) has

    chi(S) = 3*chi(W \ A_W) + 1*chi(A_W \ C_W) + 0*chi(C_W)
           = 3(1 - chi(A_W)) + chi(A_W) - #C_W
           = 3 - 2*chi(A_W) - #C_W                                          (*)

    A_W := W n {Delta = 0}   (a plane quartic),   C_W := W n C_sing  (<= 3 points).

S = C^2 forces chi(S) = 1, i.e.

    *** 2*chi(A_W) + #C_W = 2 ***                                           (**)

In particular #C_W must be EVEN, so #C_W in {0,2}: a plane meeting Sing(Delta)
in 3 distinct points (the GENERIC behaviour -- C_sing meets a plane in the roots
of 27c t^3 - 27k t^2 + 36b t + 4a) is excluded outright.  That already kills the
generic member of the family, which is why the H_1 filter alone was too weak.

This module computes chi of an affine plane curve EXACTLY (projection +
motivic additivity, no resolution), hence chi(S) exactly, and scans the family.
"""
import sympy as sp
from itertools import product

w1, w2, w3, T = sp.symbols('w1 w2 w3 T')
s, t = sp.symbols('s t')

DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)


def chi_affine_plane_curve(f, u, v):
    """Exact chi of the reduced affine plane curve {f=0} in C^2_{u,v}.

    Uses motivic additivity along the projection to u:
        chi = n_gen*(1 - #special) + sum over special u of #fibre,
    where #fibre counts DISTINCT points.  Exact: no floating point, no
    resolution of singularities.
    """
    f = sp.expand(sp.together(f))
    f = sp.Poly(f, u, v)
    # reduce: work with the squarefree part (the curve is a set)
    fe = sp.factor_list(f.as_expr())
    red = sp.Integer(1)
    for base, _m in fe[1]:
        if base.free_symbols:
            red *= base
    if not red.free_symbols:
        return 0                      # empty curve
    F = sp.Poly(sp.expand(red), v)    # as a polynomial in v over Q[u]
    if F.degree() == 0:
        # curve is {g(u)=0}: a union of vertical lines
        g = sp.Poly(sp.expand(red), u)
        return len(sp.roots(g, multiple=False))   # each line has chi = 1
    lc = sp.Poly(F.LC(), u)
    disc = sp.Poly(sp.expand(sp.discriminant(F, v)), u) if F.degree() >= 2 else None
    special = set()
    for poly in [lc] + ([disc] if disc is not None and disc.total_degree() > 0 else []):
        if poly.as_expr().free_symbols:
            for r in sp.roots(poly, multiple=False):
                special.add(sp.nsimplify(r))
        elif poly.as_expr() == 0:
            return None               # degenerate; caller should special-case
    n_gen = F.degree()                # generic #distinct roots (disc != 0 there)
    total = n_gen*(1 - len(special))
    for r in special:
        fr = sp.Poly(sp.expand(red.subs(u, r)), v)
        if fr.as_expr() == 0:
            return None               # a whole vertical line sits in the curve
        total += len(sp.roots(fr, multiple=False))
    return sp.Integer(total)


def plane_coords(a, b, c, k):
    """Return (substitution dict, the two free coordinates) for W: a w1+b w2+c w3=k."""
    if c != 0:
        return {w3: (k - a*w1 - b*w2)/c}, (w1, w2)
    if b != 0:
        return {w2: (k - a*w1 - c*w3)/b}, (w1, w3)
    return {w1: (k - b*w2 - c*w3)/a}, (w2, w3)


def n_Csing(a, b, c, k):
    """#(W n C_sing): distinct NONZERO roots of 27c t^3 - 27k t^2 + 36b t + 4a."""
    poly = sp.Poly(27*c*t**3 - 27*k*t**2 + 36*b*t + 4*a, t)
    if poly.as_expr() == 0:
        return sp.oo                          # plane contains C_sing (impossible: C_sing is non-planar)
    if poly.degree() < 1:
        return 0                              # nonzero constant: no roots
    return len([r for r in sp.roots(poly, multiple=False) if sp.simplify(r) != 0])


def chi_S(a, b, c, k):
    """Exact chi(F^{-1}(W)) via (*).  Returns (chi_S, chi_A_W, #C_W)."""
    sub, params = plane_coords(a, b, c, k)
    cut = sp.numer(sp.together(sp.expand(DELTA.subs(sub))))
    chiA = chi_affine_plane_curve(cut, params[0], params[1])
    if chiA is None:
        return None, None, None
    nC = n_Csing(a, b, c, k)
    if nC is sp.oo:
        return None, chiA, nC
    return sp.Integer(3) - 2*chiA - nC, chiA, nC


if __name__ == '__main__':
    print("controls (computed independently in strata.py / pathS_modification.py):")
    for (a, b, c, k), note in [((0, 1, 0, 0), "W={w2=0}: chi(S)=1 known, but pi_1(S)=Z"),
                               ((1, 0, 0, 0), "W={w1=0}: S splits, chi(S)=1"),
                               ((0, 0, 1, 0), "W={w3=0}: S splits, chi(S)=1")]:
        cs, ca, nc = chi_S(a, b, c, k)
        print("   (%s,%s,%s,%s)  chi(A_W)=%s  #C_W=%s  chi(S)=%s     %s"
              % (a, b, c, k, ca, nc, cs, note))

    print("\nSCAN: exact chi(S) over the (a,b,c,k) family (chi(S)=1 is necessary for S=C^2)")
    vals = [0, 1, -1, 2, -2, sp.Rational(1, 2), 3, sp.Rational(-1, 4), 4]
    hits, tally = [], {}
    for a, b, c in product([0, 1, -1, 2, -2, 3], repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        for k in [0, 1, -1, sp.Rational(-1, 4), 2, -2]:
            cs, ca, nc = chi_S(a, b, c, k)
            if cs is None:
                tally['degenerate'] = tally.get('degenerate', 0) + 1
                continue
            tally[int(cs)] = tally.get(int(cs), 0) + 1
            if cs == 1:
                hits.append((a, b, c, k, ca, nc))
    print("   chi(S) distribution over the scan:", dict(sorted(tally.items(), key=str)))
    print("   planes with chi(S) = 1 :", len(hits))
    for h in hits[:40]:
        print("      (a,b,c,k)=(%s,%s,%s,%s)   chi(A_W)=%s  #C_W=%s" % h)
