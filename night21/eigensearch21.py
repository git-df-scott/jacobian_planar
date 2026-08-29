#!/usr/bin/env python3
"""Exact sparse search for [P,A]=P.

For fixed A the equation is linear in P.  If P=0 is irreducible, the pole
theorem turns A/P into a polynomial mate.  This is therefore a direct CE
construction search, not a bounded mate search.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from pole21 import clean, add, scale, mul, dx, dy, D, ONE  # noqa: E402


def carrier(d, nonconstant=False):
    return [(i, n-i) for n in range(1 if nonconstant else 0, d+1)
            for i in range(n+1)]


def rref_nullspace(rows, ncols):
    rows = [dict(r) for r in rows if r]
    pivots = []
    rr = 0
    for c in range(ncols):
        k = next((k for k in range(rr, len(rows)) if rows[k].get(c)), None)
        if k is None:
            continue
        rows[rr], rows[k] = rows[k], rows[rr]
        a = rows[rr][c]
        rows[rr] = {j: v/a for j, v in rows[rr].items()}
        for k in range(len(rows)):
            if k == rr or not rows[k].get(c):
                continue
            a = rows[k][c]
            nr = dict(rows[k])
            for j, v in rows[rr].items():
                z = nr.get(j, F(0))-a*v
                if z:
                    nr[j] = z
                elif j in nr:
                    del nr[j]
            rows[k] = nr
        pivots.append(c)
        rr += 1
        if rr == len(rows):
            break
    free = [c for c in range(ncols) if c not in set(pivots)]
    basis = []
    for f in free:
        v = [F(0)]*ncols
        v[f] = F(1)
        for r, c in enumerate(pivots):
            v[c] = -rows[r].get(f, F(0))
        basis.append(v)
    return basis


def eigenbasis(A, dP):
    S = carrier(dP)
    cols = []
    allrows = set()
    for m in S:
        col = add(D({m: F(1)}, A), {(m[0], m[1]): F(-1)})
        cols.append(col)
        allrows.update(col)
    R = sorted(allrows)
    ri = {m: i for i, m in enumerate(R)}
    rows = [dict() for _ in R]
    for j, col in enumerate(cols):
        for m, a in col.items():
            rows[ri[m]][j] = a
    vecs = rref_nullspace(rows, len(S))
    return [clean({S[i]: a for i, a in enumerate(v) if a}) for v in vecs]


def solve_linear(rows, rhs, ncols):
    rows = [dict(r) for r in rows]
    rhs = [F(v) for v in rhs]
    piv = []
    rr = 0
    for c in range(ncols):
        k = next((k for k in range(rr, len(rows)) if rows[k].get(c)), None)
        if k is None:
            continue
        rows[rr], rows[k] = rows[k], rows[rr]
        rhs[rr], rhs[k] = rhs[k], rhs[rr]
        a = rows[rr][c]
        rows[rr] = {j: v/a for j, v in rows[rr].items()}
        rhs[rr] /= a
        for k in range(len(rows)):
            if k == rr or not rows[k].get(c):
                continue
            a = rows[k][c]
            nr = dict(rows[k])
            for j, v in rows[rr].items():
                z = nr.get(j, F(0))-a*v
                if z:
                    nr[j] = z
                elif j in nr:
                    del nr[j]
            rows[k] = nr
            rhs[k] -= a*rhs[rr]
        piv.append(c)
        rr += 1
        if rr == len(rows):
            break
    if any(not row and b for row, b in zip(rows, rhs)):
        return None
    out = [F(0)]*ncols
    for r, c in enumerate(piv):
        out[c] = rhs[r]
    return out


def bezout(P, maxdeg=8):
    Px, Py = dx(P), dy(P)
    for d in range(maxdeg+1):
        S = carrier(d)
        cols = [mul(Px, {m: F(1)}) for m in S]
        cols += [mul(Py, {m: F(1)}) for m in S]
        R = sorted(set().union(*[set(c) for c in cols]) | {(0, 0)})
        ri = {m: i for i, m in enumerate(R)}
        rows = [dict() for _ in R]
        for j, col in enumerate(cols):
            for m, a in col.items():
                rows[ri[m]][j] = a
        rhs = [F(1) if m == (0, 0) else F(0) for m in R]
        sol = solve_linear(rows, rhs, len(cols))
        if sol is not None:
            U = clean({S[i]: sol[i] for i in range(len(S)) if sol[i]})
            V = clean({S[i]: sol[len(S)+i] for i in range(len(S)) if sol[len(S)+i]})
            resid = add(mul(U, Px), mul(V, Py), scale(-1, ONE))
            assert not resid
            return U, V, d
    return None


def pstr(P):
    if not P:
        return "0"
    ts = []
    for (i, j), a in sorted(P.items()):
        c = str(a.numerator) if a.denominator == 1 else "(%d/%d)" % (a.numerator, a.denominator)
        ts.append("(%s)*x^%d*y^%d" % (c, i, j))
    return "+".join(ts)


def singular_zero_fibre(P):
    sc = ('LIB "absfact.lib"; ring r=0,(x,y),dp; poly f=%s; '
          'ideal I=diff(f,x),diff(f,y); ideal G=std(I); '
          '"RED:",reduce(poly(1),G); def L=absFactorize(f); setring L; '
          '"NF:",absolute_factors[4]; quit;\n' % pstr(P))
    try:
        z = subprocess.run(["Singular", "-q"], input=sc, text=True,
                           capture_output=True, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    out = z.stdout+z.stderr
    def mark(k):
        for line in out.splitlines():
            if line.startswith(k+":"):
                return line[len(k)+1:].strip()
    return {"reduce_1": mark("RED"), "absolute_factors": mark("NF"),
            "raw_tail": out[-300:]}


def candidates_from_basis(B):
    if not B:
        return []
    out = list(B)
    if len(B) <= 5:
        for co in product((F(1), F(-1), F(2)), repeat=len(B)):
            P = {}
            for a, b in zip(co, B):
                P = add(P, scale(a, b))
            out.append(P)
    seen, ans = set(), []
    for P in out:
        key = tuple(sorted(P.items()))
        if key not in seen:
            seen.add(key)
            ans.append(P)
    return ans


def main():
    rng = random.Random(210829)
    mons = carrier(5, nonconstant=True)
    As = []
    coefs = (F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2))
    # Exhaustive two-term A, normalized at the first term.
    for S in combinations(mons, 2):
        for c in coefs:
            As.append({S[0]: F(1), S[1]: c})
    # Structured/random 3- and 4-term A.
    for _ in range(5000):
        k = rng.choice((3, 3, 4))
        S = rng.sample(mons, k)
        As.append(clean({m: (F(1) if i == 0 else rng.choice(coefs))
                         for i, m in enumerate(S)}))
    seenA, results = set(), []
    neigen = nunimod = nirred = nfactor = nunavailable = 0
    for idx, A in enumerate(As, 1):
        ka = tuple(sorted(A.items()))
        if ka in seenA:
            continue
        seenA.add(ka)
        B = eigenbasis(A, 8)
        if not B:
            continue
        neigen += 1
        for P in candidates_from_basis(B):
            if not ((1, 0) in P or (0, 1) in P):
                continue
            bz = bezout(P, maxdeg=8)
            if bz is None:
                continue
            nunimod += 1
            assert D(P, A) == P
            sf = singular_zero_fibre(P)
            if sf is None:
                nunavailable += 1
            else:
                nfactor += 1
            rec = {"P": pstr(P), "A": pstr(A), "deg_P": max(sum(m) for m in P),
                   "deg_A": max(sum(m) for m in A), "bezout_degree": bz[2],
                   "zero_fibre_check": sf}
            if sf and sf.get("absolute_factors") == "1":
                nirred += 1
                rec["DIRECT_CE_CANDIDATE"] = True
                print("DIRECT CANDIDATE", rec, flush=True)
            results.append(rec)
        if idx % 1000 == 0:
            print("%d A; eigen=%d unimod=%d irreducible-zero=%d" %
                  (idx, neigen, nunimod, nirred), flush=True)
    out = {"A_tested": len(seenA), "A_with_eigenvectors": neigen,
           "unimodular_eigenpolynomials": nunimod,
           "zero_fibre_checks_available": nfactor,
           "zero_fibre_check_unavailable": nunavailable,
           "irreducible_zero_fibre_certified": nirred, "rows": results}
    with open(os.path.join(HERE, "eigensearch21.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("FINAL", {k: v for k, v in out.items() if k != "rows"})


if __name__ == "__main__":
    main()
