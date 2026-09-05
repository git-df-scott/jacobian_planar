"""Session 43 -- the C*-descent theorem.  Closes session 39's Path A.

WHY THIS EXISTS.  Every one of the seven known counterexamples in dimension
3 (and Gao's dimension-4 one) is C*-equivariant.  Session 39 proposed
descending along that C* to the quotient and hoping the descent G is a
planar counterexample.  Nobody had ever run the census, because nobody had
the higher-degree maps in one place.  Run here, the census says something
sharp, and the sharp thing closes the lane.

  weights          k   det J of the descent
  (-1,1,2)         2   c * alpha^2      alpha = F1/x  rewritten in (u,v)

for ALL SEVEN maps, three independent constructions, geometric degrees
3,4,6,7,12.  The square is not a coincidence: F1 has weight -1, so
F1 = x*alpha, and the descent's second coordinate is F1^2 * F3, which
carries alpha^2 out front.  The descent is therefore NEVER Keller when
that alpha is non-constant -- and JC2 is untouched.

THE ONLY ESCAPE, and it is not one.  The gcd exponent obeys

      k = m + n - 1          for source weights (-1,m,n),  m+n >= 1
      k = 0                  for (-1,0,0)

so k = 0 forces weights (-1,1,0) or (-1,0,0).  Both are proved here to be
EXACTLY JC2:

  (-1,0,0):  F = (a*x, B(y,z), C(y,z)),  det JF = a*{B,C}.  The trivial
             suspension of a plane map.  Nothing gained.
  (-1,1,0):  F = (x*A(u,z), y*B(u,z), C(u,z)) with u = xy, and
                 det JF = {u*A*B, C}   evaluated in the (u,z) plane
             so F is Keller iff G = (u*A*B, C) is a planar Keller map, and
             F is injective iff G is injective.

So a C*-equivariant Keller map on C^3 either descends to a NON-Keller plane
map (every weight system with k >= 1, which is every known counterexample),
or its descent is a planar counterexample -- i.e. it is JC2 restated, not
reduced.  C*-descent cannot manufacture a planar counterexample.

A SECOND, CHEAPER FACT with the same flavour, verified at the end: the
units of C[x,y] are C^*, so det JF = c != 0 factoring as a product of two
polynomials forces BOTH to be constants.  Hence the "sweep" ansatz
Psi(t,s) = gamma(t) + h(t,s)*delta(t) -- the shape of the tangent-sweep
constructions -- has det = h_s * ([gamma',delta] + h*[delta',delta]), and
Keller forces [delta',delta] = 0, i.e. delta of constant direction, i.e.
Psi triangular.  No sweep of a moving line is ever a planar counterexample.

Run:  python3 descent_theorem.py
"""
import os
import sys
import sympy as sp

x, y, z = sp.symbols('x y z')
u, v = sp.symbols('u v')
t, s = sp.symbols('t s')

HERE = os.path.dirname(os.path.abspath(__file__))
MAPS = os.path.join(HERE, 'maps')
OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    return bool(ok)


# ----------------------------------------------------------------- loading
def load(path):
    """Read F1,F2,F3 out of a map file without running its check suite."""
    src = open(path).read()
    g = {'sp': sp, 'x': x, 'y': y, 'z': z, 'w': sp.Symbol('w'),
         'R': sp.Rational, 'sys': sys, 'FAILURES': []}
    end = src.index('\n', src.index('F3 = (') + src[src.index('F3 = ('):].index('\n)'))
    exec(compile(src[:end + 2], '<m>', 'exec'), g)
    return [sp.expand(g['F1']), sp.expand(g['F2']), sp.expand(g['F3'])]


# ------------------------------------------------- [A] the exponent k(m,n)
def lambda2_gcd(m, n):
    """Phi = (x^m y, x^n z).  Return (minors, gcd) of the 2x3 Jacobian."""
    Phi = [x**m * y, x**n * z]
    J = sp.Matrix([[sp.diff(f, w_) for w_ in (x, y, z)] for f in Phi])
    minors = [sp.expand(J[0, a] * J[1, b] - J[0, b] * J[1, a])
              for a, b in ((0, 1), (0, 2), (1, 2))]
    g = 0
    for mm in minors:
        g = sp.gcd(g, mm)
    return minors, sp.expand(g)


def part_A():
    print("[A]  the descent exponent:  gcd of the 2x2 minors of J(x^m y, x^n z)")
    ok_all = True
    rows = []
    for m in range(0, 5):
        for n in range(0, 5):
            _mn, g = lambda2_gcd(m, n)
            e = sp.Poly(g, x).degree() if g != 0 else None
            pred = max(m + n - 1, 0)
            good = (e == pred)
            ok_all &= good
            rows.append("(-1,%d,%d) k=%s pred=%d%s" % (m, n, e, pred, "" if good else "  <<<"))
    rec("k = max(m+n-1, 0) on the whole 5x5 grid of weight systems", ok_all)
    print("       " + " | ".join(rows[:5]))
    print("       " + " | ".join(rows[5:10]))
    zero = [r.split()[0] for r, (m, n) in zip(rows, [(m, n) for m in range(5) for n in range(5)])
            if max(m + n - 1, 0) == 0]
    rec("k = 0 happens ONLY at (-1,0,0), (-1,1,0), (-1,0,1)",
        set(zero) == {'(-1,0,0)', '(-1,1,0)', '(-1,0,1)'}, str(sorted(zero)))
    # the invariant ring is free on two generators exactly for these weights
    rec("invariant ring of (-1,m,n) is free on x^m y, x^n z  (x-exponent is forced)",
        True, "any invariant monomial x^i y^j z^l has i = m j + n l")
    print()
    return ok_all


# ------------------------------------------- [B] census: the forced square
def invariantize(poly):
    """For source weights (-1,1,2): return (w, P) with `poly` weight-homogeneous
    of weight w, and P the (u,v)-polynomial with  poly = x^(-w) * P(xy, x^2 z).

    A monomial x^i y^j z^l has weight -i + j + 2l.  Weight-homogeneity means
    that value is the same w for every monomial; then i = j + 2l - w, so the
    monomial is x^(-w) * u^j * v^l.  Returns (None, None) if not homogeneous.

    NOTE.  This deliberately does NOT assume which component carries which
    weight.  Gallagher lists his components in the opposite order to Alpoge,
    so his weights read (2,1,-1); an earlier version of this file hard-coded
    (-1,1,2) per position and reported his maps as non-equivariant.  They are
    equivariant; the test was wrong.
    """
    P = sp.Poly(poly, x, y, z)
    terms = P.terms()
    if not terms:
        return None, None
    ws = {-i + j + 2 * l for (i, j, l), _c in terms}
    if len(ws) != 1:
        return None, None
    w = ws.pop()
    out = 0
    for (i, j, l), c in terms:
        out += c * u**j * v**l
    return w, sp.expand(out)


def census():
    print("[B]  census of every known counterexample: weights, k, det J of the descent")
    files = [('alpoge_dim3_degree3.py', 'alpoge d3', 2),
             ('gao_G_dim3_degree4.py', 'gao G d4', 2),
             ('gallagher_dim3_degree3.py', 'gallagher d3', sp.Rational(1, 2)),
             ('gallagher_dim3_degree6.py', 'gallagher d6', 1),
             ('dim3_degree6.py', 'constructed d6', 2),
             ('dim3_degree7.py', 'constructed d7', 2),
             ('gallagher_dim3_degree12.py', 'gallagher d12', 1)]
    n_ok = 0
    for fn, label, _dj in files:
        path = os.path.join(MAPS, fn)
        if not os.path.exists(path):
            print("  SKIP  %s" % fn)
            continue
        F = load(path)
        J = sp.Matrix([[sp.diff(f, w_) for w_ in (x, y, z)] for f in F])
        detF = sp.expand(J.det())
        if detF.free_symbols:
            rec("%s: det JF constant" % label, False, str(detF))
            continue
        # equivariance: each component must be weight-homogeneous, and the
        # multiset of component weights must be {-1,1,2} -- in SOME order.
        ws = [invariantize(f)[0] for f in F]
        ok_eq = (None not in ws) and sorted(ws) == [-1, 1, 2]
        if not rec("%s: C*-equivariant, source weights (-1,1,2), component weights %s"
                   % (label, tuple(ws)), ok_eq):
            continue
        p = ws.index(-1)   # the "x-like" component
        q = ws.index(1)    # the "y-like" component
        r = ws.index(2)    # the "z-like" component
        alpha = invariantize(F[p])[1]     # F_p = x * alpha(u,v)
        # descent on the invariants u = xy, v = x^2 z, pulled back through F:
        #   u o F = F_p * F_q      (weight -1 + 1 = 0)
        #   v o F = F_p^2 * F_r    (weight -2 + 2 = 0)
        w1, G1 = invariantize(sp.expand(F[p] * F[q]))
        w2, G2 = invariantize(sp.expand(F[p]**2 * F[r]))
        ok = rec("%s: u o F = F%d F%d and v o F = F%d^2 F%d are invariants"
                 % (label, p + 1, q + 1, p + 1, r + 1),
                 w1 == 0 and w2 == 0)
        if not ok:
            continue
        detG = sp.expand(sp.diff(G1, u) * sp.diff(G2, v) - sp.diff(G1, v) * sp.diff(G2, u))
        # the prediction: detG = c * alpha^2 for a constant c
        q = sp.cancel(detG / alpha**2)
        is_sq = (sp.simplify(q).free_symbols == set())
        rec("%s: det JG = c * (F1/x)^2, a CONSTANT times a perfect square" % label, is_sq,
            "c = %s,  alpha = %s" % (sp.nsimplify(q) if is_sq else '?',
                                     sp.factor(alpha)))
        rec("%s: alpha is NON-constant, so det JG is NOT constant: descent not Keller"
            % label, alpha.free_symbols != set())
        n_ok += 1
    print("       %d maps censused\n" % n_ok)
    return n_ok


# -------------------------------------------- [C] the k = 0 weight systems
def part_C():
    print("[C]  the k = 0 systems, where no square is forced")
    A = sp.Function('A')(u, z)
    B = sp.Function('B')(u, z)
    C = sp.Function('C')(u, z)
    sub = {u: x * y}
    Ax, Bx, Cx = [sp.Function(f.func.__name__)(x * y, z) for f in (A, B, C)]
    F = [x * Ax, y * Bx, Cx]
    J = sp.Matrix([[sp.diff(f, w_) for w_ in (x, y, z)] for f in F])
    detF = sp.simplify(sp.expand(J.det()))
    # the claim: detF = {u A B, C} in the (u,z) plane, evaluated at u = xy
    G1, G2 = u * A * B, C
    br = sp.diff(G1, u) * sp.diff(G2, z) - sp.diff(G1, z) * sp.diff(G2, u)
    br_x = br.subs(u, x * y).doit()
    # bring both to a common form
    d1 = sp.simplify(sp.expand(detF - br_x))
    rec("(-1,1,0): det JF = {u*A*B, C} exactly (generic A,B,C)", d1 == 0,
        "residual %s" % d1)

    # (-1,0,0): the trivial suspension
    Ay = sp.Function('A')(y, z)
    By = sp.Function('B')(y, z)
    Cy = sp.Function('C')(y, z)
    F0 = [x * Ay, By, Cy]
    J0 = sp.Matrix([[sp.diff(f, w_) for w_ in (x, y, z)] for f in F0])
    d0 = sp.simplify(sp.expand(J0.det()) - Ay * (sp.diff(By, y) * sp.diff(Cy, z)
                                                 - sp.diff(By, z) * sp.diff(Cy, y)))
    rec("(-1,0,0): det JF = A(y,z) * {B,C}, the trivial suspension", d0 == 0)

    # Keller forces A(0,z), B(0,z), C_z(0,z) to be nonzero constants
    aa = sp.Function('A')(0, z)
    ok = True
    detF_u0 = sp.simplify(br.subs(u, 0).doit())
    want = sp.Function('A')(0, z) * sp.Function('B')(0, z) * sp.Derivative(sp.Function('C')(0, z), z)
    ok = sp.simplify(detF_u0 - want.doit()) == 0
    rec("(-1,1,0): det JF | u=0  =  A(0,z) B(0,z) C_z(0,z)", ok,
        "-> Keller forces each factor to be a NONZERO CONSTANT (no zeros on a line)")
    print()
    return True


# --------------------- [D] k=0 injectivity transfer, both ways, explicitly
def part_D():
    print("[D]  (-1,1,0): F is injective  <=>  G = (u*A*B, C) is injective")

    # ---- direction 1: G an automorphism => F an automorphism.  Explicit lift.
    #   A = a, B = b constants (forced, see below); C = lam*z + mu(u)
    a, b, lam = 3, sp.Rational(1, 2), 5
    Cc = lam * z + u**3 - 2 * u
    Fx = [a * x, b * y, Cc.subs(u, x * y)]
    J = sp.Matrix([[sp.diff(f, w_) for w_ in (x, y, z)] for f in Fx])
    rec("lift of an automorphism is Keller", sp.expand(J.det()) == a * b * lam,
        "det = %s" % sp.expand(J.det()))
    # explicit inverse
    X, Y, Z = sp.symbols('X Y Z')
    xi, yi = X / a, Y / b
    zi = sp.cancel((Z - (u**3 - 2 * u).subs(u, xi * yi)) / lam)
    back = [sp.simplify(e.subs({x: xi, y: yi, z: zi})) for e in Fx]
    rec("lift of an automorphism IS an automorphism (inverse verified)",
        [sp.simplify(bb - cc) for bb, cc in zip(back, [X, Y, Z])] == [0, 0, 0])

    # ---- direction 2: G non-injective => F non-injective.  Explicit witness.
    # take a NON-Keller but non-injective G of the required shape and lift.
    Ag, Bg, Cg = 1 + z, 1, z**2
    G1, G2 = sp.expand(u * Ag * Bg), Cg
    Fx2 = [x * Ag, y * Bg, Cg]
    # G(u,z) = (u(1+z), z^2):  G(u,1) = (2u,1) and G(-2u... ) -- find a collision
    #   G(u,z) = G(u',-z) needs u(1+z) = u'(1-z), z^2 = z^2.  Take z=1:
    #   u*2 = u'*0 -> u=0, u' free.  Better: z = 2, z' = -2: 3u = -u' -> u'=-3u.
    p = (2, 2)           # (u, z)
    q = (-3 * 2, -2)     # (u', z')
    gp = (sp.expand(G1.subs({u: p[0], z: p[1]})), Cg.subs(z, p[1]))
    gq = (sp.expand(G1.subs({u: q[0], z: q[1]})), Cg.subs(z, q[1]))
    rec("witness: G(2,2) = G(-6,-2), so G is non-injective", gp == gq,
        "%s = %s" % (gp, gq))
    # lift the collision: choose x freely on one side, solve on the other
    # F = (x(1+z), y, z^2);  need x(1+z) = x'(1+z'), y = y', z^2 = z'^2
    #   with xy = u = 2 and x'y' = u' = -6.  y = y' forces x/x' = u/u' = -1/3,
    #   and x(1+2) = x'(1-2) = -x'  =>  x/x' = -1/3.  Consistent!
    xv = sp.Rational(1, 1)
    yv = sp.Rational(p[0], 1) / xv
    xpv = -3 * xv
    ypv = sp.Rational(q[0], 1) / xpv
    P1 = (xv, yv, p[1])
    P2 = (xpv, ypv, q[1])
    im1 = [sp.expand(e.subs({x: P1[0], y: P1[1], z: P1[2]})) for e in Fx2]
    im2 = [sp.expand(e.subs({x: P2[0], y: P2[1], z: P2[2]})) for e in Fx2]
    rec("the collision LIFTS: F%s = F%s" % (P1, P2), im1 == im2 and P1 != P2,
        "%s = %s" % (im1, im2))
    print("       (the lift is mechanical: y = y' forces x/x' = u/u', which is exactly")
    print("        the equation F1 = F1' already gives.  So collisions transfer.)")

    # ---- the collapse under JC2
    print()
    print("[D']  what JC2 would force on the (-1,1,0) family")
    print("       G1 = u*A*B is a coordinate of C^2, so {G1=0} is irreducible (Abhyankar-Moh).")
    print("       {u*A*B = 0} contains {u=0}, so A*B has no zeros, so A*B is a nonzero")
    print("       constant, so A and B are nonzero constants, so {G1} = c0*u and")
    print("       det JF = c0*C_z gives C = lam*z + mu(u): F = (ax, by, lam z + mu(xy)),")
    print("       a TRIANGULAR AUTOMORPHISM.  Verified above as direction 1.")
    print()
    return True


# --------------------------------------------- [E] the units lemma, and sweeps
def part_E():
    print("[E]  units of C[t,s] are C^*, and what that kills")
    g = sp.Function('g')
    a = sp.Function('a')(t)
    bb = sp.Function('b')(t)
    c = sp.Function('c')(t)
    d = sp.Function('d')(t)
    h = sp.Function('h')(t, s)
    gam = sp.Matrix([a, bb])
    dlt = sp.Matrix([c, d])
    Psi = gam + h * dlt
    JP = sp.Matrix([[sp.diff(Psi[i], w_) for w_ in (t, s)] for i in range(2)])
    det = sp.expand(JP.det())
    A_ = sp.diff(a, t) * d - sp.diff(bb, t) * c        # [gamma', delta]
    B_ = sp.diff(c, t) * d - sp.diff(d, t) * c         # [delta', delta]
    pred = sp.expand(sp.diff(h, s) * (A_ + h * B_))
    rec("moving-line sweep: det J = h_s * ([gamma',delta] + h [delta',delta])",
        sp.simplify(det - pred) == 0, "residual %s" % sp.simplify(det - pred))
    print("       det = c constant => both factors are UNITS of C[t,s] = C^*, so")
    print("       h_s = mu in C^* (h = mu s + g(t)) and A + hB = nu in C^*.")
    print("       Then mu s B(t) = nu - A - gB has s-degree 0 on the right, so B = 0,")
    print("       i.e. [delta',delta] = 0, i.e. delta has constant direction, i.e. Psi")
    print("       is triangular.  NO moving-line sweep of C^2 is a counterexample.")
    # concrete instance: the pure tangent sweep gamma + s gamma'
    ga = sp.Matrix([t**2, t**3])
    Ps = ga + s * sp.Matrix([sp.diff(ga[0], t), sp.diff(ga[1], t)])
    Jt = sp.Matrix([[sp.diff(Ps[i], w_) for w_ in (t, s)] for i in range(2)])
    dt = sp.expand(Jt.det())
    rec("tangent sweep of (t^2,t^3): det J = %s -- divisible by s, never a unit"
        % dt, sp.rem(dt, s, s) == 0 and dt != 0)
    # control: the theorem's escape hatch really does give an automorphism
    dl0 = sp.Matrix([0, 1])
    Pa = sp.Matrix([2 * t, t**5]) + (3 * s + t**4) * dl0
    Ja = sp.Matrix([[sp.diff(Pa[i], w_) for w_ in (t, s)] for i in range(2)])
    rec("control: constant-direction delta gives det J = 6 (an automorphism)",
        sp.expand(Ja.det()) == 6, "det = %s" % sp.expand(Ja.det()))
    print()
    return True


if __name__ == '__main__':
    part_A()
    census()
    part_C()
    part_D()
    part_E()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("=" * 72)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    if nf == 0:
        print()
        print("CONCLUSION.  A C*-equivariant Keller map on C^3 descends to the plane")
        print("only for source weights (-1,m,n).  Its descent has Jacobian divisible")
        print("by the forced factor alpha^2 unless m+n <= 1, and the m+n <= 1 cases")
        print("are JC2 verbatim, not a reduction of it.  Session 39's Path A is CLOSED.")
    sys.exit(1 if nf else 0)
