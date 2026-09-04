#!/usr/bin/env python3
"""Push the descent to levels 10, 9, 8 with every gate found so far hard-coded.

Gates established by nullspace extraction (final_descent.py):
    L15 : g11_11 = 0                       (the lambda = 0 collapse)
    L14 : g10_10 = 64 g9_11^2/15 , g9_4 = g9_5 = 0
    L13 : g9_11 = 0 , g9_9 = 3 h5_5/2 , g8_4 = g8_5 = 0   (so g10_10 = 0)
    L12 : g8_10 = 2 g9_10 , g7_4 = g7_5 = 0
    L11 : solved by hand from the seven gates --
            -4 g9_6^3          -> g9_6 = 0
            -2*(2 g9_7^3)      -> g9_7 = 0  (after g9_6 = 0)
            the remaining four vanish identically once g9_6 = g9_7 = 0
            -35(2g7_7 - 2g8_7 + 2g9_7 - 3h3_3) -> g7_7 = g8_7 + 3 h3_3/2
"""
import sympy as sp, sys
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0, 6): H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0, 12): G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
def lev(L):
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return sp.expand(e - (s**2 if L == -2 else 0))
def newsyms(L):
    out = []
    if -1 <= L-12 <= 5: out += [sp.Symbol(f'h{L-12}_{i}') for i in hsup(L-12)]
    if 0 <= L-8 <= 11:  out += [sp.Symbol(f'g{L-8}_{k}') for k in gsup(L-8)]
    return out
S = sp.Symbol
sub = {S('g11_11'):0, S('g9_4'):0, S('g9_5'):0, S('g9_11'):0, S('g10_10'):0,
       S('g9_9'):sp.Rational(3,2)*S('h5_5'), S('g8_4'):0, S('g8_5'):0,
       S('g8_10'):2*S('g9_10'), S('g7_4'):0, S('g7_5'):0,
       S('g9_6'):0, S('g9_7'):0, S('g7_7'):S('g8_7')+sp.Rational(3,2)*S('h3_3')}
sub = {k: sp.sympify(v) for k, v in sub.items()}
def res(e):
    for _ in range(16):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    return e
for L in range(19, 7, -1):
    for attempt in range(10):
        e = res(lev(L))
        eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs: print(f"L={L:3d}: satisfied", flush=True); break
        new = [u for u in newsyms(L) if u not in sub]
        if not new:
            bad = [c for c in eqs if sp.expand(c) != 0]
            print(f"L={L:3d}: no new unknowns, {len(bad)} PURE condition(s)", flush=True)
            for c in bad[:2]: print("      ", str(sp.factor(c))[:170], flush=True)
            break
        M, v = sp.linear_eq_to_matrix(eqs, new)
        if M.rank() == M.row_join(v).rank():
            sol = sp.solve(eqs, new, dict=True)[0]
            sub.update({k: sp.expand(vv) for k, vv in sol.items()})
            for _ in range(5):
                sub = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
            print(f"L={L:3d}: OK  ({len(eqs)} eqs, {len(new)} new, rank {M.rank()}, "
                  f"kernel {len(new)-M.rank()})", flush=True)
            break
        conds = []
        for n in M.T.nullspace():
            val = sp.cancel(sp.expand((n.T*v)[0,0]))
            if val != 0: conds.append(sp.expand(sp.numer(sp.together(val))))
        print(f"L={L:3d}: {len(conds)} GATE(S):", flush=True)
        for c_ in conds[:6]: print("      ", str(sp.factor(c_))[:170], flush=True)
        cv = sorted(set().union(*[c_.free_symbols for c_ in conds]), key=str)
        cs = sp.solve(conds, cv, dict=True)
        if not cs:
            print(f"      NO SOLUTION in {[str(x) for x in cv][:8]} -> genuine obstruction",
                  flush=True); sys.exit(0)
        if len(cs) > 1: print(f"      {len(cs)} components; taking first (branch choice)", flush=True)
        sub.update({k: sp.expand(vv) for k, vv in cs[0].items()})
        for _ in range(5):
            sub = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
        print(f"      imposing {cs[0]}", flush=True)
