"""night20 -- exact mate solving and rational-mate solving.

The exact bivariate kernel (dict-of-monomials polynomials, exact linear
algebra over Q, the transposed lambda certificate) is imported UNCHANGED from
night19/mate19.py, which is read-only for this lane; night19's own controls
(C1) hard-gate that code path on coordinates of degree 1..10.  This file adds:
the escalation schedule, the h(P) null-direction bookkeeping, and the
rational-mate solve in the fraction field.
"""
import sys, os
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "night19"))
sys.path.insert(0, HERE)
import sympy as sp
import mate19 as M
import inst20 as I

x, y, c = I.x, I.y, I.c


# ------------------------------------------------------------- conversions
def to_dict(P):
    p = sp.Poly(sp.expand(P), x, y)
    return {m: F(sp.Rational(co).p, sp.Rational(co).q)
            for m, co in zip(p.monoms(), p.coeffs())}


def to_expr(d):
    return sp.expand(sum(sp.Rational(v.numerator, v.denominator) * x**i * y**j
                         for (i, j), v in d.items()))


# ------------------------------------------------------------ the mate solve
def mate_verdict(P, Dlist, verbose=False):
    """Decide [P,Q] = 1 exactly over Q on the carriers S(D), D in Dlist.
    Stops at the first MATE.  Records the h(P) null-direction count."""
    Pd = to_dict(P)
    dP = M.tdeg(Pd)
    rows = []
    for D in Dlist:
        r = M.decide(Pd, D)
        nulls = D // dP + 1 if dP > 0 else 0      # 1, P, P^2, ... with deg <= D
        rec = {"D": D, "verdict": r["verdict"], "n_unknowns": r["n_unknowns"],
               "n_equations": r["n_equations"],
               "h(P)_null_directions_expected": nulls}
        if r["verdict"] == "MATE_over_Q":
            Q = to_expr(r["Q"])
            resid = sp.expand(sp.diff(P, x)*sp.diff(Q, y)
                              - sp.diff(P, y)*sp.diff(Q, x) - 1)
            rec.update({"Q": sp.sstr(Q), "deg_Q": r["deg_Q"],
                        "bracket_minus_1": sp.sstr(resid),
                        "verified": bool(resid == 0)})
            rows.append(rec)
            return "MATE", rows
        if r["verdict"] == "EMPTY_over_Q":
            rec.update({"lambda_support": r["lambda_support"],
                        "lambda_verified": r["lambda_verified"],
                        "verification": r["verification"],
                        "lambda": r["lambda"] if r["lambda_support"] <= 40 else "(large)"})
        rows.append(rec)
        if verbose:
            print("      D=%-3d %-14s unknowns=%-5d eqs=%-5d %s"
                  % (D, r["verdict"], r["n_unknowns"], r["n_equations"],
                     ("|lambda|=%d verified=%s" % (r.get("lambda_support"),
                      r.get("lambda_verified"))) if r["verdict"] == "EMPTY_over_Q" else ""),
                  flush=True)
    return "EMPTY", rows


def schedule(P, mult=2, cap=26):
    d = sp.Poly(P, x, y).total_degree()
    top = min(cap, max(mult * d, d + 4))
    return sorted(set(list(range(1, min(top, 8) + 1)) +
                      list(range(8, top + 1, 2)) + [top]))


# ------------------------------------------------------- the rational mate
def _solve_A(P, B, DA):
    """solve  P_x (A_y B - A B_y) - P_y (A_x B - A B_x) = B^2  for a
    polynomial A of total degree <= DA, exactly over Q.  Q = A/B then has
    [P, Q] = 1."""
    Px, Py = sp.expand(sp.diff(P, x)), sp.expand(sp.diff(P, y))
    Bx, By = sp.expand(sp.diff(B, x)), sp.expand(sp.diff(B, y))
    mons = [(i, j) for d in range(DA + 1) for i in range(d + 1) for j in [d - i]]
    a = sp.symbols('a0:%d' % len(mons))
    A = sum(ai * x**i * y**j for ai, (i, j) in zip(a, mons))
    expr = sp.expand(Px * (sp.diff(A, y) * B - A * By)
                     - Py * (sp.diff(A, x) * B - A * Bx) - sp.expand(B**2))
    eqs = sp.Poly(expr, x, y).coeffs()
    M, b = sp.linear_eq_to_matrix(eqs, a)
    sol = sp.linsolve((M, b), a)
    if not sol:
        return None
    s0 = list(sol)[0]
    if s0 is None:
        return None
    sub = {}
    free = [t for t in s0.free_symbols if t in set(a)]
    for t in free:
        sub[t] = 0
    vals = [sp.simplify(t.subs(sub)) if hasattr(t, 'subs') else t for t in s0]
    if all(v == 0 for v in vals):
        # try setting one free parameter to 1
        for t in free:
            sub2 = {u: (1 if u == t else 0) for u in free}
            vals = [sp.simplify(v.subs(sub2)) if hasattr(v, 'subs') else v
                    for v in s0]
            if any(v != 0 for v in vals):
                break
    if all(v == 0 for v in vals):
        return None
    return sp.expand(A.subs(dict(zip(a, vals))))


def rational_mate(P, g, kmax=3, DAmax=None, verbose=False):
    """Search for Q = A / g^k with [P, Q] = 1 (kept for the night19 control)."""
    d = sp.Poly(P, x, y).total_degree()
    if DAmax is None:
        DAmax = max(6, 2 * d)
    for k in range(1, kmax + 1):
        B = sp.expand(g**k)
        for DA in range(0, DAmax + 1):
            A = _solve_A(P, B, DA)
            if A is None or A == 0:
                continue
            Q = sp.cancel(A / B)
            chk = sp.simplify(sp.diff(P, x) * sp.diff(Q, y)
                              - sp.diff(P, y) * sp.diff(Q, x) - 1)
            if chk == 0:
                return {"found": True, "k": k, "deg_A": DA, "A": sp.sstr(A),
                        "g": sp.sstr(g), "Q": sp.sstr(Q),
                        "poles": sp.sstr(sp.factor(B)), "check": "0"}
    return {"found": False, "g": sp.sstr(g), "kmax": kmax, "DAmax": DAmax}


def rational_mate_box(P, gens, kmax=3, DAmax=None, verbose=False):
    """Search for a rational mate Q = A / B whose pole divisor is supported on
    the given generators: B runs over all products g1^k1 ... gr^kr with
    0 <= ki <= kmax and B non-constant, A over all polynomials of total degree
    <= DAmax.  Exact linear algebra over Q throughout."""
    import itertools
    d = sp.Poly(P, x, y).total_degree()
    if DAmax is None:
        DAmax = max(8, 2 * d)
    tried = []
    for ks in itertools.product(*[range(kmax + 1)] * len(gens)):
        if all(k == 0 for k in ks):
            continue
        B = sp.expand(sp.prod([g**k for g, k in zip(gens, ks)]))
        if sp.Poly(B, x, y).total_degree() > 3 * d + 4:
            continue
        tried.append(sp.sstr(sp.factor(B)))
        for DA in range(0, DAmax + 1):
            A = _solve_A(P, B, DA)
            if A is None or A == 0:
                continue
            Q = sp.cancel(A / B)
            chk = sp.simplify(sp.diff(P, x) * sp.diff(Q, y)
                              - sp.diff(P, y) * sp.diff(Q, x) - 1)
            if chk == 0:
                return {"found": True, "exponents": list(ks), "deg_A": DA,
                        "A": sp.sstr(A), "Q": sp.sstr(Q),
                        "poles": sp.sstr(sp.factor(B)), "check": "0",
                        "n_denominators_tried": len(tried)}
    return {"found": False, "n_denominators_tried": len(tried),
            "denominators_tried": tried[:40], "kmax": kmax, "DAmax": DAmax,
            "generators": [sp.sstr(g) for g in gens]}
