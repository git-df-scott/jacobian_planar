"""Session 43 — EXACT Euler characteristic of an affine plane curve.

This replaces the chi computation in pathS_chi.py, which carried three bugs
found in the audit sweep:

  BUG 5  inclusion-exclusion over components used only PAIRWISE intersections,
         so any point lying on three or more components was over-subtracted.
         Three concurrent lines {uv(u-v)=0} have chi = 3 - 3 + 1 = 1; the old
         code returned 0.
  BUG 6  the count of points at infinity used the number of irreducible factors
         of the leading form OVER Q.  A binary form splits into linear factors
         over C, so an irreducible quadratic like u^2+v^2 is TWO points at
         infinity, not one.  The old code undercounted, which makes chi look
         LARGER than it is -- i.e. it could manufacture false candidates.
  BUG 7  a component f with f | B is a 1-DIMENSIONAL centre of the affine
         modification, so S is reducible (hence disconnected, being smooth) --
         but the Nullstellensatz hit-test reports it as an ordinary hit.

The fix for BUG 5 is structural: do not decompose into components at all.
Apply a generic shear so that NO component is vertical, then push the whole
reduced curve through one projection and use motivic additivity:

    chi(C) = n_gen * (1 - s) + sum over the s special u-values of #fibre

where the special values are the roots of lc_V(f) * disc_V(f).  Over the
complement the projection is finite and unramified, hence a covering of degree
n_gen, so chi multiplies exactly.  This is valid for reducible curves and needs
no intersection bookkeeping whatsoever.

Fibre counts at a special value are computed EXACTLY, not by sampling mod p:
the special locus is factored over Q, all roots of an irreducible factor q are
Galois-conjugate and so give the same count, and that count is obtained by
running the Euclidean algorithm in (Q[U]/(q))[V] -- q is irreducible, so
Q[U]/(q) is a field and every nonzero element is invertible by gcdex.
"""
import sympy as sp

U, V = sp.symbols('U V')


# ---------------------------------------------------------------- field Q[U]/(q)
def _red(a, q):
    a = sp.expand(a)
    if a == 0:
        return sp.Integer(0)
    return sp.expand(sp.rem(sp.Poly(a, U), sp.Poly(q, U)).as_expr())


def _inv(a, q):
    """Inverse of a in the field Q[U]/(q); q irreducible, a not divisible by q."""
    a = _red(a, q)
    if a == 0:
        raise ZeroDivisionError
    s, t, h = sp.gcdex(sp.Poly(a, U), sp.Poly(q, U))
    h = h.as_expr()
    if h.free_symbols:
        raise ArithmeticError("q is not irreducible: gcd = %s" % h)
    return _red(sp.expand(s.as_expr()/h), q)


def _gcd_degree(A, B, q):
    """deg of gcd of two polynomials in (Q[U]/(q))[V], given as coefficient lists
    (index = power of V).  Pure Euclidean algorithm over the field."""
    def deg(c):
        d = -1
        for i, t in enumerate(c):
            if _red(t, q) != 0:
                d = i
        return d

    A = [_red(t, q) for t in A]
    B = [_red(t, q) for t in B]
    while deg(B) >= 0:
        dA, dB = deg(A), deg(B)
        if dA < dB:
            A, B = B, A
            continue
        inv = _inv(B[dB], q)
        f = _red(A[dA]*inv, q)
        new = list(A)
        for i in range(dB + 1):
            new[i + dA - dB] = _red(new[i + dA - dB] - f*B[i], q)
        A = new
        if deg(A) == dA:                      # safety: must strictly decrease
            A[dA] = sp.Integer(0)
    return deg(A)


def _coeff_list(f, var):
    p = sp.Poly(f, var)
    d = p.degree()
    cs = [sp.Integer(0)]*(d + 1)
    for (e,), c in p.terms():
        cs[e] = sp.expand(c)
    return cs


def n_distinct_fibre_at(f, q):
    """#distinct V-roots of f(a,V) for a a root of the irreducible q.  Exact."""
    cs = _coeff_list(f, V)
    cs = [_red(c, q) for c in cs]
    d = -1
    for i, c in enumerate(cs):
        if c != 0:
            d = i
    if d <= 0:
        return 0                                   # f(a,V) is a nonzero constant
    dcs = [sp.expand(i*cs[i]) for i in range(1, d + 1)]
    return d - max(_gcd_degree(cs[:d + 1], dcs, q), 0)


def _squarefree(f, *vars_):
    fl = sp.factor_list(sp.expand(f))[1]
    out = sp.Integer(1)
    for b, _m in fl:
        if b.free_symbols:
            out *= b
    return sp.expand(out)


def chi_plane_curve(f, uu=None, vv=None, _depth=0):
    """Exact chi of the reduced affine plane curve {f=0} in C^2."""
    if uu is not None:
        f = sp.expand(sp.sympify(f).subs({uu: U, vv: V}, simultaneous=True))
    f = _squarefree(f, U, V)
    if not f.free_symbols:
        return sp.Integer(0)                       # empty curve
    # kill vertical components with a shear: a component {U = c} would make the
    # fibre infinite over c and break the projection argument.
    for mu in ([0] if _depth == 0 else []) + [1, -1, 2, -2, 3, 5, 7, 11]:
        g = sp.expand(f.subs(U, U + mu*V)) if mu else f
        if sp.Poly(g, V).degree() >= 1 and all(
                sp.Poly(b, V).degree() >= 1
                for b, _m in sp.factor_list(g)[1] if b.free_symbols):
            f = g
            break
    else:
        raise ArithmeticError("could not remove vertical components")

    F = sp.Poly(f, V)
    n_gen = F.degree()
    lc = sp.expand(F.LC())
    special = sp.Integer(1)
    if sp.sympify(lc).free_symbols:
        special = lc
    if n_gen >= 2:
        dsc = sp.expand(sp.discriminant(F, V))
        if dsc == 0:
            raise ArithmeticError("discriminant vanishes on a reduced curve")
        if sp.sympify(dsc).free_symbols:
            special = sp.expand(special*dsc) if special != 1 else dsc
    if not sp.sympify(special).free_symbols:
        return sp.Integer(n_gen)                   # covering of C: chi = n_gen
    S = sp.Poly(_squarefree(special, U), U)
    total = sp.Integer(n_gen)*(1 - S.degree())
    for q, _m in sp.factor_list(S.as_expr())[1]:
        qq = sp.Poly(q, U)
        if qq.degree() < 1:
            continue
        total += qq.degree()*n_distinct_fibre_at(f, sp.expand(q))
    return sp.Integer(total)


def n_points_at_infinity(f, uu=None, vv=None):
    """#distinct points at infinity = degree of the RADICAL of the leading form
    (a binary form splits into linear factors over C -- BUG 6)."""
    if uu is not None:
        f = sp.expand(sp.sympify(f).subs({uu: U, vv: V}, simultaneous=True))
    f = sp.expand(f)
    P = sp.Poly(f, U, V)
    d = P.total_degree()
    top = sum(c*U**m[0]*V**m[1] for m, c in zip(P.monoms(), P.coeffs()) if sum(m) == d)
    return sp.Poly(_squarefree(top, U, V), U, V).total_degree()


def is_A1(f, uu=None, vv=None):
    """A component is = A^1 iff irreducible, SMOOTH and chi = 1."""
    if uu is not None:
        f = sp.expand(sp.sympify(f).subs({uu: U, vv: V}, simultaneous=True))
    if chi_plane_curve(f) != 1:
        return False
    G = sp.groebner([sp.expand(f), sp.diff(f, U), sp.diff(f, V)], U, V, order='grevlex')
    return list(G.exprs) == [sp.Integer(1)]


# ---------------------------------------------------------------- calibration
CAL = [
    ("line {V=0}",                        V,                            1),
    ("parabola {V=U^2} ~ A^1",            V - U**2,                     1),
    ("hyperbola {UV=1} ~ C*",             U*V - 1,                      0),
    ("circle {U^2+V^2=1} ~ C*",           U**2 + V**2 - 1,              0),
    ("cuspidal cubic {V^2=U^3}",          V**2 - U**3,                  1),
    ("nodal cubic {V^2=U^3+U^2}",         V**2 - U**3 - U**2,           0),
    ("elliptic {V^2=U^3-U} g=1,s=1",      V**2 - U**3 + U,             -1),
    ("two disjoint lines",                V*(V - 1),                    2),
    ("two crossing lines {UV=0}",         U*V,                          1),
    ("THREE concurrent lines",            U*V*(U - V),                  1),
    ("line disjoint from a hyperbola",    U*(U*V - 1),                  1),
    ("two disjoint hyperbolas",           (U*V - 1)*(U*V - 2),          0),
    ("three parallel lines",              V*(V - 1)*(V - 2),            3),
    ("conic pair meeting in 2 points",    (U**2 + V**2 - 1)*V,          -1),
    ("A^1 and a nodal cubic, disjoint?",  (V - U**2),                   1),
    ("{V^2 = U^2(U+1)} nodal",            V**2 - U**2*(U + 1),          0),
    ("{U^2 V^2 = 1} two hyperbolas",      U**2*V**2 - 1,                0),
]

INF_CAL = [("u^2+v^2 is 2 points over C", U**2 + V**2 - 1, 2),
           ("u*v is 2 points", U*V - 1, 2),
           ("(u-v)^3 is 1 point", (U - V)**3 - 1, 1),
           ("u^3+v^3 is 3 points", U**3 + V**3 - 1, 3)]

if __name__ == '__main__':
    nf = 0
    print("CALIBRATION of chi_plane_curve")
    for nm, f, exp in CAL:
        got = chi_plane_curve(f)
        ok = (got == exp)
        nf += 0 if ok else 1
        print(("  PASS  " if ok else "  FAIL  ") + "chi(%-34s) = %-3s" % (nm, exp)
              + ("" if ok else "   GOT %s" % got))
    print("\nCALIBRATION of n_points_at_infinity")
    for nm, f, exp in INF_CAL:
        got = n_points_at_infinity(f)
        ok = (got == exp)
        nf += 0 if ok else 1
        print(("  PASS  " if ok else "  FAIL  ") + "%-32s = %s" % (nm, exp)
              + ("" if ok else "   GOT %s" % got))
    print("\nCALIBRATION of is_A1")
    for nm, f, exp in [("line", V, True), ("parabola", V - U**2, True),
                       ("cuspidal cubic", V**2 - U**3, False),
                       ("hyperbola", U*V - 1, False)]:
        got = is_A1(f)
        ok = (got == exp)
        nf += 0 if ok else 1
        print(("  PASS  " if ok else "  FAIL  ") + "is_A1(%-16s) = %s" % (nm, exp)
              + ("" if ok else "   GOT %s" % got))
    print("\n%s" % ("ALL CALIBRATIONS PASS" if nf == 0 else "%d CALIBRATION FAILURES" % nf))
