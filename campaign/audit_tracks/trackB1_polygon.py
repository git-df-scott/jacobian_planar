#!/usr/bin/env python3
"""Polygon-generic y-adic engine: works for ANY N(P), N(Q), not just case (1).

Given Newton polygons N(P), N(Q) (as vertex lists) and a bracket right-hand
side [P,Q] = x^r, expand in powers of y.  If N(Q)'s j = 0 row is {(0,0)} alone
then Q_0 is a constant, Q_0' = 0, and the order-y^0 equation

        P_0' Q_1 - P_1 Q_0'  =  x^r        becomes      P_0' Q_1 = x^r.

If moreover N(P)'s j = 0 row is {(0,0),(1,0)} then P_0' = p_10 is a nonzero
constant, so Q_1 = x^r / p_10 exactly and every higher order solves for
Q_{k+1}: **Q is a function of P**, with no square roots, no denominators beyond
p_10, and no formal series.

The verdict conditions are exactly membership of each Q_j in N(Q)'s j-th row,
plus termination (Q_j = 0 beyond N(Q)'s top row).

This generalization is what the above-125 program needs: given any candidate
polygon pair it produces the exact condition system and its Jacobian rank, so a
pair can be tested without hand geometry.
"""
import random, sys
from fractions import Fraction

p = 65521

# ------------------------------------------------------------------ geometry
def hull_rows(verts, jmax=None):
    """i-range of the convex hull of `verts` at each integer j."""
    vs = list(verts)
    n = len(vs)
    # edges as half-planes: for hull traversal, use all pairs and keep those
    # for which every vertex lies weakly on one side
    halves = []
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            (x1, y1), (x2, y2) = vs[a], vs[b]
            # normal form: A*i + B*j <= C  with (A,B) = (y1-y2, x2-x1)
            A, B = y1 - y2, x2 - x1
            C = A * x1 + B * y1
            if all(A * x + B * y <= C for (x, y) in vs):
                halves.append((A, B, C))
    jlo = min(y for _, y in vs)
    jhi = max(y for _, y in vs) if jmax is None else jmax
    ilo_all = min(x for x, _ in vs)
    ihi_all = max(x for x, _ in vs)
    rows = {}
    for j in range(jlo, jhi + 1):
        good = [i for i in range(ilo_all, ihi_all + 1)
                if all(A * i + B * j <= C for (A, B, C) in halves)]
        if good:
            rows[j] = (min(good), max(good))
    return rows

# ------------------------------------------------- polynomial algebra mod p
def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a

def pmul(a, b):
    if not a or not b:
        return []
    o = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                if v:
                    o[i + j] = (o[i + j] + u * v) % p
    return trim(o)

def padd(a, b):
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) +
                  (b[i] if i < len(b) else 0)) % p for i in range(n)])

def pscal(a, c):
    c %= p
    return trim([u * c % p for u in a]) if c else []

def pderiv(a):
    return trim([i * a[i] % p for i in range(1, len(a))]) if len(a) > 1 else []

# ------------------------------------------------- dual-number (exact Jacobian)
def dadd(x, y):
    return (padd(x[0], y[0]), padd(x[1], y[1]))

def dmul(x, y):
    A, B = x
    C, D = y
    return (pmul(A, C), padd(pmul(A, D), pmul(B, C)))

def dscal(x, c):
    return (pscal(x[0], c), pscal(x[1], c))

def dderiv(x):
    return (pderiv(x[0]), pderiv(x[1]))

def dinv_scalar(a, b):
    ia = pow(a, p - 2, p)
    return (ia, (-b * ia % p) * ia % p)

# ---------------------------------------------------------------- the engine
class Shape:
    def __init__(self, name, NP, NQ, r):
        self.name = name
        self.NP = NP
        self.NQ = NQ
        self.r = r                       # [P,Q] = x^r
        self.PR = hull_rows(NP)
        self.QR = hull_rows(NQ)
        self.idx = [(j, i) for j in sorted(self.PR)
                    for i in range(self.PR[j][0], self.PR[j][1] + 1)]
        self.jP = max(self.PR)
        self.jQ = max(self.QR)

    def describe(self):
        r0 = self.PR.get(0)
        q0 = self.QR.get(0)
        return (f"{self.name}: N(P) rows j=0..{self.jP}, "
                f"{len(self.idx)} lattice points; N(Q) rows j=0..{self.jQ}, "
                f"{sum(hi-lo+1 for lo,hi in self.QR.values())} points; "
                f"P j=0 row {r0}, Q j=0 row {q0}")

    def usable(self):
        """The engine needs Q_0 constant and P_0 = p_00 + p_10 x."""
        q0 = self.QR.get(0)
        r0 = self.PR.get(0)
        return q0 == (0, 0) and r0 == (0, 1)

    def build_P(self, vec, k=None):
        P = {}
        for t, ((j, i), val) in enumerate(zip(self.idx, vec)):
            A, B = P.setdefault(j, ([], []))
            while len(A) <= i:
                A.append(0)
                B.append(0)
            A[i] = val % p
            if k is not None and t == k:
                B[i] = 1
            P[j] = (A, B)
        return {j: (trim(a), trim(b)) for j, (a, b) in P.items()}

    def run_Q(self, P, N):
        A0, B0 = P[0]
        p10 = (A0[1] if len(A0) > 1 else 0, B0[1] if len(B0) > 1 else 0)
        if p10[0] == 0:
            return None
        inv10 = dinv_scalar(*p10)
        xr = [0] * self.r + [1]
        Q = {0: ([0], [0]),
             1: (pscal(xr, inv10[0]), pscal(xr, inv10[1]))}
        for k in range(1, N):
            acc = ([], [])
            for a in range(0, k + 1):
                b = k - a
                if (a + 1) in P and b in Q:
                    acc = dadd(acc, dscal(dmul(P[a + 1], dderiv(Q[b])), a + 1))
                if a >= 1 and a in P and (b + 1) in Q:
                    acc = dadd(acc,
                               dscal(dmul(dderiv(P[a]), Q[b + 1]), -(b + 1)))
            Q[k + 1] = dscal(dmul(acc, ([inv10[0]], [inv10[1]])),
                             pow(k + 1, p - 2, p))
        return Q

    def conditions(self, P, jmax=None):
        """Return (values, eps-parts) of all N(Q) violations, in a fixed order."""
        jmax = jmax if jmax is not None else self.jQ + 2
        Q = self.run_Q(P, jmax + 1)
        if Q is None:
            return None, None
        val, eps = [], []
        for j in range(1, jmax + 1):
            A, B = Q.get(j, ([], []))
            if j in self.QR:
                lo, hi = self.QR[j]
                idxs = [i for i in range(max(len(A), len(B)))
                        if i < lo or i > hi]
            else:
                idxs = list(range(max(len(A), len(B))))
            for i in idxs:
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
                M[i] = [(M[i][t] - f * M[r][t]) % p for t in range(cols)]
        r += 1
        if r == rows:
            break
    return r

def analyze(shape, rng, jmax=None, trials=2):
    if not shape.usable():
        return None
    best_rank, ncond, zero_cols = 0, None, None
    for _ in range(trials):
        vec = [rng.randrange(p) for _ in shape.idx]
        # ensure p_10 != 0
        k10 = shape.idx.index((0, 1))
        vec[k10] = rng.randrange(1, p)
        cols = []
        for k in range(len(shape.idx)):
            P = shape.build_P(vec, k)
            v, e = shape.conditions(P, jmax)
            if v is None:
                cols = None
                break
            cols.append(e)
        if cols is None:
            continue
        ncond = len(cols[0])
        J = [[cols[k][r] for k in range(len(shape.idx))]
             for r in range(ncond)]
        rk = rank_mod_p(J)
        if rk >= best_rank:
            best_rank = rk
            zero_cols = [shape.idx[k] for k in range(len(shape.idx))
                         if all(J[r][k] == 0 for r in range(ncond))]
    return {"nparams": len(shape.idx), "nconds": ncond,
            "rank": best_rank, "zero_cols": zero_cols,
            "dim_bound": len(shape.idx) - best_rank}

CASE1 = Shape("GGHV 4.3 case (1) pentagons",
              [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)],
              [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)], 2)
CASE2 = Shape("GGHV 4.3 case (2) quadrilaterals",
              [(0, 0), (1, 0), (8, 14), (8, 16)],
              [(0, 0), (2, 1), (12, 21), (12, 24)], 2)

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(seed)
    for sh in (CASE1, CASE2):
        print(sh.describe())
        print(f"   engine usable (Q_0 constant, P_0 = p00 + p10 x): "
              f"{sh.usable()}")
        print(f"   N(P) rows: " +
              " ".join(f"{j}:{lo}-{hi}" for j, (lo, hi) in sh.PR.items()))
        print(f"   N(Q) rows: " +
              " ".join(f"{j}:{lo}-{hi}" for j, (lo, hi) in sh.QR.items()))
        r = analyze(sh, rng)
        if r:
            print(f"   >>> params={r['nparams']}  conditions={r['nconds']}  "
                  f"exact Jacobian rank={r['rank']}  "
                  f"dim bound={r['dim_bound']}")
            print(f"   >>> identically-zero Jacobian columns: {r['zero_cols']}")
        print()
