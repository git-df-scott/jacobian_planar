"""
The mu = 1 strip:  P = f0(xy) + x*phi(xy),  Q = g0(xy) + x*psi(xy).

With T = xy the graded equations (rho,sigma in {0,1}, level rho+sigma = 2
carries x^2 = T^2 y^-2) are

    level 2 :  f1 g1' - f1' g1 = T^2            (f1 = T*phi, g1 = T*psi)
    level 1 :  f1 g0' - f0' g1 = 0

and  W(T*phi, T*psi) = T^2 * W(phi,psi), so the whole system is

    (i)  W(phi, psi) = phi psi' - phi' psi = 1
    (ii) phi | f0'   and   g0' = (f0'/phi) * psi.

(i) is the classical "constant Wronskian" condition: psi exists for phi iff
int dT/phi^2 is rational, i.e. phi is an Adler-Moser polynomial.
"""
import sympy as sp

T = sp.Symbol('T')
x, y = sp.symbols('x y')


def psi_for(phi, dpsi=None):
    """All psi with W(phi,psi) = 1 (deg psi <= dpsi). Returns (particular, homogeneous basis)."""
    m = sp.degree(phi, T)
    if dpsi is None:
        dpsi = m
    cs = sp.symbols(f'z0:{dpsi+1}')
    psi = sum(cs[i] * T**i for i in range(dpsi + 1))
    W = sp.expand(phi * sp.diff(psi, T) - sp.diff(phi, T) * psi - 1)
    eqs = sp.Poly(W, T).all_coeffs()
    sol = sp.solve(eqs, cs, dict=True)
    return [sp.expand(psi.subs(s)) for s in sol]


def build(phi, psi, h, const=0):
    """f0' = phi*h  ->  f0 ;  g0' = h*psi -> g0.  Returns (P,Q) in x,y."""
    f0 = sp.integrate(sp.expand(phi * h), T) + const
    g0 = sp.integrate(sp.expand(h * psi), T)
    P = sp.expand(f0.subs(T, x * y) + x * phi.subs(T, x * y))
    Q = sp.expand(g0.subs(T, x * y) + x * psi.subs(T, x * y))
    return sp.expand(P), sp.expand(Q)


def bracket(P, Q):
    return sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))


def newton(P):
    d = sp.Poly(P, x, y).as_dict()
    return sorted(k for k, v in d.items() if v != 0)


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
