"""Weighted-homogeneous form of the face system, and its solution.

With q = u*A (deg A = 7) and t = u^2*B (deg B = 10), the face equation
2qt' - 3q't = u^2 reads

    sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m == 0],     m = 0..17,

the m=17 row vanishing identically.  Gauge A_0 = 1 (the A->cA, B->B/c
scaling).  Assign weight k to A_k and weight m to B_m: this is exactly the
u -> lambda*u gauge, under which the whole system is weighted-homogeneous.
Rows m = 0..10 determine B_0..B_10 as weighted-homogeneous polynomials of
weight m in A_1..A_7; rows m = 11..16 are 6 residual weighted-homogeneous
equations of weights 11..16 in A_1..A_7.

Their common zero locus is a union of G_m-orbits.  The orbit invariant
X = A_7 / A_1^7 satisfies a univariate equation, extracted here from a
weighted-degree-d Macaulay matrix (FLINT rref); the remaining coordinates
come out of the same matrices as A_k / A_1^k = (rational function of X).
"""
import flint

NV = 7                      # A_1..A_7, index k-1
W = [1, 2, 3, 4, 5, 6, 7]   # weights


def wdeg(m):
    return sum(w * e for w, e in zip(W, m))


def mons_of_weight(d, nv=NV, weights=None):
    ws = weights or W
    out = []

    def rec(k, rem, cur):
        if k == nv:
            if rem == 0:
                out.append(tuple(cur))
            return
        w = ws[k]
        e = 0
        while e * w <= rem:
            rec(k + 1, rem - e * w, cur + [e])
            e += 1
    rec(0, d, [])
    return out


def padd(a, b, p):
    r = dict(a)
    for m, c in b.items():
        v = (r.get(m, 0) + c) % p
        if v:
            r[m] = v
        else:
            r.pop(m, None)
    return r


def pmul(a, b, p):
    r = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(x + y for x, y in zip(m1, m2))
            v = (r.get(m, 0) + c1 * c2) % p
            if v:
                r[m] = v
            else:
                r.pop(m, None)
    return r


def Avar(k):
    e = [0] * NV
    if k >= 1:
        e[k - 1] = 1
    return {tuple(e): 1}


def build(p):
    """Return (B_0..B_10, residuals m=11..16) as polys in A_1..A_7."""
    one = {(0,) * NV: 1}
    A = {0: one}
    for k in range(1, 8):
        A[k] = Avar(k)
    B = {}
    for m in range(0, 11):
        c0 = (1 + 2 * m) % p
        acc = dict(one) if m == 0 else {}
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = (1 + 2 * j - 3 * i) % p
            if c:
                term = pmul(A[i], B[j], p)
                acc = padd(acc, {k: (-c * v) % p for k, v in term.items()}, p)
        inv = pow(c0, p - 2, p)
        B[m] = {k: v * inv % p for k, v in acc.items()}
        assert all(wdeg(k) == m for k in B[m]), ("B_%d not weight-homogeneous" % m)
    res = []
    for m in range(11, 18):
        acc = {}
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = (1 + 2 * j - 3 * i) % p
                if c:
                    term = pmul(A[i], B[j], p)
                    acc = padd(acc, {k: c * v % p for k, v in term.items()}, p)
        if m < 17:
            assert all(wdeg(k) == m for k in acc), "residual not weight-homog"
        res.append(acc)
    assert res[-1] == {}, "m=17 row is not identically zero"
    return B, res[:-1]


def macaulay(res, d, p, tail_mons):
    """Rows of the weighted-degree-d Macaulay matrix, reduced; return the
    rows supported only on `tail_mons` (a list of monomials placed last)."""
    mons = mons_of_weight(d)
    tailset = set(tail_mons)
    others = [m for m in mons if m not in tailset]
    tail = [m for m in tail_mons if m in set(mons)]
    cols = others + tail
    cidx = {m: i for i, m in enumerate(cols)}
    rows = []
    for f in res:
        w = wdeg(next(iter(f)))
        if w > d:
            continue
        for m in mons_of_weight(d - w):
            row = {}
            for k, c in f.items():
                row[cidx[tuple(x + y for x, y in zip(k, m))]] = c % p
            rows.append(row)
    if not rows:
        return [], tail, 0, len(cols)
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
    return out, tail, len(rows), len(cols)


def pure_mons(d, k=7):
    """monomials A_1^a * A_k^b of weight d, listed by increasing b"""
    out = []
    b = 0
    while b * k <= d:
        e = [0] * NV
        e[k - 1] += b
        e[0] += d - b * k
        out.append(tuple(e))
        b += 1
    return out
