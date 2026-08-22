#!/usr/bin/env python3
"""The pentagon on the witness, with NO symbolic division anywhere.

Every earlier run solved each level with sp.solve, which divides by whatever
pivot it likes.  Two things go wrong.  Loudly: if that pivot is later forced to
zero, stored values become zoo and the run dies (levels 13 and 8 both did).
Quietly, and far worse: dividing by a quantity DELETES that quantity's
vanishing locus from the chart.  That is how the g9_8 = 0 chart stayed hidden,
and on it 47 of 51 endgame conditions died at once.  Any verdict obtained that
way is conditional on assumptions nobody wrote down.

This removes the problem instead of managing it.  At each level, eliminate new
unknowns by Gaussian elimination using ONLY pivots that are nonzero RATIONAL
numbers.  Those divisions are unconditional and delete nothing.  Any row with no
rational pivot is not solved at all -- it is simply carried out as a condition.
Levels 7 down to -2 contribute all their coefficients as conditions too.

The result is ONE polynomial system whose variety is exactly the pentagon on
this witness: no charts, no branch choices, no saturation, no inherited
assumptions such as g8_6 = g8_7 = 0.  It is larger than any single chart, which
is the price of not assuming anything.
"""
import sympy as sp, pickle, sys
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
    if 0 <= L-12 <= 5: out += [sp.Symbol(f'h{L-12}_{i}') for i in hsup(L-12)]
    if 0 <= L-8 <= 11: out += [sp.Symbol(f'g{L-8}_{k}') for k in gsup(L-8)]
    return out
sub, conds = {}, []
USES = {}          # symbol -> set of sub keys whose stored value mentions it
def setsub(x, val):
    """record x = val and push it into ONLY the stored values that mention x.

    The naive version re-expanded every entry of sub after every pivot; sub
    reaches ~150 entries with large values, so that is quadratic and the run
    produced no output at all in nine minutes.  A reverse index makes each
    update touch only what actually changes."""
    for k in list(USES.get(x, ())):
        if k not in sub: continue
        nv = sp.expand(sub[k].subs(x, val))
        sub[k] = nv
        for y in nv.free_symbols: USES.setdefault(y, set()).add(k)
    USES.pop(x, None)
    sub[x] = val
    for y in val.free_symbols: USES.setdefault(y, set()).add(x)
def norm(): pass
def res(e):
    for _ in range(26):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("no fixed point")
for L in range(19, -3, -1):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if sp.expand(c) != 0]
    if not eqs:
        print(f"L={L:3d}: satisfied", flush=True); continue
    new = [u for u in newsyms(L) if u not in sub]
    solved = 0
    changed = True
    while changed and new:
        changed = False
        for idx, c in enumerate(eqs):
            P = {x: sp.Poly(c, x) for x in new if x in c.free_symbols}
            for x, Px in P.items():
                if Px.degree() != 1: continue
                c1 = Px.coeff_monomial(x)
                if not (c1.is_number and c1 != 0): continue     # RATIONAL PIVOTS ONLY
                val = sp.expand(-Px.coeff_monomial(1)/c1)
                assert not val.has(sp.zoo) and not val.has(sp.nan), f"L={L} degenerate"
                setsub(x, val)
                new.remove(x); solved += 1
                eqs = [q for k, q in enumerate(eqs) if k != idx]
                eqs = [sp.expand(q.subs(sub)) for q in eqs]
                eqs = [q for q in eqs if sp.expand(q) != 0]
                changed = True; break
            if changed: break
    left = [sp.expand(q) for q in eqs if sp.expand(q) != 0]
    conds += left
    print(f"L={L:3d}: {solved} solved on rational pivots, {len(left)} condition(s) carried out, "
          f"{len(new)} new unknown(s) left free", flush=True)
V = sorted(set().union(*[c.free_symbols for c in conds]), key=str) if conds else []
print(f"\nTOTAL {len(conds)} conditions in {len(V)} variables")
pickle.dump((conds, sub), open('nodivide.pkl','wb'))
print("saved nodivide.pkl", flush=True)
