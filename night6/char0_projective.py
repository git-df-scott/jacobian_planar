"""night6 -- characteristic zero: the projective question in one computation.

Both charts at once, exactly, with no Groebner engine and no elimination in a
chart parameter.  Write the kernel element as

        (p_, s_) = alpha*(p1,s1) + beta*(p2,s2),     (alpha,beta) != (0,0)

and use the following structure of the three identities.

* **E2** `3f't + 2p_'s_ + q'r - p_ s_' - 2q r' = 0` (19 rows) is affine-linear
  in (f, r) -- g does not occur -- and its COEFFICIENT matrix `M2` (19 x 20)
  does not involve (p_,s_) at all.  The whole dependence on (alpha,beta) is in
  the inhomogeneous term, which is a homogeneous QUADRATIC
  `b(alpha,beta) = alpha^2 b11 + alpha*beta b12 + beta^2 b22`.
  `M2` has rank 18, and its one left null vector `c` satisfies
  `c.b11 = c.b12 = c.b22 = 0`, so E2 is consistent for every (alpha,beta) and
  its solution set is
        (f,r) = x(alpha,beta) + lam1*w1 + lam2*w2
  with `w1,w2` a basis of ker M2 (independent of alpha,beta) and
  `x(alpha,beta)` a homogeneous quadratic (one fixed solve per coefficient).

* **E1** `2f's_ + p_'r - p_ r' - 2q g' = 0` (19 rows) is linear in (f,g,r); its
  (f,r) block `P(alpha,beta) = alpha*P1 + beta*P2` is homogeneous LINEAR in
  (alpha,beta), and its g block `G` (19 x 12) is independent of (alpha,beta)
  and of rank 12.

Substituting the E2 solution set into E1 gives

        G g + lam1 P(a,b) w1 + lam2 P(a,b) w2 = -P(a,b) x(a,b)

and applying the 7 left null vectors `z` of `G` removes g entirely, leaving,
for each z, one equation in (lam1, lam2):

        lam1 * L1_z(a,b) + lam2 * L2_z(a,b) = C_z(a,b)

with `L1_z, L2_z` binary LINEAR forms and `C_z` a binary CUBIC form over K.
So the identities have a solution at [alpha:beta] only if the 7 x 3 system
[L1 | L2 | C] has rank <= 2 there, i.e. only if every 3 x 3 minor -- a binary
form of degree 5 -- vanishes at [alpha:beta].

If those minors have no common zero in P^1 over the algebraic closure, then no
(alpha,beta) != (0,0) admits a solution of E1 and E2, hence none of E0,E1,E2:
chart A and chart B, free and Rabinowitsch variants alike.
"""
import os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FIDX = list(range(1, 9))
GIDX = list(range(1, 13))
RIDX = list(range(1, 13))
FRNAMES = ["f%d" % i for i in FIDX] + ["r%d" % k for k in RIDX]
FRIDX = {n: i for i, n in enumerate(FRNAMES)}
NFR = len(FRNAMES)


def uderiv(d, K):
    return {k - 1: K.smul(k, v) for k, v in d.items() if k > 0}


# --------------------------------------------------------------- the blocks
def E2_matrix(q, t, K):
    """19 x 20 coefficient matrix of E2 in (f,r); independent of (p_,s_)."""
    qd = uderiv(q, K)
    M = []
    for k in range(1, 20):
        row = [K.zero] * NFR
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


def E2_rhs(pa, sa, pb, sb, K):
    """u^k coefficients of -(2 pa' sb - pa sb'), k = 1..19"""
    pad, sbd = uderiv(pa, K), uderiv(sb, K)
    out = [K.zero] * 19
    for i, pi in pad.items():
        for j, sj in sb.items():
            if 1 <= i + j <= 19:
                out[i + j - 1] = K.add(out[i + j - 1], K.smul(2, K.mul(pi, sj)))
    for i, pi in pa.items():
        for j, sj in sbd.items():
            if 1 <= i + j <= 19:
                out[i + j - 1] = K.sub(out[i + j - 1], K.mul(pi, sj))
    return [K.sub(K.zero, v) for v in out]


def E1_fr_matrix(pv, sv, K):
    """19 x 20 block of E1 in (f,r); linear homogeneous in (p_,s_)."""
    pd = uderiv(pv, K)
    M = []
    for k in range(1, 20):
        row = [K.zero] * NFR
        for i in FIDX:
            for j, sj in sv.items():
                if i - 1 + j == k:
                    c = FRIDX["f%d" % i]
                    row[c] = K.add(row[c], K.smul(2 * i, sj))
        for m in RIDX:
            c = FRIDX["r%d" % m]
            for i, pi in pd.items():
                if i + m == k:
                    row[c] = K.add(row[c], pi)
            for i, pi in pv.items():
                if i + m - 1 == k:
                    row[c] = K.sub(row[c], K.smul(m, pi))
        M.append(row)
    return M


def E1_g_matrix(q, K):
    """19 x 12 block of E1 in g; independent of (p_,s_)."""
    M = []
    for k in range(1, 20):
        row = [K.zero] * len(GIDX)
        for j in GIDX:
            for i, qi in q.items():
                if i + j - 1 == k:
                    row[j - 1] = K.sub(row[j - 1], K.smul(2 * j, qi))
        M.append(row)
    return M


# ------------------------------------------------------------ linear algebra
def rref(M, K, extra=0):
    m, n = len(M), len(M[0])
    A = [list(r) for r in M]
    piv, r = [], 0
    for c in range(n - extra):
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
    return A, piv, r


def solve(M, b, K):
    """one solution of M x = b, plus the kernel basis; None if inconsistent"""
    n = len(M[0])
    A = [list(M[i]) + [b[i]] for i in range(len(M))]
    R, piv, rk = rref(A, K, extra=1)
    for i in range(rk, len(R)):
        if all(K.iszero(v) for v in R[i][:n]) and not K.iszero(R[i][n]):
            return None, None, rk
    x = [K.zero] * n
    for ri, c in enumerate(piv):
        x[c] = R[ri][n]
    free = [c for c in range(n) if c not in piv]
    ker = []
    for fc in free:
        v = [K.zero] * n
        v[fc] = K.one
        for ri, c in enumerate(piv):
            v[c] = K.sub(K.zero, R[ri][fc])
        ker.append(v)
    return x, ker, rk


def left_nullspace(M, K):
    m, n = len(M), len(M[0])
    A = [list(M[i]) + [K.one if j == i else K.zero for j in range(m)]
         for i in range(m)]
    R, piv, rk = rref(A, K, extra=m)
    return rk, [R[i][n:] for i in range(rk, m)]


def matvec(M, v, K):
    out = []
    for row in M:
        acc = K.zero
        for a, b in zip(row, v):
            if not K.iszero(a) and not K.iszero(b):
                acc = K.add(acc, K.mul(a, b))
        out.append(acc)
    return out


def dot(u, v, K):
    acc = K.zero
    for a, b in zip(u, v):
        if not K.iszero(a) and not K.iszero(b):
            acc = K.add(acc, K.mul(a, b))
    return acc


# ------------------------------------------------------------- binary forms
# a binary form of degree d is a list [c_0..c_d]:  sum c_i alpha^i beta^(d-i)
def bf_mul(a, b, K):
    out = [K.zero] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if K.iszero(x):
            continue
        for j, y in enumerate(b):
            if K.iszero(y):
                continue
            out[i + j] = K.add(out[i + j], K.mul(x, y))
    return out


def bf_sub(a, b, K):
    n = max(len(a), len(b))
    a = a + [K.zero] * (n - len(a))
    b = b + [K.zero] * (n - len(b))
    return [K.sub(x, y) for x, y in zip(a, b)]


def bf_iszero(a, K):
    return all(K.iszero(x) for x in a)


def det3_bf(rows, K):
    """3x3 determinant of binary forms"""
    (a, b, c), (d, e, f), (g, h, i) = rows
    t1 = bf_mul(a, bf_sub(bf_mul(e, i, K), bf_mul(f, h, K), K), K)
    t2 = bf_mul(b, bf_sub(bf_mul(d, i, K), bf_mul(f, g, K), K), K)
    t3 = bf_mul(c, bf_sub(bf_mul(d, h, K), bf_mul(e, g, K), K), K)
    return bf_sub(bf_sub(t1, t2, K), t3, K)


def poly_gcd(a, b, K):
    a = [x for x in a]
    b = [x for x in b]
    def trim(p):
        while p and K.iszero(p[-1]):
            p.pop()
        return p
    a, b = trim(a), trim(b)
    while b:
        while len(a) >= len(b) and a:
            f = K.mul(a[-1], K.inv(b[-1]))
            sh = len(a) - len(b)
            for i, bv in enumerate(b):
                a[i + sh] = K.sub(a[i + sh], K.mul(f, bv))
            a = trim(a)
            if not a:
                break
        a, b = b, a
    a = trim(a)
    if not a:
        return []
    iv = K.inv(a[-1])
    return [K.mul(v, iv) for v in a]


# ------------------------------------------------------------------ analysis
def analyse(q, t, pv1, sv1, pv2, sv2, K, show=print):
    out = {}
    M2 = E2_matrix(q, t, K)
    b11 = E2_rhs(pv1, sv1, pv1, sv1, K)
    b12 = [K.add(x, y) for x, y in zip(E2_rhs(pv1, sv1, pv2, sv2, K),
                                       E2_rhs(pv2, sv2, pv1, sv1, K))]
    b22 = E2_rhs(pv2, sv2, pv2, sv2, K)
    xs, kers, rks = [], None, []
    for name, bb in (("b11", b11), ("b12", b12), ("b22", b22)):
        x, ker, rk = solve(M2, bb, K)
        assert x is not None, ("E2 inconsistent for " + name)
        xs.append(x)
        kers = ker
        rks.append(rk)
    show("   E2 block: %d x %d over K, rank %d, kernel dimension %d;"
         " consistent for all three quadratic coefficients: yes"
         % (len(M2), len(M2[0]), rks[0], len(kers)))
    out['E2_rank'] = rks[0]
    out['E2_kerdim'] = len(kers)
    assert len(kers) == 2, ("expected a 2-dimensional E2 kernel",
                            len(kers))
    w1, w2 = kers

    G = E1_g_matrix(q, K)
    rkG, zs = left_nullspace(G, K)
    show("   E1 g-block: %d x %d over K, rank %d, left null space dimension %d"
         % (len(G), len(G[0]), rkG, len(zs)))
    out['G_rank'] = rkG
    out['G_leftnull'] = len(zs)

    P1 = E1_fr_matrix(pv1, sv1, K)
    P2 = E1_fr_matrix(pv2, sv2, K)

    # P(a,b) w_i  = a*P1 w_i + b*P2 w_i         (linear in (a,b))
    Pw = {}
    for nm, w in (("w1", w1), ("w2", w2)):
        Pw[nm] = (matvec(P1, w, K), matvec(P2, w, K))
    # x(a,b) = a^2 x11 + a b x12 + b^2 x22 ; rhs = -P(a,b) x(a,b) : cubic
    Px = []
    for xv in xs:                       # xs = [x11, x12, x22]
        Px.append((matvec(P1, xv, K), matvec(P2, xv, K)))

    rows = []
    for z in zs:
        # L1, L2 : linear forms   [coeff of beta^1 , coeff of alpha^1]
        L1 = [dot(z, Pw["w1"][1], K), dot(z, Pw["w1"][0], K)]
        L2 = [dot(z, Pw["w2"][1], K), dot(z, Pw["w2"][0], K)]
        # C = - z . P(a,b) x(a,b)
        # P(a,b) x(a,b) = (a P1 + b P2)(a^2 x11 + ab x12 + b^2 x22)
        #  a^3 : P1 x11
        #  a^2 b : P1 x12 + P2 x11
        #  a b^2 : P1 x22 + P2 x12
        #  b^3 : P2 x22
        c3 = dot(z, Px[0][0], K)
        c2 = K.add(dot(z, Px[1][0], K), dot(z, Px[0][1], K))
        c1 = K.add(dot(z, Px[2][0], K), dot(z, Px[1][1], K))
        c0 = dot(z, Px[2][1], K)
        C = [K.sub(K.zero, v) for v in (c0, c1, c2, c3)]
        rows.append((L1, L2, C))
    out['n_rows'] = len(rows)
    nz = sum(1 for L1, L2, C in rows
             if not (bf_iszero(L1, K) and bf_iszero(L2, K)
                     and bf_iszero(C, K)))
    show("   reduced system: %d equations in (lam1, lam2) with binary-form"
         " coefficients (linear) and binary-cubic right-hand sides;"
         " %d of them not identically zero" % (len(rows), nz))

    minors = []
    n = len(rows)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                d = det3_bf([rows[i], rows[j], rows[k]], K)
                if not bf_iszero(d, K):
                    minors.append(d)
    show("   3 x 3 minors of [L1 | L2 | C]: %d of %d are not identically zero"
         % (len(minors), n * (n - 1) * (n - 2) // 6))
    out['n_minors_nonzero'] = len(minors)
    if not minors:
        out['verdict'] = 'inconclusive: every 3x3 minor vanishes identically'
        show("   => INCONCLUSIVE at this level: the reduced system has rank"
             " <= 2 identically; E0 would be needed.")
        return out, rows, minors
    g = minors[0]
    for mm in minors[1:]:
        g = poly_gcd(g, mm, K)
        if len(g) <= 1:
            break
    # a common zero at [1:0] would show as every minor having zero top
    # coefficient (the coefficient of alpha^deg)
    top_all_zero = all(K.iszero(mm[-1]) for mm in minors)
    show("   gcd of those minors, as polynomials in alpha (beta = 1):"
         " degree %d" % (len(g) - 1))
    show("   common zero at [alpha:beta] = [1:0] (i.e. beta = 0): %s"
         % top_all_zero)
    empty = (len(g) - 1 <= 0) and not top_all_zero
    out['gcd_degree'] = len(g) - 1
    out['common_zero_at_beta0'] = top_all_zero
    out['empty'] = empty
    if empty:
        show("   => the minors have NO common zero in P^1: for EVERY"
             " (alpha,beta) != (0,0) the identities E1 and E2 already have no"
             " common solution in (f,g,r).")
    else:
        show("   => a common zero survives; those (alpha,beta) need E0.")
    return out, rows, minors


# ----------------------------------------------------- Bezout certificate
def poly_trim(p, K):
    p = list(p)
    while p and K.iszero(p[-1]):
        p.pop()
    return p


def poly_add(a, b, K):
    n = max(len(a), len(b))
    a = list(a) + [K.zero] * (n - len(a))
    b = list(b) + [K.zero] * (n - len(b))
    return poly_trim([K.add(x, y) for x, y in zip(a, b)], K)


def poly_mul(a, b, K):
    if not a or not b:
        return []
    out = [K.zero] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if K.iszero(x):
            continue
        for j, y in enumerate(b):
            if K.iszero(y):
                continue
            out[i + j] = K.add(out[i + j], K.mul(x, y))
    return poly_trim(out, K)


def poly_divmod(a, b, K):
    a = poly_trim(list(a), K)
    b = poly_trim(list(b), K)
    assert b, "division by zero polynomial"
    qout = [K.zero] * max(1, len(a) - len(b) + 1)
    ib = K.inv(b[-1])
    while len(a) >= len(b) and a:
        f = K.mul(a[-1], ib)
        sh = len(a) - len(b)
        qout[sh] = K.add(qout[sh], f)
        for i, bv in enumerate(b):
            a[i + sh] = K.sub(a[i + sh], K.mul(f, bv))
        a = poly_trim(a, K)
    return poly_trim(qout, K), a


def poly_xgcd(a, b, K):
    """returns (g, u, v) with u*a + v*b = g, g monic"""
    r0, r1 = poly_trim(list(a), K), poly_trim(list(b), K)
    u0, u1 = [K.one], []
    v0, v1 = [], [K.one]
    while r1:
        qq, rr = poly_divmod(r0, r1, K)
        r0, r1 = r1, rr
        u0, u1 = u1, poly_add(u0, [K.sub(K.zero, x) for x in
                                   poly_mul(qq, u1, K)], K)
        v0, v1 = v1, poly_add(v0, [K.sub(K.zero, x) for x in
                                   poly_mul(qq, v1, K)], K)
    if not r0:
        return [], [], []
    iv = K.inv(r0[-1])
    sc = lambda p: [K.mul(x, iv) for x in p]
    return sc(r0), sc(u0), sc(v0)


def bezout_certificate(minors, K, show=print):
    """cofactors u_i with sum u_i * m_i = 1, verified by direct expansion.

    Each m_i is the dehomogenisation (beta = 1) of a 3 x 3 minor.  A common
    zero with beta != 0 would be a common root of the m_i; the identity below
    proves there is none, without trusting the gcd routine.
    """
    g = poly_trim(list(minors[0]), K)
    co = [[K.one]] + [[] for _ in minors[1:]]
    used = 1
    for idx in range(1, len(minors)):
        if len(g) == 1:
            break
        ng, u, v = poly_xgcd(g, poly_trim(list(minors[idx]), K), K)
        co = [poly_mul(u, c, K) for c in co]
        co[idx] = poly_add(co[idx], v, K)
        g = ng
        used = idx + 1
    acc = []
    for c, m in zip(co, minors):
        if c:
            acc = poly_add(acc, poly_mul(c, poly_trim(list(m), K), K), K)
    ok = (len(acc) == 1 and not K.iszero(acc[0]))
    if ok:
        iv = K.inv(acc[0])
        co = [[K.mul(x, iv) for x in c] for c in co]
        acc2 = []
        for c, m in zip(co, minors):
            if c:
                acc2 = poly_add(acc2, poly_mul(c, poly_trim(list(m), K), K), K)
        ok = (len(acc2) == 1 and K.show(acc2[0]) == "1")
    show("   Bezout certificate over %d of the minors: sum u_i(alpha)*m_i"
         "(alpha) expands to a nonzero constant: %s ; normalised to exactly 1:"
         " %s" % (used, len(acc) == 1 and not K.iszero(acc[0]), ok))
    return ok, used, len(g) - 1
