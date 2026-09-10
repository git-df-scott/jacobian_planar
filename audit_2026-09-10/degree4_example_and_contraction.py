import sympy as sp
x,y,z,u,v = sp.symbols('x y z u v')
R = sp.Rational
# arXiv:2608.00222 degree-4 three-dimensional example (transcribed from the paper's Section 3.5)
g1 = -x**3*z - 4*x**2*y + 2*x
g2 = (x**6*y**3*z**2 + 8*x**5*y**4*z + 3*x**5*y**2*z**2 + 16*x**4*y**5 + 20*x**4*y**3*z + 3*x**4*y*z**2
      + 32*x**3*y**4 + 18*x**3*y**2*z + x**3*z**2 + 28*x**2*y**3 + 8*x**2*y*z + 16*x*y**2 + 2*x*z + 2*y)
g3 = (R(3,8)*x**6*y**4*z**2 + 3*x**5*y**5*z + R(3,2)*x**5*y**3*z**2 + 6*x**4*y**6 + R(21,2)*x**4*y**4*z
      + R(9,4)*x**4*y**2*z**2 + 18*x**3*y**5 + 14*x**3*y**3*z + R(3,2)*x**3*y*z**2 + R(43,2)*x**2*y**4
      + 9*x**2*y**2*z + R(3,8)*x**2*z**2 + 14*x*y**3 + 3*x*y*z + R(9,2)*y**2 + R(1,2)*z)
G = [g1,g2,g3]
det = sp.expand(sp.Matrix([[sp.diff(g,t) for t in (x,y,z)] for g in G]).det())
print("degree-4 map: det J =", det, "; max total degree =", max(sp.Poly(g,x,y,z).total_degree() for g in G))
lam = sp.symbols('lam')
def weight_of(f):
    e = sp.expand(f.subs({x:lam*x, y:y/lam, z:z/lam**2}))
    # find k with e == lam^k f
    for k in range(-6,7):
        if sp.expand(e - lam**k*f)==0: return k
    return None
print("C* weights (1,-1,-2) on source -> component weights:", [weight_of(g) for g in G])
# descent: source invariants u=xy, v=x^2 z; target invariants for weights (1,-1,-2): g1*g2, g1^2*g3
D1 = sp.expand(sp.cancel(sp.expand(g1*g2).subs({y:u/x, z:v/x**2})))
D2 = sp.expand(sp.cancel(sp.expand(g1**2*g3).subs({y:u/x, z:v/x**2})))
assert not D1.has(x) and not D2.has(x)
dD = sp.factor(sp.Matrix([D1,D2]).jacobian([u,v]).det())
print("descent Jacobian =", dD, "   (theorem predicts 2*(g1/x)^2 = 2*(2-4u-v)^2)")
gam = sp.expand(g1/x).subs({y:u/x, z:v/x**2}); gam = sp.expand(gam)
print("gamma = g1/x =", gam)
# contraction: the descent sends the whole line gamma=0 to a single point
sol = sp.solve(gam, v)[0]
print("descent restricted to the line gamma=0:", (sp.simplify(D1.subs(v,sol)), sp.simplify(D2.subs(v,sol))))
# same for Alpoge's descent
G1 = (u+1)*(3*u+v-2)**2*(3*u**3 + u**2*v + 4*u**2 + 2*u*v + v)
G2 = -(3*u+v-2)*(9*u**3 + 3*u**2*v + 12*u**2 + 6*u*v + u + 3*v)
print("Alpoge descent on the line 3u+v-2=0:", (sp.simplify(G1.subs(v,2-3*u)), sp.simplify(G2.subs(v,2-3*u))))
# shadow structure: G = (gamma^2 * a, gamma * b) with a,b polynomial?
# with target weights (1,-1,-2): D1 = g1*g2 = gamma*b, D2 = g1^2*g3 = gamma^2*a, a,b polynomial in (u,v)
b = sp.cancel(D1/gam); a = sp.cancel(D2/gam**2)
print("degree-4 descent = (gamma*b, gamma^2*a) with polynomial a,b:", sp.fraction(a)[1]==1 and sp.fraction(b)[1]==1)
