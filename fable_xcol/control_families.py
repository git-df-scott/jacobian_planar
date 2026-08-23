"""POSITIVE CONTROL for the determinantal reformulation.

The campaign's degenerate families are KNOWN solutions of {P,Q}=x^2:
  Family A: P = x + f(y), deg f <= 5.
  Reason it works: in coordinates u = x+f(y) the equation becomes dQ/dy|_u = x^2,
  so Q = int (u-f(y))^2 dy is polynomial -- but it has x-degree 2, so the vertex
  q_24_12 = 0 and the point is degenerate.

So ker(L'_P) MUST be nonzero at family A.  If my rank test says otherwise, the
reformulation in FABLE_DETERMINANTAL.md is wrong.  This is the control I owed.

Also tests: family B (P = x*sigma + f, sigma = 1+lambda y, f' = sigma^2)
and random P (must stay full rank).
"""
import random, sys, math
from fractions import Fraction as F
P_MOD=(1<<31)-1
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
Apos={t:n for n,t in enumerate(Aidx)}
rowset=sorted({(i+k-1,ja+jb-1) for (i,ja) in Aidx for (k,jb) in Bidx
               if i+k-1>=0 and ja+jb-1>=0})
rowpos={r:n for n,r in enumerate(rowset)}
row20=rowpos[(2,0)]
def build(pv):
    M=[[0]*len(Bidx) for _ in rowset]
    for ai,(i,ja) in enumerate(Aidx):
        c=pv[ai]
        if c==0: continue
        for bi,(k,jb) in enumerate(Bidx):
            v=(i*jb-k*ja)%P_MOD
            if v==0: continue
            r=rowpos.get((i+k-1,ja+jb-1))
            if r is None: continue
            M[r][bi]=(M[r][bi]+c*v)%P_MOD
    return M
def rank_hom(M,drop=None):
    A=[M[r][:] for r in range(len(M)) if r!=drop]
    nr,nc=len(A),len(A[0]); rk=0
    for c in range(nc):
        piv=None
        for r in range(rk,nr):
            if A[r][c]: piv=r;break
        if piv is None: continue
        A[rk],A[piv]=A[piv],A[rk]
        inv=pow(A[rk][c],P_MOD-2,P_MOD)
        A[rk]=[(v*inv)%P_MOD for v in A[rk]]
        for r in range(nr):
            if r!=rk and A[r][c]:
                f=A[r][c]; A[r]=[(A[r][j]-f*A[rk][j])%P_MOD for j in range(nc)]
        rk+=1
        if rk==nr: break
    return rk
NB=len(Bidx)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 5)

print("=== NEGATIVE CONTROL: random P (rank must be FULL = %d) ==="%NB)
for t in range(2):
    pv=[random.randrange(1,P_MOD) for _ in Aidx]
    print(f"   rank(L'_P) = {rank_hom(build(pv),row20)}")

print("\n=== POSITIVE CONTROL: FAMILY A, P = x + f(y), deg f <= 5 ===")
print("   (a known solution, so the kernel MUST be nontrivial)")
for t in range(3):
    pv=[0]*len(Aidx)
    pv[Apos[(1,0)]]=1                        # the x term
    for j in range(1,6):                     # f(y), degree <= 5, val >= 1
        pv[Apos[(0,j)]]=random.randrange(1,P_MOD)
    r=rank_hom(build(pv),row20)
    print(f"   rank(L'_P) = {r} of {NB}   kernel dim = {NB-r}   "
          f"{'PASS (drops)' if r<NB else '*** FAIL -- reformulation is WRONG ***'}")

print("\n=== POSITIVE CONTROL: FAMILY A with deg f up to 8 (still inside N(P)) ===")
for t in range(2):
    pv=[0]*len(Aidx)
    pv[Apos[(1,0)]]=1
    for j in range(1,9):
        pv[Apos[(0,j)]]=random.randrange(1,P_MOD)
    r=rank_hom(build(pv),row20)
    print(f"   rank(L'_P) = {r} of {NB}   kernel dim = {NB-r}")

print("\n=== FAMILY B: P = x*sigma + f,  sigma = 1 + lam*y,  f' = sigma^2 ===")
for t in range(2):
    lam=random.randrange(1,P_MOD)
    pv=[0]*len(Aidx)
    pv[Apos[(1,0)]]=1; pv[Apos[(1,1)]]=lam           # x*(1+lam y)
    # f' = (1+lam y)^2 = 1 + 2 lam y + lam^2 y^2  ->  f = y + lam y^2 + lam^2 y^3/3
    inv3=pow(3,P_MOD-2,P_MOD)
    pv[Apos[(0,1)]]=1
    pv[Apos[(0,2)]]=lam
    pv[Apos[(0,3)]]=(lam*lam%P_MOD)*inv3%P_MOD
    r=rank_hom(build(pv),row20)
    print(f"   rank(L'_P) = {r} of {NB}   kernel dim = {NB-r}")

print("\n=== THE REAL QUESTION ===")
print("   The rank-drop locus CONTAINS the degenerate families.")
print("   Pentagon nonempty  <=>  that locus has another component on which the")
print("   six vertices are all nonzero.  That is now a sharply posed question")
print("   about one determinantal variety, not a 186-variable Groebner problem.")
