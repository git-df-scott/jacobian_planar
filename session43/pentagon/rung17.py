#!/usr/bin/env python3
"""Rung 17 done as a RANK computation, not sp.solve.

sp.solve returning [] on a linear system with symbolic coefficients means
'generically inconsistent' -- which is a statement that residual conditions on
the A_i must hold, NOT a verdict of emptiness.  The conditions are exactly the
minors that force rank[Mat|vec] == rank[Mat].
"""
import sympy as sp
y = sp.symbols('y'); M, N = 8, 12
def rung_edge(d, A, B):
    s = 0
    for i in range(1, M+1):
        k = d+1-i
        if 2 <= k <= N and i in A and k in B:
            s += (2*k-3*i)*A[i]*B[k] + y*(i*A[i]*sp.diff(B[k],y) - k*sp.diff(A[i],y)*B[k])
    return sp.expand(s)
al, be, r = sp.symbols('alpha beta r', nonzero=True)
def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    return sum(c[i]*y**i for i in range(deg+1)), c
A = {8: al*(y-r)**2}; B = {12: be*(y-r)**3}
A[7], cA7 = gen('a7_', 3)
A[6], cA6 = gen('a6_', 4)
B[11] = sp.Rational(3,2)*be/al*(y-r)*A[7]        # from rung 18 (verified)
assert sp.simplify(rung_edge(18, A, B)) == 0, "rung 18 re-check FAILED"
print("rung 18 re-check: PASS")

B[10], cB10 = gen('b10_', 5)
eqs = sp.Poly(rung_edge(17, A, B), y).all_coeffs()
Mat, vec = sp.linear_eq_to_matrix(eqs, cB10)
print(f"rung 17: {Mat.shape[0]} equations, {Mat.shape[1]} unknowns")
Aug = Mat.row_join(vec)
rM, rA = Mat.rank(), Aug.rank()
print(f"  generic rank(Mat)={rM}  rank([Mat|vec])={rA}")
if rM == rA:
    print("  CONSISTENT generically -> no residual condition at rung 17")
else:
    print("  generically INCONSISTENT -> residual conditions are the (rM+1)-minors of [Mat|vec]")
    n = rM + 1
    from itertools import combinations
    conds = set()
    for rows in combinations(range(Aug.shape[0]), n):
        for cols in combinations(range(Aug.shape[1]), n):
            dd = Aug[list(rows), list(cols)].det()
            if dd != 0:
                conds.add(sp.factor(dd))
    print(f"  {len(conds)} nonzero minors; smallest by op-count:")
    for c in sorted(conds, key=sp.count_ops)[:8]:
        print("   ", c)
