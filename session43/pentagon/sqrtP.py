#!/usr/bin/env python3
"""HYPOTHESIS: the edge ladder == 'the edge polynomial of P has a square root
regular at y = r'.

The top rung gave B_12^2 = zeta A_8^3, i.e. Q ~ P^{3/2} on the edge.  Write the
reversed edge polynomial Psi(z) = sum_i A_{8-i} z^i and expand
sqrt(Psi) = s (y-r) * sqrt(1 + u),  u = (Psi - A_8)/A_8,  with alpha = s^2.
Each coefficient c_i(y) may have a pole at y = r; requiring none should
reproduce the descent's conditions one for one.
"""
import sympy as sp
y, z, s = sp.symbols('y z s')
r = sp.Integer(1)
al = s**2
def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    return sum(c[i]*y**i for i in range(deg+1)), c

A = {8: al*(y-r)**2}
C7, cC7 = gen('c7_', 2); A[7] = sp.expand((y-r)*C7)     # rung 17 imposed
A[6], cA6 = gen('a6_', 4)
A[5], cA5 = gen('a5_', 5)

u = sp.cancel(sum(A[8-i]*z**i for i in range(1, 4))/A[8])
root = sp.series(sp.sqrt(1+sp.Symbol('U')), sp.Symbol('U'), 0, 4).removeO()
S = sp.expand(s*(y-r)*root.subs(sp.Symbol('U'), u))
S = sp.Poly(sp.expand(S), z)

print("pole orders at y = r, and the condition that kills each pole:")
for i in range(0, 4):
    ci = sp.cancel(sp.together(S.coeff_monomial(z**i)))
    num, den = sp.fraction(ci)
    k = 0
    while sp.rem(sp.Poly(den, y), sp.Poly(y-r, y)).is_zero:
        den = sp.quo(sp.Poly(den, y), sp.Poly(y-r, y)).as_expr(); k += 1
    # cancel any (y-r) in the numerator against it
    j = 0
    nn = sp.Poly(num, y)
    while k - j > 0 and sp.rem(nn, sp.Poly(y-r, y)).is_zero:
        nn = sp.quo(nn, sp.Poly(y-r, y)); j += 1
    pole = k - j
    print(f"\nc_{i}: pole order {pole}")
    if pole > 0:
        cond = sp.expand(nn.as_expr().subs(y, r))
        fl = [f for f, m in sp.factor_list(cond)[1] if not f.is_number and f != s]
        for f in fl:
            print("    COND:", sp.expand(f))
        if not fl:
            print("    (condition is a nonzero constant -- unsatisfiable)" if cond != 0
                  else "    (identically zero)")
