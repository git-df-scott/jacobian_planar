#!/usr/bin/env python3
"""BREAKTHROUGH 2: the BOTTOM of the v-cascade -- 9 levels of pure conditions.

Going down, v-level V introduces F_{V-2} and G_{V-1}.  F exists for d >= -8 and
G for e >= -12, so:
    V = 4 .. -6   both new
    V = -7 .. -11 only G new
    V = -12 .. -20  NOTHING new  ->  PURE CONDITIONS (9 levels)

The very bottom levels involve only the top-left corner of both polygons and are
tiny -- V = -20 is a single equation.  These are conditions no attack so far has
used: the w-cascade's bottom involves different variables entirely.
"""
import sympy as sp
r = sp.Symbol('r')
def P_ok(j,i): return 0<=i<=8 and 0<=j<=16 and max(0,j-8)<=i<=min(8,j//2+1)
def Q_ok(j,k):
    if not (0<=k<=12): return False
    lo=(k+1)//2 if k<=2 else 2*k-3
    return lo<=j<=12+k
def Fd(d):
    t=0
    for i in range(9):
        j=2*i-d
        if j>=0 and P_ok(j,i):
            t+=(sp.Integer(0) if (j,i)==(0,0) else sp.Integer(1) if (j,i)==(0,1)
                else sp.Symbol(f'p_{j}_{i}'))*r**i
    return sp.expand(t)
def Ge(e):
    t=0
    for k in range(13):
        j=2*k-e
        if j>=0 and Q_ok(j,k):
            t+=(sp.Integer(0) if (j,k)==(0,0) else sp.Integer(1) if (j,k)==(1,2)
                else sp.Symbol(f'q_{j}_{k}'))*r**k
    return sp.expand(t)
F={d:Fd(d) for d in range(-8,3)}
G={e:Ge(e) for e in range(-12,4)}
def lev(V):
    out=0
    for d in range(-8,3):
        e=V+1-d
        if -12<=e<=3: out += d*F[d]*sp.diff(G[e],r) - e*sp.diff(F[d],r)*G[e]
    return sp.expand(out - (r**2 if V==4 else 0))
print("bottom of the v-cascade (no new unknowns at these levels):\n")
allc=[]
for V in range(-20,-11):
    e=lev(V)
    cs=[c for c in (sp.Poly(e,r).all_coeffs() if e!=0 else []) if c!=0]
    print(f"V = {V}:  {len(cs)} condition(s)")
    for c in cs: print("     ", sp.factor(c))
    allc+=cs
print(f"\nTOTAL {len(allc)} pure conditions from the v-cascade bottom")
vs=sorted(set().union(*[c.free_symbols for c in allc]),key=str) if allc else []
print(f"involving {len(vs)} variables: {[str(v) for v in vs]}")
