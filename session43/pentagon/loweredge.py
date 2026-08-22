#!/usr/bin/env python3
"""THE LOWER EDGE, exactly: an INHOMOGENEOUS one-variable ODE.

Grade by v(x^i y^j) = 2i - j.  On N(P) the maximum of v is 2, attained on the
edge (1,0)-(8,14); on N(Q) it is 3, on (2,1)-(12,21).  The bracket satisfies
v({f,g}) <= v(f)+v(g)-1, and v(x^2) = 4 = 2+3-1 EXACTLY -- so, unlike the upper
edge (where the top term vanishes), here the top term IS x^2.

With r := x y^2, every v-homogeneous piece is y^a F(r), and

    { y^a F(r), y^b G(r) } = y^(a+b+1) ( b F'(r) G(r) - a F(r) G'(r) )

In_v(P) = y^-2 Ah(r),  Ah(r) = sum_{i=1..8} p_{2i-2,i} r^i     (deg 8, ord 1)
In_v(Q) = y^-3 Qh(r),  Qh(r) = sum_{k=2..12} q_{2k-3,k} r^k    (deg 12, ord 2)

so the top v-piece of {P,Q} = x^2 reads, after y^-4 = (r/y^2)^2 / r^2,

    **2 Ah Qh' - 3 Ah' Qh = r^2**
"""
import sympy as sp
x, y, r = sp.symbols('x y r')
def br(f, g): return sp.expand(sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x))

print("CONTROL 1: {y^a F(xy^2), y^b G(xy^2)} = y^(a+b+1)(b F' G - a F G')")
ok = True
for a in range(-3, 3):
    for b in range(-3, 3):
        F, G = sp.Function('F'), sp.Function('G')
        lhs = sp.simplify(br(y**a*F(x*y**2), y**b*G(x*y**2)))
        R = sp.Symbol('R')
        rhs = sp.simplify((y**(a+b+1)*(b*sp.diff(F(R),R)*G(R) - a*F(R)*sp.diff(G(R),R))
                           ).subs(R, x*y**2))
        if sp.simplify(lhs-rhs) != 0: ok = False; print(f"   MISMATCH a={a} b={b}")
print("  ", "PASS" if ok else "FAIL")

print("\nCONTROL 2: v-degrees.  v(x^2) = 4 and v(P)+v(Q)-1 = 2+3-1 = 4 -> the top")
print("   v-piece of the bracket is x^2 itself, not zero.")
a, b = -2, -3
print(f"   y^(a+b+1) = y^{a+b+1} = y^-4, and x^2 = r^2/y^4 -> the relation is")
print("   2 Ah Qh' - 3 Ah' Qh = r^2")

Ah = sum(sp.Symbol(f'p_{2*i-2}_{i}')*r**i for i in range(1, 9))
Qh = sum(sp.Symbol(f'q_{2*k-3}_{k}')*r**k for k in range(2, 13))
E = sp.expand(2*Ah*sp.diff(Qh, r) - 3*sp.diff(Ah, r)*Qh - r**2)
P_ = sp.Poly(E, r)
eqs = P_.all_coeffs()
unk = sorted(E.free_symbols - {r}, key=str)
print(f"\nsystem: {len(eqs)} equations (r-degrees {P_.degree()}..0), {len(unk)} unknowns")
print("   deg(2 Ah Qh') = 8+11 = 19, deg(3 Ah' Qh) = 7+12 = 19, RHS degree 2")
print("   -> the top 17 coefficients must cancel; only r^2 survives.")

print("\nHOMOGENEOUS part: 2 Ah Qh' = 3 Ah' Qh  =>  (Qh^2/Ah^3)' = 0  =>  Qh^2 = c Ah^3")
A_, Q_ = sp.Function('A')(r), sp.Function('Q')(r)
chk = sp.simplify(sp.diff(Q_**2/A_**3, r)*A_**4/Q_ - (2*A_*sp.diff(Q_,r) - 3*sp.diff(A_,r)*Q_))
print("   CONTROL:", "PASS" if chk == 0 else f"FAIL {chk}")
print("   -- same shape as the UPPER edge, but here it is INHOMOGENEOUS (= r^2),")
print("      which is strictly more restrictive.")
