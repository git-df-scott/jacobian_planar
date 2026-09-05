"""night17 -- RESIDUE ENGINE: residues of the Gelfand-Leray form at the places
at infinity of a fibre, in closed form, exactly, with SYMBOLIC coefficients.

The form is  eta = dy/P_x = -dx/P_y  (night15/PERIODS.md section 1).  For the
two shapes used in this lane it is a RADICAL DIFFERENTIAL in x alone:

  (HE)  deg_y P = 2,  P = g y^2 + h y + k,  P_y = 2gy + h =: w,
        w^2 = Delta_c := h^2 - 4 g k + 4 g c,      eta = -dx / Delta_c^(1/2).

  (SE)  P = A(x) + B(x) y^m,  m >= 2.   On {P = lam}: y^m = (lam - A)/B and
        P_y = m B y^(m-1), so
            eta = -dx / (m B y^(m-1)) = -y dx / (m B y^m) = -y dx/(m(lam - A))
        and with y = ((lam-A)/B)^(1/m)
            eta = -(1/m) (lam - A)^((1-m)/m) B^(-1/m) dx.
        (The swap (x,y) -> (y,x) negates the bracket and carries this shape to
        P = A(y) + B(y) x^n, which is the night14/night15 v-power family
        P = h0 y + c x^n y^m; that instance is used as a cross-check below.)

RESIDUE RULE (the only thing the engine needs).  Let

        eta / dx = C * prod_i f_i(x)^(alpha_i),      alpha_i in Q, C != 0.

*At a finite point b.*  Write f_i = (x-b)^(n_i) h_i with h_i(b) != 0 and put
w = sum_i alpha_i n_i.  Let r be the ramification index of x at the place.
With x - b = tau^r and dx = r tau^(r-1) dtau, the term of order k of the
analytic part contributes tau^(r(w+k)+r-1); this is tau^(-1) iff k = -w-1.
Hence

    residue = 0 unless w is an INTEGER <= -1, and then
    residue = r * (prod_i h_i(b)^(alpha_i)) * [t^(-w-1)] prod_i (h_i(b+t)/h_i(b))^(alpha_i).

The prefactor r * prod h_i(b)^alpha_i is NONZERO, so the residue vanishes iff
the bracketed Taylor coefficient -- a POLYNOMIAL in the coefficients of P and
in lam after clearing denominators -- vanishes.  This is where the residue
equations come from.

*At infinity.*  Put u = 1/x, W = sum_i alpha_i deg(f_i), F_i(u) = u^deg(f_i)
f_i(1/u) (so F_i(0) = lc(f_i) != 0).  Then eta/dx = u^(-W) prod F_i^alpha_i and
eta = -u^(-W-2) prod_i F_i(u)^(alpha_i) du.  The same count gives

    residue = 0 unless W is an INTEGER >= -1, and then
    residue = -r_inf * (prod lc(f_i)^alpha_i) * [u^(W+1)] prod (F_i/lc_i)^(alpha_i).

Neither rule depends on the ramification index r beyond the nonzero factor, so
residue VANISHING is a purely algebraic condition on the coefficients.

Control C3 (residues sum to zero) is structural here: the several places over
one branch point differ only by the choice of the branch of the radical, i.e.
by a root of unity on the prefactor, and those roots of unity sum to zero
whenever more than one place lies over the point; a place carrying an honest
nonzero residue therefore never occurs alone over its point.  The sum is also
checked numerically against night15's NUM-MONO in controls17.py.
"""
import sympy as sp

X, U, T, LAM, C = sp.symbols("x u t lam c")


def _poly(e):
    return sp.Poly(sp.expand(e), X)


def _coeffs(expr, var, k):
    """truncated coefficient list [c_0 .. c_k] of a polynomial expr in var."""
    p = sp.Poly(sp.expand(expr), var)
    out = [sp.Integer(0)] * (k + 1)
    for m, c in zip(p.monoms(), p.coeffs()):
        if m[0] <= k:
            out[m[0]] = sp.expand(c)
    return out


def _mul(a, b, k):
    out = [sp.Integer(0)] * (k + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j > k:
                break
            if bj != 0:
                out[i + j] = out[i + j] + ai * bj
    return [sp.expand(v) for v in out]


def series_coeff(factors, k, var=T):
    """[var^k] prod (1 + g_i)^alpha_i  for factors = [(g_i, alpha_i)], each g_i
    a polynomial in var with zero constant term."""
    if k < 0:
        return sp.Integer(0)
    acc = [sp.Integer(1)] + [sp.Integer(0)] * k
    for g, a in factors:
        gc = _coeffs(g, var, k)
        assert gc[0] == 0, "g must have zero constant term"
        s = [sp.Integer(0)] * (k + 1)
        gp = [sp.Integer(1)] + [sp.Integer(0)] * k          # g^0
        for j in range(k + 1):
            cb = sp.binomial(sp.Rational(a), j)
            if cb != 0:
                s = [sp.expand(si + cb * gi) for si, gi in zip(s, gp)]
            gp = _mul(gp, gc, k)
        acc = _mul(acc, s, k)
    return sp.expand(acc[k])


def residue_at_finite(fs, b, orders):
    """fs = [(f_i(expr in X), alpha_i)]; orders[i] = ord_b(f_i).
    Returns (vanishes_identically, expr) -- expr is the coefficient whose
    vanishing is equivalent to the residue vanishing (None if identically 0)."""
    w = sum(sp.Rational(a) * o for (_, a), o in zip(fs, orders))
    if w != int(w) or w > -1:
        return True, None
    k = int(-w - 1)
    gg = []
    for (f, a), o in zip(fs, orders):
        h = sp.simplify(sp.cancel(sp.expand(f) / (X - b) ** o))
        h0 = sp.expand(h.subs(X, b))
        g = sp.expand(sp.expand(h.subs(X, b + T)) / h0 - 1)
        gg.append((g, a))
    return False, sp.simplify(series_coeff(gg, k))


def residue_at_infinity(fs):
    """fs = [(f_i, alpha_i)].  Same contract as residue_at_finite."""
    W = sum(sp.Rational(a) * _poly(f).degree() for f, a in fs)
    if W != int(W) or W < -1:
        return True, None
    k = int(W + 1)
    gg = []
    for f, a in fs:
        p = _poly(f)
        d = p.degree()
        Fu = sp.expand(sum(co * U ** (d - m[0]) for m, co in
                           zip(p.monoms(), p.coeffs())))
        lc = p.LC()
        gg.append((sp.expand(Fu / lc - 1).subs(U, T), a))
    return False, sp.simplify(series_coeff(gg, k))


# --------------------------------------------------------------- SE17 driver
def se17(A, Broots, m, lam=LAM, Bc=C):
    """P = A(x) + B(x) y^m with B = Bc * prod (x - a_i)^(e_i).

    Broots: list of (a_i, e_i) with a_i sympy expressions (may be symbols).
    Returns a dict with the places, their residue conditions, genus, punctures.
    """
    B = Bc * sp.prod([(X - a) ** e for a, e in Broots])
    f1 = sp.expand(lam - A)
    fs = [(f1, sp.Rational(1 - m, m)), (sp.expand(B), sp.Rational(-1, m))]
    p, q = _poly(f1).degree(), _poly(B).degree()
    out = {"m": m, "deg_A": _poly(A).degree(), "deg_B": q, "places": [],
           "equations": []}

    # places over the roots of B  (these are punctures: y -> infinity)
    for a, e in Broots:
        d = sp.igcd(m, e)
        # ord_a(lam - A) = 0 for generic lam, ord_a(B) = e
        van, expr = residue_at_finite(fs, a, [0, e])
        pl = {"over": "x = %s (root of B, mult %d)" % (sp.sstr(a), e),
              "n_places": int(d), "y": "infinity",
              "residue": "identically 0 (exponent rule)" if van else "conditional"}
        if not van:
            pl["residue_expr"] = sp.sstr(expr)
            out["equations"].append(sp.together(expr))
        out["places"].append(pl)

    # places over x = infinity
    van, expr = residue_at_infinity(fs)
    r = p - q
    dinf = int(sp.igcd(m, r)) if r != 0 else m
    pl = {"over": "x = infinity", "n_places": dinf,
          "residue": "identically 0 (exponent rule)" if van else "conditional"}
    if not van:
        pl["residue_expr"] = sp.sstr(expr)
        out["equations"].append(sp.together(expr))
    out["places"].append(pl)

    # genus of y^m = (lam - A)/B by Riemann-Hurwitz over P^1, generic lam
    # (lam - A squarefree for generic lam when A is nonconstant)
    orders = []
    if p >= 1:
        orders += [1] * p                      # simple zeros of lam - A
    orders += [-e for _, e in Broots]          # poles of order e
    orders.append(-(p - q))                    # order at x = infinity
    ram = sum(m - sp.igcd(m, abs(o)) if o != 0 else 0 for o in orders)
    out["genus"] = sp.Rational(2 - 2 * m + ram, 2) / 1
    out["genus"] = sp.nsimplify((ram - 2 * m + 2) / 2)
    out["n_punctures"] = int(sum(sp.igcd(m, e) for _, e in Broots)) + dinf
    return out


# --------------------------------------------- finite places of a radical
def he_finite_residues(D, cc=C):
    """eta = -dx / Delta_c^(1/2).  Residues at the FINITE places.

    At a root b of Delta_c of multiplicity mu the exponent is w = -mu/2, so by
    the residue rule the residue can be nonzero only when mu is EVEN and >= 2,
    and then it is a nonzero constant times

        [t^(mu/2 - 1)] ( Delta_c(b+t) / (T_mu t^mu) )^(-1/2),
        T_mu = Delta_c^(mu)(b)/mu!  (nonzero at b).

    b runs over the roots of each irreducible factor f of Delta_c; the residue
    vanishes at ALL of them iff f divides the numerator of that coefficient,
    which is decided by polynomial remainder over Q(c).  Simple roots (mu = 1)
    give w = -1/2, not an integer: residue identically 0 -- which is why a
    fibre whose Delta_c is squarefree has no finite residues at all.
    """
    b = sp.Symbol("b_root")
    P = sp.Poly(sp.expand(D), X)
    out = []
    for f, mu in P.factor_list()[1]:
        if f.degree() == 0:
            continue
        info = {"factor": sp.sstr(f.as_expr()), "mult": mu,
                "deg_factor": f.degree()}
        if mu % 2 or mu < 2:
            info["residue"] = "identically 0 (exponent rule: mu = %d)" % mu
            out.append(info)
            continue
        k = mu // 2 - 1
        fb = sp.Poly(f.as_expr().subs(X, b), b)
        Dp = sp.Poly(sp.expand(D).subs(X, b + T), T)
        Tc = {}
        for j in range(mu, mu + k + 1):
            cj = Dp.coeff_monomial(T ** j) if j <= Dp.degree() else 0
            Tc[j] = sp.rem(sp.Poly(sp.expand(cj), b), fb).as_expr()
        if k == 0:
            info["residue"] = "NONZERO (leading coefficient, no condition)"
            info["vanishes"] = False
        else:
            g = sum(sp.Rational(1) * (Tc[mu + i] / Tc[mu]) * T ** i
                    for i in range(1, k + 1))
            co = series_coeff([(sp.expand(g), sp.Rational(-1, 2))], k)
            num = sp.Poly(sp.numer(sp.cancel(sp.together(co))), b)
            r = sp.rem(num, fb).as_expr()
            info["residue_expr"] = sp.sstr(sp.simplify(r))
            info["vanishes"] = bool(sp.simplify(r) == 0)
            info["residue"] = ("identically 0 on this factor" if info["vanishes"]
                               else "conditional")
        out.append(info)
    return out


# --------------------------------------------------------------- HE17 driver
def he17(g, h, k, cc=C):
    """P = g(x) y^2 + h(x) y + k(x).  Delta_c = h^2 - 4 g k + 4 g c."""
    D = sp.expand(h ** 2 - 4 * g * k + 4 * g * cc)
    fs = [(D, sp.Rational(-1, 2))]
    dd = _poly(D).degree()
    van, expr = residue_at_infinity(fs)
    sf = sp.Poly(sp.expand(D), X).factor_list()[1]
    d0 = sum(f.degree() for f, mu in sf if mu % 2)
    fin = he_finite_residues(D, cc)
    out = {"Delta_c": sp.sstr(sp.expand(D)), "deg_Delta_c": dd,
           "deg_Delta_0": d0, "genus": max(0, (d0 - 1) // 2),
           "n_places_inf": 1 if d0 % 2 else 2,
           "residue_at_infinity": "identically 0" if van else sp.sstr(expr),
           "finite_places": fin,
           "finite_residues_all_zero": all(
               p["residue"].startswith("identically 0") or p.get("vanishes")
               for p in fin)}
    out["residues_all_zero"] = bool(out["finite_residues_all_zero"] and van)
    return out
