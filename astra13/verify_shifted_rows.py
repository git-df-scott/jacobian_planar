#!/usr/bin/env python3
"""Exact checks of the restored shifted rational rows and chart identity."""
import sympy as s
y,u,t,Z,eta,mu,tau,X,Y=s.symbols('y u t Z eta mu tau X Y')
h=1+y**5;c=y**3*h
E1=3+5*y**4+8*y**5;E2=3+5*y**2+8*y**5
R=12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
p11=mu*y**8*h*h*E1
p10=mu*mu*y**7*h*R/3+tau*y**8*h*h*E2
XX=t**4;YY=t**(-1)+eta*t**(-2)+Z
br=lambda f,g:s.diff(f,t)*s.diff(g,Z)-s.diff(f,Z)*s.diff(g,t)
assert s.expand(br(XX,YY)-4*t**3)==0
assert s.expand(br(XX+YY**2,YY)-4*t**3)==0
# There is only one eligible intermediate type-III direction.
directions=[]
for rho in [1,2,4]:
    for sigma in range(-rho,1):
        if s.gcd(rho,sigma)==1 and -s.Rational(7,12)<s.Rational(sigma,rho)<-s.Rational(1,4):
            directions.append((rho,sigma))
assert directions==[(2,-1)]
print('PASS: shifted chart, ordinary Keller control, intermediate-direction census')

aa=s.symbols('a0:6');bb=s.symbols('b0:5')
a=sum(aa[i]*y**i for i in range(6));B=sum(bb[i]*y**(i-1) for i in range(5))
D=y+y**6
eq=s.Poly(s.expand(y*(2*D*s.diff(B,y)-s.diff(D,y)*B)-2*a),y).all_coeffs()
sol=list(s.linsolve(eq,aa+bb))
assert sol==[(-3*bb[0]/2,0,0,0,5*bb[4]/2,-4*bb[0],bb[0],0,0,0,bb[4])]
Bg=2*mu*(y**3-1/y)
assert s.expand(y*(2*D*s.diff(Bg,y)-s.diff(D,y)*Bg)-2*mu*E1)==0
for k in range(3):assert s.diff(p11,y,k).subs(y,-1)==0
assert s.expand(p11).coeff(y,8)==3*mu
print('PASS: complete widened first-row primitive and original descent')

# Original polynomiality of both complete rows, including the nonzero shift.
for row,k in [(p11,11),(p10,10)]:
    lifted=s.cancel(Y**(-k)*row.subs(y,X*Y**4-1))
    assert s.denom(lifted)==1
    poly=s.Poly(lifted,X,Y)
    assert poly.degree(X)<=24 and poly.degree(Y)<=84
assert s.rem(s.expand(p10-p11**2/(3*c**3)),h*h,y)==0
assert s.expand(p10).coeff(y,7)==4*mu*mu
print('PASS: p10 local cube congruence, shift coefficient and exact plane lifts')

# Verify rational primitive existence without relying on the exploratory output.
D=1+u**5;bb=s.symbols('v0:14');B=sum(bb[i]*u**i for i in range(14))
N=s.expand(24*u**24*p10.subs(y,1/u)-13*mu*mu*u**12*D*E1.subs(y,1/u)**2)
eq=s.Poly(s.expand(4*D*s.diff(B,u)-45*u**4*B-4*N),u).all_coeffs()
sol=list(s.linsolve(eq,bb));assert len(sol)==1
pr=s.expand(B.subs(dict(zip(bb,sol[0])),simultaneous=True))
assert s.expand(4*D*s.diff(pr,u)-45*u**4*pr-4*N)==0
print('PASS: exact next global primitive for all mu and tau')

# Leading cancellation in the additional shifted chart.
shift=-mu/12
assert s.expand(4**8*3*mu+9*shift*4**9)==0
assert s.expand(4**7*4*mu**2+8*shift*4**8*3*mu+36*shift**2*4**9)==0
print('PASS: first two shifted terminal-row cancellations')
print('SCOPE: complete first-two-row necessary classification, not a finite Keller pair')
