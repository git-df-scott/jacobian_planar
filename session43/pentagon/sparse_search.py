#!/usr/bin/env python3
"""Sparse structured search: the needle-in-haystack fix.

Uniform random points miss a codimension-52 locus with probability ~1.  But a
Newton-polygon solution, if one exists, is plausibly SPARSE.  So: pin the gauge
p_1_0 = 1, let a small subset S of the other 58 variables be free, set the rest
to zero, and decide those tiny systems exactly.

|S| = 0 : one evaluation.
|S| = 1 : each condition is a univariate polynomial of degree <= 9; interpolate
          it exactly and intersect the root sets over all 66 conditions.
|S| = 2 : bivariate; solved by resultant of two conditions, then verified.

A hit is a genuine point of the full system (nothing is relaxed), so this is
asymmetric: NONEMPTY is a witness, EMPTY on a family says nothing about others.
"""
import sys, itertools, json
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p

FREE=[v for v in VARS if v!="p_1_0"]

def base():
    d={v:0 for v in VARS}; d["p_1_0"]=1; return d

def interp(vals, npts):
    xs=list(range(npts)); coef=vals[:]
    for j in range(1,npts):
        for i in range(npts-1,j-1,-1):
            coef[i]=(coef[i]-coef[i-1])*pow(xs[i]-xs[i-j],p-2,p)%p
    poly=[0]*(npts); cur=[1]+[0]*(npts-1)
    for k in range(npts):
        for d_ in range(npts): poly[d_]=(poly[d_]+coef[k]*cur[d_])%p
        new=[0]*npts
        for d_ in range(npts-1):
            new[d_+1]=(new[d_+1]+cur[d_])%p
            new[d_]=(new[d_]-cur[d_]*xs[k])%p
        cur=new
    while len(poly)>1 and poly[-1]==0: poly.pop()
    return poly

def roots(poly):
    """roots in F_p of a low-degree poly, by trial over a small set is impossible;
    use gcd with x^p - x via repeated squaring -> then factor by brute force on
    the (tiny) degree.  Here: just find roots by evaluating a Cantor-Zassenhaus
    style gcd; for deg<=9 we do it by computing gcd(f, x^p-x) then root-finding."""
    import sympy as sp
    x=sp.Symbol('x')
    f=sp.Poly(list(reversed(poly)),x,modulus=p)
    if f.degree()<1: return None if any(c%p for c in poly) else "ALL"
    rs=[]
    for r,_ in sp.factor_list(f, modulus=p)[1]:
        if sp.Poly(r,x).degree()==1:
            c=sp.Poly(r,x).all_coeffs()
            rs.append((-c[1]*pow(int(c[0]),p-2,p))%p)
    return rs

# ---- |S| = 0
b=base()
c0=conditions(b)
nz=[i for i,v in enumerate(c0) if v%p]
print(f"|S|=0  (P = x + y): {66-len(nz)}/66 conditions vanish", flush=True)
if not nz:
    print("*** WITNESS at |S|=0 ***"); json.dump(b,open('/tmp/hunt/HIT_S0.json','w')); sys.exit()

# ---- |S| = 1
NP=11
hits=[]
best=(0,None)
for v in FREE:
    vals=[]
    for t in range(NP):
        d=base(); d[v]=t
        vals.append(conditions(d))
    common=None; ok=True
    percond=[]
    for c in range(66):
        poly=interp([vals[t][c] for t in range(NP)],NP)
        r=roots(poly)
        if r=="ALL": continue
        if r is None or r==[]: ok=False; break
        percond.append(set(r))
    if not ok: continue
    common=set.intersection(*percond) if percond else {"ANY"}
    common={r for r in common if r!=0} if common!={"ANY"} else common
    if common:
        hits.append((v,sorted(common)))
        print(f"*** |S|=1 CANDIDATE: {v} = {sorted(common)} ***", flush=True)
print(f"|S|=1  families scanned: {len(FREE)}   candidates: {len(hits)}", flush=True)
if hits: json.dump(hits,open('/tmp/hunt/HIT_S1.json','w'))
