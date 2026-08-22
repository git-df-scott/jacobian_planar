"""
Plane Jacobian campaign - Session 3
Target: upgrade the y-degree theorem from <=2 to <=3.

Structure of the (<=3, <=3) case after Wronskian reduction:
  (1,n): P linear in y  ->  claim Q = phi(P) - (c/alpha)x + const  [PART A]
  (2,3): A = s^2, B = tau*s^3 forced.  Cascade gives
         b2 = (3tau/2) s a1 + kappa s^2
         b1 = (3tau/8) a1^2/s + kappa a1 + (3tau/2) s a0 + nu s
         so s | a1^2.                                             [PART B]
     - s nonconstant squarefree: killed by hand (root evaluation).
     - s with repeated roots / s constant: machine sweeps.        [PART C]
"""

from sympy import (symbols, Function, symarray, expand, simplify, diff,
                   collect, Poly, linsolve, S, together, cancel)

x, y = symbols('x y')

# ============ PART A: (1,n) normal form, n = 3 and 4 ============
# With P = y + b(x) (alpha=1 wlog), homogeneous solutions of J(P,Q)=0
# with deg_y Q <= n should be exactly span{1, P, ..., P^n}, and
# Q = -x is a particular solution of J = 1.
for n in (3, 4):
    bc = symarray('beta', 4)
    b = sum(bc[i]*x**i for i in range(4))
    P = y + b
    dx = 3*n + 1
    qc = symarray('q', (n+1, dx+1))
    Q = sum(qc[i][j]*x**j*y**i for i in range(n+1) for j in range(dx+1))
    J0 = expand(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x))
    eqs = [J0.coeff(x, j).coeff(y, i) for j in range(2*dx+2)
           for i in range(2*n+2)]
    unk = [qc[i][j] for i in range(n+1) for j in range(dx+1)]
    sol = linsolve(eqs, unk)
    nfree = len((list(sol)[0]).free_symbols - set(bc)) if sol != S.EmptySet else -1
    print(f"PART A  (1,{n}): dim of homogeneous solution space = {nfree}"
          f"   (expect {n+1}, i.e. span of 1, P, ..., P^{n})")

# ============ PART B: verify the (2,3) cascade formulas ============
s, a1, a0, b2, b1, b0 = [Function(nm)(x) for nm in
                         ('s', 'a1', 'a0', 'b2', 'b1', 'b0')]
tau, kap, nu, c = symbols('tau kappa nu c', nonzero=True)
P = s**2*y**2 + a1*y + a0
Q = tau*s**3*y**3 + b2*y**2 + b1*y + b0
J = expand(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x))
Jy = collect(J, y)
conds = {k: simplify(Jy.coeff(y, k)) for k in range(5)}
print("PART B  [y^4] condition (expect 0):", conds[4])
# substitute the integrated formulas and check [y^3], [y^2] vanish
sub2 = {b2: tau*S(3)/2*s*a1 + kap*s**2}
c3 = simplify(conds[3].subs(sub2).doit())
print("PART B  [y^3] after b2-formula (expect 0):", c3)
sub1 = {b1: tau*S(3)/8*a1**2/s + kap*a1 + tau*S(3)/2*s*a0 + nu*s}
c2 = simplify(conds[2].subs(sub2).subs(sub1).doit())
print("PART B  [y^2] after b1-formula (expect 0):", cancel(c2))
print("PART B  => s | a1^2 required for b1 to be a polynomial.")

# ============ PART C: kill sweeps for surviving branches ============
def keller_partner(Pcand, dx=10, dy=3, cval=1):
    qc = symarray('q', (dy+1, dx+1))
    Qc = sum(qc[i][j]*x**j*y**i for i in range(dy+1) for j in range(dx+1))
    Jc = expand(diff(Pcand, x)*diff(Qc, y) - diff(Pcand, y)*diff(Qc, x) - cval)
    eqs = [Jc.coeff(x, j).coeff(y, i) for j in range(2*dx+2)
           for i in range(2*dy+2)]
    unk = [qc[i][j] for i in range(dy+1) for j in range(dx+1)]
    return linsolve(eqs, unk)

print("\nPART C1  repeated-root branch, s = x^2 (A = x^4, dangerous "
      "profile: x | a1, x^2 does not divide a1, a0'(0) != 0):")
for a1c, a0c in [(x, x), (x, x + x**2), (x + x**3, x),
                 (x*(1 + x), x + x**3), (x, x + x**2 + x**4)]:
    Pc = x**4*y**2 + a1c*y + a0c
    res = keller_partner(Pc)
    print(f"   P = x^4*y^2 + ({a1c})*y + ({a0c}):",
          "FEASIBLE" if res != S.EmptySet else "infeasible")

print("\nPART C2  constant-lead branch, s = 1 (A = 1, B = tau):")
for a1c, a0c in [(0, x), (0, x + x**3), (1, x), (x, x), (x, x + x**2),
                 (x**2, x), (x**2, x + x**3), (2*x, x**2 + x)]:
    Pc = y**2 + a1c*y + a0c
    res = keller_partner(Pc)
    print(f"   P = y^2 + ({a1c})*y + ({a0c}):",
          "FEASIBLE" if res != S.EmptySet else "infeasible")


# ============ PART D: pinned-lead re-sweeps and phantom check ============


def partner_pinned(Pcand, lead, dx=12, dy_low=2, cval=1):
    """Keller partner with y^3-coefficient PINNED to `lead` (tau=1)."""
    qc = symarray('q', (dy_low+1, dx+1))
    Qc = lead*y**3 + sum(qc[i][j]*x**j*y**i
                         for i in range(dy_low+1) for j in range(dx+1))
    Jc = expand(diff(Pcand,x)*diff(Qc,y) - diff(Pcand,y)*diff(Qc,x) - cval)
    eqs = [Jc.coeff(x,j).coeff(y,i) for j in range(2*dx+4) for i in range(2*dy_low+4)]
    unk = [qc[i][j] for i in range(dy_low+1) for j in range(dx+1)]
    return linsolve(eqs, unk)

print("Constant-lead branch, y^3-coefficient pinned to 1:")
for a1c, a0c in [(0,x),(1,x),(2*x,x**2+x),(0,x+x**3),(x,x),(3,x+5)]:
    r = partner_pinned(y**2 + a1c*y + a0c, 1)
    print(f"   P = y^2 + ({a1c})*y + ({a0c}):",
          "FEASIBLE" if r != S.EmptySet else "infeasible")

print("Repeated/mixed-root branch, y^3-coefficient pinned to s^3:")
for sc, a1c, a0c in [(x**2, x, x), (x**2, x, x+x**2), (x**3, x**2, x),
                     (x**3, x, x), (x**2*(x-1), x*(x-1), x)]:
    r = partner_pinned(sc**2*y**2 + a1c*y + a0c, sc**3)
    print(f"   s = {sc}, P = s^2*y^2 + ({a1c})*y + ({a0c}):",
          "FEASIBLE" if r != S.EmptySet else "infeasible")

# sanity: the earlier 'FEASIBLE' phantom really was a degenerate partner
qc = symarray('q', (2, 4))
Qc = sum(qc[i][j]*x**j*y**i for i in range(2) for j in range(4))
Jc = expand(diff(y**2+x,x)*diff(Qc,y) - diff(y**2+x,y)*diff(Qc,x) - 1)
eqs = [Jc.coeff(x,j).coeff(y,i) for j in range(8) for i in range(6)]
sol = linsolve(eqs, [qc[i][j] for i in range(2) for j in range(4)])
print("phantom check, P = y^2 + x, deg_y Q <= 1 partner exists:",
      sol != S.EmptySet, " (e.g. Q = y, the Session-2 family)")
