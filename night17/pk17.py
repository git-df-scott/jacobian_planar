"""night17 -- in-lane bivariate polynomial kernel over Q.

Representation: dict {(i, j): Fraction} for sum c_ij x^i y^j; zero coefficients
are pruned, so {} is the zero polynomial.  Reimplemented in this lane.
"""
from fractions import Fraction as F


def clean(A):
    return {k: F(v) for k, v in A.items() if F(v) != 0}


def padd(*Ps):
    C = {}
    for A in Ps:
        for k, v in A.items():
            C[k] = C.get(k, F(0)) + F(v)
    return clean(C)


def pscal(c, A):
    c = F(c)
    return {} if c == 0 else {k: c * F(v) for k, v in A.items()}


def psub(A, B):
    return padd(A, pscal(-1, B))


def pmul(A, B):
    C = {}
    for a, ca in A.items():
        for b, cb in B.items():
            k = (a[0] + b[0], a[1] + b[1])
            C[k] = C.get(k, F(0)) + F(ca) * F(cb)
    return clean(C)


def ppow(A, n):
    R = {(0, 0): F(1)}
    for _ in range(n):
        R = pmul(R, A)
    return R


def dx(A):
    return clean({(i - 1, j): F(c) * i for (i, j), c in A.items() if i > 0})


def dy(A):
    return clean({(i, j - 1): F(c) * j for (i, j), c in A.items() if j > 0})


def bracket(P, Q):
    return psub(pmul(dx(P), dy(Q)), pmul(dy(P), dx(Q)))


def tdeg(A):
    return max(i + j for (i, j) in A) if A else -1


def degy(A):
    return max(j for (i, j) in A) if A else -1


def compose(A, X, Y):
    """A(X(x,y), Y(x,y)) with X, Y polynomials in the same representation."""
    out = {}
    xp = {0: {(0, 0): F(1)}}
    yp = {0: {(0, 0): F(1)}}
    for (i, j), c in A.items():
        while i not in xp:
            xp[max(xp) + 1] = pmul(xp[max(xp)], X)
        while j not in yp:
            yp[max(yp) + 1] = pmul(yp[max(yp)], Y)
        out = padd(out, pscal(c, pmul(xp[i], yp[j])))
    return out


def to_str(A):
    if not A:
        return "0"
    terms = []
    for (i, j) in sorted(A, key=lambda k: (-(k[0] + k[1]), -k[0])):
        c = A[(i, j)]
        m = ""
        if i:
            m += "*x" + ("^%d" % i if i > 1 else "")
        if j:
            m += "*y" + ("^%d" % j if j > 1 else "")
        terms.append(("(%s)" % c if c.denominator != 1 else str(c)) + m)
    return " + ".join(terms).replace("+ -", "- ")


def from_sympy(expr, x, y):
    import sympy as sp
    p = sp.Poly(sp.expand(expr), x, y)
    return clean({(int(m[0]), int(m[1])): F(str(c)) for m, c in
                  zip(p.monoms(), p.coeffs())})
