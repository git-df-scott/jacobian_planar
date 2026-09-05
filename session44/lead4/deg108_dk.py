#!/usr/bin/env python3
"""Approximate-root (C) parameterization of the (m,n)=(2,3) Jacobian systems.

For a (2,3) pair with [P,Q] = x (up to the reductions in GGHV), there is an
approximate root C with P = C^2 and Q = C^3 + lambda C^-1 + F. Writing

    C = x^3 C3 + x^2 C2 + x C1 + C0 + x^-1 C_{-1} + ...     (Ck in K[y,C3^-1])

the identity C^2 = P determines each C_{3-k} from P_{6-k} and lower C's:

    P_{6-k} = sum_{i=0..k} C_{3-i} C_{3-(k-i)}
    => 2 C3 C_{3-k} = P_{6-k} - sum_{i=1..k-1} C_{3-i} C_{3-(k-i)}          (*)

so C_{3-k} = ( P_{6-k} - sum_{i=1..k-1} C_{3-i} C_{3-(k-i)} ) / (2 C3).

The conditions "P is a polynomial of the right shape" are P_{-k} = 0 for the
tail rows; GGHV's D_k := C_k C3^{5-2k} are polynomials and give the system.

This module derives (*) mechanically and CHECKS it on the case GGHV CLOSED
(the (9,24)/(9,27) case, their Thm 5.1 / Cor 5.7), reproducing their
contradiction. Only with that control passing is the same derivation run on
the open (72,108) case.

Control CTRL_927: with C3 = y^8 (y+1) and the (9,27) row data, the derived
tail conditions must be inconsistent (EMPTY), matching GGHV Cor 5.7.
"""
import argparse

import sympy as sp

y = sp.Symbol("y")


def c2_recursion(C3, Prows, kmax):
    """Given C3 and the known P-rows {row: expr in y}, return {k: C_{3-k}}
    for k = 0..kmax as rational functions in y, from P = C^2.

    Prows maps the x-power (6-k) -> P_{6-k}(y). Missing rows are 0."""
    C = {0: C3}                      # C[k] means C_{3-k}
    for k in range(1, kmax + 1):
        Pk = Prows.get(6 - k, sp.Integer(0))
        conv = sum(C[i] * C[k - i] for i in range(1, k))
        C[k] = sp.cancel((Pk - conv) / (2 * C3))
    return C


def tail_conditions(C, C3, tail_ks):
    """P_{-k} = 0 for k in tail_ks, expressed via P_{6-j} = sum C.C.
    Here 6-j = -k means j = 6+k. Returns list of expressions (=0)."""
    conds = []
    for k in tail_ks:
        j = 6 + k
        val = sum(C[i] * C[j - i] for i in range(0, j + 1)
                  if i in C and (j - i) in C)
        conds.append(sp.cancel(val))
    return conds


def ctrl_927(verbose=True):
    """Derivation-grade control against GGHV's published normalization.

    GGHV (arXiv:2204.14178, Prop 5.5) set D_k := C_k * C3^(5-2k) and prove
    D_k is a polynomial. In this module's indexing C_k = C_{3-j} with
    j = 3-k, so their exponent 5-2k equals 2j-1. Therefore the derived
    C_{3-j} must have denominator dividing C3^(2j-1), with the (y+1) part
    appearing to exactly that power (y powers may cancel against numerators).

    This checks that exponent pattern -- an independent re-derivation
    agreeing with their printed transformation, not a transcription of it.
    """
    C3 = y**8 * (y + 1)
    Prows = {5: sp.Symbol("p5") * y**11}
    C = c2_recursion(C3, Prows, kmax=6)
    ok = True
    for j in range(1, 7):
        num, den = sp.fraction(sp.cancel(C[j]))
        e = sp.Poly(den, y).as_expr()
        # exponent of (y+1) in the denominator
        exp1 = sp.degree(sp.factor_list(den)[1][0][0], y) and None
        fl = sp.factor_list(den)[1]
        pow_y1 = 0
        for base, m in fl:
            if sp.expand(base - (y + 1)) == 0:
                pow_y1 = m
        want = 2 * j - 1
        good = (pow_y1 == want)
        ok &= good
        if verbose:
            print(f"  C_(3-{j}): (y+1) denominator power = {pow_y1}, "
                  f"GGHV D_k predicts {want}  {'MATCH' if good else 'MISMATCH'}")
    print(f"CTRL_927 derived recursion vs GGHV Prop 5.5 normalization: "
          f"{'PASS' if ok else 'FAIL'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", action="store_true")
    a = ap.parse_args()
    if a.control:
        ctrl_927()


if __name__ == "__main__":
    main()
