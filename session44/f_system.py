#!/usr/bin/env python3
"""The F-system: the paper's reduced B=16 system, derived mechanically.

Everything is derived HERE from the four bracket equations (the x^3..x^0
coefficients of [P,Q] = x^4 y + mu3 x^3 + mu2 x^2 + mu1 x + mu0 for
P = x^3 y + x^2 p2 + x p1 + p0, Q = x^2 y + x q1 + q0):

  eq3: 3y q1' + 2 p2 - 2y p2' - q1              = mu3
  eq2: 3y q0' + 2 p2 q1' + p1 - 2y p1' - p2' q1 = mu2
  eq1: 2 p2 q0' + p1 q1' - 2y p0' - p1' q1      = mu1
  eq0: p1 q0' - p0' q1                          = mu0

The paper's general solution of eq3:  q1 = mu3 + y^2 F',
p2 = mu3 + y F + (3/2) y^2 F'  for F in yK[y]  — VERIFIED symbolically here
(control D0).  eq2 then gives q0' and eq1 gives p0'; both are CHECKED against
the paper's printed (3.2)/(3.3) (controls D1, D2).  eq0 becomes the single
polynomial condition E(F, p1, mu's) = 0, plus two POLYNOMIALITY conditions
(the numerators of q0', p0' must be divisible by their y-denominators).

Unknowns per level j (deg q1 = j+1): F = sum_{1..j} F_i y^i (j coeffs),
p1 = sum_{0..2j+1} coeffs (2j+2), mu0..mu3 -> 3j + 6 unknowns.  Controls:
  D3: planted deg-3 solution (j=2: F = y^2/2, p1 = y^5 + mu3 y^2,
      mu0=mu1=mu2=0) annihilates the whole system, symbolic mu3.
  D4: j=2, mu3=1, mu0 != 0 saturated must be EMPTY (paper 3.5 + Abel deg-3).
Then the crack test: j=7 (deg q1 = 8), mu1 != 0.
"""
import argparse
import subprocess
import sys
import tempfile

import sympy as sp

y = sp.Symbol("y")
mu0, mu1, mu2, mu3 = sp.symbols("mu0 mu1 mu2 mu3")
Ff = sp.Function("Ff")(y)
p1f = sp.Function("p1f")(y)

q1_expr = mu3 + y**2 * sp.diff(Ff, y)
p2_expr = mu3 + y * Ff + sp.Rational(3, 2) * y**2 * sp.diff(Ff, y)


def derive():
    """Return (q0p, p0p, E) symbolically in terms of Ff, p1f, mu's."""
    q1, p2 = q1_expr, p2_expr
    # D0: eq3 must vanish identically
    eq3 = 3 * y * sp.diff(q1, y) + 2 * p2 - 2 * y * sp.diff(p2, y) - q1 - mu3
    assert sp.simplify(eq3) == 0, f"D0 FAIL: {sp.simplify(eq3)}"
    # eq2 -> q0'
    q0p = sp.simplify((mu2 - 2 * p2 * sp.diff(q1, y) - p1f
                       + 2 * y * sp.diff(p1f, y) + sp.diff(p2, y) * q1)
                      / (3 * y))
    # eq1 -> p0'
    p0p = sp.simplify((2 * p2 * q0p + p1f * sp.diff(q1, y)
                       - sp.diff(p1f, y) * q1 - mu1) / (2 * y))
    # eq0 -> E
    E = sp.simplify(p1f * q0p - p0p * q1 - mu0)
    return q0p, p0p, E


def controls_D1_D2(q0p, p0p):
    F, p1v = Ff, p1f
    Fp = sp.diff(F, y)
    Fpp = sp.diff(F, y, 2)
    printed_q0p = (-2 * p1v + 2 * mu2 + 2 * mu3 * F + 4 * y * sp.diff(p1v, y)
                   - 6 * y**2 * F * Fp - mu3 * y**2 * Fpp
                   - 4 * y**3 * Fp**2 - 4 * y**3 * F * Fpp
                   - 3 * y**4 * Fp * Fpp) / (6 * y)
    d1 = sp.simplify(q0p - printed_q0p)
    print(f"D1 (derived q0' == printed (3.2)): "
          f"{'PASS' if d1 == 0 else 'FAIL: ' + str(d1)}")
    printed_p0p = (y * p1v * (2 * Fp + y * Fpp) - mu1
                   - sp.diff(p1v, y) * (mu3 + y**2 * Fp)
                   + (2 * mu3 + y * (2 * F + 3 * y * Fp)) * q0p) / (2 * y)
    d2 = sp.simplify(p0p - printed_p0p)
    print(f"D2 (derived p0' == printed (3.3)): "
          f"{'PASS' if d2 == 0 else 'FAIL: ' + str(d2)}")
    return d1 == 0 and d2 == 0


def instantiate(j, q0p, p0p, E):
    Fc = sp.symbols(f"F1:{j + 1}")
    p1c = sp.symbols(f"P0:{2 * j + 2}")
    Fpoly = sum(c * y**i for i, c in enumerate(Fc, start=1))
    p1poly = sum(c * y**i for i, c in enumerate(p1c))
    sub = {Ff: Fpoly, p1f: p1poly}

    def inst(expr):
        e = expr.subs(sub)
        return sp.expand(sp.simplify(e.doit() if hasattr(e, "doit") else e))

    q0p_i = inst(q0p)
    p0p_i = inst(p0p)
    E_i = inst(E)
    eqs = []
    # E = 0 coefficientwise (E is a polynomial in y after clearing; take
    # numerator to be safe)
    En, Ed = sp.fraction(sp.together(E_i))
    eqs += sp.Poly(sp.expand(En), y).all_coeffs()
    # polynomiality: numerators of q0', p0' divisible by y
    for expr in (q0p_i, p0p_i):
        n, d = sp.fraction(sp.together(expr))
        k = sp.degree(d, y)
        n = sp.expand(n)
        for t in range(int(k)):
            eqs.append(n.coeff(y, t))
    unks = list(Fc) + list(p1c) + [mu0, mu1, mu2, mu3]
    eqs = [sp.expand(e) for e in eqs if sp.expand(e) != 0]
    return eqs, unks


def to_msolve(gens, vars2):
    vs = ",".join(str(v) for v in vars2)
    polys = []
    for g in gens:
        pe = sp.Poly(g, *vars2, domain="QQ")
        L = 1
        for c in pe.coeffs():
            L = sp.ilcm(L, sp.Rational(c).q)
        polys.append(str(sp.expand(g * L)).replace("**", "^").replace(" ", ""))
    return vs + "\n0\n" + ",\n".join(polys) + "\n"


def msolve_verdict(eqs, unks, timeout):
    txt = to_msolve(eqs, unks)
    with tempfile.NamedTemporaryFile("w", suffix=".ms", delete=False) as f:
        f.write(txt)
        path = f.name
    try:
        r = subprocess.run(["msolve", "-f", path], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    out = (r.stdout or "").strip()
    if out.startswith("[-1]"):
        return "EMPTY"
    if out and out[0] == "[":
        return "NONEMPTY " + out[:80].replace("\n", " ")
    return "NO-OUTPUT(OOM?)"


def query(j, satvar, gauge, timeout, q0p, p0p, E):
    eqs, unks = instantiate(j, q0p, p0p, E)
    if gauge is not None:
        eqs = [sp.expand(e.subs(mu3, gauge)) for e in eqs]
        unks = [u for u in unks if u != mu3]
    s = sp.Symbol("s_sat")
    sv = {"mu0": mu0, "mu1": mu1, "mu2": mu2}[satvar]
    eqs = eqs + [sv * s - 1]
    unks = unks + [s]
    v = msolve_verdict(eqs, unks, timeout)
    print(f"F-system j={j} (deg q1={j+1}) mu3={gauge} sat[{satvar}!=0]: {v}",
          flush=True)
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("j", type=int)
    ap.add_argument("--satvar", default="mu0", choices=["mu0", "mu1", "mu2"])
    ap.add_argument("--gauge", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=3000)
    ap.add_argument("--skipcal", action="store_true")
    a = ap.parse_args()
    q0p, p0p, E = derive()
    print("D0 (eq3 identity for the paper's q1,p2 ansatz): PASS")
    if not a.skipcal:
        if not controls_D1_D2(q0p, p0p):
            sys.exit(1)
        # D3: planted deg-3 solution annihilates the j=2 system
        eqs, unks = instantiate(2, q0p, p0p, E)
        assign = {u: 0 for u in unks if str(u) not in ("mu0", "mu1", "mu2",
                                                       "mu3")}
        assign.update({mu0: 0, mu1: 0, mu2: 0})
        for u in unks:
            if str(u) == "F2":
                assign[u] = sp.Rational(1, 2)
            if str(u) == "P5":
                assign[u] = 1
            if str(u) == "P2":
                assign[u] = mu3
        bad = [sp.expand(e.subs(assign)) for e in eqs]
        bad = [b for b in bad if b != 0]
        print(f"D3 (planted deg-3 solution annihilates j=2 system): "
              f"{'PASS' if not bad else 'FAIL ' + str(bad[:2])}")
        if bad:
            sys.exit(1)
        v = query(2, "mu0", 1, a.timeout, q0p, p0p, E)
        print(f"D4 (j=2 mu0!=0 must be EMPTY): "
              f"{'PASS' if v == 'EMPTY' else 'FAIL'}")
        if v != "EMPTY":
            sys.exit(1)
    query(a.j, a.satvar, a.gauge, a.timeout, q0p, p0p, E)


if __name__ == "__main__":
    main()
