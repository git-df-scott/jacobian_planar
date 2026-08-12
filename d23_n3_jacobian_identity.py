"""
Plane Jacobian campaign - Session N2 continuation (N3).
THE MIRACLE-JACOBIAN IDENTITY, abstract and general.

Setting: v = x1 x2^3 - 1, w = v^3/x2, and the product ansatz
    y1 = x1^a x2^(3a-1) P(w),    y2 = x1^c x2^(3c-1) v R(w)
(the exponent relations b = 3a-1, d = 3c-1 are forced by the (-2)-pole
depths).  GENERAL IDENTITY (hand derivation via log-derivatives,
verified symbolically below for (a,c) = (3,2), (5,4), (4,3)):

    J(y1,y2) = (v+1)^(a+c-1) * [ (c-a) v P R  +  (v+1) P R
               + w( ((3-a)v+3) P R'  +  ((c-2)v-2) P' R ) ]

The bracket collapses to -h = -(2P'Rw - P(R+3wR')) IFF (a,c) = (3,2):
the First-Framework prefactors are the UNIQUE miracle pair.  Then
    J = -(v+1)^4 h(w) = -h(w) x1^4 x2^12,
which with h = h0 constant is the near-miss Jacobian -- Session 7's FF
spot-check upgraded to a degree-independent theorem, applying verbatim
to the Second Framework's certified (P, R) pair of degrees (14, 9).

CAVEAT (the session's honest correction): for the Second Framework,
deg P = 14 > 8 makes x1^3 x2^8 P(w) a LAURENT polynomial (x2-poles up
to order 6), so the (3,8)/(2,5) miracle map is Laurent, not the
polynomial near-miss; the polynomial object requires the long-branch
surgery (the paper's Fibonacci reconstruction ladder (60,40), (105,70),
(165,110), (270,180), (435,290) -- each rung the sum of the previous
two).  Constructing it is the first N4 task.
"""
from sympy import symbols, Function, simplify, together, diff

x1, x2, W = symbols('x1 x2 W')
P = Function('P')
R = Function('R')
v = x1*x2**3 - 1
w = v**3/x2
Pw, Rw = P(w), R(w)
Ppw = diff(P(W), W).subs(W, w)
Rpw = diff(R(W), W).subs(W, w)
h = 2*Ppw*Rw*w - Pw*(Rw + 3*w*Rpw)

for (a, c) in [(3, 2), (5, 4), (4, 3)]:
    y1 = x1**a*x2**(3*a - 1)*Pw
    y2 = x1**c*x2**(3*c - 1)*v*Rw
    J = diff(y1, x1)*diff(y2, x2) - diff(y1, x2)*diff(y2, x1)
    bracket = ((c - a)*v*Pw*Rw + (v + 1)*Pw*Rw
               + w*(((3 - a)*v + 3)*Pw*Rpw + ((c - 2)*v - 2)*Ppw*Rw))
    ok_gen = simplify(together(J - (v + 1)**(a + c - 1)*bracket)) == 0
    ok_mir = simplify(together(J + h*x1**(a + c - 1)*x2**(3*(a + c - 1)))) == 0
    print(f"(a,c) = ({a},{c}):  general identity: {ok_gen} | "
          f"miracle form J = -h x1^{a+c-1} x2^{3*(a+c-1)}: {ok_mir}"
          f"{'   <-- unique miracle pair' if ok_mir else ''}")
