#!/usr/bin/env python3
"""Codex's CODEX-014 tasks, plus the two upper gates at level 15.

TASK 1: independently check his two linear coefficients on branch 2 --
        kappa in C5 at  -45 a0^3 / (16 c0^2)
        d0    in C6 at   24 c1 F3 / c0^2
TASK 2: decompose the exceptional divisor  a0 = 0  OR  F3 = 0.
MINE  : the two UPPER gates at level 15 (deg W_7 <= 10, RHS degree 12).

His conventions throughout, so a mismatch is a real mismatch.
"""
import sympy as sp
z = sp.Symbol('z')
c0, c1 = sp.symbols('c0 c1', nonzero=True)
lam, kappa, eta, mu = sp.symbols('lambda kappa eta mu')
a = sp.symbols('a0:5'); b = sp.symbols('b0:9'); d = sp.symbols('d0:8'); e = sp.symbols('e0:7')
def pairing(wf,f,wg,g): return sp.expand(wg*sp.diff(f,z)*g - wf*f*sp.diff(g,z))
def D(w,f): return sp.expand(w*f - z*sp.diff(f,z))
def invert(w,rhs,ker,bound=None):
    ans = ker*z**w
    for (deg,),co in sp.Poly(rhs,z).terms():
        if deg != w: ans += co*z**deg/(w-deg)
    ans = sp.expand(ans)
    assert sp.simplify(D(w,ans)-rhs) == 0
    if bound is not None and ans != 0:
        dg = sp.degree(ans, z)
        if dg > bound: print(f"   !! invert: degree {dg} exceeds support bound {bound}")
    return ans

h7 = z**4*sum(a[i]*z**i for i in range(5))
h6 = sum(b[i]*z**i for i in range(9))
h5 = sum(d[i]*z**i for i in range(8))
h4 = sum(e[i]*z**i for i in range(7))
g12 = c1*z**12
g11 = 3*c1*z**4*h7/(2*c0) + lam*z**11/(8*c0)

c18 = pairing(7,h7,11,g11) + pairing(6,h6,12,g12)
g10 = invert(10, sp.cancel(-c18/(8*c0*z**7)), kappa, 12)
c17 = pairing(7,h7,10,g10) + pairing(6,h6,11,g11)
W9  = invert(9, sp.cancel(-c17/(8*c0*z**7)), eta, 12)
g9  = sp.expand(W9 + 3*c1*z**4*h5/(2*c0))

# BRANCH 2 of level 16, plus the level-16 upper gate a4^2 = 4 c0 b8
br2 = {lam: 0, b[0]: a[0]**2/(4*c0), b[1]: a[0]*a[1]/(2*c0), b[8]: a[4]**2/(4*c0)}
c16 = sp.expand((pairing(7,h7,9,g9) + pairing(6,h6,10,g10) + pairing(5,h5,11,g11)).subs(br2))
print("level 16 on branch 2 + upper gate:")
print("   [z^19] carried16 =", sp.simplify(sp.expand(c16).coeff(z,19)), " (upper gate imposed)")
low16 = [sp.factor(sp.simplify(sp.expand(c16).coeff(z,dd))) for dd in range(7)]
F2 = 2*a[0]*a[2] + a[1]**2 - 4*c0*b[2]
print("   C3 = low16[3]; Codex: 33 a0 c1 F2^2/(32 c0^4)")
print("      match:", sp.simplify(low16[3] - 33*a[0]*c1*F2**2/(32*c0**4)) == 0,
      "  (sign-flipped match:", sp.simplify(low16[3] + 33*a[0]*c1*F2**2/(32*c0**4)) == 0, ")")
g8 = sp.expand(invert(8, sp.cancel(-c16/(8*c0*z**7)), mu, 11) + 3*c1*z**4*h4/(2*c0))

c15 = sp.expand(pairing(7,h7,8,g8) + pairing(6,h6,9,g9)
                + pairing(5,h5,10,g10) + pairing(4,h4,11,g11)).subs(br2)
c15 = sp.expand(c15)
print("\nlevel 15:")
print("   deg carried15 =", sp.degree(c15, z), " -> RHS degree", sp.degree(c15,z)-7,
      ", deg W_7 <= 10")
for dd in (19, 18):
    co = sp.factor(sp.simplify(sp.expand(c15).coeff(z, dd)))
    print(f"   UPPER GATE [z^{dd}] carried15 =", str(co)[:200])
F3 = a[0]*a[3] + a[1]*a[2] - 2*c0*b[3]
C = {k: sp.simplify(sp.expand(c15).coeff(z,k)) for k in (3,4,5,6)}
print("\nTASK 1 -- Codex's two linear coefficients on branch 2:")
ck = sp.simplify(sp.expand(C[5]).coeff(kappa))
print("   coefficient of kappa in C5 :", sp.factor(ck))
print("   Codex says -45 a0^3/(16 c0^2)  -> match:",
      sp.simplify(ck + 45*a[0]**3/(16*c0**2)) == 0,
      " | sign-flipped:", sp.simplify(ck - 45*a[0]**3/(16*c0**2)) == 0)
cd = sp.simplify(sp.expand(C[6]).coeff(d[0]))
print("   coefficient of d0 in C6    :", sp.factor(cd))
print("   Codex says 24 c1 F3 / c0^2     -> match:",
      sp.simplify(cd - 24*c1*F3/c0**2) == 0,
      " | sign-flipped:", sp.simplify(cd + 24*c1*F3/c0**2) == 0)
