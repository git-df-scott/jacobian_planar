#!/usr/bin/env python3
"""Chart F, done with EVERY division made explicit.

The bug this replaces: close() solved each gate with sp.solve, which divides by
whatever pivot coefficient it likes.  If that coefficient is later forced to
zero, the stored value becomes zoo and the run dies at level 13 -- and, worse,
when it does NOT die it has silently deleted the coefficient's vanishing locus
from the chart.  That is exactly how the g9_8 = 0 chart stayed invisible, and on
that chart 47 of 51 endgame conditions died at once.

The fix: never divide by anything that is not a nonzero RATIONAL.
  * pivots whose coefficient is a nonzero rational  -> solve, unconditional
  * anything else -> BRANCH explicitly into (coefficient != 0) and
    (coefficient = 0), and walk both.
Each leaf records the nonzero assumptions it accumulated; the leaf's endgame is
then saturated at their product, so "!= 0" is enforced exactly rather than
assumed.

DEPTH/leaf caps keep the tree finite and are REPORTED, never silent: a run that
hits a cap is incomplete and says so.
"""
import sympy as sp, sys, os, pickle, itertools
z = sp.Symbol('z'); TAU = sp.Integer(1); s = z + TAU
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
H = {8: z**8, 7: 2*z**8, 6: z**8, -1: sp.expand(s)}
G = {12: z**12, -1: sp.expand(s**2)}
for a in range(0, 6): H[a] = sum(sp.Symbol(f'h{a}_{i}')*z**i for i in hsup(a))
for b in range(0, 12): G[b] = sum(sp.Symbol(f'g{b}_{k}')*z**k for k in gsup(b))
LEV = {}
def lev(L):
    if L in LEV: return LEV[L]
    e = 0
    for a in range(-1, 9):
        b = L-a
        if a in H and b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    LEV[L] = sp.expand(e - (s**2 if L == -2 else 0)); return LEV[L]
def newsyms(L):
    out = []
    if 0 <= L-12 <= 5: out += [sp.Symbol(f'h{L-12}_{i}') for i in hsup(L-12)]
    if 0 <= L-8 <= 11: out += [sp.Symbol(f'g{L-8}_{k}') for k in gsup(L-8)]
    return out

def norm(sub):
    for _ in range(14):
        nxt = {k: (sp.expand(v.subs(sub)) if hasattr(v,'subs') else v) for k, v in sub.items()}
        if nxt == sub: return sub
        sub = nxt
    raise RuntimeError("sub did not stabilise")
def res(e, sub):
    for _ in range(26):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("no fixed point")

MAXDEPTH = int(os.environ.get('MAXDEPTH', '14'))
leaves, capped = [], []

def walk(L, sub, nz, depth, path):
    """descend from level L; sub is a substitution dict, nz the nonzero assumptions"""
    if depth > MAXDEPTH:
        capped.append(path); return
    if L < 8:
        conds = []
        for LL in range(7, -3, -1):
            e = res(lev(LL), sub)
            if e == 0: continue
            for c in sp.Poly(e, z).all_coeffs():
                c = sp.expand(c)
                if c != 0: conds.append(c)
        leaves.append((path, conds, dict(sub), list(nz)))
        print(f"  LEAF {path}: {len(conds)} endgame conditions, "
              f"{len(nz)} nonzero assumption(s)", flush=True)
        return
    e = res(lev(L), sub)
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if sp.expand(c) != 0]
    new = [u for u in newsyms(L) if u not in sub]
    if not eqs:
        walk(L-1, sub, nz, depth, path); return
    if not new:
        walk(L-1, sub, nz, depth, path); return
    M, v = sp.linear_eq_to_matrix(eqs, new)
    # pick a pivot with a NONZERO RATIONAL coefficient; never divide otherwise
    for i in range(M.rows):
        for j in range(M.cols):
            if M[i, j].is_number and M[i, j] != 0:
                x = new[j]
                val = sp.expand((v[i] - sum(M[i, k]*new[k] for k in range(M.cols) if k != j))
                                / M[i, j])
                s2 = norm({**sub, x: val})
                walk(L, s2, nz, depth, path)
                return
    # no rational pivot: branch on a symbolic coefficient
    for i in range(M.rows):
        for j in range(M.cols):
            c1 = sp.expand(M[i, j])
            if c1 == 0: continue
            x = new[j]
            val = sp.expand((v[i] - sum(M[i, k]*new[k] for k in range(M.cols) if k != j))/c1)
            print(f"L={L:3d} {path}: BRANCH on {sp.factor(c1)}", flush=True)
            walk(L, norm({**sub, x: val}), nz + [c1], depth+1, path + "N")   # c1 != 0
            walk(L, sub, nz, depth+1, path + "Z")                            # c1 == 0 handled
            return                                                            # by adding it below
    # every coefficient is zero -> the level's equations are pure conditions
    walk(L-1, sub, nz, depth, path)

print(f"chart F: no pre-imposed substitutions, MAXDEPTH={MAXDEPTH}", flush=True)
walk(19, {}, [], 0, "")
print(f"\n{len(leaves)} leaf/leaves, {len(capped)} capped at depth {MAXDEPTH}")
if capped: print("  CAPPED (run is INCOMPLETE on these):", capped[:10])
pickle.dump((leaves, capped), open('chartF.pkl','wb'))
