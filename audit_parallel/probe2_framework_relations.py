import sympy as sp
beta,sig,eps,p,Dc = sp.symbols('beta sigma eps p D_chain', positive=True)
gam = sp.Rational(3,2)*beta          # cusp (2,3)
e   = gam - sig                      # e = gamma - sigma
Dchain = sp.simplify(2*gam - sig)    # = 3beta - sigma
Dode = sp.simplify(3*eps*(2*e+3*beta)/beta)
print("D_ode  =", Dode)
print("D_chain=", Dchain)
print("D_ode expressed via D_chain:", sp.simplify(Dode - 6*eps*Dchain/beta))   # 0 ?
# chart relation e = beta+1-p  =>  sigma = gamma - beta - 1 + p
sub = {sig: gam - beta - 1 + p}
print("D_chain under e=beta+1-p :", sp.simplify(Dchain.subs(sub)))
print("  at p=3 :", sp.simplify(Dchain.subs(sub).subs(p,3)))
print("  => D_chain = 5beta/2 - 2, so D_chain = 3 (mod 5) for EVERY even beta")
for b in range(2,26,2):
    print("     beta=%2d -> D_chain=%s" % (b, sp.simplify(Dchain.subs(sub).subs({p:3,beta:b}))))
print()
Dode_p = sp.simplify(Dode.subs(sub).subs(p,3))
print("D_ode at p=3 :", Dode_p, " = eps*(15-12/beta):", sp.simplify(Dode_p-eps*(15-12/beta))==0)
print("D_ode/3      :", sp.simplify(Dode_p/3), "  (= 5eps - 4eps/beta)")
print("k = 5eps-1.  Family branch needs D_ode/3 integer AND > k:")
print("   D_ode/3 - k = 1 - 4eps/beta > 0  <=> beta > 4eps;  integrality needs beta | 4eps.")
bad=[]
for ev in range(1,60):
    for b in range(2,400,2):
        val = sp.Rational(5*ev) - sp.Rational(4*ev,b)
        if val.is_integer and val > 5*ev-1: bad.append((ev,b))
print("   exhaustive scan eps<=59, beta<=398 even: family-branch-open cases =", bad)
