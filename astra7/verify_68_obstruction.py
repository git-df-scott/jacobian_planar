#!/usr/bin/env python3
"""Exact identities and elimination certificate for both (6,8) branches."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
import sympy as s
from exact_tools import zero,polynomial_part_power,derivative_operator

HERE=Path(__file__).resolve().parent
x=s.symbols('x')
a,b,t,u,w,k,l=s.symbols('a b t u w k l')
da,db,dt,du,dw=s.symbols('da db dt du dw')
Dv=derivative_operator([a,b,t,u,w],[da,db,dt,du,dw])

def minimum_terms(poly,bounds):
    variables=[a,b,t,u,w,k]
    values=[]
    for mon,coef in s.Poly(poly,*variables).terms():
        order=sum(n*bounds.get(v,0) for v,n in zip(variables,mon))
        term=coef*s.prod(v**n for v,n in zip(variables,mon))
        values.append((order,term))
    minimum=min(order for order,term in values)
    return minimum,[str(term) for order,term in values if order==minimum]

def main():
    T=x*x+a
    P=T**3+(b*x+t-3*k/2)*T+u*x+w-3*l/4
    Q=T**4+(s.Rational(4,3)*(b*x+t)-k)*T*T \
      +s.Rational(4,3)*(u*x+w)*T+s.Rational(2,9)*(b*x+t)**2 \
      +s.Rational(4,9)*b*u-k*k/2
    independent=sum(coef*polynomial_part_power(P,exponent,x) for coef,exponent in
                    [(1,s.Rational(4,3)),(k,s.Rational(2,3)),(l,s.Rational(1,3))])
    zero(Q-independent)
    print('68_FINITE_POLYNOMIAL_PART: PASS',flush=True)
    jac=s.Poly(s.expand(s.diff(P,x)*Dv(Q)-Dv(P)*s.diff(Q,x)),x)
    assert jac.degree()<=4
    F4=b**3-9*b*w-9*t*u
    C=-12*a*b*u+3*k*b*b-4*b*b*t+12*t*w+6*u*u
    F2=-2*a*b**3+6*b*b*u-9*k*b*t+6*b*t*t-18*u*w
    D=b**4+27*k*a*b*b-36*a*b*b*t+54*a*u*u-18*b*b*w \
       -54*k*b*u+18*b*t*u-27*k*t*t+12*t**3-54*w*w
    final=s.Rational(4,9)*(b*Dv(a*b*u)+u*Dv(b*u)-b*t*dw+u*t*dt)
    identities={4:s.Rational(8,27)*Dv(F4),3:-s.Rational(2,9)*Dv(C),
      2:s.Rational(4,27)*Dv(F2)+s.Rational(8,27)*a*Dv(F4)-s.Rational(4,27)*da*F4,
      1:s.Rational(2,81)*Dv(D)-s.Rational(8,81)*db*F4-s.Rational(2,9)*a*Dv(C),
      0:final-s.Rational(2,27)*da*F2-s.Rational(4,27)*a*da*F4}
    for i in range(5):zero(jac.coeff_monomial(x**i)-identities[i])
    for f in [F4,F2]:zero(f.subs({b:-b,u:-u},simultaneous=True)+f)
    for f in [C,D]:zero(f.subs({b:-b,u:-u},simultaneous=True)-f)
    print('68_FIVE_UNCONSTRAINED_ROW_IDENTITIES: PASS',flush=True)
    # Use q=sqrt(h) to check exact scaling without any branch simplifier.
    q,A,B,TT,U,W=s.symbols('q A B TT U W')
    subst={a:A/q**2,b:B/q,t:TT/q**2,u:U/q,w:W/q**2}
    scaled2=s.cancel(q**5*F2.subs(subst,simultaneous=True))
    scaledD=s.cancel(q**6*D.subs(subst,simultaneous=True))
    E2=s.expand(scaled2).subs(q,0)
    E3=s.expand(scaledD).subs(q,0)
    zero(E2-2*B*(3*TT**2-A*B**2))
    zero(E3-12*TT*(TT**2-3*A*B**2))
    resultant=s.factor(s.resultant(E2,E3,TT))
    zero(resultant+73728*A**3*B**9)
    comb=B*E3-2*TT*E2
    mult2=-6*TT*comb-512*A*A*B**5
    mult3=3*B*comb
    zero(mult2*E2+mult3*E3-1024*A**3*B**8)
    print('68_LEADING_ELIMINATION_AND_BEZOUT_CERTIFICATE: PASS',flush=True)
    half=s.Rational(1,2)
    cases=[
      ('first_u_pole', {a:-1,b:-half,t:-1,u:-3*half,w:-1},-4,'54*a*u**2'),
      ('first_w_pole', {a:-1,b:-half,t:-1,u:-half,w:-2},-4,'-54*w**2'),
      ('second_u_pole',{a:-1,b:half,t:0,u:-half,w:1},-2,'54*a*u**2'),
      ('second_w_pole',{a:-1,b:half,t:0,u:half,w:-1},-2,'-54*w**2')]
    valuation_checks={}
    for name,bounds,want,term in cases:
        minimum,terms=minimum_terms(D,bounds)
        assert minimum==want and terms==[term],(name,minimum,terms)
        valuation_checks[name]={'unique_minimum':str(minimum),'term':term,
                               'bounds':{str(v):str(o) for v,o in bounds.items()}}
    without_uw=F2+18*u*w
    minimum,_=minimum_terms(without_uw,{a:-1,b:half,t:0,u:-half,w:-1})
    assert minimum==half
    valuation_checks['second_F2_constraint']='all terms except -18*u*w have order >=1/2'
    print('68_EXACT_VALUATION_COMPARISONS: PASS',flush=True)
    # Verify the last factorization before using regularity of its factors.
    h=s.symbols('h',nonzero=True)
    Ader,Bder,Uder,hd=s.symbols('Ader Bder Uder hd')
    conversion={a:A/h,b:B/s.sqrt(h),u:U/s.sqrt(h),
      da:Ader/h-A*hd/h**2,
      db:Bder/s.sqrt(h)-B*hd/(2*h**s.Rational(3,2)),
      du:Uder/s.sqrt(h)-U*hd/(2*h**s.Rational(3,2))}
    orig=s.sqrt(h)*final.subs(conversion,simultaneous=True)
    dd=derivative_operator([A,B,U,h],[Ader,Bder,Uder,hd])
    target=s.Rational(4,9)*(B*dd(A*B*U/h**2)+U*dd(B*U/h)-B*t*dw+U*t*dt)
    zero(orig-target)
    print('68_ORIGINAL_JACOBIAN_VANISHING_FACTOR: PASS',flush=True)
    result={'status':'CLOSED_WITH_WRITTEN_LOCAL_VALUATION_PROOF',
      'normalized_P':str(s.expand(P)),'normalized_Q':str(s.expand(Q)),
      'redundant_parameter':'l is an additive target translation of P',
      'invariants':{key:str(f) for key,f in [('F4',F4),('C',C),('F2',F2),('D',D)]},
      'row_identities':{str(i):str(s.expand(f)) for i,f in identities.items()},
      'identity_residuals':{str(i):'0' for i in range(5)},
      'Galois_consequences':['F4=0','F2=0','C constant','D constant'],
      'scaled_residue_equations':[str(E2),str(E3)],'resultant':str(resultant),
      'Bezout':{'target':'1024*A^3*B^8','multipliers':[str(s.expand(mult2)),str(s.expand(mult3))]},
      'valuation_checks':valuation_checks,
      'final_orders':{'a':'-1','b':'>=1/2','u':'>=1/2','t':'>=0','w':'>=0'},
      'original_Jacobian':'4/9*(B*(a*b*u)prime+U*(b*u)prime-B*t*wprime+U*t*tprime)',
      'contradiction':'B=sqrt(h)*b and U=sqrt(h)*u vanish at c=0; all other factors are regular',
      'leading_branches_covered':['rho=2/3','rho=4/3'],
      'even_trace_assumption':False,'division_by_unknown_function':False,
      'coefficient_degree_bound':None,
      'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                       for name in ['verify_68_obstruction.py','exact_tools.py']}}
    (HERE/'certificate_68.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
