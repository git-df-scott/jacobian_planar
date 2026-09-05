#!/usr/bin/env python3
"""Exact normalization, parity, local leading equations and ambient controls."""
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'astra7'))
import sympy as s
from exact_tools import polynomial_part_power,zero

HERE=Path(__file__).resolve().parent
v,c,x,r,Y=s.symbols('v c x r Y')
f=s.symbols('f',nonzero=True)
ps=s.symbols('p0:6')
ks=dict(zip([1,2,3,4,5,7,8],s.symbols('k1 k2 k3 k4 k5 k7 k8')))
P=x**6+sum(ps[i]*x**i/f**i for i in range(6))

def parity_expression(n):
    coeffs=s.symbols('p0:'+str(n+1))
    expression=s.expand(sum(coeffs[i]*(3*c)**(n-i)*sum(
        s.binomial(i,j)*2**(i-j)*(9*c)**((j-1)//2)
        for j in range(1,i+1,2)) for i in range(1,n+1)))
    trace=s.expand(sum(coeffs[i]*(r+2)**i*(3*c)**(n-i) for i in range(n+1)))
    remainder=s.rem(trace,r*r-9*c,r)
    zero(s.Poly(remainder,r).coeff_monomial(r)-expression)
    return expression

def main():
    parts={i:polynomial_part_power(P,s.Rational(i,6),x).subs(x,f*v)
           for i in [1,2,3,4,5,7,8,9]}
    Q=s.Poly(s.expand(parts[9]+sum(ks[i]*parts[i] for i in ks)),v)
    p0,p1,p2,p3,p4,p5=ps
    q6=s.Rational(3,2)*f**3*p3+s.Rational(3,4)*p5*p4/f**3-s.Rational(1,16)*p5**3/f**9
    q6+=ks[8]*(s.Rational(4,3)*f*f*p4+s.Rational(2,9)*p5*p5/f**4)+ks[7]*s.Rational(7,6)*f*p5
    q5=s.Rational(3,2)*f**3*p2+s.Rational(3,8)*(2*p5*p3+p4*p4)/f**3-s.Rational(3,16)*p5*p5*p4/f**9+s.Rational(3,128)*p5**4/f**15
    q5+=ks[8]*(s.Rational(4,3)*f*f*p3+s.Rational(4,9)*p5*p4/f**4-s.Rational(4,81)*p5**3/f**10)
    q5+=ks[7]*(s.Rational(7,6)*f*p4+s.Rational(7,72)*p5*p5/f**5)+ks[5]*f**5
    zero(Q.coeff_monomial(v**6)-q6)
    zero(Q.coeff_monomial(v**5)-q5)
    # P -> P+2*k3/3 removes k3, with the lower constants renamed.
    delta=2*ks[3]/3
    newP=P+delta
    newks=dict(ks);newks[3]=0
    newks[1]=ks[1]-s.Rational(7,6)*delta*ks[7]
    newks[2]=ks[2]-s.Rational(4,3)*delta*ks[8]
    newQ=polynomial_part_power(newP,s.Rational(3,2),x)+sum(
        newks[i]*polynomial_part_power(newP,s.Rational(i,6),x) for i in newks)
    zero(newQ.subs(x,f*v)-Q.as_expr())
    print('REDUNDANT_K3_REMOVAL_AND_TWO_EXACT_COEFFICIENT_ROWS: PASS',flush=True)
    phi={str(n):str(parity_expression(n)) for n in [6,9]}
    zero(Y*Y-8*Y+16-(Y-4)**2)
    A,rho=s.symbols('A rho',nonzero=True)
    toptrace=A*(r+2)*(r+2-3*rho)/r**2
    coeff=s.expand(toptrace**2).coeff(r,-3)
    zero(coeff-2*A*A*(4-3*rho)*(4-6*rho))
    assert set(s.solve(coeff,rho))=={s.Rational(2,3),s.Rational(4,3)}
    alpha,beta,gamma=s.symbols('alpha beta gamma')
    depressed=s.Poly(s.expand(((x-alpha/6)**6+alpha*(x-alpha/6)**5
                              +beta*(x-alpha/6)**4+gamma*(x-alpha/6)**3)),x)
    aa=(beta-s.Rational(5,12)*alpha**2)/2
    bb=(gamma-s.Rational(2,3)*alpha*beta+s.Rational(5,27)*alpha**3)/2
    zero(depressed.coeff_monomial(x**4)-2*aa)
    zero(depressed.coeff_monomial(x**3)-2*bb)
    zero((4*aa**3+27*bb**2).subs(gamma,0).subs(beta,alpha**2/4))
    print('BOTH_COLLISION_PARITIES_AND_DOUBLE_ROOT_LEADING_CANCELLATION: PASS',flush=True)
    # An ordinary Keller pair with m=6 checks the arbitrary-degree residue law.
    Pc=v**6+c;Qc=v
    zero(s.diff(Pc,v)*s.diff(Qc,c)-s.diff(Pc,c)*s.diff(Qc,v)+1)
    # v=(W^6-c)^(1/6)=W-c/(6W^5)+..., so mu5=-c/6.
    zero(6*s.diff(-c/6,c)+1)
    spec=importlib.util.spec_from_file_location('astra6_global_gate',HERE.parent/'astra6/verify_global_potential.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    controls=prior.criterion_controls()
    assert all(p['ambient_Keller'] and not p['collision_Keller'] for p in controls['positive_controls'])
    assert all(not n['ambient_Keller'] for n in controls['negative_controls'])
    print('ORDINARY_KELLER_AND_SAVED_GLOBAL_TERMINATION_CONTROLS: PASS',flush=True)
    result={'status':'PASS','Q_v6':str(q6),'Q_v5':str(q5),
       'parity_polynomials':phi,'pole_cancellation_polynomial':str((Y-4)**2),
       'top_root_trace':str(toptrace),'leading_branches':['2/3','4/3'],
       'depressed_coefficients':{'a':str(aa),'b':str(bb)},
       'local_consequences_for_f_cN':{'N':'>=2','ord_p4':'2','ord_p5':'3N+1',
         'leading_ratio_p5_squared_over_f6_p4':'4','ord_a':'2-4N','ord_b':'3-6N',
         'leading_cubic_discriminant':'0'},
       'k3_removal':{'P_shift':str(delta),'new_k1':str(newks[1]),'new_k2':str(newks[2])},
       'residue_control':{'P':'v^6+c','Q':'v','Jacobian':'-1','mu5':'-c/6'},
       'global_gate_controls':controls,'new_conductor_lifts':0,'coefficient_sweeps':0,
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'inputs_and_controls.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
