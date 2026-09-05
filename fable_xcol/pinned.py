"""Pin two Newton vertices by scaling gauge; ask whether [P,Q]=x still closes."""
import numpy as np, time, sys
_ARGS=sys.argv[1:]
sys.argv=['x','none']
import truesearch as T
from scipy.optimize import least_squares
NPv=[(0,0),(1,1),(6,16),(6,18)]; NQv=[(0,0),(1,0),(9,24),(9,27)]
obj,NS,AR,BR,slots,unpack,jac=T.make_objective(NPv,NQv,6,9,1,None)
def slot(typ,idx,e):
    R=AR if typ=='a' else BR
    j=R[idx].index(e)
    for n,(t2,i2,j2) in enumerate(slots):
        if t2==typ and i2==idx and j2==j: return n
V={'p_18_6':slot('a',6,18),'p_16_6':slot('a',6,16),
   'q_27_9':slot('b',9,27),'q_24_9':slot('b',9,24)}
PIN={V['p_18_6']:1.0, V['q_27_9']:1.0}
free=[n for n in range(NS) if n not in PIN]; NF=len(free)
def expand(x):
    z=np.zeros(NS,dtype=complex)
    for n,v in PIN.items(): z[n]=v
    z[free]=x[:NF]+1j*x[NF:]
    return z
def Fr(x):
    z=expand(x)
    r=obj(np.concatenate([z.real,z.imag]))
    pen=np.array([0.02/(abs(z[V['p_16_6']])+1e-12),0.02/(abs(z[V['q_24_9']])+1e-12)])
    return np.concatenate([r,pen])
def Jr(x):
    z=expand(x)
    J=jac(np.concatenate([z.real,z.imag]))       # (2K, 2NS)
    K2=J.shape[0]//2
    cols=[free[i] for i in range(NF)]
    Jr_=np.zeros((J.shape[0]+2,2*NF))
    Jr_[:J.shape[0],:NF]=J[:,cols]
    Jr_[:J.shape[0],NF:]=J[:,[NS+c for c in cols]]
    return Jr_
rng=np.random.default_rng(int(_ARGS[0]) if len(_ARGS)>0 else 3)
best=(1e99,None)
print(f"pinned search: {NF} free complex coefficients, p_18_6 = q_27_9 = 1")
for t in range(int(_ARGS[1]) if len(_ARGS)>1 else 200):
    x0=rng.normal(size=2*NF)*0.5; t0=time.time()
    try: s=least_squares(Fr,x0,jac=Jr,method='lm',max_nfev=6000)
    except Exception: continue
    z=expand(s.x)
    v=float(np.linalg.norm(obj(np.concatenate([z.real,z.imag]))))
    vs=[abs(z[V[k]]) for k in V]
    if v<best[0]:
        best=(v,s.x.copy())
        print(f"  trial {t:3d} ({time.time()-t0:.0f}s): ||[P,Q]-x||={v:.6e}  "
              f"vmin={min(vs):.3e} vmax={max(vs):.3e}",flush=True)
        if v<1e-9 and min(vs)>1e-4:
            print("  *** CANDIDATE with all four vertices nonzero ***")
            np.save('pinned_candidate.npy',z)
print(f"\nBEST = {best[0]:.8e}")
