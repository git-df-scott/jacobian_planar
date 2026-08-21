import sympy as sp

x, y, z, u, v, lam = sp.symbols('x y z u v lam')
PASS = []

# Alpoge's degree-7 counterexample in C^3
f1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
f2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
f3 = 2*x - 3*x**2*y - x**3*z

J = sp.Matrix([[sp.diff(f, w) for w in (x, y, z)] for f in (f1, f2, f3)])
detJ = sp.simplify(sp.expand(J.det()))
PASS.append(("det JF is the constant -2", detJ == -2))

# C*-equivariance: weights (1,-1,-2) on source, (-2,-1,1) on target
sub = {x: lam*x, y: y/lam, z: z/lam**2}
for f, w in ((f1, -2), (f2, -1), (f3, 1)):
    lhs = sp.simplify(sp.expand(f.subs(sub, simultaneous=True) - lam**w * f))
    PASS.append((f"component weight {w}", lhs == 0))

# Invariant rings.  Source: a-b-2c=0  ->  C[xy, x^2 z].
# Target: -2a-b+c=0 ->  C[f1*f3^2, f2*f3].   Both free on two generators.
w1 = sp.expand(f1 * f3**2)
w2 = sp.expand(f2 * f3)

# Rewrite in u = xy, v = x^2 z.  Substitute y -> u/x, z -> v/x^2 and check x cancels.
def to_uv(expr):
    e = sp.simplify(sp.expand(expr.subs({y: u/x, z: v/x**2})))
    e = sp.simplify(sp.cancel(sp.together(e)))
    return sp.expand(sp.simplify(e))

W1 = to_uv(w1)
W2 = to_uv(w2)
PASS.append(("W1 is x-free (descends)", sp.simplify(sp.diff(W1, x)) == 0))
PASS.append(("W2 is x-free (descends)", sp.simplify(sp.diff(W2, x)) == 0))

W1 = sp.expand(W1)
W2 = sp.expand(W2)

print("G_1(u,v) =", sp.factor(W1))
print()
print("G_2(u,v) =", sp.factor(W2))
print()
print("deg G_1 =", sp.Poly(W1, u, v).total_degree(), "  deg G_2 =", sp.Poly(W2, u, v).total_degree())

JG = sp.Matrix([[sp.diff(g, t) for t in (u, v)] for g in (W1, W2)])
detJG = sp.expand(JG.det())
print()
print("det JG =", sp.factor(detJG))
print()
print("det JG is constant? ", sp.simplify(sp.diff(detJG, u)) == 0 and sp.simplify(sp.diff(detJG, v)) == 0)

# Non-injectivity downstairs, inherited from the known collision upstairs.
pts3 = [(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
        (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
pts2 = [(px*py, px**2*pz) for (px, py, pz) in pts3]
print()
print("upstairs collision maps to quotient points:", pts2)
imgs = [(W1.subs({u: a, v: b}), W2.subs({u: a, v: b})) for (a, b) in pts2]
print("images under G:", imgs)
distinct = len(set(pts2))
PASS.append(("quotient points collapse 3 -> 2", distinct == 2))
PASS.append(("G is non-injective on those", len(set(imgs)) == 1 and distinct == 2))

# Where does the Jacobian degenerate?
print()
print("det JG factors:", sp.factor_list(detJG))

for name, ok in PASS:
    print(("PASS " if ok else "FAIL ") + name)
assert all(ok for _, ok in PASS)
