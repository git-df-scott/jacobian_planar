import sys, random
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p

rnd=random.Random(17)
base={v:rnd.randrange(p) for v in VARS}
def degree_in(var, npts=10):
    ys=[]
    for t in range(npts):
        d=dict(base); d[var]=(base[var]+t)%p
        ys.append(conditions(d))
    best=0
    for c in range(66):
        col=[y[c] for y in ys]
        # successive finite differences; degree = last order with nonzero diff
        deg=0
        cur=col[:]
        for order in range(1,npts):
            cur=[(cur[i+1]-cur[i])%p for i in range(len(cur)-1)]
            if any(x!=0 for x in cur): deg=order
            else: break
        best=max(best,deg)
    return best
prof={}
for v in VARS:
    prof[v]=degree_in(v)
from collections import Counter
print("degree histogram over the 59 variables:",dict(sorted(Counter(prof.values()).items())))
lin=[v for v in VARS if prof[v]<=1]
print("variables entering AFFINELY (deg<=1):",len(lin))
print(sorted(lin))
print("\nper-variable degrees:")
for v in VARS: print(f"  {v}: {prof[v]}", end="")
print()
