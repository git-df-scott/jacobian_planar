"""
Plane Jacobian campaign - Session N2 continuation (N3 layer 1).
The SECOND FRAMEWORK (99,66)-analog decision system at degrees (165,110):
support boxes, (-2)-pole cuts, (-5)-pole linear conditions, exact ranks.
(The Session-8 layer-1 construction, rebuilt for D = 23.)

BOX DERIVATION (closes the L1 gap flagged in D23_phase1_report.md).
The First Framework's boxes [0,27]x[0,72], [0,18]x[0,48] (stated in the
paper, Sec. 3) are exactly the bidegrees of the near-miss shape
    y1 = x1^3 x2^8 p(w),   y2 = x1^2 x2^5 v r(w),   w = v^3/x2,
namely (3,8) + deg(p)*(3,8) and (2,5)+(1,3) + deg(r)*(3,8).  The Second
Framework keeps the same stem geometry (d23_phase1_chart.py), the same
(-5)-side pole bounds (-3,-2), and (-2)-side depths (-15,-10), so the
same prefactors saturate and the SF near-miss shape is
    y1 = x1^3 x2^8 P(w),   y2 = x1^2 x2^5 v R(w),  deg P = 14, deg R = 9,
with bidegrees
    y1: (3,8) + 14*(3,8) = (45, 120),    y2: (3,8) + 9*(3,8) = (30, 80).
CROSS-CHECK against the paper: the totals (45+120, 30+80) = (165, 110)
are EXACTLY the first rung of the paper's reconstruction ladder
(165,110) -> (270,180) -> (435,290).  The remaining rungs are the
long-branch surgery; both coordinate systems are polynomial coordinate
systems on the same A^2, so they differ by a polynomial AUTOMORPHISM
(constant Jacobian): the Keller demand is equivalent in either system,
and the decision system may be built at (165,110) in stem coordinates.

LAYER-1 SYSTEM (this file, all exact over Q):
  support boxes with the (-2)-pole support cut  j - 3i >= -15 (y1),
  j - 3i >= -10 (y2)  [FF: -9/-6], and the (-5)-curve pole conditions
  from the s-chart monomial rule x1^i x2^j = (sw+1)^i s^(3d) w^(2d),
  d = j - 3i:  ord_s y1 >= -3, ord_s y2 >= -2  [same bounds as FF].
Certification target for N3c: the SF near-miss (once P, R are derived)
must satisfy every condition and saturate both pole bounds, reproducing
G1 = P(w)/w^2, G2 = R(w)/w as its (-5)-curve leading blocks.
"""
from fractions import Fraction as F
from math import comb

# ---------- boxes and support sets ----------
B1 = (45, 120, 15)     # y1: i-max, j-max, (-2)-cut depth
B2 = (30, 80, 10)      # y2
S1 = [(i, j) for i in range(B1[0]+1) for j in range(B1[1]+1) if j - 3*i >= -B1[2]]
S2 = [(i, j) for i in range(B2[0]+1) for j in range(B2[1]+1) if j - 3*i >= -B2[2]]
ix1 = {m: k for k, m in enumerate(S1)}
ix2 = {m: k for k, m in enumerate(S2)}
print(f"support sizes after (-2)-pole cut: |S1| = {len(S1)}, |S2| = {len(S2)}"
      f"   (full boxes: {(B1[0]+1)*(B1[1]+1)}, {(B2[0]+1)*(B2[1]+1)})")

# ---------- (-5)-curve pole conditions ----------
def build_eqs(ix, imax, cut, bound):
    eqs = []
    for delta in range(-cut, 0):
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

E1 = build_eqs(ix1, B1[0], B1[2], 3)
E2 = build_eqs(ix2, B2[0], B2[2], 2)
print(f"(-5)-pole linear conditions: y1: {len(E1)} equations, y2: {len(E2)}")

# ---------- exact sparse Gaussian elimination over Q ----------
def qrank(eqs):
    pivots = {}
    rank = 0
    for r0 in eqs:
        r = dict((k, F(v)) for k, v in r0.items())
        while True:
            common = set(r) & set(pivots)
            if not common:
                break
            pc = min(common)
            f = r.pop(pc)
            for c, val in pivots[pc].items():
                if c in r:
                    r[c] -= f*val
                    if r[c] == 0:
                        del r[c]
                else:
                    r[c] = -f*val
        if r:
            pc = min(r)
            inv = 1/r.pop(pc)
            pivots[pc] = {c: v*inv for c, v in r.items()}
            rank += 1
    return rank

rk1, rk2 = qrank(E1), qrank(E2)
print(f"exact ranks over Q: {rk1}, {rk2}")
print(f"dim L1 = {len(S1)-rk1},  dim L2 = {len(S2)-rk2},  total = "
      f"{len(S1)-rk1 + len(S2)-rk2}  (from "
      f"{(B1[0]+1)*(B1[1]+1) + (B2[0]+1)*(B2[1]+1)} raw unknowns)")
print()
print("FF comparison (Session 8): |S1|=1849, |S2|=825 -> dims 1508 total.")
print("Near-miss certification (support membership, saturation, G-blocks)")
print("PENDING the N3c derivation of (P, R).")
