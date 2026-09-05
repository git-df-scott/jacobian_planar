"""Night 6 -- the E3 kernel computation.

The mathematics is built from scratch here; Singular is used only as a
Groebner engine on the 6 residual equations in q_2..q_7, and every point it
produces is rebuilt and verified by exact substitution.

FACE SYSTEM (the brief's gauge q_1 = q_8 = 1)
    2*q*t' - 3*q'*t = u^2,   q on u^1..u^8,  t on u^2..u^12
    coefficient of u^(n-1), n = i+j:  sum_{i+j=n} (2j - 3i) q_i t_j = [n==3]
    n = 3..20; the n = 20 row vanishes identically
    -> 17 equations in 17 unknowns (q_2..q_7, t_2..t_12)

  Writing q = u*A (deg A = 7, A_k = q_{k+1}) and t = u^2*B (deg B = 10,
  B_k = t_{k+2}) the same system is
    sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m == 0],  m = 0..17 (m=17 vanishes)
  with A_0 = A_7 = 1.  The equation is LINEAR in t for fixed q and the rows
  m = 0..10 are triangular (the i=0 term is (1+2m) B_m), so t is eliminated
  outright, leaving 6 residual equations in q_2..q_7 alone.

E3 OPERATOR
    E3(p_,s_) = 3*p_'*t + 2*q'*s_ - p_*t' - 2*q*s_'
    p_ on u^1..u^8 (8 columns), s_ on u^2..u^12 (11 columns)
    coefficient of u^(n-1): sum_{i+j=n}(3i-j) p_i t_j + sum_{i+j=n}(2i-2j) q_i s_j
    n = 3..20  ->  an 18 x 19 matrix.

Each irreducible factor h of the degree-35 eliminant is handled in the
residue field F_p[T]/(h), so all 35 face solutions are covered, not only the
F_p-rational ones.
"""
import sys, os, re, json, time, subprocess
import flint

QIDX = list(range(1, 9))
TIDX = list(range(2, 13))
PIDX = list(range(1, 9))
SIDX = list(range(2, 13))
SCRATCH = os.environ.get('N6SCRATCH', '/tmp')


def flush(*a):
    print(*a)
    sys.stdout.flush()


# --------------------------------------------- multivariate polys over F_p
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


def build_residuals(p):
    """6 residual equations in A_1..A_6 (gauge A_0 = A_7 = 1)."""
    nv = 6
    one = {(0,) * nv: 1}
    A = {0: one, 7: one}
    for k in range(1, 7):
        e = [0] * nv
        e[k - 1] = 1
        A[k] = {tuple(e): 1}
    B = {}
    for m in range(0, 11):
        c0 = (1 + 2 * m) % p
        assert c0
        acc = dict(one) if m == 0 else {}
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = (1 + 2 * j - 3 * i) % p
            if c:
                acc = padd(acc, {k: (-c * v) % p
                                 for k, v in pmul(A[i], B[j], p).items()}, p)
        inv = pow(c0, p - 2, p)
        B[m] = {k: v * inv % p for k, v in acc.items()}
    res = []
    for m in range(11, 18):
        acc = {}
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = (1 + 2 * j - 3 * i) % p
                if c:
                    acc = padd(acc, {k: c * v % p
                                     for k, v in pmul(A[i], B[j], p).items()}, p)
        res.append(acc)
    assert res[-1] == {}, "the m = 17 row is not identically zero"
    return res[:-1]


def count_face_rows(p):
    live, dead = 0, []
    for n in range(3, 21):
        terms = [2 * (n - i) - 3 * i for i in QIDX if (n - i) in TIDX]
        if all(c % p == 0 for c in terms):
            dead.append(n)
        else:
            live += 1
    return live, dead


# ------------------------------------------------------ residue field F_p[T]/h
class Ext:
    def __init__(self, h, p):
        self.h, self.p = h, p
        self.deg = h.degree()
        self.one = flint.nmod_poly([1], p)
        self.zero = flint.nmod_poly([], p)

    def c(self, k):
        return flint.nmod_poly([int(k) % self.p], self.p)

    def gen(self):
        return flint.nmod_poly([0, 1], self.p) % self.h

    def mul(self, a, b):
        return (a * b) % self.h

    def add(self, a, b):
        return (a + b) % self.h

    def sub(self, a, b):
        return (a - b) % self.h

    def smul(self, k, a):
        return (self.c(k) * a) % self.h

    def inv(self, a):
        g, s, _ = a.xgcd(self.h)
        assert g.degree() == 0, "not invertible"
        ci = pow(int(g[0]), self.p - 2, self.p)
        return (s * flint.nmod_poly([ci], self.p)) % self.h

    def iszero(self, a):
        return a.is_zero()

    def show(self, a):
        return a.str().replace(' ', '') if not a.is_zero() else "0"


def evalpoly_ext(coeffs, x, K):
    """coeffs: list of ints (low -> high); Horner in K"""
    r = K.zero
    for c in reversed(coeffs):
        r = K.add(K.mul(r, x), K.c(c))
    return r


# ------------------------------------------------------------------- Singular
def parse_poly(s, nv=6):
    s = s.replace(' ', '')
    out = {}
    for sign, body in re.findall(r'([+-]?)([^+-]+)', s):
        if not body:
            continue
        coef, mon = 1, [0] * nv
        for part in body.split('*'):
            if part.isdigit():
                coef *= int(part)
            else:
                m = re.fullmatch(r'A(\d)(?:\^(\d+))?', part)
                assert m, (s, part)
                mon[int(m.group(1)) - 1] += int(m.group(2) or 1)
        if sign == '-':
            coef = -coef
        out[tuple(mon)] = out.get(tuple(mon), 0) + coef
    return out


def singular_lexgb(res, p, tag):
    def s(f):
        ts = []
        for m, c in sorted(f.items()):
            t = str(c % p)
            for i, e in enumerate(m):
                if e:
                    t += "*A%d^%d" % (i + 1, e)
            ts.append(t)
        return "+".join(ts)
    src = ["ring R=%d,(A1,A2,A3,A4,A5,A6),dp;" % p,
           "ideal I=%s;" % (",\n".join(s(f) for f in res)),
           "option(redSB);", "ideal G=std(I);",
           '"VDIM:"; vdim(G); "DIM:"; dim(G);',
           "ring S=%d,(A1,A2,A3,A4,A5,A6),lp;" % p,
           "ideal L=fglm(R,G);", '"LEXGB:";', "int i;",
           "for(i=1;i<=size(L);i++){ L[i]; }", '"END";', "quit;"]
    path = os.path.join(SCRATCH, 'face_%s.sing' % tag)
    open(path, 'w').write("\n".join(src) + "\n")
    t0 = time.time()
    out = subprocess.run(['Singular', '-q', path], capture_output=True,
                         text=True, timeout=7200).stdout
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    assert 'VDIM:' in lines and 'LEXGB:' in lines, out[:2000]
    vdim = int(lines[lines.index('VDIM:') + 1])
    dim = int(lines[lines.index('DIM:') + 1])
    gbs = lines[lines.index('LEXGB:') + 1:lines.index('END')]
    return vdim, dim, [parse_poly(g) for g in gbs], gbs, time.time() - t0


# ------------------------------------------ face point + verification over K
def face_point(K, x, shape, p):
    """x = value of A_6 = q_7 in K; shape maps k -> coeff list for A_k."""
    A = {0: K.one, 7: K.one, 6: x}
    for k in range(1, 6):
        num, den = shape[k]
        A[k] = K.mul(K.sub(K.zero, evalpoly_ext(num, x, K)),
                     K.inv(evalpoly_ext(den, x, K)))
    B = {}
    for m in range(0, 11):
        acc = K.one if m == 0 else K.zero
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = (1 + 2 * j - 3 * i) % p
            if c:
                acc = K.sub(acc, K.smul(c, K.mul(A[i], B[j])))
        B[m] = K.smul(pow((1 + 2 * m) % p, p - 2, p), acc)
    for m in range(11, 18):
        acc = K.zero
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = (1 + 2 * j - 3 * i) % p
                if c:
                    acc = K.add(acc, K.smul(c, K.mul(A[i], B[j])))
        assert K.iszero(acc), ("residual row m=%d nonzero" % m)
    q = {i: A[i - 1] for i in QIDX}
    t = {j: B[j - 2] for j in TIDX}
    return q, t


def face_residual(q, t, K, p):
    res = {}
    for i, qi in q.items():
        for j, tj in t.items():
            c = (2 * j - 3 * i) % p
            if c:
                k = i + j - 1
                res[k] = K.add(res.get(k, K.zero), K.smul(c, K.mul(qi, tj)))
    res[2] = K.sub(res.get(2, K.zero), K.one)
    return {k: v for k, v in res.items() if not K.iszero(v)}


# ------------------------------------------------------------------ E3 matrix
def e3_matrix(q, t, K, p, s_min=2):
    sidx = list(range(s_min, 13))
    cols = [('p', i) for i in PIDX] + [('s', j) for j in sidx]
    ns = list(range(min(3, 1 + s_min), 21))
    M = [[K.zero] * len(cols) for _ in ns]
    for ri, n in enumerate(ns):
        for ci, (kind, k) in enumerate(cols):
            if kind == 'p':
                i, j = k, n - k
                if j in TIDX:
                    M[ri][ci] = K.smul((3 * i - j) % p, t[j])
            else:
                j, i = k, n - k
                if i in QIDX:
                    M[ri][ci] = K.smul((2 * i - 2 * j) % p, q[i])
    return M, cols, ns


def nullspace_ext(M, K):
    m, n = len(M), len(M[0])
    A = [row[:] for row in M]
    piv, r = [], 0
    for c in range(n):
        pr = next((rr for rr in range(r, m) if not K.iszero(A[rr][c])), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = K.inv(A[r][c])
        A[r] = [K.mul(x, iv) for x in A[r]]
        for rr in range(m):
            if rr != r and not K.iszero(A[rr][c]):
                f = A[rr][c]
                A[rr] = [K.sub(a, K.mul(f, b)) for a, b in zip(A[rr], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [K.zero] * n
        v[fc] = K.one
        for ri, pc in enumerate(piv):
            v[pc] = K.sub(K.zero, A[ri][fc])
        basis.append(v)
    return r, basis


def apply_e3(pv, sv, q, t, K, p):
    res = {}
    for i, pi in pv.items():
        for j, tj in t.items():
            c = (3 * i - j) % p
            if c:
                k = i + j - 1
                res[k] = K.add(res.get(k, K.zero), K.smul(c, K.mul(pi, tj)))
    for i, qi in q.items():
        for j, sj in sv.items():
            c = (2 * i - 2 * j) % p
            if c:
                k = i + j - 1
                res[k] = K.add(res.get(k, K.zero), K.smul(c, K.mul(qi, sj)))
    return {k: v for k, v in res.items() if not K.iszero(v)}


def split(vec, cols):
    pv, sv = {}, {}
    for val, (kind, k) in zip(vec, cols):
        (pv if kind == 'p' else sv)[k] = val
    return pv, sv


def pstr(d, name, K):
    ts = ["(%s)*u^%d" % (K.show(v), k) for k, v in sorted(d.items())
          if not K.iszero(v)]
    return "%s = %s" % (name, " + ".join(ts) if ts else "0")


# --------------------------------------------------------------------- driver
def run(p):
    flush("=" * 78)
    flush("PRIME p = %d        7 divides p-1 ?  %s" % (p, (p - 1) % 7 == 0))
    flush("=" * 78)
    live, dead = count_face_rows(p)
    flush("STEP 1  face system in the gauge q_1 = q_8 = 1")
    flush("   rows n = 3..20 of  sum_{i+j=n} (2j-3i) q_i t_j = [n==3];"
          "  rows vanishing identically: n = %s" % dead)
    flush("   => %d equations in %d unknowns (q_2..q_7 and t_2..t_12)"
          % (live, 17))
    assert (live, 17) == (17, 17)
    res = build_residuals(p)
    flush("   t_2..t_12 eliminated (linear in t at fixed q, triangular);"
          " %d residual equations in q_2..q_7, total degrees %s"
          % (len(res), [max(sum(m) for m in f) for f in res]))
    vdim, dim, gb, gbs, secs = singular_lexgb(res, p, str(p))
    flush("   residual ideal: dim = %d, vdim = %d   (%.0fs)" % (dim, vdim, secs))
    flush("   lex Groebner basis (shape position, A_k = q_{k+1}):")
    for g in gbs:
        flush("      " + g)

    uni = [g for g in gb if all(m[i] == 0 for m in g for i in range(5))]
    assert len(uni) == 1
    U = uni[0]
    deg = max(m[5] for m in U)
    ucoef = [0] * (deg + 1)
    for m, c in U.items():
        ucoef[m[5]] = c % p
    f = flint.nmod_poly([c % p for c in ucoef], p)
    facs = [(g, e) for g, e in f.factor()[1]]
    degs = sorted((g.degree(), e) for g, e in facs)
    flush("   eliminant in q_7: degree %d, irreducible factor degrees"
          " (degree, multiplicity) = %s" % (deg, degs))
    flush("   sum of factor degrees = %d ; F_p-rational roots = %d"
          % (sum(g.degree() * e for g, e in facs),
             sum(1 for g, e in facs if g.degree() == 1)))

    # shape polynomials: A_k = -num_k(A_6)/den_k(A_6), k = 1..5
    shape = {}
    for g in gb:
        if g is U:
            continue
        lin = [i for i in range(5) if any(m[i] for m in g)]
        assert len(lin) == 1, ("not shape position", g)
        k = lin[0] + 1
        num = {}
        den = {}
        for m, c in g.items():
            if m[k - 1]:
                assert m[k - 1] == 1
                den[m[5]] = (den.get(m[5], 0) + c) % p
            else:
                num[m[5]] = (num.get(m[5], 0) + c) % p
        nl = [0] * (max(num or [0]) + 1)
        for e, c in num.items():
            nl[e] = c
        dl = [0] * (max(den or [0]) + 1)
        for e, c in den.items():
            dl[e] = c
        shape[k] = (nl, dl)
    assert sorted(shape) == [1, 2, 3, 4, 5]

    flush("")
    flush("STEP 2/3  face solutions and their E3 kernels")
    recs = []
    covered = 0
    for gi, (h, mult) in enumerate(sorted(facs, key=lambda x: x[0].degree())):
        d = h.degree()
        assert mult == 1, "eliminant is not squarefree"
        K = Ext(h, p)
        x = K.gen()
        q, t = face_point(K, x, shape, p)
        bad = face_residual(q, t, K, p)
        assert not bad, ("FACE VERIFICATION FAILED", bad)
        assert not K.iszero(t[2]) and not K.iszero(t[12])
        assert K.show(q[1]) == "1" and K.show(q[8]) == "1"
        covered += d
        M, cols, ns = e3_matrix(q, t, K, p)
        rank, basis = nullspace_ext(M, K)
        Mx, colsx, nsx = e3_matrix(q, t, K, p, s_min=1)
        rankx, basisx = nullspace_ext(Mx, K)
        zrows = [ns[i] - 1 for i in range(len(ns))
                 if all(K.iszero(v) for v in M[i])]
        zrowsx = [nsx[i] - 1 for i in range(len(nsx))
                  if all(K.iszero(v) for v in Mx[i])]
        flush("-" * 74)
        flush("face family #%d : residue field F_p[T]/(h),  deg h = %d"
              "  (covers %d of the 35 face solutions)" % (gi, d, d))
        flush("   h(T) = %s" % h.str().replace(' ', ''))
        if d == 1:
            flush("   this family is F_p-rational")
            flush("   q_1..q_8  = %s" % [K.show(q[i]) for i in QIDX])
            flush("   t_2..t_12 = %s" % [K.show(t[j]) for j in TIDX])
        flush("   deg q = 8 (q_8 != 0): True ;  deg t = 12 (t_12 != 0): %s ;"
              "  t_2 != 0: %s"
              % (not K.iszero(t[12]), not K.iszero(t[2])))
        flush("   support-restricted E3  (p_ on u^1..u^8, s_ on u^2..u^12)")
        flush("      matrix %d x %d over the residue field, rows u^%d..u^%d,"
              " identically zero rows: %s"
              % (len(M), len(M[0]), ns[0] - 1, ns[-1] - 1, zrows or "none"))
        flush("      rank = %d      KERNEL DIMENSION = %d" % (rank, len(basis)))
        kb = []
        for b in basis:
            pv, sv = split(b, cols)
            assert not apply_e3(pv, sv, q, t, K, p), "kernel vector fails E3"
            flush("      kernel basis vector (VERIFIED: E3(p_,s_) = 0):")
            flush("         %s" % pstr(pv, "p_", K))
            flush("         %s" % pstr(sv, "s_", K))
            nzp = [k for k, v in pv.items() if not K.iszero(v)]
            nzs = [k for k, v in sv.items() if not K.iszero(v)]
            flush("         val p_ = %s, deg p_ = %s, val s_ = %s, deg s_ = %s"
                  % (min(nzp, default=None), max(nzp, default=None),
                     min(nzs, default=None), max(nzs, default=None)))
            kb.append([K.show(v) for v in b])
        v0 = [K.zero] * len(colsx)
        for ci, (kind, k) in enumerate(colsx):
            if kind == 's' and k in q:
                v0[ci] = q[k]
        pv0, sv0 = split(v0, colsx)
        in0 = not apply_e3(pv0, sv0, q, t, K, p)
        flush("   reference, s_ allowed from u^1 (20 columns): %d x %d,"
              " identically zero rows %s, rank = %d, kernel dim = %d"
              % (len(Mx), len(Mx[0]), zrowsx or "none", rankx, len(basisx)))
        flush("      (p_, s_) = (0, q) lies in that relaxed kernel: %s" % in0)
        recs.append(dict(hdeg=d, h=h.str(), rank=rank, kerdim=len(basis),
                         shape=[len(M), len(M[0])], kernel=kb,
                         cols=["%s%d" % (k, i) for k, i in cols],
                         rational=(d == 1),
                         q=[K.show(q[i]) for i in QIDX],
                         t=[K.show(t[j]) for j in TIDX],
                         relaxed=dict(shape=[len(Mx), len(Mx[0])], rank=rankx,
                                      kerdim=len(basisx),
                                      zero_q_in_kernel=in0)))
    flush("-" * 74)
    flush("   face solutions covered: %d of 35" % covered)
    assert covered == 35
    return dict(vdim=vdim, dim=dim, elim_factor_degrees=degs,
                n_rational=sum(1 for r in recs if r['rational']),
                lexgb=gbs, families=recs)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'night6/e3_kernel_results.json'
    R = {}
    for p in (999983, 1000003):
        R[str(p)] = run(p)
        flush("")
    json.dump(R, open(out, 'w'), indent=1)
    flush("=" * 78)
    flush("STEP 4  cross-prime comparison")
    for p in R:
        flush("   p=%s : dim=%d, vdim=%d, eliminant factor degrees %s,"
              " F_p-rational families %d"
              % (p, R[p]['dim'], R[p]['vdim'], R[p]['elim_factor_degrees'],
                 R[p]['n_rational']))
        flush("            restricted kernel dims per family %s (covering %s"
              " face solutions each)"
              % ([f['kerdim'] for f in R[p]['families']],
                 [f['hdeg'] for f in R[p]['families']]))
        flush("            relaxed  kernel dims per family %s"
              % [f['relaxed']['kerdim'] for f in R[p]['families']])
    ka = set(f['kerdim'] for f in R['999983']['families'])
    kb = set(f['kerdim'] for f in R['1000003']['families'])
    flush("   restricted kernel dimension is constant over all 35 face"
          " solutions at p=999983: %s (value %s)" % (len(ka) == 1, sorted(ka)))
    flush("   restricted kernel dimension is constant over all 35 face"
          " solutions at p=1000003: %s (value %s)" % (len(kb) == 1, sorted(kb)))
    flush("   the two primes agree: %s" % (ka == kb))
    flush("   vdim agrees across the two primes: %s"
          % (R['999983']['vdim'] == R['1000003']['vdim']))
    flush("wrote " + out)
