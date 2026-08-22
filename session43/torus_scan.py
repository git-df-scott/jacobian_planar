#!/usr/bin/env python3
import glob, os, re, sys, json
from fractions import Fraction
import numpy as np
import sympy as sp

BASE = "/tmp/claude-0/-home-user-jacobian-planar/211fa372-1945-5d1c-89a5-22497f8a4ea2/scratchpad"

def parse_ms(path):
    with open(path) as f:
        txt = f.read()
    lines = txt.splitlines()
    vars_ = [v.strip() for v in lines[0].split(",") if v.strip()]
    prime = int(lines[1].strip())
    tail = "".join(l.strip() for l in lines[2:])
    polys = [p for p in tail.split(",") if p.strip()]
    return vars_, prime, polys

term_re = re.compile(r'[+-]')

def poly_exponents(poly, varidx):
    # split into terms on + and - (no parentheses expected)
    if '(' in poly:
        raise ValueError("parens present")
    s = poly.replace('-', '+')
    terms = [t for t in s.split('+') if t.strip()]
    exps = []
    for t in terms:
        e = [0]*len(varidx)
        for fac in t.split('*'):
            fac = fac.strip()
            if not fac: continue
            if '^' in fac:
                v, p = fac.split('^')
                e[varidx[v.strip()]] += int(p)
            elif fac.isdigit():
                pass
            else:
                e[varidx[fac]] += 1
        exps.append(tuple(e))
    return exps

def analyze(path):
    vars_, prime, polys = parse_ms(path)
    varidx = {v:i for i,v in enumerate(vars_)}
    n = len(vars_)
    rows = []
    perpoly_exps = []
    for p in polys:
        exps = poly_exponents(p, varidx)
        perpoly_exps.append(exps)
        e0 = exps[0]
        for e in exps[1:]:
            rows.append([a-b for a,b in zip(e, e0)])
    if not rows:
        return dict(file=path, nvars=n, npolys=len(polys), rank=n, basis=[sp.eye(n).col(i).T.tolist()[0] for i in range(n)], vars=vars_, prime=prime, polys=polys, perpoly=perpoly_exps)
    A = np.array(rows, dtype=np.int64)
    # exact nullspace via Gram matrix (over Q: null(A) == null(A^T A))
    G = sp.Matrix((A.T @ A).tolist())
    ns = G.nullspace()
    basis = []
    for v in ns:
        dens = [Fraction(sp.Rational(x).p, sp.Rational(x).q).denominator for x in v]
        L = 1
        for d in dens:
            L = L*d//__import__('math').gcd(L, d)
        iv = [int(sp.Rational(x)*L) for x in v]
        g = 0
        for x in iv: g = __import__('math').gcd(g, x)
        if g > 1: iv = [x//g for x in iv]
        basis.append(iv)
    return dict(file=path, nvars=n, npolys=len(polys), rank=len(basis), basis=basis, vars=vars_, prime=prime, polys=polys, perpoly=perpoly_exps)

def slice_system(res, outdir):
    """Set one variable to 1 per torus dimension. Choose vars greedily so the
    chosen weight-columns are independent."""
    vars_, polys, prime = res['vars'], res['polys'], res['prime']
    B = sp.Matrix(res['basis'])  # rank x n
    chosen = []
    M = sp.zeros(B.rows, 0)
    for j in range(B.cols):
        col = B[:, j]
        if col.is_zero_matrix: continue
        Mt = M.row_join(col)
        if Mt.rank() > M.rank():
            M = Mt; chosen.append(j)
        if len(chosen) == B.rows: break
    setvars = [vars_[j] for j in chosen]
    keep = [v for v in vars_ if v not in setvars]
    newpolys = []
    for p in polys:
        q = p
        for v in setvars:
            # replace var tokens with 1: var alone or var^k
            q = re.sub(r'\b%s\^\d+\b' % re.escape(v), '1', q)
            q = re.sub(r'\b%s\b' % re.escape(v), '1', q)
        newpolys.append(q)
    name = os.path.basename(res['file']).replace('.ms', '_torus_sliced.ms')
    out = os.path.join(outdir, name)
    with open(out, 'w') as f:
        f.write(",".join(keep) + "\n")
        f.write(str(prime) + "\n")
        f.write(",\n".join(newpolys) + "\n")
    return setvars, keep, out

def main():
    files = sorted(glob.glob(os.path.join(BASE, "state/wave6/ms/*.ms")) +
                   glob.glob(os.path.join(BASE, "state/wave5/ms2/*.ms")))
    results = []
    md = open(os.path.join(BASE, "torus_results.md"), "w")
    md.write("# Torus grading diagnostic (nullspace of monomial-difference matrix)\n\n")
    md.flush()
    for f in files:
        try:
            r = analyze(f)
        except Exception as ex:
            md.write(f"- PARSE-FAIL {os.path.relpath(f, BASE)}: {ex}\n"); md.flush()
            continue
        line = f"- {os.path.relpath(f, BASE)}: nvars={r['nvars']} npolys={r['npolys']} torus_rank={r['rank']}"
        if r['rank'] >= 1:
            line += f" WEIGHTS={r['basis']}"
            sv, keep, out = slice_system(r, BASE)
            line += f" | SLICED: set {sv}=1, vars {r['nvars']}->{len(keep)} -> {os.path.basename(out)}"
        md.write(line + "\n"); md.flush()
        print(line[:200], flush=True)
        results.append(r)
    # final table sorted by rank desc
    md.write("\n## Final table (sorted by torus rank)\n\n")
    md.write("| file | #vars | #polys | torus rank | weight vector(s) |\n|---|---|---|---|---|\n")
    for r in sorted(results, key=lambda x: -x['rank']):
        w = "; ".join("("+",".join(map(str,b))+")" for b in r['basis']) if r['rank'] else "-"
        md.write(f"| {os.path.relpath(r['file'], BASE)} | {r['nvars']} | {r['npolys']} | {r['rank']} | {w} |\n")
    md.close()

if __name__ == "__main__":
    main()
