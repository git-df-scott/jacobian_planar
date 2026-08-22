#!/usr/bin/env python3
"""Levels 10, 9, 8 -- gate resolution to the bottom of the descent.

LEVEL 9 gate resolution (by hand, re-verified by re-deriving the gates after
each imposition rather than trusting the algebra):

  gate 1 : 5(2 g7_9 - 4 g8_9 + 9 h5_5)^2       PERFECT SQUARE -> forced,
           2 g7_9 - 4 g8_9 + 9 h5_5 = 0, a single component, no branch.
  gate 6 : -20 g8_6^2 g9_8                      product -> g8_6 = 0 or g9_8 = 0.
  gate 5 : -8 g8_6 (3 g8_6 h5_5 + 4 g8_7 g9_8)

  On the component that keeps g8_6 free (the one level 10's branch B' already
  preserved), g8_6 != 0 forces from gate 6:   g9_8 = 0
  then gate 5 collapses to -24 g8_6^2 h5_5 :   h5_5 = 0
  then gate 1 gives                            g7_9 = 2 g8_9
  gate 4 is linear in g5_4 with coefficient 24 g8_6 (nonzero here):
                                               g5_4 = g8_6 g9_10 / 2
  gates 2 and 3 are then linear in g5_5 and h1_1 and are solved together.

  This is a BRANCH CHOICE at gate 6 -- fine for a witness hunt, never for an
  emptiness claim.  The other component (g8_6 = 0) is recorded, not explored.
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
    if not eqs: return 'sat', [], [], []
    if not new: return 'pure', eqs, [], []
    M, v = sp.linear_eq_to_matrix(eqs, new)
    r = M.rank()
    if r == M.row_join(v).rank(): return 'ok', eqs, [], [len(eqs), len(new), r]
    cs = []
    for n in M.T.nullspace():
        val = sp.cancel(sp.expand((n.T*v)[0,0]))
        if val != 0: cs.append(sp.expand(sp.numer(sp.together(val))))
    return 'gate', eqs, cs, [len(eqs), len(new), r]
def close(L):
    """solve the level for its new unknowns; asserts consistency first"""
    st, eqs, cs, info = analyse(L)
    assert st == 'ok', (L, st, [str(sp.factor(c)) for c in cs])
    new = [u for u in newsyms(L) if u not in sub]
    sol = sp.solve(eqs, new, dict=True)[0]
    sub.update({k: sp.expand(vv) for k, vv in sol.items()}); norm()
    assert res(lev(L)) == 0, f"L={L} residual not identically zero after solve"
    print(f"L={L:3d}: OK ({info[0]} eqs, {info[1]} new, rank {info[2]}, "
          f"kernel {info[1]-info[2]}), residual 0", flush=True)

for L in range(19, 10, -1): close(L)

# ---------- LEVEL 10 : branch B' ----------
sub.update({S('g6_4'): S('g9_8')**2/3, S('g6_5'): S('g9_8')*S('h5_5')}); norm()
st, eqs, cs, info = analyse(10)
assert st == 'gate' and len(cs) == 1, (st, len(cs))
sol = sp.solve(cs[0], S('h2_2'), dict=True); assert len(sol) == 1
sub.update({k: sp.expand(v) for k, v in sol[0].items()}); norm()
print("\nL= 10 branch B' imposed: g6_4 = g9_8^2/3, g6_5 = g9_8 h5_5, h2_2 fixed")
close(10)

# ---------- LEVEL 9 : the g8_6 != 0 component ----------
sub.update({S('g9_8'): 0, S('h5_5'): 0}); norm()
sub.update({S('g7_9'): 2*S('g8_9')}); norm()
sub.update({S('g5_4'): S('g8_6')*S('g9_10')/2}); norm()
st, eqs, cs, info = analyse(9)
print(f"\nL=  9 after g9_8=0, h5_5=0, g7_9=2g8_9, g5_4=g8_6 g9_10/2: "
      f"status={st}, gates={len(cs)}")
for c_ in cs: print("      ", sp.factor(c_))
if st == 'gate':
    cv = [x for x in (S('g5_5'), S('h1_1')) if any(x in c_.free_symbols for c_ in cs)]
    sol = sp.solve(cs, cv, dict=True)
    print(f"      solving for {[str(x) for x in cv]} -> {len(sol)} solution(s)")
    assert sol, "level 9 gates have no solution in g5_5, h1_1"
    sub.update({k: sp.expand(v) for k, v in sol[0].items()}); norm()
    for k, v in sol[0].items(): print(f"      {k} = {sp.factor(sub[k])}")
close(9)

# ---------- LEVEL 8 ----------
st, eqs, cs, info = analyse(8)
print(f"\nL=  8: status={st}  info={info}")
if st == 'gate':
    print(f"       {len(cs)} GATE(S):")
    for i, c_ in enumerate(cs, 1):
        print(f"\n gate {i}: {sp.factor(c_)}")
        print(f"   free: {sorted(map(str,c_.free_symbols))}")
elif st == 'pure':
    print("       PURE conditions (no new unknowns):", len(eqs))
    for c_ in eqs[:8]: print("      ", sp.factor(c_))
else:
    close(8)
