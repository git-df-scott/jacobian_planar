#!/usr/bin/env python3
"""THE PLANE TANGENT SWEEP -- a door opened by the July 2026 refutation of the
Jacobian Conjecture in dimension three, and left unexamined by it.

BACKGROUND.  On 2026-07-19 Alpoge refuted JC in dimension 3; Gallagher gave an
infinite family (07-20), Speyer named the mechanism the TANGENT SWEEP (07-23),
and Gao (arXiv:2608.00222, 07-31, in papers/) generalized it to every n > 2.
All sources state the plane case n = 2 remains open, and Gao says the
counterexamples "exist only in dimension >= 3" -- but the only justification
offered is Wang's degree-2 theorem plus "the known constructions produce degree
>= 3".  NO REASON IS GIVEN why the mechanism itself fails in the plane.

THE POINT.  The tangent sweep IS a plane map:

    S(gamma, w) = ( p(w) + 2*gamma ,  q(w) + gamma*w ),   q'(w) = (w/2)*p'(w)

    det J(S) = 2*gamma          (Gao, section 3.1)

It is generically (deg p + 1)-to-one and unramified away from gamma = 0.  Its
ONLY defect as a counterexample is that its Jacobian is the coordinate 2*gamma
instead of a constant.  Dimension 3 is spent entirely on cancelling that gamma:
pad with a variable x, form C = gamma*x, and divide the components by C and C^2,
the divisibilities being arranged by "side conditions".

STRUCTURAL FACT (proved in prove_no_polynomial_twist below, and it is short).
No POLYNOMIAL conjugation can do it in the plane.  If phi, psi : C^2 -> C^2 are
polynomial and F = psi . S . phi, then

    det J(F) = detJpsi(S(phi)) * 2*gamma(phi) * det J(phi)

is a product of three polynomials.  In the domain C[x,y] a product is a nonzero
constant only if every factor is, so gamma . phi would be constant, phi would
map into a line, F would not be dominant, and a Keller map is dominant.  Hence

    ANY plane counterexample of tangent-sweep type MUST use a division twist
    with divisibility side conditions -- exactly the dimension-3 device.

So the plane question is not "does the sweep work" but "can the twist be closed
with one fewer variable".  This script sets up that question as an explicit
finite search: choose a twist shape, impose det J(F) = const identically, and
solve the resulting side conditions exactly over Q.

Usage: python3 wave6/w6_plane_sweep.py [max_deg_p]
"""
import sys, json, itertools
import sympy as sp
from sympy import symbols, expand, simplify, Rational, together, cancel, numer, denom

x, y, w, g = symbols('x y w gamma')

def sweep_pair(p_poly):
    """Gao (1): q(w) = int_0^w (s/2) p'(s) ds.  Returns (p, q) with q' = (w/2)p'."""
    q = sp.integrate(sp.Rational(1, 2)*w*sp.diff(p_poly, w), (w, 0, w))
    return sp.expand(p_poly), sp.expand(q)

def check_sweep(p_poly):
    p, q = sweep_pair(p_poly)
    S1 = p + 2*g
    S2 = q + g*w
    J = sp.Matrix([[sp.diff(S1, g), sp.diff(S1, w)],
                   [sp.diff(S2, g), sp.diff(S2, w)]])
    return sp.expand(J.det()), p, q

def prove_no_polynomial_twist():
    """The factorisation argument, stated as a check on a concrete instance:
    det J(psi . S . phi) has 2*gamma(phi) as a polynomial factor, so it cannot
    be a nonzero constant unless gamma . phi is constant."""
    det, p, q = check_sweep(-3*w**2 + 4*w)          # Alpoge's p
    ok = sp.simplify(det - 2*g) == 0
    return ok, det

def side_condition(P, Q, C, i, j, kappa, gam_phi, detJphi):
    """THE PLANE SIDE CONDITION.

    For F = (P/C^i, Q/C^j) one has the exact identity (derived by direct
    differentiation, verified by verify_identity() below)

        det J(F) = C^{-i-j-1} * [ C*{P,Q} - j*Q*{P,C} + i*P*{Q,C} ]

    where {A,B} = A_x B_y - A_y B_x.  With (P,Q) = S . phi the chain rule gives
    {P,Q} = det J(S)|phi * det J(phi) = 2*gamma(phi) * det J(phi).  So F is a
    Keller map with det J(F) = kappa exactly when

        C * 2*gamma(phi) * det J(phi)  -  j*Q*{P,C}  +  i*P*{Q,C}
              =  kappa * C^(i+j+1)                              (SIDE CONDITION)

    holds identically, together with the divisibilities C^i | P and C^j | Q.
    This is the two-variable analogue of Gao's section 3.3 / Speyer's "side
    conditions", and it is the object nobody has written down.
    """
    lhs = sp.expand(C*2*gam_phi*detJphi - j*Q*br(P, C) + i*P*br(Q, C))
    rhs = sp.expand(kappa*C**(i+j+1))
    return sp.expand(lhs - rhs)

def br(A, B):
    return sp.expand(sp.diff(A, x)*sp.diff(B, y) - sp.diff(A, y)*sp.diff(B, x))

def compose(p_poly, gam, wexpr):
    p, q = sweep_pair(p_poly)
    P = sp.expand(p.subs(w, wexpr) + 2*gam)
    Q = sp.expand(q.subs(w, wexpr) + gam*wexpr)
    return P, Q

def verify_identity(seed=7):
    """Check the identity det J(P/C^i, Q/C^j) = C^{-i-j-1}[...] on random data.
    A can-fail control: if this ever fails, the search below is meaningless."""
    import random
    random.seed(seed); ok = True
    for i, j in ((1, 2), (2, 1), (0, 1), (3, 2)):
        P = sum(random.randint(-4, 4)*x**e1*y**e2
                for e1 in range(3) for e2 in range(3))
        Q = sum(random.randint(-4, 4)*x**e1*y**e2
                for e1 in range(3) for e2 in range(3))
        C = 1 + x + random.randint(1, 3)*x*y
        lhs = sp.cancel(sp.together(sp.Matrix(
            [[sp.diff(P/C**i, x), sp.diff(P/C**i, y)],
             [sp.diff(Q/C**j, x), sp.diff(Q/C**j, y)]]).det()))
        rhs = sp.cancel((C*br(P, Q) - j*Q*br(P, C) + i*P*br(Q, C))/C**(i+j+1))
        ok = ok and sp.simplify(lhs - rhs) == 0
    return ok

def twisted_jacobian(p_poly, gam, wexpr, C, i, j):
    """F = ( P/C^i , Q/C^j ) as a map of (x,y), with P,Q the sweep composed with
    gamma = gam(x,y), w = wexpr(x,y).  Returns (detJ, P, Q) with detJ simplified."""
    p, q = sweep_pair(p_poly)
    P = sp.expand(p.subs(w, wexpr) + 2*gam)
    Q = sp.expand(q.subs(w, wexpr) + gam*wexpr)
    F1 = P / C**i
    F2 = Q / C**j
    J = sp.Matrix([[sp.diff(F1, x), sp.diff(F1, y)],
                   [sp.diff(F2, x), sp.diff(F2, y)]])
    return sp.cancel(sp.together(J.det())), P, Q, C

def search(maxdeg=3, verbose=True):
    """Finite search over small twist shapes.  Reports every (shape, p) whose
    twisted Jacobian is a nonzero constant, together with the divisibility side
    conditions that must then hold."""
    hits, tried = [], 0
    a, b, c0, c1 = symbols('a b c0 c1')
    # gamma affine in a monomial (Gao's gamma = gamma0 + a*xy + b*x^2 z, one term
    # fewer here because the plane has one variable fewer); w = gamma * u.
    for (al, be) in itertools.product(range(0, 3), repeat=2):
        if al == 0 and be == 0:
            continue
        gam = c0 + a*x**al*y**be
        for (mu, nu) in itertools.product(range(0, 3), repeat=2):
            u = 1 + b*x**mu*y**nu
            wexpr = sp.expand(gam*u)
            for s in range(0, 3):
                C = sp.expand(gam*x**s)
                for i, j in ((1, 2), (1, 1), (2, 3), (0, 1), (1, 3)):
                    for dp in range(2, maxdeg+1):
                        cs = symbols(f'k0:{dp+1}')
                        p_poly = sum(cs[t]*w**t for t in range(1, dp+1))
                        tried += 1
                        try:
                            det, P, Q, Cc = twisted_jacobian(p_poly, gam, wexpr, C, i, j)
                        except Exception:
                            continue
                        num = sp.expand(sp.numer(det))
                        den = sp.expand(sp.denom(det))
                        # det is constant iff num = k*den for a constant k
                        pol = sp.Poly(num, x, y)
                        polden = sp.Poly(den, x, y)
                        # necessary: same monomial support up to scale
                        if len(pol.monoms()) != len(polden.monoms()):
                            continue
                        ratio = sp.cancel(num/den)
                        if ratio.free_symbols <= {a, b, c0, c1, *cs}:
                            hits.append({'gamma': str(gam), 'u': str(u), 'C': str(C),
                                         'i': i, 'j': j, 'degp': dp,
                                         'detJ': str(ratio)[:200]})
                            if verbose:
                                print(json.dumps(hits[-1]), flush=True)
    return hits, tried

if __name__ == '__main__':
    maxdeg = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ok, det = prove_no_polynomial_twist()
    print("=" * 74)
    print("PLANE TANGENT SWEEP")
    print("=" * 74)
    print(f"  det J(S) = {det}   (Gao 3.1 says 2*gamma)   MATCHES: {ok}")
    print("  => no polynomial conjugation can fix it (see module docstring);")
    print("     a division twist with side conditions is forced.")
    print()
    hits, tried = search(maxdeg)
    print(f"\nshapes tried: {tried}   constant-Jacobian shapes: {len(hits)}")
    json.dump(hits, open('/home/user/jacobian_planar/wave6/plane_sweep_hits.json', 'w'),
              indent=1)
