"""Descend the rational branch below Astra 13: load the 21-parameter p9,p8 family (mu=1, tau free),
solve q13,q12 exactly, then introduce symbolic p7 and solve q11 with its polynomiality/bound gates.
Every output is a necessary condition; nothing here is a Keller pair."""
import sympy as s, json, time, sys
from row_engine import *
t0=time.time()
data=json.load(open('astra13_coupled_certificate.json'))
E1=3+5*y**4+8*y**5; E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
mp={s.Symbol(k):s.sympify(v) for k,v in data['affine_solution'].items()}
e=sum(mp[s.Symbol('e%d'%j)]*y**j for j in range(13)); k=sum(mp[s.Symbol('k%d'%j)]*y**j for j in range(19))
f=E1**3/27+h*e
P={12:s.expand(c**3),11:s.expand(y**8*h**2*E1),10:s.expand(y**7*h*R/3+tau*y**8*h**2*E2),
   9:s.expand(y**6*f),8:s.expand(y**5*k)}
params=sorted(set().union(*(v.free_symbols for v in mp.values()))-{tau},key=str)
print("free parameters carried:",len(params),flush=True)
Q={16:s.expand(c**4)}
log={}
for l in (15,14,13,12):
    ql,cf,sol=solve_q_row(P,Q,l,params); sol=list(sol)
    print(f"q{l}: solutions={len(sol)}  t={round(time.time()-t0,1)}s",flush=True)
    if not sol:
        # find the obstruction: which conditions on params are needed
        lo,m1,hi=qb(l); print("  NO polynomial q%d in bounds for generic parameters -> extracting conditions"%l,flush=True)
        # solve jointly for q coefficients and treat params as unknowns too (linear? only if equations are linear in params)
        Q2=dict(Q); Q2[l]=ql
        eq=s.Poly(row_equation(P,Q2,l+11),y).all_coeffs()+[s.diff(ql,y,j).subs(y,-1) for j in range(m1)]
        sol2=list(s.linsolve(eq,list(cf)+params))
        print("  joint solve (q coeffs + params):",("empty" if not sol2 else "affine, free=%s"%sorted(set().union(*(v.free_symbols for v in sol2[0]))-{y},key=str)),flush=True)
        if sol2:
            sub=dict(zip(list(cf)+params,sol2[0])); Q[l]=s.expand(ql.subs(sub))
            for i,pk in P.items(): P[i]=s.expand(pk.subs(sub))
            params=sorted(set().union(*(v.free_symbols for v in sol2[0]))-{y,tau},key=str)
            print("  remaining free parameters:",len(params),flush=True)
            continue
        sys.exit(1)
    Q[l]=s.expand(ql.subs(dict(zip(cf,sol[0]))))
    print(f"  q{l} deg={s.degree(Q[l],y)}",flush=True)
json.dump({'params':[str(p) for p in params],'Q':{str(l):str(v) for l,v in Q.items()},'P':{str(kk):str(v) for kk,v in P.items()}},open('descend_stage1.json','w'))
print("stage 1 saved; elapsed",round(time.time()-t0,1),flush=True)
