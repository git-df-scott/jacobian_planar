#!/usr/bin/env python3
"""R := Q^2 - c P^3 and its top rung.

The edge theorems make the leading forms of Q^2 and cP^3 cancel:
upper edge Qh^2 = c A^3, and the top rung of the x-ladder gives q_12^2 = zeta a_8^3.
So R is genuinely smaller.  Two exact identities follow from {P,Q} = x^2:

    {P,R} = {P,Q^2} - c{P,P^3} = 2Q{P,Q} = 2 x^2 Q
    {Q,R} = -3c P^2 {Q,P}      = 3c x^2 P^2

R != 0, since R = 0 forces {P,Q} = 0.  Matching x-degrees in the first identity,
7 + deg_x R = 14, so deg_x R = 7, and its top rung (i,k) = (8,7) reads

    8 a_8 r_7' - 7 a_8' r_7 = 2 q_12 .

With the edge results a_8 = alpha y^14 (y-rho)^2 and q_12 = beta y^21 (y-rho)^3
this is one explicit first-order linear ODE, and POLYNOMIALITY of r_7 is the
obstruction.
"""
import sympy as sp
y, rho, al, be = sp.symbols('y rho alpha beta', nonzero=True)

a8  = al*y**14*(y-rho)**2
q12 = be*y**21*(y-rho)**3

# CONTROL: the two bracket identities, symbolically, on free P,Q with {P,Q}=x^2
x = sp.symbols('x')
Pf, Qf, cc = sp.Function('P')(x, y), sp.Function('Q')(x, y), sp.Symbol('c')
def br(F, G): return sp.diff(F, x)*sp.diff(G, y) - sp.diff(F, y)*sp.diff(G, x)
Rf = Qf**2 - cc*Pf**3
i1 = sp.simplify(br(Pf, Rf) - 2*Qf*br(Pf, Qf))
i2 = sp.simplify(br(Qf, Rf) + 3*cc*Pf**2*br(Pf, Qf))
print("CONTROL {P,R} = 2Q{P,Q}:", "PASS" if i1 == 0 else f"FAIL {i1}")
print("CONTROL {Q,R} = -3cP^2{P,Q}:", "PASS" if i2 == 0 else f"FAIL {i2}")

# the top-rung ODE, reduced
r7 = sp.Function('r')(y)
ode = sp.expand(8*a8*sp.diff(r7, y) - 7*sp.diff(a8, y)*r7 - 2*q12)
red = sp.simplify(sp.cancel(ode/(al*y**13*(y-rho))))
print("\ntop-rung ODE divided by alpha*y^13*(y-rho):")
print("   ", sp.collect(sp.expand(red), r7))

# solve for a polynomial r_7 of each plausible degree
print("\npolynomial solutions r_7 of degree D:")
for D in range(6, 20):
    cs = [sp.Symbol(f'r{i}') for i in range(D+1)]
    R7 = sum(cs[i]*y**i for i in range(D+1))
    E = sp.expand(8*y*(y-rho)*sp.diff(R7, y) - (112*y - 98*rho)*R7
                  - (2*be/al)*y**8*(y-rho)**2)
    eqs = sp.Poly(sp.together(E)*al, y).all_coeffs()
    sol = sp.solve(eqs, cs, dict=True)
    if sol and any(sp.simplify(R7.subs(s)) != 0 for s in sol):
        s = sol[0]
        got = sp.factor(sp.simplify(R7.subs(s)))
        print(f"  D={D:2d}: SOLUTION  r_7 = {got}")
    else:
        print(f"  D={D:2d}: none")
