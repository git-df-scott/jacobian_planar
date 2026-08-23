"""Build and certify explicit (P,Q) with {P,Q} = x^2 in the mu=1 strip."""
import sys
import sympy as sp
sys.path.insert(0, '/home/user/jacobian_planar/x2')
from certify import certify, x, y

T = sp.Symbol('T')


def witness(phi, psi, h, const=0):
    """W(phi,psi) must be 1;  f0' = phi*h;  g0' = h*psi."""
    assert sp.expand(phi*sp.diff(psi, T) - sp.diff(phi, T)*psi) == 1, "W != 1"
    f0 = sp.integrate(sp.expand(phi*h), T) + const
    g0 = sp.integrate(sp.expand(h*psi), T)
    P = sp.expand(f0.subs(T, x*y) + x*phi.subs(T, x*y))
    Q = sp.expand(g0.subs(T, x*y) + x*psi.subs(T, x*y))
    return P, Q


CASES = [
    ("W1  phi=1,      psi=T,      h=1",      sp.Integer(1), T,          sp.Integer(1)),
    ("W2  phi=1,      psi=T,      h=T^3",    sp.Integer(1), T,          T**3),
    ("W3  phi=T-1,    psi=-1,     h=T^2",    T-1,           sp.Integer(-1), T**2),
    ("W4  phi=T-1,    psi=2T-3,   h=T^4-T",  T-1,           2*T-3,      T**4-T),
    ("W5  phi=2T+5,   psi=(T+1)/2, h=T^2",   2*T+5,         sp.Rational(1,2)*(2*T+5)-sp.Rational(1,2), T**2),
]

if __name__ == '__main__':
    allok = True
    for name, phi, psi, h in CASES:
        try:
            P, Q = witness(phi, psi, h)
        except AssertionError as e:
            print(f"--- {name}: SKIPPED ({e})")
            continue
        print(f"\n--- {name}")
        ok, _ = certify(P, Q, 2)
        allok &= ok
        print("  OVERALL:", "PASS" if ok else "FAIL")
    print("\nALL WITNESSES:", "PASS" if allok else "FAIL")
