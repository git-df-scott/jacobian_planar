from collections import defaultdict
from trackB1_polygon import hull_rows
def lat(v):
    R=hull_rows([tuple(p) for p in v]); return [(i,j) for j in sorted(R) for i in range(R[j][0],R[j][1]+1)]
import json,math
def levels(v,u,w):
    d=defaultdict(list)
    for (i,j) in lat(v): d[u*i+w*j].append((i,j))
    return {k:len(x) for k,x in sorted(d.items())}
T=json.load(open('trackD_targets_validate.json'))[0]
NP=[tuple(p) for p in T['NP']]; NQ=[tuple(p) for p in T['NQ']]
print("validate NP",NP,"NQ",NQ,"r",T['r'])
print(" #P",len(lat(NP)),"#Q",len(lat(NQ)))
for (u,w) in [(1,-2),(-1,2)]:
    print(" weight",(u,w)," P:",levels(NP,u,w)," Q:",levels(NQ,u,w), " rhs w=",u*T['r'])
# all edge directions of both polygons -> candidate weights
def edges(v):
    # convex hull order
    import itertools
    pts=sorted(set(v))
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower=[]
    for p in pts:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0: lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(pts):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0: upper.pop()
        upper.append(p)
    h=lower[:-1]+upper[:-1]
    return [(h[k],h[(k+1)%len(h)]) for k in range(len(h))]
for nm,V in [("NP",NP),("NQ",NQ)]:
    print(nm,"edges:",[(a,b,(b[0]-a[0],b[1]-a[1])) for a,b in edges(V)])
