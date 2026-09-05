#!/usr/bin/env python3
"""Exact checks accompanying PROOFS.md; not a formalization of its theorems."""
from pathlib import Path
import importlib.util
import json
import sys
import sympy as S

sys.dont_write_bytecode = True

x, y, s, p, t, z, w, r = S.symbols("x y s p t z w r")
checks = {}
data = {}


def zero(expr):
    assert S.cancel(expr) == 0, S.factor(expr)


def passed(name):
    checks[name] = True
    print("PASS", name)


def jac(f, g, a=x, b=y):
    return S.diff(f, a)*S.diff(g, b)-S.diff(f, b)*S.diff(g, a)


# The chart preserves the full function field; no subfield substitution.
sx = x*y+1
px = x*sx+1
ux = sx**2+y
zero((px-1)*ux-sx*(sx*px-1))
zero(jac(sx, px)+(px-1))
zero(((p-1)/s).subs({p: px, s: sx}, simultaneous=True)-x)
zero((s*(s-1)/(p-1)).subs({p: px, s: sx}, simultaneous=True)-y)
passed("birational_chart_and_volume")

# Universal quadratic completion, with arbitrary coefficient functions of p.
R, A, C = S.symbols("R A C")
B = (p-1)*A-R
H = p*R*s**2+B*s+(p-1)*(C-t)
D = B**2+4*p*R*(p-1)*(t-C)
zero((2*p*R*s+B)**2-D-4*p*R*H)
zero(S.diff(H, s)-(2*p*R*s+B))
passed("universal_hyperelliptic_identity")

# One source-derived high-degree example, not a degree sweep.
A16 = -S.Rational(1, 5)-S.Rational(3, 5)*p-S.Rational(11, 5)*p**2+p**3
B16 = S.expand((p-1)*A16-p**4)
D16 = S.expand(B16**2+4*t*p**5*(p-1))
assert S.degree(D16, p) == 6
assert S.gcd(S.Poly(D16, p, domain=S.QQ.frac_field(t)),
             S.Poly(S.diff(D16, p), p, domain=S.QQ.frac_field(t))).degree() == 0
data["degree16_source_example"] = {"A": str(A16), "B": str(B16),
    "D": str(D16), "compact_genus": 2, "time_form_infinity_orders": [1, 1]}
passed("higher_Briancon_example_squarefree_positive_genus")

# The simple-pole exceptional cases are retained, not divided away.
a1 = S.symbols("a1")
E_m1 = ((p-1)*a1-1)**2+4*t*(p-1)
zero(E_m1.subs(p, 0)-((a1+1)**2-4*t))
E_m2 = ((p-1)*a1-p)**2+4*t*p*(p-1)
zero(E_m2.subs(p, 0)-a1**2)
assert px.subs({x: -1, y: 0}) == 0
data["residue_squared_denominators"] = [str((a1+1)**2-4*t), str(a1**2)]
passed("exceptional_coefficient_residue_cases")

# Extract all residual equations in the degree-six elliptic primitive case.
u, v = S.symbols("u v")
d0, d1, d2, d3, d4 = S.symbols("d0 d1 d2 d3 d4")
Dz = d0+d1*z+d2*z**2+d3*z**3+d4*z**4
az = (u*z+v)/z**3
residual = S.Poly(S.cancel(z**4*(Dz*S.diff(az, z)+S.diff(Dz, z)*az/2)+1), z)
expected = [1-3*v*d0, -(4*u*d0+5*v*d1)/2,
    -(3*u*d1+4*v*d2)/2, -(2*u*d2+3*v*d3)/2,
    -(u*d3+2*v*d4)/2]
assert residual.degree() == 4
for i, e in enumerate(expected):
    zero(residual.nth(i)-e)
params = {d0: 5*d3**4/(16*d4**3), d1: d3**3/(2*d4**2),
          d2: 3*d3**2/(4*d4), v: 16*d4**3/(15*d3**4),
          u: -32*d4**4/(15*d3**5)}
for e in expected:
    zero(e.subs(params, simultaneous=True))
data["quartic_residual_equations"] = [str(e) for e in expected]
data["quartic_elimination"] = {str(k): str(val) for k, val in params.items()}
passed("complete_quartic_residual_extraction_and_elimination")

# An independent genus-one invariant check for the moving pencil.
a, c0, c1, c2, c3, c4 = S.symbols("a c0 c1 c2 c3 c4")
coeffs = [c0+4*a*(a-1)*t, c1+4*(2*a-1)*t, c2+4*t, c3, c4]
e0, e1, e2, e3, e4 = coeffs
I = S.expand(12*e4*e0-3*e3*e1+e2**2)
J = S.expand(72*e4*e2*e0+9*e3*e2*e1-27*e4*e1**2
             -27*e3**2*e0-2*e2**3)
assert S.Poly(I, t).LC() == 16
assert S.Poly(J, t).LC() == -128
assert S.degree(4*I**3-J**2, t) < 6
data["quartic_invariant_leading_terms"] = {"I": "16*t^2", "J": "-128*t^3",
    "discriminant_degree_bound": int(S.degree(4*I**3-J**2, t))}
passed("moving_quartic_modulus_invariant")

# A positive exact elliptic control: isotrivial pencils are not rejected.
Dstar = (z**4-2*z**3+3*z**2-4*z+5)/5
assert S.gcd(Dstar, S.diff(Dstar, z)) == 1
astar = (z+1)/(3*z**3)
zero(Dstar*S.diff(astar, z)+S.diff(Dstar, z)*astar/2+1/z**4)
Dt = t*Dstar
at = astar/t
zero(Dt*S.diff(at, z)+S.diff(Dt, z)*at/2+1/z**4)
# A second exact elliptic control with a different pole divisor order.
Dcontrol = z**4+t
acontrol = -1/(2*t*z**2)
zero(Dcontrol*S.diff(acontrol, z)+S.diff(Dcontrol, z)*acontrol/2-1/z**3)
passed("two_exact_elliptic_positive_controls")

# Attempted faithful rational reconstruction, followed by its exact failure.
Pmodel = w**2/Dstar
Qmodel = (z+1)*w/(3*Pmodel*z**3)
F = r**6/9+S.Rational(2, 15)*r**5+S.Rational(1, 45)
zero(Pmodel*Qmodel**2-F.subs(r, 1/z))
zero(jac(Pmodel, Qmodel, z, w)-2/(z**4*Dstar))
zero(S.diff(F, r)-S.Rational(2, 3)*r**4*(r+1))
assert F.subs(r, 0) == S.Rational(1, 45)
assert F.subs(r, -1) == 0
data["exact_degree6_model"] = {"Dstar": str(Dstar), "F": str(F),
    "F_prime": str(S.factor(S.diff(F, r))), "critical_values": ["1/45", "0"],
    "rational_chart_jacobian": str(S.factor(jac(Pmodel, Qmodel, z, w))),
    "primitive_degree": 6, "polynomial_Keller_chart": "excluded_by_Theorem_3"}
passed("degree6_reconstruction_and_nonzero_critical_value")

# Ordinary Keller maps and the sharp mixed-power boundary remain legal.
Pauto = x+y**2
Qauto = y+Pauto**3
zero(jac(Pauto, Qauto)-1)
zero(Pauto**2*Qauto**2-(Pauto*Qauto)**2)
# Rational mate distinct from a polynomial mate; a singular-gradient rational
# mate demonstrates why the theorem deliberately limits that case's scope.
P_rat = x*y**2+y
Q_rat = -x/(x*y+1)
zero(jac(P_rat, Q_rat)-1)
zero(jac(x**2, y/(2*x))-1)
# Retain the earlier global-potential positives and the nonterminating
# conductor-family negative control, without computing any new jets.
gate_path = Path(__file__).resolve().parents[1]/"astra6"/"verify_global_potential.py"
spec = importlib.util.spec_from_file_location("astra6_global_controls", gate_path)
gate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate_module)
data["retained_global_potential_controls"] = gate_module.criterion_controls()
passed("polynomial_Keller_and_rational_mate_positive_controls")

out = {"status": "OPEN_NO_COUNTEREXAMPLE", "arithmetic": "exact characteristic zero",
       "checks": checks, "data": data,
       "scope": "Identities and controls only; arbitrary-degree proofs are in PROOFS.md."}
Path(__file__).with_name("certificate.json").write_text(json.dumps(out, indent=2)+"\n")
print(f"{len(checks)} exact checks passed; certificate.json written.")
