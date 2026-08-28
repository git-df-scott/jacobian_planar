"""night13 -- kernel for the compressed cusp prestratum at degrees (84, 126).

Ring / characteristic conventions used throughout this lane (every recorded
number in night13/PRESTRATUM.md carries one of these labels):

  ring: Z          exact integer arithmetic (python int), used for the
                   Newton-polygon combinatorics and for the symbolic
                   identity checks with integer parameter values
  ring: Q          exact rational arithmetic (fractions.Fraction), used only
                   for rational reconstruction / exact verification
  char p           the prime fields F_p with p = 999983 and p = 1000003

Nothing in this file draws a conclusion; it only computes.
"""

from fractions import Fraction

P1 = 999983
P2 = 1000003
PRIMES = (P1, P2)

# --------------------------------------------------------------- polynomials
# A polynomial is a dict {(i, j): coeff} with no zero coefficients.


def pmul(A, B, mod=None):
    C = {}
    for a, ca in A.items():
        for b, cb in B.items():
            k = (a[0] + b[0], a[1] + b[1])
            C[k] = C.get(k, 0) + ca * cb
    if mod:
        return {k: v % mod for k, v in C.items() if v % mod}
    return {k: v for k, v in C.items() if v != 0}


def ppow(A, n, mod=None):
    R = {(0, 0): 1}
    for _ in range(n):
        R = pmul(R, A, mod)
    return R


def padd(A, B, mod=None):
    C = dict(A)
    for b, cb in B.items():
        C[b] = C.get(b, 0) + cb
    if mod:
        return {k: v % mod for k, v in C.items() if v % mod}
    return {k: v for k, v in C.items() if v != 0}


def pscale(A, c, mod=None):
    if mod:
        return {k: (v * c) % mod for k, v in A.items() if (v * c) % mod}
    return {k: v * c for k, v in A.items() if v * c != 0}


def pdeg(A):
    return max(i + j for (i, j) in A) if A else -1


def dx(A, mod=None):
    R = {(i - 1, j): c * i for (i, j), c in A.items() if i > 0}
    if mod:
        return {k: v % mod for k, v in R.items() if v % mod}
    return {k: v for k, v in R.items() if v != 0}


def dy(A, mod=None):
    R = {(i, j - 1): c * j for (i, j), c in A.items() if j > 0}
    if mod:
        return {k: v % mod for k, v in R.items() if v % mod}
    return {k: v for k, v in R.items() if v != 0}


def bracket(P, Q, mod=None):
    """P_x Q_y - P_y Q_x."""
    T1 = pmul(dx(P, mod), dy(Q, mod), mod)
    T2 = pmul(dy(P, mod), dx(Q, mod), mod)
    return padd(T1, pscale(T2, -1, mod), mod)


# ------------------------------------------------------------- Newton polygon

def hull(pts):
    """Monotone chain, exact integer arithmetic (ring: Z).  Counter-clockwise."""
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def inside(hl, pt):
    n = len(hl)
    if n == 1:
        return pt == hl[0]
    if n == 2:
        a, b = hl
        cr = (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0])
        if cr != 0:
            return False
        return (min(a[0], b[0]) <= pt[0] <= max(a[0], b[0])
                and min(a[1], b[1]) <= pt[1] <= max(a[1], b[1]))
    for i in range(n):
        a = hl[i]
        b = hl[(i + 1) % n]
        if (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0]) < 0:
            return False
    return True


def lattice_in(hl, dmax, res_mod=3, res=None, deg_lt=None):
    """All (i, j) with i + j <= dmax inside the hull, optional i = res (mod
    res_mod) and optional strict total-degree bound i + j < deg_lt."""
    out = []
    for i in range(dmax + 1):
        if res is not None and i % res_mod != res:
            continue
        for j in range(dmax + 1 - i):
            if deg_lt is not None and i + j >= deg_lt:
                continue
            if inside(hl, (i, j)):
                out.append((i, j))
    return out


# ------------------------------------------------- dense mod-p linear algebra

def rank_modp(rows, ncols, p, seed=0, augment=False):
    """rank of the sparse matrix `rows` = {rowkey: {col: val}} over F_p.

    The row count is compressed by a random F_p-linear map onto ncols + 16
    rows.  A random compression preserves the rank with probability
    >= 1 - O(n/p); it is drawn afresh per (seed, p).

    If augment is True an extra final column carrying the indicator of the
    row key (0, 0) is appended (the right-hand side e of the Keller equation)
    and the returned dict also reports the augmented rank and consistency.
    """
    import numpy as np
    m = ncols + 16
    keys = sorted(set(rows) | {(0, 0)}) if augment else sorted(rows)
    w = ncols + (1 if augment else 0)
    B = np.zeros((m, w), dtype=np.int64)
    g = np.random.default_rng((seed, p, len(keys), ncols))
    for key in keys:
        r = g.integers(0, p, size=m, dtype=np.int64)
        for j, v in rows.get(key, {}).items():
            v %= p
            if v:
                B[:, j] = (B[:, j] + r * v) % p
        if augment and key == (0, 0):
            B[:, ncols] = (B[:, ncols] + r) % p
    row = 0
    pivcols = []
    for col in range(w):
        nz = np.nonzero(B[row:, col])[0]
        if nz.size == 0:
            continue
        piv = row + int(nz[0])
        if piv != row:
            B[[row, piv]] = B[[piv, row]]
        inv = pow(int(B[row, col]), p - 2, p)
        B[row] = (B[row] * inv) % p
        if nz.size > 1:
            sub = B[row + 1:]
            f = sub[:, col].copy()
            mask = f != 0
            if mask.any():
                sub[mask] = (sub[mask] - f[mask, None] * B[row][None, :]) % p
        pivcols.append(col)
        row += 1
        if row >= m:
            break
    if not augment:
        return {"rank": len(pivcols), "pivcols": [int(c) for c in pivcols],
                "n_rows_nonzero": len(keys)}
    rank_Ae = len(pivcols)
    rank_A = rank_Ae - (1 if ncols in pivcols else 0)
    return {"rank_A": int(rank_A), "rank_Ae": int(rank_Ae),
            "consistent": ncols not in pivcols,
            "pivcols": [int(c) for c in pivcols if c != ncols],
            "n_rows_nonzero": len(keys)}


def solve_modp(rows, ncols, p, cols=None):
    """Exact solve of  A z = e  over F_p on the given columns (default: all).

    Returns (solution dict {col: value}, status).  No compression is used
    here: every row is kept, so the returned vector satisfies every equation
    of the system, not a random combination of them.
    """
    import numpy as np
    cols = list(range(ncols)) if cols is None else list(cols)
    cidx = {c: t for t, c in enumerate(cols)}
    keys = sorted(set(rows) | {(0, 0)})
    n = len(cols)
    M = np.zeros((len(keys), n + 1), dtype=np.int64)
    for t, key in enumerate(keys):
        for j, v in rows.get(key, {}).items():
            if j in cidx:
                M[t, cidx[j]] = v % p
        if key == (0, 0):
            M[t, n] = 1
    row = 0
    where = [None] * n
    for c in range(n):
        nz = np.nonzero(M[row:, c])[0]
        if nz.size == 0:
            continue
        piv = row + int(nz[0])
        if piv != row:
            M[[row, piv]] = M[[piv, row]]
        inv = pow(int(M[row, c]), p - 2, p)
        M[row] = (M[row] * inv) % p
        f = M[:, c].copy()
        f[row] = 0
        mask = f != 0
        if mask.any():
            M[mask] = (M[mask] - f[mask, None] * M[row][None, :]) % p
        where[c] = row
        row += 1
        if row >= len(keys):
            break
    for t in range(row, len(keys)):
        if M[t, n] % p and not M[t, :n].any():
            return None, "inconsistent"
    sol = {}
    for c in range(n):
        if where[c] is not None:
            v = int(M[where[c], n]) % p
            if v:
                sol[cols[c]] = v
    return sol, "ok"


def ratrecon(a, m):
    """Rational reconstruction of a/1 mod m with |num|,|den| <= sqrt(m/2).
    Returns Fraction or None (ring: Q from char-p data)."""
    a %= m
    bound = int((m // 2) ** 0.5)
    r0, r1 = m, a
    s0, s1 = 0, 1
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    from math import gcd
    if gcd(abs(s1), abs(r1)) != 1:
        return None
    return Fraction(r1 if s1 > 0 else -r1, abs(s1))


def divisibility_ordered(a, b):
    return (a % b == 0) or (b % a == 0)
