"""
Plane Jacobian campaign - Session N2, Phase 1: the D=23 ENDGAME OPERATOR.

Transfer conjecture (Sessions 16-18): for chain degree D the First-
Framework endgame mechanism yields the block equation

    T_{D,k}(R) := (v+1)^k * ( 3v(v+1) R' - D*R )  =  -c   (c != 0),

with R the degree-D realization polynomial of the (-2)-curve Belyi map
(certified for D=23 in Phase 0) and k >= 0 the rigidity prefactor
exponent (k = 4 for D=13; k depends on the rigidity layer, so all k are
covered below).  "Fatal whenever D/3 is not an integer."  Here D = 23.

This file certifies, in exact arithmetic, every algebraic component of
the D=23 endgame, plus a D=13 regression against the Sessions 16-18
ledger (kernel trivial / rank 14 / T(R)=1 infeasible).

RESULTS (all exact):
  E1. kernel of R |-> 3v(v+1)R' - 23R on deg<=23 is trivial (rank 24).
  E2. 3v(v+1)R' - 23R = gamma (const != 0) has the UNIQUE solution
      R = -gamma/23: degree 0.  Realization demands deg R = 23
      (affine image of the certified degree-23 Shabat polynomial),
      so the k=0 endgame already contradicts realization.
  E3. for every k >= 1: T_{23,k}(R) = gamma != 0 is infeasible outright
      (evaluation at v = -1 annihilates the left side -- an identity
      argument covering ALL k >= 1; redundantly certified by exact
      linear algebra for k = 1..8).
  E4. the integrality obstruction: any Laurent-series solution of
      3v(v+1)R' = 23R at v=0 needs leading exponent n with 3n = 23 --
      impossible in Z.  (General D: solvable iff 3 | D; the M == 0
      branch of the Sessions 16-18 proof kills rational R exactly when
      3 does not divide D.  23 = 3*7 + 2.)
  E5. the rigidity collapse identity transfers with the SAME constant:
      FF: 13*(9v+8) - 117*(v+1) = -13   (deg g = 9,  g = alpha*U*v^8)
      SF: 23*(15v+14) - 345*(v+1) = -23 (deg g = 15, g = alpha*U*v^14
      predicted from val(y1,y2) = (-15,-10) = 5*(-3,-2) on the SF
      (-2)-curves; the (U-1)-exponent pattern deg(g)-1 as in FF).
      [E5 is labeled PREDICTED SHAPE: the SF rigidity layer itself is
      not re-derived here -- see D23_phase1_report.md for the honest
      conditionality ledger.]
"""
from fractions import Fraction as F
from sympy import symbols, Poly, expand, diff, Rational, linsolve, S, Matrix

v = symbols('v')

def operator_matrix(D, k, degR):
    """matrix of R -> (v+1)^k (3v(v+1)R' - D R) from deg<=degR to its image,
    as a list of rows of Fractions ((degT+1) x (degR+1))."""
    cols = []
    degT = degR + 1 + k
    for j in range(degR + 1):
        R = v**j
        T = expand((v+1)**k*(3*v*(v+1)*diff(R, v) - D*R))
        P = Poly(T, v)
        cols.append([F(int(P.nth(i))) for i in range(degT + 1)])
    return [[cols[j][i] for j in range(degR + 1)] for i in range(degT + 1)]

def qrank(M):
    """exact rank over Q by fraction Gaussian elimination."""
    M = [row[:] for row in M]
    nr, nc = len(M), len(M[0])
    rank, prow = 0, 0
    for col in range(nc):
        piv = next((r for r in range(prow, nr) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[prow], M[piv] = M[piv], M[prow]
        pv = M[prow][col]
        for r in range(nr):
            if r != prow and M[r][col] != 0:
                fac = M[r][col]/pv
                M[r] = [a - fac*b for a, b in zip(M[r], M[prow])]
        prow += 1
        rank += 1
    return rank

# ---------- D=13 regression against the Sessions 16-18 ledger ----------
M13 = operator_matrix(13, 4, 13)
r13 = qrank(M13)
print("D=13 regression:  rank of T_{13,4} on deg<=13 =", r13,
      "(Sessions 16-18: 14, kernel trivial)")
aug13 = [row + [F(1) if i == 0 else F(0)] for i, row in enumerate(M13)]
print("D=13 regression:  T_{13,4}(R) = 1 solvable:",
      r13 == qrank(aug13), "(Sessions 16-18: infeasible)")

# ---------- E1: D=23 kernel triviality ----------
M0 = operator_matrix(23, 0, 23)
r0 = qrank(M0)
print("\nE1  rank of 3v(v+1)R'-23R on deg<=23:", r0,
      "of 24  -> kernel trivial:", r0 == 24)

# ---------- E2: k=0 forced degenerate solution ----------
gamma = symbols('gamma', nonzero=True)
coeffs = symbols('r0:24')
R = sum(coeffs[i]*v**i for i in range(24))
T0 = expand(3*v*(v+1)*diff(R, v) - 23*R - gamma)
eqs = Poly(T0, v).all_coeffs()
sol = linsolve(eqs, list(coeffs))
sols = list(sol)
print("E2  solution set of 3v(v+1)R'-23R = gamma:", sols[0] if sols else "empty")
forced = sols and all(x == 0 for x in sols[0][1:]) and sols[0][0] == -gamma/23
print("E2  unique solution R = -gamma/23 (degree 0):", bool(forced))
print("E2  realization demands deg R = 23 (Phase 0 certified map)  =>"
      "  CONTRADICTION at k=0")

# ---------- E3: k >= 1 outright infeasibility ----------
# identity argument, ALL k >= 1: T_{23,k}(R) carries the factor (v+1)^k,
# so T_{23,k}(R)(-1) = 0, while gamma != 0.  Exact symbolic certificate:
Rgen = sum(coeffs[i]*v**i for i in range(24))
core = 3*v*(v+1)*diff(Rgen, v) - 23*Rgen
print("E3  identity: [(v+1)^k core](-1) = 0 for k>=1; core(-1) =",
      expand(core.subs(v, -1) + 23*Rgen.subs(v, -1)) == 0 and
      "-23*R(-1) (finite), so any k>=1 prefactor kills it")
# redundant exact-LA certificate for k = 1..8:
bad = []
for k in range(1, 9):
    Mk = operator_matrix(23, k, 23)
    augk = [row + [F(1) if i == 0 else F(0)] for i, row in enumerate(Mk)]
    if qrank(Mk) == qrank(augk):
        bad.append(k)
print("E3  k in 1..8 with T_{23,k}(R) = 1 solvable:", bad if bad else
      "none -- infeasible (matches the v = -1 evaluation argument)")

# ---------- E4: the 23/3 integrality obstruction ----------
n = symbols('n', integer=True)
# leading-order balance at v=0 for a Laurent solution of 3v(v+1)R' = 23R:
# ord-0 term: 3*n*r_n = 23*r_n  ->  3n = 23.
print("E4  3n = 23 solvable in Z:", 23 % 3 == 0, " (23 = 3*7+2)")
print("E4  general D: homogeneous branch admits rational R iff 3 | D;")
print("    D = 13: 13 % 3 =", 13 % 3, " | D = 23: 23 % 3 =", 23 % 3,
      " -> both fatal; first 'safe' chain degrees would be D = 0 mod 3")

# ---------- E5: rigidity collapse identity, FF vs SF (predicted shape) ----------
ff = expand(13*(9*v + 8) - 117*(v + 1))
sf = expand(23*(15*v + 14) - 345*(v + 1))
print("\nE5  FF collapse: 13(9v+8) - 117(v+1) =", ff, " (Sessions 16-18: -13)")
print("E5  SF collapse: 23(15v+14) - 345(v+1) =", sf, " (predicted: -23)")
print("E5  pattern: D*((deg g)v + deg g - 1) - D*deg(g)*(v+1) = -D, any D, deg g:")
Dg, dg = symbols('D dg')
print("    identity check:", expand(Dg*(dg*v + dg - 1) - Dg*dg*(v+1)) == -Dg)
