"""THE DEFORMATION LIFT, with the right instrument.

At P0 in family A, ker(L'_P0) = span{Q0}, dim 1.  The rank-drop locus persists
to first order along P1 iff there is Q1 with

        L'_{P0} Q1 + L'_{P1} Q0 = 0      i.e.   L'_{P1} Q0  in  Image(L'_{P0}).

Since L'_{P1} is LINEAR in P1, that is a linear condition on P1: the tangent
space to the rank-drop locus at P0 is the kernel of

        P1  |-->  Pi_perp ( L'_{P1} Q0 )        (a 180 x 60 linear map)

Compute its dimension, and -- the whole point -- whether any tangent direction
switches ON the vertices  p_8_0 = a_{0,8},  p_14_8 = a_{8,14},  p_16_8 = a_{8,16},
all of which VANISH on family A.  CODEX-004 reported such directions exist and
nobody followed them.  This settles it exactly, over Q, at a specific point.
"""
import sympy as sp, math, sys
from sympy import Rational as R
NP=[(0,0),(1,0),(8,14),(8,16),(0,8)]; NQ=[(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+R(y2-y1,x2-x1)*(i-x1))
        lo[i]=int(sp.ceiling(min(pts))); hi[i]=int(sp.floor(max(pts)))
    return lo,hi
loP,hiP=bounds(NP,8); loQ,hiQ=bounds(NQ,12); loP[0]=max(loP[0],1); loQ[0]=max(loQ[0],1)
Aidx=[(i,j) for i in range(9) for j in range(loP[i],hiP[i]+1)]
Bidx=[(k,j) for k in range(13) for j in range(loQ[k],hiQ[k]+1)]
Apos={t:n for n,t in enumerate(Aidx)}; Bpos={t:n for n,t in enumerate(Bidx)}
rowset=sorted({(i+k-1,ja+jb-1) for (i,ja) in Aidx for (k,jb) in Bidx
               if i+k-1>=0 and ja+jb-1>=0})
rowpos={r:n for n,r in enumerate(rowset)}
row20=rowpos[(2,0)]
NR,NA,NB=len(rowset),len(Aidx),len(Bidx)
hom=[r for r in range(NR) if r!=row20]           # homogeneous rows
hpos={r:n for n,r in enumerate(hom)}

def Lmat(pv):
    M=sp.zeros(len(hom),NB)
    for ai,(i,ja) in enumerate(Aidx):
        c=pv[ai]
        if c==0: continue
        for bi,(k,jb) in enumerate(Bidx):
            v=i*jb-k*ja
            if v==0: continue
            r=rowpos.get((i+k-1,ja+jb-1))
            if r is None or r==row20: continue
            M[hpos[r],bi]+=c*v
    return M

# ---- the base point: family A, P = x + f(y), f = y + 2y^2 + 3y^3 + y^4 + y^5
pv0=[0]*NA
pv0[Apos[(1,0)]]=1
for j,c in zip(range(1,6),[1,2,3,1,1]): pv0[Apos[(0,j)]]=c
M0=Lmat(pv0)
ns=M0.nullspace()
print(f"base point family A: ker(L'_P0) dim = {len(ns)}")
assert len(ns)==1, "expected a 1-dimensional kernel"
Q0=ns[0]
print("kernel vector Q0 found; its x-degree support:",
      sorted({Bidx[i][0] for i in range(NB) if Q0[i]!=0}))

# ---- tangent space: P1 with Pi_perp( L'_{P1} Q0 ) = 0, i.e. L'_{P1} Q0 in Im(M0)
cols=[]
for ai in range(NA):
    e=[0]*NA; e[ai]=1
    cols.append(Lmat(e)*Q0)
Wmat=sp.Matrix.hstack(*cols)                  # (rows) x NA :  P1 -> L'_{P1} Q0
Aug=sp.Matrix.hstack(M0,Wmat)                 # [ Im(M0) | image of P1 ]
r_M0=M0.rank()
print(f"rank(M0) = {r_M0},  rank[M0 | W] = {Aug.rank()}")
# tangent = { P1 : W*P1 in col(M0) }  -> solve  M0*Q1 + W*P1 = 0
Big=sp.Matrix.hstack(M0,Wmat)
K=Big.nullspace()
print(f"solution space of  M0*Q1 + W*P1 = 0  has dim {len(K)}")
tang=[]
for v in K:
    tang.append([v[NB+a] for a in range(NA)])   # the P1 part
T=sp.Matrix(tang).T if tang else sp.zeros(NA,0)
dimT=T.rank() if tang else 0
print(f"\nTANGENT SPACE to the rank-drop locus at this point: dim = {dimT}")

# ---- do any tangent directions switch on the vertices?
VERT={'p_8_0':Apos[(0,8)], 'p_14_8':Apos[(8,14)], 'p_16_8':Apos[(8,16)]}
print("\nvertex values at the base point:",
      {k:pv0[v] for k,v in VERT.items()}, " (all zero on family A)")
print("\nCan a tangent direction make each vertex nonzero?")
for nm,idx in VERT.items():
    vals=[T[idx,c] for c in range(T.cols)]
    nz=any(v!=0 for v in vals)
    print(f"   {nm}: {'YES -- some tangent direction turns it on' if nz else 'NO -- every tangent direction keeps it ZERO'}")
allthree=[]
for c in range(T.cols):
    if all(T[VERT[n],c]!=0 for n in VERT): allthree.append(c)
print(f"\ndirections turning on ALL THREE simultaneously: {len(allthree)}")
print("\nINTERPRETATION: a vertex that every tangent direction keeps at zero cannot")
print("be switched on by a first-order deformation of this component.  If all three")
print("are pinned, family A is not connected to a nondegenerate point to first")
print("order, and the lift CODEX-004 hoped for does not exist here.")
