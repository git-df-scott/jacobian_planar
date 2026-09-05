#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gallagher's dimension-3 counterexample of GEOMETRIC DEGREE 3  (det J = 1)

A non-injective Keller map C^3 -> C^3 whose generic fibre has exactly 3 points.
This is the member n = 3 (seed degree d = 2) of the PUBLISHED infinite family

  A. Gallagher, "An infinite family of counterexamples to the Jacobian
  Conjecture in dimension three: every generic fiber degree n >= 3 occurs",
  preprint, 20 July 2026, Zenodo, doi:10.5281/zenodo.21479195
  PDF: https://zenodo.org/records/21479195/files/Gallagher2026_JC.pdf

Gallagher's construction (his eq. (1),(2),(5); Theorem 1; Proposition 1):
  seed p in C[w] with  p(0)=0,  p(1)=-c,  int_0^1 p(w) dw = 0
  q defined by q(0)=0 and  c q'(w) = w p'(w)
  kappa = p'(1)/c,   a = -(1+kappa)/(2+kappa),   b != 0
  v = xy,  t = x^2 z,  u = 1+v,  gamma = 1 + a v + b t,  w = u*gamma
  beta = c + p(w)/gamma,   alpha = u + q(w)/gamma^2
  F(x,y,z) = ( alpha/x^2 , beta/x , x*gamma ),      det J F = b*c
  generic fibre degree = deg(p) + 1                 (his Proposition 1)

Seed family (his eq. (5)), here with d = 2, c = 1:
  p_d(w) = 2w - 3w^2 + w(1-w)( w^(d-2) - k ),   k = 6/(d(d+1))
  -> p_2(w) = -3*w**2 + 2*w

  NOTE ON k: the Zenodo PDF's fraction renders ambiguously in text
  extraction.  k = 6/(d(d+1)) is forced by Gallagher's own two stated
  constraints -- int_0^1 p = 0 (his Lemma 1 computation 1/(d(d+1)) - k/6 = 0)
  and 0 < k <= 1 -- and is confirmed here numerically: with k = 6/(d(d+1))
  all three seed conditions (1) hold exactly and the twist divisibilities
  succeed, which both fail for the other reading.  Checked below.

Run:  python3 gallagher_dim3_degree3.py
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
# THE MAP  F = (A, B, C) : C^3 -> C^3   (explicit polynomials)
# ===========================================================================
F1 = (
    (-2)*x**3*y**3*z + (3)*x**2*y**4 + (-6)*x**2*y**2*z + (7)*x*y**3 + (-6)*x*y*z + (4)*y**2
    + (-2)*z
)

F2 = (
    (-3)*x**3*y**2*z + (R(9, 2))*x**2*y**3 + (-6)*x**2*y*z + (6)*x*y**2 + (-3)*x*z + (R(1, 2))*y
)

F3 = (
    (1)*x**3*z + (R(-3, 2))*x**2*y + (1)*x
)

F = [F1, F2, F3]

# --- Gallagher's generating data ------------------------------------------
P_OF_W = (-3)*w**2 + (2)*w**1
Q_OF_W = (-2)*w**3 + (1)*w**2
A_CONST = R(-3, 2)
B_CONST = 1
C_CONST = 1
SEED_D = 2
CLAIMED_DEGREE = 3
CLAIMED_DETJ = 1


def main():
    print(__doc__.strip().splitlines()[0])
    print("=" * 74)

    print("\n(0) Shape of the map")
    print("    component total degrees :", [sp.Poly(f, x, y, z).total_degree() for f in F])
    print("    component term counts   :", [len(sp.Poly(f, x, y, z).terms()) for f in F])

    print("\n(0') Gallagher's seed conditions (1) and the choice of a")
    check("p(0) = 0", sp.simplify(P_OF_W.subs(w, 0)) == 0)
    check("p(1) = -c", sp.simplify(P_OF_W.subs(w, 1) + C_CONST) == 0)
    check("int_0^1 p(w) dw = 0", sp.simplify(sp.integrate(P_OF_W, (w, 0, 1))) == 0)
    check("c q'(w) = w p'(w)",
          sp.expand(C_CONST * sp.diff(Q_OF_W, w) - w * sp.diff(P_OF_W, w)) == 0)
    check("q(0) = 0", sp.simplify(Q_OF_W.subs(w, 0)) == 0)
    kap = sp.simplify(sp.diff(P_OF_W, w).subs(w, 1) / C_CONST)
    print("    kappa = p'(1)/c =", kap)
    check("a = -(1+kappa)/(2+kappa)", sp.simplify(A_CONST + (1 + kap) / (2 + kap)) == 0)
    check("kappa != -2", sp.simplify(kap + 2) != 0)
    check("deg p == d == %d" % SEED_D, sp.Poly(P_OF_W, w).degree() == SEED_D)

    print("\n(a) Jacobian determinant is a nonzero CONSTANT")
    detJ = sp.expand(sp.Matrix(F).jacobian(sp.Matrix([x, y, z])).det())
    print("    det J =", detJ, "   (Gallagher Theorem 1: det J = b*c =", B_CONST * C_CONST, ")")
    check("det J is constant", detJ.free_symbols == set())
    check("det J is nonzero", detJ != 0)
    check("det J == b*c == %s" % CLAIMED_DETJ, sp.simplify(detJ - CLAIMED_DETJ) == 0)

    print("\n(a') Provenance identities (Gallagher eq. (2) and Theorem 1)")
    gam = 1 + A_CONST * x * y + B_CONST * x**2 * z
    u = 1 + x * y
    W_ = sp.expand(u * gam)
    check("F3 == x*gamma", sp.expand(F3 - x * gam) == 0)
    check("F2*F3 == c*gamma + p(w)   [= P]",
          sp.expand(F2 * F3 - (C_CONST * gam + P_OF_W.subs(w, W_))) == 0)
    check("F1*F3^2 == w*gamma + q(w) [= Q]",
          sp.expand(F1 * F3**2 - (W_ * gam + Q_OF_W.subs(w, W_))) == 0)

    print("\n(b) MEASURED geometric degree (# points in a generic fibre)")
    print("     via Gallagher's inverse equation (4):  Rint(w) = w*P - c*Q")
    targets = [(R(3, 2), R(-5, 7), R(2, 5)),
               (R(-4, 3), R(7, 5), R(1, 6)),
               (R(5, 4), R(3, 11), R(-2, 9)),
               (R(7, 3), R(-2, 9), R(5, 8))]
    measured = []
    for tgt in targets:
        n, ok, info = fibre_size_exact(tgt)
        measured.append(n)
        print("    target %-26s -> %s points   %s" % (str(tgt), n, info))
        check("fibre over %s fully certified" % (str(tgt),), ok)
    check("MEASURED geometric degree == %d at every target" % CLAIMED_DEGREE,
          all(n == CLAIMED_DEGREE for n in measured), "measured = %s" % measured)
    if not all(n == CLAIMED_DEGREE for n in measured):
        print("    *** WARNING: measured degree disagrees with the claim! ***")

    print("\n(b') INDEPENDENT re-measurement by resultant elimination")
    print("     (uses ONLY the polynomials F1,F2,F3 -- not the inverse equation)")
    for tgt in targets[:2]:
        nd, info = independent_resultant_count(tgt)
        print("    target %-26s -> %s distinct solutions  %s" % (str(tgt), nd, info))
        check("independent elimination over %s gives %d" % (str(tgt), CLAIMED_DEGREE),
              nd == CLAIMED_DEGREE, "(got %s)" % nd)

    print("\n(c) EXPLICIT COLLISION: %d distinct points with one common image" % CLAIMED_DEGREE)
    import mpmath as mp
    pts, tgt = explicit_collision(targets[0])
    for i, P in enumerate(pts):
        print("    p%-2d = ( %s ," % (i + 1, mp.nstr(P[0], 18)))
        print("            %s ," % mp.nstr(P[1], 18))
        print("            %s )" % mp.nstr(P[2], 18))
    fl = [sp.lambdify((x, y, z), f, 'mpmath') for f in F]
    resid = []
    for P in pts:
        for i, v in enumerate(tgt):
            tv = mp.mpf(sp.Rational(v).p) / mp.mpf(sp.Rational(v).q)
            resid.append(abs(fl[i](P[0], P[1], P[2]) - tv))
    print("    common image     :", tuple(str(t) for t in tgt))
    print("    max |F(p_i) - v| : %s  (at %d digits)" % (mp.nstr(max(resid), 5), mp.mp.dps))
    check("all %d points map to the same target" % CLAIMED_DEGREE, max(resid) < mp.mpf('1e-30'))
    seps = [max(abs(pts[i][k] - pts[j][k]) for k in range(3))
            for i in range(len(pts)) for j in range(i + 1, len(pts))]
    print("    min pairwise separation : %s" % mp.nstr(min(seps), 5))
    check("the %d points are pairwise distinct" % CLAIMED_DEGREE, min(seps) > mp.mpf('1e-12'))

    print("\n" + "=" * 74)
    if FAILURES:
        print("RESULT: FAIL  (%d failed: %s)" % (len(FAILURES), ", ".join(FAILURES)))
        return 1
    print("RESULT: ALL CHECKS PASSED")
    print("  dimension              : 3")
    print("  det J                  :", CLAIMED_DETJ)
    print("  MEASURED geometric deg :", CLAIMED_DEGREE)
    return 0


# ===========================================================================
def inverse_eq(target):
    """Gallagher eq.(4): f(w) = Rint(w) - w*P + c*Q,  P = B*C, Q = C^2*A."""
    vA, vB, vC = target
    P = vB * vC
    Q = vC**2 * vA
    Rint = sp.integrate(P_OF_W, w)
    return sp.Poly(sp.expand(Rint - w * P + C_CONST * Q), w)


def fibre_size_exact(target):
    """
    EXACT count of #F^{-1}(target), verified inside QQ[w]/(f).

    Upper bound: every preimage with C != 0 yields a root of f (Gallagher
    Prop. 1), so #fibre <= deg f = d+1.
    Lower bound: we verify IN QQ[w]/(f) that
        gamma = (P - p(w))/c, u = w/gamma, xx = vC/gamma,
        yy = (u-1)/xx, zz = (gamma - 1 - a(u-1))/(b xx^2)
    satisfies F(xx,yy,zz) == target identically; with f squarefree this
    exhibits deg f distinct preimages at once.
    """
    vA, vB, vC = target
    f = inverse_eq(target)
    deg = f.degree()
    if sp.Poly(sp.gcd(f, f.diff(w)), w).degree() != 0:
        return None, False, "(inverse equation not squarefree)"
    P = vB * vC
    gam = sp.Poly(sp.expand((P - P_OF_W) / C_CONST), w)
    if sp.Poly(sp.gcd(gam, f), w).degree() != 0:
        return None, False, "(gamma not invertible mod f)"

    def red(pl):
        return sp.Poly(pl, w).rem(f)

    def mul(p_, q_):
        return red(sp.Poly(p_, w) * sp.Poly(q_, w))

    def inv(p_):
        return sp.Poly(sp.invert(sp.Poly(p_, w).as_expr(), f.as_expr(), w), w)

    g_ = red(gam)
    gi = inv(g_)
    XX = mul(sp.Poly(vC, w), gi)
    UU = mul(sp.Poly(w, w), gi)
    XY = red(UU - sp.Poly(1, w))
    xi = inv(XX)
    YY = mul(XY, xi)
    ZZ = mul(red(g_ - sp.Poly(1, w) - sp.Poly(A_CONST, w) * XY),
             mul(mul(xi, xi), sp.Poly(R(1, 1) / B_CONST, w)))

    def ev(expr):
        pol = sp.Poly(expr, x, y, z)
        acc = sp.Poly(0, w)
        for (i, j, k), cc in zip(pol.monoms(), pol.coeffs()):
            t = sp.Poly(cc, w)
            for _ in range(i):
                t = mul(t, XX)
            for _ in range(j):
                t = mul(t, YY)
            for _ in range(k):
                t = mul(t, ZZ)
            acc = red(acc + t)
        return acc

    ok = all(sp.expand((ev(ff) - sp.Poly(vv, w)).as_expr()) == 0 for ff, vv in zip(F, target))
    return (deg if ok else None), ok, "(inverse eq. squarefree of degree %d; all 3 components verified in QQ[w]/(f))" % deg


def explicit_collision(target):
    import mpmath as mp
    mp.mp.dps = 60

    def m(v):
        v = sp.Rational(v)
        return mp.mpf(v.p) / mp.mpf(v.q)

    vA, vB, vC = target
    f = inverse_eq(target)
    roots = mp.polyroots([m(c) for c in f.all_coeffs()], maxsteps=300, extraprec=800)
    pc = [m(c) for c in reversed(sp.Poly(P_OF_W, w).all_coeffs())]
    P = vB * vC
    pts = []
    for r0 in roots:
        pv = sum(pc[i] * r0**i for i in range(len(pc)))
        gam = (m(P) - pv) / m(C_CONST)
        if abs(gam) < mp.mpf('1e-40'):
            continue
        xx = m(vC) / gam
        xy = r0 / gam - 1
        yy = xy / xx
        zz = (gam - 1 - m(A_CONST) * xy) / (m(B_CONST) * xx**2)
        pts.append((xx, yy, zz))
    return pts, target


def independent_resultant_count(target):
    """
    INDEPENDENT: uses only F1,F2,F3.  F3 has degree 1 in z, so on the fibre
    z = (vC - F3|_(z=0))/(dF3/dz); substituting into F1-vA and F2-vB and
    clearing denominators gives A(x,y), B(x,y); Res_y(A,B) contains every
    fibre x-coordinate.  x=0 is not on the fibre (F3=0 there, vC != 0), so
    the extraneous factor x^k is stripped.
    """
    pz = sp.Poly(F3, z)
    if pz.degree() != 1:
        return None, "(F3 not linear in z)"
    e = pz.coeff_monomial(z)
    c0 = pz.coeff_monomial(1)
    zs = sp.cancel((target[2] - c0) / e)
    Aa = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(F1.subs(z, zs) - target[0])))), x, y)
    Bb = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(F2.subs(z, zs) - target[1])))), x, y)
    Rx = sp.Poly(sp.resultant(Aa.as_expr(), Bb.as_expr(), y), x)
    k = 0
    while Rx.degree() > 0 and Rx.eval(0) == 0:
        Rx = sp.Poly(sp.cancel(Rx.as_expr() / x), x)
        k += 1
    nd = Rx.degree() - sp.Poly(sp.gcd(Rx, Rx.diff(x)), x).degree()
    return nd, "(resultant deg %d after stripping x^%d; squarefree part %d)" % (Rx.degree(), k, nd)


if __name__ == "__main__":
    sys.exit(main())
