"""SUB-CASE (2), BOTTOM-UP LADDER.  Exact, from the hulls, no assumptions.

Facts used (all proved):
  a_0 = b_0 = 0            (hull meets x=0 only at the origin + additive gauge)
  a_1(0) != 0              (the Newton vertex (1,0))
Rungs are solved from d = 0 upward, imposing each result before the next.
"""
import sympy as sp, math
from fractions import Fraction as F
y=sp.Symbol('y')
NP=[(0,0),(1,0),(8,14),(8,16)]; NQ=[(0,0),(2,1),(12,21),(12,24)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+F(y2-y1,x2-x1)*(i-x1))
        if not pts: lo[i]=hi[i]=None; continue
        lo[i]=int(math.ceil(min(pts))); hi[i]=int(math.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12)
loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
def rg(lo,hi): return [] if lo is None or lo>hi else list(range(lo,hi+1))
a={i:sum(sp.Symbol(f'a{i}_{j}')*y**j for j in rg(loP[i],hiP[i])) for i in range(9)}
b={k:sum(sp.Symbol(f'b{k}_{j}')*y**j for j in rg(loQ[k],hiQ[k])) for k in range(13)}
A10=sp.Symbol('a1_0')
def rung(d,sub):
    e=0
    for i in range(9):
        k=d+1-i
        if 0<=k<=12: e+= i*a[i]*sp.diff(b[k],y)-k*sp.diff(a[i],y)*b[k]
    e=sp.expand(sp.expand(e).xreplace(sub)-(1 if d==2 else 0))
    return [] if e==0 else [c for c in sp.Poly(e,y).all_coeffs() if c!=0]
def newvars(d):
    """unknowns entering at rung d from the BOTTOM: a_{d+1}, b_{d+1} roughly"""
    out=[]
    for i in range(9):
        k=d+1-i
        if 0<=k<=12:
            out+=[sp.Symbol(f'a{i}_{j}') for j in rg(loP[i],hiP[i])]
            out+=[sp.Symbol(f'b{k}_{j}') for j in rg(loQ[k],hiQ[k])]
    return sorted(set(out),key=str)
sub={}
print("supports: a_1 on y^%s..%s , b_1 on y^%s..%s , b_2 on y^%s..%s"%(
      loP[1],hiP[1],loQ[1],hiQ[1],loQ[2],hiQ[2]))
for d in range(0,7):
    cs=rung(d,sub)
    if not cs:
        print(f"\nd={d}: VACUOUS"); continue
    nv=[v for v in newvars(d) if v not in sub]
    sol=sp.solve(cs,nv,dict=True)
    print(f"\nd={d}: {len(cs)} equations, {len(nv)} unknowns -> {len(sol)} branch(es)")
    if not sol:
        print("   NO SOLUTION -> conditions on carried parameters (extract gates)"); break
    # prefer the branch that keeps a1_0 != 0
    good=[s for s in sol if s.get(A10,A10)!=0]
    s0=good[0] if good else sol[0]
    for k_,v_ in s0.items(): sub[k_]=sp.simplify(v_)
    sub={k_:sp.simplify(sp.expand(v_).xreplace(sub)) for k_,v_ in sub.items()}
    shown={str(k):sp.simplify(v) for k,v in s0.items()}
    for k_ in sorted(shown): print(f"     {k_} = {shown[k_]}")
    res=rung(d,sub)
    print(f"   residual after substitution: {len(res)} equation(s)")
print("\n=== accumulated substitutions ===")
for k_ in sorted(sub,key=str): print(f"  {k_} = {sub[k_]}")
print(f"\ntotal coefficients pinned from the bottom: {len(sub)}")
