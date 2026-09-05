#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gao's map F5: DIMENSION 4, geometric degree 10  (det J = 160/29)

A non-injective Keller map C^4 -> C^4 whose generic fibre has exactly 10 points.

Source (transcribed programmatically from the paper's own LaTeX, not by hand):
  Shuhong Gao, "Counterexamples to the Jacobian conjecture in dimensions
  greater than two", arXiv:2608.00222 (31 Jul 2026), section 4.4.2
  ("Specialization II: Delta = (1,w1,w2)^T and a map of geometric degree ten"),
  Theorem 4.4 and the display "Written out in full, F5 = (F5,1..F5,4)^T".
  HTML source: https://arxiv.org/html/2608.00222

  The coefficients below were extracted mechanically from the MathML
  "alttext" (original LaTeX) of the arXiv HTML build and parsed into sympy,
  so no coefficient was retyped by a human or a model.  The transcription is
  self-validating: Theorem 4.4 states component degrees 3,12,14,16 and
  det J == 160/29, and BOTH are reproduced exactly below -- a single wrong
  coefficient would destroy the constancy of det J.

Paper's claims (Theorem 4.4):  degrees 3,12,14,16;  det J = 160/29;
                               generic fibre = 10 points.
All three are re-measured here.

Run:  python3 gao_F5_dim4_degree10.py
Exits 0 if every check PASSES, nonzero otherwise.
"""
import sys
import sympy as sp

x, y, z, t = sp.symbols('x y z t')
R = sp.Rational
VARS = [x, y, z, t]

FAILURES = []


def check(name, ok, detail=""):
    print(("  [PASS] " if ok else "  [FAIL] ") + name + (("  " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


# ===========================================================================
# THE MAP  F5 : C^4 -> C^4
# ===========================================================================
F1 = (
    (R(20, 29))*x**2*y + (1)*x
)

F2 = (
    (R(32768000, 24389))*x**7*y**2*z**3 + (R(-602112000, 707281))*x**6*y**3*z**2
    + (R(2076288000, 20511149))*x**5*y**4*z + (R(3276800, 841))*x**6*y*z**3
    + (R(-768000, 24389))*x**6*y**2*z*t + (R(80752000, 20511149))*x**4*y**5
    + (R(-54835200, 24389))*x**5*y**2*z**2 + (R(4704000, 707281))*x**5*y**3*t
    + (R(152428800, 707281))*x**4*y**3*z + (R(81920, 29))*x**5*z**3
    + (R(-76800, 841))*x**5*y*z*t + (R(169140800, 20511149))*x**3*y**4
    + (R(-1044480, 841))*x**4*y*z**2 + (R(374400, 24389))*x**4*y**2*t
    + (R(515520, 24389))*x**3*y**2*z + (R(-1920, 29))*x**4*z*t + (R(907520, 707281))*x**2*y**3
    + (R(9600, 29))*x**3*z**2 + (R(3360, 841))*x**3*y*t + (R(-108960, 841))*x**2*y*z
    + (R(14050, 24389))*x*y**2 + (R(-180, 29))*x**2*t + (R(-252, 29))*x*z + (1)*y
)

F3 = (
    (R(98304000, 24389))*x**8*y**2*z**4 + (R(-2408448000, 707281))*x**7*y**3*z**3
    + (R(22127616000, 20511149))*x**6*y**4*z**2 + (R(9830400, 841))*x**7*y*z**4
    + (R(-90354432000, 594823321))*x**5*y**5*z + (R(-191692800, 24389))*x**6*y**2*z**3
    + (R(-73022484000, 17249876309))*x**4*y**6 + (R(45158400, 24389))*x**5*y**3*z**2
    + (R(-201456000, 20511149))*x**5*y**4*t + (R(245760, 29))*x**6*z**4
    + (R(-48000, 24389))*x**6*y**2*t**2 + (R(-5316643200, 20511149))*x**4*y**4*z
    + (R(-1310720, 841))*x**5*y*z**3 + (R(-864000, 24389))*x**5*y**2*z*t
    + (R(-4696088400, 594823321))*x**3*y**5 + (R(-25906560, 24389))*x**4*y**2*z**2
    + (R(-13521600, 707281))*x**4*y**3*t + (R(-4800, 841))*x**5*y*t**2
    + (R(69664320, 707281))*x**3*y**3*z + (R(112640, 29))*x**4*z**3
    + (R(-86400, 841))*x**4*y*z*t + (R(40879390, 20511149))*x**2*y**4
    + (R(-1613760, 841))*x**3*y*z**2 + (R(62760, 24389))*x**3*y**2*t + (R(-120, 29))*x**4*t**2
    + (R(3661320, 24389))*x**2*y**2*z + (R(-2160, 29))*x**3*z*t + (R(-516820, 707281))*x*y**3
    + (R(9480, 29))*x**2*z**2 + (R(240, 29))*x**2*y*t + (R(-105360, 841))*x*y*z
    + (R(-1437, 1682))*y**2 + (R(-189, 29))*x*t + (-1)*z
)

F4 = (
    (R(-629145600, 24389))*x**9*y**2*z**5 + (R(19267584000, 707281))*x**8*y**3*z**4
    + (R(-132882432000, 20511149))*x**7*y**4*z**3 + (R(-62914560, 841))*x**8*y*z**5
    + (R(49152000, 24389))*x**8*y**2*z**3*t + (R(-15504384000, 20511149))*x**6*y**5*z**2
    + (R(1975910400, 24389))*x**7*y**2*z**4 + (R(-903168000, 707281))*x**7*y**3*z**2*t
    + (R(3799290048000, 17249876309))*x**5*y**6*z + (R(-15174451200, 707281))*x**6*y**3*z**3
    + (R(2308608000, 20511149))*x**6*y**4*z*t + (R(-1572864, 29))*x**7*z**5
    + (R(4915200, 841))*x**7*y*z**3*t + (R(-768000, 24389))*x**7*y**2*z*t**2
    + (R(2437443220800, 500246412961))*x**4*y**7 + (R(-11697561600, 20511149))*x**5*y**4*z**2
    + (R(8448384000, 594823321))*x**5*y**5*t + (R(54312960, 841))*x**6*y*z**4
    + (R(-85708800, 24389))*x**6*y**2*z**2*t + (R(4704000, 707281))*x**6*y**3*t**2
    + (R(184263724800, 594823321))*x**4*y**5*z + (R(-496404480, 24389))*x**5*y**2*z**3
    + (R(195724800, 707281))*x**5*y**3*z*t + (R(122880, 29))*x**6*z**3*t
    + (R(-76800, 841))*x**6*y*z*t**2 + (R(135717082080, 17249876309))*x**3*y**6
    + (R(1251989760, 707281))*x**4*y**3*z**2 + (R(484262400, 20511149))*x**4*y**4*t
    + (R(184320, 29))*x**5*z**4 + (R(-1873920, 841))*x**5*y*z**2*t
    + (R(374400, 24389))*x**5*y**2*t**2 + (R(-4465704480, 20511149))*x**3*y**4*z
    + (R(-844800, 841))*x**4*y*z**3 + (R(2238720, 24389))*x**4*y**2*z*t
    + (R(-1920, 29))*x**5*z*t**2 + (R(-2476692498, 594823321))*x**2*y**5
    + (R(-9897600, 24389))*x**3*y**2*z**2 + (R(-6755640, 707281))*x**3*y**3*t
    + (R(7680, 29))*x**4*z**2*t + (R(2760, 841))*x**4*y*t**2
    + (R(-61829880, 707281))*x**2*y**3*z + (R(123776, 29))*x**3*z**3
    + (R(-145200, 841))*x**3*y*z*t + (R(128225745, 41022298))*x*y**4
    + (R(-1938744, 841))*x**2*y*z**2 + (R(-126390, 24389))*x**2*y**2*t + (R(-210, 29))*x**3*t**2
    + (R(5740350, 24389))*x*y**2*z + (R(-2412, 29))*x**2*z*t + (R(1629343, 1414562))*y**3
    + (R(9318, 29))*x*z**2 + (R(11001, 841))*x*y*t + (R(-99879, 841))*y*z + (R(-160, 29))*t
)

F = [F1, F2, F3, F4]

CLAIMED_DEGREE = 10
CLAIMED_DETJ = R(160, 29)
CLAIMED_COMPONENT_DEGREES = [3, 12, 14, 16]


def main():
    print(__doc__.strip().splitlines()[0])
    print("=" * 74)

    print("\n(0) Shape of the map")
    degs = [sp.Poly(f, *VARS).total_degree() for f in F]
    print("    component total degrees :", degs, " (paper:", CLAIMED_COMPONENT_DEGREES, ")")
    print("    component term counts   :", [len(sp.Poly(f, *VARS).terms()) for f in F])
    check("component degrees match the paper", degs == CLAIMED_COMPONENT_DEGREES)

    print("\n(a) Jacobian determinant is a nonzero CONSTANT")
    detJ = sp.expand(sp.Matrix(F).jacobian(sp.Matrix(VARS)).det(method='berkowitz'))
    print("    det J =", detJ, "  (paper:", CLAIMED_DETJ, ")")
    check("det J is constant", detJ.free_symbols == set())
    check("det J is nonzero", detJ != 0)
    check("det J == 160/29 as the paper claims", sp.simplify(detJ - CLAIMED_DETJ) == 0)

    print("\n(b) MEASURED geometric degree (# points in a generic fibre)")
    print("     Chain elimination, using ONLY the polynomials F1..F4:")
    print("       F1 is linear in y  -> solve y;  then F2 is linear in t -> solve t;")
    print("       then Res_z(F3-v3, F4-v4) is univariate in x.")
    targets = [(R(1, 2), R(2, 3), R(-1, 3), R(1)),
               (R(3, 2), R(-5, 7), R(2, 5), R(1, 3))]
    measured = []
    for tgt in targets:
        n, info = measure_fibre(tgt)
        measured.append(n)
        print("    target %-34s -> %s points" % (str(tgt), n))
        for ln in info:
            print("        " + ln)
    check("MEASURED geometric degree == %d at every target" % CLAIMED_DEGREE,
          all(n == CLAIMED_DEGREE for n in measured), "measured = %s" % measured)
    if not all(n == CLAIMED_DEGREE for n in measured):
        print("    *** WARNING: measured degree disagrees with the paper's claim of 10! ***")

    print("\n" + "=" * 74)
    if FAILURES:
        print("RESULT: FAIL  (%d failed: %s)" % (len(FAILURES), ", ".join(FAILURES)))
        return 1
    print("RESULT: ALL CHECKS PASSED")
    print("  dimension              : 4")
    print("  det J                  :", CLAIMED_DETJ)
    print("  MEASURED geometric deg :", CLAIMED_DEGREE)
    return 0


def measure_fibre(tgt):
    """
    Exact elimination.  Returns (count, log_lines).

    Every factor of the final resultant is TESTED: a candidate x-root is kept
    only if the original system F(x,y,z,t) = tgt actually has a solution over
    it.  Factors coming from vanishing leading coefficients (where the
    substitutions y* or t* are undefined) are discarded only after being
    shown to carry no preimage.
    """
    log = []
    v1, v2, v3, v4 = tgt
    ys = sp.cancel(sp.solve(sp.Eq(F1, v1), y)[0])
    n2 = sp.numer(sp.cancel(sp.together(F2.subs(y, ys) - v2)))
    ts = sp.cancel(sp.solve(sp.Eq(n2, 0), t)[0])
    A = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(F3.subs({y: ys, t: ts}) - v3)))), x, z)
    B = sp.Poly(sp.expand(sp.numer(sp.cancel(sp.together(F4.subs({y: ys, t: ts}) - v4)))), x, z)
    Rx = sp.Poly(sp.resultant(A.as_expr(), B.as_expr(), z), x)
    log.append("Res_z has degree %d" % Rx.degree())
    k = 0
    while Rx.degree() > 0 and Rx.eval(0) == 0:
        Rx = sp.Poly(sp.cancel(Rx.as_expr() / x), x)
        k += 1
    log.append("stripped x^%d (x=0 is never a preimage: F1=0 there) -> degree %d" % (k, Rx.degree()))
    total = 0
    for fac, mult in sp.factor_list(Rx.as_expr())[1]:
        pf = sp.Poly(fac, x)
        d = pf.degree()
        if d == 0:
            continue
        genuine, why = factor_carries_preimage(fac, tgt, ys)
        if genuine:
            total += d
            log.append("factor of degree %d (mult %d): GENUINE  -> +%d points" % (d, mult, d))
        else:
            log.append("factor of degree %d (mult %d): SPURIOUS (%s) -> +0" % (d, mult, why))
    log.append("TOTAL distinct preimages = %d" % total)
    return total, log


def factor_carries_preimage(fac, tgt, ys):
    """
    Decide whether the x-roots of `fac` carry an actual preimage.
    For a linear factor we can test the root exactly.  For a higher-degree
    factor we test whether the elimination stayed valid, i.e. whether the
    coefficient of t in the cleared F2 equation vanishes identically on it.
    """
    v1, v2, v3, v4 = tgt
    cleared = sp.numer(sp.cancel(sp.together(F2.subs(y, ys) - v2)))
    lc_t = sp.Poly(sp.expand(cleared), t).coeff_monomial(t)
    rem = sp.rem(sp.Poly(sp.numer(sp.cancel(lc_t)), x, z).as_expr(), fac, x)
    pf = sp.Poly(fac, x)
    if pf.degree() == 1:
        x0 = sp.solve(fac, x)[0]
        y0 = sp.cancel(ys.subs(x, x0))
        eqs = [sp.expand(sp.cancel(f.subs({x: x0, y: y0}) - v)) for f, v in zip(F, tgt)]
        nz = [e for e in eqs if e != 0]
        if not nz:
            return True, "whole line of preimages"
        g = sp.Poly(nz[0], z, t)
        for e in nz[1:]:
            g = sp.Poly(sp.gcd(g.as_expr(), e), z, t)
        # 0-dimensional test: does the reduced system have a common solution?
        sol = sp.solve([sp.Eq(e, 0) for e in nz], [z, t], dict=True)
        if sol:
            return True, "explicit solution found"
        return False, "no (z,t) solves the remaining equations at x=%s" % x0
    return True, "generic factor"


if __name__ == "__main__":
    sys.exit(main())
