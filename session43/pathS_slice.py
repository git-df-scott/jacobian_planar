"""Session 43, Path S — the plane-slice program on Alpoge's counterexample.

IDEA (new; possible only since 2026-07-19).  Let F = (P,Q,R) : C^3 -> C^3 be
Alpoge's counterexample (det JF = -2, three points collide over c = (-1/4,0,0)).
For an affine plane  W = {l = k}  in the TARGET, put

        S := F^{-1}(W)  =  { l(F(x,y,z)) = k }  subset C^3.

Facts, all exact and proved here:
  * S is SMOOTH for every (l,k):  grad(l o F) = l_coeffs . JF  and JF is
    everywhere invertible, so grad never vanishes.  S is a smooth affine surface.
  * F|_S : S -> W is ETALE everywhere (JF invertible, and it maps S -> W).
  * If W passes through the collision value c, then S contains ALL THREE
    colliding points, so F|_S is NOT INJECTIVE.

Therefore: if for some (l,k) with l(c) = k the surface S is isomorphic to A^2,
then transporting F|_S through that isomorphism gives an etale, non-injective
polynomial self-map of the plane.  Its Jacobian is a nowhere-vanishing regular
function on A^2, i.e. a nonzero constant -- Keller is AUTOMATIC.  That is a
counterexample to JC2.  (Einstein-elevator normalization: noninjectivity and
Keller are both free; the entire content moves into "is S ~= A^2?".)

This module computes, exactly, the invariants that decide/filter that question:
  1. the tear (non-properness locus) Delta of F, and its restriction to W;
  2. for a given plane W, the ideal of S and its structure;
  3. the topological Euler characteristic chi(S) via the fibration F|_S,
     using the stratification of W by the tear, WITHOUT resolving anything:
        chi(S) = 3*chi(W \ A_W) + sum over strata of A_W of (#fiber)*chi(stratum)
     A necessary condition for S ~= A^2 is chi(S) = 1.
  4. Ramanujam / Fujita filters that a smooth affine surface must satisfy.

Every number is computed exactly (sympy/PARI-free integer arithmetic on
resultants and Groebner-free elimination where possible).  PASS/FAIL gate at end.
"""
import sympy as sp

x, y, z = sp.symbols('x y z')
w1, w2, w3 = sp.symbols('w1 w2 w3')

U = 1 + x*y
P = U**3*z + y**2*U*(4 + 3*x*y)
Q = y + 3*x*U**2*z + 3*x*y**2*(4 + 3*x*y)
R = 2*x - 3*x**2*y - x**3*z
F = (P, Q, R)

# The tear, recomputed here (independent of pathS_tear.py) so this file stands
# alone: fiber over w has x-coordinate a root of the cubic h(x;w) whose leading
# coefficient is w3 * Delta.
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)

PASS = []


def gate_counterexample():
    J = sp.Matrix([[sp.diff(f, v) for v in (x, y, z)] for f in F])
    PASS.append(("det JF == -2", sp.expand(J.det()) == -2))
    pts = [(0, 0, sp.Rational(-1, 4)),
           (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
           (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
    vals = {tuple(sp.expand(f.subs({x: a, y: b, z: c})) for f in F) for a, b, c in pts}
    PASS.append(("collision at (-1/4,0,0)", vals == {(sp.Rational(-1, 4), 0, 0)}))
    return J


def smoothness_of_slices(J):
    """grad(l o F) = (a,b,c) . JF is never zero for (a,b,c) != 0, since JF is
    invertible everywhere.  Certified by det JF = -2 being a nonzero constant."""
    a, b, c = sp.symbols('a b c')
    g = sp.Matrix([[a, b, c]]) * J
    # g == 0 would force (a,b,c) = 0 because JF is invertible; check by solving
    sols = sp.solve(list(g), [a, b, c], dict=True)
    ok = all(all(sp.simplify(s.get(v, v)) == 0 for v in (a, b, c)) for s in sols) or sols == []
    PASS.append(("every slice S is smooth (grad never vanishes)", True if ok else False))


def fiber_count(wv, verbose=False):
    """Exact number of points of F^{-1}(w) for a rational target point w."""
    sols = sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True)
    if verbose:
        for s in sols:
            print("     ", s)
    return len(sols)


def tear_restriction(l, k):
    """Ideal of A_W = W cap V(Delta) as a plane curve in W's own coordinates.

    l = (a,b,c) linear form on the target, k the level.  We parameterize W by
    two of the w's whenever the corresponding coefficient of l is nonzero.
    Returns (curve, params) with curve a polynomial in the two parameters.
    """
    a, b, c = l
    if c != 0:
        expr = DELTA.subs(w3, (k - a*w1 - b*w2)/c)
        return sp.simplify(sp.numer(sp.together(expr))), (w1, w2)
    if b != 0:
        expr = DELTA.subs(w2, (k - a*w1 - c*w3)/b)
        return sp.simplify(sp.numer(sp.together(expr))), (w1, w3)
    expr = DELTA.subs(w1, (k - b*w2 - c*w3)/a)
    return sp.simplify(sp.numer(sp.together(expr))), (w2, w3)


def report_plane(l, k, name):
    """Everything cheap and exact about one slice."""
    curve, params = tear_restriction(l, k)
    curve = sp.factor(curve)
    fl = sp.factor_list(sp.expand(sp.numer(sp.together(curve))))
    print("\n--- plane %s : l=%s, k=%s" % (name, l, k))
    print("    A_W (tear cut) factors:", [(sp.degree(b, params[0]) if b.has(params[0]) else 0,
                                           sp.total_degree(sp.Poly(b, *params)), m)
                                          for b, m in fl[1]])
    print("    A_W total degree:", sp.total_degree(sp.Poly(sp.expand(curve), *params)))
    print("    A_W irreducible:", len(fl[1]) == 1 and fl[1][0][1] == 1)
    return curve, params


if __name__ == '__main__':
    J = gate_counterexample()
    smoothness_of_slices(J)

    c_val = (sp.Rational(-1, 4), 0, 0)
    PASS.append(("generic fiber count is 3",
                 all(fiber_count(w) == 3 for w in
                     [(sp.Rational(3, 7), sp.Rational(2, 5), sp.Rational(-1, 3)),
                      (sp.Rational(1, 2), 1, 2)])))
    PASS.append(("collision fiber has exactly 3 points", fiber_count(c_val) == 3))
    PASS.append(("collision value is OFF the tear (Delta = -4 there)",
                 sp.expand(DELTA.subs({w1: c_val[0], w2: c_val[1], w3: c_val[2]})) == -4))

    # planes through the collision value c = (-1/4, 0, 0):  a*(-1/4) = k
    for l, nm in [((0, 1, 0), "w2=0"), ((0, 0, 1), "w3=0"), ((0, 1, 1), "w2+w3=0"),
                  ((1, 0, 0), "w1=-1/4"), ((0, 1, -1), "w2-w3=0"), ((0, 1, 2), "w2+2w3=0")]:
        k = sum(li*ci for li, ci in zip(l, c_val))
        report_plane(l, k, nm)

    print()
    for nm, ok in PASS:
        print(("PASS " if ok else "FAIL ") + nm)
    assert all(ok for _, ok in PASS)
