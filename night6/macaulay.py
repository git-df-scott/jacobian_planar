"""Macaulay-matrix elimination over F_p (FLINT rref), used to extract a
univariate eliminant of a 0-dimensional ideal without a Groebner basis.

Build all monomial multiples m*f of the generators with deg(m*f) <= D, order
the columns so that the pure powers of the target variable come LAST, row
reduce, and read off any row supported only on that final block: such a row
is a univariate polynomial in the target variable lying in the ideal.
"""
import flint
from itertools import combinations


def monomials_upto(nv, d):
    """all exponent tuples with total degree <= d"""
    out = []

    def rec(prefix, rem, k):
        if k == nv - 1:
            for e in range(rem + 1):
                out.append(tuple(prefix + [e]))
            return
        for e in range(rem + 1):
            rec(prefix + [e], rem - e, k + 1)
    rec([], d, 0)
    return out


def mmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def total_degree(f):
    return max(sum(m) for m in f)


def _pivot(R, r, ncol):
    for c in range(ncol):
        if R[r, c]:
            return c
    return ncol


def _first_row_with_pivot_ge(R, rank, ncol, start):
    lo, hi = 0, rank
    while lo < hi:
        mid = (lo + hi) // 2
        if _pivot(R, mid, ncol) >= start:
            hi = mid
        else:
            lo = mid + 1
    return lo


def eliminant(polys, nv, p, D, target):
    """Return the coefficient list (low->high) of the lowest-degree univariate
    polynomial in variable `target` found in the degree-D Macaulay span, or
    None."""
    mons = monomials_upto(nv, D)
    pure = []
    for e in range(D + 1):
        t = [0] * nv
        t[target] = e
        pure.append(tuple(t))
    pureset = set(pure)
    others = [m for m in mons if m not in pureset]
    cols = others + pure                       # pure powers last
    cidx = {m: i for i, m in enumerate(cols)}
    ncol = len(cols)

    rows = []
    for f in polys:
        d = total_degree(f)
        if d > D:
            continue
        for m in monomials_upto(nv, D - d):
            row = {}
            for k, c in f.items():
                row[cidx[mmul(k, m)]] = c % p
            rows.append(row)
    nrow = len(rows)
    M = flint.nmod_mat(nrow, ncol, p)
    for r, row in enumerate(rows):
        for c, v in row.items():
            if v:
                M[r, c] = v
    R, rank = M.rref()
    start = len(others)
    best = None
    r0 = _first_row_with_pivot_ge(R, rank, ncol, start)
    for r in range(r0, rank):
        coeffs = [int(R[r, start + e]) for e in range(D + 1)]
        while coeffs and coeffs[-1] == 0:
            coeffs.pop()
        if coeffs and (best is None or len(coeffs) < len(best)):
            best = coeffs
    return best, nrow, ncol, rank


def relation_rows(polys, nv, p, D, target, extra):
    """Rows supported on {pure powers of target} U {the single monomial
    `extra`}: gives  c*extra = univariate(target)."""
    mons = monomials_upto(nv, D)
    pure = []
    for e in range(D + 1):
        t = [0] * nv
        t[target] = e
        pure.append(tuple(t))
    tail = pure + [extra]
    tailset = set(tail)
    others = [m for m in mons if m not in tailset]
    cols = others + tail
    cidx = {m: i for i, m in enumerate(cols)}
    ncol = len(cols)
    rows = []
    for f in polys:
        d = total_degree(f)
        if d > D:
            continue
        for m in monomials_upto(nv, D - d):
            row = {}
            for k, c in f.items():
                row[cidx[mmul(k, m)]] = c % p
            rows.append(row)
    nrow = len(rows)
    M = flint.nmod_mat(nrow, ncol, p)
    for r, row in enumerate(rows):
        for c, v in row.items():
            if v:
                M[r, c] = v
    R, rank = M.rref()
    start = len(others)
    out = []
    r0 = _first_row_with_pivot_ge(R, rank, ncol, start)
    for r in range(r0, rank):
        out.append([int(R[r, c]) for c in range(start, ncol)])
    return out, cols[start:]
