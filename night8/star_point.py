#!/usr/bin/env python3
"""
night8/star_point.py -- JOB 1: identify the distinguished F_2 point

    (a_1_0, a_2_1, a_4_0, a_6_2, b_0_1, b_5_0, b_6_1, b_7_2, b_8_3)
  = (1,     0,     1,     0,     1,     1,     0,     0,     0)

of the E0 system of night8/MONDELLO_LIFT.md, and measure it.

Everything here is reimplemented IN-LANE: the formal-inverse tail recursion
(same method as night4/tail.py) and the resultant / leading-coefficient
measurement (same statement as night7's tear evaluator) are coded afresh in
this file; nothing is imported from night4/, night6/ or night7/.

MEASUREMENTS ONLY.  Every characteristic-2 result is labelled as such.
"""
import json
import sys

import sympy as sp

x, y, u, v = sp.symbols('x y u v')

# E0 coordinate order -- stated explicitly and used everywhere below
E0_ORDER = ['a_1_0', 'a_2_1', 'a_4_0', 'a_6_2',
            'b_0_1', 'b_5_0', 'b_6_1', 'b_7_2', 'b_8_3']
E0_MONOMS = {'a_1_0': (1, 0), 'a_2_1': (2, 1), 'a_4_0': (4, 0),
             'a_6_2': (6, 2), 'b_0_1': (0, 1), 'b_5_0': (5, 0),
             'b_6_1': (6, 1), 'b_7_2': (7, 2), 'b_8_3': (8, 3)}
STAR = (1, 0, 1, 0, 1, 1, 0, 0, 0)
BASE = (1, 1, 1, 1, 1, 1, 1, 1, 1)


def pair_from_vector(vec):
    P = sum(c * x ** E0_MONOMS[n][0] * y ** E0_MONOMS[n][1]
            for c, n in zip(vec, E0_ORDER) if n.startswith('a') and c)
    Q = sum(c * x ** E0_MONOMS[n][0] * y ** E0_MONOMS[n][1]
            for c, n in zip(vec, E0_ORDER) if n.startswith('b') and c)
    return sp.expand(P), sp.expand(Q)


# ===========================================================================
# in-lane polynomials over F_2 as dicts {(i, j): 1}
# ===========================================================================
def d_add(a, b):
    r = dict(a)
    for k in b:
        if k in r:
            del r[k]
        else:
            r[k] = 1
    return r


def d_mul(a, b, D=None):
    r = {}
    for (i1, j1) in a:
        for (i2, j2) in b:
            if D is not None and i1 + i2 + j1 + j2 > D:
                continue
            k = (i1 + i2, j1 + j2)
            if k in r:
                del r[k]
            else:
                r[k] = 1
    return r


def d_deg(a):
    return max((i + j for i, j in a), default=-1)


def d_homog(a, d):
    return {k: 1 for k in a if k[0] + k[1] == d}


def to_dict(expr):
    p = sp.Poly(expr, x, y)
    return {tuple(int(e) for e in m): 1
            for m, c in zip(p.monoms(), p.coeffs()) if int(c) % 2}


# ---- formal inverse mod 2 (method of night4/tail.py, reimplemented) --------
def subst_linear2(A, M):
    """A(x,y) with x -> M[0][0]x + M[0][1]y, y -> M[1][0]x + M[1][1]y, mod 2."""
    xs = {k: 1 for k, c in ((( 1, 0), M[0][0]), ((0, 1), M[0][1])) if c % 2}
    ys = {k: 1 for k, c in ((( 1, 0), M[1][0]), ((0, 1), M[1][1])) if c % 2}
    D = d_deg(A)
    xp, yp = [{(0, 0): 1}], [{(0, 0): 1}]
    for _ in range(max(D, 0)):
        xp.append(d_mul(xp[-1], xs, D))
        yp.append(d_mul(yp[-1], ys, D))
    out = {}
    for (i, j) in A:
        out = d_add(out, d_mul(xp[i], yp[j], D))
    return out


def powers(P, Q, D):
    Pp, Qp = [{(0, 0): 1}], [{(0, 0): 1}]
    for _ in range(D):
        Pp.append(d_mul(Pp[-1], P, D))
        Qp.append(d_mul(Qp[-1], Q, D))
    return Pp, Qp


def compose_trunc(A, Pp, Qp, D):
    out = {}
    for (i, j) in A:
        if i + j > D:
            continue
        out = d_add(out, d_mul(Pp[i], Qp[j], D))
    return out


def tail_mod2(P, Q, D):
    """Formal inverse G with G(F) = id through degree D, over F_2.

    Returns the tail profile: nnz(G^(m)) summed over both components for
    m = deg F + 1 .. D, plus the mandatory recomposition self-check.
    CHARACTERISTIC-2 MEASUREMENT.
    """
    if (0, 0) in P or (0, 0) in Q:
        raise ValueError('F must satisfy P(0,0) = Q(0,0) = 0')
    L = [[P.get((1, 0), 0), P.get((0, 1), 0)],
         [Q.get((1, 0), 0), Q.get((0, 1), 0)]]
    det = (L[0][0] * L[1][1] - L[0][1] * L[1][0]) % 2
    if det == 0:
        return {'linear_part_invertible_mod2': False, 'L': L}
    Linv = [[L[1][1] % 2, L[0][1] % 2], [L[1][0] % 2, L[0][0] % 2]]  # det = 1
    Pp, Qp = powers(P, Q, D)
    A = {k: 1 for k, c in (((1, 0), Linv[0][0]), ((0, 1), Linv[0][1])) if c}
    B = {k: 1 for k, c in (((1, 0), Linv[1][0]), ((0, 1), Linv[1][1])) if c}
    G = {1: (A, B)}
    S1 = compose_trunc(A, Pp, Qp, D)
    S2 = compose_trunc(B, Pp, Qp, D)
    for d in range(2, D + 1):
        Ad = subst_linear2(d_homog(S1, d), Linv)   # -1 = +1 mod 2
        Bd = subst_linear2(d_homog(S2, d), Linv)
        G[d] = (Ad, Bd)
        if Ad:
            S1 = d_add(S1, compose_trunc(Ad, Pp, Qp, D))
        if Bd:
            S2 = d_add(S2, compose_trunc(Bd, Pp, Qp, D))
    G1, G2 = {}, {}
    for d in range(1, D + 1):
        G1 = d_add(G1, G[d][0])
        G2 = d_add(G2, G[d][1])
    C1 = compose_trunc(G1, Pp, Qp, D)
    C2 = compose_trunc(G2, Pp, Qp, D)
    ok = (C1 == {(1, 0): 1}) and (C2 == {(0, 1): 1})
    degF = max(d_deg(P), d_deg(Q))
    prof = [len(G[m][0]) + len(G[m][1]) for m in range(degF + 1, D + 1)]
    return {
        'linear_part_invertible_mod2': True,
        'deg_F': degF, 'D': D,
        'tail_profile_degrees': list(range(degF + 1, D + 1)),
        'tail_profile': prof,
        'tail_all_zero': all(n == 0 for n in prof),
        'first_nonzero_tail_degree':
            next((degF + 1 + i for i, n in enumerate(prof) if n), None),
        'recomposition_selfcheck_G_of_F_is_identity': bool(ok),
        'deg_G_computed': max(d_deg(G1), d_deg(G2)),
        'characteristic': 2,
    }


# ===========================================================================
# in-lane resultant / leading-coefficient measurement (statement as in
# night7's tear evaluator; reimplemented here)
# ===========================================================================
def resultant_data(P, Q, char):
    """R1 = Res_y(P-u, Q-v) in x; R2 = Res_x(P-u, Q-v) in y; leading coeffs."""
    g1, g2 = sp.expand(P - u), sp.expand(Q - v)
    jac = sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))
    if char:
        jac = sp.expand(sp.Poly(jac, x, y, domain=sp.GF(char)).as_expr())
    out = {'char': char, 'jacobian_det': str(jac), 'branches': {}, 'flags': []}
    if char:
        out['flags'].append('POSITIVE_CHARACTERISTIC')
    if jac == 0:
        out['flags'].append('NOT_DOMINANT')
    lcs = []
    for name, elim, src in (('R1', y, x), ('R2', x, y)):
        dom = sp.GF(char)[(src, u, v)] if char else sp.ZZ[(src, u, v)]
        R = sp.expand(sp.sympify(sp.Poly(g1, elim, domain=dom)
                                 .resultant(sp.Poly(g2, elim, domain=dom))))
        b = {'eliminated': str(elim), 'source_var': str(src),
             'resultant': str(R)}
        if R == 0:
            b['degree_in_source_var'] = None
            b['leading_coefficient'] = None
            out['flags'].append('RESULTANT_IDENTICALLY_ZERO:' + name)
            out['branches'][name] = b
            continue
        cdom = sp.GF(char)[(u, v)] if char else sp.ZZ[(u, v)]
        Rp = sp.Poly(R, src, domain=cdom)
        lc = sp.expand(sp.sympify(Rp.LC()))
        # generic Sylvester bound on deg_src
        d1e = sp.Poly(g1, elim).degree()
        d2e = sp.Poly(g2, elim).degree()
        d1s = sp.Poly(g1, src).degree() if g1.has(src) else 0
        d2s = sp.Poly(g2, src).degree() if g2.has(src) else 0
        bound = int(d1s * d2e + d2s * d1e)
        b.update({'degree_in_source_var': int(Rp.degree()),
                  'sylvester_degree_bound': bound,
                  'leading_coefficient': str(lc),
                  'leading_coefficient_is_constant': not lc.free_symbols})
        if int(Rp.degree()) == 0:
            out['flags'].append('DEGREE_ZERO_IN_SOURCE_VAR:' + name)
        if int(Rp.degree()) < bound:
            out['flags'].append('DEGREE_DROP:%s(%d<%d)'
                                % (name, int(Rp.degree()), bound))
        lcs.append(lc)
        out['branches'][name] = b
    if len(lcs) == 2:
        prod = sp.expand(lcs[0] * lcs[1])
        if char:
            prod = sp.expand(sp.Poly(prod, u, v, domain=sp.GF(char)).as_expr())
        out['product_of_leading_coefficients'] = str(prod)
        out['product_is_a_nonzero_constant'] = bool(
            prod != 0 and not prod.free_symbols)
    return out


# ===========================================================================
def main():
    rep = {'E0_coordinate_order': E0_ORDER,
           'E0_monomials': {k: list(vmn) for k, vmn in E0_MONOMS.items()},
           'star_point_vector': list(STAR),
           'base_point_vector': list(BASE)}

    Ps, Qs = pair_from_vector(STAR)
    Pb, Qb = pair_from_vector(BASE)
    rep['star_pair'] = {'P_star': str(Ps), 'Q_star': str(Qs)}
    print('P* =', Ps)
    print('Q* =', Qs)

    # --- supports actually present / absent -------------------------------
    present = [n for n, c in zip(E0_ORDER, STAR) if c]
    absent = [n for n, c in zip(E0_ORDER, STAR) if not c]
    rep['coefficients_present'] = present
    rep['coefficients_zero'] = absent
    rep['support_P_star'] = [list(E0_MONOMS[n]) for n in present
                             if n.startswith('a')]
    rep['support_Q_star'] = [list(E0_MONOMS[n]) for n in present
                             if n.startswith('b')]
    rep['deg_P_star'] = int(sp.Poly(Ps, x, y).total_degree())
    rep['deg_Q_star'] = int(sp.Poly(Qs, x, y).total_degree())
    rep['deg_F_star'] = max(rep['deg_P_star'], rep['deg_Q_star'])
    rep['P_star_involves_y'] = bool(Ps.has(y))
    rep['Q_star_minus_y_involves_y'] = bool(sp.expand(Qs - y).has(y))

    # --- det J by direct expansion over F_2 -------------------------------
    detJ = sp.expand(sp.diff(Ps, x) * sp.diff(Qs, y)
                     - sp.diff(Ps, y) * sp.diff(Qs, x))
    detJ2 = sp.expand(sp.Poly(detJ, x, y, domain=sp.GF(2)).as_expr())
    rep['det_J_over_Z'] = str(detJ)
    rep['det_J_over_F2'] = str(detJ2)
    rep['det_J_equals_1_in_F2'] = bool(sp.simplify(detJ2 - 1) == 0)
    print('det J over Z =', detJ, '| over F_2 =', detJ2)

    # --- collision images --------------------------------------------------
    imgs = {}
    for pt in [(0, 1), (1, 0), (1, 1), (0, 0)]:
        sub = {x: pt[0], y: pt[1]}
        imgs[str(pt)] = [int(Ps.subs(sub)) % 2, int(Qs.subs(sub)) % 2]
    rep['images_over_F2'] = imgs
    rep['collision_F01_equals_F10'] = imgs['(0, 1)'] == imgs['(1, 0)']
    rep['collision_includes_F11'] = (imgs['(0, 1)'] == imgs['(1, 1)'])
    rep['common_image_of_(0,1)_and_(1,0)'] = imgs['(0, 1)']
    print('images:', imgs)

    # --- relation to the Mondello base point -------------------------------
    swapP = sp.expand(Qb.subs({x: y, y: x}, simultaneous=True))
    swapQ = sp.expand(Pb.subs({x: y, y: x}, simultaneous=True))
    sym = {
        'base_pair': {'P': str(Pb), 'Q': str(Qb)},
        'star_is_base_with_these_coefficients_set_to_zero': absent,
        'equal_to_base': bool(sp.expand(Ps - Pb) == 0
                              and sp.expand(Qs - Qb) == 0),
        'xy_swap_conjugate_of_base': {'P': str(swapP), 'Q': str(swapQ)},
        'star_equals_xy_swap_conjugate_of_base':
            bool(sp.expand(Ps - swapP) == 0 and sp.expand(Qs - swapQ) == 0),
        'xy_swap_conjugate_of_star': {
            'P': str(sp.expand(Qs.subs({x: y, y: x}, simultaneous=True))),
            'Q': str(sp.expand(Ps.subs({x: y, y: x}, simultaneous=True)))},
        'star_is_xy_swap_invariant':
            bool(sp.expand(Ps - Qs.subs({x: y, y: x}, simultaneous=True)) == 0
                 and sp.expand(Qs - Ps.subs({x: y, y: x},
                                            simultaneous=True)) == 0),
        'frobenius_squaring_of_coefficients_note':
            'over F_2 every coefficient satisfies c^2 = c, so coefficientwise '
            'Frobenius is the identity on both pairs; it relates nothing that '
            'was not already equal',
        'coefficientwise_frobenius_changes_star': False,
    }
    rel = (sym['equal_to_base'] or sym['star_equals_xy_swap_conjugate_of_base'])
    sym['verdict'] = ('related by one of the checked symmetries' if rel
                      else 'no obvious relation under the checked symmetries '
                           '(equality, x<->y swap conjugation, coefficientwise '
                           'Frobenius); the only recorded relation is the '
                           'coordinate one: the star point is the base point '
                           'with the listed coefficients set to 0')
    rep['symmetry'] = sym
    print('symmetry verdict:', sym['verdict'])

    # --- tail recursion mod 2 (CHARACTERISTIC-2 MEASUREMENT) ---------------
    D = 2 * rep['deg_F_star'] + 4
    Pd, Qd = to_dict(Ps), to_dict(Qs)
    t_star = tail_mod2(Pd, Qd, D)
    rep['tail_mod2_star'] = t_star
    print('tail (char 2) D=%d: %s  selfcheck=%s'
          % (D, t_star.get('tail_profile'),
             t_star.get('recomposition_selfcheck_G_of_F_is_identity')))

    # control on the reimplementation: a tame automorphism must have zero tail
    for lbl, (A, B) in [('(x, y+x^2)', (x, y + x ** 2)),
                        ('(x+y^3, y)', (x + y ** 3, y)),
                        ('(x, y+x^2) o (x+y^2, y)',
                         (sp.expand((x).subs({x: x + y ** 2}, simultaneous=True)),
                          sp.expand((y + x ** 2).subs({x: x + y ** 2},
                                                      simultaneous=True))))]:
        tt = tail_mod2(to_dict(sp.expand(A)), to_dict(sp.expand(B)), 14)
        rep.setdefault('tail_controls', {})[lbl] = {
            'tail_all_zero': tt.get('tail_all_zero'),
            'selfcheck': tt.get('recomposition_selfcheck_G_of_F_is_identity')}
        if not (tt.get('tail_all_zero') and
                tt.get('recomposition_selfcheck_G_of_F_is_identity')):
            print('TAIL CONTROL FAILED on %s' % lbl)
            json.dump(rep, open(OUT, 'w'), indent=1, default=str)
            sys.exit(4)
    print('tail controls (tame automorphisms, mod 2): all pass')

    # for comparison, the same measurement on the Mondello base pair
    rep['tail_mod2_base_pair'] = tail_mod2(to_dict(Pb), to_dict(Qb),
                                           2 * 11 + 4)

    # --- resultant / leading-coefficient data (CHARACTERISTIC-2) ----------
    rep['tear_char2_star'] = resultant_data(Ps, Qs, 2)
    rep['tear_char2_base'] = resultant_data(Pb, Qb, 2)
    # control on the reimplementation, characteristic 0
    c_tame = resultant_data(x, y + x ** 2, 0)
    c_xxy = resultant_data(x, x * y, 0)
    rep['tear_controls'] = {
        'char0_(x, y+x^2)_leading_coeffs_constant': [
            c_tame['branches'][k]['leading_coefficient_is_constant']
            for k in ('R1', 'R2')],
        'char0_(x, x*y)_product_of_leading_coefficients':
            c_xxy.get('product_of_leading_coefficients'),
    }
    print('tear char 2 (star): R1 lc = %s ; R2 lc = %s ; flags %s'
          % (rep['tear_char2_star']['branches']['R1']['leading_coefficient'],
             rep['tear_char2_star']['branches']['R2']['leading_coefficient'],
             rep['tear_char2_star']['flags']))

    json.dump(rep, open(OUT, 'w'), indent=1, default=str)
    print('written', OUT)


OUT = '/home/user/jacobian_planar/night8/star_point.json'

if __name__ == '__main__':
    main()
