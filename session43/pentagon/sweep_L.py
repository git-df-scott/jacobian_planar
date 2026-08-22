#!/usr/bin/env python3
"""Find the sweet spot between the two extremes.

L = 23 : full elimination  -> 59 vars, degree 22, 1,080,147 terms (msolve OOM)
L =  1 : no elimination    -> 180 vars, degree 2, 4,736 terms   (both engines time out)

Eliminate Q symbolically up to level L, keep q as unknowns above it, and MEASURE
(vars, equations, degree, terms) rather than guessing.  Example 14, done properly.
"""
import sys, time
sys.path.insert(0,'/tmp/hunt')
from pentev import PR, p, VARS as PVARS
import bilinear as B
degQ=B.degQ
ZERO={(j,i) for j in range(13,24) for i in range(0,j-12)}
VIDX={v:k for k,v in enumerate(PVARS)}

def pmul(a,b):
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            d=dict(ma)
            for v,e in mb: d[v]=d.get(v,0)+e
            m=tuple(sorted(d.items()))
            c=(out.get(m,0)+ca*cb)%p
            if c: out[m]=c
            elif m in out: del out[m]
    return out
def padd(a,b):
    out=dict(a)
    for m,c in b.items():
        cc=(out.get(m,0)+c)%p
        if cc: out[m]=cc
        elif m in out: del out[m]
    return out
def pscal(a,c):
    c%=p
    return {m:(v*c)%p for m,v in a.items()} if c else {}
def xmul(A,B_):
    if not A or not B_: return []
    out=[{} for _ in range(len(A)+len(B_)-1)]
    for i,ai in enumerate(A):
        if not ai: continue
        for j,bj in enumerate(B_):
            if bj: out[i+j]=padd(out[i+j],pmul(ai,bj))
    return out
def xadd(A,B_):
    n=max(len(A),len(B_))
    return [padd(A[i] if i<len(A) else {}, B_[i] if i<len(B_) else {}) for i in range(n)]
def xscal(A,c): return [pscal(a,c) for a in A]
def xderiv(A): return [pscal(A[i],i) for i in range(1,len(A))] if len(A)>1 else []

Pn={}
for j in sorted(PR):
    lo,hi=PR[j]; row=[{} for _ in range(hi+1)]
    for i in range(lo,hi+1):
        if (j,i)==(0,0): row[i]={}
        elif (j,i)==(0,1): row[i]={():1}
        else: row[i]={((f"p_{j}_{i}",1),):1}
    Pn[j]=row
P=[Pn.get(j,[]) for j in range(25)]

def profile(L, jtop=23):
    Q=[[] for _ in range(jtop+2)]
    Q[0]=[{():1}]; Q[1]=[{},{},{():1}]
    t0=time.time()
    for k in range(1,min(L,jtop)+1):     # symbolic elimination up to level L
        acc=[]
        for a in range(1,k+1):
            b=k+1-a
            if b<1 or a>=len(P) or not P[a] or not Q[b]: continue
            acc=xadd(acc,xscal(xmul(P[a],xderiv(Q[b])),a))
            acc=xadd(acc,xscal(xmul(xderiv(P[a]),Q[b]),-(k+1-a)))
        Q[k+1]=xscal(acc,pow(k+1,p-2,p))
        if time.time()-t0>60: return None
    # equations for levels above L, with q's as fresh variables
    nq=0; eqs=0; terms=0; maxdeg=0
    for k in range(L+1,jtop):
        for d in range(0,degQ.get(k+1,-1)+1):
            eqs+=1
    for k in range(L+1,jtop+1):
        for d in range(0,degQ.get(k,-1)+1):
            if (k,d) not in ZERO: nq+=1
    # size of the symbolic tail actually used (levels <= L feeding equations above L)
    used_terms=0; used_deg=0
    for b in range(1,L+1):
        for c in Q[b]:
            used_terms+=len(c)
            for m in c: used_deg=max(used_deg,sum(e for _,e in m))
    nvars=len(PVARS)+nq
    # each equation above L couples P (deg 1) with either a symbolic Q (deg used_deg) or a q var
    maxdeg=max(2, 1+used_deg)
    return dict(L=L, nvars=nvars, nq=nq, eqs=eqs, sym_terms=used_terms,
                maxdeg=maxdeg, secs=round(time.time()-t0,1))

print(f"{'L':>3} {'vars':>6} {'q-vars':>7} {'eqs':>5} {'symbolic terms':>15} {'maxdeg':>7} {'secs':>6}")
for L in [1,3,5,7,9,11,12,13,14,15,16]:
    r=profile(L)
    if r is None: print(f"{L:>3}   (symbolic elimination exceeded 60 s)"); break
    print(f"{r['L']:>3} {r['nvars']:>6} {r['nq']:>7} {r['eqs']:>5} {r['sym_terms']:>15,} {r['maxdeg']:>7} {r['secs']:>6}")
