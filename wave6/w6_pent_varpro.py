#!/usr/bin/env python3
"""PENTAGON CASE (1) -- VARIABLE-PROJECTION (VARPRO) multi-start.  NEW METHOD.

WHY THIS IS DIFFERENT FROM w6_pentnum.py
----------------------------------------
The trackB1 system is EXACTLY BILINEAR in the c-block and the d-block:
every monomial has c-degree <= 1 AND d-degree <= 1 (verified by census;
shapes are c*d, d*s^2, c*s^3, c*s^2, d*s, c*s, d, c, s^2, s, 1).  s reaches
degree 3 but is only 4 variables.

Consequence: for ANY fixed (c, s) the system is a LINEAR system in d.
  F(c,d,s) = Ad(c,s) . d + a0(c,s)
So d never has to be searched -- it is solved EXACTLY by linear least squares
at every evaluation.  This is Golub-Pereyra variable projection.

  w6_pentnum.py : multi-start Newton over all 165 unknowns.
  this script   : multi-start over 55 unknowns (51 c + 4 s), with the
                  remaining 110 d-unknowns eliminated exactly, not iterated.

Besides the 3x dimension drop, VARPRO removes the long curved valleys that
trap Gauss-Newton in separable problems -- the residual is the distance from
a0(c,s) to the column space of Ad(c,s), which is what the geometry actually
cares about.

WHAT A RESULT MEANS
  residual^2 -> 0 with c_1_0, c_8_14, d_12_21, s_4_8 bounded away from 0
      = CANDIDATE point of case (1).  NOT a verdict: it requires exact lifting
        and verification against the exact system before it is anything.
  persistent positive floor
      = evidence of emptiness, NEVER proof.  A miss is a miss.  The floor
        value is itself new data: it is the distance from the Keller condition
        to the non-injectivity locus, which the campaign has never measured.

CONTROLS (both MUST pass before any hunt output is believed)
  pos : the SAME system with each equation's constant shifted so that a chosen
        random point is a root by construction.  The solver MUST find a root.
        Validates the solver on the true monomial structure and conditioning.
  neg : the system plus the contradictory pair c_1_0 = 1 and c_1_0 = 2.
        The solver MUST NOT reach residual 0.  Guards against a can't-fail
        certifier -- the failure mode that has bitten this campaign five times.

Usage:  python3 w6_pent_varpro.py {pos|neg|hunt} NSTARTS [SEED]
"""
import sys, os, json, time
import numpy as np
from scipy.optimize import least_squares

ROOT = '/home/user/jacobian_planar'
SRC = os.path.join(ROOT, 'campaign/audit_tracks/trackB1_param_system.json')
TOL_HIT = 1e-16          # residual^2 below this is a candidate
NONZERO = ['c_1_0', 'c_8_14', 'd_12_21', 's_4_8']


class PentVarPro:
    """F(c,d,s) = Ad(c,s).d + a0(c,s);  residual = min_d ||F||."""

    def __init__(self):
        D = json.load(open(SRC))
        V = list(D['variables'])
        self.V = V
        self.cvars = [v for v in V if v.startswith('c')]
        self.dvars = [v for v in V if v.startswith('d')]
        self.svars = [v for v in V if v.startswith('s')]
        assert len(self.cvars) + len(self.dvars) + len(self.svars) == len(V)
        self.ci = {v: i for i, v in enumerate(self.cvars)}
        self.di = {v: i for i, v in enumerate(self.dvars)}
        self.si = {v: i for i, v in enumerate(self.svars)}
        self.nc, self.nd, self.ns = len(self.cvars), len(self.dvars), len(self.svars)
        self.neq = len(D['equations'])
        self.ncol = self.nd + 1                      # d-columns plus constant

        eq, col, coef, cidx, smon = [], [], [], [], []
        stab = {}                                    # s-monomial -> id
        for ei, e in enumerate(D['equations']):
            for mono, co in e['terms']:
                dcol, cj, sexp = self.nd, -1, [0] * self.ns
                ddeg = cdeg = 0
                for v, x in mono:
                    x = int(x)
                    if v in self.di:
                        dcol = self.di[v]; ddeg += x
                    elif v in self.ci:
                        cj = self.ci[v]; cdeg += x
                    else:
                        sexp[self.si[v]] += x
                assert ddeg <= 1 and cdeg <= 1, "system is not bilinear -- abort"
                key = tuple(sexp)
                if key not in stab:
                    stab[key] = len(stab)
                num, den = co
                eq.append(ei); col.append(dcol); coef.append(complex(num) / complex(den))
                cidx.append(cj); smon.append(stab[key])
        self.eq = np.array(eq); self.col = np.array(col)
        self.coef = np.array(coef, dtype=complex)
        self.cidx = np.array(cidx); self.smon = np.array(smon)
        self.flat = self.eq * self.ncol + self.col
        self.sexps = np.array(sorted(stab, key=stab.get))     # (nsmono, ns)
        self.has_c = self.cidx >= 0
        self.cidx_safe = np.where(self.has_c, self.cidx, 0)
        self.shift = np.zeros(self.neq, dtype=complex)        # P-POS constant shift
        self.extra = []                                       # P-NEG rows

    # ---- assembly -------------------------------------------------------
    def matrix(self, c, s):
        """Build [Ad | a0] for the given (c, s)."""
        sv = np.prod(np.power(s[None, :], self.sexps), axis=1)   # s-monomial values
        tv = self.coef * sv[self.smon]
        tv = np.where(self.has_c, tv * c[self.cidx_safe], tv)
        n = self.neq * self.ncol
        A = (np.bincount(self.flat, weights=tv.real, minlength=n)
             + 1j * np.bincount(self.flat, weights=tv.imag, minlength=n)).reshape(self.neq, self.ncol)
        A[:, self.nd] -= self.shift
        if self.extra:
            rows = np.zeros((len(self.extra), self.ncol), dtype=complex)
            for k, (cj, rhs) in enumerate(self.extra):
                rows[k, self.nd] = c[cj] - rhs
            A = np.vstack([A, rows])
        return A

    def residual(self, c, s):
        """VARPRO residual vector: distance from -a0 to colspace(Ad)."""
        A = self.matrix(c, s)
        Ad, a0 = A[:, :self.nd], A[:, self.nd]
        sol, *_ = np.linalg.lstsq(Ad, -a0, rcond=None)
        return Ad @ sol + a0, sol

    # ---- real packing for scipy ----------------------------------------
    def unpack(self, th):
        z = th[:len(th) // 2] + 1j * th[len(th) // 2:]
        return z[:self.nc], z[self.nc:]

    def fun(self, th):
        c, s = self.unpack(th)
        r, _ = self.residual(c, s)
        return np.concatenate([r.real, r.imag])

    def evaluate_exact(self, c, d, s):
        """Direct evaluation of the ORIGINAL F at a full point (for controls)."""
        sv = np.prod(np.power(s[None, :], self.sexps), axis=1)
        tv = self.coef * sv[self.smon]
        tv = np.where(self.has_c, tv * c[self.cidx_safe], tv)
        dfull = np.append(d, 1.0)
        tv = tv * dfull[self.col]
        return (np.bincount(self.eq, weights=tv.real, minlength=self.neq)
                + 1j * np.bincount(self.eq, weights=tv.imag, minlength=self.neq))

    # ---- driver ---------------------------------------------------------
    def run(self, nstarts, rng, label):
        dim = 2 * (self.nc + self.ns)
        best = np.inf; best_pt = None; hits = []
        t0 = time.time()
        for k in range(nstarts):
            th0 = rng.normal(scale=1.0, size=dim)
            try:
                out = least_squares(self.fun, th0, method='lm', xtol=1e-14,
                                    ftol=1e-14, gtol=1e-14, max_nfev=20000)
            except Exception as ex:
                print(f"  start {k}: solver error {ex}"); continue
            r2 = float(np.sum(out.fun ** 2))
            if r2 < best:
                best = r2; best_pt = out.x.copy()
            if r2 < TOL_HIT:
                c, s = self.unpack(out.x)
                _, d = self.residual(c, s)
                hits.append((r2, c, d, s))
            print(f"  [{label}] start {k:3d}  res^2 = {r2:.6e}"
                  f"{'   <-- HIT' if r2 < TOL_HIT else ''}", flush=True)
        print(f"  [{label}] {nstarts} starts in {time.time()-t0:.1f}s   best res^2 = {best:.6e}")
        return best, best_pt, hits


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'hunt'
    nst = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260821
    rng = np.random.default_rng(seed)
    P = PentVarPro()
    print(f"system: {P.neq} equations, {P.nc} c + {P.nd} d + {P.ns} s = "
          f"{P.nc+P.nd+P.ns} unknowns")
    print(f"VARPRO search dimension: {P.nc + P.ns} complex "
          f"({2*(P.nc+P.ns)} real); {P.nd} d-unknowns eliminated exactly\n")

    if mode == 'pos':
        c0 = rng.normal(size=P.nc) + 1j * rng.normal(size=P.nc)
        d0 = rng.normal(size=P.nd) + 1j * rng.normal(size=P.nd)
        s0 = rng.normal(size=P.ns) + 1j * rng.normal(size=P.ns)
        P.shift = P.evaluate_exact(c0, d0, s0)
        r, _ = P.residual(c0, s0)
        print(f"P-POS: planted root check at the planted point: res^2 = "
              f"{float(np.sum(np.abs(r)**2)):.3e}  (must be ~0)")
        best, _, hits = P.run(nst, rng, 'pos')
        ok = best < 1e-14
        print(f"\nP-POS {'PASS' if ok else 'FAIL'}: solver "
              f"{'found' if ok else 'DID NOT find'} a root of a system that has one.")
        sys.exit(0 if ok else 1)

    if mode == 'neg':
        P.extra = [(P.ci['c_1_0'], 1.0), (P.ci['c_1_0'], 2.0)]
        best, _, hits = P.run(nst, rng, 'neg')
        ok = best > 1e-10
        print(f"\nP-NEG {'PASS' if ok else 'FAIL'}: solver "
              f"{'correctly refused' if ok else 'FALSELY SOLVED'} a contradictory system."
              f"  floor = {best:.6e}")
        sys.exit(0 if ok else 1)

    best, best_pt, hits = P.run(nst, rng, 'hunt')
    print(f"\nHUNT: best residual^2 over {nst} starts = {best:.6e}")
    if not hits:
        print("NO CANDIDATE.  This is evidence of emptiness, not proof -- a miss is a miss.")
        print(f"Measured floor (new datum): {best:.6e}")
        sys.exit(0)
    for r2, c, d, s in hits:
        vals = {'c_1_0': c[P.ci['c_1_0']], 'c_8_14': c[P.ci['c_8_14']],
                'd_12_21': d[P.di['d_12_21']], 's_4_8': s[P.si['s_4_8']]}
        good = all(abs(v) > 1e-6 for v in vals.values())
        print(f"CANDIDATE res^2={r2:.3e} nondegeneracy "
              f"{ {k: f'{abs(v):.3e}' for k, v in vals.items()} } "
              f"-> {'ADMISSIBLE' if good else 'degenerate, discard'}")
        if good:
            np.save(os.path.join(ROOT, 'wave6/pentseed/varpro_candidate.npy'),
                    np.concatenate([c, d, s]))
            print("saved wave6/pentseed/varpro_candidate.npy -- REQUIRES EXACT LIFT "
                  "AND VERIFICATION BEFORE IT IS ANY KIND OF RESULT")


if __name__ == '__main__':
    main()
