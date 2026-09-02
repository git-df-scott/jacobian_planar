import sympy as sp
y = sp.symbols('y')
m0,m1,m2,m3 = sp.symbols('mu0 mu1 mu2 mu3')
# GGV2013 sec.3: general solution of eq.1 : q1 = mu3 + y^2 F', p2 = mu3 + yF + (3/2) y^2 F', F in yK[y]
# represent F as a truncated series with F(0)=0
f1,f2,f3,f4,f5 = sp.symbols('f1 f2 f3 f4 f5')
F = f1*y + f2*y**2 + f3*y**3 + f4*y**4 + f5*y**5
Fp = sp.diff(F,y); Fpp = sp.diff(F,y,2)
q1 = m3 + y**2*Fp
p2 = m3 + y*F + sp.Rational(3,2)*y**2*Fp
# p1 generic polynomial
c0,c1,c2,c3,c4 = sp.symbols('c0 c1 c2 c3 c4')
p1 = c0 + c1*y + c2*y**2 + c3*y**3 + c4*y**4
p1p = sp.diff(p1,y)
# (3.2)
num32 = (-2*p1 + 2*m2 + 2*m3*F + 4*y*p1p - 6*y**2*F*Fp - m3*y**2*Fpp
         - 4*y**3*Fp**2 - 4*y**3*F*Fpp - 3*y**4*Fp*Fpp)
q0p = sp.simplify(num32/(6*y))
cond_a = sp.expand(num32.subs(y,0))          # must vanish  -> p1(0)=mu2
print("cond from (3.2) polynomiality [num(0)=0]:", cond_a, "  => c0 =", sp.solve(cond_a,c0))
q0p_poly = sp.simplify(sp.series(num32,y,0,6).removeO()/(6*y)).subs(c0,m2)
q0p0 = sp.limit(sp.simplify(num32.subs(c0,m2)/(6*y)), y, 0)
print("q0'(0) =", sp.simplify(q0p0), "   (expect (c1+mu3*f1)/3 )")
# (3.3)
num33 = (y*p1*(2*Fp + y*Fpp) - m1 - p1p*(m3 + y**2*Fp) + (2*m3 + y*(2*F + 3*y*Fp))*q0p)
cond_b = sp.simplify(sp.limit(num33.subs(c0,m2), y, 0))    # must vanish
print("cond from (3.3) polynomiality [num(0)=0]:", sp.expand(cond_b))
sol_c1 = sp.solve(sp.Eq(cond_b,0), c1); print("  => c1 =", sol_c1)
# A
A = y*p1 - q1*p2 + sp.Rational(3,4)*q1**2
A = A.subs(c0,m2)
print("\nA(0) =", sp.simplify(A.subs(y,0)), " (expect -mu3^2/4)")
print("A'(0) =", sp.simplify(sp.diff(A,y).subs(y,0)), " (expect mu2)")
App0 = sp.simplify(sp.diff(A,y,2).subs(y,0))
q1pp0 = sp.simplify(sp.diff(q1,y,2).subs(y,0))
print("A''(0) =", App0, "   q1''(0) =", q1pp0)
if sol_c1:
    c1v = sol_c1[0]
    lhs = sp.simplify((m3*App0).subs(c1,c1v))
    print("\nWITH the (3.3) condition imposed:")
    print("  mu3*A''(0) =", sp.expand(lhs))
    print("  PRINTED RHS  -6*mu1 - 2*mu3*q1''(0) =", sp.expand(-6*m1-2*m3*q1pp0))
    print("  CAMPAIGN RHS -6*mu1                 =", sp.expand(-6*m1))
    print("  printed identity holds identically? ", sp.simplify(lhs-(-6*m1-2*m3*q1pp0))==0)
    print("  campaign identity holds identically?", sp.simplify(lhs-(-6*m1))==0)
    print("  difference (printed - true) =", sp.simplify((-6*m1-2*m3*q1pp0)-lhs))
