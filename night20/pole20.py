"""night20 -- the pole theorem and the generative construction D_P(A) = P.

D_P(Q) := P_x Q_y - P_y Q_x  (so D_P(Q) = [P, Q]).

R2 (identity).  D_P(P) = 0, so for any A,
      D_P(A/P) = ( P_x (A_y P - A P_y) - P_y (A_x P - A P_x) ) / P^2
               = P (P_x A_y - P_y A_x) / P^2  =  D_P(A) / P ,
hence D_P(A) = P  ==>  Q = A/P is a rational mate.  Verified symbolically in
verify_identity() below, on generic A and P and on explicit examples.

R1 (pole theorem, as used here).  For gradient-unimodular P every finite
denominator component of a rational solution of D_P(Q) = 1 is a component of
some fibre {P = c}.  Consequence used below: if every fibre of P is irreducible
then a rational mate exists iff a polynomial mate exists.  The reason, and what
the verification below exhibits: a pole of order k along the FULL fibre
{P = c0} means Q = f/(P-c0)^k with D_P(f) = (P-c0)^k, and restricting to the
fibre gives D_P(f)|_{P=c0} = 0, i.e. f is constant along the fibre; if the fibre
is irreducible that constant is a single number a, so (P-c0) divides f - a, and
since D_P(a/(P-c0)^k) = 0 the pole order drops by one.  Induction ends at k = 0,
a polynomial mate.  When the fibre is REDUCIBLE, f may take a different constant
on each component and the induction breaks -- which is exactly the night19
mechanism.
"""
import sys, os, json
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "night19"))
import sympy as sp
import mate19 as M
import inst20 as I
import mate20 as MT
x, y, c = I.x, I.y, I.c


def D(P, Q):
    return sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))


# ------------------------------------------------------------- verification 1
def verify_identity():
    out = []
    A = sp.Function('A')(x, y)
    P = sp.Function('P')(x, y)
    lhs = sp.simplify(sp.diff(P, x) * sp.diff(A / P, y)
                      - sp.diff(P, y) * sp.diff(A / P, x))
    rhs = sp.simplify((sp.diff(P, x) * sp.diff(A, y)
                       - sp.diff(P, y) * sp.diff(A, x)) / P)
    out.append(("generic A, P (sympy Functions): D_P(A/P) - D_P(A)/P simplifies to",
                sp.sstr(sp.simplify(lhs - rhs))))
    out.append(("D_P(P) for generic P", sp.sstr(sp.simplify(
        sp.diff(P, x)*sp.diff(P, y) - sp.diff(P, y)*sp.diff(P, x)))))
    a = sp.symbols('a0:6')
    Ae = a[0] + a[1]*x + a[2]*y + a[3]*x*y + a[4]*x**2 + a[5]*y**3
    Pe = 1 + 2*x - 3*y + x**2*y - 5*y**2 + x*y**3
    lhs2 = sp.simplify(D(Pe, Ae/Pe) - D(Pe, Ae)/Pe)
    out.append(("explicit dense A (6 free coefficients) and P of degree 4: "
                "D_P(A/P) - D_P(A)/P =", sp.sstr(sp.simplify(lhs2))))
    return out


# ------------------------------------------------------------- verification 2
def verify_pole_theorem(P, Q):
    """Given a rational mate Q of P, factor its denominator and report, for
    each factor g, whether g divides P - c for some c, i.e. whether the pole
    component is a component of a fibre.  The value c is found by reducing P
    modulo g: P is constant on {g = 0} exactly when the remainder is a
    constant."""
    Q = sp.cancel(sp.together(Q))
    num, den = sp.fraction(Q)
    rows = []
    for (g, e) in sp.factor_list(sp.expand(den))[1]:
        if sp.Poly(g, x, y).total_degree() < 1:
            continue
        # is P constant on {g = 0}?  reduce P modulo g in Singular
        sc = ("ring r=0,(x,y),dp;\npoly g=%s;\npoly P=%s;\n"
              "ideal G=std(ideal(g));\n\"RED:\",reduce(P,G);\n"
              % (I.sstr(g), I.sstr(P)))
        out = I.singular(sc)
        red = I.parse_marked(out, "RED")
        r = I.s2sympy(red) if red else None
        isconst = (r is not None and sp.Poly(sp.expand(r), x, y).total_degree() <= 0)
        rows.append({"pole component g": sp.sstr(g), "multiplicity": e,
                     "P mod g": sp.sstr(r),
                     "g divides P - c with c =": sp.sstr(r) if isconst else None,
                     "is a fibre component": bool(isconst)})
    return {"Q": sp.sstr(Q), "bracket_minus_1": sp.sstr(sp.simplify(D(P, Q) - 1)),
            "poles": rows,
            "all poles are fibre components": all(r["is a fibre component"]
                                                  for r in rows) if rows else True}


# ------------------------------------------------- the linear system D_P(A)=P
def solve_A_rhs(P, RHS, D_A):
    """Decide  D_P(A) = RHS  exactly over Q for A on the carrier S(D_A).

    The general rational mate allowed by the pole theorem has its poles on
    fibres: Q = A / prod_i (P - c_i)^{k_i}.  Since D_P(P - c) = 0,
        D_P( A / prod (P-c_i)^{k_i} ) = D_P(A) / prod (P-c_i)^{k_i} ,
    so Q is a rational mate exactly when D_P(A) = prod (P - c_i)^{k_i}.
    RHS = P is the special case of a simple pole on the fibre P = 0."""
    Pd = MT.to_dict(P)
    S = M.carrier(D_A)
    cols, rows = M.build(Pd, S)
    rhs = MT.to_dict(RHS)
    rows = sorted(set(rows) | set(rhs))
    ci = {m: k for k, m in enumerate(S)}
    ri = {m: k for k, m in enumerate(rows)}
    Amat = [dict() for _ in rows]
    for m, col in cols.items():
        for rr, v in col.items():
            Amat[ri[rr]][ci[m]] = F(v)
    b = [rhs.get(rows[k], F(0)) for k in range(len(rows))]
    sol = M.solve_linear(Amat, b, len(S))
    if sol is not None:
        A = MT.to_expr({S[k]: sol[k] for k in range(len(S)) if sol[k] != 0})
        res = sp.expand(D(P, A) - RHS)
        return {"verdict": "A_over_Q", "A": sp.sstr(A),
                "residual": sp.sstr(res), "verified": bool(res == 0),
                "n_unknowns": len(S), "n_equations": len(rows)}
    At = [dict() for _ in range(len(S) + 1)]
    for m, col in cols.items():
        for rr, v in col.items():
            At[ci[m]][ri[rr]] = F(v)
    for k in range(len(rows)):
        if b[k]:
            At[len(S)][k] = F(b[k])
    bt = [F(0)] * len(S) + [F(1)]
    lamv = M.solve_linear(At, bt, len(rows))
    if lamv is None:
        return {"verdict": "INDETERMINATE", "n_unknowns": len(S),
                "n_equations": len(rows)}
    lam = {rows[k]: lamv[k] for k in range(len(rows)) if lamv[k] != 0}
    bad = [m for m, col in cols.items()
           if sum(lam.get(r, F(0)) * v for r, v in col.items()) != 0]
    pair = sum(lam.get(rows[k], F(0)) * b[k] for k in range(len(rows)))
    return {"verdict": "EMPTY_over_Q", "lambda_support": len(lam),
            "lambda_verified": bool(not bad and pair == 1),
            "verification": "lambda^T M = 0 on all %d columns and lambda^T b = %s"
                            % (len(cols), pair),
            "lambda": {str(k): str(v) for k, v in sorted(lam.items())}
                      if len(lam) <= 40 else "(large)",
            "n_unknowns": len(S), "n_equations": len(rows)}


def solve_A(P, D_A):
    """Decide  D_P(A) = P  exactly over Q for A on the carrier S(D_A).
    Same machinery as the mate system, different right-hand side; on EMPTY a
    lambda certificate is produced and re-verified by expansion."""
    Pd = MT.to_dict(P)
    S = M.carrier(D_A)
    cols, rows = M.build(Pd, S)
    rhs = MT.to_dict(P)
    for r in rhs:
        if r not in rows:
            rows = sorted(set(rows) | {r})
    ci = {m: k for k, m in enumerate(S)}
    ri = {m: k for k, m in enumerate(rows)}
    Amat = [dict() for _ in rows]
    for m, col in cols.items():
        for rr, v in col.items():
            Amat[ri[rr]][ci[m]] = F(v)
    b = [rhs.get(rows[k], F(0)) for k in range(len(rows))]
    sol = M.solve_linear(Amat, b, len(S))
    if sol is not None:
        A = MT.to_expr({S[k]: sol[k] for k in range(len(S)) if sol[k] != 0})
        res = sp.expand(D(P, A) - P)
        return {"verdict": "A_over_Q", "A": sp.sstr(A),
                "residual": sp.sstr(res), "verified": bool(res == 0),
                "n_unknowns": len(S), "n_equations": len(rows)}
    # transposed certificate: lambda^T M = 0 and lambda^T b = 1
    At = [dict() for _ in range(len(S) + 1)]
    for m, col in cols.items():
        for rr, v in col.items():
            At[ci[m]][ri[rr]] = F(v)
    for k in range(len(rows)):
        if b[k]:
            At[len(S)][k] = F(b[k])
    bt = [F(0)] * len(S) + [F(1)]
    lamv = M.solve_linear(At, bt, len(rows))
    if lamv is None:
        return {"verdict": "INDETERMINATE", "n_unknowns": len(S),
                "n_equations": len(rows)}
    lam = {rows[k]: lamv[k] for k in range(len(rows)) if lamv[k] != 0}
    bad = []
    for m, col in cols.items():
        s = sum(lam.get(r, F(0)) * v for r, v in col.items())
        if s != 0:
            bad.append(m)
    pair = sum(lam.get(rows[k], F(0)) * b[k] for k in range(len(rows)))
    return {"verdict": "EMPTY_over_Q", "lambda_support": len(lam),
            "lambda_verified": bool(not bad and pair == 1),
            "verification": "lambda^T M = 0 on all %d columns and lambda^T b = %s"
                            % (len(cols), pair),
            "lambda": {str(k): str(v) for k, v in sorted(lam.items())}
                      if len(lam) <= 40 else "(large)",
            "n_unknowns": len(S), "n_equations": len(rows)}


# --------------------------------------- the inverted sweep: fix A, solve for P
def kernel_P(A, DP):
    """All P on the carrier S(DP) with D_P(A) = P, i.e.
       A_y P_x - A_x P_y - P = 0  --  linear in the coefficients of P.
    Returns a basis of the solution space (exact over Q)."""
    Ax, Ay = sp.expand(sp.diff(A, x)), sp.expand(sp.diff(A, y))
    S = M.carrier(DP)
    colpolys = []
    for (i, j) in S:
        m = x**i * y**j
        colpolys.append(sp.expand(Ay * sp.diff(m, x) - Ax * sp.diff(m, y) - m))
    rowset = set()
    cps = []
    for cp in colpolys:
        d = MT.to_dict(cp) if cp != 0 else {}
        cps.append(d)
        rowset |= set(d)
    rows = sorted(rowset)
    ri = {m: k for k, m in enumerate(rows)}
    Amat = [dict() for _ in rows]
    for k, d in enumerate(cps):
        for rr, v in d.items():
            Amat[ri[rr]][k] = F(v)
    return _kernel(Amat, len(S), S)


def _kernel(Amat, ncols, S):
    rowsA = [dict(r) for r in Amat]
    piv = {}
    r = 0
    for cix in range(ncols):
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
        for k in range(len(rowsA)):
            if k == r:
                continue
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
        piv[cix] = r
        r += 1
        if r == len(rowsA):
            break
    free = [k for k in range(ncols) if k not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for pcix, rr in piv.items():
            v[pcix] = -rowsA[rr].get(fc, F(0))
        basis.append(MT.to_expr({S[k]: v[k] for k in range(ncols) if v[k] != 0}))
    return basis
