#!/usr/bin/env python3
"""
night8/mondello_lift.py

Deformation space (char 2) and 2-adic lift obstruction measurements for the
extracted pair of night5/mondello/ (arXiv 2608.02634, Theorem 1.2):

    P(x,y) = x + x^2 y + x^4 + x^6 y^2
    Q(x,y) = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3      over F_2

MEASUREMENTS ONLY.  Nothing in this file interprets a result.

Unknowns: the coefficients a_m (m in support E_P) of P and b_n (n in E_Q) of Q.
System:
  (K)  every coefficient of  P_x Q_y - P_y Q_x - 1  vanishes
  (C2) P(0,1) - P(1,0) = 0   and   Q(0,1) - Q(1,0) = 0
       (collision POINTS fixed at (0,1),(1,0); the coefficients are unknown)

Everything is built once over Z with sympy; the char-2 system is the mod-2
reduction of the same expressions, so reduction and differentiation commute
and one code path serves STEP 1 and STEP 2/3.
"""
import itertools
import json
import sys
import time
from fractions import Fraction

import sympy as sp

x, y = sp.symbols('x y')

S_P0 = [(1, 0), (2, 1), (4, 0), (6, 2)]
S_Q0 = [(0, 1), (5, 0), (6, 1), (7, 2), (8, 3)]


# ---------------------------------------------------------------- hulls -----
def hull_lattice_points(pts):
    """All integer points of the convex hull of pts (2-D, exact rational)."""
    pts = sorted(set(pts))
    if len(pts) == 1:
        return list(pts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    out = []
    for i in range(min(xs), max(xs) + 1):
        for j in range(min(ys), max(ys) + 1):
            if in_hull((i, j), pts):
                out.append((i, j))
    return sorted(out)


def in_hull(p, pts):
    """Is p in conv(pts)?  Exact LP-free test via convex-hull edges (2-D)."""
    H = convex_hull(pts)
    if len(H) == 1:
        return p == H[0]
    if len(H) == 2:
        a, b = H
        cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cr != 0:
            return False
        return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
                min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))
    n = len(H)
    for k in range(n):
        a, b = H[k], H[(k + 1) % n]
        cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cr < 0:
            return False
    return True


def convex_hull(pts):
    """Counter-clockwise convex hull (Andrew monotone chain), exact ints."""
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return list(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


# ------------------------------------------------------------- systems ------
class System:
    def __init__(self, SP, SQ, name):
        self.name = name
        self.SP = list(SP)
        self.SQ = list(SQ)
        self.avars = [sp.Symbol('a_%d_%d' % m) for m in self.SP]
        self.bvars = [sp.Symbol('b_%d_%d' % n) for n in self.SQ]
        self.vars = self.avars + self.bvars
        P = sum(c * x ** m[0] * y ** m[1] for c, m in zip(self.avars, self.SP))
        Q = sum(c * x ** n[0] * y ** n[1] for c, n in zip(self.bvars, self.SQ))
        self.P, self.Q = P, Q
        D = sp.expand(sp.diff(P, x) * sp.diff(Q, y)
                      - sp.diff(P, y) * sp.diff(Q, x) - 1)
        pol = sp.Poly(D, x, y)
        self.K_monoms = []
        self.eqs = []
        for mon, coeff in pol.terms():
            self.K_monoms.append(tuple(mon))
            self.eqs.append(sp.expand(coeff))
        self.n_K = len(self.eqs)
        # (C2): the two collision equations, points fixed at (0,1) and (1,0)
        sub01 = {x: 0, y: 1}
        sub10 = {x: 1, y: 0}
        self.eqs.append(sp.expand(P.subs(sub01) - P.subs(sub10)))
        self.eqs.append(sp.expand(Q.subs(sub01) - Q.subs(sub10)))
        self.labels = (['K%s' % (m,) for m in self.K_monoms]
                       + ['C2_P', 'C2_Q'])
        # base point: coefficient 1 on the extracted support, 0 elsewhere
        self.base = {}
        for c, m in zip(self.avars, self.SP):
            self.base[c] = 1 if m in S_P0 else 0
        for c, n in zip(self.bvars, self.SQ):
            self.base[c] = 1 if n in S_Q0 else 0
        # integer Jacobian at the base point
        self.J = [[int(sp.diff(e, v).subs(self.base)) for v in self.vars]
                  for e in self.eqs]
        self.residual = [int(e.subs(self.base)) for e in self.eqs]

    def eval_at(self, point):
        """point: dict var -> int.  Returns integer residual vector."""
        return [int(e.subs(point)) for e in self.eqs]


# --------------------------------------------------- linear algebra mod 2 ---
def rref2(rows, ncols):
    """Returns (R, pivots) reduced row echelon form over F_2."""
    R = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(R)):
            if R[i][c] & 1:
                pr = i
                break
        if pr is None:
            continue
        R[r], R[pr] = R[pr], R[r]
        for i in range(len(R)):
            if i != r and (R[i][c] & 1):
                R[i] = [(u ^ v) & 1 for u, v in zip(R[i], R[r])]
        piv.append(c)
        r += 1
        if r == len(R):
            break
    return R, piv


def rank2(rows, ncols):
    return len(rref2(rows, ncols)[1])


def solve2(A, b):
    """Solve A z = b over F_2.  Returns (solution list or None, nullity)."""
    m = len(A)
    n = len(A[0]) if m else 0
    aug = [[v & 1 for v in A[i]] + [b[i] & 1] for i in range(m)]
    R, piv = rref2(aug, n + 1)
    if (n) in piv:           # pivot in the augmented column => inconsistent
        return None, None
    nullity = n - len(piv)
    z = [0] * n
    for r, c in enumerate(piv):
        z[c] = R[r][n]
    return z, nullity


def nullspace2(A, n):
    R, piv = rref2(A, n)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n
        v[f] = 1
        for r, c in enumerate(piv):
            v[c] = R[r][f]
        basis.append(v)
    return basis


# ------------------------------------------------------------------ run -----
def main():
    out = {}
    log = []

    def say(s):
        print(s)
        log.append(s)

    # ---------------- supports ----------------
    hullP = hull_lattice_points(S_P0)
    hullQ = hull_lattice_points(S_Q0)
    out['supports'] = {
        'E0_P': S_P0, 'E0_Q': S_Q0,
        'E0_sizes': [len(S_P0), len(S_Q0)],
        'E1_P': hullP, 'E1_Q': hullQ,
        'E1_sizes': [len(hullP), len(hullQ)],
        'hull_vertices_P': convex_hull(S_P0),
        'hull_vertices_Q': convex_hull(S_Q0),
    }
    say('E0 support sizes: |S_P|=%d |S_Q|=%d  (unknowns %d)'
        % (len(S_P0), len(S_Q0), len(S_P0) + len(S_Q0)))
    say('E1 hull lattice sizes: |S_P|=%d |S_Q|=%d  (unknowns %d)'
        % (len(hullP), len(hullQ), len(hullP) + len(hullQ)))

    systems = {'E0': System(S_P0, S_Q0, 'E0'),
               'E1': System(hullP, hullQ, 'E1')}

    # ---------------- WITNESS CONTROL ----------------
    say('')
    say('=== WITNESS CONTROL (base point satisfies the F_2 system) ===')
    out['witness_control'] = {}
    for nm, S in systems.items():
        res2 = [r % 2 for r in S.residual]
        bad = [(S.labels[i], S.residual[i]) for i, v in enumerate(res2) if v]
        out['witness_control'][nm] = {
            'n_equations': len(S.eqs),
            'n_K_equations': S.n_K,
            'n_unknowns': len(S.vars),
            'residual_mod2_all_zero': not bad,
            'failures': bad,
            'integer_residual_nonzero_entries':
                {S.labels[i]: S.residual[i]
                 for i in range(len(S.eqs)) if S.residual[i] != 0},
        }
        say('%s: %d equations (%d from K, 2 from C2), %d unknowns; '
            'base residual mod 2 all zero: %s'
            % (nm, len(S.eqs), S.n_K, len(S.vars), not bad))
        if bad:
            say('WITNESS CONTROL FAILED for %s: %r' % (nm, bad))
            json.dump(out, open(OUT_JSON, 'w'), indent=1)
            sys.exit(2)
    say('WITNESS CONTROL PASSED for E0 and E1.')

    # ---------------- STEP 1: tangent space over F_2 ----------------
    say('')
    say('=== STEP 1: Jacobian of (K)+(C2) at the base point over F_2 ===')
    out['step1'] = {}
    for nm, S in systems.items():
        J2 = [[v % 2 for v in row] for row in S.J]
        n = len(S.vars)
        r = rank2(J2, n)
        zero_rows = [S.labels[i] for i, row in enumerate(J2) if not any(row)]
        out['step1'][nm] = {
            'n_unknowns': n,
            'n_equations': len(J2),
            'rank_mod2': r,
            'nullity_mod2': n - r,
            'n_identically_zero_rows_mod2': len(zero_rows),
            'zero_rows_mod2': zero_rows,
        }
        say('%s: unknowns=%d equations=%d  rank(J mod 2)=%d  nullity=%d  '
            '(zero rows mod 2: %d)'
            % (nm, n, len(J2), r, n - r, len(zero_rows)))
        S.J2 = J2

    # Groebner over GF(2) for E0
    say('')
    say('--- STEP 1b: Groebner basis of the E0 ideal over GF(2) ---')
    S0 = systems['E0']
    gb_rec = {'attempted': True, 'timeout_s': 600}
    t0 = time.time()
    import signal

    def _alarm(signum, frame):
        raise TimeoutError('groebner exceeded 600s')

    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(600)
    try:
        gb = sp.groebner(S0.eqs, *S0.vars, order='grevlex', modulus=2)
        el = time.time() - t0
        lead = [sp.Poly(g, *S0.vars, modulus=2).LM(order='grevlex')
                for g in gb.exprs]
        lead_exp = [tuple(int(e) for e in m.exponents) for m in lead]
        pure = set()
        for e in lead_exp:
            nz = [i for i, v in enumerate(e) if v]
            if len(nz) == 1:
                pure.add(nz[0])
        gb_rec.update({
            'status': 'COMPLETED',
            'elapsed_s': round(el, 2),
            'n_basis_elements': len(gb.exprs),
            'basis': [str(g) for g in gb.exprs],
            'leading_exponents': [list(e) for e in lead_exp],
            'vars': [str(v) for v in S0.vars],
            'variables_with_pure_power_leading_term':
                sorted(str(S0.vars[i]) for i in pure),
            'quotient_finite_dimensional_over_GF2bar':
                len(pure) == len(S0.vars),
        })
        say('Groebner (GF(2), grevlex) COMPLETED in %.2fs; %d basis elements'
            % (el, len(gb.exprs)))
        say('  variables with a pure-power leading term: %d of %d'
            % (len(pure), len(S0.vars)))
        say('  Krull dimension of the ideal is 0 iff that count is full: %s'
            % (len(pure) == len(S0.vars)))
    except TimeoutError as exc:
        gb_rec.update({'status': 'TIMEOUT', 'error': str(exc),
                       'elapsed_s': round(time.time() - t0, 2)})
        say('Groebner TIMEOUT after %.0fs (TIMEOUT is a recorded outcome)'
            % (time.time() - t0))
    except Exception as exc:                                   # noqa: BLE001
        gb_rec.update({'status': 'ERROR', 'error': repr(exc)[:400],
                       'elapsed_s': round(time.time() - t0, 2)})
        say('Groebner ERROR: %r' % (exc,))
    finally:
        signal.alarm(0)
    out['step1_groebner_E0'] = gb_rec

    # ---------------- STEP 2/3: 2-adic lifting on E0 ----------------
    say('')
    say('=== STEP 2: integral system on E0, smoothness mod 2 at the base ===')
    S = systems['E0']
    n = len(S.vars)
    M = len(S.eqs)
    J2 = S.J2
    r = rank2(J2, n)
    smooth = (r == n)
    out['step2'] = {
        'n_unknowns': n,
        'n_equations': M,
        'rank_J_mod2': r,
        'corank_in_unknowns': n - r,
        'full_unknown_rank_odd_minor_exists': smooth,
        'smooth_mod2_point_of_integral_system': smooth,
        'equations_with_vanishing_gradient_mod2':
            [S.labels[i] for i, row in enumerate(J2) if not any(row)],
        'integer_residual_at_base':
            {S.labels[i]: S.residual[i] for i in range(M)
             if S.residual[i] != 0},
        'all_residuals_even': all(v % 2 == 0 for v in S.residual),
        'J_mod2': J2,
        'equation_labels': S.labels,
        'variable_names': [str(v) for v in S.vars],
    }
    say('unknowns N=%d, equations M=%d, rank(J mod 2)=%d, corank=%d'
        % (n, M, r, n - r))
    say('square minor of size N=%d that is odd exists: %s' % (n, smooth))
    say('all integer residuals at the base even: %s'
        % all(v % 2 == 0 for v in S.residual))
    if not all(v % 2 == 0 for v in S.residual):
        say('HARD EXIT: base point is not a mod-2 solution of the integral '
            'system.')
        json.dump(out, open(OUT_JSON, 'w'), indent=1)
        sys.exit(3)

    # Hensel iteration.  x_{k+1} = x_k + 2^k d,  r(x_k) = 2^k s_k,
    # r is quadratic so r(x_k + 2^k d) = r(x_k) + 2^k J d + 2^{2k} B(d,d);
    # for k >= 1, 2^{2k} = 0 mod 2^{k+1}, so the condition mod 2^{k+1} is
    #     s_k + J(x_k) d = 0  (mod 2),  and J(x_k) = J(x_0) mod 2.
    say('')
    say('=== STEP 2/3: 2-adic lifting of the base point on E0 ===')
    point = dict(S.base)
    levels = []
    ok = True
    for k in range(1, 5):          # produce solutions mod 4, 8, 16 (stop at 16)
        mod_from, mod_to = 2 ** k, 2 ** (k + 1)
        res = S.eval_at(point)
        assert all(v % mod_from == 0 for v in res), (k, res)
        s = [(v // mod_from) % 2 for v in res]
        d, nullity = solve2(J2, s)      # J d = s (mod 2); -s = s over F_2
        rec = {'level_from': mod_from, 'level_to': mod_to,
               'rhs_s_mod2': s,
               'rhs_nonzero_positions': [S.labels[i] for i, v in enumerate(s)
                                         if v]}
        if d is None:
            rec.update({'exists': 'DOES-NOT-EXIST',
                        'reason': 'J*delta = s (mod 2) inconsistent: '
                                  's is not in the column space of J mod 2',
                        'rank_J_mod2': r,
                        'rank_augmented_mod2':
                            rank2([J2[i] + [s[i]] for i in range(M)], n + 1)})
            say('mod %d: DOES-NOT-EXIST (linear system inconsistent mod 2)'
                % mod_to)
            levels.append(rec)
            ok = False
            break
        rec.update({'exists': 'EXISTS',
                    'particular_delta': d,
                    'solution_space_dim_of_linear_step': nullity,
                    'rank_J_mod2': r})
        say('mod %d: EXISTS; linear step solution space dimension = %d'
            % (mod_to, nullity))
        for i, v in enumerate(S.vars):
            point[v] = point[v] + mod_from * d[i]
        res_new = S.eval_at(point)
        good = all(v % mod_to == 0 for v in res_new)
        rec['verified_residual_zero_mod_%d' % mod_to] = good
        rec['lifted_point'] = {str(v): int(point[v]) % mod_to
                               for v in S.vars}
        say('   verified: all residuals = 0 mod %d: %s' % (mod_to, good))
        if not good:
            ok = False
            levels.append(rec)
            break
        levels.append(rec)
        if mod_to == 16:
            break
    out['step3_lift_levels'] = levels
    out['lift_summary'] = {
        ('mod%d' % L['level_to']): L['exists'] for L in levels}
    out['lift_reached'] = max([L['level_to'] for L in levels
                               if L['exists'] == 'EXISTS'], default=2)
    out['log'] = log
    json.dump(out, open(OUT_JSON, 'w'), indent=1, default=str)
    say('')
    say('JSON written to %s' % OUT_JSON)
    return 0


OUT_JSON = '/home/user/jacobian_planar/night8/mondello_lift.json'

if __name__ == '__main__':
    sys.exit(main())
