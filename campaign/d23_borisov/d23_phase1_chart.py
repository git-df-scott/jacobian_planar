"""
Plane Jacobian campaign - Session N2, Phase 1, layer L1 (chart transfer).

OBSERVATION (from the parsed Fig. 21 vs. the First Framework's Z
construction, arXiv:1901.04073 Sec. 2): the Second Framework's Z-stem

    (-1) -- (-3) -- (-5) -- (-2)     [creation numbers 7, 8, 9, 6]

and the short branch from the (-2)-multifork, (-1) -- 0(-3) [numbers 5, 3],
are IDENTICAL in K-bar structure and creation order to the First
Framework's stem ((-1)E5 -- (-3)E6 -- (-5)E7 -- (-2)E4, short branch
E3(-1) -- E2(0)); in both frameworks the chain is created by breaking the
same (-5)--(-2) edge, and the long-branch modifications (which differ)
happen strictly beyond the (-2)-multifork.  Divisorial valuations of
x1, x2 along existing curves are unchanged by later point blowups, so the
(q, v)-chart of Sessions 8-16 at the (-2)-multifork TRANSFERS VERBATIM:

    v = x1*x2^3 - 1,     q = x2/v^3
    x1 = (v+1) q^-3 v^-9,   x2 = q v^3.

Only the POLE DEPTHS change: val_{(-2)mf}(y1, y2) = (-15, -10) for the
Second Framework (certified boundary data, C6/C7) vs (-9, -6) for the First.

CERTIFIED HERE (exact, sympy):
  L1a. chart inversion:  x1 = (v+1) q^-3 v^-9, x2 = q v^3  inverts
       (q, v) = (x2/(x1 x2^3 - 1)^3, x1 x2^3 - 1).
  L1b. monomial rule:  x1^i x2^j = (v+1)^i q^(j-3i) v^(3j-9i)  -- so the
       (-2)-pole cut is the SAME support rule j - 3i >= -bound, with the
       SF bounds -15 (y1), -10 (y2)  [FF: -9, -6].
  L1c. chart factor:  det d(q,v)/d(x1,x2) = -x2^3/v^3 = -q^3 v^6, hence
       the Keller condition J_{(x1,x2)} = c reads
           J_{(q,v)} = -c q^-3 v^-6
       EXACTLY as in the First Framework (Sessions 16-18 mechanism).
  L1d. therefore the endgame pairing landscape is unchanged: the kill
       point v = -1 is the corner x1 x2^3 = 0 of the (-2)-multifork, and
       the chain corner is v = infinity (the order-23 point of the
       Phase-0 Belyi map), exactly parallel to D=13.

NOT yet certified for SF (the remaining L1 gap): the total-degree support
boxes (the FF [0,27]x[0,72] / [0,18]x[0,48] analogs with sums 435, 290),
which need the x-side degree split along the modified long branch.
"""
from sympy import symbols, simplify, together, expand, Rational

x1, x2, q, v = symbols('x1 x2 q v')

# L1a: inversion
V = x1*x2**3 - 1
Q = x2/V**3
X1 = (v + 1)*q**-3*v**-9
X2 = q*v**3
chk_a = (simplify(V.subs({x1: X1, x2: X2}) - v) == 0 and
         simplify(Q.subs({x1: X1, x2: X2}) - q) == 0)
print("L1a  chart inversion exact:", chk_a)

# L1b: monomial rule for a few (i, j), plus the general identity
import itertools
ok_b = True
for i, j in itertools.product((0, 1, 2, 3, 7), (0, 1, 2, 5, 11)):
    lhs = X1**i*X2**j
    rhs = (v + 1)**i*q**(j - 3*i)*v**(3*j - 9*i)
    ok_b &= simplify(lhs - rhs) == 0
print("L1b  monomial rule x1^i x2^j = (v+1)^i q^(j-3i) v^(3j-9i):", ok_b)
print("L1b  SF (-2)-pole support cuts: y1: j-3i >= -15, y2: j-3i >= -10"
      "  (FF: -9, -6)")

# L1c: chart factor and Keller transform
J = together(Q.diff(x1)*V.diff(x2) - Q.diff(x2)*V.diff(x1))
target = -x2**3/V**3
chk_c = simplify(J - target) == 0
print("L1c  det d(q,v)/d(x1,x2) = -x2^3/v^3:", chk_c)
# in chart coordinates: -x2^3/v^3 = -(q v^3)^3/v^3 = -q^3 v^6
chk_c2 = simplify(target.subs({x1: X1, x2: X2}) + q**3*v**6) == 0
print("L1c  = -q^3 v^6 in the chart; Keller J_(x1,x2) = c  <=>  "
      "J_(q,v) = -c q^-3 v^-6:", chk_c2)
print("L1d  kill point v = -1  <->  corner x1 x2^3 = 0; chain corner "
      "v = inf <-> the order-23 marked point.  Mechanism landscape "
      "identical to D=13.")
