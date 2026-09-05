"""EXACT mod-p ladder for sub-case (2).  Decides whether rungs 13..19 are
genuinely independent conditions or largely automatic.

All arithmetic is integers mod p, so 'zero' means exactly zero -- no
floating-point ambiguity.  Free (kernel) directions are filled with random
values, so the ladder produces a generic point of the rungs-2..12 variety.
"""
import random, math, sys
from fractions import Fraction as F
P=(1<<61)-1        # Mersenne prime, plenty of room
def inv(a): return pow(a%P, P-2, P)
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
AR={i:rg(loP[i],hiP[i]) for i in range(9)}; BR={k:rg(loQ[k],hiQ[k]) for k in range(13)}

def terms(A,B,d,skipA=None,skipB=None):
    acc={}
    for i in range(9):
        k=d+1-i
        if not (0<=k<=12): continue
        if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
        for ca,xa in zip(A[i],AR[i]):
            if ca==0: continue
            for cb,xb in zip(B[k],BR[k]):
                if cb==0: continue
                if xb: e=xa+xb-1; acc[e]=(acc.get(e,0)+i*ca%P*cb%P*xb)%P
                if xa: e=xa-1+xb; acc[e]=(acc.get(e,0)-k*ca%P*cb%P*xa)%P
    return {e:c%P for e,c in acc.items()}

def solve_mod(M,v):
    """solve M u = v mod P; returns (particular, nullspace basis)"""
    nr=len(M); nc=len(M[0]) if nr else 0
    Aug=[row[:]+[v[i]] for i,row in enumerate(M)]
    piv=[]; r=0
    for c in range(nc):
        pr=None
        for i in range(r,nr):
            if Aug[i][c]%P: pr=i; break
        if pr is None: continue
        Aug[r],Aug[pr]=Aug[pr],Aug[r]
        iv=inv(Aug[r][c]); Aug[r]=[x*iv%P for x in Aug[r]]
        for i in range(nr):
            if i!=r and Aug[i][c]%P:
                f=Aug[i][c]; Aug[i]=[(Aug[i][j]-f*Aug[r][j])%P for j in range(nc+1)]
        piv.append(c); r+=1
    for i in range(r,nr):
        if all(Aug[i][j]%P==0 for j in range(nc)) and Aug[i][nc]%P:
            return None,None      # inconsistent
    part=[0]*nc
    for i,c in enumerate(piv): part[c]=Aug[i][nc]%P
    free=[c for c in range(nc) if c not in piv]
    ns=[]
    for fc in free:
        vec=[0]*nc; vec[fc]=1
        for i,c in enumerate(piv): vec[c]=(-Aug[i][fc])%P
        ns.append(vec)
    return part,ns

def run(seed):
    rnd=random.Random(seed)
    A={i:[0]*len(AR[i]) for i in range(9)}; B={k:[0]*len(BR[k]) for k in range(13)}
    Av=rnd.randrange(1,P); Bv=rnd.randrange(1,P)
    for idx,e in enumerate(AR[1]): A[1][idx]= Av if e==0 else (2*Av*Av%P*Bv%P if e==1 else 0)
    for idx,e in enumerate(BR[2]): B[2][idx]= inv(Av) if e==1 else (Bv if e==2 else 0)
    nfree=0
    for d in range(3,13):
        ia=d-1 if 0<=d-1<=8 else None; kb=d if 0<=d<=12 else None
        unk=[]
        if ia is not None: unk+=[('a',ia,j) for j in range(len(AR[ia]))]
        if kb is not None: unk+=[('b',kb,j) for j in range(len(BR[kb]))]
        if not unk: continue
        known=terms(A,B,d,skipA=ia,skipB=kb)
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
        exps=sorted(set(list(cols)+list(known)))
        M=[[cols.get(e,{}).get(ui,0) for ui in range(len(unk))] for e in exps]
        v=[(-known.get(e,0))%P for e in exps]
        part,ns=solve_mod(M,v)
        if part is None:
            return None,f"rung {d}: INCONSISTENT (gate)"
        sol=part[:]
        for vec in ns:
            t=rnd.randrange(1,P); nfree+=1
            sol=[(sol[i]+t*vec[i])%P for i in range(len(sol))]
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    return (A,B,nfree),None

if __name__=='__main__':
    for seed in [1,2,3]:
        res,err=run(seed)
        if err: print(f"seed {seed}: {err}"); continue
        A,B,nf=res
        print(f"\nseed {seed}: ladder ran rungs 2..12, {nf} kernel parameters filled randomly")
        print(f"  a_8 = {A[8]}")
        print(f"  vertices: a8_16={'NONZERO' if A[8][-1] else 'zero'}, "
              f"a8_14={'NONZERO' if A[8][0] else 'zero'}, "
              f"b12_24={'NONZERO' if B[12][-1] else 'zero'}, "
              f"b12_21={'NONZERO' if B[12][0] else 'zero'}")
        tot=0; zed=0
        for d in range(13,20):
            acc=terms(A,B,d)
            nz=sum(1 for c in acc.values() if c%P)
            tot+=len(acc); zed+=len(acc)-nz
            print(f"  rung {d}: {len(acc)} coeffs, {len(acc)-nz} EXACTLY zero, {nz} nonzero")
        print(f"  TOTAL: {zed}/{tot} vanish identically  ->  effective conditions = {tot-zed}")
