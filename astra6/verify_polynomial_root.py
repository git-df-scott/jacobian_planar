#!/usr/bin/env python3
"""Exact certificate excluding R polynomial in B in the (6,8) component."""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
v,c,r=s.symbols('v c r')
F=s.symbols('F',nonzero=True)
T,M,W=s.symbols('T M W')
k,l=s.symbols('k l')
dF,dT,dM,dW=s.symbols('dF dT dM dW')
a=-c*v**3+v*v+v
b=-3*c*v*v+4*v+2
R=F*b+T
S=M*(3*c*a-b)-s.Rational(3,2)*k*F*b+W
P=s.expand(R**3+S)

def zero(x):assert s.cancel(s.expand(x))==0,x
def quo(x,y):return s.div(x,y,v)[0]
def derivative(x):
    return s.diff(x,c)+sum(s.diff(x,z)*dz for z,dz in
                          [(F,dF),(T,dT),(M,dM),(W,dW)])

def main():
    L=quo(S,R);N=s.cancel(S-L*R);Z=s.cancel(L**2+2*quo(L*N,R))
    Q=s.cancel(R**4+s.Rational(4,3)*R*S+s.Rational(2,9)*Z
               +k*(R**2+s.Rational(2,3)*L)+l*R)
    jac=s.Poly(s.cancel(s.diff(P,v)*derivative(Q)-derivative(P)*s.diff(Q,v)),v)
    assert jac.degree()<=4
    rows={str(i):s.factor(jac.coeff_monomial(v**i)) for i in range(5)}
    comb=s.factor(rows['3']+8*rows['4']/(3*c))
    zero(s.diff(comb,W));zero(s.diff(comb,dW));zero(s.diff(comb,l))
    # Combination is homogeneous of degree 2 in M,dM. For M=c^m*unit,
    # divide by c^(2m), then extract the constant coefficient exactly.
    eta=s.symbols('eta')
    zero(comb.subs({M:eta*M,dM:eta*dM},simultaneous=True)-eta*eta*comb)
    mu,m=s.symbols('mu m',nonzero=True)
    indicial=s.limit(comb.subs({M:mu,dM:m*mu/c},simultaneous=True),c,0)
    zero(indicial-s.Rational(64,3)*F*mu*mu*(2*m-1))
    # Parity is checked in the coefficient field; polynomiality is a
    # separate hypothesis retained in the written proof.
    tr={v:3*(r+2)/r**2,c:r*r/9}
    for expression in (P,Q):
        value=s.cancel(expression.subs(tr,simultaneous=True))
        zero(value-value.subs(r,-r))
    print('EXACT_JACOBIAN_AND_PARITY: PASS',flush=True)
    print('HALF_INTEGER_VALUATION_OBSTRUCTION: PASS',flush=True)
    result={'status':'PASS','hypotheses':['F,T,M,W rational in c and regular at c=0','F(0)!=0',
                'R=F*b+T','P,Q as displayed','all rational coefficients of Q polynomial'],
            'R':str(R),'S':str(S),'L':str(s.factor(L)),'Z':str(s.factor(Z)),
            'Jacobian_rows':{key:str(value) for key,value in rows.items()},
            'combination_J3_plus_8J4_over_3c':str(comb),
            'indicial_coefficient':str(s.factor(indicial)),
            'forced_nonzero_M_valuation':'1/2, impossible for a polynomial',
            'M_zero_case':'P,Q in C[c,R], Jacobian divisible by R_v',
            'remaining_gap':'R may have non-even rational trace',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'polynomial_root_certificate.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
