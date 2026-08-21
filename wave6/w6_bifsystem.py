#!/usr/bin/env python3
"""FIRST-ORDER BIFURCATION SYSTEM -- solve for the degenerate point directly.

Because mu0 enters the GGV system linearly and in exactly ONE term, the whole
system splits as
        F(p, mu0)  =  F0(p) + mu0 * G(p)
with G = dF/dmu0 (a fixed vector of polynomials).  A counterexample branch
sprouts off the mu0 = 0 locus at a point p exactly when the mu0-direction is
in the image of the linearisation there, i.e. when

        F0(p) = 0     AND     J(p) v = G(p)   is solvable for v.

So instead of hunting for such a p by luck, SOLVE for it: treat (p, v) as
unknowns and solve the augmented square-ish system

        F0(p) = 0,        J(p) v - G(p) = 0.

A solution is a first-order counterexample seed: Newton from (p + eps*v,
mu0 = eps) then either converges to a genuine solution (-> CANDIDATE, verify
exactly) or shows the obstruction returns at higher order.

CONTROL (mathematical, decisive): at d=3 the obstruction is exactly 6*mu0,
constant along the family, so the augmented system MUST be infeasible --
best residual must stay far from zero.  If d=3 reports a bifurcation point,
the code is wrong.

Usage: python3 w6_bifsystem.py MODE [nstarts]
   MODE: b3 (control) | b12r (seed -1/12) | b12s (seed 1/20) | b13 | dNN
"""
import sys, os, json, time
import numpy as np
from scipy.optimize import least_squares

ROOT = '/home/user/jacobian_planar'
sys.path.insert(0, os.path.join(ROOT, 'wave5'))
os.chdir(os.path.join(ROOT, 'wave5'))
import sympy as sp
from sympy import symbols, expand, Symbol, Rational
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3

def split_system(d, seed=None):
    """Return (F0, G, vars) with F(p,mu0) = F0(p) + mu0*G(p)."""
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    subs = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
            mu1: -mu3*a[2]/3}
    if seed is not None:
        subs[a[2*d]] = seed
    core = [expand(e.subs(subs)) for e in eqs]
    core = [e for e in core if e != 0]
    vars_ = [a[i] for i in range(2, 2*d+1) if not (seed is not None and i == 2*d)]
    vars_ += [b[i] for i in range(2, d)] + [mu2, mu3]
    F0, G = [], []
    for e in core:
        p = sp.Poly(e, mu0)
        cd = p.all_coeffs()          # highest degree first
        deg = p.degree()
        if deg > 1:
            raise RuntimeError(f'mu0 appears with degree {deg} -- split invalid')
        g = cd[0] if deg == 1 else sp.Integer(0)
        f0 = expand(e.subs(mu0, 0))
        F0.append(f0); G.append(sp.expand(g))
    return F0, G, vars_

def build_callables(F0, G, vars_):
    n = len(vars_)
    J = sp.Matrix(F0).jacobian(sp.Matrix(vars_))
    f0f = sp.lambdify(vars_, F0, modules='numpy')
    gf = sp.lambdify(vars_, G, modules='numpy')
    jf = sp.lambdify(vars_, J, modules='numpy')
    return f0f, gf, jf, n

def make_bif_res(f0f, gf, jf, n, m):
    """Unknowns x = [Re p, Im p, Re v, Im v]; residual = [F0(p), J(p)v - G(p)]."""
    def res(x):
        p = x[:n] + 1j*x[n:2*n]
        v = x[2*n:3*n] + 1j*x[3*n:]
        f0 = np.asarray(f0f(*p), dtype=complex).reshape(-1)
        g = np.asarray(gf(*p), dtype=complex).reshape(-1)
        Jm = np.asarray(jf(*p), dtype=complex).reshape(m, n)
        r2 = Jm.dot(v) - g
        out = np.concatenate([f0, r2])
        return np.concatenate([out.real, out.imag])
    return res

if __name__ == '__main__':
    mode = sys.argv[1]
    nstarts = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    d, seed = 3, None
    if mode == 'b12r': d, seed = 12, Rational(-1, 12)
    if mode == 'b12s': d, seed = 12, Rational(1, 20)
    if mode == 'b13':  d, seed = 13, None
    if mode.startswith('d') and mode[1:].isdigit(): d, seed = int(mode[1:]), None

    t0 = time.time()
    F0, G, vars_ = split_system(d, seed)
    m = len(F0)
    f0f, gf, jf, n = build_callables(F0, G, vars_)
    print(json.dumps({'mode': mode, 'd': d, 'eqs': m, 'vars': n,
                      'unknowns_real': 4*n, 'residuals_real': 4*m,
                      'build_secs': round(time.time()-t0, 1)}), flush=True)

    res = make_bif_res(f0f, gf, jf, n, m)
    rng = np.random.default_rng(2718)
    best, bestx = np.inf, None
    hits = []
    for k in range(nstarts):
        x0 = rng.normal(0, 1.0, 4*n)
        try:
            r = least_squares(res, x0, method='lm', max_nfev=6000)
        except Exception as e:
            continue
        c = float(np.sum(r.fun**2))
        if c < best:
            best, bestx = c, r.x
            print(json.dumps({'mode': mode, 'start': k, 'best_residual2': best,
                              'elapsed': round(time.time()-t0, 1)}), flush=True)
        if c < 1e-16:
            rec = {'mode': mode, 'BIFURCATION-POINT-FOUND': True, 'residual2': c,
                   'p_re': list(r.x[:n]), 'p_im': list(r.x[n:2*n]),
                   'v_re': list(r.x[2*n:3*n]), 'v_im': list(r.x[3*n:]),
                   'vars': [str(v) for v in vars_]}
            print(json.dumps(rec), flush=True)
            hits.append(rec)
            break
    summary = {'mode': mode, 'nstarts': nstarts, 'best_residual2': best,
               'bifurcation_points': len(hits)}
    json.dump({'summary': summary, 'hits': hits},
              open(f'{ROOT}/wave6/bifsystem_{mode}.json', 'w'), indent=1)
    print(json.dumps(summary))
