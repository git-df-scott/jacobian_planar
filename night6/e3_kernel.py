"""Night 6 -- from-scratch face system + E3 kernel computation.

Face equation:  2*q*t' - 3*q'*t = u^2   in F_p[u]
    q supported on u^1..u^8   (gauge q_1 = q_8 = 1)
    t supported on u^2..u^12
Coefficient of u^(n-1), n = i+j:   sum_{i+j=n} (2j - 3i) q_i t_j  =  [n == 3]

E3 operator:  E3(p_, s_) = 3*p_'*t + 2*q'*s_ - p_*t' - 2*q*s_'
    p_ supported on u^1..u^8   (8 unknowns)
    s_ supported on u^2..u^12  (11 unknowns)
Coefficient of u^(n-1), n = i+j:
    sum_{i+j=n} (3i - j) p_i t_j  +  sum_{i+j=n} (2i - 2j) q_i s_j

All arithmetic is done directly in F_p; sympy is used only for the Groebner
step on the 6 residual equations in q_2..q_7.
"""
import sys, json

QIDX = list(range(1, 9))    # q_1..q_8
TIDX = list(range(2, 13))   # t_2..t_12
PIDX = list(range(1, 9))    # p_1..p_8
SIDX = list(range(2, 13))   # s_2..s_12
NV = 6                      # q_2..q_7


# ------------------------------------------------- tiny multivariate F_p polys
# a poly is dict: monomial (6-tuple of exponents) -> coeff in [0,p)
def padd(a, b, p):
    r = dict(a)
    for m, c in b.items():
        v = (r.get(m, 0) + c) % p
        if v:
            r[m] = v
        else:
            r.pop(m, None)
    return r


def pscal(a, k, p):
    k %= p
    if k == 0:
        return {}
    return {m: (c * k) % p for m, c in a.items()}


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


ONE = {(0,) * NV: 1}


def var(i):  # q_i for i in 2..7
    e = [0] * NV
    e[i - 2] = 1
    return {tuple(e): 1}


def peval(a, vals, p):
    """vals: list of 6 ints for q_2..q_7."""
    tot = 0
    for m, c in a.items():
        term = c
        for k, e in enumerate(m):
            if e:
                term = term * pow(vals[k], e, p) % p
        tot = (tot + term) % p
    return tot % p


def to_sympy(a, gens):
    from sympy import Integer
    e = 0
    for m, c in a.items():
        t = Integer(int(c))
        for k, ex in enumerate(m):
            if ex:
                t *= gens[k] ** ex
        e += t
    return e


# ---------------------------------------------------------------- face system
def face_rows():
    rows = {}
    for n in range(3, 21):
        terms = []
        for i in QIDX:
            j = n - i
            if j in TIDX:
                c = 2 * j - 3 * i
                if c != 0:
                    terms.append((i, j, c))
        rows[n] = terms
    return rows


def build_face(p):
    """Triangular elimination: t_2..t_12 as F_p-polys in q_2..q_7;
    returns (t_polys, 6 residual equations)."""
    rows = face_rows()
    qsym = {1: ONE, 8: ONE}
    for i in range(2, 8):
        qsym[i] = var(i)

    neq = 0
    t = {}
    for n in range(3, 14):
        terms = {(i, j): c for i, j, c in rows[n]}
        lead = (1, n - 1)
        c0 = terms.pop(lead)
        acc = ONE if n == 3 else {}          # rhs: [n==3]
        for (i, j), c in terms.items():
            acc = padd(acc, pscal(pmul(qsym[i], t[j], p), -c, p), p)
        t[n - 1] = pscal(acc, pow(c0 % p, p - 2, p), p)
        neq += 1

    eqs = []
    for n in range(14, 20):
        acc = {}
        for i, j, c in rows[n]:
            acc = padd(acc, pscal(pmul(qsym[i], t[j], p), c, p), p)
        eqs.append(acc)
        neq += 1

    # n = 20 must be identically zero (leading-coefficient degeneracy)
    acc20 = {}
    for i, j, c in rows[20]:
        acc20 = padd(acc20, pscal(pmul(qsym[i], t[j], p), c, p), p)
    assert acc20 == {}, "row n=20 is not identically zero"

    assert neq == 17, neq
    return t, eqs


def face_residual_mod(qv, tv, p):
    res = {}
    for i, qi in qv.items():
        for j, tj in tv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (2 * j - 3 * i) * qi * tj) % p
    res[2] = (res.get(2, 0) - 1) % p
    return {k: v for k, v in res.items() if v % p}


def solve_face(p, verbose=True):
    from sympy import symbols, groebner, Poly, factor_list, expand
    t_poly, eqs = build_face(p)
    gens = list(symbols('q2 q3 q4 q5 q6 q7'))
    if verbose:
        print("face system: 17 equations (n=3..19) in 17 unknowns "
              "(q_2..q_7, t_2..t_12);  row n=20 identically zero")
        print("triangular elimination gives t_2..t_12 in terms of q_2..q_7,")
        print("leaving %d residual equations in %d unknowns" % (len(eqs), NV))
        print("residual eq total degrees:",
              [max(sum(m) for m in e) for e in eqs])

    sy = [to_sympy(e, gens) for e in eqs]
    Gd = groebner(sy, *gens, order='grevlex', modulus=p)
    if verbose:
        print("grevlex GB size:", len(Gd.exprs),
              " zero-dimensional:", Gd.is_zero_dimensional)
    G = Gd.fglm('lex')
    polys = list(G.exprs)
    if verbose:
        print("lex GB size:", len(polys))
        top = Poly(polys[0], gens[-1], modulus=p)
        print("eliminant in %s has degree %d" % (gens[-1], top.degree()))

    # back-substitution for F_p-rational points
    sols = []

    def roots_of(g, v):
        P = Poly(g, v, modulus=p)
        r = set()
        for fac, m in factor_list(P)[1]:
            fp = Poly(fac, v, modulus=p)
            if fp.degree() == 1:
                a, b = fp.all_coeffs()
                r.add(int((-int(b) * pow(int(a) % p, p - 2, p)) % p))
        return r

    def rec(assign, idx):
        if idx < 0:
            sols.append(dict(assign))
            return
        v = gens[idx]
        rs = None
        for f in polys:
            g = expand(f.subs(assign))
            if g == 0:
                continue
            fs = g.free_symbols
            if not fs:
                if int(g) % p:
                    return
                continue
            if fs == {v}:
                rr = roots_of(g, v)
                rs = rr if rs is None else (rs & rr)
        if rs is None:
            raise RuntimeError("no univariate polynomial for %s" % v)
        for r in sorted(rs):
            a2 = dict(assign)
            a2[v] = r
            rec(a2, idx - 1)

    rec({}, NV - 1)

    faces = []
    for assign in sols:
        vals = [int(assign[g]) % p for g in gens]
        qv = {1: 1, 8: 1}
        for i in range(2, 8):
            qv[i] = vals[i - 2]
        tv = {j: peval(t_poly[j], vals, p) for j in TIDX}
        bad = face_residual_mod(qv, tv, p)
        assert not bad, ("FACE VERIFICATION FAILED", qv, tv, bad)
        assert tv[2] % p and tv[12] % p, ("t_2 or t_12 vanishes", qv, tv)
        faces.append((qv, tv))
    return faces, len(polys)


# ---------------------------------------------------------------- E3 operator
def e3_matrix(qv, tv, p):
    """rows u^2..u^19 (n=3..20): 18 rows; cols p_1..p_8, s_2..s_12: 19."""
    cols = [('p', i) for i in PIDX] + [('s', j) for j in SIDX]
    ns = list(range(3, 21))
    M = [[0] * len(cols) for _ in ns]
    for ri, n in enumerate(ns):
        for ci, (kind, k) in enumerate(cols):
            if kind == 'p':
                i, j = k, n - k
                if j in TIDX:
                    M[ri][ci] = ((3 * i - j) * tv[j]) % p
            else:
                j, i = k, n - k
                if i in QIDX:
                    M[ri][ci] = ((2 * i - 2 * j) * qv[i]) % p
    return M, cols, ns


def nullspace_mod(M, p):
    m, n = len(M), len(M[0])
    A = [row[:] for row in M]
    piv, r = [], 0
    for c in range(n):
        pr = next((rr for rr in range(r, m) if A[rr][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for rr in range(m):
            if rr != r and A[rr][c] % p:
                f = A[rr][c]
                A[rr] = [(a - f * b) % p for a, b in zip(A[rr], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for ri, pc in enumerate(piv):
            v[pc] = (-A[ri][fc]) % p
        basis.append(v)
    return r, basis


def verify_e3(vec, cols, qv, tv, p):
    pv, sv = {}, {}
    for val, (kind, k) in zip(vec, cols):
        (pv if kind == 'p' else sv)[k] = val % p
    res = {}
    for i, pi in pv.items():
        for j, tj in tv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (3 * i - j) * pi * tj) % p
    for i, qi in qv.items():
        for j, sj in sv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (2 * i - 2 * j) * qi * sj) % p
    return {k: v for k, v in res.items() if v % p}, pv, sv


# ---------------------------------------------------------------------- driver
if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'night6/e3_kernel_results.json'
    results = {}
    for p in (999983, 1000003):
        print("=" * 72)
        print("PRIME p = %d   (7 divides p-1 ? %s)" % (p, (p - 1) % 7 == 0))
        print("=" * 72)
        faces, gbsz = solve_face(p)
        print("F_p-rational face solutions found and verified: %d" % len(faces))
        recs = []
        for si, (qv, tv) in enumerate(faces):
            M, cols, ns = e3_matrix(qv, tv, p)
            rank, basis = nullspace_mod(M, p)
            print("-" * 66)
            print("face #%d" % si)
            print("  q = %s" % [qv[i] for i in QIDX])
            print("  t = %s" % [tv[j] for j in TIDX])
            print("  E3 matrix %dx%d   rank = %d   kernel dim = %d"
                  % (len(M), len(M[0]), rank, len(basis)))
            kb = []
            for b in basis:
                bad, pvv, svv = verify_e3(b, cols, qv, tv, p)
                assert not bad, ("kernel vector fails E3", bad)
                print("    kernel basis vector VERIFIED (E3 == 0 mod p):")
                print("      p_ nonzero coeffs:",
                      {k: v for k, v in sorted(pvv.items()) if v})
                print("      s_ nonzero coeffs:",
                      {k: v for k, v in sorted(svv.items()) if v})
                kb.append([int(x) for x in b])
            recs.append(dict(q=[qv[i] for i in QIDX], t=[tv[j] for j in TIDX],
                             shape=[len(M), len(M[0])], rank=rank,
                             kerdim=len(basis), kernel=kb))
        results[str(p)] = recs
    json.dump(results, open(out, 'w'), indent=1)
    print("\nkernel dims p=999983 :", [r['kerdim'] for r in results['999983']])
    print("kernel dims p=1000003:", [r['kerdim'] for r in results['1000003']])
    print("wrote", out)
