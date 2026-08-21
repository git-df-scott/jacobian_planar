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
