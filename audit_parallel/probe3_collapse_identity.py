import sympy as sp
v,alpha = sp.symbols('v alpha'); e,beta,epsn,a_,b_ = sp.symbols('e beta eps a b')
R = sp.Function('R')(v); U = v+1
# general block with eps symbolic is hard (U**(2*eps)); do it for eps=1..6 with a,b,e,beta free
print("general collapse identity, eps = 1..6, a,b,e,beta symbolic:")
for ev in range(1,7):
    eta = alpha**2*U**(2*ev)*v**a_
    delta = sp.Rational(1,2)*alpha**3*U**(3*ev)*R*v**b_
    blk = e*delta*sp.diff(eta,v) + beta*sp.diff(delta,v)*eta
    # impose collapse: e*a + beta*b = -eps*(2e+3beta)  ->  solve for b
    bsol = sp.solve(sp.Eq(e*a_+beta*b_, -ev*(2*e+3*beta)), b_)[0]
    Dode = 3*ev*(2*e+3*beta)/beta
    tgt = (alpha**5/2)*(beta/3)*U**(5*ev-1)*v**(a_+bsol-1)*(3*v*U*sp.diff(R,v)-Dode*R)
    ok = sp.simplify(sp.expand(sp.powsimp((blk.subs(b_,bsol)-tgt),force=True)))==0
    print("   eps=%d  collapse => block == (a^5/2)(beta/3)U^{5eps-1}v^{a+b-1}[3vUR' - D_ode R] :"%ev, ok)
print()
print("does the identity depend on G (the hand-picked 14)?  G enters only through a,b,")
print("which are free above -> NO.  So the '(1,14,69) built from scratch' check is one")
print("instance of a formula that holds for every (a,b) satisfying collapse.")
print()
# what happens WITHOUT collapse: R-coefficient is v-dependent, not an Euler operator
ev=1
eta = alpha**2*U**(2*ev)*v**a_; delta = sp.Rational(1,2)*alpha**3*U**(3*ev)*R*v**b_
blk = e*delta*sp.diff(eta,v) + beta*sp.diff(delta,v)*eta
gen = sp.simplify(sp.expand(blk/((alpha**5/2)*U**(5*ev-1)*v**(a_+b_-1))))
print("bracket without collapse:", sp.collect(sp.expand(gen),[sp.diff(R,v),R]))
