"""
Wave 2, Task 5 - det JF == -2 on the Alpoge map.

This is the one-minute check that everything upstream leans on: the descent
(Path A), the census (Session 38), the sweep separator (Sessions 28-32) and
the whole "the mechanism is unavailable in the plane" claim all start from
the assertion that Alpoge's degree-7 map of C^3 is Keller.

It is verified here three independent ways:
   (1) exact symbolic determinant over Q[x,y,z];
   (2) exact evaluation at random rational points (a determinant that is
       constant must take the same value everywhere);
   (3) reduction mod several primes, so an arithmetic slip in (1) cannot
       survive.

The map, as recorded in the campaign's Session 1 and Session 39 files:

    f1 = (1 + x y)^3 z + y^2 (1 + x y)(4 + 3 x y)
    f2 = y + 3 x (1 + x y)^2 z + 3 x y^2 (4 + 3 x y)
    f3 = 2 x - 3 x^2 y - x^3 z

NEGATIVE CONTROL: a one-character perturbation of the map must NOT have a
constant Jacobian, otherwise the test is not measuring anything.
"""

import random
import sympy as sp

x, y, z = sp.symbols('x y z')
PASS = []


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


f1 = (1 + x * y) ** 3 * z + y ** 2 * (1 + x * y) * (4 + 3 * x * y)
f2 = y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y ** 2 * (4 + 3 * x * y)
f3 = 2 * x - 3 * x ** 2 * y - x ** 3 * z
F = (f1, f2, f3)

print("=" * 74)
print("ALPOGE MAP:  det JF")
print("=" * 74)

J = sp.Matrix([[sp.diff(f, w) for w in (x, y, z)] for f in F])
detJ = sp.expand(J.det())
print(f"    (1) exact symbolic det JF = {detJ}")
check("det JF == -2 exactly (symbolic)", sp.simplify(detJ + 2) == 0)
check("det JF is constant in x", sp.simplify(sp.diff(detJ, x)) == 0)
check("det JF is constant in y", sp.simplify(sp.diff(detJ, y)) == 0)
check("det JF is constant in z", sp.simplify(sp.diff(detJ, z)) == 0)

# (2) exact rational point evaluation
rnd = random.Random(20260819)
pts = [(sp.Rational(rnd.randint(-40, 40), rnd.randint(1, 17)),
        sp.Rational(rnd.randint(-40, 40), rnd.randint(1, 17)),
        sp.Rational(rnd.randint(-40, 40), rnd.randint(1, 17))) for _ in range(25)]
vals = {sp.nsimplify(J.subs({x: a, y: b, z: t}).det()) for (a, b, t) in pts}
print(f"    (2) exact values at 25 random rational points: {vals}")
check("det JF == -2 at 25 independent rational points", vals == {sp.Integer(-2)})

# (3) modular reduction
mods = []
for p in (101, 1009, 10007, 65537, 2 ** 31 - 1):
    Jp = sp.Matrix(3, 3, lambda i, j: sp.Poly(J[i, j], x, y, z, modulus=p).as_expr())
    dp = sp.expand(Jp.det()) % p
    mods.append((p, sp.simplify(dp - (-2) % p) == 0))
print(f"    (3) mod-p reductions agree with -2: {[m[0] for m in mods if m[1]]}")
check("det JF == -2 mod every tested prime", all(ok for _, ok in mods))

# NEGATIVE CONTROL
g3 = 2 * x - 3 * x ** 2 * y - x ** 3 * z + x
Jn = sp.Matrix([[sp.diff(f, w) for w in (x, y, z)] for f in (f1, f2, g3)])
dn = sp.expand(Jn.det())
print(f"    NEGATIVE CONTROL: perturbed f3 -> det J = {sp.factor(dn)}")
check("NEGATIVE CONTROL: perturbed map does NOT have constant Jacobian",
      sp.simplify(sp.diff(dn, x)) != 0 or sp.simplify(sp.diff(dn, y)) != 0
      or sp.simplify(sp.diff(dn, z)) != 0)

# The C*-equivariance the descent leans on, checked here too since it is cheap.
lam = sp.symbols('lam')
sub = {x: lam * x, y: y / lam, z: z / lam ** 2}
for f, w in ((f1, -2), (f2, -1), (f3, 1)):
    d = sp.simplify(sp.expand(f.subs(sub, simultaneous=True) - lam ** w * f))
    check(f"C*-equivariance: component has weight {w}", d == 0)

print()
print("=" * 74)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 74)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w2_alpoge_detjf.py: a check FAILED"
print("    VERDICT: det JF == -2.  The upstream assumption is sound.")
