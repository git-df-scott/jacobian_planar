"""night6 -- characteristic zero: BOTH charts at once, by a binary form.

Structure that settles the projective question without any elimination in be.

Write the kernel element as (p_, s_) = alpha*(p1,s1) + beta*(p2,s2).  Among the
three identities, E2

        3f't + 2p_'s_ + q'r - p_ s_' - 2q r'  = 0                (19 rows)

is affine-linear in (f, r) -- g does not occur in it at all -- and, crucially,
its COEFFICIENT matrix

        f_i  ->  3i t_{k-i+1},     r_m  ->  (q'r - 2q r')_k

does not involve (p_, s_) at all: the whole dependence on (alpha,beta) sits in
the inhomogeneous term

        2p_'s_ - p_ s_'
          = alpha^2 (2p1's1 - p1 s1')
          + alpha*beta (2p1's2 + 2p2's1 - p1 s2' - p2 s1')
          + beta^2 (2p2's2 - p2 s2')

So: 19 equations, 20 unknowns (f_1..f_8, r_1..r_12), a fixed coefficient
matrix M_E2 over K of rank 18, hence a left null space of dimension 1 (or
more).  For every left null vector c the system can only be consistent if

        Q_c(alpha,beta)  =  c . b(alpha,beta)  =  0,

a BINARY QUADRATIC FORM in (alpha,beta) with coefficients in K.  That is a
necessary condition for the full system E0,E1,E2 to have a solution, so:

    the identities have no solution at any (alpha,beta) outside the common
    zero locus of the forms Q_c in P^1.

If the Q_c have no common zero in P^1 over the algebraic closure, then
(alpha,beta) = (0,0) is forced -- chart A and chart B, free and Rabinowitsch
variants alike, since extra conditions only remove solutions.

Every step is exact linear algebra over K = Q[T]/(h); no Groebner engine.
"""
import os, sys, json, time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_lib as C

FIDX = list(range(1, 9))
RIDX = list(range(1, 13))
FRNAMES = ["f%d" % i for i in FIDX] + ["r%d" % k for k in RIDX]
FRIDX = {n: i for i, n in enumerate(FRNAMES)}


def uderiv(d, K):
    return {k - 1: K.smul(k, v) for k, v in d.items() if k > 0}


def e2_coeff_matrix(q, t, K):
    """the 19 x 20 coefficient matrix of E2 in (f, r).  No (p_,s_) in it."""
    qd = uderiv(q, K)
    M = []
    for k in range(1, 20):
        row = [K.zero] * len(FRNAMES)
        for i in FIDX:
            for j, tj in t.items():
                if i - 1 + j == k:
                    c = FRIDX["f%d" % i]
                    row[c] = K.add(row[c], K.smul(3 * i, tj))
        for m in RIDX:
            c = FRIDX["r%d" % m]
            for i, qi in qd.items():
                if i + m == k:
                    row[c] = K.add(row[c], qi)
            for i, qi in q.items():
                if i + m - 1 == k:
                    row[c] = K.sub(row[c], K.smul(2 * m, qi))
        M.append(row)
    return M


def bilinear_rhs(pa, sa, pb, sb, K):
    """the u^k coefficients of  2 pa' sb - pa sb'  as a 19-vector"""
    pad = uderiv(pa, K)
    sbd = uderiv(sb, K)
    out = [K.zero] * 19
    for i, pi in pad.items():
        for j, sj in sb.items():
            if 1 <= i + j <= 19:
                out[i + j - 1] = K.add(out[i + j - 1], K.smul(2, K.mul(pi, sj)))
    for i, pi in pa.items():
        for j, sj in sbd.items():
            if 1 <= i + j <= 19:
                out[i + j - 1] = K.sub(out[i + j - 1], K.mul(pi, sj))
    return out


def rhs_forms(pv1, sv1, pv2, sv2, K):
    """(b11, b12, b22): b(alpha,beta) = -(2p_'s_ - p_ s_') expanded"""
    A = bilinear_rhs(pv1, sv1, pv1, sv1, K)
    Bc = [K.add(x, y) for x, y in
          zip(bilinear_rhs(pv1, sv1, pv2, sv2, K),
              bilinear_rhs(pv2, sv2, pv1, sv1, K))]
    Cc = bilinear_rhs(pv2, sv2, pv2, sv2, K)
    neg = lambda v: [K.sub(K.zero, x) for x in v]
    return neg(A), neg(Bc), neg(Cc)


def left_nullspace(M, K):
    """vectors c with c.M = 0, M given by rows"""
    m, n = len(M), len(M[0])
    A = [list(M[i]) + [K.one if j == i else K.zero for j in range(m)]
         for i in range(m)]
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
    null = [A[i][n:] for i in range(r, m)]
    return r, null


def verify_left_null(c, M, K):
    for j in range(len(M[0])):
        acc = K.zero
        for i, ci in enumerate(c):
            if not K.iszero(ci):
                acc = K.add(acc, K.mul(ci, M[i][j]))
        if not K.iszero(acc):
            return False
    return True


def pair(c, v, K):
    acc = K.zero
    for ci, vi in zip(c, v):
        if not K.iszero(ci):
            acc = K.add(acc, K.mul(ci, vi))
    return acc


def analyse(q, t, pv1, sv1, pv2, sv2, K, show=print):
    """Returns a dict describing the common zeros of the forms Q_c in P^1."""
    M = e2_coeff_matrix(q, t, K)
    rank, null = left_nullspace(M, K)
    show("   E2 coefficient matrix in (f,r): %d x %d over K, rank = %d,"
         " left null space dimension = %d"
         % (len(M), len(M[0]), rank, len(null)))
    b11, b12, b22 = rhs_forms(pv1, sv1, pv2, sv2, K)
    forms = []
    for c in null:
        assert verify_left_null(c, M, K), "left null vector fails c.M = 0"
        Q = (pair(c, b11, K), pair(c, b12, K), pair(c, b22, K))
        forms.append(Q)
        show("      left null vector verified (c.M_E2 = 0); binary form"
             " Q_c(alpha,beta) = A*alpha^2 + B*alpha*beta + C*beta^2 with"
             " A,B,C nonzero: %s, %s, %s"
             % (not K.iszero(Q[0]), not K.iszero(Q[1]), not K.iszero(Q[2])))
    res = dict(rank=rank, nullity=len(null), forms=[])
    for A, B, Cc in forms:
        if K.iszero(A) and K.iszero(B) and K.iszero(Cc):
            res['forms'].append(dict(identically_zero=True))
            show("      Q_c is identically zero -- carries no information")
            continue
        disc = K.sub(K.mul(B, B), K.smul(4, K.mul(A, Cc)))
        info = dict(identically_zero=False,
                    A_zero=K.iszero(A), B_zero=K.iszero(B),
                    C_zero=K.iszero(Cc), disc_zero=K.iszero(disc))
        res['forms'].append(info)
        show("      Q_c not identically zero; discriminant B^2-4AC zero: %s"
             % K.iszero(disc))
        show("         zeros of Q_c in P^1: %s"
             % ("[1:0] only (A=0, B=0 impossible here)" if False else
                "at most two points"))
    return res, forms, M, null, (b11, b12, b22)
