#!/usr/bin/env python3
"""NUMERICAL HUNT (new lane, thinking pass 4): Gauss-Newton multi-start on
the GGV cell systems in CHAR 0 -- the systems that resist exact Groebner.

Rationale: finding a point needs no basis.  scipy least_squares over
C^n (split into R^{2n}) at ~ms/iteration, thousands of starts.  A residual
converging to ~1e-25 = numerical solution -> exact lift (LLL / p-adic) ->
GGV Sec 2 construction -> counterexample.  Persistent floor = evidence of
emptiness (not proof) directing the exact budget.

CONTROLS (must pass before any hunt result is reported):
  C1 d=3, mu0=0, unsaturated: the degenerate family EXISTS
     (q1=y^3+mu3, A=-q1^2/4) -> some start MUST reach residual < 1e-18.
  C2 d=3, saturated chart N: proven EMPTY -> best residual over all starts
     MUST stay > 1e-10 (a convergence here means the method lies).

Usage: python3 w6_numhunt.py MODE NSTARTS  (MODE: c1, c2, d12N_r (seed -1/12),
       d12N_s (seed 1/20), d13N)
Streams results to wave6/numhunt_<mode>.json; prints CANDIDATE-NUMERIC
immediately on any residual < 1e-16 with the full point.
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

def chart_system(d, seed=None, mu0_zero=False, saturate=True):
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    subs = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
            mu1: -mu3*(a[2] + 2*b[2])/3}
    if mu0_zero:
        subs[mu0] = 0
    if seed is not None:
        subs[a[2*d]] = seed
    core = [expand(e.subs(subs)) for e in eqs]
    core = [e for e in core if e != 0]
    vars_ = [a[i] for i in range(2, 2*d+1) if not (seed is not None and i == 2*d)]
    vars_ += [b[i] for i in range(2, d)] + [mu2, mu3]
    if not mu0_zero:
        vars_.append(mu0)
        if saturate:
            t = Symbol('t'); vars_.append(t)
            core.append(expand(t*mu0 - 1))
    return core, vars_

def make_resfun(core, vars_):
    n = len(vars_)
    F = sp.lambdify(vars_, core, modules='numpy')
    def res(x):
        z = x[:n] + 1j*x[n:]
        v = np.asarray(F(*z), dtype=complex)
        return np.concatenate([v.real, v.imag])
    return res, n

def hunt(core, vars_, nstarts, scale=1.0, seed0=0, tag='', fastexit=None):
    res, n = make_resfun(core, vars_)
    rng = np.random.default_rng(seed0)
    best = np.inf; bestx = None; hits = []
    t0 = time.time()
    for k in range(nstarts):
        x0 = rng.normal(0, scale, 2*n)
        try:
            r = least_squares(res, x0, method='lm', max_nfev=4000)
        except Exception:
            continue
        c = float(np.sum(r.fun**2))
        if c < best:
            best = c; bestx = r.x
            print(json.dumps({'tag': tag, 'start': k, 'best_residual2': best,
                              'elapsed': round(time.time()-t0, 1)}), flush=True)
        if c < 1e-16:
            pt = {'tag': tag, 'CANDIDATE-NUMERIC': True, 'residual2': c,
                  'point_re': list(r.x[:n]), 'point_im': list(r.x[n:]),
                  'vars': [str(v) for v in vars_]}
            print(json.dumps(pt), flush=True)
            hits.append(pt)
            if fastexit:
                break
    return {'tag': tag, 'nstarts': nstarts, 'best_residual2': best,
            'nhits': len(hits), 'hits': hits[:3],
            'best_point': list(bestx) if bestx is not None else None}

if __name__ == '__main__':
    mode = sys.argv[1]; nstarts = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    if mode == 'c1':
        core, v = chart_system(3, mu0_zero=True, saturate=False)
        out = hunt(core, v, nstarts, tag='C1-d3-family-must-hit', fastexit=True)
        ok = out['nhits'] > 0
        print(json.dumps({'control': 'C1', 'PASS': ok, 'best': out['best_residual2']}))
    elif mode == 'c2':
        core, v = chart_system(3)
        out = hunt(core, v, nstarts, tag='C2-d3-empty-must-floor')
        ok = out['best_residual2'] > 1e-10
        print(json.dumps({'control': 'C2', 'PASS': ok, 'best': out['best_residual2']}))
    else:
        d = 13 if mode == 'd13N' else 12
        if mode.startswith('d') and mode[1:].isdigit():
            d = int(mode[1:])
        seed = None
        if mode == 'd12N_r': seed = Rational(-1, 12)
        if mode == 'd12N_s': seed = Rational(1, 20)
        core, v = chart_system(d, seed=seed)
        out = hunt(core, v, nstarts, tag=mode)
        json.dump(out, open(f'{ROOT}/wave6/numhunt_{mode}.json', 'w'), indent=1)
        print(json.dumps({'mode': mode, 'best': out['best_residual2'], 'nhits': out['nhits']}))
