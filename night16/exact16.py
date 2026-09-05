"""night12 v1 -- exact-over-Q decision layer.

Modular ranks are used for SCHEDULING ONLY.  Every verdict emitted here is a
statement about Q, backed by one of:

  (E1) lambda certificate.  An explicit rational vector lambda with
       lambda^T M = 0 on every column and lambda^T e_00 = 1, verified by exact
       arithmetic over Q.  Its existence proves M q = e has no solution over Q.

  (E2) full-column-rank certificate.  If the modular elimination returns
       rank_p(A) = n (n = number of unknowns after kernel deflation) and
       rank_p([A|e]) = n+1, then, because reduction mod p can only LOWER rank,
           rank_Q(A)     >= rank_p(A)     = n,  and rank_Q(A) <= n  (n columns)
           rank_Q([A|e]) >= rank_p([A|e]) = n+1 > n = rank_Q(A),
       so the system is inconsistent over Q.  Both modular numbers are lower
       bounds, which is the direction that makes this exact -- the random row
       compression can only lower them too, so it cannot fake this certificate.
       This is precisely the case v0's gate could not distinguish from a false
       negative; here it is decided.

  (E3) exact solution.  A rational Q reconstructed and then certified by
       expanding P_x Q_y - P_y Q_x - 1 coefficientwise over Q and checking it
       is identically zero.

Anything not reaching E1/E2/E3 is recorded as NOT CERTIFIED and stays
prime-relative; it is never reported as an emptiness result.
"""

from fractions import Fraction
import matekit16 as M

LAMBDA_MAX_N = 350          # explicit lambda is solved exactly below this size
RECON_PRIMES = [999983, 1000003, 1000033, 1000037, 1000039, 1000081, 1000099,
                1000117, 1000121, 1000133, 1000151, 1000159, 1000171, 1000183,
                1000187, 1000193, 1000199, 1000211, 1000213, 1000231]


# ------------------------------------------------------------------ lambda

def zero_row_certificate(rows):
    """cheapest exact lambda: the constant row of A is identically zero while
    the right-hand side there is 1, so lambda = e_00 works verbatim."""
    if (0, 0) not in rows or not rows[(0, 0)]:
        return {(0, 0): Fraction(1)}
    return None


def _lam_out(lam):
    """Serialise a lambda certificate so it can be re-checked offline.

    Recording only -- no verdict depends on this.  Previously a record kept
    only `lambda_support`, the number of nonzero entries, so the certificate
    the brief asks to be emitted on EMPTY could not actually be verified from
    the record.  Entries are [[i, j], [numerator, denominator]] over the
    monomial keys of the Keller rows.
    """
    return [[[int(k[0]), int(k[1])],
             [int(v.numerator), int(v.denominator)]]
            for k, v in sorted(lam.items()) if v != 0]


def verify_lambda(lam, rows, ncols):
    """exact check (ring: Q): lambda^T A = 0 on every column, lambda^T e = 1."""
    acc = {}
    for key, w in lam.items():
        for j, v in rows.get(key, {}).items():
            acc[j] = acc.get(j, Fraction(0)) + w * Fraction(v)
    if any(v != 0 for v in acc.values()):
        return False
    return lam.get((0, 0), Fraction(0)) == 1


def solve_lambda_exact(rows, ncols, pivot_rows):
    """left null vector of the pivot-row block, normalized by lambda^T e = 1.
    Exact Fraction elimination; only called for small systems."""
    R = list(pivot_rows)
    if (0, 0) not in R:
        R = [(0, 0)] + R
    m = len(R)
    # unknowns lam_0..lam_{m-1}; equations: sum_i lam_i A[R_i][j] = 0 for each j
    # plus lam at (0,0) = 1.
    cols = sorted({j for k in R for j in rows.get(k, {})})
    A = []
    for j in cols:
        A.append([Fraction(rows.get(R[i], {}).get(j, 0)) for i in range(m)] + [Fraction(0)])
    i0 = R.index((0, 0))
    nrm = [Fraction(0)] * (m + 1)
    nrm[i0] = Fraction(1)
    nrm[m] = Fraction(1)
    A.append(nrm)
    # gaussian elimination
    r = 0
    where = [None] * m
    for c in range(m):
        piv = None
        for i in range(r, len(A)):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = Fraction(1) / A[r][c]
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
    lam = {}
    for c in range(m):
        if where[c] is not None and A[where[c]][m] != 0:
            lam[R[c]] = A[where[c]][m]
    if (0, 0) not in lam:
        lam[(0, 0)] = Fraction(0)
    return lam


# ------------------------------------------------- rational reconstruction

def rat_recon(a, m):
    """reconstruct r/s = a (mod m) with |r|,s <= sqrt(m/2)."""
    import math
    bound = int(math.isqrt(m // 2))
    r0, r1 = m, a % m
    s0, s1 = 0, 1
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    return Fraction(r1, s1) if s1 > 0 else Fraction(-r1, -s1)


def solve_mod(rows, ncols, cols, p):
    """particular solution of A q = e over F_p on the given columns, or None."""
    import numpy as np
    cidx = {c: t for t, c in enumerate(cols)}
    keys = sorted(set(rows) | {(0, 0)})
    m = len(cols) + 16
    B = np.zeros((m, len(cols) + 1), dtype=np.int64)
    rngs = {}
    for t, key in enumerate(keys):
        r = M._rng_vec((77, p, t), m, p)
        rngs[key] = r
        for j, v in rows.get(key, {}).items():
            if j in cidx:
                B[:, cidx[j]] = (B[:, cidx[j]] + r * (v % p)) % p
        if key == (0, 0):
            B[:, len(cols)] = (B[:, len(cols)] + r) % p
    n = len(cols)
    row = 0
    where = [None] * n
    for c in range(n):
        nz = np.nonzero(B[row:, c])[0]
        if nz.size == 0:
            continue
        piv = row + nz[0]
        if piv != row:
            B[[row, piv]] = B[[piv, row]]
        inv = pow(int(B[row, c]), p - 2, p)
        B[row] = (B[row] * inv) % p
        f = B[:, c].copy()
        f[row] = 0
        mask = f != 0
        if mask.any():
            B[mask] = (B[mask] - f[mask, None] * B[row][None, :]) % p
        where[c] = row
        row += 1
        if row >= m:
            break
    for i in range(row, m):
        if B[i, n] % p != 0 and not B[i, :n].any():
            return None
    sol = [0] * n
    for c in range(n):
        if where[c] is not None:
            sol[c] = int(B[where[c], n]) % p
    return sol


def reconstruct_solution(rows, ncols, S, cols, P, max_primes=len(RECON_PRIMES)):
    """multi-modular solve + rational reconstruction, certified by exact
    bracket expansion (ring: Q).  Returns (Qdict, status)."""
    mod = 1
    res = None
    for pi, p in enumerate(RECON_PRIMES[:max_primes]):
        s = solve_mod(rows, ncols, cols, p)
        if s is None:
            return None, "inconsistent_mod_%d" % p
        if res is None:
            res = list(s)
            mod = p
        else:
            newmod = mod * p
            for t in range(len(res)):
                a, b = res[t], s[t]
                x = a + mod * (((b - a) * pow(mod, -1, p)) % p)
                res[t] = x % newmod
            mod = newmod
        if pi < 1:
            continue
        cand = []
        ok = True
        for v in res:
            f = rat_recon(v, mod)
            if f is None:
                ok = False
                break
            cand.append(f)
        if not ok:
            continue
        Qd = {S[c]: cand[t] for t, c in enumerate(cols) if cand[t] != 0}
        if M.is_one(M.bracket(P, Qd)):
            return Qd, "verified_bracket_eq_1"
    return None, "reconstruction_failed"


# --------------------------------------------------------------- the decider

def decide(P, S, sched_prime=M.P1, want_lambda=True):
    """Exact verdict for the mate system of P on carrier S."""
    rows, _ = M.build_system(P, S)
    n = len(S)
    out = {"n_unknowns": n, "n_rows_nonzero": len(rows)}

    lam = zero_row_certificate(rows)
    if lam is not None and verify_lambda(lam, rows, n):
        out.update({"verdict": "EMPTY_over_Q", "certificate": "lambda_exact",
                    "lambda_support": 1,
                    "lambda_vector": _lam_out(lam),
                    "lambda_reverified": bool(verify_lambda(lam, rows, n)),
                    "lambda_detail": "constant row of A is identically zero",
                    "rank_A_p": None, "rank_Ae_p": None})
        return out, rows, None

    r = M.consistency_mod_p(rows, n, sched_prime, seed=20260831)
    out["rank_A_p"] = r["rank_A"]
    out["rank_Ae_p"] = r["rank_Ae"]
    out["sched_prime"] = sched_prime
    out["nullity_p"] = n - r["rank_A"]

    if r["consistent"]:
        cols = r["pivcols"] if n > 500 else list(range(n))
        Qd, st = reconstruct_solution(rows, n, S, cols, P)
        if Qd is None and cols != list(range(n)):
            Qd, st = reconstruct_solution(rows, n, S, list(range(n)), P)
        if Qd is not None:
            out.update({"verdict": "MATE_over_Q", "certificate": "exact_solution",
                        "exact_status": st, "deg_Q": M.pdeg(Qd)})
            return out, rows, Qd
        out.update({"verdict": "NOT_CERTIFIED", "certificate": "none",
                    "exact_status": st})
        return out, rows, None

    # inconsistent at the scheduling prime
    if r["rank_A"] == n and r["rank_Ae"] == n + 1:
        out.update({"verdict": "EMPTY_over_Q",
                    "certificate": "rank_full_column_exact",
                    "lambda_support": 0,
                    "lambda_detail": "rank_p(A)=n and rank_p([A|e])=n+1; "
                                     "both are lower bounds for the ranks over Q"})
        if want_lambda and n <= LAMBDA_MAX_N:
            lam = solve_lambda_exact(rows, n, sorted(rows))
            if lam is not None and verify_lambda(lam, rows, n):
                out["certificate"] = "lambda_exact"
                out["lambda_support"] = sum(1 for v in lam.values() if v != 0)
                out["lambda_vector"] = _lam_out(lam)
                out["lambda_reverified"] = True
        return out, rows, None

    out.update({"verdict": "NOT_CERTIFIED", "certificate": "none",
                "note": "rank_p(A) < n at the scheduling prime; the negative "
                        "is prime-relative and is not reported as emptiness"})
    return out, rows, None
