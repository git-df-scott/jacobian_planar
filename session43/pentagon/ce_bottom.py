#!/usr/bin/env python3
"""Decide the bottom: descend with most free parameters zeroed but a few kept
symbolic, then hand levels 7..-2 to a solver.

Levels 7 down to -2 introduce NO new unknowns (level L's new g is g_{L-8}, and
L=7 gives g_{-1} which is gauge-fixed), so they are pure conditions.  The
all-zeros descent reaches level 7 and dies there.  Keeping a few free parameters
symbolic turns those ten levels into a small polynomial system in exactly those
parameters -- small enough to decide.
"""
import sys, sympy as sp
z = sp.Symbol('z')
KEEP = int(sys.argv[1]) if len(sys.argv) > 1 else 6
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
TAU = sp.Integer(1); s = z + TAU
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
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
sub, kept = {}, []
def res(e):
    for _ in range(14):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    return e
print(f"descending, keeping up to {KEEP} free parameters symbolic:", flush=True)
for L in range(19, 7, -1):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    if not eqs: continue
    # kept symbols ride as PARAMETERS; solving for them too is nonlinear
    unk = sorted({v for v in set().union(*[c.free_symbols for c in eqs])
                  if v in SY and v not in kept}, key=str)
    if not unk:
        bad = [c for c in eqs if sp.simplify(c) != 0]
        print(f"  L={L}: no unknowns, {len(bad)} obstruction(s)", flush=True)
        if bad: sys.exit(0)
        continue
    M, v = sp.linear_eq_to_matrix(eqs, unk)
    if M.rank() != M.row_join(v).rank():
        print(f"  L={L}: INCONSISTENT", flush=True); sys.exit(0)
    sol = sp.solve(eqs, unk, dict=True)[0]
    free = [u for u in unk if u not in sol]
    take = free[:max(0, KEEP-len(kept))]
    zero = {u: sp.Integer(0) for u in free if u not in take}
    kept += take
    sd = {k: sp.expand(vv.subs(zero)) for k, vv in sol.items()}
    sd.update(zero); sd.update({u: u for u in take})
    sub.update(sd)
    for _ in range(4):
        sub = {k: (sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
    print(f"  L={L}: solved, {len(free)} free, keeping {len(take)} symbolic "
          f"(total kept {len(kept)})", flush=True)
print(f"\nkept symbolic: {[str(k) for k in kept]}", flush=True)
eqs = []
for L in range(7, -3, -1):
    e = res(lev(L))
    cs = [sp.expand(c) for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    eqs += cs
    print(f"  level {L}: {len(cs)} conditions", flush=True)
eqs = [c for c in eqs if sp.simplify(c) != 0]
print(f"\nBOTTOM SYSTEM: {len(eqs)} equations in {len(kept)} unknowns", flush=True)
if not kept:
    print("  no unknowns ->", "SATISFIED" if not eqs else "OBSTRUCTED"); sys.exit(0)
sol = sp.solve(eqs, kept, dict=True)
print("  sympy solve ->", "NO SOLUTION (obstructed)" if not sol else f"SOLUTIONS: {sol[:2]}")
