"""night18 -- bivariate polynomial kernel with SYMBOLIC (sympy) coefficients.

Representation: dict {(i, j): sympy expression} for sum c_ij x^i y^j.
Coefficients live in Q(params); zero coefficients are pruned, so {} is zero.
This is the symbolic analogue of night17/pk17.py and is checked against it by
specialisation (control C1).
"""
import sympy as sp

X, Y = sp.symbols('x y')


def clean(A):
    out = {}
    for k, v in A.items():
        v = sp.cancel(sp.together(sp.expand(v)))
        if v != 0:
            out[k] = v
    return out


def padd(*Ps):
    C = {}
    for A in Ps:
        for k, v in A.items():
            C[k] = C.get(k, 0) + v
    return clean(C)


def pscal(c, A):
    return clean({k: c * v for k, v in A.items()})


def psub(A, B):
    return padd(A, pscal(-1, B))


def pmul(A, B):
    C = {}
    for a, ca in A.items():
        for b, cb in B.items():
            k = (a[0] + b[0], a[1] + b[1])
            C[k] = C.get(k, 0) + ca * cb
    return clean(C)


def ppow(A, n):
    R = {(0, 0): sp.Integer(1)}
    for _ in range(n):
        R = pmul(R, A)
    return R


def dx(A):
    return clean({(i - 1, j): v * i for (i, j), v in A.items() if i > 0})


def dy(A):
    return clean({(i, j - 1): v * j for (i, j), v in A.items() if j > 0})


def bracket(P, Q):
    return psub(pmul(dx(P), dy(Q)), pmul(dy(P), dx(Q)))


def tdeg(A):
    return max(i + j for (i, j) in A) if A else -1


def from_expr(e):
    """sympy expression in x, y (coefficients rational in the parameters)."""
    e = sp.expand(e)
    p = sp.Poly(e, X, Y)
    return clean({(int(m[0]), int(m[1])): c for m, c in zip(p.monoms(), p.coeffs())})


def to_expr(A):
    return sp.expand(sum(v * X**i * Y**j for (i, j), v in A.items()))


def subs(A, d):
    return clean({k: sp.nsimplify(sp.cancel(v.subs(d))) if hasattr(v, 'subs') else v
                  for k, v in A.items()})


def to_pk(A):
    """specialised symbolic poly -> night17/pk17 rational dict."""
    from fractions import Fraction as F
    out = {}
    for k, v in A.items():
        r = sp.nsimplify(sp.cancel(sp.sympify(v)))
        r = sp.Rational(r)
        if r != 0:
            out[k] = F(int(r.p), int(r.q))
    return out


def to_str(A):
    return sp.sstr(to_expr(A))
