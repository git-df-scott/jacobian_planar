"""night14 -- candidate families F1, F2, F2b, F3, F4.

Every generator returns (family, label, P) with P a dict {(i,j): Fraction}.
The F2/F2b constructions follow the derivation in PROSPECTOR.md section 2.
"""

import random
from fractions import Fraction as F
import poly14 as P14

U = P14  # univariate helpers live in poly14 as u_*


def _ux(coeffs):
    """univariate poly from a list of (exponent, coeff)."""
    return {i: F(c) for i, c in coeffs if F(c) != 0}


def _rand_upoly(rng, deg, lo=-3, hi=3, allow_zero=True):
    d = rng.randint(0, deg)
    p = {}
    for i in range(d + 1):
        c = rng.randint(lo, hi)
        if c:
            p[i] = F(c)
    if not p and not allow_zero:
        p = {0: F(1)}
    return p


def _gyk_to_P(g, h, k):
    """P = g(x)*y^2 + h(x)*y + k(x)."""
    out = {}
    for i, c in g.items():
        out[(i, 2)] = out.get((i, 2), F(0)) + c
    for i, c in h.items():
        out[(i, 1)] = out.get((i, 1), F(0)) + c
    for i, c in k.items():
        out[(i, 0)] = out.get((i, 0), F(0)) + c
    return P14.clean(out)


def _shift_x(u, a):
    """substitute x -> x - a in a univariate poly (a in Q)."""
    out = {}
    for i, c in u.items():
        # (x - a)^i
        term = P14.u_pow({1: F(1), 0: F(-a)} if a else {1: F(1)}, i)
        out = P14.u_add(out, P14.u_scal(c, term))
    return out


# ------------------------------------------------------------------- F2 (D const)

def gen_F2(rng):
    """g = c*(x-a)^n, h = h0 + g*t, k = (2*h0*t + g*t^2)/4  ->  D = h0^2 const.

    Derived consequence: critical locus empty for every n >= 1.
    """
    n = rng.randint(1, 4)
    c = F(rng.choice([1, -1, 2, 3, -2]))
    a = F(rng.choice([0, 0, 0, 1, -1, 2]))
    h0 = F(rng.choice([1, -1, 2, -3]))
    t = _rand_upoly(rng, rng.randint(0, 3))
    g = P14.u_scal(c, _shift_x({n: F(1)}, a))
    h = P14.u_add({0: h0}, P14.u_mul(g, t))
    k = P14.u_scal(F(1, 4), P14.u_add(P14.u_scal(2 * h0, t), P14.u_mul(g, P14.u_mul(t, t))))
    P = _gyk_to_P(g, h, k)
    lab = "F2 n=%d c=%s a=%s h0=%s t=%s" % (n, c, a, h0, sorted(t.items()))
    # 4g(P - lam) = (2gy+h)^2 - (D + 4g*lam); D = h0^2 is constant, so the
    # square (and hence the reducible fibre) occurs at lam = 0.
    return ("F2", lab, P, [F(0)])


# ------------------------------------------------------------------ F2b (D nonconst)

def gen_F2b(rng):
    """g = c*x^n, h = h0 + x^n*s, k = (2*h0*s + x^n*s^2 - d_n)/(4c)
       ->  D = h0^2 + d_n*x^n, nonconstant when d_n != 0.

    Derived consequence: R = g'D - g D' = c*n*h0^2*x^(n-1), all roots at 0,
    a root of g; and D(0) = h0^2 != 0 kills the g = 0 branch.  So the critical
    locus is empty for every n >= 1 here too.
    """
    n = rng.randint(1, 5)
    c = F(rng.choice([1, -1, 2]))
    h0 = F(rng.choice([1, -1, 2]))
    dn = F(rng.choice([1, -1, 2, 3, -2]))
    s = _rand_upoly(rng, rng.randint(0, 3))
    g = P14.u_scal(c, {n: F(1)})
    h = P14.u_add({0: h0}, P14.u_mul({n: F(1)}, s))
    k = P14.u_scal(F(1, 1) / (4 * c),
                   P14.u_add(P14.u_scal(2 * h0, s),
                             P14.u_mul({n: F(1)}, P14.u_mul(s, s)),
                             {0: -dn}))
    P = _gyk_to_P(g, h, k)
    lab = "F2b n=%d c=%s h0=%s d_n=%s s=%s" % (n, c, h0, dn, sorted(s.items()))
    # D + 4g*lam = h0^2 + (d_n + 4c*lam)*x^n is a perfect square exactly at
    # lam = -d_n/(4c); that is where the fibre splits.
    return ("F2b", lab, P, [-dn / (4 * c), F(0)])


def f2_discriminant(P):
    """D = h^2 - 4*g*k recovered from P (assumes deg_y P <= 2)."""
    g = {i: c for (i, j), c in P.items() if j == 2}
    h = {i: c for (i, j), c in P.items() if j == 1}
    k = {i: c for (i, j), c in P.items() if j == 0}
    return P14.u_add(P14.u_mul(h, h), P14.u_scal(-4, P14.u_mul(g, k)))


# ------------------------------------------------------------------------ F1

def gen_F1(rng):
    """top form with 2+ distinct non-associate irreducible factors, plus
    lower-order terms."""
    facs = []
    pool = [({(1, 0): F(1)}, "x"), ({(0, 1): F(1)}, "y"),
            ({(1, 0): F(1), (0, 1): F(1)}, "(x+y)"),
            ({(1, 0): F(1), (0, 1): F(-1)}, "(x-y)"),
            ({(2, 0): F(1), (0, 2): F(1)}, "(x^2+y^2)")]
    picks = rng.sample(range(len(pool)), rng.randint(2, 3))
    names = []
    top = {(0, 0): F(1)}
    for i in picks:
        e = rng.randint(1, 2)
        top = P14.pmul(top, P14.ppow(pool[i][0], e))
        names.append(pool[i][1] + ("^%d" % e if e > 1 else ""))
    d = P14.tdeg(top)
    low = {}
    for _ in range(rng.randint(1, 4)):
        i = rng.randint(0, d - 1)
        j = rng.randint(0, max(0, d - 1 - i))
        c = rng.randint(-3, 3)
        if c:
            low[(i, j)] = low.get((i, j), F(0)) + c
    P = P14.padd(top, P14.clean(low))
    return ("F1", "F1 top=%s + %d low terms" % ("*".join(names), len(low)), P)


# ------------------------------------------------------------------------ F3

def gen_F3(rng):
    """near-coordinate twists: u + u^m * w and triangular images of x."""
    kind = rng.randint(0, 2)
    x = {(1, 0): F(1)}
    y = {(0, 1): F(1)}
    if kind == 0:
        # P = u + u^m * w  with u, w a coordinate pair (x, y) up to a shear
        sh = _rand_upoly(rng, rng.randint(1, 3))
        u = P14.padd(x, {})  # u = x
        w = P14.padd(y, P14.u_to_bi(sh))  # w = y + f(x)
        m = rng.randint(2, 4)
        P = P14.padd(u, P14.pmul(P14.ppow(u, m), w))
        lab = "F3 u+u^%d*w, w=y+f(x) deg f=%d" % (m, P14.u_deg(sh))
    elif kind == 1:
        # triangular image of a coordinate: x -> x + f(y), then P = x + g(y)
        f = _rand_upoly(rng, rng.randint(1, 3))
        fb = P14.clean({(0, i): c for i, c in f.items()})
        g = _rand_upoly(rng, rng.randint(1, 4))
        gb = P14.clean({(0, i): c for i, c in g.items()})
        P = P14.padd(x, fb, gb)
        lab = "F3 triangular x + f(y) + g(y)"
    else:
        # perturbed coordinate: x + y^k + small correction
        k = rng.randint(2, 5)
        P = P14.padd(x, {(0, k): F(1)},
                     {(rng.randint(1, 2), rng.randint(1, 2)): F(rng.choice([1, -1, 2]))})
        lab = "F3 x + y^%d + correction" % k
    return ("F3", lab, P)


# ------------------------------------------------------------------------ F4

def gen_F4(rng):
    """random sparse with a linear term (background)."""
    P = {(1, 0): F(rng.choice([1, -1, 2]))}
    for _ in range(rng.randint(2, 5)):
        i = rng.randint(0, 5)
        j = rng.randint(0, 5)
        if i + j == 0:
            continue
        c = rng.randint(-3, 3)
        if c:
            P[(i, j)] = P.get((i, j), F(0)) + c
    return ("F4", "F4 random sparse (%d terms)" % len(P), P14.clean(P))


def gen_F1b(rng):
    """F1 done constructively: top form a monomial with two distinct
    irreducible factors, lower terms tuned so that the critical locus is empty.

    Two-term member P = c1*x + c2*x^(m+1)*y^n (m >= 1, n >= 1): the top form
    c2*x^(m+1)*y^n has the two distinct irreducible factors x and y (two places
    at infinity), and P_y = c2*n*x^(m+1)*y^(n-1) vanishes only on {x = 0} and
    (for n >= 2) {y = 0}, where P_x = c1 + c2*(m+1)*x^m*y^n equals c1 != 0.  So
    the two-term member has empty critical locus by derivation.

    The optional extra term is a genuine perturbation, NOT covered by that
    derivation: it can give P_y a further nonconstant factor whose zero locus
    meets {P_x = 0} (measured: the perturbed members are the U-test failures of
    this family).
    """
    m = rng.randint(1, 4)
    n = rng.randint(1, 4)
    c1 = F(rng.choice([1, -1, 2, 3]))
    c2 = F(rng.choice([1, -1, 2, -3]))
    P = {(1, 0): c1, (m + 1, n): c2}
    # optional extra term, still divisible by x^2*y so it cannot revive a
    # critical point on {x = 0} or {y = 0}
    if rng.random() < 0.5:
        i, j = rng.randint(2, 4), rng.randint(1, 3)
        P[(i, j)] = P.get((i, j), F(0)) + F(rng.choice([1, -1, 2]))
    P = P14.clean(P)
    lab = "F1b c1*x + c2*x^%d*y^%d (+extra), top form has factors x and y" % (m + 1, n)
    return ("F1b", lab, P, [F(0)])


GENERATORS = {"F2": gen_F2, "F2b": gen_F2b, "F1": gen_F1, "F1b": gen_F1b,
              "F3": gen_F3, "F4": gen_F4}
