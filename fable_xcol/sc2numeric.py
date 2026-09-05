"""SUB-CASE (2): NUMERIC bottom-up ladder + search.  The direct attack.

Established structure:
  a_0 = b_0 = b_1 = 0                       (proved)
  rung d introduces a_{d-1} (d<=9) and b_d (d<=12)
  rung 2 is the ONLY nonlinear rung, and it is INHOMOGENEOUS (= 1), so it fixes
  the scale -- no bihomogeneous degeneracy, unlike the naive VARPRO search.
  rungs 3..12 are small LINEAR solves.
  rungs 13..19 introduce nothing: ~34 PURE CONDITIONS.

So: given the free parameters, running the ladder is microseconds.  The whole
problem becomes a low-dimensional search with a cheap residual.

Parametrisation of rung 2 (exact, derived earlier):
    a_1 = A(1 + 2 A B y),   b_2 = y/A + B y^2       (A != 0)
with the gauge A = 1 available.  Everything above is then linear.
"""
import numpy as np, math, sys
_last_free=[0]
from fractions import Fraction as F
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
AR={i:rg(loP[i],hiP[i]) for i in range(9)}
BR={k:rg(loQ[k],hiQ[k]) for k in range(13)}
NEWA={d:(d-1 if 0<=d-1<=8 else None) for d in range(2,20)}
NEWB={d:(d if 0<=d<=12 else None) for d in range(2,20)}

def polymul_terms(coefA, expA, coefB, expB):
    """returns dict exponent->coeff for product"""
    out={}
    for ca,ea in zip(coefA,expA):
        if ca==0: continue
        for cb,eb in zip(coefB,expB):
            if cb==0: continue
            out[ea+eb]=out.get(ea+eb,0.0)+ca*cb
    return out

def rung_terms(d, A, B, skipA=None, skipB=None):
    """dict exponent->coeff of rung d, skipping the columns named (they are unknown)"""
    acc={}
    for i in range(9):
        k=d+1-i
        if not (0<=k<=12): continue
        if (skipA is not None and i==skipA) or (skipB is not None and k==skipB): continue
        ai=A.get(i); bk=B.get(k)
        if ai is None or bk is None: continue
        ea=AR[i]; eb=BR[k]
        # i*a_i*b_k'
        for ca,xa in zip(ai,ea):
            if ca==0: continue
            for cb,xb in zip(bk,eb):
                if cb==0 or xb==0: continue
                e=xa+xb-1; acc[e]=acc.get(e,0.0)+i*ca*cb*xb
        # -k*a_i'*b_k
        for ca,xa in zip(ai,ea):
            if ca==0 or xa==0: continue
            for cb,xb in zip(bk,eb):
                if cb==0: continue
                e=xa-1+xb; acc[e]=acc.get(e,0.0)-k*ca*cb*xa
    return acc

def ladder(params):
    """params: dict of free values. returns (A,B) coefficient lists or None."""
    A={i:[0.0]*len(AR[i]) for i in range(9)}
    B={k:[0.0]*len(BR[k]) for k in range(13)}
    Av=params['A']; Bv=params['B']
    # a_1 = Av + 2 Av^2 Bv y  (support y^0..y^2)
    for idx,e in enumerate(AR[1]):
        A[1][idx] = Av if e==0 else (2*Av*Av*Bv if e==1 else 0.0)
    # b_2 = y/Av + Bv y^2 (support y^1..y^4)
    for idx,e in enumerate(BR[2]):
        B[2][idx] = (1.0/Av) if e==1 else (Bv if e==2 else 0.0)
    free_idx=0
    _last_free[0]=0
    for d in range(3,13):
        ia=NEWA[d]; kb=NEWB[d]
        unk=[]
        if ia is not None: unk+= [('a',ia,j) for j in range(len(AR[ia]))]
        if kb is not None: unk+= [('b',kb,j) for j in range(len(BR[kb]))]
        if not unk: continue
        known=rung_terms(d,A,B,skipA=ia,skipB=kb)
        exps=sorted(set(list(known.keys())+[e for e in range(0,60)]))
        # build linear system: for each output exponent, coeff
        rows={}
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a':
                i=idx; k=d+1-i
                if not (0<=k<=12) or B.get(k) is None: continue
                xa=AR[i][j]
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb!=0:
                        e=xa+xb-1; rows.setdefault(e,{}); rows[e][ui]=rows[e].get(ui,0.0)+i*cb*xb
                    if xa!=0:
                        e=xa-1+xb; rows.setdefault(e,{}); rows[e][ui]=rows[e].get(ui,0.0)-k*cb*xa
            else:
                k=idx; i=d+1-k
                if not (0<=i<=8) or A.get(i) is None: continue
                xb=BR[k][j]
                for ca,xa in zip(A[i],AR[i]):
                    if ca==0: continue
                    if xb!=0:
                        e=xa+xb-1; rows.setdefault(e,{}); rows[e][ui]=rows[e].get(ui,0.0)+i*ca*xb
                    if xa!=0:
                        e=xa-1+xb; rows.setdefault(e,{}); rows[e][ui]=rows[e].get(ui,0.0)-k*ca*xa
        allexp=sorted(set(list(rows.keys())+list(known.keys())))
        M=np.zeros((len(allexp),len(unk))); v=np.zeros(len(allexp))
        for ri,e in enumerate(allexp):
            for ui,c in rows.get(e,{}).items(): M[ri,ui]=c
            v[ri]=-known.get(e,0.0)
        sol,res,rk,sv=np.linalg.lstsq(M,v,rcond=None)
        # THE FIX: add the kernel directions, scaled by the free parameters.
        # lstsq alone returns the minimum-norm solution (= 0 on a homogeneous
        # rung), which is exactly the degenerate collapse.
        U,S,Vt=np.linalg.svd(M)
        tol=max(M.shape)*(S[0] if S.size else 0.0)*1e-12
        ns=[Vt[i] for i in range(Vt.shape[0]) if i>=S.size or S[i]<=tol]
        for vec in ns:
            key=f'f{d}_{free_idx}'; free_idx+=1
            sol=sol+params.get(key,0.0)*vec
            _last_free[0]=free_idx
        for ui,(typ,idx,j) in enumerate(unk):
            if typ=='a': A[idx][j]=sol[ui]
            else: B[idx][j]=sol[ui]
    return A,B

def nfree():
    """how many kernel parameters the ladder consumes"""
    p={'A':1.0,'B':0.3}; A,B=ladder(p); return _last_free[0]

def residual(A,B):
    """sum of squares of rungs 13..19 (pure conditions) plus rung 19 edge"""
    tot=0.0; n=0
    for d in range(13,20):
        acc=rung_terms(d,A,B)
        for e,c in acc.items():
            tot+=c*c; n+=1
    return tot,n

if __name__=='__main__':
    rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    print("free-parameter search on sub-case (2), scale fixed by rung 2")
    best=(1e99,None)
    for t in range(int(sys.argv[2]) if len(sys.argv)>2 else 200):
        p={'A':rng.normal()or 1.0,'B':rng.normal()}
        try:
            A,B=ladder(p)
        except Exception as ex:
            continue
        r,n=residual(A,B)
        if r<best[0]: best=(r,dict(p))
        if t<3 or r<best[0]*1.0001:
            print(f"  trial {t:4d}: ||rungs 13-19||^2 = {r:.6e} over {n} conditions")
    print(f"\nBEST = {best[0]:.6e} at {best[1]}")
    print("NOTE: with only (A,B) free the ladder is fully determined, so this")
    print("measures whether the 2-parameter bottom family can satisfy the top.")
