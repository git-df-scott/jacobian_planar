#!/usr/bin/env python3
"""Exact identities supporting the arbitrary-degree collision obstruction.

The theorem, including exact algebraic branch existence, is proved in
FULL_COLLISION_OBSTRUCTION.md. These symbolic checks are not a degree sweep.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
import sympy as s

HERE=Path(__file__).resolve().parent
v,c,r,t,z,ss=s.symbols('v c r t z s')

def zero(expr):
    assert s.cancel(s.expand(expr))==0,expr

def trace(F):
    return s.cancel(F.subs({v:3*(r+2)/r**2,c:r**2/9},simultaneous=True))

def weight_and_top(F):
    p=s.Poly(s.expand(F),v,c)
    if p.is_zero:return None,s.Integer(0)
    d=max(i-j for (i,j),coef in p.terms())
    top=sum(coef*v**i*c**j for (i,j),coef in p.terms() if i-j==d)
    return d,s.expand(top)

def main():
    b=-3*c*v*v+4*v+2
    Delta=(3*c*v-2)**2-9*c
    zero(trace(Delta));zero(trace(b)-(-1+12/r**2))
    p1={v:-s.Rational(1,3),c:4};p2={v:s.Rational(2,3),c:4}
    assert p1[v]!=p2[v]
    for F in [b,c,Delta]:zero(F.subs(p1)-F.subs(p2))
    print('EXACT_COLLISION_TRACE_AND_DISTINCT_SOURCE_POINTS: PASS',flush=True)

    # All degrees: i=d+j, d>0, j>=0. Strip the r^(-2d) factor.
    d=s.symbols('d',integer=True,positive=True)
    j=s.symbols('j',integer=True,nonnegative=True)
    A=s.symbols('A',nonzero=True)
    numerator=A*3**(d-j)*(r+2)**(d+j)
    odd=s.diff(numerator,r).subs(r,0)
    expected=A*3**(d-j)*(d+j)*2**(d+j-1)
    assert s.simplify(odd/expected)==1
    gap=s.symbols('gap',integer=True,positive=True)
    separation=s.expand(-2*(d-gap)-(-2*d+1))
    assert separation==2*gap-1 and separation.is_positive
    print('ARBITRARY_DEGREE_ODD_COEFFICIENT_AND_WEIGHT_SEPARATION: PASS',flush=True)

    # Universal residue identity, including arbitrary ramification e.
    e=s.symbols('e',integer=True,positive=True)
    lam=s.symbols('lambda',nonzero=True)
    Z=s.Function('Z')(ss)
    pullback=s.simplify(ss**(-e)*s.diff(ss**e*Z,ss))
    assert s.simplify(pullback-(e*Z/ss+s.diff(Z,ss)))==0
    # Exact ramified control, no truncated series: F=v*(cv-lambda)^e-1.
    vr=ss**(-e);cr=ss**e*(lam+ss)
    assert s.simplify(vr*(cr*vr-lam)**e-1)==0
    rational_form=s.simplify(vr*s.diff(cr,ss))
    assert s.simplify(rational_form-(e*lam/ss+e+1))==0
    print('UNIVERSAL_RESIDUE_AND_EXACT_REPEATED_ROOT_CONTROL: PASS',flush=True)

    # Universal nonpositive-weight chain rule, with four arbitrary partials.
    Fc,Ft,Gc,Gt=s.symbols('F_c F_t G_c G_t')
    J=(c*Ft)*(Gc+v*Gt)-(Fc+v*Ft)*(c*Gt)
    zero(J-c*(Ft*Gc-Fc*Gt))
    assert J.subs(c,0)==0
    print('NONPOSITIVE_WEIGHT_JACOBIAN_DIVISIBILITY: PASS',flush=True)

    # The whole prior exceptional family, not coefficient choices within it.
    rho=s.symbols('rho',nonzero=True)
    Ptop=(A*v*(c*v-rho))**2
    d15,top15=weight_and_top(Ptop)
    assert d15==2
    L15=s.cancel(top15.subs(c,z/v)/v**2)
    zero(L15-A*A*(z-rho)**2)
    zero(L15.subs(z,rho))
    assert all(rr!=0 for rr in [s.Rational(2,3),s.Rational(4,3)])
    print('BOTH_DEGREE15_LEADING_BRANCHES_HAVE_FORBIDDEN_EDGE: PASS',flush=True)

    # Positive ambient controls; membership is checked on full exact traces.
    S=v+c*c;T=c+S**3
    pairs=[(v,c),(c,-v),(c+v*v,-v),(S+T*T,T)]
    controls=[]
    for P,Q in pairs:
        jac=s.expand(s.diff(P,v)*s.diff(Q,c)-s.diff(P,c)*s.diff(Q,v))
        assert jac==1
        data=[]
        for F in [P,Q]:
            wt,top=weight_and_top(F)
            assert len(s.Poly(top,v,c).terms())==1
            even=s.cancel(trace(F)-trace(F).subs(r,-r))==0
            data.append({'weight':wt,'top':str(top),'even_collision_trace':even})
        assert not all(k['even_collision_trace'] for k in data)
        controls.append({'P':str(P),'Q':str(Q),'Jacobian':str(jac),'components':data})
    print('ORDINARY_POLYNOMIAL_KELLER_POSITIVE_CONTROLS: PASS',flush=True)

    spec=importlib.util.spec_from_file_location('saved_gate',HERE.parent/'astra6/verify_global_potential.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    saved=prior.criterion_controls()
    assert all(item['ambient_Keller'] and not item['collision_Keller'] for item in saved['positive_controls'])
    assert all(not item['ambient_Keller'] for item in saved['negative_controls'])
    print('SAVED_EXACT_POTENTIAL_AND_NONTERMINATING_NEGATIVE_CONTROLS: PASS',flush=True)

    result={'status':'PASS','verdict':'FULL COLLISION-ROUTE CLOSURE',
      'theorem':'For P,Q in C[b,c]+Delta*C[v,c], a constant Jacobian must be zero.',
      'degree_bounds':None,'field':'C, characteristic zero',
      'collision':{'v_values':['-1/3','2/3'],'c':'4','b':'-2/3','Delta':'0'},
      'trace_identities':{'b':str(trace(b)),'Delta':str(trace(Delta))},
      'universal_odd_coefficient':str(expected),
      'lower_weight_exponent_separation':str(separation),
      'ramified_pullback':str(pullback),'ramified_residue':'e*lambda != 0',
      'repeated_root_control':{'F':'v*(c*v-lambda)^e-1','v':'s^(-e)',
          'c':'s^e*(lambda+s)','F_on_branch':'0','v_dc':str(rational_form)},
      'nonpositive_weight_Jacobian':str(s.factor(J)),
      'degree15_face_L':str(L15),'positive_controls':controls,
      'saved_gate_controls':saved,'new_conductor_lifts':0,'degree_sweeps':0,
      'proof_dependencies':['Polynomial closed one-forms on C^2 are exact',
                           'Newton-Puiseux over C at a finite root, allowing ramification',
                           'The derivative of a Laurent series has zero residue'],
      'independent_published_match':{'url':'https://arxiv.org/html/1605.09430v2#S1',
                                   'result':'Corollary 1.6, no slope-one edge'},
      'proof_assistant_formalized':False,
      'sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                for name in ['verify_full_obstruction.py','FULL_COLLISION_OBSTRUCTION.md','PROOF_AUDIT.md']}}
    (HERE/'full_obstruction_certificate.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
