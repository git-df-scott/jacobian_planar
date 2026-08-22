#!/usr/bin/env python3
"""Rung 13 of the R-ladder:  {P,R} = 2 x^2 Q  with  R = Q^2 - c P^3.

Rung d:  sum_{i+k=d+1} [ i a_i r_k' - k a_i' r_k ]  =  2 q_{d-2}.
d = 14 gave r_7 uniquely.  d = 13 is (7,7) and (8,6):

    7 a_7 r_7' - 7 a_7' r_7 + 8 a_8 r_6' - 6 a_8' r_6 = 2 q_11

Everything except r_6 is known in closed form from the edge results:
    a_8  = alpha y^14 (y-rho)^2
    a_7  = y^12 (y-rho) C_7 ,  deg C_7 = 2
    q_12 = beta y^21 (y-rho)^3
    q_11 = y^19 B_11 = y^19 (3 beta / 2 alpha)(y-rho) (y-rho) C_7
    r_7  = solved at d = 14.
Polynomiality of r_6 is then a condition on C_7.
"""
import sympy as sp
y, rho, al, be = sp.symbols('y rho alpha beta', nonzero=True)
c = [sp.Symbol(f'c7_{i}') for i in range(3)]
C7 = sum(c[i]*y**i for i in range(3))

a8  = al*y**14*(y-rho)**2
a7  = y**12*(y-rho)*C7
q12 = be*y**21*(y-rho)**3
q11 = y**19*sp.Rational(3,2)*be/al*(y-rho)**2*C7
r7  = be*y**8*(y-rho)**2*(195*rho**4 + 240*rho**3*y + 320*rho**2*y**2
                          + 512*rho*y**3 + 2048*y**4)/(3315*al*rho**5)

# re-check the d=14 rung with these
chk = sp.simplify(sp.expand(8*a8*sp.diff(r7,y) - 7*sp.diff(a8,y)*r7 - 2*q12))
print("rung 14 re-check:", "PASS" if chk == 0 else f"FAIL {chk}")

print("\nrung 13: solving for r_6 (support j in [6,30] from N(Q^2)/N(P^3))")
found = None
for D in range(6, 26):
    rs = [sp.Symbol(f's{i}') for i in range(D+1)]
    r6 = sum(rs[i]*y**i for i in range(D+1))
    E = 7*a7*sp.diff(r7,y) - 7*sp.diff(a7,y)*r7 + 8*a8*sp.diff(r6,y) \
        - 6*sp.diff(a8,y)*r6 - 2*q11
    num, den = sp.fraction(sp.together(sp.expand(E)))
    eqs = sp.Poly(sp.expand(num), y).all_coeffs()
    Mat, vec = sp.linear_eq_to_matrix(eqs, rs)
    LN = Mat.T.nullspace()
    conds = set()
    for n in LN:
        v = sp.simplify(sp.expand((n.T*vec)[0,0]))
        if v != 0:
            nn, _ = sp.fraction(sp.together(v))
            for f, m in sp.factor_list(sp.expand(nn))[1]:
                if not f.is_number and f not in (al, be, rho):
                    conds.add(sp.expand(f))
    if not conds:
        sol = sp.solve(eqs, rs, dict=True)
        if sol and any(sp.simplify(r6.subs(s)) != 0 for s in sol):
            print(f"  D={D:2d}: CONSISTENT, no condition; r_6 = "
                  f"{sp.factor(sp.simplify(r6.subs(sol[0])))}")
            found = D; break
        else:
            print(f"  D={D:2d}: only r_6 = 0")
    else:
        print(f"  D={D:2d}: {len(conds)} residual condition(s) on C_7:")
        for x in sorted(conds, key=sp.count_ops)[:4]:
            print("       COND:", sp.factor(x))
        found = D; break
