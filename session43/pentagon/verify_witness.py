#!/usr/bin/env python3
"""Verify Codex's explicit branch-1 witness (commit 2ba8e30) in MY s-ladder.

His witness: c0 = c1 = lambda = 1, a_4 = b_8 = d_7 = 1, all other coefficients
and both earlier kernel constants zero, i.e. with z = s - tau:

    h_8 = z^8 ,  g_12 = z^12 ,  h_7 = z^8 ,  h_6 = z^8 ,  h_5 = z^7
    g_11 = (3/2) z^4 h_7 + (1/8) z^11

Claim: levels 19, 18, 17, 16 all vanish, with g_10, g_9, g_8 reconstructed
coefficientwise.  A witness is immune to solver case-splitting -- exactly what I
said would settle branch 1 -- so this is the decisive test of my retracted
disagreement.

Ladder:  sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = 0   for L >= -1
(derivative d/ds = d/dz, so the whole check can be done in z).
"""
import sympy as sp
z = sp.Symbol('z')
H = {8: z**8, 7: z**8, 6: z**8, 5: z**7}
G = {12: z**12, 11: sp.Rational(3,2)*z**4*H[7] + sp.Rational(1,8)*z**11}
print("witness inputs:")
for k in sorted(H, reverse=True): print(f"   h_{k} = {sp.expand(H[k])}")
for k in sorted(G, reverse=True): print(f"   g_{k} = {sp.expand(G[k])}")

def lev(L, H, G):
    e = 0
    for a in sorted(H):
        b = L - a
        if b in G: e += b*sp.diff(H[a], z)*G[b] - a*H[a]*sp.diff(G[b], z)
    return sp.expand(e)

print(f"\nlevel 19 (must vanish with the given g_11): {sp.expand(lev(19,H,G))}")
ok19 = sp.expand(lev(19,H,G)) == 0
print("   ->", "PASS" if ok19 else "FAIL")

# reconstruct g_10, g_9, g_8 by solving each level; h_4 free
for L, b in ((18, 10), (17, 9), (16, 8)):
    deg = min(12, b+3)
    cs = [sp.Symbol(f'g{b}_{i}') for i in range(deg+1)]
    G[b] = sum(cs[i]*z**i for i in range(deg+1))
    if L == 16:
        h4 = [sp.Symbol(f'h4_{i}') for i in range(0, 7)]
        H[4] = sum(h4[i]*z**i for i in range(7))
        unk = cs + h4
    else:
        unk = cs
    e = lev(L, H, G)
    eqs = [c for c in sp.Poly(e, z).all_coeffs() if c != 0]
    M, v = sp.linear_eq_to_matrix(eqs, unk)
    rM, rA = M.rank(), M.row_join(v).rank()
    print(f"\nlevel {L}: {len(eqs)} eqs, {len(unk)} unknowns, rank {rM} vs aug {rA}"
          f" -> {'SOLVABLE' if rM == rA else 'INCONSISTENT'}")
    if rM != rA:
        print("   witness FAILS here"); break
    sol = sp.solve(eqs, unk, dict=True)[0]
    G[b] = sp.expand(G[b].subs(sol))
    if L == 16: H[4] = sp.expand(H[4].subs(sol))
    resid = sp.expand(lev(L, H, G))
    free = sorted([u for u in unk if u not in sol], key=str)
    print(f"   residual after substitution: {resid}  ({'PASS' if resid == 0 else 'FAIL'})")
    print(f"   g_{b} = {G[b]}")
    print(f"   free kernel constants retained: {free}")
