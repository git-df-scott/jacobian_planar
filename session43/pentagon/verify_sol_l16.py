#!/usr/bin/env python3
"""INDEPENDENT check of Codex's level-16 branch 1.

His result: level 16 is the JOINT condition  a0^2 - 4 c0 b0 = 0,
a0 a1 - 2 c0 b1 = 0, a0^3 lambda = 0 -- on h_7, h_6 AND the level-19 kernel
constant.  Two branches:
   (1) a0 = 0, b0 = b1 = 0   i.e.  sigma^5 | h_7  and  sigma^2 | h_6
   (2) lambda = 0, with h_6's first two coefficients matching (h_7/sigma^4)^2/(4 c0)

Branch 1 is testable directly with my machinery.  My scans failed because they
varied ONE polynomial at a time: sigma^5 | h_7 alone -> inconsistent, and
sigma^m | h_6 with h_7 at sigma^4 -> inconsistent.  Neither is his branch.
"""
import sympy as sp
s, tau, c0, c1 = sp.symbols('s tau c0 c1')
def h_rng(a):
    lo, hi = max(0,-a), min(8, a+2)
    return [i for i in range(lo,hi+1) if 0 <= i+a <= 16]
def g_rng(b):
    return [k for k in range(13)
            if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
def build(m7, m6):
    H, G = {}, {}
    for a in range(-1,9):
        H[a] = sp.expand(sum((sp.Integer(0) if (i+a,i)==(0,0) else sp.Integer(1) if (i+a,i)==(0,1)
                              else sp.Symbol(f'p_{i+a}_{i}'))*s**i for i in h_rng(a)))
    for b in range(-1,13):
        G[b] = sp.expand(sum((sp.Integer(0) if (k+b,k)==(0,0) else sp.Integer(1) if (k+b,k)==(1,2)
                              else sp.Symbol(f'q_{k+b}_{k}'))*s**k for k in g_rng(b)))
    H[8] = sp.expand(c0*(s-tau)**8); G[12] = sp.expand(c1*(s-tau)**12)
    for a, m in ((7, m7), (6, m6)):
        if m <= 0: continue
        v = sorted([z for z in H[a].free_symbols if str(z)[0]=='p'], key=str)
        if m > len(v): return None
        sol = sp.solve([sp.diff(H[a], s, d).subs(s, tau) for d in range(m)], v[:m], dict=True)
        if not sol: return None
        H[a] = sp.expand(H[a].subs(sol[0]))
    return H, G
def lev(L, H, G):
    e = 0
    for a in range(-1,9):
        b = L-a
        if -1 <= b <= 12: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
    return sp.expand(e)
def run(m7, m6):
    HG = build(m7, m6)
    if HG is None: return "unsatisfiable support"
    H, G = HG; free = []; st = None
    for L in (19, 18, 17, 16):
        new = []
        a, b = L-12, L-8
        if -1 <= a <= 8: new += [v for v in H[a].free_symbols if str(v)[0]=='p']
        if -1 <= b <= 12: new += [v for v in G[b].free_symbols if str(v)[0]=='q']
        new = sorted(set(new)-set(free), key=str)
        e = lev(L, H, G)
        eqs = [c for c in (sp.Poly(e,s).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs or not new: st = f"trivial at {L}"; break
        M, v = sp.linear_eq_to_matrix(eqs, new)
        if M.rank() != M.row_join(v).rank(): st = f"INCONSISTENT at level {L}"; break
        sol = sp.solve(eqs, new, dict=True)
        if not sol: st = f"solve empty at {L}"; break
        sub = {k: sp.expand(val) for k, val in sol[0].items()}
        for k_ in H: H[k_] = sp.expand(H[k_].subs(sub))
        for k_ in G: G[k_] = sp.expand(G[k_].subs(sub))
        free = sorted((set(new)-set(sub)) | set(free), key=str)
        st = f"CONSISTENT through level {L}"
    return st
print("CODEX branch 1: sigma^5 | h_7 AND sigma^2 | h_6")
print("   ->", run(5, 2), flush=True)
print("\ncontrols (each alone, both already known to fail):")
print("   sigma^5|h_7, h_6 free ->", run(5, 0), flush=True)
print("   sigma^4|h_7 & sigma^2|h_6 ->", run(4, 2), flush=True)
