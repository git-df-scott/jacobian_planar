#!/usr/bin/env python3
"""THE UPPER EDGE.  A second, independent ladder -- and it is algebraic.

Supports:  a_i has y-range [2i-2, i+8]  (i=0..8);  q_k has [2k-3, 12+k] (k=0..12).
The LOWER ends gave the edge ladder of EDGE_LADDER.md.  The UPPER ends give
deg(a_i q_k') = deg(a_i' q_k) = (i+8)+(12+k)-1 = d+20, uniform for EVERY rung d
(the lower edge was uniform only for d = 12..19).

Top-y coefficient of rung d, with  ahat_i = p_{i+8,i},  qhat_k = q_{12+k,k}:
    i*ahat_i*(12+k)*qhat_k - k*(i+8)*ahat_i*qhat_k = (12i - 8k) ahat_i qhat_k
so rung d contributes   sum_{i+k=d+1} (3i - 2k) ahat_i qhat_k = 0 .
The RHS x^2 sits at y^0, never at y^(d+20), so EVERY rung is homogeneous.

In generating functions A(t) = sum ahat_i t^i, Qh(t) = sum qhat_k t^k:
    sum_{i,k} (3i-2k) ahat_i qhat_k t^(i+k) = t*(3 A' Qh - 2 A Qh')
so the whole system is  3 A' Qh = 2 A Qh'  <=>  (Qh^2 / A^3)' = 0  <=>  Qh^2 = c A^3.
"""
import sympy as sp
t, y, x = sp.symbols('t y x')
M, N = 8, 12

# ---------------------------------------------------------------- CONTROL 1
# top-y coefficient of each raw rung == the (3i-2k) anti-diagonal sum
ah = [sp.Symbol(f'ah{i}') for i in range(M+1)]
qh = [sp.Symbol(f'qh{k}') for k in range(N+1)]
lo_a = {i: 2*i-2 if i >= 1 else 0 for i in range(M+1)}
lo_q = {k: 2*k-3 if k >= 2 else (1 if k == 1 else 0) for k in range(N+1)}
a, q = {}, {}
for i in range(M+1):
    lo, hi = lo_a[i], i+8
    a[i] = sum(sp.Symbol(f'pa_{i}_{j}')*y**j for j in range(lo, hi)) + ah[i]*y**hi
for k in range(N+1):
    lo, hi = lo_q[k], 12+k
    q[k] = sum(sp.Symbol(f'qq_{k}_{j}')*y**j for j in range(lo, hi)) + qh[k]*y**hi

def rung(d):
    s = 0
    for i in range(M+1):
        k = d+1-i
        if 0 <= k <= N:
            s += i*a[i]*sp.diff(q[k], y) - k*sp.diff(a[i], y)*q[k]
    return sp.expand(s)

ok = True
for d in range(0, M+N):
    top = sp.expand(sp.Poly(rung(d), y).coeff_monomial(y**(d+20)))
    pred = sp.expand(sum((3*i - 2*(d+1-i))*ah[i]*qh[d+1-i]
                         for i in range(M+1) if 0 <= d+1-i <= N))
    if sp.simplify(top - 4*pred) != 0:
        ok = False; print(f"  MISMATCH d={d}: {sp.simplify(top-4*pred)}")
print("CONTROL 1 (top-y coefficient == 4*(3i-2k) anti-diagonal sum, all d):",
      "PASS" if ok else "FAIL")

# ---------------------------------------------------------------- CONTROL 2
# generating-function identity
A = sum(ah[i]*t**i for i in range(M+1))
Qh = sum(qh[k]*t**k for k in range(N+1))
lhs = sp.expand(sum((3*i-2*k)*ah[i]*qh[k]*t**(i+k)
                    for i in range(M+1) for k in range(N+1)))
rhs = sp.expand(t*(3*sp.diff(A, t)*Qh - 2*A*sp.diff(Qh, t)))
print("CONTROL 2 (generating function identity):", "PASS" if sp.expand(lhs-rhs) == 0 else "FAIL")

# ---------------------------------------------------------------- THE RESULT
print("\nSystem: 3 A' Qh = 2 A Qh'  for deg A = 8, deg Qh = 12  (2*12 = 3*8, consistent)")
print("=> (Qh^2/A^3)' = 0 => Qh^2 = c A^3 => every root of A has even multiplicity")
print("=> A(t) = c0 * G(t)^2 with deg G = 4, and Qh = c1 * G^3.\n")

# POSITIVE control: A = G^2, Qh = G^3 satisfies every rung
g = [sp.Symbol(f'g{i}') for i in range(5)]
G = sum(g[i]*t**i for i in range(5))
Asq, Qcu = sp.expand(G**2), sp.expand(G**3)
res = sp.expand(3*sp.diff(Asq,t)*Qcu - 2*Asq*sp.diff(Qcu,t))
print("POSITIVE control (A = G^2, Qh = G^3, G a free quartic):",
      "PASS" if sp.simplify(res) == 0 else f"FAIL {res}")

# NEGATIVE control: A with a simple root -> only Qh = 0
Abad = sp.expand((t-1)*(t-2)**2*(t-3)**2*(t-5)**2*(t-7))   # deg 8, two simple roots
cq = [sp.Symbol(f'z{k}') for k in range(N+1)]
Qb = sum(cq[k]*t**k for k in range(N+1))
eqs = sp.Poly(sp.expand(3*sp.diff(Abad,t)*Qb - 2*Abad*sp.diff(Qb,t)), t).all_coeffs()
sol = sp.solve(eqs, cq, dict=True)
allzero = bool(sol) and all(sp.simplify(Qb.subs(s)) == 0 for s in sol)
print("NEGATIVE control (A has simple roots -> Qh forced to 0):",
      "PASS" if allzero else f"FAIL {sol}")

# and a square A does admit a nonzero Qh
Agood = sp.expand(((t-2)*(t-3)*(t-5)*(t-7))**2)
eqs = sp.Poly(sp.expand(3*sp.diff(Agood,t)*Qb - 2*Agood*sp.diff(Qb,t)), t).all_coeffs()
sol = sp.solve(eqs, cq, dict=True)
Qs = sp.factor(Qb.subs(sol[0])) if sol else 0
print("POSITIVE control (A a perfect square -> nonzero Qh exists):",
      "PASS" if Qs != 0 else "FAIL", "  Qh =", Qs)
