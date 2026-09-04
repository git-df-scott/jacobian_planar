#!/usr/bin/env python3
"""Saturated sparse search: solutions with p_1_0 = 1 and at least one OTHER
coefficient nonzero.  t = 0 recovers the degenerate witness P = x + y, so we
discard that root and keep only t != 0."""
import sys, json
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p
import sympy as sp

FREE=[v for v in VARS if v!="p_1_0"]
NP=12
X=sp.Symbol('X')

def interp(vals):
    xs=list(range(NP)); coef=vals[:]
    for j in range(1,NP):
        for i in range(NP-1,j-1,-1):
            coef[i]=(coef[i]-coef[i-1])*pow(xs[i]-xs[i-j],p-2,p)%p
    poly=[0]*NP; cur=[1]+[0]*(NP-1)
    for k in range(NP):
        for d in range(NP): poly[d]=(poly[d]+coef[k]*cur[d])%p
        new=[0]*NP
        for d in range(NP-1):
            new[d+1]=(new[d+1]+cur[d])%p
            new[d]=(new[d]-cur[d]*xs[k])%p
        cur=new
    while len(poly)>1 and poly[-1]%p==0: poly.pop()
    return poly

def nz_roots(poly):
    """nonzero roots in F_p; 'ALL' if the polynomial is identically zero."""
    if all(c%p==0 for c in poly): return "ALL"
    f=sp.Poly(list(reversed([c%p for c in poly])),X,modulus=p)
    if f.degree()<1: return set()
    out=set()
    for r,_ in sp.factor_list(f,modulus=p)[1]:
        pr=sp.Poly(r,X)
        if pr.degree()==1:
            a,b=pr.all_coeffs()
            root=(-int(b)*pow(int(a),p-2,p))%p
            if root: out.add(root)
    return out

cands=[]
allzero=[]
for v in FREE:
    vals=[]
    for t in range(NP):
        d={u:0 for u in VARS}; d["p_1_0"]=1; d[v]=t
        vals.append(conditions(d))
    sets=[]; dead=False
    for c in range(66):
        r=nz_roots(interp([vals[t][c] for t in range(NP)]))
        if r=="ALL": continue
        if not r: dead=True; break
        sets.append(r)
    if dead: continue
    common=set.intersection(*sets) if sets else "ANY"
    if common=="ANY":
        allzero.append(v)
    elif common:
        cands.append((v,sorted(common)[:5]))
        print(f"*** CANDIDATE {v} = {sorted(common)[:5]} ***", flush=True)

print(f"scanned {len(FREE)} one-parameter families through the degenerate witness")
print(f"  families where ALL 66 conditions vanish identically in t: {len(allzero)}")
if allzero: print("   ->",allzero)
print(f"  families with an isolated nonzero root: {len(cands)}")
json.dump({"identically_zero":allzero,"isolated":cands},open('/tmp/hunt/sat_S1.json','w'))
