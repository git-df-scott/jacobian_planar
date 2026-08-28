"""night9 — TEAR DATA mod p (protocol addition from the coordinator).

For a verified hit (P, Q) over F_p, with two fresh indeterminates u, v:

    R1 = Res_y(P - u, Q - v)   in F_p[x, u, v]
    R2 = Res_x(P - u, Q - v)   in F_p[y, u, v]

Recorded: the leading coefficient of R1 in its source variable x (the
coefficient of x^{deg_x R1}, an element of F_p[u,v]), the leading coefficient
of R2 in y, and their product.

    product a nonzero CONSTANT  ->  TEAR-EMPTY
    product NONCONSTANT in u,v  ->  TEAR-NONEMPTY

All of this is a characteristic-p measurement and is labelled with p.

Computation.  Everything is done directly over F_p (never over Z), by an exact
Laplace expansion with row-subset memoisation of the Sylvester matrix, whose
entries are sparse multivariate polynomials held as dicts
{(deg in the surviving variable, deg u, deg v) : coefficient}.  The expansion
is used when the Sylvester size is at most LAPLACE_MAX; above that the cell is
recorded as not computed rather than guessed.

Shortcut used (exact, not a heuristic).  F_p[u,v] is an integral domain, so if
lc_x(R1) is NONCONSTANT and R2 is not the zero polynomial, then
lc_x(R1)*lc_y(R2) is nonconstant and the hit is TEAR-NONEMPTY whatever lc_y(R2)
is.  R2 != 0 is certified by exhibiting numeric (y0,u0,v0) in F_p^3 at which
the x-Sylvester determinant is nonzero.  Only when lc_x(R1) is a constant is
R2 itself expanded.
"""
import numpy as np

LAPLACE_MAX = 18
DP_STATE_CAP = 200000


# ---------------------------------------------------- sparse poly over F_p
def pmul(a, b, p):
    out = {}
    for ka, ca in a.items():
        for kb, cb in b.items():
            k = (ka[0] + kb[0], ka[1] + kb[1], ka[2] + kb[2])
            c = out.get(k, 0) + ca * cb
            c %= p
            if c:
                out[k] = c
            elif k in out:
                del out[k]
    return out


def padd(a, b, p):
    out = dict(a)
    for k, c in b.items():
        c2 = (out.get(k, 0) + c) % p
        if c2:
            out[k] = c2
        elif k in out:
            del out[k]
    return out


def pneg(a, p):
    return {k: (-c) % p for k, c in a.items()}


ONE = {(0, 0, 0): 1}


def det_laplace(M, p):
    """Exact determinant of a square matrix of sparse polys, by row-subset DP."""
    N = len(M)
    dp = {0: ONE}
    for col in range(N):
        ndp = {}
        for mask, poly in dp.items():
            for r in range(N):
                if mask >> r & 1:
                    continue
                e = M[r][col]
                if not e:
                    continue
                # inversions: already-placed rows with index > r
                inv = bin(mask >> (r + 1)).count("1")
                t = pmul(poly, e, p)
                if inv & 1:
                    t = pneg(t, p)
                nm = mask | (1 << r)
                ndp[nm] = padd(ndp.get(nm, {}), t, p)
        dp = ndp
        if len(dp) > DP_STATE_CAP:
            return None
    return dp.get((1 << N) - 1, {})


# ------------------------------------------------------- Sylvester set-up
def _split(terms, var):
    """terms: list of ((ex, ey), coefdict over (u,v)) -> dict deg_in_var ->
    poly dict keyed (other_var_deg, du, dv)."""
    out = {}
    for (ex, ey), cd in terms:
        d = ey if var == 'y' else ex
        o = ex if var == 'y' else ey
        tgt = out.setdefault(d, {})
        for (du, dv), c in cd.items():
            k = (o, du, dv)
            tgt[k] = (tgt.get(k, 0) + c) % 1000000007
    for d in out:
        out[d] = {k: c for k, c in out[d].items() if c}
    return out


def _terms(S, coef, p, minus_which):
    """polynomial P - u (minus_which='u') or Q - v, as list of
    ((ex,ey), {(du,dv):c})."""
    d = {}
    for i, (ex, ey) in enumerate(S):
        c = coef[i] % p
        if c:
            d.setdefault((ex, ey), {})
            d[(ex, ey)][(0, 0)] = (d[(ex, ey)].get((0, 0), 0) + c) % p
    key = (0, 0)
    du = (1, 0) if minus_which == 'u' else (0, 1)
    d.setdefault(key, {})
    d[key][du] = (d[key].get(du, 0) - 1) % p
    return [(k, {kk: cc for kk, cc in vv.items() if cc}) for k, vv in d.items()]


def sylvester(fd, gd, p):
    """fd, gd: dict deg -> poly (coefficients in the surviving variables).
    Returns (N, matrix) of the Sylvester matrix, or (None, None) if a degree
    is 0 (handled separately)."""
    m = max(fd); n = max(gd)
    N = m + n
    M = [[{} for _ in range(N)] for _ in range(N)]
    for i in range(n):
        for k, c in fd.items():
            M[i][i + (m - k)] = c
    for i in range(m):
        for k, c in gd.items():
            M[n + i][i + (n - k)] = c
    return N, M


def _pow_poly(a, e, p):
    r = ONE
    for _ in range(e):
        r = pmul(r, a, p)
    return r


def resultant_exact(SP, SQ, a, b, p, var):
    """Res_var(P-u, Q-v) as a dict {(deg other var, du, dv): c} over F_p,
    or None if not computed within LAPLACE_MAX."""
    fd = _split(_terms(SP, a, p, 'u'), var)
    gd = _split(_terms(SQ, b, p, 'v'), var)
    fd = {k: v for k, v in fd.items() if v}
    gd = {k: v for k, v in gd.items() if v}
    if not fd or not gd:
        return {}
    m = max(fd); n = max(gd)
    if m == 0 and n == 0:
        return None
    if m == 0:
        return _pow_poly(fd[0], n, p)
    if n == 0:
        return _pow_poly(gd[0], m, p)
    if m + n > LAPLACE_MAX:
        return None
    N, M = sylvester(fd, gd, p)
    return det_laplace(M, p)   # None if the DP state cap is exceeded


# --------------------------------------- numeric certificate that R2 != 0
def _numeric_sylvester_det(SP, SQ, a, b, p, var, y0, u0, v0, rng):
    fd = _split(_terms(SP, a, p, 'u'), var)
    gd = _split(_terms(SQ, b, p, 'v'), var)
    fd = {k: v for k, v in fd.items() if v}
    gd = {k: v for k, v in gd.items() if v}
    if not fd or not gd:
        return 0
    def ev(poly):
        s = 0
        for (o, du, dv), c in poly.items():
            s += c * pow(y0, o, p) * pow(u0, du, p) * pow(v0, dv, p)
        return s % p
    fdn = {k: ev(v) for k, v in fd.items()}
    gdn = {k: ev(v) for k, v in gd.items()}
    fdn = {k: v for k, v in fdn.items() if v}
    gdn = {k: v for k, v in gdn.items() if v}
    if not fdn or not gdn:
        return 0
    m = max(fdn); n = max(gdn)
    if m == 0:
        return pow(fdn[0], n, p)
    if n == 0:
        return pow(gdn[0], m, p)
    N = m + n
    A = np.zeros((N, N), dtype=np.int64)
    for i in range(n):
        for k, c in fdn.items():
            A[i, i + (m - k)] = c
    for i in range(m):
        for k, c in gdn.items():
            A[n + i, i + (n - k)] = c
    det = 1
    r = 0
    for j in range(N):
        piv = None
        for i in range(r, N):
            if A[i, j] % p:
                piv = i
                break
        if piv is None:
            return 0
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
            det = (-det) % p
        det = (det * int(A[r, j])) % p
        iv = pow(int(A[r, j]), p - 2, p)
        A[r] = (A[r] * iv) % p
        col = A[r + 1:, j].copy()
        if col.any():
            A[r + 1:] = (A[r + 1:] - col[:, None] * A[r][None, :]) % p
        r += 1
    return det % p


def certify_nonzero(SP, SQ, a, b, p, var, tries=300, seed=1):
    rng = np.random.default_rng(seed)
    for _ in range(tries):
        y0 = int(rng.integers(0, p)); u0 = int(rng.integers(0, p))
        v0 = int(rng.integers(0, p))
        if _numeric_sylvester_det(SP, SQ, a, b, p, var, y0, u0, v0, rng):
            return True
    return False


# -------------------------------------------------------------- classify
def _lead(d):
    if not d:
        return None, None
    dd = max(k[0] for k in d)
    return dd, {(k[1], k[2]): c for k, c in d.items() if k[0] == dd}


def fmt(d):
    return {"u^%d v^%d" % k: c for k, c in sorted(d.items())}


SYMPY_MAX = 0        # sympy-over-Z fallback disabled: too slow to be useful
SYMPY_TIMEOUT = 20


class _TO(Exception):
    pass


def resultant_sympy(SP, SQ, a, b, p, var, timeout=SYMPY_TIMEOUT):
    """Fallback: sympy resultant over Z, then reduced mod p.  Valid because
    the coefficients of P, Q are the integer representatives 0..p-1, so the
    var-degree of P-u and Q-v is unchanged by reduction and Res commutes with
    reduction.  The reduction is done BEFORE the leading coefficient is read
    off, since the top degree can drop mod p."""
    import signal, sympy
    x, y, u, v = sympy.symbols('x y u v')

    def h(sig, frm):
        raise _TO()
    fP = sum(int(a[i]) * x ** SP[i][0] * y ** SP[i][1]
             for i in range(len(SP))) - u
    fQ = sum(int(b[i]) * x ** SQ[i][0] * y ** SQ[i][1]
             for i in range(len(SQ))) - v
    e = y if var == 'y' else x
    other = x if var == 'y' else y
    old = signal.signal(signal.SIGALRM, h)
    signal.alarm(timeout)
    try:
        R = sympy.resultant(sympy.Poly(fP, e), sympy.Poly(fQ, e))
        Pl = sympy.Poly(R, other, u, v)
        d = {}
        for mono, c in zip(Pl.monoms(), Pl.coeffs()):
            c = int(c) % p
            if c:
                d[mono] = c
        return d
    except _TO:
        return None
    except Exception:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _syl_size(SP, SQ, a, b, p, var):
    fd = _split(_terms(SP, a, p, 'u'), var)
    gd = _split(_terms(SQ, b, p, 'v'), var)
    fd = {k: v for k, v in fd.items() if v}
    gd = {k: v for k, v in gd.items() if v}
    if not fd or not gd:
        return 0
    return max(fd) + max(gd)


def _get_res(SP, SQ, a, b, p, var):
    R = resultant_exact(SP, SQ, a, b, p, var)
    if R is not None:
        return R, "laplace-mod-p"
    if _syl_size(SP, SQ, a, b, p, var) <= SYMPY_MAX:
        R = resultant_sympy(SP, SQ, a, b, p, var)
        if R is not None:
            return R, "sympy-ZZ-then-mod-p"
    return None, "not-computed"


def tear_data(SP, SQ, a, b, p):
    """Cheap side first: the two resultants play symmetric roles in the
    product, so whichever has the smaller Sylvester matrix is expanded first,
    and a nonconstant leading coefficient there already decides the class."""
    out = {"characteristic": p}
    sy = _syl_size(SP, SQ, a, b, p, 'y')
    sx = _syl_size(SP, SQ, a, b, p, 'x')
    order = ['y', 'x'] if sy <= sx else ['x', 'y']
    lab = {'y': ('R1', 'deg_x_R1', 'lead_coeff_R1_in_x'),
           'x': ('R2', 'deg_y_R2', 'lead_coeff_R2_in_y')}
    got = {}
    first = order[0]
    R, how = _get_res(SP, SQ, a, b, p, first)
    out["method_" + lab[first][0]] = how
    if R is None:
        out["tear"] = "TEAR-NOT-COMPUTED"
        out["reason"] = "Sylvester size %d for elimination of %s" % (
            sy if first == 'y' else sx, first)
        return out
    if not R:
        out["tear"] = "TEAR-RES-ZERO"
        out[lab[first][0] + "_zero_mod_p"] = True
        return out
    d0, lc0 = _lead(R)
    out[lab[first][1]] = d0
    out[lab[first][2]] = fmt(lc0)
    got[first] = lc0
    if set(lc0.keys()) != {(0, 0)}:
        if certify_nonzero(SP, SQ, a, b, p, order[1]):
            out["tear"] = "TEAR-NONEMPTY"
            out["decided_by"] = (
                "leading coefficient of the cheaper resultant is nonconstant "
                "and the other resultant is certified nonzero by numeric "
                "evaluation; F_p[u,v] is a domain, so the product is "
                "nonconstant")
            return out
    second = order[1]
    R2, how2 = _get_res(SP, SQ, a, b, p, second)
    out["method_" + lab[second][0]] = how2
    if R2 is None:
        out["tear"] = "TEAR-NOT-COMPUTED"
        out["reason"] = "Sylvester size %d for elimination of %s" % (
            sy if second == 'y' else sx, second)
        return out
    if not R2:
        out["tear"] = "TEAR-RES-ZERO"
        out[lab[second][0] + "_zero_mod_p"] = True
        return out
    d1, lc1b = _lead(R2)
    out[lab[second][1]] = d1
    out[lab[second][2]] = fmt(lc1b)
    lc1, lc2 = lc0, lc1b
    prod = {}
    for k1, c1 in lc1.items():
        for k2, c2 in lc2.items():
            k = (k1[0] + k2[0], k1[1] + k2[1])
            prod[k] = (prod.get(k, 0) + c1 * c2) % p
    prod = {k: c for k, c in prod.items() if c}
    out["product"] = fmt(prod)
    if not prod:
        out["tear"] = "TEAR-PRODUCT-ZERO"
    elif set(prod.keys()) == {(0, 0)}:
        out["tear"] = "TEAR-EMPTY"
    else:
        out["tear"] = "TEAR-NONEMPTY"
    return out
