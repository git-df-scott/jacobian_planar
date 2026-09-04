import sys, random
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p
rnd=random.Random(23)
base={v:rnd.randrange(p) for v in VARS}
b0=conditions(base)
sup={}
for v in VARS:
    d=dict(base); d[v]=(base[v]+1)%p
    c=conditions(d)
    sup[v]={k for k in range(66) if c[k]!=b0[k]}
# condition -> variables
cv={k:[v for v in VARS if k in sup[v]] for k in range(66)}
names=[]
for j in range(13,24):
    for i in range(0,j-12): names.append(f"Q[{j}][{i}]")
print("condition : #vars   (sorted by #vars)")
order=sorted(range(66), key=lambda k: len(cv[k]))
for k in order[:14]:
    print(f"  {names[k]:>10} : {len(cv[k]):>2}   {cv[k] if len(cv[k])<=12 else cv[k][:12]+['...']}")
print("...")
print("  largest:", [(names[k],len(cv[k])) for k in order[-3:]])
