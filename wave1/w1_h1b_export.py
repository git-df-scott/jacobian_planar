#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 5 -- EXPORT the pentagon conditions to msolve.

WHY THIS IS NOW POSSIBLE.  Step 4c measured the actual monomial counts: the
conditions are ELEVEN ORDERS OF MAGNITUDE sparser than the dense bound
(686 monomials at level 13, not ~1e14).  So they CAN be written down, and the
campaign's long-standing assumption to the contrary -- which this session
repeated in H1B_STATUS.md before measuring -- is wrong.

WHY A SUBSYSTEM SUFFICES FOR A VERDICT.  Emptiness is monotone: if any SUBSET
of the conditions has no common zero, the full system has none.  So exporting
levels 13..J for increasing J and testing each is a sound route to EMPTY, and
the smallest J that closes is the cheapest possible verdict.

GAUGE AND ITS CAVEAT.  p_00 = 0 and p_10 = 1 are imposed (two of the three
gauges).  p_10 = 1 also encodes p_10 != 0, which the y-adic recursion requires
anyway (it divides by p_10).  An EMPTY verdict here therefore covers the
p_10 != 0 chart only; the p_10 = 0 locus is a separate branch and is recorded
as such, NOT silently absorbed.
"""
import sys, time, os
p = 1000003
OUT = "/home/user/jacobian_planar/wave1"

def P_rows(jmax=16):
    r = {}
    for j in range(jmax+1):
        lo, hi = max(0, j-8), min(8, j//2+1)
        if lo <= hi: r[j] = (lo, hi)
    return r
PR = P_rows()
PARAMS = [(j,i) for j in sorted(PR) for i in range(PR[j][0], PR[j][1]+1)]
VN = {}
for (j,i) in PARAMS:
    if (j,i) in ((0,0),(0,1)): continue
    VN[(j,i)] = f"p_{j}_{i}"
VARS = [VN[k] for k in PARAMS if k in VN]
NV = len(VARS)

def pmul(a,b,cap):
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            d=dict(ma)
            for v,e in mb: d[v]=d.get(v,0)+e
            m=tuple(sorted(d.items()))
            c=(out.get(m,0)+ca*cb)%p
            if c: out[m]=c
            elif m in out: del out[m]
    if len(out)>cap: raise MemoryError("cap")
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
def xmul(A,B,cap):
    if not A or not B: return []
    out=[{} for _ in range(len(A)+len(B)-1)]
    for i,ai in enumerate(A):
        if not ai: continue
        for j,bj in enumerate(B):
            if not bj: continue
            out[i+j]=padd(out[i+j], pmul(ai,bj,cap))
    return out
def xadd(A,B):
    n=max(len(A),len(B))
    return [padd(A[i] if i<len(A) else {}, B[i] if i<len(B) else {}) for i in range(n)]
def xscal(A,c): return [pscal(a,c) for a in A]
def xderiv(A): return [pscal(A[i], i) for i in range(1,len(A))] if len(A)>1 else []

def build(JMAX, cap=60_000_000):
    Pn={}
    for (j,i) in PARAMS:
        row=Pn.setdefault(j,[])
        while len(row)<=i: row.append({})
        if (j,i)==(0,0): row[i]={}
        elif (j,i)==(0,1): row[i]={():1}
        else: row[i]={((VN[(j,i)],1),):1}
    P=[Pn.get(j,[]) for j in range(JMAX+2)]
    Q=[[] for _ in range(JMAX+2)]
    Q[0]=[{():1}]; Q[1]=[{},{},{():1}]
    for k in range(1,JMAX):
        acc=[]
        for a in range(1,k+1):
            b=k+1-a
            if b<0 or a>=len(P) or not P[a]: continue
            acc=xadd(acc, xscal(xmul(P[a], xderiv(Q[b]),cap), a))
            acc=xadd(acc, xscal(xmul(xderiv(P[a]), Q[b],cap), -(k+1-a)))
        Q[k+1]=xscal(acc, pow(k+1,p-2,p))
    return Q

def mono_str(m):
    if not m: return "1"
    return "*".join(v if e==1 else f"{v}^{e}" for v,e in m)
def poly_str(P):
    return "+".join(f"{c}*{mono_str(m)}" for m,c in P.items()) if P else "0"

if __name__ == "__main__":
    JTOP = int(sys.argv[1]) if len(sys.argv)>1 else 18
    t0=time.time()
    print(f"building conditions to level {JTOP} ({NV} variables after gauges)...", flush=True)
    Q = build(JTOP)
    conds=[]
    for j in range(13, JTOP+1):
        for i in range(0, j-12):
            c = Q[j][i] if i < len(Q[j]) else {}
            conds.append(((j,i), c))
    tot=sum(len(c) for _,c in conds)
    print(f"  {len(conds)} conditions, {tot:,} monomials total, "
          f"max {max(len(c) for _,c in conds):,}   ({time.time()-t0:.0f}s)", flush=True)
    path=os.path.join(OUT, f"pent_L{JTOP}.ms")
    with open(path,"w") as f:
        f.write(",".join(VARS)+"\n"+str(p)+"\n")
        f.write(",\n".join(poly_str(c) for _,c in conds)+"\n")
    print(f"  wrote {path}  ({os.path.getsize(path)/1e6:.1f} MB)")
