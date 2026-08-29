"""night19 -- the transport of the all-D statement along Jacobian-1 moves.

L1  If T = (T1, T2) is a polynomial map with det J(T) = 1 then
    [P o T, Q o T] = [P, Q] o T.  Hence P has a polynomial mate iff P o T does.
L2  Adding a constant to P changes nothing: [P + k, Q] = [P, Q].
L3  For the night18 deg h = 1 stratum (FAMILY.md 1.1)
        P = gamma (x-a) y^2 + (h0 + h1 x) y + h1^2/(4 gamma) x
            + (a h1^2 + 2 h0 h1 - alpha)/(4 gamma),
    the explicit Jacobian-1 map  T(x,y) = (x + a, y - h1/(2 gamma))  gives
        P o T = gamma x y^2 + c y + (a constant),   c = h(a) = h0 + h1 a,
    checked here symbolically over Q(gamma, a, alpha, h0, h1).
"""
import json, os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
x, y = sp.symbols('x y')
gam, a, al, h0, h1, c = sp.symbols('gamma a alpha h0 h1 c')
OUT = {}

print("=" * 78)
print("L1  Jacobian-1 invariance of the bracket")
print("=" * 78)
u, v = sp.symbols('u v')
# a random Jacobian-1 map and random P, Q
T1 = x + y**3
T2 = y + 2 * x**2 + 3 * x * y**3 + 3 * sp.Rational(1, 1) * x  # will be fixed below
# build a genuine J=1 map: T = (x + y^3, y) o (x, y + x^2) -- both triangular
A1 = (x + y**3, y)
A2 = (x, y + x**2 - 5 * x)
T = (A1[0].subs({x: A2[0], y: A2[1]}), A1[1].subs({x: A2[0], y: A2[1]}))
J = sp.simplify(sp.diff(T[0], x) * sp.diff(T[1], y) - sp.diff(T[0], y) * sp.diff(T[1], x))
Pt = 3 * x**2 * y - y**4 + x
Qt = x * y + y**2 - 7
br = sp.diff(Pt, x) * sp.diff(Qt, y) - sp.diff(Pt, y) * sp.diff(Qt, x)
PT = Pt.subs({x: T[0], y: T[1]}, simultaneous=True)
QT = Qt.subs({x: T[0], y: T[1]}, simultaneous=True)
brT = sp.diff(PT, x) * sp.diff(QT, y) - sp.diff(PT, y) * sp.diff(QT, x)
lhs = sp.expand(brT)
rhs = sp.expand(br.subs({x: T[0], y: T[1]}, simultaneous=True))
print("  T = %s ,  det J(T) = %s" % (sp.sstr(T), sp.sstr(J)))
print("  [P o T, Q o T] - ([P,Q] o T) expands to %s   (must be 0)" % sp.sstr(sp.expand(lhs - rhs)))
OUT["L1"] = {"T": sp.sstr(T), "detJ": sp.sstr(J), "residual": sp.sstr(sp.expand(lhs - rhs))}
assert J == 1 and sp.expand(lhs - rhs) == 0

print()
print("=" * 78)
print("L3  the explicit move to the slice, over Q(gamma, a, alpha, h0, h1)")
print("=" * 78)
P = (gam * (x - a) * y**2 + (h0 + h1 * x) * y + h1**2 / (4 * gam) * x
     + (a * h1**2 + 2 * h0 * h1 - al) / (4 * gam))
PT = sp.expand(sp.together(P.subs({x: x + a, y: y - h1 / (2 * gam)}, simultaneous=True)))
R = gam * x * y**2 + (h0 + h1 * a) * y
diff = sp.simplify(sp.expand(PT - R))
print("  P o T - ( gamma x y^2 + h(a) y ) = %s" % sp.sstr(sp.simplify(diff)))
print("  is it free of x and y (i.e. a constant)? %s"
      % (sp.simplify(sp.diff(diff, x)) == 0 and sp.simplify(sp.diff(diff, y)) == 0))
OUT["L3"] = {"P_o_T_minus_R": sp.sstr(sp.simplify(diff)),
             "is_constant": bool(sp.simplify(sp.diff(diff, x)) == 0
                                 and sp.simplify(sp.diff(diff, y)) == 0),
             "c_equals": "h(a) = h0 + h1*a"}
assert OUT["L3"]["is_constant"]
json.dump(OUT, open(os.path.join(HERE, 'cor19.json'), 'w'), indent=1)
print()
print("TRANSPORT CHECKS PASS")
