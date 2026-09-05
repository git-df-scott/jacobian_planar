"""Numerically exhaust E1 (the leading level) for p108_525122.

E1 alone involves only f_2 = T*F, deg F = 7.  With F_0 = 1 (scaling) and
F_7 = 1 (nondegeneracy c23 != 0 plus the residual weighted scaling
F_i -> mu^i F_i, mu^7 = 1) it is 6 equations in the 6 unknowns F_1..F_6.
"""
import numpy as np, sys
sys.path.insert(0, '/home/user/jacobian_planar/x2')
import gsys

def resid(v):
    F = [1.0 + 0j] + list(v) + [1.0 + 0j]      # F0=1, F1..F6 = v, F7=1
    G, r = gsys.solve_G(F, 0j)
    return np.array(r[:6], dtype=complex)

def jac(v, h=1e-7):
    n = len(v)
    J = np.zeros((6, n), dtype=complex)
    f0 = resid(v)
    for k in range(n):
        w = v.copy(); w[k] += h
        J[:, k] = (resid(w) - f0) / h
    return J, f0

def newton(v, iters=200):
    for _ in range(iters):
        J, f = jac(v)
        if not np.all(np.isfinite(f)):
            return None
        try:
            d = np.linalg.lstsq(J, -f, rcond=None)[0]
        except np.linalg.LinAlgError:
            return None
        step = 1.0
        v = v + step * d
        if np.max(np.abs(v)) > 1e8:
            return None
        if np.max(np.abs(f)) < 1e-13 and np.max(np.abs(d)) < 1e-12:
            return v
    return v if np.max(np.abs(resid(v))) < 1e-9 else None

if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    sols = []
    for t in range(N):
        scale = 10 ** rng.uniform(-1, 1)
        v = scale * (rng.normal(size=6) + 1j * rng.normal(size=6))
        s = newton(v)
        if s is None:
            continue
        r = np.max(np.abs(resid(s)))
        if r > 1e-9:
            continue
        if any(np.max(np.abs(s - u)) < 1e-6 for u in sols):
            continue
        sols.append(s)
        print(f"[{t}] residual {r:.2e}  F1..F6 = "
              + ", ".join(f"{z.real:+.10g}{z.imag:+.10g}j" for z in s), flush=True)
    print(f"\ndistinct solutions found: {len(sols)} (from {N} random starts)")
