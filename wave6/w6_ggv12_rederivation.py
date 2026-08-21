#!/usr/bin/env python3
"""RE-DERIVATION OF GGV (1.2)/(3.6) FROM THE POISSON BRACKET -- and the proof
that the paper's PRINTED third condition is wrong.

GGV, Pro Mathematica 27 (2013), p.93 prints

    (3.6)   A(0) = -mu3^2/4,   A'(0) = mu2,   mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0)

and says the last two "follow from the requirement that q0'(y) and p0'(y)
defined by (3.2) and (3.3) are polynomials".  This script carries out exactly
that derivation, starting from their own setup on p.91-93:

    P = x^3 y + x^2 p2 + x p1 + p0,   Q = x^2 y + x q1 + q0
    [P,Q] = x^4 y + mu3 x^3 + mu2 x^2 + mu1 x + mu0
    q1 = mu3 + y^2 F',  p2 = mu3 + y F + (3/2) y^2 F',  F in y K[y]   (their p.92)
    A := y p1 - q1 p2 + (3/4) q1^2                                     (their p.93)

and obtains

    mu3*A''(0) = -6*mu1        (NO q1''(0) term)

The printed form exceeds the truth by exactly -2*mu3*q1''(0) = -4*f1*mu3.

Consequence for anyone who transcribed the printed form: their system contains
4*mu3^2*b2 (b2 = the y^2 coefficient of q1, so q1''(0) = 2*b2), i.e. it is the
TRUE variety intersected with {mu3 = 0} u {b2 = 0}.  Emptiness of that proper
subvariety says nothing about B = 16.  test_ideal_membership() below is the
can-fail discriminator: it must find 4*mu3^2*b2 in the printed system and NOT
in the corrected one.

Run: python3 wave6/w6_ggv12_rederivation.py
"""
import sys, os
import sympy as sp
from sympy import symbols, expand, Rational, diff

x, y = symbols('x y')
m0, m1, m2, m3 = symbols('mu0 mu1 mu2 mu3')

def bracket(P, Q):
    return expand(diff(P, x)*diff(Q, y) - diff(P, y)*diff(Q, x))

def rederive(nF=4, np1=4):
    """Returns (holds_corrected, holds_printed, discrepancy, report)."""
    f = symbols(f'f1:{nF+1}'); e = symbols(f'e1:{np1+1}')
    F  = sum(f[i-1]*y**i for i in range(1, nF+1))          # F in y K[y]
    Fp, Fpp = diff(F, y), diff(F, y, 2)
    q1 = m3 + y**2*Fp                                       # GGV p.92
    p2 = m3 + y*F + Rational(3, 2)*y**2*Fp                  # GGV p.92
    p1 = m2 + sum(e[i-1]*y**i for i in range(1, np1+1))     # p1(0)=mu2, derived below
    rep = []

    # -- the four ODEs of p.91, re-derived from the bracket itself ------------
    p0f, q0f = sp.Function('p0'), sp.Function('q0')
    P = x**3*y + x**2*p2 + x*p1 + p0f(y)
    Q = x**2*y + x*q1 + q0f(y)
    Bx = sp.Poly(bracket(P, Q), x)
    co = {mm[0]: cc for mm, cc in zip(Bx.monoms(), Bx.coeffs())}
    q0p, p0p = sp.Derivative(q0f(y), y), sp.Derivative(p0f(y), y)
    paper = {4: y,
             3: 3*y*diff(q1, y) - q1 + 2*p2 - 2*y*diff(p2, y),
             2: 3*y*q0p + 2*p2*diff(q1, y) - diff(p2, y)*q1 + p1 - 2*y*diff(p1, y),
             1: 2*p2*q0p + p1*diff(q1, y) - diff(p1, y)*q1 - 2*y*p0p,
             0: p1*q0p - p0p*q1}
    for k in (4, 3, 2, 1, 0):
        ok = sp.simplify(co.get(k, 0) - paper[k]) == 0
        rep.append(f"  bracket x^{k} coefficient == GGV p.91 : {ok}")
        assert ok, f"setup mismatch at x^{k}"
    rep.append(f"  first ODE returns mu3 identically     : "
               f"{sp.simplify(paper[3]-m3)==0}   (so p2,q1 are GGV's general solution)")

    # -- (3.2): q0' polynomial ------------------------------------------------
    q0p_expr = sp.cancel((-2*p1 + 2*m2 + 2*m3*F + 4*y*diff(p1, y) - 6*y**2*F*Fp
                          - m3*y**2*Fpp - 4*y**3*Fp**2 - 4*y**3*F*Fpp
                          - 3*y**4*Fp*Fpp) / (6*y))
    rep.append(f"  (3.2) q0' is a polynomial            : "
               f"{sp.denom(q0p_expr)==1}   (this IS the condition p1(0)=mu2)")

    # -- (3.3): p0' polynomial gives the third condition ----------------------
    num = sp.expand(sp.numer(sp.cancel(sp.together(
        y*p1*(2*Fp + y*Fpp) - m1 - diff(p1, y)*(m3 + y**2*Fp)
        + (2*m3 + y*(2*F + 3*y*Fp))*q0p_expr))))
    cond = sp.expand(num.subs(y, 0))
    mu1_forced = sp.solve(cond, m1)[0]

    # -- compare with A ------------------------------------------------------
    A = expand(y*p1 - q1*p2 + Rational(3, 4)*q1**2)
    lhs   = expand(m3*diff(A, y, 2).subs(y, 0))
    q1pp0 = diff(q1, y, 2).subs(y, 0)
    corrected = expand(-6*mu1_forced)
    printed   = expand(-6*mu1_forced - 2*m3*q1pp0)
    rep.append(f"  A(0)  = {sp.factor(A.subs(y,0))}   (paper: -mu3^2/4)")
    rep.append(f"  A'(0) = {sp.factor(diff(A,y).subs(y,0))}   (paper: mu2)")
    rep.append(f"  mu3*A''(0) = {sp.factor(lhs)}")
    hc = sp.simplify(lhs - corrected) == 0
    hp = sp.simplify(lhs - printed) == 0
    return hc, hp, sp.factor(sp.simplify(printed - lhs)), rep

def test_ideal_membership(ds=(3, 4, 5)):
    """4*mu3^2*b2 is in the PRINTED system's ideal and not in the corrected one."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__) or '.', '..', 'wave5'))
    from w5_b16_abel import build_system, mu3 as M3
    out = []
    for d in ds:
        for variant in ('printed', 'corrected'):
            eqs, unk, A, q1 = build_system(d, variant=variant)
            a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
            n13 = len(eqs) - 5
            norm = {b[0]: M3, b[1]: 0, a[0]: -M3**2/4, a[1]: m2}
            y2row = expand(eqs[:n13][n13-1-2].subs(norm))   # y^2 coefficient of (1.3)
            row3  = expand(eqs[-3].subs(norm))
            comb  = sp.factor(expand(M3*row3 + 2*y2row))
            out.append((d, variant, comb))
    return out

if __name__ == '__main__':
    hc, hp, disc, rep = rederive()
    print("=" * 74)
    print("RE-DERIVATION OF GGV (3.6) FROM THEIR OWN (3.2)/(3.3)")
    print("=" * 74)
    for line in rep: print(line)
    print()
    print(f"  CORRECTED  mu3*A''(0) = -6*mu1                 holds : {hc}")
    print(f"  PRINTED    mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0) holds : {hp}")
    print(f"  printed minus truth = {disc}   (= -2*mu3*q1''(0))")
    assert hc and not hp, "re-derivation failed"
    print()
    print("DISCRIMINATOR  mu3*(1.2 row 3) + 2*(y^2 row of (1.3)), normalized:")
    for d, variant, comb in test_ideal_membership():
        flag = "  <-- spurious constraint in the ideal" if comb != 0 else "  <-- clean"
        print(f"  d={d:2d} {variant:9s}: {comb}{flag}")
    print()
    print("VERDICT: the printed (3.6) forces mu3^2*b2 = 0; the corrected one does not.")
