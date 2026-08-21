#!/usr/bin/env python3
"""WAVE 5 -- the B=16 door: GGV's equation (1.3)+(1.2), Pro Mathematica 27 (2013).

THE SOURCE (papers/GGV_ProMathematica27_2013.pdf, transcribed from 150dpi page
renders ggv_p3-03.png and ggv_p-11.png, not from pdftotext; (1.3) on p.85 and
(3.5) on p.93 are character-identical, so one transcription covers both):

  THEOREM 1.2 (GGV 2013).  B = 16 if and only if there exist A, q1 in K[y]
  and mu0..mu3 in K with mu0 != 0 such that

    (1.2)  A(0) = -mu3^2/4,   A'(0) = mu2,   mu3*A''(0) = -6*mu1

  *** CORRECTED 2026-08-21.  The paper PRINTS the third condition as
      mu3*A''(0) = -6*mu1 - 2*mu3*q1''(0)  ((3.6), p.93), and this file
      transcribed it faithfully.  That printed form is WRONG: re-deriving it
      from GGV's own (3.2)/(3.3) polynomiality requirements gives no
      q1''(0) term.  The spurious term made the system a PROPER SUBVARIETY
      ({mu3=0} u {q1''(0)=0}) of the real one -- see the CATCHES.md entry
      "GGV (1.2) ROW 3 IS MIS-PRINTED".  build_system(d, variant='printed')
      reproduces the old, wrong system for comparison. ***

    (1.3)  6*( A - q1^2/4 + (mu3/4)*q1 - (mu2/6)*y )^2
             = 4*y*A*A' + 6*( (mu3/4)*q1 - (mu2/6)*y )^2
               - mu2*y*q1^2 + 3*mu1*y^2*q1 - 6*mu0*y^3

  and a solution with mu0 != 0 "would yield a counterexample to the JC"
  (their words, p.85); B > 16 iff no such solution exists.  deg A = 2 deg q1
  (their Section 3.5); q1 is taken monic (their Section 3.5).

STATE OF THE DOOR IN THE LITERATURE:
  - GGV 2013 solved deg(q1) = 2, 3, 4 only (all solutions have mu0 = 0) and
    STALLED at deg(q1) = 5 ("after an hour the PC hadn't solved").
  - GGV's refereed J.Algebra 2017 paper (arXiv:1401.1784, p.2) states
    Heitmann's claimed B > 16 rests on a gapped lemma ([15, Lemma 4.10]), so
    "B >= 16 remains up to the moment the best lower limit" and "the possible
    counterexample at B = 16 is still within reach".
  - GGHV 2022 (arXiv:2204.14178) cites [4, section 3.5] for its 64- and
    112-degree rows, i.e. exactly the solved cells deg(q1) <= 3.  The cells
    deg(q1) >= 5 correspond to degree pairs above the 125 window and have
    never been decided by anyone.

TRANSCRIPTION FINDING (recorded, affects nothing downstream): the Section 3.1
example is printed with mu0 = 1; substituting it into (3.5) leaves the residual
-6*y^3 + 6*mu0*y^3, which vanishes iff mu0 = 2.  The example satisfies (1.3)
with mu0 = 2 and fails (1.2) exactly as the paper says.  A typo in their prose,
pinned by the uniqueness of the fixing value.

WHAT THIS FILE DOES: builds the exact coefficient system for given d = deg(q1)
and certifies the transcription against the paper's own data.  Solving is done
by msolve via w5_b16_export.py / w5_b16_run.py -- any solution found there is
raw witness data only; the HIT protocol adjudicates, never this file.
"""
import sys
from sympy import symbols, Symbol, expand, Poly, Rational, diff

y = Symbol('y')
mu0, mu1, mu2, mu3 = symbols('mu0 mu1 mu2 mu3')

FAIL = []
def check(label, cond, note=""):
    print(("PASS " if cond else "FAIL ") + label + ("   [" + note + "]" if note else ""))
    if not cond:
        FAIL.append(label)

def build_system(d, variant='corrected'):
    """Coefficient system of (1.3)+(1.2) for q1 monic of degree d, deg A = 2d.
    Returns (equations, unknowns, A, q1); the last 3 equations are (1.2).

    variant='corrected' (default) uses the RE-DERIVED (1.2) row 3,
        mu3*A''(0) + 6*mu1 = 0.
    variant='printed' uses GGV's printed (3.6), which carries a spurious
        +2*mu3*q1''(0); kept only to reproduce the campaign's pre-2026-08-21
        results.  Do not use it for verdicts."""
    assert variant in ('corrected', 'printed')
    a = symbols(f'a0:{2*d+1}')          # A = sum a_i y^i
    b = symbols(f'b0:{d}')              # q1 = y^d + sum_{i<d} b_i y^i
    A  = sum(a[i]*y**i for i in range(2*d+1))
    q1 = y**d + sum(b[i]*y**i for i in range(d))
    S  = A - q1**2/4 + (mu3/4)*q1 - (mu2/6)*y
    T  = (mu3/4)*q1 - (mu2/6)*y
    E  = expand(6*S**2 - (4*y*A*diff(A, y) + 6*T**2
                          - mu2*y*q1**2 + 3*mu1*y**2*q1 - 6*mu0*y**3))
    eqs = Poly(E, y).all_coeffs()       # identity in y
    Ap  = diff(A, y); App = diff(Ap, y); q1pp = diff(q1, y, 2)
    eqs += [expand(A.subs(y, 0) + mu3**2/4),
            expand(Ap.subs(y, 0) - mu2),
            expand(mu3*App.subs(y, 0) + 6*mu1
                   + (2*mu3*q1pp.subs(y, 0) if variant == 'printed' else 0))]
    # GGV p.92 WLOG normalizations, used by their own Sec 3.5 computations
    # ("we can and will assume q1(0) = mu3, q1'(0) = 0"): without these the
    # system carries gauge freedom (observed: d=2 mod-p points that are pure
    # gauge copies).  They remove copies, never solutions.
    eqs += [expand(b[0] - mu3), b[1]]
    unknowns = list(a) + list(b) + [mu0, mu1, mu2, mu3]
    return [expand(e) for e in eqs], unknowns, A, q1

def subs_check(eqs, sol):
    vals = [expand(e.subs(sol)) for e in eqs]
    return all(v == 0 for v in vals), vals

def main():
    print("="*78)
    print("W5 -- the B=16 Abel door: transcription certification of GGV (1.2)+(1.3)")
    print("="*78)
    eqs3, unk3, A3, q13 = build_system(3)
    a3 = symbols('a0:7'); b3 = symbols('b0:3')

    # positive control: the paper's published d=3 solution (Section 3.5):
    sol_pub = {a3[0]: -mu3**2/4, a3[1]: 0, a3[2]: 0, a3[3]: -mu3/2,
               a3[4]: 0, a3[5]: 0, a3[6]: Rational(-1, 4),
               b3[0]: mu3, b3[1]: 0, b3[2]: 0,
               mu0: 0, mu1: 0, mu2: 0}
    ok, _ = subs_check(eqs3, sol_pub)
    check("d=3 positive control: published solution satisfies ALL equations", ok,
          "GGV Sec 3.5, symbolic mu3")

    # Section 3.1 example: satisfies (1.3) with mu0 = 2 (typo: paper prints 1),
    # and fails (1.2) exactly as the paper says.
    base = {a3[0]: 1, a3[1]: 0, a3[2]: 0, a3[3]: -1, a3[4]: 0, a3[5]: 0,
            a3[6]: Rational(-1, 4), b3[0]: 2, b3[1]: 0, b3[2]: 0,
            mu1: 0, mu2: 0, mu3: 2}
    s1 = dict(base); s1[mu0] = 1
    s2 = dict(base); s2[mu0] = 2
    E13 = eqs3[:-5]  # (1.3) rows; then 3x(1.2); then 2 normalization rows
    ok1, _ = subs_check(E13, s1)
    ok2, _ = subs_check(E13, s2)
    ok2b, vals12 = subs_check(eqs3[-5:-2], s2)
    check("Sec 3.1 example fails (1.3) at the printed mu0=1", not ok1)
    check("Sec 3.1 example satisfies (1.3) at mu0=2 (typo pinned)", ok2)
    check("Sec 3.1 example fails (1.2), as the paper says", not ok2b,
          f"(1.2) residuals: {vals12}")

    # negative control: perturbing the published solution breaks the system
    sol_bad = dict(sol_pub); sol_bad[a3[3]] = -mu3/2 + 1
    okbad, _ = subs_check(eqs3, sol_bad)
    check("negative control: perturbed solution violates the system", not okbad)

    print(("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL)))
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
