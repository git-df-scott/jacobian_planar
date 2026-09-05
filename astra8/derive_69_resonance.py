#!/usr/bin/env python3
"""Exact finite polynomial-part and residue system for partial degrees (6,9).

This is a symbolic reduction, not a solver or a conductor-adic lift.
"""
from pathlib import Path
import hashlib, json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'astra7'))
import sympy as s
from exact_tools import polynomial_part_power, derivative_operator, zero

HERE = Path(__file__).resolve().parent
x, t = s.symbols('x t')
a,b,u,w,z = variables = s.symbols('a b u w z')
derivatives = s.symbols('da db du dw dz')
D = derivative_operator(variables, derivatives)
indices = [1,2,4,5,7,8]
ks = dict(zip(indices, s.symbols('k1 k2 k4 k5 k7 k8')))
R = x**3+a*x+b
P = s.expand(R**2+u*x*x+w*x+z)

def power_coefficients(exponent, depth):
    """Coefficients in (1+lower(t))**exponent through t**depth."""
    small = s.Poly(sum(s.Poly(P,x).coeff_monomial(x**i)*t**(6-i)
                       for i in range(5)),t)
    power = s.Poly(1,t)
    out = {0:s.Integer(1)}
    for j in range(1, depth//2+1):
        power = s.Poly.from_dict({mon:coef for mon,coef in (power*small).terms()
                                  if mon[0]<=depth},t)
        for (i,),coef in power.terms():
            out[i] = out.get(i,0)+s.binomial(exponent,j)*coef
    return {i:s.expand(coef) for i,coef in out.items()}

def main():
    parts = {i:polynomial_part_power(P,s.Rational(i,6),x)
             for i in indices+[9]}
    Q = s.expand(parts[9]+sum(ks[i]*parts[i] for i in indices))
    qprime = s.Poly(s.diff(Q,x),x)
    mu = {}
    # Change-of-variable residue: mu_i=-Res_x(Q_x P^(i/6))/i.
    for i in range(1,6):
        coeff = power_coefficients(s.Rational(i,6),i+9)
        mu[i] = s.expand(-sum(coef*coeff.get(degree+i+1,0)
                              for (degree,),coef in qprime.terms())/i)
    J = s.Poly(s.expand(s.diff(P,x)*D(Q)-D(P)*s.diff(Q,x)),x)
    assert J.degree()<=4
    reconstructed = 0
    multipliers = {}
    for i in range(1,6):
        coeff = power_coefficients(-s.Rational(i,6),5-i)
        multiplier = s.expand(sum(coef*value*x**(degree-i-depth)
                      for (degree,),coef in s.Poly(s.diff(P,x),x).terms()
                      for depth,value in coeff.items() if degree-i-depth>=0))
        multipliers[i] = multiplier
        reconstructed += multiplier*D(mu[i])
    zero(J.as_expr()-reconstructed)
    for i in range(1,6):
        assert s.Poly(multipliers[i],x).degree()==5-i
        assert s.Poly(multipliers[i],x).LC()==6
    print('ALL_JACOBIAN_ROWS_AND_FIVE_RESIDUE_IDENTITIES: PASS',flush=True)
    # Recover the noncube specialization independently.
    noncube = {ks[i]:0 for i in indices}
    explicit = R**3+s.Rational(3,2)*R*(u*x*x+w*x+z)+s.Rational(3,8)*(u*u*x+2*u*w)
    zero(Q.subs(noncube)-explicit)
    print('NONCUBE_SPECIALIZATION: PASS',flush=True)
    result = {
      'status':'EXACT_REDUCTION_VERIFIED_RESONANT_SYSTEM_OPEN',
      'P':str(P),'Q':str(Q),'polynomial_parts':{str(i):str(parts[i]) for i in parts},
      'residues_mu':{str(i):str(mu[i]) for i in mu},
      'Jacobian_derivative_multipliers':{str(i):str(multipliers[i]) for i in multipliers},
      'exact_equations':['mu_1=C1','mu_2=C2','mu_3=C3','mu_4=C4',
                         'mu_5=C5+kappa*c^(1-N)/(6*(1-N))'],
      'equivalent_last_differential_row':'6*c^N*d(mu_5)/dc=kappa != 0',
      'Laurent_polynomial_coefficient_functions':['a','b','u','w','z','eta'],
      'leading_factor':'f=c^N, N an integer >=2; h=f^3',
      'constants':[str(ks[i]) for i in indices]+['C1','C2','C3','C4','C5','kappa'],
      'reconstruction':'x=c^N*(v+eta(c)); substitute into the displayed P,Q',
      'removed_freedoms':['constant Q term','constant multiple of P in Q',
                         'k3 by P -> P+2*k3/3','leading scalar gamma'],
      'additional_conditions':['Both reconstructed polynomials belong to C[c,v]',
                               'Both collision traces are even in r'],
      'claims':{'counterexample':False,'resonant_component_closed':False,
                'irreducibility_proved':False,'arbitrary_degree_closure':False},
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'resonant_69_system.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__': main()
