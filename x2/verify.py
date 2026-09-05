"""Cross-validation of the graded reduction against direct 2-variable algebra.

(1) identity   {y^-rho f(T), y^-sigma g(T)} = y^(1-rho-sigma) (rho f g' - sigma f' g),
    T = x y^2, checked on random polynomials.
(2) the coefficientwise forms E1..E5 in gsys.py, checked against the direct
    2-variable Poisson bracket of the assembled P and Q.
"""
import random, sys
import sympy as sp
sys.path.insert(0, '/home/user/jacobian_planar/x2')
import gsys, cascade

x, y, T = sp.symbols('x y T')
R = sp.Rational


def as_xy(coeffs, start, rho):
    """y^-rho * sum coeffs[i] T^(start+i),  T = x y^2  -> sympy expr in x,y."""
    e = 0
    for i, c in enumerate(coeffs):
        n = start + i
        e += c * x**n * y**(2 * n - rho)
    return sp.expand(e)


def pb(f, g):
    return sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x))


def check_identity():
    ok = True
    for rho in range(0, 4):
        for sigma in range(0, 4):
            fc = [R(random.randint(-5, 5)) for _ in range(4)]
            gc = [R(random.randint(-5, 5)) for _ in range(4)]
            # use start large enough that y-powers stay non-negative
            P = as_xy(fc, 3, rho)
            Q = as_xy(gc, 3, sigma)
            f = sum(c * T**(3 + i) for i, c in enumerate(fc))
            g = sum(c * T**(3 + i) for i, c in enumerate(gc))
            pred = rho * f * sp.diff(g, T) - sigma * sp.diff(f, T) * g
            pred = sp.expand(pred)
            predxy = 0
            for n, c in sp.Poly(pred, T).terms():
                predxy += c * x**n[0] * y**(2 * n[0] + 1 - rho - sigma)
            d = sp.expand(pb(P, Q) - sp.expand(predxy))
            if d != 0:
                ok = False
                print("IDENTITY FAIL", rho, sigma, d)
    print("(1) graded bracket identity:", "PASS" if ok else "FAIL")
    return ok


def check_levels(seed=1):
    """Assemble random P and (random) Q from graded slices and check that the
    coefficientwise E1..E5 residuals equal the corresponding graded pieces of
    {P,Q} - x^2."""
    random.seed(seed)
    F = [R(1)] + [R(random.randint(-4, 4)) for _ in range(gsys.dF)]
    A = [R(random.randint(-4, 4)) for _ in range(gsys.dA + 1)]
    B = [R(random.randint(-4, 4)) for _ in range(gsys.dB + 1)]
    out = gsys.all_residuals(F, A, B, zero=R(0))
    G, G2, G1, G0 = out['G'], out['G2'], out['G1'], out['G0']

    f2 = as_xy(F, 1, 2)          # rho = 2 :  y^-2 * T*F  -> sum F_i x^{1+i} y^{2i}
    f1 = as_xy(A, 1, 1)
    f0 = as_xy(B, 0, 0)
    g3 = as_xy(G, 2, 3)
    g2 = as_xy(G2, 2, 2)
    g1 = as_xy(G1, 1, 1)
    g0 = as_xy(G0, 1, 0)
    P = sp.expand(f0 + f1 + f2)
    Q = sp.expand(g0 + g1 + g2 + g3)
    br = sp.expand(pb(P, Q) - x**2)

    # split br by rho = 2a - j and compare with the residual lists
    pieces = {}
    for mono, c in sp.Poly(br, x, y).terms():
        a, j = mono
        pieces.setdefault(2 * a - j, {})[a] = c

    def cmp(name, res, rho_level, start_n):
        # res[k] should be the coefficient of T^(start_n+k) in the level
        got = pieces.get(rho_level, {})
        exp = {}
        for k, v in enumerate(res):
            if v != 0:
                exp[start_n + k] = v
        same = got == exp
        print(f"    {name}: level rho={rho_level} match={same}"
              + ("" if same else f"\n      direct={got}\n      gsys ={exp}"))
        return same

    ok = True
    ok &= cmp('E1', out['r1'], 4, 13)
    ok &= cmp('E2', out['r2'], 3, 13)
    ok &= cmp('E3', out['r3'], 2, 13)
    ok &= cmp('E4', out['r4'], 1, 13)
    ok &= cmp('E5', out['r5'], 0, 0)
    print("(2) coefficientwise levels:", "PASS" if ok else "FAIL")
    return ok


if __name__ == '__main__':
    a = check_identity()
    b = check_levels()
    print("OVERALL:", "PASS" if (a and b) else "FAIL")
