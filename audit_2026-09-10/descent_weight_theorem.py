"""
Descent-exponent identity for C*-equivariant Keller maps C^3 -> C^3.

Setup: C* acts on source with weights w=(w1,w2,w3) (vector field xi = sum w_i x_i d/dx_i)
and on target with weights w'. Suppose invariant rings are polynomial: C[m1,m2], C[M1,M2],
quotient maps pi=(m1,m2), pi'=(M1,M2), and F equivariant, so G o pi = pi' o F for a
polynomial G: C^2 -> C^2.

Claim:  dm1^dm2 = phi * i_xi(vol),  dM1^dM2 = phi' * i_xi'(vol'),  and
        (det dG o pi) * phi = (phi' o F) * det dF.
Hence for a Keller F,  det dG o pi = c * (phi' o F) / phi,  and
weight(phi) = -(w1+w2+w3), weight(phi') = -(w1'+w2'+w3').
So det dG can only be constant if phi' o F = const * phi; with nonzero weight sum this
forces a nonconstant factor.  We verify every piece on Alpoge's map exactly.
"""
import sympy as sp
x,y,z = sp.symbols('x y z'); u,v = sp.symbols('u v')
f1 = (1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y)
f2 = y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z
F = [f1,f2,f3]; X=[x,y,z]
w  = (1,-1,-2)          # source weights
wp = (-2,-1,1)          # target weights
detF = sp.expand(sp.Matrix([[sp.diff(f,t) for t in X] for f in F]).det())
print("det dF =", detF)
# invariants
m1, m2 = x*y, x**2*z                          # source quotient
def minors2(rows):  # 2x2 minors (dy^dz, dz^dx, dx^dy) ordering of a 2x3 jacobian
    J = sp.Matrix(rows)
    return (J[0,1]*J[1,2]-J[0,2]*J[1,1], J[0,2]*J[1,0]-J[0,0]*J[1,2], J[0,0]*J[1,1]-J[0,1]*J[1,0])
def ixi_vol(weights, coords):  # i_xi(dx^dy^dz) components on (dy^dz, dz^dx, dx^dy)
    return (weights[0]*coords[0], weights[1]*coords[1], weights[2]*coords[2])
dm = minors2([[sp.diff(m,t) for t in X] for m in (m1,m2)])
iv = ixi_vol(w, X)
phi = sp.cancel(dm[0]/iv[0]); assert all(sp.expand(dm[i]-phi*iv[i])==0 for i in range(3))
print("phi (source) =", sp.factor(phi))
# target invariants
W1,W2,W3 = sp.symbols('W1 W2 W3'); W=[W1,W2,W3]
M1, M2 = W1*W3**2, W2*W3
dM = minors2([[sp.diff(M,t) for t in W] for M in (M1,M2)])
ivp = ixi_vol(wp, W)
phip = sp.cancel(dM[0]/ivp[0]); assert all(sp.expand(dM[i]-phip*ivp[i])==0 for i in range(3))
print("phi' (target) =", sp.factor(phip))
# descent G
G1 = sp.expand(sp.cancel(sp.expand(f1*f3**2).subs({y:u/x, z:v/x**2})))
G2 = sp.expand(sp.cancel(sp.expand(f2*f3).subs({y:u/x, z:v/x**2})))
detG = sp.factor(sp.Matrix([G1,G2]).jacobian([u,v]).det())
print("det dG =", detG)
lhs = sp.expand(detG.subs({u:m1, v:m2}) * phi)
rhs = sp.expand(phip.subs({W1:f1,W2:f2,W3:f3}) * detF)
print("identity (det dG o pi)*phi == (phi' o F)*det dF :", sp.expand(lhs-rhs)==0)
print("weight(phi) = -(sum w) :", -sum(w), "; phi = x^2 has weight", 2)
print("phi'/W3^2 =", sp.cancel(phip/W3**2), "  => det dG = det dF * (f3/x)^2 * const")
print("check: det dG o pi ==", sp.factor(sp.cancel(detF*phip.subs({W1:f1,W2:f2,W3:f3})/phi)), " vs h=f3/x =", sp.factor(sp.cancel(f3/x)))
