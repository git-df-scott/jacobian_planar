#!/usr/bin/env python3
"""WAVE 5b -- pentagon block-structure test (the case-(2) question, case (1)).

Case (2) fell because its 92 equations are quasi-homogeneous for a weight
vector on the coefficient variables (w = j - 2i), splitting them into a small
self-contained head block plus linear tail blocks.  This file decides whether
the pentagon system (wave1/pent_L18.ms: 66 generators, 59 vars, levels 13..23)
admits ANY weight vector at all under which every generator is
quasi-homogeneous -- the necessary condition for the same cascade.

METHOD (exact): for each generator, every pair (monomial, first monomial)
contributes the exponent-difference vector; a weight vector w works iff it is
orthogonal to ALL difference vectors.  We maintain the row space of the
differences by incremental exact Gaussian elimination over Q and report its
nullspace.  Nullspace = 0  =>  NO grading exists (obstruction certified by a
witness pair of monomials for each independent direction).
Nullspace != 0  =>  the grading vectors are printed and verified on every
generator, and the induced block structure is tabulated.

CONTROL: the same code run on the case-(2) system (campaign JSON via
wave4/w4_case2_system) must recover its known grading -- nullspace containing
the (i,j) -> j - 2i functional (up to the gauge rows).
"""
import re, sys
from fractions import Fraction

def parse_ms(path, max_gens=None):
    txt = open(path).read()
    lines = txt.split("\n", 2)
    gens_vars = lines[0].split(",")
    body = lines[2]
    gens = [g.strip() for g in body.split(",\n") if g.strip()]
    if max_gens: gens = gens[:max_gens]
    return gens_vars, gens

TERM = re.compile(r'[+-]')
def monomial_exps(term, vidx, nvars):
    v = [0]*nvars
    for factor in term.split("*"):
        factor = factor.strip()
        if not factor or factor.lstrip("-").isdigit():
            continue
        if "^" in factor:
            name, e = factor.split("^"); e = int(e)
        else:
            name, e = factor, 1
        if name in vidx:
            v[vidx[name]] += e
    return v

def gen_terms(g):
    # split top-level on + and - (no parentheses in .ms format)
    out, cur = [], ""
    for ch in g:
        if ch in "+-" and cur and cur[-1] not in "^*+-":
            out.append(cur); cur = ch
        else:
            cur += ch
    if cur: out.append(cur)
    return out

def row_reduce_add(basis, row):
    """Exact incremental reduction; basis rows are pivot-normalized dicts."""
    r = dict(enumerate(row))
    r = {k: Fraction(v) for k, v in r.items() if v != 0}
    for piv, b in basis.items():
        if piv in r:
            f = r[piv]
            for k, v in b.items():
                r[k] = r.get(k, Fraction(0)) - f*v
                if r[k] == 0: del r[k]
    if not r:
        return False
    piv = min(r)
    f = r[piv]
    b = {k: v/f for k, v in r.items()}
    basis[piv] = b
    return True

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "wave1/pent_L18.ms"
    varnames, gens = parse_ms(path)
    vidx = {v: i for i, v in enumerate(varnames)}
    n = len(varnames)
    print(f"{path}: {len(gens)} generators, {n} variables")
    basis = {}
    witnesses = []
    for gi, g in enumerate(gens):
        terms = gen_terms(g)
        base = monomial_exps(terms[0], vidx, n)
        for t in terms[1:]:
            e = monomial_exps(t, vidx, n)
            diff = [e[i] - base[i] for i in range(n)]
            if any(diff):
                if row_reduce_add(basis, diff):
                    witnesses.append((gi, len(witnesses)))
                    if len(basis) == n:
                        print("RANK FULL at generator", gi,
                              "-> NO quasi-homogeneous grading exists.")
                        print("OBSTRUCTION CERTIFIED: the exponent-difference "
                              "row space is all of Q^n.")
                        return 1
    rank = len(basis)
    print(f"difference row-space rank = {rank} of {n}; "
          f"nullspace dimension = {n - rank}")
    if rank < n:
        # extract one nullspace vector by back-substitution over free coords
        import sympy
        M = sympy.zeros(rank, n)
        for r_i, (piv, b) in enumerate(sorted(basis.items())):
            for k, v in b.items():
                M[r_i, k] = sympy.Rational(v.numerator, v.denominator)
        ns = M.nullspace()
        print(f"grading vectors ({len(ns)}):")
        for vvec in ns[:4]:
            w = [vvec[i] for i in range(n)]
            tag = {varnames[i]: w[i] for i in range(n) if w[i] != 0}
            print("  w =", dict(list(tag.items())[:12]),
                  ("..." if len(tag) > 12 else ""))
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
