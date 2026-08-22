#!/usr/bin/env python3
"""Descend the s-ladder.  ONE variable.

    sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} s^2
    h_a(s) = sum_i p_{i+a,i} s^i ,  g_b(s) = sum_k q_{k+b,k} s^k

Supports straight from the Newton polygons.  Top: h_8 = c0 (s-tau)^8,
g_12 = c1 (s-tau)^12 (the eighth-power theorem).
At level L the new unknowns are h_{L-12} and g_{L-8}; each meets a determined
partner, so the level is LINEAR in them.  Carried free parameters are kept
SYMBOLIC (A3) and consistency is decided by RANK (A14/A16).
"""
import sympy as sp
s, tau, c0, c1 = sp.symbols('s tau c0 c1')

def h_range(a):                      # P: i in [max(0,-a), min(8, a+2)], j=i+a<=16
    lo, hi = max(0, -a), min(8, a+2)
    return [i for i in range(lo, hi+1) if 0 <= i+a <= 16]
def g_range(b):                      # Q: k, j=k+b in [qlo(k), 12+k]
    out = []
    for k in range(0, 13):
        j = k+b
        lo = (k+1)//2 if k <= 2 else 2*k-3
        if j >= 0 and lo <= j <= 12+k: out.append(k)
    return out

H, G, sym = {}, {}, {}
for a in range(-1, 9):
    t = 0
    for i in h_range(a):
        j = i+a
        c = sp.Integer(0) if (j,i)==(0,0) else sp.Integer(1) if (j,i)==(0,1) else sp.Symbol(f'p_{j}_{i}')
        t += c*s**i
    H[a] = sp.expand(t)
for b in range(-1, 13):
    t = 0
    for k in g_range(b):
        j = k+b
        c = sp.Integer(0) if (j,k)==(0,0) else sp.Integer(1) if (j,k)==(1,2) else sp.Symbol(f'q_{j}_{k}')
        t += c*s**k
    G[b] = sp.expand(t)

def lev(L, H, G):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if -1 <= b <= 12:
            e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
    return sp.expand(e)

print("CONTROL A: level -2 == s^2 :", sp.simplify(lev(-2,H,G) - s**2) == 0, flush=True)
print("supports: deg h_a =", {a: sp.degree(H[a],s) if H[a]!=0 else None for a in range(8,-2,-1)}, flush=True)
print("          deg g_b =", {b: sp.degree(G[b],s) if G[b]!=0 else None for b in range(12,-2,-1)}, flush=True)

H[8]  = sp.expand(c0*(s-tau)**8)
G[12] = sp.expand(c1*(s-tau)**12)
print("\nCONTROL B: level 20 with the eighth-power family:",
      sp.simplify(lev(20,H,G)) == 0, flush=True)

free = []
for L in range(19, -2, -1):
    new = []
    for a in (L-12,):
        if -1 <= a <= 8: new += [v for v in H[a].free_symbols if str(v).startswith('p_')]
    for b in (L-8,):
        if -1 <= b <= 12: new += [v for v in G[b].free_symbols if str(v).startswith('q_')]
    new = sorted(set(new) - set(free), key=str)
    e = sp.expand(lev(L, H, G))
    eqs = sp.Poly(e, s).all_coeffs() if e != 0 else []
    eqs = [c for c in eqs if c != 0]
    if not eqs:
        print(f"level {L:3d}: identically satisfied", flush=True); continue
    if not new:
        print(f"level {L:3d}: {len(eqs)} eqs, NO new unknowns -> PURE CONDITIONS", flush=True)
        for c in eqs[:2]: print("       COND:", sp.factor(c), flush=True)
        break
    M, v = sp.linear_eq_to_matrix(eqs, new)
    rM, rA = M.rank(), M.row_join(v).rank()
    print(f"level {L:3d}: {len(eqs):2d} eqs, {len(new):2d} new ({len(free)} carried), "
          f"rank {rM}, kernel {len(new)-rM} -> {'CONSISTENT' if rM==rA else 'CONDITIONS'}",
          flush=True)
    if rM != rA:
        for n in M.T.nullspace():
            val = sp.simplify(sp.expand((n.T*v)[0,0]))
            if val != 0: print("       COND:", sp.factor(val), flush=True)
        break
    sol = sp.solve(eqs, new, dict=True)
    if not sol: print("       !! rank consistent but solve empty", flush=True); break
    sub = {k: sp.expand(val) for k, val in sol[0].items()}
    for a in H: H[a] = sp.expand(H[a].subs(sub))
    for b in G: G[b] = sp.expand(G[b].subs(sub))
    free = sorted((set(new)-set(sub)) | set(free), key=str)
    assert sp.simplify(lev(L,H,G)) == 0, f"level {L} re-check FAILED"
