#!/usr/bin/env python3
"""The edge cascade: run rungs 18..12, at each one solving for B_{d-7} by RANK
(not sp.solve) and imposing the residual conditions on the A_i.

Established so far, each by an independent rank computation:
  rung 19 -> disc(A_8) = 0, i.e. A_8 = alpha (y-r)^2 ; B_12 = beta (y-r)^3
  rung 18 -> B_11 = (3 beta / 2 alpha) (y-r) A_7 , no residual condition
  rung 17 -> A_7(r) = 0
alpha, beta, r are all nonzero: alpha = p_16_8, A_8(0) = alpha r^2 = p_14_8,
beta = q_24_12, B_12(0) = -beta r^3 = q_21_12, and all six are the mutable
Newton-polygon vertices a genuine candidate must keep nonzero.
"""
import sympy as sp
from itertools import combinations
y = sp.symbols('y'); M, N = 8, 12
def rung_edge(d, A, B):
    s = 0
    for i in range(1, M+1):
        k = d+1-i
        if 2 <= k <= N and i in A and k in B:
            s += (2*k-3*i)*A[i]*B[k] + y*(i*A[i]*sp.diff(B[k],y) - k*sp.diff(A[i],y)*B[k])
    return sp.expand(s)
al, be, r = sp.symbols('alpha beta r', nonzero=True)
NZ = {al, be, r}
def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    return sum(c[i]*y**i for i in range(deg+1)), c
A = {8: al*(y-r)**2}; B = {12: be*(y-r)**3}
Ac = {}
for i in range(1, 8):
    A[i], Ac[i] = gen(f'a{i}_', 10-i)

def strip(e):
    """drop factors that are nonzero by the six-vertex non-degeneracy"""
    e = sp.factor(e)
    num, _ = sp.fraction(sp.together(e))
    out = sp.S(1)
    for f, m in sp.factor_list(num)[1]:
        if f.is_number or f in NZ: continue
        out *= f
    return sp.factor(out)

for d in range(18, 11, -1):
    k = d+1-M
    B[k], cB = gen(f'b{k}_', 15-k)
    eqs = sp.Poly(rung_edge(d, A, B), y).all_coeffs()
    Mat, vec = sp.linear_eq_to_matrix(eqs, cB)
    Aug = Mat.row_join(vec); rM = Mat.rank()
    conds = set()
    if Aug.rank() > rM:
        for rows in combinations(range(Aug.shape[0]), rM+1):
            for cols in combinations(range(Aug.shape[1]), rM+1):
                dd = Aug[list(rows), list(cols)].det()
                if dd != 0: conds.add(strip(dd))
    conds = sorted(conds - {sp.S(1)}, key=sp.count_ops)
    print(f"\nrung {d:2d}: {Mat.shape[0]} eqs, {Mat.shape[1]} unknowns, rank {rM}")
    print(f"  residual conditions: {len(conds)}")
    for c in conds: print("    COND:", c)
    if conds:
        # impose the simplest condition by solving it for one A-coefficient
        c0 = conds[0]
        base = sp.factor_list(c0)[1][0][0] if sp.factor_list(c0)[1] else c0
        tgt = sorted(base.free_symbols - NZ, key=str)
        if not tgt: print("  !! condition involves no A-coefficient:", base); break
        sol = sp.solve(base, tgt[0], dict=True)
        if not sol: print("  !! could not solve", base, "for", tgt[0]); break
        sub = sol[0]
        print(f"  imposing {base} = 0  ->  {tgt[0]} = {sp.factor(sub[tgt[0]])}")
        for i in A: A[i] = sp.expand(A[i].subs(sub))
        for kk in B: B[kk] = sp.expand(B[kk].subs(sub))
        # re-solve this rung with the condition imposed
        eqs = sp.Poly(rung_edge(d, A, B), y).all_coeffs()
        s2 = sp.solve(eqs, cB, dict=True)
        if not s2: print("  !! still inconsistent after imposing"); break
        B[k] = sp.expand(B[k].subs(s2[0]))
    else:
        s2 = sp.solve(eqs, cB, dict=True)
        B[k] = sp.expand(B[k].subs(s2[0]))
    for i in range(1, 8):
        Ai = sp.factor(A[i])
        if Ai != 0 and sp.simplify(Ai.subs(y, r)) == 0:
            print(f"  => (y-r) divides A_{i}")
