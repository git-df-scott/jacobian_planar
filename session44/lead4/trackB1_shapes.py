#!/usr/bin/env python3
"""Per-pair verdict machine for ANY Newton-polygon pair — the regression bar.

The y-adic engine needs a "driver": one of the two polygons must have j = 0 row
exactly {(0,0),(1,0)} (so its y^0 part is p_00 + p_10 x with p_10 a nonzero
constant) and the other must have j = 0 row exactly {(0,0)} (so its y^0 part is
a constant, killing the Q_0' term).  Then the order-y^0 equation determines the
other polynomial's y^1 coefficient outright and the whole recursion unwinds.

Which polygon plays which role DEPENDS ON THE SHAPE:

    (8,28) case (1)/(2):  N(P) j=0 row = {(0,0),(1,0)},  N(Q) j=0 row = {(0,0)}
                          -> P drives, [P,Q] = x^2
    (9,27):               N(P) j=0 row = {(0,0)},  N(Q) j=0 row = {(0,0),(1,0)}
                          -> Q drives; use [Q,P] = -x

so the engine orients itself, and a shape where neither polygon qualifies is
reported as OUT OF SCOPE rather than silently mis-analysed.

Decision 1's acceptance bar was: reproduce the published cases before emitting
anything new.  This module is that bar, in the only form that is sound without
re-deriving GGHV's §4 reduction: it does not GUESS polygons, it VERIFIES a given
pair, exactly, and reports the condition count and exact Jacobian rank.
"""
import random, sys
from trackB1_polygon import (hull_rows, rank_mod_p, trim, padd, pmul, pscal,
                             pderiv, dadd, dmul, dscal, dderiv, dinv_scalar, p)

class Pair:
    def __init__(self, name, NA, NB, rhs, note=""):
        """[A,B] = rhs, where rhs is a list of (i, j, coeff) monomials."""
        self.name = name
        self.NA, self.NB = NA, NB
        self.rhs = rhs
        self.note = note
        self.RA, self.RB = hull_rows(NA), hull_rows(NB)

    def orient(self):
        """Return (driver_rows, other_rows, rhs, flipped) or None."""
        a0, b0 = self.RA.get(0), self.RB.get(0)
        if a0 == (0, 1) and b0 == (0, 0):
            return self.RA, self.RB, self.rhs, False
        if b0 == (0, 1) and a0 == (0, 0):
            neg = [(i, j, (-c) % p) for (i, j, c) in self.rhs]
            return self.RB, self.RA, neg, True
        return None

def rhs_rows(rhs, jmax):
    """R_k(x) for k = 0..jmax as coefficient lists."""
    out = {}
    for (i, j, c) in rhs:
        out.setdefault(j, [])
        while len(out[j]) <= i:
            out[j].append(0)
        out[j][i] = (out[j][i] + c) % p
    return {j: trim(v) for j, v in out.items()}

def run_pair(pair, rng, jextra=2, trials=2):
    o = pair.orient()
    if o is None:
        return {"status": "OUT OF SCOPE",
                "detail": f"j=0 rows are {pair.RA.get(0)} and {pair.RB.get(0)}; "
                          f"engine needs one (0,1) and one (0,0)"}
    DR, OR_, rhs, flipped = o
    idx = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]
    # jmax must reach BOTH polygons' top rows: far enough to impose "the
    # computed polynomial vanishes above N's top row", and far enough that
    # every driver parameter can influence some condition.  Using only
    # max(OR_) leaves the driver's high-j parameters invisible (they show up
    # as spurious identically-zero Jacobian columns).
    jmax = max(max(OR_), max(DR)) + jextra
    R = rhs_rows(rhs, jmax)

    def build(vec, k=None):
        D = {}
        for t, ((j, i), val) in enumerate(zip(idx, vec)):
            A, B = D.setdefault(j, ([], []))
            while len(A) <= i:
                A.append(0)
                B.append(0)
            A[i] = val % p
            if k is not None and t == k:
                B[i] = 1
            D[j] = (A, B)
        return {j: (trim(a), trim(b)) for j, (a, b) in D.items()}

    def conds(D):
        A0, B0 = D[0]
        p10 = (A0[1] if len(A0) > 1 else 0, B0[1] if len(B0) > 1 else 0)
        if p10[0] == 0:
            return None
        inv = dinv_scalar(*p10)
        r0 = R.get(0, [])
        Q = {0: ([0], [0]),
             1: (pscal(r0, inv[0]), pscal(r0, inv[1]))}
        for k in range(1, jmax + 1):
            acc = (list(R.get(k, [])), [])
            for a in range(0, k + 1):
                b = k - a
                if (a + 1) in D and b in Q:
                    acc = dadd(acc, dscal(dmul(D[a + 1], dderiv(Q[b])), a + 1))
                if a >= 1 and a in D and (b + 1) in Q:
                    acc = dadd(acc,
                               dscal(dmul(dderiv(D[a]), Q[b + 1]), -(b + 1)))
            Q[k + 1] = dscal(dmul(acc, ([inv[0]], [inv[1]])),
                             pow(k + 1, p - 2, p))
        val, eps = [], []
        for j in range(1, jmax + 1):
            A, B = Q.get(j, ([], []))
            if j in OR_:
                lo, hi = OR_[j]
                bad = [i for i in range(max(len(A), len(B)))
                       if i < lo or i > hi]
            else:
                bad = list(range(max(len(A), len(B))))
            for i in bad:
                val.append(A[i] if i < len(A) else 0)
                eps.append(B[i] if i < len(B) else 0)
        return val, eps

    best, ncond, zc = 0, None, None
    for _ in range(trials):
        vec = [rng.randrange(p) for _ in idx]
        vec[idx.index((0, 1))] = rng.randrange(1, p)
        cols = []
        for k in range(len(idx)):
            c = conds(build(vec, k))
            if c is None:
                cols = None
                break
            cols.append(c[1])
        if cols is None:
            continue
        ncond = len(cols[0])
        J = [[cols[k][r] for k in range(len(idx))] for r in range(ncond)]
        rk = rank_mod_p(J)
        if rk >= best:
            best = rk
            zc = [idx[k] for k in range(len(idx))
                  if all(J[r][k] == 0 for r in range(ncond))]
    return {"status": "OK", "flipped": flipped, "nparams": len(idx),
            "nconds": ncond, "rank": best, "zero_cols": zc,
            "dim_bound": len(idx) - best}

SHAPES = [
    Pair("(8,28) case (1) pentagons  [OPEN in GGHV]",
         [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)],
         [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)],
         [(2, 0, 1)], "degrees (72,108)"),
    Pair("(8,28) case (2) quadrilaterals  [OPEN in GGHV]",
         [(0, 0), (1, 0), (8, 14), (8, 16)],
         [(0, 0), (2, 1), (12, 21), (12, 24)],
         [(2, 0, 1)], "degrees (72,108)"),
    Pair("(9,27)  [CLOSED by GGHV Prop 4.1 + Cor 5.7]",
         [(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)],
         [(0, 0), (1, 0), (9, 24), (9, 27), (0, 27)],
         [(1, 0, 1)], "degrees (66,99); [P,Q] = x"),
]

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(seed)
    for sh in SHAPES:
        print(f"=== {sh.name}   {sh.note}")
        print(f"    N(A) j=0 row {sh.RA.get(0)}   N(B) j=0 row {sh.RB.get(0)}")
        r = run_pair(sh, rng)
        if r["status"] != "OK":
            print(f"    {r['status']}: {r['detail']}")
        else:
            print(f"    driver = {'B (roles flipped)' if r['flipped'] else 'A'}"
                  f"   params={r['nparams']}  conditions={r['nconds']}  "
                  f"exact rank={r['rank']}  dim bound={r['dim_bound']}")
            print(f"    identically-zero Jacobian columns: {r['zero_cols']}")
        print()


def _external_conds(pair, vec, k):
    """Expose run_pair's inner build+conds for external solvers (cand_hunt)."""
    o = pair.orient()
    if o is None:
        return None
    DR, OR_, rhs, flipped = o
    idx = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]
    jmax = max(max(OR_), max(DR)) + 2
    R = rhs_rows(rhs, jmax)
    def build(vec, k=None):
        D = {}
        for t, ((j, i), val) in enumerate(zip(idx, vec)):
            A, B = D.setdefault(j, ([], []))
            while len(A) <= i:
                A.append(0); B.append(0)
            A[i] = val % p
            if k is not None and t == k:
                B[i] = 1
            D[j] = (A, B)
        return {j: (trim(a), trim(b)) for j, (a, b) in D.items()}
    def conds(D):
        A0, B0 = D[0]
        p10 = (A0[1] if len(A0) > 1 else 0, B0[1] if len(B0) > 1 else 0)
        if p10[0] == 0:
            return None
        inv = dinv_scalar(*p10)
        r0 = R.get(0, [])
        Q = {0: ([0], [0]), 1: (pscal(r0, inv[0]), pscal(r0, inv[1]))}
        for kk in range(1, jmax + 1):
            acc = (list(R.get(kk, [])), [])
            for a in range(0, kk + 1):
                b = kk - a
                if (a + 1) in D and b in Q:
                    acc = dadd(acc, dscal(dmul(D[a + 1], dderiv(Q[b])), a + 1))
                if a >= 1 and a in D and (b + 1) in Q:
                    acc = dadd(acc, dscal(dmul(dderiv(D[a]), Q[b + 1]), -(b + 1)))
            Q[kk + 1] = dscal(dmul(acc, ([inv[0]], [inv[1]])), pow(kk + 1, p - 2, p))
        val, eps = [], []
        for j in range(1, jmax + 1):
            A, B = Q.get(j, ([], []))
            if j in OR_:
                lo, hi = OR_[j]
                bad = [i for i in range(max(len(A), len(B))) if i < lo or i > hi]
            else:
                bad = list(range(max(len(A), len(B))))
            for i in bad:
                val.append(A[i] if i < len(A) else 0)
                eps.append(B[i] if i < len(B) else 0)
        return val, eps
    return conds(build(vec, k))
