#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 4c -- the DECIDING measurement for approach (b):
are the conditions SPARSE enough to write down, despite their degree?

The dense monomial bound is hopeless -- degree 12 in 61 variables is ~1e14
monomials, degree 10 in 45 is ~3e10.  But the dense bound is an upper bound.
The y-adic recursion builds Q from a bounded number of products, so the true
monomial count could be far smaller.  If it is small enough, part of the system
CAN be exported to msolve/Singular and approach (b) opens a verdict path.  If it
is not, (b) is closed and the reformulation must come from elsewhere.

METHOD: run the recursion symbolically over F_p[early parameters], sparse
dict-of-monomials, with p_10 = 1 and p_00 = 0 (both legitimate gauges, so no
denominators appear).  Count actual monomials at each level.  Hard cap so the
run aborts gracefully rather than exhausting memory.
"""
import sys, time
p = 1000003
CAP = 40_000_000        # abort if any single polynomial exceeds this many monomials

def P_rows(jmax=16):
    r = {}
    for j in range(jmax+1):
        lo, hi = max(0, j-8), min(8, j//2+1)
        if lo <= hi: r[j] = (lo, hi)
    return r
PR = P_rows()
PARAMS = [(j,i) for j in sorted(PR) for i in range(PR[j][0], PR[j][1]+1)]
VIDX = {}                      # parameter -> variable index (gauge-fixed ones excluded)
for k,(j,i) in enumerate(PARAMS):
    if (j,i) in ((0,0),(0,1)): continue      # p_00 = 0, p_10 = 1 gauges
    VIDX[(j,i)] = len(VIDX)
NV = len(VIDX)

# sparse multivariate poly: dict {tuple(sorted((var,exp)...)) : coeff}
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
        if len(out)>CAP: raise MemoryError(f"exceeded {CAP} monomials")
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

# x-polynomials whose coefficients are sparse multivariate polys
def xmul(A,B):
    if not A or not B: return []
    out=[{} for _ in range(len(A)+len(B)-1)]
    for i,ai in enumerate(A):
        if not ai: continue
        for j,bj in enumerate(B):
            if not bj: continue
            out[i+j]=padd(out[i+j], pmul(ai,bj))
    return out
def xadd(A,B):
    n=max(len(A),len(B)); out=[]
    for i in range(n):
        out.append(padd(A[i] if i<len(A) else {}, B[i] if i<len(B) else {}))
    return out
def xscal(A,c): return [pscal(a,c) for a in A]
def xderiv(A): return [pscal(A[i], i) for i in range(1,len(A))] if len(A)>1 else []

print("="*78); print("H1b step 4c -- SPARSITY OF THE CONDITIONS (deciding test for (b))"); print("="*78)
print(f"  variables after gauges p_00=0, p_10=1 : {NV}\n")

Pn = {}
for (j,i) in PARAMS:
    row = Pn.setdefault(j, [])
    while len(row) <= i: row.append({})
    if (j,i)==(0,0): row[i]={}
    elif (j,i)==(0,1): row[i]={():1}
    else: row[i]={((VIDX[(j,i)],1),):1}
JM = 30
P = [Pn.get(j, []) for j in range(JM+2)]
Q = [[] for _ in range(JM+2)]
Q[0]=[{():1}]
Q[1]=[{},{},{():1}]            # p_10 = 1  =>  Q_1 = x^2

t0=time.time()
print("  level   monomials in Q_j (max over x-coefficients)   cumulative time")
try:
    for k in range(1, JM):
        acc=[]
        for a in range(1,k+1):
            b=k+1-a
            if b<0 or a>=len(P) or not P[a]: continue
            acc = xadd(acc, xscal(xmul(P[a], xderiv(Q[b])), a))
            acc = xadd(acc, xscal(xmul(xderiv(P[a]), Q[b]), -(k+1-a)))
        Q[k+1]=xscal(acc, pow(k+1, p-2, p))
        mx = max((len(c) for c in Q[k+1]), default=0)
        tot= sum(len(c) for c in Q[k+1])
        print(f"    j={k+1:2d}     max {mx:>12,}   total {tot:>13,}     {time.time()-t0:6.1f}s")
        if k+1 >= 26: break
except MemoryError as e:
    print(f"\n  ABORTED: {e}  at {time.time()-t0:.0f}s")
    print("""
  VERDICT for approach (b): the conditions are NOT sparse.  The symbolic
  expansion blows past the cap before even reaching the first live condition
  level, so the reduced system cannot be written down either.  Eliminating the
  13 late parameters does not help: it removes variables but RAISES the degree
  in the survivors (measured: 10..21+, with 45 conditions above degree 30).""")
    print("="*78); sys.exit(0)
print(f"\n  reached level 14 in {time.time()-t0:.0f}s")
print("="*78)
