"""night12 -- mate search kernel.

Ring convention used throughout this lane:
  - "ring: Q"    exact rational arithmetic (python Fraction / int)
  - "ring: F_p"  the finite field with p = 999983 or p = 1000003

Core fact exploited: for FIXED P in Q[x,y], the Keller equation
    P_x Q_y - P_y Q_x = 1
is LINEAR in the coefficients of Q.  For a P-monomial c*x^p1 y^p2 and a
Q-monomial q_a * x^a1 y^a2 the product contributes exactly one term:

    c * (p1*a2 - p2*a1) * x^(p1+a1-1) y^(p2+a2-1)

so the linear system has at most |supp P| nonzeros per unknown.  The
right-hand side e is the indicator of the monomial (0,0).
"""

from fractions import Fraction
import random

P1 = 999983
P2 = 1000003
PRIMES = (P1, P2)

# ---------------------------------------------------------------- polynomials

def pmul(A, B):
    C = {}
    for a, ca in A.items():
        for b, cb in B.items():
            k = (a[0] + b[0], a[1] + b[1])
            C[k] = C.get(k, 0) + ca * cb
    return {k: v for k, v in C.items() if v != 0}


def ppow(A, n):
    R = {(0, 0): 1}
    for _ in range(n):
        R = pmul(R, A)
    return R


def padd(A, B):
    C = dict(A)
    for b, cb in B.items():
        C[b] = C.get(b, 0) + cb
    return {k: v for k, v in C.items() if v != 0}


def pdeg(A):
    return max(i + j for (i, j) in A) if A else -1


def dx(A):
    return {(i - 1, j): c * i for (i, j), c in A.items() if i > 0 and c * i != 0}


def dy(A):
    return {(i, j - 1): c * j for (i, j), c in A.items() if j > 0 and c * j != 0}


def bracket(P, Q):
    """P_x Q_y - P_y Q_x, exact (ring: Q)."""
    return padd(pmul(dx(P), dy(Q)), {k: -v for k, v in pmul(dy(P), dx(Q)).items()})


def is_one(A):
    return A == {(0, 0): 1} or (len(A) == 1 and A.get((0, 0)) == 1)


# ------------------------------------------------------------- Newton polygon

def _hull(pts):
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


def _inside(hull, pt):
    n = len(hull)
    if n == 1:
        return pt == hull[0]
    if n == 2:
        a, b = hull
        cr = (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0])
        if cr != 0:
            return False
        return (min(a[0], b[0]) <= pt[0] <= max(a[0], b[0])
                and min(a[1], b[1]) <= pt[1] <= max(a[1], b[1]))
    for i in range(n):
        a = hull[i]
        b = hull[(i + 1) % n]
        cr = (b[0] - a[0]) * (pt[1] - a[1]) - (b[1] - a[1]) * (pt[0] - a[0])
        if cr < 0:
            return False
    return True


BASE = [(0, 0), (1, 0), (0, 1)]


def q_support(P, cap_full=4000, cap_work=None):
    """Q-support: monomials of total degree <= floor(3 deg P / 2) lying in the
    (3/2)-scaled Newton polygon of P.

    The polygon is  NP(P) = conv( supp(P) u {(0,0),(1,0),(0,1)} ).  The three
    BASE points are forced in because the constant coefficient of the bracket
    is  P[1,0] Q[0,1] - P[0,1] Q[1,0]  -- without (1,0),(0,1) available to Q
    the constant 1 is unreachable for trivial support reasons rather than
    arithmetic ones.

    Scaling by 3/2 is done exactly on the doubled lattice: a is in
    (3/2)NP(P) iff 2a is in conv(3 * vertices).

    Returns (support_list, info_dict).  If the full count exceeds cap_full the
    support is thinned to the self-similar sublattice k*Z^2 (union BASE) for
    the least k making the count fit; cap_work (if given) is a further,
    purely computational cap applied the same way.
    """
    d = pdeg(P)
    D = (3 * d) // 2
    verts = _hull([(3 * a, 3 * b) for (a, b) in (list(P.keys()) + BASE)])
    full = []
    for i in range(D + 1):
        for j in range(D + 1 - i):
            if _inside(verts, (2 * i, 2 * j)):
                full.append((i, j))
    info = {"deg_P": d, "deg_Q_max": D, "n_full": len(full), "thin_k": 1}
    cap = cap_full if cap_work is None else min(cap_full, cap_work)
    if len(full) <= cap:
        info["n_used"] = len(full)
        return sorted(full), info
    k = 2
    while True:
        S = [a for a in full if a[0] % k == 0 and a[1] % k == 0]
        S = sorted(set(S) | set(b for b in BASE if b in set(full)))
        if len(S) <= cap:
            info["thin_k"] = k
            info["n_used"] = len(S)
            return S, info
        k += 1
        if k > 200:
            info["thin_k"] = k
            info["n_used"] = len(S)
            return S, info


# ------------------------------------------------------------- linear system

def build_system(P, S):
    """Rows of  P_x Q_y - P_y Q_x - 1  as a sparse map.

    Returns (rows, e_key) where rows is {monomial: {col_index: int_coeff}}
    over the integers (ring: Q), and the target vector is the indicator of
    e_key = (0,0).
    """
    rows = {}
    for jdx, (a1, a2) in enumerate(S):
        for (p1, p2), c in P.items():
            f = p1 * a2 - p2 * a1
            if f == 0:
                continue
            key = (p1 + a1 - 1, p2 + a2 - 1)
            r = rows.setdefault(key, {})
            r[jdx] = r.get(jdx, 0) + c * f
    for key in list(rows):
        rows[key] = {k: v for k, v in rows[key].items() if v != 0}
        if not rows[key]:
            del rows[key]
    return rows, (0, 0)


def _rng_vec(seed, m, p):
    import numpy as np
    g = np.random.default_rng(seed)
    return g.integers(0, p, size=m, dtype=np.int64)


def consistency_mod_p(rows, ncols, p, seed=0):
    """Decide  rank(A) vs rank([A|e])  over F_p.

    The row count is compressed by a random F_p-linear map of rank ncols+16;
    a random compression preserves both ranks with probability >= 1 - O(n/p),
    and is applied independently for each prime.

    Returns dict with rank_A, rank_Ae, consistent (bool), plus the echelon
    data needed to pull out pivot rows/columns for an exact solve.
    """
    import numpy as np
    m = ncols + 16
    # (0,0) must be present even when A's constant row is identically zero:
    # in that case the equation reads 0 = 1 and the system is inconsistent.
    keys = sorted(set(rows) | {(0, 0)})
    B = np.zeros((m, ncols + 1), dtype=np.int64)
    for t, key in enumerate(keys):
        r = _rng_vec((seed, p, t), m, p)
        for j, v in rows.get(key, {}).items():
            B[:, j] = (B[:, j] + r * (v % p)) % p
        if key == (0, 0):
            B[:, ncols] = (B[:, ncols] + r) % p   # the RHS e
    # forward elimination on [A | e]
    row = 0
    pivcols = []
    for col in range(ncols + 1):
        piv = None
        nz = np.nonzero(B[row:, col])[0]
        if nz.size == 0:
            continue
        piv = row + nz[0]
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
    rank_Ae = len(pivcols)
    rank_A = rank_Ae - (1 if (ncols in pivcols) else 0)
    return {
        "rank_A": int(rank_A),
        "rank_Ae": int(rank_Ae),
        "consistent": ncols not in pivcols,
        "pivcols": [int(c) for c in pivcols if c != ncols],
        "n_rows_nonzero": len(keys),
    }


# ------------------------------------------------------------- exact solving

def exact_solve(rows, ncols, S, pivcols):
    """Exact rational solve (ring: Q).

    Restricted to the pivot columns found mod p: all other unknowns are set
    to 0.  Any Q produced is then verified by direct bracket expansion over
    Q, so the modular pivot choice is only a heuristic for *finding* a
    solution and never part of the certificate.
    """
    cols = list(pivcols)
    cidx = {c: t for t, c in enumerate(cols)}
    keys = sorted(set(rows) | {(0, 0)})
    M = []
    for key in keys:
        r = rows.get(key, {})
        vec = [Fraction(0)] * (len(cols) + 1)
        touched = False
        for j, v in r.items():
            if j in cidx:
                vec[cidx[j]] = Fraction(v)
                touched = True
        if key == (0, 0):
            vec[-1] = Fraction(1)
            touched = True
        elif not touched:
            continue
        # a row with support entirely outside the pivot columns and zero rhs
        # is 0 = 0 and may be dropped; a row with nonzero rhs and no support
        # is an exact obstruction.
        M.append(vec)
    n = len(cols)
    r0 = 0
    where = []
    for c in range(n):
        piv = None
        for i in range(r0, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            where.append(None)
            continue
        M[r0], M[piv] = M[piv], M[r0]
        pr = M[r0]
        inv = Fraction(1) / pr[c]
        M[r0] = [v * inv for v in pr]
        pr = M[r0]
        for i in range(len(M)):
            if i != r0 and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], pr)]
        where.append(r0)
        r0 += 1
    for i in range(r0, len(M)):
        if M[i][-1] != 0 and all(v == 0 for v in M[i][:-1]):
            return None, "inconsistent_exact"
    sol = [Fraction(0)] * n
    for c in range(n):
        if where[c] is not None:
            sol[c] = M[where[c]][-1]
    Qd = {}
    for t, c in enumerate(cols):
        if sol[t] != 0:
            Qd[S[c]] = sol[t]
    return Qd, "ok"


def divisibility_ordered(a, b):
    if a <= 0 or b <= 0:
        return None
    return (a % b == 0) or (b % a == 0)
