#!/usr/bin/env python3
"""Levels 10 and 9.

LEVEL 10 gate resolution (done by hand, verified below):
  8 eqs, 6 new unknowns (g2_0..g2_5), rank 5 -> left nullspace dim 3,
  so THREE conditions on the carried parameters.  (The rank defect
  rank[M|v]-rank[M] = 1 counts how far v sits outside col(M) at a generic
  parameter point; it does NOT count the conditions.  Consistency requires
  n.v = 0 for EVERY n in the left nullspace, hence all three.)

    gate 3 :  32 g8_6 (3 g6_4 - g9_8^2)                       = 0
    gate 2 :  8(3 g6_4 g8_7 + 3 g6_5 g8_6
                 - 3 g8_6 g9_8 h5_5 - g8_7 g9_8^2)            = 0
    gate 1 :  linear in h2_2

  gate 3 is a product -> a UNION of two components:
    (A) g8_6 = 0          then gate 2 becomes 8 g8_7 (3 g6_4 - g9_8^2) = 0,
                          splitting again into g8_7 = 0 or 3 g6_4 = g9_8^2.
    (B) 3 g6_4 = g9_8^2   then gate 2 becomes 24 g8_6 (g6_5 - g9_8 h5_5) = 0,
                          so g8_6 = 0 (back to A) or g6_5 = g9_8 h5_5.

  We take the GENERIC component B' = {3 g6_4 = g9_8^2, g6_5 = g9_8 h5_5},
  which leaves g8_6 free -- the largest of the components.  This is a BRANCH
  CHOICE: legitimate for a witness hunt, never for an emptiness claim.
  gate 1 then determines h2_2.
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
    for _ in range(8):
        nxt = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
        if nxt == sub: return
        sub = nxt
    raise RuntimeError("sub did not stabilise")
def res(e):
    for _ in range(20):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("no fixed point")
def gates(L):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    new = [u for u in newsyms(L) if u not in sub]
    if not eqs: return 'sat', [], []
    if not new: return 'pure', eqs, []
    M, v = sp.linear_eq_to_matrix(eqs, new)
    r = M.rank()
    if r == M.row_join(v).rank():
        sol = sp.solve(eqs, new, dict=True)[0]
        sub.update({k: sp.expand(vv) for k, vv in sol.items()}); norm()
        return 'ok', eqs, [len(eqs), len(new), r]
    cs = []
    for n in M.T.nullspace():
        val = sp.cancel(sp.expand((n.T*v)[0,0]))
        if val != 0: cs.append(sp.expand(sp.numer(sp.together(val))))
    return 'gate', eqs, cs

for L in range(19, 10, -1):
    st, eqs, info = gates(L)
    assert st == 'ok', (L, st)
    print(f"L={L:3d}: OK ({info[0]} eqs, {info[1]} new, rank {info[2]}, kernel {info[1]-info[2]})", flush=True)

# ---- LEVEL 10 : impose branch B' then re-solve the level linearly ----
sub.update({S('g6_4'): S('g9_8')**2/3, S('g6_5'): S('g9_8')*S('h5_5')}); norm()
st, eqs, cs = gates(10)
print(f"\nL= 10 after branch B': status={st}, remaining gates={len(cs)}")
for c_ in cs: print("      ", sp.factor(c_))
assert st == 'gate' and len(cs) == 1, "expected exactly the linear h2_2 gate"
sol = sp.solve(cs[0], S('h2_2'), dict=True)
assert len(sol) == 1
sub.update({k: sp.expand(v) for k, v in sol[0].items()}); norm()
print("      h2_2 =", sp.factor(sub[S('h2_2')]))
st, eqs, info = gates(10)
assert st == 'ok', ('L10 still not consistent', st)
print(f"L= 10: OK ({info[0]} eqs, {info[1]} new, rank {info[2]}, kernel {info[1]-info[2]})")
resid = res(lev(10))
print("L= 10 residual identically zero:", sp.expand(resid) == 0)

# ---- LEVEL 9 ----
st, eqs, cs = gates(9)
print(f"\nL=  9: status={st}")
if st == 'ok':
    print(f"L=  9: OK ({info[0]} eqs, ...)" )
elif st == 'gate':
    print(f"       {len(cs)} GATE(S):")
    for i, c_ in enumerate(cs, 1):
        print(f"\n gate {i}: {sp.factor(c_)}")
        print(f"   free syms: {sorted(map(str,c_.free_symbols))}")
else:
    print("       eqs with no new unknowns:", len(eqs))
    for c_ in eqs[:6]: print("      ", sp.factor(c_))
