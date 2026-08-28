"""night6 TASK 3, stage 1 -- the face system over Q (characteristic zero).

Same from-scratch construction as e3_final.py, with exact rational
arithmetic instead of F_p:

    q = u*A (deg A = 7, A_k = q_{k+1}),  t = u^2*B (deg B = 10, B_k = t_{k+2})
    sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m == 0],   m = 0..17
    gauge A_0 = A_7 = 1 (i.e. q_1 = q_8 = 1); the m = 17 row vanishes
    identically; rows m = 0..10 eliminate B_0..B_10; rows m = 11..16 are 6
    residual equations in A_1..A_6 = q_2..q_7.

Emits a Singular char-0 script: std, dim, vdim, lex GB by fglm, and the
factorisation over Q of the univariate eliminant.
"""
import sys, os, subprocess, time
from fractions import Fraction as F

SCRATCH = os.environ.get('N6SCRATCH', '/tmp')
NV = 6


def padd(a, b):
    r = dict(a)
    for m, c in b.items():
        v = r.get(m, F(0)) + c
        if v:
            r[m] = v
        else:
            r.pop(m, None)
    return r


def pmul(a, b):
    r = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(x + y for x, y in zip(m1, m2))
            v = r.get(m, F(0)) + c1 * c2
            if v:
                r[m] = v
            else:
                r.pop(m, None)
    return r


def pscal(a, c):
    if c == 0:
        return {}
    return {m: v * c for m, v in a.items()}


def build_residuals_Q():
    one = {(0,) * NV: F(1)}
    A = {0: one, 7: one}
    for k in range(1, 7):
        e = [0] * NV
        e[k - 1] = 1
        A[k] = {tuple(e): F(1)}
    B = {}
    for m in range(0, 11):
        c0 = F(1 + 2 * m)
        acc = dict(one) if m == 0 else {}
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = F(1 + 2 * j - 3 * i)
            if c:
                acc = padd(acc, pscal(pmul(A[i], B[j]), -c))
        B[m] = pscal(acc, F(1) / c0)
    res = []
    for m in range(11, 18):
        acc = {}
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = F(1 + 2 * j - 3 * i)
                if c:
                    acc = padd(acc, pscal(pmul(A[i], B[j]), c))
        res.append(acc)
    assert res[-1] == {}, "the m = 17 row is not identically zero over Q"
    # clear denominators
    out = []
    for f in res[:-1]:
        den = 1
        for c in f.values():
            den = den * c.denominator // _gcd(den, c.denominator)
        g = {m: int(c * den) for m, c in f.items()}
        num = 0
        for c in g.values():
            num = _gcd(num, abs(c))
        if num > 1:
            g = {m: c // num for m, c in g.items()}
        out.append(g)
    return out, B


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def sing_terms(f):
    """list of signed term strings"""
    ts = []
    for m, c in sorted(f.items()):
        t = ("+" if c > 0 else "-") + str(abs(c))
        for i, e in enumerate(m):
            if e:
                t += "*A%d^%d" % (i + 1, e)
        ts.append(t)
    return ts or ["+0"]


def sing_poly(f):
    return "".join(sing_terms(f))


def sing_poly_stmts(f, name, per=8):
    """emit `poly name = ...;` in short lines (Singular chokes on long ones)"""
    ts = sing_terms(f)
    out = ["poly %s = 0;" % name]
    for i in range(0, len(ts), per):
        out.append("%s = %s %s;" % (name, name, "".join(ts[i:i + per])))
    return out


def main():
    res, B = build_residuals_Q()
    sys.stdout.write("residual equations over Q: %d, total degrees %s,"
                     " term counts %s\n"
                     % (len(res), [max(sum(m) for m in f) for f in res],
                        [len(f) for f in res]))
    src = ["ring R=0,(A1,A2,A3,A4,A5,A6),dp;",
           "ideal I=%s;" % (",\n".join(sing_poly(f) for f in res)),
           "option(redSB);",
           'int t0=timer;',
           "ideal G=std(I);",
           '"STDSEC:"; (timer-t0)/1000;',
           '"DIM:"; dim(G);',
           '"VDIM:"; vdim(G);',
           "ring S=0,(A1,A2,A3,A4,A5,A6),lp;",
           'int t1=timer;',
           "ideal L=fglm(R,G);",
           '"FGLMSEC:"; (timer-t1)/1000;',
           '"LEXGB:";', "int i;",
           "for(i=1;i<=size(L);i++){ L[i]; }",
           '"ELIMFACTORS:";',
           "list fl = factorize(L[1]);",
           "for(i=1;i<=size(fl[1]);i++){ \"FACTOR\"; fl[1][i]; \"MULT\";"
           " fl[2][i]; }",
           '"END";', "quit;"]
    path = os.path.join(SCRATCH, 'char0_face.sing')
    open(path, 'w').write("\n".join(src) + "\n")
    sys.stdout.write("running Singular (char 0) on %s\n" % path)
    sys.stdout.flush()
    t0 = time.time()
    r = subprocess.run(['Singular', '-q', path], capture_output=True,
                       text=True, timeout=100000)
    open(os.path.join(SCRATCH, 'char0_face.out'), 'w').write(r.stdout)
    sys.stdout.write("wall %.1fs\n" % (time.time() - t0))
    sys.stdout.write(r.stdout[:20000])
    sys.stdout.flush()


if __name__ == '__main__':
    main()
