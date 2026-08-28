"""night6 -- characteristic-zero integration test for the E3 kernel.

Mirror of night6/integrate.py (the mod-p instrument) with exact arithmetic.
The five identities of the handoff:

    E0:  f'r - p_ g'                           = 0     (z^0)
    E1:  2f's_ + p_'r - p_ r' - 2q g'          = 0     (z^1)
    E2:  3f't + 2p_'s_ + q'r - p_ s_' - 2q r'  = 0     (z^2)
    E3:  3p_'t + 2q's_ - p_ t' - 2q s_'        = 0     (z^3)  [kernel]
    E4:  3q't - 2q t'                          = -u^2  (z^4)  [face]

with (p_, s_) = alpha*(p1,s1) + beta*(p2,s2) a general element of the
2-dimensional E3 kernel at a face solution (q,t) in K = Q[T]/(h).

Charts (the system is weighted-homogeneous, weight 1 on (alpha,beta), 2 on f
and r, 3 on g):
    chart A : alpha = 1, beta a free unknown
    chart B : alpha = 0, beta = 1

Singular is used as the Groebner engine over Q.  The number field is carried
as an EXTRA VARIABLE T with the minimal polynomial h(T) adjoined to the ideal
(equivalent to Singular's `minpoly`, and it works for h of any degree); the
unit-ideal verdict then means: no solution for ANY root of h.
"""
import os, sys, time, subprocess
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_lib as C
from integrate import Poly, var, const, umul, uadd

SCRATCH = os.environ.get('N6SCRATCH', '/tmp')

FIDX = list(range(1, 9))
GIDX = list(range(1, 13))
RIDX = list(range(1, 13))


def uscal0(a, c, K):
    r = {}
    for k, v in a.items():
        w = v.scal(K.c(c))
        if not w.iszero():
            r[k] = w
    return r


def uderiv0(a, K):
    r = {}
    for k, v in a.items():
        if k > 0:
            w = v.scal(K.c(k))
            if not w.iszero():
                r[k - 1] = w
    return r


def build_system0(K, q, t, v1, v2, cols, chart, rabin, zero_ps=False):
    """Return (eqs, names, meta).  zero_ps=True is the control (p_,s_)=(0,0)."""
    names = (["f%d" % i for i in FIDX] + ["g%d" % j for j in GIDX]
             + ["r%d" % k for k in RIDX])
    if chart == 'A' and not zero_ps:
        names.append("be")
    if rabin:
        names += ["Wf", "Wg"]
    names.append("T")
    nv = len(names)
    idx = {n: i for i, n in enumerate(names)}
    V = lambda n: var(K, nv, idx[n])
    Co = lambda c: const(K, nv, c)

    if zero_ps:
        pu, su = {}, {}
    else:
        pv1, sv1 = C.split(v1, cols)
        pv2, sv2 = C.split(v2, cols)
        if chart == 'A':
            be = V("be")
            pu = {i: Co(pv1[i]) + be * Co(pv2[i]) for i in C.PIDX}
            su = {j: Co(sv1[j]) + be * Co(sv2[j]) for j in C.SIDX}
        else:
            pu = {i: Co(pv2[i]) for i in C.PIDX}
            su = {j: Co(sv2[j]) for j in C.SIDX}
        pu = {k: v for k, v in pu.items() if not v.iszero()}
        su = {k: v for k, v in su.items() if not v.iszero()}

    qu = {i: Co(q[i]) for i in C.QIDX if not K.iszero(q[i])}
    tu = {j: Co(t[j]) for j in C.TIDX if not K.iszero(t[j])}
    fu = {i: V("f%d" % i) for i in FIDX}
    gu = {j: V("g%d" % j) for j in GIDX}
    ru = {k: V("r%d" % k) for k in RIDX}

    fd, gd, rd = uderiv0(fu, K), uderiv0(gu, K), uderiv0(ru, K)
    qd, td = uderiv0(qu, K), uderiv0(tu, K)
    pd, sd = uderiv0(pu, K), uderiv0(su, K)

    E0 = uadd(umul(fd, ru, K), uscal0(umul(pu, gd, K), -1, K))
    E1 = uadd(uscal0(umul(fd, su, K), 2, K), umul(pd, ru, K),
              uscal0(umul(pu, rd, K), -1, K), uscal0(umul(qu, gd, K), -2, K))
    E2 = uadd(uscal0(umul(fd, tu, K), 3, K), uscal0(umul(pd, su, K), 2, K),
              umul(qd, ru, K), uscal0(umul(pu, sd, K), -1, K),
              uscal0(umul(qu, rd, K), -2, K))
    E3 = uadd(uscal0(umul(pd, tu, K), 3, K), uscal0(umul(qd, su, K), 2, K),
              uscal0(umul(pu, td, K), -1, K), uscal0(umul(qu, sd, K), -2, K))

    eqs = []
    for Ex in (E0, E1, E2):
        for k in sorted(Ex):
            eqs.append(Ex[k])
    if rabin:
        eqs.append(V("f8") * V("Wf") + Co(K.smul(-1, K.one)))
        eqs.append(V("g12") * V("Wg") + Co(K.smul(-1, K.one)))
    meta = dict(n_E0=len(E0), n_E1=len(E1), n_E2=len(E2),
                E3_identically_zero=(len(E3) == 0),
                n_eqs=len(eqs), n_vars=nv, names=names)
    return eqs, names, meta


# ------------------------------------------------------------------ Singular
def _terms_of(P, names, K, tvar="T"):
    """Poly over K -> list of signed integer-coefficient term strings.

    Each K element is a polynomial in T; denominators are cleared globally.
    """
    ti = names.index(tvar)
    raw = []           # (monomial tuple, T-exponent, Fraction)
    for m, c in P.d.items():
        for e, coef in enumerate(K.coeffs(c)):
            if coef:
                raw.append((m, e, coef))
    if not raw:
        return ["+0"]
    den = 1
    for _, _, coef in raw:
        d = coef.denominator
        g = den
        b = d
        while b:
            g, b = b, g % b
        den = den * d // g
    out = []
    for m, e, coef in raw:
        v = coef * den
        assert v.denominator == 1
        v = int(v)
        s = ("+" if v > 0 else "-") + str(abs(v))
        mm = list(m)
        mm[ti] += e
        for i, ex in enumerate(mm):
            if ex:
                s += "*%s^%d" % (names[i], ex)
        out.append(s)
    return out


def _stmts(terms, name, per=6):
    out = ["poly %s = 0;" % name]
    for i in range(0, len(terms), per):
        out.append("%s = %s %s;" % (name, name, "".join(terms[i:i + per])))
    return out


def hpoly_terms(K, names, tvar="T"):
    """h(T) as signed integer terms (h monic over Q -> clear denominators)."""
    cs = [F(int(c.p), int(c.q)) for c in K.h.coeffs()]
    den = 1
    for c in cs:
        d = c.denominator
        g, b = den, d
        while b:
            g, b = b, g % b
        den = den * d // g
    out = []
    for e, c in enumerate(cs):
        v = int(c * den)
        if v:
            s = ("+" if v > 0 else "-") + str(abs(v))
            if e:
                s += "*%s^%d" % (tvar, e)
            out.append(s)
    return out


def run_singular0(eqs, names, K, tag, timeout=36000, want_gb=True):
    src = ["ring R = 0,(%s),dp;" % ",".join(names)]
    enames = []
    for i, e in enumerate(eqs):
        n = "q%d" % i
        src += _stmts(_terms_of(e, names, K), n)
        enames.append(n)
    src += _stmts(hpoly_terms(K, names), "hh")
    enames.append("hh")
    src += ["ideal I = %s;" % ",".join(enames),
            "option(redSB);",
            "int t0 = timer;",
            "ideal G = std(I);",
            '"SECS:"; (timer-t0) div 1000;',
            '"SIZE:"; size(G);',
            '"ISUNIT:"; int uu = (size(G)==1 && G[1]==1); uu;',
            '"DIM:"; dim(G);']
    if want_gb:
        src += ['"GB:";', "int i;",
                "for(i=1;i<=size(G);i++){ if(i<=40){G[i];} }"]
    else:
        src += ['"GB:";']
    src += ['"END";', "quit;"]
    path = os.path.join(SCRATCH, 'char0_%s.sing' % tag)
    open(path, 'w').write("\n".join(src) + "\n")
    t0 = time.time()
    out = subprocess.run(['Singular', '-q', path], capture_output=True,
                         text=True, timeout=timeout)
    txt = out.stdout
    open(os.path.join(SCRATCH, 'char0_%s.out' % tag), 'w').write(txt)
    lines = [l.strip() for l in txt.splitlines() if l.strip()
             and not l.startswith('// **')]
    assert 'ISUNIT:' in lines, txt[:4000]
    size = int(lines[lines.index('SIZE:') + 1])
    isunit = int(lines[lines.index('ISUNIT:') + 1]) == 1
    dim = int(lines[lines.index('DIM:') + 1])
    gb = lines[lines.index('GB:') + 1:lines.index('END')]
    return isunit, dim, size, gb, time.time() - t0, path
