"""WHICH NEWTON POLYGONS ADMIT ENOUGH FREEDOM FOR A COUNTEREXAMPLE?

The bottom-up accounting (freedom created vs conditions imposed) depends only on
the two Newton polygons and the bracket exponent.  So we can sweep it over
candidate shapes WITHOUT deriving each case's automorphism reduction.

For a solution to exist the system must not be hopelessly over-determined.
This sweep finds the shapes where freedom is largest relative to conditions --
those are where a counterexample could live, and they are the targets worth the
cost of deriving their reductions.

Bracket condition [P,Q] = x^K.
"""
import random, math, sys
from fractions import Fraction as F
P=(1<<31)-1
def inv(a): return pow(a%P,P-2,P)
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
def rref(M,v):
    nr=len(M); nc=len(M[0]) if nr else 0
    Aug=[M[i][:]+[v[i]] for i in range(nr)]
    piv=[]; r=0
    for c in range(nc):
        pr=None
        for i in range(r,nr):
            if Aug[i][c]%P: pr=i;break
        if pr is None: continue
        Aug[r],Aug[pr]=Aug[pr],Aug[r]
        iv=inv(Aug[r][c]); Aug[r]=[x*iv%P for x in Aug[r]]
        for i in range(nr):
            if i!=r and Aug[i][c]%P:
                f=Aug[i][c]; Aug[i]=[(Aug[i][j]-f*Aug[r][j])%P for j in range(nc+1)]
        piv.append(c); r+=1
    gates=[Aug[i][nc]%P for i in range(r,nr) if all(Aug[i][j]%P==0 for j in range(nc))]
    part=[0]*nc
    for i,c in enumerate(piv): part[c]=Aug[i][nc]%P
    ns=[]
    for fc in [c for c in range(nc) if c not in piv]:
        vec=[0]*nc; vec[fc]=1
        for i,c in enumerate(piv): vec[c]=(-Aug[i][fc])%P
        ns.append(vec)
    return part,ns,[g for g in gates if g%P]

def analyse(NPv,NQv,K,mx=8,mq=12,seed=4):
    loP,hiP=bounds(NPv,mx); loQ,hiQ=bounds(NQv,mq)
    if loP[0] is not None: loP[0]=max(loP[0],1)
    if loQ[0] is not None: loQ[0]=max(loQ[0],1)
    rg=lambda lo,hi: [] if lo is None or lo>hi else list(range(lo,hi+1))
    AR={i:rg(loP[i],hiP[i]) for i in range(mx+1)}; BR={k:rg(loQ[k],hiQ[k]) for k in range(mq+1)}
    if not any(AR.values()) or not any(BR.values()): return None
    nun=sum(len(AR[i]) for i in range(mx+1))+sum(len(BR[k]) for k in range(mq+1))
    rnd=random.Random(seed)
    A={i:[0]*len(AR[i]) for i in range(mx+1)}; B={k:[0]*len(BR[k]) for k in range(mq+1)}
    imin=min([i for i in range(mx+1) if AR[i]]); kmin=min([k for k in range(mq+1) if BR[k]])
    def terms(d,skipA=None,skipB=None):
        acc={}
        for i in range(mx+1):
            k=d+1-i
            if not (0<=k<=mq): continue
            if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
            for ca,xa in zip(A[i],AR[i]):
                if ca==0: continue
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb: e=xa+xb-1; acc[e]=(acc.get(e,0)+i*ca*cb%P*xb)%P
                    if xa: e=xa-1+xb; acc[e]=(acc.get(e,0)-k*ca*cb%P*xa)%P
        return acc
    cum=0; cond=0; first=None
    for d in range(-1,mx+mq+2):
        iN=d+1-kmin; kN=d+1-imin
        ia=iN if 0<=iN<=mx and AR.get(iN) else None
        kb=kN if 0<=kN<=mq and BR.get(kN) else None
        unk=[]
        if ia is not None: unk+=[('a',ia,j) for j in range(len(AR[ia]))]
        if kb is not None: unk+=[('b',kb,j) for j in range(len(BR[kb]))]
        known=terms(d,skipA=ia,skipB=kb)
        rhs1=1 if d==K else 0
        cols={}
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a':
                i=idx; k=d+1-i
                if not (0<=k<=mq): continue
                xa=AR[i][j]
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)+i*cb%P*xb)%P
                    if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)-k*cb%P*xa)%P
            else:
                k=idx; i=d+1-k
                if not (0<=i<=mx): continue
                xb=BR[k][j]
                for ca,xa in zip(A[i],AR[i]):
                    if ca==0: continue
                    if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)+i*ca%P*xb)%P
                    if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)-k*ca%P*xa)%P
        exps=sorted(set(list(cols)+list(known)+([0] if rhs1 else [])))
        if not exps:
            if unk:
                cum+=len(unk)
                for (typ,idx,j) in unk:
                    v=rnd.randrange(1,P)
                    if typ=='a': A[idx][j]=v
                    else: B[idx][j]=v
            continue
        M=[[cols.get(e,{}).get(ui,0) for ui in range(len(unk))] for e in exps]
        v=[((rhs1 if e==0 else 0)-known.get(e,0))%P for e in exps]
        if not unk:
            cond+=sum(1 for x in v if x%P); continue
        part,ns,gates=rref(M,v)
        cond+=len(gates)
        if gates and first is None: first=d
        cum+=len(ns)
        sol=part[:]
        for vec in ns:
            t=rnd.randrange(1,P); sol=[(sol[i]+t*vec[i])%P for i in range(len(sol))]
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    return dict(unknowns=nun,freedom=cum,conditions=cond,first_gate=first,
                slack=cum-cond)

if __name__=='__main__':
    print(f"{'shape':<46} {'unk':>4} {'free':>5} {'cond':>5} {'slack':>6} {'gate@':>6}")
    shapes=[]
    # the two known cases
    shapes.append(("(8,28) sub-case 1 pentagon  [P,Q]=x^2",
                   [(0,0),(1,0),(8,14),(8,16),(0,8)],[(0,0),(2,1),(12,21),(12,24),(0,12)],2))
    shapes.append(("(8,28) sub-case 2 quadrilateral [x^2]",
                   [(0,0),(1,0),(8,14),(8,16)],[(0,0),(2,1),(12,21),(12,24)],2))
    # GGHV Prop 4.1, the (9,27) case the paper discards: [P,Q] = x
    shapes.append(("(9,27) Prop 4.1  [P,Q]=x  (discarded)",
                   [(0,0),(1,1),(6,16),(6,18),(0,18)],[(0,0),(1,0),(9,24),(9,27),(0,27)],1))
    # Prop 4.2's three sub-cases for (9,24), [P,Q] = x
    shapes.append(("(9,24) Prop 4.2 (1)  [P,Q]=x",
                   [(0,0),(1,1),(6,16),(6,18),(0,12)],[(0,0),(1,0),(9,24),(9,27),(0,18)],1))
    shapes.append(("(9,24) Prop 4.2 (2)  [P,Q]=x",
                   [(0,0),(1,1),(6,16),(6,18),(0,6)],[(0,0),(1,0),(9,24),(9,27),(0,9)],1))
    shapes.append(("(9,24) Prop 4.2 (3)  [P,Q]=x",
                   [(0,0),(1,1),(6,16),(6,18)],[(0,0),(1,0),(9,24),(9,27)],1))
    for nm,NPv,NQv,K in shapes:
        r=analyse(NPv,NQv,K)
        if r is None: print(f"{nm:<46}  (degenerate support)"); continue
        print(f"{nm:<46} {r['unknowns']:>4} {r['freedom']:>5} {r['conditions']:>5} "
              f"{r['slack']:>6} {str(r['first_gate']):>6}")
    print("\nslack = freedom - conditions.  The less negative, the more room a")
    print("counterexample has.  Shapes with slack >= 0 would be UNDER-determined.")
