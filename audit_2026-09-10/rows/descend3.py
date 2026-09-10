"""Stage 3: descend on Astra 13's three retained particular sections (tau symbolic).
With p9,p8 specialized, every further row is LINEAR in the new P row and new Q row.
Descend as far as the bounds allow; report the first row that fails (contradiction for that section)
or survival with the free-parameter count. Necessary conditions only."""
import sympy as s, json, time, sys
from row_engine import *
sec=sys.argv[1]
d=json.load(open('astra13_retained_local_branches.json'))['branches'][sec]
E1=3+5*y**4+8*y**5; E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
P={12:s.expand(c**3),11:s.expand(y**8*h**2*E1),10:s.expand(y**7*h*R/3+tau*y**8*h**2*E2),
   9:s.expand(s.sympify(d['p9_particular'])),8:s.expand(s.sympify(d['p8_particular']))}
Q={16:s.expand(c**4)}
t0=time.time(); free=[]
for l in range(15,-1,-1):
    kk=l-4
    unk=[]
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
        print(f"[{sec}] row x^{l+11} (q{l},p{kk}): NO SOLUTION for any tau -> this particular section is excluded  t={round(time.time()-t0,1)}s",flush=True)
        json.dump({'section':sec,'excluded_at_row':l+11},open(f'descend3_{sec}.json','w')); sys.exit(0)
    sub=dict(zip(unk,sol[0]))
    for i in P: P[i]=s.expand(P[i].subs(sub))
    for i in Q: Q[i]=s.expand(Q[i].subs(sub))
    free=sorted((set().union(*(v.free_symbols for v in P.values()))|set().union(*(v.free_symbols for v in Q.values())))-{y,tau},key=str)
    print(f"[{sec}] row x^{l+11} (q{l},p{kk}): solved, free params {len(free)}  t={round(time.time()-t0,1)}s",flush=True)
    json.dump({'section':sec,'last_row':l+11,'free':len(free)},open(f'descend3_{sec}.json','w'))
print("reached bottom of loop")
