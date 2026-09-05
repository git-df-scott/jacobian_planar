import sympy as s
u,y,L=s.symbols('u y L')
D=1+u**5
# First correction: genus two curve z^2=y+y^6.
b=s.symbols('b0:4');a=s.symbols('a0:5')
BB=sum(b[i]*y**i for i in range(4)); aa=sum(a[i]*y**i for i in range(5))
E=s.Poly(s.expand(2*(y+y**6)*s.diff(BB,y)-(1+6*y**5)*BB-2*aa),y)
print('first',s.linsolve(E.all_coeffs(),a+b),flush=True)
# Second correction, assuming integral first approximate-root coefficients.
t=s.symbols('t0:6');B=s.symbols('B0:8')
tpoly=sum(t[i]*y**i for i in range(6))
bpoly=L*y**7/3+(1+y**5)*tpoly
N=s.expand(24*u**11*bpoly.subs(y,1/u)-13*L*u**4)
Bp=sum(B[i]*u**i for i in range(8))
E=s.Poly(s.expand(4*D*s.diff(Bp,u)-25*u**4*Bp-4*N),u)
print('second numerator',s.factor(N),flush=True)
print('second',s.linsolve(E.all_coeffs(),t+B),flush=True)
