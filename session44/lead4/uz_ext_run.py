#!/usr/bin/env python3
"""Run the cascade over every irreducible factor of the q-layer eliminating
polynomial, covering ALL solutions of the q-layer with gauge q8 = 1."""
import ast
import os
import subprocess
import sys

from uz_eliminate import run
from uz_system import PVARS
from uz_ext import (Field, nullspace_F, solve_affine_F, partial_F, PV, FV)

HERE = os.path.dirname(os.path.abspath(__file__))


def singular(script, tag):
    path = os.path.join(HERE, f"{tag}.sing")
    open(path, "w").write(script)
    r = subprocess.run(["Singular", "-q", path], capture_output=True,
                       text=True, timeout=7200)
    return r.stdout.strip(), r.stderr.strip()


def factor_univariate(coeffs, p, tag):
    """factor a univariate polynomial over GF(p) using Singular"""
    terms = "+".join(f"{c}*T^{i}" for i, c in enumerate(coeffs) if c % p)
    sc = [f"ring R = {p}, T, dp;", f"poly f = {terms};",
          "list L = factorize(f);",
          'for (int i=1; i<=size(L[1]); i++) { "FACTOR " + string(L[2][i]) '
          '+ " : " + string(L[1][i]); }', "exit;"]
    out, err = singular("\n".join(sc), tag)
    facs = []
    for line in out.splitlines():
        if line.startswith("FACTOR"):
            mult, poly = line[len("FACTOR "):].split(" : ", 1)
            facs.append((int(mult), poly.strip()))
    return facs


def poly_from_string(s, p):
    """parse a Singular univariate polynomial in T into a coefficient list"""
    s = s.replace("-", "+-").replace(" ", "")
    co = {}
    for t in s.split("+"):
        if not t:
            continue
        neg = t.startswith("-")
        if neg:
            t = t[1:]
        if "T" in t:
            parts = t.split("T")
            c = int(parts[0].rstrip("*")) if parts[0].rstrip("*") else 1
            e = int(parts[1].lstrip("^")) if parts[1] else 1
        else:
            c, e = int(t), 0
        if neg:
            c = -c
        co[e] = (co.get(e, 0) + c) % p
    d = max(co)
    return [co.get(i, 0) % p for i in range(d + 1)]


def main(path):
    txt = open(path).read().strip().rstrip(":").replace("\n", "")
    D = ast.literal_eval(txt)
    p, nv, deg, varn, lf, rest = D[1]
    elim, den, plist = rest[1]
    w = elim[1]
    facs = factor_univariate(w, p, "elimfac")
    print(f"eliminating polynomial of degree {len(w)-1} over GF({p}) factors "
          f"as {[(m, len(poly_from_string(f,p))-1) for m, f in facs]}"
          f"  (multiplicity, degree)")
    obs, _ = run(mod=p, fixed={}, verbose=False)
    obs = dict(obs)
    E4 = [obs[(n, 4)] for n in range(13, 19)]
    E3 = [obs[(n, 3)] for n in range(13, 20)]
    E2 = [obs[(n, 2)] for n in range(13, 20)]
    E1 = [obs[(n, 1)] for n in range(13, 20)]
    E0 = [obs[(n, 0)] for n in range(2, 20)]
    total = 0
    for fi, (mult, fs) in enumerate(facs):
        h = poly_from_string(fs, p)
        if h[-1] != 1:
            iv = pow(h[-1], p - 2, p)
            h = [c * iv % p for c in h]
        d = len(h) - 1
        K = Field(p, h)
        T = K.gen() if d > 1 else K.const((-h[0]) % p)
        total += d

        def ev(co):
            r = K.zero()
            for c in reversed(co):
                r = K.add(K.mul(r, T), K.const(c))
            return r
        dv = ev(den[1])
        if K.iszero(dv):
            print(f"  factor {fi} (deg {d}): denominator vanishes, skipped")
            continue
        iv = K.inv(dv)
        val = {v: K.zero() for v in PVARS}
        val[varn[-1]] = T
        for name, entry in zip(varn[:len(plist)], plist):
            dd, co = entry[0]
            val[name] = K.sub(K.zero(), K.mul(ev(co), iv))
        ok = all(not partial_F(K, e, val, []) for e in E4)
        print(f"  factor {fi}: deg {d}, mult {mult}, q verifies: {ok}")
        if not ok:
            print("     *** q does not satisfy the q-layer -- parse error")
            continue
        # p layer
        A = []
        for e in E3:
            dd = partial_F(K, e, val, PV)
            row = [K.zero()] * 8
            for mono, c in dd.items():
                row[list(mono).index(1)] = c
            A.append(row)
        ker = nullspace_F(K, A)
        nk = len(ker)
        # f layer
        Mrows, Qrows = [], []
        for e in E2:
            dd = partial_F(K, e, val, FV + PV)
            row = [K.zero()] * 8
            quad = {}
            for mono, c in dd.items():
                fp, pp = mono[:8], mono[8:]
                if sum(fp) == 1 and sum(pp) == 0:
                    row[list(fp).index(1)] = c
                elif sum(fp) == 0 and sum(pp) == 2:
                    quad[pp] = c
                else:
                    raise RuntimeError("unexpected monomial")
            Mrows.append(row)
            Qrows.append(quad)
        parts = {}
        bad = False
        for i in range(nk):
            for j in range(i, nk):
                vec = []
                for quad in Qrows:
                    tot = K.zero()
                    for pp, c in quad.items():
                        idx = [a for a in range(8) for _ in range(pp[a])]
                        a, b = idx
                        if i == j:
                            tot = K.add(tot, K.mul(c, K.mul(ker[i][a],
                                                            ker[i][b])))
                        else:
                            tot = K.add(tot, K.mul(c, K.add(
                                K.mul(ker[i][a], ker[j][b]),
                                K.mul(ker[j][a], ker[i][b]))))
                    vec.append(K.sub(K.zero(), tot))
                r = solve_affine_F(K, Mrows, vec)
                if r is None:
                    bad = True
                parts[(i, j)] = r
        kerM = nullspace_F(K, Mrows)
        nf = len(kerM)
        print(f"     p-kernel dim {nk}, ker(M) dim {nf}, "
              f"f-layer solvable {not bad}")
        if bad:
            print("     -> no solution for this q at all")
            continue
        # ---- build the (n,1),(n,0) equations in nk+nf parameters, over K
        NV = nk + nf
        names = ["lam", "mu", "nu1", "nu2", "nu3", "nu4"][:NV]

        def tmul(A1, B1):
            C = {}
            for m1, c1 in A1.items():
                for m2, c2 in B1.items():
                    m = tuple(a + b for a, b in zip(m1, m2))
                    C[m] = K.add(C.get(m, K.zero()), K.mul(c1, c2))
            return {m: c for m, c in C.items() if not K.iszero(c)}

        def tadd(A1, B1):
            C = dict(A1)
            for m, c in B1.items():
                C[m] = K.add(C.get(m, K.zero()), c)
            return {m: c for m, c in C.items() if not K.iszero(c)}

        def gen(i):
            e = [0] * NV
            e[i] = 1
            return {tuple(e): K.one()}
        X = [gen(i) for i in range(nk)]
        NUS = [gen(nk + i) for i in range(nf)]
        pexpr = []
        for a in range(8):
            e = {}
            for i in range(nk):
                e = tadd(e, {m: K.mul(c, ker[i][a]) for m, c in X[i].items()})
            pexpr.append(e)
        fexpr = []
        for a in range(8):
            e = {}
            for i in range(nf):
                e = tadd(e, {m: K.mul(c, kerM[i][a])
                             for m, c in NUS[i].items()})
            for (i, j), vec in parts.items():
                term = tmul(X[i], X[j])
                e = tadd(e, {m: K.mul(c, vec[a]) for m, c in term.items()})
            fexpr.append(e)

        def subst(poly):
            out = {}
            for m, c in poly.items():
                term = {(0,) * NV: K.const(c)}
                for i, e in enumerate(m):
                    if not e:
                        continue
                    nm = PVARS[i]
                    if nm[0] == "q":
                        vv = val[nm]
                        for _ in range(e):
                            term = {mm: K.mul(cc, vv)
                                    for mm, cc in term.items()}
                    elif nm[0] == "p":
                        for _ in range(e):
                            term = tmul(term, pexpr[int(nm[1:]) - 1])
                    else:
                        for _ in range(e):
                            term = tmul(term, fexpr[int(nm[1:]) - 1])
                out = tadd(out, term)
            return out

        def tostr(P):
            if not P:
                return "0"
            out = []
            for m, c in sorted(P.items()):
                cs = "+".join((f"{v}*a^{i}" if i else str(v))
                              for i, v in enumerate(c.c) if v)
                f = ["(" + cs + ")"]
                for i, e in enumerate(m):
                    if e:
                        f.append(names[i] + (f"^{e}" if e > 1 else ""))
                out.append("*".join(f))
            return "+".join(out)
        eqs = [tostr(subst(e)) for e in E1 + E0]
        eqs = [e for e in eqs if e != "0"]
        fs = [tostr(fexpr[a]) for a in range(8)]
        ps = [tostr(pexpr[a]) for a in range(8)]
        minp = "+".join(f"{c}*a^{i}" for i, c in enumerate(h) if c)
        L = [f"ring R = ({p},a), ({','.join(names)},W), dp;",
             f"minpoly = {minp};",
             "ideal I = " + ",".join(eqs) + ";",
             '"     base system dim (in the (par,W) ring) = " + '
             "string(dim(std(I)));"]
        for a in range(8):
            for nm, ex in (("f", fs[a]), ("p", ps[a])):
                if ex == "0":
                    L.append(f'"     {nm}{a+1}: identically 0";')
                    continue
                L.append(f"ideal J = I, ({ex})*W-1; ideal G = std(J);")
                L.append(f'"     {nm}{a+1} can be nonzero: " + '
                         "string(!(size(G)==1 and G[1]==1));")
        L.append("exit;")
        out, err = singular("\n".join(L), f"ext_{p}_{fi}")
        print(out)
        if err:
            print("     STDERR:", err[:300])
    print(f"total degree covered: {total} (should be 35)")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(a)
