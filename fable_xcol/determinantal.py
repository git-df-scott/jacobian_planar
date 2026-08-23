"""THE DETERMINANTAL FORMULATION -- eliminate Q entirely.

{P,Q} = x^2 is  X_P(Q) = x^2  where X_P = P_x d/dy - P_y d/dx is the Hamiltonian
vector field of P.  For FIXED P this is LINEAR in Q.  So the pentagon is NOT a
bilinear variety to Groebner: it is the locus of P for which

        x^2  lies in  Image(L_P) ,      L_P : Q-space -> polynomials

i.e.  rank[L_P | x^2] == rank[L_P].  A DETERMINANTAL condition on P's 60
coefficients -- a 60-dimensional search with a fast rank test, instead of a
184-unknown Groebner problem.  Nobody in this campaign has set it up this way.

This script measures the ranks over F_p at random P (and at structured P obeying
the forced edge data), which tells us the codimension of the solvable locus.
"""
import random, sys
P_MOD = (1 << 31) - 1   # 2147483647, prime
NP = [(0,0),(1,0),(8,14),(8,16),(0,8)]
NQ = [(0,0),(2,1),(12,21),(12,24),(0,12)]
from fractions import Fraction as F
import math
def bounds(v, imax):
    lo, hi = {}, {}
    for i in range(imax+1):
        pts = []
        for t in range(len(v)):
            (x1,y1),(x2,y2) = v[t], v[(t+1)%len(v)]
            if x1 == x2 == i: pts += [y1,y2]
            elif (x1-i)*(x2-i) <= 0 and x1 != x2: pts.append(y1 + F(y2-y1,x2-x1)*(i-x1))
        lo[i] = int(math.ceil(min(pts))); hi[i] = int(math.floor(max(pts)))
    return lo, hi
loP,hiP = bounds(NP,8); loQ,hiQ = bounds(NQ,12)
loP[0] = max(loP[0],1); loQ[0] = max(loQ[0],1)
Aidx = [(i,j) for i in range(9) for j in range(loP[i],hiP[i]+1)]
Bidx = [(k,j) for k in range(13) for j in range(loQ[k],hiQ[k]+1)]
print(f"P coefficients: {len(Aidx)}    Q coefficients: {len(Bidx)}")

# rung/monomial indexing for the output space
rows = {}
for (i,ja) in Aidx:
    for (k,jb) in Bidx:
        rows.setdefault((i+k-1, ja+jb-1), None)
rowlist = sorted(r for r in rows if r[0] >= 0 and r[1] >= 0)
rowpos = {r:n for n,r in enumerate(rowlist)}
print(f"output monomials (rows): {len(rowlist)}")

def build_LP(pval):
    """matrix of Q -> {P,Q}, columns indexed by Bidx, rows by (x-exp, y-exp)"""
    M = [[0]*len(Bidx) for _ in rowlist]
    for ai,(i,ja) in enumerate(Aidx):
        c = pval[ai]
        if c == 0: continue
        for bi,(k,jb) in enumerate(Bidx):
            v = (i*jb - k*ja) % P_MOD
            if v == 0: continue
            r = rowpos.get((i+k-1, ja+jb-1))
            if r is None: continue
            M[r][bi] = (M[r][bi] + c*v) % P_MOD
    return M

def rank_mod(M, extra=None):
    """Gaussian elimination mod P_MOD; extra = optional appended column"""
    A = [row[:] for row in M]
    if extra is not None:
        for r in range(len(A)): A[r] = A[r] + [extra[r]]
    nr, nc = len(A), len(A[0])
    rk = 0
    for c in range(nc):
        piv = None
        for r in range(rk, nr):
            if A[r][c]: piv = r; break
        if piv is None: continue
        A[rk], A[piv] = A[piv], A[rk]
        inv = pow(A[rk][c], P_MOD-2, P_MOD)
        A[rk] = [(v*inv) % P_MOD for v in A[rk]]
        for r in range(nr):
            if r != rk and A[r][c]:
                f = A[r][c]
                A[r] = [(A[r][j] - f*A[rk][j]) % P_MOD for j in range(nc)]
        rk += 1
        if rk == nr: break
    return rk

rhs = [0]*len(rowlist)
if (2,0) in rowpos: rhs[rowpos[(2,0)]] = 1
else: print("WARNING: x^2 not in the row space!")

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
print("\n=== generic P (uniformly random coefficients) ===")
for trial in range(3):
    pv = [random.randrange(1, P_MOD) for _ in Aidx]
    M = build_LP(pv)
    r0 = rank_mod(M); r1 = rank_mod(M, rhs)
    print(f"  trial {trial}: rank(L_P) = {r0}, rank[L_P|x^2] = {r1}, "
          f"consistent = {r0 == r1}")

print("\n=== P obeying the forced edge structure ===")
print("   a_8 = alpha*y^14*(y-r)^2  (rung-19 closed form), rest random")
for trial in range(3):
    pv = [random.randrange(1, P_MOD) for _ in Aidx]
    al = random.randrange(1, P_MOD); rr = random.randrange(1, P_MOD)
    for n,(i,j) in enumerate(Aidx):
        if i == 8:
            if j == 16: pv[n] = al
            elif j == 15: pv[n] = (-2*al*rr) % P_MOD
            elif j == 14: pv[n] = (al*rr*rr) % P_MOD
    M = build_LP(pv)
    r0 = rank_mod(M); r1 = rank_mod(M, rhs)
    print(f"  trial {trial}: rank(L_P) = {r0}, rank[L_P|x^2] = {r1}, "
          f"consistent = {r0 == r1}")
print("\nInterpretation: the number of independent conditions on P is the number")
print("of left-nullspace vectors of L_P that pair nontrivially with x^2.  If")
print("rank[L_P|x^2] = rank(L_P)+1 generically, the solvable locus is where a")
print("single determinantal condition drops -- and its codimension in P-space")
print("(60 coefficients) is what decides emptiness.")
