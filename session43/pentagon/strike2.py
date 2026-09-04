#!/usr/bin/env python3
"""Is level 17's obstruction also a divisibility -- sigma^m | h_6 ?

Level 18 collapsed to sigma^2 | h_7.  Test the same shape at level 17 by
imposing sigma^m | h_6 for m = 0..4 and asking whether the level becomes
consistent (rank test, not sp.solve).
"""
import sympy as sp
s, tau, c0, c1 = sp.symbols('s tau c0 c1')
sg = s - tau
def h_rng(a):
    lo, hi = max(0,-a), min(8, a+2)
    return [i for i in range(lo,hi+1) if 0 <= i+a <= 16]
def g_rng(b):
    return [k for k in range(13)
            if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

def build(m6):
    H, G = {}, {}
    for a in range(-1,9):
        H[a] = sp.expand(sum((sp.Integer(0) if (i+a,i)==(0,0) else sp.Integer(1) if (i+a,i)==(0,1)
                              else sp.Symbol(f'p_{i+a}_{i}'))*s**i for i in h_rng(a)))
    for b in range(-1,13):
        G[b] = sp.expand(sum((sp.Integer(0) if (k+b,k)==(0,0) else sp.Integer(1) if (k+b,k)==(1,2)
                              else sp.Symbol(f'q_{k+b}_{k}'))*s**k for k in g_rng(b)))
    H[8]  = sp.expand(c0*sg**8); G[12] = sp.expand(c1*sg**12)
    # sigma^2 | h_7
    v7 = sorted([x for x in H[7].free_symbols if str(x)[0]=='p'], key=str)
    sol = sp.solve([H[7].subs(s,tau), sp.diff(H[7],s).subs(s,tau)], v7[:2], dict=True)[0]
    H[7] = sp.expand(H[7].subs(sol))
    # sigma^m | h_6
    if m6 > 0:
        v6 = sorted([x for x in H[6].free_symbols if str(x)[0]=='p'], key=str)
        eqs = [sp.diff(H[6], s, d).subs(s, tau) for d in range(m6)]
        sol6 = sp.solve(eqs, v6[:m6], dict=True)
        if not sol6: return None
        H[6] = sp.expand(H[6].subs(sol6[0]))
    return H, G

def lev(L, H, G):
    e = 0
    for a in range(-1,9):
        b = L-a
        if -1 <= b <= 12: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
    return sp.expand(e - (s**2 if L == -2 else 0))

for m6 in range(0, 5):
    HG = build(m6)
    if HG is None: print(f"sigma^{m6} | h_6 : unsatisfiable support"); continue
    H, G = HG
    free = []
    status = None
    for L in (19, 18, 17):
        new = []
        a, b = L-12, L-8
        if -1 <= a <= 8: new += [v for v in H[a].free_symbols if str(v)[0]=='p']
        if -1 <= b <= 12: new += [v for v in G[b].free_symbols if str(v)[0]=='q']
        new = sorted(set(new)-set(free), key=str)
        e = lev(L, H, G)
        eqs = [c for c in (sp.Poly(e,s).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs or not new: status = f"L{L} trivial"; break
        M, v = sp.linear_eq_to_matrix(eqs, new)
        if M.rank() != M.row_join(v).rank():
            status = f"INCONSISTENT at level {L}"; break
        sol = sp.solve(eqs, new, dict=True)
        if not sol: status = f"solve empty at {L}"; break
        sub = {k: sp.expand(val) for k, val in sol[0].items()}
        for k_ in H: H[k_] = sp.expand(H[k_].subs(sub))
        for k_ in G: G[k_] = sp.expand(G[k_].subs(sub))
        free = sorted((set(new)-set(sub)) | set(free), key=str)
        status = f"consistent through level {L}"
    print(f"sigma^{m6} | h_6 : {status}", flush=True)
