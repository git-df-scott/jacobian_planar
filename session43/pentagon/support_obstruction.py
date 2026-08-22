#!/usr/bin/env python3
"""The level-16 disagreement resolved: a SUPPORT obstruction, not an arithmetic slip.

Codex's verifier gates level 16 on the LOW coefficients -- z^7 | carried16 -- and
then inverts D_8 coefficientwise.  `invert_diagonal` will happily return a W_8 of
whatever degree the right-hand side demands.  But W_8 is not free:

    W_8 = g_8 - (3 c1 / 2 c0) z^4 h_4 ,
    deg g_8 <= 11   (its coefficients are q_{k+8,k}, k in 0..11, since
                     Q_ok(k+8,k) needs 2k-3 <= k+8, i.e. k <= 11)
    deg h_4 <= 6    (its coefficients are p_{i+4,i}, i in 0..6, since
                     i <= min(8,(i+4)//2+1) gives i <= 6)
    => deg(z^4 h_4) <= 10 ,  so  **deg W_8 <= 11**

and D_8 preserves degree, so `D_8(W_8)` has degree <= 11 too.  Meanwhile

    RHS = -carried16 / (8 c0 z^7)

and carried16 reaches degree 19, so the RHS reaches degree 12.  **A degree-12
right-hand side is outside the image of D_8 on the admissible support.**

So level 16 carries an obstruction at the TOP as well as the bottom:

    [z^19] carried16 = 0 ,

which is exactly the 27/4 I reported in OPUS43-023.
"""
import sympy as sp
z = sp.Symbol('z')
c0, c1 = sp.symbols('c0 c1', nonzero=True)
def pairing(wf, f, wg, g): return sp.expand(wg*sp.diff(f,z)*g - wf*f*sp.diff(g,z))

# support bounds, derived from the Newton polygons
def g_deg(b):
    return max(k for k in range(13)
               if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k)
def h_deg(a):
    return max(i for i in range(9)
               if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1))
print("support degree bounds from the Newton polygons:")
for b in (12,11,10,9,8): print(f"   deg g_{b} <= {g_deg(b)}")
for a in (8,7,6,5,4):    print(f"   deg h_{a} <= {h_deg(a)}")
print(f"\n   deg W_8 = deg(g_8 - (3c1/2c0) z^4 h_4) <= max({g_deg(8)}, 4+{h_deg(4)}) = "
      f"{max(g_deg(8), 4+h_deg(4))}")

# Codex's witness
h7 = z**8; h6 = z**8; h5 = z**7
g12 = c1*z**12
g11 = 3*c1*z**4*h7/(2*c0) + 0
def D(w, f): return sp.expand(w*f - z*sp.diff(f, z))
def invert(w, rhs, ker):
    ans = ker*z**w
    for (d,), co in sp.Poly(rhs, z).terms():
        if d != w: ans += co*z**d/(w-d)
    ans = sp.expand(ans)
    assert sp.simplify(D(w, ans) - rhs) == 0
    return ans
carried18 = pairing(7,h7,11,g11) + pairing(6,h6,12,g12)
g10 = invert(10, sp.cancel(-carried18/(8*c0*z**7)), 0)
carried17 = pairing(7,h7,10,g10) + pairing(6,h6,11,g11)
W9 = invert(9, sp.cancel(-carried17/(8*c0*z**7)), 0)
g9 = sp.expand(W9 + 3*c1*z**4*h5/(2*c0))
carried16 = sp.expand(pairing(7,h7,9,g9) + pairing(6,h6,10,g10) + pairing(5,h5,11,g11))
print(f"\nwith c0 = c1 = 1 substituted:")
sub = {c0: 1, c1: 1}
print(f"   deg carried16 = {sp.degree(sp.expand(carried16.subs(sub)), z)}")
print(f"   [z^19] carried16 = {sp.expand(carried16.subs(sub)).coeff(z,19)}")
rhs8 = sp.cancel(-carried16/(8*c0*z**7))
print(f"   deg RHS for D_8 = {sp.degree(sp.expand(rhs8.subs(sub)), z)}   (must be <= 11)")
W8 = invert(8, sp.expand(rhs8.subs(sub)), 0)
print(f"   deg W_8 produced by coefficientwise inversion = {sp.degree(W8, z)}"
      f"   -> {'OUTSIDE the support' if sp.degree(W8,z) > 11 else 'inside'}")
print(f"   its z^12 coefficient = {sp.expand(W8).coeff(z,12)}")
print("\nCONCLUSION: level 16 needs [z^19] carried16 = 0 as an UPPER-end gate,")
print("in addition to Codex's lower gate z^7 | carried16.  His verifier tests")
print("only the lower gate, so the witness passes there and fails here.")
