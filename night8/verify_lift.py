#!/usr/bin/env python3
"""
night8/verify_lift.py -- independent controls on night8/mondello_lift.py.

(1) exhaustive brute force over Z/4: is there ANY point of (Z/4)^9 solving the
    E0 integral system mod 4, and is there one congruent to the base point
    mod 2?  (The linear-algebra answer of STEP 2 must agree with the second.)
(2) control on the GF(2) Groebner basis: every generator reduces to 0 modulo
    the basis, and the base point satisfies every basis element.
(3) dimension of the leading-term ideal (maximal independent set of variables),
    i.e. the Krull dimension of the E0 ideal over the algebraic closure of F_2.

MEASUREMENTS ONLY.
"""
import itertools
import json
import sys

import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar/night8')
from mondello_lift import System, S_P0, S_Q0, convex_hull   # noqa: E402

S = System(S_P0, S_Q0, 'E0')
vars_ = S.vars
n = len(vars_)
base = [S.base[v] for v in vars_]

# compiled integer evaluators for the 15 equations
f = sp.lambdify(vars_, S.eqs, modules='math')

out = {}

# ---- (1) exhaustive mod-4 search ------------------------------------------
all4 = []
lift_of_base = []
for pt in itertools.product(range(4), repeat=n):
    r = f(*pt)
    if all(v % 4 == 0 for v in r):
        all4.append(pt)
        if all((pt[i] - base[i]) % 2 == 0 for i in range(n)):
            lift_of_base.append(pt)
out['brute_force_mod4'] = {
    'search_space': 4 ** n,
    'n_solutions_mod4_total': len(all4),
    'n_solutions_mod4_congruent_to_base_mod2': len(lift_of_base),
    'example_solutions_mod4': [list(p) for p in all4[:5]],
    'variable_names': [str(v) for v in vars_],
    'base_point': base,
}
print('brute force over (Z/4)^%d: %d solutions mod 4 in total, %d of them '
      'congruent to the base point mod 2'
      % (n, len(all4), len(lift_of_base)))

# also: exhaustive mod-2 solution count (the F_2 deformation space, E0)
sol2 = [pt for pt in itertools.product(range(2), repeat=n)
        if all(v % 2 == 0 for v in f(*pt))]
out['brute_force_mod2'] = {
    'n_F2_points_of_the_E0_system': len(sol2),
    'base_point_is_among_them': tuple(base) in set(sol2),
    'solutions': [list(p) for p in sol2],
}
print('F_2 points of the E0 system (K)+(C2): %d; base point among them: %s'
      % (len(sol2), tuple(base) in set(sol2)))

# ---- (2) Groebner controls -------------------------------------------------
gb = sp.groebner(S.eqs, *vars_, order='grevlex', modulus=2)
red = [sp.simplify(gb.reduce(e)[1]) for e in S.eqs]
red_zero = all(sp.Poly(r, *vars_, modulus=2).is_zero if r != 0 else True
               for r in red)
base_ok = all(int(sp.expand(g).subs(dict(zip(vars_, base)))) % 2 == 0
              for g in gb.exprs)
out['groebner_controls'] = {
    'all_generators_reduce_to_zero': bool(red_zero),
    'base_point_satisfies_every_basis_element': bool(base_ok),
    'n_basis_elements': len(gb.exprs),
}
print('GB control: generators reduce to 0: %s; base point on every basis '
      'element: %s' % (red_zero, base_ok))

# ---- (3) Krull dimension via maximal independent set -----------------------
lead = [sp.Poly(g, *vars_, modulus=2).LM(order='grevlex') for g in gb.exprs]
supports = [frozenset(i for i, e in enumerate(m.exponents) if e) for m in lead]
best = []
for k in range(n, -1, -1):
    found = None
    for U in itertools.combinations(range(n), k):
        Us = set(U)
        if all(not (sup <= Us) for sup in supports):
            found = U
            break
    if found is not None:
        best = list(found)
        break
out['krull_dimension_E0_over_closure_F2'] = {
    'dimension': len(best),
    'a_maximal_independent_set': [str(vars_[i]) for i in best],
    'leading_monomial_supports': [sorted(str(vars_[i]) for i in s)
                                  for s in supports],
    'method': 'dim V(I) = max |U| with LT(I) cap k[U] = 0 (grevlex GB, GF(2))',
}
print('Krull dimension of the E0 ideal (char 2): %d, independent set %s'
      % (len(best), [str(vars_[i]) for i in best]))


# ---- (4) which F_2 points of the system admit a mod-4 lift ------------------
from mondello_lift import rank2   # noqa: E402
red_of_mod4 = sorted({tuple(v % 2 for v in p4) for p4 in all4})
per_point = []
for p2 in sol2:
    sub = dict(zip(vars_, p2))
    J2 = [[int(sp.diff(e, v).subs(sub)) % 2 for v in vars_] for e in S.eqs]
    r = rank2(J2, n)
    per_point.append({
        'point': list(p2),
        'is_base_point': tuple(p2) == tuple(base),
        'rank_J_mod2': r,
        'nullity_mod2': n - r,
        'admits_mod4_lift': tuple(p2) in set(red_of_mod4),
        'n_mod4_lifts': sum(1 for q in all4
                            if all((q[i] - p2[i]) % 2 == 0 for i in range(n))),
    })
out['per_F2_point'] = per_point
print('per F_2 point (rank mod 2, # mod-4 lifts):')
for d in per_point:
    print('   ', d['point'], 'rank', d['rank_J_mod2'],
          'lifts', d['n_mod4_lifts'], 'base' if d['is_base_point'] else '')

json.dump(out, open('/home/user/jacobian_planar/night8/verify_lift.json', 'w'),
          indent=1, default=str)
print('written night8/verify_lift.json')
