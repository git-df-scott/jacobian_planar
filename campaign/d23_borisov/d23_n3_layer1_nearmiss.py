"""
Plane Jacobian campaign - Session N2 continuation (N3, layer-1 close-out).
CERTIFICATION of the Second Framework near-miss against the layer-1
decision system -- the exact analog of Session 8's certification of the
First Framework near-miss.

The near-miss (certified in d23_n3_certifyPR.gp + the abstract Jacobian
identity):
    y1 = x1^3 x2^8 P(v^3/x2),  y2 = x1^2 x2^5 v R(v^3/x2),  v = x1 x2^3 - 1
with (P, R) the exact degree-(14,9) pair over K14 = Q[th]/(E), and
J(y1, y2) = -h0 x1^4 x2^12.

CERTIFIED HERE (all exact over K14; every check is Q-LINEAR in the
K14-coefficients, so plain Fraction-vector arithmetic suffices):
  NM1. support: the expansions lie inside the LAURENT windows
       [0,45]x[-6,120] (y1) and [0,30]x[-4,80] (y2) with cuts
       j-3i >= -15 / -10.  (The x2-negative terms are the session's
       corrective discovery: the (3,8)/(2,5) miracle map is Laurent for
       SF -- deg P = 14 > 8 -- so the polynomial near-miss needs the
       long-branch surgery; see D23_n3_report.md.);
  NM2. (-2)-pole saturation: min(j-3i) equals EXACTLY -15 and -10;
  NM3. every (-5)-curve pole condition of d23_n3_layer1.py holds
       (315 + 145 linear conditions);
  NM4. (-5)-curve leading blocks at s-order -3 / -2 reproduce the Belyi
       data:  G1 = P(w)/w^2,  G2 = R(w)/w  (Session 8's block extraction).
"""
import os
from fractions import Fraction as F
from math import comb
from sympy import Poly, symbols, sympify

y = symbols('y')
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'd23_PR_data')
DEGK = 14

def loadK(name):
    """K14 element from a gp-lifted polynomial in y -> tuple of 14 Fractions."""
    s = open(os.path.join(HERE, name)).read().strip()
    P = Poly(sympify(s.replace('^', '**'), rational=True), y)
    cs = [F(int(c.p), int(c.q)) for c in reversed(P.all_coeffs())]
    cs += [F(0)]*(DEGK - len(cs))
    return tuple(cs)

ZERO = tuple([F(0)]*DEGK)
def kadd(a, b): return tuple(x + z for x, z in zip(a, b))
def kscal(c, a): return tuple(F(c)*x for x in a)

Pc = {14: tuple([F(1)] + [F(0)]*(DEGK-1))}
for k in range(14):
    Pc[k] = loadK(f'sf_PR_p{k}.txt')
Rc = {9: tuple([F(1)] + [F(0)]*(DEGK-1)),
      8: tuple([F(1)] + [F(0)]*(DEGK-1))}       # slice r8 = 1
for k in range(8):
    Rc[k] = loadK(f'sf_PR_r{k}.txt')

def expand_nm(poly, i0, j0, ev):
    """coefficients of x1^i0 x2^j0 v^ev poly(v^3/x2) as {(i,j): K14}"""
    out = {}
    for k, ck in poly.items():
        N = 3*k + ev
        for u in range(N + 1):
            key = (i0 + u, j0 - k + 3*u)
            c = comb(N, u)*(-1)**(N - u)
            out[key] = kadd(out.get(key, ZERO), kscal(c, ck))
    return {k2: v for k2, v in out.items() if v != ZERO}

nm1 = expand_nm(Pc, 3, 8, 0)
nm2 = expand_nm(Rc, 2, 5, 1)

# ---------- NM1 + NM2: support and saturation ----------
B1 = (45, 120, 15)
B2 = (30, 80, 10)
in1 = all(0 <= i <= B1[0] and -6 <= j <= B1[1] and j - 3*i >= -B1[2]
          for (i, j) in nm1)
in2 = all(0 <= i <= B2[0] and -4 <= j <= B2[1] and j - 3*i >= -B2[2]
          for (i, j) in nm2)
neg1 = sorted((i, j) for (i, j) in nm1 if j < 0)
neg2 = sorted((i, j) for (i, j) in nm2 if j < 0)
sat1 = min(j - 3*i for (i, j) in nm1)
sat2 = min(j - 3*i for (i, j) in nm2)
print(f"[{'PASS' if in1 and in2 else 'FAIL'}] NM1 support inside the Laurent "
      f"windows (|nm1| = {len(nm1)}, |nm2| = {len(nm2)} monomials)")
print(f"      x2-negative terms (the Laurent defect): y1: {len(neg1)} "
      f"terms, j down to {min(j for _, j in neg1)}; y2: {len(neg2)} terms, "
      f"j down to {min(j for _, j in neg2)}")
print(f"[{'PASS' if (sat1, sat2) == (-15, -10) else 'FAIL'}] NM2 (-2)-pole "
      f"saturation exactly (-15, -10): got ({sat1}, {sat2})")

# ---------- NM3: all (-5)-pole conditions ----------
def check_conditions(nm, imax, cut, bound):
    bad = total = 0
    for delta in range(-cut, 0):
        tmax = -(bound + 1) - 3*delta
        for t in range(0, min(tmax, imax) + 1):
            acc = ZERO
            hit = False
            for i in range(t, imax + 1):
                key = (i, 3*i + delta)
                if key in nm:
                    acc = kadd(acc, kscal(comb(i, t), nm[key]))
                    hit = True
            if hit:
                total += 1
                if acc != ZERO:
                    bad += 1
    return bad, total

bad1, tot1 = check_conditions(nm1, B1[0], B1[2], 3)
bad2, tot2 = check_conditions(nm2, B2[0], B2[2], 2)
print(f"[{'PASS' if bad1 + bad2 == 0 else 'FAIL'}] NM3 (-5)-pole conditions: "
      f"y1 violates {bad1} of {tot1}, y2 violates {bad2} of {tot2}")

# ---------- NM4: (-5)-curve leading blocks ----------
def sblock(nm, order):
    G = {}
    for (i, j), c in nm.items():
        delta = j - 3*i
        t = order - 3*delta
        if 0 <= t <= i:
            mkey = 2*delta + t
            G[mkey] = kadd(G.get(mkey, ZERO), kscal(comb(i, t), c))
    return {m: c for m, c in G.items() if c != ZERO}

G1 = sblock(nm1, -3)
G2 = sblock(nm2, -2)
T1 = {k - 2: v for k, v in Pc.items()}          # P(w)/w^2
T2 = {k - 1: v for k, v in Rc.items()}          # R(w)/w
print(f"[{'PASS' if G1 == T1 else 'FAIL'}] NM4 G1 == P(w)/w^2 exactly over K14")
print(f"[{'PASS' if G2 == T2 else 'FAIL'}] NM4 G2 == R(w)/w exactly over K14")
print()
print("Layer-1 anchoring of the Laurent miracle map certified: saturation,")
print("all 460 (-5)-pole conditions, and the exact G-blocks.  Polynomial")
print("near-miss via the surgery: N4.")
