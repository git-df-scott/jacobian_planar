import sympy as sp
from trackB1_polygon import hull_rows
x,y = sp.symbols('x y')

def lattice_pts(verts):
    R = hull_rows(verts)
    return [(i,j) for j in sorted(R) for i in range(R[j][0], R[j][1]+1)]

NP=[(0,0),(1,0),(8,14),(8,16)]
NQ=[(0,0),(2,1),(12,21),(12,24)]
LP=lattice_pts(NP); LQ=lattice_pts(NQ)
print("NP pts",len(LP),"NQ pts",len(LQ))
from collections import defaultdict
wp=defaultdict(list); wq=defaultdict(list)
for (i,j) in LP: wp[j-2*i].append((i,j))
for (i,j) in LQ: wq[j-2*i].append((i,j))
print("P w-levels:", {k:len(v) for k,v in sorted(wp.items())})
print("Q w-levels:", {k:len(v) for k,v in sorted(wq.items())})
for k in sorted(wp): print("  P w=",k,"i-range",sorted(i for i,j in wp[k])[:3],"...",sorted(i for i,j in wp[k])[-1])
for k in sorted(wq): print("  Q w=",k,"i-range",sorted(i for i,j in wq[k])[:3],"...",sorted(i for i,j in wq[k])[-1])
