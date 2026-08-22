#!/usr/bin/env python3
"""EXACT Jacobian of the N(Q) conditions with respect to P, via dual numbers.

The conditions are polynomial (not linear) in P's coefficients, so a finite
difference f(v + e_k) - f(v) over F_p is a secant, NOT a derivative, and its
rank means nothing.  This module runs the whole y-adic recursion over the ring
of dual numbers F_p[eps]/(eps^2): a polynomial is carried as a pair (A, B)
meaning A + eps*B, with

    (A + eps B)(C + eps D) = AC + eps (AD + BC).

Seeding B = e_k on the k-th coefficient of P and reading the eps-part of the
conditions gives the exact partial derivative in one pass per parameter.

Cross-check built in: the eps-part must agree with the interpolated linear term
of f(v + t e_k) as a polynomial in t.
"""
import random, sys
from trackB1_yadic_verdict import p, PR, QR, random_P, trim

# ---------------------------------------------- dual-number polynomial algebra
# a "dpoly" is (A, B): two coefficient lists over F_p, meaning A + eps*B.
def dtrim(x):
    return (trim(list(x[0])), trim(list(x[1])))

def dadd(x, y):
    def add1(a, b):
        n = max(len(a), len(b))
        return trim([((a[i] if i < len(a) else 0) +
                      (b[i] if i < len(b) else 0)) % p for i in range(n)])
    return (add1(x[0], y[0]), add1(x[1], y[1]))

def pmul1(a, b):
    if not a or not b:
        return []
    o = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                if v:
                    o[i + j] = (o[i + j] + u * v) % p
    return trim(o)

def dmul(x, y):
    A, B = x
    C, D = y
    def add1(a, b):
        n = max(len(a), len(b))
        return trim([((a[i] if i < len(a) else 0) +
                      (b[i] if i < len(b) else 0)) % p for i in range(n)])
    return (pmul1(A, C), add1(pmul1(A, D), pmul1(B, C)))

def dscal(x, c):
    c %= p
    return (trim([u * c % p for u in x[0]]), trim([u * c % p for u in x[1]]))

def dderiv(x):
    def d1(a):
        return trim([i * a[i] % p for i in range(1, len(a))]) if len(a) > 1 else []
    return (d1(x[0]), d1(x[1]))

def dinv_scalar(x):
    """1/(a + eps b) = 1/a - eps b/a^2, for a scalar dual number (a, b)."""
    a, b = x
    ia = pow(a, p - 2, p)
    return (ia, (-b * ia % p) * ia % p)

# ------------------------------------------------------------------- recursion
def yadic_Q_dual(P, N):
    """P: dict j -> dpoly.  Returns Q: dict j -> dpoly."""
    p0 = P[0]
    p10 = (p0[0][1] if len(p0[0]) > 1 else 0,
           p0[1][1] if len(p0[1]) > 1 else 0)
    inv10 = dinv_scalar(p10)
    Q = {0: ([0], [0]),
         1: ([0, 0, inv10[0]], [0, 0, inv10[1]])}
    for k in range(1, N):
        acc = ([], [])
        for a in range(0, k + 1):
            b = k - a
            if (a + 1) in P and b in Q:
                acc = dadd(acc, dscal(dmul(P[a + 1], dderiv(Q[b])), a + 1))
            if a >= 1 and a in P and (b + 1) in Q:
                acc = dadd(acc, dscal(dmul(dderiv(P[a]), Q[b + 1]), -(b + 1)))
        ik = pow(k + 1, p - 2, p)
        # inv10 is a SCALAR dual number; lift it to a constant dpoly
        Q[k + 1] = dscal(dmul(acc, ([inv10[0]], [inv10[1]])), ik)
    return Q

# --------------------------------------------------------------------- wiring
def param_index():
    idx = []
    for j in sorted(PR):
        lo, hi = PR[j]
        for i in range(lo, hi + 1):
            idx.append((j, i))
    return idx

IDX = param_index()

def build_dual_P(vec, k=None):
    """P as dpolys; if k is not None, seed eps on the k-th coefficient."""
    P = {}
    for t, ((j, i), val) in enumerate(zip(IDX, vec)):
        A, B = P.setdefault(j, ([], []))
        while len(A) <= i:
            A.append(0)
        while len(B) <= i:
            B.append(0)
        A[i] = val % p
        if k is not None and t == k:
            B[i] = 1
        P[j] = (A, B)
    return {j: dtrim(v) for j, v in P.items()}

def conds_dual(P, jlo=13, jhi=24):
    Q = yadic_Q_dual(P, jhi + 1)
    val, eps = [], []
    for j in range(jlo, jhi + 1):
        lo = max(0, j - 12)
        A, B = Q.get(j, ([], []))
        for i in range(lo):
            val.append(A[i] if i < len(A) else 0)
            eps.append(B[i] if i < len(B) else 0)
    return val, eps

def rank_mod_p(M):
    if not M or not M[0]:
        return 0
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i][c] % p), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = pow(M[r][c], p - 2, p)
        M[r] = [x * iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(M[i][k2] - f * M[r][k2]) % p for k2 in range(cols)]
        r += 1
        if r == rows:
            break
    return r

def jacobian(vec, jlo=13, jhi=24):
    cols = []
    for k in range(len(IDX)):
        P = build_dual_P(vec, k)
        _, eps = conds_dual(P, jlo, jhi)
        cols.append(eps)
    m = len(cols[0])
    return [[cols[k][r] for k in range(len(IDX))] for r in range(m)]

def vec_from_P(P):
    return [(P.get(j, [])[i] if i < len(P.get(j, [])) else 0) for (j, i) in IDX]

def crosscheck(vec, k, jhi=16, npts=26):
    """npts must EXCEED the degree of the conditions in the single parameter t;
    those degrees reach 11 already at jhi = 14, so small npts silently fits the
    wrong polynomial and the check fails for no reason."""
    """The eps-part must equal the t-linear coefficient of f(v + t e_k)."""
    from trackB1_yadic_verdict import yadic_Q, P_rows
    import trackB1_yadic_rank as R
    base = None
    vals = []
    for t in range(npts):
        v2 = list(vec)
        v2[k] = (v2[k] + t) % p
        c = R.conditions(v2, 13, jhi)
        if c is None:
            return None
        vals.append(c)
    # linear coefficient by finite differences of the interpolating polynomial
    lin = []
    for r in range(len(vals[0])):
        y = [vals[t][r] for t in range(npts)]
        # Newton forward differences: f(t) = sum C(t,m) D^m f(0); linear term
        # of the polynomial is D^1 f(0) - D^2 f(0)/2 + D^3 f(0)/3 - ...
        D = [y[:]]
        for m in range(1, npts):
            D.append([(D[m-1][i+1] - D[m-1][i]) % p
                      for i in range(len(D[m-1]) - 1)])
        s = 0
        for m in range(1, npts):
            term = D[m][0] * pow(m, p - 2, p) % p
            s = (s + term) if m % 2 == 1 else (s - term)
        lin.append(s % p)
    P = build_dual_P(vec, k)
    _, eps = conds_dual(P, 13, jhi)
    return lin == eps

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    vec0 = vec_from_P(random_P(rng))
    ok = crosscheck(vec0, 3)
    print(f"CROSSCHECK dual-number derivative == interpolated linear term: {ok}")
    print(f"\nP has {len(IDX)} coefficients\n")
    print(f"{'j-range':<12}{'#conds':>9}{'rank':>7}{'dim bound':>12}")
    for jhi in (13, 16, 18, 20, 21, 22, 23, 24):
        best, ncond = 0, None
        for _ in range(n):
            vec = vec_from_P(random_P(rng))
            J = jacobian(vec, 13, jhi)
            ncond = len(J)
            best = max(best, rank_mod_p(J))
        print(f"{'13..'+str(jhi):<12}{ncond:>9}{best:>7}"
              f"{max(0, len(IDX)-best):>12}")
