"""night20 -- second sweep: supports WITHOUT the MV = 0 requirement, so the
coefficient-degenerate critical-point-free polynomials are reached too.

A polynomial has NO critical point in C^2 as soon as Res_y(P_x, P_y) is a
non-zero constant (any common zero (x0,y0) forces the resultant to vanish at
x0).  That is the arbiter used here, after two free filters:
 * conv(supp P u {0}) must have an interior lattice point (Baker: else genus 0);
 * no critical point on x = 0 and none on y = 0 (a one-variable gcd).
Everything that survives is re-decided by Singular in pipe20.py.
"""
import sys, os, json, itertools, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen20 as G


# ----------------------------------------------- fast univariate arithmetic
def pgcd(a, b):
    """a, b : lists of Fraction, low degree first.  Return gcd (monic) or []"""
    a = trim(a); b = trim(b)
    while b:
        a, b = b, trim(prem(a, b))
    if not a:
        return []
    lc = a[-1]
    return [t / lc for t in a]


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def prem(a, b):
    a = a[:]
    db = len(b) - 1
    while len(a) - 1 >= db and a:
        d = len(a) - 1 - db
        f = a[-1] / b[-1]
        for i in range(len(b)):
            a[i + d] -= f * b[i]
        trim(a)
    return a


def axis_free(S, cf):
    """no critical point on x = 0 and none on y = 0."""
    Px = [(i - 1, j, F(a) * i) for a, (i, j) in zip(cf, S) if i >= 1]
    Py = [(i, j - 1, F(a) * j) for a, (i, j) in zip(cf, S) if j >= 1]
    if not Px or not Py:
        return False
    for (fix, keep) in ((0, 1), (1, 0)):
        A, B = {}, {}
        for (i, j, v) in Px:
            if (i, j)[fix] == 0:
                A[(i, j)[keep]] = A.get((i, j)[keep], F(0)) + v
        for (i, j, v) in Py:
            if (i, j)[fix] == 0:
                B[(i, j)[keep]] = B.get((i, j)[keep], F(0)) + v
        la = [F(0)] * (max(A) + 1) if A else []
        for k, v in A.items():
            la[k] = v
        lb = [F(0)] * (max(B) + 1) if B else []
        for k, v in B.items():
            lb[k] = v
        la, lb = trim(la), trim(lb)
        if not la and not lb:
            return False
        g = pgcd(la, lb) if (la and lb) else (la or lb)
        if len(g) - 1 >= 1:
            return False
    return True


def main(jobs, coefs, out="search2_raw.json", tlim=9000):
    """Stage 1 (pure python, fast): free filters + the axis test.
    Stage 2: the survivors are batched into Singular, 250 at a time, and the
    Groebner verdict "1 in (P_x, P_y)" is read off for each."""
    t0 = time.time()
    import sympy as sp
    import inst20 as I
    x, y = sp.symbols('x y')
    cands = []
    seen = set()
    for (D, size) in jobs:
        mons = [(i, j) for d in range(D + 1) for i in range(d + 1) for j in [d - i]]
        nsup = ntry = 0
        for S in itertools.combinations(mons, size):
            if all(m[0] > 0 for m in S) or all(m[1] > 0 for m in S):
                continue
            if max(i + j for (i, j) in S) < 3:
                continue
            if G.interior(S) < 1:
                continue
            nsup += 1
            for cf in itertools.product(coefs, repeat=size):
                if cf[-1] < 0:
                    continue
                ntry += 1
                if not axis_free(S, cf):
                    continue
                if not G.torus_may_be_empty(S, cf):
                    continue
                key = tuple(sorted((m, a) for a, m in zip(cf, S)))
                if key in seen:
                    continue
                seen.add(key)
                cands.append((S, cf))
            if time.time() - t0 > tlim:
                break
        print("D=%d size=%d : %d supports, %d coefficient vectors, "
              "%d axis-free candidates so far, %.0fs"
              % (D, size, nsup, ntry, len(cands), time.time() - t0), flush=True)
    print("axis-free candidates: %d" % len(cands), flush=True)
    res = []
    B = 250
    for b in range(0, len(cands), B):
        chunk = cands[b:b + B]
        lines = ["ring r=0,(x,y),dp;"]
        for n, (S, cf) in enumerate(chunk):
            Ps = "+".join("(%s)*x^%d*y^%d" % (a, i, j) for a, (i, j) in zip(cf, S))
            lines.append("poly P%d=%s;" % (n, Ps))
            lines.append("ideal I%d=diff(P%d,x),diff(P%d,y);" % (n, n, n))
            lines.append('"R%d:",reduce(poly(1),std(I%d));' % (n, n))
        try:
            outp = I.singular("\n".join(lines), timeout=1800)
        except Exception as e:
            print("  batch failed: %s" % e, flush=True)
            continue
        for n, (S, cf) in enumerate(chunk):
            v = I.parse_marked(outp, "R%d" % n)
            if v is not None and v.strip() == "0":
                P = sp.expand(sum(a * x**i * y**j for a, (i, j) in zip(cf, S)))
                res.append({"support": [list(m) for m in S],
                            "coeffs": [str(t) for t in cf],
                            "P": sp.sstr(P), "deg": max(i + j for (i, j) in S),
                            "baker": G.interior(S)})
        print("  batch %d..%d -> %d unimodular so far (%.0fs)"
              % (b, b + len(chunk), len(res), time.time() - t0), flush=True)
        json.dump(res, open(os.path.join(HERE, out), "w"), indent=1)
    json.dump(res, open(os.path.join(HERE, out), "w"), indent=1)
    print("UNIMODULAR FOUND: %d" % len(res), flush=True)


if __name__ == "__main__":
    main([(10, 2), (10, 3), (8, 4), (6, 5)], [1, -1, 2, -2, 3, -3])
