#!/usr/bin/env python3
"""EXACT solvability locus of the pentagon's bottom ODE.

The pentagon endgame (trackB1_THEOREM_S_square.md) reduces to ONE criterion on
the weight-4 form S (deg S^ = 4, S^(0) != 0):

    (C4)   [P_8, G] = z^2   for some RATIONAL G,   P_8^ = a S^2.

Univariately  [P_8,G]^ = -2aS(10 S'G + 4 S G'), and with R := S^2 G this is

    (STAR)     2 S R' + S' R = 2 z^2 S ,           R rational,

i.e.  int z^2 sqrt(S) dz  in  C(z)*sqrt(S).

The published table checked 40 RANDOM S per class and found 0/40 for the
non-square classes.  But (STAR) is 7 linear equations in the 4 coefficients of
R, so its solvable locus is cut out by (at most) 3 conditions on the 5
coefficients of S -- a codimension-<=3 CONE, invisible to random sampling.
This script computes that locus EXACTLY.

Symmetries of (STAR):  S -> u S (R fixed);  S(z) -> S(tz), R -> t^-3 R(tz).
So a 2-dimensional cone would be a FINITE list modulo both -- and any
squarefree member is a place where the perfect-square theorem fails and a
pentagon counterexample could live.
"""
import sympy as sp

z = sp.symbols('z')
s = sp.symbols('s0:5')          # S = sum s_k z^k
r = sp.symbols('r0:4')          # R = sum r_j z^j   (deg R = 3 forced)

S = sum(s[k] * z**k for k in range(5))
R = sum(r[j] * z**j for j in range(4))

star = sp.expand(2*S*sp.diff(R, z) + sp.diff(S, z)*R - 2*z**2*S)
coeffs = [sp.expand(star.coeff(z, n)) for n in range(7)]

print("=" * 72)
print("(STAR)  2 S R' + S' R = 2 z^2 S     coefficient equations")
print("=" * 72)
for n, c in enumerate(coeffs):
    print(f"  z^{n}: {c} = 0")

# ---- solve the top four (n = 6,5,4,3) for r3, r2, r1, r0 --------------------
sol = sp.solve(coeffs[3:][::-1], r, dict=True)
assert len(sol) == 1, sol
sol = sol[0]
print("\nSolved (triangular, from the top):")
for j in range(3, -1, -1):
    print(f"  r{j} = {sp.simplify(sol[r[j]])}")

# ---- the three remaining conditions on S ------------------------------------
conds = []
for n in (2, 1, 0):
    c = sp.simplify(sp.together(coeffs[n].subs(sol)))
    c = sp.numer(sp.cancel(c))
    c = sp.factor(sp.expand(c))
    conds.append(c)
    print(f"\nCONDITION from z^{n} (numerator, factored):\n  {c}")

import pickle
with open('/home/user/jacobian_planar/_elliptic_locus_conds.pkl', 'wb') as f:
    pickle.dump({'conds': [sp.srepr(c) for c in conds],
                 'sol': {str(k): sp.srepr(v) for k, v in sol.items()}}, f)
print("\n[saved conditions]")
