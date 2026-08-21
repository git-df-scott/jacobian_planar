#!/usr/bin/env python3
"""Extract every F_p-rational bottom-edge seed at one prime, VERIFY each against
all 17 equations, and classify it by the side conditions c_8_14, d_12_21 != 0."""
import re, sys, sympy as sp, json, os
p=int(sys.argv[1]); fn=f"wave6/bottomedge/be_p{p}.out"
if not os.path.exists(fn) or os.path.getsize(fn)==0:
    print(f"p={p} NO OUTPUT (timeout/crash) - not a verdict"); sys.exit()
w=sp.Symbol('w')
C=[sp.Symbol(f'c{i}') for i in range(1,9)]; D=[sp.Symbol(f'd{j}') for j in range(3,13)]
f=sum(C[i-1]*w**i for i in range(1,9)); g=w**2+sum(D[j-3]*w**j for j in range(3,13))
E=sp.expand(2*f*sp.diff(g,w)-3*sp.diff(f,w)*g-w**2)
eqs=[sp.expand(v) for k,v in sp.Poly(E,w).as_dict().items() if sp.expand(v)!=0]
t=open(fn).read()
if t.strip().startswith('[-1]'): print(f"p={p} EMPTY"); sys.exit()
vn=[v.strip().strip("'") for v in re.search(r"\[('c1'.*?'A')\]", t, re.S).group(1).split(',')]
b=re.findall(r"\[(\d+),\s*\n?\s*\[([0-9,\s]+)\]\]", t)
b=[(int(d),[int(c) for c in cs.replace('\n','').split(',') if c.strip()]) for d,cs in b]
dg,wco=b[0]; params=b[2:]
rts=[x for x in range(p) if sum(c*pow(x,i,p) for i,c in enumerate(wco))%p==0]
adm=deg=bad=0
for x in rts:
    pt={nm:(-sum(c*pow(x,i,p) for i,c in enumerate(co)))%p for nm,(d_,co) in zip(vn,params)}
    sub={sp.Symbol(k):v for k,v in pt.items()}
    if not all(int(sp.expand(e).subs(sub))%p==0 for e in eqs): bad+=1; continue
    if pt['c1']%p and pt['c8']%p and pt['d12']%p: adm+=1
    else: deg+=1
print(f"p={p} elim_deg={dg} rational={len(rts)}/9 admissible={adm} degenerate={deg} verify_fail={bad}")
