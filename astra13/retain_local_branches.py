"""Retain two sufficient local branches of the coupled affine solution.

These uniform choices do not exhaust mixed choices at the four other roots.
"""
import json
from pathlib import Path
import sympy as s
root=Path(__file__).resolve().parent
data=json.loads((root/'coupled_rational_certificate.json').read_text())
y,tau=s.symbols('y tau');G=1+y**5;a=3+5*y**4+8*y**5
E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
d=R/3+tau*y*G*E2;b=s.cancel((d-a*a/3)/G)
mapping={s.Symbol(k):s.sympify(v) for k,v in data['affine_solution'].items()}
e=sum(mapping[s.Symbol('e'+str(j))]*y**j for j in range(13))
k=sum(mapping[s.Symbol('k'+str(j))]*y**j for j in range(19))
B=sum(mapping[s.Symbol('b'+str(j))]*y**j for j in range(19))
f=a**3/27+G*e
F1=s.rem(s.expand(e-2*a*b/3),G,y)
F2=s.rem(s.expand(k-a*e/3+a*a*b/9),G,y)
unknowns=[s.Symbol(v) for v in data['free_parameters']]
out={'scope':'Two uniform choices and their intersection, not all mixed local assignments','branches':{}}
for name,polys in [('factor_one',[F1]),('factor_two',[F2]),('intersection',[F1,F2])]:
    eq=sum((s.Poly(pp,y).all_coeffs() for pp in polys),[])
    sol=list(s.linsolve(eq,unknowns))
    if not sol:
        out['branches'][name]={'soluble':False};continue
    vv=sol[0];sub=dict(zip(unknowns,vv))
    assert all(s.expand(v.subs(sub,simultaneous=True))==0 for v in eq)
    free=set().union(*(v.free_symbols for v in vv))-{tau}
    pp9=s.expand(y**6*f.subs(sub,simultaneous=True));pp8=s.expand(y**5*k.subs(sub,simultaneous=True))
    prim=s.expand(B.subs(sub,simultaneous=True))
    part={v:0 for v in free}
    pp9=s.factor(pp9.subs(part));pp8=s.factor(pp8.subs(part));prim=s.factor(prim.subs(part))
    ef=s.cancel((pp9/y**6-a**3/27)/G);kf=s.cancel(pp8/y**5)
    assert s.rem(s.expand((ef-2*a*b/3)*(kf-a*ef/3+a*a*b/9)),G,y)==0
    N=-G*kf/4+s.Rational(11,48)*a*(a**3/27+G*ef)+s.Rational(11,96)*d*d-s.Rational(253,1152)*a*a*d+s.Rational(8855,165888)*a**4
    assert s.expand(4*y*G*s.diff(prim,y)-(3*G+9*y*s.diff(G,y))*prim-4*N)==0
    out['branches'][name]={'soluble':True,'free_dimension':len(free),
        'free_parameters':sorted(map(str,free)),
        'additional_linear_solution':{str(v):str(w) for v,w in zip(unknowns,vv)},
        'p9_particular':str(pp9),'p8_particular':str(pp8),'primitive_numerator_particular':str(prim)}
    print(name,'survives for all tau; free dimension',len(free),flush=True)
(root/'retained_local_branches.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: each retained particular satisfies the global equation and next local gate')
