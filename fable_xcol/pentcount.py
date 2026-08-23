"""Same freedom-vs-gate accounting, applied to BOTH sub-cases, bottom-up.

Which branch has more room for a counterexample?  Exact mod p.
For each rung: how many new unknowns, what rank, how many gates, how much
freedom is created.  The branch where freedom outruns conditions longest is the
better place to hunt.
"""
import random, math, sys
from fractions import Fraction as F
P=(1<<31)-1
def inv(a): return pow(a%P,P-2,P)
CASES={
 "PENTAGON  sub-case (1)": ([(0,0),(1,0),(8,14),(8,16),(0,8)],
                            [(0,0),(2,1),(12,21),(12,24),(0,12)]),
 "QUADRILAT sub-case (2)": ([(0,0),(1,0),(8,14),(8,16)],
                            [(0,0),(2,1),(12,21),(12,24)]),
}
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

for name,(NPv,NQv) in CASES.items():
    loP,hiP=bounds(NPv,8); loQ,hiQ=bounds(NQv,12)
    loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
    rg=lambda lo,hi: [] if lo is None or lo>hi else list(range(lo,hi+1))
    AR={i:rg(loP[i],hiP[i]) for i in range(9)}; BR={k:rg(loQ[k],hiQ[k]) for k in range(13)}
    nun=sum(len(AR[i]) for i in range(9))+sum(len(BR[k]) for k in range(13))
    print(f"\n{'='*70}\n{name}: {nun} unknowns")
    rnd=random.Random(4)
    A={i:[0]*len(AR[i]) for i in range(9)}; B={k:[0]*len(BR[k]) for k in range(13)}
    def terms(d,skipA=None,skipB=None):
        acc={}
        for i in range(9):
            k=d+1-i
            if not (0<=k<=12): continue
            if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
            for ca,xa in zip(A[i],AR[i]):
                if ca==0: continue
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb: e=xa+xb-1; acc[e]=(acc.get(e,0)+i*ca*cb%P*xb)%P
                    if xa: e=xa-1+xb; acc[e]=(acc.get(e,0)-k*ca*cb%P*xa)%P
        return acc
    cum=0; firstgate=None
    print(f"{'rung':>5} {'eqs':>4} {'new':>4} {'rank':>5} {'gates':>6} {'free+':>6} {'cum':>5}")
    for d in range(-1,20):
        # bottom-up: new unknowns are the highest-index columns not yet set
        newA=[i for i in range(9) if any(A[i][j]==0 for j in range(len(AR[i]))) and AR[i]]
        unk=[]
        imin=min([i for i in range(9) if AR[i]]); kmin=min([k for k in range(13) if BR[k]])
        iN=d+1-kmin; kN=d+1-imin
        ia=iN if 0<=iN<=8 and AR.get(iN) else None
        kb=kN if 0<=kN<=12 and BR.get(kN) else None
        if ia is not None: unk+=[('a',ia,j) for j in range(len(AR[ia]))]
        if kb is not None: unk+=[('b',kb,j) for j in range(len(BR[kb]))]
        known=terms(d,skipA=ia,skipB=kb)
        rhs1 = 1 if d==2 else 0
        cols={}
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a':
                i=idx; k=d+1-i
                if not (0<=k<=12): continue
                xa=AR[i][j]
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)+i*cb%P*xb)%P
                    if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)-k*cb%P*xa)%P
            else:
                k=idx; i=d+1-k
                if not (0<=i<=8): continue
                xb=BR[k][j]
                for ca,xa in zip(A[i],AR[i]):
                    if ca==0: continue
                    if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)+i*ca%P*xb)%P
                    if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=(cols[e].get(ui,0)-k*ca%P*xa)%P
        exps=sorted(set(list(cols)+list(known)+([0] if rhs1 else [])))
        if not exps:
            # rung imposes nothing: every new unknown is free
            if unk:
                print(f"{d:>5} {0:>4} {len(unk):>4} {0:>5} {0:>6} {len(unk):>6} {cum+len(unk):>5}")
                cum+=len(unk)
                for (typ,idx,j) in unk:
                    val=rnd.randrange(1,P)
                    if typ=='a': A[idx][j]=val
                    else: B[idx][j]=val
            continue
        M=[[cols.get(e,{}).get(ui,0) for ui in range(len(unk))] for e in exps]
        v=[((rhs1 if e==0 else 0)-known.get(e,0))%P for e in exps]
        if not unk:
            ng=sum(1 for x in v if x%P)
            print(f"{d:>5} {len(exps):>4} {0:>4} {'-':>5} {ng:>6} {0:>6} {cum:>5}  (pure)")
            continue
        part,ns,gates=rref(M,v)
        print(f"{d:>5} {len(exps):>4} {len(unk):>4} {len(unk)-len(ns):>5} {len(gates):>6} {len(ns):>6} {cum+len(ns):>5}")
        if gates and firstgate is None: firstgate=d
        cum+=len(ns)
        sol=part[:]
        for vec in ns:
            t=rnd.randrange(1,P)
            sol=[(sol[i]+t*vec[i])%P for i in range(len(sol))]
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    print(f"  -> first gate at rung {firstgate}, total freedom created: {cum}")
