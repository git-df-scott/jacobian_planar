"""Affine weighted-degree Macaulay elimination for the face system.

Variables A_2..A_7 with weights 2..7 (gauge A_0 = A_1 = 1).  The six
residual equations have weighted degrees 11..16.  Columns are the monomials
of weighted degree <= D, with the pure powers A_7^b placed last; rref then
exposes any univariate polynomial in A_7 lying in the degree-D span.
"""
import sys, time
import flint

NV = 6
WT = [2, 3, 4, 5, 6, 7]      # weight of A_{k} is k, k = 2..7


def wdeg(m):
    return sum(w * e for w, e in zip(WT, m))


def mons_upto(D):
    out = []

    def rec(k, rem, cur):
        if k == NV:
            out.append(tuple(cur))
            return
        e = 0
        while e * WT[k] <= rem:
            rec(k + 1, rem - e * WT[k], cur + [e])
            e += 1
    rec(0, D, [])
    return out


def dehomogenise(res_h):
    """weighted-homogeneous polys in A_1..A_7  ->  polys in A_2..A_7 (A_1=1)"""
    out = []
    for f in res_h:
        g = {}
        for m, c in f.items():
            mm = tuple(m[1:])
            g[mm] = (g.get(mm, 0) + c)
        out.append({m: c for m, c in g.items() if c})
    return out


def macaulay_pure(eqs, D, p, target=5, wtarget=7):
    mons = mons_upto(D)
    pure = []
    b = 0
    while b * wtarget <= D:
        e = [0] * NV
        e[target] = b
        pure.append(tuple(e))
        b += 1
    pureset = set(pure)
    others = [m for m in mons if m not in pureset]
    cols = others + pure
    cidx = {m: i for i, m in enumerate(cols)}
    rows = []
    for f in eqs:
        w = max(wdeg(m) for m in f)
        for m in mons_upto(D - w):
            row = {}
            for k, c in f.items():
                mm = tuple(x + y for x, y in zip(k, m))
                row[cidx[mm]] = c % p
            rows.append(row)
    M = flint.nmod_mat(len(rows), len(cols), p)
    for r, row in enumerate(rows):
        for c, v in row.items():
            if v:
                M[r, c] = v
    R, rank = M.rref()
    start = len(others)

    def pivot(r):
        for c in range(len(cols)):
            if R[r, c]:
                return c
        return len(cols)

    lo, hi = 0, rank
    while lo < hi:
        mid = (lo + hi) // 2
        if pivot(mid) >= start:
            hi = mid
        else:
            lo = mid + 1
    out = [[int(R[r, c]) for c in range(start, len(cols))] for r in range(lo, rank)]
    return out, len(rows), len(cols), rank


def macaulay_tail(eqs, D, p, tail):
    """generic version: `tail` is an explicit list of monomials placed last."""
    mons = mons_upto(D)
    tset = set(tail)
    tl = [m for m in tail if m in set(mons)]
    others = [m for m in mons if m not in tset]
    cols = others + tl
    cidx = {m: i for i, m in enumerate(cols)}
    rows = []
    for f in eqs:
        w = max(wdeg(m) for m in f)
        for m in mons_upto(D - w):
            row = {}
            for k, c in f.items():
                row[cidx[tuple(x + y for x, y in zip(k, m))]] = c % p
            rows.append(row)
    M = flint.nmod_mat(len(rows), len(cols), p)
    for r, row in enumerate(rows):
        for c, v in row.items():
            if v:
                M[r, c] = v
    R, rank = M.rref()
    start = len(others)

    def pivot(r):
        for c in range(len(cols)):
            if R[r, c]:
                return c
        return len(cols)

    lo, hi = 0, rank
    while lo < hi:
        mid = (lo + hi) // 2
        if pivot(mid) >= start:
            hi = mid
        else:
            lo = mid + 1
    return ([[int(R[r, c]) for c in range(start, len(cols))]
             for r in range(lo, rank)], tl)
