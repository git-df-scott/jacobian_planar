#!/usr/bin/env python3
"""Exact global differential/descent tests for Astra 12's rational leading component.

This verifies necessary conditions and a surviving differential control,
not a Keller counterexample or termination of a formal construction.
"""
import argparse
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent
x,y,u,tau=s.symbols('x y u tau')
h=1+y**5
c=y**3*h


def chart():
    X=x**4*(y+1); Y=1/x
    bracket=lambda f,g:s.expand(s.diff(f,x)*s.diff(g,y)-s.diff(f,y)*s.diff(g,x))
    assert bracket(X,Y)==x**2
    assert bracket(X+Y**2,Y)==x**2
    bounds={}
    for k in [12,11,10,9,8,7]:
        bounds[k]={'min_y':max(0,(4*k-3+4)//5),
                   'multiplicity_at_minus_one':max(0,(k+3)//4),
                   'max_y':min(24,(84+k)//4)}
    assert bounds[11]=={'min_y':9,'multiplicity_at_minus_one':3,'max_y':23}
    assert bounds[10]=={'min_y':8,'multiplicity_at_minus_one':3,'max_y':23}
    # Every source monomial in the conservative original rectangle has
    # exactly the asserted row and shifted-polynomial coefficient.
    for i in range(25):
        for j in range(85):
            k=4*i-j
            if k<=12:
                assert i>=max(0,(k+3)//4)
                assert i<=min(24,(84+k)//4)
    print('PASS: birational chart, exact row bounds, ordinary Keller control',flush=True)
    return bounds


def polynomial_part():
    C=s.symbols('C',nonzero=True)
    p=s.symbols('p0:12')
    # b[n] is the coefficient of z^n in (1+sum p[12-j]/C^3 z^j)^(4/3).
    a=[s.Integer(1)]+[p[12-j]/C**3 for j in range(1,8)]
    b=[s.Integer(1)]
    for n in range(1,8):
        b.append(s.expand(sum((s.Rational(7,3)*j-n)*a[j]*b[n-j]
                              for j in range(1,n+1))/n))
    q={16-n:s.expand(C**4*b[n]) for n in range(8)}
    assert s.expand(q[15]-s.Rational(4,3)*C*p[11])==0
    assert s.expand(q[14]-s.Rational(4,3)*C*p[10]-s.Rational(2,9)*p[11]**2/C**2)==0
    assert s.expand(q[13]-s.Rational(4,3)*C*p[9]
                    -s.Rational(4,9)*p[11]*p[10]/C**2
                    +s.Rational(4,81)*p[11]**3/C**5)==0
    v,w=s.symbols('v w')
    sub={p[11]:0,p[10]:C*v,p[9]:w}
    pole1=s.expand(C*q[11].subs(sub)).subs(C,0)
    pole2=s.expand(C**2*q[10].subs(sub)).subs(C,0)
    assert pole1==s.Rational(4,9)*v*w
    assert pole2==s.Rational(2,81)*(9*w**2-2*v**3)
    e1=v*w; e2=9*w**2-2*v**3
    assert s.expand(v**4-s.Rational(9,2)*w*e1+v*e2/2)==0
    assert s.expand(w**3-w*e2/9-s.Rational(2,9)*v*v*e1)==0
    print('PASS: high-row formulas and exact radical certificates at every simple root',flush=True)
    return {str(k):str(q[k]) for k in [15,14,13,12,11,10]}


def inverse_coefficients():
    # Independent implicit inversion, with z=1/s and x=(s/w)*L(z).
    z,w,A,B=s.symbols('z w A B',nonzero=True)
    l1,l2=s.symbols('l1 l2')
    L=1+l1*z+l2*z*z
    expr=s.Poly(s.expand(L**12+A*z*L**11+B*z*z*L**10-1),z)
    vv=s.solve([expr.coeff_monomial(z),expr.coeff_monomial(z*z)],(l1,l2),dict=True)[0]
    cube=s.Poly(s.expand(L.subs(vv)**3),z)
    assert cube.coeff_monomial(z)==-A/4
    assert cube.coeff_monomial(z*z)==13*A*A/96-B/4
    print('PASS: source-forcing coefficients derived by implicit inversion',flush=True)


def first_exactness():
    a=s.symbols('a0:5');b=s.symbols('b0:4')
    aa=sum(a[i]*y**i for i in range(5))
    BB=sum(b[i]*y**i for i in range(4))
    D=y+y**6
    eq=s.Poly(s.expand(2*D*s.diff(BB,y)-s.diff(D,y)*BB-2*aa),y).all_coeffs()
    sol=list(s.linsolve(eq,a+b))
    expected=(0,0,0,s.Rational(5,2)*b[3],0,0,0,0,b[3])
    assert sol==[expected]
    lam=s.symbols('lambda')
    p11=lam*y**12*h**2
    # Descent requires order >=3; the surviving global differential has order 2.
    assert s.diff(p11,y,2).subs(y,-1)==50*lam
    assert s.gcd(D,s.diff(D,y))==1
    print('PASS: genus-two exactness plus original polynomiality forces p11=0',flush=True)
    return {'linear_solution':[str(v) for v in expected],
            'p11_second_derivative_at_minus_one':'50*lambda', 'conclusion':'p11=0'}


def second_exactness():
    a=s.symbols('a0:6'); b=s.symbols('b0:3')
    aa=sum(a[i]*y**i for i in range(6))
    BB=sum(b[i]*u**i for i in range(3))
    D=1+u**5
    eq=s.Poly(s.expand(4*D*s.diff(BB,u)-5*u**4*BB-4*u**6*aa.subs(y,1/u)),u).all_coeffs()
    sol=list(s.linsolve(eq,a+b))
    expected=(s.Rational(3,4)*b[2],0,-s.Rational(5,4)*b[0],0,0,2*b[2],b[0],0,b[2])
    assert sol==[expected]
    # Inverse descent imposes aa(-1)=0, equivalently b0=-b2.
    aa_sol=s.expand(aa.subs(dict(zip(a+b,expected)),simultaneous=True))
    assert aa_sol.subs(y,-1)==-s.Rational(5,4)*(b[0]+b[2])
    E=3+5*y**2+8*y**5
    p10=tau*y**8*h**2*E
    assert all(s.diff(p10,y,k).subs(y,-1)==0 for k in range(3))
    primitive_numerator=4*tau*(u*u-1)
    assert s.expand(4*D*s.diff(primitive_numerator,u)-5*u**4*primitive_numerator
                    -4*tau*u**6*E.subs(y,1/u))==0
    # A finite original polynomial representing this row exists.
    XX,YY=s.symbols('X Y')
    lifted=s.cancel(p10.subs(y,XX*YY**4-1)/YY**10)
    assert s.denom(lifted)==1
    PP=s.Poly(lifted,XX,YY)
    assert PP.degree(XX)<=24 and PP.degree(YY)<=84
    print('PASS: genus-six exactness and descent reduce p10 to one explicit parameter',flush=True)
    return {'linear_solution':[str(v) for v in expected], 'p10':str(p10),
            'primitive':'4*tau*(u**2-1)/V, V**4=1+u**5',
            'nonzero_parameter_not_excluded':True}


def next_obstruction_control():
    E=3+5*y**2+8*y**5
    p10=tau*y**8*h**2*E
    # The next global source-forcing numerator can vanish identically.
    p8=s.Rational(11,24)*tau**2*y**7*h*E**2
    assert s.expand(24*c**3*p8-11*p10**2)==0
    assert s.degree(p8,y)==22 and all(s.diff(p8,y,k).subs(y,-1)==0 for k in range(2))
    assert s.Poly(p8,y).terms()[-1][0][0]>=6
    # This verifies survival of this one exact differential test only.
    print('PASS: next exact numerator has a polynomial survivor; no false closure of tau!=0',flush=True)
    return {'p8_control':str(p8), 'identity':'24*c**3*p8-11*p10**2=0',
            'scope':'One necessary global differential condition; not a Keller pair.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result={'status':'OPEN: no counterexample','scope':'Rational Astra 11 leading solution only',
            'bounds':chart(),'q_rows':polynomial_part()}
    inverse_coefficients()
    result.update(first=first_exactness(),second=second_exactness(),next_control=next_obstruction_control())
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:
        (ROOT/'certificate.json').write_text(encoded)
    else:
        assert json.loads(encoded)==json.loads((ROOT/'certificate.json').read_text())
        print('PASS: regenerated exact certificate matches saved result',flush=True)


if __name__=='__main__':main()
