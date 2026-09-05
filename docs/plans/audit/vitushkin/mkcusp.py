"""Impose a (2,k)-cusp of the parametrised curve (a(t), b(t)) at a critical parameter t0 of a
(a'(t0) = 0, a''(t0) != 0) by linear conditions on the coefficients of b."""
import sympy as sp
t = sp.symbols('t')
def cusp_conditions(a, b, t0, k):
    """Return linear expressions (in b's symbolic coefficients) that vanish iff the branch at t0 is a (2,k')-cusp with k' >= k."""
    s = sp.symbols('s_')
    N = k + 1
    u = sp.expand(sp.series(a.subs(t, t0 + s) - a.subs(t, t0), s, 0, N).removeO())
    v = sp.expand(sp.series(b.subs(t, t0 + s) - b.subs(t, t0), s, 0, N).removeO())
    conds = [v.coeff(s, 1)]           # b'(t0) = 0
    alpha2 = u.coeff(s, 2)
    assert alpha2 != 0
    # successively kill even powers of v with powers of u; odd coefficients below k must vanish
    for j in range(1, (k - 1)//2 + 1):
        # kill s^(2j) term using u^j (leading coefficient alpha2^j)
        c = v.coeff(s, 2*j) / alpha2**j
        v = sp.expand(v - c * sp.expand(u**j))
        v = sum(v.coeff(s, i) * s**i for i in range(N))
        if 2*j + 1 < k:
            conds.append(v.coeff(s, 2*j + 1))
    return conds
def build(a, beta, cusps, extra_vals):
    """cusps: list of (t0, k).  Returns b of degree beta with those cusp types (generic otherwise)."""
    cs = sp.symbols('c1:%d' % (beta + 1))
    b = sum(c * t**(i+1) for i, c in enumerate(cs))
    eqs = []
    for t0, k in cusps:
        eqs += cusp_conditions(a, b, t0, k)
    eqs = [sp.expand(e) for e in eqs]
    sol = list(sp.linsolve(eqs, cs))
    if not sol: return None
    sol = sol[0]
    free = sorted(set().union(*[e.free_symbols for e in sol]), key=str)
    vals = dict(zip(free, extra_vals))
    bb = sp.expand(b.subs(dict(zip(cs, sol))).subs(vals))
    if sp.Poly(bb, t).degree() != beta: return None
    return bb
if __name__ == '__main__':
    R = sp.Rational
    a4 = t**4 - 2*t**2
    print(build(a4, 5, [(1, 5), (-1, 5), (0, 3)], [1, 2, 3, 5, 7]))
    print(build(a4, 5, [(1, 7), (-1, 3), (0, 3)], [1, 2, 3, 5, 7]))
    a3 = t**3 - 3*t
    print(build(a3, 5, [(1, 5), (-1, 3)], [1, 2, 3, 5, 7]), ' (should match the c35_25 family)')
