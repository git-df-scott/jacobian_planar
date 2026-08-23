"""SOLVE the sub-case (2) endgame: ~40 conditions in 16 unknowns.

Structure established exactly (sc2gate.py, mod p):
  rungs 3..9 : each adds exactly 2 free parameters, imposes NOTHING
               -> t in C^16  (A, B, and 14 kernel parameters)
  rungs 10-12: rank = #new unknowns, so the new unknowns are DETERMINED and
               each rung leaves ~2 residual conditions (gates)
  rungs 13-19: introduce nothing -> 34 pure conditions

So  F : C^16 -> C^~40  is a well-defined map and we want F(t) = 0 with the four
Newton vertices nonzero.  Scale-invariance is enforced by normalising each
condition against the magnitude of the terms being cancelled, so a collapse to
zero cannot masquerade as a solution (the trap that invalidated the earlier
float search).
"""
import numpy as np, math, sys
from fractions import Fraction as F
from scipy.optimize import least_squares
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

def contrib(A,B,d,skipA=None,skipB=None,want_mag=False):
    acc={}; mag={}
    for i in range(9):
        k=d+1-i
        if not (0<=k<=12): continue
        if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
        for ca,xa in zip(A[i],AR[i]):
            if ca==0: continue
            for cb,xb in zip(B[k],BR[k]):
                if cb==0: continue
                if xb:
                    e=xa+xb-1; t=i*ca*cb*xb
                    acc[e]=acc.get(e,0j)+t
                    if want_mag: mag[e]=mag.get(e,0.)+abs(t)
                if xa:
                    e=xa-1+xb; t=-k*ca*cb*xa
                    acc[e]=acc.get(e,0j)+t
                    if want_mag: mag[e]=mag.get(e,0.)+abs(t)
    return (acc,mag) if want_mag else acc

def cols_for(d,A,B,unk):
    cols={}
    for ui,(typ,idx,j) in enumerate(unk):
        if typ=='a':
            i=idx; k=d+1-i
            if not (0<=k<=12): continue
            xa=AR[i][j]
            for cb,xb in zip(B[k],BR[k]):
                if cb==0: continue
                if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)+i*cb*xb
                if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)-k*cb*xa
        else:
            k=idx; i=d+1-k
            if not (0<=i<=8): continue
            xb=BR[k][j]
            for ca,xa in zip(A[i],AR[i]):
                if ca==0: continue
                if xb: e=xa+xb-1; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)+i*ca*xb
                if xa: e=xa-1+xb; cols.setdefault(e,{}); cols[e][ui]=cols[e].get(ui,0j)-k*ca*xa
    return cols

def run(t):
    """t: complex vector length 16.  Returns (A,B,residuals)."""
    A={i:[0j]*len(AR[i]) for i in range(9)}; B={k:[0j]*len(BR[k]) for k in range(13)}
    Av=t[0]; Bv=t[1]; ptr=2
    for idx,e in enumerate(AR[1]): A[1][idx]= Av if e==0 else (2*Av*Av*Bv if e==1 else 0j)
    for idx,e in enumerate(BR[2]): B[2][idx]= (1/Av) if e==1 else (Bv if e==2 else 0j)
    res=[]
    for d in range(3,20):
        ia=d-1 if 0<=d-1<=8 else None; kb=d if 0<=d<=12 else None
        unk=[]
        if ia is not None: unk+=[('a',ia,j) for j in range(len(AR[ia]))]
        if kb is not None: unk+=[('b',kb,j) for j in range(len(BR[kb]))]
        if not unk:
            acc,mag=contrib(A,B,d,want_mag=True)
            for e,c in acc.items():
                m=mag.get(e,0.)
                if m>1e-300: res.append(c/m)
            continue
        known=contrib(A,B,d,skipA=ia,skipB=kb)
        cols=cols_for(d,A,B,unk)
        exps=sorted(set(list(cols)+list(known)))
        M=np.zeros((len(exps),len(unk)),dtype=complex); v=np.zeros(len(exps),dtype=complex)
        for ri,e in enumerate(exps):
            for ui,c in cols.get(e,{}).items(): M[ri,ui]=c
            v[ri]=-known.get(e,0j)
        sol,_,_,sv=np.linalg.lstsq(M,v,rcond=None)
        rank=int((sv>sv[0]*1e-12).sum()) if sv.size else 0
        nk=len(unk)-rank
        if nk>0:
            U,S,Vt=np.linalg.svd(M)
            ns=[Vt[i].conj() for i in range(Vt.shape[0]) if i>=S.size or S[i]<=S[0]*1e-12]
            for vec in ns:
                sol=sol+ (t[ptr] if ptr<len(t) else 0j)*vec; ptr+=1
        else:
            r=M@sol-v
            nrm=np.linalg.norm(np.abs(M)@np.abs(sol))+np.linalg.norm(np.abs(v))+1e-300
            for c in r: res.append(c/nrm)
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    return A,B,np.array(res)

def resid(x):
    t=x[:16]+1j*x[16:]
    try: A,B,r=run(t)
    except Exception: return np.ones(200)
    out=np.concatenate([r.real,r.imag])
    # keep the vertices away from zero (scale-invariantly)
    vs=[A[8][0],A[8][-1],B[12][0],B[12][-1]]
    sc=max(abs(v) for v in vs)+1e-300
    pen=np.array([0.05*sc/(abs(v)+1e-300) for v in vs])
    return np.concatenate([out,pen])

if __name__=='__main__':
    rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    N=int(sys.argv[2]) if len(sys.argv)>2 else 40
    best=(1e99,None)
    print("solving ~40 conditions in 16 unknowns (scale-invariant residual)")
    for trial in range(N):
        x0=rng.normal(size=32)
        try:
            s=least_squares(resid,x0,method='lm',max_nfev=20000,xtol=1e-14,ftol=1e-14)
        except Exception: continue
        r=resid(s.x); core=r[:-8]
        val=float(np.linalg.norm(core))
        if val<best[0]:
            best=(val,s.x.copy())
            t=s.x[:16]+1j*s.x[16:]
            A,B,_=run(t)
            print(f"  trial {trial:3d}: ||F|| = {val:.6e}   "
                  f"|p_16_8|={abs(A[8][-1]):.2e} |q_24_12|={abs(B[12][-1]):.2e}",flush=True)
    print(f"\nBEST ||F|| = {best[0]:.8e}   (0 would be a solution)")
    if best[1] is not None: np.save('sc2_best.npy',best[1])
