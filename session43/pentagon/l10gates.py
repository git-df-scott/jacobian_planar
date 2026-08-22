#!/usr/bin/env python3
"""Level 10: re-derive the gates from scratch and resolve them by hand.

Loads every gate established at levels 19..11, re-runs the descent, and at
level 10 prints (a) the equations, (b) the new unknowns, (c) the rank defect
and (d) the nullspace gates in FACTORED form so the branch structure is
visible.  Nothing is solved automatically -- the branching is a human call
because a product-form gate is a UNION of components and picking one is only
legitimate for a witness hunt.
"""
import sympy as sp
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
def res(e):
    for _ in range(20):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("no fixed point")
for L in range(19, 10, -1):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    if not eqs:
        print(f"L={L:3d}: satisfied", flush=True); continue
    new = [u for u in newsyms(L) if u not in sub]
    M, v = sp.linear_eq_to_matrix(eqs, new)
    assert M.rank() == M.row_join(v).rank(), f"L={L} unexpected rank defect"
    sol = sp.solve(eqs, new, dict=True)[0]
    sub.update({k: sp.expand(vv) for k, vv in sol.items()})
    for _ in range(6):
        sub = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
    print(f"L={L:3d}: OK ({len(eqs)} eqs, {len(new)} new, rank {M.rank()}, kernel {len(new)-M.rank()})", flush=True)

L = 10
e = res(lev(L))
eqs = [c for c in sp.Poly(e, z).all_coeffs() if c != 0]
new = [u for u in newsyms(L) if u not in sub]
M, v = sp.linear_eq_to_matrix(eqs, new)
r, ra = M.rank(), M.row_join(v).rank()
print(f"\nL= 10: {len(eqs)} eqs, {len(new)} new unknowns {[str(x) for x in new]}")
print(f"       rank(M)={r}  rank([M|v])={ra}  defect={ra-r}  kernel={len(new)-r}")
conds = []
for n in M.T.nullspace():
    val = sp.cancel(sp.expand((n.T*v)[0,0]))
    if val != 0: conds.append(sp.expand(sp.numer(sp.together(val))))
print(f"\n{len(conds)} GATE(S), factored:")
for i, c_ in enumerate(conds, 1):
    print(f"\n gate {i}: {sp.factor(c_)}")
    print(f"   free syms: {sorted(map(str,c_.free_symbols))}")
