#!/usr/bin/env python3
"""NUMERICAL mu0-WALK (homotopy continuation) -- the bifurcation program made
executable without any Groebner basis.

Idea: the degenerate structure of the GGV cells lives at mu0 = 0.  A
counterexample needs mu0 != 0.  So: find a mu0 = 0 point numerically, then
TRACK it as mu0 is increased continuously from 0.  Each step is a Newton
correction (one linear solve, milliseconds, fixed memory).  If the path
survives to mu0 = eps != 0 with residual ~ 0, that point is a counterexample
seed; if the path breaks (residual blows up / Jacobian degenerates), the
family is obstructed in the mu0 direction -- the local certificate the
descent-closure argument needs.

Nobody has applied homotopy continuation to the GGV system; it is the
standard tool of numerical algebraic geometry (Bertini / HomotopyContinuation.jl)
and it is immune to the memory wall that kills exact elimination here.

CONTROLS (both must pass before any walk result is believed):
  W0 TRACKER control (synthetic): a path that provably exists must be
     tracked -- x^2+y^2-(1+s)=0 walked from s=0 to s=1.
  W1 NEGATIVE control (mathematical): at d=3 the mu0=0 family EXISTS but the
     mu0!=0 cell is PROVEN EMPTY (GGV).  So every walk from a d=3 family
     point MUST break.  A "successful" d=3 walk means the code is wrong.

Usage: python3 w6_mu0walk.py MODE [nstarts]
  MODE: w0 | w1 | d12r (seed -1/12) | d12s (seed 1/20) | d13
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

S = Symbol('s_param')

def cell_system(d, seed=None):
    """Core equations with mu0 replaced by the walk parameter s_param."""
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    subs = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
            mu1: -mu3*(a[2] + 2*b[2])/3, mu0: S}
    if seed is not None:
        subs[a[2*d]] = seed
    core = [expand(e.subs(subs)) for e in eqs]
    core = [e for e in core if e != 0]
    vars_ = [a[i] for i in range(2, 2*d+1) if not (seed is not None and i == 2*d)]
    vars_ += [b[i] for i in range(2, d)] + [mu2, mu3]
    return core, vars_

def make_res(core, vars_):
    n = len(vars_)
    F = sp.lambdify(list(vars_) + [S], core, modules='numpy')
    def res(x, s):
        z = x[:n] + 1j*x[n:]
        v = np.asarray(F(*z, s), dtype=complex)
        return np.concatenate([v.real, v.imag])
    return res, n

def find_seed_points(res, n, nstarts, rng, tol=1e-18):
    """Multi-start solve at s=0 -- the mu0=0 (degenerate) locus."""
    pts = []
    for k in range(nstarts):
        x0 = rng.normal(0, 1.0, 2*n)
        try:
            r = least_squares(lambda x: res(x, 0.0), x0, method='lm', max_nfev=4000)
        except Exception:
            continue
        c = float(np.sum(r.fun**2))
        if c < tol:
            pts.append((c, r.x))
    return pts

def walk(res, n, x0, smax=1.0, nsteps=60, tol=1e-16):
    """Track the point as s goes 0 -> smax.  Returns (reached_s, residual)."""
    x = x0.copy()
    reached = 0.0
    for i in range(1, nsteps + 1):
        s = smax * i / nsteps
        try:
            r = least_squares(lambda z: res(z, s), x, method='lm', max_nfev=2000)
        except Exception:
            return reached, np.inf
        c = float(np.sum(r.fun**2))
        if c > tol:
            return reached, c          # path broke here: obstruction
        x = r.x
        reached = s
    return reached, float(np.sum(res(x, smax)**2))

def w0_control():
    """Synthetic tracker control: x^2+y^2-(1+s)=0 must track s: 0 -> 1."""
    # square system (LM needs #residuals >= #unknowns):
    #   z0^2 + z1^2 = 1 + s,  z0 = z1   ->  z0 = z1 = sqrt((1+s)/2)
    def res(x, s):
        z = x[:2] + 1j*x[2:]
        v = np.array([z[0]**2 + z[1]**2 - (1.0 + s), z[0] - z[1]], dtype=complex)
        return np.concatenate([v.real, v.imag])
    r0 = np.sqrt(0.5)
    x0 = np.array([r0, r0, 0.0, 0.0])
    reached, c = walk(res, 2, x0, smax=1.0, nsteps=20)
    ok = reached >= 0.999 and c < 1e-16
    print(json.dumps({'control': 'W0-tracker', 'PASS': bool(ok),
                      'reached_s': reached, 'residual2': c}))
    return ok

if __name__ == '__main__':
    mode = sys.argv[1]
    nstarts = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    rng = np.random.default_rng(12345)

    if mode == 'w0':
        sys.exit(0 if w0_control() else 1)

    if not w0_control():
        print('TRACKER CONTROL FAILED -- refusing to run walks'); sys.exit(1)

    d, seed = (3, None)
    if mode == 'w1':   d, seed = 3, None
    if mode == 'd12r': d, seed = 12, Rational(-1, 12)
    if mode == 'd12s': d, seed = 12, Rational(1, 20)
    if mode == 'd13':  d, seed = 13, None
    if mode.startswith('d') and mode[1:].isdigit():
        d, seed = int(mode[1:]), None

    core, vars_ = cell_system(d, seed)
    res, n = make_res(core, vars_)
    print(json.dumps({'mode': mode, 'd': d, 'eqs': len(core), 'vars': n}), flush=True)

    t0 = time.time()
    pts = find_seed_points(res, n, nstarts, rng)
    print(json.dumps({'mode': mode, 'mu0_zero_points_found': len(pts),
                      'elapsed': round(time.time()-t0, 1)}), flush=True)
    if not pts:
        print(json.dumps({'mode': mode, 'result': 'NO-DEGENERATE-POINTS',
                          'note': 'nothing to walk from at this size/starts'}))
        sys.exit(0)

    out = []
    for j, (c0, x0) in enumerate(sorted(pts, key=lambda t: t[0])[:12]):
        best_reached = 0.0
        for smax in (1e-3, 1e-2, 1e-1, 1.0):
            reached, cend = walk(res, n, x0, smax=smax, nsteps=40)
            best_reached = max(best_reached, reached)
            rec = {'mode': mode, 'point': j, 'seed_residual2': c0,
                   'smax': smax, 'reached_mu0': reached, 'end_residual2': cend}
            if reached >= smax * 0.999 and cend < 1e-16:
                rec['WALK-SUCCESS'] = True
                rec['point_re'] = list(x0[:n]); rec['point_im'] = list(x0[n:])
                rec['vars'] = [str(v) for v in vars_]
                print(json.dumps(rec), flush=True)
                out.append(rec)
                break
            print(json.dumps(rec), flush=True)
            out.append(rec)
            break   # first break tells us the obstruction scale
    json.dump(out, open(f'{ROOT}/wave6/mu0walk_{mode}.json', 'w'), indent=1)
    succ = [r for r in out if r.get('WALK-SUCCESS')]
    print(json.dumps({'mode': mode, 'walks': len(out), 'successes': len(succ),
                      'max_reached_mu0': max((r['reached_mu0'] for r in out), default=0.0)}))
