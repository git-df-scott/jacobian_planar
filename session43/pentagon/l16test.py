#!/usr/bin/env python3
"""TOP-DOWN strike, levels 16 -> 13, with the VERIFIED sigma^4 | h_7 imposed.

My half of the OPUS43-017 split (Codex takes bottom-up 9 -> 12).
Original header follows.

INDEPENDENT verification of Codex CODEX-011:

    level 17 is completely solvable  <=>  (s - tau)^4 | h_7 .

My own five hypotheses sigma^m | h_6 (m = 0..4) all left level 17 inconsistent.
Codex's claim says why: the obstruction is a FURTHER condition on h_7, not a
condition on h_6 at all.  Tested here from my own s-ladder, not his code.
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

def build(m7):
    H, G = {}, {}
    for a in range(-1,9):
        H[a] = sp.expand(sum((sp.Integer(0) if (i+a,i)==(0,0) else sp.Integer(1) if (i+a,i)==(0,1)
                              else sp.Symbol(f'p_{i+a}_{i}'))*s**i for i in h_rng(a)))
    for b in range(-1,13):
        G[b] = sp.expand(sum((sp.Integer(0) if (k+b,k)==(0,0) else sp.Integer(1) if (k+b,k)==(1,2)
                              else sp.Symbol(f'q_{k+b}_{k}'))*s**k for k in g_rng(b)))
    H[8] = sp.expand(c0*sg**8); G[12] = sp.expand(c1*sg**12)
    if m7:
        v7 = sorted([x for x in H[7].free_symbols if str(x)[0]=='p'], key=str)
        eqs = [sp.diff(H[7], s, d).subs(s, tau) for d in range(m7)]
        sol = sp.solve(eqs, v7[:m7], dict=True)
        if not sol: return None
        H[7] = sp.expand(H[7].subs(sol[0]))
        for d in range(m7):
            assert sp.simplify(sp.diff(H[7], s, d).subs(s, tau)) == 0
    return H, G

def lev(L, H, G):
    e = 0
    for a in range(-1,9):
        b = L-a
        if -1 <= b <= 12: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
    return sp.expand(e)

for m7 in (5, 6, 7, 8):
    HG = build(m7)
    if HG is None: print(f"sigma^{m7} | h_7 : unsatisfiable"); continue
    H, G = HG
    free, status = [], None
    for L in (19, 18, 17, 16):
        new = []
        a, b = L-12, L-8
        if -1 <= a <= 8: new += [v for v in H[a].free_symbols if str(v)[0]=='p']
        if -1 <= b <= 12: new += [v for v in G[b].free_symbols if str(v)[0]=='q']
        new = sorted(set(new)-set(free), key=str)
        e = lev(L, H, G)
        eqs = [c for c in (sp.Poly(e,s).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs or not new: status = f"trivial at {L}"; break
        M, v = sp.linear_eq_to_matrix(eqs, new)
        if M.rank() != M.row_join(v).rank():
            status = f"INCONSISTENT at level {L}"; break
        sol = sp.solve(eqs, new, dict=True)
        if not sol: status = f"solve empty at {L}"; break
        sub = {k: sp.expand(val) for k, val in sol[0].items()}
        for k_ in H: H[k_] = sp.expand(H[k_].subs(sub))
        for k_ in G: G[k_] = sp.expand(G[k_].subs(sub))
        free = sorted((set(new)-set(sub)) | set(free), key=str)
        status = f"CONSISTENT through level {L}"
    print(f"sigma^{m7} | h_7 : {status}", flush=True)
