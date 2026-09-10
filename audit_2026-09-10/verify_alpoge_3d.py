import sympy as sp
x,y,z,u,v,lam = sp.symbols('x y z u v lam')
# Alpoge's degree-7 map C^3 -> C^3 as transcribed in docs/sessions/active/session-39.md
f1 = (1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y)
f2 = y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z
F = sp.Matrix([f1,f2,f3])
J = F.jacobian([x,y,z])
det = sp.expand(J.det())
print("det JF =", det)
pts = [(0,0,sp.Rational(-1,4)), (1,sp.Rational(-3,2),sp.Rational(13,2)), (-1,sp.Rational(3,2),sp.Rational(13,2))]
for p in pts:
    print("F",p,"=", tuple(F.subs({x:p[0],y:p[1],z:p[2]})))
print("max total degree:", max(sp.Poly(f,x,y,z).total_degree() for f in (f1,f2,f3)))
# planar descent from session 39: u=xy, v=x^2 z ; G1=f1*f3^2, G2=f2*f3
G1 = sp.cancel(sp.expand(f1*f3**2).subs({y:u/x, z:v/x**2}))
G2 = sp.cancel(sp.expand(f2*f3).subs({y:u/x, z:v/x**2}))
print("G1 x-free:", not G1.has(x), " G2 x-free:", not G2.has(x))
G1 = sp.expand(G1); G2 = sp.expand(G2)
dG = sp.factor(sp.Matrix([G1,G2]).jacobian([u,v]).det())
print("det JG =", dG)
print("deg G1, G2 =", sp.Poly(G1,u,v).total_degree(), sp.Poly(G2,u,v).total_degree())
print("G(0,0) =", (G1.subs({u:0,v:0}), G2.subs({u:0,v:0})), " G(-3/2,13/2) =", (G1.subs({u:sp.Rational(-3,2),v:sp.Rational(13,2)}), G2.subs({u:sp.Rational(-3,2),v:sp.Rational(13,2)})))
