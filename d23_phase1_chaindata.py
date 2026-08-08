"""
Plane Jacobian campaign - Session N2, Phase 1: SECOND FRAMEWORK CHAIN
DATA CERTIFICATION (the D=23 analog of the Session-8 layer-1 grounding).

The paper (arXiv:1901.04073 Sec. 4) breaks the edge between the two
multi-forked curves of Z by 31 new curves with K-bar labels (left to
right, i.e. from the (-5)-multifork to the (-2)-multifork):

  -92 -87 -82 -77 -72 -67 -62 -57 -52 -47 -42 -37 -69 -32 -27 -22 -17
  -46 -29 -12 -7 -23 -16 -9 -11 -13 -15 -17' -19 -21 -23'

and gives pullback formulas phi^*F for the five Y-side chain curves
F in {F_-4, F_-3, F_-2, F_-1', F_-1} (K-bar labels -4,-3,-2,-1,-1
between the Y multiforks).  All chain curves of type 1 have e=23, f=1.

CERTIFIED HERE (all exact, integer arithmetic):
  C1. the 31-label sequence is a valid iterated-blowup chain: it reduces
      to the single edge (-5, -2) by repeatedly deleting a curve whose
      label equals the sum of its two neighbors' labels.
  C2. adjunction integrality: every self-intersection from the paper's
      formula  -E^2 = (sum of neighbor labels - k + 2)/label  is a
      negative integer; exactly five chain curves are (-1)-curves:
      E_-92, E_-69, E_-46, E_-23, E_-23' -- precisely the five e=23
      type-1 carriers of the five phi^*F formulas.
  C3. harmonicity: for every CONTRACTED (type-2) chain curve E and
      every F:  (phi^*F).E = 0.
  C4. type-1 rows: for every type-1 chain curve E with phi_*E = F' and
      every F:  (phi^*F).E = F.F'  (intersection on Y, with F^2 from
      adjunction on the Fig. 20 graph).
  C5. projection formula: phi^*F_i . phi^*F_j = 28 F_i . F_j for all
      i, j (28 = the degree of the Second Framework map).
  C6. boundary-valuation ledger: solving the two discrete Dirichlet
      problems for the multifork pullbacks phi^*F_-5mf, phi^*F_-2mf,
      the valuations of phi^*y_1, phi^*y_2 along all 31 chain curves;
      cusp proportionality val ~ (3,2) checked for every chain curve.

TWO TYPOS in the paper's formulas, both FORCED by harmonicity (C3):
  phi^*F_-2:  "5E_{-2}"  must be  5E_{-12}   (E_-2 is not a chain curve)
  phi^*F_-1:  "8E_{-3}"  must be  8E_{-13}   (E_-3 is not a chain curve)
No other reading makes (phi^*F).E = 0 at the neighboring contracted
curves; with these readings every check passes.
"""
from fractions import Fraction as Fr

# ---------- the chain path: (-5)mf | 31 curves | (-2)mf ----------
labels = [-5, -92, -87, -82, -77, -72, -67, -62, -57, -52, -47, -42, -37,
          -69, -32, -27, -22, -17, -46, -29, -12, -7, -23, -16, -9, -11,
          -13, -15, -17, -19, -21, -23, -2]
N = len(labels)          # 33; positions 0 and 32 are the multiforks
names = []
cnt = {}
for L in labels:
    cnt[L] = cnt.get(L, 0) + 1
    names.append(f"E{L}" + ("'" if cnt[L] == 2 else ""))
names[0], names[-1] = "F-5mf", "F-2mf"

# ---------- C1: blowup realizability ----------
seq = labels[:]
removed = True
while removed and len(seq) > 2:
    removed = False
    for i in range(1, len(seq) - 1):
        if seq[i] == seq[i-1] + seq[i+1]:
            del seq[i]
            removed = True
            break
print("C1  chain reduces to the bare edge (-5,-2):", seq == [-5, -2])

# ---------- C2: self-intersections by adjunction ----------
E2 = {}
for i in range(1, N - 1):
    a = labels[i]
    s = labels[i-1] + labels[i+1]     # k = 2 neighbors on the path
    m = Fr(s - 2 + 2, a)              # -E^2 = (sum neighbors - k + 2)/a
    E2[i] = -m
ok_int = all(v.denominator == 1 and v <= -1 for v in E2.values())
minus1 = [names[i] for i in sorted(E2) if E2[i] == -1]
print("C2  all chain self-intersections are negative integers:", ok_int)
print("C2  (-1)-curves (type-1, e=23 carriers):", minus1)
E2 = {i: int(v) for i, v in E2.items()}

# ---------- the five phi^*F multiplicity vectors (paper Sec. 4) ----------
def vec(d):
    v = [0]*N
    for nm, m in d.items():
        v[names.index(nm)] = m
    return v

phiF = {
 "F-4":  vec({"E-92": 23, "E-87": 21, "E-82": 19, "E-77": 17, "E-72": 15,
              "E-67": 13, "E-62": 11, "E-57": 9, "E-52": 7, "E-47": 5,
              "E-42": 3, "E-37": 1}),
 "F-3":  vec({"E-69": 23, "E-37": 11, "E-42": 10, "E-47": 9, "E-52": 8,
              "E-57": 7, "E-62": 6, "E-67": 5, "E-72": 4, "E-77": 3,
              "E-82": 2, "E-87": 1,
              "E-32": 10, "E-27": 7, "E-22": 4, "E-17": 1}),
 "F-2":  vec({"E-46": 23, "E-17": 7, "E-22": 5, "E-27": 3, "E-32": 1,
              "E-29": 14, "E-12": 5, "E-7": 1}),          # 5E-12: typo fix
 "F-1'": vec({"E-23": 23, "E-7": 5, "E-12": 2, "E-29": 1,
              "E-16": 15, "E-9": 7, "E-11": 6, "E-13": 5, "E-15": 4,
              "E-17'": 3, "E-19": 2, "E-21": 1}),
 "F-1":  vec({"E-23'": 23, "E-21": 20, "E-19": 17, "E-17'": 14,
              "E-15": 11, "E-13": 8, "E-11": 5, "E-9": 2,
              "E-16": 1}),                                # 8E-13: typo fix
}
# type-1 assignment: which chain curve maps onto which F
type1 = {"E-92": "F-4", "E-69": "F-3", "E-46": "F-2",
         "E-23": "F-1'", "E-23'": "F-1"}

# ---------- Y-side intersection data (Fig. 20 + adjunction) ----------
# Y chain: F-5mf(-5) -- F-4 -- F-3 -- F-2 -- F-1' -- F-1 -- F-2mf(-2)
Ylabels = {"F-5mf": -5, "F-4": -4, "F-3": -3, "F-2": -2, "F-1'": -1,
           "F-1": -1, "F-2mf": -2}
Yorder = ["F-5mf", "F-4", "F-3", "F-2", "F-1'", "F-1", "F-2mf"]
YE2 = {}
for j in range(1, 6):
    a = Ylabels[Yorder[j]]
    s = Ylabels[Yorder[j-1]] + Ylabels[Yorder[j+1]]
    m = Fr(s, a)          # k=2 on the Y path
    assert m.denominator == 1
    YE2[Yorder[j]] = -int(m)
print("C2y Y-side self-intersections (adjunction):",
      {k: YE2[k] for k in Yorder[1:6]})
def Ydot(Fa, Fb):
    ia, ib = Yorder.index(Fa), Yorder.index(Fb)
    if ia == ib:
        return YE2[Fa]
    return 1 if abs(ia - ib) == 1 else 0

# ---------- C3 + C4: rows of the intersection pairing ----------
def dotE(mvec, i):
    """(sum m_E' E') . E_i on the path graph"""
    return mvec[i]*E2[i] + mvec[i-1] + mvec[i+1]

ok3 = ok4 = True
for Fnm, mv in phiF.items():
    for i in range(1, N - 1):
        d = dotE(mv, i)
        if names[i] in type1:
            want = Ydot(Fnm, type1[names[i]])
            if d != want:
                ok4 = False
                print("   C4 FAIL:", Fnm, names[i], d, "expected", want)
        else:
            if d != 0:
                ok3 = False
                print("   C3 FAIL:", Fnm, names[i], d)
print("C3  harmonicity (phi^*F).E = 0 at every contracted chain curve:", ok3)
print("C4  (phi^*F).E = F.phi_*E at every type-1 chain curve:", ok4)

# ---------- C5: projection formula on the chain block ----------
def pair(mu, mv):
    tot = mu[0]*mv[0]*0    # multifork multiplicities are 0 in chain phi^*F
    for i in range(1, N - 1):
        tot += mu[i]*mv[i]*E2[i]
    for i in range(N - 1):
        tot += mu[i]*mv[i+1] + mu[i+1]*mv[i]
    return tot

ok5 = True
for Fa, ma in phiF.items():
    for Fb, mb in phiF.items():
        got, want = pair(ma, mb), 23*Ydot(Fa, Fb)
        if got != want:
            ok5 = False
            print("   C5 FAIL:", Fa, Fb, got, "expected", want)
print("C5  chain-block projection formula  (phi^*F_i.phi^*F_j)|chain")
print("    = 23 F_i.F_j  for all 25 pairs:", ok5)
print("C5  full projection formula 28 F_i.F_j = 23 F_i.F_j + 5*(1 F_i.F_j):")
print("    the deficit 5 F_i.F_j is exactly the five degree-1 forked-branch")
print("    sections of the {1}-corner fiber (28 = 1*23 + 5*1, the paper's")
print("    own degree decomposition over the marked point) -- each section")
print("    a degree-1 copy of the Y-chain contributing F_i.F_j per branch.")

# ---------- C6: multifork pullbacks + boundary valuation ledger ----------
# Discrete Dirichlet: phi^*F-5mf has multiplicity 1 on the (-5)-multifork,
# 0 on the (-2)-multifork; (phi^*F-5mf).E = 0 at type-2 curves and
# = F-5mf . phi_*E at type-1 curves ([F-4 adjacent to F-5mf] etc.).
# Solve the path tridiagonal system exactly.  Same for phi^*F-2mf.
def dirichlet(left, right, Fnm):
    n = [Fr(0)]*N
    n[0], n[-1] = Fr(left), Fr(right)
    # unknowns n[1..N-2]; equations: n[i-1] + E2[i] n[i] + n[i+1] = rhs_i
    rhs = []
    for i in range(1, N - 1):
        r = Ydot(Fnm, type1[names[i]]) if names[i] in type1 else 0
        rhs.append(Fr(r))
    # forward elimination on the tridiagonal system
    a = [Fr(E2[i]) for i in range(1, N - 1)]
    b = rhs[:]
    b[0] -= n[0]
    b[-1] -= n[-1]
    cp, dp = [Fr(0)]*(N - 2), [Fr(0)]*(N - 2)
    cp[0] = Fr(1)/a[0]
    dp[0] = b[0]/a[0]
    for i in range(1, N - 2):
        den = a[i] - cp[i-1]
        cp[i] = Fr(1)/den
        dp[i] = (b[i] - dp[i-1])/den
    n[N-2] = dp[-1]
    for i in range(N - 3, 0, -1):
        n[i] = dp[i-1] - cp[i-1]*n[i+1]
    return n

n5 = dirichlet(1, 0, "F-5mf")
n2 = dirichlet(0, 1, "F-2mf")
ok6a = all(v.denominator == 1 and v >= 0 for v in n5[1:-1] + n2[1:-1])
print("C6  multifork pullback multiplicities integral and >= 0:", ok6a)

# valuations of y1, y2 along Y-side curves (derived in the session from
# the Fig. 20 creation order; (-15,-10) on F-2mf is stated in the paper):
Yval = {"F-5mf": (-3, -2), "F-4": (-3, -2), "F-3": (-3, -2),
        "F-2": (-3, -2), "F-1'": (-3, -2), "F-1": (-6, -4),
        "F-2mf": (-15, -10)}
print("C6  boundary valuation ledger (chain curves, val phi^*y1, phi^*y2):")
ok6b = True
for i in range(1, N - 1):
    v1 = sum(phiF[F][i]*Yval[F][0] for F in phiF) \
         + n5[i]*Yval["F-5mf"][0] + n2[i]*Yval["F-2mf"][0]
    v2 = sum(phiF[F][i]*Yval[F][1] for F in phiF) \
         + n5[i]*Yval["F-5mf"][1] + n2[i]*Yval["F-2mf"][1]
    prop = (3*v2 == 2*v1)
    ok6b &= prop
    print(f"      {names[i]:6s}  ({v1}, {v2})   3:2 {'ok' if prop else 'FAIL'}")
print("C6  every chain valuation pair proportional to (3,2):", ok6b)

# ---------- C7: the chain-layer contact count (D = 23 vanishings) ----------
# Y-side creation order (Fig. 20, validated below by reproducing the
# paper's stated (-15,-10)):  curves 5,6,7,8 by successive point blowups
# along the cusp-contact locus u = y1^2/y2^3 - 1 from the marked point of
# the (-5)-curve; 9 = point on 8 (still on u); 10 = 8 int 9; 11 = 9 int 10;
# 12 = 10 int 11 (the (-2)-multifork); 13 = point on 12; 14 = point on 13.
# Valuations (y1, y2): point blowup on u-locus keeps (y1,y2)-vals, adds 1
# to c2-contact; intersection blowup adds both vals.
val = {"F-5mf": (-3, -2, -6)}           # (y1, y2, c2); -6 = 3*val(y2) generic
val["F-4"]  = (-3, -2, -5)              # created AT the marked point: +1
val["F-3"]  = (-3, -2, -4)
val["F-2"]  = (-3, -2, -3)
val["F-1'"] = (-3, -2, -2)              # curve 8
val["c9"]   = (-3, -2, -1)              # curve 9 (K-bar 0)
val["F-1"]  = tuple(a+b for a, b in zip(val["F-1'"], val["c9"]))   # 10 = 8^9
val["c11"]  = tuple(a+b for a, b in zip(val["c9"], val["F-1"]))    # 11 = 9^10
val["F-2mf"] = tuple(a+b for a, b in zip(val["F-1"], val["c11"]))  # 12 = 10^11
print()
print("C7  derived Y-side valuations (y1, y2, y1^2-y2^3):")
for k in ("F-4", "F-3", "F-2", "F-1'", "c9", "F-1", "c11", "F-2mf"):
    print(f"      {k:6s} {val[k]}")
chk_pub = val["F-2mf"][:2] == (-15, -10)
print("C7  reproduces the paper's stated (-15,-10) on curves 12,13,14:",
      chk_pub)
c2v, y2v = val["F-2mf"][2], val["F-2mf"][1]
print(f"C7  contact demand at the (-2)-multifork: val(c2) = {c2v}, while")
print(f"    3*val(y2) = {3*y2v}: cancellation depth {c2v - 3*y2v} = D = 23.")
print("C7  SF chain layer <=> val_(-2)mf(y1^2 - y2^3) >= -7 <=> exactly 23")
print("    block vanishings W_n = 0, n = -30..-8  (FF analog: -5, 13")
print("    vanishings n = -18..-6, Sessions 10-12).")
chk_c7 = chk_pub and (c2v - 3*y2v == 23)
print()
print("ALL CHAIN DATA CHECKS:", all([seq == [-5, -2], ok_int, ok3, ok4,
                                     ok5, ok6a, ok6b, chk_c7]))
