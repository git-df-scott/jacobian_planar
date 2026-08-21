"""
ITEM 1 -- the residual system over the quotient ring, at fresh primes p = 1 (3).

PIPELINE (per prime, per chart)
-------------------------------
1.  The w = -4 block is reduced to 9 polynomials in the 11 G-coefficients by the
    triangular elimination of C (w4_c2_reduce.py; validated in
    w4_case2_selftest.py), the chart d_3_3 = 1 or 0 is imposed, the gauge is
    fixed, and the nonzero conditions are saturated by one Rabinowitsch
    variable.  msolve returns a RATIONAL UNIVARIATE REPRESENTATION: an eliminant
    f(w) and one numerator polynomial per coordinate.
2.  The RUR is used SYMBOLICALLY: w is kept as a variable and f(w) = 0 is added
    to the ideal, so every root of the eliminant -- including those in
    extensions of F_p -- is covered at once, rather than only the F_p-rational
    ones.  Each C and G coefficient becomes a polynomial in w.
3.  Those values are substituted into the remaining 75 equations (weights
    -3, -2, -1, 0), which involve A (9), B (8), D (13), E (12), F (11).  Two of
    those, c_0_0 and d_0_0, occur in no equation and are dropped.  The result is
    the RESIDUAL SYSTEM; its w = -1 block is the 13-variable D-block.
4.  msolve decides it.  EMPTY means no case-(2) point lies over ANY root of the
    eliminant at that prime, in that chart.

CONTROLS at every prime and chart
---------------------------------
  MUTANT  a random admissible point is planted by subtracting each residual
          equation's value at it.  A solver that answers EMPTY on the mutant
          voids that cell, and the cell is reported VOID rather than EMPTY.
  PIN     a contradictory pair is added; the solver must answer EMPTY.
The RUR itself is verified before use: the substituted C and G values must
annihilate all 17 equations of the w = -4 block modulo f(w).  That check is a
polynomial identity in w, not a spot check.
"""

import ast
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_case2_system as S
import w4_c2_reduce as RED
import w4_run as RUN

VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)
CG = set(RED.C_VARS) | set(RED.G_VARS)
REST = [v for v in VARS if v not in CG]
USED_REST = sorted({v for w in (-3, -2, -1, 0) for k in BYW[w]
                    for v in S.eq_vars(EQS[k])} - CG)


def parse_rur(path):
    txt = open(path).read().strip().rstrip(":").replace("\n", "")
    d = ast.literal_eval(txt)
    if d[0] != 0:
        return None
    p, nv, deg, names, lf, body = d[1]
    elim, den, nums = body[1][0], body[1][1], body[1][2]
    params = [n for n in names if n != names[[i for i, c in enumerate(lf)
                                             if c][-1]]] if any(lf) else names
    return dict(p=p, names=names, lf=lf, deg=deg,
                elim=elim[1], den=den, nums=[n[0][1] for n in nums],
                params=params)


def rur_values(rur):
    """{variable: coefficient list of its numerator in w}.  msolve's sign
    convention is fixed by testing against the w=-4 block, not assumed."""
    lfvar = rur["names"][[i for i, c in enumerate(rur["lf"]) if c][-1]]
    others = [n for n in rur["names"] if n != lfvar]
    return dict(zip(others, rur["nums"])), lfvar


def polystr(coeffs, p, wname="w"):
    out = []
    for i, c in enumerate(coeffs):
        c %= p
        if c == 0:
            continue
        out.append(str(c) if i == 0 else (f"{c}*{wname}^{i}" if i > 1
                                          else f"{c}*{wname}"))
    return " + ".join(out) if out else "0"


def verify_rur(vals, sign, rur, p, chart=None, gauge=()):
    """Every w=-4 equation must vanish identically modulo f(w), AND the chart
    and gauge equations must hold identically.  Exact, in F_p[w]/(f).

    Both signs satisfy the w=-4 block on their own -- the block is bilinear in
    (C,G), so (C,G) -> (-C,-G) is a symmetry, which is exactly the order-2
    residue of the gauge fixing (its determinant is 2).  The chart and gauge
    equations are what pick the sign out, so they are checked here.
    """
    import sympy as sp
    w = sp.Symbol("w")
    f = sum(c * w ** i for i, c in enumerate(rur["elim"]))
    sub = {}
    for v in RED.G_VARS:
        cs = vals.get(v)
        if cs is None:
            return False, f"RUR has no entry for {v}"
        sub[v] = sign * sum(c * w ** i for i, c in enumerate(cs))
    # solve the C's triangularly over F_p[w]/(f)
    rows, consts = RED.w4_coefficients()
    ks = sorted(rows)
    C = {}
    inv_g2 = sp.invert(sp.Poly(sub["d_2_1"], w, modulus=p), sp.Poly(f, w, modulus=p))
    for k in ks[:8]:
        pivot, acc = None, sp.Integer(0)
        pcoef = None
        for coef, cv, gv in rows[k]:
            if RED.C_IDX[cv] == k:
                pivot, pcoef = cv, sp.Rational(coef) * sub[gv]
            else:
                acc += sp.Rational(coef) * C[cv] * sub[gv]
        num = -sp.Rational(consts[k]) - acc
        pc = sp.Poly(sp.expand(pcoef), w, modulus=p)
        inv = sp.invert(pc, sp.Poly(f, w, modulus=p))
        C[pivot] = sp.rem(sp.Poly(sp.expand(num), w, modulus=p) * inv,
                          sp.Poly(f, w, modulus=p)).as_expr()
    bad = []
    for k in ks[8:]:
        e = sp.Rational(consts[k])
        for coef, cv, gv in rows[k]:
            e += sp.Rational(coef) * C[cv] * sub[gv]
        r = sp.rem(sp.Poly(sp.expand(e), w, modulus=p), sp.Poly(f, w, modulus=p))
        if not r.is_zero:
            bad.append(k)
    if bad:
        return False, f"residual rows nonzero mod f: {bad}"
    wrong = []
    targets = list(gauge)
    if chart is not None:
        targets.append(("d_3_3", 1 if chart == "one" else 0))
    for v, val in targets:
        e = sub[v] if v in sub else None
        if e is None:
            wrong.append((v, "absent"))
            continue
        r = sp.rem(sp.Poly(sp.expand(e - val), w, modulus=p),
                   sp.Poly(f, w, modulus=p))
        if not r.is_zero:
            wrong.append((v, val))
    if wrong:
        return False, f"chart/gauge equations fail for {wrong}"
    return True, ("all 9 residual rows vanish identically mod f(w); chart and "
                  f"gauge equations {targets} hold identically")


# ---------------------------------------------------------------------------
# building the reduced w=-4 export with an explicit, per-chart gauge
# ---------------------------------------------------------------------------
GAUGE_BY_CHART = {
    # (C,G) sees a 2-parameter gauge  g_j -> g_j / (alpha * lambda^(3-j)).
    # chart d_3_3 = 1 fixes alpha; d_2_1 = 1 then fixes lambda.
    "one":  [("d_2_1", 1)],
    # chart d_3_3 = 0 fixes nothing, so a second nonzero G coefficient is used;
    # exponent vectors (d_2_1) = (-1,-1), (d_12_21) = (-1,9), det = -10 != 0.
    "zero": [("d_2_1", 1), ("d_12_21", 1)],
}
# the remaining (nu-) gauge is invisible to (C,G) and is fixed downstream:
NU_GAUGE = ("c_8_16", 1)


def export_w4(p, chart, path, gauge=None, mutant_seed=None, pin=False):
    import sympy as sp
    rows, consts = RED.w4_coefficients()
    gs = {v: sp.Symbol(v) for v in RED.G_VARS}
    C, ks = {}, sorted(rows)
    for k in ks[:8]:
        pivot, pexpr, acc = None, None, sp.Integer(0)
        for coef, cv, gv in rows[k]:
            if RED.C_IDX[cv] == k:
                pivot, pexpr = cv, sp.Rational(coef) * gs[gv]
            else:
                acc += sp.Rational(coef) * C[cv] * gs[gv]
        C[pivot] = sp.cancel((-sp.Rational(consts[k]) - acc) / pexpr)
    polys = []
    for k in ks[8:]:
        e = sp.Rational(consts[k])
        for coef, cv, gv in rows[k]:
            e += sp.Rational(coef) * C[cv] * gs[gv]
        num, _ = sp.fraction(sp.cancel(sp.together(e)))
        polys.append(sp.expand(num))
    names = RED.G_VARS
    gauge = GAUGE_BY_CHART[chart] if gauge is None else gauge
    pt = None
    if mutant_seed is not None:
        rnd = random.Random(mutant_seed)
        pt = {v: rnd.randrange(1, p) for v in names}
        pt["d_3_3"] = 1 if chart == "one" else 0
        for v, val in gauge:
            pt[v] = val
    lines = []
    for e in polys:
        pol = sp.Poly(e, *[gs[v] for v in names])
        terms = []
        for mono, coef in zip(pol.monoms(), pol.coeffs()):
            cc = sp.Rational(coef)
            val = (int(cc.p) % p) * pow(int(cc.q) % p, p - 2, p) % p
            if val == 0:
                continue
            terms.append("*".join([str(val)] +
                                  [f"{names[i]}^{e2}" if e2 > 1 else names[i]
                                   for i, e2 in enumerate(mono) if e2]))
        s = " + ".join(terms) if terms else "0"
        if pt is not None:
            val = sp.Rational(pol.eval([sp.Integer(pt[v]) for v in names]))
            v = (int(val.p) % p) * pow(int(val.q) % p, p - 2, p) % p
            if v:
                s = s + " + " + str((-v) % p)
        lines.append(s)
    lines.append("d_3_3 + " + str((-1) % p) if chart == "one" else "d_3_3")
    for v, val in gauge:
        lines.append(f"{v} + {(-val) % p}")
    nz = [v for v in NONZERO if v in names]
    lines.append("sat*" + "*".join(nz) + " + " + str((-1) % p))
    if pin:
        lines += [f"d_4_5 + {(-1) % p}", f"d_4_5 + {(-2) % p}"]
    with open(path, "w") as f:
        f.write(",".join(list(names) + ["sat"]) + "\n")
        f.write(f"{p}\n")
        f.write(",\n".join(lines) + "\n")
    return path, pt


def export_residual(p, chart, rur, sign, path, mutant_seed=None, pin=False):
    """The 75 remaining equations with (C,G) replaced by their RUR values."""
    import sympy as sp
    w = sp.Symbol("w")
    vals, lfvar = rur_values(rur)
    f = sum(c * w ** i for i, c in enumerate(rur["elim"]))
    fpoly = sp.Poly(f, w, modulus=p)
    sub = {}
    for v in RED.G_VARS:
        sub[v] = sign * sum(c * w ** i for i, c in enumerate(vals[v]))
    rows, consts = RED.w4_coefficients()
    ks = sorted(rows)
    Cv = {}
    for k in ks[:8]:
        pivot, pexpr, acc = None, None, sp.Integer(0)
        for coef, cv, gv in rows[k]:
            if RED.C_IDX[cv] == k:
                pivot, pexpr = cv, sp.Rational(coef) * sub[gv]
            else:
                acc += sp.Rational(coef) * Cv[cv] * sub[gv]
        num = -sp.Rational(consts[k]) - acc
        inv = sp.invert(sp.Poly(sp.expand(pexpr), w, modulus=p), fpoly)
        Cv[pivot] = sp.rem(sp.Poly(sp.expand(num), w, modulus=p) * inv,
                           fpoly).as_expr()
    known = dict(sub)
    known.update(Cv)

    unknown = [v for v in USED_REST]
    syms = {v: sp.Symbol(v) for v in unknown}
    rnd = random.Random(mutant_seed) if mutant_seed is not None else None
    pt = None
    if rnd is not None:
        pt = {v: rnd.randrange(1, p) for v in unknown}
        pt[NU_GAUGE[0]] = NU_GAUGE[1]
        wval = rnd.randrange(0, p)
    lines = []
    for wt in (-3, -2, -1, 0):
        for idx in BYW[wt]:
            e = sp.Integer(0)
            for c, m in S.eq_terms(EQS[idx]):
                term = sp.Rational(c)
                for v, ex in m.items():
                    term *= (known[v] ** ex if v in known else syms[v] ** ex)
                e += term
            e = sp.expand(e)
            pol = sp.Poly(e, *( [syms[v] for v in unknown] + [w] ))
            terms = []
            for mono, coef in zip(pol.monoms(), pol.coeffs()):
                cc = sp.Rational(coef)
                val = (int(cc.p) % p) * pow(int(cc.q) % p, p - 2, p) % p
                if val == 0:
                    continue
                nm = [str(val)]
                for i, ex in enumerate(mono):
                    if not ex:
                        continue
                    nme = (unknown[i] if i < len(unknown) else "w")
                    nm.append(f"{nme}^{ex}" if ex > 1 else nme)
                terms.append("*".join(nm))
            s = " + ".join(terms) if terms else "0"
            if pt is not None:
                sd = {syms[v]: sp.Integer(pt[v]) for v in unknown}
                sd[w] = sp.Integer(wval)
                val = sp.Rational(sp.expand(e.subs(sd)))
                vv = (int(val.p) % p) * pow(int(val.q) % p, p - 2, p) % p
                if vv:
                    s = s + " + " + str((-vv) % p)
            lines.append(s)
    lines.append(polystr([c % p for c in rur["elim"]], p))
    if pt is not None:
        fv = sum(c * pow(wval, i, p) for i, c in enumerate(rur["elim"])) % p
        if fv:
            lines[-1] = lines[-1] + " + " + str((-fv) % p)
    lines.append(f"{NU_GAUGE[0]} + {(-NU_GAUGE[1]) % p}")
    nz = [v for v in NONZERO if v in unknown]
    lines.append("sat2*" + "*".join(nz) + " + " + str((-1) % p))
    if pin:
        lines += [f"c_1_2 + {(-1) % p}", f"c_1_2 + {(-2) % p}"]
    with open(path, "w") as fh:
        fh.write(",".join(unknown + ["w", "sat2"]) + "\n")
        fh.write(f"{p}\n")
        fh.write(",\n".join(lines) + "\n")
    return path, len(unknown) + 2, len(lines), pt
