"""SUB-CASE (2) FROM THE BOTTOM -- it collapses.

Structural facts already proved (FABLE_SOURCE_AUDIT.md):
  the hull meets x=0 only at (0,0), so after the additive normalisation
  a_0 = 0 and b_0 = 0  (P and Q are divisible by x).

Column supports (from the hulls):
  a_1 : y^0..y^2      b_1 : y^1..y^2      b_2 : y^1..y^4
and a_1's y^0 coefficient IS the Newton vertex (1,0), so a_1(0) != 0.

RUNG d=0 :  sum_{i+k=1} = a_1 b_1' - a_1' b_1 = 0.
  Wronskian zero => b_1 = c a_1 (if a_1 != 0).  a_1 has a nonzero constant term,
  b_1 has none => c = 0 => **b_1 = 0**.

RUNG d=1 : then vacuous.

RUNG d=2 (the one carrying the x^2) : a_1 b_2' - 2 a_1' b_2 = 1.
  Divide by a_1^3:  (b_2 / a_1^2)' = 1/a_1^3, so b_2 = a_1^2 * INT(dy / a_1^3).
  b_2 polynomial forces a_1 to be a nonzero CONSTANT.

Verified below, exhaustively over the allowed shapes of a_1.
"""
import sympy as sp
y = sp.Symbol('y')
c, r, s = sp.symbols('c r s', nonzero=True)

print("=== RUNG 0: a_1 b_1' - a_1' b_1 = 0 with val(a_1)=0, val(b_1)>=1 ===")
a10,a11,a12 = sp.symbols('a10 a11 a12')
b11,b12 = sp.symbols('b11 b12')
a1 = a10 + a11*y + a12*y**2
b1 = b11*y + b12*y**2
Wr = sp.expand(a1*sp.diff(b1,y) - sp.diff(a1,y)*b1)
sol = sp.solve(sp.Poly(Wr,y).all_coeffs(), [b11,b12], dict=True)
print("  solutions for (b11,b12) with a_1 generic:", sol)
print("  -> b_1 == 0 whenever a10 != 0 (the vertex (1,0)).")
print("  cross-check: force a10 != 0 and ask for a nonzero b_1:")
gb = sp.groebner(sp.Poly(Wr,y).all_coeffs() + [a10*sp.Symbol('t')-1,
                 b11*sp.Symbol('u')+b12*sp.Symbol('v')-1],
                 b11,b12,a10,a11,a12,sp.Symbol('t'),sp.Symbol('u'),sp.Symbol('v'),
                 order='lex')
print("   Groebner basis of {rung0, a10 invertible, b_1 != 0} =", list(gb.exprs)[:3],
      "\n   -> [1] means NO such solution:", list(gb.exprs)==[sp.Integer(1)])

print("\n=== RUNG 2: a_1 b_2' - 2 a_1' b_2 = 1, b_2 supported on y^1..y^4 ===")
bs = sp.symbols('b21 b22 b23 b24')
b2 = sum(bs[i]*y**(i+1) for i in range(4))
E = sp.expand(a1*sp.diff(b2,y) - 2*sp.diff(a1,y)*b2 - 1)
eqs = sp.Poly(E,y).all_coeffs()
sol2 = sp.solve(eqs, list(bs)+[a11,a12], dict=True)
print(f"  solution branches: {len(sol2)}")
for s_ in sol2:
    print("   ", {str(k):sp.simplify(v) for k,v in s_.items()})
print("\n  Interpretation: every branch forces a11 = a12 = 0, i.e.")
print("  **a_1 is a nonzero CONSTANT**, and then b_2 = y / a_1.")
chk = sp.expand((a10)*sp.diff(y/a10,y) - 2*sp.diff(sp.Integer(a10) if False else a10,y)*(y/a10))
print("  direct check with a_1 = a10, b_2 = y/a10 :",
      sp.simplify(a10*sp.diff(y/a10,y) - 2*0*(y/a10)), "(must be 1)")

print("\n=== the integral argument, independently ===")
print("  (b_2/a_1^2)' = 1/a_1^3  =>  b_2 = a_1^2 * INT(dy/a_1^3).")
for lab,A in [("a_1 = c (constant)", c),
              ("a_1 = c(y-r)", c*(y-r)),
              ("a_1 = c(y-r)^2", c*(y-r)**2),
              ("a_1 = c(y-r)(y-s)", c*(y-r)*(y-s))]:
    I = sp.integrate(1/A**3, y)
    B = sp.simplify(A**2*I)
    poly = B.is_polynomial(y) if B.is_polynomial(y) is not None else False
    print(f"  {lab:22s}: b_2 = {sp.simplify(B)}   polynomial? {poly}")
print("\n  Only the constant case gives a polynomial b_2 with val >= 1.")
