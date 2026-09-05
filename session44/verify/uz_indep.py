#!/usr/bin/env python3
"""(u,z) form of subcase 2, derived here from scratch and CROSS-CHECKED
against the direct (x,y) bracket of indep2.py.

Change of variables u = x y^2, z = 1/y.  Then x = u z^2, y = 1/z and
    d(u,z)/d(x,y) = det [[y^2, 2xy],[0, -y^-2]] = -1,
so  [P,Q]_{x,y} = - [P,Q]_{u,z}  and the target x^2 = u^2 z^4 gives

        [P,Q]_{u,z} = - u^2 z^4 .

With  w = j - 2i  taking values {0,-1,-2} on N(P) and {0,-1,-2,-3} on N(Q)
(verified by indep2.py) the monomial x^i y^j = u^i z^(2i-j) = u^i z^(-w), so

    P = f(u) + p(u) z + q(u) z^2
    Q = g(u) + r(u) z + s(u) z^2 + t(u) z^3

and expanding P_u Q_z - P_z Q_u by powers of z gives, by hand,

  z^0 :  f'r - p g'                                       = 0
  z^1 :  2f's + p'r - p r' - 2q g'                        = 0
  z^2 :  3f't + 2p's + q'r - p s' - 2q r'                 = 0
  z^3 :  3p't + 2q's - p t' - 2q s'                       = 0
  z^4 :  3q't - 2q t'                                     = -u^2

The last is the ESSENTIAL FACE equation 2 q t' - 3 q' t = u^2.

Nothing here is taken from any other script: the supports come from the
lattice-point enumeration in indep2.py and the five identities are
re-derived above.  main() checks the whole thing against a direct (x,y)
bracket on random data before anything is concluded from it.
"""
import random, sys
import sympy as sp

from indep2 import poly_points, NP, NQ

u = sp.Symbol("u")
x, y = sp.symbols("x y")

def supports():
    """layer -> sorted list of u-exponents, from the polygon points."""
    lay = {}
    for tag, pts in (("P", poly_points(NP)), ("Q", poly_points(NQ))):
        for (i, j) in pts:
            m = 2 * i - j                     # power of z
            lay.setdefault((tag, m), []).append(i)
    return {k: sorted(v) for k, v in lay.items()}

def build():
    S = supports()
    names = {0: "f", 1: "p", 2: "q"}
    namesQ = {0: "g", 1: "r", 2: "s", 3: "t"}
    coef, poly = {}, {}
    for m, nm in names.items():
        cs = {k: sp.Symbol(f"{nm}{k}") for k in S[("P", m)]}
        coef[nm] = cs
        poly[nm] = sum(c * u**k for k, c in cs.items())
    for m, nm in namesQ.items():
        cs = {k: sp.Symbol(f"{nm}{k}") for k in S[("Q", m)]}
        coef[nm] = cs
        poly[nm] = sum(c * u**k for k, c in cs.items())
    return coef, poly, S

def identities(poly):
    f, p, q = poly["f"], poly["p"], poly["q"]
    g, r, s, t = poly["g"], poly["r"], poly["s"], poly["t"]
    d = lambda e: sp.diff(e, u)
    return [
        d(f) * r - p * d(g),
        2 * d(f) * s + d(p) * r - p * d(r) - 2 * q * d(g),
        3 * d(f) * t + 2 * d(p) * s + d(q) * r - p * d(s) - 2 * q * d(r),
        3 * d(p) * t + 2 * d(q) * s - p * d(t) - 2 * q * d(s),
        3 * d(q) * t - 2 * q * d(t) + u**2,
    ]

def crosscheck(seed=0, prime=1000003):
    """Random-data check: build P,Q in (x,y) from the SAME coefficients and
    verify  [P,Q]_{x,y} - x^2  vanishes exactly when all five (u,z)
    identities vanish -- by comparing the two polynomials coefficient by
    coefficient after substituting u = x y^2 back."""
    coef, poly, S = build()
    rng = random.Random(seed)
    val = {}
    for nm, cs in coef.items():
        for k, c in cs.items():
            val[c] = rng.randrange(1, prime)
    # (x,y) side
    lay = {"f": 0, "p": 1, "q": 2, "g": 0, "r": 1, "s": 2, "t": 3}
    P = sum(val[c] * x**k * y**(2 * k - lay[nm])
            for nm in ("f", "p", "q") for k, c in coef[nm].items())
    Q = sum(val[c] * x**k * y**(2 * k - lay[nm])
            for nm in ("g", "r", "s", "t") for k, c in coef[nm].items())
    br = sp.expand(sp.diff(P, x) * sp.diff(Q, y)
                   - sp.diff(P, y) * sp.diff(Q, x) - x**2)
    # (u,z) side: sum_m  E_m(u) * z^m  with the sign  [.,.]_{x,y} = -[.,.]_{u,z}
    E = [sp.expand(e.subs(val)) for e in identities(poly)]
    rebuilt = 0
    for m, Em in enumerate(E):
        pe = sp.Poly(Em, u)
        for (k,), c in pe.terms():
            rebuilt += c * x**k * y**(2 * k - m)
    rebuilt = sp.expand(rebuilt)
    # [P,Q]_{x,y} = -[P,Q]_{u,z}, so the two sides must be NEGATIVES
    diff = sp.expand(br + rebuilt)
    return diff, br

if __name__ == "__main__":
    coef, poly, S = build()
    print("layer supports (u-exponents):")
    for nm in ("f", "p", "q", "g", "r", "s", "t"):
        ks = sorted(coef[nm].keys())
        print(f"   {nm}: {len(ks):2d} coefficients, u-exponents "
              f"{ks[0]}..{ks[-1]}")
    tot = sum(len(coef[nm]) for nm in coef)
    print(f"total coefficients: {tot}")
    ok = True
    for seed in range(3):
        diff, br = crosscheck(seed)
        good = (diff == 0)
        ok &= good
        print(f"  seed {seed}: direct (x,y) bracket == rebuilt (u,z) "
              f"identities -> {good}")
    print(f"CROSSCHECK: {'PASS' if ok else 'FAIL'}")
