"""
wave4 / the case-(2) weight cascade, derived from the JSON and nothing else.

STRUCTURE (verified, not assumed -- see w4_case2_selftest.py)
------------------------------------------------------------
In the grading w = j - 2i the 92 bracket equations split as

    w = -4 : 17 equations in (C, G)                 <- self-contained
    w = -3 : 18 equations, linear in (B, F) over (C, G)
    w = -2 : 19 equations, linear in (A, E) over (B, C, F, G)
    w = -1 : 19 equations, linear in (D) over (A, B, C, E, F)   <- 13 variables
    w =  0 : 19 equations in (A, B, D, E), no new unknowns

with

    A = c_i_{2i}  (9)   B = c_i_{2i-1} (8)   C = c_i_{2i-2} (8)
    D = d_i_{2i}  (13)  E = d_i_{2i-1}(12)   F = d_i_{2i-2}(11)  G = d_i_{2i-3}(11)

REDUCTION OF THE w = -4 BLOCK
-----------------------------
Writing C = sum_{i=1..8} c_i t^i and G = sum_{j=2..12} g_j t^j, the block is
2 C G' - 3 C' G = t^2, whose t^k coefficient is sum_{i+j=k+1} (2j - 3i) c_i g_j.
For k = 2..9 the term of largest i is (i,j) = (k-1, 2) with coefficient
4 - 3(k-1) != 0, so c_1, ..., c_8 are solved TRIANGULARLY, over the localisation
at g_2.  What remains is 9 equations in g_2..g_12 -- and that is the object the
campaign calls the edge system.  This module derives it here, from the JSON,
without reading wave1/edgeQ_input.ms.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w4_case2_system as S

VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)

C_VARS = [v for v in VARS if v.startswith("c_") and S.var_weight(v) == -2]
G_VARS = [v for v in VARS if v.startswith("d_") and S.var_weight(v) == -3]
C_IDX = {v: int(v.split("_")[1]) for v in C_VARS}          # c_i_{2i-2} -> i
G_IDX = {v: int(v.split("_")[1]) for v in G_VARS}          # d_j_{2j-3} -> j


def w4_coefficients():
    """The t^k coefficient of 2CG' - 3C'G - t^2, k = 2..18, from the JSON.

    Returned as {k: [(Fraction, ci, gj), ...], "const": {k: Fraction}} so that
    the triangular solve below never re-derives the equations itself.
    """
    rows = {}
    consts = {}
    for idx in BYW[-4]:
        eq = EQS[idx]
        i, j = eq["bracket_point"]
        k = i - 1                       # bracket point (i, 2i-4) <-> t^(i-1)
        terms = []
        const = Fraction(0)
        for c, m in S.eq_terms(eq):
            if not m:
                const += c
                continue
            cv = [v for v in m if v in C_IDX]
            gv = [v for v in m if v in G_IDX]
            if len(cv) != 1 or len(gv) != 1 or m[cv[0]] != 1 or m[gv[0]] != 1:
                raise SystemExit(f"w=-4 equation {idx} is not bilinear in (C,G): {m}")
            terms.append((c, cv[0], gv[0]))
        rows[k] = terms
        consts[k] = const
    return rows, consts


def reduced_edge_system_modp(p, gvals=None):
    """Return (c_solution, residual_polys) as functions on F_p.

    Nothing symbolic: the caller supplies g values in F_p (or in a ring with
    inverse), and this returns the triangularly determined c values plus the
    9 residual equation values.  Used both for the exact residual export and
    for point checks.
    """
    rows, consts = w4_coefficients()
    if gvals is None:
        raise ValueError("gvals required")
    inv = lambda z: pow(z, p - 2, p)
    cf = lambda fr: (fr.numerator % p) * inv(fr.denominator % p) % p
    c = {}
    ks = sorted(rows)
    for k in ks[:8]:                       # k = 2..9 -> solve c_1..c_8
        target = (-cf(consts[k])) % p
        pivot_var, pivot_coef = None, None
        acc = 0
        for coef, cv, gv in rows[k]:
            if C_IDX[cv] == k:
                pivot_var, pivot_coef = cv, cf(coef) * gvals[gv] % p
            else:
                acc = (acc + cf(coef) * c[cv] % p * gvals[gv]) % p
        if pivot_var is None or pivot_coef == 0:
            return None, None
        c[pivot_var] = (target - acc) % p * inv(pivot_coef) % p
    res = []
    for k in ks[8:]:                       # k = 10..18 -> residual
        acc = cf(consts[k])
        acc = acc % p
        for coef, cv, gv in rows[k]:
            if cv not in c:
                return None, None
            acc = (acc + cf(coef) * c[cv] % p * gvals[gv]) % p
        res.append(acc % p)
    return c, res


def reduced_polys_Q():
    """The 9 residual w=-4 polynomials in the 11 G-coefficients, over Q.

    Same triangular elimination as export_reduced_ms, but nothing is reduced
    mod anything, so the result is the exact rational system that the lift
    pipeline (T4) verifies a reconstructed point against.
    """
    import sympy as sp
    rows, consts = w4_coefficients()
    gs = {v: sp.Symbol(v) for v in G_VARS}
    c, ks = {}, sorted(rows)
    for k in ks[:8]:
        pivot, pexpr, acc = None, None, sp.Integer(0)
        for coef, cv, gv in rows[k]:
            if C_IDX[cv] == k:
                pivot, pexpr = cv, sp.Rational(coef) * gs[gv]
            else:
                acc += sp.Rational(coef) * c[cv] * gs[gv]
        c[pivot] = sp.cancel((-sp.Rational(consts[k]) - acc) / pexpr)
    out = []
    for k in ks[8:]:
        e = sp.Rational(consts[k])
        for coef, cv, gv in rows[k]:
            e += sp.Rational(coef) * c[cv] * gs[gv]
        num, _ = sp.fraction(sp.cancel(sp.together(e)))
        out.append(sp.expand(num))
    return out, [gs[v] for v in G_VARS]


def export_reduced_ms(p, chart, path, planted=None, contradictory=False,
                      gauge2=False, mutant_seed=None):
    """Write the g-only reduced system to an msolve file, over F_p.

    The c's are eliminated symbolically with sympy over Q(g_2..g_12), then the
    residual equations are cleared of their g_2 denominators.
    """
    import sympy as sp
    rows, consts = w4_coefficients()
    gs = {v: sp.Symbol(v) for v in G_VARS}
    c = {}
    ks = sorted(rows)
    for k in ks[:8]:
        pivot_var, pivot_expr = None, None
        acc = sp.Integer(0)
        for coef, cv, gv in rows[k]:
            if C_IDX[cv] == k:
                pivot_var, pivot_expr = cv, sp.Rational(coef) * gs[gv]
            else:
                acc += sp.Rational(coef) * c[cv] * gs[gv]
        c[pivot_var] = sp.cancel((-sp.Rational(consts[k]) - acc) / pivot_expr)
    polys = []
    for k in ks[8:]:
        e = sp.Rational(consts[k])
        for coef, cv, gv in rows[k]:
            e += sp.Rational(coef) * c[cv] * gs[gv]
        num, _ = sp.fraction(sp.cancel(sp.together(e)))
        polys.append(sp.expand(num))
    return _write(p, chart, path, polys, gs, planted, contradictory,
                  gauge2, mutant_seed)


def _write(p, chart, path, polys, gs, planted, contradictory,
           gauge2=False, mutant_seed=None):
    import sympy as sp
    names = [str(gs[v]) for v in G_VARS]
    lines = []
    for e in polys:
        pol = sp.Poly(e, *[gs[v] for v in G_VARS])
        terms = []
        for mono, coef in zip(pol.monoms(), pol.coeffs()):
            cc = sp.Rational(coef)
            val = (int(cc.p) % p) * pow(int(cc.q) % p, p - 2, p) % p
            if val == 0:
                continue
            f = [str(val)] + [f"{names[i]}^{e2}" if e2 > 1 else names[i]
                              for i, e2 in enumerate(mono) if e2]
            terms.append("*".join(f))
        lines.append(" + ".join(terms) if terms else "0")
    pt = None
    if mutant_seed is not None:
        import random
        rnd = random.Random(mutant_seed)
        pt = {v: rnd.randrange(1, p) for v in G_VARS}
        pt["d_3_3"] = 1 if chart == "one" else 0
        if gauge2:
            pt["d_2_1"] = 1
        newlines = []
        for e, s0 in zip(polys, lines):
            val = sp.Poly(e, *[gs[x] for x in G_VARS]).eval(
                [sp.Integer(pt[x]) for x in G_VARS])
            val = sp.Rational(val)
            v = (int(val.p) % p) * pow(int(val.q) % p, p - 2, p) % p
            newlines.append(s0 if v == 0 else s0 + " + " + str((-v) % p))
        lines = newlines
    nz = [v for v in NONZERO if v in G_VARS]
    varnames = list(names) + ["sat"]
    lines.append("d_3_3 + " + str((-1) % p) if chart == "one" else "d_3_3")
    if gauge2:
        lines.append("d_2_1 + " + str((-1) % p))
    lines.append("sat*" + "*".join(nz) + " + " + str((-1) % p))
    if contradictory:
        lines.append("d_4_5 + " + str((-1) % p))
        lines.append("d_4_5 + " + str((-2) % p))
    with open(path, "w") as f:
        f.write(",".join(varnames) + "\n")
        f.write(f"{p}\n")
        f.write(",\n".join(lines) + "\n")
    return path, len(polys), varnames, pt
