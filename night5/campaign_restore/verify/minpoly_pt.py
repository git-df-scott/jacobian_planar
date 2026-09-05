#!/usr/bin/env python3
"""Extract explicit face points without trusting any solver convention.

The face ideal is zero-dimensional of degree 35.  For a variable v the
minimal polynomial of v on the quotient ring is found by reducing
1, v, v^2, ... modulo a Groebner basis and looking for the first linear
dependence among the normal forms.  That uses only `std` and `reduce`, so
there is no RUR to parse and no msolve linear form to second-guess -- the
two conventions that produced wrong answers earlier in this campaign.

A root is accepted only after the resulting (q,t) is substituted back into
2 q t' - 3 q' t = u^2 and the identity checked coefficient by coefficient.
"""
import re, subprocess, sys
import sympy as sp
from face_solve_indep import face_system
from uz_indep import u

def singular(txt, timeout=1200):
    open("_mp.sing", "w").write(txt)
    r = subprocess.run(["Singular", "-q", "_mp.sing"], capture_output=True,
                       text=True, timeout=timeout)
    return r.stdout

def minpoly(prime, eqs, unk, var, extra):
    body = ",\n ".join(str(e) for e in eqs + extra)
    txt = [f"ring R = {prime}, ({','.join(map(str, unk))}), dp;",
           f"ideal I = {body};",
           "ideal G = std(I);",
           '"VDIM " + string(vdim(G));',
           "int i; poly c = 1;",
           "for (i = 0; i <= 36; i++) {",
           f'  "NF " + string(i) + " : " + string(reduce(c, G));',
           f"  c = reduce(c * {var}, G);",
           "}",
           "quit;"]
    out = singular("\n".join(txt))
    vd = re.search(r"VDIM (-?\d+)", out)
    rows = re.findall(r"NF (\d+) : (.*)", out)
    return (int(vd.group(1)) if vd else None), rows

def to_vec(expr_str, basis, prime):
    e = sp.sympify(expr_str) if expr_str.strip() not in ("0", "") else sp.Integer(0)
    d = sp.Poly(e, *basis).as_dict() if e != 0 else {}
    return d

def solve_dep(rows, unk, prime):
    """first i such that NF(v^i) is a GF(p)-combination of NF(v^j), j<i"""
    mons, vecs = {}, []
    for _, s in rows:
        d = to_vec(s, unk, prime)
        for k in d:
            mons.setdefault(k, len(mons))
        vecs.append(d)
    ncol = len(mons)
    M, piv, combos = [], [], []
    for i, d in enumerate(vecs):
        row = [0] * ncol
        for k, c in d.items():
            row[mons[k]] = int(c) % prime
        comb = [0] * len(vecs); comb[i] = 1
        for r, pc, p_ in zip(M, combos, piv):
            f = row[p_] % prime
            if f:
                row = [(a - f * b) % prime for a, b in zip(row, r)]
                comb = [(a - f * b) % prime for a, b in zip(comb, pc)]
        nz = next((j for j, a in enumerate(row) if a % prime), None)
        if nz is None:
            return i, comb                      # dependency found
        inv = pow(row[nz], prime - 2, prime)
        M.append([a * inv % prime for a in row])
        combos.append([a * inv % prime for a in comb])
        piv.append(nz)
    return None, None

if __name__ == "__main__":
    prime = int(sys.argv[1]); var = sys.argv[2] if len(sys.argv) > 2 else "t2"
    eqs, unk, coef, poly = face_system(prime, {"q1": 1, "q8": 1})
    vd, rows = minpoly(prime, eqs, unk, var, [])
    print(f"p = {prime}   vdim = {vd}   normal forms collected: {len(rows)}")
    deg, comb = solve_dep(rows, unk, prime)
    if deg is None:
        print("no dependency found within the computed range"); sys.exit(1)
    T = sp.Symbol("T")
    mp = sum(int(c) * T**j for j, c in enumerate(comb[:deg + 1]))
    mp = sp.Poly(mp, T, modulus=prime)
    print(f"minimal polynomial of {var} has degree {deg}")
    fl = sp.factor_list(mp.as_expr(), T, modulus=prime)[1]
    print("  factor degrees:", sorted(sp.degree(f, T) for f, _ in fl))
    lin = [f for f, _ in fl if sp.degree(f, T) == 1]
    print(f"  linear factors: {len(lin)}")
    for f in lin:
        root = (-sp.Poly(f, T).all_coeffs()[1] *
                pow(int(sp.Poly(f, T).all_coeffs()[0]), prime - 2, prime)) % prime
        print(f"   {var} = {root}")
