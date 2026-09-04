#!/usr/bin/env python3
"""Decisive test: with rung 15 imposed, does c_3's residual pole reproduce the
rung-13 condition exactly?"""
import sympy as sp
y, z, s = sp.symbols('y z s')
r = sp.Integer(1); al = s**2
def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    return sum(c[i]*y**i for i in range(deg+1)), c
A = {8: al*(y-r)**2}
C7, cC7 = gen('c7_', 2); A[7] = sp.expand((y-r)*C7)
A[6], cA6 = gen('a6_', 4)
A[5], cA5 = gen('a5_', 5)
# rung 15:  4 alpha A_6(r) = A_7'(r)^2
sub15 = {cA6[0]: sp.expand(sp.diff(A[7], y).subs(y, r)**2/(4*al) - sum(cA6[1:]))}
A6 = sp.expand(A[6].subs(sub15)); A[6] = A6

u = sp.cancel(sum(A[8-i]*z**i for i in range(1, 4))/A[8])
root = sp.series(sp.sqrt(1+sp.Symbol('U')), sp.Symbol('U'), 0, 4).removeO()
S = sp.Poly(sp.expand(s*(y-r)*root.subs(sp.Symbol('U'), u)), z)
c3 = sp.cancel(sp.together(S.coeff_monomial(z**3)))
num, den = sp.fraction(c3)
k = 0
while sp.rem(sp.Poly(den, y), sp.Poly(y-r, y)).is_zero:
    den = sp.quo(sp.Poly(den, y), sp.Poly(y-r, y)).as_expr(); k += 1
nn = sp.Poly(num, y); j = 0
while j < k and sp.rem(nn, sp.Poly(y-r, y)).is_zero:
    nn = sp.quo(nn, sp.Poly(y-r, y)); j += 1
print(f"c_3 with rung 15 imposed: pole order {k-j}")
cond_sqrt = sp.expand(nn.as_expr().subs(y, r))
cond_sqrt = sp.expand(cond_sqrt * sp.denom(sp.together(cond_sqrt)))
print("  sqrt-regularity condition:")
print("   ", sp.factor(cond_sqrt))

# the rung-13 condition, verbatim from rung14.log, with alpha -> s^2
R13 = sp.sympify("4*a5_0*alpha**2 + 4*a5_1*alpha**2 + 4*a5_2*alpha**2 + 4*a5_3*alpha**2 + 4*a5_4*alpha**2 + 4*a5_5*alpha**2 - 2*a6_1*alpha*c7_0 - 2*a6_1*alpha*c7_1 - 2*a6_1*alpha*c7_2 - 4*a6_2*alpha*c7_0 - 4*a6_2*alpha*c7_1 - 4*a6_2*alpha*c7_2 - 6*a6_3*alpha*c7_0 - 6*a6_3*alpha*c7_1 - 6*a6_3*alpha*c7_2 - 8*a6_4*alpha*c7_0 - 8*a6_4*alpha*c7_1 - 8*a6_4*alpha*c7_2 + c7_0**2*c7_1 + 2*c7_0**2*c7_2 + 2*c7_0*c7_1**2 + 6*c7_0*c7_1*c7_2 + 4*c7_0*c7_2**2 + c7_1**3 + 4*c7_1**2*c7_2 + 5*c7_1*c7_2**2 + 2*c7_2**3").subs(sp.Symbol('alpha'), s**2)
print("\n  rung-13 condition (from the descent):")
print("   ", sp.factor(sp.expand(R13)))
# compare up to a nonzero scalar factor in s
q = sp.cancel(sp.expand(cond_sqrt)/sp.expand(R13))
print("\n  ratio (sqrt-condition)/(rung-13 condition) =", sp.simplify(q))
print("  MATCH:", sp.simplify(q).free_symbols <= {s} and sp.simplify(q) != 0)
