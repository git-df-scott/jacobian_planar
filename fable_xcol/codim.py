"""How special must P be?  Measure the codimension of {P : x^2 in Image(L_P)}.

Facts established: L_P has full column rank 124, so Q is determined by P, and the
obstruction is the projected residual  r(P) = P_perp(x^2)  living in the
180-dimensional cokernel.  The pentagon is nonempty iff r(P) = 0 for some P.

Three measurements:
 1. Is there a UNIVERSAL obstruction -- a fixed covector n with n^T L_P = 0 for
    EVERY P and n nonzero at the x^2 row?  If yes the pentagon is empty in one
    line.  (Answer below; it is a pure combinatorial statement about which output
    monomials are reachable.)
 2. rank of d r / d P at random P.  If it is full (= #free P params), the image
    of P-space is a submanifold of the cokernel of that dimension, and hitting 0
    has codimension 180 - rank.
 3. which single output monomial carries the x^2 target, and how many terms feed it.
"""
import numpy as np, math
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
rowset=sorted({(i+k-1,ja+jb-1) for (i,ja) in Aidx for (k,jb) in Bidx
               if i+k-1>=0 and ja+jb-1>=0})
rowpos={r:n for n,r in enumerate(rowset)}
NR,NA,NB=len(rowset),len(Aidx),len(Bidx)

print("=== 3. which terms feed the x^2 monomial (row (2,0))? ===")
feed=[]
for ai,(i,ja) in enumerate(Aidx):
    for bi,(k,jb) in enumerate(Bidx):
        if i+k-1==2 and ja+jb-1==0:
            c=i*jb-k*ja
            feed.append(((i,ja),(k,jb),c))
for f in feed: print("   P coeff x^%d y^%d  *  Q coeff x^%d y^%d   coefficient %d"%(f[0][0],f[0][1],f[1][0],f[1][1],f[2]))
print(f"   -> exactly {len([f for f in feed if f[2]!=0])} term(s) with nonzero coefficient.")
print("   So the inhomogeneous equation is p_{0,1} * q_{1,2} = 1, satisfied by the")
print("   campaign's normalisation.  EVERY other row is homogeneous.")

print("\n=== 1. universal obstruction? ===")
hit=set()
for (i,ja) in Aidx:
    for (k,jb) in Bidx:
        if i*jb-k*ja!=0 and i+k-1>=0 and ja+jb-1>=0: hit.add((i+k-1,ja+jb-1))
print(f"   rows reachable with a nonzero structure constant: {len(hit)} of {NR}")
print(f"   is the x^2 row (2,0) reachable? {(2,0) in hit}")
print("   A universal covector must vanish on every reachable row, so it must")
print("   vanish at (2,0) too => NO universal obstruction.  (Expected: otherwise")
print("   the whole system would be trivially empty.)")

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
DER=[]
for ai in freeP:
    m=(pa==ai); DER.append((pr[m],pb[m],pc[m]))
def build(pv):
    M=np.zeros((NR,NB)); np.add.at(M,(pr,pb),pc*pv[pa]); return M
print(f"\n=== 2. rank of d(residual)/dP at random P  (free params {NF}) ===")
rng=np.random.default_rng(11)
for trial in range(4):
    pv=np.zeros(NA)
    for k,v in GAUGE.items(): pv[k]=v
    pv[freeP]=rng.normal(size=NF)
    M=build(pv)
    Q,_,_,_=np.linalg.lstsq(M,rhs,rcond=None)
    Qq,_=np.linalg.qr(M)
    J=np.zeros((NR,NF))
    for j in range(NF):
        rr,bb,cc=DER[j]
        w=np.zeros(NR); np.add.at(w,rr,cc*Q[bb])
        J[:,j]=-(w-Qq@(Qq.T@w))
    s=np.linalg.svd(J,compute_uv=False)
    rk=int((s>s[0]*1e-10).sum())
    r0=float(np.linalg.norm(M@Q-rhs))
    print(f"   trial {trial}: ||r(P)||={r0:.4f}   rank(dr/dP)={rk} of {NF}"
          f"   => codim of the zero locus ~ {NR-NB} - {rk} = {NR-NB-rk}")
print("\n   cokernel dimension = 304 - 124 = 180.  If rank(dr/dP) = 57 (full), the")
print("   image of P-space is a 57-dim submanifold of a 180-dim space, so r(P)=0")
print("   is codimension 123 -- overwhelmingly empty UNLESS r(P) is confined to a")
print("   much smaller subspace.  The next line measures exactly that.")
rs=[]
for trial in range(30):
    pv=np.zeros(NA)
    for k,v in GAUGE.items(): pv[k]=v
    pv[freeP]=rng.normal(size=NF)
    M=build(pv); Q,_,_,_=np.linalg.lstsq(M,rhs,rcond=None)
    rs.append(M@Q-rhs)
Rm=np.array(rs); sv=np.linalg.svd(Rm,compute_uv=False)
eff=int((sv>sv[0]*1e-10).sum())
print(f"   span of r(P) over 30 random P: dimension {eff} (of the 180-dim cokernel)")
print("   -> the obstruction genuinely explores a {}-dimensional space.".format(eff))
