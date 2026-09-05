"""night6 -- characteristic-zero integration test by EXACT LINEAR ALGEBRA.

Structural observation that makes the char-0 question cheap: with the face
solution (q,t) and the kernel element (p_,s_) fixed, two of the three
identities are AFFINE-LINEAR in the unknowns (f, g, r):

    E1:  2f's_ + p_'r - p_ r' - 2q g'          = 0      linear in f, g, r
    E2:  3f't + 2p_'s_ + q'r - p_ s_' - 2q r'  = 0      linear in f, r,
                                                        inhomogeneous term
                                                        2p_'s_ - p_ s_'
    E0:  f'r - p_ g'                           = 0      quadratic (f*r)

E1 and E2 give 19 rows each, so 38 affine-linear equations in the 32 unknowns
f_1..f_8, g_1..g_12, r_1..r_12 -- overdetermined by 6.  If that linear system
is already inconsistent over the number field K = Q[T]/(h), the chart is
empty, E0 is not needed, and both variants (free, and with the Rabinowitsch
vertex non-degeneracy) are empty a fortiori, since imposing more conditions
cannot create solutions.

Inconsistency is certified here, not asserted: the row operations are tracked
on an appended identity block, so the reduction produces an explicit vector c
with

        c . M = 0   and   c . b = 1

and that identity is then re-verified against the ORIGINAL rows in exact
arithmetic.  A Groebner engine is not used anywhere in this module.

    chart A :  (p_,s_) = v1 + be*v2   (alpha = 1, beta = be a free unknown)
    chart B :  (p_,s_) = v2           (alpha = 0, beta = 1)
    control :  (p_,s_) = (0,0)        (the handoff's section 3d branch)

Chart A carries the unknown `be`.  There the 38 x 33 augmented matrix N(be)
has entries polynomial in `be` (degree <= 1 in the coefficient block, <= 2 in
the right-hand column), so a 33 x 33 minor of N is a polynomial in `be` of
degree <= 34; each such minor is obtained exactly by evaluating the
determinant over K at 35+ rational values of `be` and interpolating.  The
chart-A linear system is inconsistent for EVERY value of `be` iff some family
of these minors has no common root, i.e. iff their gcd in K[be] is a nonzero
constant.
"""
import os, sys, time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_lib as C

FIDX = list(range(1, 9))
GIDX = list(range(1, 13))
RIDX = list(range(1, 13))
NAMES = (["f%d" % i for i in FIDX] + ["g%d" % j for j in GIDX]
         + ["r%d" % k for k in RIDX])
IDX = {n: i for i, n in enumerate(NAMES)}
NC = len(NAMES)


def uderiv(d, K):
    return {k - 1: K.smul(k, v) for k, v in d.items() if k > 0}


def build_rows(q, t, pv, sv, K):
    """Return (M, b, labels): 38 rows of E1 and E2, M x = b, over K."""
    pd, sd = uderiv(pv, K), uderiv(sv, K)
    qd = uderiv(q, K)
    M, b, labels = [], [], []

    # E1 : 2 f' s_ + p_' r - p_ r' - 2 q g'  = 0
    for k in range(1, 20):
        row = [K.zero] * NC
        for i in FIDX:
            for j, sj in sv.items():
                if i - 1 + j == k:
                    c = IDX["f%d" % i]
                    row[c] = K.add(row[c], K.smul(2 * i, sj))
        for m in RIDX:
            c = IDX["r%d" % m]
            for i, pi in pd.items():
                if i + m == k:
                    row[c] = K.add(row[c], pi)
            for i, pi in pv.items():
                if i + m - 1 == k:
                    row[c] = K.sub(row[c], K.smul(m, pi))
        for j in GIDX:
            c = IDX["g%d" % j]
            for i, qi in q.items():
                if i + j - 1 == k:
                    row[c] = K.sub(row[c], K.smul(2 * j, qi))
        M.append(row)
        b.append(K.zero)
        labels.append("E1:u^%d" % k)

    # E2 : 3 f' t + 2 p_' s_ + q' r - p_ s_' - 2 q r'  = 0
    for k in range(1, 20):
        row = [K.zero] * NC
        for i in FIDX:
            for j, tj in t.items():
                if i - 1 + j == k:
                    c = IDX["f%d" % i]
                    row[c] = K.add(row[c], K.smul(3 * i, tj))
        for m in RIDX:
            c = IDX["r%d" % m]
            for i, qi in qd.items():
                if i + m == k:
                    row[c] = K.add(row[c], qi)
            for i, qi in q.items():
                if i + m - 1 == k:
                    row[c] = K.sub(row[c], K.smul(2 * m, qi))
        cst = K.zero
        for i, pi in pd.items():
            for j, sj in sv.items():
                if i + j == k:
                    cst = K.add(cst, K.smul(2, K.mul(pi, sj)))
        for i, pi in pv.items():
            for j, sj in sd.items():
                if i + j == k:
                    cst = K.sub(cst, K.mul(pi, sj))
        M.append(row)
        b.append(K.sub(K.zero, cst))       # M x = -constant term
        labels.append("E2:u^%d" % k)
    return M, b, labels


def rref_tracked(M, b, K):
    """Row-reduce [M | b] carrying an identity block.

    Returns (rank, rows_of_the_reduced_system, transform, pivots).
    transform[i] is the combination of ORIGINAL rows giving reduced row i.
    """
    m, n = len(M), len(M[0])
    A = [list(M[i]) + [b[i]] + [K.one if j == i else K.zero
                                for j in range(m)] for i in range(m)]
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, m) if not K.iszero(A[i][c])), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = K.inv(A[r][c])
        A[r] = [K.mul(v, iv) for v in A[r]]
        for i in range(m):
            if i != r and not K.iszero(A[i][c]):
                f = A[i][c]
                A[i] = [K.sub(u, K.mul(f, v)) for u, v in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    coef = [row[:n] for row in A]
    rhs = [row[n] for row in A]
    tr = [row[n + 1:] for row in A]
    return r, coef, rhs, tr, piv


def inconsistent_rows(coef, rhs, K):
    return [i for i in range(len(coef))
            if all(K.iszero(v) for v in coef[i]) and not K.iszero(rhs[i])]


def verify_certificate(c, M, b, K):
    """check c.M = 0 and c.b != 0 against the ORIGINAL rows"""
    n = len(M[0])
    bad = 0
    for j in range(n):
        acc = K.zero
        for i, ci in enumerate(c):
            if not K.iszero(ci):
                acc = K.add(acc, K.mul(ci, M[i][j]))
        if not K.iszero(acc):
            bad += 1
    rhs = K.zero
    for i, ci in enumerate(c):
        if not K.iszero(ci):
            rhs = K.add(rhs, K.mul(ci, b[i]))
    return bad == 0, not K.iszero(rhs), K.show(rhs)


# ---------------------------------------------------------------- determinants
def det_K(rows, K):
    """determinant of a square matrix over K, fraction-free-free (Gauss)."""
    n = len(rows)
    A = [list(r) for r in rows]
    det = K.one
    for c in range(n):
        pr = next((i for i in range(c, n) if not K.iszero(A[i][c])), None)
        if pr is None:
            return K.zero
        if pr != c:
            A[c], A[pr] = A[pr], A[c]
            det = K.sub(K.zero, det)
        det = K.mul(det, A[c][c])
        iv = K.inv(A[c][c])
        A[c] = [K.mul(v, iv) for v in A[c]]
        for i in range(c + 1, n):
            if not K.iszero(A[i][c]):
                f = A[i][c]
                A[i] = [K.sub(u, K.mul(f, v)) for u, v in zip(A[i], A[c])]
    return det


def interpolate(xs, ys, K):
    """Lagrange interpolation over K at rational nodes xs -> coefficient list"""
    n = len(xs)
    coeffs = [K.zero] * n
    for i in range(n):
        # basis polynomial prod_{j != i} (X - x_j) / (x_i - x_j)
        num = [K.one] + [K.zero] * (n - 1)
        deg = 0
        den = K.one
        for j in range(n):
            if j == i:
                continue
            new = [K.zero] * n
            for d in range(deg + 1):
                new[d + 1] = K.add(new[d + 1], num[d])
                new[d] = K.sub(new[d], K.smul(xs[j], num[d]))
            num = new
            deg += 1
            den = K.mul(den, K.c(xs[i] - xs[j]))
        f = K.mul(ys[i], K.inv(den))
        for d in range(n):
            coeffs[d] = K.add(coeffs[d], K.mul(num[d], f))
    while coeffs and K.iszero(coeffs[-1]):
        coeffs.pop()
    return coeffs


def poly_gcd_K(a, b, K):
    """gcd in K[X] of coefficient lists (low -> high), returned monic"""
    a, b = list(a), list(b)
    while b:
        while b and K.iszero(b[-1]):
            b.pop()
        if not b:
            break
        # a mod b
        while len(a) >= len(b) and any(not K.iszero(v) for v in a):
            while a and K.iszero(a[-1]):
                a.pop()
            if len(a) < len(b):
                break
            f = K.mul(a[-1], K.inv(b[-1]))
            sh = len(a) - len(b)
            for i, bv in enumerate(b):
                a[i + sh] = K.sub(a[i + sh], K.mul(f, bv))
            while a and K.iszero(a[-1]):
                a.pop()
        a, b = b, a
    while a and K.iszero(a[-1]):
        a.pop()
    if not a:
        return []
    iv = K.inv(a[-1])
    return [K.mul(v, iv) for v in a]


# ------------------------------------------------------------------- chart A
def chartA_pv_sv(pv1, sv1, pv2, sv2, be, K):
    """(p_,s_) = v1 + be*v2 at a rational value of be"""
    c = K.c(be)
    pv = {i: K.add(pv1[i], K.mul(c, pv2[i])) for i in pv1}
    sv = {j: K.add(sv1[j], K.mul(c, sv2[j])) for j in sv1}
    return pv, sv


def minor_poly(rows_subset, q, t, pv1, sv1, pv2, sv2, K, nodes):
    """determinant of the 33 x 33 augmented minor as a polynomial in be.

    The entries of the coefficient block are of degree <= 1 in be and the
    right-hand column of degree <= 2, so the determinant has degree <= 34;
    it is recovered exactly by interpolation through `nodes` rational values.
    """
    xs, ys = [], []
    for x in nodes:
        pv, sv = chartA_pv_sv(pv1, sv1, pv2, sv2, x, K)
        M, b, labels = build_rows(q, t, pv, sv, K)
        sub = [[M[i][j] for j in range(len(M[0]))] + [b[i]]
               for i in rows_subset]
        xs.append(F(x))
        ys.append(det_K(sub, K))
    return interpolate(xs, ys, K), xs, ys
