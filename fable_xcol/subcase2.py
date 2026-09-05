"""GGHV Prop 4.3 SUB-CASE (2) -- never examined by this campaign.

    N(P) = {(0,0),(1,0),(8,14),(8,16)}      (quadrilateral: no (0,8))
    N(Q) = {(0,0),(2,1),(12,21),(12,24)}    (quadrilateral: no (0,12))
    [P,Q] = x^2

Same machinery as the pentagon (supports from the hulls, x-column grading,
determinantal rank test).  Reports: system size, the rung-19 closed form, the
rank of L'_P, and the positive/negative controls.
"""
import sympy as sp, math, random
from sympy import Rational as R
P_MOD=(1<<31)-1
CASES={
 "pentagon  (sub-case 1)": ([(0,0),(1,0),(8,14),(8,16),(0,8)],
                            [(0,0),(2,1),(12,21),(12,24),(0,12)]),
 "quadrilateral (sub-case 2)": ([(0,0),(1,0),(8,14),(8,16)],
                                [(0,0),(2,1),(12,21),(12,24)]),
}
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        n=len(v)
        for t in range(n):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%n]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+R(y2-y1,x2-x1)*(i-x1))
        if not pts: lo[i]=None;hi[i]=None;continue
        lo[i]=int(sp.ceiling(min(pts))); hi[i]=int(sp.floor(max(pts)))
    return lo,hi
y=sp.Symbol('y')
for name,(NPv,NQv) in CASES.items():
    print("="*66); print(name)
    loP,hiP=bounds(NPv,8); loQ,hiQ=bounds(NQv,12)
    loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
    Aidx=[(i,j) for i in range(9) if loP[i] is not None for j in range(loP[i],hiP[i]+1)]
    Bidx=[(k,j) for k in range(13) if loQ[k] is not None for j in range(loQ[k],hiQ[k]+1)]
    print(f"  P columns: {[(i,loP[i],hiP[i]) for i in range(9)]}")
    print(f"  Q columns: {[(k,loQ[k],hiQ[k]) for k in range(13)]}")
    a={i:sum(sp.Symbol(f'a{i}_{j}')*y**j for j in range(loP[i],hiP[i]+1)) for i in range(9)}
    b={k:sum(sp.Symbol(f'b{k}_{j}')*y**j for j in range(loQ[k],hiQ[k]+1)) for k in range(13)}
    neq=0; per={}
    for d in range(-1,20):
        e=0
        for i in range(9):
            k=d+1-i
            if 0<=k<=12: e+= i*a[i]*sp.diff(b[k],y)-k*sp.diff(a[i],y)*b[k]
        e=sp.expand(e-(1 if d==2 else 0))
        cs=[] if e==0 else [c for c in sp.Poly(e,y).all_coeffs() if c!=0]
        per[d]=len(cs); neq+=len(cs)
    print(f"  unknowns: P {len(Aidx)} + Q {len(Bidx)} = {len(Aidx)+len(Bidx)} (+2 additive)")
    print(f"  equations: {neq}   per x-column: {[per[d] for d in range(19,-2,-1)]}")
    # rung 19 closed form
    a8=a[8]; b12=b[12]
    E=sp.expand(8*a8*sp.diff(b12,y)-12*sp.diff(a8,y)*b12)
    cs=[c for c in sp.Poly(E,y).all_coeffs() if c!=0] if E!=0 else []
    A=[sp.Symbol(f'a8_{j}') for j in range(loP[8],hiP[8]+1)]
    B=[sp.Symbol(f'b12_{j}') for j in range(loQ[12],hiQ[12]+1)]
    sol=sp.solve(cs,A+B,dict=True)
    print(f"  rung 19: {len(cs)} eqs, {len(A)+len(B)} unknowns -> {len(sol)} components; "
          f"free dim = {len(A)+len(B)-len(cs)}")
    # determinantal rank test
    rowset=sorted({(i+k-1,ja+jb-1) for (i,ja) in Aidx for (k,jb) in Bidx
                   if i+k-1>=0 and ja+jb-1>=0})
    rowpos={r:n for n,r in enumerate(rowset)}
    def build(pv):
        M=[[0]*len(Bidx) for _ in rowset]
        for ai,(i,ja) in enumerate(Aidx):
            c=pv[ai]
            if c==0: continue
            for bi,(k,jb) in enumerate(Bidx):
                v=(i*jb-k*ja)%P_MOD
                if v==0: continue
                r=rowpos.get((i+k-1,ja+jb-1))
                if r is None: continue
                M[r][bi]=(M[r][bi]+c*v)%P_MOD
        return M
    def rank_hom(M,drop):
        Am=[M[r][:] for r in range(len(M)) if r!=drop]
        nr,nc=len(Am),len(Am[0]); rk=0
        for c in range(nc):
            piv=None
            for r in range(rk,nr):
                if Am[r][c]: piv=r;break
            if piv is None: continue
            Am[rk],Am[piv]=Am[piv],Am[rk]
            inv=pow(Am[rk][c],P_MOD-2,P_MOD)
            Am[rk]=[(v*inv)%P_MOD for v in Am[rk]]
            for r in range(nr):
                if r!=rk and Am[r][c]:
                    f=Am[r][c]; Am[r]=[(Am[r][j]-f*Am[rk][j])%P_MOD for j in range(nc)]
            rk+=1
            if rk==nr: break
        return rk
    row20=rowpos.get((2,0))
    random.seed(7)
    if row20 is not None:
        rs=[rank_hom(build([random.randrange(1,P_MOD) for _ in Aidx]),row20) for _ in range(2)]
        print(f"  rank(L'_P) at random P: {rs} of {len(Bidx)} columns")
    else:
        print("  *** the x^2 row is NOT in the row space -> system is INCONSISTENT by support alone ***")
