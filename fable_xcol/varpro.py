"""VARIABLE-PROJECTION WITNESS SEARCH -- the right search for this problem.

Since L_P has FULL COLUMN RANK 124, Q is determined by P.  So instead of
optimising 184 coefficients jointly (my earlier search3.py, badly conditioned),
optimise only P's 60 and solve the inner linear least squares for Q exactly at
every step:

        rho(P) = min_Q || L_P Q - x^2 ||          (linear, closed form)
        minimise rho(P) over P-space              (57 free params after gauge)

rho(P) = 0  <=>  x^2 in Image(L_P)  <=>  a pentagon point with that P.
This is the classical VARPRO method for separable least squares; nobody in this
campaign applied it.  SEARCH HEURISTIC: every hit is checked exactly by verify.py.

Gauge (proved in gauge.py): alpha = 1, r = 1, so a_8 = y^14 (y-1)^2 is FIXED and
three P-vertices are automatically nonzero.
"""
import numpy as np, math, sys
from fractions import Fraction as F
from scipy.optimize import minimize
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
print(f"rows {NR}, P coeffs {NA}, Q coeffs {NB}")
# sparse structure: for each (P-index, Q-index) -> (row, coefficient)
TRIP=[]
for ai,(i,ja) in enumerate(Aidx):
    for bi,(k,jb) in enumerate(Bidx):
        c=i*jb-k*ja
        if c==0: continue
        r=rowpos.get((i+k-1,ja+jb-1))
        if r is not None: TRIP.append((ai,bi,r,float(c)))
TRIP=np.array(TRIP,dtype=object)
pa=np.array([t[0] for t in TRIP]); pb=np.array([t[1] for t in TRIP])
pr=np.array([t[2] for t in TRIP]); pc=np.array([t[3] for t in TRIP])
rhs=np.zeros(NR,dtype=complex); rhs[rowpos[(2,0)]]=1.0
# gauge: a_8 = y^14 (y-1)^2 -> coefficients at (8,14),(8,15),(8,16) = 1,-2,1
GAUGE={Aidx.index((8,16)):1.0, Aidx.index((8,15)):-2.0, Aidx.index((8,14)):1.0}
freeP=[n for n in range(NA) if n not in GAUGE]
NF=len(freeP); print(f"free P params after gauge: {NF} complex")
VERT_P=[Aidx.index((0,8))]                 # p_8_0 must be nonzero
VERT_Q=[Bidx.index((0,12)),Bidx.index((12,21)),Bidx.index((12,24))]

def LP(pv):
    M=np.zeros((NR,NB),dtype=complex)
    np.add.at(M,(pr,pb),pc*pv[pa])
    return M

def rho(z):
    pv=np.zeros(NA,dtype=complex)
    for k,v in GAUGE.items(): pv[k]=v
    pv[freeP]=z[:NF]+1j*z[NF:]
    M=LP(pv)
    Q,res,rk,sv=np.linalg.lstsq(M,rhs,rcond=None)
    r=M@Q-rhs
    pen=0.0
    pen+=0.05/max(abs(pv[VERT_P[0]]),1e-12)**2
    for v in VERT_Q: pen+=0.05/max(abs(Q[v]),1e-12)**2
    return float(np.vdot(r,r).real)+pen, Q, pv

def obj(z): return rho(z)[0]

trials=int(sys.argv[1]) if len(sys.argv)>1 else 25
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 3)
best=(1e99,None)
for t in range(trials):
    z0=0.6*rng.normal(size=2*NF)
    r=minimize(obj,z0,method='Powell',
               options={'maxiter':40000,'maxfev':400000,'xtol':1e-12,'ftol':1e-14})
    val,Q,pv=rho(r.x)
    M=LP(pv); resid=float(np.linalg.norm(M@Q-rhs))
    if val<best[0]: best=(val,r.x.copy())
    print(f"trial {t:3d}: obj={val:.4e}  ||L_P Q - x^2||={resid:.4e}  "
          f"min|Qvtx|={min(abs(Q[v]) for v in VERT_Q):.2e}",flush=True)
print(f"\nBEST objective = {best[0]:.6e}")
if best[1] is not None:
    val,Q,pv=rho(best[1])
    np.save('varpro_P.npy',pv); np.save('varpro_Q.npy',Q)
    print("saved varpro_P.npy / varpro_Q.npy")
