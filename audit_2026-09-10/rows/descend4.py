"""Stage 4: descend each Astra 13 uniform slice with ALL its free parameters symbolic.
Rows below p8 are linear in the new P/Q rows; the slice parameters enter the coefficients.
When a row admits no generic solution, extract the polynomial consistency conditions on the
parameters (rref of the augmented system over Q(tau, params)). Necessary conditions only."""
import sympy as s, json, time, sys
from row_engine import *
sec=sys.argv[1]
cert=json.load(open('astra13_coupled_certificate.json')); br=json.load(open('astra13_retained_local_branches.json'))['branches'][sec]
base={s.Symbol(k):s.sympify(v) for k,v in cert['affine_solution'].items()}
slice_sub={s.Symbol(k):s.sympify(v) for k,v in br['additional_linear_solution'].items()}
E1=3+5*y**4+8*y**5; E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
e=sum(base[s.Symbol('e%d'%j)]*y**j for j in range(13)); k=sum(base[s.Symbol('k%d'%j)]*y**j for j in range(19))
e=s.expand(e.subs(slice_sub)); k=s.expand(k.subs(slice_sub))
f=E1**3/27+h*e
P={12:s.expand(c**3),11:s.expand(y**8*h**2*E1),10:s.expand(y**7*h*R/3+tau*y**8*h**2*E2),9:s.expand(y**6*f),8:s.expand(y**5*k)}
Q={16:s.expand(c**4)}
params=sorted((e.free_symbols|k.free_symbols)-{y,tau},key=str)
print(f"[{sec}] slice parameters: {len(params)}",flush=True)
t0=time.time()
for l in range(15,-1,-1):
    kk=l-4; unk=[]
    newp = kk<=7 and kk>=-84
    if newp:
        lo,m1,hi=pb(kk); pc=s.symbols(f'p{kk}_0:{hi-lo+1}'); P[kk]=sum(cf*y**(lo+i) for i,cf in enumerate(pc)); unk+=list(pc)
    qlo,qm1,qhi=qb(l); qc=s.symbols(f'q{l}_0:{qhi-qlo+1}'); Q[l]=sum(cf*y**(qlo+i) for i,cf in enumerate(qc)); unk+=list(qc)
    eq=s.Poly(row_equation(P,Q,l+11),y).all_coeffs()
    eq+=[s.diff(Q[l],y,j).subs(y,-1) for j in range(qm1)]
    if newp: eq+=[s.diff(P[kk],y,j).subs(y,-1) for j in range(m1)]
    eq=[q for q in eq if q!=0]
    sol=list(s.linsolve(eq,unk))
    if not sol:
        print(f"[{sec}] row x^{l+11}: no generic solution; extracting consistency conditions on the {len(params)} slice parameters  t={round(time.time()-t0,1)}s",flush=True)
        A,bv=s.linear_eq_to_matrix(eq,unk)
        aug=A.row_join(bv)
        rr,piv=aug.rref(simplify=True)
        conds=[]
        for i in range(rr.rows):
            if all(rr[i,j]==0 for j in range(A.cols)) and rr[i,A.cols]!=0:
                conds.append(s.factor(s.numer(s.together(rr[i,A.cols]))))
        json.dump({'section':sec,'row':l+11,'conditions':[str(cnd) for cnd in conds],'params':[str(p) for p in params]},open(f'descend4_{sec}.json','w'),indent=1)
        print(f"[{sec}] {len(conds)} consistency conditions saved  t={round(time.time()-t0,1)}s",flush=True)
        for cnd in conds[:10]: print("   ",cnd,flush=True)
        sys.exit(0)
    sub=dict(zip(unk,sol[0]))
    for i in P: P[i]=s.expand(P[i].subs(sub))
    for i in Q: Q[i]=s.expand(Q[i].subs(sub))
    free=sorted((set().union(*(v.free_symbols for v in P.values()))|set().union(*(v.free_symbols for v in Q.values())))-{y,tau},key=str)
    print(f"[{sec}] row x^{l+11} (q{l},p{kk}): solved, free {len(free)}  t={round(time.time()-t0,1)}s",flush=True)
print("reached bottom")
