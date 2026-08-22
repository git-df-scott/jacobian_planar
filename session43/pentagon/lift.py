#!/usr/bin/env python3
"""Order-by-order deformation lift at a point of the pentagon variety.

gamma(t) = pt + t v + t^2 w2 + ... ; at each order solve J w_k = -(residual)_k.
If the residual is not in image(J) the direction is obstructed at that order.
Otherwise continue.  A direction that lifts through many orders is a genuine
curve in the variety, and its higher coefficients say which x-degrees it reaches.
"""
import sys
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p
from jacrank import jacobian
n=len(VARS); NP=26
inv3=pow(3,p-2,p)
def famB(lam):
    d={v:0 for v in VARS}; d["p_1_0"]=1; d["p_1_1"]=lam%p
    d["p_2_0"]=lam%p; d["p_3_0"]=lam*lam%p*inv3%p
    return d
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
            new[d+1]=(new[d+1]+cur[d])%p; new[d]=(new[d]-cur[d]*xs[k])%p
        cur=new
    return poly
def solve_in_image(J,b):
    """return w with J w = b, or None."""
    m=len(J); aug=[J[i][:]+[b[i]%p] for i in range(m)]
    piv=[]; rr=0
    for c in range(n+1):
        sel=next((i for i in range(rr,m) if aug[i][c]%p),None)
        if sel is None: continue
        if c==n: return None
        aug[rr],aug[sel]=aug[sel],aug[rr]
        iv=pow(aug[rr][c],p-2,p); aug[rr]=[(x*iv)%p for x in aug[rr]]
        for i in range(m):
            if i!=rr and aug[i][c]%p:
                f=aug[i][c]; aug[i]=[(aug[i][j]-f*aug[rr][j])%p for j in range(n+1)]
        piv.append(c); rr+=1
    w=[0]*n
    for i,c in enumerate(piv): w[c]=aug[i][n]
    return w
def curve_vals(pt,coeffs):
    out=[]
    for t in range(NP):
        d={}
        for i,v in enumerate(VARS):
            s=pt[v]
            tp=1
            for k in range(1,len(coeffs)+1):
                tp=tp*t%p
                s=(s+tp*coeffs[k-1][i])%p
            d[v]=s
        out.append(conditions(d))
    return out
def lift(pt,v,maxorder=8):
    J,_=jacobian(pt)
    coeffs=[v]
    for order in range(2,maxorder+1):
        vals=curve_vals(pt,coeffs)
        res=[interp([vals[t][c] for t in range(NP)])[order] for c in range(66)]
        if all(x%p==0 for x in res):
            coeffs.append([0]*n); continue
        w=solve_in_image(J,[(-x)%p for x in res])
        if w is None: return order,coeffs
        coeffs.append(w)
    return None,coeffs
if __name__=="__main__":
    pt=famB(1); J,_=jacobian(pt)
    rows=[r[:] for r in J]; piv=[]; r=0
    for c in range(n):
        sel=next((i for i in range(r,len(rows)) if rows[i][c]%p),None)
        if sel is None: continue
        rows[r],rows[sel]=rows[sel],rows[r]
        iv=pow(rows[r][c],p-2,p); rows[r]=[(x*iv)%p for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][c]%p:
                f=rows[i][c]; rows[i]=[(rows[i][j]-f*rows[r][j])%p for j in range(n)]
        piv.append(c); r+=1
    free=[c for c in range(n) if c not in piv]
    basis=[]
    for fc in free:
        v=[0]*n; v[fc]=1
        for i,c in enumerate(piv): v[c]=(-rows[i][fc])%p
        basis.append(v)
    surv=[]
    for k,v in enumerate(basis):
        ob,coeffs=lift(pt,v,maxorder=8)
        if ob is None:
            hi=[VARS[i] for i in range(n) if any(c[i]%p for c in coeffs) and int(VARS[i].split('_')[2])>=2]
            surv.append((k,hi))
            print(f"  direction {k}: LIFTS THROUGH ORDER 8; i>=2 coords touched: {len(hi)}; p_16_8 touched: {'p_16_8' in hi}", flush=True)
        else:
            print(f"  direction {k}: obstructed at order {ob}", flush=True)
    print(f"\ndirections surviving to order 8: {len(surv)} of {len(basis)}")
