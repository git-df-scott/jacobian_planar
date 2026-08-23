"""DIRECT ATTACK on GGHV Prop 4.2 sub-case (3) for (9,24) -- the best-scoring
shape in the whole sub-125 landscape (slack -11, 54 unknowns, 28 conditions).

    N(P) = {(0,0),(1,1),(6,16),(6,18)}      deg_x P = 6
    N(Q) = {(0,0),(1,0),(9,24),(9,27)}      deg_x Q = 9
    [P,Q] = x                                (bracket exponent K = 1)

The paper discards this case via Theorem 5.1 (section 5), which this campaign's
own audit records as its single highest-value UNREPLICATED exclusion.  So a
solution here would either be a counterexample or a refutation of Theorem 5.1.

Same machinery as sub-case (2): bottom-up ladder (a chain of small linear
solves), free kernel parameters, scale-invariant residual so a collapse cannot
masquerade as a solution, and vertex barriers.
"""
import numpy as np, math, sys
from fractions import Fraction as F
from scipy.optimize import least_squares
MX, MQ, K = 6, 9, 1
NPv=[(0,0),(1,1),(6,16),(6,18)]
NQv=[(0,0),(1,0),(9,24),(9,27)]
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
loP,hiP=bounds(NPv,MX); loQ,hiQ=bounds(NQv,MQ)
if loP[0] is not None: loP[0]=max(loP[0],1)
if loQ[0] is not None: loQ[0]=max(loQ[0],1)
rg=lambda lo,hi: [] if lo is None or lo>hi else list(range(lo,hi+1))
AR={i:rg(loP[i],hiP[i]) for i in range(MX+1)}
BR={k:rg(loQ[k],hiQ[k]) for k in range(MQ+1)}
NU=sum(len(AR[i]) for i in range(MX+1))+sum(len(BR[k]) for k in range(MQ+1))
IMIN=min([i for i in range(MX+1) if AR[i]]); KMIN=min([k for k in range(MQ+1) if BR[k]])
print(f"(9,24) sub-case (3): P columns {[(i,loP[i],hiP[i]) for i in range(MX+1)]}")
print(f"                     Q columns {[(k,loQ[k],hiQ[k]) for k in range(MQ+1)]}")
print(f"                     {NU} unknowns, bracket [P,Q] = x^{K}\n")

def contrib(A,B,d,skipA=None,skipB=None,mag=False):
    acc={}; mg={}
    for i in range(MX+1):
        k=d+1-i
        if not (0<=k<=MQ): continue
        if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
        for ca,xa in zip(A[i],AR[i]):
            if ca==0: continue
            for cb,xb in zip(B[k],BR[k]):
                if cb==0: continue
                if xb:
                    e=xa+xb-1; t=i*ca*cb*xb; acc[e]=acc.get(e,0j)+t
                    if mag: mg[e]=mg.get(e,0.)+abs(t)
                if xa:
                    e=xa-1+xb; t=-k*ca*cb*xa; acc[e]=acc.get(e,0j)+t
                    if mag: mg[e]=mg.get(e,0.)+abs(t)
    return (acc,mg) if mag else acc

def run(t):
    A={i:[0j]*len(AR[i]) for i in range(MX+1)}
    B={k:[0j]*len(BR[k]) for k in range(MQ+1)}
    ptr=0; res=[]
    # BOTTOM RUNG solved exactly: Wronskian(a_1,b_1) = 1 has ONE branch,
    #   a_1 = -y/b0   (higher coeffs forced zero),   b_1 = b0 + b1*y
    b0=t[0]; b1=t[1]; ptr=2
    for idx,e in enumerate(AR[1]): A[1][idx] = (-1.0/b0) if e==1 else 0j
    for idx,e in enumerate(BR[1]): B[1][idx] = b0 if e==0 else (b1 if e==1 else 0j)
    for d in range(2,MX+MQ+2):
        iN=d+1-KMIN; kN=d+1-IMIN
        ia=iN if 0<=iN<=MX and AR.get(iN) else None
        kb=kN if 0<=kN<=MQ and BR.get(kN) else None
        unk=[]
        if ia is not None: unk+=[('a',ia,j) for j in range(len(AR[ia]))]
        if kb is not None: unk+=[('b',kb,j) for j in range(len(BR[kb]))]
        known=contrib(A,B,d,skipA=ia,skipB=kb)
        rhs1 = 1 if d==K else 0
        cols={}
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a':
                i=idx; k=d+1-i
                if not (0<=k<=MQ): continue
                xa=AR[i][j]
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)+i*cb*xb
                    if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)-k*cb*xa
            else:
                k=idx; i=d+1-k
                if not (0<=i<=MX): continue
                xb=BR[k][j]
                for ca,xa in zip(A[i],AR[i]):
                    if ca==0: continue
                    if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)+i*ca*xb
                    if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)-k*ca*xa
        exps=sorted(set(list(cols)+list(known)+([0] if rhs1 else [])))
        if not exps:
            for (typ,idx,j) in unk:
                v=t[ptr] if ptr<len(t) else 0j; ptr+=1
                if typ=='a': A[idx][j]=v
                else: B[idx][j]=v
            continue
        M=np.zeros((len(exps),len(unk)),dtype=complex); v=np.zeros(len(exps),dtype=complex)
        for ri,e in enumerate(exps):
            for ui,c in cols.get(e,{}).items(): M[ri,ui]=c
            v[ri]=((rhs1 if e==0 else 0)-known.get(e,0j))
        if not unk:
            acc,mg=contrib(A,B,d,mag=True)
            for e,c in acc.items():
                tgt=(rhs1 if e==0 else 0)
                m=mg.get(e,0.)
                if m>1e-300: res.append((c-tgt)/m)
            continue
        sol,_,_,sv=np.linalg.lstsq(M,v,rcond=None)
        rank=int((sv>sv[0]*1e-11).sum()) if sv.size else 0
        if rank<len(unk):
            U,S,Vt=np.linalg.svd(M)
            for i2 in range(Vt.shape[0]):
                if i2>=S.size or S[i2]<=S[0]*1e-11:
                    vec=Vt[i2].conj()
                    sol=sol+(t[ptr] if ptr<len(t) else 0j)*vec; ptr+=1
        else:
            r=M@sol-v
            nrm=float(np.linalg.norm(np.abs(M)@np.abs(sol))+np.linalg.norm(np.abs(v)))+1e-300
            for c in r: res.append(c/nrm)
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    return A,B,np.array(res),ptr

NF=None
_RLEN=[100]
def resid(x):
    n=len(x)//2
    t=x[:n]+1j*x[n:]
    try:
        A,B,r,_=run(t)
        if not np.all(np.isfinite(r)): return np.full(_RLEN[0],1e3)
    except Exception:
        return np.full(_RLEN[0],1e3)
    out=np.concatenate([r.real,r.imag])
    vs=[A[6][-1],A[6][0],B[9][-1],B[9][0]]
    sc=max(abs(v) for v in vs)+1e-300
    pen=np.array([0.05*sc/(abs(v)+1e-300) for v in vs])
    r2=np.concatenate([out,pen])
    _RLEN[0]=len(r2)
    if not np.all(np.isfinite(r2)): return np.full(len(r2),1e3)
    return r2

if __name__=='__main__':
    probe=np.ones(200,dtype=complex)*0.7
    _,_,_,nf=run(probe)
    print(f"ladder consumes {nf} free parameters\n")
    rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    N=int(sys.argv[2]) if len(sys.argv)>2 else 60
    best=(1e99,None)
    for trial in range(N):
        x0=rng.normal(size=2*nf)
        try: s=least_squares(resid,x0,method='lm',max_nfev=30000)
        except Exception: continue
        r=resid(s.x); core=r[:-8]; val=float(np.linalg.norm(core))
        if val<best[0]:
            best=(val,s.x.copy())
            t=s.x[:nf]+1j*s.x[nf:]
            A,B,_,_=run(t)
            print(f"  trial {trial:3d}: ||F|| = {val:.6e}  "
                  f"|p_18_6|={abs(A[6][-1]):.2e} |q_27_9|={abs(B[9][-1]):.2e}",flush=True)
    print(f"\nBEST ||F|| = {best[0]:.8e}")
    if best[1] is not None: np.save('case924_best.npy',best[1])
