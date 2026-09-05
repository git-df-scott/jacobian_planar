import sympy as s
u,y,L=s.symbols('u y L');D=1+u**5;E=3+5*y**2+8*y**5
A=s.symbols('a0:18'); B=s.symbols('b0:13')
p8=y**6*sum(A[i]*y**i for i in range(18))
N=s.expand(-24*u**20*p8.subs(y,1/u)+11*L*u**8*D*E.subs(y,1/u)**2)
H=sum(B[i]*u**(i-2) for i in range(13))
eq=s.Poly(s.expand(u**3*(4*D*s.diff(H,u)-35*u**4*H-4*N)),u).all_coeffs()
eq +=[p8.subs(y,-1),s.diff(p8,y).subs(y,-1)]
sol=list(s.linsolve(eq,A+B))
assert len(sol)==1
sol=sol[0]
free=set().union(*(v.free_symbols for v in sol))-{L}
print('free count',len(free),sorted(map(str,free)),flush=True)
sub={v:s.expand(z.subs({f:0 for f in free})) for v,z in zip(A+B,sol)}
pp=s.factor(p8.subs(sub,simultaneous=True)); HH=s.factor(H.subs(sub,simultaneous=True))
print('particular p8=',pp)
print('primitive numerator=',HH)
print('L forced?',L not in set().union(*(v.free_symbols for v in sol)))
assert s.expand(u**3*(4*D*s.diff(HH,u)-35*u**4*HH-4*(-24*u**20*pp.subs(y,1/u)+11*L*u**8*D*E.subs(y,1/u)**2)))==0
