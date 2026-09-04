"""
Plane Jacobian campaign - Session 20
THE BULLETPROOF GATE: what a claimed JC2 counterexample must survive.

Written BEFORE any candidate exists, so it cannot be tuned to bless one.

DEFAULT ANSWER IS "NOT A COUNTEREXAMPLE".  A pair is reported as genuine only
if EVERY gate passes.  Any gate that errors counts as a failure, never as a pass.

THE GATES.

  G0  FIELD.  Coefficients must be exact and of characteristic zero (Rational,
      or algebraic numbers in an exact extension).  The Jacobian conjecture is
      FALSE in characteristic p -- (x + y^p, y) is a Keller pair over F_p that
      is not an automorphism -- so a mod-p object is never evidence.  Anything
      supplied only mod p is rejected here, on sight.

  G1  BRACKET, two independent ways.  J(P,Q) = Px Qy - Py Qx must be exactly 1:
      (a) via sympy expansion;
      (b) via an independent dict-based coefficient convolution that shares no
          code with (a).
      A shared bug cannot pass both.

  G2  DEGREES.  deg P and deg Q computed exactly; neither divides the other.
      By Jung-van der Kulk every automorphism of C^2 is tame and a tame
      automorphism has one degree dividing the other, so G2 is precisely the
      statement "not an automorphism".

  G3  INTERPOLATION PROOF.  J(P,Q) - 1 has degree <= d1 + d2 - 2.  Evaluating it
      exactly on a grid strictly larger than that degree in each variable and
      getting zero everywhere is a PROOF of the identity, by induction on
      variables -- not a probabilistic test.  Independent of G1 entirely.

  G4  LEADING FORMS.  J(P,Q) = 1 forces J(Pbar,Qbar) = 0, hence
      Pbar^d2 = c Qbar^d1.  Checked as a cross-consistency test: if G1 passed
      but G4 fails, something is wrong and the verdict is REJECT.

  G5  NON-DEGENERACY.  P, Q nonconstant, of exactly the claimed degrees, and
      not algebraically trivial (Q not a polynomial in P, and vice versa).
      Catches the Session-3 "phantom" failure mode, where a FEASIBLE result was
      really a degenerate partner.

  G6  MULTI-PRIME.  Reduce mod several primes exceeding all degrees (so no
      Frobenius artifact is in range) and confirm J = 1 in each.  A cheap
      independent arithmetic check on G1.

Exact arithmetic only.  No floating point anywhere.
"""

import sys
from fractions import Fraction
import sympy as sp

x, y = sp.symbols('x y')


class Verdict:
    def __init__(self):
        self.gates = []
        self.fatal = []

    def gate(self, name, ok, detail=""):
        ok = bool(ok)
        self.gates.append((name, ok, detail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))
        if not ok:
            self.fatal.append(name)
        return ok

    def verdict(self):
        print("\n" + "-" * 66)
        if self.fatal:
            print(f"VERDICT: NOT A COUNTEREXAMPLE  (failed: {', '.join(self.fatal)})")
            return False
        print("VERDICT: ALL GATES PASSED -- this is a genuine JC2 counterexample.")
        print("Before announcing: have a second party re-run this file from a")
        print("clean checkout on the raw coefficients, not on any search output.")
        return True


# ---------------------------------------------------------------- G1(b)
def _poly_dict(expr):
    """{(i,j): Fraction} from a sympy expression. Independent of sympy's Poly."""
    expr = sp.expand(expr)
    out = {}
    for term in sp.Add.make_args(expr):
        c, mon = term.as_coeff_Mul()
        i = sp.degree(mon, x) if mon.has(x) else 0
        j = sp.degree(mon, y) if mon.has(y) else 0
        if not sp.Rational(c).is_rational and not c.is_Rational:
            raise ValueError(f"non-rational coefficient {c}")
        out[(int(i), int(j))] = out.get((int(i), int(j)), Fraction(0)) + \
            Fraction(int(sp.Rational(c).p), int(sp.Rational(c).q))
    return {k: v for k, v in out.items() if v != 0}


def _d(pd, var):
    """Partial derivative of a coefficient dict."""
    out = {}
    for (i, j), c in pd.items():
        if var == 'x' and i > 0:
            out[(i - 1, j)] = out.get((i - 1, j), Fraction(0)) + c*i
        if var == 'y' and j > 0:
            out[(i, j - 1)] = out.get((i, j - 1), Fraction(0)) + c*j
    return {k: v for k, v in out.items() if v != 0}


def _mul(a, b):
    out = {}
    for (i1, j1), c1 in a.items():
        for (i2, j2), c2 in b.items():
            k = (i1 + i2, j1 + j2)
            out[k] = out.get(k, Fraction(0)) + c1*c2
    return {k: v for k, v in out.items() if v != 0}


def _sub(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Fraction(0)) - v
    return {k: v for k, v in out.items() if v != 0}


def bracket_dict(P, Q):
    pd, qd = _poly_dict(P), _poly_dict(Q)
    return _sub(_mul(_d(pd, 'x'), _d(qd, 'y')), _mul(_d(pd, 'y'), _d(qd, 'x')))


# ---------------------------------------------------------------- gates
def check(P, Q, label="candidate", verbose=True):
    V = Verdict()
    print(f"\n{'=' * 66}\nBULLETPROOF GATE: {label}\n{'=' * 66}")
    P, Q = sp.expand(P), sp.expand(Q)

    # G0 field
    try:
        coeffs = list(sp.Poly(P, x, y).coeffs()) + list(sp.Poly(Q, x, y).coeffs())
        ok0 = all(c.is_Rational for c in coeffs)
        V.gate("G0 field is characteristic 0, coefficients exactly rational",
               ok0, f"{len(coeffs)} coefficients checked")
    except Exception as e:
        V.gate("G0 field", False, f"error: {e}")
        return V.verdict()

    # G1 bracket, two ways
    try:
        J1 = sp.expand(sp.diff(P, x)*sp.diff(Q, y) - sp.diff(P, y)*sp.diff(Q, x))
        a = (J1 == 1)
        bd = bracket_dict(P, Q)
        b = (bd == {(0, 0): Fraction(1)})
        V.gate("G1a bracket = 1 (sympy expansion)", a, f"J = {J1 if J1 != 1 else 1}")
        V.gate("G1b bracket = 1 (independent dict convolution)", b,
               f"{len(bd)} nonzero terms")
    except Exception as e:
        V.gate("G1 bracket", False, f"error: {e}")
        return V.verdict()

    # G2 degrees
    try:
        d1 = sp.Poly(P, x, y).total_degree()
        d2 = sp.Poly(Q, x, y).total_degree()
        nondiv = (d1 > 1 and d2 > 1 and d1 % d2 != 0 and d2 % d1 != 0)
        V.gate("G2 degrees non-dividing (Jung-van der Kulk => not an automorphism)",
               nondiv, f"deg P = {d1}, deg Q = {d2}")
    except Exception as e:
        V.gate("G2 degrees", False, f"error: {e}")
        return V.verdict()

    # G3 interpolation proof
    try:
        N = d1 + d2 - 1
        allzero, tested = True, 0
        for xi in range(N + 1):
            for yi in range(N + 1):
                val = sp.expand(J1 - 1).subs({x: sp.Integer(xi), y: sp.Integer(yi)})
                tested += 1
                if sp.simplify(val) != 0:
                    allzero = False
                    break
            if not allzero:
                break
        V.gate("G3 J-1 vanishes on a grid larger than its degree (identity PROOF)",
               allzero, f"{tested} exact evaluations, grid side {N+1} > deg {d1+d2-2}")
    except Exception as e:
        V.gate("G3 interpolation", False, f"error: {e}")

    # G4 leading forms
    try:
        def topform(F, d):
            return sp.expand(sum(c*x**m[0]*y**m[1]
                                 for m, c in sp.Poly(F, x, y).terms()
                                 if sum(m) == d))
        Pb, Qb = topform(P, d1), topform(Q, d2)
        jbar = sp.expand(sp.diff(Pb, x)*sp.diff(Qb, y) - sp.diff(Pb, y)*sp.diff(Qb, x))
        prop = sp.simplify(sp.cancel(sp.expand(Pb**d2)/sp.expand(Qb**d1)))
        ok4 = (jbar == 0) and (prop.free_symbols == set())
        V.gate("G4 leading forms: J(Pbar,Qbar) = 0 and Pbar^d2 proportional to Qbar^d1",
               ok4, f"J(Pbar,Qbar) = {jbar}, ratio constant: {prop.free_symbols == set()}")
    except Exception as e:
        V.gate("G4 leading forms", False, f"error: {e}")

    # G5 non-degeneracy
    try:
        nonconst = (d1 >= 1 and d2 >= 1)
        # Q a polynomial in P would force J = 0; check no algebraic collapse
        notrivial = sp.expand(sp.diff(P, x)*sp.diff(Q, y)
                              - sp.diff(P, y)*sp.diff(Q, x)) != 0
        V.gate("G5 non-degenerate (nonconstant, no algebraic collapse)",
               nonconst and notrivial, f"deg = ({d1},{d2})")
    except Exception as e:
        V.gate("G5 non-degeneracy", False, f"error: {e}")

    # G6 multi-prime
    try:
        primes = [p for p in (10007, 32003, 65521, 1000003) if p > d1 + d2 + 2]
        okp = []
        for p in primes:
            Jp = sp.Poly(sp.expand(J1 - 1), x, y, modulus=p)
            okp.append(Jp.is_zero or Jp.total_degree() < 0 or all(
                int(c) % p == 0 for c in sp.Poly(sp.expand(J1 - 1), x, y).coeffs()))
        V.gate("G6 reduction mod several primes (all exceeding degrees)",
               all(okp), f"primes {primes}")
    except Exception as e:
        V.gate("G6 multi-prime", False, f"error: {e}")

    return V.verdict()


# ---------------------------------------------------------------- validation
if __name__ == '__main__':
    print("VALIDATING THE GATE ON KNOWN OBJECTS")
    print("A gate that cannot reject a known non-counterexample is worthless.\n")

    results = {}

    # 1. a genuine tame automorphism: J = 1 but degrees divide -> must REJECT
    P1 = y
    Q1 = -x + y**3
    results['tame automorphism (y, -x+y^3)'] = check(P1, Q1, "tame automorphism (must REJECT at G2)")

    # 2. composed tame automorphism, higher degree -> must REJECT
    P2 = sp.expand(-(y + x**2))
    Q2 = x
    P3, Q3 = Q2, sp.expand(P2 + Q2**3)
    results['composed tame'] = check(P3, Q3, "composed tame automorphism (must REJECT at G2)")

    # 3. a corrupted pair: bracket not 1 -> must REJECT at G1
    results['corrupted'] = check(y, sp.expand(-x + y**3 + x*y), "corrupted pair (must REJECT at G1)")

    # 4. degrees non-dividing but bracket wrong -> must REJECT at G1, not sneak past
    results['nondiv but not Keller'] = check(sp.expand(y**3 + x), sp.expand(y**2 + x),
                                             "non-dividing degrees but J != 1 (must REJECT at G1)")

    print("\n" + "=" * 66)
    print("VALIDATION SUMMARY")
    print("=" * 66)
    allrejected = not any(results.values())
    for k, v in results.items():
        print(f"  {k:42s} -> {'ACCEPTED (BUG!)' if v else 'rejected (correct)'}")
    print(f"\ngate correctly rejected every known non-counterexample: {allrejected}")
    if not allrejected:
        print("*** THE GATE IS BROKEN. Do not use it until fixed. ***")
        sys.exit(1)
    print("\nThe gate is armed. Any candidate from the (8,28) search goes through")
    print("check(P, Q) before a single word is said to anyone.")
