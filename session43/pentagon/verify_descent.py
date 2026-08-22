#!/usr/bin/env python3
"""RIGOROUS verification of the descent state before trusting levels 10 and 9.

Rank equality is NOT the same as the level vanishing.  This rebuilds everything
and asserts, at each level, that the residual is IDENTICALLY ZERO after
substitution.  It also re-derives the ladder identity and the supports from
first principles rather than reusing them.
"""
import sympy as sp
x, y, z = sp.symbols('x y z')
TAU = sp.Integer(1); s = z + TAU

# ---- CHECK 1: the ladder identity itself, from the bracket ------------------
def br(f, g): return sp.expand(sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x))
ok = True
for a in range(-1, 4):
    for b in range(-1, 4):
        F, Gf = sp.Function('F'), sp.Function('G')
        lhs = sp.simplify(br(y**a*F(x*y), y**b*Gf(x*y)))
        S_ = sp.Symbol('S')
        rhs = sp.simplify((y**(a+b)*(b*sp.diff(F(S_),S_)*Gf(S_) - a*F(S_)*sp.diff(Gf(S_),S_))
                           ).subs(S_, x*y))
        if sp.simplify(lhs-rhs) != 0: ok = False
print("CHECK 1  ladder identity {y^a F(s), y^b G(s)} = y^(a+b)(b F'G - a F G'):",
      "PASS" if ok else "FAIL")

# ---- CHECK 2: supports, re-derived from the Newton polygons ----------------
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
import sys; sys.path.insert(0, 'session43/pentagon')
from pentev import PR
ok2 = all(sorted(hsup(a)) == sorted([j-a for j,(lo,hi) in PR.items() if lo <= j-a <= hi])
          for a in range(-1, 9))
print("CHECK 2  h-supports vs the original wave1 P_rows:", "PASS" if ok2 else "FAIL")
print("         h_{-1} support:", hsup(-1), " g_{-1} support:", gsup(-1),
      "  (the two gauge-fixed vertices)")

# ---- CHECK 3: the starting point is a legitimate branch-1 point -------------
a4, b8, c0 = 2, 1, 1
print(f"CHECK 3  level-16 upper gate a4^2 = 4 c0 b8 : {a4**2} = {4*c0*b8} ->",
      "PASS" if a4**2 == 4*c0*b8 else "FAIL")
print("         branch 1 needs a0 = 0 and b0 = b1 = 0; our h_7 = 2z^8 and")
print("         h_6 = z^8 have ALL lower coefficients zero, so both hold.")
print("         NOTE this is ONE POINT of branch 1, not the generic branch.")

# ---- CHECK 4: rebuild the descent and assert each residual is exactly 0 -----
H = {8: z**8, 7: sp.Integer(a4)*z**8, 6: sp.Integer(b8)*z**8, -1: sp.expand(s)}
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
sub = {S('g11_11'):sp.Integer(0), S('g9_4'):sp.Integer(0), S('g9_5'):sp.Integer(0),
       S('g9_11'):sp.Integer(0), S('g10_10'):sp.Integer(0),
       S('g9_9'):sp.Rational(3,2)*S('h5_5'), S('g8_4'):sp.Integer(0), S('g8_5'):sp.Integer(0),
       S('g8_10'):2*S('g9_10'), S('g7_4'):sp.Integer(0), S('g7_5'):sp.Integer(0),
       S('g9_6'):sp.Integer(0), S('g9_7'):sp.Integer(0),
       S('g7_7'):S('g8_7')+sp.Rational(3,2)*S('h3_3')}
def res(e):
    for _ in range(20):
        e2 = sp.expand(e.subs(sub))
        if e2 == e: return e2
        e = e2
    raise RuntimeError("substitution did not reach a fixed point")
print("\nCHECK 4  residual is IDENTICALLY ZERO at each solved level:")
for L in range(19, 10, -1):
    e = res(lev(L))
    eqs = [c for c in (sp.Poly(e, z).all_coeffs() if e != 0 else []) if c != 0]
    if eqs:
        new = [u for u in newsyms(L) if u not in sub]
        M, v = sp.linear_eq_to_matrix(eqs, new)
        assert M.rank() == M.row_join(v).rank(), f"L={L} inconsistent"
        sol = sp.solve(eqs, new, dict=True)[0]
        sub.update({k: sp.expand(vv) for k, vv in sol.items()})
        for _ in range(6):
            sub = {k:(sp.expand(vv.subs(sub)) if hasattr(vv,'subs') else vv) for k,vv in sub.items()}
    r = sp.expand(res(lev(L)))
    print(f"   L={L:3d}: residual {'ZERO  PASS' if r == 0 else 'NONZERO  ** FAIL **'}",
          flush=True)
    if r != 0: print("        ", str(r)[:200]); break
print("\n   support check on every solved piece (must stay inside its polygon slot):")
bad = 0
for a in range(0, 6):
    p = sp.expand(res(H[a]))
    if p != 0 and sp.degree(p, z) > max(hsup(a)): bad += 1; print(f"      h_{a} DEGREE VIOLATION")
for b in range(0, 12):
    p = sp.expand(res(G[b]))
    if p != 0 and sp.degree(p, z) > max(gsup(b)): bad += 1; print(f"      g_{b} DEGREE VIOLATION")
print(f"      {'PASS -- all pieces within support' if bad == 0 else f'{bad} VIOLATIONS'}")
