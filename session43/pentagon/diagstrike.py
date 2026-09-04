#!/usr/bin/env python3
"""DIRECT STRIKE, done with the diagonal structure instead of sp.solve.

Level L (for L >= 7), isolating the new unknowns against h_8 = c0 sigma^8 and
g_12 = c1 sigma^12:

    8 c0 sigma^7 D_{L-8}(g_{L-8})  -  12 c1 sigma^11 D_{L-12}(h_{L-12})  =  -C_L

where D_k(f) = k f - sigma f'  and  C_L is everything else at that level.
D_k is DIAGONAL in the sigma-basis: D_k(sigma^m) = (k-m) sigma^m.  Hence, writing
[.]_m for the sigma^m coefficient, level L is

    8 c0 (L-8-m) [g_{L-8}]_m  -  12 c1 (L-8-m) [h_{L-12}]_{m-4}  =  -[C_L/sigma^7]_m

(the two diagonal factors coincide: L-8-m and (L-12)-(m-4) are equal).  So:

  * m != L-8 : solvable, one equation in two unknowns -> freedom
  * m == L-8 : BOTH coefficients vanish -> the scalar obstruction
                    [C_L]_{sigma^(L-1)} = 0
  * plus the divisibility  sigma^7 | C_L   (7 more conditions)

Eight conditions per level, no linear solve anywhere.
"""
import sympy as sp
s, tau, c0, c1 = sp.symbols('s tau c0 c1')
sg = sp.Symbol('sigma')

def D(k, f):   # k f - sigma f'
    return sp.expand(k*f - sg*sp.diff(f, sg))
print("CONTROL: D_k is diagonal, D_k(sigma^m) = (k-m) sigma^m")
ok = all(sp.simplify(D(k, sg**m) - (k-m)*sg**m) == 0 for k in range(-2, 14) for m in range(0, 14))
print("  ", "PASS" if ok else "FAIL")

print("\nCONTROL: the two diagonal factors coincide")
print("   from g: (L-8) - m ;  from h: (L-12) - (m-4) = L-8-m.  Identical -> PASS")

# verify the isolation identity symbolically in s
S, TAU = sp.symbols('s tau')
sig = S - TAU
g = sp.Function('g'); h = sp.Function('h')
L = sp.Symbol('L')
for Lv in (19, 18, 17, 12, 11):
    gg, hh = sp.Function('g')(S), sp.Function('h')(S)
    lhs = ((Lv-8)*sp.diff(c0*sig**8, S)*gg - 8*(c0*sig**8)*sp.diff(gg, S)
           + 12*sp.diff(hh, S)*(c1*sig**12) - (Lv-12)*hh*sp.diff(c1*sig**12, S))
    rhs = (8*c0*sig**7*((Lv-8)*gg - sig*sp.diff(gg, S))
           - 12*c1*sig**11*((Lv-12)*hh - sig*sp.diff(hh, S)))
    same = sp.simplify(sp.expand(lhs - rhs)) == 0
    print(f"CONTROL isolation identity at L={Lv}:", "PASS" if same else "FAIL")
