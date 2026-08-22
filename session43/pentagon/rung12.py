#!/usr/bin/env python3
"""Rung 12 -- the last rung of the edge ladder -- with rungs 15 and 13 imposed."""
import sympy as sp
y = sp.symbols('y'); M, N = 8, 12
r = sp.Integer(1)
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
A = {8: al*(y-r)**2}; B = {12: be*(y-r)**3}
C7, cC7 = gen('c7_', 2); A[7] = sp.expand((y-r)*C7)
A[6], cA6 = gen('a6_', 4); A[5], cA5 = gen('a5_', 5)
A[4], cA4 = gen('a4_', 6); A[3], cA3 = gen('a3_', 7)
B[11] = sp.expand(sp.Rational(3,2)*be/al*(y-r)*A[7])
A[6] = sp.expand(A[6].subs({cA6[0]: sp.diff(A[7],y).subs(y,r)**2/(4*al) - sum(cA6[1:])}))
R13 = sp.sympify("4*a5_0*alpha**2 + 4*a5_1*alpha**2 + 4*a5_2*alpha**2 + 4*a5_3*alpha**2 + 4*a5_4*alpha**2 + 4*a5_5*alpha**2 - 2*a6_1*alpha*c7_0 - 2*a6_1*alpha*c7_1 - 2*a6_1*alpha*c7_2 - 4*a6_2*alpha*c7_0 - 4*a6_2*alpha*c7_1 - 4*a6_2*alpha*c7_2 - 6*a6_3*alpha*c7_0 - 6*a6_3*alpha*c7_1 - 6*a6_3*alpha*c7_2 - 8*a6_4*alpha*c7_0 - 8*a6_4*alpha*c7_1 - 8*a6_4*alpha*c7_2 + c7_0**2*c7_1 + 2*c7_0**2*c7_2 + 2*c7_0*c7_1**2 + 6*c7_0*c7_1*c7_2 + 4*c7_0*c7_2**2 + c7_1**3 + 4*c7_1**2*c7_2 + 5*c7_1*c7_2**2 + 2*c7_2**3").subs(sp.Symbol("alpha"), al)
A[5] = sp.expand(A[5].subs(sp.solve(R13, cA5[0], dict=True)[0]))
print("rung 13 imposed, residual =", sp.simplify(R13.subs(sp.solve(R13, cA5[0], dict=True)[0])))
free = []
for d in (17, 16, 15, 14, 13, 12):
    k = d+1-M
    Bk, cB = gen(f'b{k}_', 15-k)
    eqs = sp.Poly(rung_edge(d, A, {**B, k: Bk}), y).all_coeffs()
    unk = cB + free
    Mat, vec = sp.linear_eq_to_matrix(eqs, unk)
    conds = []
    for n in Mat.T.nullspace():
        c = sp.simplify(sp.expand((n.T*vec)[0,0]))
        if c != 0:
            num,_ = sp.fraction(sp.together(c))
            for f,m in sp.factor_list(sp.expand(num))[1]:
                if not f.is_number and f not in (al,be) and f not in conds:
                    conds.append(sp.expand(f))
    print(f"rung {d:2d}: {Mat.shape[0]} eqs, {len(unk)} unk, rank {Mat.rank()}, "
          f"kernel {len(unk)-Mat.rank()}, NEW CONDITIONS {len(conds)}")
    for c in conds: print("   COND:", sp.factor(c))
    if conds and d < 13: break
    sol = sp.solve(eqs, unk, dict=True)
    if not sol: print("   !! no solve"); break
    sset = sol[0]
    Bk = sp.expand(Bk.subs(sset)); B[k] = Bk
    free = sorted((set(Bk.free_symbols) & set(unk)) | (set(free)-set(sset)), key=str)
