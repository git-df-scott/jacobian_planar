"""night18 -- the HE stratum with deg g = 1, as an EXPLICIT rational family.

night17/SYNTHESIS.md section 2.1 solves the residue system RES(HE) on the
stratum deg g = 1 and reports the parametrisation

    g     = gamma (x - a)                       gamma != 0
    h     = h_0 + h_1 x + ... + h_H x^H         free
    alpha free,  beta = h(a)^2 - alpha a
    k     = (h^2 - alpha x - beta) / (4 gamma (x - a))          (exact division)
    P     = g y^2 + h y + k

of dimension deg h + 4 inside the support HE(1, H, 2H-1), with the open
conditions gamma != 0 (so deg g = 1) and h(a) != 0 (gradient-unimodularity).

This module builds P over Q(gamma, a, alpha, h_0..h_H) and carries the two
identity-level verifications.
"""
import sympy as sp
import spk18 as spk

X, Y = spk.X, spk.Y


def params(H):
    gam, a, al = sp.symbols('gamma a alpha')
    hs = sp.symbols('h0:%d' % (H + 1))
    return gam, a, al, list(hs)


def family(H):
    """returns dict with the symbolic data of the deg g = 1, deg h = H family."""
    gam, a, al, hs = params(H)
    h = sum(hs[i] * X**i for i in range(H + 1))
    ha = sum(hs[i] * a**i for i in range(H + 1))
    beta = ha**2 - al * a
    Delta = al * X + beta
    g = gam * (X - a)
    num = sp.expand(h**2 - Delta)
    k, rem = sp.div(sp.Poly(num, X), sp.Poly(4 * g, X))
    k = sp.expand(k.as_expr())
    rem = sp.expand(rem.as_expr())
    P = spk.from_expr(sp.expand(g * Y**2 + h * Y + k))
    return dict(H=H, gam=gam, a=a, al=al, hs=hs, h=h, ha=ha, beta=beta,
                Delta=Delta, g=g, k=k, k_remainder=rem, P=P,
                free=[gam, a, al] + list(hs))


def bezout(F):
    """explicit A, B with A*P_x + B*P_y = R, R the constant gamma*h(a)^2.

    L := 2 g = 2 gamma (x-a);  P_y = L y + h;  and
        L^2 P_x - (gamma h^2 - h' h L + k' L^2) = P_y * (gamma (P_y - 2h) + h' L),
    so A = L^2, B = -(gamma (P_y - 2h) + h' L), R = gamma h^2 - h' h L + k' L^2.
    """
    gam, h, k, g = F['gam'], F['h'], F['k'], F['g']
    L = sp.expand(2 * g)
    hp = sp.diff(h, X)
    kp = sp.diff(k, X)
    Py = sp.expand(L * Y + h)
    A = sp.expand(L**2)
    B = sp.expand(-(gam * (Py - 2 * h) + hp * L))
    R = sp.expand(gam * h**2 - hp * h * L + kp * L**2)
    return A, B, R


def verify(H, verbose=True):
    """the two identity-level checks, as polynomial identities in the params."""
    F = family(H)
    out = {"deg_h": H}
    P = F['P']
    Px, Py = spk.dx(P), spk.dy(P)
    out['deg_P'] = spk.tdeg(P)
    out['deg_y_P'] = max(j for (i, j) in P)
    out['n_free_params'] = len(F['free'])
    out['free_params'] = [str(s) for s in F['free']]
    out['P'] = spk.to_str(P)
    out['k'] = sp.sstr(F['k'])
    out['k_division_remainder'] = sp.sstr(F['k_remainder'])

    # (0) k is a polynomial: the division was exact, identically in the params
    out['k_is_polynomial'] = (F['k_remainder'] == 0)

    # (i) exact Bezout identity, as an identity in x, y AND the parameters
    A, B, R = bezout(F)
    Rexp = sp.expand(R - F['gam'] * F['ha']**2)
    out['R'] = sp.sstr(sp.expand(R))
    out['R_minus_gamma_ha2'] = sp.sstr(Rexp)
    out['R_equals_gamma_ha2'] = (Rexp == 0)
    resid = spk.psub(spk.padd(spk.pmul(spk.from_expr(A), Px),
                              spk.pmul(spk.from_expr(B), Py)),
                     spk.from_expr(R))
    out['bezout_residual_terms'] = len(resid)
    out['bezout_identity_holds'] = (resid == {})
    # normalised cofactors U = A/R, V = B/R : U Px + V Py = 1
    out['U'] = sp.sstr(sp.cancel(A / R))
    out['V'] = sp.sstr(sp.cancel(B / R))
    out['bezout_denominator'] = sp.sstr(sp.factor(R))

    # (ii) residues: RES(HE) is  Delta := h^2 - 4 g k  =  alpha x + beta,
    #      hence deg_x Delta_c = deg_x (Delta + 4 g c) <= 1 for every c.
    Delta = sp.expand(F['h']**2 - 4 * F['g'] * F['k'])
    dres = sp.expand(Delta - F['Delta'])
    out['Delta'] = sp.sstr(Delta)
    out['Delta_minus_alpha_x_beta'] = sp.sstr(dres)
    out['RES_HE_holds_identically'] = (dres == 0)
    c = sp.Symbol('c')
    Dc = sp.expand(Delta + 4 * F['g'] * c)
    out['Delta_c'] = sp.sstr(Dc)
    out['deg_x_Delta_c'] = int(sp.degree(sp.Poly(Dc, X)))
    # discriminant of Delta_c in x is meaningless for degree <= 1; record instead
    # that every root is simple (degree <= 1) so mu = 1 at every finite place.
    out['residue_argument'] = (
        "deg_x Delta_c <= 1 identically, so (night17 1.3) every finite branch "
        "point has multiplicity mu = 1 and w = -mu/2 = -1/2 is not an integer "
        "(no finite residue); at infinity W = -deg(Delta_c)/2 = -1/2 is not an "
        "integer when deg = 1 (no place with a residue), and on the single "
        "fibre c = -alpha/(4 gamma) where deg Delta_c = 0 the series is 1 and "
        "[u^1] 1 = 0.  All residues vanish identically on the family.")
    return F, out


if __name__ == "__main__":
    import json
    res = {}
    for H in (1, 2, 3):
        F, o = verify(H)
        res[str(H)] = o
        print("deg h = %d : deg P = %d, params = %d %s" % (H, o['deg_P'], o['n_free_params'], o['free_params']))
        print("   k polynomial              : %s  (remainder %s)" % (o['k_is_polynomial'], o['k_division_remainder']))
        print("   R = gamma*h(a)^2          : %s   R = %s" % (o['R_equals_gamma_ha2'], o['R']))
        print("   A*Px + B*Py - R == 0      : %s   (%d residual terms)" % (o['bezout_identity_holds'], o['bezout_residual_terms']))
        print("   Delta - (alpha x + beta)  : %s  -> RES(HE) identically: %s" % (o['Delta_minus_alpha_x_beta'], o['RES_HE_holds_identically']))
        print("   deg_x Delta_c             : %d" % o['deg_x_Delta_c'])
        print("   P = %s" % o['P'])
    json.dump(res, open('family18.json', 'w'), indent=1)
