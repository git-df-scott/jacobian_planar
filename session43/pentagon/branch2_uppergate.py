#!/usr/bin/env python3
"""DIRECT ATTACK: does Codex's branch 2 also fail the level-16 UPPER gate?

Branch 1 fails it ([z^19] carried16 = 27/4 on his witness).  If branch 2 fails it
too, then level 16 is EMPTY, and since level 16 is NECESSARY, **(72,108) is
EMPTY** -- the last degree pair below 125.

Branch 2 (Codex, CODEX-012):  lambda = 0,  b0 = a0^2/(4c0),  b1 = a0 a1/(2c0).

Built with HIS conventions exactly (pairing, invert_diagonal, h7 = z^4 sum a_i z^i)
so that any disagreement is not a convention mismatch.
"""
import sympy as sp
z = sp.Symbol('z')
c0, c1 = sp.symbols('c0 c1', nonzero=True)
lam, kappa, eta = sp.symbols('lambda kappa eta')
a = sp.symbols('a0:5'); b = sp.symbols('b0:9'); d = sp.symbols('d0:8')
def pairing(wf, f, wg, g): return sp.expand(wg*sp.diff(f,z)*g - wf*f*sp.diff(g,z))
def D(w, f): return sp.expand(w*f - z*sp.diff(f,z))
def invert(w, rhs, ker):
    ans = ker*z**w
    for (deg,), co in sp.Poly(rhs, z).terms():
        if deg != w: ans += co*z**deg/(w-deg)
    ans = sp.expand(ans)
    assert sp.simplify(D(w, ans) - rhs) == 0
    return ans

h7 = z**4*sum(a[i]*z**i for i in range(5))
h6 = sum(b[i]*z**i for i in range(9))
h5 = sum(d[i]*z**i for i in range(8))
g12 = c1*z**12
g11 = 3*c1*z**4*h7/(2*c0) + lam*z**11/(8*c0)

carried18 = pairing(7,h7,11,g11) + pairing(6,h6,12,g12)
rhs10 = sp.cancel(-carried18/(8*c0*z**7))
assert sp.expand(rhs10).coeff(z,10) == 0
g10 = invert(10, rhs10, kappa)
carried17 = pairing(7,h7,10,g10) + pairing(6,h6,11,g11)
rhs9 = sp.cancel(-carried17/(8*c0*z**7))
assert sp.expand(rhs9).coeff(z,9) == 0
W9 = invert(9, rhs9, eta)
g9 = sp.expand(W9 + 3*c1*z**4*h5/(2*c0))
carried16 = sp.expand(pairing(7,h7,9,g9) + pairing(6,h6,10,g10) + pairing(5,h5,11,g11))

print("CONTROL: reproduce Codex's lower gates at level 16")
F0 = a[0]**2 - 4*c0*b[0]; F1 = a[0]*a[1] - 2*c0*b[1]
low = [sp.factor(sp.expand(carried16).coeff(z, dd)) for dd in range(7)]
print("   low[0:3] all zero:", all(sp.simplify(x) == 0 for x in low[:3]))
print("   low[3] + 9 c1 F0^2/(4c0^3) = ", sp.simplify(low[3] + 9*c1*F0**2/(4*c0**3)))
print("   low[4] + 33 c1 F0 F1/(4c0^3) =", sp.simplify(low[4] + 33*c1*F0*F1/(4*c0**3)))

print("\nUPPER gate at level 16:  deg W_8 <= 11, RHS degree 12")
top = sp.factor(sp.simplify(sp.expand(carried16).coeff(z, 19)))
print("   [z^19] carried16 =", top)

print("\n--- on BRANCH 2:  lambda = 0, b0 = a0^2/(4c0), b1 = a0 a1/(2c0) ---")
br2 = {lam: 0, b[0]: a[0]**2/(4*c0), b[1]: a[0]*a[1]/(2*c0)}
top2 = sp.factor(sp.simplify(sp.expand(top.subs(br2))))
print("   [z^19] carried16 | branch2 =", top2)
print("   identically zero on branch 2?", sp.simplify(top2) == 0)
if sp.simplify(top2) != 0:
    print("\n   -> branch 2 must ALSO satisfy this as an extra condition.")
    print("      free symbols:", sorted([str(s_) for s_ in top2.free_symbols]))

print("\n--- on BRANCH 1:  a0 = 0, b0 = b1 = 0 ---")
br1 = {a[0]: 0, b[0]: 0, b[1]: 0}
top1 = sp.factor(sp.simplify(sp.expand(top.subs(br1))))
print("   [z^19] carried16 | branch1 =", top1)
print("   identically zero on branch 1?", sp.simplify(top1) == 0)
