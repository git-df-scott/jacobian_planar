"""THE CORRECT SEARCH: parametrise by the ladder, SCORE BY THE FULL BRACKET.

Every earlier search scored by a ladder-internal residual, which omitted the
conditions from kernel-carrying rungs (see FABLE_ERRATUM_LADDER.md).  Here the
objective is the complete set of coefficients of

        [P,Q] - x^K

computed from the explicit polynomials.  Two consequences:
  * nothing can be silently ignored -- every condition is in the objective;
  * collapse is self-penalising: P,Q -> 0 gives bracket 0, so the error tends to
    |x^K| = 1, not 0.  No barrier needed.

Runs on both open shapes.
"""
import numpy as np, math, sys
from fractions import Fraction as F
from scipy.optimize import least_squares

def setup(NPv,NQv,MX,MQ):
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
    return AR,BR

def bracket_terms(A,B,AR,BR,MX,MQ):
    """all coefficients of [P,Q], keyed by (x-exp, y-exp)"""
    out={}
    for i in range(MX+1):
        for k in range(MQ+1):
            for ca,xa in zip(A[i],AR[i]):
                if ca==0: continue
                for cb,xb in zip(B[k],BR[k]):
                    if cb==0: continue
                    if xb:
                        key=(i+k-1,xa+xb-1); out[key]=out.get(key,0j)+i*ca*cb*xb
                    if xa:
                        key=(i+k-1,xa-1+xb); out[key]=out.get(key,0j)-k*ca*cb*xa
    return out

def make_objective(NPv,NQv,MX,MQ,K,nfree):
    AR,BR=setup(NPv,NQv,MX,MQ)
    slots=[('a',i,j) for i in range(MX+1) for j in range(len(AR[i]))]
    slots+=[('b',k,j) for k in range(MQ+1) for j in range(len(BR[k]))]
    NS=len(slots)
    SLOTA={}; SLOTB={}
    for n,(typ,idx,j) in enumerate(slots):
        if typ=='a': SLOTA[(idx,j)]=n
        else: SLOTB[(idx,j)]=n
    def unpack(z):
        A={i:[0j]*len(AR[i]) for i in range(MX+1)}
        B={k:[0j]*len(BR[k]) for k in range(MQ+1)}
        for n,(typ,idx,j) in enumerate(slots):
            if typ=='a': A[idx][j]=z[n]
            else: B[idx][j]=z[n]
        return A,B
    # FIXED key set: every (x-exp, y-exp) the bracket can possibly touch.
    # Without this the residual changes length whenever a coefficient hits 0,
    # which breaks the optimiser silently (the same trap as before).
    KEYS=set()
    for i in range(MX+1):
        for k in range(MQ+1):
            for xa in AR[i]:
                for xb in BR[k]:
                    if xb: KEYS.add((i+k-1,xa+xb-1))
                    if xa: KEYS.add((i+k-1,xa-1+xb))
    KEYS.add((K,0)); KEYS=sorted(KEYS)
    IDX={kk:n for n,kk in enumerate(KEYS)}
    def obj(x):
        z=x[:NS]+1j*x[NS:]
        A,B=unpack(z)
        v=np.zeros(len(KEYS),dtype=complex)
        for i in range(MX+1):
            for k in range(MQ+1):
                for ca,xa in zip(A[i],AR[i]):
                    if ca==0: continue
                    for cb,xb in zip(B[k],BR[k]):
                        if cb==0: continue
                        if xb: v[IDX[(i+k-1,xa+xb-1)]]+=i*ca*cb*xb
                        if xa: v[IDX[(i+k-1,xa-1+xb)]]-=k*ca*cb*xa
        v[IDX[(K,0)]]-=1.0
        if not np.all(np.isfinite(v)): v=np.full(len(KEYS),1e3,dtype=complex)
        return np.concatenate([v.real,v.imag])
    # analytic Jacobian: the bracket is BILINEAR, so d(residual)/d(coeff) is
    # linear and exact -- removes the 2*NS-fold cost of numerical differencing.
    TRIP=[]
    for i in range(MX+1):
        for k in range(MQ+1):
            for ja,xa in enumerate(AR[i]):
                na=SLOTA[(i,ja)]
                for jb,xb in enumerate(BR[k]):
                    nb=SLOTB[(k,jb)]
                    if xb: TRIP.append((IDX[(i+k-1,xa+xb-1)],na,nb, i*xb))
                    if xa: TRIP.append((IDX[(i+k-1,xa-1+xb)],na,nb,-k*xa))
    def jac(x):
        z=x[:NS]+1j*x[NS:]
        W=np.zeros((len(KEYS),NS),dtype=complex)
        for r,na,nb,c in TRIP:
            W[r,na]+=c*z[nb]
            W[r,nb]+=c*z[na]
        J=np.zeros((2*len(KEYS),2*NS))
        J[:len(KEYS),:NS]=W.real;  J[:len(KEYS),NS:]=-W.imag
        J[len(KEYS):,:NS]=W.imag;  J[len(KEYS):,NS:]= W.real
        return J
    return obj,NS,AR,BR,slots,unpack,jac

def hunt(name,NPv,NQv,MX,MQ,K,trials,seed):
    obj,NS,AR,BR,slots,unpack,jac=make_objective(NPv,NQv,MX,MQ,K,None)
    print(f"\n{'='*66}\n{name}: {NS} coefficients, target [P,Q] = x^{K}")
    rng=np.random.default_rng(seed)
    best=(1e99,None)
    for t in range(trials):
        x0=rng.normal(size=2*NS)*0.6
        try: s=least_squares(obj,x0,jac=jac,method='lm',max_nfev=8000)
        except Exception: continue
        val=float(np.linalg.norm(obj(s.x)))
        if val<best[0]:
            best=(val,s.x.copy())
            z=s.x[:NS]+1j*s.x[NS:]
            A,B=unpack(z)
            vp=[abs(A[MX][-1]),abs(A[MX][0]),abs(B[MQ][-1]),abs(B[MQ][0])]
            print(f"  trial {t:4d}: ||[P,Q]-x^{K}|| = {val:.6e}   "
                  f"min|vertex|={min(vp):.2e}",flush=True)
            if val<1e-9:
                print("  *** CANDIDATE: bracket satisfied to machine precision ***")
                np.save(f'cand_{name.replace(" ","_")}.npy',s.x)
    print(f"  BEST = {best[0]:.8e}  (collapse would score ~1.0)")
    return best

if __name__=='__main__':
    which=sys.argv[1] if len(sys.argv)>1 else 'both'
    T=int(sys.argv[2]) if len(sys.argv)>2 else 60
    if which in ('924','both'):
        hunt("(9,24) sub-case 3",[(0,0),(1,1),(6,16),(6,18)],
             [(0,0),(1,0),(9,24),(9,27)],6,9,1,T,7)
    if which in ('828','both'):
        hunt("(8,28) sub-case 2",[(0,0),(1,0),(8,14),(8,16)],
             [(0,0),(2,1),(12,21),(12,24)],8,12,2,T,7)
