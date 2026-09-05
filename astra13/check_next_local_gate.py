"""Next local Q-polynomiality gate; reject or retain the saved particular family."""
import json
from pathlib import Path
import sympy as s
y,t,tau=s.symbols('y t tau');a,b,e,k=s.symbols('a b e k')
A=a/3
coeff=s.Poly(s.expand((b+e*t+k*t*t)**2*sum((-1)**j*(j+1)*A**j*t**j for j in range(4))),t).coeff_monomial(t**3)
factor=2*(e-2*A*b)*(k-A*e+A*A*b)
assert s.expand(coeff-factor)==0
data=json.loads(Path(__file__).with_name('coupled_rational_certificate.json').read_text())
P9=s.sympify(data['p9_particular']);P8=s.sympify(data['p8_particular'])
G=1+y**5;aa=3+5*y**4+8*y**5;E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
dd=R/3+tau*y*G*E2
bb=s.cancel((dd-aa**2/3)/G)
ee=s.cancel((P9/y**6-aa**3/27)/G);kk=s.cancel(P8/y**5)
F1=s.rem(s.expand(ee-2*aa*bb/3),G,y)
F2=s.rem(s.expand(kk-aa*ee/3+aa**2*bb/9),G,y)
res=s.rem(s.expand(F1*F2),G,y)
coef=s.Poly(res,y).all_coeffs()
gg=s.Poly(0,tau)
multipliers=[]
for c in coef:
    cc=s.Poly(c,tau)
    if not gg and not cc:
        multipliers.append(s.S(0));continue
    v,w,new=s.gcdex(gg,cc)
    multipliers=[s.expand(v.as_expr()*m) for m in multipliers]+[w.as_expr()]
    gg=new
assert s.expand(sum(m*c for m,c in zip(multipliers,coef))-gg.as_expr())==0
print('PASS: exact factored local Q-row gate')
print('particular-family residual degree in y',s.degree(res,y))
print('gcd of tau coefficient conditions',gg.as_expr())
print('particular family excluded for every complex tau',gg.degree()==0)
Path(__file__).with_name('next_local_gate.json').write_text(json.dumps({
    'gate':'(e-2*a*b/3)*(k-a*e/3+a*a*b/9)=0 modulo h',
    'particular_residual':str(res),'coefficient_gcd':str(gg.as_expr()),
    'particular_family_excluded':gg.degree()==0,
    'coefficient_equations':[str(v) for v in coef],
    'bezout_multipliers':[str(v) for v in multipliers],
    'scope':'The chosen particular affine section only; all 21 free parameters remain necessary'},indent=2)+'\n')
