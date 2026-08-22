#!/usr/bin/env python3
"""Export the pentagon system in its BILINEAR form, keeping Q as unknowns.

{P,Q} = x^2 is degree 2 in the coefficients of (P,Q).  The 43 MB degree-22
export exists only because the recursion was used to eliminate Q.  Here every
q-coefficient is an unknown and every equation is the recursion step

  (k+1) q_{k+1,d} = sum_a [ a*(P[a]*Q[b]')_d - (k+1-a)*(P[a]'*Q[b])_d ],  b=k+1-a

which is bilinear (one p times one q per term).  The Newton-polygon conditions
q_{j,i} = 0 for j=13..23, i<=j-13 are imposed by SUBSTITUTING ZERO, so they cost
no equations and remove 66 unknowns.
"""
import sys, random
sys.path.insert(0,'/tmp/hunt')
from pentev import PR, p, VARS as PVARS

degP = {j: PR[j][1] for j in PR}
degQ = {0:0, 1:2}
for k in range(1,24):
    best=-1
    for a in range(1,k+1):
        b=k+1-a
        if a not in degP or b not in degQ or degQ[b]<1: continue
        best=max(best, degP[a]+degQ[b]-1)
        if degP[a]>=1: best=max(best,(degP[a]-1)+degQ[b])
    degQ[k+1]=best

ZERO_FULL = {(j,i) for j in range(13,24) for i in range(0, j-12)}
ZERO = ZERO_FULL

def pterm(j,i):
    """symbol or constant for P[j] coefficient of x^i"""
    if (j,i)==(0,0): return ("c",0)
    if (j,i)==(0,1): return ("c",1)
    if j in PR and PR[j][0]<=i<=PR[j][1]: return ("v",f"p_{j}_{i}")
    return ("c",0)

def qterm(k,d):
    if k==0: return ("c",1 if d==0 else 0)
    if k==1: return ("c",1 if d==2 else 0)
    if d<0 or d>degQ.get(k,-1): return ("c",0)
    if (k,d) in ZERO: return ("c",0)
    return ("v",f"q_{k}_{d}")

QVARS=[f"q_{k}_{d}" for k in range(2,24) for d in range(0,degQ[k]+1) if (k,d) not in ZERO]
ALLVARS=PVARS+QVARS

def build_equations(zero=None):
    global ZERO
    ZERO = ZERO_FULL if zero is None else zero
    eqs=[]
    for k in range(1,23):
        for d in range(0, degQ[k+1]+1):
            terms=[]   # list of (coeff, [vars])
            lhs=qterm(k+1,d)
            if lhs[0]=="v": terms.append(((k+1)%p,[lhs[1]]))
            else:
                if lhs[1]%p: terms.append((((k+1)*lhs[1])%p,[]))
            for a in range(1,k+1):
                b=k+1-a
                if a not in PR or b<1: continue
                lo,hi=PR[a]
                for i in range(lo,hi+1):
                    P=pterm(a,i)
                    if P[0]=="c" and P[1]%p==0: continue
                    # term  - a * P[a]_i * (m+1) q_{b,m+1}   with i+m=d
                    m=d-i
                    Qc=qterm(b,m+1)
                    if not(Qc[0]=="c" and Qc[1]%p==0):
                        co=(-a*(m+1))%p
                        if P[0]=="c": co=co*P[1]%p
                        if Qc[0]=="c": co=co*Qc[1]%p
                        vs=([P[1]] if P[0]=="v" else [])+([Qc[1]] if Qc[0]=="v" else [])
                        if co%p: terms.append((co%p,vs))
                    # term  + (k+1-a) * (i+1) P[a]_{i+1} * q_{b,m}   with (i+1-1)+m=d -> handled below
            # second sum, indexed cleanly:  + (k+1-a) * sum_{i+m=d} (i+1)P[a]_{i+1} q_{b,m}
            for a in range(1,k+1):
                b=k+1-a
                if a not in PR or b<1: continue
                lo,hi=PR[a]
                for i in range(0,hi):
                    P=pterm(a,i+1)
                    if P[0]=="c" and P[1]%p==0: continue
                    m=d-i
                    Qc=qterm(b,m)
                    if Qc[0]=="c" and Qc[1]%p==0: continue
                    co=((k+1-a)*(i+1))%p
                    if P[0]=="c": co=co*P[1]%p
                    if Qc[0]=="c": co=co*Qc[1]%p
                    vs=([P[1]] if P[0]=="v" else [])+([Qc[1]] if Qc[0]=="v" else [])
                    if co%p: terms.append((co%p,vs))
            agg={}
            for co,vs in terms:
                key=tuple(sorted(vs))
                agg[key]=(agg.get(key,0)+co)%p
            agg={kk:vv for kk,vv in agg.items() if vv%p}
            if agg: eqs.append(agg)
    return eqs

def eq_str(agg):
    parts=[]
    for vs,co in agg.items():
        parts.append(f"{co}" + ("".join("*"+v for v in vs)))
    return "+".join(parts)

if __name__=="__main__":
    import builtins
    eqs_ctl=build_equations(set())
    eqs=build_equations()
    print("q-variables:",len(QVARS)," total variables:",len(ALLVARS)," equations:",len(eqs))
    mx=max(len(a) for a in eqs); tot=sum(len(a) for a in eqs)
    print("max terms in an equation:",mx," total terms:",tot)
    deg=max(max(len(vs) for vs in a) for a in eqs)
    print("max total degree:",deg)
    # POSITIVE CONTROL: random p -> recursion q must satisfy every equation
    import pentev
    rnd=random.Random(77)
    vals={v:rnd.randrange(p) for v in PVARS}
    P=[]
    for j in range(25):
        if j not in PR: P.append([]); continue
        lo,hi=PR[j]; row=[0]*(hi+1)
        for i in range(lo,hi+1):
            row[i]=0 if (j,i)==(0,0) else (1 if (j,i)==(0,1) else vals[f"p_{j}_{i}"]%p)
        P.append(row)
    Q=[[] for _ in range(25)]; Q[0]=[1]; Q[1]=[0,0,1]
    for k in range(1,24):
        acc=[]
        for a in range(1,k+1):
            b=k+1-a
            if b<0 or a>=len(P) or not P[a] or not Q[b]: continue
            acc=pentev.xadd(acc,pentev.xscal(pentev.xmul(P[a],pentev.xderiv(Q[b])),a))
            acc=pentev.xadd(acc,pentev.xscal(pentev.xmul(pentev.xderiv(P[a]),Q[b]),-(k+1-a)))
        Q[k+1]=pentev.xscal(acc,pow(k+1,p-2,p))
    full=dict(vals)
    for k in range(2,24):
        for d in range(0,degQ[k]+1):
            full[f"q_{k}_{d}"]=(Q[k][d] if d<len(Q[k]) else 0)%p
    bad=0
    for a in eqs_ctl:
        s=0
        for vs,co in a.items():
            t=co
            for v in vs: t=t*full[v]%p
            s=(s+t)%p
        if s%p: bad+=1
    print("POSITIVE CONTROL (random P, recursion Q satisfies every bilinear equation):",
          "PASS" if bad==0 else f"FAIL ({bad} violated)")
    # note: this control does NOT impose q_{j,i}=0; it checks the recursion encoding only
