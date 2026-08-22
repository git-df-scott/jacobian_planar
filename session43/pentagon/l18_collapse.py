#!/usr/bin/env python3
"""The level-18 obstruction, in its real variables.

Level 19's kernel is 10-dimensional, and it is exactly h_7 (9 coefficients) plus
one constant lambda:  W_19 = 8 c0 g_11 - 12 c1 sigma^4 h_7 = lambda sigma^11,
i.e.  g_11 = (3 c1 / 2 c0) sigma^4 h_7 + (lambda / 8 c0) sigma^11 ,  sigma = s - tau.

Then, by hand,
    11 h_7' g_11 - 7 h_7 g_11'
      = E * sigma^3 * [ (6 c1/c0) h_7 + (11 lambda / 8 c0) sigma^7 ] ,
        E := sigma h_7' - 7 h_7 = sum_m (m-7) a_m sigma^m   (note: no sigma^7 term)

and the level-18 requirement is that this be divisible by sigma^7, i.e.

    **sigma^4 | E * [ (6c1/c0) h_7 + (11 lambda/8 c0) sigma^7 ]**

With nu := ord_sigma(h_7), both factors have order nu, so the product has order
2*nu and the condition is  **nu >= 2, i.e. sigma^2 | h_7**.
Everything below is checked, not asserted.
"""
import sympy as sp
sg, tau, c0, c1, lam = sp.symbols('sigma tau c0 c1 lambda')
a = sp.symbols('a0:9')
h7 = sum(a[m]*sg**m for m in range(9))
g11 = sp.Rational(3,2)*c1/c0*sg**4*h7 + lam/(8*c0)*sg**11
lhs = sp.expand(11*sp.diff(h7,sg)*g11 - 7*h7*sp.diff(g11,sg))
E = sp.expand(sg*sp.diff(h7,sg) - 7*h7)
pred = sp.expand(E*sg**3*(6*c1/c0*h7 + sp.Rational(11,8)*lam/c0*sg**7))
print("CONTROL: hand factorisation of 11 h_7' g_11 - 7 h_7 g_11':",
      "PASS" if sp.simplify(lhs - pred) == 0 else "FAIL")
print("E has no sigma^7 term:", sp.Poly(E, sg).coeff_monomial(sg**7) == 0)

def order(e):
    e = sp.expand(e)
    if e == 0: return None
    P = sp.Poly(e, sg)
    return min(m[0] for m in P.monoms())

print("\ndivisibility test: is sigma^7 | (11 h_7' g_11 - 7 h_7 g_11') * sigma^0 ?")
print("  (the level-18 requirement, after the sigma^3 already present)")
for nu in range(0, 5):
    sub = {a[m]: 0 for m in range(nu)}
    val = sp.expand(lhs.subs(sub))
    o = order(val)
    print(f"  ord_sigma(h_7) = {nu}: ord of the product = {o}  -> "
          f"divisible by sigma^7: {'YES' if o is not None and o >= 7 else 'NO'}")

print("\nNow the decisive check: do the SEVEN level-18 conditions vanish")
print("identically once sigma^2 | h_7 is imposed?")
import io, contextlib
src = open('session43/pentagon/sdescend.py').read()
