#!/usr/bin/env python3
"""The w-graded cascade.  w(x^i y^j) = j - i.

P splits as P_8 + ... + P_{-1}, Q as Q_12 + ... + Q_{-1} (the w-ranges of N(P)
and N(Q)).  The bracket adds w-degrees, so {P,Q} = x^2 becomes

    level L:   sum_{a+b=L} {P_a, Q_b}  =  [L = -2] * x^2 ,     L = 20 .. -2 .

22 homogeneous levels, then one inhomogeneous one at the bottom.
"""
import sympy as sp
x, y = sp.symbols('x y')
def br(f, g): return sp.expand(sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x))

def Prows(jmax=16):
    r = {}
    for j in range(jmax+1):
        lo, hi = max(0, j-8), min(8, j//2+1)
        if lo <= hi: r[j] = (lo, hi)
    return r
PR = Prows()
def p_ok(j, i): return j in PR and PR[j][0] <= i <= PR[j][1]
def q_ok(j, k):
    if not (0 <= k <= 12): return False
    lo = (k+1)//2 if k <= 2 else 2*k-3
    return lo <= j <= 12+k

PS, QS = {}, {}
for a in range(-1, 9):
    t = 0
    for i in range(0, 9):
        j = i+a
        if j >= 0 and p_ok(j, i):
            t += (0 if (j,i)==(0,0) else 1 if (j,i)==(0,1) else sp.Symbol(f'p_{j}_{i}'))*x**i*y**j
    PS[a] = sp.expand(t)
for b in range(-1, 13):
    t = 0
    for k in range(0, 13):
        j = k+b
        if j >= 0 and q_ok(j, k):
            t += (0 if (j,k)==(0,0) else 1 if (j,k)==(1,2) else sp.Symbol(f'q_{j}_{k}'))*x**k*y**j
    QS[b] = sp.expand(t)

print("w-graded pieces:")
for a in range(8, -2, -1):
    print(f"  P_{a:2d}: {sp.Poly(PS[a],x,y).length() if PS[a]!=0 else 0} terms   {PS[a] if a<=0 or a>=8 else ''}")
print()
for b in range(12, -2, -1):
    if b in (12, 0, -1):
        print(f"  Q_{b:2d}: {sp.Poly(QS[b],x,y).length() if QS[b]!=0 else 0} terms   {QS[b] if b<=0 else ''}")

def level(L):
    s = 0
    for a in range(-1, 9):
        b = L-a
        if -1 <= b <= 12: s += br(PS[a], QS[b])
    return sp.expand(s)

print("\nCONTROL level -2 must be exactly x^2 (both pieces are gauge-fixed vertices):")
l2 = level(-2)
print("   level(-2) =", l2, " ->", "PASS" if sp.simplify(l2 - x**2) == 0 else "FAIL")

print("\nCONTROL level -1 (first genuine condition):")
l1 = level(-1)
eqs = sp.Poly(l1, x, y).coeffs() if l1 != 0 else []
print("   level(-1) =", l1)
print("   conditions:", [sp.factor(e) for e in eqs])
