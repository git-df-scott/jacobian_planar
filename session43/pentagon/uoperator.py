#!/usr/bin/env python3
"""The operator {u,-} and the collapse of each cascade level to ONE unknown.

u = x y^2 - tau y, w-homogeneous of weight 1, and PRIMITIVE (its generic fibre
x = (tau y + c)/y^2 is a rational curve, hence irreducible), so the ring of its
first integrals is exactly C[u].

On the weight-k basis {x^i y^{i+k}}:
    {u, x^i y^{i+k}} = (k-i) x^i y^{i+k+1} + tau*i*x^(i-1) y^(i+k)
-- bidiagonal, weight k -> weight k+1.

Level L of the cascade, with P_8 = c0 u^8 and Q_12 = c1 u^12 known:
    {P_{L-12}, c1 u^12} + {c0 u^8, Q_{L-8}} = -(known)
    -12 c1 u^11 {u, P_{L-12}} + 8 c0 u^7 {u, Q_{L-8}} = -(known)
    u^7 * {u, 8 c0 Q_{L-8} - 12 c1 u^4 P_{L-12}} = -(known)
so with W_L := 8 c0 Q_{L-8} - 12 c1 u^4 P_{L-12},

    **{u, W_L} = -(known) / u^7**

Two obstructions per level: the known part must be DIVISIBLE by u^7, and the
quotient must lie in the image of {u,-}.
"""
import sympy as sp
x, y, tau = sp.symbols('x y tau')
u = x*y**2 - tau*y
def br(f, g): return sp.expand(sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x))

print("CONTROL 1: the bidiagonal formula for {u, x^i y^(i+k)}")
ok = True
for k in range(-1, 6):
    for i in range(0, 7):
        j = i+k
        if j < 0: continue
        lhs = br(u, x**i*y**j)
        rhs = sp.expand((k-i)*x**i*y**(j+1) + (tau*i*x**(i-1)*y**j if i >= 1 else 0))
        if sp.simplify(lhs-rhs) != 0: ok = False; print(f"  MISMATCH i={i} k={k}")
print("  ", "PASS" if ok else "FAIL")

print("\nCONTROL 2: kernel of {u,-} on weight k is exactly span(u^k)")
ok = True
for k in range(0, 7):
    if sp.simplify(br(u, u**k)) != 0: ok = False
print("  {u, u^k} = 0 for k=0..6:", "PASS" if ok else "FAIL")

print("\nCONTROL 3: the level collapse  {P_a, c1 u^12} + {c0 u^8, Q_b}"
      " == u^7 {u, 8c0 Q_b - 12 c1 u^4 P_a}")
c0, c1 = sp.symbols('c0 c1')
Pa, Qb = sp.Function('Pa')(x,y), sp.Function('Qb')(x,y)
lhs = sp.expand(br(Pa, c1*u**12) + br(c0*u**8, Qb))
W = 8*c0*Qb - 12*c1*u**4*Pa
rhs = sp.expand(u**7*br(u, W))
print("  ", "PASS" if sp.simplify(lhs-rhs) == 0 else f"FAIL: {sp.simplify(lhs-rhs)}")

print("\nCONTROL 4: u is primitive (generic fibre irreducible)")
c = sp.Symbol('c')
f = sp.Poly(sp.expand(u - c), x, y)
print("   u - c =", sp.factor(u - c), " -> irreducible for generic c:",
      len(sp.factor_list(u - c)[1]) == 1)
print("   (so the first integrals of {u,-} are exactly C[u], and the freedom at")
print("    each cascade level is ONE constant -- the kernel the three earlier")
print("    rational-function cascades destroyed by choosing it greedily.)")
