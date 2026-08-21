#!/usr/bin/env python3
"""C3 layer 1 — the sqrt-reduction / divisibility ladder, formalized.

Directive Step 2: "Before writing trackC_c3_ladder.py, formally convert the
prose from Sessions 10-13 into verified, symbolic polynomial relations over Q."

Provenance of the inputs, stated up front because it decides what may be
leaned on:

  Session 10  EXECUTABLE and Track-F-certified (it reruns with zero
              divergences). Its content: the framework's 13-curve chain is
              EQUIVALENT to the thirteen block vanishings W_n = 0,
              n = -18..-6, where W = y1^2 - y2^3.
  Session 11  PROSE. Its "executable engine ... in the transcript" is LOST.
  Sessions 12-14  PROSE. Their "inline runs" are LOST. THEOREM 1
              (sqrt-reduction), THEOREM 2 (total rigidity), THEOREM 3
              (pole-fiber) are asserted there with no surviving certificate.

So Sessions 11-14 are re-derived here, not imported. Nothing below cites them
as authority; where a claim of theirs is reproduced, it is reproduced as an
independently checked identity, and where it is not reproduced that is said
plainly.

What this module certifies, all exact over Q, generic symbols (no near-miss
numerics needed — the identities are universal):

  L1  The formal (b/a)-th root exists and is unique with S_0 = 1:
      given T = sum_{m>=1} T_m x^m over any Q-algebra, there is a unique
      S = sum_{m>=0} S_m x^m with S_0 = 1 and S^a = (1+T)^b. The S_m are
      universal polynomials in T_1..T_m over Q. For (a,b) = (2,3) this is
      Sessions 12-14's (sum S_m x^m)^2 = (1+T)^3.
  L2  Chain <=> square-root agreement. With
          y2 = X^(-ka) g^a (1 + T),  y1 = X^(-kb) g^b (S + Delta),
      W := y1^2 - y2^3 vanishes through the chain range exactly when
      Delta = O(x^D). (Stated and checked for (a,b) = (2,3), which is the
      case where W = y1^2 - y2^3 is the relevant cusp function.)
  L3  Endgame collapse. With Delta = delta x^D + O(x^(D+1)), the first
      surviving W-block is  2 g^3 (delta - g^3 S_D)  in the Sessions 12-14
      normalization — i.e. the deviation enters LINEARLY, which is what makes
      the endgame functional an ODE in R rather than a quadratic condition.
  L4  Ladder operator. The divisibility ladder is exactly: g^b * S_m is
      polynomial for m = 0..D-1, where T_m carries the B-tower. This module
      provides the operator that decides it for given (g, B-tower); it does
      NOT decide it in general, which is the open part of C3.

NOT certified here, and NOT to be treated as available: THEOREM 2 (total
rigidity, g = alpha U (U-1)^8) and THEOREM 3 (pole-fiber => R polynomial).
Both are load-bearing for any (72,108) conclusion and both remain prose. C1's
pole-forcing result covers the *order* of the pole, not the pole-fiber
argument that makes R a polynomial.

Run:  python3 trackC_c3_ladder.py
"""
import json, os, sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
PASS = FAIL = 0


def report(name, ok, extra=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + extra) if extra else ""))
    return ok


# ------------------------------------------------------------------ L1 engine
def series_mul(A, B, N):
    """Truncated product of two coefficient lists, length N+1."""
    out = [sp.Integer(0)] * (N + 1)
    for i, a in enumerate(A[:N + 1]):
        if a == 0:
            continue
        for j, b in enumerate(B[:N + 1 - i]):
            if b:
                out[i + j] += a * b
    return [sp.expand(c) for c in out]


def series_pow(A, e, N):
    out = [sp.Integer(1)] + [sp.Integer(0)] * N
    for _ in range(e):
        out = series_mul(out, A, N)
    return out


def frac_root(T, a, b, N):
    """Unique S with S_0 = 1 and S^a = (1 + T)^b, to order N.

    T is a coefficient list with T[0] = 0. Recursion from matching
    coefficients of S^a: a*S_m = C_m - [x^m](S^a with S_m set to 0), which is
    linear in S_m because S_0 = 1.
    """
    assert T[0] == 0, "T must have no constant term"
    C = series_pow([sp.Integer(1)] + list(T[1:]), b, N)
    S = [sp.Integer(1)] + [sp.Integer(0)] * N
    for m in range(1, N + 1):
        cur = series_pow(S, a, m)          # S_m still 0 at this point
        S[m] = sp.expand((C[m] - cur[m]) / a)
    return S


def run_L1(N=8):
    print("\n== L1: existence/uniqueness of the formal (b/a)-th root ==")
    Ts = sp.symbols("T1:%d" % (N + 1))
    T = [sp.Integer(0)] + list(Ts)
    for (a, b) in ((2, 3), (2, 5), (3, 5), (4, 7)):
        S = frac_root(T, a, b, N)
        lhs = series_pow(S, a, N)
        rhs = series_pow([sp.Integer(1)] + list(T[1:]), b, N)
        ok = all(sp.simplify(lhs[m] - rhs[m]) == 0 for m in range(N + 1))
        report("S^%d == (1+T)^%d to order %d (generic T)" % (a, b, N), ok)
    # the (2,3) coefficients, printed so they can be eyeballed against
    # Sessions 12-14's S_m if that prose is ever recovered
    S23 = frac_root(T, 2, 3, 4)
    print("     (2,3): S_1 =", sp.simplify(S23[1]))
    print("     (2,3): S_2 =", sp.simplify(S23[2]))
    ok = sp.simplify(S23[1] - sp.Rational(3, 2) * Ts[0]) == 0
    report("S_1 = (3/2) T_1  (the condition-free first ladder level)", ok)
    return True


# ------------------------------------------------- L2/L3 chain and collapse
def run_L2_L3(N=6):
    """Chain <=> sqrt-agreement, and linearity of the first deviation block.

    Work in the (2,3) cusp case, where the cusp function is W = y1^2 - y2^3.
    Carry g and the T-tower as generic symbols; the prefactors X^(-ka),
    X^(-kb) are pure bookkeeping (they multiply every block by the same
    power), so they are set to 1 and their exponents tracked in the comments
    rather than in the algebra.
    """
    print("\n== L2/L3: chain <=> sqrt-agreement; deviation enters linearly ==")
    g = sp.Symbol("g")
    Ts = sp.symbols("T1:%d" % (N + 1))
    T = [sp.Integer(0)] + list(Ts)
    S = frac_root(T, 2, 3, N)

    # y2 = g^2 (1 + T);  y1 = g^3 (S + Delta)
    y2 = [sp.expand(g**2 * c) for c in ([sp.Integer(1)] + list(T[1:]))]
    for D in range(1, N + 1):
        dl = sp.Symbol("delta")
        Delta = [sp.Integer(0)] * (N + 1)
        if D <= N:
            Delta[D] = dl
        y1 = [sp.expand(g**3 * (S[m] + Delta[m])) for m in range(N + 1)]
        W = [sp.expand(a - b) for a, b in
             zip(series_mul(y1, y1, N), series_pow(y2, 3, N))]
        # blocks strictly below the deviation order must vanish identically
        ok_low = all(sp.simplify(W[m]) == 0 for m in range(D))
        first = sp.simplify(W[D]) if D <= N else None
        # and the first nonvanishing block must be linear in delta with
        # coefficient 2 g^3 * (leading sqrt factor) = 2 g^6
        ok_lin = (sp.degree(sp.Poly(first, dl), dl) == 1 and
                  sp.simplify(sp.diff(first, dl) - 2 * g**6) == 0)
        report("D = %d: blocks 0..%d vanish; first block linear in delta "
               "with coefficient 2g^6" % (D, D - 1), ok_low and ok_lin)
    print("     => chain of length D  <=>  y1 = g^3 * (2,3)-root of y2 "
          "through order D-1;")
    print("        the first deviation block is 2 g^6 * delta — LINEAR, which")
    print("        is what makes the endgame an ODE in R and not a quadratic.")
    return True


# ------------------------------------------------------------ L4 ladder op
def ladder_obstructions(gpoly, Bt, a, b, D, var):
    """Decide the divisibility ladder for a concrete tower.

    gpoly : sympy expression in `var` (the boundary polynomial g)
    Bt    : list of sympy expressions, Bt[m] is the tower entry at level m
            (m = 1..D-1); T_m := Bt[m] / gpoly**a
    Returns list of (m, remainder) for the levels where gpoly**b * S_m FAILS
    to be polynomial. An empty list means the ladder is satisfied.
    """
    T = [sp.Integer(0)] + [sp.together(Bt[m] / gpoly**a) for m in
                           range(1, D)]
    S = frac_root(T, a, b, D - 1)
    bad = []
    for m in range(1, D):
        expr = sp.cancel(sp.together(gpoly**b * S[m]))
        num, den = sp.fraction(expr)
        if sp.simplify(den - 1) == 0:
            continue
        q, r = sp.div(sp.Poly(num, var), sp.Poly(den, var))
        if not r.is_zero:
            bad.append((m, sp.simplify(r.as_expr())))
    return bad


def run_L4():
    """Exercise the ladder operator on two synthetic towers: one built to
    satisfy the ladder by construction, one perturbed to break it."""
    print("\n== L4: the divisibility ladder operator ==")
    U = sp.Symbol("U")
    g = U * (U - 1)**2
    D = 5
    # tower built so that every T_m is g^2 times a polynomial: ladder holds
    good = [None] + [g**2 * (U**m + 1) for m in range(1, D)]
    bad0 = ladder_obstructions(g, good, 2, 3, D, U)
    report("ladder satisfied on a by-construction-polynomial tower",
           bad0 == [], "obstructions: %s" % ([m for m, _ in bad0]))
    # perturb one level by a genuine pole: ladder must break at that level
    pert = list(good)
    pert[2] = pert[2] + 1        # no longer divisible by g^2
    bad1 = ladder_obstructions(g, pert, 2, 3, D, U)
    report("ladder breaks when one level is perturbed off the divisibility",
           bad1 != [], "first failing level: %s" %
           (bad1[0][0] if bad1 else None))
    print("     NOTE the operator decides the ladder for a GIVEN (g, tower).")
    print("     Deciding it over the whole parameter family is the open half")
    print("     of C3 and is not attempted here.")
    return True


def main():
    print("== C3 layer 1: sqrt-reduction / divisibility ladder, formalized ==")
    print("   Sessions 11-14 are re-derived, not imported: their executable")
    print("   engines were lost with the transcripts. Session 10 (the chain")
    print("   <=> block-vanishing equivalence) is Track-F-certified and is")
    print("   the only inherited input.\n")
    run_L1()
    run_L2_L3()
    run_L4()
    print("\n== NOT certified here (still prose, still load-bearing) ==")
    print("   THEOREM 2 total rigidity  g = alpha U (U-1)^8  — the Taylor-pin")
    print("     argument at general parameters is not reproduced.")
    print("   THEOREM 3 pole-fiber => R is a polynomial — C1 forces the pole")
    print("     ORDER; the fiber-counting step that makes R polynomial is not")
    print("     reproduced. Every (72,108) statement that assumes a polynomial")
    print("     R inherits this gap.")
    out = os.path.join(HERE, "trackC_c3_ladder.json")
    with open(out, "w") as fh:
        json.dump({"certified": ["L1 formal (b/a)-root existence/uniqueness",
                                 "L2 chain <=> sqrt agreement (2,3)",
                                 "L3 first deviation block linear, coeff 2g^6",
                                 "L4 ladder operator (per-tower decision)"],
                   "not_certified": ["THEOREM 2 total rigidity",
                                     "THEOREM 3 pole-fiber polynomiality"],
                   "pass": PASS, "fail": FAIL}, fh, indent=1)
    print("\n  artifact: trackC_c3_ladder.json")
    print("\nTOTAL: %d PASS, %d FAIL" % (PASS, FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
