#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 3 (v2) -- PENTAGON HIT-DETECTOR, CORRECTED.

WHY v2 EXISTS.  v1 reported five "candidate hits".  All five were ARTEFACTS of
a defect in v1, caught by the adversarial diagnosis Plan 43 Sec.6.1 step 5
mandates.  Recorded in full because the failure is instructive:

  * P's overall SCALE is a gauge of this problem: [cP, Q/c] = [P,Q], and the
    y-adic recursion makes Q -> Q/c when P -> cP, so every support condition is
    unchanged.  The conditions are therefore HOMOGENEOUS of degree -1 in the
    scale -- measured: scaling P by c divides the absolute residual by c while
    the ratio (forbidden coefficients)/(allowed coefficients) stays FIXED at
    1.1721e+06 across six orders of magnitude.
  * v1's Newton stopped on an ABSOLUTE test ||F|| < 1e-9.  That test is solved
    by "make P big", not by "solve the system".  Newton duly drove ||x|| to
    ~1e10, Q collapsed to ~1e-9 everywhere, and every support condition was
    satisfied vacuously -- including the ones that must NOT vanish.  At the
    deepest level the "vanishing" coefficients were LARGER than the allowed
    ones (ratio 1.36).

CORRECTIONS IN v2:
  1. GAUGE-FIX the scale: p_10 = 1 (legitimate -- the scale is a true gauge),
     alongside the p_00 = 0 translation gauge.  59 essential parameters.
  2. SCALE-INVARIANT objective: at each level j the residual is
         max |Q_j[i]| over forbidden i   /   max |Q_j[i]| over allowed i,
     which cannot be made small by rescaling anything.
  3. A root is accepted only if that RATIO is small AND the allowed
     coefficients are genuinely O(1) -- i.e. Q is not the zero polynomial.
  4. __main__ guard (v1 had none, so importing it re-ran the whole search).
  5. Jacobian by finite differences is stated as such; v1's docstring wrongly
     claimed dual numbers.

VERDICT DISCIPLINE: HIT-FINDER ONLY.  Non-discovery is never emptiness.
"""
import sys, time
import numpy as np

def build():
    def P_rows(jmax=16):
        r = {}
        for j in range(jmax + 1):
            lo, hi = max(0, j - 8), min(8, j // 2 + 1)
            if lo <= hi: r[j] = (lo, hi)
        return r
    PR = P_rows()
    PARAMS = [(j, i) for j in sorted(PR) for i in range(PR[j][0], PR[j][1] + 1)]
    return PARAMS
PARAMS = build()
NP = len(PARAMS); P00 = PARAMS.index((0, 0)); P10 = PARAMS.index((0, 1))
FREE = [k for k in range(NP) if k not in (P00, P10)]     # 59 essential
JMAX = 40

def cpoly_run(Pvals):
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i: row.append(0j)
        row[i] = Pvals[k]
    P = [np.array(Pd.get(j, [0j]), dtype=complex) for j in range(JMAX + 2)]
    p10 = P[0][1] if len(P[0]) > 1 else 0j
    if abs(p10) < 1e-14: return None
    Q = [np.zeros(1, dtype=complex) for _ in range(JMAX + 2)]
    Q[0] = np.array([1.0 + 0j]); Q[1] = np.array([0j, 0j, 1.0 / p10])
    def dv(a): return (a[1:] * np.arange(1, len(a))) if len(a) > 1 else np.zeros(1, dtype=complex)
    for k in range(1, JMAX):
        acc = np.zeros(1, dtype=complex)
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P): continue
            for t in (np.convolve(P[a], dv(Q[b])) * a,
                      np.convolve(dv(P[a]), Q[b]) * (-(k + 1 - a))):
                if len(t) > len(acc): acc = np.pad(acc, (0, len(t) - len(acc)))
                acc[:len(t)] += t
        Q[k + 1] = acc / ((k + 1) * p10)
    return Q

def embed(x):
    Pv = np.zeros(NP, dtype=complex); Pv[FREE] = x
    Pv[P00] = 0.0; Pv[P10] = 1.0          # gauge: translation and SCALE fixed
    return Pv

def residual(Q, jmax=23):
    """Scale-invariant per-level residual, and the allowed-coefficient scale."""
    rat, allowed_scale, raw = [], [], []
    for j in range(13, jmax + 1):
        q = Q[j]
        forb = [abs(q[i]) for i in range(min(j - 12, len(q)))]
        allw = [abs(q[i]) for i in range(j - 12, len(q))]
        mf = max(forb) if forb else 0.0
        ma = max(allw) if allw else 0.0
        raw.append(mf); allowed_scale.append(ma)
        rat.append(mf / ma if ma > 0 else np.inf)
    return max(rat), max(allowed_scale), max(raw)

def Fvec(x, jmax=23):
    Q = cpoly_run(embed(x))
    if Q is None: return None, None
    out = []
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(min(j - 12, len(q))): out.append(q[i])
        for i in range(len(q), j - 12): out.append(0j)
    return np.array(out, dtype=complex), Q

def newton(x0, iters=80):
    x = x0.copy(); best = (np.inf, x.copy())
    for _ in range(iters):
        f, Q = Fvec(x)
        if f is None: return best
        ratio, ascale, _ = residual(Q)
        if ratio < best[0]: best = (ratio, x.copy())
        if ratio < 1e-10 and ascale > 1e-6: return (ratio, x.copy())
        J = np.zeros((len(f), len(x)), dtype=complex); h = 1e-7
        for c in range(len(x)):
            xp = x.copy(); xp[c] += h
            fp, _ = Fvec(xp)
            if fp is None: return best
            J[:, c] = (fp - f) / h
        try: dx = np.linalg.lstsq(J, -f, rcond=None)[0]
        except np.linalg.LinAlgError: return best
        step, improved = 1.0, False
        for _ in range(30):
            xn = x + step * dx
            fn, Qn = Fvec(xn)
            if fn is not None and residual(Qn)[0] < ratio:
                x = xn; improved = True; break
            step *= 0.5
        if not improved: return best
    return best

def main(nstart=30):
    print("="*78); print("H1b step 3 v2 -- PENTAGON HIT-DETECTOR (scale-gauge fixed)"); print("="*78)
    print(f"  essential parameters : {len(FREE)}  (61 minus p_00 translation minus p_10 scale)")
    print(f"  objective            : SCALE-INVARIANT max_j (forbidden/allowed)")
    print(f"  acceptance           : ratio < 1e-10 AND allowed coefficients O(1)")
    print(f"  discipline           : HIT-FINDER ONLY\n")
    rng = np.random.default_rng(2026); t0 = time.time(); best_all = []
    for s in range(nstart):
        x0 = rng.normal(size=len(FREE)) + 1j * rng.normal(size=len(FREE))
        r, x = newton(x0)
        best_all.append(r)
        f, Q = Fvec(x)
        ascale = residual(Q)[1] if Q is not None else 0
        if r < 1e-10 and ascale > 1e-6:
            print(f"  start {s:3d}: *** ratio {r:.3e}, allowed scale {ascale:.3e} -- ESCALATE ***")
        elif s % 5 == 0:
            print(f"  start {s:3d}: best scale-invariant ratio {r:.3e}   ({time.time()-t0:.0f}s)")
    best_all.sort()
    print(f"\n  {nstart} starts in {time.time()-t0:.0f}s")
    print(f"  best scale-invariant ratios: " + ", ".join(f"{r:.2e}" for r in best_all[:8]))
    hits = [r for r in best_all if r < 1e-10]
    print(f"  genuine candidates (scale-invariant): {len(hits)}")
    print("""
  READING.  Under the corrected, scale-invariant objective the trivial
  direction is closed: no amount of rescaling P moves this number.  A ratio
  that stays O(1) means the forbidden coefficients are the same size as the
  allowed ones -- i.e. Newton is not approaching any solution, which for a
  degree-12..23 system in 59 variables from random starts is the expected
  default and is NOT evidence of emptiness.""")
    print("="*78)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
