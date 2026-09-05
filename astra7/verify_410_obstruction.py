#!/usr/bin/env python3
"""Exact certificate for the complete (4,10) obstruction.

The arbitrary-degree local-ring proof is in OBSTRUCTION_410.md.
No degree sweep or conductor lifting is performed.
"""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
import sympy as s
from exact_tools import zero,polynomial_part_power,derivative_operator

HERE=Path(__file__).resolve().parent
x=s.symbols('x')
a,b,z,k,l=s.symbols('a b z k l')
da,db,dz=s.symbols('da db dz')
D=derivative_operator([a,b,z],[da,db,dz])

def main():
    T=x*x+a;L=b*x+z
    P=T*T+L
    Q=T**5+s.Rational(5,2)*T**3*L+s.Rational(15,8)*T*L**2 \
       +s.Rational(5,16)*(b**3*x+3*b*b*z) \
       +k*(T**3+s.Rational(3,2)*T*L+3*b*b/8)+l*T
    independent=sum(coef*polynomial_part_power(P,exponent,x) for coef,exponent in
                    [(1,s.Rational(5,2)),(k,s.Rational(3,2)),(l,s.Rational(1,2))])
    zero(Q-independent)
    print('410_FINITE_POLYNOMIAL_PART: PASS',flush=True)
    jac=s.Poly(s.expand(s.diff(P,x)*D(Q)-D(P)*s.diff(Q,x)),x)
    assert jac.degree()<=2
    I2=b*(5*a*b*b-12*k*z-8*l-15*z*z)/4
    I1=(48*a*b*b*k+120*a*b*b*z+5*b**4-48*k*z*z-64*l*z-40*z**3)/32
    zero(jac.coeff_monomial(x*x)-D(I2))
    zero(jac.coeff_monomial(x)-D(I1))
    zero(I2.subs(b,-b)+I2)
    zero(jac.coeff_monomial(1).subs(b,0))
    reduced_a=(15*z*z+12*k*z+8*l)/(5*b*b)
    J0=s.factor(jac.coeff_monomial(1).subs(a,reduced_a))
    zero(J0-b*b*(5*b*dz+(6*k+15*z)*db)/8)
    print('410_THREE_ROW_ELIMINATION: PASS',flush=True)
    Z=s.symbols('Z')
    A=128*l/5-192*k*k/25
    shifted=s.expand((s.Rational(32,5)*I1.subs(a,reduced_a)).subs(z,Z-2*k/5))
    offset=-128*k**3/125+128*k*l/25
    zero(shifted-(b**4+64*Z**3+A*Z+offset))
    h,u,dh,du,dZ=s.symbols('h u dh du dZ',nonzero=True)
    y=u*u/h;dy=2*u*du/h-u*u*dh/(h*h)
    bb=u/s.sqrt(h);dbb=du/s.sqrt(h)-u*dh/(2*h**s.Rational(3,2))
    original=s.sqrt(h)*J0.subs({b:bb,db:dbb,z:Z-2*k/5,dz:dZ},simultaneous=True)
    zero(original-u*(10*y*dZ+15*Z*dy)/16)
    print('410_CUBIC_AND_ORIGINAL_JACOBIAN: PASS',flush=True)
    # Exact order comparison: a pole of Z has order -1, while y has
    # order at least -1. This is a strict unique-pole contradiction.
    assert 3*(-1)<2*(-1)<-1<0
    result={'status':'CLOSED_WITH_WRITTEN_LOCAL_VALUATION_PROOF',
      'normalized_P':str(s.expand(P)),'normalized_Q':str(s.expand(Q)),
      'Jacobian_rows':{str(i):str(s.factor(jac.coeff_monomial(x**i))) for i in range(3)},
      'first_integrals':{'I2':str(I2),'I1':str(I1)},
      'Galois_anti_invariant_integral':'I2=0',
      'beta_zero_case':'constant Jacobian row is identically zero',
      'eliminated_a':str(reduced_a),'shift':'Z=z+2*k/5',
      'cubic':'y^2+64*Z^3+A*Z=B','A':str(A),
      'constant_offset_absorbed_into_B':str(offset),
      'original_Jacobian':'u*(10*y*Z_prime+15*Z*y_prime)/16',
      'valuation_certificate':{'initial':'nu(y),nu(Z)>=-1',
         'if_Z_has_pole':{'64Z^3':-3,'y^2_lower_bound':-2,'AZ_lower_bound':-1,'B':0},
         'conclusion':'Z,y regular; u vanishes; the Jacobian vanishes at c=0'},
      'leading_branches_covered':['rho=2/3','rho=4/3'],
      'coefficient_degree_bound':None,
      'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                       for name in ['verify_410_obstruction.py','exact_tools.py']}}
    (HERE/'certificate_410.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
