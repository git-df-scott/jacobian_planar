"""
Plane Jacobian campaign - Session 10, layer 3
THE CHAIN-MIRACLE UNIFICATION (First Framework, degrees (99,66)).

Theorem (this session, certified below on the exact near-miss):
In the (q, v)-chart (q = x2/v^3, v = x1 x2^3 - 1), write
    y1 = sum q^n v^{3n} At_n(U),   y2 = sum q^n v^{3n} Bt_n(U),   U = v+1,
and W = y1^2 - y2^3, so  Wt_n = sum_{a+b=n} At_a At_b - sum_{a+b+c=n} Bt.

1. The framework's 13-curve chain between the forked (-5)- and
   (-2)-curves is EQUIVALENT to the thirteen block vanishings
        Wt_n = 0   for n = -18, ..., -6,
   i.e. to the contact condition  val_{E_-2}(y1^2 - y2^3) >= -5.
   No figure data is required: the chain layer is fully specified.

2. On the near-miss these thirteen identities ARE the thirteen-fold
   miracle cancellation deg(p^2 - w r^3) = 3 of the certified Belyi
   map; e.g. the first cascade relation 2 At_-8 = 3 g Bt_-5 reduces
   to 2 p7 = 3 r4.  The chain is the cancellation, geometrized.

3. The surviving blocks of the near-miss are exactly
        Wt_-5 = n3 U^6 (U-1)^9,  Wt_-4 = n2 U^6 (U-1)^6,
        Wt_-3 = n1 U^6 (U-1)^3,  Wt_-2 = n0 U^6,
   with N = p^2 - w r^3 = n3 w^3 + n2 w^2 + n1 w + n0 the certified
   cubic; all other blocks vanish identically.

4. The 13-realization (the framework's remaining boundary demand):
   the first nonvanishing block of y1^2/y2^3 - 1 along E_-2, namely
   W_-5 / K_-6^3, must be a degree-13 polynomial realizing the
   certified degree-13 Belyi map in the parameter v.  The near-miss
   yields the CONSTANT n3 = (-128 + 64 sqrt(-3))/3: degree 0.  This
   is the near-miss's precise, proven failure point.

Run to re-certify (exact arithmetic over Q(sqrt(-3)) throughout).
"""
from fractions import Fraction as F
from math import comb

def q2(a, b=0, den=1): return (F(a, den), F(b, den))
def add2(x, y): return (x[0]+y[0], x[1]+y[1])
def mul2(x, y): return (x[0]*y[0]-3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def scal(c, x): return (c*x[0], c*x[1])
ZERO = q2(0)

p_coef = {8: q2(1), 7: q2(2, 8), 6: q2(-233, 50, 3),
          5: (F(-4600, 27), F(-376, 3)), 4: q2(835, -890, 3),
          3: q2(2420, 22, 3), 2: (F(1043, 3), F(336)),
          1: q2(-118, 158), 0: q2(-28, 4)}
r_coef = {5: q2(1), 4: q2(4, 16, 3), 3: q2(-278, 68, 9),
          2: (F(-140, 3), F(-24)), 1: q2(35, -112, 3), 0: q2(68, -20, 3)}

def expand_nm(poly, i0, j0, ev):
    out = {}
    for k, pk in poly.items():
        N = 3*k + ev
        for u in range(N + 1):
            key = (i0 + u, j0 - k + 3*u)
            out[key] = add2(out.get(key, ZERO),
                            scal(F(comb(N, u)*(-1)**(N-u)), pk))
    return {k: v for k, v in out.items() if v != ZERO}

nm1 = expand_nm(p_coef, 3, 8, 0)
nm2 = expand_nm(r_coef, 2, 5, 1)

def blocks(vec):
    B = {}
    for (i, j), c in vec.items():
        B.setdefault(j - 3*i, {})[i] = add2(
            B.get(j - 3*i, {}).get(i, ZERO), c)
    return {n: {i: c for i, c in P.items() if c != ZERO}
            for n, P in B.items()}

def pmul(X, Y):
    out = {}
    for i, x in X.items():
        for j, y in Y.items():
            out[i+j] = add2(out.get(i+j, ZERO), mul2(x, y))
    return {k: v for k, v in out.items() if v != ZERO}

def padd(X, Y):
    out = dict(X)
    for k, v in Y.items():
        out[k] = add2(out.get(k, ZERO), v)
    return {k: v for k, v in out.items() if v != ZERO}

def pscal(c, X): return {k: scal(c, v) for k, v in X.items()}

A, Bb = blocks(nm1), blocks(nm2)
Wt = {}
for a in A:
    for b in A:
        if a <= b:
            t = pscal(F(2) if a < b else F(1), pmul(A[a], A[b]))
            Wt[a+b] = padd(Wt.get(a+b, {}), t)
B2 = {}
for a in Bb:
    for b in Bb:
        if a <= b:
            t = pscal(F(2) if a < b else F(1), pmul(Bb[a], Bb[b]))
            B2[a+b] = padd(B2.get(a+b, {}), t)
Y3 = {}
for ab, Pab in B2.items():
    for c, Pc in Bb.items():
        Y3[ab+c] = padd(Y3.get(ab+c, {}), pmul(Pab, Pc))
for n, Pn in Y3.items():
    Wt[n] = padd(Wt.get(n, {}), pscal(F(-1), Pn))
Wt = {n: P for n, P in Wt.items() if P}

def poly1mul(X, Y):
    out = {}
    for i, x in X.items():
        for j, y in Y.items():
            out[i+j] = add2(out.get(i+j, ZERO), mul2(x, y))
    return out

p2 = poly1mul(p_coef, p_coef)
r3 = poly1mul(poly1mul(r_coef, r_coef), r_coef)
N = {}
for k, v in p2.items(): N[k] = add2(N.get(k, ZERO), v)
for k, v in r3.items(): N[k+1] = add2(N.get(k+1, ZERO), scal(F(-1), v))
N = {k: v for k, v in N.items() if v != ZERO}
n3, n2, n1, n0 = N[3], N[2], N[1], N[0]

def mk(nc, e):
    return {6+u: scal(F(comb(e, u)*(-1)**(e-u)), nc) for u in range(e+1)
            if scal(F(comb(e, u)*(-1)**(e-u)), nc) != ZERO}

checks = {
    "cubic N has degree exactly 3": sorted(N) == [0, 1, 2, 3],
    "chain vanishing W_n = 0, n = -18..-6": all(
        n not in Wt for n in range(-18, -5)),
    "surviving blocks are {-5,-4,-3,-2}": set(Wt) == {-5, -4, -3, -2},
    "Wt_-5 = n3 U^6(U-1)^9": Wt[-5] == mk(n3, 9),
    "Wt_-4 = n2 U^6(U-1)^6": Wt[-4] == mk(n2, 6),
    "Wt_-3 = n1 U^6(U-1)^3": Wt[-3] == mk(n1, 3),
    "Wt_-2 = n0 U^6": Wt[-2] == mk(n0, 0),
    "cascade C2 <=> 2 p7 = 3 r4": add2(
        scal(F(2), p_coef[7]), scal(F(-3), r_coef[4])) == ZERO,
}
for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
assert all(checks.values())
print(f"\n13-block of the near-miss: constant n3 = {n3}  (degree 0);")
print("framework demands a degree-13 Belyi polynomial there.")
