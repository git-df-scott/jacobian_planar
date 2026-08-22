"""Exact gauge group of {P,Q}=x^2 preserving the pentagon, acting on (alpha,beta,r).
x->lam*x, y->mu*y : {P,Q} -> lam^3*mu*x^2  => mu = lam^-3.
P->c*P, Q->d*Q    : {P,Q} -> c*d*x^2       => d = 1/c.
Group is 2-dimensional: (lam, c)."""
import sympy as sp
lam, c, al, be, r = sp.symbols('lam c alpha beta r', nonzero=True)
mu = lam**-3
# a_8 = al*y^14*(y-r)^2  ->  lam^8 * a_8(mu*y), then P -> c*P
al_n = sp.simplify(lam**8 * al * mu**16) * c
r_n  = sp.simplify(r/mu)
be_n = sp.simplify(lam**12 * be * mu**24)/c
print("r     ->", sp.simplify(r_n))
print("alpha ->", sp.simplify(al_n))
print("beta  ->", sp.simplify(be_n))
print("alpha*beta ->", sp.simplify(al_n*be_n))
lv = sp.solve(sp.Eq(r_n, 1), lam)
print("\nlam values fixing r=1:", lv)
a2 = sp.simplify(al_n.subs(lam, lv[0]))
b2 = sp.simplify(be_n.subs(lam, lv[0]))
cv = sp.solve(sp.Eq(a2, 1), c)
print("c fixing alpha=1:", cv)
print("resulting beta =", sp.simplify(b2.subs(c, cv[0])))
print("\n=> 3 params - 2 group dims = 1 modulus; r=1, alpha=1 is a legitimate gauge.")
