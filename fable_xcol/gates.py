"""Rung-by-rung with CANONICAL gate extraction (left nullspace) + denominator ledger.
Start from the exact d=19 closed form: a8 = al*W^2, b12 = be*W^3, W=y^7(y-r)."""
import sympy as sp
from sympy import Rational as R
y=sp.Symbol('y'); al,be,r=sp.symbols('alpha beta r')
NP=[(0,0),(1,0),(8,14),(8,16),(0,8)]; NQ=[(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+R(y2-y1,x2-x1)*(i-x1))
        lo[i]=int(sp.ceiling(min(pts))); hi[i]=int(sp.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12); loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
W=y**7*(y-r)
a={i:sum(sp.Symbol(f'a{i}_{j}')*y**j for j in range(loP[i],hiP[i]+1)) for i in range(9)}
b={k:sum(sp.Symbol(f'b{k}_{j}')*y**j for j in range(loQ[k],hiQ[k]+1)) for k in range(13)}
a[8]=sp.expand(al*W**2); b[12]=sp.expand(be*W**3)
def rung(d,sub):
    e=0
    for i in range(9):
        k=d+1-i
        if 0<=k<=12: e+= i*a[i]*sp.diff(b[k],y)-k*sp.diff(a[i],y)*b[k]
    e=sp.expand(sp.expand(e).subs(sub)-(1 if d==2 else 0))
    return [] if e==0 else [c for c in sp.Poly(e,y).all_coeffs() if c!=0]
sub={}; report=[]
for d in [18,17,16]:
    new=[]
    i0,k0=d-11,d-7
    if 0<=i0<=8: new+=[sp.Symbol(f'a{i0}_{j}') for j in range(loP[i0],hiP[i0]+1)]
    if 0<=k0<=12: new+=[sp.Symbol(f'b{k0}_{j}') for j in range(loQ[k0],hiQ[k0]+1)]
    cs=rung(d,sub)
    M=sp.zeros(len(cs),len(new)); v=sp.zeros(len(cs),1)
    for ii,c in enumerate(cs):
        p=sp.expand(c)
        for jj,nv in enumerate(new): M[ii,jj]=sp.expand(sp.diff(p,nv))
        v[ii,0]=sp.expand(p.subs({nv:0 for nv in new}))
    rk=M.rank(); ns=M.T.nullspace()
    gset=[sp.factor(sp.expand((n.T*v)[0,0])) for n in ns]
    gset=[g for g in gset if g!=0]
    print(f"\nd={d}: {len(cs)} eqs, {len(new)} new, rank {rk}, left-nullspace dim {len(ns)}")
    print(f"   GATES ({len(gset)}):")
    for g in gset[:6]: print("      ",g)
    report.append((d,len(cs),len(new),rk,gset))
    if gset: break
    s=sp.solve(cs,new,dict=True)
    if s: sub.update({k_:sp.simplify(v_) for k_,v_ in s[0].items()})
import pickle; pickle.dump(report,open('gates.pkl','wb'))
