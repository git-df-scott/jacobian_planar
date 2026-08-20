#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 3b -- ADVERSARIAL DIAGNOSIS of the Newton roots.

Plan 43 Sec.6.1 step 5 and the CASE2 dim-4 incident say the default explanation
for an apparent hit is DEGENERACY, not a counterexample.  The obvious failure
mode here: the conditions have degree 12..23, so at a point of small norm
EVERYTHING is small and a residual of 1e-9 means nothing.  A vanishing
coefficient is only meaningful RELATIVE to the coefficients that are allowed to
be nonzero at the same level.

DECISIVE TEST.  At each level j, compare
    max |Q_j[i]| over FORBIDDEN i (i < j-12)     <- must vanish
    max |Q_j[i]| over ALLOWED  i (i >= j-12)     <- must NOT vanish
If both are ~1e-8, the "root" is a degenerate point, not a solution.
"""
import sys, numpy as np
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_newton_hitdetector import (PARAMS, ESS, NP, P00, P10, cpoly_run,
                                        LOW, cond_vec, newton, JMAX)

rng = np.random.default_rng(43)
print("="*78); print("H1b step 3b -- ADVERSARIAL DIAGNOSIS OF THE NEWTON ROOTS"); print("="*78)

found = 0
for s in range(14):
    x0 = rng.normal(size=len(ESS)) + 1j * rng.normal(size=len(ESS)); x0 *= 0.5
    x, nrm = newton(x0, LOW)
    if x is None or nrm is None or nrm > 1e-8: continue
    found += 1
    Pv = np.zeros(NP, dtype=complex); Pv[ESS] = x
    Q = cpoly_run(Pv)
    print(f"\n  --- root from start {s}:  |F| = {nrm:.3e} ---")
    print(f"      ||x||_2 = {np.linalg.norm(x):.4e}   ||x||_inf = {np.max(np.abs(x)):.4e}")
    print(f"      p_10 = {Pv[P10]:.4e}   |p_10| = {abs(Pv[P10]):.4e}")
    print(f"      |P| coefficients: min {np.min(np.abs(x)):.3e}  max {np.max(np.abs(x)):.3e}")
    print(f"      level   max|Q_j| FORBIDDEN      max|Q_j| ALLOWED      ratio")
    degenerate = True
    for j in range(13, 25):
        q = Q[j]
        forb = [abs(q[i]) for i in range(min(j - 12, len(q)))]
        allw = [abs(q[i]) for i in range(j - 12, len(q))]
        mf = max(forb) if forb else 0.0
        ma = max(allw) if allw else 0.0
        ratio = (mf / ma) if ma > 0 else float('inf')
        if ma > 1e-3: degenerate = False
        print(f"      j={j:2d}    {mf:.4e}              {ma:.4e}          {ratio:.2e}")
    msg = ("DEGENERATE: the allowed coefficients vanish too -- Q is (near) ZERO, "
           "so this is the trivial solution, NOT a counterexample") if degenerate else (
           "allowed coefficients are genuinely nonzero -- ESCALATE")
    print(f"      ==> {msg}")
    if found >= 3: break

print("\n" + "="*78)
print("""READING.  If the ALLOWED coefficients are also ~0, the root is the trivial
point Q == 0 (equivalently P degenerating so the recursion produces nothing),
which satisfies every support condition vacuously and is NOT a Keller pair.
That is the degenerate-solution failure mode Plan 43 Sec.6.1 step 5 exists to
catch, and it is why 'numerical root' and 'hit' are different words.""")
print("="*78)
