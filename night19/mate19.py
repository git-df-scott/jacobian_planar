"""night19 -- in-lane kernel for the mate problem.

Representation of a bivariate polynomial: dict {(i, j): coeff} for
sum coeff * x^i y^j, zero coefficients pruned.  Coefficients may be
Fraction (ring Q) or sympy expressions (field Q(params)); every routine
below is coefficient-agnostic and uses only +, -, *, / and == 0.

Nothing here is imported from another lane except, in the callers,
night14/sy14.py (read-only) for the Shpilrain-Yu certificate.
"""
from fractions import Fraction as F
import sympy as sp


# ---------------------------------------------------------------- polynomials
def clean(A):
    return {k: v for k, v in A.items() if not _iszero(v)}


def _iszero(v):
    if isinstance(v, F) or isinstance(v, int):
        return v == 0
    if isinstance(v, sp.Expr):
        z = sp.cancel(sp.together(v))
        if z == 0:
            return True
        return sp.simplify(z) == 0
    return v == 0


def padd(*Ps):
    C = {}
    for A in Ps:
        for k, v in A.items():
            C[k] = C.get(k, 0) + v
    return clean(C)


def pmul(A, B):
    C = {}
    for a, ca in A.items():
        for b, cb in B.items():
            k = (a[0] + b[0], a[1] + b[1])
            C[k] = C.get(k, 0) + ca * cb
    return clean(C)


def pscal(c, A):
    return clean({k: c * v for k, v in A.items()})


def psub(A, B):
    return padd(A, pscal(-1, B))


def dx(A):
    return clean({(i - 1, j): v * i for (i, j), v in A.items() if i > 0})


def dy(A):
    return clean({(i, j - 1): v * j for (i, j), v in A.items() if j > 0})


def bracket(A, B):
    """[A,B] = A_x B_y - A_y B_x."""
    return psub(pmul(dx(A), dy(B)), pmul(dy(A), dx(B)))


def tdeg(A):
    return max(i + j for (i, j) in A) if A else -1


def to_str(A):
    if not A:
        return "0"
    return " + ".join("(%s)*x^%d*y^%d" % (sp.sstr(v), i, j)
                      for (i, j), v in sorted(A.items()))


# ------------------------------------------------------------- the mate system
def carrier(D):
    """S(D) = { x^i y^j : i + j <= D }, ordered."""
    return [(i, j) for d in range(D + 1) for i in range(d + 1) for j in [d - i]]


def build(P, S):
    """Columns of M: for each monomial m = x^i y^j in S, the polynomial [P, m],
    as a dict row -> coefficient.  Built by honest polynomial multiplication
    (bracket()), NOT by any closed row formula -- so it is an independent check
    on the row formula derived in UNCONDITIONAL.md.

    Returns (cols, rows) with cols a dict (i,j) -> {row: coeff} and rows the
    sorted list of all rows that occur.
    """
    cols = {}
    rows = set()
    for (i, j) in S:
        col = bracket(P, {(i, j): 1})
        cols[(i, j)] = col
        rows.update(col)
    rows.add((0, 0))                      # the target row is always an equation
    return cols, sorted(rows)


def verify_lambda(lam, cols):
    """lam: dict row -> value.  Check lam^T M = 0 on EVERY column and
    lam^T e_{(0,0)} = 1.  Returns (bool, message)."""
    bad = []
    for m, col in cols.items():
        s = 0
        for r, v in col.items():
            if r in lam:
                s = s + lam[r] * v
        if not _iszero(s):
            bad.append((m, sp.sstr(sp.simplify(s))))
    e = lam.get((0, 0), 0)
    okE = _iszero(e - 1)
    if bad:
        return False, "lambda^T M != 0 at %d columns, e.g. %s" % (len(bad), bad[:3])
    if not okE:
        return False, "lambda^T e = %s != 1" % sp.sstr(e)
    return True, "lambda^T M = 0 on all %d columns and lambda^T e = 1" % len(cols)


# ------------------------------------------------- exact linear algebra over Q
def solve_linear(A, b, ncols):
    """A: list of rows, each a dict col_index -> Fraction.  b: list of Fraction.
    Return one solution vector (list of Fraction, length ncols) or None."""
    rows = [dict(r) for r in A]
    rhs = [F(v) for v in b]
    piv = {}                                   # col -> row index
    r = 0
    order = list(range(ncols))
    for c in order:
        pr = None
        for k in range(r, len(rows)):
            if rows[k].get(c):
                pr = k
                break
        if pr is None:
            continue
        rows[r], rows[pr] = rows[pr], rows[r]
        rhs[r], rhs[pr] = rhs[pr], rhs[r]
        pc = rows[r][c]
        rows[r] = {k: v / pc for k, v in rows[r].items()}
        rhs[r] = rhs[r] / pc
        for k in range(len(rows)):
            if k == r:
                continue
            f = rows[k].get(c)
            if f:
                nr = dict(rows[k])
                for kk, vv in rows[r].items():
                    nv = nr.get(kk, F(0)) - f * vv
                    if nv:
                        nr[kk] = nv
                    elif kk in nr:
                        del nr[kk]
                rows[k] = nr
                rhs[k] = rhs[k] - f * rhs[r]
        piv[c] = r
        r += 1
        if r == len(rows):
            break
    for k in range(len(rows)):
        if not rows[k] and rhs[k] != 0:
            return None                        # inconsistent
    x = [F(0)] * ncols
    for c, ri in piv.items():
        x[c] = rhs[ri]
    return x


def decide(P, D):
    """Decide the mate system of P on S(D) EXACTLY over Q.

    Returns dict with verdict MATE_over_Q (with Q and residual) or
    EMPTY_over_Q (with a lambda certificate, re-verified by expansion)."""
    S = carrier(D)
    cols, rows = build(P, S)
    ci = {m: k for k, m in enumerate(S)}
    ri = {m: k for k, m in enumerate(rows)}
    # forward system  M q = e_{00}
    A = [dict() for _ in rows]
    for m, col in cols.items():
        for rr, v in col.items():
            A[ri[rr]][ci[m]] = F(v)
    b = [F(1) if rows[k] == (0, 0) else F(0) for k in range(len(rows))]
    q = solve_linear(A, b, len(S))
    if q is not None:
        Q = clean({S[k]: q[k] for k in range(len(S))})
        res = psub(bracket(P, Q), {(0, 0): F(1)})
        return {"verdict": "MATE_over_Q", "Q": Q, "Q_str": to_str(Q),
                "deg_Q": tdeg(Q), "residual_terms": len(res),
                "n_unknowns": len(S), "n_equations": len(rows)}
    # transposed system  [M^T ; e^T] lambda = (0,...,0,1)
    At = [dict() for _ in range(len(S) + 1)]
    for m, col in cols.items():
        for rr, v in col.items():
            At[ci[m]][ri[rr]] = F(v)
    At[len(S)][ri[(0, 0)]] = F(1)
    bt = [F(0)] * len(S) + [F(1)]
    lamv = solve_linear(At, bt, len(rows))
    if lamv is None:
        return {"verdict": "INDETERMINATE", "n_unknowns": len(S), "n_equations": len(rows)}
    lam = {rows[k]: lamv[k] for k in range(len(rows)) if lamv[k] != 0}
    good, msg = verify_lambda(lam, cols)
    return {"verdict": "EMPTY_over_Q", "lambda": {str(k): str(v) for k, v in sorted(lam.items())},
            "lambda_support": len(lam), "lambda_verified": bool(good), "verification": msg,
            "n_unknowns": len(S), "n_equations": len(rows)}


# ----------------------------------------------------------------- unimodular
def bezout(P, maxdeg=14):
    """Search for U, V with U*P_x + V*P_y = 1 by exact linear algebra over Q,
    raising the degree bound until found.  Returns (U, V, deg, residual) or None."""
    Px, Py = dx(P), dy(P)
    for d in range(0, maxdeg + 1):
        S = carrier(d)
        n = len(S)
        colpolys = []
        for m in S:
            colpolys.append(pmul(Px, {m: F(1)}))
        for m in S:
            colpolys.append(pmul(Py, {m: F(1)}))
        rows = sorted(set().union(*[set(cp) for cp in colpolys]) | {(0, 0)})
        ri = {m: k for k, m in enumerate(rows)}
        A = [dict() for _ in rows]
        for k, cp in enumerate(colpolys):
            for rr, v in cp.items():
                A[ri[rr]][k] = F(v)
        b = [F(1) if rows[k] == (0, 0) else F(0) for k in range(len(rows))]
        sol = solve_linear(A, b, 2 * n)
        if sol is not None:
            U = clean({S[k]: sol[k] for k in range(n)})
            V = clean({S[k]: sol[n + k] for k in range(n)})
            res = psub(padd(pmul(U, Px), pmul(V, Py)), {(0, 0): F(1)})
            return U, V, d, res
    return None


def certificate_search(P, D):
    """Solve the transposed system [M^T ; e^T] lambda = (0,...,0,1) over Q,
    UNCONDITIONALLY (i.e. also when a mate exists).  Returns (lam, cols) with
    lam None when no certificate exists."""
    S = carrier(D)
    cols, rows = build(P, S)
    ci = {m: k for k, m in enumerate(S)}
    ri = {m: k for k, m in enumerate(rows)}
    At = [dict() for _ in range(len(S) + 1)]
    for m, col in cols.items():
        for rr, v in col.items():
            At[ci[m]][ri[rr]] = F(v)
    At[len(S)][ri[(0, 0)]] = F(1)
    bt = [F(0)] * len(S) + [F(1)]
    lamv = solve_linear(At, bt, len(rows))
    if lamv is None:
        return None, cols
    return {rows[k]: lamv[k] for k in range(len(rows)) if lamv[k] != 0}, cols


def kernel_dim(P, D):
    """dim { lambda : lambda^T M = 0 } on the carrier S(D), over Q."""
    S = carrier(D)
    cols, rows = build(P, S)
    ri = {m: k for k, m in enumerate(rows)}
    ci = {m: k for k, m in enumerate(S)}
    At = [dict() for _ in range(len(S))]
    for m, col in cols.items():
        for rr, v in col.items():
            At[ci[m]][ri[rr]] = F(v)
    # rank by elimination
    rowsA = [dict(r) for r in At]
    r = 0
    for cix in range(len(rows)):
        pr = None
        for k in range(r, len(rowsA)):
            if rowsA[k].get(cix):
                pr = k
                break
        if pr is None:
            continue
        rowsA[r], rowsA[pr] = rowsA[pr], rowsA[r]
        pc = rowsA[r][cix]
        rowsA[r] = {k: v / pc for k, v in rowsA[r].items()}
        for k in range(r + 1, len(rowsA)):
            f = rowsA[k].get(cix)
            if f:
                nr = dict(rowsA[k])
                for kk, vv in rowsA[r].items():
                    nv = nr.get(kk, F(0)) - f * vv
                    if nv:
                        nr[kk] = nv
                    elif kk in nr:
                        del nr[kk]
                rowsA[k] = nr
        r += 1
        if r == len(rowsA):
            break
    return len(rows) - r, len(rows), len(S)
