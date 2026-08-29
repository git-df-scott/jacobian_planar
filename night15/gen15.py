"""night15 -- the screening corpus: certified gradient-unimodular P.

DERIVATIONS (each one is carried out here the way night14 derived F2's).

--------------------------------------------------------------------------
G1  THE v-POWER FAMILY   P = h0*v + c*(x-a)^n * v^m ,  v = y + t(x)/2
--------------------------------------------------------------------------
Write g = c*(x-a)^n and v_x = t'(x)/2.  Then

    P_y = h0 + m*g*v^(m-1)
    P_x = v_x*(h0 + m*g*v^(m-1)) + g'*v^m = v_x*P_y + g'*v^m

so ON the locus {P_y = 0} we have P_x = g'*v^m.  A common zero therefore
needs g' = 0 or v = 0.
  * v = 0  =>  P_y = h0 != 0.
  * g' = 0 =>  x = a (as g' = c*n*(x-a)^(n-1))  =>  g = 0  =>  P_y = h0 != 0.
So the critical locus is EMPTY for every m >= 1, n >= 1, h0 != 0, and every
t(x).  m = 2 recovers night14's F2; m = 3 is species S1 (v-cubic).

--------------------------------------------------------------------------
G1'  WHY THE MIXED v^2/v^3 MEMBER IS NOT UNIMODULAR (a derived negative)
--------------------------------------------------------------------------
Take P = h0*v + g1(x)*v^2 + g2(x)*v^3.  The same computation gives
    P_x = v_x*P_y + g1'*v^2 + g2'*v^3 = v_x*P_y + v^2*(g1' + g2'*v),
so on {P_y = 0} a critical point needs v = 0 (excluded as above) or
v = -g1'/g2'.  Substituting that v into P_y = h0 + 2*g1*v + 3*g2*v^2 gives a
rational function of x whose numerator is h0 * (denominator) + (a polynomial
that vanishes at x = a).  Concretely for g1 = gamma*(x-a)^n, g2 = delta*(x-a)^n
one gets v = -gamma/delta and

    P_y = h0 + (gamma^2/delta) * (x-a)^n ,

which has a root over C unless gamma = 0.  The same happens for n1 != n2
(e.g. n1 = 2, n2 = 1 gives P_y = h0 + (8*gamma^2/delta)*(x-a)^3).  So inside
this shape only the PURE v^m members are gradient-unimodular; the mixed ones
always acquire a critical point.  Recorded as a measurement, not a conclusion
about mixed families in general.

--------------------------------------------------------------------------
G2  THE MULTIPLE-ROOT FAMILY  P = alpha*x + beta + c*B(x)*y^m
    with B = prod (x - a_i)^(e_i),  every e_i >= 2,  alpha != 0
--------------------------------------------------------------------------
    P_y = c*m*B*y^(m-1),   P_x = alpha + c*B'*y^m.
{P_y = 0} = {B = 0} u {y = 0} (the latter only when m >= 2).
  * on {y = 0}: P_x = alpha != 0.
  * on {x = a_i}: B'(a_i) = 0 because a_i is a MULTIPLE root of B, so
    P_x = alpha != 0.
So the critical locus is EMPTY.  Several distinct a_i put several places at
infinity on the fibres (species S2): over each a_i the fibre has gcd(m, e_i)
places with y -> infinity, and over x = infinity it has gcd(m, deg B - 1).

--------------------------------------------------------------------------
G3  SHEARING (species S5, and an internal control)
--------------------------------------------------------------------------
If phi is a polynomial automorphism of A^2 with Jacobian 1 then P o phi is
gradient-unimodular exactly when P is (the gradient transforms by the
invertible Jacobian matrix), P o phi is a coordinate exactly when P is, and
the fibres of P o phi are ISOMORPHIC to those of P by a map pulling eta back
to eta (phi preserves dx ^ dy).  So the period verdict must be identical --
which is used below as an internal control, and the shear is used to
manufacture genuinely mixed Newton supports.
"""

import random
from fractions import Fraction as F

import pk15 as P14


def _shift_pow(a, n):
    """(x - a)^n as a univariate dict."""
    return P14.u_pow({1: F(1), 0: F(-a)} if a else {1: F(1)}, n)


def _upoly(rng, deg, lo=-3, hi=3):
    p = {}
    for i in range(deg + 1):
        c = rng.randint(lo, hi)
        if c:
            p[i] = F(c)
    return p


def v_poly(t):
    """v = y + t(x)/2 as a bivariate dict."""
    out = {(0, 1): F(1)}
    for i, c in t.items():
        out[(i, 0)] = out.get((i, 0), F(0)) + c / 2
    return P14.clean(out)


def G1(h0, c, a, n, m, t):
    """P = h0*v + c*(x-a)^n * v^m."""
    v = v_poly(t)
    g = P14.u_to_bi(P14.u_scal(c, _shift_pow(a, n)))
    P = P14.padd(P14.pscal(h0, v), P14.pmul(g, P14.ppow(v, m)))
    lab = "G1 h0=%s c=%s a=%s n=%d m=%d t=%s" % (h0, c, a, n, m, sorted(t.items()))
    return P, lab, {"h0": str(h0), "c": str(c), "a": str(a), "n": n, "m": m,
                    "t": {str(k): str(vv) for k, vv in t.items()}}


def G2(alpha, beta, c, roots, m):
    """P = alpha*x + beta + c*B(x)*y^m,  B = prod (x-a_i)^(e_i), e_i >= 2."""
    B = {0: F(1)}
    for a, e in roots:
        assert e >= 2
        B = P14.u_mul(B, _shift_pow(a, e))
    P = P14.padd({(1, 0): F(alpha), (0, 0): F(beta)},
                 P14.pmul(P14.u_to_bi(P14.u_scal(c, B)), {(0, m): F(1)}))
    lab = "G2 alpha=%s beta=%s c=%s B=%s m=%d" % (alpha, beta, c, roots, m)
    return P14.clean(P), lab, {"alpha": str(alpha), "beta": str(beta),
                               "c": str(c), "roots": [[str(a), e] for a, e in roots],
                               "m": m}


def shear(P, s_y, t_x):
    """P o phi with phi: (x, y) -> (x + s(y), y),  then (x, y) -> (x, y + t(x)).

    Both factors are triangular with Jacobian 1, so phi has Jacobian 1.
    """
    x = {(1, 0): F(1)}
    y = {(0, 1): F(1)}
    S = P14.padd(x, P14.clean({(0, i): cc for i, cc in s_y.items()}))
    out = {}
    for (i, j), cc in P.items():
        out = P14.padd(out, P14.pscal(cc, P14.pmul(P14.ppow(S, i), P14.ppow(y, j))))
    # now apply y -> y + t(x)
    Ty = P14.padd(y, P14.u_to_bi(t_x))
    res = {}
    for (i, j), cc in out.items():
        res = P14.padd(res, P14.pscal(cc, P14.pmul(P14.ppow(x, i), P14.ppow(Ty, j))))
    return P14.clean(res)




# ----------------------------------------------------------------- species

def species_of(P, meta):
    tags = []
    if meta.get("gen") == "G1":
        tags.append("S1_v_cubic" if meta["m"] == 3 else
                    ("v_quadratic" if meta["m"] == 2 else "v_power_m%d" % meta["m"]))
    if meta.get("gen") == "G2":
        tags.append("G2_multiple_root")
    if meta.get("sheared"):
        tags.append("S5_mixed_support")
    return tags


def corpus(seed=20260829, want=260):
    """The screening corpus.  Yields (P, label, meta)."""
    rng = random.Random(seed)
    out = []

    # ---- G1: the v-power family, degrees 3..30, m = 2 (F2 species) ------
    for m in (2, 3, 4, 5):
        for n in range(1, 13):
            for dt in (0, 1, 2, 3):
                t = _upoly(rng, dt)
                if dt and t.get(dt, 0) == 0:
                    t[dt] = F(rng.choice([1, -1, 2]))
                h0 = F(rng.choice([1, -1, 2, -3]))
                c = F(rng.choice([1, -1, 2, 3, -2]))
                a = F(rng.choice([0, 0, 1, -1, 2]))
                P, lab, par = G1(h0, c, a, n, m, t)
                d = P14.tdeg(P)
                if not (3 <= d <= 30):
                    continue
                par.update({"gen": "G1"})
                out.append((P, lab, par))

    # ---- G2: the multiple-root family (species S2) ----------------------
    for m in (1, 2, 3, 4):
        for roots in ([(F(0), 2)], [(F(0), 2), (F(1), 2)],
                      [(F(0), 2), (F(1), 3)],
                      [(F(0), 2), (F(1), 2), (F(-1), 2)],
                      [(F(0), 3), (F(2), 2)],
                      [(F(1), 4)], [(F(0), 2), (F(1), 2), (F(-1), 2), (F(2), 2)]):
            alpha = F(rng.choice([1, -1, 2]))
            beta = F(rng.choice([0, 0, 1, -1]))
            c = F(rng.choice([1, -1, 2, 3]))
            P, lab, par = G2(alpha, beta, c, roots, m)
            d = P14.tdeg(P)
            if not (3 <= d <= 30):
                continue
            par.update({"gen": "G2"})
            out.append((P, lab, par))

    # ---- S4: fibres with >= 3 irreducible components --------------------
    # P = -v + (x-a)^2 v^3 : the zero fibre is v * ((x-a)v - 1) * ((x-a)v + 1)
    # P = -v + (x-a)^4 v^5 : v * ((x-a)v-1) * ((x-a)v+1) * ((x-a)^2 v^2 + 1)
    for (n, m) in ((2, 3), (4, 5), (2, 3), (6, 7)):
        for dt in (0, 1, 2):
            t = _upoly(rng, dt)
            P, lab, par = G1(F(-1), F(1), F(rng.choice([0, 1, -1])), n, m, t)
            d = P14.tdeg(P)
            if not (3 <= d <= 30):
                continue
            par.update({"gen": "G1", "s4_intent": True})
            out.append((P, lab + " [S4 intent]", par))

    # ---- S5: sheared copies (genuinely mixed Newton supports) -----------
    base = list(out)
    rng2 = random.Random(seed + 1)
    for k in range(28):
        P0, lab0, par0 = base[rng2.randrange(len(base))]
        s_y = _upoly(rng2, rng2.randint(1, 2))
        t_x = _upoly(rng2, rng2.randint(1, 2))
        if not s_y and not t_x:
            continue
        P = shear(P0, s_y, t_x)
        d = P14.tdeg(P)
        if not (3 <= d <= 30):
            continue
        par = dict(par0)
        par.update({"sheared": True, "base_label": lab0,
                    "s_y": {str(a): str(b) for a, b in s_y.items()},
                    "t_x": {str(a): str(b) for a, b in t_x.items()}})
        out.append((P, lab0 + " | sheared", par))

    # dedupe by hash
    seen = set()
    uniq = []
    for P, lab, par in out:
        hh = P14.phash(P)
        if hh in seen:
            continue
        seen.add(hh)
        uniq.append((P, lab, par))
    return uniq[:want]
