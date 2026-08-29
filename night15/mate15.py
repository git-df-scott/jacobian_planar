"""night15 -- exact mate solve for the survivors of the period screen.

The Keller equation P_x Q_y - P_y Q_x = 1 is LINEAR in the coefficients of Q,
so for a fixed carrier S (a finite monomial set for Q) it is a linear system
over Q.  night12's kernel is imported read-only for the linear algebra:
matekit.build_system / consistency_mod_p and exact.decide, which emits either

  * MATE_over_Q          -- an exact Q, verified by expanding [P,Q] - 1 = 0
                            coefficientwise over Q, or
  * EMPTY_over_Q         -- with a lambda certificate (lambda^T A = 0,
                            lambda^T e = 1) re-verified exactly over Q, or
  * NOT_CERTIFIED        -- prime-relative only; never reported as emptiness.

Carrier: ALL monomials of total degree <= D, with D escalating
    D = deg P, ceil(3 deg P / 2), 2 deg P
(the brief's floor is 2 deg P).  The null directions Q -> Q + h(P) live inside
the carrier whenever D >= deg P; they only enlarge the solution space, so they
cannot turn a consistent system inconsistent, and the exact solver reports the
kernel dimension it deflated.
"""

import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "night12"))
import matekit as M          # noqa: E402  (night12, read-only)
import exact as EX           # noqa: E402  (night12, read-only)

import pk15 as P14           # noqa: E402


def carrier(D):
    return sorted((i, j) for i in range(D + 1) for j in range(D + 1 - i))


def solve(P, max_cols=2600, verbose=True):
    d = P14.tdeg(P)
    Pi = {k: int(v) if F(v).denominator == 1 else F(v) for k, v in P.items()}
    den = 1
    from math import gcd
    for v in P.values():
        den = den * F(v).denominator // gcd(den, F(v).denominator)
    Pi = {k: int(F(v) * den) for k, v in P.items()}      # scaling Q by 1/den
    stages = []
    for D in (d, (3 * d + 1) // 2, 2 * d):
        S = carrier(D)
        if len(S) > max_cols:
            stages.append({"deg_Q_bound": D, "n_unknowns": len(S),
                           "verdict": "SKIPPED_too_large"})
            continue
        t = time.time()
        out, rows, Qd = EX.decide(Pi, S)
        out["deg_Q_bound"] = D
        out["secs"] = round(time.time() - t, 1)
        out["scale_den"] = den
        stages.append(out)
        if verbose:
            print("    D=%-4d n=%-5d %-16s %s (%.1fs)"
                  % (D, len(S), out["verdict"], out.get("certificate"), out["secs"]))
            sys.stdout.flush()
        if out["verdict"] == "MATE_over_Q":
            # undo the integerising scale: [P, Q] = 1 with P = den * P_orig
            Q = {k: F(v) * den for k, v in Qd.items()}
            br = P14.psub(P14.padd(P14.pmul(P14.dx(P), P14.dy(Q)),
                                   P14.pscal(-1, P14.pmul(P14.dy(P), P14.dx(Q)))),
                          {(0, 0): F(1)})
            return {"verdict": "MATE_over_Q", "stages": stages,
                    "Q": {"%d,%d" % k: [F(v).numerator, F(v).denominator]
                          for k, v in Q.items()},
                    "bracket_minus_one_terms": len(br)}
    verd = "EMPTY_all_stages" if all(
        s.get("verdict") == "EMPTY_over_Q" for s in stages if "verdict" in s
        and s["verdict"] != "SKIPPED_too_large") else "NOT_CERTIFIED"
    return {"verdict": verd, "stages": stages}
