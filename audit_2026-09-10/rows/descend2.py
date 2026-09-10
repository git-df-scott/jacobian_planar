"""Stage 2: introduce symbolic P rows p7, p6, p5 one at a time and solve q11, q10, q9 jointly
(linear in the new row and the new Q row; parameters from Astra 13 carried symbolically)."""
import sympy as s, json, time, sys
from row_engine import *
t0=time.time()
st=json.load(open('descend_stage1.json'))
P={int(k):s.sympify(v) for k,v in st['P'].items()}; Q={int(k):s.sympify(v) for k,v in st['Q'].items()}
params=[s.Symbol(p) for p in st['params']]
for l in (11,10,9):
    kk=l-4; lo,m1,hi=pb(kk)
    pc=s.symbols(f'p{kk}_0:{hi-lo+1}'); pk=sum(cf*y**(lo+i) for i,cf in enumerate(pc))
    P[kk]=pk
    qlo,qm1,qhi=qb(l); qc=s.symbols(f'q{l}_0:{qhi-qlo+1}'); ql=sum(cf*y**(qlo+i) for i,cf in enumerate(qc))
    Q[l]=ql
    eq=s.Poly(row_equation(P,Q,l+11),y).all_coeffs()
    eq+=[s.diff(ql,y,j).subs(y,-1) for j in range(qm1)]+[s.diff(pk,y,j).subs(y,-1) for j in range(m1)]
    unk=list(qc)+list(pc)
    sol=list(s.linsolve(eq,unk))
    print(f"row {l+11}: q{l} with p{kk} ({len(pc)} coeffs): solutions={len(sol)} t={round(time.time()-t0,1)}s",flush=True)
    if not sol:
        print("  generic parameters admit no solution; attempting joint solve including Astra-13 parameters (linear part)",flush=True)
        try:
            sol2=list(s.linsolve(eq,unk+params))
        except Exception as ex:
            print("  joint linear solve failed (nonlinear in parameters):",type(ex).__name__,flush=True); sys.exit(2)
        print("  joint:", "empty -> CONTRADICTION under all bounds" if not sol2 else "affine solution", flush=True)
        if not sol2: sys.exit(3)
        sub=dict(zip(unk+params,sol2[0]))
    else:
        sub=dict(zip(unk,sol[0]))
    P[kk]=s.expand(pk.subs(sub)); Q[l]=s.expand(ql.subs(sub))
    for i in P: P[i]=s.expand(P[i].subs(sub))
    for i in Q: Q[i]=s.expand(Q[i].subs(sub))
    free=sorted(set().union(*(v.free_symbols for v in P.values()))|set().union(*(v.free_symbols for v in Q.values()))-{y,tau},key=str)
    params=[f for f in free]
    print(f"  free parameters now: {len(params)}",flush=True)
    json.dump({'params':[str(p) for p in params],'Q':{str(l):str(v) for l,v in Q.items()},'P':{str(k):str(v) for k,v in P.items()}},open(f'descend_stage2_row{l}.json','w'))
print("stage 2 done; elapsed",round(time.time()-t0,1),flush=True)
