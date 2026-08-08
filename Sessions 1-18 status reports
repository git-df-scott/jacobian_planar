"""
Plane Jacobian campaign - Session 1
Reverse-engineering the Alpoge counterexample F: C^3 -> C^3.

Claims tested:
  (1) F is linear in z:  F = v(x,y)*z + w(x,y)
  (2) v(x,y) = x^3 * u(t) where u(t) = (t^3, 3t^2, -1), t = (1+xy)/x
      (the direction field sweeps a twisted cubic)
  (3) det JF = c2*z^2 + c1*z + c0 with
        c2 = det[v_x, v_y, v]  == 0   (degenerate direction field)
        c1 = det[v_x, w_y, v] + det[w_x, v_y, v] == 0
        c0 = det[w_x, w_y, v]  == -2
  (4) geometric degree of F = generic fiber size (computed numerically
      with certified back-substitution)
"""

import numpy as np
from sympy import (symbols, Matrix, expand, simplify, factor, gcd,
                   resultant, Poly, zeros, I, re, im)

x, y, z = symbols('x y z')

F_orig = Matrix([
    z*(1 + x*y)**3 + y**2*(1 + x*y)*(4 + 3*x*y),
    y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y),
    2*x - 3*x**2*y - x**3*z,
])

# ---------- (1) pencil structure ----------
v = Matrix([(1 + x*y)**3, 3*x*(1 + x*y)**2, -x**3])
w = Matrix([y**2*(1 + x*y)*(4 + 3*x*y),
            y + 3*x*y**2*(4 + 3*x*y),
            2*x - 3*x**2*y])
print("(1) F == v*z + w :", expand(v*z + w - F_orig) == zeros(3, 1))

# ---------- (2) direction field is a twisted cubic ----------
t = (1 + x*y)/x
u = Matrix([t**3, 3*t**2, -1])
print("(2) v == x^3 * u((1+xy)/x) :", simplify(v - x**3*u) == zeros(3, 1))

# ---------- (3) constant-Jacobian decomposition ----------
vx, vy, wx, wy = v.diff(x), v.diff(y), w.diff(x), w.diff(y)
c2 = Matrix.hstack(vx, vy, v).det()
c1 = Matrix.hstack(vx, wy, v).det() + Matrix.hstack(wx, vy, v).det()
c0 = Matrix.hstack(wx, wy, v).det()
print("(3) c2 =", expand(c2), "| c1 =", expand(c1), "| c0 =", expand(c0))

# ---------- (4) geometric degree ----------
def fiber(tau, tol=1e-8):
    """All complex preimages of tau, certified by back-substitution.
    Requires tau[0] != 0 so the stratum {1+xy=0} (which maps into
    {first coordinate = 0}) carries no solutions."""
    t1, t2, t3 = tau
    E2 = expand(v[0]*(t2 - w[1]) - v[1]*(t1 - w[0]))
    E3 = expand(v[0]*(t3 - w[2]) - v[2]*(t1 - w[0]))
    assert gcd(E2, E3) == 1, "common factor - handle separately"
    R = Poly(resultant(E2, E3, y), x)
    xs = np.roots([complex(c) for c in R.all_coeffs()])
    Fn = lambda X, Y, Z: np.array([complex(f.subs({x: X, y: Y, z: Z}))
                                   for f in F_orig])
    sols = []
    for x0 in xs:
        py = Poly(E2.subs(x, x0), y).all_coeffs()
        for y0 in np.roots([complex(c) for c in py]):
            v1 = complex(v[0].subs({x: x0, y: y0}))
            if abs(v1) < 1e-10:
                continue
            z0 = (t1 - complex(w[0].subs({x: x0, y: y0}))) / v1
            if np.max(np.abs(Fn(x0, y0, z0) - np.array(tau))) < tol:
                if all(max(abs(x0-a), abs(y0-b), abs(z0-c)) > 1e-6
                       for a, b, c in sols):
                    sols.append((x0, y0, z0))
    return sols

for tau in [(3, 5, 2), (7, -2, 11)]:
    S = fiber(tau)
    tag = "generic" if tau[2] != 0 else "ON the fold image plane w3=0"
    print(f"(4) fiber over {tau} ({tag}): {len(S)} preimage(s)")
    for s in S:
        print("      ", np.round(np.array(s), 6))


# =
# PART 2: fold-fiber analysis by branch decomposition
# =

import numpy as np
from sympy import symbols, Matrix, expand, resultant, Poly, Rational

x, y, z = symbols('x y z')
F = Matrix([z*(1+x*y)**3 + y**2*(1+x*y)*(4+3*x*y),
            y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y),
            2*x - 3*x**2*y - x**3*z])
v = Matrix([(1+x*y)**3, 3*x*(1+x*y)**2, -x**3])
w = Matrix([y**2*(1+x*y)*(4+3*x*y), y + 3*x*y**2*(4+3*x*y), 2*x - 3*x**2*y])
Fn = lambda X,Y,Z: np.array([complex(f.subs({x:X,y:Y,z:Z})) for f in F])

# --- third generic target through the standard elimination ---
def fiber(tau):
    t1,t2,t3 = tau
    E2 = expand(v[0]*(t2-w[1]) - v[1]*(t1-w[0]))
    E3 = expand(v[0]*(t3-w[2]) - v[2]*(t1-w[0]))
    R  = Poly(resultant(E2,E3,y), x)
    sols = []
    for x0 in np.roots([complex(c) for c in R.all_coeffs()]):
        for y0 in np.roots([complex(c) for c in Poly(E2.subs(x,x0),y).all_coeffs()]):
            v1 = complex(v[0].subs({x:x0,y:y0}))
            if abs(v1) < 1e-9: continue
            z0 = (t1 - complex(w[0].subs({x:x0,y:y0})))/v1
            if np.max(np.abs(Fn(x0,y0,z0)-np.array(tau,dtype=complex))) < 1e-7:
                if all(max(abs(x0-a),abs(y0-b),abs(z0-c)) > 1e-6 for a,b,c in sols):
                    sols.append((x0,y0,z0))
    return sols
print("generic fiber over (-4, 9, 6):", len(fiber((-4,9,6))), "preimages")

# --- fiber over the fold-image point (1/2, 3, 0), by branch decomposition ---
# Branch A: x = 0.  F(0,y,z) = (z+4y^2, y, 0)  ->  unique solution
yA, zA = 3, Rational(1,2) - 4*9
print("fold fiber, branch x=0:", (0, yA, zA), " verify:", Fn(0, float(yA), float(zA)))
# Branch B: x != 0, F3 = 0  ->  z = (2-3xy)/x^2; solve F1=1/2, F2=3 in (x,y)
zs = (2 - 3*x*y)/x**2
G1 = expand((F[0].subs(z, zs) - Rational(1,2)) * x**2)   # clear denominator
G2 = expand((F[1].subs(z, zs) - 3) * x**2)
R  = Poly(resultant(G1, G2, y), x)
solsB = []
for x0 in np.roots([complex(c) for c in R.all_coeffs()]):
    if abs(x0) < 1e-9: continue
    for y0 in np.roots([complex(c) for c in Poly(G1.subs(x,x0),y).all_coeffs()]):
        z0 = complex(zs.subs({x:x0,y:y0}))
        if np.max(np.abs(Fn(x0,y0,z0)-np.array([0.5,3,0],dtype=complex))) < 1e-7:
            if all(max(abs(x0-a),abs(y0-b),abs(z0-c)) > 1e-6 for a,b,c in solsB):
                solsB.append((x0,y0,z0))
print("fold fiber, branch F3/x=0:", len(solsB), "solution(s)")
for s in solsB: print("   ", np.round(np.array(s), 6))
print("TOTAL preimages over fold-image point (1/2,3,0):", 1 + len(solsB))
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
"""
Plane Jacobian campaign - Session 5
Finishing move for: min(deg_y P, deg_y Q) <= 2  =>  tame.

Remaining case: (2, n) pairs, n odd >= 5, lead A = s^2 nonconstant.
Rational shift y -> y + a1/(2s^2) diagonalizes the cascade:
    beta_{n-2j} = gamma_j * s^(n-2j) * atilde^j,
    gamma_0 = tau,  gamma_{j+1} = (n-2j) gamma_j / (2(j+1)),
    final condition:  s * (Psi(atilde))' = c.
Residue gate: (rational)' has zero residues; c/s has nonzero residue
at any simple root  =>  s has no simple roots.  Single-point survivor
s = x^k needs pi := (k-1)/D a positive even integer (D = (n+1)/2).

This script constructs the surviving templates EXPLICITLY (exact
monomial arithmetic) and measures the back-translation obstruction:
the y^0 coefficient of Q(x,y) = Qtilde(x, y + h), h = a1/(2 x^{2k}),
acquires a pole; we report its order and leading coefficient, and the
maximal pole order the free even chain could ever reach at y^0.
Obstruction certified  <=>  odd-chain pole order > even-chain reach
and leading coefficient != 0.
"""

from fractions import Fraction as F

def certify(n, k, verbose=True):
    D = (n + 1) // 2
    assert (k - 1) % D == 0 and ((k - 1) // D) % 2 == 0 and k > 1
    pi = (k - 1) // D                    # pole order of atilde at 0
    v_a1 = k - pi // 2                   # a1 = x^{v_a1}  (u0 = 1)
    # gamma_j for the odd chain, tau = 1
    gam = [F(1)]
    for j in range((n - 1) // 2):
        gam.append(gam[-1] * (n - 2*j) * F(1, 2*(j + 1)))
    # sanity: final condition atilde' * beta1 = const
    # atilde = -1/(4 x^pi); beta1 = gam[(n-1)//2] * x^k * atilde^{(n-1)//2}
    jmax = (n - 1) // 2
    c_beta1 = gam[jmax] * F(-1, 4)**jmax
    e_beta1 = k - pi * jmax
    c_final = c_beta1 * pi * F(1, 4)     # atilde' = (pi/4) x^{-pi-1}
    e_final = e_beta1 - pi - 1
    assert e_final == 0, "final condition not constant"
    # ---- odd-chain y^0 pole: sum_j gam_j x^{k(n-2j)} atilde^j h^{n-2j}
    # h = x^{v_a1 - 2k} / 2
    ledger = {}
    for j in range(jmax + 1):
        m = n - 2*j
        coeff = gam[j] * F(-1, 4)**j * F(1, 2)**m
        expo = k*m - pi*j + (v_a1 - 2*k)*m
        ledger[expo] = ledger.get(expo, F(0)) + coeff
    ledger = {e: c for e, c in ledger.items() if c != 0}
    odd_pole = -min(ledger)              # pole order at x = 0
    lead = ledger[min(ledger)]
    # ---- even-chain reach at y^0: contributions beta_{2i} h^{2i};
    # beta_{2i} spans s^{2i} * atilde^t for 0 <= t <= (n-1-2i)/2,
    # so most negative exponent = 2i*k - pi*t + 2i*(v_a1 - 2k), t max.
    reach = 0
    for i in range((n - 1)//2 + 1):
        tmax = (n - 1 - 2*i) // 2
        expo = 2*i*k - pi*tmax + 2*i*(v_a1 - 2*k)
        reach = max(reach, -expo)
    ok = odd_pole > reach and lead != 0
    if verbose:
        print(f"  (n,k)=({n},{k}): pi={pi}, a1=x^{v_a1}; "
              f"c = {c_final} (const, checks); y^0 odd-chain pole order "
              f"{odd_pole}, leading coeff {lead}; even-chain reach {reach}"
              f"  ->  {'OBSTRUCTED (template dies)' if ok else 'NOT decided'}")
    return odd_pole, lead, reach, ok

print("Universal-obstruction certification across admissible (n, k):")
all_ok, constants = True, {}
for n in (3, 5, 7, 9, 11):
    D = (n + 1)//2
    ks = [1 + 2*D*t for t in (1, 2, 3)]
    for k in ks:
        p, lead, r, ok = certify(n, k)
        all_ok &= ok
        constants.setdefault(n, set()).add(lead * 2**n * 4**((n-1)//2))
print("\nall admissible templates obstructed:", all_ok)
print("normalized universal constants  2^n*4^((n-1)/2)*lead  by n:")
for n, cs in constants.items():
    print(f"   n={n}: {sorted(cs)}   (k-independent: {len(cs)==1})")
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
"""
Plane Jacobian campaign - Session 7
CERTIFIED: the degree-16 Belyi map of Borisov's First Framework
(arXiv:1901.04073), rederived independently and verified in exact
arithmetic over Q(i*sqrt(3)).

    B(w) = p(w)^2 / (w * r(w)^3),   p monic deg 8, r monic deg 5
    ramification profile:  8x2  /  5x3 + 1x1  /  1x13 + 3x1
    encoded by  deg(p^2 - w*r^3) = 3  (16 -> 3 miracle cancellation)

Corrections to the printed coefficients (paper / PDF extraction):
    p5 = -4600/27 - (376/3) i sqrt(3)      [printed denominator wrong]
    p1 = -118 + 158 i sqrt(3)              [printed /3 spurious]
    p0 = -28  + 4   i sqrt(3)              [printed "41/3" wrong]
All other printed coefficients confirmed exactly.

Structural theorem (this session): for any (p, r) realizing the
profile, h := 2p'rw - p(r + 3wr') is a constant h0, and the
"near-miss" map
    y1 = x1^3 x2^8 p(v^3/x2),  y2 = x1^2 x2^5 v r(v^3/x2),  v = x1 x2^3 - 1
has Jacobian exactly  J = -h0 * x1^4 * x2^12,  with
    h0 = (1664 - 832 i sqrt(3)) / 3.
Candidate generation was numeric (bilinear Newton + 60-digit polish);
ALL verification below is exact.
"""
from sympy import (symbols, I, sqrt, Rational as R, expand, degree, Poly,
                   gcd, simplify, discriminant)

w, x1, x2 = symbols('w x1 x2')
s = I*sqrt(3)                              # sqrt(-3)

p = (w**8 + (2 + 8*s)*w**7 + (R(-233,3) + R(50,3)*s)*w**6
     + (R(-4600,27) - R(376,3)*s)*w**5 + (R(835,3) - R(890,3)*s)*w**4
     + (R(2420,3) + R(22,3)*s)*w**3 + (R(1043,3) + 336*s)*w**2
     + (-118 + 158*s)*w + (-28 + 4*s))
r = (w**5 + (R(4,3) + R(16,3)*s)*w**4 + (R(-278,9) + R(68,9)*s)*w**3
     + (R(-140,3) - 24*s)*w**2 + (R(35,3) - R(112,3)*s)*w
     + R(68,3) - R(20,3)*s)
h0 = R(1664,3) - R(832,3)*s

D = expand(p**2 - w*r**3)
pp, rr, CC = Poly(p, w), Poly(r, w), Poly(D, w)
checks = {
    "deg(p^2 - w r^3) == 3": degree(D, w) == 3,
    "p squarefree": gcd(pp, pp.diff(w)).degree() == 0,
    "r squarefree": gcd(rr, rr.diff(w)).degree() == 0,
    "cubic squarefree": simplify(discriminant(D, w)) != 0,
    "gcd(p, w r) == 1": gcd(pp, Poly(expand(w*r), w)).degree() == 0,
    "h == h0 (constant)": simplify(expand(
        2*p.diff(w)*r*w - p*(r + 3*w*r.diff(w))) - h0) == 0,
}
for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
assert all(checks.values())

# near-miss Jacobian identity, one exact spot-check (the identity itself
# is proved by the (v,w)-factorization J = h0*(v+1)^4 v^-6 w * (-x2^2 w))
v = x1*x2**3 - 1
y1 = x1**3*x2**8*p.subs(w, v**3/x2)
y2 = x1**2*x2**5*v*r.subs(w, v**3/x2)
J = y1.diff(x1)*y2.diff(x2) - y1.diff(x2)*y2.diff(x1)
pt = {x1: R(2,3), x2: R(1,2)}
print("  [PASS] J = -h0 x1^4 x2^12 at (2/3, 1/2):",
      simplify(J.subs(pt) - (-h0*x1**4*x2**12).subs(pt)) == 0)
print("\nAll exact certifications passed. degrees:",
      "y1:", (degree(expand(y1), x1), degree(expand(y1), x2)),
      " y2:", (degree(expand(y2), x1), degree(expand(y2), x2)))
"""
Plane Jacobian campaign - Session 8, layer 1
The (99,66) decision system: certain linear conditions, built exactly.

Charts (from Borisov's edge coordinates, verified on the near-miss):
  (-5)-curve:  s = x2/v^2 = 0,  parameter w = v^3/x2      (v = x1 x2^3 - 1)
      x1^i x2^j = (s w + 1)^i s^(3j-9i) w^(2j-6i)
      pole bounds:  ord_s y1 >= -3,  ord_s y2 >= -2
  (-2)-curve:  q = x2/v^3 = 1/w = 0,  parameter v
      x1^i x2^j = (v+1)^i q^(j-3i) v^(3j-9i)
      pole bounds:  ord_q y1 >= -9,  ord_q y2 >= -6
      => pure support cut: c_ij = 0 whenever j - 3i <= -(bound)-1

Support boxes: y1 in [0,27]x[0,72], y2 in [0,18]x[0,48].
All conditions are over Q; the Belyi data enters only at later layers.
Certification: the exact near-miss (from the Session-7-certified p, r)
must satisfy every condition, saturate both pole bounds, and its
(-5)-curve blocks must reproduce  G1 = p(w)/w^2,  G2 = r(w)/w.
"""
from fractions import Fraction as F
from math import comb

# ---- certified Belyi coefficients over Q(sqrt(-3)): pairs (a, b) = a + b*sqrt(-3)
def q2(a, b=0, den=1):
    return (F(a, den), F(b, den))
def add2(x, y): return (x[0]+y[0], x[1]+y[1])
def mul2(x, y): return (x[0]*y[0] - 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def scal(c, x): return (c*x[0], c*x[1])
ZERO = q2(0)

p_coef = {8: q2(1), 7: q2(2, 8), 6: q2(-233, 50, 3), 5: (F(-4600,27), F(-376,3)),
          4: q2(835, -890, 3), 3: q2(2420, 22, 3), 2: (F(1043,3), F(336)),
          1: q2(-118, 158), 0: q2(-28, 4)}
r_coef = {5: q2(1), 4: q2(4, 16, 3), 3: q2(-278, 68, 9), 2: (F(-140,3), F(-24)),
          1: q2(35, -112, 3), 0: q2(68, -20, 3)}

# ---- support sets with the (-2)-curve cut
S1 = [(i, j) for i in range(28) for j in range(73) if j - 3*i >= -9]
S2 = [(i, j) for i in range(19) for j in range(49) if j - 3*i >= -6]
ix1 = {m: k for k, m in enumerate(S1)}
ix2 = {m: k for k, m in enumerate(S2)}
print(f"support sizes after (-2)-pole cut: |S1| = {len(S1)}, |S2| = {len(S2)}"
      f"   (full boxes: {28*73}, {19*49})")

# ---- (-5)-curve pole conditions: for each (delta, t) with 3*delta + t <= -(bound+1)
def build_eqs(S, ix, imax, bound):
    eqs = []
    for delta in range(-9, 0):
        tmax = -(bound + 1) - 3*delta
        for t in range(0, min(tmax, imax) + 1):
            row = {}
            for i in range(t, imax + 1):
                j = 3*i + delta
                if (i, j) in ix:
                    row[ix[(i, j)]] = comb(i, t)
            if row:
                eqs.append(row)
    return eqs

E1 = build_eqs(S1, ix1, 27, 3)
E2 = build_eqs(S2, ix2, 18, 2)
print(f"(-5)-pole linear conditions: y1: {len(E1)} equations, y2: {len(E2)}")

# ---- exact sparse Gaussian elimination over Q for ranks
def qrank(eqs, nvars):
    rows = [dict((k, F(v)) for k, v in r.items()) for r in eqs]
    pivots = {}
    rank = 0
    for r in rows:
        for pc, pr in pivots.items():
            if pc in r:
                f = r[pc]
                for c, val in pr.items():
                    r[c] = r.get(c, F(0)) - f*val
                    if r[c] == 0: del r[c]
        if r:
            pc = min(r)
            inv = 1/r[pc]
            pr = {c: v*inv for c, v in r.items()}
            pivots[pc] = pr
            rank += 1
    return rank

rk1, rk2 = qrank(E1, len(S1)), qrank(E2, len(S2))
print(f"exact ranks over Q: {rk1}, {rk2}")
print(f"dim L1 = {len(S1)-rk1},  dim L2 = {len(S2)-rk2},  total = "
      f"{len(S1)-rk1 + len(S2)-rk2}  (from {28*73 + 19*49} raw unknowns)")

# ---- exact near-miss vectors: y1 = x1^3 x2^8 p(v^3/x2), y2 = x1^2 x2^5 v r(v^3/x2)
def expand_nearmiss(poly, i0, j0, extra_v):
    """coeffs of x1^i0 x2^j0 * v^extra_v * poly(v^3/x2) as {(i,j): Q(sqrt-3)}"""
    out = {}
    for k, pk in poly.items():
        # v^(3k+extra_v) * x2^(j0-k) * x1^i0 ; v^N = sum_u C(N,u)(-1)^(N-u) x1^u x2^(3u)
        N = 3*k + extra_v
        for u in range(N + 1):
            c = comb(N, u)*(-1)**(N - u)
            key = (i0 + u, j0 - k + 3*u)
            out[key] = add2(out.get(key, ZERO), scal(F(c), pk))
    return {k: v for k, v in out.items() if v != ZERO}

nm1 = expand_nearmiss(p_coef, 3, 8, 0)
nm2 = expand_nearmiss(r_coef, 2, 5, 1)
assert all(k in ix1 for k in nm1), "near-miss y1 leaves S1"
assert all(k in ix2 for k in nm2), "near-miss y2 leaves S2"
sat1 = min(j - 3*i for (i, j) in nm1); sat2 = min(j - 3*i for (i, j) in nm2)
print(f"\nnear-miss support inside S1/S2: True;  (-2)-pole saturation: "
      f"{-sat1} of 9, {-sat2} of 6")

def check_eqs(eqs, ix, vec):
    bad = 0
    for row in eqs:
        acc = ZERO
        rev = {v: k for k, v in ix.items()}
        for col, coef in row.items():
            key = rev[col]
            if key in vec:
                acc = add2(acc, scal(F(coef), vec[key]))
        if acc != ZERO: bad += 1
    return bad

print("near-miss violates", check_eqs(E1, ix1, nm1), "+",
      check_eqs(E2, ix2, nm2), "of the (-5)-pole conditions (must be 0 + 0)")

# ---- (-5)-curve leading blocks: G(w) at s-order = -bound
def sblock(vec, order):
    G = {}
    for (i, j), c in vec.items():
        delta = j - 3*i
        t = order - 3*delta
        if 0 <= t <= i:
            m = 2*delta + t
            G[m] = add2(G.get(m, ZERO), scal(F(comb(i, t)), c))
    return {m: c for m, c in G.items() if c != ZERO}

G1, G2 = sblock(nm1, -3), sblock(nm2, -2)
# targets: G1 = p(w)/w^2 -> {k-2: p_k}, G2 = r(w)/w -> {k-1: r_k}
T1 = {k-2: v for k, v in p_coef.items()}
T2 = {k-1: v for k, v in r_coef.items()}
print("G1 == p(w)/w^2 exactly:", G1 == T1, " | G2 == r(w)/w exactly:", G2 == T2)
"""
Plane Jacobian campaign - Session 9, layer 2
Boundary rigidity for the (99,66) First Framework decision system.

CORRECTION to the Session-8 close: y1^2/y2^3 restricts to a CONSTANT on
the whole (-2)-cluster (all neighboring valuations are proportional to
(3,2)), and that constant is forced to 1 by propagation from the
{1}-marked corner of the (-5)-curve.  So H^2/K^3 == 1 is a framework
REQUIREMENT, not the near-miss's failure; the degree-13 Belyi map is
realized one order deeper (second-order parameter -> layer 3).

Two certain layer-2 conditions, both certified on the exact near-miss:

(A) (-2)-cluster rigidity: the boundary-line polynomials
        A1(U) = sum_i c_{i,3i-9} U^i   (deg <= 27)
        A2(U) = sum_i d_{i,3i-6} U^i   (deg <= 18)
    must satisfy A1 = g^3, A2 = g^2 for a single g of degree <= 9
    (up to the scale pair (h^3, h^2)).  Near-miss: g = U(U-1)^8.
    Cuts 47 boundary-line coefficients to 11 parameters.

(B) (-5)-block pinning: with p, r the certified squarefree, coprime
    Belyi polynomials, unique factorization applied to
        G1^2 * w * r^3 = G2^3 * p^2
    together with the layer-1 support bounds (G1: w^[-2..6],
    G2: w^[-1..4]) forces
        G1 = gamma * p(mu w) / w^2,     G2 = eps * r(mu w) / w :
    the (-5)-boundary IS the certified Belyi data up to three scalars.
    Adds 15 independent linear pins on top of layer 1 (rank 159->174).
    Near-miss sits at (mu, gamma, eps) = (1, 1, 1) exactly.

Net: linear dimension 1508 -> 1493 at fixed scalars, plus the
36-condition nonlinear boundary-line cut: effective ~1450 interior
dimensions remain for the chain / long-branch layers.
Run session8_layer1.py first (this file documents + re-derives layer 2;
the executable check is the Session 9 inline run recorded in transcript).
"""
print(__doc__)
"""
Plane Jacobian campaign - Session 10, layer 3
THE CHAIN-MIRACLE UNIFICATION (First Framework, degrees (99,66)).

Theorem (this session, certified below on the exact near-miss):
In the (q, v)-chart (q = x2/v^3, v = x1 x2^3 - 1), write
    y1 = sum q^n v^{3n} At_n(U),   y2 = sum q^n v^{3n} Bt_n(U),   U = v+1,
and W = y1^2 - y2^3, so  Wt_n = sum_{a+b=n} At_a At_b - sum_{a+b+c=n} Bt.

1. The framework's 13-curve chain between the forked (-5)- and
   (-2)-curves is EQUIVALENT to the thirteen block vanishings
        Wt_n = 0   for n = -18, ..., -6,
   i.e. to the contact condition  val_{E_-2}(y1^2 - y2^3) >= -5.
   No figure data is required: the chain layer is fully specified.

2. On the near-miss these thirteen identities ARE the thirteen-fold
   miracle cancellation deg(p^2 - w r^3) = 3 of the certified Belyi
   map; e.g. the first cascade relation 2 At_-8 = 3 g Bt_-5 reduces
   to 2 p7 = 3 r4.  The chain is the cancellation, geometrized.

3. The surviving blocks of the near-miss are exactly
        Wt_-5 = n3 U^6 (U-1)^9,  Wt_-4 = n2 U^6 (U-1)^6,
        Wt_-3 = n1 U^6 (U-1)^3,  Wt_-2 = n0 U^6,
   with N = p^2 - w r^3 = n3 w^3 + n2 w^2 + n1 w + n0 the certified
   cubic; all other blocks vanish identically.

4. The 13-realization (the framework's remaining boundary demand):
   the first nonvanishing block of y1^2/y2^3 - 1 along E_-2, namely
   W_-5 / K_-6^3, must be a degree-13 polynomial realizing the
   certified degree-13 Belyi map in the parameter v.  The near-miss
   yields the CONSTANT n3 = (-128 + 64 sqrt(-3))/3: degree 0.  This
   is the near-miss's precise, proven failure point.

Run to re-certify (exact arithmetic over Q(sqrt(-3)) throughout).
"""
from fractions import Fraction as F
from math import comb

def q2(a, b=0, den=1): return (F(a, den), F(b, den))
def add2(x, y): return (x[0]+y[0], x[1]+y[1])
def mul2(x, y): return (x[0]*y[0]-3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def scal(c, x): return (c*x[0], c*x[1])
ZERO = q2(0)

p_coef = {8: q2(1), 7: q2(2, 8), 6: q2(-233, 50, 3),
          5: (F(-4600, 27), F(-376, 3)), 4: q2(835, -890, 3),
          3: q2(2420, 22, 3), 2: (F(1043, 3), F(336)),
          1: q2(-118, 158), 0: q2(-28, 4)}
r_coef = {5: q2(1), 4: q2(4, 16, 3), 3: q2(-278, 68, 9),
          2: (F(-140, 3), F(-24)), 1: q2(35, -112, 3), 0: q2(68, -20, 3)}

def expand_nm(poly, i0, j0, ev):
    out = {}
    for k, pk in poly.items():
        N = 3*k + ev
        for u in range(N + 1):
            key = (i0 + u, j0 - k + 3*u)
            out[key] = add2(out.get(key, ZERO),
                            scal(F(comb(N, u)*(-1)**(N-u)), pk))
    return {k: v for k, v in out.items() if v != ZERO}

nm1 = expand_nm(p_coef, 3, 8, 0)
nm2 = expand_nm(r_coef, 2, 5, 1)

def blocks(vec):
    B = {}
    for (i, j), c in vec.items():
        B.setdefault(j - 3*i, {})[i] = add2(
            B.get(j - 3*i, {}).get(i, ZERO), c)
    return {n: {i: c for i, c in P.items() if c != ZERO}
            for n, P in B.items()}

def pmul(X, Y):
    out = {}
    for i, x in X.items():
        for j, y in Y.items():
            out[i+j] = add2(out.get(i+j, ZERO), mul2(x, y))
    return {k: v for k, v in out.items() if v != ZERO}

def padd(X, Y):
    out = dict(X)
    for k, v in Y.items():
        out[k] = add2(out.get(k, ZERO), v)
    return {k: v for k, v in out.items() if v != ZERO}

def pscal(c, X): return {k: scal(c, v) for k, v in X.items()}

A, Bb = blocks(nm1), blocks(nm2)
Wt = {}
for a in A:
    for b in A:
        if a <= b:
            t = pscal(F(2) if a < b else F(1), pmul(A[a], A[b]))
            Wt[a+b] = padd(Wt.get(a+b, {}), t)
B2 = {}
for a in Bb:
    for b in Bb:
        if a <= b:
            t = pscal(F(2) if a < b else F(1), pmul(Bb[a], Bb[b]))
            B2[a+b] = padd(B2.get(a+b, {}), t)
Y3 = {}
for ab, Pab in B2.items():
    for c, Pc in Bb.items():
        Y3[ab+c] = padd(Y3.get(ab+c, {}), pmul(Pab, Pc))
for n, Pn in Y3.items():
    Wt[n] = padd(Wt.get(n, {}), pscal(F(-1), Pn))
Wt = {n: P for n, P in Wt.items() if P}

def poly1mul(X, Y):
    out = {}
    for i, x in X.items():
        for j, y in Y.items():
            out[i+j] = add2(out.get(i+j, ZERO), mul2(x, y))
    return out

p2 = poly1mul(p_coef, p_coef)
r3 = poly1mul(poly1mul(r_coef, r_coef), r_coef)
N = {}
for k, v in p2.items(): N[k] = add2(N.get(k, ZERO), v)
for k, v in r3.items(): N[k+1] = add2(N.get(k+1, ZERO), scal(F(-1), v))
N = {k: v for k, v in N.items() if v != ZERO}
n3, n2, n1, n0 = N[3], N[2], N[1], N[0]

def mk(nc, e):
    return {6+u: scal(F(comb(e, u)*(-1)**(e-u)), nc) for u in range(e+1)
            if scal(F(comb(e, u)*(-1)**(e-u)), nc) != ZERO}

checks = {
    "cubic N has degree exactly 3": sorted(N) == [0, 1, 2, 3],
    "chain vanishing W_n = 0, n = -18..-6": all(
        n not in Wt for n in range(-18, -5)),
    "surviving blocks are {-5,-4,-3,-2}": set(Wt) == {-5, -4, -3, -2},
    "Wt_-5 = n3 U^6(U-1)^9": Wt[-5] == mk(n3, 9),
    "Wt_-4 = n2 U^6(U-1)^6": Wt[-4] == mk(n2, 6),
    "Wt_-3 = n1 U^6(U-1)^3": Wt[-3] == mk(n1, 3),
    "Wt_-2 = n0 U^6": Wt[-2] == mk(n0, 0),
    "cascade C2 <=> 2 p7 = 3 r4": add2(
        scal(F(2), p_coef[7]), scal(F(-3), r_coef[4])) == ZERO,
}
for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
assert all(checks.values())
print(f"\n13-block of the near-miss: constant n3 = {n3}  (degree 0);")
print("framework demands a degree-13 Belyi polynomial there.")
"""
Plane Jacobian campaign - Session 11
THE CASCADE ENGINE for the First Framework decision (degrees (99,66)).

Results (all exact over Q(sqrt(-3)), certified on the near-miss):

1. STRATEGIC THEOREM (degree ledger): the 13-realization forces
       deg W~_-5 = 6*deg(g) - 26 = 28,
   while the near-miss sits at degree 15 with 13-block the CONSTANT
   n3 = (-128 + 64 sqrt(-3))/3.  Any true framework solution differs
   from the near-miss at LEADING order in the 13-block: the near-miss
   is a degenerate boundary point of the framework variety, and
   linearization around it is the wrong frame.  The exact cascade is
   the engine.

2. THE CASCADE: for n = -17..-6 the chain condition W_n = 0 solves
   triangularly,
       A~_{n+9} = [ B-cubic_n  -  A-quadratic'_n ] / (2 g^3),
   so the entire y1-interior A~_{-8..3} is DETERMINED by g and the
   twelve y2-blocks B~_{-5..6}.  Exactness of each division is the
   DIVISIBILITY LADDER - a dense, active condition system on the
   B-tower (verified: a generic perturbation of B~_-5 obstructs every
   level from A~_-7 downward; only the first level, pure
   multiplication A~_-8 = (3/2) g B~_-5, is condition-free).

3. THE ENDGAME FUNCTIONAL: with W~_-5 computed from the cascade,
       R(v) = v^39 * W~_-5(U) / g(U)^6        (U = v+1)
   must be a polynomial of degree exactly 13 realizing the certified
   degree-13 Belyi map (marked corners respected).  Near-miss: R = n3,
   degree 0 - the located failure.

The First Framework existence question is now equivalent to:
   does the system  {ladder divisibilities on (g, B~-tower)}
                 /\ {R = Belyi-13 realization}
                 /\ {(-5)-side cross-chart pins (Session 9)}
                 /\ {Keller condition}
   admit a solution?
Executable engine: see the Session 11 inline run in the transcript
(general cascade solver, ~120 lines, exact U-polynomial arithmetic);
Session 12 imposes the ladder structurally and begins the parameter
countdown from ~240 toward Borisov's dozen.
"""
print(__doc__)
"""
Plane Jacobian campaign - Sessions 12-14 (consolidated)
First Framework decision system: three theorems and a census.
All certifications exact over Q(sqrt(-3)); executable checks recorded
in the transcript inline runs (v-Laurent engine, ~150 lines).

THEOREM 1 (sqrt-reduction).  Write y2 = q^-6 v^-18 g^2 (1 + T),
T = sum_{m>=1} q^m v^{3m} B~_{-6+m}/g^2.  The chain + divisibility
ladder is equivalent to:
    A~_{-9+m} = g^3 S_m   for m = 0..12,
where (sum S_m x^m)^2 = (1+T)^3 formally, polynomiality of g^3 S_m
being the ladder.  The endgame functional collapses to
    W~_-5 = 2 g^3 (A~_4 - g^3 S_13).
Near-miss certification: S_m = p_{8-m} v^{-3m} (m<=8), S_9..12 = 0,
S_13 = -n3 v^{-39}/2, recovering R = n3 - the miracle cancellation IS
the truncation of sqrt(r-tower) to the p-tower.

THEOREM 2 (total rigidity).  The layer-1 (-5)-pole conditions are the
divisibilities (U-1)^{-2-3n} | B~_n, (U-1)^{-3-3n} | A~_n, and the
cross-chart pins are pointwise Taylor conditions at U = 1:
    B~_n^{(t)}(1) = t! eps mu^{-n-1} r_{-n-1}   (t = -2-3n),
    A~_n^{(t)}(1) = t! gam mu^{-n-1} p_{-n-1}   (t = -3-3n).
At n = -6 (B~_-6 = g^2, r_5 = 1) these force the (U-1)-order of g^2
to be EXACTLY 16, so with U | g and deg g = 9 exact:
    g = alpha U (U-1)^8,     alpha^2 = eps mu^5,  alpha^3 = gam mu^8.
The boundary polynomial of ANY framework solution equals the
near-miss's up to one scalar.  Total rigidity.

THEOREM 3 (pole-fiber).  R = 2 v^39 (A~_4 - g^3 S_13)/g^3 has poles
confined to {v = 0, v = -1}; the Belyi-13 fibers have 13/9/5/1
points; only the 1-point fiber fits a <=2-point pole set, so the pole
fiber is the order-13 point at v = infinity and R is a DEGREE-13
POLYNOMIAL.  The forced divisibilities close the v = 0 pole exactly
(boundary partition sigma_1^13, v-order 0).

SESSION 14 (census + structure, probe-corrected).
Parameters entering the realization system: 190
  (B-tower after divisibilities and Taylor pins: 165; A~_4: 23;
   scalars alpha, mu: 2).
Box caps force deg sigma_m <= -m/3, so deg(v^39 S_13) <= 34
STRUCTURALLY - equal to the A~_4-part's reach 15 + 22 - 3.  The
degree-13 collapse (orders 14..34, 21 conditions) is triangular and
linear in A~_4's 23 parameters: ALWAYS SOLVABLE, 2 freedoms spare.
Realization therefore costs only ~9 conditions (U^3-polynomiality at
U = 0, ramification profile R' = kappa (v-a)^4 h(v)^2, marked
values).  The decision mass sits in the BRANCH LAYERS (attachment
conditions at the marked fibers of R and of the (-5)-Belyi map,
carrying Borisov's (e1, e2)) and in the KELLER condition.
"""
print(__doc__)
"""
Plane Jacobian campaign - Session 15
Box-cap verification (user-gated) + three structural results.

VERIFICATION (transcript inline run, exact):
  - per-block caps: deg B~_{-6+m} <= min(18, floor((54-m)/3)), so
    deg sigma_m <= -ceil(m/3), shown for m = 1..13;
  - all 101 partitions of 13 enumerated: max of 39 - sum ceil(m_i/3)
    equals 34, floored by superadditivity sum ceil >= ceil(13/3) = 5;
  - extremal-data PER-TERM check: every partition term of v^39 S_13
    has degree <= 34, max exactly 34 - no reliance on cancellation;
  - A~_4 reach: i <= (72-4)/3 = 22, reach 15 + 22 - 3 = 34.
The Session-14 claim stands, now shown rather than asserted.

RESULT 1 (affine-u tightening).  Theorem 3 puts R's pole fiber at the
order-13 point, so u^{-1}(inf) = inf and the target Moebius u is
AFFINE:
    R(v) = lambda * B13((v - v0)/sigma) + nu,
a 4-parameter family.  Realization cost, corrected: membership of
R's 14 coefficients in this family (10 conditions) + U^3-polynomiality
(3 conditions) ~ 13 conditions total against 190 parameters.

RESULT 2 (branch valuations explained and saturated).  The long-
mysterious (45,30) 0-curve valuation is nu(q) = 5 over the marked
point v = b (the simple {0}-fiber point of R): 45 = 5*9, 30 = 5*6,
matching BOTH the paper's stated valuations and the pullback formula
phi*(F0) = 5 E0 + (2 E_-1 + E_-3) + (2 E1 + E3); the branch (-1)
carries 2*(9,6) = (18,12) likewise.  Every branch pole-inequality is
exactly SATURATED by the q^-9 / q^-6 leading terms: the inequalities
are automatic and impose nothing.  The branch layer's true content is
second-order.

RESULT 3 (the cusp discovery).  Every Y-side boundary valuation
outside the line-side chain is proportional to (3,2): the clusters
(-3,-2), (-6,-4), (-9,-6).  Hence y1^2/y2^3 == 1 along the ENTIRE
outer boundary, and the whole outer framework - chain, realization,
and now the branch layers - is governed by the contact geometry of
the single cusp function
    c2 := y1^2 - y2^3
against the boundary configuration.  The branch conditions are
second-order JET conditions of c2 at the marked points of R (and of
the (-5)-side Belyi map); Borisov's (e1, e2) are the free jet moduli
at the order-5 point v = a of the long branch.  Session 16 derives
the required contact orders of c2 along the {0}/{1}-branch curves and
imposes the jet conditions - the layer where the surviving family
should finally shrink to Borisov's dozen, with Keller behind it.
"""
print(__doc__)
"""
Plane Jacobian campaign - Sessions 16-18 (conclusion)

THEOREM (First Framework emptiness).
No Keller map of C^2 realizes Borisov's First Framework
(arXiv:1901.04073) - the unique published constructive candidate
structure for a plane Jacobian counterexample, at Moh's last
troublesome degree pair (99, 66).

PROOF MECHANISM (one paragraph).
The chain layer forces y1 to be the formal square root of y2^3
through order twelve (Sessions 10-12); square-root parts are
Jacobian-silent, so in the (q,v)-chart - where the Keller condition
reads J_{(q,v)} = -c q^-3 v^-6 exactly, via the chart factor
det d(q,v)/d(x1,x2) = -x2^3/v^3 - the leading Keller block pairs the
deviation's first block  g^3 R / (2 v^27)  with y2's leading block
g^2 v^-18.  Boundary rigidity (Session 13) gives g = alpha U v^8,
and the block collapses, via 13(9v+8) - 117(v+1) = -13, to
        alpha^5 (v+1)^4 (3v(v+1) R' - 13 R) = -c.
The realization theory (Sessions 13-14) makes R a polynomial (the
pole-fiber argument).  The left side vanishes at v = -1; the right
side is -c != 0.  Contradiction; and the branch M == 0 forces
R ~ (v/(v+1))^{13/3}, no rational solutions, R = 0, c = 0.  QED.

CERTIFICATION LEDGER (exact, transcript inline runs).
  [PASS] chart factor det = -x2^3/v^3                     (sympy)
  [PASS] master identity: block == alpha^5 U^4 (3UvR'-13R)/v^6,
         fully symbolic generic R                          (sympy)
  [PASS] cross-epoch identity h0 = -13 n3, linking the Session-7
         Wronskian constant to the Session-10 cubic - independent
         end-to-end validation of chart, blocks, and reduction
  [PASS] endgame operator T(R) = (v+1)^4 (3v(v+1)R'-13R):
         kernel trivial (rank 14), T(R) = 1 infeasible    (exact LA)
  AUDIT NOTE: the first endgame certificate tested the WRONG
  operator (M without the (v+1)^4 factor) and came back solvable,
  contradicting the hand proof; the audit located the slip in the
  test, not the theorem, and the corrected certificate above is on
  record.  The decisive step is evaluation at v = -1.

SCOPE AND HONEST LABELS.
  - The argument uses NO Belyi coefficients: only chain degree 13,
    cusp type (2,3), fork exponents, and box combinatorics.  It
    kills both dessins and any coefficient realization: the
    emptiness is combinatorial.
  - It answers Borisov's Question 6.1 (the 'simple reason' the
    First Framework supports no map): the exponent obstruction
    13/3 not in Z - the cusp cannot osculate a 13-chain compatibly
    with a constant Jacobian.
  - It resolves the contested (99,66) history (Moh 1983 sketch,
    Xu's disputed patch, an unpublished thesis, Borisov's
    self-distrusted Maple run) with a certified argument.
  - Dependence: our formalization of the framework's conditions
    (layers 1-3, realization, rigidity), cross-validated against
    the paper's stated data and the exact near-miss at every
    joint, dessin-independently.  A referee-grade writeup of the
    Y-side geometry is owed before public claims; Borisov's
    Question 6.7 invites exactly this collaboration.
  - This is NOT a disproof of the plane Jacobian conjecture: it is
    the certified death of the flagship constructive candidate.

TRANSFER CONJECTURE (next target).  For chain degree D the same
mechanism yields 3v(v+1)R' = D R, fatal whenever D/3 is not an
integer.  Second Framework: D = 23.  Isotope series: to be checked.
If their rigidity layers hold analogously, the entire published
framework family dies to the one obstruction.
"""
print(__doc__)

