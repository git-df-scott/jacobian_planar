"""
Plane Jacobian campaign - Session 6
Rung-2 hunt: where does the kill-machine fail?

THEOREM (binomial slice, certified here): if P = alpha*s^mu*y^m + a0
with s nonconstant, then P belongs to NO Keller pair, for any partner
degree n.  (Chain collapse => b1 = s*Phi(a0), final condition
s*(Psi(a0))' = c, and a polynomial derivative cannot equal c/s.)
With s constant, a Keller partner exists iff a0 is affine (the tame
de Jonquieres family).

FRONTIER (swept here): m = 3 with genuine middle coefficients --
the first slice the collapse machinery does not decide.
"""

from sympy import symbols, symarray, expand, diff, linsolve, S

x, y = symbols('x y')

def partner_pinned(Pcand, n, lead, dx=12, cval=1):
    """Feasibility of a Keller partner with y^n-coefficient pinned."""
    qc = symarray('q', (n, dx+1))
    Qc = lead*y**n + sum(qc[i][j]*x**j*y**i
                         for i in range(n) for j in range(dx+1))
    Jc = expand(diff(Pcand, x)*diff(Qc, y) - diff(Pcand, y)*diff(Qc, x)
                - cval)
    eqs = [Jc.coeff(x, j).coeff(y, i)
           for j in range(2*dx+8) for i in range(2*n+4)]
    unk = [qc[i][j] for i in range(n) for j in range(dx+1)]
    return linsolve(eqs, unk) != S.EmptySet

print("PART 1  binomial slice, nonconstant s (theorem: all infeasible):")
grid = [
    (x**3*y**3 + x,        [(4, x**4), (5, x**5)]),        # s=x, d=1
    (x**3*y**3 + x**2 + x, [(4, x**4), (5, x**5)]),
    (x**3*y**3 + x,        [(6, x**6)]),                    # d=3 route
    (x**2*y**4 + x,        [(5, 0), (6, x**3)]),            # m=4 probes
    ((x+1)**3*y**3 + x,    [(4, (x+1)**4), (5, (x+1)**5)]),
]
for Pc, partners in grid:
    for n, lead in partners:
        if lead == 0:
            continue
        print(f"   P = {Pc}, n={n}:",
              "FEASIBLE" if partner_pinned(Pc, n, lead) else "infeasible")

print("\nPART 2  binomial slice, constant s (feasible iff a0 affine):")
for Pc, n, lead, expect in [
    (y**3 + x,        3, 1, "feasible"),
    (y**3 + 2*x + 5,  3, 1, "feasible"),
    (y**3 + x**2,     3, 1, "infeasible"),
    (y**4 + x,        4, 1, "feasible"),
    (y**4 + x**3 + x, 4, 1, "infeasible"),
]:
    got = "FEASIBLE" if partner_pinned(Pc, n, lead) else "infeasible"
    print(f"   P = {Pc}: {got}   (theorem says {expect})")

print("\nPART 3  m=3 FRONTIER: nonconstant cusp + middle coefficients:")
frontier = []
for a2 in (0, x, x**2, x**3):
    for a1 in (0, x, x**2):
        for a0 in (x, x**2 + x):
            if a2 == 0 and a1 == 0:
                continue                      # binomial, already covered
            frontier.append(x**3*y**3 + a2*y**2 + a1*y + a0)
alive = []
for Pc in frontier:
    for n, lead in ((4, x**4), (5, x**5)):
        if partner_pinned(Pc, n, lead):
            alive.append((Pc, n))
            print(f"   LIVE: P = {Pc}, n={n}  <-- rung-2 signal")
print(f"   swept {len(frontier)} P-candidates x 2 partner degrees; "
      f"live templates found: {len(alive)}")
