#!/usr/bin/env python3
"""The EDGE LADDER: rungs 19..12 of the m=8 x-ladder involve only the top edge.

With  a_i = y^(2i-2) A_i,  deg A_i = 10-i   (i = 1..8)
      q_k = y^(2k-3) B_k,  deg B_k = 15-k   (k = 2..12)
every rung d = 12..19 has all its terms on the single power y^(2d-4), so it
divides down to a relation among the EDGE polynomials alone:

    sum_{i+k=d+1} { (2k-3i) A_i B_k + y [ i A_i B_k' - k A_i' B_k ] } = 0

Note 2k-3i vanishes exactly on the edge slope k/i = 3/2, which is why the top
rung (8,12) is purely differential.
"""
import sympy as sp
y = sp.symbols('y')
M, N = 8, 12

def rung_raw(d, a, q):
    s = 0
    for i in range(M + 1):
        k = d + 1 - i
        if 0 <= k <= N:
            s += i * a[i] * sp.diff(q[k], y) - k * sp.diff(a[i], y) * q[k]
    return sp.expand(s)

def rung_edge(d, A, B):
    s = 0
    for i in range(1, M + 1):
        k = d + 1 - i
        if 2 <= k <= N:
            s += (2*k - 3*i) * A[i] * B[k] + y * (i*A[i]*sp.diff(B[k], y) - k*sp.diff(A[i], y)*B[k])
    return sp.expand(s)

# ---------------------------------------------------------------- CONTROL
# The reduction itself: raw rung must equal y^(2d-4) * edge rung, for d=12..19.
A = {i: sp.Function(f'A{i}')(y) for i in range(1, M + 1)}
B = {k: sp.Function(f'B{k}')(y) for k in range(2, N + 1)}
a = {i: y**(2*i - 2) * A[i] for i in range(1, M + 1)}
q = {k: y**(2*k - 3) * B[k] for k in range(2, N + 1)}
print("CONTROL: raw rung == y^(2d-4) * edge rung, d = 12..19")
allok = True
for d in range(12, 20):
    lhs = rung_raw(d, a, q)
    rhs = sp.expand(y**(2*d - 4) * rung_edge(d, A, B))
    ok = sp.simplify(lhs - rhs) == 0
    allok &= ok
    print(f"  d={d:2d}  {'PASS' if ok else 'FAIL'}")
print("  overall:", "PASS" if allok else "FAIL")

# ---------------------------------------------------------------- DESCENT
print("\nDESCENT along the top edge")
al, r = sp.symbols('alpha r', nonzero=True)
be = sp.symbols('beta', nonzero=True)
A8 = al*(y - r)**2          # rung 19: disc(A_8) = 0
B12 = be*(y - r)**3
print("  rung 19 =>  A_8 = alpha (y-r)^2 ,  B_12 = beta (y-r)^3")
print("     check:", sp.simplify(rung_edge(19, {8: A8}, {12: B12})) == 0)

def poly(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg + 1)]
    return sum(c[i]*y**i for i in range(deg + 1)), c

A7, cA7 = poly('a7_', 3)          # deg A_7 = 10-7 = 3
B11, cB11 = poly('b11_', 4)       # deg B_11 = 15-11 = 4
E = sp.Poly(rung_edge(18, {7: A7, 8: A8}, {11: B11, 12: B12}), y)
eqs = E.all_coeffs()
print(f"\n  rung 18: {len(eqs)} equations, {len(cB11)} unknowns (B_11 coeffs)")
Mat, vec = sp.linear_eq_to_matrix(eqs, cB11)
sol = sp.solve(eqs, cB11, dict=True)
print("  solve for B_11 ->", "solution found" if sol else "NO SOLUTION")
if sol:
    s = sol[0]
    print("  solved:", {k: sp.factor(v) for k, v in s.items()})
    left = [c for c in cB11 if c not in s]
    print("  free B_11 coeffs:", left)
    resid = [sp.factor(sp.simplify(e.subs(s))) for e in eqs]
    resid = [x for x in resid if x != 0]
    print("  RESIDUAL conditions on A_7 (count %d):" % len(resid))
    for x in sorted(set(resid), key=sp.count_ops):
        print("    ", x)
