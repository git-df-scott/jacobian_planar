#!/usr/bin/env python3
"""Planted-witness instance for the pentagon pipeline (Example 10).

Take a random P with pentagon support obeying the gauges, compute Q by the
recursion, and build the SAME bilinear system except that the 66 Newton-polygon
slots are pinned to the values Q actually takes instead of to 0.  The resulting
system has a solution BY CONSTRUCTION.  Any solver or pipeline that cannot
return NONEMPTY on this instance cannot be trusted to have decided the real one.
"""
import sys, random, os
sys.path.insert(0,'/tmp/hunt')
import pentev, bilinear as B
p=B.p

rnd=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 101)
vals={v:rnd.randrange(p) for v in pentev.VARS}
vals["p_1_0"]=1; vals["p_1_1"]=1          # the two gauges
# recursion Q for this P
P=[]
for j in range(25):
    if j not in pentev.PR: P.append([]); continue
    lo,hi=pentev.PR[j]; row=[0]*(hi+1)
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
qval={(k,d):(Q[k][d] if d<len(Q[k]) else 0)%p for k in range(2,24) for d in range(0,B.degQ[k]+1)}

# Build equations with the 66 slots PINNED to their true values.
PIN={(j,i) for j in range(13,24) for i in range(0,j-12)}
orig_qterm=B.qterm
def qterm_pinned(k,d):
    if (k,d) in PIN: return ("c", qval[(k,d)])
    return orig_qterm(k,d)
B.qterm=qterm_pinned
eqs=B.build_equations(set())          # zero-set empty: pinning handled by qterm
vars_=[]
used=set()
for a in eqs:
    for vs in a: used.update(vs)
vars_=[v for v in pentev.VARS+B.QVARS if v in used]
extra=["1*p_1_0+%d"%(p-1),"1*p_1_1+%d"%(p-1)]
path="/tmp/hunt/planted.ms"
with open(path,"w") as f:
    f.write(",".join(vars_)+"\n"+str(p)+"\n")
    f.write(",\n".join([B.eq_str(a) for a in eqs]+extra)+"\n")
print("planted instance:",len(vars_),"vars",len(eqs),"eqs",os.path.getsize(path),"bytes")
# CONTROL ON THE CONTROL: the planted point must satisfy every exported equation
full=dict(vals)
for (k,d),val in qval.items():
    if (k,d) not in PIN: full[f"q_{k}_{d}"]=val
bad=0
for a in eqs:
    s=0
    for vs,co in a.items():
        t=co
        for v in vs: t=t*full.get(v,0)%p
        s=(s+t)%p
    if s%p: bad+=1
print("planted point satisfies exported equations:","PASS" if bad==0 else f"FAIL ({bad})")
import json
json.dump({k:v for k,v in full.items()}, open("/tmp/hunt/planted_point.json","w"))
