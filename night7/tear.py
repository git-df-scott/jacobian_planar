#!/usr/bin/env python3
"""
night7 TEAR EVALUATOR
=====================

Detector for the non-properness locus (Jelonek set / asymptotic variety) of a
polynomial map F = (P, Q) : A^2 -> A^2.

LITERATURE STATEMENT IMPLEMENTED (see TEAR_NOTES.md for full discussion):

  Jelonek, "Note about the set S_f for a polynomial mapping f : C^2 -> C^2",
  Bull. Polish Acad. Sci. Math. 49(1) (2001), 67-72, Theorem 2.2,
  restated verbatim as Theorem 2.3 of El Hilany-Tsigaridas, "Computing the
  non-properness set of real polynomial maps in the plane", arXiv:2101.05245v3:

    "Consider a dominant polynomial map f : C^2 -> C^2, (x_1,x_2) |-> f(x_1,x_2).
     Let P_i(y_1,y_2,x_i) = sum_{k=0}^{n_i} P_{ik}(y_1,y_2) x_i^{n_i-k} be the
     resultant of the polynomials (f_1 - y_1, f_2 - y_2) with respect to x_j for
     distinct i,j in {1,2}. Then, the Jelonek set of f is
     {(y_1,y_2) in C^2 | P_{1,0} P_{2,0} = 0}."

  (P_{i,0} is the LEADING coefficient of the resultant in the surviving source
  variable x_i.  Note this is an EQUALITY, not merely a containment; the
  containment-only form comes from Jelonek 1993 Prop. 7, see TEAR_NOTES.md.)

  Underlying: Jelonek, "The set of points at which a polynomial map is not
  proper", Ann. Polon. Math. 58(3) (1993), 259-266, Proposition 7 + Remark 10.

Degenerate cases are reported explicitly, never silently swallowed:
  * resultant identically zero            -> flag "RESULTANT_IDENTICALLY_ZERO"
  * resultant free of the source variable -> flag "DEGREE_ZERO_IN_SOURCE_VAR"
  * actual x-degree < Sylvester bound      -> flag "DEGREE_DROP"
  * non-dominant map (jacobian det == 0)   -> flag "NOT_DOMINANT"
  * positive characteristic                -> flag "POSITIVE_CHARACTERISTIC"
    (the char-0 theorem above is NOT claimed to apply)

Controls C1/C2/C3 run at import and hard-exit on failure.  C4 is a
measurement only (no pass/fail).

Measurements only.  No conclusions are drawn here.
"""

import json
import sys

import sympy as sp

x, y, u, v = sp.symbols("x y u v")

# --------------------------------------------------------------------------
# core
# --------------------------------------------------------------------------


def _poly_ring(gens, char):
    return sp.GF(char)[tuple(gens)] if char else sp.ZZ[tuple(gens)]


def _res(g1, g2, elim, keep, char):
    """Resultant of g1,g2 eliminating `elim`, coefficients in ZZ[keep] / GF(p)[keep]."""
    dom = _poly_ring(keep, char)
    p1 = sp.Poly(g1, elim, domain=dom)
    p2 = sp.Poly(g2, elim, domain=dom)
    return sp.expand(sp.sympify(p1.resultant(p2)))


def _sylvester_bound(g1, g2, elim, src):
    """Generic bound on deg_src of Res_elim(g1,g2)."""
    p1 = sp.Poly(g1, elim)
    p2 = sp.Poly(g2, elim)
    d1e, d2e = p1.degree(), p2.degree()
    d1s = sp.Poly(g1, src).degree() if g1.has(src) else 0
    d2s = sp.Poly(g2, src).degree() if g2.has(src) else 0
    return int(d1s * d2e + d2s * d1e)


def _factors(expr, char):
    """Irreducible factorisation of expr in the (u,v) coefficient ring.

    sympy cannot factor MULTIVARIATE polynomials over a finite field; in that
    case we return a partial, explicitly-labelled description instead of
    silently pretending the factorisation exists.
    """
    if expr == 0:
        return None
    if not expr.free_symbols:
        return {"unit": str(expr), "factors": []}
    dom = sp.GF(char) if char else sp.QQ
    try:
        c, facs = sp.factor_list(sp.Poly(expr, u, v, domain=dom))
        return {
            "unit": str(c),
            "factors": [{"poly": str(f.as_expr()), "mult": int(m)} for f, m in facs],
            "complete": True,
        }
    except NotImplementedError:
        p = sp.Poly(expr, u, v, domain=dom)
        mono = [tuple(int(e) for e in m) for m in p.monoms()]
        cu = min(m[0] for m in mono)
        cv = min(m[1] for m in mono)
        if len(mono) == 1:
            # a single monomial: the factorisation is unambiguous
            facs = []
            if cu:
                facs.append({"poly": "u", "mult": cu})
            if cv:
                facs.append({"poly": "v", "mult": cv})
            return {"unit": str(p.coeffs()[0]), "factors": facs, "complete": True,
                    "note": "monomial; factored by inspection (sympy GF(%d) "
                            "multivariate factorisation unavailable)" % char}
        return {
            "complete": False,
            "reason": "sympy cannot factor multivariate polynomials over GF(%d)" % char,
            "polynomial": str(expr),
            "total_degree": int(p.total_degree()),
            "n_monomials": len(mono),
            "monomial_content": "u**%d*v**%d" % (cu, cv),
            "divisible_by_u": cu > 0,
            "divisible_by_v": cv > 0,
        }


def tear(P, Q, char=0, label=""):
    """Compute the non-properness (Jelonek) locus data of F=(P,Q): A^2 -> A^2.

    Returns a dict of MEASUREMENTS; see module docstring for the statement used.
    """
    flags = []
    if char:
        flags.append("POSITIVE_CHARACTERISTIC")

    jac = sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))
    if char:
        jac = sp.expand(sp.Poly(jac, x, y, domain=sp.GF(char)).as_expr())
    if jac == 0:
        flags.append("NOT_DOMINANT")

    g1 = P - u
    g2 = Q - v

    out = {
        "label": label,
        "char": char,
        "P": str(sp.expand(P)),
        "Q": str(sp.expand(Q)),
        "deg_P": int(sp.Poly(P, x, y).total_degree()),
        "deg_Q": int(sp.Poly(Q, x, y).total_degree()),
        "jacobian_det": str(jac),
        "branches": {},
        "flags": flags,
    }

    lcs = []
    for name, elim, src in (("R1", y, x), ("R2", x, y)):
        R = _res(g1, g2, elim, [src, u, v], char)
        b = {"eliminated": str(elim), "source_var": str(src), "resultant": str(R)}
        if R == 0:
            b["degree_in_source_var"] = None
            b["leading_coefficient"] = None
            flags.append("RESULTANT_IDENTICALLY_ZERO:" + name)
            out["branches"][name] = b
            continue
        dom = _poly_ring([u, v], char)
        Rp = sp.Poly(R, src, domain=dom)
        d = int(Rp.degree())
        lc = sp.expand(sp.sympify(Rp.LC()))
        bound = _sylvester_bound(g1, g2, elim, src)
        b["degree_in_source_var"] = d
        b["sylvester_degree_bound"] = bound
        b["leading_coefficient"] = str(lc)
        b["leading_coefficient_factorisation"] = _factors(lc, char)
        b["leading_coefficient_is_constant"] = not lc.free_symbols
        if d == 0:
            flags.append("DEGREE_ZERO_IN_SOURCE_VAR:" + name)
        if d < bound:
            flags.append("DEGREE_DROP:%s(%d<%d)" % (name, d, bound))
        lcs.append(lc)
        out["branches"][name] = b

    if len(lcs) == 2:
        prod = sp.expand(lcs[0] * lcs[1])
        if char:
            prod = sp.expand(sp.Poly(prod, u, v, domain=sp.GF(char)).as_expr())
        out["locus_polynomial"] = str(prod)
        out["locus_factorisation"] = _factors(prod, char)
        out["locus_empty"] = (prod != 0) and (not prod.free_symbols)
        lf = out["locus_factorisation"] or {}
        if out["locus_empty"]:
            out["locus_components"] = []
        elif lf.get("complete"):
            out["locus_components"] = sorted({f["poly"] for f in lf["factors"]})
        else:
            out["locus_components"] = None
            flags.append("FACTORISATION_UNAVAILABLE")
    else:
        out["locus_polynomial"] = None
        out["locus_factorisation"] = None
        out["locus_empty"] = None
        out["locus_components"] = None

    out["flags"] = flags
    return out


# --------------------------------------------------------------------------
# tame automorphisms (for C1)
# --------------------------------------------------------------------------


def compose(F, G):
    """(F o G)(x,y)."""
    return (
        sp.expand(F[0].subs({x: G[0], y: G[1]}, simultaneous=True)),
        sp.expand(F[1].subs({x: G[0], y: G[1]}, simultaneous=True)),
    )


def e1(k):
    return (x, sp.expand(y + x**k))


def e2(k):
    return (sp.expand(x + y**k), y)


def aff(a, b, c, d, e, f):
    assert a * d - b * c != 0
    return (sp.expand(a * x + b * y + e), sp.expand(c * x + d * y + f))


TAME_SAMPLES = [
    ("T1 deg2  (x, y+x^2)", e1(2)),
    ("T2 deg3  aff o (x+y^3, y)", compose(aff(1, 2, 3, 7, -1, 5), e2(3))),
    ("T3 deg4  (x, y+x^2) o (x+y^2, y)", compose(e1(2), e2(2))),
    ("T4 deg5  (x+y^5, y) o aff", compose(e2(5), aff(2, 1, 1, 1, 0, -3))),
    ("T5 deg6  (x+y^2, y) o (x, y+x^3)", compose(e2(2), e1(3))),
]


# --------------------------------------------------------------------------
# controls
# --------------------------------------------------------------------------

MONDELLO_P = x + x**2 * y + x**4 + x**6 * y**2
MONDELLO_Q = y + x**5 + x**6 * y + x**7 * y**2 + x**8 * y**3


def _die(msg, data):
    sys.stderr.write("night7/tear.py CONTROL FAILURE: %s\n" % msg)
    sys.stderr.write(json.dumps(data, indent=1) + "\n")
    sys.exit(1)


def run_controls(verbose=False):
    report = {"C1": [], "C2": None, "C3": None, "C4": None}

    # --- C1: tame automorphisms are proper -> locus EMPTY -------------------
    for name, (A, B) in TAME_SAMPLES:
        d = tear(A, B, char=0, label="C1 " + name)
        report["C1"].append(d)
        if d["locus_empty"] is not True:
            _die("C1 tame automorphism %s produced a non-empty locus" % name, d)
        bad = [f for f in d["flags"] if f.startswith(("RESULTANT_IDENTICALLY_ZERO", "NOT_DOMINANT"))]
        if bad:
            _die("C1 tame automorphism %s hit a degenerate branch %s" % (name, bad), d)

    # --- C2: (x, x*y) non-proper, locus exactly {u = 0} ---------------------
    d2 = tear(x, x * y, char=0, label="C2 (x, x*y)")
    report["C2"] = d2
    if d2["locus_empty"] is not False:
        _die("C2 (x, x*y) produced an empty locus", d2)
    if d2["locus_components"] != ["u"]:
        _die("C2 (x, x*y) locus components %r != ['u'] (hand-derived {u=0})"
             % (d2["locus_components"],), d2)

    # --- C3: (x^2, y) is finite hence proper -> locus EMPTY -----------------
    d3 = tear(x**2, y, char=0, label="C3 (x^2, y)")
    report["C3"] = d3
    if d3["locus_empty"] is not True:
        _die("C3 (x^2, y) produced a non-empty locus", d3)

    # --- C4: MEASUREMENT ONLY, characteristic 2 ----------------------------
    # The characteristic-zero theorem above is NOT claimed to apply here.
    report["C4"] = tear(MONDELLO_P, MONDELLO_Q, char=2,
                        label="C4 mondello pair over F_2 (MEASUREMENT ONLY, char 2)")

    if verbose:
        print(json.dumps(report, indent=1))
    return report


CONTROLS = run_controls(verbose=False)


if __name__ == "__main__":
    print(json.dumps(CONTROLS, indent=1))
