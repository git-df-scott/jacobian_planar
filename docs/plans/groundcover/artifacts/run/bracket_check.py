import sympy as sp
x,y,z,lam = sp.symbols('x y z lambda_', positive=True)  # z = x^(1/2)
# GGV 1401.1784 p.? Prop 3.10 / def of bracket in L^(l): identify L^(l) with K[z,z^-1,y], z=x^(1/l),
#   [A,B] = (A_z B_y - A_y B_z) * 1/(l z^(l-1)).
l = 2
def brk_l(A,B,var=z,l=2):
    return sp.simplify((sp.diff(A,var)*sp.diff(B,y) - sp.diff(A,y)*sp.diff(B,var))/(l*var**(l-1)))
def brk_xy(A,B):
    return sp.simplify(sp.diff(A,x)*sp.diff(B,y) - sp.diff(A,y)*sp.diff(B,x))

# --- generic P,Q with [P,Q]=x : use symbolic unspecified functions is awkward;
# instead use a CONCRETE exact pair with [P,Q]=x to make the chain rule verifiable numerically,
# plus the abstract chain-rule computation (Prop 3.10) which is what the proof actually uses.
P = sp.Function('P'); Q = sp.Function('Q')
Pf = P(x,y); Qf = Q(x,y)
J = sp.diff(Pf,x)*sp.diff(Qf,y)-sp.diff(Pf,y)*sp.diff(Qf,x)

# 1) FIRST APPLICATION: psi(P)=P(z,y), psi(Q)=Q(z,y), with [P,Q]=x  (so J(z,y)=z^2? no: J(x,y)=x -> J(z,y)=z^2)
A1 = P(z,y); B1 = Q(z,y)
b1 = (sp.diff(A1,z)*sp.diff(B1,y)-sp.diff(A1,y)*sp.diff(B1,z))/(l*z**(l-1))
# substitute the jacobian identity: (P_x Q_y - P_y Q_x)(z,y) = z^2   [since [P,Q]=x]
Jzy = sp.Derivative(P(z,y),z)*sp.Derivative(Q(z,y),y)-sp.Derivative(P(z,y),y)*sp.Derivative(Q(z,y),z)
b1s = sp.simplify(b1.subs(Jzy, z**2))
print("[psi P, psi Q]  raw =", sp.simplify(b1))
print("[psi P, psi Q]  with J(z,y)=z^2 :", sp.simplify(z**2/(2*z)), "=", sp.nsimplify(sp.Rational(1,2)))

# 2) SECOND APPLICATION: psi(phi(P)) = P(z+lam, y)
#    J evaluated at (z+lam,y) = (z+lam) since [P,Q]=x
b2 = sp.simplify((z+lam)/(2*z))
print("[psi phi P, psi phi Q] =", sp.expand(b2), " = ", sp.simplify(sp.Rational(1,2) + lam/(2*z)))
print("  in terms of x:", sp.simplify(sp.Rational(1,2) + lam/2 * x**sp.Rational(-1,2)))

# 3) CONCRETE SANITY CHECK with an explicit pair having [P,Q]=x  (P=x^2/2, Q=y  -> [P,Q]=x)
Pc = x**2/2; Qc = y
print("\nconcrete pair P=x^2/2,Q=y : [P,Q]_xy =", brk_xy(Pc,Qc))
psiP = (z**2/2); psiQ = y
print("  [psi P, psi Q]_{L(2)} =", brk_l(psiP,psiQ))
phiP = ((x+lam)**2/2); phiQ = y
print("  [phi P, phi Q]_xy =", brk_xy(phiP,phiQ), " (= x + lambda)")
psiphiP = ((z+lam)**2/2); psiphiQ = y
r = brk_l(psiphiP,psiphiQ)
print("  [psi phi P, psi phi Q]_{L(2)} =", sp.expand(r), " -> in x:", sp.expand(r).subs(z, sp.sqrt(x)))
print("  is it in K^x (constant in z)? ", sp.simplify(sp.diff(sp.expand(r),z))==0, " ; equals 1/2 + (lam/2) z^-1 :",
      sp.simplify(sp.expand(r) - (sp.Rational(1,2)+lam/(2*z)))==0)

# 4) another concrete pair, non-trivial in both variables: P = x*? ; use P=x^2/2 + f(y)? keep [P,Q]=x
Pc2 = x**2/2 + y**3; Qc2 = y
print("\nsecond concrete pair P=x^2/2+y^3, Q=y: [P,Q]=", brk_xy(Pc2,Qc2))
r2 = brk_l((z+lam)**2/2 + y**3, y)
print("  [psi phi P, psi phi Q] =", sp.expand(r2))

# 5) Theorem 5.1 hypothesis (2) check on the UNTRANSLATED polygons
NP = [(0,0),(1,1),(6,16),(6,18),(0,18)]
NQ = [(0,0),(1,0),(9,24),(9,27),(0,27)]
for name,N in (("P",NP),("Q",NQ)):
    vals = {p: -p[0]+p[1] for p in N}
    mx = max(vals.values()); arg=[p for p in N if vals[p]==mx]
    print(f"v_(-1,1) on N({name}):", vals, "max", mx, "attained at", arg)

# 6) count of conditions imposed by (5.12)
def count(amax,bmax,thr):
    return sum(1 for a in range(amax+1) for b in range(bmax+1) if b-a>thr)
cP=count(6,18,12); cQ=count(9,27,18)
print("\n(5.12) conditions: P:",cP," Q:",cQ," total:",cP+cQ)
print("delivered by the claim (top rows b=18 a=0..5 ; b=27 a=0..8):", 6+9, " unsupported:", cP+cQ-15)

# 7) Is there ANY xi(x)=h(x), xi(y)=y making [xi(phiP),xi(phiQ)] constant?
h = sp.Function('h')
c = sp.symbols('c')
sol = sp.dsolve(sp.Eq((h(x)+lam)*sp.diff(h(x),x), c), h(x))
print("\n(h+lambda) h' = c  =>", sol)
