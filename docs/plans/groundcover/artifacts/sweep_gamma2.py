import sympy as sp
g, w = sp.symbols('gamma w')
X1,X2,D1,D2,E1,E2 = [sp.Function(n)(w) for n in ('X1','X2','D1','D2','E1','E2')]
S1 = X1 + g*D1 + g**2*E1
S2 = X2 + g*D2 + g**2*E2
J  = sp.Matrix([[sp.diff(S1,g), sp.diff(S1,w)],[sp.diff(S2,g), sp.diff(S2,w)]])
det = sp.expand(J.det())
P = sp.Poly(det, g)
def dt(A,B): return sp.expand(A[0]*B[1]-A[1]*B[0])
D=(D1,D2); E=(E1,E2); Xp=(sp.diff(X1,w),sp.diff(X2,w))
Dp=(sp.diff(D1,w),sp.diff(D2,w)); Ep=(sp.diff(E1,w),sp.diff(E2,w))
claim = {0: dt(D,Xp),
         1: sp.expand(dt(D,Dp) + 2*dt(E,Xp)),
         2: sp.expand(2*dt(E,Dp) + dt(D,Ep)),
         3: sp.expand(2*dt(E,Ep))}
print("det J(S) as a polynomial in gamma, degree", P.degree())
for k in range(4):
    c = sp.expand(det.coeff(g,k))
    print(f"  [gamma^{k}] {c}")
    print(f"     matches claim: {sp.simplify(c-claim[k])==0}")
print()
# ---- branch (b) generalized: E parallel to constant v=(0,1), i.e. E=(0,k)
c,e,d1 = sp.symbols('c e d1')
k = sp.Function('k')(w)
sub = {E1: sp.Integer(0), E2: k}
co = {n: sp.expand(det.coeff(g,n).subs(sub).doit()) for n in (1,2,3)}
print("with E = (0, k(w))  [forced by gamma^3 coeff = 0]:")
for n in (1,2,3): print(f"  [gamma^{n}] = {co[n]}")
# gamma^2 = 0  <=>  k' D1 - 2 k D1' = 0  <=>  k = c*D1^2
print("  gamma^2 coeff with k = c*D1**2 :",
      sp.simplify(co[2].subs(k, c*D1**2).doit()))
# gamma^1 = 0 with k=c D1^2 :
g1 = sp.simplify(co[1].subs(k, c*D1**2).doit())
print("  gamma^1 coeff with k = c*D1**2 :", sp.factor(g1))
print("      => D1*D2' - D2*D1' = 2c*D1^2*X1'  <=>  (D2/D1)' = 2c*X1'  =>  D2 = D1*(2c*X1+e)")
# substitute D2 = D1*(2c X1 + e) and check gamma^1, gamma^2, gamma^3 all vanish
full = {E1: sp.Integer(0), E2: c*D1**2, D2: D1*(2*c*X1+e)}
for n in (1,2,3):
    print(f"  after D2 = D1*(2c*X1+e):  [gamma^{n}] =",
          sp.simplify(sp.expand(det.coeff(g,n).subs(full).doit())))
c0 = sp.simplify(sp.expand(det.coeff(g,0).subs(full).doit()))
print("  [gamma^0] =", sp.factor(c0), "  ( = kappa, a nonzero constant )")
print("      => D1 = const d1 != 0  (a polynomial factor of a nonzero constant)")
print()
# ---- the elementary target shear that trivialises it
S1c = X1 + g*d1
S2c = X2 + g*d1*(2*c*X1+e) + g**2*c*d1**2
T   = sp.simplify(sp.expand(S2c - c*S1c**2 - e*S1c))
print("T := S2 - c*S1^2 - e*S1 =", sp.simplify(T), "   <- depends on w only, no gamma:",
      sp.diff(sp.simplify(T), g) == 0)
Jc = sp.Matrix([[sp.diff(S1c,g), sp.diff(S1c,w)],[sp.diff(T,g), sp.diff(T,w)]])
print("det J(S1, T) =", sp.simplify(Jc.det()), " => G' const => G linear => (gamma,w) recoverable => INJECTIVE")
