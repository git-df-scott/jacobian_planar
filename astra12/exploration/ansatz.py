import sympy as s
x,y,u,v=s.symbols('x y u v')
R=s.Function('R')(x,y)
A=s.Function('A')(x,y)
B=s.Function('B')(x,y)
def bracket(f,g):
    return s.diff(f,x)*s.diff(g,y)-s.diff(f,y)*s.diff(g,x)
P=R**3+A*R+B
Q=R**4+s.Rational(4,3)*A*R**2+s.Rational(4,3)*B*R+s.Rational(2,9)*A**2
identity=s.Rational(4,9)*(A**2-3*B*R)*bracket(R,A)-s.Rational(4,3)*(A*R+B)*bracket(R,B)-s.Rational(4,9)*A*bracket(A,B)
assert s.expand(bracket(P,Q)-identity)==0
special=s.expand(identity.subs({A:u*x**3*y**2,B:v*x**2*y}).doit())
r,rx,ry=s.symbols('r rx ry')
quotient=s.cancel(special.subs({s.diff(R,x):rx,s.diff(R,y):ry,R:r})/(x**3*y))
s.Poly(quotient,x,y,r,rx,ry,u,v)
print('PASS universal polynomial-part bracket identity')
print('PASS specialized bracket divisible by x^3*y for every polynomial R')
print('quotient =',s.factor(quotient))
