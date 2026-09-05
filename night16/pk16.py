# night15: in-lane copy of the night14 bivariate kernel (read-only lane).
"""night14 -- in-lane bivariate polynomial kernel (ring: Q).

Representation: dict {(i, j): Fraction}  for  sum c_ij x^i y^j.
Zero coefficients are always pruned, so the empty dict is the zero polynomial.
Reimplemented in-lane; night12 sources were read for reference only.
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
    if c == 0:
        return {}
    return {k: c * F(v) for k, v in A.items()}


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


def tdeg(A):
    return max(i + j for (i, j) in A) if A else -1


def degx(A):
    return max(i for (i, j) in A) if A else -1


def degy(A):
    return max(j for (i, j) in A) if A else -1


def topform(A):
    d = tdeg(A)
    return {k: v for k, v in A.items() if k[0] + k[1] == d}


# ------------------------------------------------------------- univariate (x)
# univariate polys are dicts {i: Fraction}; used for the F2 family algebra.

def u_to_bi(u):
    return clean({(i, 0): c for i, c in u.items()})


def u_mul(a, b):
    c = {}
    for i, ai in a.items():
        for j, bj in b.items():
            c[i + j] = c.get(i + j, F(0)) + F(ai) * F(bj)
    return {k: v for k, v in c.items() if v != 0}


def u_add(*ps):
    c = {}
    for p in ps:
        for i, v in p.items():
            c[i] = c.get(i, F(0)) + F(v)
    return {k: v for k, v in c.items() if v != 0}


def u_scal(s, a):
    s = F(s)
    return {} if s == 0 else {i: s * F(v) for i, v in a.items()}


def u_pow(a, n):
    r = {0: F(1)}
    for _ in range(n):
        r = u_mul(r, a)
    return r


def u_diff(a):
    return {i - 1: F(c) * i for i, c in a.items() if i > 0 and F(c) * i != 0}


def u_deg(a):
    return max(a) if a else -1


# ------------------------------------------------------------------ printing

def to_str(A, xv="x", yv="y"):
    if not A:
        return "0"
    terms = []
    for (i, j) in sorted(A, key=lambda k: (-(k[0] + k[1]), -k[0])):
        c = A[(i, j)]
        cs = str(c.numerator) if c.denominator == 1 else "(%d/%d)" % (c.numerator, c.denominator)
        parts = []
        if not (cs == "1" and (i or j)):
            parts.append(cs)
        if i:
            parts.append(xv if i == 1 else "%s^%d" % (xv, i))
        if j:
            parts.append(yv if j == 1 else "%s^%d" % (yv, j))
        terms.append("*".join(parts) if parts else cs)
    return " + ".join(terms).replace("+ -", "- ")


def to_singular(A, xv="x", yv="y"):
    """Exact Q representation for Singular: integer-cleared is not required,
    Singular's char-0 ring handles rationals, but we clear denominators anyway
    (scaling by a nonzero rational does not change the ideal)."""
    if not A:
        return "0"
    from math import gcd
    den = 1
    for c in A.values():
        den = den * c.denominator // gcd(den, c.denominator)
    terms = []
    for (i, j), c in sorted(A.items()):
        n = c * den
        assert n.denominator == 1
        t = "(%d)" % n.numerator
        if i:
            t += "*%s^%d" % (xv, i)
        if j:
            t += "*%s^%d" % (yv, j)
        terms.append(t)
    return "+".join(terms)


def phash(A):
    import hashlib
    return hashlib.sha256(to_str(A).encode()).hexdigest()[:12]
