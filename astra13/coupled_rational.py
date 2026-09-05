"""Coupled p9,p8 global test on the shifted rational branch, mu=1, all tau.

Necessary conditions only. No truncation is claimed to give a Keller pair.
"""
import sympy as s
import json
from pathlib import Path
y,tau=s.symbols('y tau')
G=1+y**5; a=3+5*y**4+8*y**5; E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
d=R/3+tau*y*G*E2
ee=s.symbols('e0:13');kk=s.symbols('k0:19');bb=s.symbols('b0:19')
e=sum(ee[j]*y**j for j in range(13));k=sum(kk[j]*y**j for j in range(19))
B=sum(bb[j]*y**j for j in range(19)); f=a**3/27+G*e
N=-G*k/4+s.Rational(11,48)*a*f+s.Rational(11,96)*d*d-s.Rational(253,1152)*a*a*d+s.Rational(8855,165888)*a**4
op=4*y*G*s.diff(B,y)-(3*G+9*y*s.diff(G,y))*B
eq=s.Poly(s.expand(op-4*N),y).all_coeffs()
eq += [e.subs(y,-1),s.diff(e,y).subs(y,-1),k.subs(y,-1),s.diff(k,y).subs(y,-1)]
eq += [e.subs(y,0)-s.Rational(19,9),k.subs(y,0)-s.Rational(14,9)]
unknowns=ee+kk+bb
sol=list(s.linsolve(eq,unknowns))
assert len(sol)==1
vv=sol[0];free=set().union(*(v.free_symbols for v in vv))-{tau}
sub=dict(zip(unknowns,vv))
P9=s.expand(y**6*f.subs(sub,simultaneous=True));P8=s.expand(y**5*k.subs(sub,simultaneous=True))
primitive=s.expand(B.subs(sub,simultaneous=True))
# Verify the whole affine solution, retaining every free parameter.
assert all(s.expand(v.subs(sub,simultaneous=True))==0 for v in eq)
part={v:0 for v in free}
data={'status':'Necessary coupled test survives for arbitrary tau; not a Keller pair',
      'free_dimension':len(free),'free_parameters':sorted(map(str,free)),
      'p9_particular':str(s.factor(P9.subs(part))),
      'p8_particular':str(s.factor(P8.subs(part))),
      'primitive_numerator_particular':str(s.factor(primitive.subs(part))),
      'affine_solution':{str(v):str(w) for v,w in zip(unknowns,vv)},
      'scope':'Global exactness, stated local cube congruence and chart/descent conditions; remaining bracket rows untested'}
Path(__file__).with_name('coupled_rational_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
print(data['status']);print('free dimension',len(free))
print('PASS: all symbolic equations vanish on the complete affine parametrization')
