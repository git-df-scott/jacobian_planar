#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 3 -- THE PENTAGON HIT-DETECTOR.

WHY THIS SHAPE OF ATTACK.  Measured this session:
  * the conditions have degree 12..23 in the 61 parameters (step 2c), so a
    degree-12 form in 61 variables already admits ~1e14 monomials -- the system
    CANNOT be written down, and no exact elimination engine can be handed it.
    (Consistent with every recorded stall: msolve dies in monomial hash-table
    growth on the 166-variable form; the symbolic tower stalls at level 16.)
  * but EVALUATION is cheap: the y-adic recursion returns all 374 conditions in
    milliseconds, and dual numbers give the exact Jacobian (step 1).
  * and the system is SQUARE modulo the single p_00 gauge: 60 essential
    parameters, 60 independent conditions reached at level j <= 23, with 314
    further conditions as surplus (step 1b, 2a).

So: Newton over C on the square 60x60 subsystem from many random starts.  Any
root found is then tested against the 314 SURPLUS conditions -- a root of the
square system that also kills the surplus is a pentagon solution, i.e. a
candidate counterexample, and goes to Hensel + LLL + the full gate.

VERDICT DISCIPLINE (Plan 43 Sec.6.2).  This is a HIT-FINDER ONLY.  Numerical
non-discovery is NEVER evidence of emptiness and is reported as such.
"""
import random, sys, math, time
import numpy as np
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_yadic_independent import PARAMS, PR, QR

NP = len(PARAMS)
P00 = PARAMS.index((0, 0))
P10 = PARAMS.index((0, 1))
ESS = [k for k in range(NP) if k != P00]          # 60 essential parameters
JMAX = 40

def cpoly_run(Pvals):
    """y-adic recursion over C.  Pvals: complex array of length 61."""
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i: row.append(0j)
        row[i] = Pvals[k]
    P = [np.array(Pd.get(j, [0j]), dtype=complex) for j in range(JMAX + 2)]
    p10 = P[0][1] if len(P[0]) > 1 else 0j
    if abs(p10) < 1e-14: return None
    Q = [np.zeros(1, dtype=complex) for _ in range(JMAX + 2)]
    Q[0] = np.array([1.0 + 0j])
    Q[1] = np.array([0j, 0j, 1.0 / p10])              # p10 Q1 = x^2
    def dv(a):
        return (a[1:] * np.arange(1, len(a))) if len(a) > 1 else np.zeros(1, dtype=complex)
    for k in range(1, JMAX):
        acc = np.zeros(1, dtype=complex)
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P): continue
            t1 = np.convolve(P[a], dv(Q[b])) * a
            t2 = np.convolve(dv(P[a]), Q[b]) * (-(k + 1 - a))
            for t in (t1, t2):
                if len(t) > len(acc): acc = np.pad(acc, (0, len(t) - len(acc)))
                acc[:len(t)] += t
        Q[k + 1] = acc / ((k + 1) * p10)
    return Q

LOW, SUR = [], []
for j in range(13, 25):
    for i in range(0, j - 12):
        (LOW if j <= 23 else SUR).append((j, i))
SURPLUS = [(j, i) for (j, i) in SUR]
def cond_vec(Q, spec):
    out = []
    for (j, i) in spec:
        out.append(Q[j][i] if i < len(Q[j]) else 0j)
    return np.array(out, dtype=complex)

def surplus_all(Q):
    v = list(cond_vec(Q, SURPLUS))
    for j in range(25, JMAX + 1):
        v.extend(Q[j][:len(Q[j])])
    return np.array(v, dtype=complex)

def F_and_J(x, rows):
    """residual on `rows` and its Jacobian wrt the 60 essential params, by
    complex-step-free exact forward differences of the recursion (the recursion
    is holomorphic; we use a small complex perturbation with Richardson)."""
    Pv = np.zeros(NP, dtype=complex); Pv[ESS] = x
    Q = cpoly_run(Pv)
    if Q is None: return None, None
    f0 = cond_vec(Q, rows)
    J = np.zeros((len(rows), len(ESS)), dtype=complex)
    h = 1e-6
    for c, k in enumerate(ESS):
        Pp = Pv.copy(); Pp[k] += h
        Qp = cpoly_run(Pp)
        if Qp is None: return None, None
        J[:, c] = (cond_vec(Qp, rows) - f0) / h
    return f0, J

def newton(x0, rows, iters=60):
    x = x0.copy(); best = None
    for it in range(iters):
        f, J = F_and_J(x, rows)
        if f is None: return None, None
        nrm = np.linalg.norm(f)
        if best is None or nrm < best[0]: best = (nrm, x.copy())
        if nrm < 1e-9: return x, nrm
        try:
            dx = np.linalg.lstsq(J, -f, rcond=None)[0]
        except np.linalg.LinAlgError:
            return None, None
        step = 1.0
        for _ in range(25):
            xn = x + step * dx
            fn, _ = F_and_J(xn, rows) if False else (None, None)
            Pv = np.zeros(NP, dtype=complex); Pv[ESS] = xn
            Qn = cpoly_run(Pv)
            if Qn is not None:
                fn = cond_vec(Qn, rows)
                if np.linalg.norm(fn) < nrm: break
            step *= 0.5
        else:
            return best[1], best[0]
        x = x + step * dx
        if not np.all(np.isfinite(x)): return best[1], best[0]
    return best[1], best[0]

print("="*78); print("H1b step 3 -- PENTAGON HIT-DETECTOR (Newton over C)"); print("="*78)
print(f"  essential parameters : {len(ESS)}  (61 minus the p_00 gauge)")
print(f"  square subsystem     : {len(LOW)} conditions, levels 13..23")
print(f"  surplus to test      : all conditions at j = 24 and every j > 24")
print(f"  discipline           : HIT-FINDER ONLY -- non-discovery proves nothing\n")

rng = np.random.default_rng(43)
t0 = time.time(); results = []
NSTART = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for s in range(NSTART):
    x0 = rng.normal(size=len(ESS)) + 1j * rng.normal(size=len(ESS))
    x0 *= 0.5
    x, nrm = newton(x0, LOW)
    if x is None: continue
    results.append((nrm, x))
    if nrm < 1e-8:
        Pv = np.zeros(NP, dtype=complex); Pv[ESS] = x
        Q = cpoly_run(Pv)
        sur = surplus_all(Q)
        smax = float(np.max(np.abs(sur)))
        print(f"  start {s:3d}: ROOT of the square subsystem, |F| = {nrm:.3e}")
        print(f"             surplus conditions max |.| = {smax:.3e}"
              f"  -> {'*** CANDIDATE HIT ***' if smax < 1e-6 else 'surplus NOT satisfied (not a solution)'}")
    elif s % 10 == 0:
        print(f"  start {s:3d}: best |F| = {nrm:.3e}  ({time.time()-t0:.0f}s)")

results.sort(key=lambda r: r[0])
print(f"\n  {len(results)} starts completed in {time.time()-t0:.0f}s")
print(f"  best residuals: " + ", ".join(f"{r[0]:.2e}" for r in results[:8]))
roots = [r for r in results if r[0] < 1e-8]
print(f"  roots of the square subsystem found: {len(roots)}")
print("""
  VERDICT DISCIPLINE.  Whatever this run shows, it is a HIT-FINDER result.
  Finding no root is NOT emptiness -- Newton has a small basin on a degree-23
  system in 60 variables and non-convergence is the expected default.  Only a
  root that also kills all 314 surplus conditions means anything, and that would
  go to Hensel lift + LLL + the full Sec.6.1 gate before the word counterexample
  is used anywhere.""")
print("="*78)
