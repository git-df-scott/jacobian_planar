"""Exact global first/second forcing with the possible extra type-III shift."""
import sympy as s
y,u,M=s.symbols('y u M')
h=1+y**5;D=1+u**5;E=3+5*y**4+8*y**5
a=s.symbols('a0:17');b=s.symbols('b0:14')
p10=y**7*sum(a[i]*y**i for i in range(17))
B=sum(b[i]*u**i for i in range(14))
N=s.expand(24*u**24*p10.subs(y,1/u)-13*M*u**12*D*E.subs(y,1/u)**2)
eq=s.Poly(s.expand(4*D*s.diff(B,u)-45*u**4*B-4*N),u).all_coeffs()
eq += [s.diff(p10,y,k).subs(y,-1) for k in range(3)]
eq += [a[0]-4*M]
sol=list(s.linsolve(eq,a+b))
print('solution empty',not sol,flush=True)
if sol:
    vv=sol[0];free=set().union(*(v.free_symbols for v in vv))-{M}
    print('free count',len(free),sorted(map(str,free)),flush=True)
    sub=dict(zip(a+b,vv));PP=s.factor(p10.subs(sub,simultaneous=True))
    print('p10=',PP,flush=True)
    print('particular=',s.factor(PP.subs({f:0 for f in free})),flush=True)
    base=M*y**7*h*E**2/3
    loc=s.Poly(s.rem(s.expand(PP-base),h*h,y),y).all_coeffs()
    fs=sorted(free,key=str)
    locsol=list(s.linsolve(loc,fs))
    print('after local cube condition empty',not locsol,flush=True)
    if locsol:
        final=s.factor(PP.subs(dict(zip(fs,locsol[0])),simultaneous=True))
        print('after local cube p10=',final,flush=True)
        print('remaining free',sorted(map(str,final.free_symbols-{M,y})),flush=True)
