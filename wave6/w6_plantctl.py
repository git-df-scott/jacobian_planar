#!/usr/bin/env python3
"""SIZE-MATCHED PLANTED-ROOT CONTROL for the numerical ladder hunts.

The C1/C2 controls were run only at d=3 (8 unknowns).  The hunts that produced
tonight's "empty floor" readings ran at d=8..13 (20-40 unknowns).  If
multi-start Newton loses power with dimension -- as it demonstrably does at
165 unknowns (pentagon P-POS control failed) -- then those floors measure the
SOLVER, not the mathematics, and cannot be cited as evidence of emptiness.

Test: build cell d's saturated chart-N system, choose a random point z*,
subtract F(z*) from the equations so z* is a root BY CONSTRUCTION (same
monomials, same conditioning), then run the identical multi-start hunt.
  found  -> the method has power at this size; floors are meaningful evidence
  missed -> the floors are artefacts and must be retracted as evidence.

Usage: python3 w6_plantctl.py D NSTARTS [seed]
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

d = int(sys.argv[1]); nst = int(sys.argv[2]) if len(sys.argv) > 2 else 40
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5

eqs, unk, A, q1 = build_system(d)
a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
subs = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
        mu1: -mu3*a[2]/3}
core = [expand(e.subs(subs)) for e in eqs]
core = [e for e in core if e != 0]
vars_ = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)] + [mu2, mu3, mu0]
t = Symbol('t'); vars_.append(t)
core.append(expand(t*mu0 - 1))
n = len(vars_)
F = sp.lambdify(vars_, core, modules='numpy')

rng = np.random.default_rng(seed)
zstar = rng.normal(0, 1, n) + 1j*rng.normal(0, 1, n)
shift = np.asarray(F(*zstar), dtype=complex)     # F(z*) ; subtract to plant

def res(x):
    z = x[:n] + 1j*x[n:]
    v = np.asarray(F(*z), dtype=complex) - shift
    return np.concatenate([v.real, v.imag])

chk = float(np.max(np.abs(np.asarray(F(*zstar), dtype=complex) - shift)))
print(json.dumps({'d': d, 'eqs': len(core), 'vars': n,
                  'planted_root_residual': chk}), flush=True)

best = np.inf; found = 0; t0 = time.time()
for k in range(nst):
    x0 = rng.normal(0, 1.0, 2*n)
    try:
        r = least_squares(res, x0, method='lm', max_nfev=4000)
    except Exception:
        continue
    c = float(np.sum(r.fun**2))
    if c < best:
        best = c
        print(json.dumps({'d': d, 'start': k, 'best_residual2': c,
                          'elapsed': round(time.time()-t0,1)}), flush=True)
    if c < 1e-16:
        found += 1
        print(json.dumps({'d': d, 'PLANTED-ROOT-FOUND': True, 'start': k,
                          'residual2': c}), flush=True)
        break
verdict = 'METHOD-HAS-POWER' if found else 'METHOD-BLIND-AT-THIS-SIZE'
print(json.dumps({'d': d, 'nstarts': nst, 'best_residual2': best,
                  'found': found, 'VERDICT': verdict,
                  'elapsed': round(time.time()-t0,1)}))
