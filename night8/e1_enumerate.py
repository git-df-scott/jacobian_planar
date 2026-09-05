#!/usr/bin/env python3
"""
night8/e1_enumerate.py -- exhaustive enumeration of the F_2 points of the
(K)+(C2) system on the E1 enlarged support (22 unknowns).

E1 supports (hull lattice points, computed in night8/mondello_lift.py):
  P: 9 monomials, Q: 13 monomials.

METHOD.  det J = P_x Q_y - P_y Q_x is BILINEAR in (a, b), and (C2) is linear,
so every equation has the shape

      e(a, b) = const + sum_m alpha_m a_m + sum_n beta_n b_n
                      + sum_{m,n} c_{mn} a_m b_n .

Those coefficients are extracted once symbolically.  Then for each of the
2^9 = 512 choices of a the whole system becomes an AFFINE LINEAR system in the
13 unknowns b over F_2, solved exactly by Gaussian elimination.  This is an
exhaustive search of all 2^22 = 4194304 points -- every point of F_2^22 is
covered, none is sampled -- carried out in 512 linear solves.

CONTROL: the identical routine is run on the E0 support, where it must return
the 8 points already enumerated by brute force in night8/verify_lift.py.

MEASUREMENTS ONLY.
"""
import itertools
import json
import sys

import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar/night8')
from mondello_lift import System, S_P0, S_Q0, rref2, rank2, nullspace2  # noqa


def bilinear_data(S):
    """const, alpha, beta, C for every equation of the system S, mod 2."""
    na, nb = len(S.avars), len(S.bvars)
    zero = {v: 0 for v in S.vars}
    data = []
    for e in S.eqs:
        const = int(e.subs(zero)) % 2
        alpha = [int(sp.diff(e, v).subs(zero)) % 2 for v in S.avars]
        beta = [int(sp.diff(e, v).subs(zero)) % 2 for v in S.bvars]
        C = [[int(sp.diff(e, va, vb)) % 2 for vb in S.bvars] for va in S.avars]
        data.append((const, alpha, beta, C))
    return data, na, nb


def solve_all(A, rhs, nb):
    """All b with A b = rhs over F_2 (A a list of rows), or None."""
    aug = [list(A[i]) + [rhs[i]] for i in range(len(A))]
    rk = rank2([r[:nb] for r in aug], nb)
    if rank2(aug, nb + 1) != rk:
        return None
    R, piv = rref2(aug, nb + 1)
    part = [0] * nb
    for r_, c in enumerate(piv):
        if c < nb:
            part[c] = R[r_][nb]
    ker = nullspace2([r[:nb] for r in aug], nb)
    sols = []
    for co in itertools.product((0, 1), repeat=len(ker)):
        d = list(part)
        for c, kv in zip(co, ker):
            if c:
                d = [(p + q) % 2 for p, q in zip(d, kv)]
        sols.append(tuple(d))
    return sols


def enumerate_points(SP, SQ, label):
    S = System(SP, SQ, label)
    data, na, nb = bilinear_data(S)
    pts = []
    n_consistent = 0
    for abits in itertools.product((0, 1), repeat=na):
        rows, rhs = [], []
        for (const, alpha, beta, C) in data:
            row = list(beta)
            c0 = const
            for m in range(na):
                if abits[m]:
                    c0 ^= alpha[m]
                    row = [(row[n] ^ C[m][n]) for n in range(nb)]
            rows.append(row)
            rhs.append(c0)          # row.b + c0 = 0  =>  row.b = c0 (mod 2)
        sols = solve_all(rows, rhs, nb)
        if sols is None:
            continue
        n_consistent += 1
        for b in sols:
            pts.append(tuple(list(abits) + list(b)))
    return S, pts, n_consistent


if __name__ == '__main__':
    out = {}

    # ---- CONTROL on E0 -----------------------------------------------------
    S0, pts0, nc0 = enumerate_points(S_P0, S_Q0, 'E0')
    f0 = sp.lambdify(S0.vars, S0.eqs, modules='math')
    ok0 = all(all(v % 2 == 0 for v in f0(*p)) for p in pts0)
    brute = {tuple(p) for p in json.load(
        open('/home/user/jacobian_planar/night8/verify_lift.json')
    )['brute_force_mod2']['solutions']}
    out['control_E0'] = {
        'n_points': len(pts0),
        'every_point_satisfies_the_system': bool(ok0),
        'matches_brute_force_enumeration': (set(pts0) == brute),
        'n_a_vectors_with_a_consistent_linear_system': nc0,
    }
    print('CONTROL E0: %d points, all satisfy the system: %s, matches the '
          'brute-force set: %s' % (len(pts0), ok0, set(pts0) == brute))
    if not (ok0 and set(pts0) == brute and len(pts0) == 8):
        sys.exit(6)

    # ---- E1 ----------------------------------------------------------------
    from mondello_lift import hull_lattice_points
    HP = hull_lattice_points(S_P0)
    HQ = hull_lattice_points(S_Q0)
    S1, pts1, nc1 = enumerate_points(HP, HQ, 'E1')
    f1 = sp.lambdify(S1.vars, S1.eqs, modules='math')
    ok1 = all(all(v % 2 == 0 for v in f1(*p)) for p in pts1)
    out['E1'] = {
        'support_P': [list(m) for m in HP],
        'support_Q': [list(m) for m in HQ],
        'n_unknowns': len(S1.vars),
        'variable_names': [str(v) for v in S1.vars],
        'search_space': 2 ** len(S1.vars),
        'n_a_vectors_tried': 2 ** len(S1.avars),
        'n_a_vectors_with_a_consistent_linear_system': nc1,
        'n_F2_points': len(pts1),
        'every_point_satisfies_the_system': bool(ok1),
        'points': [list(p) for p in pts1],
    }
    print('E1: search space 2^%d = %d; %d of the %d a-vectors give a '
          'consistent linear system; %d F_2 points in total; all verified: %s'
          % (len(S1.vars), 2 ** len(S1.vars), nc1, 2 ** len(S1.avars),
             len(pts1), ok1))
    json.dump(out, open('/home/user/jacobian_planar/night8/e1_points.json',
                        'w'), indent=1)
    print('written night8/e1_points.json')
