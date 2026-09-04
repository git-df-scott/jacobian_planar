#!/usr/bin/env python3
"""THE ENDGAME: levels 7 down to -2.

Structure discovered: newsyms(L) is empty for L <= 7, because h stops at
h_{-1} (needs L-12 >= -1, i.e. L >= 11 for new h, and the last new h is h_0 at
L = 12... more precisely L-12 in [-1,5] and L-8 in [0,11] both fail for L < 8).
So levels 20..8 introduce every unknown and CLOSE, and levels 7, 6, ..., -2 are
TEN levels of pure polynomial conditions on the surviving carried parameters.
That system is the whole remaining content of the pentagon on this component.

Strategy: collect all conditions from all ten levels at once, then repeatedly
  (a) drop conditions that are identically zero,
  (b) find a condition that is a pure power of a single variable -> forced,
  (c) find a condition linear in some variable that appears in no denominator
      -> solve and back-substitute,
  (d) otherwise report the irreducible core.
Never specialise a carried parameter that is not forced.
"""
import sympy as sp, sys, itertools
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
       S('g9_6'):0, S('g9_7'):0, S('g7_7'):S('g8_7')+sp.Rational(3,2)*S('h3_3'),
       S('g8_6'):0, S('g8_7'):0, S('g9_8'):0}
sub = {k: sp.sympify(v) for k, v in sub.items()}
def norm():
    global sub
    for _ in range(12):
        nxt = {k:(sp.cancel(sp.expand(vv.subs(sub))) if hasattr(vv,'subs') else vv)
               for k,vv in sub.items()}
        if nxt == sub: return
        sub = nxt
    raise RuntimeError("sub did not stabilise")
def res(e):
    for _ in range(26):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("no fixed point")
def analyse(L):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    new = [u for u in newsyms(L) if u not in sub]
    if not eqs: return 'sat', [], [], [0,len(new),0]
    if not new: return 'pure', eqs, [], [len(eqs),0,0]
    M, v = sp.linear_eq_to_matrix(eqs, new)
    r = M.rank()
    if r == M.row_join(v).rank(): return 'ok', eqs, [], [len(eqs), len(new), r]
    cs = []
    for n in M.T.nullspace():
        val = sp.cancel(sp.expand((n.T*v)[0,0]))
        if val != 0: cs.append(sp.expand(sp.numer(sp.together(val))))
    return 'gate', eqs, cs, [len(eqs), len(new), r]
def close(L):
    st, eqs, cs, info = analyse(L)
    for _round in range(8):
        if st != 'gate': break
        cv = sorted(set().union(*[c_.free_symbols for c_ in cs]), key=str)
        lin = [x for x in cv if all(sp.degree(sp.Poly(c_, x), x) <= 1 for c_ in cs)]
        sol = sp.solve(cs, lin or cv, dict=True)
        assert sol, f"L={L} gates unsolvable: {[str(sp.factor(c)) for c in cs]}"
        if len(sol) > 1:
            print(f"L={L:3d}: {len(sol)} components -> taking first (BRANCH CHOICE)", flush=True)
        sub.update({k: sp.cancel(sp.expand(v)) for k, v in sol[0].items()}); norm()
        print(f"L={L:3d}: {len(cs)} gate(s) -> imposed {sorted(map(str,sol[0]))}", flush=True)
        st, eqs, cs, info = analyse(L)
    assert st == 'ok', (L, st, [str(sp.factor(c)) for c in cs])
    new = [u for u in newsyms(L) if u not in sub]
    sol = sp.solve(eqs, new, dict=True)[0]
    sub.update({k: sp.cancel(sp.expand(vv)) for k, vv in sol.items()}); norm()
    assert res(lev(L)) == 0, f"L={L} residual not identically zero"
    print(f"L={L:3d}: OK ({info[0]} eqs, {info[1]} new, rank {info[2]}, "
          f"kernel {info[1]-info[2]}), residual 0", flush=True)
for L in range(19, 7, -1): close(L)

print("\n=== ENDGAME: levels 7 .. -2 (no new unknowns) ===", flush=True)
conds = []
for L in range(7, -3, -1):
    st, eqs, cs, info = analyse(L)
    nz = [sp.expand(sp.numer(sp.together(c))) for c in eqs]
    nz = [c for c in nz if sp.simplify(c) != 0]
    print(f"L={L:3d}: {len(nz)} nontrivial condition(s)", flush=True)
    conds += nz
free = sorted(set().union(*[c.free_symbols for c in conds]), key=str)
print(f"\nTOTAL {len(conds)} conditions in {len(free)} parameters: {[str(x) for x in free]}",
      flush=True)
import pickle
pickle.dump((conds, sub), open('endgame_g98zero.pkl','wb'))
print("saved endgame_g98zero.pkl", flush=True)
