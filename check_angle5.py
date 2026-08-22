# Angle 5 control: top x-column (x^19) of {P,Q} = x^2.
# Only (i,k)=(8,12) contributes: 8 a8 b12' - 12 a8' b12 = 0  =>  b12^2 = c a8^3.
# With a8 = p168 y^14 (y-r0)^2 (rung-19 disc), polynomial b12 with support y^21..y^24
# must be b12 = c' y^21 (y-r0)^3, so q_21_12 = -c' r0^3 and p_14_8 = p168 r0^2.
# CLAIM: q_21_12 != 0  <=>  r0 != 0  <=>  p_14_8 != 0.
import sympy as sp
y, p168, r0, cp = sp.symbols('y p168 r0 cprime')
a8 = p168*y**14*(y-r0)**2
b12 = cp*y**21*(y-r0)**3
wron = sp.expand(8*a8*sp.diff(b12,y) - 12*sp.diff(a8,y)*b12)
print("Wronskian identically zero:", wron == 0)
poly = sp.Poly(sp.expand(b12), y)
print("y-support of b12:", sorted(m[0] for m in poly.monoms()), "(needs subset of 21..24)")
print("q_21_12 =", sp.factor(poly.coeff_monomial(y**21)), " -> zero iff r0=0")
print("q_24_12 =", poly.coeff_monomial(y**24), " (vertex, nonzero <=> c' != 0)")
print("p_14_8  =", sp.expand(a8).coeff(y,14), " -> zero iff r0=0 (given p168!=0)")
# converse control: generic b12 with support 21..24 solving the Wronskian ODE
# 2 b' a = 3 a' b on a=y^14*quad forces quad to be a square (disc=0 re-derived):
q0,q1,q2 = sp.symbols('q0 q1 q2')
aa = y**14*(q0+q1*y+q2*y**2)
bb = sum(sp.Symbol(f'b{j}')*y**j for j in range(21,25))
eqs = sp.Poly(sp.expand(8*aa*sp.diff(bb,y)-12*sp.diff(aa,y)*bb), y).all_coeffs()
sol = sp.solve(eqs, [sp.Symbol(f'b{j}') for j in range(21,25)], dict=True)
# nontrivial solution requires resultant condition; check disc factor appears
import itertools
gb = sp.groebner(eqs + [sp.Symbol('b24')*sp.Symbol('t')-1], *[sp.Symbol(f'b{j}') for j in range(21,25)], sp.Symbol('t'), q0,q1,q2, order='lex')
disc_in = any(sp.simplify(sp.factor(g) / (q1**2-4*q0*q2)).is_polynomial(q0,q1,q2) if (q1**2-4*q0*q2).free_symbols <= sp.factor(g).free_symbols else False for g in gb.exprs)
print("disc(q) = q1^2-4q0q2 forced when b24!=0:", disc_in or [sp.factor(g) for g in gb.exprs if g.free_symbols <= {q0,q1,q2}])
