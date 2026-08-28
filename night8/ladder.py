#!/usr/bin/env python3
"""
night8/ladder.py -- JOB 2: climb the 2-adic ladder over the distinguished
F_2 point

  star = (a_1_0, a_2_1, a_4_0, a_6_2, b_0_1, b_5_0, b_6_1, b_7_2, b_8_3)
       = (1,     0,     1,     0,     1,     1,     0,     0,     0),
  i.e.  P* = x + x^4,  Q* = y + x^5.

System: the E0 system of night8/MONDELLO_LIFT.md over Z --
  (K)  every coefficient of P_x Q_y - P_y Q_x - 1 = 0
  (C2) P(0,1) - P(1,0) = 0,  Q(0,1) - Q(1,0) = 0.

Step used at every level (derivation in night8/MONDELLO_LIFT.md sec. 5):
with r quadratic and x_{k+1} = x_k + 2^k d, r(x_k) = 2^k s_k,

      r(x_k + 2^k d) = 2^k ( s_k + J d )   (mod 2^{k+1}),   J = Dr(x_0) mod 2,

so the level step is the F_2 linear system  J d = s_k, solvable iff
rank(J) = rank([J | s_k]); its solution set is a coset of ker(J).
J is recomputed at the star point (it need not equal the base point's J).

ALL lifts are carried forward: at each level the complete set of solutions
mod 2^{k+1} lying over the star point is enumerated.  Ceiling: mod 64.

MEASUREMENTS ONLY.
"""
import itertools
import json
import sys

import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar/night8')
from mondello_lift import System, S_P0, S_Q0, rank2, rref2, nullspace2  # noqa

STAR = [1, 0, 1, 0, 1, 1, 0, 0, 0]
CEILING = 64
OUT = '/home/user/jacobian_planar/night8/ladder.json'

S = System(S_P0, S_Q0, 'E0')
VARS = [str(v) for v in S.vars]
N = len(VARS)
M = len(S.eqs)
f = sp.lambdify(S.vars, S.eqs, modules='math')

out = {'E0_coordinate_order': VARS, 'star_point': STAR,
       'n_unknowns': N, 'n_equations': M,
       'equation_labels': S.labels, 'ceiling': CEILING}

# --- J mod 2 at the star point ---------------------------------------------
sub = dict(zip(S.vars, STAR))
J2 = [[int(sp.diff(e, v).subs(sub)) % 2 for v in S.vars] for e in S.eqs]
rk = rank2(J2, N)
nul = N - rk
ker = nullspace2(J2, N)
zero_rows = [S.labels[i] for i, row in enumerate(J2) if not any(row)]
out['J_mod2_at_star'] = J2
out['rank_J_mod2_at_star'] = rk
out['nullity_J_mod2_at_star'] = nul
out['rows_with_vanishing_gradient_mod2'] = zero_rows
out['J_mod2_equals_base_point_J'] = None      # filled below
print('star point: rank(J mod 2) = %d, nullity = %d, %d zero rows'
      % (rk, nul, len(zero_rows)))

Jb = [[int(sp.diff(e, v).subs(dict(zip(S.vars, [1] * N)))) % 2
       for v in S.vars] for e in S.eqs]
out['J_mod2_equals_base_point_J'] = (J2 == Jb)
print('J mod 2 at star equals J mod 2 at the Mondello base point: %s'
      % (J2 == Jb))

# residual of the star point must be 0 mod 2
r0 = f(*STAR)
assert all(vv % 2 == 0 for vv in r0), r0
out['star_residual_over_Z'] = {S.labels[i]: r0[i] for i in range(M) if r0[i]}


def coset(s):
    """All d with J d = s over F_2, or None if inconsistent."""
    aug = [J2[i] + [s[i]] for i in range(M)]
    if rank2(aug, N + 1) != rk:
        return None
    R, piv = rref2(aug, N + 1)
    part = [0] * N
    for rr, c in enumerate(piv):
        if c < N:
            part[c] = R[rr][N]
    sols = []
    for coeffs in itertools.product((0, 1), repeat=len(ker)):
        d = list(part)
        for c, b in zip(coeffs, ker):
            if c:
                d = [(p + q) % 2 for p, q in zip(d, b)]
        sols.append(d)
    return sols


# --- climb ------------------------------------------------------------------
level = [tuple(STAR)]          # solutions mod 2 (= the star point itself)
table = []
k = 1
death = None
while 2 ** k < CEILING * 2:
    mod_from, mod_to = 2 ** k, 2 ** (k + 1)
    survivors = []
    n_consistent = 0
    dead_examples = []
    for pt in level:
        res = f(*pt)
        assert all(vv % mod_from == 0 for vv in res)
        s = [(vv // mod_from) % 2 for vv in res]
        sols = coset(s)
        if sols is None:
            if len(dead_examples) < 3:
                bad = [S.labels[i] for i in range(M)
                       if s[i] and not any(J2[i])]
                dead_examples.append({
                    'point_mod_%d' % mod_from: [int(c) % mod_from for c in pt],
                    'rhs_s_mod2_nonzero_rows':
                        [S.labels[i] for i in range(M) if s[i]],
                    'obstruction_rows_zero_gradient_but_rhs_1': bad,
                    'rank_J_mod2': rk,
                    'rank_augmented_mod2':
                        rank2([J2[i] + [s[i]] for i in range(M)], N + 1)})
            continue
        n_consistent += 1
        for d in sols:
            survivors.append(tuple(pt[i] + mod_from * d[i] for i in range(N)))
    rec = {'level_from': mod_from, 'level_to': mod_to,
           'n_points_at_level_%d' % mod_from: len(level),
           'n_of_them_with_a_solvable_linear_step': n_consistent,
           'linear_step_solution_space_dim': nul if n_consistent else None,
           'n_solutions_at_level_%d' % mod_to: len(survivors),
           'exists': 'EXISTS' if survivors else 'DOES-NOT-EXIST',
           'dead_examples': dead_examples}
    print('mod %2d -> mod %2d : %6d points in, %6d solvable, %6d out'
          % (mod_from, mod_to, len(level), n_consistent, len(survivors)))
    table.append(rec)
    if not survivors:
        death = mod_to
        break
    # verification control on a sample of the new level
    import random
    random.seed(20260828)
    smp = random.sample(survivors, min(20, len(survivors)))
    okall = all(all(vv % mod_to == 0 for vv in f(*p)) for p in smp)
    rec['sampled_verification_residual_zero_mod_%d' % mod_to] = okall
    rec['n_sampled'] = len(smp)
    if not okall:
        print('VERIFICATION FAILURE at level %d' % mod_to)
        out['ladder'] = table
        json.dump(out, open(OUT, 'w'), indent=1, default=str)
        sys.exit(5)
    level = survivors
    if mod_to >= CEILING:
        break
    k += 1

out['ladder'] = table
out['death_level'] = death
out['highest_level_reached'] = (table[-1]['level_to'] if table[-1]['exists']
                               == 'EXISTS' else table[-1]['level_from'])
out['example_solutions_at_highest_level'] = [list(p) for p in level[:5]] \
    if table[-1]['exists'] == 'EXISTS' else []
json.dump(out, open(OUT, 'w'), indent=1, default=str)
print('highest level reached:', out['highest_level_reached'])
print('written', OUT)

# ---------------------------------------------------------------------------
# CONTROLS
# (a) the 16 mod-4 solutions produced by the ladder must coincide, as residues
#     mod 4, with the 16 found by the exhaustive (Z/4)^9 search of
#     night8/verify_lift.py;
# (b) exhaustive mod-8 brute force over every point congruent to one of those
#     16 solutions mod 4 (16 * 2^9 = 8192 candidates) must find nothing, which
#     is an enumeration check on the linear-algebra verdict.
# ---------------------------------------------------------------------------
ctrl = {}
bf = json.load(open('/home/user/jacobian_planar/night8/verify_lift.json'))
ex4 = {tuple(p) for p in bf['brute_force_mod4'].get('all_solutions_mod4', [])}
lad4 = {tuple(c % 4 for c in p) for p in
        (level if table[0]['exists'] == 'EXISTS' else [])}
ctrl['ladder_mod4_count'] = len(lad4)
if ex4:
    ctrl['matches_exhaustive_mod4_search'] = (lad4 == ex4)
else:
    ctrl['matches_exhaustive_mod4_search'] = 'exhaustive list not stored'

found8 = []
for p4 in sorted(lad4):
    for bits in itertools.product((0, 1), repeat=N):
        p8 = tuple(p4[i] + 4 * bits[i] for i in range(N))
        if all(vv % 8 == 0 for vv in f(*p8)):
            found8.append(p8)
ctrl['exhaustive_mod8_candidates_tested'] = len(lad4) * 2 ** N
ctrl['exhaustive_mod8_solutions_over_the_16'] = len(found8)
out['controls'] = ctrl
json.dump(out, open(OUT, 'w'), indent=1, default=str)
print('control: ladder mod-4 set size %d; exhaustive mod-8 search over them '
      'tested %d candidates and found %d solutions'
      % (len(lad4), ctrl['exhaustive_mod8_candidates_tested'], len(found8)))
