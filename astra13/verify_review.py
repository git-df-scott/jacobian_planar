#!/usr/bin/env python3
"""Exact algebra supporting the five-branch review; not a full Keller solve."""
import json
from pathlib import Path
import sympy as s
from math import gcd

ROOT=Path(__file__).resolve().parents[1]
A,T,z,b=s.symbols('A T z b')
branches=json.loads((ROOT/'astra11/certificate.json').read_text())['leading']['branches']
patterns=[]
for br in branches:
    if br['degree']==1:
        BB=s.Poly(T**4-5*T**3+10*T**2-10*T+5,T)
    else:
        q=s.Poly(s.sympify(br['minimal_polynomial'],locals={'a3':A}),A)
        K=s.QQ.alg_field_from_poly(q,alias='A')
        p={k:K.from_sympy(s.sympify(v,locals={'a3':K.ext}))
           for k,v in br['parameters'].items() if k.startswith('a')}
        BB=s.Poly.from_list([K.one,K.unit,p['a2'],p['a1'],p['a0']],T,domain=K)
    pat=[3]+[e for f,e in BB.sqf_list()[1] for _ in range(f.degree())]
    patterns.append(pat)
assert [sorted(p) for p in patterns]==[sorted(p) for p in
    [[3,1,1,1,1],[3,4],[3,2,2],[3,3,1],[3,2,1,1]]]
genera=[(-6+sum(4-gcd(4,m) for m in [1]+p))//2 for p in patterns]
assert genera==[6,0,2,3,4]
assert sum(br['degree'] for br,p in zip(branches,patterns) if 2 in p or 4 in p)==12
print('PASS: exact root patterns, auxiliary genera, excluded-factor count')

for nu,expected in [(2,(s.Rational(2,13),s.Rational(6,13),s.Rational(8,13))),
                    (3,(s.Rational(1,4),s.Rational(3,4),s.Integer(1))),
                    (4,(s.Rational(8,27),s.Rational(8,9),s.Rational(32,27)))]:
    j=s.Rational(3*nu-4,7*nu-1)
    assert (j,3*j,4*j)==expected
print('PASS: integer terminal-endpoint arithmetic')

q=3*A**4+60*A**3+394*A**2+620*A+475
r=(3*A**3+135*A**2-851*A+905)/6160
ss=-A-3*r
sigma=-(9*A**3+195*A**2+1507*A+3905)/280
assert s.rem(s.together(sigma.subs(A,sigma)-A),q,A)==0
assert s.rem(s.together(q.subs(A,sigma)),q,A)==0
assert s.gcd(s.together(sigma-A),q)==1
assert s.rem(s.together(sigma*r+3+ss),q,A)==0
print('PASS: other triple-root marking is a fixed-point-free involution')

yp=1/(z**4-1)
wp=z*(1+b-b*z**4)/(z**4-1)**2
assert s.factor(wp**4-yp**3*(yp+1)*(yp-b)**4)==0
print('PASS: genus-zero control parametrization (branch excluded geometrically)')

# Independent inverse calculation. Arrays hold series through degree six.
aa=s.symbols('a2:7'); ll=s.symbols('l2:7')
def mul(U,V):
    out=[s.S(0)]*7
    for i in range(7):
        for j in range(7-i): out[i+j]+=U[i]*V[j]
    return [s.expand(e) for e in out]
def power(U,n):
    out=[s.S(1)]+[s.S(0)]*6
    for _ in range(n): out=mul(out,U)
    return out
U=[s.S(1),s.S(0)]+list(ll)
eq=power(U,12)
for j,aj in zip(range(2,7),aa):
    v=power(U,12-j)
    for k in range(j,7): eq[k]+=aj*v[k-j]
sol={}
for k in range(2,7): sol[ll[k-2]]=s.solve(s.expand(eq[k].subs(sol)),ll[k-2])[0]
cub=power(U,3); a2,a3,a4,a5,a6=aa
expected=[-a2/4,-a3/4,(11*a2**2-24*a4)/96,
          (5*a2*a3-6*a5)/24,(-7*a2**3+24*a2*a4+12*a3**2-32*a6)/128]
for k,e in zip(range(2,7),expected): assert s.expand(cub[k].subs(sol)-e)==0
print('PASS: inverse expansion through drop six, including invisible constant term')
print('SCOPE: exact algebra only; geometric proof in JC2_RETHINK_AND_COUNTEREXAMPLE_PLAN.md')
