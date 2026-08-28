"""Solve the weighted-homogeneous face system and recover the face solutions.

Pipeline
  1. build the 6 weighted-homogeneous residual equations of weights 11..16
     in A_1..A_7 (weights 1..7);
  2. weighted-degree-d Macaulay matrix, columns ordered with the "pure"
     monomials A_1^(d-7b) A_7^b last -> a univariate relation in
     X = A_7 / A_1^7;
  3. same matrices with tail {pure} u {A_1^(d-k) A_k} -> A_k / A_1^k as a
     function of X, for k = 2..6;
  4. gauge A_1 = 1, transport to the brief's gauge q_1 = q_8 = 1 by
     lambda^7 = 1/A_7, verify the face equation exactly.
"""
import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import wface as W


def flush(*a):
    print(*a)
    sys.stdout.flush()


def find_pure_relation(res, p, dmin=38, dmax=60):
    for d in range(dmin, dmax):
        t = time.time()
        tm = W.pure_mons(d, 7)
        rows, tail, nr, nc = W.macaulay(res, d, p, tm)
        flush("   weighted degree %d: %d rows, %d cols, %d pure monomials,"
              " %d relation(s)  (%.1fs)"
              % (d, nr, nc, len(tail), len(rows), time.time() - t))
        if rows:
            return d, rows, tail
    return None, None, None


def relation_for(res, p, d, k):
    """rows supported on {A_1^(d-7b) A_7^b} u {A_1^(d-k) A_k}"""
    tm = list(W.pure_mons(d, 7))
    e = [0] * W.NV
    e[k - 1] = 1
    e[0] += d - k
    extra = tuple(e)
    if extra in set(tm):
        return None, None
    rows, tail, nr, nc = W.macaulay(res, d, p, tm + [extra])
    return rows, tail


def polyroots(coeffs, p):
    import flint
    f = flint.nmod_poly(list(int(c) % p for c in coeffs), p)
    out = []
    for fac, m in f.factor()[1]:
        if fac.degree() == 1:
            c = [int(fac[i]) for i in range(2)]
            out.append((-c[0] * pow(c[1], p - 2, p)) % p)
    return sorted(set(out)), f.degree(), [ (g.degree(), m) for g, m in f.factor()[1] ]


def solve(p, dmin=38):
    B, res = W.build(p)
    flush("   residual equations: weights %s, term counts %s"
          % ([W.wdeg(next(iter(f))) for f in res], [len(f) for f in res]))
    d, rows, tail = find_pure_relation(res, p, dmin)
    if d is None:
        raise RuntimeError("no pure relation found")
    # tail monomials are A_1^(d-7b) A_7^b, b = 0,1,2,...
    best = None
    for r in rows:
        c = list(r)
        while c and c[-1] == 0:
            c.pop()
        if c and (best is None or len(c) < len(best)):
            best = c
    flush("   eliminant in X = A_7/A_1^7 : degree %d, coefficients %s"
          % (len(best) - 1, best))
    roots, deg, facs = polyroots(best, p)
    flush("   eliminant factor degrees (with multiplicity): %s" % facs)
    flush("   F_p-rational values of X: %d  -> %s" % (len(roots), roots))

    # coordinates A_2..A_6 as functions of X (gauge A_1 = 1)
    coord = {}
    for k in range(2, 7):
        rws, tl = relation_for(res, p, d, k)
        assert rws, "no relation row for A_%d" % k
        # each row: coefficients on [pure..., A_1^(d-k) A_k]
        use = None
        for r in rws:
            if r[-1] % p:
                use = r
                break
        assert use is not None, "no row involving A_%d" % k
        coord[k] = use
        flush("   A_%d recovered from a relation row with %d pure terms"
              % (k, len(use) - 1))

    sols = []
    for X in roots:
        A = {0: 1, 1: 1, 7: X}
        for k in range(2, 7):
            r = coord[k]
            npure = len(r) - 1
            val = 0
            for b in range(npure):
                val = (val + r[b] * pow(X, b, p)) % p
            A[k] = (-val * pow(r[-1], p - 2, p)) % p
        sols.append(A)
    # verify each against the residual equations
    good = []
    for A in sols:
        vals = [A[k] for k in range(1, 8)]
        ok = True
        for f in res:
            s = 0
            for m, c in f.items():
                t = c
                for i, e in enumerate(m):
                    if e:
                        t = t * pow(vals[i], e, p) % p
                s = (s + t) % p
            if s % p:
                ok = False
        if ok:
            good.append(A)
    flush("   points satisfying all 6 residual equations exactly: %d of %d"
          % (len(good), len(sols)))
    return good, d


def branch_A1_zero(p, dmin=30, dmax=60):
    """Check the locus A_1 = 0 (i.e. q_2 = 0) for solutions with A_7 != 0."""
    B, res = W.build(p)
    res0 = []
    for f in res:
        g = {m: c for m, c in f.items() if m[0] == 0}
        if g:
            res0.append(g)
    # dehomogenise by A_7 = 1: substitute e_7 -> 0 and collect
    from collections import defaultdict
    eqs = []
    for f in res0:
        g = defaultdict(int)
        for m, c in f.items():
            mm = tuple(list(m[1:6]))
            g[mm] = (g[mm] + c) % p
        g = {m: c for m, c in g.items() if c}
        if g:
            eqs.append(g)
    return eqs
