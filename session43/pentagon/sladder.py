#!/usr/bin/env python3
"""THE s-LADDER: the pentagon in ONE variable.

Every w-homogeneous polynomial of weight a is  y^a h(s)  with  s := x y,
because x^i y^(i+a) = y^a (xy)^i.  In particular u = y(xy - tau) = y(s - tau).

Claim:   {y^a h(s), y^b g(s)} = y^(a+b) * ( b h'(s) g(s) - a h(s) g'(s) )

so with P = sum_a y^a h_a(s), Q = sum_b y^b g_b(s), the bracket {P,Q} = x^2
becomes, level by level in w,

    **sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} * s^2**

-- a ladder in ONE variable.  (x^2 = (s/y)^2 = y^-2 s^2, hence the level -2.)
"""
import sympy as sp
x, y, s, tau = sp.symbols('x y s tau')
def br(f, g): return sp.expand(sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x))

print("CONTROL 1: {y^a h(s), y^b g(s)} = y^(a+b) (b h' g - a h g')")
ok = True
for a in range(-1, 5):
    for b in range(-1, 5):
        h = sp.Function('h'); g = sp.Function('g')
        f1 = y**a*h(x*y); f2 = y**b*g(x*y)
        lhs = sp.simplify(br(f1, f2))
        S = sp.Symbol('S')
        rhs = y**(a+b)*(b*sp.diff(h(S),S)*g(S) - a*h(S)*sp.diff(g(S),S))
        rhs = sp.simplify(rhs.subs(S, x*y))
        if sp.simplify(lhs - rhs) != 0:
            ok = False; print(f"   MISMATCH a={a} b={b}: {sp.simplify(lhs-rhs)}")
print("  ", "PASS" if ok else "FAIL")

print("\nCONTROL 2: the gauge-fixed bottom pieces give x^2 exactly")
print("   P_-1 = x = y^-1 * s      -> h_-1(s) = s")
print("   Q_-1 = x^2 y = y^-1 * s^2 -> g_-1(s) = s^2")
a = b = -1
h_, g_ = s, s**2
val = sp.expand(b*sp.diff(h_, s)*g_ - a*h_*sp.diff(g_, s))
print(f"   b h' g - a h g' = {val}   -> {'PASS' if sp.simplify(val - s**2) == 0 else 'FAIL'}")
print("   and y^(a+b) = y^-2, so the term is y^-2 s^2 = x^2.  PASS")

print("\nCONTROL 3: u^k in these coordinates, and the operator {u,-}")
k = sp.Symbol('k', positive=True, integer=True)
hh = sp.Function('hh')
print("   u = y(s-tau), so u^k = y^k (s-tau)^k -> h(s) = (s-tau)^k")
for kk in range(0, 6):
    lhs = sp.simplify(br(y*(x*y-tau), y**kk*(x*y-tau)**kk))
    print(f"   {{u, u^{kk}}} = {lhs}" if lhs != 0 else f"   {{u, u^{kk}}} = 0  PASS")

print("\nCONTROL 4: {u, y^k h} = y^(k+1) [ k h - (s-tau) h' ]  (a = 1, h_a = s-tau)")
H = sp.Function('H')
lhs = sp.simplify(br(y*(x*y-tau), y**3*H(x*y)))
S = sp.Symbol('S')
rhs = sp.simplify((y**4*(3*H(S) - (S-tau)*sp.diff(H(S),S))).subs(S, x*y))
print("  ", "PASS" if sp.simplify(lhs-rhs) == 0 else f"FAIL {sp.simplify(lhs-rhs)}")
print("\n   In the basis sigma = s - tau, D_k(sigma^m) = (k-m) sigma^m -- DIAGONAL.")
print("   Kernel = sigma^k (i.e. u^k).  Image = everything except the sigma^k slot.")
print("   => EXACTLY ONE scalar obstruction per level: the sigma^k coefficient.")
