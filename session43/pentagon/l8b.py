#!/usr/bin/env python3
"""Levels 10-8 on the g8_6 = 0 component.

WHY: on the g8_6 != 0 component the descent closes levels 10 and 9 but
level 8 produces gate 7 = -8 g8_6^3, a PURE POWER of g8_6 -- so g8_6 = 0 is
forced unconditionally there and that whole component is empty.  Every
level-9 imposition I made on that component (g9_8 = 0, h5_5 = 0,
g5_4 = g8_6 g9_10/2, ...) was derived from g8_6 != 0 and is therefore VOID.
This script starts over with g8_6 = 0 and re-derives every gate.

With g8_6 = 0 the level-10 gates become
    gate 3 : 32 g8_6 (3 g6_4 - g9_8^2)  -> identically 0
    gate 2 : 8 g8_7 (3 g6_4 - g9_8^2)   -> g8_7 = 0  or  3 g6_4 = g9_8^2
    gate 1 : linear in h2_2
and we take 3 g6_4 = g9_8^2, which keeps g8_7 free (the larger component,
and it no longer forces g6_5 as branch B' did).
"""
import sympy as sp, sys
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
       S('g9_6'):0, S('g9_7'):0, S('g7_7'):S('g8_7')+sp.Rational(3,2)*S('h3_3')}
sub = {k: sp.sympify(v) for k, v in sub.items()}
def norm():
    global sub
    for _ in range(10):
        nxt = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
        if nxt == sub: return
        sub = nxt
    raise RuntimeError("sub did not stabilise")
def res(e):
    for _ in range(24):
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
    assert st == 'ok', (L, st, [str(sp.factor(c)) for c in cs])
    new = [u for u in newsyms(L) if u not in sub]
    sol = sp.solve(eqs, new, dict=True)[0]
    sub.update({k: sp.expand(vv) for k, vv in sol.items()}); norm()
    assert res(lev(L)) == 0, f"L={L} residual not identically zero"
    print(f"L={L:3d}: OK ({info[0]} eqs, {info[1]} new, rank {info[2]}, "
          f"kernel {info[1]-info[2]}), residual 0", flush=True)
def show(L, tag):
    st, eqs, cs, info = analyse(L)
    print(f"\nL={L:3d} [{tag}]: status={st} info={info} gates={len(cs)}")
    for i, c_ in enumerate(cs, 1):
        print(f"  gate {i}: {sp.factor(c_)}")
        print(f"     free: {sorted(map(str,c_.free_symbols))}")
    return st, eqs, cs

sub.update({S('g8_6'): 0}); norm()
for L in range(19, 10, -1): close(L)
sub.update({S('g6_4'): S('g9_8')**2/3}); norm()
show(10, "g8_6=0, 3g6_4=g9_8^2")
st, eqs, cs = show(10, "recheck")
assert st == 'gate' and len(cs) == 1
sol = sp.solve(cs[0], S('h2_2'), dict=True); assert len(sol) == 1
sub.update({k: sp.expand(v) for k, v in sol[0].items()}); norm()
print("      h2_2 fixed")
close(10)
show(9, "g8_6=0 component")

# ---- LEVEL 9 on g8_6 = 0 :
#   gate 1 : 5(2 g7_9 - 4 g8_9 + 9 h5_5)^2   PERFECT SQUARE -> forced
#   gate 4 : -4 g8_7^2 g9_8                  -> g8_7 = 0 or g9_8 = 0
#   take g9_8 = 0 (keeps g8_7 free, the larger component); then
#   gate 3 : 4(12 g5_4 g8_7 + 12 g6_5 g7_6 - 9 g8_7^2 h5_5) linear in g5_4
#   gate 2 : linear in h1_1
sub.update({S('h5_5'): (4*S('g8_9') - 2*S('g7_9'))/9, S('g9_8'): 0}); norm()
st, eqs, cs = show(9, "g9_8=0, gate1 imposed")
assert st == 'gate'
cv = [x for x in (S('g5_4'), S('h1_1')) if any(x in c_.free_symbols for c_ in cs)]
sol = sp.solve(cs, cv, dict=True)
assert sol, "level 9 gates unsolvable in g5_4, h1_1"
print(f"      {len(sol)} solution(s) in {[str(x) for x in cv]}")
sub.update({k: sp.expand(v) for k, v in sol[0].items()}); norm()
for k in cv: print(f"      {k} = {sp.factor(sub[k])}")
close(9)
show(8, "g8_6=0, g9_8=0 component")
