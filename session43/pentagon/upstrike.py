#!/usr/bin/env python3
"""BOTTOM-UP strike on the s-ladder -- the mirror of the downward descent.

Level L:  sum_{a+b=L} [ b h_a' g_b - a h_a g_b' ] = delta_{L,-2} s^2

Going UP, the new pieces at level L are h_{L+1} and g_{L+1}; they meet the
gauge-fixed partners g_{-1} = s^2 and h_{-1} = s, so the level is LINEAR in them:

    -s^2 h_{L+1}' - 2(L+1) s h_{L+1} + (L+1) g_{L+1} + s g_{L+1}' = -C_L

Low levels have tiny polynomials (deg h_0 = 2, deg g_0 = 3), so this is cheap.
Whatever it forces must agree with the top-down descent; they meet in the middle.

Consistency by RANK.  Free parameters kept SYMBOLIC (A3).
"""
import sympy as sp
s = sp.Symbol('s')
def hdeg(a): return min(8, a+2)
def gdeg(b): return min(12, b+3)
def hlo(a):  return max(0, -a)
def glo(b):
    return min([k for k in range(13)
                if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k] or [0])

H, G, FREE = {}, {}, []
for a in range(-1, 9):
    lo, hi = hlo(a), hdeg(a)
    cs = [sp.Symbol(f'p_{i+a}_{i}') for i in range(lo, hi+1)]
    H[a] = sp.expand(sum((sp.Integer(0) if (i+a,i)==(0,0) else sp.Integer(1) if (i+a,i)==(0,1)
                          else cs[i-lo])*s**i for i in range(lo, hi+1)))
for b in range(-1, 13):
    ks = [k for k in range(13)
          if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
    G[b] = sp.expand(sum((sp.Integer(0) if (k+b,k)==(0,0) else sp.Integer(1) if (k+b,k)==(1,2)
                          else sp.Symbol(f'q_{k+b}_{k}'))*s**k for k in ks))
def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if -1 <= b <= 12: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
    return sp.expand(e - (s**2 if L == -2 else 0))

print("CONTROL: level -2 == s^2 :", sp.simplify(lev(-2)) == 0, flush=True)
free, sub = [], {}
for L in range(-1, 13):
    new = []
    for a in (L+1,):
        if -1 <= a <= 8: new += [v for v in H[a].free_symbols if str(v)[0]=='p']
    for b in (L+1,):
        if -1 <= b <= 12: new += [v for v in G[b].free_symbols if str(v)[0]=='q']
    new = sorted(set(new)-set(free), key=str)
    e = lev(L)
    eqs = [c for c in (sp.Poly(e,s).all_coeffs() if e != 0 else []) if c != 0]
    if not eqs:
        print(f"level {L:3d}: identically satisfied", flush=True); continue
    if not new:
        print(f"level {L:3d}: {len(eqs)} eqs, NO new unknowns -> PURE CONDITIONS", flush=True)
        break
    try:
        M, v = sp.linear_eq_to_matrix(eqs, new)
    except Exception as ex:
        print(f"level {L:3d}: NOT linear in the new unknowns ({ex}) -- stop", flush=True); break
    rM, rA = M.rank(), M.row_join(v).rank()
    print(f"level {L:3d}: {len(eqs):2d} eqs, {len(new):2d} new, {len(free):2d} carried, "
          f"rank {rM}, kernel {len(new)-rM} -> {'CONSISTENT' if rM==rA else 'CONDITIONS'}",
          flush=True)
    if rM != rA:
        for n in M.T.nullspace()[:2]:
            val = sp.simplify(sp.expand((n.T*v)[0,0]))
            if val != 0: print("       COND:", sp.factor(val), flush=True)
        break
    sol = sp.solve(eqs, new, dict=True)
    if not sol: print("       !! solve empty", flush=True); break
    sb = {k: sp.expand(val) for k, val in sol[0].items()}
    z = [str(k) for k,val in sb.items() if val == 0]
    if z: print(f"       forced to ZERO: {z}", flush=True)
    for a in H: H[a] = sp.expand(H[a].subs(sb))
    for b in G: G[b] = sp.expand(G[b].subs(sb))
    free = sorted((set(new)-set(sb)) | set(free), key=str)
