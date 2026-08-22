#!/usr/bin/env python3
"""Partial-elimination exporter: eliminate Q symbolically up to level L, keep the
rest as unknowns.  L=23 is the campaign's 43 MB degree-22 export; L=1 is the pure
bilinear form.  Everything in between is unexplored."""
import sys, time, os
sys.path.insert(0,'/tmp/hunt')
from pentev import PR, p, VARS as PVARS
import bilinear as B
degQ=B.degQ
ZERO={(j,i) for j in range(13,24) for i in range(0,j-12)}

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
def xmul(A,C):
    if not A or not C: return []
    out=[{} for _ in range(len(A)+len(C)-1)]
    for i,ai in enumerate(A):
        if not ai: continue
        for j,bj in enumerate(C):
            if bj: out[i+j]=padd(out[i+j],pmul(ai,bj))
    return out
def xadd(A,C):
    n=max(len(A),len(C))
    return [padd(A[i] if i<len(A) else {}, C[i] if i<len(C) else {}) for i in range(n)]
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

def mono_str(m):
    return "*".join(v if e==1 else f"{v}^{e}" for v,e in m)
def poly_str(d):
    if not d: return "0"
    return "+".join((f"{c}" if not m else f"{c}*{mono_str(m)}") for m,c in d.items())

def export(L, path, jtop=23, gauges=True):
    Q=[[] for _ in range(jtop+2)]
    Q[0]=[{():1}]; Q[1]=[{},{},{():1}]
    conds=[]                       # explicit conditions from levels <= L
    for k in range(1,min(L,jtop)+1):
        acc=[]
        for a in range(1,k+1):
            b=k+1-a
            if b<1 or a>=len(P) or not P[a] or not Q[b]: continue
            acc=xadd(acc,xscal(xmul(P[a],xderiv(Q[b])),a))
            acc=xadd(acc,xscal(xmul(xderiv(P[a]),Q[b]),-(k+1-a)))
        Q[k+1]=xscal(acc,pow(k+1,p-2,p))
        # any condition slot at this level becomes an explicit equation, then is zeroed
        for d in range(0,len(Q[k+1])):
            if (k+1,d) in ZERO:
                if Q[k+1][d]: conds.append(Q[k+1][d])
                Q[k+1][d]={}
    # bilinear equations for levels above L
    eqs=[]
    qused=set()
    def qref(k,d):
        if k<=L:
            if k>=len(Q) or d<0 or d>=len(Q[k]): return ("sym", {})
            return ("sym", Q[k][d])
        if k==0: return ("sym", {():1} if d==0 else {})
        if k==1: return ("sym", {():1} if d==2 else {})
        if d<0 or d>degQ.get(k,-1) or (k,d) in ZERO: return ("sym", {})
        qused.add(f"q_{k}_{d}")
        return ("var", f"q_{k}_{d}")
    for k in range(L+1,jtop):
        for d in range(0,degQ.get(k+1,-1)+1):
            acc={}
            lhs=qref(k+1,d)
            if lhs[0]=="var": acc=padd(acc,{((lhs[1],1),):(k+1)%p})
            else: acc=padd(acc,pscal(lhs[1],k+1))
            for a in range(1,k+1):
                b=k+1-a
                if a not in PR or b<1: continue
                lo,hi=PR[a]
                for i in range(lo,hi+1):
                    pc=Pn[a][i]
                    if not pc: continue
                    m=d-i
                    qc=qref(b,m+1)
                    if qc[0]=="var": term=pmul(pc,{((qc[1],1),):1})
                    else: term=pmul(pc,qc[1]) if qc[1] else {}
                    if term: acc=padd(acc,pscal(term,-a*(m+1)))
                for i in range(0,hi):
                    pc=Pn[a][i+1] if i+1<len(Pn[a]) else {}
                    if not pc: continue
                    m=d-i
                    qc=qref(b,m)
                    if qc[0]=="var": term=pmul(pc,{((qc[1],1),):1})
                    else: term=pmul(pc,qc[1]) if qc[1] else {}
                    if term: acc=padd(acc,pscal(term,(k+1-a)*(i+1)))
            if acc: eqs.append(acc)
    allv=[v for v in PVARS]+sorted(qused, key=lambda s:(int(s.split('_')[1]),int(s.split('_')[2])))
    body=[poly_str(c) for c in conds]+[poly_str(e) for e in eqs]
    if gauges: body+= ["p_1_0+%d"%(p-1),"p_1_1+%d"%(p-1)]
    with open(path,"w") as f:
        f.write(",".join(allv)+"\n"+str(p)+"\n"+",\n".join(body)+"\n")
    nt=sum(len(c) for c in conds)+sum(len(e) for e in eqs)
    md=0
    for c in conds+eqs:
        for m in c: md=max(md,sum(e for _,e in m))
    return dict(L=L,vars=len(allv),conds=len(conds),eqs=len(eqs),terms=nt,maxdeg=md,
                bytes=os.path.getsize(path))

if __name__=="__main__":
    for L in [int(a) for a in sys.argv[1:]] or [9,11,13]:
        t0=time.time()
        r=export(L, f"/tmp/hunt/pl_L{L}.ms")
        r["secs"]=round(time.time()-t0,1)
        print(r, flush=True)
