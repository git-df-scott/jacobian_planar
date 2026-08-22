"""
Plane Jacobian campaign - Session 4
Target: min(deg_y P, deg_y Q) <= 2  =>  tame automorphism.

  Even n:  leading condition forces B = tau*A^(n/2), so Q - tau*P^(n/2)
           drops deg_y; telescopes into classified cases.        [PART A]
  Odd n:   cusp lead (s^2, tau*s^n); general cascade formulas
             b_{n-1} = (n*tau/2) s^(n-2) a1 + kappa s^(n-1)
             b_{n-2} = (n(n-2)tau/8) s^(n-4) a1^2
                       + (kappa(n-1)/2) s^(n-3) a1
                       + (n*tau/2) s^(n-2) a0 + nu s^(n-2)       [PART B]
           and for n=5 the root-forcing identity: at a simple root
           rho of s, condition C3 evaluates to (15tau/8) s' a1^3,
           forcing s | a1 -- the root-death chain restarts.      [PART B]
  Sweeps:  pinned-lead feasibility for (2,5), (2,7).             [PART C]
"""

from sympy import (symbols, symarray, Function, expand, diff, simplify,
                   collect, linsolve, S, cancel, together, Poly, Rational)

x, y = symbols('x y')

# ============ PART A: even case, n = 4 ============
# leading condition nullspace: with A = a(x) generic, solutions B of
# 4A'B - 2AB' = 0, deg B <= 8, should be span{A^2}
a = x**2 + x + 2
Bc = list(symarray('B', 9)); B = sum(Bc[i]*x**i for i in range(9))
eqs = Poly(expand(4*diff(a, x)*B - 2*a*diff(B, x)), x).all_coeffs()
sol = linsolve(eqs, Bc)
print("PART A  (2,4) leading nullspace (expect span{A^2}, A^2 =",
      expand(a**2), "):")
print("        ", sol)
# worked example: (P, Q) = (y^2+x, tau*P^2 + y) is a (2,4) Keller pair
# and the reduction Q - tau*P^2 = y lands in the Session-2 family
tau = symbols('tau', nonzero=True)
P4 = y**2 + x; Q4 = tau*P4**2 + y
J4 = expand(diff(P4, x)*diff(Q4, y) - diff(P4, y)*diff(Q4, x))
print("PART A  J(y^2+x, tau*P^2+y) =", J4, " | reduction Q - tau*P^2 =",
      expand(Q4 - tau*P4**2))

# ============ PART B: (2,5) cascade and root-forcing ============
s, a1, a0 = [Function(nm)(x) for nm in ('s', 'a1', 'a0')]
b4, b3, b2, b1, b0 = [Function(nm)(x) for nm in ('b4', 'b3', 'b2', 'b1', 'b0')]
kap, nu, c = symbols('kappa nu c', nonzero=True)
P = s**2*y**2 + a1*y + a0
Q = tau*s**5*y**5 + b4*y**4 + b3*y**3 + b2*y**2 + b1*y + b0
J = expand(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x))
conds = {k: J.coeff(y, k) for k in range(7)}
print("PART B  [y^6] (expect 0):", simplify(conds[6]))
f_b4 = Rational(5, 2)*tau*s**3*a1 + kap*s**4
c5 = simplify(conds[5].subs(b4, f_b4).doit())
print("PART B  [y^5] with general b4-formula (expect 0):", c5)
f_b3 = (Rational(15, 8)*tau*s*a1**2 + 2*kap*s**2*a1
        + Rational(5, 2)*tau*s**3*a0 + nu*s**3)
c4 = simplify(conds[4].subs(b4, f_b4).subs(b3, f_b3).doit())
print("PART B  [y^4] with general b3-formula (expect 0):", cancel(c4))
# root-forcing: C3 = [y^3]; the b2-terms carry factors s or A=s^2, so
# C3 mod (s) reduces to  a1*b3' - 3*a1'*b3 - 4*a0'*b4  mod (s).
# With the formulas, that should equal (15*tau/8) * s' * a1^3  mod (s).
expr = (a1*diff(f_b3, x) - 3*diff(a1, x)*f_b3 - 4*diff(a0, x)*f_b4)
target = Rational(15, 8)*tau*diff(s, x)*a1**3
print("PART B  (C3 residue - target) as a multiple of s:",
      simplify(cancel(together(expr - target)/s)) != S.NaN and
      "divisible" if simplify(expand(expr - target).subs(s, 0)) == 0
      else "NOT divisible")

# ============ PART C: pinned-lead sweeps ============
def partner_pinned(Pcand, n, lead, dx=12, cval=1):
    qc = symarray('q', (n, dx+1))
    Qc = lead*y**n + sum(qc[i][j]*x**j*y**i
                         for i in range(n) for j in range(dx+1))
    Jc = expand(diff(Pcand, x)*diff(Qc, y) - diff(Pcand, y)*diff(Qc, x)
                - cval)
    eqs = [Jc.coeff(x, j).coeff(y, i)
           for j in range(2*dx+6) for i in range(2*n+3)]
    unk = [qc[i][j] for i in range(n) for j in range(dx+1)]
    return linsolve(eqs, unk)

print("\nPART C  (2,5) pinned-lead sweeps (s=x squarefree, s=x^2, s=1):")
grid5 = [(x, x**2, x), (x, x**2 + x**3, x + x**2), (x, x**3, x),
         (x**2, x**2, x), (x**2, x**3, x + x**2),
         (1, 0, x), (1, x, x), (1, 3, x + 5)]
for sc, a1c, a0c in grid5:
    Pc = sc**2*y**2 + a1c*y + a0c
    r = partner_pinned(Pc, 5, sc**5)
    print(f"   s={sc}, P=s^2*y^2+({a1c})*y+({a0c}):",
          "FEASIBLE" if r != S.EmptySet else "infeasible")

print("PART C  (2,7) pinned-lead spot checks:")
for sc, a1c, a0c in [(x, x**2, x), (1, 0, x), (x**2, x**3, x)]:
    Pc = sc**2*y**2 + a1c*y + a0c
    r = partner_pinned(Pc, 7, sc**7)
    print(f"   s={sc}, P=s^2*y^2+({a1c})*y+({a0c}):",
          "FEASIBLE" if r != S.EmptySet else "infeasible")
