#!/usr/bin/env python3
"""What the eighth-power theorem SAYS: P and Q are powers of one cubic.

The upper edge of N(P) runs (0,8) -> (8,16), so j - i = 8 is constant on it.
Grade by w(x^i y^j) := j - i.  The upper edge is the MAXIMUM of w on N(P) (w=8)
and on N(Q) (w=12), and the w-initial forms are y^8 A(xy) and y^12 Qh(xy).
With A(t) = c0 (t-tau)^8 and Qh(t) = c1 (t-tau)^12:

    In_w(P) = c0 u^8 ,  In_w(Q) = c1 u^12 ,   u := y(xy - tau) = x y^2 - tau y .

u is w-homogeneous of weight 1 and is a CUBIC.
"""
import sympy as sp
x, y, t, tau, c0, c1 = sp.symbols('x y t tau c0 c1')
u = x*y**2 - tau*y
def br(f, g): return sp.diff(f,x)*sp.diff(g,y) - sp.diff(f,y)*sp.diff(g,x)
A  = sp.expand(c0*(t-tau)**8); Qh = sp.expand(c1*(t-tau)**12)
InP = sp.expand(y**8*A.subs(t, x*y)); InQ = sp.expand(y**12*Qh.subs(t, x*y))
print("u =", u, "= ", sp.factor(u), " total degree", sp.Poly(u,x,y).total_degree())
print("w(x y^2) =", 2-1, " w(y) =", 1-0, "-> u is w-homogeneous of weight 1")
print("\nCONTROL In_w(P) == c0 u^8 :", sp.simplify(InP - c0*u**8) == 0)
print("CONTROL In_w(Q) == c1 u^12:", sp.simplify(InQ - c1*u**12) == 0)
print("CONTROL {In_w(P), In_w(Q)} == 0:", sp.simplify(br(InP, InQ)) == 0)
print("   -> the top w-piece of {P,Q} vanishes identically, exactly as")
print("      {P,Q} = x^2 (w = -2, against 8+12 = 20) demands.")
pt, qt = sp.Function('pt')(x,y), sp.Function('qt')(x,y)
chk = sp.simplify(br(u, 2*c0*qt - 3*c1*u**4*pt) - (2*c0*br(u,qt) - 3*c1*u**4*br(u,pt)))
print("\nnext w-order: 8 c0 u^7 {u,qt} - 12 c1 u^11 {u,pt} = 0  <=>  {u, 2c0 qt - 3c1 u^4 pt} = 0")
print("CONTROL {u, u^4 pt} = u^4 {u,pt}:", chk == 0)
print("=> qtilde = (3 c1 u^4 ptilde + lambda u^11) / (2 c0):  Q's next order is")
print("   DETERMINED by P's, up to one constant.")
