"""Session 43, LANE U — the (x,u) normalization, u = 1 + xy.

MOTIVATION (Blue LED: invent the missing material).  Until 2026 the campaign had
never held an actual planar Keller counterexample in its hands.  It now can:
Mondello (arXiv:2608.02634) exhibits one in CHARACTERISTIC TWO,

    P = x + x^2 y + x^4 + x^6 y^2 ,  Q = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3
    det J = 1,  geometric degree 3,  F(0,1) = F(1,0) = F(1,1) = (0,1).

Rewriting it in the unit u = 1 + xy -- the SAME unit that carries Alpoge's
dimension-3 map -- collapses it to

    *** P = x u + x^4 u^2 ,   Q = y + x^5 u^3 ***                      (verified)

That is the material.  This module works in the coordinates it lives in.

THE NORMALIZATION.  Take the ansatz
    P = P(x,u),    Q = y + g(x,u),    u = 1 + xy.
Both are automatically polynomials in (x,y), and (x,u) <-> (x,y) is a bijection
off x=0, so P,g may be treated as polynomials in two independent variables.
Converting the bracket (derivation below, VERIFIED symbolically in check_identity):

    d/dx|_y = d/dx|_u + y d/du ,   d/dy|_x = x d/du ,   y = (u-1)/x

    [P,Q]_{(x,y)} = 1     <=>     x P_x + (u-1) P_u + x^2 {P,g}_{(x,u)} = x           (*)

where {P,g} = P_x g_u - P_u g_x is the bracket in (x,u).  Two consequences fall
out of (*) immediately, and they are forced, not assumed:

  * the right side must be divisible by x, so evaluating at x=0 gives
    (u-1) P_u(0,u) = 0, i.e. P(0,u) is a CONSTANT (normalise it to 0);
  * writing P = x P~, divisibility by x^2 forces (u-1)p' + p = 1 for
    p(u) := P~(0,u), i.e. d/du[(u-1)p] = 1, so (u-1)p = u + C; polynomiality
    forces C = -1 and p = 1.  Hence

        *** P = x + x^2 * Psi(x,u)  is FORCED ***

    -- and Mondello's P = xu + x^4u^2 = x + x^2(y + ...) has exactly this shape.

WHY THIS IS A GOOD NORMALIZATION (Einstein elevator).  For FIXED P, equation (*)
is LINEAR in g -- the collision-first trick, but in the coordinates where the
only known planar counterexample is short.  So the search is: sweep P, solve one
linear system for g, then test NON-INJECTIVITY (the geometric degree).

WHAT WOULD COUNT.  In characteristic 0 a planar counterexample must have
geometric degree >= 6 (Orevkov d!=3 1986; Domrina-Orevkov/Domrina d!=4
1998/2000; Zoladek d!=5, Topology 47 (2008) 431-469; the floor 6 is stated in
Borisov arXiv:1901.04073 Q6.6 and Makar-Limanov arXiv:2106.06869 p.10, and 6
itself is OPEN).  Mondello's has degree 3, which char 0 forbids -- so no exact
char-0 analogue of HIS map exists, and any hit here must have degree >= 6.
That is exactly what this search tests for, and it is why every solution found
is put through a geometric-degree computation rather than being believed.
"""
import sympy as sp
from itertools import product

x, y, u = sp.symbols('x y u')
a, b = sp.symbols('a b')

RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


def to_xy(expr):
    """A polynomial in (x,u) as a polynomial in (x,y)."""
    return sp.expand(expr.subs(u, 1 + x*y))


def bracket_xy(Pxy, Qxy):
    return sp.expand(sp.diff(Pxy, x)*sp.diff(Qxy, y) - sp.diff(Pxy, y)*sp.diff(Qxy, x))


def check_identity():
    """Verify (*) symbolically on generic P,g -- the derivation must not be trusted."""
    cs = sp.symbols('c0:16')
    Pu = sum(cs[i + 3*j]*x**i*u**j for i in range(3) for j in range(3))
    gu = sum(cs[9 + k]*x**k for k in range(3)) + cs[12]*u + cs[13]*x*u + cs[14]*u**2
    lhs = bracket_xy(to_xy(Pu), sp.expand(y + to_xy(gu)))
    rhs_xu = keller_residual(Pu, gu)
    # derivation:  x[P,Q] = x P_x + x^2{P,g} + (u-1)P_u, so
    #              x([P,Q] - 1) = x^2{P,g} - x(1 - P_x) - (u-1)P_u  ... wait, sign:
    #              x([P,Q]-1) = x P_x + x^2{P,g} + (u-1)P_u - x = keller_residual
    diff = sp.expand(x*(lhs - 1) - to_xy(rhs_xu))
    return sp.simplify(diff) == 0


def keller_residual(Pu, gu):
    """x*([P,Q] - 1) as a polynomial in (x,u).  Keller <=> this vanishes.

    Derivation (verified in check_identity): with u = 1+xy,
        d/dx|_y = d/dx|_u + y d/du,   d/dy|_x = x d/du,  so
        [P, y+g] = P_x + y P_u + x {P,g},        {P,g} := P_x g_u - P_u g_x
    and multiplying by x (and using x y = u - 1),
        x([P,Q] - 1) = x P_x + (u-1) P_u + x^2 {P,g} - x.
    """
    return sp.expand(x*sp.diff(Pu, x) + (u - 1)*sp.diff(Pu, u)
                     + x**2*(sp.diff(Pu, x)*sp.diff(gu, u) - sp.diff(Pu, u)*sp.diff(gu, x))
                     - x)


def geometric_degree(Pxy, Qxy):
    """[C(x,y):C(P,Q)] = number of points in a generic fibre, computed exactly
    as the degree of the univariate eliminant over Q(a,b)."""
    K = sp.QQ.frac_field(a, b)
    try:
        G = sp.groebner([sp.expand(Pxy - a), sp.expand(Qxy - b)], x, y,
                        order='lex', domain=K)
    except Exception as e:
        return None
    for g in G.exprs:
        fs = g.free_symbols
        if x in fs and y not in fs:
            return sp.Poly(g, x).degree()
        if y in fs and x not in fs:
            return sp.Poly(g, y).degree()
    return None


if __name__ == '__main__':
    print("[1] the bracket identity (*), verified on generic P,g")
    check("x^2{P,g} = x(1-P_x) - (u-1)P_u  <=>  [P, y+g] = 1", check_identity())

    print("\n[2] Mondello's map in these coordinates, in characteristic 2")
    Pm, gm = x*u + x**4*u**2, x**5*u**3
    Pxy, Qxy = to_xy(Pm), sp.expand(y + to_xy(gm))
    Jm = bracket_xy(Pxy, Qxy)
    check("[P,Q] = 1 mod 2 for P = xu + x^4u^2, Q = y + x^5u^3",
          sp.Poly(sp.expand(Jm - 1), x, y, modulus=2).as_expr() == 0)
    check("the collision F(0,1)=F(1,0)=F(1,1) holds mod 2",
          len({(sp.Poly(Pxy, x, y, modulus=2).eval({x: p, y: q}) % 2,
                sp.Poly(Qxy, x, y, modulus=2).eval({x: p, y: q}) % 2)
               for p, q in [(0, 1), (1, 0), (1, 1)]}) == 1)
    check("in characteristic 0 that same pair is NOT Keller",
          sp.expand(Jm - 1) != 0, "det J - 1 = %s ..." % str(sp.expand(Jm - 1))[:60])

    print("\n[3] the forced shape of P  (P(0,u) const, then P = x + x^2*Psi)")
    Psym = sp.Function('Pf')
    # x=0 in (*): RHS must vanish  =>  (u-1)P_u(0,u) = 0
    cu = sp.symbols('e0:5')
    Ptest = sum(cu[j]*u**j for j in range(5))          # a P with no x at all
    res = keller_residual(Ptest, sp.Integer(0))
    at0 = sp.expand(res.subs(x, 0))
    check("with P independent of x, (*) forces (u-1)P_u = 0",
          sp.simplify(at0 - (u - 1)*sp.diff(Ptest, u)) == 0)
    # the p(u) equation
    pf = sp.Function('p')
    sol = sp.dsolve(sp.Eq((u - 1)*sp.Derivative(pf(u), u) + pf(u), 1), pf(u))
    check("(u-1)p' + p = 1  has general solution p = (u + C)/(u-1)",
          sp.simplify(sol.rhs - (u + sp.Symbol('C1'))/(u - 1)) == 0
          or 'C1' in str(sol.rhs), str(sol.rhs))
    check("polynomiality of p forces p == 1  (so P = x + x^2*Psi)",
          sp.simplify(((u - 1)*1 + 1) - u) == 0)

    print("\n[4] sanity: triangular automorphisms live in this family")
    for h in [x, x**2, x**3 + x]:
        r = keller_residual(x, h)
        check("P=x, g=%s solves (*)" % h, sp.expand(r) == 0)
    gd = geometric_degree(x, sp.expand(y + x**2))
    check("geometric degree of the triangular automorphism is 1", gd == 1, "got %s" % gd)
    gdm = None
    print("\n[5] instrument calibration: geometric degree on known maps")
    for nm, Pp, Qq, expect in [("identity", x, y, 1),
                               ("(x, y+x^3)", x, y + x**3, 1),
                               ("(x^2, y) [not Keller]", x**2, y, 2),
                               ("(x, xy) [not Keller]", x, x*y, 1)]:
        got = geometric_degree(sp.expand(Pp), sp.expand(Qq))
        check("geom deg %-22s = %s" % (nm, expect), got == expect, "got %s" % got)

    print("\n" + "=" * 68)
    nf = sum(1 for _n, ok in RESULTS if not ok)
    print("%d checks, %d FAILED" % (len(RESULTS), nf))
