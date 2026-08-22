import sys, random
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, EARLY, LATE, p

random.seed(3)
# Is the system affine in the 13 late parameters?  Test: along a random line in
# late-space, each condition must be a degree-<=1 polynomial in t.
def deg_in_t(early, direction, base, npts=6):
    ys=[]
    for t in range(npts):
        val=dict(early)
        for k,v in enumerate(LATE): val[v]=(base[k]+t*direction[k])%p
        ys.append(conditions(val))
    # finite differences: 2nd difference must vanish for affine
    d2=[]
    for c in range(66):
        col=[y[c] for y in ys]
        dd=[(col[i+2]-2*col[i+1]+col[i])%p for i in range(len(col)-2)]
        d2.append(max(dd) if dd else 0)
    return d2

for trial in range(3):
    early={v:random.randrange(p) for v in EARLY}
    direction=[random.randrange(p) for _ in LATE]
    base=[random.randrange(p) for _ in LATE]
    d2=deg_in_t(early,direction,base)
    nz=[c for c in range(66) if d2[c]!=0]
    print(f"trial {trial}: conditions with NONZERO 2nd difference in late block: {len(nz)} {nz[:8]}")
print("AFFINE-IN-LATE" if not nz else "NOT AFFINE")
