#!/usr/bin/env python3
"""Exact algebra for the global criterion and the written degree proofs.

This does not enumerate all potentials or prove the remaining component empty.
No conductor-adic approximations are computed.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
v,c,r = s.symbols('v c r')
R=3*c*v-2
b=-3*c*v*v+4*v+2
trace={v:3*(r+2)/r**2,c:r**2/9}

def zero(f):
    assert s.cancel(s.expand(f)) == 0, f

def J(p,q):
    return s.diff(p,v)*s.diff(q,c)-s.diff(p,c)*s.diff(q,v)

def in_B(p):
    tr=s.cancel(p.subs(trace,simultaneous=True))
    return s.cancel(tr-tr.subs(r,-r)) == 0

def gate(H):
    A=s.diff(H,v);C=s.diff(H,c)+v
    g=s.Poly(s.gcd(A,C),v,c).monic().as_expr()
    residual=s.expand(C*s.diff(g,v)-A*s.diff(g,c)-g)
    aa,bb=s.cancel(A/g),s.cancel(C/g)
    zero(s.diff(aa,c)-s.diff(bb,v)-residual/g**2)
    result={'g':str(g),'identity_residual':str(residual),
            'admissible_H':in_B(H+2*R/3),'g_in_B':in_B(g)}
    if residual != 0:
        result['ambient_Keller']=False
        return result
    q=s.integrate(aa,v)
    rem=s.expand(bb-s.diff(q,c))
    zero(s.diff(rem,v))
    q=s.expand(q+s.integrate(rem,c))
    zero(J(g,q)-1)
    result.update(ambient_Keller=True,Q=str(q),Q_in_B=in_B(q))
    result['collision_Keller']=result['admissible_H'] and result['g_in_B']
    if result['collision_Keller']:
        assert in_B(q)
        for f in (g,q):
            zero(f.subs({v:-s.Rational(1,3),c:4})-
                 f.subs({v:s.Rational(2,3),c:4}))
    return result

def potential(p,q):
    zero(J(p,q)-1)
    H=s.integrate(p*s.diff(q,v),v)
    rem=s.expand(p*s.diff(q,c)-v-s.diff(H,c))
    zero(s.diff(rem,v))
    return s.expand(H+s.integrate(rem,c))

def criterion_controls():
    p=v+c*c;q=c+p*p
    positives=[gate(0),gate(-c*v),gate(-c*v-v**3/3),gate(potential(p,q))]
    assert all(x['ambient_Keller'] and not x['collision_Keller'] for x in positives)
    inv=(R*v-3)/6
    negatives=[gate(-2*R/3),gate(-c*v-27*c*c*inv**3)]
    assert all(x['admissible_H'] and not x['ambient_Keller'] for x in negatives)
    # Global rejection of the old formal limit; no new truncations.
    k=s.symbols('k',integer=True)
    assert s.expand(1+2*k).coeff(k)==2
    f=s.Function('f')(c)
    zero(J(c,-v+f)-1)
    tr=s.cancel((-v+f).subs(trace,simultaneous=True))
    zero(tr-tr.subs(r,-r)+6/r)
    return {'status':'PASS','positive_controls':positives,'negative_controls':negatives,
            'formal_limit_rejection':'valuation_c(c*(Q+v)^2)=1+2k cannot be 0',
            'no_additional_conductor_orders':True}

def low_degree():
    a,d,e,f,h0,b0=s.symbols('a d e f h0 b0')
    H=a*v*v/2+b0*v*c+d*c*c/2+e*v+f*c+h0
    M=s.Matrix([[a,b0,e],[b0+1,d,f]])
    minors=[s.expand(M[:,[i,j]].det()) for i,j in [(0,1),(0,2),(1,2)]]
    assert minors==[a*d-b0*b0-b0,a*f-b0*e-e,b0*f-d*e]
    assert minors[0].subs({a:0,b0:-2})==-2
    lam=s.symbols('lam',nonzero=True)
    Fc=s.Function('F')(c)
    H=Fc+lam*b-2*c*v
    zero(s.diff(H,v)+2*(lam*R+c))
    vv=(2*lam-c)/(3*lam*c)
    zero((s.diff(H,c)+v).subs(v,vv)-s.diff(Fc,c)
         +4*lam/(3*c*c)-2/(3*c))
    return {'status':'PASS','quadratic_minors':[str(x) for x in minors],
            'cubic_and_unbounded_F_family':'gcd=1 by the written irreducible-factor proof'}

def nonsquare46():
    x,z=s.symbols('x z')
    a,bb,d,da,db,dd,k=s.symbols('a bb d da db dd k')
    D=lambda f:s.diff(f,a)*da+s.diff(f,bb)*db+s.diff(f,d)*dd
    P=x**4+a*x*x+bb*x+d
    Q=x**6+3*a*x**4/2+3*bb*x**3/2+(3*a*a/8+3*d/2)*x*x \
      +3*a*bb*x/4-a**3/16+3*a*d/4+3*bb*bb/8+k*(x*x+a/2)
    jac=s.Poly(s.expand(s.diff(P,x)*D(Q)-D(P)*s.diff(Q,x)),x)
    I2=3*a*a*bb/4-3*bb*d-2*bb*k
    I1=-3*a**4/32+3*a*a*d/4+3*a*bb*bb/4+a*a*k/2-3*d*d/2-2*d*k
    zero(jac.coeff_monomial(x*x)-D(I2))
    zero(jac.coeff_monomial(x)-D(I1))
    zero(I2.subs(d,a*a/4+z-2*k/3)+3*bb*z)
    zero(I1.subs(d,a*a/4+z-2*k/3)-(3*a*bb*bb/4-3*z*z/2+2*k*k/3))
    zero(jac.coeff_monomial(1).subs({d:a*a/4-2*k/3,dd:a*da/2})-3*bb*bb*db/4)
    h,u,dh,du=s.symbols('h u dh du',nonzero=True)
    ee=3*u*u/(8*h)
    ep=s.diff(ee,h)*dh+s.diff(ee,u)*du
    zero(u*ep-3*u*u*(2*h*du-u*dh)/(8*h*h))
    E,kap,m=s.symbols('E kap m',nonzero=True)
    U=-kap/(m*E);HH=3*kap*kap/(8*m*m*E**3)
    zero(U*U/HH-8*E/3)
    zero(-s.Rational(1,2)*(8*E/3)+E+E/3)
    # Exact trace equation used in the square branch.
    B3,C2,D1,E0=s.symbols('B3 C2 D1 E0')
    poly=h*h*v**4+B3*v**3+C2*v*v+D1*v+E0
    tr=s.cancel(poly.subs(trace,simultaneous=True))
    phi=27*c**3*D1+36*c*c*C2+(36*c+27*c*c)*B3+(32+72*c)*h*h
    zero(tr-tr.subs(r,-r)-2*r*phi.subs(c,r*r/9)/(3*(r*r/9))**4)
    return {'status':'PASS','upper_integrals':[str(I2),str(I1)],
            'last_row_on_z_zero':'3*bb^2*bb_prime/4',
            'rational_equation':'u*(3*u^2/(8*h))prime=kappa',
            'uncancelled_pole_coefficient':'-E/3'}

def degree_strata():
    unresolved=[]
    for total in range(2,15):
        for m in range(1,total//2+1):
            n=total-m
            if m<=2 or s.gcd(m,n)==1 or n%m==0 or (m,n)==(4,6):
                continue
            unresolved.append((total,m,n))
    assert unresolved==[(14,4,10),(14,6,8)]
    rho=s.symbols('rho')
    top=v*(c*v-rho)
    odd=[]
    for power in (3,4):
        tr=s.expand(top.subs(trace,simultaneous=True)**power)
        coefficient=s.factor(tr.coeff(r,-2*power+1))
        expected=power*2**(power-1)*(2-3*rho)**(power-1)*(4-3*rho)
        zero(coefficient-expected)
        odd.append(str(coefficient))
    return {'status':'PASS','first_unexcluded_stratum':unresolved,
            'leading_odd_coefficients':odd,'both_branches':['2/3','4/3'],
            'scope':'Arithmetic coverage of the written arbitrary-coefficient proofs; no degree-box search'}

def main():
    result={}
    for name,fn in [('EXACT_CRITERION',criterion_controls),('LOWEST_DEGREES',low_degree),
                    ('NONSQUARE_46_POLE',nonsquare46),('DEGREE_STRATA',degree_strata)]:
        result[name]=fn();print(name+': PASS',flush=True)
    result.update(verdict='OPEN',counterexample_found=False,
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
