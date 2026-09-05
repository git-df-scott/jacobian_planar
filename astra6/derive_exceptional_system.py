#!/usr/bin/env python3
"""Emit the complete rational coefficient system for partial degrees (6,8).

Polynomial parts at v=infinity are finite exact expressions. The five
remaining equations are recorded as OPEN, not certified inconsistent.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
v,t=s.symbols('v t')
h=s.symbols('h',nonzero=True)
ps=s.symbols('p0:6');dh=s.symbols('dh');dps=s.symbols('dp0:6')
k2,k4=s.symbols('k2 k4')
p=list(ps)+[h**3]
dp=list(dps)+[3*h*h*dh]

def derivative(f):
    return s.diff(f,h)*dh+sum(s.diff(f,x)*dx for x,dx in zip(ps,dps))

def part(j):
    # P^(j/3) with leading h^j v^(2j). Coefficient truncation is exact.
    lower=sum(ps[i]*t**(6-i)/h**3 for i in range(6))
    power=s.Poly(1,t)
    lowpoly=s.Poly(lower,t)
    out={0:s.Integer(1)}
    for n in range(1,2*j+1):
        raw=power*lowpoly
        power=s.Poly.from_dict({mon:coef for mon,coef in raw.terms() if mon[0]<=2*j},t)
        bn=s.binomial(s.Rational(j,3),n)
        for (degree,),coef in power.terms():
            out[degree]=out.get(degree,0)+bn*coef
    return s.expand(sum(h**j*coef*v**(2*j-degree) for degree,coef in out.items()))

def main():
    Q=s.Poly(part(4)+k4*part(2)+k2*part(1),v)
    q=[s.factor(Q.coeff_monomial(v**i)) for i in range(9)]
    dq=[derivative(x) for x in q]
    rows={}
    for degree in range(13,-1,-1):
        row=sum(i*p[i]*dq[j]-j*dp[i]*q[j]
                for i in range(7) for j in range(9) if i+j==degree+1)
        row=s.factor(s.cancel(row))
        if degree>=5:
            assert row==0,(degree,row)
        else:rows[str(degree)]=str(row)
    print('UPPER_JACOBIAN_ROWS_5_THROUGH_13: PASS',flush=True)
    root=part(1)
    P=sum(p[i]*v**i for i in range(7))
    remainder=s.Poly(s.expand(P-root**3),v)
    assert remainder.degree()<=3
    print('QUADRATIC_ROOT_REMAINDER: PASS',flush=True)
    result={'status':'EXACT_REDUCTION_VERIFIED_REMAINING_SYSTEM_OPEN',
            'variables':{'coefficient_functions':['h']+[str(x) for x in ps],
                         'derivative_symbols':['dh']+[str(x) for x in dps],
                         'constant_parameters':['k2','k4','kappa']},
            'P_coefficients':[str(x) for x in p],
            'Q_coefficients':[str(x) for x in q],
            'quadratic_root':str(root),
            'remaining_Jacobian_rows':rows,
            'required_right_hand_sides':{'4':'0','3':'0','2':'0','1':'0','0':'kappa != 0'},
            'additional_conditions':['h has a simple zero at c=0',
                'h,p_i and every rational q_j are polynomial in c',
                'Phi_6(P)=Phi_8(Q)=0 as defined in EXCEPTIONAL_68.md'],
            'leading_branches':['rho=2/3','rho=4/3'],
            'solutions_found':0,'classification_complete':False,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'exceptional_system.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
