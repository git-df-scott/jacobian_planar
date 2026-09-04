#!/usr/bin/env python3
"""Randomised CE search with depth tracking.

The all-zeros specialisation reached level 7; random ints died at 15.  So the
closing configuration, if any, is near the sparse end.  Search: mostly zeros with
a few nonzero entries, varying tau and the vertex data (a4^2 = 4 c0 b8 enforced).
Records the deepest level reached by each trial.  Anything reaching -2 is a
candidate and gets verified by direct substitution into {P,Q}.
"""
import random, sys
import sympy as sp
z = sp.Symbol('z')
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]

def trial(TAU, A4, B8, density, seed):
    rnd = random.Random(seed)
    def pick(u):
        return sp.Integer(rnd.randrange(-3, 4)) if rnd.random() < density else sp.Integer(0)
    s = z + TAU
    H = {8: z**8, 7: A4*z**8, 6: B8*z**8, -1: sp.expand(s)}
    G = {12: z**12, -1: sp.expand(s**2)}
    SY = []
    for a in range(0, 6):
        cs = [sp.Symbol(f'h{a}_{i}') for i in hsup(a)]; SY += cs
        H[a] = sum(cs[j]*z**i for j, i in enumerate(hsup(a)))
    for b in range(0, 12):
        cs = [sp.Symbol(f'g{b}_{k}') for k in gsup(b)]; SY += cs
        G[b] = sum(cs[j]*z**k for j, k in enumerate(gsup(b)))
    def lev(L):
        e = 0
        for a in range(-1, 9):
            b = L-a
            if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
        return sp.expand(e - (s**2 if L == -2 else 0))
    sub = {}
    def res(e):
        for _ in range(14):
            e2 = sp.expand(e.subs(sub))
            if e2 == e: return e2
            e = e2
        return e
    for L in range(19, -3, -1):
        e = res(lev(L))
        eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs: continue
        unk = sorted({v for v in set().union(*[c.free_symbols for c in eqs]) if v in SY}, key=str)
        if not unk: return L, None
        try: M, v = sp.linear_eq_to_matrix(eqs, unk)
        except Exception: return L, None
        if M.rank() != M.row_join(v).rank(): return L, None
        sol = sp.solve(eqs, unk, dict=True)
        if not sol: return L, None
        sd = dict(sol[0])
        free = [u for u in unk if u not in sd]
        fv = {u: pick(u) for u in free}
        for k in list(sd):
            sd[k] = sp.expand(sd[k].subs(fv)) if hasattr(sd[k], 'subs') else sd[k]
        sd.update(fv); sub.update(sd)
        for _ in range(4):
            sub = {k: (sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
    return -3, (H, G, sub, s)

best = 99; n = 0
from collections import Counter
depth = Counter()
for TAU in (1, 2):
    for (A4, B8) in ((2,1), (4,4), (2,1)):
        for density in (0.0, 0.15, 0.35):
            for seed in range(3):
                n += 1
                L, res_ = trial(sp.Integer(TAU), sp.Integer(A4), sp.Integer(B8), density, seed)
                depth[L] += 1
                if L < best:
                    best = L
                    print(f"  new best: reached level {L}  (tau={TAU}, a4={A4}, b8={B8}, "
                          f"density={density}, seed={seed})", flush=True)
                if res_ is not None:
                    print("  *** REACHED LEVEL -2 -- CANDIDATE ***", flush=True)
                    sys.exit(0)
print(f"\n{n} trials.  depth histogram (level where it died):")
for L in sorted(depth, reverse=True): print(f"   level {L:3d}: {depth[L]}")
print(f"deepest reached: level {best}")
