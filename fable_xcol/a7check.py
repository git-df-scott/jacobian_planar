"""Is the d=17 gate equivalent to the campaign's rung-17 condition A_7(r)=0?
Also: test the conjecture that all conditions are regularity/Taylor conditions at y=r."""
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
# solve d=18
new18=[sp.Symbol(f'a7_{j}') for j in range(loP[7],hiP[7]+1)]+[sp.Symbol(f'b11_{j}') for j in range(loQ[11],hiQ[11]+1)]
s18=sp.solve(rung(18,{}),new18,dict=True)[0]
sub=dict(s18)
print("d=18 solved for:",[str(k) for k in s18])
a7=sp.expand(a[7].subs(sub)); b11=sp.expand(b[11].subs(sub))
# the campaign's rung-17 condition is A_7(r)=0 where A_7 is a_7's lower-edge part.
# Test BOTH readings against my gate G:
G = sp.Symbol('b11_20')+2*sp.Symbol('b11_21')*r+3*sp.Symbol('b11_22')*r**2+4*sp.Symbol('b11_23')*r**3
G = sp.expand(G.subs(sub))
print("\nGATE G =",sp.factor(G))
cand={
 "a_7(r)": sp.expand(a7.subs(y,r)),
 "(a_7/y^12)(r)": sp.expand(sp.simplify(a7/y**12).subs(y,r)),
 "(b_11/y^19)'(r)": sp.expand(sp.diff(sp.simplify(b11/y**19),y).subs(y,r)),
 "b_11(r)": sp.expand(b11.subs(y,r)),
}
for nm,e in cand.items():
    e=sp.simplify(e)
    if e==0: print(f"  {nm} == 0 identically after d=18"); continue
    q=sp.simplify(sp.cancel(G/e))
    print(f"  {nm}: proportional to G ? ratio = {sp.factor(q) if q.is_number or len(sp.factor(q).free_symbols)<3 else 'no'}   value={sp.factor(e)}")
