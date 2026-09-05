#!/usr/bin/env python3
"""Exact Astra 11 calculations. Run from any directory; --write refreshes outputs.

Requires Python 3 and SymPy. No numerical solving or modular inference.
The leading-edge classification is not a classification of Keller pairs.
"""
import argparse
import json
from pathlib import Path
import sys
import sympy as s

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
T, x, y = s.symbols('T x y')
c1, c2, c3, a0, a1, a2, a3 = variables = s.symbols('c1 c2 c3 a0 a1 a2 a3')


def leading_system():
    B = T**4 + a3*T**3 + a2*T**2 + a1*T + a0
    g = -1+c1*T+c2*T**2+c3*T**3+(s.Rational(4,5)-c1-c2-c3)*T**4
    E = s.expand(4*T*(T-1)*B*s.diff(g,T)
                 -3*T*(T-1)*s.diff(B,T)*g-(4*T+1)*B*g-B)
    quotient, remainder = s.div(E, T*(T-1), T)
    assert remainder == 0
    equations = s.Poly(quotient, T).all_coeffs()
    assert len(equations) == 7
    G = s.groebner(equations, *variables, order='grevlex')
    assert G.is_zero_dimensional
    L = G.fglm('lex')
    assert len(L.polys) == 7
    assert all(L.reduce(e)[1] == 0 for e in equations)
    # Recompute lex from the seven triangular polynomials as a separate check.
    replay=s.groebner([p.as_expr() for p in L.polys], *variables,domain=s.QQ)
    assert [p.as_expr() for p in replay.polys] == [p.as_expr() for p in L.polys]
    eliminant = s.Poly(L.polys[-1].as_expr(), a3).monic().as_expr()
    assert s.degree(eliminant,a3) == 17
    assert s.degree(s.gcd(eliminant,s.diff(eliminant,a3)),a3) == 0
    parameters = {}
    for v, poly in zip(variables[:-1], L.polys[:-1]):
        assert s.diff(poly.as_expr(),v) == 1
        parameters[v] = -poly.as_expr().subs(v,0)
        assert parameters[v].free_symbols <= {a3}
    factors = s.factor_list(eliminant,a3)[1]
    branches = []
    for factor, exponent in factors:
        assert exponent == 1
        factor = s.Poly(factor,a3).clear_denoms()[1].primitive()[1].as_expr()
        params = {v:s.rem(p,factor,a3) for v,p in parameters.items()}
        bb = s.expand(B.subs(params, simultaneous=True))
        gg = s.expand(g.subs(params, simultaneous=True))
        assert all(s.rem(s.expand(e.subs(params,simultaneous=True)),factor,a3)==0
                   for e in equations)
        for nonzero in [bb.subs(T,0),bb.subs(T,1),s.expand(gg).coeff(T,4)]:
            assert s.degree(s.gcd(factor,nonzero),a3) == 0
        if s.degree(factor,a3) == 1:
            root = s.solve(factor,a3)[0]
            BB = s.Poly(bb.subs(a3,root),T)
        else:
            field = s.QQ.alg_field_from_poly(s.Poly(factor,a3))
            BB = s.Poly(bb.subs(a3,field.ext.as_expr()),T,domain=field)
        pattern = sorted([[q.degree(),e] for q,e in BB.sqf_list()[1]])
        branches.append({'minimal_polynomial':str(factor),
                         'degree':int(s.degree(factor,a3)),
                         'parameters':{str(v):str(s.factor(p)) for v,p in params.items()},
                         'B_squarefree_factor_degrees_and_multiplicities':pattern})
    assert sorted(b['degree'] for b in branches)==[1,2,4,4,6]
    print('PASS: exact leading ideal, 17 reduced marked solutions, five number fields',flush=True)
    return {'equations':[str(e) for e in equations],
            'lex_basis':[str(p.as_expr()) for p in L.polys],
            'eliminant':str(s.factor(eliminant)), 'branches':branches,
            'scope':'Leading auxiliary equation only; not Keller pairs.'}


def transport_and_controls():
    B = T**4-5*T**3+10*T**2-10*T+5
    h = (T-1)**3*B
    f = -(T-1)*B/5
    assert s.expand(4*T*h*s.diff(f,T)+(h-3*T*s.diff(h,T))*f-h)==0
    assert s.gcd(B,s.diff(B,T))==1
    root_before = y*h.subs(T,x**4*y)
    root_sheared = root_before.subs(y,y+x**-4)
    root_after = s.expand(root_sheared.subs({x:1/x,y:x**4*y},simultaneous=True))
    assert s.expand(root_after-x**4*y**3*(1+y**5))==0
    assert s.Poly(root_after,x,y).degree(y)==8
    # Highest corner under swap, any y-translation, and the displayed twist.
    swapped_corner = (28,8)
    transported_corner = (4*swapped_corner[1]-swapped_corner[0],swapped_corner[1])
    assert transported_corner==(4,8) and transported_corner!=(4,4)
    bracket = lambda P,Q:s.expand(s.diff(P,x)*s.diff(Q,y)-s.diff(P,y)*s.diff(Q,x))
    assert bracket(x+y**2,y)==1
    assert bracket(x**2*y,x)==-x**2
    # Fractional terminal chart is made ordinary by x=t^4.
    t, z, a = s.symbols('t z a',nonzero=True)
    terminal = []
    for sign in [-1,1]:
        b=a**2*(s.Rational(1,3)+sign*s.sqrt(6)/18)
        cc=4*a/3
        d=2*a**2*(9+sign*s.sqrt(6))/27
        e=2*a**3*(4+sign*s.sqrt(6))/81
        F=z**2+a*z+b
        G=z**3+cc*z**2+d*z+e
        expr=s.expand(3*z*F*s.diff(G,z)-4*z*s.diff(F,z)*G-F*G)
        assert s.simplify(expr+b*e)==0
        PP=t**3*y*F.subs(z,t**9*y**4)
        QQ=t*G.subs(z,t**9*y**4)
        JJ=s.expand((s.diff(PP,t)*s.diff(QQ,y)-s.diff(PP,y)*s.diff(QQ,t))/(4*t**3))
        assert s.simplify(JJ+b*e/4)==0
        assert s.simplify((b*e).subs(a,1)) != 0
        terminal.append({'sign':sign,'b':str(b),'c':str(cc),'d':str(d),'e':str(e),
                         'kappa':str(s.simplify(-b*e/4))})
    # Completeness of the terminal calculation after eliminating c,d,e.
    a,b=s.symbols('a b')
    cc=4*a/3; d=s.expand((a*cc+8*b)/6); e=s.expand((-2*a*d+5*b*cc)/9)
    last=s.factor(-5*a*e+2*b*d)
    assert s.expand(last-s.Rational(4,81)*(5*a**4-36*a*a*b+54*b*b))==0
    print('PASS: corner transport, surviving leading control, terminal forms, Keller controls',flush=True)
    return {'transported_base_corner':[4,8],
            'rational_root':'x**4*y**3*(1+y**5)', 'terminal_forms':terminal,
            'terminal_remaining_equation':str(last)}


def graded_obstruction():
    c=s.Function('c')(y); A=s.Function('A')(y); B=s.Function('B')(y)
    F=s.Rational(4,3)*c*B
    E=s.Rational(4,3)*c*A+s.Rational(2,9)*B**2/c**2
    D=s.Rational(4,9)*A*B/c**2-s.Rational(4,81)*B**3/c**5
    P=x**2*A+x**7*B+x**12*c**3
    Q=x*D+x**6*E+x**11*F+x**16*c**4
    J=s.Poly(s.expand(s.diff(P,x)*s.diff(Q,y)-s.diff(P,y)*s.diff(Q,x)),x)
    assert all(s.simplify(J.coeff_monomial(x**i))==0 for i in [12,17,22,27])
    # At any simple zero of c, polynomiality forces B=c^2*b locally.
    b=s.Function('b')(y)
    E2=s.Rational(4,3)*c*A+s.Rational(2,9)*c**2*b**2
    D2=s.Rational(4,9)*A*b-s.Rational(4,81)*c*b**3
    B2=c**2*b
    residual7=s.expand(2*A*s.diff(E2,y)-6*s.diff(A,y)*E2
                        +7*B2*s.diff(D2,y)-s.diff(B2,y)*D2)
    cp=s.symbols('c_prime_at_root',nonzero=True)
    at_root=residual7.subs(s.diff(c,y),cp).subs(c,0)
    assert s.simplify(at_root-s.Rational(8,3)*cp*A**2)==0
    print('PASS: graded slice identities and simple-root obstruction (all coefficient degrees)',flush=True)
    return {'D':str(D),'E':str(E),'F':str(F),
            'residual_x7_at_simple_root':'(8/3)*c_prime(alpha)*A(alpha)**2',
            'scope':'Only P rows 2,7,12 and Q rows 1,6,11,16; other rows remain live.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result={'status':'OPEN: no counterexample', 'leading':leading_system(),
            'controls':transport_and_controls(),'graded':graded_obstruction()}
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write:
        (OUT/'certificate.json').write_text(encoded)
        (OUT/'leading_lex.txt').write_text('\n'.join(result['leading']['lex_basis'])+'\n')
    else:
        assert json.loads((OUT/'certificate.json').read_text())==result
        print('PASS: regenerated certificate matches committed output',flush=True)


if __name__=='__main__':
    main()
