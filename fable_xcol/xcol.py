"""Independent reconstruction of the pentagon from the convex hulls alone,
graded by x-column d.  {P,Q} = sum_d ( sum_{i+k=d+1} [i a_i b_k' - k a_i' b_k] ) x^d = x^2.
Supports come from N(P), N(Q) vertices ONLY (no campaign code reused)."""
import sympy as sp
from sympy import Rational as R

# convex hulls in (x-exp, y-exp)
NP = [(0,0),(1,0),(8,14),(8,16),(0,8)]
NQ = [(0,0),(2,1),(12,21),(12,24),(0,12)]

def bounds(verts, imax):
    """lower/upper y bound at each x-exponent from the convex hull"""
    lo, hi = {}, {}
    for i in range(imax+1):
        ys=[]
        # intersect vertical line x=i with hull: use LP over hull edges
        pts=[]
        n=len(verts)
        for t in range(n):
            (x1,y1),(x2,y2)=verts[t],verts[(t+1)%n]
            if x1==x2==i: pts += [y1,y2]
            elif (x1-i)*(x2-i) <= 0 and x1!=x2:
                pts.append(y1 + R(y2-y1,x2-x1)*(i-x1))
        lo[i]=sp.ceiling(min(pts)); hi[i]=sp.floor(max(pts))
    return lo,hi

loP,hiP = bounds(NP,8); loQ,hiQ = bounds(NQ,12)
# additive normalisation kills the constant terms p_0_0, q_0_0
loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
print("P columns (val,deg):", [(i,int(loP[i]),int(hiP[i])) for i in range(9)])
print("Q columns (val,deg):", [(k,int(loQ[k]),int(hiQ[k])) for k in range(13)])
nP=sum(int(hiP[i]-loP[i])+1 for i in range(9)); nQ=sum(int(hiQ[k]-loQ[k])+1 for k in range(13))
print("unknowns: P",nP," Q",nQ," total",nP+nQ)

y=sp.Symbol('y')
a={i: sum(sp.Symbol(f'a{i}_{j}')*y**j for j in range(int(loP[i]),int(hiP[i])+1)) for i in range(9)}
b={k: sum(sp.Symbol(f'b{k}_{j}')*y**j for j in range(int(loQ[k]),int(hiQ[k])+1)) for k in range(13)}

eqs=[]; per={}
for d in range(-1,20):
    expr=0
    for i in range(9):
        k=d+1-i
        if 0<=k<=12: expr += i*a[i]*sp.diff(b[k],y) - k*sp.diff(a[i],y)*b[k]
    expr = sp.expand(expr - (1 if d==2 else 0))
    if expr==0: per[d]=0; continue
    cs = sp.Poly(expr,y).all_coeffs()
    cs = [c for c in cs if c!=0]
    per[d]=len(cs); eqs+=cs
print("equations per x-column d:", {d:per[d] for d in sorted(per)})
print("TOTAL equations:", len(eqs))
