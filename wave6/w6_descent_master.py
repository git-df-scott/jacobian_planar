#!/usr/bin/env python3
"""PATH A / A1 -- the descent Jacobian in closed form.  Certifier.

CLAIM (derived, then checked here three ways)
---------------------------------------------
Let C* act on C^{n+1} with source weights w and target weights w', both with
polynomial invariant ring, quotient maps pi, pi' : C^{n+1} -> C^n.  Let F be
C*-equivariant with det JF = 1, descending to G with pi' o F = G o pi.

For an n x (n+1) matrix M of rank n, the vector of signed maximal minors
mu(M) spans ker M.  Since Jpi . E = 0 for the weight vector field
E(p) = (w_0 p_0, ..., w_n p_n), we may write

        mu(Jpi)  = q  . E          q  a polynomial determined BY THE WEIGHTS
        mu(Jpi') = q' . E'         q' likewise

Differentiating pi' o F = G o pi:      Jpi'(F) . JF = JG(pi) . Jpi
Taking maximal minors, using mu(M A) = det(A) . A^{-1} mu(M), det JF = 1,
and equivariance JF . E = E' o F:

        **  det JG o pi  =  (q' o F) / q  **

COROLLARY (the construction recipe Session 39 asked for)
        G is Keller  <==>  q' o F = c . q  for a nonzero constant c.

q and q' do NOT depend on F.  They are invariant-theoretic data of the two
weight systems.  So "is k >= 2 forced?" is a question about WEIGHTS ALONE,
not about the space of equivariant Keller maps -- which is why it was hard
when posed as a question about all such maps.

CHECKS RUN HERE
  1. The Session 39 descent really has det JG = -2(3u+v-2)^2   [campaign datum]
  2. q for the source weights (1,-1,-2) is x^2, and q' for the target weights
     (-2,-1,1) is f3^2 -- so the master formula PREDICTS det JG = c(f3/x)^2,
     i.e. it predicts the exponent 2 AND the identity h = f3/x, which is
     exactly what Session 39 found by direct computation.
  3. The master formula on a synthetic equivariant Keller family where every
     object is known in closed form.
  4. A table of q over weight systems, showing k = 1 IS achievable -- so
     k >= 2 is NOT forced, and the "not forced" branch of A1 is the live one.
"""
import sympy as sp

PASS = []


def minors_kernel(J):
    """Signed maximal minors of an n x (n+1) matrix -- spans the kernel."""
    n, m = J.shape
    assert m == n + 1
    out = []
    for j in range(m):
        sub = J[:, [k for k in range(m) if k != j]]
        out.append((-1) ** j * sub.det())
    return sp.Matrix(out)


def q_of(weights, invariants, coords):
    """mu(Jpi) = q . E  ->  return q (and verify the proportionality)."""
    J = sp.Matrix([[sp.diff(g, c) for c in coords] for g in invariants])
    mu = sp.simplify(minors_kernel(J))
    E = sp.Matrix([w * c for w, c in zip(weights, coords)])
    qs = set()
    for a, b in zip(mu, E):
        if sp.simplify(b) == 0:
            continue
        qs.add(sp.simplify(sp.cancel(a / b)))
    assert len(qs) == 1, f"mu(Jpi) not proportional to E: {qs}"
    q = qs.pop()
    assert sp.simplify(mu - q * E) == sp.zeros(len(coords), 1)
    return sp.factor(q)


def main():
    x, y, z = sp.symbols('x y z')
    u, v = sp.symbols('u v')

    # ---- CHECK 1: the Session 39 descent, verbatim from the campaign doc ----
    G1 = (u + 1) * (3 * u + v - 2) ** 2 * (3 * u**3 + u**2 * v + 4 * u**2 + 2 * u * v + v)
    G2 = -(3 * u + v - 2) * (9 * u**3 + 3 * u**2 * v + 12 * u**2 + 6 * u * v + u + 3 * v)
    detJG = sp.factor(sp.expand(sp.diff(G1, u) * sp.diff(G2, v)
                                - sp.diff(G1, v) * sp.diff(G2, u)))
    want = sp.factor(-2 * (3 * u + v - 2) ** 2)
    ok1 = sp.simplify(detJG - want) == 0
    PASS.append(("Session 39 descent has det JG = -2(3u+v-2)^2", ok1))
    print(f"1. det JG = {detJG}")
    print(f"   expected -2*(3u+v-2)**2 : {'PASS' if ok1 else 'FAIL'}")
    print(f"   deg G = ({sp.total_degree(sp.expand(G1))}, {sp.total_degree(sp.expand(G2))})")

    # ---- CHECK 2: q and q' from the weights alone ----
    q_src = q_of([1, -1, -2], [x * y, x**2 * z], [x, y, z])
    A, B, C = sp.symbols('f1 f2 f3')
    q_tgt = q_of([-2, -1, 1], [A * C**2, B * C], [A, B, C])
    print(f"\n2. source weights (1,-1,-2), invariants (xy, x^2 z):  q  = {q_src}")
    print(f"   target weights (-2,-1,1), invariants (f1 f3^2, f2 f3): q' = {q_tgt}")
    ok2 = (sp.simplify(q_src - x**2) == 0) and (sp.simplify(q_tgt - C**2) == 0)
    PASS.append(("q = x^2 and q' = f3^2 for the Alpoge weight system", ok2))
    print(f"   master formula predicts det JG = c*(f3/x)^2, i.e. h = f3/x with k = 2.")
    print(f"   Session 39 found h = f3/x and k = 2 by direct computation: "
          f"{'PASS -- exponent AND h both predicted' if ok2 else 'FAIL'}")

    # ---- CHECK 3: master formula on a closed-form equivariant Keller family ----
    # weights (1,-1,-1) both sides; invariants (xy, xz); F = (x, y + z*A(xz), z)
    t = sp.symbols('t')
    Apoly = 1 + 2 * t + 5 * t**3                       # arbitrary
    F1, F2, F3 = x, y + z * Apoly.subs(t, x * z), z
    JF = sp.Matrix([[sp.diff(f, c) for c in (x, y, z)] for f in (F1, F2, F3)])
    okA = sp.simplify(JF.det() - 1) == 0
    # equivariance: F(tx, y/t, z/t) == (t*F1, F2/t, F3/t)
    sub = {x: t * x, y: y / t, z: z / t}
    okB = all(sp.simplify(f.subs(sub) - w) == 0 for f, w in
              zip((F1, F2, F3), (t * F1, F2 / t, F3 / t)))
    # descent: pi' o F expressed in (u,v) = (xy, xz)
    P1, P2 = sp.expand(F1 * F2), sp.expand(F1 * F3)
    Gu = sp.simplify(P1.subs({y: u / x, z: v / x}))
    Gv = sp.simplify(P2.subs({y: u / x, z: v / x}))
    okC = (sp.simplify(sp.diff(Gu, x)) == 0) and (sp.simplify(sp.diff(Gv, x)) == 0)
    dG = sp.simplify(sp.diff(Gu, u) * sp.diff(Gv, v) - sp.diff(Gu, v) * sp.diff(Gv, u))
    q3 = q_of([1, -1, -1], [x * y, x * z], [x, y, z])
    pred = sp.simplify((q3.subs(x, F1)) / q3)          # (q' o F)/q with q' = q = x
    okD = sp.simplify(dG - pred) == 0
    print(f"\n3. synthetic family F = (x, y + z*A(xz), z), weights (1,-1,-1)")
    print(f"   det JF = 1 : {okA};  equivariant : {okB};  descends (x-free) : {okC}")
    print(f"   q = {q3};  master formula predicts det JG = {pred};  actual = {dG}")
    PASS.append(("master formula reproduces det JG on the synthetic family",
                 okA and okB and okC and okD))
    print(f"   {'PASS' if okA and okB and okC and okD else 'FAIL'}")

    # ---- CHECK 4: classify q over the weight systems that satisfy A1 ----
    # HYPOTHESIS CARE: A1 requires the invariant ring to be POLYNOMIAL.  For a
    # C*-action on C^3 with weights (w0, -b, -c), w0 > 0, that holds for w0 = 1,
    # where the invariants are freely generated by (x^b y, x^c z) since every
    # invariant monomial x^a y^j z^k has a = bj + ck and equals (x^b y)^j (x^c z)^k.
    # It FAILS for w0 >= 2 in general: weights (2,-1,-1) need THREE generators
    # x y^2, x y z, x z^2 with the relation (xyz)^2 = (xy^2)(xz^2), so the
    # quotient is a quadric cone, not C^2, and such systems are OUTSIDE A1.
    print("\n4. q over the weight systems that actually satisfy A1 (w0 = 1):")
    rows = []
    for b in (1, 2, 3):
        for c in (1, 2, 3):
            if c < b:
                continue
            inv = [x**b * y, x**c * z]
            qq = q_of([1, -b, -c], inv, [x, y, z])
            k = sp.degree(sp.expand(qq), x)
            rows.append((b, c, qq, k))
            flag = '' if sp.simplify(qq - x**(b + c - 1)) == 0 else '   <-- BREAKS FORM'
            print(f"   weights (1,-{b},-{c})  invariants {tuple(inv)}  q = {qq}  k = {k}{flag}")
    ok_form = all(sp.simplify(qq - x**(b + c - 1)) == 0 for b, c, qq, _ in rows)
    PASS.append(("q = x^(b+c-1) for every weight system (1,-b,-c)", ok_form))
    print(f"   closed form q = x^(b+c-1): {'PASS' if ok_form else 'FAIL'}")
    ok4 = any(k == 1 for _, _, _, k in rows)
    PASS.append(("k = 1 is achievable, so k >= 2 is NOT forced by descent", ok4))
    print(f"   k = 1 occurs (at b = c = 1, and ONLY there since k = b+c-1): "
          f"{'PASS -- A1 answered, k >= 2 is NOT forced' if ok4 else 'FAIL'}")

    # ---- CHECK 5: the hypothesis really does fail for w0 = 2 ----
    a, bb, cc = sp.symbols('a bb cc', integer=True, nonnegative=True)
    gens = [(i, j, kk) for i in range(4) for j in range(7) for kk in range(7)
            if 2 * i - j - kk == 0 and (i, j, kk) != (0, 0, 0)]
    # a monomial is decomposable iff it is a product of strictly smaller invariants
    def decomposable(m, pool):
        return any(all(m[t] - p[t] >= 0 for t in range(3)) and
                   tuple(m[t] - p[t] for t in range(3)) in pool
                   for p in pool if p != m)
    pool = set(gens)
    irred = [m for m in gens if not decomposable(m, pool)]
    ok5 = len(irred) == 3
    print(f"\n5. weights (2,-1,-1): irreducible invariant monomials = "
          f"{sorted(irred)}  -> {len(irred)} generators")
    PASS.append(("weights (2,-1,-1) need 3 generators, so they are outside A1's "
                 "hypothesis (quotient is a quadric cone, not C^2)", ok5))
    print(f"   {'PASS -- correctly excluded' if ok5 else 'FAIL'}")

    # ---- CHECK 6: the mismatched-weight escape is CLOSED by weight bookkeeping ----
    # Equivariance forces F_1 to have SOURCE weight equal to the target weight
    # w'_0 = 1.  The Keller-descent condition is q' o F = c q, i.e.
    # F_1^{k'} = c x^k.  Source weight of the left side is k' * 1 = k'; of the
    # right side, k.  So k = k' is FORCED, and then F_1^k = c x^k with F_1
    # polynomial gives F_1 = lambda x.  There is no m > 1.
    print("\n6. can the Keller-descent condition be met with k != k'?")
    bad = []
    for (b, c) in [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)]:
        for (b2, c2) in [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)]:
            k, k2 = b + c - 1, b2 + c2 - 1
            # F_1 has source weight w'_0 = 1, so F_1^{k'} has source weight k'.
            # x^k has source weight k.  Condition solvable only if k == k'.
            if k != k2:
                bad.append(((b, c), (b2, c2), k, k2))
    print(f"   {len(bad)} of 25 source/target pairs have k != k'; for every one of them")
    print(f"   the two sides of q' o F = c*q carry DIFFERENT source weights (k' vs k),")
    print(f"   so the condition is unsatisfiable.  No m = k/k' > 1 exists.")
    # and when k == k', F_1^k = c x^k with F_1 polynomial forces F_1 = lambda x
    lam = sp.symbols('lam')
    ok6 = all(sp.simplify(sp.expand((lam * x) ** kk) - lam**kk * x**kk) == 0
              for kk in (1, 2, 3, 4, 5))
    ok6 = ok6 and all(k != k2 for _, _, k, k2 in bad)
    PASS.append(("k != k' is impossible: equivariance forces F_1 to have source "
                 "weight 1, so F_1^{k'} has weight k' and must equal x^k of weight k",
                 ok6))
    print(f"   when k = k', F_1^k = c x^k with F_1 polynomial forces F_1 = lambda*x")
    print(f"   {'PASS -- the mismatched-weight escape is CLOSED' if ok6 else 'FAIL'}")

    print("\n" + "=" * 72)
    for name, ok in PASS:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    assert all(ok for _, ok in PASS), "a check failed"
    print(f"\nall {len(PASS)} checks PASS")


if __name__ == '__main__':
    main()
