"""Session 43 — Path S at geometric degree NINE: slicing F o F.

WHY.  Orevkov (1986) proves a planar Keller map of geometric degree 3 is an
automorphism, and Alpoge's map F has geometric degree 3 (fibre-size set {3,1,0},
Gao arXiv:2608.00222 Thm 3.4 = the stratification derived here).  So every slice
of F is dead before any computation: F|_S has degree 3 or 1.  The confirmed
floor is that degrees 2,3,4,5 are all excluded and 6 is OPEN.

The cheapest way over the floor needs no new counterexample from the literature:
COMPOSE.  F o F : C^3 -> C^3 has det J = (-2)^2 = 4, is non-injective, and has
geometric degree 3 x 3 = 9 >= 6.  So if S = (F o F)^{-1}(W) = C^2 for some plane
W, the induced planar map is Keller, non-injective, of geometric degree 9 --
excluded by NO known theorem.

THE COMPUTATION.  Write X -F-> Y -F-> Z, W a plane in Z, Sigma := F^{-1}(W) in Y
(this is exactly the surface the plane scan already studied, so chi(Sigma) is
known -- 1 for the 90 planes that passed the Euler filter), and
S := F^{-1}(Sigma) in X.  Applying the same stratification, now in Y:

    chi(S) = 3 chi(Sigma) - 2 chi(Sigma n A) - chi(Sigma n C_sing)

with A = {Delta = 0} in Y and C_sing = Sing(A).  Both intersections are
computable because A is rational and explicitly parametrized:

    A n {w3 != 0}  <->  (mu, r),  w = ( (mu+1)(mu-2)^2/27r^2, -(mu-2)(mu+2)/3r, r )
    A n {w3  = 0}  =  the parabola {16 w1 = w2^2}, parametrized by w2 = s
    C_sing         =  {mu = 0},  i.e. ( 4/27t^2, 4/3t, t )

and Sigma = { y in Y : l(F(y)) = k }.  So

    Sigma n A(parametrized)  =  { (mu,r) : l(F(w(mu,r))) = k },  r != 0
    Sigma n A(parabola)      =  { s : l(F(s^2/16, s, 0)) = k }
    Sigma n C_sing           =  { t : l(F(4/27t^2, 4/3t, t)) = k }

all plane/affine-line conditions, handled by the calibrated chi_exact.py.

chi(S) = 1 is then necessary for S = C^2, and the same H_1 test applies (S is
again cut out of C^3 by ONE equation, l(F(F(x,y,z))) = k, though it is no longer
linear in z, so the affine-modification form is not automatic -- flagged below).
"""
import sys
import sympy as sp
from itertools import product

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import chi_exact as CE

x, y, z = sp.symbols('x y z')
w1, w2, w3 = sp.symbols('w1 w2 w3')
mu, r, s, t = sp.symbols('mu r s t')

U = 1 + x*y
P = U**3*z + y**2*U*(4 + 3*x*y)
Q = 3*x*U**2*z + y + 3*x*y**2*(4 + 3*x*y)
R = -x**3*z + 2*x - 3*x**2*y
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)

# F written in the target coordinates (same map, applied to a point of Y)
FW = [f.subs({x: w1, y: w2, z: w3}, simultaneous=True) for f in (P, Q, R)]

# the three strata of the tear
PAR = {w1: (mu + 1)*(mu - 2)**2/(27*r**2), w2: -(mu - 2)*(mu + 2)/(3*r), w3: r}
PARAB = {w1: s**2/16, w2: s, w3: 0}
CSING = {w1: sp.Rational(4, 27)/t**2, w2: sp.Rational(4, 3)/t, w3: t}


def l_of_F(a, b, c, k, sub):
    """numerator of  a P(w) + b Q(w) + c R(w) - k  on a parametrized stratum."""
    e = sp.together(sp.expand(a*FW[0].subs(sub, simultaneous=True)
                              + b*FW[1].subs(sub, simultaneous=True)
                              + c*FW[2].subs(sub, simultaneous=True) - k))
    return sp.expand(sp.numer(e)), sp.expand(sp.denom(e))


def n_finite_roots(expr, var, exclude_zero=False):
    if expr == 0:
        return sp.oo
    p = sp.Poly(expr, var)
    if p.degree() < 1:
        return 0
    sq = sp.Poly(sp.quo(p, sp.gcd(p, p.diff(var))), var)
    n = sq.degree()
    if exclude_zero and sq.eval(0) == 0:
        n -= 1
    return n


def chi_sigma_cap_A(a, b, c, k, verbose=False):
    """chi(Sigma n A) = chi(curve in (mu,r) with r != 0) + #(Sigma n parabola)."""
    num, den = l_of_F(a, b, c, k, PAR)
    if num == 0:
        return sp.oo, None
    # the parametrized stratum needs r != 0; strip any r^j factor (r=0 is not
    # in this stratum) and then subtract the points of the curve with r = 0.
    num = sp.expand(num)
    while sp.simplify(sp.rem(num, r, r)) == 0 and num != 0:
        num = sp.expand(sp.quo(num, r, r))
    curve = sp.expand(num.subs({mu: CE.U, r: CE.V}, simultaneous=True))
    if not sp.sympify(curve).free_symbols:
        chi_tor = sp.Integer(0)
    else:
        chi_full = CE.chi_plane_curve(curve)
        at0 = sp.expand(curve.subs(CE.V, 0))
        n0 = n_finite_roots(at0, CE.U) if at0 != 0 else sp.oo
        if n0 is sp.oo:
            return sp.oo, None
        chi_tor = chi_full - n0
    npar, _ = l_of_F(a, b, c, k, PARAB)
    n_parab = n_finite_roots(sp.expand(npar), s)
    if n_parab is sp.oo:
        return sp.oo, None
    if verbose:
        print("      chi(torus part)=%s  #(parabola part)=%s" % (chi_tor, n_parab))
    return chi_tor + n_parab, (chi_tor, n_parab)


def n_sigma_cap_Csing(a, b, c, k):
    num, _ = l_of_F(a, b, c, k, CSING)
    return n_finite_roots(sp.expand(num), t, exclude_zero=True)


def chi_S_of_sigma(a, b, c, k, chi_sigma):
    cA, detail = chi_sigma_cap_A(a, b, c, k)
    if cA is sp.oo:
        return None, None, None
    nC = n_sigma_cap_Csing(a, b, c, k)
    if nC is sp.oo:
        return None, cA, nC
    return 3*chi_sigma - 2*cA - nC, cA, nC


if __name__ == '__main__':
    # chi(Sigma) for the plane, from the (corrected) first-stage computation
    from pathS_scan2 import plane_cut, n_Csing
    print("Path S at geometric degree 9:  S = (F o F)^{-1}(W) = F^{-1}(Sigma)")
    print("necessary for S = C^2:  chi(S) = 3 chi(Sigma) - 2 chi(Sigma n A) - #(Sigma n C_sing) = 1\n")
    vals = [0, 1, -1, 2, -2, 3]
    ks = [0, 1, -1, sp.Rational(-1, 4), 2]
    tally, hits, n_done = {}, [], 0
    for a, b, c in product(vals, repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        for k in ks:
            try:
                nCw = n_Csing(a, b, c, k)
                if nCw is sp.oo or nCw % 2 == 1:
                    continue
                cut = plane_cut(a, b, c, k)
                if not sp.sympify(cut).free_symbols:
                    continue
                chi_sig = 3 - 2*CE.chi_plane_curve(cut) - nCw
                if chi_sig != 1:
                    continue                      # only stage-1 survivors matter
                n_done += 1
                cs, cA, nC = chi_S_of_sigma(a, b, c, k, chi_sig)
                if cs is None:
                    tally['degenerate'] = tally.get('degenerate', 0) + 1
                    continue
                tally[int(cs)] = tally.get(int(cs), 0) + 1
                if cs == 1:
                    hits.append((a, b, c, k, cA, nC))
                    print("   *** chi(S)=1 at (a,b,c,k)=(%s,%s,%s,%s)  "
                          "chi(Sigma n A)=%s  #(Sigma n C_sing)=%s" % (a, b, c, k, cA, nC))
            except Exception as e:
                tally['ERR:' + type(e).__name__] = tally.get('ERR:' + type(e).__name__, 0) + 1
    print("\nplanes with chi(Sigma)=1 examined at stage 2:", n_done)
    print("chi(S) distribution:", dict(sorted(tally.items(), key=str)))
    print("candidates with chi(S) = 1:", len(hits))
