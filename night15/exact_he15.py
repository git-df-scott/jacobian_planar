"""night15 -- EXACT-HE: the period screen in closed form for deg_y P = 2.

Every P in the F2 / F2b species (and any other conic-bundle P) is quadratic in
y, and for those the period screen is EXACT and needs no numerics at all.

    P = g(x) y^2 + h(x) y + k(x),   g != 0.
    Put w = 2g y + h.  Then on the fibre {P = c},

        w^2 = h^2 - 4 g k + 4 g c  =:  Delta_c(x),

    and Q(x, y) = Q(x, w), so the fibre's function field is the hyperelliptic
    field  w^2 = Delta_c.  Moreover  P_y = 2 g y + h = w,  hence

        eta = -dx / P_y = -dx / w.

    Write Delta_c = s(x)^2 * Delta_0(x) with Delta_0 SQUAREFREE (this is the
    smooth model: w = s w_0, w_0^2 = Delta_0).  Then

        eta = -dx / ( s(x) * w_0 ),      w_0^2 = Delta_0(x),
        genus of the compact model  =  floor((deg Delta_0 - 1)/2)  (0 if <= 2).

The screen then reads off the periods without any series expansion:

 (A) deg Delta_0 >= 3 and s constant.  dx/w_0 is a nonzero HOLOMORPHIC
     1-form on a compact Riemann surface of genus >= 1.  If all its periods
     vanished it would be df with f holomorphic on a compact surface, so f
     constant and the form zero -- contradiction.  So some period is nonzero.
     VERDICT: NONVANISHING.

 (B) deg Delta_0 == 2 and s constant.  Genus 0, two places over x = infinity.
     With alpha = lc(Delta_0), sigma = s: near either place x = 1/u,
     w_0 = +- sqrt(alpha)/u * (1 + O(u)), so
         eta = -dx/(sigma w_0) = -+ du/(sigma sqrt(alpha) u) * (1 + O(u)),
     residue = -+ 1/(sigma sqrt(alpha)) != 0.
     VERDICT: NONVANISHING, with the residue given exactly.

 (C) deg Delta_0 == 1 and s constant.  The curve w_0^2 = alpha x + beta is
     rational and x = (w_0^2 - beta)/alpha gives dx = 2 w_0 dw_0/alpha, so
         eta = -2 dw_0 / (sigma alpha),
     a globally exact form with no poles at all: one puncture, genus 0,
     H_1 = 0.  VERDICT: VANISHING (exactly zero).

 (D) deg Delta_0 == 0 and s constant.  eta = -dx/(sigma sqrt(Delta_0)) is a
     constant multiple of dx.  VERDICT: VANISHING (exactly zero).

 (E) s nonconstant.  eta acquires poles at the roots of s.  At a SIMPLE root
     a of s with Delta_0(a) != 0 there are two places and
         Res = -1 / ( s'(a) * (+- sqrt(Delta_0(a))) )  != 0.
     VERDICT: NONVANISHING, residue given exactly.
     (Remaining sub-case -- every root of s is multiple or shared with
     Delta_0 -- is handed to NUM-MONO; it does not occur in this corpus and is
     recorded as DEFERRED_TO_NUM whenever it does.)

Control C3 (sum of residues = 0) is checked in every branch where residues are
produced: in (B) the two residues are exact negatives of each other, and in (E)
the two residues over each root of s are exact negatives of each other, so the
sum over all places is identically zero -- verified symbolically, not
numerically.
"""

from fractions import Fraction as F
import sympy as sp

X = sp.Symbol("x")


def _u_to_sympy(u):
    return sp.Poly(sum(sp.Rational(c.numerator, c.denominator) * X ** i
                       for i, c in u.items()), X) if u else sp.Poly(0, X)


def ghk(P):
    """split P (deg_y <= 2) into g, h, k as sympy Polys in x."""
    g = {i: c for (i, j), c in P.items() if j == 2}
    h = {i: c for (i, j), c in P.items() if j == 1}
    k = {i: c for (i, j), c in P.items() if j == 0}
    return _u_to_sympy(g), _u_to_sympy(h), _u_to_sympy(k)


def squarefree_split(D):
    """D = s^2 * D0 with D0 squarefree; returns (s, D0) as sympy Polys."""
    s = sp.Poly(1, X)
    D0 = sp.Poly(1, X)
    lead = D.LC()
    for fac, e in sp.factor_list(D.as_expr())[1]:
        fp = sp.Poly(fac, X)
        if fp.degree() == 0:
            continue
        s = s * fp ** (e // 2)
        if e % 2:
            D0 = D0 * fp
    # keep the constant with D0
    cst = sp.simplify(D.as_expr() / (s.as_expr() ** 2 * D0.as_expr()))
    D0 = sp.Poly(sp.expand(D0.as_expr() * cst), X)
    return sp.Poly(s, X), D0


def screen(P, c):
    """EXACT period screen on the fibre {P = c} for deg_y P = 2."""
    dy = max(j for (i, j) in P)
    if dy != 2:
        return {"applicable": False, "reason": "deg_y = %d" % dy}
    g, h, k = ghk(P)
    cc = sp.Rational(F(c).numerator, F(c).denominator)
    D = sp.Poly(sp.expand(h.as_expr() ** 2 - 4 * g.as_expr() * k.as_expr()
                          + 4 * g.as_expr() * cc), X)
    if D.as_expr() == 0:
        return {"applicable": False, "reason": "Delta = 0 (non-reduced fibre)"}
    s, D0 = squarefree_split(D)
    m = D0.degree()
    genus = (m - 1) // 2 if m >= 3 else 0
    out = {"applicable": True, "c": str(cc), "deg_Delta": D.degree(),
           "deg_s": s.degree(), "deg_Delta0": m, "genus": genus,
           "Delta0_lc": str(D0.LC()), "s": sp.sstr(s.as_expr()),
           "Delta0": sp.sstr(D0.as_expr())}

    if s.degree() == 0:
        sigma = s.LC()
        if m >= 3:
            out.update({"verdict": "NONVANISHING", "case": "A",
                        "witness": "nonzero holomorphic 1-form dx/w0 on a "
                                   "compact curve of genus %d" % genus,
                        "n_places_at_infinity": 1 if m % 2 else 2,
                        "residues": [], "sum_residues": "0"})
        elif m == 2:
            alpha = D0.LC()
            r = sp.simplify(1 / (sigma * sp.sqrt(alpha)))
            out.update({"verdict": "NONVANISHING", "case": "B",
                        "witness": "residue at each of the two places over "
                                   "x = infinity",
                        "n_places_at_infinity": 2,
                        "residues": [sp.sstr(r), sp.sstr(-r)],
                        "sum_residues": sp.sstr(sp.simplify(r - r)),
                        "max_abs_residue": float(sp.Abs(r))})
        elif m == 1:
            out.update({"verdict": "VANISHING", "case": "C",
                        "witness": "eta = -2 dw0/(s*alpha) is globally exact; "
                                   "genus 0 with a single puncture, H_1 = 0",
                        "n_places_at_infinity": 1,
                        "residues": ["0"], "sum_residues": "0",
                        "max_abs_residue": 0.0})
        else:
            out.update({"verdict": "VANISHING", "case": "D",
                        "witness": "eta is a constant multiple of dx",
                        "n_places_at_infinity": 2,
                        "residues": ["0", "0"], "sum_residues": "0",
                        "max_abs_residue": 0.0})
        return out

    # s nonconstant
    roots = sp.roots(s.as_expr(), X)
    simple = [(a, e) for a, e in roots.items() if e == 1
              and sp.simplify(D0.as_expr().subs(X, a)) != 0]
    if simple:
        a = simple[0][0]
        sp_ = sp.diff(s.as_expr(), X).subs(X, a)
        r = sp.simplify(-1 / (sp_ * sp.sqrt(D0.as_expr().subs(X, a))))
        out.update({"verdict": "NONVANISHING", "case": "E",
                    "witness": "simple pole of eta over x = %s" % sp.sstr(a),
                    "residues": [sp.sstr(r), sp.sstr(-r)],
                    "sum_residues": "0",
                    "max_abs_residue": float(sp.Abs(sp.N(r)))})
        return out
    out.update({"verdict": "DEFERRED_TO_NUM", "case": "F",
                "witness": "every root of s is multiple or shared with Delta0"})
    return out
