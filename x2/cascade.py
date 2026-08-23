"""
Exact cascade solver for  {P,Q} = R  with prescribed Newton supports.

Setup (mirrors the campaign's Singular `extract` systems, re-derived here):

    P = sum_j Pd_j(x) y^j ,  Q = sum_k Q_k(x) y^k ,  R = sum_m Rr_m(x) y^m
    {P,Q} = P_x Q_y - P_y Q_x

Coefficient of y^m in {P,Q}:
    sum_{i+k=m+1} [ k Pd_i' Q_k - i Pd_i Q_k' ]

Isolating the i=0 term and using deg Pd_0 <= 1 (so Pd_0' = p10 is a nonzero
CONSTANT -- this is exactly what the Newton-polygon vertex (1,0) buys):

    (m+1) p10 Q_{m+1} = Rr_m + sum_{i>=1, k=m+1-i} [ i Pd_i Q_k' - k Pd_i' Q_k ]

so Q is uniquely determined by P, R and the choice Q_0 (taken 0), and it is
automatically POLYNOMIAL.  The whole problem is therefore a condition on P
alone: the cascade must land inside the prescribed x-windows and terminate.

Polynomials in x are dicts {exponent: coefficient}; coefficients are sympy
expressions in the unknowns c1..cN.
"""
from sympy import symbols, expand, simplify, Poly, Rational, together, factor
import sympy as sp


def padd(a, b):
    r = dict(a)
    for e, c in b.items():
        r[e] = r.get(e, 0) + c
    return {e: c for e, c in r.items() if c != 0}


def pscal(a, s):
    if s == 0:
        return {}
    return {e: c * s for e, c in a.items()}


def pmul(a, b):
    r = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            r[e1 + e2] = r.get(e1 + e2, 0) + c1 * c2
    return {e: c for e, c in r.items() if c != 0}


def pdiff(a):
    r = {}
    for e, c in a.items():
        if e > 0:
            r[e - 1] = r.get(e - 1, 0) + e * c
    return {e: c for e, c in r.items() if c != 0}


def pexpand(a, fn=expand):
    r = {}
    for e, c in a.items():
        v = fn(c)
        if v != 0:
            r[e] = v
    return r


def bracket(P, Q):
    """P, Q as dicts {(i,j): coeff}. Returns {P,Q} as dict {(i,j): coeff}."""
    def dx(F):
        return {(i - 1, j): i * c for (i, j), c in F.items() if i > 0}

    def dy(F):
        return {(i, j - 1): j * c for (i, j), c in F.items() if j > 0}

    def mul(A, B):
        r = {}
        for ka, ca in A.items():
            for kb, cb in B.items():
                k = (ka[0] + kb[0], ka[1] + kb[1])
                r[k] = r.get(k, 0) + ca * cb
        return r

    out = {}
    for k, c in mul(dx(P), dy(Q)).items():
        out[k] = out.get(k, 0) + c
    for k, c in mul(dy(P), dx(Q)).items():
        out[k] = out.get(k, 0) - c
    return {k: expand(c) for k, c in out.items() if expand(c) != 0}


class Cascade:
    """P given as list Pd[j] = dict{xexp: coeff}; R as list Rr[m] = dict."""

    def __init__(self, Pd, Rr, p10):
        self.Pd = Pd
        self.Rr = Rr
        self.p10 = p10          # = Pd[0][1], a nonzero constant
        self.Q = [{}]           # Q_0 = 0

    def step(self, m):
        """Compute Q_{m+1} from Q_0..Q_m."""
        acc = dict(self.Rr[m]) if m < len(self.Rr) else {}
        for i in range(1, len(self.Pd)):
            k = m + 1 - i
            if k < 0 or k >= len(self.Q):
                continue
            Pi = self.Pd[i]
            if not Pi:
                continue
            Qk = self.Q[k]
            if not Qk:
                continue
            acc = padd(acc, pscal(pmul(Pi, pdiff(Qk)), i))
            acc = padd(acc, pscal(pmul(pdiff(Pi), Qk), -k))
        Qnext = pscal(acc, Rational(1, m + 1) / self.p10)
        self.Q.append(pexpand(Qnext))
        return self.Q[m + 1]
