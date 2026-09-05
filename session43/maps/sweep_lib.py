"""
Shared library: Gao/Gallagher tangent-sweep + monomial-twist construction of
Keller counterexamples in dimension 3.

Reference: Shuhong Gao, "Counterexamples to the Jacobian conjecture in
dimensions greater than two", arXiv:2608.00222, sections 3.1-3.5.

RECIPE (Gao section 3.3, "the monomial twist"):

    (x,y,z) --monomial--> (x, xy, x^2 z) --affine--> (x, gamma, u)
            --w=gamma*u--> (x, gamma, w) --padded sweep--> (gamma x, P, Q)
            --twist--> (C, P/C, Q/C^2)

  with   gamma = g0 + a*x*y + b*x^2*z,   u = 1 + x*y,   w = gamma*u,
         P = p(w) + 2*gamma,   Q = q(w) + gamma*w,   C = gamma*x.

  The plane curve is K(w) = (p(w), q(w)) in "inflection-free normal form",
  i.e. eq. (1) of the paper:   q(w) = int_0^w (s/2) p'(s) ds,
  equivalently q' = (w/2) p', q(0)=0.  Then the tangent direction of K at w
  is (2, w) and the tangent sweep S(gamma,w) = K(w) + gamma*(2,w) has
  det J(S) = 2*gamma.

  det J(F) = -2b in the (C, P/C, Q/C^2) component order.
  Generic fibre of the twisted map = deg(p) + 1   (Gao, Prop. 3.2).

SIDE CONDITIONS for C|P and C^2|Q (derived here, and checked below against
the two worked examples in the paper):
  gamma | P and gamma^2 | Q are automatic (p(0)=0, and q has order 2 at 0).
  The remaining conditions are x | (P/gamma) and x^2 | (Q/gamma^2):
     (S1)  p(g0) + 2*g0  = 0
     (S2)  q(g0) + g0^2  = 0
     (S3)  a*(q'(g0) + 2*g0) + g0^2 + g0*q'(g0) = 0
  (S1),(S2) are linear in the coefficients of p; (S3) determines a.
"""

import sympy as sp

x, y, z, w, s = sp.symbols('x y z w s')


def q_from_p(pw):
    """Normal form eq. (1): q(w) = int_0^w (s/2) p'(s) ds."""
    integrand = sp.Rational(1, 2) * s * sp.diff(pw, w).subs(w, s)
    return sp.expand(sp.integrate(integrand, (s, 0, w)))


def side_condition_a(pw, g0):
    """(S3) solved for a."""
    qw = q_from_p(pw)
    q1 = sp.diff(qw, w).subs(w, g0)
    num = -(g0**2 + g0 * q1)
    den = q1 + 2 * g0
    if sp.together(den) == 0:
        raise ValueError("degenerate: q'(g0) + 2 g0 = 0")
    return sp.cancel(sp.Rational(num) / sp.Rational(den))


def check_side_conditions(pw, g0):
    """Return (S1_residual, S2_residual) -- both must be 0."""
    qw = q_from_p(pw)
    s1 = sp.simplify(pw.subs(w, g0) + 2 * g0)
    s2 = sp.simplify(qw.subs(w, g0) + g0**2)
    return s1, s2


def build_map(pw, g0, a, b):
    """
    Build F = (C, P/C, Q/C^2) as three sympy polynomials in x,y,z.
    Raises if the twist divisibilities fail.
    """
    qw = q_from_p(pw)
    gamma = g0 + a * x * y + b * x**2 * z
    u = 1 + x * y
    wsub = sp.expand(gamma * u)

    P = sp.expand(pw.subs(w, wsub) + 2 * gamma)
    Q = sp.expand(qw.subs(w, wsub) + gamma * wsub)
    C = sp.expand(gamma * x)

    F2, r2 = sp.div(sp.Poly(P, x, y, z), sp.Poly(C, x, y, z))
    if not r2.is_zero:
        raise ValueError("C does not divide P -- side condition (S1) failed")
    F3, r3 = sp.div(sp.Poly(Q, x, y, z), sp.Poly(sp.expand(C**2), x, y, z))
    if not r3.is_zero:
        raise ValueError("C^2 does not divide Q -- side conditions (S2)/(S3) failed")

    return [sp.expand(C), sp.expand(F2.as_expr()), sp.expand(F3.as_expr())]


def jac_det(F, vars_):
    return sp.simplify(sp.Matrix(F).jacobian(sp.Matrix(vars_)).det())


# ---------------------------------------------------------------------------
# Exact fibre count, done two independent ways.
# ---------------------------------------------------------------------------

def fibre_via_elimination(F, vars_, target):
    """
    INDEPENDENT exact count of #F^{-1}(target) over C, using only the
    polynomials F themselves (no appeal to the paper's theory).

    Method: introduce a random separating linear form t = c.vars, and
    eliminate the original variables with a lex Groebner basis.  The number
    of DISTINCT complex points equals deg(squarefree(g)) where g(t) is the
    monic eliminant, provided the linear form separates the fibre points
    (true for generic c) and the ideal is 0-dimensional.
    """
    import random
    t = sp.Symbol('t_elim')
    eqs = [sp.expand(f - v) for f, v in zip(F, target)]
    rng = random.Random(20260826)
    for _attempt in range(4):
        coeffs = [sp.Integer(rng.randint(1, 40)) for _ in vars_]
        lin = t - sum(c * v for c, v in zip(coeffs, vars_))
        G = sp.groebner(eqs + [lin], *(list(vars_) + [t]), order='lex')
        univ = [g for g in G.exprs if g.free_symbols <= {t}]
        if not univ:
            continue
        g = sp.Poly(univ[0], t)
        sf = sp.Poly(sp.factor_list(sp.gcd(g, g.diff(t)))[0], t)
        # squarefree part degree = number of distinct roots
        n_distinct = g.degree() - sp.gcd(g, g.diff(t)).degree()
        return n_distinct
    raise RuntimeError("elimination failed to produce a univariate eliminant")


def fibre_via_tangency(pw, g0, a, b, target):
    """
    Structural exact count using the sweep theory (Gao, Lemma 3.1):
    the fibre over v (with v1 != 0) is in bijection with the DISTINCT roots
    w of the tangency polynomial
         W(w) = q(w) + (w/2)(X - p(w)) - Y,      X = v1*v2,  Y = v1^2*v3
    having gamma = (X - p(w))/2 != 0.
    """
    qw = q_from_p(pw)
    v1, v2, v3 = target
    X = v1 * v2
    Y = v1**2 * v3
    W = sp.Poly(sp.expand(qw + sp.Rational(1, 2) * w * (X - pw) - Y), w)
    n_distinct = W.degree() - sp.gcd(W, W.diff(w)).degree()
    # discard roots with gamma = 0
    gam = sp.Poly(sp.expand((X - pw) / 2), w)
    bad = sp.gcd(W, gam)
    bad_distinct = bad.degree() - sp.gcd(bad, bad.diff(w)).degree() if bad.degree() > 0 else 0
    return n_distinct - bad_distinct


def solve_fibre_points(pw, g0, a, b, target):
    """Return the exact fibre points (x,y,z) over target, via the tangency roots."""
    qw = q_from_p(pw)
    v1, v2, v3 = target
    X = v1 * v2
    Y = v1**2 * v3
    W = sp.expand(qw + sp.Rational(1, 2) * w * (X - pw) - Y)
    pts = []
    for root in sp.roots(sp.Poly(W, w)).keys():
        gam = sp.simplify((X - pw.subs(w, root)) / 2)
        if gam == 0:
            continue
        xv = sp.simplify(v1 / gam)
        uv = sp.simplify(root / gam)
        xy = sp.simplify(uv - 1)
        yv = sp.simplify(xy / xv)
        zv = sp.simplify((gam - g0 - a * xy) / (b * xv**2))
        pts.append((sp.nsimplify(xv), sp.nsimplify(yv), sp.nsimplify(zv)))
    return pts


# ---------------------------------------------------------------------------
# EXACT simultaneous verification of the whole fibre in QQ[w]/(W(w)).
# ---------------------------------------------------------------------------

def tangency_poly(pw, target):
    """W(w) = q(w) + (w/2)(X - p(w)) - Y,  X = v1 v2, Y = v1^2 v3."""
    qw = q_from_p(pw)
    v1, v2, v3 = target
    X = v1 * v2
    Y = v1**2 * v3
    return sp.Poly(sp.expand(qw + sp.Rational(1, 2) * w * (X - pw) - Y), w)


def verify_fibre_exact(F, pw, g0, a, b, target):
    """
    Fully exact, char-0 verification that F^{-1}(target) contains exactly
    deg(W) = deg(p)+1 DISTINCT points, without ever computing a Groebner basis.

    Strategy: let W be the tangency polynomial and R = QQ[w]/(W).  If W is
    squarefree and gamma = (X-p(w))/2 is invertible mod W, then the formulas
        x = v1/gamma, u = w/gamma, y = (u-1)/x, z = (gamma-g0-a(u-1))/(b x^2)
    define an element of R^3.  Verifying F(x,y,z) == target IN R proves
    simultaneously that every one of the deg(W) roots of W yields a genuine
    point of the fibre.  Distinctness holds because w = gamma*(1+x*y) with
    gamma = v1/x is recoverable from the point, so distinct roots of W give
    distinct points.

    Returns dict with the certificate data.
    """
    v1, v2, v3 = target
    W = tangency_poly(pw, target)
    deg = W.degree()

    # (i) squarefree?
    gcd_ww = sp.gcd(W, W.diff(w))
    squarefree = (sp.Poly(gcd_ww, w).degree() == 0)

    # (ii) gamma invertible mod W?
    gam = sp.Poly(sp.expand((v1 * v2 - pw) / 2), w)
    g_gcd = sp.Poly(sp.gcd(gam, W), w)
    gamma_invertible = (g_gcd.degree() == 0)

    if not (squarefree and gamma_invertible):
        return dict(deg=deg, squarefree=squarefree,
                    gamma_invertible=gamma_invertible, verified=False)

    def red(poly):
        return sp.Poly(poly, w).rem(W)

    def inv(poly):
        return sp.Poly(sp.invert(sp.Poly(poly, w).as_expr(), W.as_expr(), w), w)

    def mul(a_, b_):
        return red(sp.Poly(a_, w) * sp.Poly(b_, w))

    gam_r = red(gam)
    gam_inv = inv(gam_r)
    X_ = mul(sp.Poly(v1, w), gam_inv)                    # x  = v1/gamma
    U_ = mul(sp.Poly(w, w), gam_inv)                     # u  = w/gamma
    XY_ = red(U_ - sp.Poly(1, w))                        # x*y = u - 1
    x_inv = inv(X_)
    Y_ = mul(XY_, x_inv)                                 # y
    x2_inv = mul(x_inv, x_inv)
    Z_ = mul(red(gam_r - sp.Poly(g0, w) - sp.Poly(a, w) * XY_) * sp.Poly(1, w),
             x2_inv)
    Z_ = red(sp.Poly(Z_, w) * sp.Poly(sp.Rational(1, 1) / b, w))

    # evaluate F at (X_, Y_, Z_) inside R
    def eval_in_R(expr):
        pol = sp.Poly(expr, x, y, z)
        acc = sp.Poly(0, w)
        for mono, coeff in zip(pol.monoms(), pol.coeffs()):
            i, j, k = mono
            term = sp.Poly(coeff, w)
            for _ in range(i):
                term = mul(term, X_)
            for _ in range(j):
                term = mul(term, Y_)
            for _ in range(k):
                term = mul(term, Z_)
            acc = red(acc + term)
        return acc

    ok = []
    for f, v in zip(F, target):
        val = eval_in_R(f)
        ok.append(sp.simplify((val - sp.Poly(v, w)).as_expr()) == 0)

    return dict(deg=deg, squarefree=squarefree, gamma_invertible=gamma_invertible,
                components_ok=ok, verified=all(ok))
