"""night17 -- EXACT MATE SOLVER, in-lane and self-contained.

For a fixed carrier S (a finite set of monomials for Q) the Keller equation

    [P, Q] = P_x Q_y - P_y Q_x = 1

is LINEAR in the coefficients of Q: the column of the monomial (i,j) in S is
the polynomial [P, x^i y^j], and the right-hand side is the monomial 1.  So

    A q = e,     A over Q,  e = indicator of the monomial (0,0).

Two exact verdicts:

  MATE_over_Q   -- a rational solution q is produced and [P, Q] - 1 is expanded
                   coefficientwise over Q; the verdict is issued only when the
                   residual dict is EMPTY.
  EMPTY_over_Q  -- a rational row vector lambda with lambda^T A = 0 on EVERY
                   column and lambda^T e = 1 (Fredholm); it is FOUND mod p
                   (a heuristic for a small support only) and then SOLVED and
                   VERIFIED exactly over Q.  Only the exact verification is the
                   certificate.

Anything else is NOT_CERTIFIED -- never reported as emptiness.

Null directions.  Q -> Q + h(P) leaves [P,Q] unchanged, and those directions
lie inside the carrier whenever deg-bound >= deg P; they enlarge the solution
space, so they can never turn a consistent system inconsistent.  The kernel
dimension is reported.

CONTROL (mandatory): the solver must recover the mate of a known coordinate of
degree >= 10 before any EMPTY it produces is trusted -- see the __main__ block.
"""
import sys
import time
from fractions import Fraction as F

import pk17 as pk

PRIME = (1 << 61) - 1


def carrier(D):
    return sorted((i, j) for i in range(D + 1) for j in range(D + 1 - i))


def build(P, S):
    cols = [pk.bracket(P, {m: F(1)}) for m in S]
    rows = sorted({k for c in cols for k in c})
    return cols, rows


def _modp(v):
    v = F(v)
    return (v.numerator % PRIME) * pow(v.denominator % PRIME, PRIME - 2, PRIME) % PRIME


def _elim_modp(M, ncol):
    """in-place gauss-jordan mod PRIME; returns pivot columns and row ops."""
    m = len(M)
    C = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
    piv, r = [], 0
    for c in range(ncol):
        pr = next((i for i in range(r, m) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        C[r], C[pr] = C[pr], C[r]
        inv = pow(M[r][c], PRIME - 2, PRIME)
        M[r] = [v * inv % PRIME for v in M[r]]
        C[r] = [v * inv % PRIME for v in C[r]]
        for i in range(m):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % PRIME for a, b in zip(M[i], M[r])]
                C[i] = [(a - f * b) % PRIME for a, b in zip(C[i], C[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    return piv, C, r


def _exact_solve(cols, rows, S, pivcols):
    """solve A q = e exactly over Q using only the pivot columns."""
    ridx = {m: i for i, m in enumerate(rows)}
    nr, nc = len(rows), len(pivcols)
    M = [[F(0)] * (nc + 1) for _ in range(nr)]
    for j, c in enumerate(pivcols):
        for m, v in cols[c].items():
            M[ridx[m]][j] = F(v)
    if (0, 0) in ridx:
        M[ridx[(0, 0)]][nc] = F(1)
    r, where = 0, [None] * nc
    for c in range(nc):
        pr = next((i for i in range(r, nr) if M[i][c] != 0), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = F(1) / M[r][c]
        M[r] = [v * inv for v in M[r]]
        for i in range(nr):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        where[c] = r
        r += 1
    for i in range(nr):
        if M[i][nc] != 0 and all(v == 0 for v in M[i][:nc]):
            return None
    q = {}
    for c in range(nc):
        if where[c] is not None and M[where[c]][nc] != 0:
            q[S[pivcols[c]]] = M[where[c]][nc]
    return q


def _lambda_exact(cols, rows, support):
    """solve lambda supported on `support` (row indices) exactly over Q."""
    R = list(support)
    r0 = rows.index((0, 0))
    if r0 not in R:
        R = [r0] + R
    n = len(R)
    eqs = []
    for c in cols:                                  # lambda^T A = 0 per column
        eqs.append([F(c.get(rows[i], 0)) for i in R] + [F(0)])
    nrm = [F(0)] * (n + 1)
    nrm[R.index(r0)] = F(1)
    nrm[n] = F(1)                                   # lambda^T e = 1
    eqs.append(nrm)
    r, where = 0, [None] * n
    for c in range(n):
        pr = next((i for i in range(r, len(eqs)) if eqs[i][c] != 0), None)
        if pr is None:
            continue
        eqs[r], eqs[pr] = eqs[pr], eqs[r]
        inv = F(1) / eqs[r][c]
        eqs[r] = [v * inv for v in eqs[r]]
        for i in range(len(eqs)):
            if i != r and eqs[i][c] != 0:
                f = eqs[i][c]
                eqs[i] = [a - f * b for a, b in zip(eqs[i], eqs[r])]
        where[c] = r
        r += 1
    for i in range(len(eqs)):
        if eqs[i][n] != 0 and all(v == 0 for v in eqs[i][:n]):
            return None
    lam = {}
    for c in range(n):
        if where[c] is not None and eqs[where[c]][n] != 0:
            lam[rows[R[c]]] = eqs[where[c]][n]
    return lam


def verify_lambda(lam, cols, S):
    """lambda^T A = 0 on every column and lambda^T e = 1, exactly over Q."""
    if lam.get((0, 0), F(0)) != 1:
        return False
    for c in cols:
        s = sum(F(v) * lam.get(m, F(0)) for m, v in c.items())
        if s != 0:
            return False
    return True


def stage(P, D, verbose=True):
    S = carrier(D)
    cols, rows = build(P, S)
    if (0, 0) not in rows:
        # no column of A has a constant term: lambda = e_{(0,0)} kills every
        # column and pairs to 1 with the right-hand side -- an exact certificate
        return ({"deg_Q_bound": D, "n_unknowns": len(S), "n_equations": len(rows),
                 "verdict": "EMPTY_over_Q", "certificate": "lambda_exact",
                 "lambda_support": 1, "lambda": {"0,0": "1"},
                 "note": "no column of [P, monomial] has a constant term"},
                cols, rows, None)
    ridx = {m: i for i, m in enumerate(rows)}
    nr, nc = len(rows), len(S)
    M = [[0] * (nc + 1) for _ in range(nr)]
    for j, c in enumerate(cols):
        for m, v in c.items():
            M[ridx[m]][j] = _modp(v)
    M[ridx[(0, 0)]][nc] = 1
    piv, C, rank = _elim_modp([r[:] for r in M], nc)
    Mr = [r[:] for r in M]
    piv2, C2, rank2 = _elim_modp(Mr, nc)
    incons = [i for i in range(nr) if Mr[i][nc] and not any(Mr[i][:nc])]
    out = {"deg_Q_bound": D, "n_unknowns": nc, "n_equations": nr,
           "rank_mod_p": rank2, "kernel_dim_mod_p": nc - rank2}
    if not incons:
        q = _exact_solve(cols, rows, S, piv2)
        if q is None:
            out["verdict"] = "NOT_CERTIFIED"
            out["note"] = "consistent mod p, exact solve on the pivot columns failed"
            return out, cols, rows, None
        resid = pk.psub(pk.bracket(P, q), {(0, 0): F(1)})
        if resid:
            out["verdict"] = "NOT_CERTIFIED"
            out["note"] = "exact candidate failed the coefficientwise check"
            return out, cols, rows, None
        out["verdict"] = "MATE_over_Q"
        out["bracket_minus_one_terms"] = 0
        return out, cols, rows, q
    sup = [i for i in range(nr) if C2[incons[0]][i]]
    lam = _lambda_exact(cols, rows, sup)
    if lam is not None and verify_lambda(lam, cols, S):
        out["verdict"] = "EMPTY_over_Q"
        out["certificate"] = "lambda_exact"
        out["lambda_support"] = len(lam)
        out["lambda"] = {"%d,%d" % k: str(v) for k, v in
                         sorted(lam.items())[:40]}
        return out, cols, rows, None
    out["verdict"] = "NOT_CERTIFIED"
    out["note"] = "inconsistent mod p; the candidate lambda did not lift to Q"
    return out, cols, rows, None


def solve(P, max_cols=1400, verbose=True, degs=None):
    d = pk.tdeg(P)
    stages = []
    for D in (degs or (d, (3 * d + 1) // 2, 2 * d)):
        if len(carrier(D)) > max_cols:
            stages.append({"deg_Q_bound": D, "n_unknowns": len(carrier(D)),
                           "verdict": "SKIPPED_too_large"})
            continue
        t = time.time()
        out, cols, rows, q = stage(P, D, verbose)
        out["secs"] = round(time.time() - t, 1)
        stages.append(out)
        if verbose:
            print("      D=%-3d n=%-5d %-16s (%.1fs)"
                  % (D, out["n_unknowns"], out["verdict"], out["secs"]))
            sys.stdout.flush()
        if out["verdict"] == "MATE_over_Q":
            return {"verdict": "MATE_over_Q", "stages": stages,
                    "Q": {"%d,%d" % k: str(v) for k, v in q.items()},
                    "Q_str": pk.to_str(q)}
    done = [s for s in stages if s.get("verdict") not in (None, "SKIPPED_too_large")]
    if done and all(s["verdict"] == "EMPTY_over_Q" for s in done):
        v = "EMPTY_over_Q_all_stages"
    else:
        v = "NOT_CERTIFIED"
    return {"verdict": v, "stages": stages}


if __name__ == "__main__":
    import coord17 as CO
    print("MATE-SOLVER CONTROL -- recover the mate of a known coordinate")
    ok = True
    for pd in (5, 6):
        P, Qk = CO.deg_y2_coordinate(pd)
        t = time.time()
        r = solve(P)
        good = r["verdict"] == "MATE_over_Q"
        ok &= good
        print("  coordinate deg %-3d (known mate deg %d): %-14s  %s  [%.1fs]"
              % (pk.tdeg(P), pk.tdeg(Qk), r["verdict"],
                 "ok" if good else "*** FAILED ***", time.time() - t))
        if good:
            Q = {tuple(int(a) for a in k.split(",")): F(v)
                 for k, v in r["Q"].items()}
            chk = pk.psub(pk.bracket(P, Q), {(0, 0): F(1)})
            print("      [P,Q]-1 residual terms = %d ; deg Q = %d"
                  % (len(chk), pk.tdeg(Q)))
            ok &= (chk == {})
    for lab, P in (("x*y", {(1, 1): F(1)}), ("x^2 + y^2", {(2, 0): F(1), (0, 2): F(1)})):
        r = solve(pk.clean(P), verbose=False)
        print("  negative control %-10s -> %s" % (lab, r["verdict"]))
        ok &= r["verdict"].startswith("EMPTY")
    print("CONTROL PASS" if ok else "*** CONTROL FAILED ***")
