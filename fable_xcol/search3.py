"""Vectorised numerical WITNESS SEARCH.  SEARCH HEURISTIC ONLY -- any hit is
checked exactly by verify.py; a miss proves nothing (campaign erratum P15).

Gauge-fixed (proved legitimate in gauge.py): alpha=1, r=1, so
    a8 = y^14 (y-1)^2   -> a8_16=1, a8_15=-2, a8_14=1   (3 vertices automatic)
    b12 = beta y^21 (y-1)^3 -> b12_24=beta, ..., b12_21=-beta
and rung 19 holds IDENTICALLY.  Unknowns: everything else, plus beta.
Barriers keep beta, p_8_0=a0_8, q_12_0=b0_12 away from 0.
"""
import numpy as np, sys, math
from scipy.optimize import least_squares
from fractions import Fraction as F
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
Apos={t:n for n,t in enumerate(Aidx)}; Bpos={t:len(Aidx)+n for n,t in enumerate(Bidx)}
NT=len(Aidx)+len(Bidx)
# fixed slots from the gauge
FIXED={Apos[(8,16)]:1.0, Apos[(8,15)]:-2.0, Apos[(8,14)]:1.0}
BETA_SLOT={Bpos[(12,24)]:1.0, Bpos[(12,23)]:-3.0, Bpos[(12,22)]:3.0, Bpos[(12,21)]:-1.0}
free=[n for n in range(NT) if n not in FIXED and n not in BETA_SLOT]
NF=len(free); print(f"total slots {NT}, free {NF} (+1 for beta)")
eqi=[];coef=[];ia=[];ib=[];rhs_map={}
neq=0
for d in range(-1,20):
    acc={}
    for i in range(9):
        k=d+1-i
        if not (0<=k<=12): continue
        for ja in range(loP[i],hiP[i]+1):
            for jb in range(loQ[k],hiQ[k]+1):
                c=i*jb-k*ja
                if c: acc.setdefault(ja+jb-1,[]).append((c,Apos[(i,ja)],Bpos[(k,jb)]))
    for e,lst in sorted(acc.items()):
        for c,p,q in lst: eqi.append(neq);coef.append(float(c));ia.append(p);ib.append(q)
        rhs_map[neq]=1.0 if (d==2 and e==0) else 0.0
        neq+=1
eqi=np.array(eqi);coef=np.array(coef);ia=np.array(ia);ib=np.array(ib)
rhs=np.array([rhs_map[n] for n in range(neq)])
print(f"equations {neq}, terms {len(coef)}")
def assemble(p):
    z=np.zeros(NT,dtype=complex)
    b=p[0]+1j*p[1]
    for s,v in FIXED.items(): z[s]=v
    for s,v in BETA_SLOT.items(): z[s]=v*b
    z[free]=p[2:2+NF]+1j*p[2+NF:]
    return z,b
def resid(p):
    z,b=assemble(p)
    prod=coef*z[ia]*z[ib]
    acc=np.zeros(neq,dtype=complex)
    np.add.at(acc,eqi,prod)
    acc=acc-rhs
    bar=np.array([0.2/b, 0.2/z[Apos[(0,8)]], 0.2/z[Bpos[(0,12)]]],dtype=complex)
    out=np.concatenate([acc,bar])
    return np.concatenate([out.real,out.imag])
def jac(p):
    z,b=assemble(p)
    W=np.zeros((neq+3,NT),dtype=complex)
    np.add.at(W,(eqi,ia),coef*z[ib])
    np.add.at(W,(eqi,ib),coef*z[ia])
    Wb=np.zeros((neq+3,1+NF),dtype=complex)
    for s_,v in BETA_SLOT.items(): Wb[:,0]+=W[:,s_]*v
    Wb[:,1:]=W[:,free]
    Wb[neq+0,0]+= -0.2/b**2
    Wb[neq+1,1+free.index(Apos[(0,8)])]+= -0.2/z[Apos[(0,8)]]**2
    Wb[neq+2,1+free.index(Bpos[(0,12)])]+= -0.2/z[Bpos[(0,12)]]**2
    C=np.zeros((2*(neq+3),2+2*NF))
    C[:neq+3,0]=Wb[:,0].real; C[:neq+3,1]=-Wb[:,0].imag
    C[neq+3:,0]=Wb[:,0].imag; C[neq+3:,1]=Wb[:,0].real
    C[:neq+3,2:2+NF]=Wb[:,1:].real; C[:neq+3,2+NF:]=-Wb[:,1:].imag
    C[neq+3:,2:2+NF]=Wb[:,1:].imag; C[neq+3:,2+NF:]=Wb[:,1:].real
    return C

def seed(rng,scale=0.5):
    p=np.zeros(2+2*NF)
    p[0],p[1]=rng.normal(),rng.normal()
    p[2:]=scale*rng.normal(size=2*NF)
    return p
trials=int(sys.argv[1]) if len(sys.argv)>1 else 30
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 7)
best=(1e99,None)
for t in range(trials):
    s=least_squares(resid,seed(rng),jac=jac,method='lm',max_nfev=20000,xtol=1e-15,ftol=1e-15,gtol=1e-15)
    R=resid(s.x); half=len(R)//2
    core=np.concatenate([R[:neq],R[half:half+neq]])
    val=float(np.linalg.norm(core))
    z,b=assemble(s.x)
    vm=min(abs(b),abs(z[Apos[(0,8)]]),abs(z[Bpos[(0,12)]]))
    if val<best[0]: best=(val,s.x.copy())
    print(f"trial {t:3d}: ||F||={val:.4e}  min|vtx|={vm:.3e}",flush=True)
print(f"\nBEST ||F|| = {best[0]:.6e}")
if best[1] is not None:
    z,b=assemble(best[1]); np.save('best_z2.npy',z)
    print("beta =",b," saved best_z2.npy")
