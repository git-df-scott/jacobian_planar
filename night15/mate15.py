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


# --------------------------------------------------------- exact lambda
# night12's decider emits a lambda certificate only when rank_p(A) = n.  With
# the FULL triangular carrier the null directions Q -> Q + h(P) sit inside the
# carrier, so rank_p(A) < n always and that branch never fires.  The certificate
# itself does not need full rank: A q = e is unsolvable over Q iff there is a
# rational lambda with lambda^T A = 0 on every column and lambda^T e = 1
# (Fredholm).  Below, a candidate lambda is FOUND mod p -- cheap, and only a
# heuristic for locating a small support -- and then SOLVED and VERIFIED
# exactly over Q on that support.  Only the exact verification is a certificate.

def _lambda_mod_p(rows, ncols, p=M.P1):
    """row-combination over F_p giving 0 = 1; returns the list of row keys."""
    import numpy as np
    keys = sorted(set(rows) | {(0, 0)})
    m = len(keys)
    A = np.zeros((m, ncols + 1), dtype=np.int64)
    for t, k in enumerate(keys):
        for j, v in rows.get(k, {}).items():
            A[t, j] = v % p
        if k == (0, 0):
            A[t, ncols] = 1
    C = np.zeros((m, m), dtype=np.int64)          # the row combination so far
    C[np.arange(m), np.arange(m)] = 1
    r = 0
    for c in range(ncols):
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0:
            continue
        piv = r + int(nz[0])
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
            C[[r, piv]] = C[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        C[r] = (C[r] * inv) % p
        f = A[:, c].copy()
        f[r] = 0
        mask = f != 0
        if mask.any():
            A[mask] = (A[mask] - f[mask, None] * A[r][None, :]) % p
            C[mask] = (C[mask] - f[mask, None] * C[r][None, :]) % p
        r += 1
        if r >= m:
            break
    for i in range(m):
        if A[i, ncols] % p != 0 and not A[i, :ncols].any():
            return [keys[t] for t in range(m) if C[i, t] % p != 0]
    return None


def _lambda_exact_on(rows, ncols, support):
    """solve for lambda supported on `support`, exactly over Q, then verify."""
    R = list(support)
    if (0, 0) not in R:
        R = [(0, 0)] + R
    cols = sorted({j for k in R for j in rows.get(k, {})})
    m = len(R)
    A = [[F(rows.get(R[i], {}).get(j, 0)) for i in range(m)] + [F(0)] for j in cols]
    nrm = [F(0)] * (m + 1)
    nrm[R.index((0, 0))] = F(1)
    nrm[m] = F(1)
    A.append(nrm)
    r = 0
    where = [None] * m
    for c in range(m):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = F(1) / A[r][c]
        A[r] = [v * inv for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        where[c] = r
        r += 1
    for i in range(r, len(A)):
        if A[i][m] != 0 and all(v == 0 for v in A[i][:m]):
            return None
    lam = {R[c]: A[where[c]][m] for c in range(m)
           if where[c] is not None and A[where[c]][m] != 0}
    if (0, 0) not in lam:
        return None
    return lam if EX.verify_lambda(lam, rows, ncols) else None


def exact_lambda(rows, ncols, cap=900):
    if ncols > cap:
        return None, "carrier too large for the exact lambda solve (n=%d)" % ncols
    sup = _lambda_mod_p(rows, ncols)
    if sup is None:
        return None, "no lambda mod p (the system is consistent mod p)"
    lam = _lambda_exact_on(rows, ncols, sup)
    if lam is None:
        return None, "candidate support (%d rows) did not lift to Q" % len(sup)
    return lam, "verified exactly over Q on %d rows" % len(lam)


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
        if out["verdict"] == "NOT_CERTIFIED":
            lam, why = exact_lambda(rows, len(S))
            out["lambda_attempt"] = why
            if lam is not None:
                out["verdict"] = "EMPTY_over_Q"
                out["certificate"] = "lambda_exact"
                out["lambda_support"] = len(lam)
                out["lambda_vector"] = EX._lam_out(lam)
                out["lambda_reverified"] = bool(EX.verify_lambda(lam, rows, len(S)))
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
