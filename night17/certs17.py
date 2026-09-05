"""night17 -- certificates: (a) gradient-unimodularity by an exact Bezout
identity, (b) non-coordinacy by Shpilrain-Yu gradient-row reduction.

Both reimplemented in this lane.

(a) UNIMODULARITY.  P is gradient-unimodular iff 1 lies in the ideal
    (P_x, P_y) of Q[x,y].  The certificate is an explicit pair (U, V) with

        U P_x + V P_y - 1 = 0        expanded coefficientwise over Q,

    i.e. the residual dict must be EMPTY.  Two producers:
      * EUCLID  -- extended Euclid for (P_x, P_y) in the euclidean ring
        Q(x)[y]; clearing denominators gives S P_x + T P_y = d(x), and the
        identity is a certificate exactly when d is a nonzero constant.
      * LINALG  -- unknown U, V with total degree <= D, solved exactly over Q
        (pivots located mod p, then the square subsystem solved with
        Fractions).  D escalates until it succeeds or the cap is reached.
    Failure to produce a certificate is reported as NOT_CERTIFIED, never as
    "not unimodular".

(b) NON-COORDINACY (Shpilrain-Yu).  Rows (P_x, P_y); order: total degree then
    the x-exponent; step f <- f - (LT(f)/LT(g)) g whenever LM(g) | LM(f); both
    directions explored when the leading monomials are equal; memoised on the
    unordered pair of leading-coefficient-normalised rows.  A node {c, 0} with
    c a nonzero constant certifies COORDINATE; an exhausted DAG certifies
    NON_COORDINATE.
"""
from fractions import Fraction as F
import sympy as sp
import pk17 as pk

X, Y = sp.symbols("x y")
PRIME = 1000003


def to_sympy(P):
    return sum(sp.Rational(F(c).numerator, F(c).denominator) * X ** i * Y ** j
               for (i, j), c in P.items())


# ---------------------------------------------------------------- (a) Bezout
def _bezout_euclid(P):
    px, py = to_sympy(pk.dx(P)), to_sympy(pk.dy(P))
    if px == 0 or py == 0:
        return None
    try:
        f = sp.Poly(px, Y, domain=sp.QQ.frac_field(X))
        g = sp.Poly(py, Y, domain=sp.QQ.frac_field(X))
        s, t, h = f.gcdex(g)
    except Exception:
        return None
    if h.degree() != 0:
        return None
    hc = h.coeff_monomial(1)
    s, t = (s.as_expr() / hc.as_expr() if hasattr(hc, "as_expr") else s.as_expr() / hc,
            t.as_expr() / hc.as_expr() if hasattr(hc, "as_expr") else t.as_expr() / hc)
    s, t = sp.cancel(sp.together(s)), sp.cancel(sp.together(t))
    den = sp.lcm(sp.denom(sp.cancel(s)), sp.denom(sp.cancel(t)))
    den = sp.Poly(sp.expand(den), X)
    if den.degree() != 0:
        return None
    U = sp.expand(s * den.as_expr())
    V = sp.expand(t * den.as_expr())
    d = den.as_expr()
    return sp.expand(U / d), sp.expand(V / d)


def _mono(D):
    return [(i, j) for i in range(D + 1) for j in range(D + 1 - i)]


def _bezout_linalg(P, Dmax=14):
    px, py = pk.dx(P), pk.dy(P)
    for D in range(0, Dmax + 1):
        S = _mono(D)
        cols = []
        for k in S:
            cols.append(pk.pmul({k: F(1)}, px))
        for k in S:
            cols.append(pk.pmul({k: F(1)}, py))
        rows = sorted({m for c in cols for m in c})
        ridx = {m: i for i, m in enumerate(rows)}
        n, mm = len(cols), len(rows)
        if n == 0 or mm == 0:
            continue
        Ap = [[0] * n for _ in range(mm)]
        for j, c in enumerate(cols):
            for m, v in c.items():
                Ap[ridx[m]][j] = (F(v).numerator * pow(F(v).denominator, PRIME - 2, PRIME)) % PRIME
        bp = [0] * mm
        if (0, 0) in ridx:
            bp[ridx[(0, 0)]] = 1
        # gaussian elimination mod p to find pivot columns / consistency
        Am = [r[:] + [bp[i]] for i, r in enumerate(Ap)]
        piv, r = [], 0
        for c in range(n):
            pr = next((i for i in range(r, mm) if Am[i][c] % PRIME), None)
            if pr is None:
                continue
            Am[r], Am[pr] = Am[pr], Am[r]
            inv = pow(Am[r][c], PRIME - 2, PRIME)
            Am[r] = [(v * inv) % PRIME for v in Am[r]]
            for i in range(mm):
                if i != r and Am[i][c]:
                    f = Am[i][c]
                    Am[i] = [(a - f * b) % PRIME for a, b in zip(Am[i], Am[r])]
            piv.append(c)
            r += 1
            if r == mm:
                break
        if any(Am[i][n] % PRIME and not any(Am[i][:n]) for i in range(mm)):
            continue                      # inconsistent mod p at this D
        # exact solve on the pivot columns
        pr_rows = list(range(mm))
        M = [[F(Ap0) for Ap0 in []] for _ in []]
        M = []
        for i in pr_rows:
            M.append([F(0)] * len(piv) + [F(0)])
        for jj, c in enumerate(piv):
            col = cols[c]
            for m, v in col.items():
                M[ridx[m]][jj] = F(v)
        for i in pr_rows:
            M[i][len(piv)] = F(1) if rows[i] == (0, 0) else F(0)
        rr = 0
        where = [None] * len(piv)
        for c in range(len(piv)):
            pv = next((i for i in range(rr, mm) if M[i][c] != 0), None)
            if pv is None:
                continue
            M[rr], M[pv] = M[pv], M[rr]
            inv = F(1) / M[rr][c]
            M[rr] = [v * inv for v in M[rr]]
            for i in range(mm):
                if i != rr and M[i][c] != 0:
                    f = M[i][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[rr])]
            where[c] = rr
            rr += 1
        if any(M[i][len(piv)] != 0 and all(v == 0 for v in M[i][:len(piv)])
               for i in range(mm)):
            continue
        sol = [F(0)] * n
        for c in range(len(piv)):
            if where[c] is not None:
                sol[piv[c]] = M[where[c]][len(piv)]
        U = pk.clean({S[i]: sol[i] for i in range(len(S))})
        V = pk.clean({S[i]: sol[len(S) + i] for i in range(len(S))})
        return to_sympy(U), to_sympy(V)
    return None


def unimodular(P, Dmax=14):
    out = {"method": None, "residual_terms": None, "verdict": "NOT_CERTIFIED"}
    for name, fn in (("EUCLID", _bezout_euclid), ("LINALG",
                                                  lambda p: _bezout_linalg(p, Dmax))):
        try:
            r = fn(P)
        except Exception as e:                      # noqa: BLE001
            out.setdefault("errors", []).append("%s: %s" % (name, e))
            r = None
        if r is None:
            continue
        U, V = r
        res = sp.expand(U * to_sympy(pk.dx(P)) + V * to_sympy(pk.dy(P)) - 1)
        nt = 0 if res == 0 else len(sp.Poly(res, X, Y).terms())
        if nt == 0:
            out.update({"method": name, "residual_terms": 0,
                        "verdict": "UNIMODULAR_CERTIFIED",
                        "U": sp.sstr(U), "V": sp.sstr(V)})
            return out
        out.setdefault("errors", []).append("%s: residual %d terms" % (name, nt))
    return out


# ------------------------------------------------------------------ (b) SY
def _key(m):
    return (m[0] + m[1], m[0])


def _LM(f):
    return max(f, key=_key) if f else None


def _div(a, b):
    return a[0] <= b[0] and a[1] <= b[1]


def _step(f, g):
    mf, mg = _LM(f), _LM(g)
    q = (mf[0] - mg[0], mf[1] - mg[1])
    c = F(f[mf]) / F(g[mg])
    out = dict(f)
    for (i, j), v in g.items():
        k = (i + q[0], j + q[1])
        out[k] = out.get(k, F(0)) - c * F(v)
    return {k: v for k, v in out.items() if v != 0}


def _norm(f):
    if not f:
        return ()
    c = f[_LM(f)]
    return tuple(sorted((k, F(v) / F(c)) for k, v in f.items()))


def _nzc(f):
    return len(f) == 1 and (0, 0) in f and f[(0, 0)] != 0


def sy(P, node_budget=400000):
    f0, g0 = pk.clean(pk.dx(P)), pk.clean(pk.dy(P))
    seen, stack, nodes, leaves = set(), [(f0, g0)], 0, 0
    while stack:
        f, g = stack.pop()
        a, b = _norm(f), _norm(g)
        mk = (a, b) if a <= b else (b, a)
        if mk in seen:
            continue
        seen.add(mk)
        nodes += 1
        if nodes > node_budget:
            return "BUDGET_EXHAUSTED", {"nodes": nodes, "leaves": leaves}
        if (not g and _nzc(f)) or (not f and _nzc(g)):
            return "COORDINATE", {"nodes": nodes, "leaves": leaves}
        kids = []
        if f and g:
            mf, mg = _LM(f), _LM(g)
            if _div(mg, mf):
                kids.append((_step(f, g), g))
            if _div(mf, mg):
                kids.append((f, _step(g, f)))
        if not kids:
            leaves += 1
        stack.extend(kids)
    return "NON_COORDINATE", {"nodes": nodes, "leaves": leaves}


VALIDATION = [
    ("x", {(1, 0): 1}, "COORDINATE"),
    ("x + y^2", {(1, 0): 1, (0, 2): 1}, "COORDINATE"),
    ("y + x^3", {(0, 1): 1, (3, 0): 1}, "COORDINATE"),
    ("x + x^2*y", {(1, 0): 1, (2, 1): 1}, "NON_COORDINATE"),
    ("x*y", {(1, 1): 1}, "NON_COORDINATE"),
    ("x^2 + y^2", {(2, 0): 1, (0, 2): 1}, "NON_COORDINATE"),
    ("x + y^2 + 2*x^2*y + x^4",
     {(1, 0): 1, (0, 2): 1, (2, 1): 2, (4, 0): 1}, "COORDINATE"),
]

if __name__ == "__main__":
    ok = True
    for lab, p, exp in VALIDATION:
        v, st = sy(pk.clean(p))
        ok &= (v == exp)
        print("SY  %-24s -> %-15s expect %-15s %s" %
              (lab, v, exp, "ok" if v == exp else "MISMATCH"))
    for lab, p, exp in (("x + y^2", {(1, 0): 1, (0, 2): 1}, "UNIMODULAR_CERTIFIED"),
                        ("x*y^2 + y", {(1, 2): 1, (0, 1): 1}, "UNIMODULAR_CERTIFIED"),
                        ("x*y", {(1, 1): 1}, "NOT_CERTIFIED")):
        u = unimodular(pk.clean(p))
        ok &= (u["verdict"] == exp)
        print("BEZ %-24s -> %-22s via %-7s residual=%s  %s" %
              (lab, u["verdict"], u["method"], u["residual_terms"],
               "ok" if u["verdict"] == exp else "MISMATCH"))
    print("ALL MATCH" if ok else "SOME MISMATCH")
