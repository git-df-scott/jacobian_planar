"""night17 -- the RESIDUE-EQUATION SYSTEMS, support by support, with symbolic
coefficients, and their solution structure by Groebner over Q.

Two parametrised shapes are used (see res17.py for the residue rule).

HE(G,H,K):   P = g(x) y^2 + h(x) y + k(x),  deg g = G, deg h = H, deg k = K,
             coefficients g_0..g_G, h_0..h_H, k_0..k_K.
             Delta_c = h^2 - 4 g k + 4 g c.  On the OPEN stratum where Delta_c
             is squarefree (the generic one: a square factor is a codimension
             condition) the smooth model is w^2 = Delta_c, so
                 genus = floor((deg Delta_c - 1)/2),
                 residue at the two places over x = infinity nonzero
                     <=>  deg Delta_c = 2,
                 no finite residues (simple roots give the exponent -1/2).
             Hence on that stratum
                 ALL PERIODS VANISH  <=>  deg_x Delta_c <= 1 for every c
                 <=>  [x^j] g = 0  (j >= 2)  and  [x^j](h^2 - 4 g k) = 0 (j >= 2).
             That is the residue system RES(HE; G,H,K): (G-1) linear equations
             in the g_i and (2H - 1 or K - 1)-many equations, quadratic in the
             h_i and bilinear in (g_i, k_j).

SE(m; e_1..e_s):  P = A(x) + B(x) y^m, A = alpha x + beta,
             B = c prod (x - a_i)^(e_i),  unknowns alpha, beta, c, a_1..a_s.
             eta = -(1/m) (lam - A)^((1-m)/m) B^(-1/m) dx and the residue rule
             gives one equation per root a_i with m | e_i and e_i >= m, plus one
             at x = infinity when m | (p(m-1) + q) and p(m-1) + q <= m
             (p = deg A, q = deg B).  Every other place is residue-free
             identically, by the exponent rule alone.

Emptiness is certified by Rabinowitsch: adjoin z * (the coefficient that must
not vanish) - 1 and compute a Groebner basis; a basis [1] proves the support
has NO solution with that coefficient nonzero.
"""
import sympy as sp

import res17 as R

X, C, LAM = R.X, R.C, R.LAM


def he_system(G, H, K):
    g = sp.symbols("g0:%d" % (G + 1))
    h = sp.symbols("h0:%d" % (H + 1))
    k = sp.symbols("k0:%d" % (K + 1))
    gp = sum(g[i] * X ** i for i in range(G + 1))
    hp = sum(h[i] * X ** i for i in range(H + 1))
    kp = sum(k[i] * X ** i for i in range(K + 1))
    D = sp.Poly(sp.expand(hp ** 2 - 4 * gp * kp), X)
    eqs = [sp.expand(g[i]) for i in range(2, G + 1)]
    eqs += [sp.expand(D.coeff_monomial(X ** j)) for j in range(2, D.degree() + 1)]
    eqs = [e for e in eqs if e != 0]
    return {"vars": list(g) + list(h) + list(k), "g": gp, "h": hp, "k": kp,
            "eqs": eqs, "Delta": sp.expand(hp ** 2 - 4 * gp * kp),
            "label": "HE(G=%d,H=%d,K=%d)" % (G, H, K)}


def se_system(m, mults):
    s = len(mults)
    al, be, cc = sp.symbols("alpha beta c")
    a = sp.symbols("a1:%d" % (s + 1)) if s else ()
    A = al * X + be
    o = R.se17(A, list(zip(a, mults)), m, Bc=cc)
    eqs = []
    for e in o["equations"]:
        e = sp.together(sp.simplify(e))
        n, d = sp.fraction(e)
        eqs.append(sp.expand(n))
    eqs = [e for e in eqs if e != 0]
    return {"vars": [al, be, cc] + list(a), "eqs": eqs, "places": o["places"],
            "genus": o["genus"], "n_punctures": o["n_punctures"],
            "label": "SE(m=%d;%s)" % (m, ",".join(str(e) for e in mults))}


def groebner_empty(eqs, vars_, nonzero, extra=()):
    """Rabinowitsch: is the system unsolvable with every element of `nonzero`
    nonzero?  Returns (is_empty, basis_string)."""
    zs = sp.symbols("z1:%d" % (len(nonzero) + 1))
    sys_ = list(eqs) + list(extra) + [z * n - 1 for z, n in zip(zs, nonzero)]
    gv = list(vars_) + list(zs)
    try:
        G = sp.groebner(sys_, *gv, order="grevlex")
    except Exception as e:                                   # noqa: BLE001
        return None, "groebner failed: %s" % e
    b = list(G.exprs)
    return (b == [sp.Integer(1)]), ", ".join(sp.sstr(x) for x in b[:6])


def dimension_hint(eqs, vars_):
    """crude solution-structure report: number of equations, variables, and the
    dimension of the zero set of the LINEARISATION at a random rational point
    is not attempted; instead we report the Groebner basis size and whether the
    ideal is the zero ideal (no condition at all)."""
    if not eqs:
        return {"n_eqs": 0, "structure": "no equations: the whole support solves"}
    try:
        G = sp.groebner(list(eqs), *vars_, order="grevlex")
        b = list(G.exprs)
    except Exception as e:                                   # noqa: BLE001
        return {"n_eqs": len(eqs), "structure": "groebner failed: %s" % e}
    return {"n_eqs": len(eqs), "gb_size": len(b),
            "gb_head": [sp.sstr(x) for x in b[:4]],
            "structure": "unit ideal (no solutions at all)" if b == [sp.Integer(1)]
            else "proper ideal"}
