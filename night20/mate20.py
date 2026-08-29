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
def rational_mate(P, g, kmax=3, DAmax=None, verbose=False):
    """Search for Q = A / g^k with [P, Q] = 1, i.e.
         P_x (A_y g - k A g_y) - P_y (A_x g - k A g_x) = g^(k+1),
    linear in the coefficients of A.  Returns the first solution found."""
    Px, Py = sp.expand(sp.diff(P, x)), sp.expand(sp.diff(P, y))
    gx, gy = sp.expand(sp.diff(g, x)), sp.expand(sp.diff(g, y))
    dP = sp.Poly(P, x, y).total_degree()
    dg = sp.Poly(g, x, y).total_degree()
    if DAmax is None:
        DAmax = max(6, 2 * dP)
    for k in range(1, kmax + 1):
        rhs = sp.expand(g**(k + 1))
        for DA in range(0, DAmax + 1):
            mons = [(i, j) for d in range(DA + 1) for i in range(d + 1)
                    for j in [d - i]]
            a = sp.symbols('a0:%d' % len(mons))
            A = sum(ai * x**i * y**j for ai, (i, j) in zip(a, mons))
            expr = sp.expand(Px * (sp.diff(A, y) * g - k * A * gy)
                             - Py * (sp.diff(A, x) * g - k * A * gx) - rhs)
            eqs = sp.Poly(expr, x, y).coeffs()
            sol = sp.solve(eqs, a, dict=True)
            if sol:
                s = sol[0]
                Aval = sp.expand(A.subs({ai: s.get(ai, 0) for ai in a}))
                if Aval == 0:
                    continue
                Q = sp.cancel(Aval / g**k)
                chk = sp.simplify(sp.diff(P, x) * sp.diff(Q, y)
                                  - sp.diff(P, y) * sp.diff(Q, x) - 1)
                if chk == 0:
                    return {"found": True, "k": k, "deg_A": DA,
                            "A": sp.sstr(Aval), "g": sp.sstr(g),
                            "Q": sp.sstr(Q),
                            "poles": sp.sstr(sp.factor(g)),
                            "check": "0"}
    return {"found": False, "g": sp.sstr(g), "kmax": kmax, "DAmax": DAmax}
