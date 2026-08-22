#!/usr/bin/env python3
"""TOP-Y LADDER OF THE RESIDUAL: A must be an 8th power of a linear form.

R = Q^2 - cP^3 has its top-y row (y-degree 24+k at x-exponent k) annihilated --
that row IS the upper-edge theorem Qh^2 = cA^3.  The computed r_7, r_6 both sit
exactly 17 rows lower, at y-degree 7+k, with the y-orders N(Q^2)=N(P^3) predicts.

Taking top-y coefficients of {P,R} = 2 x^2 Q with ahat_i = p_{i+8,i} at y-degree
i+8 and rhat_k at y-degree 7+k:
   LHS term (i,k) lands at y-degree (i+8)+(7+k)-1 = d+15, uniform in d;
   RHS 2 q_{d-2} lands at y-degree 12+(d-2) = d+10 < d+14.
So the LHS top-y coefficient must VANISH at every rung.
"""
import sympy as sp
y, t = sp.symbols('y t')
M, NR = 8, 7

ah = [sp.Symbol(f'ah{i}') for i in range(M+1)]
rh = [sp.Symbol(f'rh{k}') for k in range(NR+1)]
qh = [sp.Symbol(f'qh{k}') for k in range(13)]
a, r, q = {}, {}, {}
for i in range(M+1):
    a[i] = sum(sp.Symbol(f'pa_{i}_{j}')*y**j for j in range(0, i+8)) + ah[i]*y**(i+8)
for k in range(NR+1):
    r[k] = sum(sp.Symbol(f'rr_{k}_{j}')*y**j for j in range(0, 7+k)) + rh[k]*y**(7+k)
for k in range(13):
    q[k] = sum(sp.Symbol(f'qq_{k}_{j}')*y**j for j in range(0, 12+k)) + qh[k]*y**(12+k)

def rung(d):
    s = 0
    for i in range(M+1):
        k = d+1-i
        if 0 <= k <= NR:
            s += i*a[i]*sp.diff(r[k], y) - k*sp.diff(a[i], y)*r[k]
    return sp.expand(s - 2*(q[d-2] if 0 <= d-2 <= 12 else 0))

ok = True
for d in range(0, M+NR):
    top = sp.expand(sp.Poly(rung(d), y).coeff_monomial(y**(d+15)))
    pred = sp.expand(sum((7*i - 8*(d+1-i))*ah[i]*rh[d+1-i]
                         for i in range(M+1) if 0 <= d+1-i <= NR))
    if sp.simplify(top - pred) != 0:
        ok = False; print(f"  MISMATCH d={d}: {sp.simplify(top-pred)}")
print("CONTROL (top-y coefficient == (7i-8k) anti-diagonal sum, all d):",
      "PASS" if ok else "FAIL")

A  = sum(ah[i]*t**i for i in range(M+1))
Rh = sum(rh[k]*t**k for k in range(NR+1))
lhs = sp.expand(sum((7*i-8*k)*ah[i]*rh[k]*t**(i+k)
                    for i in range(M+1) for k in range(NR+1)))
rhs = sp.expand(t*(7*sp.diff(A,t)*Rh - 8*A*sp.diff(Rh,t)))
print("CONTROL (generating function 7A'Rh - 8A Rh'):",
      "PASS" if sp.expand(lhs-rhs) == 0 else "FAIL")

print("\n=> 7 A' Rh = 8 A Rh'  =>  (Rh^8 / A^7)' = 0  =>  Rh^8 = c A^7")
print("   deg A = 8, deg Rh = 7:  8*7 = 56 = 7*8, consistent.")
print("   A = c0 G^2 (upper edge) => Rh^8 = c' G^14 => every root of G has")
print("   multiplicity e with 8 | 14e, i.e. 4 | 7e, i.e. 4 | e.  G is a quartic:")
print("   => G = g (t - tau)^4   and   A = c0' (t - tau)^8 ,  Rh = c (t - tau)^7.")

# POSITIVE control
g_, tau, c0_ = sp.symbols('g tau c0')
Ag  = sp.expand(c0_*(t-tau)**8)
Rg  = sp.expand(sp.Symbol('cR')*(t-tau)**7)
res = sp.expand(7*sp.diff(Ag,t)*Rg - 8*Ag*sp.diff(Rg,t))
print("\nPOSITIVE control (A = c0(t-tau)^8, Rh = cR(t-tau)^7):",
      "PASS" if sp.simplify(res) == 0 else f"FAIL {res}")
# NEGATIVE control: A a square but NOT an 8th power
Ab = sp.expand(((t-1)*(t-2)*(t-3)*(t-5))**2)
zz = [sp.Symbol(f'z{k}') for k in range(NR+1)]
Rb = sum(zz[k]*t**k for k in range(NR+1))
eqs = sp.Poly(sp.expand(7*sp.diff(Ab,t)*Rb - 8*Ab*sp.diff(Rb,t)), t).all_coeffs()
sol = sp.solve(eqs, zz, dict=True)
allz = bool(sol) and all(sp.simplify(Rb.subs(s)) == 0 for s in sol)
print("NEGATIVE control (A = G^2 with G having 4 distinct roots -> Rh forced 0):",
      "PASS" if allz else f"FAIL {sol}")
