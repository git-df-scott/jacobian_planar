#!/usr/bin/env python3
"""Verify local coordinate conversions and retain the global gate controls.

Does not rerun the degree<=13 obstruction or any conductor-adic lifting.
"""
from pathlib import Path
import hashlib,importlib.util,json,math,sys
sys.dont_write_bytecode=True
import sympy as s
from exact_tools import zero

HERE=Path(__file__).resolve().parent
v,c,x,h,ss,tt,uu,ww=s.symbols('v c x h ss tt uu ww')

def main():
    vv=x/s.sqrt(h)-ss/(2*h)
    root=h*v*v+ss*v+tt
    aa=tt-ss*ss/(4*h)
    zero(root.subs(v,vv)-(x*x+aa))
    P4=root**2+uu*v+ww
    zero(P4.subs(v,vv)-((x*x+aa)**2+uu*x/s.sqrt(h)+ww-uu*ss/(2*h)))
    S3,S2,S1,S0=s.symbols('S3 S2 S1 S0')
    remainder=S3*v**3+S2*v*v+S1*v+S0
    bb=S3/h**s.Rational(3,2)
    dd=S2/h-3*ss*S3/(2*h*h)
    ee=S1/s.sqrt(h)-ss*S2/h**s.Rational(3,2)+3*ss*ss*S3/(4*h**s.Rational(5,2))
    ff=S0-ss*S1/(2*h)+ss*ss*S2/(4*h*h)-ss**3*S3/(8*h**3)
    zero(remainder.subs(v,vv)-(bb*x**3+dd*x*x+ee*x+ff))
    zero(s.diff(s.sqrt(h)*(v+ss/(2*h)),v)-s.sqrt(h))
    # Exact leading-root cancellation, with generic rho; no finite-order
    # conductor approximation is involved.
    h1,rho=s.symbols('h1 rho',nonzero=True)
    top=h1*v*(c*v-rho)
    top4=s.Poly(s.expand(top**2),v)
    top6=s.Poly(s.expand(top**3),v)
    p3,p2=top4.coeff_monomial(v**3),top4.coeff_monomial(v**2)
    zero(p2/(2*h1*c)-p3*p3/(8*(h1*c)**3))
    zero(p3/(2*h1*c)+rho*h1)
    p5,p4=top6.coeff_monomial(v**5),top6.coeff_monomial(v**4)
    zero(p4/(3*(h1*c)**2)-p5*p5/(9*(h1*c)**5))
    zero(p5/(3*(h1*c)**2)+rho*h1)
    # The pole of a has nonzero coefficient on each of the retained branches.
    pole=-rho*rho*h1/4
    assert all(pole.subs(rho,r)!=0 for r in [s.Rational(2,3),s.Rational(4,3)])
    print('LOCAL_CONVERSIONS_AND_BOTH_LEADING_BRANCHES: PASS',flush=True)
    spec=importlib.util.spec_from_file_location('astra6_global_gate',HERE.parent/'astra6/verify_global_potential.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    controls=prior.criterion_controls()
    assert all(p['ambient_Keller'] and not p['collision_Keller'] for p in controls['positive_controls'])
    assert all(not n['ambient_Keller'] for n in controls['negative_controls'])
    print('ORDINARY_KELLER_POSITIVE_AND_GLOBAL_NEGATIVE_CONTROLS: PASS',flush=True)
    # Only the next integer degree sum is classified. This is not a
    # polynomial-coefficient sweep or a rerun of the previous obstruction.
    next_pairs=[(m,15-m) for m in range(3,8)
                if math.gcd(m,15-m)>1 and (15-m)%m!=0]
    assert next_pairs==[(6,9)]
    result={'status':'PASS','root_conversion':'R=x^2+a',
      'cubic_remainder_conversion':{'b':str(bb),'d':str(dd),'e':str(ee),'f':str(ff)},
      'original_Jacobian_factor':'sqrt(h)',
      'leading_root_pole_cancellations':'0 for both systems, for generic rho',
      'coefficient_of_c_minus_1_in_a':str(pole),
      'branches_checked':['2/3','4/3'],'global_gate_controls':controls,
      'next_unexcluded_potential_v_degree':15,'next_coordinate_v_degrees':next_pairs,
      'degree_13_obstruction_reopened':False,'new_conductor_lifts':0,
      'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                       for name in ['verify_inputs_and_controls.py','exact_tools.py']}}
    (HERE/'controls_and_inputs.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
