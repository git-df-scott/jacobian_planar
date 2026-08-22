#!/usr/bin/env python3
"""Edge cascade, rungs 15..12, with r gauged to 1.

The y-scaling y -> lambda*y preserves every monomial support (it is a torus
action on the Newton polygon) and is NOT used by pentev's gauges (p_0_0 = 0,
p_0_1 = 1 involve x only).  So r may be set to 1 with no loss.  alpha, beta stay
symbolic.  Conditions found here are then re-verified with r symbolic by a
single rank check rather than by enumerating minors.
"""
import sympy as sp
from itertools import combinations
y = sp.symbols('y'); M, N = 8, 12
al, be = sp.symbols('alpha beta', nonzero=True)
r = sp.Integer(1)
NZ = {al, be}

def rung_edge(d, A, B):
    s = 0
    for i in range(1, M+1):
        k = d+1-i
        if 2 <= k <= N and i in A and k in B:
            s += (2*k-3*i)*A[i]*B[k] + y*(i*A[i]*sp.diff(B[k],y) - k*sp.diff(A[i],y)*B[k])
    return sp.expand(s)

def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    return sum(c[i]*y**i for i in range(deg+1)), c

A = {8: al*(y-r)**2}; B = {12: be*(y-r)**3}
Ac = {}
C7, cC7 = gen('c7_', 2)
A[7] = sp.expand((y-r)*C7); Ac[7] = cC7           # rung 17 already imposed
for i in range(1, 7):
    A[i], Ac[i] = gen(f'a{i}_', 10-i)
B[11] = sp.expand(sp.Rational(3,2)*be/al*(y-r)*A[7])
assert sp.simplify(rung_edge(18, A, B)) == 0
print("rung 18 re-check: PASS")

def strip(e):
    num, _ = sp.fraction(sp.together(sp.factor(e)))
    out = sp.S(1)
    for f, m in sp.factor_list(num)[1]:
        if f.is_number or f in NZ: continue
        out *= f
    return sp.factor(out)

for d in range(17, 11, -1):
    k = d+1-M
    B[k], cB = gen(f'b{k}_', 15-k)
    eqs = sp.Poly(rung_edge(d, A, B), y).all_coeffs()
    Mat, vec = sp.linear_eq_to_matrix(eqs, cB)
    Aug = Mat.row_join(vec); rM = Mat.rank()
    conds = []
    if Aug.rank() > rM:
        seen = set()
        for rows in combinations(range(Aug.shape[0]), rM+1):
            dd = Aug[list(rows), :].det() if Aug.shape[1] == rM+1 else None
            if dd is None: break
            if dd != 0: seen.add(strip(dd))
        conds = sorted(seen - {sp.S(1)}, key=sp.count_ops)
    print(f"\nrung {d:2d}: {Mat.shape[0]} eqs, {Mat.shape[1]} unknowns, rank {rM}, "
          f"aug rank {Aug.rank()}")
    for c in conds: print("    COND:", c)
    if conds:
        base = sp.factor_list(conds[0])[1][0][0]
        tgt = sorted(base.free_symbols - NZ, key=str)
        sol = sp.solve(base, tgt[0], dict=True)[0]
        print(f"    imposing {base} = 0 -> {tgt[0]} = {sp.factor(sol[tgt[0]])}")
        for i in list(A): A[i] = sp.expand(A[i].subs(sol))
        for kk in list(B): B[kk] = sp.expand(B[kk].subs(sol))
        eqs = sp.Poly(rung_edge(d, A, B), y).all_coeffs()
    s2 = sp.solve(eqs, cB, dict=True)
    if not s2:
        print("    !! still inconsistent"); break
    B[k] = sp.expand(B[k].subs(s2[0]))
    for i in range(1, 9):
        if i in A and A[i] != 0 and sp.simplify(A[i].subs(y, r)) == 0:
            print(f"    => (y-1) divides A_{i}")
