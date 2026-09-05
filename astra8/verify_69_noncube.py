#!/usr/bin/env python3
"""Exact algebra certificates for the noncube leading-factor obstruction.

The rational-function and valuation arguments are in OBSTRUCTION_69_NONCUBE.md.
"""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'astra7'))
import sympy as s
from exact_tools import zero,derivative_operator,polynomial_part_power

HERE=Path(__file__).resolve().parent
x,Y=s.symbols('x Y')
a,b,u,w,Z,k=s.symbols('a b u w Z k')
da,db,du,dw,dZ=s.symbols('da db du dw dZ')
D=derivative_operator([a,b,u,w,Z],[da,db,du,dw,dZ])
R=x**3+a*x+b
S=u*x*x+w*x+Z-s.Rational(2,3)*k
P=R**2+S
Q=R**3+s.Rational(3,2)*R*S+s.Rational(3,8)*(u*u*x+2*u*w)+k*R

def main():
    zero(Q-polynomial_part_power(P,s.Rational(3,2),x)
           -k*polynomial_part_power(P,s.Rational(1,2),x))
    J=s.Poly(s.expand(s.diff(P,x)*D(Q)-D(P)*s.diff(Q,x)),x)
    G4=-a*u*u+2*u*Z+w*w
    G3=-2*a*u*w-b*u*u+2*w*Z
    C=u**3+12*b*u*w-6*Z**2
    identities={
      4:-s.Rational(9,4)*D(G4),
      3:-s.Rational(9,4)*D(G3),
      2:-s.Rational(3,4)*a*D(G4)+s.Rational(3,2)*da*G4+s.Rational(3,8)*D(C),
      1:-s.Rational(3,4)*a*D(G3)+s.Rational(3,4)*da*G3+s.Rational(3,2)*db*G4+s.Rational(9,8)*D(u*u*w)}
    assert J.degree()<=4
    for i,expression in identities.items():zero(J.coeff_monomial(x**i)-expression)
    print('UNCONSTRAINED_POLYNOMIAL_PART_AND_FOUR_ROW_IDENTITIES: PASS',flush=True)
    # Every branch is separated before division by u.
    zero(J.as_expr().subs({u:0,w:0,du:0,dw:0})
          +s.Rational(3,2)*Z*dZ*s.diff(R,x))
    substitutions={b:0,w:0,db:0,dw:0}
    row0=s.factor(J.coeff_monomial(1).subs(substitutions))
    zero(row0+s.Rational(3,8)*dZ*(4*a*Z+u*u))
    W,dW,C0,h,U,kappa=s.symbols('W dW C0 h U kappa',nonzero=True)
    row0W=s.cancel(row0.subs({a:W/u,Z:W/2,dZ:dW/2}))
    zero(row0W+s.Rational(3,32)*(2*(u**3-s.Rational(3,2)*W**2)+7*W**2)*dW/u)
    # Cubing kappa=-3h(2C+7W^2)W'/(32U), with U^3=h^2(C+3W^2/2).
    hsol=-s.Integer(32768)*kappa**3*(C0+s.Rational(3,2)*W**2)/(27*(2*C0+7*W**2)**3*dW**3)
    zero((-s.Rational(3,32))**3*h**3*(2*C0+7*W**2)**3*dW**3
          -kappa**3*h**2*(C0+s.Rational(3,2)*W**2)
          -h**2*(-s.Rational(27,32768)*(2*C0+7*W**2)**3*dW**3)*(h-hsol))
    h0=s.factor(hsol.subs(C0,0))
    zero(h0+s.Rational(16384,3087)*kappa**3/(W**4*dW**3))
    print('ZERO_BRANCH_AND_RATIONAL_JACOBIAN_ELIMINATION: PASS',flush=True)
    # In the C=0 branch restore y=v+eta, q^3=h, A=q*a, U=q^2*u=3A^2/2.
    y,q,A=s.symbols('y q A',nonzero=True)
    back={x:q*y,a:A/q,b:0,u:s.Rational(3,2)*A*A/q**2,w:0,
          Z:s.Rational(3,4)*A**3/q**3}
    Pr=q**6*y**6+2*q**3*A*y**4+s.Rational(5,2)*A*A*y*y+s.Rational(3,4)*A**3/q**3-s.Rational(2,3)*k
    Qr=q**9*y**9+3*q**6*A*y**7+s.Rational(21,4)*q**3*A*A*y**5+s.Rational(35,8)*A**3*y**3+s.Rational(63,32)*A**4/q**3*y
    zero(P.subs(back,simultaneous=True)-Pr)
    zero(Q.subs(back,simultaneous=True)-Qr)
    f=Y**3+2*Y**2+s.Rational(5,2)*Y+s.Rational(3,4)
    g=Y**4+3*Y**3+s.Rational(21,4)*Y**2+s.Rational(35,8)*Y+s.Rational(63,32)
    resultant=s.resultant(f,g,Y)
    assert resultant==s.Rational(567,32768)
    bezout_f,bezout_g,gcd=s.gcdex(f,g,Y)
    zero(bezout_f*f+bezout_g*g-1)
    assert gcd==1
    print('RESTORED_POLYNOMIALS_AND_NONZERO_POLE_RESULTANT: PASS',flush=True)
    result={'status':'PASS','scope':'Complete noncube-h (6,9) obstruction; cube-h remains open',
      'P':str(s.expand(P)),'Q':str(s.expand(Q)),
      'first_integrals':{'G4':str(G4),'G3':str(G3),'C':str(C),'last_character_integral':str(u*u*w)},
      'row_identities':{str(i):str(expression) for i,expression in identities.items()},
      'reduced_constant_row':str(row0),'h_eliminated':str(hsol),'h_when_C_zero':str(h0),
      'restored_P_with_h_equal_q_cubed':str(Pr),'restored_Q_with_h_equal_q_cubed':str(Qr),
      'pole_polynomials':{'f':str(f),'g':str(g)},'resultant':str(resultant),
      'bezout_certificate':{'f_multiplier':str(bezout_f),'g_multiplier':str(bezout_g),'sum':'1'},
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'certificate_69_noncube.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
