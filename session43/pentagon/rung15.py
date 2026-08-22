#!/usr/bin/env python3
"""Rung 15's residual conditions, exactly, via the LEFT NULL SPACE.

At rung d the only term carrying the new unknown B_{d-7} is (i,k) = (8, d-7), so
the coefficient matrix Mat depends on A_8 ALONE.  Rungs 18/17/16 each had full
column rank, so no free constants of integration have appeared yet and B_8's
coefficients are the only unknowns at rung 15.  Hence:

    conditions  =  { n . vec = 0  :  n in leftnull(Mat) }

which is exact and costs one nullspace instead of 405 dense symbolic minors.
"""
import sympy as sp
y = sp.symbols('y'); M, N = 8, 12
r = sp.Integer(1)                     # y-scaling gauge
al, be = sp.symbols('alpha beta', nonzero=True)

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

A = {8: al*(y-r)**2}
B = {12: be*(y-r)**3}
C7, cC7 = gen('c7_', 2)
A[7] = sp.expand((y-r)*C7)                                  # rung 17
A[6], cA6 = gen('a6_', 4)
A[5], cA5 = gen('a5_', 5)
A[4], cA4 = gen('a4_', 6)
B[11] = sp.expand(sp.Rational(3,2)*be/al*(y-r)*A[7])
assert sp.expand(rung_edge(18, A, B)) == 0
print("rung 18 identity: PASS")

for d in (17, 16):
    k = d+1-M
    Bk, cB = gen(f'b{k}_', 15-k)
    eqs = sp.Poly(rung_edge(d, A, {**B, k: Bk}), y).all_coeffs()
    Mat, vec = sp.linear_eq_to_matrix(eqs, cB)
    assert Mat.rank() == len(cB), f"rung {d} not full column rank"
    sol = sp.solve(eqs, cB, dict=True)[0]
    B[k] = sp.expand(Bk.subs(sol))
    assert sp.expand(rung_edge(d, A, B)) == 0
    print(f"rung {d}: solved B_{k}, full column rank, identity re-check PASS")

d, k = 15, 8
Bk, cB = gen('b8_', 7)
eqs = sp.Poly(rung_edge(d, A, {**B, k: Bk}), y).all_coeffs()
Mat, vec = sp.linear_eq_to_matrix(eqs, cB)
print(f"\nrung 15: Mat {Mat.shape}, depends only on alpha: "
      f"{Mat.free_symbols <= {al}}")
LN = Mat.T.nullspace()
print(f"  left-null dim = {len(LN)}  (so {len(LN)} residual conditions)")
conds = []
for n in LN:
    c = sp.expand((n.T*vec)[0, 0])
    c = sp.factor(sp.simplify(c))
    conds.append(c)
for j, c in enumerate(conds):
    num, den = sp.fraction(sp.together(c))
    fl = [f for f, m in sp.factor_list(sp.expand(num))[1] if not f.is_number and f not in (al, be)]
    print(f"\n  COND {j+1}: nontrivial factors = {len(fl)}")
    for f in fl:
        print("     ", sp.factor(f))
