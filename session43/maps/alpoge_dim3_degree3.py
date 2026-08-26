#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alpoge's original dimension-3 counterexample  (geometric degree 3)

CONTROL / reference map, reproduced exactly from the literature.  Included
to validate the verification pipeline that the other files use.
NOTE: geometric degree 3 -- NOT useful if you need degree >= 6.

Source of the construction:
  Shuhong Gao, "Counterexamples to the Jacobian conjecture in dimensions
  greater than two", arXiv:2608.00222 (31 Jul 2026), sections 3.1-3.5
  ("the tangent sweep of a plane curve" + "the monomial twist").
  HTML: https://arxiv.org/html/2608.00222
  The same dimension-3 family is Gallagher's, doi:10.5281/zenodo.21479195.
  The components reproduce Alpoge's published map verbatim (Gao sec. 3.4):
     f1 = (1+xy)^3 z + y^2(1+xy)(4+3xy)
     f2 = y + 3x(1+xy)^2 z + 3xy^2(4+3xy)
     f3 = 2x - 3x^2 y - x^3 z
  Below they are listed in the sweep order (C, P/C, Q/C^2) = (f3, f2, f1),
  which reverses Alpoge's order and so flips det J from -2 to +2.

Run:  python3 alpoge_dim3_degree3.py
Exits 0 if every check PASSES, nonzero otherwise.
"""
import sys
import sympy as sp

x, y, z, w = sp.symbols('x y z w')
R = sp.Rational

FAILURES = []


def check(name, ok, detail=""):
    print(("  [PASS] " if ok else "  [FAIL] ") + name + (("  " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


# ===========================================================================
# THE MAP  F : C^3 -> C^3     (explicit polynomials)
# ===========================================================================
F1 = (
    (-1)*x**3*z + (-3)*x**2*y + (2)*x
)

F2 = (
    (3)*x**3*y**2*z + (9)*x**2*y**3 + (6)*x**2*y*z + (12)*x*y**2 + (3)*x*z + (1)*y
)

F3 = (
    (1)*x**3*y**3*z + (3)*x**2*y**4 + (3)*x**2*y**2*z + (7)*x*y**3 + (3)*x*y*z + (4)*y**2
    + (1)*z
)

F = [F1, F2, F3]

# --- generating data (provenance; see module docstring) --------------------
P_OF_W = (-3)*w**2 + (4)*w**1
Q_OF_W = (-1)*w**3 + (1)*w**2          # q(w) = int_0^w (s/2) p'(s) ds
G0 = 2
A  = -3
B  = -1
CLAIMED_DEGREE = 3          # = deg(p) + 1
CLAIMED_DETJ   = 2


def main():
    print(__doc__.strip().splitlines()[0])
    print("=" * 74)

    # -----------------------------------------------------------------
    print("\n(0) Shape of the map")
    degs = [sp.Poly(f, x, y, z).total_degree() for f in F]
    nter = [len(sp.Poly(f, x, y, z).terms()) for f in F]
    print("    component total degrees :", degs)
    print("    component term counts   :", nter)
    check("F has 3 polynomial components in 3 variables",
          all(sp.Poly(f, x, y, z).total_degree() >= 0 for f in F))

    # -----------------------------------------------------------------
    print("\n(a) Jacobian determinant is a nonzero CONSTANT")
    J = sp.Matrix(F).jacobian(sp.Matrix([x, y, z]))
    detJ = sp.expand(J.det())
    print("    det J =", detJ)
    check("det J is constant", detJ.free_symbols == set(),
          "(free symbols: %s)" % (detJ.free_symbols or "none"))
    check("det J is nonzero", detJ != 0)
    check("det J equals the claimed value %s" % CLAIMED_DETJ,
          sp.simplify(detJ - CLAIMED_DETJ) == 0)

    # -----------------------------------------------------------------
    print("\n(a') Provenance identities (tangent sweep + monomial twist)")
    gamma = G0 + A * x * y + B * x**2 * z
    u = 1 + x * y
    W_ = sp.expand(gamma * u)
    id1 = sp.expand(F1 - gamma * x)
    id2 = sp.expand(F2 * F1 - (P_OF_W.subs(w, W_) + 2 * gamma))
    id3 = sp.expand(F3 * F1**2 - (Q_OF_W.subs(w, W_) + gamma * W_))
    check("F1 == gamma*x", id1 == 0)
    check("F2*F1 == p(w) + 2*gamma      with w = gamma*(1+xy)", id2 == 0)
    check("F3*F1^2 == q(w) + gamma*w    with w = gamma*(1+xy)", id3 == 0)
    check("q' == (w/2) p'  (inflection-free normal form, eq.(1))",
          sp.expand(sp.diff(Q_OF_W, w) - w * sp.diff(P_OF_W, w) / 2) == 0)

    # -----------------------------------------------------------------
    # These identities make the fibre correspondence ELEMENTARY:
    #   on F^-1(v) with v1 != 0 we must have x != 0 and gamma != 0
    #   (because gamma*x = v1), the chain (x,y,z) <-> (x,gamma,w) is
    #   invertible there, and (P,Q) = (v1*v2, v1^2*v3) forces
    #        W(w) := q(w) + (w/2)(X - p(w)) - Y = 0,   X=v1*v2, Y=v1^2*v3.
    #   So the fibre injects into the roots of W  (=> size <= deg W),
    #   and every root with gamma != 0 gives a point (=> size >= #roots).
    # -----------------------------------------------------------------
    print("\n(b) MEASURED geometric degree (# points in a generic fibre)")
    targets = [(R(3, 2), R(-5, 7), R(2, 5)),
               (R(-4, 3), R(7, 5), R(1, 6)),
               (R(5, 4), R(3, 11), R(-2, 9)),
               (R(7, 3), R(-2, 9), R(5, 8))]
    measured = []
    for tgt in targets:
        n, ok, info = fibre_size_exact(tgt)
        measured.append(n)
        print("    target %-28s -> %s points   %s" % (str(tgt), n, info))
        check("fibre over %s fully certified" % (str(tgt),), ok)
    check("MEASURED geometric degree == %d at every target" % CLAIMED_DEGREE,
          all(n == CLAIMED_DEGREE for n in measured),
          "measured = %s" % measured)
    if not all(n == CLAIMED_DEGREE for n in measured):
        print("    *** WARNING: measured degree disagrees with the claim! ***")

    # -----------------------------------------------------------------
    print("\n(b') INDEPENDENT re-measurement by resultant elimination")
    print("     (uses ONLY the polynomials F1,F2,F3 -- no appeal to the sweep theory)")
    for tgt in targets[:2]:
        nd, info = independent_resultant_count(tgt)
        print("    target %-28s -> %s distinct solutions   %s" % (str(tgt), nd, info))
        check("independent elimination over %s gives %d" % (str(tgt), CLAIMED_DEGREE),
              nd == CLAIMED_DEGREE, "(got %s)" % nd)

    # -----------------------------------------------------------------
    print("\n(c) EXPLICIT COLLISION: %d distinct points with one common image" % CLAIMED_DEGREE)
    import mpmath as mp
    pts, tgt = explicit_collision(targets[0])
    for i, P in enumerate(pts):
        print("    p%-2d = ( %s ,"  % (i + 1, mp.nstr(P[0], 18)))
        print("            %s ,"    % mp.nstr(P[1], 18))
        print("            %s )"    % mp.nstr(P[2], 18))
    resid, fl = [], [sp.lambdify((x, y, z), f, 'mpmath') for f in F]
    for P in pts:
        for i, v in enumerate(tgt):
            tvv = mp.mpf(sp.Rational(v).p) / mp.mpf(sp.Rational(v).q)
            resid.append(abs(fl[i](P[0], P[1], P[2]) - tvv))
    print("    common image      :", tuple(str(t) for t in tgt))
    print("    max |F(p_i) - v|  : %s   (computed at %d digits)" % (mp.nstr(max(resid), 5), mp.mp.dps))
    check("all %d points map to the same target" % CLAIMED_DEGREE, max(resid) < mp.mpf('1e-30'))
    seps = [max(abs(pts[i][k] - pts[j][k]) for k in range(3))
            for i in range(len(pts)) for j in range(i + 1, len(pts))]
    print("    min pairwise separation : %s" % mp.nstr(min(seps), 5))
    check("the %d points are pairwise distinct" % CLAIMED_DEGREE, min(seps) > mp.mpf('1e-12'))
    check("collision has >= %d points (=> geometric degree >= %d)"
          % (CLAIMED_DEGREE, CLAIMED_DEGREE), len(pts) >= CLAIMED_DEGREE)

    # -----------------------------------------------------------------
    print("\n" + "=" * 74)
    if FAILURES:
        print("RESULT: FAIL  (%d failed check(s): %s)" % (len(FAILURES), ", ".join(FAILURES)))
        return 1
    print("RESULT: ALL CHECKS PASSED")
    print("  dimension              : 3")
    print("  det J                  :", CLAIMED_DETJ)
    print("  MEASURED geometric deg :", CLAIMED_DEGREE)
    return 0


# ===========================================================================
# machinery
# ===========================================================================
def tangency_poly(target):
    """W(w) = q(w) + (w/2)(X - p(w)) - Y,  X = v1 v2, Y = v1^2 v3."""
    v1, v2, v3 = target
    X, Y = v1 * v2, v1**2 * v3
    return sp.Poly(sp.expand(Q_OF_W + R(1, 2) * w * (X - P_OF_W) - Y), w)


def fibre_size_exact(target):
    """
    EXACT count of #F^{-1}(target) over C.

    Upper bound: by the provenance identities, the fibre injects into the
    roots of W, so #fibre <= deg W.
    Lower bound: we verify IN THE RING QQ[w]/(W) that the formulas
        x = v1/gamma,  u = w/gamma,  y = (u-1)/x,  z = (gamma-G0-A(u-1))/(B x^2)
    satisfy F(x,y,z) == target identically.  With W squarefree this
    exhibits deg W distinct points at once.
    """
    v1, v2, v3 = target
    W = tangency_poly(target)
    deg = W.degree()
    squarefree = sp.Poly(sp.gcd(W, W.diff(w)), w).degree() == 0
    gam = sp.Poly(sp.expand((v1 * v2 - P_OF_W) / 2), w)
    gamma_inv_ok = sp.Poly(sp.gcd(gam, W), w).degree() == 0
    if not (squarefree and gamma_inv_ok):
        return None, False, "(W not squarefree / gamma not invertible)"

    def red(pl):
        return sp.Poly(pl, w).rem(W)

    def mul(p_, q_):
        return red(sp.Poly(p_, w) * sp.Poly(q_, w))

    def inv(p_):
        return sp.Poly(sp.invert(sp.Poly(p_, w).as_expr(), W.as_expr(), w), w)

    g_ = red(gam)
    gi = inv(g_)
    X_ = mul(sp.Poly(v1, w), gi)
    U_ = mul(sp.Poly(w, w), gi)
    XY_ = red(U_ - sp.Poly(1, w))
    xi = inv(X_)
    Y_ = mul(XY_, xi)
    Z_ = mul(red(g_ - sp.Poly(G0, w) - sp.Poly(A, w) * XY_), mul(mul(xi, xi), sp.Poly(R(1, 1) / B, w)))

    def ev(expr):
        pol = sp.Poly(expr, x, y, z)
        acc = sp.Poly(0, w)
        for (i, j, k), c in zip(pol.monoms(), pol.coeffs()):
            t = sp.Poly(c, w)
            for _ in range(i):
                t = mul(t, X_)
            for _ in range(j):
                t = mul(t, Y_)
            for _ in range(k):
                t = mul(t, Z_)
            acc = red(acc + t)
        return acc

    ok = all(sp.expand((ev(f) - sp.Poly(v, w)).as_expr()) == 0 for f, v in zip(F, target))
    return (deg if ok else None), ok, "(W squarefree, deg %d, all 3 components verified in QQ[w]/(W))" % deg


def explicit_collision(target):
    """Return the full fibre over `target` at high precision (mpmath complex)."""
    import mpmath as mp
    mp.mp.dps = 60

    def q2m(v):
        v = sp.Rational(v)
        return mp.mpf(v.p) / mp.mpf(v.q)

    v1, v2, v3 = target
    W = tangency_poly(target)
    roots = mp.polyroots([q2m(c) for c in W.all_coeffs()], maxsteps=300, extraprec=600)
    pc = [q2m(c) for c in reversed(sp.Poly(P_OF_W, w).all_coeffs())]
    pts = []
    for r0 in roots:
        pv = sum(pc[i] * r0**i for i in range(len(pc)))
        gam = (q2m(v1) * q2m(v2) - pv) / 2
        if abs(gam) < mp.mpf('1e-40'):
            continue
        xv = q2m(v1) / gam
        xy = r0 / gam - 1
        yv = xy / xv
        zv = (gam - q2m(G0) - q2m(A) * xy) / (q2m(B) * xv**2)
        pts.append((xv, yv, zv))
    return pts, target


def independent_resultant_count(target):
    """
    INDEPENDENT exact re-measurement of the fibre size, using ONLY the
    polynomials F1,F2,F3 -- it never mentions p, q, gamma or the sweep.

    F1 has degree 1 in z (checked), so on the fibre
        z = (v1 - F1|_(z=0)) / (dF1/dz).
    Substituting into F2-v2 and F3-v3 and clearing denominators gives
    A(x,y), B(x,y).  Res_y(A,B) is a univariate polynomial whose roots
    contain every x-coordinate of the fibre; x=0 is never on the fibre
    (F1=0 there while v1!=0), so the extraneous factor x^k is stripped.
    The number of distinct remaining roots is the count reported.
    """
    F1_, F2_, F3_ = F
    pz = sp.Poly(F1_, z)
    if pz.degree() != 1:
        return None, "(F1 not linear in z -- method not applicable)"
    e = pz.coeff_monomial(z)
    c0 = pz.coeff_monomial(1)
    zs = sp.cancel((target[0] - c0) / e)
    A = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(F2_.subs(z, zs) - target[1])))), x, y)
    B = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(F3_.subs(z, zs) - target[2])))), x, y)
    Rx = sp.Poly(sp.resultant(A.as_expr(), B.as_expr(), y), x)
    k = 0
    while Rx.degree() > 0 and Rx.eval(0) == 0:
        Rx = sp.Poly(sp.cancel(Rx.as_expr() / x), x)
        k += 1
    nd = Rx.degree() - sp.Poly(sp.gcd(Rx, Rx.diff(x)), x).degree()
    return nd, "(resultant deg %d after stripping x^%d; squarefree part deg %d)" % (Rx.degree(), k, nd)


if __name__ == "__main__":
    sys.exit(main())
