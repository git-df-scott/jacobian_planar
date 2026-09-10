"""
Exact planar Jacobian-conjecture counterexample gate.

Given P, Q in Q[x,y] (sympy expressions), decide EXACTLY:
  (1) is det J(P,Q) a nonzero constant?              [Keller condition]
  (2) is (P,Q) a polynomial automorphism of C^2?      [invertibility]

(2) uses the Bass-Connell-Wright degree bound: if F=(P,Q) is a polynomial
automorphism of C^n then deg F^{-1} <= (deg F)^{n-1}; for n=2 this is deg F.
So we compute the formal power-series inverse G of the origin-normalised map
F0 = L^{-1}(F - F(0)) (L = linear part) through total degree D = deg F, and
check whether G o F0 = id EXACTLY as polynomials.  If F is an automorphism,
its inverse is a polynomial of degree <= D, hence equals the truncation and
the composition is the identity.  If the composition is not the identity, F
is not an automorphism.  This is a complete decision procedure over Q.

A pair passes the gate (is a counterexample) iff (1) holds and (2) fails.
Everything is exact rational arithmetic; no numerics.
"""
import sympy as sp

x, y = sp.symbols('x y')

def keller_constant(P, Q):
    J = sp.expand(sp.diff(P, x)*sp.diff(Q, y) - sp.diff(P, y)*sp.diff(Q, x))
    return J, (J != 0 and J.free_symbols == set())

def truncate(expr, D):
    p = sp.Poly(sp.expand(expr), x, y)
    return sum(c*x**i*y**j for (i, j), c in p.terms() if i + j <= D)

def formal_inverse(P, Q, D):
    """Return (G1,G2) with G(F0(x,y)) = (x,y) + O(deg D+1), and F0."""
    P0 = sp.expand(P - P.subs({x: 0, y: 0}))
    Q0 = sp.expand(Q - Q.subs({x: 0, y: 0}))
    L = sp.Matrix([[sp.diff(P0, x), sp.diff(P0, y)],
                   [sp.diff(Q0, x), sp.diff(Q0, y)]]).subs({x: 0, y: 0})
    assert L.det() != 0, "linear part singular at origin (impossible for a Keller map)"
    Linv = L.inv()
    F1 = sp.expand(Linv[0, 0]*P0 + Linv[0, 1]*Q0)
    F2 = sp.expand(Linv[1, 0]*P0 + Linv[1, 1]*Q0)
    # F0 = (F1,F2) = id + higher order. Inverse by fixed-point iteration:
    # G = id - H(G), where H = F0 - id, converging one degree per step.
    H1, H2 = sp.expand(F1 - x), sp.expand(F2 - y)
    G1, G2 = x, y
    for _ in range(D):
        G1n = truncate(x - H1.subs({x: G1, y: G2}, simultaneous=True), D)
        G2n = truncate(y - H2.subs({x: G1, y: G2}, simultaneous=True), D)
        if sp.expand(G1n - G1) == 0 and sp.expand(G2n - G2) == 0:
            break
        G1, G2 = G1n, G2n
    return (G1, G2), (F1, F2)

def is_automorphism(P, Q):
    D = max(sp.Poly(P, x, y).total_degree(), sp.Poly(Q, x, y).total_degree())
    (G1, G2), (F1, F2) = formal_inverse(P, Q, D)
    C1 = sp.expand(G1.subs({x: F1, y: F2}, simultaneous=True) - x)
    C2 = sp.expand(G2.subs({x: F1, y: F2}, simultaneous=True) - y)
    ok = (C1 == 0 and C2 == 0)
    return ok, (G1, G2)

def gate(P, Q, name=""):
    P, Q = sp.expand(P), sp.expand(Q)
    J, keller = keller_constant(P, Q)
    print(f"[{name}] det J = {J}  -> Keller: {keller}")
    if not keller:
        print(f"[{name}] VERDICT: not a Keller pair; cannot be a counterexample.")
        return False
    auto, G = is_automorphism(P, Q)
    if auto:
        print(f"[{name}] polynomial inverse found (deg <= {max(sp.Poly(P,x,y).total_degree(), sp.Poly(Q,x,y).total_degree())}); VERDICT: automorphism, NOT a counterexample.")
        return False
    print(f"[{name}] no polynomial inverse of degree <= deg F exists; VERDICT: *** PLANAR JACOBIAN COUNTEREXAMPLE ***")
    return True

if __name__ == "__main__":
    # Controls.
    # 1. Tame automorphism (composition of triangular and linear maps): must be accepted as automorphism.
    P1 = x + (y + x**2)**3;  Q1 = y + x**2
    assert gate(P1, Q1, "tame cubic") is False
    # 2. A more mixed tame map: (x,y)->(x+y^2, y) -> then (u, v+u^3) -> then linear.
    u = x + y**2; v = y
    P2 = 2*u + 3*(v + u**3); Q2 = u - (v + u**3)
    assert gate(P2, Q2, "tame deg 6 mixed") is False
    # 3. Non-Keller non-injective map (the session-39 descent of Alpoge's map): must be rejected at gate 1.
    uu, vv = x, y
    G1 = (uu+1)*(3*uu+vv-2)**2*(3*uu**3 + uu**2*vv + 4*uu**2 + 2*uu*vv + vv)
    G2 = -(3*uu+vv-2)*(9*uu**3 + 3*uu**2*vv + 12*uu**2 + 6*uu*vv + uu + 3*vv)
    assert gate(G1, G2, "Alpoge planar descent") is False
    # 4. Negative control for step (2): a map with constant Jacobian that is NOT an automorphism
    #    cannot be supplied in the plane (that is the conjecture), so instead check the
    #    inverse-detector on a non-Keller invertible-looking map is never reached, and that the
    #    detector correctly REJECTS a non-invertible map when we bypass gate 1:
    #    F=(x, y + x*y) has det J = 1 + x (not constant); it is not injective ((-1,0) and (-1,5) both -> (-1,0)).
    okA, _ = is_automorphism(x, y + x*y)
    assert okA is False, "inverse detector must reject a non-invertible map"
    print("ALL CONTROLS PASS")
