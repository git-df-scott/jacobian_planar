"""VARPRO witness search, real arithmetic + analytic Kaufman Jacobian.

L_P has full column rank, so Q = argmin ||L_P Q - x^2|| is unique and
    r(P) = L_P Q*(P) - x^2 = -(I - L_P L_P^+) x^2
depends only on P.  Because L_P is LINEAR in P, each dL/dp_j is a CONSTANT
sparse matrix, so the Kaufman Jacobian  J_j = -P_perp (dL/dp_j) Q*  is cheap.

57 real free parameters after the gauge alpha = r = 1.  SEARCH HEURISTIC:
any hit is verified exactly by verify.py.
"""
import numpy as np, math, sys
from fractions import Fraction as F
from scipy.optimize import least_squares
NP=[(0,0),(1,0),(8,14),(8,16),(0,8)]; NQ=[(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+F(y2-y1,x2-x1)*(i-x1))
        lo[i]=int(math.ceil(min(pts))); hi[i]=int(math.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12); loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
Aidx=[(i,j) for i in range(9) for j in range(loP[i],hiP[i]+1)]
Bidx=[(k,j) for k in range(13) for j in range(loQ[k],hiQ[k]+1)]
rowset=sorted({(i+k-1,ja+jb-1) for (i,ja) in Aidx for (k,jb) in Bidx
               if i+k-1>=0 and ja+jb-1>=0})
rowpos={r:n for n,r in enumerate(rowset)}
NR,NA,NB=len(rowset),len(Aidx),len(Bidx)
pa=[];pb=[];pr=[];pc=[]
for ai,(i,ja) in enumerate(Aidx):
    for bi,(k,jb) in enumerate(Bidx):
        c=i*jb-k*ja
        if c==0: continue
        r=rowpos.get((i+k-1,ja+jb-1))
        if r is not None: pa.append(ai);pb.append(bi);pr.append(r);pc.append(float(c))
pa=np.array(pa);pb=np.array(pb);pr=np.array(pr);pc=np.array(pc)
rhs=np.zeros(NR); rhs[rowpos[(2,0)]]=1.0
GAUGE={Aidx.index((8,16)):1.0,Aidx.index((8,15)):-2.0,Aidx.index((8,14)):1.0}
freeP=[n for n in range(NA) if n not in GAUGE]; NF=len(freeP)
print(f"rows {NR}, P {NA}, Q {NB}; free real params {NF}")
VP=Aidx.index((0,8)); VQ=[Bidx.index((0,12)),Bidx.index((12,21)),Bidx.index((12,24))]
# constant derivative matrices dL/dp_j, stored as index lists per free param
DER=[]
for j,ai in enumerate(freeP):
    m=(pa==ai); DER.append((pr[m],pb[m],pc[m]))
def build(pv):
    M=np.zeros((NR,NB))
    np.add.at(M,(pr,pb),pc*pv[pa])
    return M
def full(z):
    pv=np.zeros(NA)
    for k,v in GAUGE.items(): pv[k]=v
    pv[freeP]=z
    return pv
EPS=0.05
def resid(z):
    pv=full(z); M=build(pv)
    Q,_,_,_=np.linalg.lstsq(M,rhs,rcond=None)
    r=M@Q-rhs
    bar=np.array([EPS/max(abs(pv[VP]),1e-9)]+[EPS/max(abs(Q[v]),1e-9) for v in VQ])
    return np.concatenate([r,bar])
def jac(z):
    pv=full(z); M=build(pv)
    Q,_,_,_=np.linalg.lstsq(M,rhs,rcond=None)
    Qq,Rr=np.linalg.qr(M)                     # P_perp = I - Qq Qq^T
    J=np.zeros((NR+4,NF))
    for j in range(NF):
        rr,bb,cc=DER[j]
        w=np.zeros(NR); np.add.at(w,rr,cc*Q[bb])   # (dL/dp_j) Q
        J[:NR,j]=-(w-Qq@(Qq.T@w))
    return J
trials=int(sys.argv[1]) if len(sys.argv)>1 else 40
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 5)
best=(1e99,None)
for t in range(trials):
    z0=0.7*rng.normal(size=NF)
    s=least_squares(resid,z0,jac=jac,method='lm',max_nfev=6000,xtol=1e-15,ftol=1e-15,gtol=1e-15)
    R=resid(s.x); core=float(np.linalg.norm(R[:NR]))
    pv=full(s.x); M=build(pv); Q,_,_,_=np.linalg.lstsq(M,rhs,rcond=None)
    if core<best[0]: best=(core,s.x.copy())
    print(f"trial {t:3d}: ||L_P Q - x^2|| = {core:.6e}   min|Qvtx|={min(abs(Q[v]) for v in VQ):.2e}",flush=True)
print(f"\nBEST ||residual|| = {best[0]:.8e}")
if best[1] is not None:
    pv=full(best[1]); M=build(pv); Q,_,_,_=np.linalg.lstsq(M,rhs,rcond=None)
    np.save('vp_P.npy',pv); np.save('vp_Q.npy',Q); print("saved vp_P.npy vp_Q.npy")
