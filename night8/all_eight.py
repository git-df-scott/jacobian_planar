#!/usr/bin/env python3
"""
night8/all_eight.py -- census of all 8 F_2 points of the E0 system.

E0 coordinate order (as everywhere in night8):
    ( a_1_0 , a_2_1 , a_4_0 , a_6_2 , b_0_1 , b_5_0 , b_6_1 , b_7_2 , b_8_3 )

For each of the 8 points: reconstruct the pair, verify det J = 1 in F_2[x,y]
and the two-point collision, apply the additive-type screen, compute the
characteristic-2 resultant leading-coefficient data (EMPTY / NONEMPTY), and
climb the 2-adic ladder (carrying ALL lifts at every level, ceiling mod 64)
recording the death level and the obstruction rows.

Reimplemented in-lane; nothing imported from night4/, night6/, night7/.
MEASUREMENTS ONLY.  Characteristic-2 results are labelled as such.
"""
import itertools
import json
import sys

import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar/night8')
from mondello_lift import System, S_P0, S_Q0, rank2, rref2, nullspace2  # noqa
from star_point import (E0_ORDER, E0_MONOMS, pair_from_vector,          # noqa
                        to_dict, tail_mod2, resultant_data, x, y, u, v)

OUT = '/home/user/jacobian_planar/night8/all_eight.json'
CEILING = 64

S = System(S_P0, S_Q0, 'E0')
N = len(S.vars)
M = len(S.eqs)
LAB = S.labels
f = sp.lambdify(S.vars, S.eqs, modules='math')

BASE = (1, 1, 1, 1, 1, 1, 1, 1, 1)
STAR = (1, 0, 1, 0, 1, 1, 0, 0, 0)


# ---------------------------------------------------------------- ladder ----
def climb(point):
    """Full 2-adic ladder over an F_2 point, all lifts carried, ceiling 64."""
    sub = dict(zip(S.vars, point))
    J2 = [[int(sp.diff(e, w).subs(sub)) % 2 for w in S.vars] for e in S.eqs]
    rk = rank2(J2, N)
    ker = nullspace2(J2, N)
    zero_rows = [LAB[i] for i, row in enumerate(J2) if not any(row)]

    def coset(s):
        aug = [J2[i] + [s[i]] for i in range(M)]
        if rank2(aug, N + 1) != rk:
            return None
        R, piv = rref2(aug, N + 1)
        part = [0] * N
        for r_, c in enumerate(piv):
            if c < N:
                part[c] = R[r_][N]
        sols = []
        for co in itertools.product((0, 1), repeat=len(ker)):
            d = list(part)
            for c, b in zip(co, ker):
                if c:
                    d = [(p + q) % 2 for p, q in zip(d, b)]
            sols.append(d)
        return sols

    lvl = [tuple(point)]
    steps = []
    k = 1
    death = None
    while True:
        mf, mt = 2 ** k, 2 ** (k + 1)
        surv, nc, deaths = [], 0, []
        for pt in lvl:
            res = f(*pt)
            assert all(vv % mf == 0 for vv in res)
            s = [(vv // mf) % 2 for vv in res]
            sols = coset(s)
            if sols is None:
                if len(deaths) < 3:
                    deaths.append({
                        'point_mod_%d' % mf: [int(c) % mf for c in pt],
                        'rhs_s_mod2_nonzero_rows':
                            [LAB[i] for i in range(M) if s[i]],
                        'obstruction_rows_zero_gradient_but_rhs_1':
                            [LAB[i] for i in range(M)
                             if s[i] and not any(J2[i])],
                        'rank_J_mod2': rk,
                        'rank_augmented_mod2':
                            rank2([J2[i] + [s[i]] for i in range(M)], N + 1)})
                continue
            nc += 1
            for d in sols:
                surv.append(tuple(pt[i] + mf * d[i] for i in range(N)))
        steps.append({'level_from': mf, 'level_to': mt,
                      'points_in': len(lvl), 'solvable_steps': nc,
                      'linear_step_solution_space_dim':
                          (N - rk) if nc else None,
                      'solutions_out': len(surv),
                      'exists': 'EXISTS' if surv else 'DOES-NOT-EXIST',
                      'death_examples': deaths})
        if not surv:
            death = mt
            break
        # verification control on the new level
        smp = surv[:20]
        assert all(all(vv % mt == 0 for vv in f(*p)) for p in smp)
        steps[-1]['sampled_verification_ok'] = True
        lvl = surv
        if mt >= CEILING:
            break
        k += 1
    return {'rank_J_mod2': rk, 'nullity_J_mod2': N - rk,
            'rows_with_vanishing_gradient_mod2': zero_rows,
            'steps': steps, 'death_level': death,
            'highest_level_reached': (steps[-1]['level_to']
                                      if steps[-1]['exists'] == 'EXISTS'
                                      else steps[-1]['level_from']),
            'survives_to_ceiling': bool(death is None),
            'n_solutions_at_highest_level':
                (steps[-1]['solutions_out']
                 if steps[-1]['exists'] == 'EXISTS' else 0)}


# ------------------------------------------------------------ classify ------
def additive_screen(P, Q):
    """P free of y and Q - y free of y  (or the x <-> y mirror)."""
    fwd = (not P.has(y)) and (not sp.expand(Q - y).has(y))
    mir = (not Q.has(x)) and (not sp.expand(P - x).has(x))
    return {'forward_form_P_free_of_y_and_Q_minus_y_free_of_y': bool(fwd),
            'mirror_form_Q_free_of_x_and_P_minus_x_free_of_x': bool(mir),
            'additive_type': bool(fwd or mir)}


def main():
    pts = [tuple(p) for p in itertools.product((0, 1), repeat=N)
           if all(vv % 2 == 0 for vv in f(*p))]
    assert len(pts) == 8, len(pts)
    assert BASE in pts and STAR in pts
    rep = {'E0_coordinate_order': E0_ORDER,
           'n_F2_points': len(pts), 'points': [], 'ceiling': CEILING}

    for pt in pts:
        P, Q = pair_from_vector(pt)
        detJ = sp.expand(sp.diff(P, x) * sp.diff(Q, y)
                         - sp.diff(P, y) * sp.diff(Q, x))
        detJ2 = sp.expand(sp.Poly(detJ, x, y, domain=sp.GF(2)).as_expr())
        img = {str(q): [int(P.subs({x: q[0], y: q[1]})) % 2,
                        int(Q.subs({x: q[0], y: q[1]})) % 2]
               for q in ((0, 1), (1, 0), (1, 1))}
        add = additive_screen(P, Q)
        tear = resultant_data(P, Q, 2)
        prod = tear.get('product_of_leading_coefficients')
        empty = tear.get('product_is_a_nonzero_constant')
        degF = max(int(sp.Poly(P, x, y).total_degree()),
                   int(sp.Poly(Q, x, y).total_degree()))
        d = {
            'point': list(pt),
            'is_mondello_base_point': pt == BASE,
            'is_star_point': pt == STAR,
            'P': str(P), 'Q': str(Q),
            'deg_P': int(sp.Poly(P, x, y).total_degree()),
            'deg_Q': int(sp.Poly(Q, x, y).total_degree()),
            'det_J_over_F2': str(detJ2),
            'det_J_equals_1_in_F2': bool(sp.expand(detJ2 - 1) == 0),
            'images_over_F2': img,
            'collision_F01_equals_F10': img['(0, 1)'] == img['(1, 0)'],
            'collision_includes_F11': img['(0, 1)'] == img['(1, 1)'],
            'additive_screen_char2': add,
            'tear_char2': {
                'R1_leading_coefficient':
                    tear['branches']['R1'].get('leading_coefficient'),
                'R2_leading_coefficient':
                    tear['branches']['R2'].get('leading_coefficient'),
                'R1_degree_in_source_var':
                    tear['branches']['R1'].get('degree_in_source_var'),
                'R2_degree_in_source_var':
                    tear['branches']['R2'].get('degree_in_source_var'),
                'R1_sylvester_bound':
                    tear['branches']['R1'].get('sylvester_degree_bound'),
                'R2_sylvester_bound':
                    tear['branches']['R2'].get('sylvester_degree_bound'),
                'product_of_leading_coefficients': prod,
                'locus': 'EMPTY' if empty else 'NONEMPTY',
                'flags': tear['flags'],
            },
            'tail_mod2_char2': tail_mod2(to_dict(P), to_dict(Q), 2 * degF + 4),
        }
        # (3) ladder for the non-additive-type, TEAR-NONEMPTY points; the
        # others get classification only.  The base and star points already
        # have their ladders on record (MONDELLO_LIFT.md, LADDER_8.md); they
        # are recomputed here so the census is uniform.
        run = (not add['additive_type']) and (not empty)
        d['ladder_run'] = run or pt in (BASE, STAR)
        d['ladder_run_reason'] = (
            'non-additive-type and TEAR-NONEMPTY' if run else
            ('already on record; recomputed for a uniform census'
             if pt in (BASE, STAR) else
             'classification only: additive-type and/or TEAR-EMPTY'))
        if d['ladder_run']:
            d['ladder'] = climb(pt)
        rep['points'].append(d)
        print('%s  P=%-34s Q=%-34s  add=%-5s tear=%-8s ladder=%s'
              % (''.join(map(str, pt)), d['P'], d['Q'],
                 add['additive_type'], d['tear_char2']['locus'],
                 (d['ladder']['death_level'] if d.get('ladder') else '-')))

    json.dump(rep, open(OUT, 'w'), indent=1, default=str)
    print('written', OUT)
    surv = [p for p in rep['points']
            if p.get('ladder', {}).get('survives_to_ceiling')]
    print('points surviving to the mod-64 ceiling: %d' % len(surv))


if __name__ == '__main__':
    main()
