"""Minimal Buchberger + 0-dimensional point solver over F_p (grevlex).

Self-contained; no CAS dependency.  Polynomials are dicts
    monomial (tuple of NV exponents) -> coefficient in [0,p).
"""
import random


def make(nv, p):
    return dict(nv=nv, p=p)


# ------------------------------------------------------------------- monomials
def mdeg(m):
    return sum(m)


def grevlex_key(m):
    # total degree, then reverse lex: larger = smaller last exponents
    return (sum(m),) + tuple(-e for e in reversed(m))


def mlcm(a, b):
    return tuple(max(x, y) for x, y in zip(a, b))


def mmul(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mdiv(a, b):
    """a / b if b | a else None"""
    r = []
    for x, y in zip(a, b):
        if x < y:
            return None
        r.append(x - y)
    return tuple(r)


# ------------------------------------------------------------------ polynomials
def lm(f):
    return max(f, key=grevlex_key)


def padd(a, b, p):
    r = dict(a)
    for m, c in b.items():
        v = (r.get(m, 0) + c) % p
        if v:
            r[m] = v
        else:
            r.pop(m, None)
    return r


def pmulmono(f, m, c, p):
    c %= p
    if c == 0:
        return {}
    return {mmul(k, m): (v * c) % p for k, v in f.items()}


def pmul(a, b, p):
    r = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = mmul(m1, m2)
            v = (r.get(m, 0) + c1 * c2) % p
            if v:
                r[m] = v
            else:
                r.pop(m, None)
    return r


def normalize(f, p):
    if not f:
        return f
    c = f[lm(f)]
    inv = pow(c, p - 2, p)
    return {m: (v * inv) % p for m, v in f.items()}


def reduce_full(f, G, p):
    """Full (tail) reduction of f modulo the list G."""
    Glm = [(lm(g), g) for g in G]
    out = {}
    f = dict(f)
    while f:
        m = lm(f)
        c = f[m]
        red = False
        for glm, g in Glm:
            q = mdiv(m, glm)
            if q is not None:
                f = padd(f, pmulmono(g, q, -c * pow(g[glm], p - 2, p), p), p)
                red = True
                break
        if not red:
            out[m] = c
            del f[m]
    return out


def spoly(f, g, p):
    lf, lg = lm(f), lm(g)
    L = mlcm(lf, lg)
    a = pmulmono(f, mdiv(L, lf), pow(f[lf], p - 2, p), p)
    b = pmulmono(g, mdiv(L, lg), pow(g[lg], p - 2, p), p)
    return padd(a, {m: (-c) % p for m, c in b.items()}, p)


def buchberger(F, p, verbose=False):
    G = [normalize(f, p) for f in F if f]
    pairs = set()
    for i in range(len(G)):
        for j in range(i):
            pairs.add((j, i))
    while pairs:
        # normal strategy: smallest lcm degree first
        best = min(pairs, key=lambda ij: grevlex_key(mlcm(lm(G[ij[0]]), lm(G[ij[1]]))))
        pairs.discard(best)
        i, j = best
        li, lj = lm(G[i]), lm(G[j])
        L = mlcm(li, lj)
        if L == mmul(li, lj):          # coprime criterion
            continue
        # chain criterion
        skip = False
        for k in range(len(G)):
            if k in (i, j):
                continue
            if mdiv(L, lm(G[k])) is not None:
                a = (min(i, k), max(i, k))
                b = (min(j, k), max(j, k))
                if a not in pairs and b not in pairs:
                    skip = True
                    break
        if skip:
            continue
        h = reduce_full(spoly(G[i], G[j], p), G, p)
        if h:
            h = normalize(h, p)
            G.append(h)
            n = len(G) - 1
            for k in range(n):
                pairs.add((k, n))
            if verbose:
                print("   GB grew to %d, new LM %s" % (len(G), lm(h)))
    # reduce to a minimal reduced basis
    G.sort(key=lambda f: grevlex_key(lm(f)))
    keep = []
    for i, f in enumerate(G):
        if not any(mdiv(lm(f), lm(g)) is not None for g in G[:i] if g is not f):
            keep.append(f)
    red = []
    for i, f in enumerate(keep):
        others = keep[:i] + keep[i + 1:]
        r = reduce_full(f, others, p)
        if r:
            red.append(normalize(r, p))
    return red


# ------------------------------------------------------- 0-dimensional solving
def quotient_basis(G, nv, maxdeg=60):
    lms = [lm(g) for g in G]
    basis = []
    frontier = [(0,) * nv]
    seen = {(0,) * nv}
    while frontier:
        nxt = []
        for m in frontier:
            if any(mdiv(m, l) is not None for l in lms):
                continue
            basis.append(m)
            for k in range(nv):
                e = list(m)
                e[k] += 1
                e = tuple(e)
                if e not in seen:
                    seen.add(e)
                    nxt.append(e)
        frontier = nxt
        if len(basis) > 100000:
            raise RuntimeError("not zero-dimensional")
    return sorted(basis, key=grevlex_key)


def mult_matrix(G, basis, nv, p, k):
    """matrix of multiplication by variable k in the quotient basis."""
    idx = {m: i for i, m in enumerate(basis)}
    n = len(basis)
    M = [[0] * n for _ in range(n)]
    for j, m in enumerate(basis):
        e = list(m)
        e[k] += 1
        r = reduce_full({tuple(e): 1}, G, p)
        for mm, c in r.items():
            M[idx[mm]][j] = c % p
    return M


def matvec_left(w, M, p):
    n = len(M)
    return [sum(w[i] * M[i][j] for i in range(n)) % p for j in range(n)]


def charpoly_roots(M, p):
    """F_p roots of char poly of M, via brute Krylov + polynomial from det?
    For small n use the Leverrier-free approach: build char poly by
    interpolation over random points is unsafe; instead compute det(xI-M)
    with fraction-free expansion for small n."""
    n = len(M)
    # det(x I - M) by expansion using sympy-free polynomial Gaussian elimination
    # represent entries as lists of coeffs (polys in x) mod p
    def padd_(a, b):
        L = max(len(a), len(b))
        return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
                for i in range(L)]

    def pmul_(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    r[i + j] = (r[i + j] + x * y) % p
        return r

    def pneg(a):
        return [(-x) % p for x in a]

    A = [[[(-M[i][j]) % p] + ([1] if i == j else []) for j in range(n)]
         for i in range(n)]
    # fraction-free (Bareiss) over F_p[x] is messy; n is small (<=8) -> expansion
    def det(rows, cols):
        if not rows:
            return [1]
        r0 = rows[0]
        tot = [0]
        for ci, c in enumerate(cols):
            e = A[r0][c]
            if e == [0] or all(v == 0 for v in e):
                continue
            sub = det(rows[1:], cols[:ci] + cols[ci + 1:])
            term = pmul_(e, sub)
            if ci % 2:
                term = pneg(term)
            tot = padd_(tot, term)
        return tot

    cp = det(list(range(n)), list(range(n)))
    roots = []
    # find roots by gcd with x^p - x then splitting; n small -> just do
    # a Cantor-Zassenhaus-free approach: gcd(cp, x^p-x) then trial via
    # root-finding over small degree using Berlekamp on the split factor
    return cp


def poly_roots_fp(cp, p):
    """all roots in F_p of a univariate poly given as coeff list (low->high)."""
    def trim(a):
        while a and a[-1] % p == 0:
            a.pop()
        return a

    def pmod(a, b):
        a = list(a)
        db = len(b) - 1
        inv = pow(b[-1], p - 2, p)
        while len(a) - 1 >= db and trim(a):
            if len(a) - 1 < db:
                break
            f = a[-1] * inv % p
            sh = len(a) - 1 - db
            for i, c in enumerate(b):
                a[i + sh] = (a[i + sh] - f * c) % p
            trim(a)
        return a

    def pgcd(a, b):
        a, b = trim(list(a)), trim(list(b))
        while b:
            a, b = b, trim(pmod(a, b))
        return a

    def pmulmod(a, b, mod):
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    r[i + j] = (r[i + j] + x * y) % p
        return trim(pmod(r, mod))

    cp = trim(list(cp))
    if len(cp) <= 1:
        return []
    # x^p mod cp
    xp = [0, 1]
    base = [0, 1]
    e = p
    res = [1]
    while e:
        if e & 1:
            res = pmulmod(res, base, cp)
        base = pmulmod(base, base, cp)
        e >>= 1
    g = pgcd(cp, trim([(res[i] if i < len(res) else 0) - (1 if i == 1 else 0)
                       for i in range(max(len(res), 2))]))
    g = trim([c % p for c in g])
    if len(g) <= 1:
        return []
    roots = []

    def split(f):
        f = trim(list(f))
        d = len(f) - 1
        if d == 0:
            return
        if d == 1:
            roots.append((-f[0] * pow(f[1], p - 2, p)) % p)
            return
        while True:
            a = random.randrange(p)
            base = [a, 1]
            r = [1]
            e = (p - 1) // 2
            b = base
            while e:
                if e & 1:
                    r = pmulmod(r, b, f)
                b = pmulmod(b, b, f)
                e >>= 1
            h = pgcd(f, trim([(r[i] if i < len(r) else 0) - (1 if i == 0 else 0)
                              for i in range(max(len(r), 1))]))
            h = trim([c % p for c in h])
            if 0 < len(h) - 1 < d:
                split(h)
                q = polydiv(f, h, p)
                split(q)
                return

    def polydiv(a, b, p):
        a = list(a)
        db = len(b) - 1
        inv = pow(b[-1], p - 2, p)
        qd = len(a) - 1 - db
        q = [0] * (qd + 1)
        for k in range(qd, -1, -1):
            f = a[k + db] * inv % p
            q[k] = f
            if f:
                for i, c in enumerate(b):
                    a[i + k] = (a[i + k] - f * c) % p
        return q

    split(g)
    return sorted(set(roots))


def solve_zero_dim(G, nv, p, coord_polys):
    """Return list of dicts {k: value} for each F_p-point, k in 0..nv-1.

    coord_polys: list of nv polys whose values are the coordinates (the
    variables themselves).  Uses left eigenvectors of a random-form
    multiplication matrix.
    """
    basis = quotient_basis(G, nv)
    n = len(basis)
    Ms = [mult_matrix(G, basis, nv, p, k) for k in range(nv)]
    idx = {m: i for i, m in enumerate(basis)}
    one = idx[(0,) * nv]
    for _ in range(40):
        co = [random.randrange(1, p) for _ in range(nv)]
        ML = [[sum(co[k] * Ms[k][i][j] for k in range(nv)) % p
               for j in range(n)] for i in range(n)]
        cp = charpoly_roots(ML, p)
        rts = poly_roots_fp(cp, p)
        pts = []
        ok = True
        for lam in rts:
            # left kernel of (ML - lam I)
            A = [[(ML[i][j] - (lam if i == j else 0)) % p for j in range(n)]
                 for i in range(n)]
            # left null vectors: null space of A^T
            AT = [[A[i][j] for i in range(n)] for j in range(n)]
            ns = nullspace(AT, p)
            if len(ns) != 1:
                ok = False
                break
            w = ns[0]
            if w[one] % p == 0:
                ok = False
                break
            iv = pow(w[one], p - 2, p)
            w = [x * iv % p for x in w]
            pt = {}
            for k in range(nv):
                e = [0] * nv
                e[k] = 1
                r = reduce_full({tuple(e): 1}, G, p)
                pt[k] = sum(c * w[idx[m]] for m, c in r.items()) % p
            pts.append(pt)
        if ok:
            return pts, n, len(cp) - 1
    raise RuntimeError("eigen separation failed")


def nullspace(M, p):
    m, n = len(M), len(M[0])
    A = [row[:] for row in M]
    piv, r = [], 0
    for c in range(n):
        pr = next((rr for rr in range(r, m) if A[rr][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for rr in range(m):
            if rr != r and A[rr][c] % p:
                f = A[rr][c]
                A[rr] = [(a - f * b) % p for a, b in zip(A[rr], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in piv]
    out = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for ri, pc in enumerate(piv):
            v[pc] = (-A[ri][fc]) % p
        out.append(v)
    return out
