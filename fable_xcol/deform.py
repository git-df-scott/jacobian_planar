"""ITEM 5, DECISIVE: are the degenerate families isolated, or limits of genuine
nondegenerate solutions?

At P0 in family A, ker(L'_P0) = span{Q0}, dim 1.  The rank-drop locus persists to
first order along P1 iff there is Q1 with

        L'_{P0} Q1  +  L'_{P1} Q0  =  0 .

L' is LINEAR in P, so this is one linear system in the unknowns (Q1, P1).  Its
solution space projected to P1 is the TANGENT SPACE to the rank-drop locus at P0.

The question that decides the hunt: does any tangent direction switch ON the
vertices that vanish on the degenerate family?
    p_8_0 = a_{0,8},  p_14_8 = a_{8,14},  p_16_8 = a_{8,16}
All are zero on family A.  If every tangent direction keeps them zero, the
family is a dead end to first order and no local search will ever escape it.

Runs mod p (exact, fast).  Both sub-cases.
"""
import random, sys, math
from fractions import Fraction as F
P_MOD = (1<<31)-1

def bounds(v,imax):
    lo,hi={},{}
    for i in range(imax+1):
        pts=[]
        for t in range(len(v)):
            (x1,y1),(x2,y2)=v[t],v[(t+1)%len(v)]
            if x1==x2==i: pts+=[y1,y2]
            elif (x1-i)*(x2-i)<=0 and x1!=x2: pts.append(y1+F(y2-y1,x2-x1)*(i-x1))
        if not pts: lo[i]=None;hi[i]=None;continue
        lo[i]=int(math.ceil(min(pts))); hi[i]=int(math.floor(max(pts)))
    return lo,hi

def rref(A,ncols):
    """in-place RREF mod P_MOD; returns list of pivot columns"""
    piv=[]; r=0; nr=len(A)
    for c in range(ncols):
        pr=None
        for i in range(r,nr):
            if A[i][c]: pr=i;break
        if pr is None: continue
        A[r],A[pr]=A[pr],A[r]
        inv=pow(A[r][c],P_MOD-2,P_MOD)
        A[r]=[(v*inv)%P_MOD for v in A[r]]
        for i in range(nr):
            if i!=r and A[i][c]:
                f=A[i][c]
                A[i]=[(A[i][j]-f*A[r][j])%P_MOD for j in range(ncols)]
        piv.append(c); r+=1
        if r==nr: break
    return piv

def nullspace(A,ncols):
    M=[row[:] for row in A]
    piv=rref(M,ncols)
    free=[c for c in range(ncols) if c not in piv]
    basis=[]
    for fc in free:
        v=[0]*ncols; v[fc]=1
        for r,pc in enumerate(piv):
            v[pc]=(-M[r][fc])%P_MOD
        basis.append(v)
    return basis

def analyse(name,NPv,NQv,fam):
    loP,hiP=bounds(NPv,8); loQ,hiQ=bounds(NQv,12)
    loP[0]=max(loP[0],1) if loP[0] is not None else None
    loQ[0]=max(loQ[0],1) if loQ[0] is not None else None
    def rg(lo,hi): return [] if lo is None or lo>hi else list(range(lo,hi+1))
    Aidx=[(i,j) for i in range(9) for j in rg(loP[i],hiP[i])]
    Bidx=[(k,j) for k in range(13) for j in rg(loQ[k],hiQ[k])]
    Apos={t:n for n,t in enumerate(Aidx)}; NA,NB=len(Aidx),len(Bidx)
    rowset=sorted({(i+k-1,ja+jb-1) for (i,ja) in Aidx for (k,jb) in Bidx
                   if i+k-1>=0 and ja+jb-1>=0})
    rowpos={r:n for n,r in enumerate(rowset)}
    row20=rowpos.get((2,0))
    hom=[r for r in range(len(rowset)) if r!=row20]; hp={r:n for n,r in enumerate(hom)}
    print(f"\n{'='*64}\n{name}: P {NA}, Q {NB}, homogeneous rows {len(hom)}")
    # structure constants
    trip=[]
    for ai,(i,ja) in enumerate(Aidx):
        for bi,(k,jb) in enumerate(Bidx):
            c=i*jb-k*ja
            if c==0: continue
            r=rowpos.get((i+k-1,ja+jb-1))
            if r is None or r==row20: continue
            trip.append((ai,bi,hp[r],c%P_MOD))
    def Lmat(pv):
        M=[[0]*NB for _ in hom]
        for ai,bi,r,c in trip:
            if pv[ai]: M[r][bi]=(M[r][bi]+pv[ai]*c)%P_MOD
        return M
    # base point: family A, P = x + f(y)
    pv0=[0]*NA
    if (1,0) in Apos: pv0[Apos[(1,0)]]=1
    else: print("  (no (1,0) coefficient in this support)"); return
    random.seed(3)
    for j in fam:
        if (0,j) in Apos: pv0[Apos[(0,j)]]=random.randrange(1,P_MOD)
    M0=Lmat(pv0)
    ns0=nullspace([r[:] for r in M0],NB)
    print(f"  base point (family A, deg f <= {max(fam) if fam else 0}): ker dim = {len(ns0)}")
    if len(ns0)!=1:
        print("  -> not a rank-1 drop here; skipping tangent analysis"); return
    Q0=ns0[0]
    # joint system: [ M0 | W ] (Q1, P1) = 0  where W[:,ai] = (dL/dp_ai) Q0
    W=[[0]*NA for _ in hom]
    for ai,bi,r,c in trip:
        if Q0[bi]: W[r][ai]=(W[r][ai]+c*Q0[bi])%P_MOD
    Big=[M0[r]+W[r] for r in range(len(hom))]
    nsB=nullspace(Big,NB+NA)
    tang=[v[NB:] for v in nsB]
    T=[row[:] for row in tang]
    piv=rref([row[:] for row in T],NA) if T else []
    print(f"  tangent space to the rank-drop locus: dim = {len(piv)} (of {NA} P-coords)")
    VERT={'p_8_0':(0,8),'p_14_8':(8,14),'p_16_8':(8,16)}
    for nm,key in VERT.items():
        if key not in Apos: print(f"    {nm}: not in this support"); continue
        idx=Apos[key]
        nz=any(v[idx] for v in tang)
        print(f"    {nm} (value {pv0[idx]} at base): "
              f"{'CAN be switched on' if nz else '*** PINNED AT ZERO by every tangent direction ***'}")
    allon=sum(1 for v in tang if all(v[Apos[k]] for k in VERT.values() if k in Apos))
    print(f"    directions turning on ALL vertices at once: {allon}")

analyse("SUB-CASE (1) pentagon",
        [(0,0),(1,0),(8,14),(8,16),(0,8)],[(0,0),(2,1),(12,21),(12,24),(0,12)],
        range(1,6))
analyse("SUB-CASE (2) quadrilateral",
        [(0,0),(1,0),(8,14),(8,16)],[(0,0),(2,1),(12,21),(12,24)],
        range(1,3))
