#!/usr/bin/env python3
"""The cascade with RATIONAL slices — every condition globally defined.

The exact-division cascade (build_N via pdiv_exact) is only DEFINED on the
variety where all earlier levels already hold: off it, pdiv_exact returns None
and the level-m condition does not exist.  That makes interpolation impossible
past level 5 and is why the naive per-level solves kept mis-reporting.

Fix: carry F's slices as rational functions with denominators powers of S, the
representation the formal-F proof uses anyway.  Because P_8 = a S^2 makes
F_12 = b S^3 polynomial, the ladder

    F_{12-m} = [ gamma (P^3)_{24-m} - sum_{0<k<m} F_{12-k} F_{12-(m-k)} ]
               / (2 b S^3)

needs NO exact division: dividing by 2 b S^3 just increments the denominator
exponent.  Each F_w is a pair (num, e) meaning num / S^e, defined for ALL
parameter values, and the conditions become polynomial identities:

    w = 11..0    S^e | num                     (F_w polynomial = Q_w)
                 and supp(F_w) inside qrange(w)
    w = -1       F_-1 polynomial, supported at i = 2 only  (vertex (2,1))
    w = -2..-9   F_w = 0                       (num = 0)
    w = -10      [P_8, F_-10] proportional to z^2, nonzero

The solution variety is unchanged; every condition is now a polynomial in the
parameters and is defined everywhere, so the system can be interpolated,
accumulated, and handed to Singular.
"""
import random, sys
from trackB1_sqrt import pmul, padd, pscal, ptrim, pderiv, prange
from trackB1_cascade_general import prem, half_radical, component1_S, component2_S
from trackB1_gauge_resolve import radd, rmul, rscal, rderiv, riszero

p = 65521

def qrange(w):
    lo, hi = max(0, -2 * w), min(12, w + 3)
    return (lo, hi) if lo <= hi and w <= 12 else None

def build_F(S, P, a=1, b=1, wmin=-10):
    """All F_w as rational pairs (num, e), w = 12 down to wmin."""
    gamma = (b * b % p) * pow(pow(a, 3, p), p - 2, p) % p
    P2, P3 = {}, {}
    for w1 in P:
        for w2 in P:
            P2[w1 + w2] = padd(P2.get(w1 + w2, []), pmul(P[w1], P[w2], p), p)
    for W2 in P2:
        for w3 in P:
            P3[W2 + w3] = padd(P3.get(W2 + w3, []), pmul(P2[W2], P[w3], p), p)
    s3 = pmul(pmul(S, S, p), S, p)
    F = {12: (pscal(s3, b, p), 0)}
    inv2b = pow(2 * b % p, p - 2, p)
    for m in range(1, 12 - wmin + 1):
        W = 24 - m
        N = (pscal(P3.get(W, []), gamma, p), 0)
        for k in range(1, m):
            if 12 - k in F and 12 - (m - k) in F:
                N = radd(N, rscal(rmul(F[12 - k], F[12 - (m - k)], p), -1, p),
                         S, p)
        F[12 - m] = (pscal(N[0], inv2b, p), N[1] + 3)
    return F

def spow(S, e, p):
    r = [1]
    for _ in range(e):
        r = pmul(r, S, p)
    return r

def conditions(S, P, a=1, b=1):
    """Return (label, [F_p equations]) per weight, in cascade order."""
    F = build_F(S, P, a, b)
    out = []
    for w in range(11, -2, -1):
        num, e = F[w]
        Se = spow(S, e, p)
        r = ptrim(list(prem(num, Se, p)))
        eqs = list(r)                       # polynomiality of F_w
        # support: after dividing out S^e the quotient must sit in qrange(w)
        out.append((f"poly_{w}", eqs))
    for w in range(-2, -10, -1):
        num, e = F[w]
        out.append((f"vanish_{w}", list(ptrim(list(num)))))
    return out, F

def support_eqs(S, F, w):
    """Equations saying F_w (already polynomial) is supported in qrange(w)."""
    from trackB1_sqrt import pdiv_exact
    num, e = F[w]
    Se = spow(S, e, p)
    q = pdiv_exact(num, Se, p)
    if q is None:
        return None
    r = qrange(w)
    if r is None:
        return list(ptrim(list(q)))
    lo, hi = r
    return [c for i, c in enumerate(q) if c and not (lo <= i <= hi)]

def bracket_bottom(S, F, a=1):
    """[P_8, F_-10] as a rational pair; C4 wants it proportional to z^2."""
    num, e = F[-10]
    P8 = (pscal(pmul(S, S, p), a, p), 0)
    t1 = rscal(rmul(rderiv(P8, S, p), (num, e), p), -10 % p, p)
    t2 = rscal(rmul(P8, rderiv((num, e), S, p), p), -8 % p, p)
    return radd(t1, t2, S, p)

def make_P(S, M, wl, params, lay, a=1):
    inv4a = pow(4 * a % p, p - 2, p)
    P = {8: pscal(pmul(S, S, p), a, p), 7: pmul(S, M, p)}
    H = half_radical(S, p)
    i = 0
    for w in wl:
        n = lay[w]
        vec = params[i:i + n]
        i += n
        if w == 6:
            dY = 3 - (len(H) - 1)
            Y = pmul(H, list(vec[:dY + 1]), p) if dY >= 0 else []
            Z = list(vec[dY + 1:])
            P[6] = ptrim(padd(padd(pscal(prem(pmul(M, M, p), S, p), inv4a, p),
                                   Y, p), pmul(S, Z, p), p))
        else:
            lo, hi = prange(w)
            P[w] = ptrim([0] * lo + list(vec))
    for w in range(6, -2, -1):
        P.setdefault(w, [])
    return P

def layout_for(S):
    H = half_radical(S, p)
    lay = {}
    for w in range(6, -2, -1):
        if w == 6:
            dY = 3 - (len(H) - 1)
            lay[6] = (dY + 1 if dY >= 0 else 0) + 5
        else:
            lo, hi = prange(w)
            lay[w] = hi - lo + 1
    return lay

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    tag = sys.argv[2] if len(sys.argv) > 2 else "I"
    rng = random.Random(seed)
    if tag == "I":
        A = [1, rng.randrange(p), rng.randrange(1, p)]
        S = component1_S(A, 1, p)
    else:
        S = None
        while S is None:
            u, v = rng.randrange(1, p), rng.randrange(1, p)
            S = component2_S(u, v, 1, p)
    M = [rng.randrange(p) for _ in range(5)]
    lay = layout_for(S)
    wl = [6, 5, 4, 3, 2, 1, 0, -1]
    nv = sum(lay[w] for w in wl)
    print(f"component {tag}: {nv} parameters, layout {lay}")
    print("Condition sizes at a RANDOM parameter point "
          "(all defined -- no None):")
    par = [rng.randrange(p) for _ in range(nv)]
    P = make_P(S, M, wl, par, lay)
    conds, F = conditions(S, P)
    tot = 0
    for label, eqs in conds:
        nz = len([c for c in eqs if c])
        tot += len(eqs)
        print(f"   {label:<12} {len(eqs):>3} eqs, {nz:>3} nonzero here")
    print(f"   TOTAL {tot} equations before support/C4")
    # sanity: on the witness family P = T^2 the ladder must be exactly satisfied
    print("\nsanity: P = Stilde^2 witness (ladder must hold identically)")
    t = 1
    Sw = [1, 0, 0, 0, 1]
    Pw = {8: pmul(Sw, Sw, p),
          7: [0, 0, 0, 0, 2 * t % p, 0, 0, 0, 2 * t % p],
          6: [0] * 8 + [t * t % p]}
    for w in range(5, -2, -1):
        Pw[w] = []
    cw, Fw = conditions(Sw, Pw)
    bad = [lab for lab, eqs in cw if any(eqs)]
    print(f"   conditions violated by the witness: {bad if bad else 'NONE'}")
    br = bracket_bottom(Sw, Fw)
    print(f"   witness bottom bracket numerator: "
          f"{'zero' if riszero(br) else 'nonzero'}  (expected zero)")
