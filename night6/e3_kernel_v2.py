"""Night 6 -- face system + E3 kernel, mu_7-quotiented solve route.

Same face equation as e3_kernel.py, written in the (A,B) normalisation:
    q = u*A(u),  deg A = 7, A_0 = q_1, A_7 = q_8
    t = u^2*B(u), deg B = 10, B_0 = t_2, B_10 = t_12
    2*q*t' - 3*q'*t = u^2   <=>   sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m==0]
      for m = 0..17 (m = 17 identically zero) -- 17 equations.

Gauge group acting on (A,B):  A->cA, B->B/c  and  u->lambda*u
(A_k -> lambda^k A_k, B_k -> lambda^k B_k).  The brief's gauge A_0=A_7=1
(i.e. q_1=q_8=1) leaves the residual mu_7 (lambda^7=1); the gauge
A_0=A_1=1 leaves nothing, so its solution set is the mu_7 quotient.
Solutions are transported back to A_0=A_7=1 by lambda^7 = 1/A_7, which is
a bijection on F_p^* whenever 7 does not divide p-1; every transported
solution is then re-verified in the brief's gauge from scratch.
"""
import sys, json, time

QIDX = list(range(1, 9))
TIDX = list(range(2, 13))
PIDX = list(range(1, 9))
SIDX = list(range(2, 13))


def flush(*a):
    print(*a)
    sys.stdout.flush()


# ------------------------------------------- multivariate polys over F_p (dict)
class Ring:
    def __init__(self, nv, p):
        self.nv, self.p = nv, p
        self.one = {(0,) * nv: 1}

    def var(self, k):
        e = [0] * self.nv
        e[k] = 1
        return {tuple(e): 1}

    def add(self, a, b):
        r = dict(a)
        for m, c in b.items():
            v = (r.get(m, 0) + c) % self.p
            if v:
                r[m] = v
            else:
                r.pop(m, None)
        return r

    def scal(self, a, k):
        k %= self.p
        return {} if k == 0 else {m: (c * k) % self.p for m, c in a.items()}

    def mul(self, a, b):
        r = {}
        for m1, c1 in a.items():
            for m2, c2 in b.items():
                m = tuple(x + y for x, y in zip(m1, m2))
                v = (r.get(m, 0) + c1 * c2) % self.p
                if v:
                    r[m] = v
                else:
                    r.pop(m, None)
        return r

    def ev(self, a, vals):
        tot = 0
        for m, c in a.items():
            t = c
            for k, e in enumerate(m):
                if e:
                    t = t * pow(vals[k], e, self.p) % self.p
            tot = (tot + t) % self.p
        return tot

    def to_sympy(self, a, gens):
        from sympy import Integer
        out = 0
        for m, c in a.items():
            t = Integer(int(c))
            for k, e in enumerate(m):
                if e:
                    t *= gens[k] ** e
            out += t
        return out


# ------------------------------------------------------------- the face system
def eliminate_B(R, Avars):
    """Avars: dict k -> poly for A_0..A_7.  Returns (B dict 0..10, residuals)."""
    p = R.p
    B = {}
    for m in range(0, 11):
        # sum_{i+j=m} (1+2j-3i) A_i B_j = [m==0]; i=0 term is (1+2m)A_0 B_m
        c0 = (1 + 2 * m) % p
        assert c0 != 0
        acc = R.one if m == 0 else {}
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = (1 + 2 * j - 3 * i) % p
            if c:
                acc = R.add(acc, R.scal(R.mul(Avars[i], B[j]), -c))
        # divide by (1+2m)*A_0 ; A_0 is the constant 1 in both gauges used here
        assert Avars[0] == R.one, "A_0 must be gauged to 1"
        B[m] = R.scal(acc, pow(c0, p - 2, p))
    res = []
    for m in range(11, 17):
        acc = {}
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = (1 + 2 * j - 3 * i) % p
                if c:
                    acc = R.add(acc, R.scal(R.mul(Avars[i], B[j]), c))
        res.append(acc)
    # m = 17 must vanish identically
    acc = {}
    for i in range(0, 8):
        j = 17 - i
        if 0 <= j <= 10:
            c = (1 + 2 * j - 3 * i) % p
            if c:
                acc = R.add(acc, R.scal(R.mul(Avars[i], B[j]), c))
    assert acc == {}, "m=17 row not identically zero"
    return B, res


def face_residual_qt(qv, tv, p):
    """exact check of 2qt'-3q't-u^2 in the q_1=q_8=1 gauge."""
    res = {}
    for i, qi in qv.items():
        for j, tj in tv.items():
            res[i + j - 1] = (res.get(i + j - 1, 0) + (2 * j - 3 * i) * qi * tj) % p
    res[2] = (res.get(2, 0) - 1) % p
    return {k: v for k, v in res.items() if v % p}


def solve_gauge_A1(p):
    """Gauge A_0 = A_1 = 1; unknowns A_2..A_7 (6). Returns list of A-value dicts."""
    from sympy import symbols, groebner, Poly, factor_list, expand
    R = Ring(6, p)
    Av = {0: R.one, 1: R.one}
    for k in range(2, 8):
        Av[k] = R.var(k - 2)
    t0 = time.time()
    B, res = eliminate_B(R, Av)
    flush("  [A0=A1=1] residual equations: %d, total degrees %s"
          % (len(res), [max(sum(m) for m in e) for e in res]))
    gens = list(symbols('A2 A3 A4 A5 A6 A7'))
    sy = [R.to_sympy(e, gens) for e in res]
    Gd = groebner(sy, *gens, order='grevlex', modulus=p)
    flush("  [A0=A1=1] grevlex GB size %d, zero-dim %s (%.1fs)"
          % (len(Gd.exprs), Gd.is_zero_dimensional, time.time() - t0))
    G = Gd.fglm('lex')
    polys = list(G.exprs)
    flush("  [A0=A1=1] lex GB size %d (%.1fs)" % (len(polys), time.time() - t0))
    elim = Poly(polys[0], gens[-1], modulus=p)
    flush("  [A0=A1=1] eliminant degree in %s: %d" % (gens[-1], elim.degree()))
    fl = factor_list(elim)[1]
    flush("  [A0=A1=1] eliminant factor degrees: %s"
          % sorted(Poly(f, gens[-1], modulus=p).degree() for f, _ in fl))

    sols = []

    def roots_of(g, v):
        P = Poly(g, v, modulus=p)
        r = set()
        for fac, _ in factor_list(P)[1]:
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
            raise RuntimeError("no univariate poly for %s" % v)
        for r in sorted(rs):
            a2 = dict(assign)
            a2[v] = r
            rec(a2, idx - 1)

    rec({}, 5)
    out = []
    for a in sols:
        vals = [int(a[g]) % p for g in gens]
        A = {0: 1, 1: 1}
        for k in range(2, 8):
            A[k] = vals[k - 2]
        out.append(A)
    return out, elim.degree()


def solve_gauge_A0A7_A1zero(p):
    """Completeness branch: gauge A_0=A_7=1 with A_1=0; unknowns A_2..A_6."""
    from sympy import symbols, groebner
    R = Ring(5, p)
    Av = {0: R.one, 1: {}, 7: R.one}
    for k in range(2, 7):
        Av[k] = R.var(k - 2)
    B, res = eliminate_B(R, Av)
    gens = list(symbols('A2 A3 A4 A5 A6'))
    sy = [R.to_sympy(e, gens) for e in res]
    G = groebner(sy, *gens, order='grevlex', modulus=p)
    exprs = list(G.exprs)
    unit = (len(exprs) == 1 and exprs[0] == 1) or exprs == [1]
    return unit, exprs


def transport(A, p):
    """A_0=A_1=1 solution -> q_1=q_8=1 gauge, via lambda^7 = 1/A_7."""
    assert A[7] % p
    e = pow(7, -1, p - 1)
    lam = pow(pow(A[7], p - 2, p), e, p)
    assert pow(lam, 7, p) == pow(A[7], p - 2, p)
    At = {k: (pow(lam, k, p) * A[k]) % p for k in range(8)}
    assert At[0] == 1 and At[7] == 1, (At[0], At[7])
    # rebuild B from scratch in the transported gauge (independent recomputation)
    R = Ring(0, p)
    R.one = {(): 1}
    Av = {k: ({(): At[k]} if At[k] % p else {}) for k in range(8)}
    Av[0] = {(): 1}
    B, res = eliminate_B(R, Av)
    for e2 in res:
        assert e2 == {}, ("transported point fails a residual equation", e2)
    Bv = {m: (B[m].get((), 0) % p) for m in range(11)}
    qv = {i: At[i - 1] for i in QIDX}
    tv = {j: Bv[j - 2] for j in TIDX}
    return qv, tv


# ---------------------------------------------------------------- E3 operator
def e3_matrix(qv, tv, p):
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
        flush("=" * 72)
        flush("PRIME p = %d   (7 | p-1 ? %s)" % (p, (p - 1) % 7 == 0))
        flush("=" * 72)
        flush("face system in the brief's gauge q_1=q_8=1: 17 equations "
              "(u^2..u^18 of 2qt'-3q't-u^2; the u^19 row vanishes identically) "
              "in 17 unknowns q_2..q_7, t_2..t_12")
        sols, elimdeg = solve_gauge_A1(p)
        flush("  [A0=A1=1] F_p-rational solutions of the quotient system: %d"
              % len(sols))
        unit, exprs = solve_gauge_A0A7_A1zero(p)
        flush("  [A1=0 branch, gauge A0=A7=1] GB = %s  (unit ideal: %s)"
              % (exprs if len(str(exprs)) < 120 else "<big>", unit))
        faces = []
        for A in sols:
            qv, tv = transport(A, p)
            bad = face_residual_qt(qv, tv, p)
            assert not bad, ("FACE VERIFICATION FAILED", qv, tv, bad)
            assert qv[1] == 1 and qv[8] == 1
            assert tv[2] % p and tv[12] % p, "t_2 or t_12 vanishes"
            faces.append((qv, tv))
        flush("face solutions in gauge q_1=q_8=1, verified exactly "
              "(2qt'-3q't-u^2 == 0 mod p, t_2 != 0, t_12 != 0): %d" % len(faces))
        recs = []
        for si, (qv, tv) in enumerate(faces):
            M, cols, ns = e3_matrix(qv, tv, p)
            rank, basis = nullspace_mod(M, p)
            flush("-" * 66)
            flush("face #%d" % si)
            flush("  q = %s" % [qv[i] for i in QIDX])
            flush("  t = %s" % [tv[j] for j in TIDX])
            flush("  E3 matrix %dx%d   rank = %d   kernel dim = %d"
                  % (len(M), len(M[0]), rank, len(basis)))
            kb = []
            for b in basis:
                bad, pvv, svv = verify_e3(b, cols, qv, tv, p)
                assert not bad, ("kernel vector fails E3", bad)
                flush("    kernel basis vector VERIFIED (E3 == 0 mod p):")
                flush("      p_ = %s" % {k: v for k, v in sorted(pvv.items()) if v})
                flush("      s_ = %s" % {k: v for k, v in sorted(svv.items()) if v})
                kb.append([int(x) for x in b])
            recs.append(dict(q=[qv[i] for i in QIDX], t=[tv[j] for j in TIDX],
                             shape=[len(M), len(M[0])], rank=rank,
                             kerdim=len(basis), kernel=kb,
                             cols=[k + str(i) for k, i in cols]))
        results[str(p)] = dict(elim_degree=elimdeg, A1zero_unit=bool(unit),
                               faces=recs)
    json.dump(results, open(out, 'w'), indent=1)
    for p in ('999983', '1000003'):
        flush("kernel dims p=%s: %s"
              % (p, [r['kerdim'] for r in results[p]['faces']]))
    flush("wrote " + out)
