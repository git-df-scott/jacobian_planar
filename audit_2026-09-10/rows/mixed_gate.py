"""Classify ALL 2^5 local assignments of the Astra 13 q9 gate
      (e - 2ab/3)(k - ae/3 + a^2 b/9) = 0 at each root of h = 1+y^5,
over the field Q(r), r a primitive root of y^4-y^3+y^2-y+1 (other roots -r^2, r^3, -r^4; and -1).
Parameters (21 Astra-13 free params) are allowed to take values in Q(r); tau stays symbolic.
Necessary conditions only."""
import sympy as s, json, itertools, time
y,tau,r=s.symbols('y tau r')
data=json.load(open('astra13_coupled_certificate.json'))
G=1+y**5;a=3+5*y**4+8*y**5;E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
d=R/3+tau*y*G*E2;b=s.cancel((d-a*a/3)/G)
mp={s.Symbol(k):s.sympify(v) for k,v in data['affine_solution'].items()}
e=sum(mp[s.Symbol('e%d'%j)]*y**j for j in range(13)); k=sum(mp[s.Symbol('k%d'%j)]*y**j for j in range(19))
F1=s.expand(e-2*a*b/3); F2=s.expand(k-a*e/3+a*a*b/9)
params=[s.Symbol(v) for v in data['free_parameters']]
minpoly=r**4-r**3+r**2-r+1
roots={'m1':s.Integer(-1),'r':r,'r2':-r**2,'r3':r**3,'r4':-r**4}
# unknowns in Q(r): p = p0+p1 r+p2 r^2+p3 r^3
comp={p:s.symbols(f'{p}_0:4') for p in params}
subQ={p:sum(comp[p][i]*r**i for i in range(4)) for p in params}
def conds(F,root):
    val=s.expand(F.subs(y,root).subs(subQ))
    val=s.rem(s.Poly(val,r),s.Poly(minpoly,r)).as_expr()
    return [s.expand(val).coeff(r,i) for i in range(4)] if root!=-1 else [s.expand(val).coeff(r,i) for i in range(4)]
allunk=[c for p in params for c in comp[p]]
results={}
t0=time.time()
for choice in itertools.product([1,2],repeat=5):
    eqs=[]
    for (name,root),ch in zip(roots.items(),choice):
        eqs+=conds(F1 if ch==1 else F2, root)
    eqs=[q for q in eqs if q!=0]
    sol=list(s.linsolve(eqs,allunk))
    key=''.join(map(str,choice))
    if not sol: results[key]={'soluble':False}
    else:
        free=set().union(*(v.free_symbols for v in sol[0]))-{tau,r}
        results[key]={'soluble':True,'free_rational_dim':len(free)}
    print(key,results[key],round(time.time()-t0,1),flush=True)
json.dump({'scope':'q9 local gate, all 32 assignments, parameters in Q(zeta5), tau symbolic','results':results},open('mixed_gate_results.json','w'),indent=1)
print("done")
