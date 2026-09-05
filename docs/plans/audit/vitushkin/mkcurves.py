"""Construct polynomial curves with prescribed cusps and a tacnode, rational coefficients."""
import sympy as sp
from itertools import product
t = sp.symbols('t')
R = sp.Rational

def cubic_with_rational_cusps_and_pair():
    """a = t^3 + p t^2 + q t with a' having rational roots and a(1) = a(t2) for rational t2 != 1, t2 not a root of a'."""
    out = []
    for p in range(-6, 7):
        for t2n in range(-8, 9):
            for t2d in (1, 2, 3):
                t2 = R(t2n, t2d)
                if t2 == 1: continue
                q = -(1 + t2 + t2**2 + p*(1 + t2))
                disc = 4*p**2 - 12*q
                if disc < 0: continue
                s = sp.sqrt(disc)
                if not s.is_rational: continue
                r1, r2 = (-2*p + s)/6, (-2*p - s)/6
                if r1 == r2 or 1 in (r1, r2) or t2 in (r1, r2): continue
                out.append((p, q, t2, r1, r2))
    return out

def b_with_conditions(a, beta, cusps, tacpairs, extra=()):
    """b of degree beta: b'(c) = 0 at cusps; for (t1,t2): b(t1)=b(t2) and tangents parallel."""
    cs = sp.symbols('c1:%d' % (beta + 1))
    b = sum(c * t**(i+1) for i, c in enumerate(cs))
    eqs = []
    for c in cusps:
        eqs.append(sp.diff(b, t).subs(t, c))
    ap = sp.diff(a, t)
    for (t1, t2) in tacpairs:
        eqs.append(b.subs(t, t1) - b.subs(t, t2))
        eqs.append(sp.diff(b, t).subs(t, t1) * ap.subs(t, t2) - sp.diff(b, t).subs(t, t2) * ap.subs(t, t1))
    eqs += list(extra)
    sol = sp.linsolve(eqs, cs)
    sols = list(sol)
    if not sols: return None
    s = sols[0]
    free = sorted(set().union(*[e.free_symbols for e in s]) - {t}, key=str)
    # substitute generic rational values for free parameters
    u, v = sp.symbols('u v')
    for trial in range(8):
        vals = {f: R(3*i + 2 + 5*trial, 7*i + 3) for i, f in enumerate(free)}
        bb = sp.expand(b.subs(dict(zip(cs, s))).subs(vals))
        if sp.Poly(bb, t).degree() != beta: continue
        import numpy as np
        u0 = 0.37 + 0.61j
        ts = np.roots([complex(x) for x in sp.Poly(a - u0, t).all_coeffs()])
        vs = [complex(bb.subs(t, tr)) for tr in ts]
        if min(abs(vs[i] - vs[j]) for i in range(len(vs)) for j in range(i)) < 1e-6: continue
        return bb
    return None

if __name__ == '__main__':
    for p, q, t2, r1, r2 in cubic_with_rational_cusps_and_pair()[:8]:
        a = t**3 + p*t**2 + q*t
        b = b_with_conditions(a, 6, [r1, r2], [(1, t2)])
        print(p, q, t2, r1, r2, a, b)
