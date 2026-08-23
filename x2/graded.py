"""
Graded reduction of  {P,Q} = x^2  on a NARROW-STRIP Newton polygon.

Target p108_525122 (GGHV (72,108), (8,28)-orientation, bracket x^2):
supp(P) lies in the strip  0 <= 2a - j <= 2  and supp(Q) in  0 <= 2b - k <= 3,
where (a,j) / (b,k) are (x-exponent, y-exponent).

Grade by  rho = 2*(x-exp) - (y-exp).  Writing the rho-piece of P as
    P_rho = y^{-rho} f_rho(T),      T = x y^2
(and likewise Q_sigma = y^{-sigma} g_sigma(T)) one computes

    {P_rho, Q_sigma} = y^{1-rho-sigma} * ( rho * f_rho g_sigma'
                                         - sigma * f_rho' g_sigma )

so the whole 2-variable problem collapses to a triangular system of
ONE-VARIABLE equations.  x^2 = y^{-4} T^2 sits in rho+sigma = 5.
"""
import sympy as sp

T = sp.Symbol('T')


def poly_from_coeffs(coeffs, start=0):
    return sum(c * T**(start + i) for i, c in enumerate(coeffs))


def brk(rho, f, sigma, g):
    """rho*f*g' - sigma*f'*g."""
    return sp.expand(rho * f * sp.diff(g, T) - sigma * sp.diff(f, T) * g)


def level(fs, gs, s):
    """Sum over rho+sigma = s of brk(rho,f_rho,sigma,g_sigma)."""
    tot = 0
    for rho, f in fs.items():
        sigma = s - rho
        if sigma in gs:
            tot += brk(rho, f, sigma, gs[sigma])
    return sp.expand(tot)
