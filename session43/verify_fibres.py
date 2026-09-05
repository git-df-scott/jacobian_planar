"""Session 43 — verification of the LOAD-BEARING claim: the fibre structure.

chi(S) = 3 chi(Sigma) - 2 chi(A_Sigma) - chi(C_Sigma) is only as good as the
three fibre counts it rests on.  Motivic additivity gives
chi(F^{-1}(stratum)) = (fibre count) * chi(stratum) provided the restriction of F
over that stratum is a finite covering, so what must be established is:

    fibre = 3   off  {Delta = 0}
    fibre = 1   on   {Delta = 0} \\ C_sing
    fibre = 0   on   C_sing

Sampling is not enough -- these are proved here at the GENERIC POINT of each
stratum, over the function field of the stratum, and then cross-checked at
explicit rational points.  Each stratum is irreducible, so the generic-point
computation controls a dense open subset; the sampling is what guards against a
smaller bad locus inside it.

Independent published cross-check: Gao (arXiv:2608.00222) Theorem 3.4 states the
complete fibre-size set of this map is {3,1,0}, which is exactly what comes out
below, derived here from scratch.
"""
import sys
import sympy as sp

x, y, z = sp.symbols('x y z')
w1, w2, w3 = sp.symbols('w1 w2 w3')
mu, r = sp.symbols('mu r')

U = 1 + x*y
P = U**3*z + y**2*U*(4 + 3*x*y)
Q = 3*x*U**2*z + y + 3*x*y**2*(4 + 3*x*y)
R = -x**3*z + 2*x - 3*x**2*y
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)

W1 = (mu + 1)*(mu - 2)**2/(27*r**2)
W2 = -(mu - 2)*(mu + 2)/(3*r)
W3 = r

OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


def elim_degree(targets, K, gens=(x, y, z)):
    """Degree of the univariate eliminant in x of the fibre ideal over the field K."""
    G = sp.groebner([sp.expand(sp.numer(sp.together(f - t))) for f, t in targets],
                    *gens, order='lex', domain=K)
    if list(G.exprs) == [sp.Integer(1)]:
        return 0, G
    for g in G.exprs:
        fs = g.free_symbols
        if x in fs and not (fs & {y, z}):
            return sp.Poly(g, x).degree(), G
    return None, G


if __name__ == '__main__':
    print("[A] generic point OFF the tear: fibre must be 3")
    K = sp.QQ.frac_field(w1, w2, w3)
    d, G = elim_degree([(P, w1), (Q, w2), (R, w3)], K)
    rec("eliminant in x has degree 3 over Q(w1,w2,w3)", d == 3, "degree %s" % d)
    # and it is proportional to h
    h = sp.expand(DELTA*x**3 + (4 - 3*w2*w3)*x - 2*w3)
    gx = [g for g in G.exprs if x in g.free_symbols and not (g.free_symbols & {y, z})]
    if gx:
        ratio = sp.cancel(sp.expand(gx[0])/h)
        rec("that eliminant is proportional to h = Delta x^3 + (4-3w2w3)x - 2w3",
            x not in sp.sympify(ratio).free_symbols, "ratio = %s" % ratio)

    print("\n[B] generic point ON the tear (mu != 0): fibre must be 1")
    Kt = sp.QQ.frac_field(mu, r)
    d2, G2 = elim_degree([(P, W1), (Q, W2), (R, W3)], Kt)
    rec("eliminant in x has degree 1 over Q(mu,r)", d2 == 1, "degree %s" % d2)

    print("\n[C] generic point of C_sing (mu = 0): fibre must be EMPTY")
    Kr = sp.QQ.frac_field(r)
    d3, G3 = elim_degree([(P, sp.Rational(4, 27)/r**2), (Q, sp.Rational(4, 3)/r), (R, r)], Kr)
    rec("fibre ideal is (1) over Q(r), i.e. the fibre is empty",
        list(G3.exprs) == [sp.Integer(1)], "GB = %s" % str(list(G3.exprs))[:70])

    print("\n[D] the parametrization is ONTO the tear minus {w3=0}")
    E = 27*w1*w3**2 - 9*w2*w3 + 8
    m_of_w = E/(4 - 3*w2*w3)
    for nm, expr, tgt in [("w2", W2, w2), ("w1", W1, w1)]:
        back = sp.expand(sp.numer(sp.together(
            sp.cancel(expr.subs({mu: m_of_w, r: w3}) - tgt))))
        _q, rem = sp.reduced(back, [DELTA], w1, w2, w3)
        rec("%s is recovered modulo Delta" % nm, sp.expand(rem) == 0,
            "remainder %s" % str(sp.expand(rem))[:50])

    print("\n[E] explicit rational samples (guards a smaller bad locus)")
    import random
    random.seed(5)
    bad = []
    n_off = 0
    while n_off < 8:
        wv = tuple(sp.Rational(random.randint(-9, 9), random.randint(1, 4)) for _ in range(3))
        if sp.expand(DELTA.subs(dict(zip((w1, w2, w3), wv)))) == 0:
            continue
        n_off += 1
        n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
        if n != 3:
            bad.append(('off-tear', wv, n))
    rec("8 random points off the tear all have fibre 3", not bad, str(bad))

    bad2 = []
    for mv in [1, 2, -1, sp.Rational(1, 2), 3, -3, sp.Rational(5, 2)]:
        for rv in [1, -2, sp.Rational(1, 3)]:
            wv = (W1.subs({mu: mv, r: rv}), W2.subs({mu: mv, r: rv}), rv)
            n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
            if n != 1:
                bad2.append((mv, rv, n))
    rec("21 points on the tear (mu != 0) all have fibre 1", not bad2, str(bad2))

    bad3 = []
    for rv in [1, -1, 2, sp.Rational(1, 3), -sp.Rational(3, 2)]:
        wv = (sp.Rational(4, 27)/rv**2, sp.Rational(4, 3)/rv, rv)
        n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
        if n != 0:
            bad3.append((rv, n))
    rec("5 points of C_sing all have EMPTY fibre", not bad3, str(bad3))

    print("\n[F] the E=0 anomaly is NOT part of the tear (fibre stays 3 there)")
    bad4 = []
    for v in [sp.Rational(1, 27), sp.Rational(1, 3), 2, -sp.Rational(2, 3)]:
        wv = (v, (27*v + 8)/9, 1)                      # E = 0, w3 = 1
        if sp.expand(DELTA.subs(dict(zip((w1, w2, w3), wv)))) == 0:
            continue
        n = len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))
        if n != 3:
            bad4.append((wv, n))
    rec("points with E=0 but Delta!=0 still have fibre 3", not bad4, str(bad4))

    print("\n" + "=" * 66)
    nf = sum(1 for _n, ok in OUT if not ok)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
