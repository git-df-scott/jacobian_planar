"""
Plane Jacobian campaign - Session 2
Theorem (target): every Keller map of C^2 with deg_y P <= 2 and
deg_y Q <= 2 is a (tame) polynomial automorphism.

Proof chain being certified:
  Wronskian step: y^3-coeff of J forces top y-coefficients linearly
    dependent -> reduce to P linear in y, Q quadratic in y.
  L1: 2a'e - ae' = 0        =>  e = lambda * a^2
  L2: a'f + 2b'e - af' = 0  =>  f = a*(2*lambda*b + kappa)
  L3: b'f - ag' = c         =>  a | c  =>  a constant
  =>  Q = lambda*P^2 + kappa*P - (c/alpha)*x - h0   (explicitly invertible)

PART 4 probes door #3: y-degree (2,3) pairs. Leading condition
  3A'B - 2AB' = 0  =>  (A, B) = (s^2, tau*s^3)   (cuspidal pattern),
then a linear-in-Q feasibility test for nonconstant s.
"""

from sympy import (symbols, symarray, expand, simplify, Poly, linsolve,
                   diff, Rational, groebner, S)
import itertools, random

x, y = symbols('x y')

# ================= PART 1: forward certificate =================
alpha, lam, kap, c0, p, q = symbols('alpha lambda kappa c p q', nonzero=True)
bc = symarray('beta', 7)
b = sum(int(1)*bc[i]*x**i for i in range(7))
P = alpha*y + b
Q = lam*P**2 + kap*P - (c0/alpha)*x
J = expand(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x))
print("PART1  J(P,Q) for generic degree-6 b(x):", J)
X = (alpha/c0)*(lam*p**2 + kap*p - q)
Y = (p - b.subs(x, X))/alpha
print("PART1  P(X,Y)-p == 0 :", simplify(P.subs({x: X, y: Y}) - p) == 0)
print("PART1  Q(X,Y)-q == 0 :", simplify(Q.subs({x: X, y: Y}) - q) == 0)

# ================= PART 2: lemma certificates =================
def null_space(eq_poly, unknowns):
    eqs = Poly(expand(eq_poly), x).all_coeffs()
    sol = linsolve(eqs, unknowns)
    return sol

# L1: with generic squarefree a, solutions e (deg<=6) of 2a'e-ae'=0
a = x**3 + 2*x - 1
ec = list(symarray('e', 7)); e = sum(ec[i]*x**i for i in range(7))
sol = null_space(2*diff(a, x)*e - a*diff(e, x), ec)
print("PART2  L1 solution space (expect multiples of a^2):", sol)

# L2: with e = a^2, b fixed: solutions f of a'f + 2b'e - af' = 0
bfix = x**2 - x + 3
fc = list(symarray('f', 7)); f = sum(fc[i]*x**i for i in range(7))
sol = null_space(diff(a, x)*f + 2*diff(bfix, x)*a**2 - a*diff(f, x), fc)
print("PART2  L2 solution space (expect 2ab + kappa*a):", sol)
print("PART2  L2 reference 2ab =", expand(2*a*bfix), "   a =", expand(a))

# L3: b'f - a g' = c with f = a(2b+kappa): reduce mod a  ->  a | c
#     (machine check: remainder of b'f - c mod a is -c for symbolic kappa, c)
kappa_s, c_s = symbols('kappa_s c_s')
ff = a*(2*bfix + kappa_s)
rem = Poly(expand(diff(bfix, x)*ff - c_s), x).rem(Poly(a, x))
print("PART2  L3 (b'f - c) mod a  =", rem.as_expr(), "  (so a | c => a constant)")

# ================= PART 3: numeric sweep =================
ok = True
for trial in range(200):
    al = random.choice([1, 2, -1, 3]); la = random.choice([1, -2, 3])
    ka = random.randint(-3, 3); cc = random.choice([1, -2, 5])
    bb = sum(random.randint(-4, 4)*x**i for i in range(random.randint(1, 6)+1))
    Pn = al*y + bb; Qn = la*Pn**2 + ka*Pn - Rational(cc, al)*x
    x0, y0 = random.randint(-9, 9), random.randint(-9, 9)
    pv, qv = Pn.subs({x: x0, y: y0}), Qn.subs({x: x0, y: y0})
    Xv = Rational(al, cc)*(la*pv**2 + ka*pv - qv)
    Yv = (pv - bb.subs(x, Xv))/al
    if (Xv, Yv) != (x0, y0): ok = False
print("PART3  200 random instances, inverse(F(pt)) == pt :", ok)

# ================= PART 4: y-degree 3 opener =================
# leading condition for a (2,3) pair: 3A'B - 2AB' = 0, A=y^2-coeff of P,
# B=y^3-coeff of Q.  Solve for B (deg<=6) with A = x^2:
Bc = list(symarray('B', 7)); B = sum(Bc[i]*x**i for i in range(7))
sol = null_space(3*diff(x**2, x)*B - 2*x**2*diff(B, x), Bc)
print("PART4  leading-condition solutions with A=x^2 (expect span{x^3}):", sol)

# feasibility probe: does ANY Q with deg_y<=3, deg_x<=6 make J(P,Q)=1
# for cuspidal P?  (linear system in Q's coefficients; c set to 1)
def keller_partner_exists(Pcand, dx=6, dy=3):
    qc = symarray('q', (dy+1, dx+1))
    Qc = sum(qc[i][j]*x**j*y**i for i in range(dy+1) for j in range(dx+1))
    Jc = expand(diff(Pcand, x)*diff(Qc, y) - diff(Pcand, y)*diff(Qc, x) - 1)
    eqs = [Jc.coeff(x, j).coeff(y, i)
           for j in range(2*dx+2) for i in range(2*dy+2)]
    unknowns = [qc[i][j] for i in range(dy+1) for j in range(dx+1)]
    return linsolve(eqs, unknowns) != S.EmptySet

for Pcand in [x**2*y**2 + y, x**2*y**2 + x*y + 1, x**2*y**2 + y + x,
              x**2*y**2 + x**3*y + 1]:
    print(f"PART4  Keller partner (J=1) exists for P = {Pcand} :",
          keller_partner_exists(Pcand))
