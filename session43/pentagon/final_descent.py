#!/usr/bin/env python3
"""FINAL DESCENT: levels 19 -> 8, gates extracted by nullspace, never by solving
the full nonlinear carried system.

Discipline (per the task spec):
  * level L introduces ONLY h_{L-12} and g_{L-8}; everything else is CARRIED.
  * solve the level linearly for the NEW unknowns only -- carried parameters ride
    in the coefficients, so including them is nonlinear and is the wrong move.
  * a rank defect is NOT failure: extract the nullspace obstruction, factor it,
    and impose it as a GATE on the carried parameters.
  * never specialise carried kernel parameters early.
"""
import sympy as sp, sys
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0, 6):
    H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0, 12):
    G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
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
sub = {}
def res(e):
    for _ in range(16):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    return e
GATES = []
for L in range(19, 7, -1):
    for attempt in range(8):
        e = res(lev(L))
        eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
        if not eqs:
            print(f"L={L:3d}: satisfied", flush=True); break
        new = [u for u in newsyms(L) if u not in sub]
        if not new:
            bad = [c for c in eqs if sp.expand(c) != 0]
            print(f"L={L:3d}: no new unknowns, {len(bad)} PURE condition(s)", flush=True)
            if bad: print("      ", str(sp.factor(bad[0]))[:200], flush=True)
            break
        M, v = sp.linear_eq_to_matrix(eqs, new)
        rM, rA = M.rank(), M.row_join(v).rank()
        if rM == rA:
            sol = sp.solve(eqs, new, dict=True)[0]
            sub.update({k: sp.expand(vv) for k, vv in sol.items()})
            for _ in range(5):
                sub = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
            print(f"L={L:3d}: OK  ({len(eqs)} eqs, {len(new)} new, rank {rM}, "
                  f"kernel {len(new)-rM})", flush=True)
            break
        conds = []
        for n in M.T.nullspace():
            val = sp.cancel(sp.expand((n.T*v)[0,0]))
            if val != 0: conds.append(sp.expand(sp.numer(sp.together(val))))
        if not conds: print(f"L={L:3d}: rank defect but no condition -- investigate", flush=True); break
        for c_ in conds:
            print(f"L={L:3d}: GATE (attempt {attempt}) -> {str(sp.factor(c_))[:180]}", flush=True)
        GATES.append((L, [sp.factor(c_) for c_ in conds]))
        # solve for the union of ALL the conditions' symbols, not just the first
        cv = sorted(set().union(*[c_.free_symbols for c_ in conds]), key=str)
        cs = sp.solve(conds, cv, dict=True)
        if not cs:
            print(f"      GENUINE OBSTRUCTION at level {L}: unsatisfiable in "
                  f"{[str(x) for x in cv]}", flush=True)
            sys.exit(0)
        if len(cs) > 1:
            print(f"      NOTE: {len(cs)} components; taking the first. A product-form"
                  f" gate is a BRANCH CHOICE -- fine for a witness hunt, never for"
                  f" an emptiness claim.", flush=True)
        sub.update({k: sp.expand(vv) for k, vv in cs[0].items()})
        for _ in range(5):
            sub = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
        print(f"      imposing {cs[0]}", flush=True)
print("\nGATES FOUND:", flush=True)
for L, g_ in GATES: print(f"   L={L}: {str(g_)[:150]}", flush=True)
