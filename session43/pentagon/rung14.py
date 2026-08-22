#!/usr/bin/env python3
"""Rungs 14, 13, 12 -- the rest of the edge descent.

Carried forward, each established by its own rank/nullspace computation:
  rung 19: disc(A_8) = 0        -> A_8 = alpha (y-r)^2 , B_12 = beta (y-r)^3
  rung 18: (none)               -> B_11 = (3 beta/2 alpha)(y-r) A_7
  rung 17: A_7(r) = 0           -> A_7 = (y-r) C_7
  rung 16: (none)
  rung 15: A_7'(r)^2 = 4 alpha A_6(r)

From rung 15 on, Mat is column-rank-deficient and the solution carries a free
constant of integration.  It is kept SYMBOLIC and passed down (lesson A3).
"""
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
A[6], cA6 = gen('a6_', 4)
A[5], cA5 = gen('a5_', 5)
A[4], cA4 = gen('a4_', 6)
A[3], cA3 = gen('a3_', 7)
B[11] = sp.expand(sp.Rational(3,2)*be/al*(y-r)*A[7])

# impose rung 15's condition:  4 alpha A_6(r) = A_7'(r)^2
sub15 = {cA6[0]: sp.expand(sp.diff(A[7], y).subs(y, r)**2/(4*al) - sum(cA6[1:]))}
A[6] = sp.expand(A[6].subs(sub15))
print("rung-15 condition imposed:  4*alpha*A_6(r) - A_7'(r)^2 =",
      sp.simplify(4*al*A[6].subs(y, r) - sp.diff(A[7], y).subs(y, r)**2))

free = []
for d in (17, 16, 15, 14, 13, 12):
    k = d + 1 - M
    Bk, cB = gen(f'b{k}_', 15-k)
    eqs = sp.Poly(rung_edge(d, A, {**B, k: Bk}), y).all_coeffs()
    unk = cB + free
    Mat, vec = sp.linear_eq_to_matrix(eqs, unk)
    LN = Mat.T.nullspace()
    conds = []
    for n in LN:
        c = sp.simplify(sp.expand((n.T*vec)[0, 0]))
        if c != 0:
            num, _ = sp.fraction(sp.together(c))
            fl = [f for f, m in sp.factor_list(sp.expand(num))[1]
                  if not f.is_number and f not in (al, be)]
            for f in fl:
                if f not in conds: conds.append(sp.expand(f))
    ker = len(unk) - Mat.rank()
    print(f"\nrung {d:2d}: {Mat.shape[0]} eqs, {len(unk)} unk, rank {Mat.rank()}, "
          f"kernel {ker}, left-null {len(LN)}, NEW CONDITIONS {len(conds)}")
    for c in conds:
        print("   COND:", sp.factor(c))
    if conds: break
    sol = sp.solve(eqs, unk, dict=True)
    if not sol:
        print("   !! solve returned nothing despite consistency -- investigate")
        break
    s = sol[0]
    Bk = sp.expand(Bk.subs(s))
    B[k] = Bk
    free = sorted((set(Bk.free_symbols) & set(unk)) | (set(free) - set(s)), key=str)
    print(f"   solved B_{k}; free constants carried: {free}")
