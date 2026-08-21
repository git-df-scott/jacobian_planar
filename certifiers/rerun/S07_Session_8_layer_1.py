"""
Plane Jacobian campaign - Session 8, layer 1
The (99,66) decision system: certain linear conditions, built exactly.

Charts (from Borisov's edge coordinates, verified on the near-miss):
  (-5)-curve:  s = x2/v^2 = 0,  parameter w = v^3/x2      (v = x1 x2^3 - 1)
      x1^i x2^j = (s w + 1)^i s^(3j-9i) w^(2j-6i)
      pole bounds:  ord_s y1 >= -3,  ord_s y2 >= -2
  (-2)-curve:  q = x2/v^3 = 1/w = 0,  parameter v
      x1^i x2^j = (v+1)^i q^(j-3i) v^(3j-9i)
      pole bounds:  ord_q y1 >= -9,  ord_q y2 >= -6
      => pure support cut: c_ij = 0 whenever j - 3i <= -(bound)-1

Support boxes: y1 in [0,27]x[0,72], y2 in [0,18]x[0,48].
All conditions are over Q; the Belyi data enters only at later layers.
Certification: the exact near-miss (from the Session-7-certified p, r)
must satisfy every condition, saturate both pole bounds, and its
(-5)-curve blocks must reproduce  G1 = p(w)/w^2,  G2 = r(w)/w.
"""
from fractions import Fraction as F
from math import comb

# ---- certified Belyi coefficients over Q(sqrt(-3)): pairs (a, b) = a + b*sqrt(-3)
def q2(a, b=0, den=1):
    return (F(a, den), F(b, den))
def add2(x, y): return (x[0]+y[0], x[1]+y[1])
def mul2(x, y): return (x[0]*y[0] - 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def scal(c, x): return (c*x[0], c*x[1])
ZERO = q2(0)

p_coef = {8: q2(1), 7: q2(2, 8), 6: q2(-233, 50, 3), 5: (F(-4600,27), F(-376,3)),
          4: q2(835, -890, 3), 3: q2(2420, 22, 3), 2: (F(1043,3), F(336)),
          1: q2(-118, 158), 0: q2(-28, 4)}
r_coef = {5: q2(1), 4: q2(4, 16, 3), 3: q2(-278, 68, 9), 2: (F(-140,3), F(-24)),
          1: q2(35, -112, 3), 0: q2(68, -20, 3)}

# ---- support sets with the (-2)-curve cut
S1 = [(i, j) for i in range(28) for j in range(73) if j - 3*i >= -9]
S2 = [(i, j) for i in range(19) for j in range(49) if j - 3*i >= -6]
ix1 = {m: k for k, m in enumerate(S1)}
ix2 = {m: k for k, m in enumerate(S2)}
print(f"support sizes after (-2)-pole cut: |S1| = {len(S1)}, |S2| = {len(S2)}"
      f"   (full boxes: {28*73}, {19*49})")

# ---- (-5)-curve pole conditions: for each (delta, t) with 3*delta + t <= -(bound+1)
def build_eqs(S, ix, imax, bound):
    eqs = []
    for delta in range(-9, 0):
        tmax = -(bound + 1) - 3*delta
        for t in range(0, min(tmax, imax) + 1):
            row = {}
            for i in range(t, imax + 1):
                j = 3*i + delta
                if (i, j) in ix:
                    row[ix[(i, j)]] = comb(i, t)
            if row:
                eqs.append(row)
    return eqs

E1 = build_eqs(S1, ix1, 27, 3)
E2 = build_eqs(S2, ix2, 18, 2)
print(f"(-5)-pole linear conditions: y1: {len(E1)} equations, y2: {len(E2)}")

# ---- exact sparse Gaussian elimination over Q for ranks
def qrank(eqs, nvars):
    rows = [dict((k, F(v)) for k, v in r.items()) for r in eqs]
    pivots = {}
    rank = 0
    for r in rows:
        for pc, pr in pivots.items():
            if pc in r:
                f = r[pc]
                for c, val in pr.items():
                    r[c] = r.get(c, F(0)) - f*val
                    if r[c] == 0: del r[c]
        if r:
            pc = min(r)
            inv = 1/r[pc]
            pr = {c: v*inv for c, v in r.items()}
            pivots[pc] = pr
            rank += 1
    return rank

rk1, rk2 = qrank(E1, len(S1)), qrank(E2, len(S2))
print(f"exact ranks over Q: {rk1}, {rk2}")
print(f"dim L1 = {len(S1)-rk1},  dim L2 = {len(S2)-rk2},  total = "
      f"{len(S1)-rk1 + len(S2)-rk2}  (from {28*73 + 19*49} raw unknowns)")

# ---- exact near-miss vectors: y1 = x1^3 x2^8 p(v^3/x2), y2 = x1^2 x2^5 v r(v^3/x2)
def expand_nearmiss(poly, i0, j0, extra_v):
    """coeffs of x1^i0 x2^j0 * v^extra_v * poly(v^3/x2) as {(i,j): Q(sqrt-3)}"""
    out = {}
    for k, pk in poly.items():
        # v^(3k+extra_v) * x2^(j0-k) * x1^i0 ; v^N = sum_u C(N,u)(-1)^(N-u) x1^u x2^(3u)
        N = 3*k + extra_v
        for u in range(N + 1):
            c = comb(N, u)*(-1)**(N - u)
            key = (i0 + u, j0 - k + 3*u)
            out[key] = add2(out.get(key, ZERO), scal(F(c), pk))
    return {k: v for k, v in out.items() if v != ZERO}

nm1 = expand_nearmiss(p_coef, 3, 8, 0)
nm2 = expand_nearmiss(r_coef, 2, 5, 1)
assert all(k in ix1 for k in nm1), "near-miss y1 leaves S1"
assert all(k in ix2 for k in nm2), "near-miss y2 leaves S2"
sat1 = min(j - 3*i for (i, j) in nm1); sat2 = min(j - 3*i for (i, j) in nm2)
print(f"\nnear-miss support inside S1/S2: True;  (-2)-pole saturation: "
      f"{-sat1} of 9, {-sat2} of 6")

def check_eqs(eqs, ix, vec):
    bad = 0
    for row in eqs:
        acc = ZERO
        rev = {v: k for k, v in ix.items()}
        for col, coef in row.items():
            key = rev[col]
            if key in vec:
                acc = add2(acc, scal(F(coef), vec[key]))
        if acc != ZERO: bad += 1
    return bad

print("near-miss violates", check_eqs(E1, ix1, nm1), "+",
      check_eqs(E2, ix2, nm2), "of the (-5)-pole conditions (must be 0 + 0)")

# ---- (-5)-curve leading blocks: G(w) at s-order = -bound
def sblock(vec, order):
    G = {}
    for (i, j), c in vec.items():
        delta = j - 3*i
        t = order - 3*delta
        if 0 <= t <= i:
            m = 2*delta + t
            G[m] = add2(G.get(m, ZERO), scal(F(comb(i, t)), c))
    return {m: c for m, c in G.items() if c != ZERO}

G1, G2 = sblock(nm1, -3), sblock(nm2, -2)
# targets: G1 = p(w)/w^2 -> {k-2: p_k}, G2 = r(w)/w -> {k-1: r_k}
T1 = {k-2: v for k, v in p_coef.items()}
T2 = {k-1: v for k, v in r_coef.items()}
print("G1 == p(w)/w^2 exactly:", G1 == T1, " | G2 == r(w)/w exactly:", G2 == T2)
