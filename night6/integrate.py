"""night6 TASK 1 -- integration test for the 2-dimensional E3 kernel.

At a face solution (q,t) the E3 kernel is spanned by (p1,s1), (p2,s2).
Put  (p_, s_) = alpha*(p1,s1) + beta*(p2,s2)  and feed it into the full five
identities of the handoff:

    E0:  f'r - p_ g'                           = 0     (z^0)
    E1:  2f's_ + p_'r - p_ r' - 2q g'          = 0     (z^1)
    E2:  3f't + 2p_'s_ + q'r - p_ s_' - 2q r'  = 0     (z^2)
    E3:  3p_'t + 2q's_ - p_ t' - 2q s_'        = 0     (z^3)   [kernel]
    E4:  3q't - 2q t'                          = -u^2  (z^4)   [face]

Unknowns: f on u^0..u^8, g on u^0..u^12, r on u^1..u^12, and alpha, beta.
f_0 and g_0 never occur (only f', g'), so the live unknowns are
f_1..f_8, g_1..g_12, r_1..r_12, alpha, beta.

The system is weighted-homogeneous: with weight 1 on (alpha,beta), weight 2
on f and r, and weight 3 on g, every one of E0,E1,E2 is homogeneous (E0 and
E1 of weight 4 and 3 resp., E2 of weight 2).  So "(alpha,beta) != (0,0)" is a
projective question and is settled by two charts:

    chart A : alpha = 1, beta a free unknown
    chart B : alpha = 0, beta = 1

If both charts give the unit ideal, (alpha,beta) = (0,0) is forced.

Two variants per chart:
    (a) free
    (b) vertex non-degeneracy imposed by Rabinowitsch inverses of f_8 and
        g_12 (the vertices (8,16) of N(P) and (12,24) of N(Q)).
"""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flint
import e3_final as E

SCRATCH = os.environ.get('N6SCRATCH', '/tmp')

FIDX = list(range(1, 9))      # f_1..f_8
GIDX = list(range(1, 13))     # g_1..g_12
RIDX = list(range(1, 13))     # r_1..r_12


def flush(*a):
    print(*a)
    sys.stdout.flush()


# --------------------------------------------------- polynomials in the unknowns
# a "coefficient" is a dict: monomial (tuple of exponents) -> element of K
class Poly:
    """dict monomial -> K element, over a residue field K."""
    def __init__(self, K, d=None):
        self.K = K
        self.d = dict(d or {})

    def __add__(self, o):
        r = dict(self.d)
        for m, c in o.d.items():
            v = self.K.add(r.get(m, self.K.zero), c)
            if self.K.iszero(v):
                r.pop(m, None)
            else:
                r[m] = v
        return Poly(self.K, r)

    def scal(self, c):
        if self.K.iszero(c):
            return Poly(self.K)
        return Poly(self.K, {m: self.K.mul(v, c) for m, v in self.d.items()})

    def __mul__(self, o):
        r = {}
        for m1, c1 in self.d.items():
            for m2, c2 in o.d.items():
                m = tuple(a + b for a, b in zip(m1, m2))
                v = self.K.add(r.get(m, self.K.zero), self.K.mul(c1, c2))
                if self.K.iszero(v):
                    r.pop(m, None)
                else:
                    r[m] = v
        return Poly(self.K, r)

    def iszero(self):
        return not self.d


def var(K, nv, i):
    e = [0] * nv
    e[i] = 1
    return Poly(K, {tuple(e): K.one})


def const(K, nv, c):
    if K.iszero(c):
        return Poly(K)
    return Poly(K, {(0,) * nv: c})


# ------------------------------------------------------- u-polynomials over Poly
def umul(a, b, K):
    r = {}
    for i, ca in a.items():
        for j, cb in b.items():
            r[i + j] = r.get(i + j, Poly(K)) + ca * cb
    return {k: v for k, v in r.items() if not v.iszero()}


def uadd(*args):
    K = None
    r = {}
    for a in args:
        for k, v in a.items():
            K = v.K
            r[k] = (r.get(k, Poly(v.K)) + v)
    return {k: v for k, v in r.items() if not v.iszero()}


def uscal(a, c, K):
    return {k: v.scal(K.c(c)) for k, v in a.items()
            if not v.scal(K.c(c)).iszero()}


def uderiv(a, K, p):
    r = {}
    for k, v in a.items():
        if k > 0:
            w = v.scal(K.c(k % p))
            if not w.iszero():
                r[k - 1] = w
    return r


# -------------------------------------------------------------- Singular helper
def kstr(c, K):
    """K element -> Singular string (in the parameter `a` for extensions)."""
    cs = [int(x) for x in c.coeffs()]
    if not cs:
        return "0"
    ts = []
    for i, v in enumerate(cs):
        if v % K.p == 0:
            continue
        ts.append(str(v) if i == 0 else ("%d*a^%d" % (v, i)))
    return "(" + "+".join(ts) + ")" if ts else "0"


def run_singular(eqs, names, K, p, tag, extra_check=True):
    """eqs: list of Poly.  Returns (is_unit, dim, vdim, gb_size, stdout)."""
    nv = len(names)

    def pstr(P):
        ts = []
        for m, c in P.d.items():
            t = kstr(c, K)
            for i, e in enumerate(m):
                if e:
                    t += "*%s^%d" % (names[i], e)
            ts.append(t)
        return "+".join(ts) if ts else "0"

    if K.deg == 1:
        ringline = "ring R=%d,(%s),dp;" % (p, ",".join(names))
        mp = ""
    else:
        ringline = "ring R=(%d,a),(%s),dp;" % (p, ",".join(names))
        mp = "minpoly = %s;" % K.h.str().replace('x', 'a').replace(' ', '')
    src = [ringline]
    if mp:
        src.append(mp)
    src.append("ideal I=%s;" % (",\n".join(pstr(e) for e in eqs)))
    src += ["option(redSB);", "ideal G=std(I);",
            '"SIZE:"; size(G);',
            '"ISUNIT:"; int u = (size(G)==1 && G[1]==1); u;',
            '"DIM:"; dim(G);',
            '"GB:";', "int i;", "for(i=1;i<=size(G);i++){ G[i]; }",
            '"END";', "quit;"]
    path = os.path.join(SCRATCH, 'integ_%s.sing' % tag)
    open(path, 'w').write("\n".join(src) + "\n")
    t0 = time.time()
    out = subprocess.run(['Singular', '-q', path], capture_output=True,
                         text=True, timeout=10800)
    txt = out.stdout
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    assert 'ISUNIT:' in lines, txt[:3000]
    size = int(lines[lines.index('SIZE:') + 1])
    isunit = int(lines[lines.index('ISUNIT:') + 1]) == 1
    dim = int(lines[lines.index('DIM:') + 1])
    gb = lines[lines.index('GB:') + 1:lines.index('END')]
    return isunit, dim, size, gb, time.time() - t0, path


# --------------------------------------------------------------------- builder
def build_system(K, p, q, t, v1, v2, cols, chart, rabin):
    """Return (eqs, names, meta)."""
    pv1, sv1 = E.split(v1, cols)
    pv2, sv2 = E.split(v2, cols)
    names = (["f%d" % i for i in FIDX] + ["g%d" % j for j in GIDX]
             + ["r%d" % k for k in RIDX])
    if chart == 'A':
        names.append("be")
    if rabin:
        names += ["Wf", "Wg"]
    nv = len(names)
    idx = {n: i for i, n in enumerate(names)}
    V = lambda n: var(K, nv, idx[n])
    C = lambda c: const(K, nv, c)

    # p_, s_
    if chart == 'A':
        be = V("be")
        pu = {}
        su = {}
        for i in E.PIDX:
            pu[i] = C(pv1[i]) + be * C(pv2[i])
        for j in E.SIDX:
            su[j] = C(sv1[j]) + be * C(sv2[j])
    else:
        pu = {i: C(pv2[i]) for i in E.PIDX}
        su = {j: C(sv2[j]) for j in E.SIDX}
    pu = {k: v for k, v in pu.items() if not v.iszero()}
    su = {k: v for k, v in su.items() if not v.iszero()}

    qu = {i: C(q[i]) for i in E.QIDX if not K.iszero(q[i])}
    tu = {j: C(t[j]) for j in E.TIDX if not K.iszero(t[j])}
    fu = {i: V("f%d" % i) for i in FIDX}
    gu = {j: V("g%d" % j) for j in GIDX}
    ru = {k: V("r%d" % k) for k in RIDX}

    fd = uderiv(fu, K, p)
    gd = uderiv(gu, K, p)
    rd = uderiv(ru, K, p)
    qd = uderiv(qu, K, p)
    td = uderiv(tu, K, p)
    pd = uderiv(pu, K, p)
    sd = uderiv(su, K, p)

    E0 = uadd(umul(fd, ru, K), uscal(umul(pu, gd, K), p - 1, K))
    E1 = uadd(uscal(umul(fd, su, K), 2, K), umul(pd, ru, K),
              uscal(umul(pu, rd, K), p - 1, K),
              uscal(umul(qu, gd, K), p - 2, K))
    E2 = uadd(uscal(umul(fd, tu, K), 3, K), uscal(umul(pd, su, K), 2, K),
              umul(qd, ru, K), uscal(umul(pu, sd, K), p - 1, K),
              uscal(umul(qu, rd, K), p - 2, K))
    E3 = uadd(uscal(umul(pd, tu, K), 3, K), uscal(umul(qd, su, K), 2, K),
              uscal(umul(pu, td, K), p - 1, K),
              uscal(umul(qu, sd, K), p - 2, K))

    eqs = []
    for name, Ex in (("E0", E0), ("E1", E1), ("E2", E2)):
        for k in sorted(Ex):
            eqs.append(Ex[k])
    if rabin:
        eqs.append(V("f8") * V("Wf") + C(K.smul(p - 1, K.one)))
        eqs.append(V("g12") * V("Wg") + C(K.smul(p - 1, K.one)))
    meta = dict(n_E0=len(E0), n_E1=len(E1), n_E2=len(E2),
                E3_identically_zero=(len(E3) == 0),
                n_eqs=len(eqs), n_vars=nv, names=names)
    return eqs, names, meta
