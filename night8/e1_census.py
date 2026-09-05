#!/usr/bin/env python3
"""
night8/e1_census.py -- census of every F_2 point of the (K)+(C2) system on the
E1 enlarged support (22 unknowns), enumerated exhaustively by
night8/e1_enumerate.py.

Per point: det J = 1 in F_2[x,y] (direct expansion), the two-point collision,
the additive-type screen, the characteristic-2 tear classification
(EMPTY / NONEMPTY), and -- for every TEAR-NONEMPTY point that is not one of
the 8 E0 points embedded in E1 -- the full 2-adic ladder carrying ALL lifts,
ceiling mod 64.

MEASUREMENTS ONLY.  Characteristic-2 results are labelled as such.
"""
import itertools
import json
import sys
import time

import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar/night8')
from mondello_lift import (System, S_P0, S_Q0, hull_lattice_points,      # noqa
                           rank2, rref2, nullspace2)
from star_point import resultant_data, x, y                              # noqa

OUT = '/home/user/jacobian_planar/night8/e1_census.json'
CEILING = 64
CARRY_CAP = 200000          # guard; exceeding it is a recorded outcome

HP = hull_lattice_points(S_P0)
HQ = hull_lattice_points(S_Q0)
S = System(HP, HQ, 'E1')
VARS = [str(v) for v in S.vars]
N = len(S.vars)
M = len(S.eqs)
LAB = S.labels
f = sp.lambdify(S.vars, S.eqs, modules='math')

PTS = [tuple(p) for p in json.load(open(
    '/home/user/jacobian_planar/night8/e1_points.json'))['E1']['points']]

# --- the 8 E0 points, embedded into E1 coordinates --------------------------
E0_VARS = ['a_1_0', 'a_2_1', 'a_4_0', 'a_6_2',
           'b_0_1', 'b_5_0', 'b_6_1', 'b_7_2', 'b_8_3']
E0_PTS = [tuple(p) for p in json.load(open(
    '/home/user/jacobian_planar/night8/verify_lift.json'
))['brute_force_mod2']['solutions']]
IDX = {v: i for i, v in enumerate(VARS)}
EMB = {}
for p in E0_PTS:
    vec = [0] * N
    for name, c in zip(E0_VARS, p):
        vec[IDX[name]] = c
    EMB[tuple(vec)] = ''.join(str(c) for c in p)
assert all(e in set(PTS) for e in EMB), 'E0 points not found inside E1'


def pair(vec):
    P = sum(c * x ** m[0] * y ** m[1] for c, m in zip(vec[:len(HP)], HP) if c)
    Q = sum(c * x ** n[0] * y ** n[1]
            for c, n in zip(vec[len(HP):], HQ) if c)
    return sp.expand(P), sp.expand(Q)


def additive_screen(P, Q):
    fwd = (not P.has(y)) and (not sp.expand(Q - y).has(y))
    mir = (not Q.has(x)) and (not sp.expand(P - x).has(x))
    return {'forward': bool(fwd), 'mirror': bool(mir),
            'additive_type': bool(fwd or mir)}


def climb(point):
    sub = dict(zip(S.vars, point))
    J2 = [[int(sp.diff(e, w).subs(sub)) % 2 for w in S.vars] for e in S.eqs]
    rk = rank2(J2, N)
    ker = nullspace2(J2, N)

    def coset(s):
        aug = [J2[i] + [s[i]] for i in range(M)]
        if rank2(aug, N + 1) != rk:
            return None
        R, piv = rref2(aug, N + 1)
        part = [0] * N
        for r_, c in enumerate(piv):
            if c < N:
                part[c] = R[r_][N]
        return part

    lvl = [tuple(point)]
    steps = []
    k = 1
    death = None
    capped = False
    while True:
        mf, mt = 2 ** k, 2 ** (k + 1)
        surv, nc, deaths = [], 0, []
        for pt in lvl:
            res = f(*pt)
            s = [(vv // mf) % 2 for vv in res]
            part = coset(s)
            if part is None:
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
            for co in itertools.product((0, 1), repeat=len(ker)):
                d = list(part)
                for c, kv in zip(co, ker):
                    if c:
                        d = [(p_ + q_) % 2 for p_, q_ in zip(d, kv)]
                surv.append(tuple(pt[i] + mf * d[i] for i in range(N)))
                if len(surv) > CARRY_CAP:
                    capped = True
                    break
            if capped:
                break
        steps.append({'level_from': mf, 'level_to': mt,
                      'points_in': len(lvl), 'solvable_steps': nc,
                      'linear_step_solution_space_dim':
                          (N - rk) if nc else None,
                      'solutions_out': len(surv),
                      'exists': 'EXISTS' if surv else 'DOES-NOT-EXIST',
                      'carry_cap_reached': capped,
                      'death_examples': deaths})
        if capped:
            break
        if not surv:
            death = mt
            break
        assert all(all(vv % mt == 0 for vv in f(*p)) for p in surv[:20])
        steps[-1]['sampled_verification_ok'] = True
        lvl = surv
        if mt >= CEILING:
            break
        k += 1
    return {'rank_J_mod2': rk, 'nullity_J_mod2': N - rk, 'steps': steps,
            'death_level': death, 'carry_cap_reached': capped,
            'survives_to_ceiling': bool(death is None and not capped),
            'highest_level_reached': (steps[-1]['level_to']
                                      if steps[-1]['exists'] == 'EXISTS'
                                      else steps[-1]['level_from'])}


def main():
    t0 = time.time()
    rep = {'E1_support_P': [list(m) for m in HP],
           'E1_support_Q': [list(m) for m in HQ],
           'variable_names': VARS, 'n_unknowns': N, 'n_equations': M,
           'equation_labels': LAB, 'ceiling': CEILING,
           'n_F2_points': len(PTS), 'points': []}
    counts = {'total': len(PTS), 'additive_type': 0,
              'proper_nonadditive': 0, 'tear_EMPTY': 0, 'tear_NONEMPTY': 0,
              'is_an_E0_point': 0, 'ladder_run': 0}
    for i, pt in enumerate(PTS):
        P, Q = pair(pt)
        detJ2 = sp.expand(sp.Poly(
            sp.expand(sp.diff(P, x) * sp.diff(Q, y)
                      - sp.diff(P, y) * sp.diff(Q, x)),
            x, y, domain=sp.GF(2)).as_expr())
        img = {str(q): [int(P.subs({x: q[0], y: q[1]})) % 2,
                        int(Q.subs({x: q[0], y: q[1]})) % 2]
               for q in ((0, 1), (1, 0), (1, 1))}
        add = additive_screen(P, Q)
        tear = resultant_data(P, Q, 2)
        empty = bool(tear.get('product_is_a_nonzero_constant'))
        d = {'index': i, 'point': list(pt),
             'bits': ''.join(str(c) for c in pt),
             'is_an_E0_point': tuple(pt) in EMB,
             'E0_bits': EMB.get(tuple(pt)),
             'P': str(P), 'Q': str(Q),
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
                 'product_of_leading_coefficients':
                     tear.get('product_of_leading_coefficients'),
                 'locus': 'EMPTY' if empty else 'NONEMPTY',
                 'flags': tear['flags']}}
        counts['additive_type'] += add['additive_type']
        counts['proper_nonadditive'] += (not add['additive_type'])
        counts['tear_EMPTY'] += empty
        counts['tear_NONEMPTY'] += (not empty)
        counts['is_an_E0_point'] += d['is_an_E0_point']
        if (not empty) and not d['is_an_E0_point']:
            d['ladder'] = climb(pt)
            counts['ladder_run'] += 1
            print('  [%3d] %s ladder: death %s, highest %s'
                  % (i, d['bits'], d['ladder']['death_level'],
                     d['ladder']['highest_level_reached']))
        rep['points'].append(d)
        if i % 20 == 0:
            print('  ... %d/%d  (%.0fs)' % (i, len(PTS), time.time() - t0))
    rep['class_counts'] = counts
    bad = [p['bits'] for p in rep['points']
           if not (p['det_J_equals_1_in_F2'] and p['collision_F01_equals_F10'])]
    rep['universal_checks_failures'] = bad
    surv = [p['bits'] for p in rep['points']
            if p.get('ladder', {}).get('survives_to_ceiling')]
    caps = [p['bits'] for p in rep['points']
            if p.get('ladder', {}).get('carry_cap_reached')]
    deaths = {}
    for p in rep['points']:
        if 'ladder' in p:
            deaths[str(p['ladder']['death_level'])] = \
                deaths.get(str(p['ladder']['death_level']), 0) + 1
    rep['ladder_death_level_histogram'] = deaths
    rep['points_surviving_to_ceiling'] = surv
    rep['points_hitting_the_carry_cap'] = caps
    json.dump(rep, open(OUT, 'w'), indent=1, default=str)
    print(json.dumps(counts, indent=1))
    print('universal check failures:', bad)
    print('death level histogram:', deaths)
    print('surviving to mod 64:', surv, '| carry cap hit:', caps)
    print('written %s  (%.0fs)' % (OUT, time.time() - t0))


if __name__ == '__main__':
    main()
