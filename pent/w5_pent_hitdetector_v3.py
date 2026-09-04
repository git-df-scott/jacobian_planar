"""
ITEM 2 -- pentagon hit detector, v3.

WHAT v3 CHANGES, AND WHY (STATUS.md section 6's standing requirement)
---------------------------------------------------------------------
v1 used an ABSOLUTE stopping test on a system homogeneous of degree -1 in P's
scale, and Newton solved it by making P huge.  v2 fixed that by switching to a
RATIO objective and fixing two gauges (p_00 translation, p_10 overall scale) --
but a ratio is breakable from the other end too, which is exactly how v2's own
outlier arose: the UNFIXED coordinate-scale gauge (x,y) -> (lam x, lam^-3 y)
moves forbidden and allowed coefficients by different powers of lam, so the
ratio can be driven down with nothing solved.

v3 therefore does all three of the things STATUS section 6 demands:

  1. ALL THREE GAUGES FIXED.  Under (x,y) -> (lam x, lam^-3 y) together with
     P -> c P, the coefficient p_{j,i} scales by c * lam^(i-3j).  Fixing
     p_00 = 0 (translation) and p_10 = 1 (which sets c*lam = 1) leaves the
     one-parameter family p_{j,i} -> lam^(i-3j-1) p_{j,i}.  The exponent at
     (j,i) = (1,0) is -4, nonzero, so p_10... i.e. p_{1,0} ... can be scaled at
     will: the chart p_{1,0} = 1 fixes the last gauge, and p_{1,0} = 0 is the
     complementary chart.  BOTH are searched.  Essential parameters: 58.
  2. ABSOLUTE NORMALISATION.  The objective is the vector of FORBIDDEN
     coefficients itself, in absolute value.  No ratio appears anywhere in the
     stopping test.
  3. "ALLOWED COEFFICIENTS ARE O(1)" IS AN ACCEPTANCE CONDITION, not a post-hoc
     look.  A point is accepted only if
         max |forbidden| < TOL,  1/BAND <= max |allowed| <= BAND,
         and  max |parameter| <= XCAP,
     all three checked at the accepted point.

CONTROLS
--------
  POS-1  a planted target.  Take a random point x0, and solve F(x) = F(x0)
         instead of F(x) = 0.  x0 is a root by construction and Newton must
         find a point that passes the FULL acceptance test against that target.
  NEG-1  the v1 artefact must be REJECTED: a point with huge ||x|| whose ratio
         is tiny but whose allowed coefficients have collapsed is fed to the
         acceptance test, which must refuse it.
  NEG-2  the acceptance test must refuse a point whose forbidden coefficients
         are not small, even when everything else is in band.
  NEG-3  the mod-p exact search must REJECT a random non-root and ACCEPT a
         planted exact root.

DISCIPLINE.  This is a hit finder.  Not finding anything is not emptiness, and
nothing here is reported as a verdict about the pentagon system.
"""

import json
import os
import random
import sys
import time

import numpy as np

RESULTS = []
JMAX = 40
TOL = 1e-9
BAND = 1e3
XCAP = 1e4


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def P_rows(jmax=16):
    r = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 8), min(8, j // 2 + 1)
        if lo <= hi:
            r[j] = (lo, hi)
    return r


PR = P_rows()
PARAMS = [(j, i) for j in sorted(PR) for i in range(PR[j][0], PR[j][1] + 1)]
NP = len(PARAMS)
IDX = {k: n for n, k in enumerate(PARAMS)}
GAUGE_IDX = [IDX[(0, 0)], IDX[(0, 1)], IDX[(1, 0)]]


def gauge_exponent(j, i):
    """the exponent of lam in p_{j,i} -> lam^(i-3j-1) p_{j,i} after c*lam = 1."""
    return i - 3 * j - 1


def free_indices(chart):
    return [k for k in range(NP) if k not in GAUGE_IDX]


def embed(x, chart):
    Pv = np.zeros(NP, dtype=complex)
    fr = free_indices(chart)
    Pv[fr] = x
    Pv[IDX[(0, 0)]] = 0.0
    Pv[IDX[(0, 1)]] = 1.0
    Pv[IDX[(1, 0)]] = 1.0 if chart == "one" else 0.0
    return Pv


def cpoly_run(Pvals):
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i:
            row.append(0j)
        row[i] = Pvals[k]
    P = [np.array(Pd.get(j, [0j]), dtype=complex) for j in range(JMAX + 2)]
    p10 = P[0][1] if len(P[0]) > 1 else 0j
    if abs(p10) < 1e-14:
        return None
    Q = [np.zeros(1, dtype=complex) for _ in range(JMAX + 2)]
    Q[0] = np.array([1.0 + 0j])
    Q[1] = np.array([0j, 0j, 1.0 / p10])

    def dv(a):
        return (a[1:] * np.arange(1, len(a))) if len(a) > 1 else np.zeros(1, dtype=complex)

    for k in range(1, JMAX):
        acc = np.zeros(1, dtype=complex)
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P):
                continue
            for t in (np.convolve(P[a], dv(Q[b])) * a,
                      np.convolve(dv(P[a]), Q[b]) * (-(k + 1 - a))):
                if len(t) > len(acc):
                    acc = np.pad(acc, (0, len(t) - len(acc)))
                acc[:len(t)] += t
        Q[k + 1] = acc / ((k + 1) * p10)
    return Q


def forbidden_vector(Q, jmax=23):
    out = []
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(min(j - 12, len(q))):
            out.append(q[i])
        for i in range(len(q), j - 12):
            out.append(0j)
    return np.array(out, dtype=complex)


def allowed_scale(Q, jmax=23):
    m = 0.0
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(j - 12, len(q)):
            m = max(m, abs(q[i]))
    return m


def Fvec(x, chart, target=None):
    Q = cpoly_run(embed(x, chart))
    if Q is None:
        return None, None
    f = forbidden_vector(Q)
    if target is not None:
        f = f - target
    return f, Q


def accept(x, Q, f):
    """The FULL acceptance test.  All three conditions, all absolute."""
    if Q is None or f is None:
        return False, "no evaluation"
    a = allowed_scale(Q)
    fmax = float(np.max(np.abs(f))) if len(f) else 0.0
    xmax = float(np.max(np.abs(x))) if len(x) else 0.0
    if fmax >= TOL:
        return False, f"forbidden max {fmax:.3e} >= TOL"
    if not (1.0 / BAND <= a <= BAND):
        return False, f"allowed scale {a:.3e} outside [{1/BAND:.1e},{BAND:.1e}]"
    if xmax > XCAP:
        return False, f"parameter norm {xmax:.3e} > XCAP"
    return True, f"forbidden {fmax:.3e}, allowed {a:.3e}, |x| {xmax:.3e}"


def newton(x0, chart, target=None, iters=60):
    x = x0.copy()
    best = (np.inf, x.copy())
    for _ in range(iters):
        f, Q = Fvec(x, chart, target)
        if f is None:
            return best
        nrm = float(np.max(np.abs(f)))
        if nrm < best[0]:
            best = (nrm, x.copy())
        if nrm < TOL:
            return (nrm, x.copy())
        J = np.zeros((len(f), len(x)), dtype=complex)
        h = 1e-7
        for c in range(len(x)):
            xp = x.copy()
            xp[c] += h
            fp, _ = Fvec(xp, chart, target)
            if fp is None:
                return best
            J[:, c] = (fp - f) / h
        try:
            dx = np.linalg.lstsq(J, -f, rcond=None)[0]
        except np.linalg.LinAlgError:
            return best
        step, improved = 1.0, False
        for _ in range(30):
            xn = x + step * dx
            fn, _ = Fvec(xn, chart, target)
            if fn is not None and float(np.max(np.abs(fn))) < nrm:
                x = xn
                improved = True
                break
            step *= 0.5
        if not improved:
            return best
    return best


# ---------------------------------------------------------------------------
# exact search over F_p, p = 1 (mod 3)
# ---------------------------------------------------------------------------
def fp_run(Pvals, p):
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i:
            row.append(0)
        row[i] = Pvals[k] % p
    P = [list(Pd.get(j, [0])) for j in range(JMAX + 2)]
    p10 = P[0][1] if len(P[0]) > 1 else 0
    if p10 % p == 0:
        return None
    inv10 = pow(p10, p - 2, p)
    Q = [[0] for _ in range(JMAX + 2)]
    Q[0] = [1]
    Q[1] = [0, 0, inv10]

    def dv(a):
        return [(a[t] * t) % p for t in range(1, len(a))] or [0]

    def conv(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for s, ca in enumerate(a):
            if ca:
                for t, cb in enumerate(b):
                    out[s + t] = (out[s + t] + ca * cb) % p
        return out

    for k in range(1, JMAX):
        acc = [0]
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P):
                continue
            for t in ([(z * a) % p for z in conv(P[a], dv(Q[b]))],
                      [(z * (-(k + 1 - a))) % p for z in conv(dv(P[a]), Q[b])]):
                if len(t) > len(acc):
                    acc = acc + [0] * (len(t) - len(acc))
                for s in range(len(t)):
                    acc[s] = (acc[s] + t[s]) % p
        inv = pow((k + 1) * p10 % p, p - 2, p)
        Q[k + 1] = [(z * inv) % p for z in acc]
    return Q


def fp_embed(x, chart, p):
    Pv = [0] * NP
    fr = free_indices(chart)
    for n, k in enumerate(fr):
        Pv[k] = x[n] % p
    Pv[IDX[(0, 0)]] = 0
    Pv[IDX[(0, 1)]] = 1
    Pv[IDX[(1, 0)]] = 1 if chart == "one" else 0
    return Pv


def fp_F(x, chart, p, jmax=23):
    Q = fp_run(fp_embed(x, chart, p), p)
    if Q is None:
        return None, None
    out = []
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(j - 12):
            out.append(q[i] % p if i < len(q) else 0)
    return out, Q


def fp_allowed_nonzero(Q, p, jmax=23):
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(j - 12, len(q)):
            if q[i] % p:
                return True
    return False


def _rref_fp(M, rhs, p):
    A = [row[:] + [rhs[i]] for i, row in enumerate(M)]
    nr = len(A)
    nc = len(M[0]) if nr else 0
    piv, r = [], 0
    for c in range(nc):
        sel = None
        for i in range(r, nr):
            if A[i][c] % p:
                sel = i
                break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [v * inv % p for v in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][k] - f * A[r][k]) % p for k in range(nc + 1)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return A, r, piv


# --- dual numbers over F_p[eps]/(eps^2): EXACT partial derivatives ----------
# A finite difference over a finite field is a secant, never a derivative; the
# campaign's own A2.9 note says so.  Every Jacobian column below is an exact
# partial derivative obtained by running the recursion over F_p[eps]/(eps^2).
def dmul(a, b, p):
    return ((a[0] * b[0]) % p, (a[0] * b[1] + a[1] * b[0]) % p)


def dadd(a, b, p):
    return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)


def dinv(a, p):
    if a[0] % p == 0:
        return None
    i0 = pow(a[0], p - 2, p)
    return (i0, (-a[1] * i0 % p) * i0 % p)


def dual_run(Pvals, p):
    """The y-adic recursion over F_p[eps]/(eps^2); Pvals are dual numbers."""
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i:
            row.append((0, 0))
        row[i] = (Pvals[k][0] % p, Pvals[k][1] % p)
    P = [list(Pd.get(j, [(0, 0)])) for j in range(JMAX + 2)]
    p10 = P[0][1] if len(P[0]) > 1 else (0, 0)
    inv10 = dinv(p10, p)
    if inv10 is None:
        return None
    Q = [[(0, 0)] for _ in range(JMAX + 2)]
    Q[0] = [(1, 0)]
    Q[1] = [(0, 0), (0, 0), inv10]

    def dv(a):
        return [((a[t][0] * t) % p, (a[t][1] * t) % p) for t in range(1, len(a))] or [(0, 0)]

    def conv(a, b):
        out = [(0, 0)] * (len(a) + len(b) - 1)
        for s0, ca in enumerate(a):
            if ca[0] or ca[1]:
                for t, cb in enumerate(b):
                    out[s0 + t] = dadd(out[s0 + t], dmul(ca, cb, p), p)
        return out

    for k in range(1, JMAX):
        acc = [(0, 0)]
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P):
                continue
            for t in ([dmul(z, (a % p, 0), p) for z in conv(P[a], dv(Q[b]))],
                      [dmul(z, ((-(k + 1 - a)) % p, 0), p) for z in conv(dv(P[a]), Q[b])]):
                if len(t) > len(acc):
                    acc = acc + [(0, 0)] * (len(t) - len(acc))
                for s0 in range(len(t)):
                    acc[s0] = dadd(acc[s0], t[s0], p)
        inv = dinv(dmul(((k + 1) % p, 0), p10, p), p)
        if inv is None:
            return None
        Q[k + 1] = [dmul(z, inv, p) for z in acc]
    return Q


def dual_F(x, chart, p, dcol=None, jmax=23):
    fr = free_indices(chart)
    Pv = [(0, 0)] * NP
    for n, k in enumerate(fr):
        Pv[k] = (x[n] % p, 1 if (dcol is not None and n == dcol) else 0)
    Pv[IDX[(0, 0)]] = (0, 0)
    Pv[IDX[(0, 1)]] = (1, 0)
    Pv[IDX[(1, 0)]] = (1 if chart == "one" else 0, 0)
    Q = dual_run(Pv, p)
    if Q is None:
        return None, None
    out = []
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(j - 12):
            out.append(q[i] if i < len(q) else (0, 0))
    return out, Q


def fp_newton(x0, chart, p, iters=30, target=None):
    """Exact Newton over F_p with exact (dual-number) Jacobians.

    `target` shifts the right-hand side, so a planted system F(x) = F(x0) can
    be solved by the very same code path -- that is the positive control."""
    x = list(x0)
    for _ in range(iters):
        f, Q = dual_F(x, chart, p)
        if f is None:
            return None, None
        fv = [a for a, _ in f]
        if target is not None:
            fv = [(fv[i] - target[i]) % p for i in range(len(fv))]
        if all(v % p == 0 for v in fv):
            return x, Q
        n = len(x)
        J = [[0] * n for _ in range(len(f))]
        for c in range(n):
            fc, _ = dual_F(x, chart, p, dcol=c)
            if fc is None:
                return None, None
            for r in range(len(f)):
                J[r][c] = fc[r][1] % p
        A, rk, piv = _rref_fp(J, [(-v) % p for v in fv], p)
        dx = [0] * n
        for i, c in enumerate(piv):
            dx[c] = A[i][n] % p
        # consistency: if the reduced system is inconsistent, this start is dead
        nc = n
        if any(all(A[i][c] % p == 0 for c in range(nc)) and A[i][nc] % p
               for i in range(len(A))):
            return None, None
        x = [(x[i] + dx[i]) % p for i in range(n)]
    return None, None


# ---------------------------------------------------------------------------
# EXACT complex Jacobians by dual numbers over C[eps]/(eps^2).
#
# The float search above builds its Jacobian by finite differences with
# h = 1e-7, which caps the usable accuracy of a Newton step at about 1e-8 and
# is a plausible reason a search stalls at |forbidden| ~ 1e-5 without that being
# a fact about the system.  The recursion is a rational function of the
# parameters, so its derivative can be taken EXACTLY by running it over
# C[eps]/(eps^2) -- the same device used for the mod-p leg.  This costs one
# recursion per column, exactly what the finite difference cost, and removes
# the step-size floor entirely.
# ---------------------------------------------------------------------------
def _cd_mul(a, b):
    return (a[0] * b[0], a[0] * b[1] + a[1] * b[0])


def _cd_inv(a):
    if a[0] == 0:
        return None
    i0 = 1.0 / a[0]
    return (i0, -a[1] * i0 * i0)


def cdual_run(Pvals):
    """The y-adic recursion over C[eps]/(eps^2); Pvals are (value, deriv) pairs."""
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i:
            row.append((0j, 0j))
        row[i] = Pvals[k]
    P = [list(Pd.get(j, [(0j, 0j)])) for j in range(JMAX + 2)]
    p10 = P[0][1] if len(P[0]) > 1 else (0j, 0j)
    if abs(p10[0]) < 1e-14:
        return None
    inv10 = _cd_inv(p10)
    Q = [[(0j, 0j)] for _ in range(JMAX + 2)]
    Q[0] = [(1 + 0j, 0j)]
    Q[1] = [(0j, 0j), (0j, 0j), inv10]

    def dv(a):
        return [(a[t][0] * t, a[t][1] * t) for t in range(1, len(a))] or [(0j, 0j)]

    def conv(a, b):
        out = [(0j, 0j)] * (len(a) + len(b) - 1)
        for s, ca in enumerate(a):
            if ca[0] != 0 or ca[1] != 0:
                for t, cb in enumerate(b):
                    m = _cd_mul(ca, cb)
                    out[s + t] = (out[s + t][0] + m[0], out[s + t][1] + m[1])
        return out

    for k in range(1, JMAX):
        acc = [(0j, 0j)]
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P):
                continue
            for t in ([_cd_mul(z, (a + 0j, 0j)) for z in conv(P[a], dv(Q[b]))],
                      [_cd_mul(z, (-(k + 1 - a) + 0j, 0j))
                       for z in conv(dv(P[a]), Q[b])]):
                if len(t) > len(acc):
                    acc = acc + [(0j, 0j)] * (len(t) - len(acc))
                for s in range(len(t)):
                    acc[s] = (acc[s][0] + t[s][0], acc[s][1] + t[s][1])
        inv = _cd_inv(_cd_mul(((k + 1) + 0j, 0j), p10))
        if inv is None:
            return None
        Q[k + 1] = [_cd_mul(z, inv) for z in acc]
    return Q


def cdual_F(x, chart, dcol=None, jmax=23):
    fr = free_indices(chart)
    Pv = [(0j, 0j)] * NP
    for n, k in enumerate(fr):
        Pv[k] = (complex(x[n]), 1 + 0j if (dcol is not None and n == dcol) else 0j)
    Pv[IDX[(0, 0)]] = (0j, 0j)
    Pv[IDX[(0, 1)]] = (1 + 0j, 0j)
    Pv[IDX[(1, 0)]] = ((1 + 0j) if chart == "one" else 0j, 0j)
    Q = cdual_run(Pv)
    if Q is None:
        return None, None
    out = []
    for j in range(13, jmax + 1):
        q = Q[j]
        for i in range(j - 12):
            out.append(q[i] if i < len(q) else (0j, 0j))
    return out, Q


def newton_exact(x0, chart, target=None, iters=80):
    """Newton with EXACT Jacobians.  Same acceptance test, no step-size floor."""
    x = np.array(x0, dtype=complex)
    best = (np.inf, x.copy())
    for _ in range(iters):
        f0, Q = cdual_F(x, chart)
        if f0 is None:
            return best
        fv = np.array([a for a, _ in f0], dtype=complex)
        if target is not None:
            fv = fv - target
        nrm = float(np.max(np.abs(fv)))
        if nrm < best[0]:
            best = (nrm, x.copy())
        if nrm < TOL:
            return (nrm, x.copy())
        J = np.zeros((len(fv), len(x)), dtype=complex)
        for c in range(len(x)):
            fc, _ = cdual_F(x, chart, dcol=c)
            if fc is None:
                return best
            J[:, c] = np.array([b for _, b in fc], dtype=complex)
        try:
            dx = np.linalg.lstsq(J, -fv, rcond=None)[0]
        except np.linalg.LinAlgError:
            return best
        step, improved = 1.0, False
        for _ in range(40):
            xn = x + step * dx
            fn, _ = cdual_F(xn, chart)
            if fn is not None:
                fvn = np.array([a for a, _ in fn], dtype=complex)
                if target is not None:
                    fvn = fvn - target
                if float(np.max(np.abs(fvn))) < nrm:
                    x = xn
                    improved = True
                    break
            step *= 0.5
        if not improved:
            return best
    return best
