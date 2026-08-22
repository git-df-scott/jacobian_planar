import sympy as sp

x,y,z,u,v = sp.symbols('x y z u v')

# Alpoge example
f1 = (1+x*y)**3*z + y**2*(1+x*y)*(4+3*x*y)
f2 = y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z
F = sp.Matrix([f1,f2,f3])
JF = F.jacobian([x,y,z])
print("det JF =", sp.factor(JF.det()))

G1 = (u+1)*(3*u+v-2)**2*(3*u**3+u**2*v+4*u**2+2*u*v+v)
G2 = -(3*u+v-2)*(9*u**3+3*u**2*v+12*u**2+6*u*v+u+3*v)
G = sp.Matrix([G1,G2])
JG = G.jacobian([u,v])
print("det JG =", sp.factor(JG.det()))

# source projection: weights (1,-1,-2) -> invariants u=xy, v=x^2 z
pis = sp.Matrix([x*y, x**2*z])
# target weights (-2,-1,1), coords (X1,X2,X3)=(f1,f2,f3): invariants X2*X3, X1*X3^2
pit_of_F = sp.Matrix([f2*f3, f1*f3**2])

# check equivariance descent: G o pi_src == pi_tgt o F ?
lhs = G.subs([(u,x*y),(v,x**2*z)], simultaneous=True)
diff = sp.expand(sp.Matrix(lhs) - pit_of_F)
print("descent identity G(pi(p)) - pi_tgt(F(p)):", diff.T)

# f3 = x * p(u,v)?
p_poly = sp.simplify(f3/x)
print("f3/x =", sp.factor(p_poly))  # should be -(3u+v-2) pulled back

# Cauchy-Binet identity check: det JG(pi(p)) * minor_{yz}(Jpi_src) = sum_K minor_K(Jpi_tgt)(F)*minor_{K,yz}(JF)
Jpis = pis.jacobian([x,y,z])
X1,X2,X3 = sp.symbols('X1 X2 X3')
pit = sp.Matrix([X2*X3, X1*X3**2])
Jpit = pit.jacobian([X1,X2,X3])
detJG_pi = JG.det().subs([(u,x*y),(v,x**2*z)], simultaneous=True)

def minor2(M, cols):
    return M[:, list(cols)].det()

LHS = sp.expand(detJG_pi * minor2(Jpis,(1,2)))
JpitF = Jpit.subs([(X1,f1),(X2,f2),(X3,f3)], simultaneous=True)
RHS = 0
import itertools
for K in itertools.combinations(range(3),2):
    RHS += minor2(JpitF, K) * JF[list(K), [1,2]].det()
print("Cauchy-Binet identity holds:", sp.expand(LHS-RHS)==0)

# also verify det JG o pi == det JF * p^2
print("detJG(pi) - detJF * (f3/x)^2 :", sp.expand(detJG_pi - JF.det()*p_poly**2))

# A2: image of line h=0
h = 3*u+v-2
G_on_h0 = [sp.simplify(g.subs(v, 2-3*u)) for g in (G1,G2)]
print("G on {h=0}:", G_on_h0)
