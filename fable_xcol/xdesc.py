"""EXACT x-column descent, convex-hull supports only.
No z=s-tau, no eighth-power ansatz, no campaign code.  Records every denominator."""
import sympy as sp, pickle, sys, time
from sympy import Rational as R
y=sp.Symbol('y')
NP=[(0,0),(1,0),(8,14),(8,16),(0,8)]; NQ=[(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]; n=len(v)
        for t in range(n):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%n]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+R(y2-y1,x2-x1)*(i-x1))
        lo[i]=int(sp.ceiling(min(pts))); hi[i]=int(sp.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12); loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
a={i:sum(sp.Symbol(f'a{i}_{j}')*y**j for j in range(loP[i],hiP[i]+1)) for i in range(9)}
b={k:sum(sp.Symbol(f'b{k}_{j}')*y**j for j in range(loQ[k],hiQ[k]+1)) for k in range(13)}
def rung(d,sub):
    e=0
    for i in range(9):
        k=d+1-i
        if 0<=k<=12: e+= i*a[i]*sp.diff(b[k],y)-k*sp.diff(a[i],y)*b[k]
    e=sp.expand(e.subs(sub)-(1 if d==2 else 0))
    return [c for c in sp.Poly(e,y).all_coeffs() if c!=0] if e!=0 else []

sub={}; carried=[]; gates=[]; denoms=set()
for d in range(19,6,-1):
    new=[]
    i0=d-11; k0=d-7
    if 0<=i0<=8: new+=[sp.Symbol(f'a{i0}_{j}') for j in range(loP[i0],hiP[i0]+1)]
    if 0<=k0<=12: new+=[sp.Symbol(f'b{k0}_{j}') for j in range(loQ[k0],hiQ[k0]+1)]
    cs=rung(d,sub)
    if not cs: print(f"d={d}: vacuous"); continue
    # linear in the NEW unknowns?
    lin=all(sp.Poly(c,*new).total_degree()<=1 for c in cs) if new else True
    sol=sp.solve(cs,new,dict=True) if new else []
    if not sol:
        print(f"d={d}: {len(cs)} eqs, {len(new)} new, linear={lin} -> NO SOLUTION (conditions on carried)")
        gates.append((d,cs)); break
    s0=sol[0]
    for v_,ex in s0.items():
        for den in sp.denom(sp.together(ex)).free_symbols: denoms.add(str(den))
    sub.update({k_:sp.simplify(v_.subs(sub)) for k_,v_ in s0.items()})
    free=[v_ for v_ in new if v_ not in s0]
    carried+=free
    res=rung(d,sub)
    print(f"d={d}: {len(cs)} eqs, {len(new)} new, linear={lin}, solved {len(s0)}, free {len(free)}, residual {len(res)}", flush=True)
    if res: gates.append((d,res)); print(f"   GATES at d={d}: {[sp.factor(g) for g in res][:3]}")
print("\nDENOMINATOR LEDGER (params ever divided by):", sorted(denoms))
pickle.dump((sub,carried,gates),open('xdesc.pkl','wb'))
