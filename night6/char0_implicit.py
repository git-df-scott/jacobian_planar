"""night6 -- characteristic-zero integration test, IMPLICIT encoding.

The face solution is not written out as an explicit element of the degree-35
number field (which carries ~371-bit coefficients).  Instead the face system
itself is carried in the ideal:

    variables  A_1..A_6  (= q_2..q_7),   gauge q_1 = q_8 = 1
    q_i = A_{i-1};  t_j = B_{j-2}(A), the B_m being the polynomials over Q
    produced by the triangular elimination of t from the face equation
    + the 6 residual face equations in A (total degree 9)

The eliminant of that residual ideal is irreducible of degree 35 over Q
(night6/CHAR0_INTEGRATION.md section 1), so the residual ideal is exactly the
single irreducible factor: this one system covers all 35 face solutions.

The E3 kernel is carried the same way: p_1..p_8 and s_2..s_12 are unknowns
subject to the 18 rows of

    E3:  3p_'t + 2q's_ - p_t' - 2q s_' = 0

The char-0 rref of that 18 x 19 matrix has free columns exactly s_11 and s_12
(measured, night6/CHAR0_INTEGRATION.md section 2), so the kernel coordinates
(alpha,beta) ARE the u^11 and u^12 coefficients of s_, and the two charts are

    chart A :  s_11 = 1, s_12 a free unknown        (alpha = 1, beta free)
    chart B :  s_11 = 0, s_12 = 1                   (alpha = 0, beta = 1)

Every coefficient in the resulting system is a small integer.
"""
import os, sys, time, subprocess
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_face as CF

SCRATCH = os.environ.get('N6SCRATCH', '/tmp')

QIDX = list(range(1, 9))
TIDX = list(range(2, 13))
PIDX = list(range(1, 9))
SIDX = list(range(2, 13))
FIDX = list(range(1, 9))
GIDX = list(range(1, 13))
RIDX = list(range(1, 13))


# --------------------------------------------------- named-variable polynomials
def mono(*pairs):
    d = {}
    for n, e in pairs:
        if e:
            d[n] = d.get(n, 0) + e
    return tuple(sorted(d.items()))


def mp_add(a, b):
    r = dict(a)
    for m, c in b.items():
        v = r.get(m, F(0)) + c
        if v:
            r[m] = v
        else:
            r.pop(m, None)
    return r


def mp_mul(a, b):
    r = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            d = dict(m1)
            for n, e in m2:
                d[n] = d.get(n, 0) + e
            m = tuple(sorted(d.items()))
            v = r.get(m, F(0)) + c1 * c2
            if v:
                r[m] = v
            else:
                r.pop(m, None)
    return r


def mp_scal(a, c):
    c = F(c)
    if not c:
        return {}
    return {m: v * c for m, v in a.items()}


ONE = {(): F(1)}
ZERO = {}


def V(name):
    return {mono((name, 1)): F(1)}


def CONST(c):
    c = F(c)
    return {(): c} if c else {}


def from_A(f):
    """dict 6-tuple-exponent -> Fraction  ->  named polynomial in A1..A6"""
    out = {}
    for m, c in f.items():
        out[mono(*[("A%d" % (i + 1), e) for i, e in enumerate(m)])] = F(c)
    return out


# ------------------------------------------------------- u-polynomials over MP
def umul(a, b):
    r = {}
    for i, ca in a.items():
        for j, cb in b.items():
            r[i + j] = mp_add(r.get(i + j, ZERO), mp_mul(ca, cb))
    return {k: v for k, v in r.items() if v}


def uadd(*args):
    r = {}
    for a in args:
        for k, v in a.items():
            r[k] = mp_add(r.get(k, ZERO), v)
    return {k: v for k, v in r.items() if v}


def uscal(a, c):
    return {k: v for k, v in ((k, mp_scal(v, c)) for k, v in a.items()) if v}


def uderiv(a):
    return {k - 1: mp_scal(v, k) for k, v in a.items()
            if k > 0 and mp_scal(v, k)}


# ------------------------------------------------------------------- the system
def build(chart, rabin, zero_ps=False, with_e3=True):
    """chart in 'A','B'; zero_ps=True is the (p_,s_)=(0,0) control branch."""
    res_A, B = CF.build_residuals_Q()
    qu = {1: ONE, 8: ONE}
    for i in range(2, 8):
        qu[i] = V("A%d" % (i - 1))
    tu = {j: from_A(B[j - 2]) for j in TIDX}
    tu = {j: v for j, v in tu.items() if v}

    fu = {i: V("f%d" % i) for i in FIDX}
    gu = {j: V("g%d" % j) for j in GIDX}
    ru = {k: V("r%d" % k) for k in RIDX}

    varnames = ["A%d" % i for i in range(1, 7)]
    varnames += ["f%d" % i for i in FIDX] + ["g%d" % j for j in GIDX]
    varnames += ["r%d" % k for k in RIDX]

    if zero_ps:
        pu, su = {}, {}
    else:
        pu = {i: V("p%d" % i) for i in PIDX}
        su = {}
        for j in SIDX:
            if j == 11:
                su[j] = ONE if chart == 'A' else ZERO
            elif j == 12:
                su[j] = V("s12") if chart == 'A' else ONE
            else:
                su[j] = V("s%d" % j)
        su = {j: v for j, v in su.items() if v}
        varnames += ["p%d" % i for i in PIDX]
        varnames += ["s%d" % j for j in SIDX if j not in (11, 12)]
        if chart == 'A':
            varnames.append("s12")
    if rabin:
        varnames += ["Wf", "Wg"]

    fd, gd, rd = uderiv(fu), uderiv(gu), uderiv(ru)
    qd, td = uderiv(qu), uderiv(tu)
    pd, sd = uderiv(pu), uderiv(su)

    E0 = uadd(umul(fd, ru), uscal(umul(pu, gd), -1))
    E1 = uadd(uscal(umul(fd, su), 2), umul(pd, ru),
              uscal(umul(pu, rd), -1), uscal(umul(qu, gd), -2))
    E2 = uadd(uscal(umul(fd, tu), 3), uscal(umul(pd, su), 2),
              umul(qd, ru), uscal(umul(pu, sd), -1), uscal(umul(qu, rd), -2))
    E3 = uadd(uscal(umul(pd, tu), 3), uscal(umul(qd, su), 2),
              uscal(umul(pu, td), -1), uscal(umul(qu, sd), -2))

    eqs, labels = [], []
    for name, Ex in (("E0", E0), ("E1", E1), ("E2", E2)):
        for k in sorted(Ex):
            eqs.append(Ex[k])
            labels.append("%s:u^%d" % (name, k))
    n012 = len(eqs)
    nE3 = 0
    if with_e3 and not zero_ps:
        for k in sorted(E3):
            eqs.append(E3[k])
            labels.append("E3:u^%d" % k)
            nE3 += 1
    for i, f in enumerate(res_A):
        eqs.append(from_A({m: F(c) for m, c in f.items()}))
        labels.append("FACE:res%d" % i)
    if rabin:
        eqs.append(mp_add(mp_mul(V("f8"), V("Wf")), CONST(-1)))
        labels.append("RAB:f8")
        eqs.append(mp_add(mp_mul(V("g12"), V("Wg")), CONST(-1)))
        labels.append("RAB:g12")
    meta = dict(n_E0=len(E0), n_E1=len(E1), n_E2=len(E2), n_E3=nE3,
                n_face=len(res_A), n_eqs=len(eqs), n_vars=len(varnames),
                labels=labels, n012=n012)
    return eqs, varnames, meta


def verify_zero_point(eqs, labels, assign):
    """substitute a partial assignment (unset names = free) -- returns the
    list of equations that do NOT vanish identically after substitution."""
    bad = []
    for e, lab in zip(eqs, labels):
        acc = {}
        for m, c in e.items():
            val = c
            rest = []
            for n, ex in m:
                if n in assign:
                    val *= F(assign[n]) ** ex
                else:
                    rest.append((n, ex))
            if val:
                mm = tuple(sorted(rest))
                v = acc.get(mm, F(0)) + val
                if v:
                    acc[mm] = v
                else:
                    acc.pop(mm, None)
        if acc:
            bad.append(lab)
    return bad


# ------------------------------------------------------------------- Singular
def sing_terms(f):
    den = 1
    for c in f.values():
        d = c.denominator
        a, b = den, d
        while b:
            a, b = b, a % b
        den = den * d // a
    out = []
    for m, c in f.items():
        v = int(c * den)
        s = ("+" if v > 0 else "-") + str(abs(v))
        for n, e in m:
            s += "*%s^%d" % (n, e)
        out.append(s)
    return out or ["+0"]


def stmts(terms, name, per=8):
    out = ["poly %s = 0;" % name]
    for i in range(0, len(terms), per):
        out.append("%s = %s %s;" % (name, name, "".join(terms[i:i + per])))
    return out


def run(eqs, varnames, tag, timeout=86400, order='dp', engine='modStd',
        char=0):
    """engine='std'    : Singular's deterministic Buchberger/Groebner over Q
       engine='modStd' : modstd.lib, modStd(I, 1) -- modular computation with
                         exactness = 1, which the library documents as
                         computing a standard basis of I *for sure* (the
                         default; exactness = 0 would be the probabilistic
                         variant, and is not used here)."""
    src = []
    if engine == 'modStd':
        src.append('LIB "modstd.lib";')
    src.append("ring R = %d,(%s),%s;" % (char, ",".join(varnames), order))
    en = []
    for i, e in enumerate(eqs):
        src += stmts(sing_terms(e), "q%d" % i)
        en.append("q%d" % i)
    src += ["ideal I = %s;" % ",".join(en),
            "option(redSB);",
            "int t0 = timer;",
            "ideal G = %s;" % ("modStd(I, 1)" if engine == 'modStd'
                               else "std(I)"),]
    src += [
            '"SECS:"; (timer-t0) div 1000;',
            '"SIZE:"; size(G);',
            '"ISUNIT:"; int uu = (size(G)==1 && G[1]==1); uu;',
            '"DIM:"; dim(G);',
            '"GB:";', "int i;",
            "for(i=1;i<=size(G);i++){ if(i<=25){G[i];} }",
            '"END";', "quit;"]
    path = os.path.join(SCRATCH, 'imp_%s.sing' % tag)
    open(path, 'w').write("\n".join(src) + "\n")
    t0 = time.time()
    out = subprocess.run(['Singular', '-q', path], capture_output=True,
                         text=True, timeout=timeout)
    txt = out.stdout
    open(os.path.join(SCRATCH, 'imp_%s.out' % tag), 'w').write(txt)
    lines = [l.strip() for l in txt.splitlines() if l.strip()
             and not l.startswith('// **')]
    assert 'ISUNIT:' in lines, txt[:4000]
    size = int(lines[lines.index('SIZE:') + 1])
    isunit = int(lines[lines.index('ISUNIT:') + 1]) == 1
    dim = int(lines[lines.index('DIM:') + 1])
    gb = lines[lines.index('GB:') + 1:lines.index('END')]
    return isunit, dim, size, gb, time.time() - t0, path


if __name__ == '__main__':
    import argparse, json
    ap = argparse.ArgumentParser()
    ap.add_argument('what')            # C2 C3 Afree Arab Bfree Brab
    ap.add_argument('--timeout', type=int, default=86400)
    ap.add_argument('--order', default='dp')
    ap.add_argument('--engine', default='modStd')
    ap.add_argument('--char', type=int, default=0)
    a = ap.parse_args()
    W = a.what
    if W in ('C2', 'C3'):
        eqs, vn, meta = build('B', W == 'C3', zero_ps=True)
    else:
        eqs, vn, meta = build(W[0], W.endswith('rab'))
    print("%s : %d equations (E0 %d, E1 %d, E2 %d, E3 %d, face %d%s),"
          " %d variables"
          % (W, meta['n_eqs'], meta['n_E0'], meta['n_E1'], meta['n_E2'],
             meta['n_E3'], meta['n_face'],
             ", +2 Rabinowitsch" if W.endswith('rab') or W == 'C3' else "",
             meta['n_vars']), flush=True)
    if W == 'C2':
        assign = {}
        for i in FIDX:
            assign["f%d" % i] = 0
        for j in GIDX:
            assign["g%d" % j] = 0
        for k in RIDX:
            assign["r%d" % k] = 0
        bad = verify_zero_point(eqs, meta['labels'], assign)
        bad = [b for b in bad if not b.startswith('FACE')]
        print("   C2 known point (f, g constant, r = 0): every E0/E1/E2 row"
              " vanishes identically by exact substitution: %s"
              " (non-vanishing rows: %s)" % (not bad, bad or "none"),
              flush=True)
    t0 = time.time()
    eng = a.engine if a.char == 0 else 'std'
    tag = W if a.char == 0 else "%s_p%d" % (W, a.char)
    r = run(eqs, vn, tag, timeout=a.timeout, order=a.order,
            engine=eng, char=a.char)
    print("RESULT %s : unit ideal = %s, dim = %s, |GB| = %s, wall %.1fs"
          % (W, r[0], r[1], r[2], r[4]), flush=True)
    json.dump(dict(what=W, engine=eng, char=a.char, unit_ideal=r[0], dim=r[1], gb_size=r[2],
                   seconds=r[4], n_eqs=meta['n_eqs'], n_vars=meta['n_vars'],
                   gb=r[3] if not r[0] else []),
              open(os.path.join(SCRATCH, 'imp_%s.json' % tag), 'w'), indent=1)
