# THEOREM (abstract near-miss Jacobian): for ANY differentiable P, R,
# with v = x1 x2^3 - 1, w = v^3/x2,
#   y1 = x1^3 x2^8 P(w),  y2 = x1^2 x2^5 v R(w)
# has J(y1,y2) = -h(w) * x1^4 * x2^12,  h = 2P'Rw - P(R+3wR').
# (FF Session 7's identity, now proved degree-independently: with h = h0
# constant this gives the near-miss Jacobian for BOTH frameworks.)
from sympy import symbols, Function, simplify, expand, together, diff
x1, x2, W = symbols('x1 x2 W')
P = Function('P')
R = Function('R')
v = x1*x2**3 - 1
w = v**3/x2
y1 = x1**3*x2**8*P(w)
y2 = x1**2*x2**5*v*R(w)
J = diff(y1, x1)*diff(y2, x2) - diff(y1, x2)*diff(y2, x1)
h = (2*diff(P(W), W)*R(W)*W - P(W)*(R(W) + 3*W*diff(R(W), W))).subs(W, w)
res = simplify(together(J + h*x1**4*x2**12))
print("ABSTRACT IDENTITY  J(y1,y2) == -h(w) x1^4 x2^12 :", res == 0)
