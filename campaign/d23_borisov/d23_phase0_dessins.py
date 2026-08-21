"""
Plane Jacobian campaign - Session N2, Phase 0, dessin identification.

For each of the 15 embeddings of the certified degree-23 Belyi map
B = c t a^3 b^5 (single Galois orbit, K = Q[w]/(f15)), numerically trace
ALL 23 edges of the dessin B^{-1}([0,1]): from each black vertex
(t=0: degree 1; roots of a: degree 3; roots of b: degree 5) follow each
of its d outgoing arcs as u = B goes 0 -> 1.  Tree structure demands:
exactly one arc per black vertex arrives at the order-7 white hub t=1,
the other d-1 arrive at white leaves (the 16 simple roots of s); every
leaf receives exactly one arc.  Reading the hub arrivals by angle gives
the counterclockwise cyclic degree sequence around t=1 -- the necklace.

Expected: the 15 embeddings realize the 15 necklaces of (1,3,3,3,3,5,5)
bijectively (numerical face of the completeness theorem), conjugate
embeddings giving mirror necklaces.  Borisov's Figure 28 draws
(5,1,5,3,3,3,3): identified below among the 3 real embeddings.

Identification is NUMERIC (labeling only); certification is exact
(d23_phase0_certify.gp / d23_phase0_belyi.py).
"""
import os
import numpy as np
from sympy import Poly, symbols, sympify

w = symbols('w')
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'd23_belyi_data')

def loadpoly(name):
    return Poly(sympify(open(os.path.join(HERE, name)).read()
                        .replace('^', '**'), rational=True), w)

fW = loadpoly('d23_f.txt')
data = {n: loadpoly(f'd23_{n}.txt') for n in ('b0', 'a3', 'a2', 'a1', 'a0', 'c')}
roots15 = np.roots([complex(cf) for cf in fW.all_coeffs()])
roots15 = sorted(roots15, key=lambda z: (abs(z.imag) > 1e-9, z.real, z.imag))

def canon(seq):
    n = len(seq)
    return min(tuple(seq[(i+j) % n] for j in range(n)) for i in range(n))

BORISOV = canon((5, 1, 5, 3, 3, 3, 3))

def newton_to(F, Bp, t0, u, tol=1e-10, itmax=60):
    """solve F(t) == u; F must be numerically stable near the target level."""
    tcur = t0
    for _ in range(itmax):
        bp = Bp(tcur)
        if bp == 0 or not np.isfinite(bp):
            return None
        d = (F(tcur) - u)/bp
        if not np.isfinite(d):
            return None
        if abs(d) > 0.1:
            d *= 0.1/abs(d)
        tcur -= d
        if abs(d) < tol*max(1.0, abs(tcur)):
            return tcur
    return None

def trace_edge(Bt, Bm1f, Bp, z, K, d, j, rcap):
    """follow the arc B in [0,1] leaving black vertex z (local model
    B ~ K (t-z)^d) along its j-th outgoing direction; adaptive
    predictor-corrector in u; return endpoint t at u = 1 - 1e-9.
    For u > 0.5 Newton runs on the stable form (B-1) - (u-1)."""
    u0 = 1e-4
    eps = (u0/abs(K))**(1.0/d)
    if eps > rcap:
        eps = rcap
        u0 = abs(K)*eps**d
    F = lambda u: (Bt, u) if u <= 0.5 else (Bm1f, u - 1.0)
    phi = (-np.angle(K) + 2*np.pi*j)/d
    tcur = z + eps*np.exp(1j*phi)
    Fu, rhs = F(u0)
    tcur = newton_to(Fu, Bp, tcur, rhs) or tcur
    grid = np.concatenate([np.geomspace(u0, 0.5, 250),
                           1 - np.geomspace(0.5, 1e-9, 700)])
    uprev = u0
    for u in grid[1:]:
        # adaptive: subdivide the step until Newton converges
        stack = [u]
        for _ in range(4000):
            if not stack:
                break
            utgt = stack[-1]
            tpred = tcur + (utgt - uprev)/Bp(tcur) if Bp(tcur) != 0 else tcur
            Fu, rhs = F(utgt)
            tnew = newton_to(Fu, Bp, tpred, rhs)
            if tnew is None:
                mid = 0.5*(uprev + utgt)
                if abs(utgt - mid) < 1e-15:
                    return None
                stack.append(mid)
            else:
                tcur, uprev = tnew, utgt
                stack.pop()
        else:
            return None
    return tcur

nseen = {}
for idx, beta in enumerate(roots15):
    ev = lambda P: complex(sum(complex(cf)*beta**k for k, cf in
                               enumerate(reversed(P.all_coeffs()))))
    b0, a3, a2, a1, a0, c = (ev(data[n]) for n in ('b0','a3','a2','a1','a0','c'))
    b1 = beta
    A = np.array([1, a3, a2, a1, a0], dtype=complex)
    Bq = np.array([1, b1, b0], dtype=complex)
    Bfull = c*np.polymul(np.polymul(np.array([1, 0], dtype=complex),
             np.polymul(np.polymul(A, A), A)),
             np.polymul(np.polymul(np.polymul(np.polymul(Bq, Bq), Bq), Bq), Bq))
    # roots of s: divide B - 1 by (t-1)^7  (quotient is c*s, degree 16)
    Bm1 = Bfull.copy(); Bm1[-1] -= 1
    q7 = np.array([1.0])
    for _ in range(7):
        q7 = np.polymul(q7, [1.0, -1.0])
    q, r = np.polydiv(Bm1, q7)
    sroots = np.roots(q)
    assert max(abs(r)) < 1e-6*max(abs(Bm1)), "division residue too large"
    cs1 = c*np.prod(1 - sroots)         # c*s(1): hub spoke phase (factored)
    spoke = [(np.pi - np.angle(cs1) + 2*np.pi*j)/7 for j in range(7)]

    # ALL evaluations in factored form (a degree-23 expanded polyval at
    # |t| ~ 5 loses every significant digit to cancellation):
    pa = lambda tt: np.polyval(A, tt)
    pb = lambda tt: np.polyval(Bq, tt)
    Bt = lambda tt: c*tt*pa(tt)**3*pb(tt)**5
    Bm1f = lambda tt: (tt-1)**7*c*np.prod(tt - sroots)
    Bp = lambda tt: 23*c*pa(tt)**2*pb(tt)**4*(tt-1)**6   # master identity

    blacks = [(0j, 1)] + [(z, 3) for z in np.roots(A)] + [(z, 5) for z in np.roots(Bq)]
    allpts = [z for z, _ in blacks] + [1.0 + 0j]
    hub_slots = {}              # spoke index -> source degree
    leaf_hits, fails = 0, 0
    pap = lambda tt: np.polyval(np.polyder(A), tt)
    pbp = lambda tt: np.polyval(np.polyder(Bq), tt)
    for z, d in blacks:
        # exact local expansion factor B(z+e) ~ K e^d, in stable factored form
        if d == 1:
            K = c*pa(z)**3*pb(z)**5
        elif d == 3:
            K = c*z*pap(z)**3*pb(z)**5
        else:
            K = c*z*pa(z)**3*pbp(z)**5
        rcap = 0.3*min(abs(z - zz) for zz in allpts if abs(z - zz) > 1e-9)
        for j in range(d):
            tend = trace_edge(Bt, Bm1f, Bp, z, K, d, j, rcap)
            if tend is None:
                fails += 1
                continue
            dhub = abs(tend - 1)
            dleaf = min(abs(tend - zz) for zz in sroots)
            if dhub < dleaf:
                ang = np.angle(tend - 1)
                k = int(np.argmin([abs(np.angle(np.exp(1j*(ang - s0)))) for s0 in spoke]))
                hub_slots[k] = d
            else:
                leaf_hits += 1
    seq = tuple(hub_slots[k] for k in sorted(hub_slots)) if len(hub_slots) == 7 else ()
    key = canon(seq) if len(seq) == 7 else None
    isreal = abs(beta.imag) < 1e-9
    tag = "REAL   " if isreal else "complex"
    star = "  <-- BORISOV Fig. 28 dessin (5,1,5,3,3,3,3)" if key == BORISOV else ""
    print(f"root {idx+1:2d} [{tag}] beta = {beta:+.6f}  hub arcs {len(seq)}/7, "
          f"leaf arcs {leaf_hits}/16, failed {fails}  necklace {key}{star}")
    if key:
        nseen.setdefault(key, []).append(idx+1)

print()
print(f"distinct necklaces realized: {len(nseen)} of 15 expected")
print("bijection embeddings <-> necklaces:",
      sorted(len(v) for v in nseen.values()) == [1]*15)
