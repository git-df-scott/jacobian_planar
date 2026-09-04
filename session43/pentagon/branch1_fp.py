#!/usr/bin/env python3
"""Settle the branch-1 disagreement with exact F_p linear algebra.

My sympy test says Codex's branch 1 (sigma^5|h_7, sigma^2|h_6) is INCONSISTENT at
level 16; he derived it as valid.  My prime suspect is my own sp.solve taking
sol[0] at level 17, which can case-split on exactly the locus a0 = 0 defining his
branch.  This test uses NO solver: only rank over F_p.

Method.  Sample random numeric h_7 with sigma^5 | h_7 and h_6 with sigma^2 | h_6,
random nonzero c0, c1, tau.  Then:
  level 19 -> linear in g_11        : solve, RETAIN the kernel
  level 18 -> linear in g_10        : solve, RETAIN the kernel
  level 17 -> linear in (h_5, g_9) + carried kernels : solve, RETAIN
  level 16 -> linear in (h_4, g_8) + ALL carried kernels : RANK TEST
Carrying every kernel is the A3 discipline and is exactly what Codex's W_9
warning is about.
"""
import random, sys
import sympy as sp
p = 1000003
s = sp.Symbol('s')

def h_rng(a):
    lo, hi = max(0,-a), min(8, a+2)
    return [i for i in range(lo,hi+1) if 0 <= i+a <= 16]
def g_rng(b):
    return [k for k in range(13)
            if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

def trial(seed, verbose=False):
    rnd = random.Random(seed)
    R = lambda: sp.Integer(rnd.randrange(1, p))
    c0, c1, tau = R(), R(), R()
    sg = s - tau
    H, G = {}, {}
    H[8] = sp.expand(c0*sg**8); G[12] = sp.expand(c1*sg**12)
    # branch 1: sigma^5 | h_7 (deg 8 -> 3 free), sigma^2 | h_6 (deg 8 -> 6 free)
    H[7] = sp.expand(sg**5*sum(R()*s**i for i in range(0, 4)))
    H[6] = sp.expand(sg**2*sum(R()*s**i for i in range(0, 7)))
    syms = []
    def unkpoly(name, rng):
        cs = [sp.Symbol(f'{name}{i}') for i in rng]
        syms.extend(cs)
        return sp.expand(sum(cs[j]*s**i for j, i in enumerate(rng)))
    for a in (5, 4): H[a] = unkpoly(f'h{a}_', h_rng(a))
    for b in (11, 10, 9, 8): G[b] = unkpoly(f'g{b}_', g_rng(b))
    def lev(L):
        e = 0
        for a in range(-1, 9):
            b = L-a
            if a in H and b in G: e += b*sp.diff(H[a],s)*G[b] - a*H[a]*sp.diff(G[b],s)
        return sp.expand(e)
    carried, sub = [], {}
    for L, newsyms in ((19, [v for v in syms if str(v).startswith('g11_')]),
                       (18, [v for v in syms if str(v).startswith('g10_')]),
                       (17, [v for v in syms if str(v).startswith(('h5_','g9_'))])):
        e = sp.expand(lev(L).subs(sub))
        eqs = [c for c in sp.Poly(e, s).all_coeffs() if c != 0]
        unk = newsyms + carried
        if not eqs: continue
        M, v = sp.linear_eq_to_matrix(eqs, unk)
        Mp = sp.Matrix(M).applyfunc(lambda z: sp.Integer(int(z) % p))
        vp = sp.Matrix(v).applyfunc(lambda z: sp.Integer(int(z) % p))
        A = Mp.row_join(vp)
        rM = Mp.rank(iszerofunc=lambda z: int(z) % p == 0)
        rA = A.rank(iszerofunc=lambda z: int(z) % p == 0)
        if rM != rA:
            return f"INCONSISTENT at level {L}"
        sol = sp.solve(eqs, unk, dict=True)
        if not sol: return f"solve empty at {L}"
        sub.update({k: sp.expand(val) for k, val in sol[0].items()})
        carried = sorted((set(unk) - set(sol[0])) | set(carried), key=str)
        if verbose: print(f"   level {L}: rank {rM}/{len(unk)}, carried {len(carried)}")
    e = sp.expand(lev(16).subs(sub))
    eqs = [c for c in sp.Poly(e, s).all_coeffs() if c != 0]
    unk = [v for v in syms if str(v).startswith(('h4_','g8_'))] + carried
    M, v = sp.linear_eq_to_matrix(eqs, unk)
    Mp = sp.Matrix(M).applyfunc(lambda z: sp.Integer(int(z) % p))
    vp = sp.Matrix(v).applyfunc(lambda z: sp.Integer(int(z) % p))
    z = lambda w: int(w) % p == 0
    rM = Mp.rank(iszerofunc=z); rA = Mp.row_join(vp).rank(iszerofunc=z)
    if verbose: print(f"   level 16: {len(eqs)} eqs, {len(unk)} unk, rank {rM} vs {rA}")
    return "CONSISTENT through level 16" if rM == rA else "INCONSISTENT at level 16"

print("branch 1 (sigma^5|h_7, sigma^2|h_6), exact F_p rank, kernels retained:", flush=True)
for seed in (1, 2, 3):
    print(f"  seed {seed}: {trial(seed, verbose=(seed==1))}", flush=True)
