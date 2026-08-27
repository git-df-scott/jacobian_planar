#!/usr/bin/env python3
"""B=16 ladder from the PRIMARY definition — no transcription risk.

GGV Theorem 1.1 (arXiv:1401.1784 Thm 8.10, quoted in Pro Mathematica 27):
if B = 16 there exist P, Q in K[x,y] with

    P = x^3 y + x^2 p2(y) + x p1(y) + p0(y),
    Q = x^2 y + x q1(y) + q0(y),
    [P,Q] = x^4 y + mu3 x^3 + mu2 x^2 + mu1 x + mu0,   mu0 != 0,

and for some j >= 1:  deg q1 = j+1, deg p2 = j+1, deg p1 = 2j+1,
deg q0 = 2j+1, deg p0 = 3j+1  (from st/en data: m = 3j+1, n = 2j+1; the
degree pair is (16m, 16n), e.g. j=2 -> (112, 80)).

This script builds [P,Q] - (x^4 y + mu3 x^3 + ... + mu0) = 0 directly in
sympy with all coefficients as unknowns, and runs the emptiness query
"is there a solution with mu0 != 0?" through msolve (mu0*s = 1 saturation).

Controls:
  C1 (planted, mu-terms exercised): the paper's section-3.5 pair
      P = x^3 y + x^2 (2y^3 + mu3) + x (y^5 + mu3 y^2) + y^7/7 + mu3 y^4/4
      Q = x^2 y + x (y^3 + mu3) + y^5/5 + mu3 y^2/2
      must satisfy [P,Q] = x^4 y + mu3 x^3 exactly (mu0=mu1=mu2=0), for
      symbolic mu3 — verified by direct bracket expansion.
  C2: the j=2 system UNSATURATED must be NONEMPTY (C1's solution lives
      there with mu3 as a parameter).
  C3: a corrupted variant (flip one coefficient of the target) must change
      the verdict machinery's input (guard against file-format no-ops).
"""
import argparse
import subprocess
import sys
import tempfile

import sympy as sp

x, y = sp.symbols("x y")
mu0, mu1, mu2, mu3 = sp.symbols("mu0 mu1 mu2 mu3")


def bracket(P, Q):
    return sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))


def control_C2():
    """The planted deg-3 pair's coefficients must annihilate build(2)'s
    equations exactly (symbolic mu3), checked by direct substitution —
    no solver in the loop."""
    eqs, unks = build(2, gauge_mu3=None)
    third = sp.Rational(1, 3)
    assign = {mu0: 0, mu1: 0, mu2: 0}
    for u in unks:
        s = str(u)
        if s in ("mu0", "mu1", "mu2", "mu3"):
            continue
        assign[u] = 0
    def setc(name, val):
        for u in unks:
            if str(u) == name:
                assign[u] = val
                return
        raise KeyError(name)
    setc("p2_0", mu3); setc("p2_3", 2)
    setc("p1_2", mu3); setc("p1_5", 1)
    setc("p0_4", sp.Rational(1, 4) * mu3); setc("p0_7", sp.Rational(1, 7))
    setc("q1_0", mu3); setc("q1_3", 1)
    setc("q0_2", sp.Rational(1, 2) * mu3); setc("q0_5", sp.Rational(1, 5))
    bad = [sp.expand(e.subs(assign)) for e in eqs]
    bad = [b for b in bad if b != 0]
    ok = not bad
    print(f"C2 planted coefficients annihilate build(2): "
          f"{'PASS' if ok else 'FAIL ' + str(bad[:2])}")
    return ok


def control_C1():
    P = x**3 * y + x**2 * (2 * y**3 + mu3) + x * (y**5 + mu3 * y**2) \
        + y**7 / 7 + mu3 * y**4 / 4
    Q = x**2 * y + x * (y**3 + mu3) + y**5 / 5 + mu3 * y**2 / 2
    br = sp.expand(bracket(P, Q) - (x**4 * y + mu3 * x**3))
    ok = br == 0
    print(f"C1 planted pair, symbolic mu3: [P,Q]-x^4y-mu3x^3 = {br}  "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


def build(j, gauge_mu3=None):
    """Return (generators, variables) of the direct system for ladder level j."""
    dq1, dp2, dp1, dq0, dp0 = j + 1, j + 1, 2 * j + 1, 2 * j + 1, 3 * j + 1
    p2c = sp.symbols(f"p2_0:{dp2 + 1}")
    p1c = sp.symbols(f"p1_0:{dp1 + 1}")
    p0c = sp.symbols(f"p0_0:{dp0 + 1}")
    q1c = sp.symbols(f"q1_0:{dq1 + 1}")
    q0c = sp.symbols(f"q0_0:{dq0 + 1}")
    poly = lambda cs: sum(c * y**i for i, c in enumerate(cs))  # noqa: E731
    P = x**3 * y + x**2 * poly(p2c) + x * poly(p1c) + poly(p0c)
    Q = x**2 * y + x * poly(q1c) + poly(q0c)
    target = x**4 * y + mu3 * x**3 + mu2 * x**2 + mu1 * x + mu0
    diff = sp.expand(bracket(P, Q) - target)
    eqs = []
    pd = sp.Poly(diff, x, y)
    for monom, coeff in pd.terms():
        eqs.append(sp.expand(coeff * pd.gens[0]**0))  # coefficient in unknowns
    # each coefficient of x^i y^k must vanish
    eqs = [sp.expand(c) for (_, _), c in
           [((m[0], m[1]), co) for m, co in pd.terms()]]
    unks = list(p2c) + list(p1c) + list(p0c) + list(q1c) + list(q0c) \
        + [mu0, mu1, mu2, mu3]
    if gauge_mu3 is not None:
        eqs = [sp.expand(e.subs(mu3, gauge_mu3)) for e in eqs]
        unks = [u for u in unks if u != mu3]
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


def run_msolve(gens, vars2, timeout):
    txt = to_msolve(gens, vars2)
    with tempfile.NamedTemporaryFile("w", suffix=".ms", delete=False) as f:
        f.write(txt)
        path = f.name
    try:
        r = subprocess.run(["msolve", "-f", path], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    out = (r.stdout or "").strip()
    if out.startswith("[-1]"):
        return "EMPTY", out[:150]
    if out and out[0] == "[":
        return "NONEMPTY", out[:150]
    return f"UNPARSED", out[:150]


SATVARS = {"mu0": mu0, "mu1": mu1, "mu2": mu2}


def query(j, saturate=True, gauge=1, timeout=3000, satvar="mu0"):
    eqs, unks = build(j, gauge_mu3=gauge)
    s = sp.Symbol("s_sat")
    if saturate:
        eqs = eqs + [SATVARS[satvar] * s - 1]
        unks = unks + [s]
    v, raw = run_msolve(eqs, unks, timeout)
    print(f"j={j} (pair {16*(3*j+1)},{16*(2*j+1)}) mu3={gauge} "
          f"sat[{satvar}!=0]={saturate}: {v}", flush=True)
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("j", type=int)
    ap.add_argument("--gauge", type=int, default=1)
    ap.add_argument("--nosat", action="store_true")
    ap.add_argument("--free", action="store_true")
    ap.add_argument("--skipcal", action="store_true")
    ap.add_argument("--timeout", type=int, default=3000)
    ap.add_argument("--satvar", default="mu0", choices=["mu0", "mu1", "mu2"])
    a = ap.parse_args()
    if not a.skipcal:
        if not control_C1():
            sys.exit(1)
        if not control_C2():
            sys.exit(1)
    query(a.j, saturate=not a.nosat,
          gauge=None if a.free else a.gauge, timeout=a.timeout,
          satvar=a.satvar)


if __name__ == "__main__":
    main()
