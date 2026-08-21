#!/usr/bin/env python3
"""PENTAGON CASE (1) -- char-0 numerical multi-start.  Never attempted.

GGHV Prop 4.3 case (1) of the surviving (72,108) pair is the ONE branch that
has never received a verdict by any method: the monolithic Groebner basis
needs >40GB, and the random linear-slice search can only ever detect
POSITIVE-dimensional components -- but the system is overdetermined (283
equations, 165 unknowns), so any solution is almost certainly isolated, which
is exactly what slicing cannot see and what multi-start Newton CAN.

System: campaign/audit_tracks/trackB1_param_system.json, exact over Q, gauges
(d_2_1 = s_0_4 = a = b = 1) already substituted, nondegeneracy c_1_0,
c_8_14, d_12_21, s_4_8 != 0.

Any start converging to residual^2 < 1e-16 with all four nondegeneracy
coordinates bounded away from 0 is a CANDIDATE point of case (1) --> exact
lift, then GGHV/Prop-4.3 realization.  Persistent floor = evidence of
emptiness (never proof: a miss is a miss).

CONTROLS (both run before any hunt is reported):
  P-POS  the SAME system with constants shifted so a chosen random point is a
         root by construction MUST be found (validates solver + conditioning
         on the true monomial structure).
  P-NEG  the system plus a contradictory pair (c_1_0 = 1 and c_1_0 = 2) MUST
         NOT converge.

Usage: python3 w6_pentnum.py MODE NSTARTS   (MODE: pos | neg | hunt)
"""
import sys, os, json, time
import numpy as np
from scipy.optimize import least_squares

ROOT = '/home/user/jacobian_planar'
SRC = os.path.join(ROOT, 'campaign/audit_tracks/trackB1_param_system.json')

def load():
    d = json.load(open(SRC))
    vars_ = list(d['variables'])
    vidx = {v: i for i, v in enumerate(vars_)}
    terms = []          # (eq_index, coeff_complex, [(vidx, exp), ...])
    for ei, e in enumerate(d['equations']):
        for mono, co in e['terms']:
            num, den = co
            terms.append((ei, complex(num) / complex(den),
                          tuple((vidx[v], int(x)) for v, x in mono)))
    return vars_, vidx, len(d['equations']), terms, d['nonzero']

class Sys:
    def __init__(self, nvars, neq, terms, shift=None, extra=None):
        self.n = nvars; self.m = neq
        self.terms = terms
        self.shift = shift if shift is not None else np.zeros(neq, dtype=complex)
        self.extra = extra or []          # list of (coeff, [(vidx,exp)...], rhs) rows

    def _rows(self):
        return self.m + len(self.extra)

    def eval_full(self, z, want_jac=True):
        m = self._rows()
        F = np.zeros(m, dtype=complex)
        J = np.zeros((m, self.n), dtype=complex) if want_jac else None
        for ei, co, mono in self.terms:
            val = co
            for vi, ex in mono:
                val *= z[vi] ** ex
            F[ei] += val
            if want_jac:
                for vi, ex in mono:
                    zi = z[vi]
                    if abs(zi) > 1e-30:
                        J[ei, vi] += val * ex / zi
                    else:
                        p = co * ex
                        for vj, ej in mono:
                            e2 = ej - 1 if vj == vi else ej
                            p *= z[vj] ** e2
                        J[ei, vi] += p
        F[:self.m] -= self.shift
        for k, (co, mono, rhs) in enumerate(self.extra):
            r = self.m + k
            val = co
            for vi, ex in mono:
                val *= z[vi] ** ex
            F[r] = val - rhs
            if want_jac:
                for vi, ex in mono:
                    zi = z[vi]
                    if abs(zi) > 1e-30:
                        J[r, vi] += val * ex / zi
        return F, J

    def res(self, x):
        z = x[:self.n] + 1j * x[self.n:]
        F, _ = self.eval_full(z, want_jac=False)
        return np.concatenate([F.real, F.imag])

    def jac(self, x):
        z = x[:self.n] + 1j * x[self.n:]
        _, J = self.eval_full(z, want_jac=True)
        return np.block([[J.real, -J.imag], [J.imag, J.real]])

def hunt(S, nstarts, tag, seed=0, nonzero_idx=(), report_below=1e-16):
    rng = np.random.default_rng(seed)
    best = np.inf; hits = []
    t0 = time.time()
    for k in range(nstarts):
        x0 = rng.normal(0, 1.0, 2 * S.n)
        try:
            r = least_squares(S.res, x0, jac=S.jac, method='lm', max_nfev=3000)
        except Exception:
            continue
        c = float(np.sum(r.fun ** 2))
        if c < best:
            best = c
            print(json.dumps({'tag': tag, 'start': k, 'best_residual2': c,
                              'elapsed': round(time.time() - t0, 1)}), flush=True)
        if c < report_below:
            z = r.x[:S.n] + 1j * r.x[S.n:]
            nz = {i: abs(z[i]) for i in nonzero_idx}
            ok = all(v > 1e-8 for v in nz.values()) if nonzero_idx else True
            rec = {'tag': tag, 'CANDIDATE-PENTAGON': True, 'residual2': c,
                   'nondeg_ok': bool(ok), 'nondeg_abs': {str(i): float(v) for i, v in nz.items()},
                   'z_re': list(r.x[:S.n]), 'z_im': list(r.x[S.n:])}
            print(json.dumps(rec), flush=True)
            hits.append(rec)
            break
    return {'tag': tag, 'nstarts': nstarts, 'best_residual2': best, 'hits': len(hits),
            'elapsed': round(time.time() - t0, 1)}, hits

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'hunt'
    nst = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    vars_, vidx, neq, terms, nonzero = load()
    n = len(vars_)
    nz_idx = tuple(vidx[v] for v in nonzero)
    print(json.dumps({'vars': n, 'eqs': neq, 'terms': len(terms),
                      'nonzero': nonzero, 'mode': mode}), flush=True)

    if mode == 'pos':
        rng = np.random.default_rng(7)
        zstar = rng.normal(0, 1, n) + 1j * rng.normal(0, 1, n)
        S0 = Sys(n, neq, terms)
        Fs, _ = S0.eval_full(zstar, want_jac=False)
        S = Sys(n, neq, terms, shift=Fs)          # zstar is now an exact root
        chk = np.max(np.abs(S.eval_full(zstar, want_jac=False)[0]))
        print(json.dumps({'control': 'P-POS', 'planted_root_residual': float(chk)}), flush=True)
        out, _ = hunt(S, nst, 'P-POS', seed=1)
        print(json.dumps({'control': 'P-POS', 'PASS': out['hits'] > 0, **out}))
    elif mode == 'neg':
        S = Sys(n, neq, terms, extra=[(1.0, ((vidx['c_1_0'], 1),), 1.0),
                                      (1.0, ((vidx['c_1_0'], 1),), 2.0)])
        out, _ = hunt(S, nst, 'P-NEG', seed=2)
        print(json.dumps({'control': 'P-NEG', 'PASS': out['hits'] == 0, **out}))
    else:
        S = Sys(n, neq, terms)
        out, hits = hunt(S, nst, 'PENTAGON-CASE1', seed=11, nonzero_idx=nz_idx)
        json.dump({'summary': out, 'hits': hits, 'vars': vars_},
                  open(os.path.join(ROOT, 'wave6/pentnum_hunt.json'), 'w'), indent=1)
        print(json.dumps(out))
