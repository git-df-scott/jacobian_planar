"""
ITEM 1 -- the residual cascade, solved by exact elimination instead of by
throwing 53 variables at a Groebner engine.

WHY NOT BRUTE FORCE
-------------------
The direct route (all 92 equations, all variables, one msolve call) was run and
is recorded: at p = 1000003 in the chart d_3_3 = 1 it was OOM-killed by the
kernel at 10 GB of resident memory.  That is a resource stall, not a verdict.
The cascade below replaces it with linear algebra of the right size.

THE ELIMINATION
---------------
Fix a solution (C, G) of the w = -4 block, living in K = F_p[w]/(g) for g an
irreducible factor of the eliminant.  Then

  w = -3 :  M3 (B,F) = 0            M3 constant over K -> (B,F) = s1 v1 + s2 v2
  w = -2 :  M2 (A,E) = r2(s)        r2 QUADRATIC in s
              -> one consistency equation L2 . r2(s) = 0 per left-kernel row,
                 and (A,E) = sum_mono s^mono X_mono + sum_j u_j k_j
  w = -1 :  M1 D    = r1(s,u)       r1 of degree <= 3
              -> one consistency equation per left-kernel row of M1,
                 and D determined up to ker M1 (which is spanned by d_0_0, a
                 variable occurring in no equation at all)
  w =  0 :  19 equations, bilinear, no new unknowns -> 19 conditions

so the residual system collapses to a handful of polynomial equations in the
parameters (s1, s2, u1, ...).  Every matrix here is over K and every solve is
exact (wave4/w4_gf.py, self-tested with negative controls).

The parameter system is then handed to msolve with w kept as a variable and
g(w) = 0 adjoined, so the verdict covers the whole Galois orbit of that factor.

CONTROLS
--------
  * the (C,G) values must annihilate all 17 equations of the w = -4 block in K
    -- checked before anything else, and the run aborts if not;
  * MUTANT: a random parameter point is planted in the final system; msolve
    must not answer EMPTY;
  * PIN: a contradictory pair is added; msolve must answer EMPTY.
"""

import ast
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_case2_system as S
import w4_c2_reduce as RED
import w4_c2_residual as RS
import w4_gf as GF
import w4_msformat as MF
import w4_run as RUN

W = GF.W
VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)
PIECE = {}
for v in VARS:
    wt = S.var_weight(v)
    PIECE[v] = ({0: "A", -1: "B", -2: "C"} if v.startswith("c_")
                else {0: "D", -1: "E", -2: "F", -3: "G"})[wt]
OF = {L: [v for v in VARS if PIECE[v] == L] for L in "ABCDEFG"}


def redW(expr, g, p):
    """Reduce an expression, polynomial in W with arbitrary other symbols in the
    coefficients, modulo g(W) and modulo p."""
    e = sp.expand(expr)
    pe = sp.Poly(e, W)
    r = sp.rem(pe, sp.Poly(g, W))
    out = sp.Integer(0)
    for (k,), c in zip(r.monoms(), r.coeffs()):
        cc = sp.expand(c)
        terms = cc.as_ordered_terms()
        red = sp.Integer(0)
        for t in terms:
            num, rest = t.as_coeff_Mul()
            num = sp.Rational(num)
            v = (int(num.p) % p) * pow(int(num.q) % p, p - 2, p) % p
            if v:
                red += v * rest
        out += red * W ** k
    return sp.expand(out)


def eq_expr(idx, env, g, p):
    """Value of equation idx with `env` giving an expression for every variable."""
    e = sp.Integer(0)
    for c, m in S.eq_terms(EQS[idx]):
        t = sp.Rational(c)
        for v, ex in m.items():
            t *= env[v] ** ex
        e += t
    return redW(e, g, p)


def block_matrix(w, letters, env, g, p):
    """(M, rhs) for the block: M * unknowns + rhs = 0, unknowns = the letters."""
    cols = [v for L in letters for v in OF[L]]
    syms = {v: sp.Symbol("__" + v) for v in cols}
    env2 = dict(env)
    env2.update(syms)
    M, rhs = [], []
    for idx in BYW[w]:
        e = eq_expr(idx, env2, g, p)
        pe = sp.expand(e)
        row = []
        for v in cols:
            row.append(redW(sp.diff(pe, syms[v]), g, p))
        const = redW(pe.subs({syms[v]: 0 for v in cols}), g, p)
        # linearity check: the equation must be affine in the unknowns
        chk = redW(pe - const - sum(row[i] * syms[v] for i, v in enumerate(cols)),
                   g, p)
        if sp.expand(chk) != 0:
            raise SystemExit(f"w={w} equation {idx} is not affine in {letters}")
        M.append(row)
        rhs.append(const)
    return M, rhs, cols


def cascade(p, chart, rur, sign, g, verbose=True):
    """Return (params, equations, env) -- the collapsed residual system over K."""
    Kf = GF.K(p, g)
    vals, _lf = RS.rur_values(rur)
    env = {}
    for v in RED.G_VARS:
        env[v] = redW(sign * sum(c * W ** i for i, c in enumerate(vals[v])), g, p)
    # C from the triangular solve, in K
    rows, consts = RED.w4_coefficients()
    ks = sorted(rows)
    for k in ks[:8]:
        pivot, pexpr, acc = None, None, sp.Integer(0)
        for coef, cv, gv in rows[k]:
            if RED.C_IDX[cv] == k:
                pivot, pexpr = cv, sp.Rational(coef) * env[gv]
            else:
                acc += sp.Rational(coef) * env[cv] * env[gv]
        num = redW(-sp.Rational(consts[k]) - acc, g, p)
        env[pivot] = redW(num * Kf.inv(redW(pexpr, g, p)), g, p)
    # CONTROL: the w=-4 block must vanish in K
    env0 = dict(env)
    for v in VARS:
        env0.setdefault(v, sp.Integer(0))
    bad = [i for i in BYW[-4] if sp.expand(eq_expr(i, env0, g, p)) != 0]
    if bad:
        raise SystemExit(f"the (C,G) values do not satisfy the w=-4 block: {bad}")

    # ---- w = -3 : homogeneous in (B,F) --------------------------------------
    M3, r3, c3 = block_matrix(-3, "BF", env0, g, p)
    if any(sp.expand(x) != 0 for x in r3):
        raise SystemExit("the w=-3 block is not homogeneous in (B,F)")
    _, ker3, _ = GF.solve(Kf, M3, [sp.Integer(0)] * len(M3))
    d = len(ker3)
    S_ = sp.symbols(f"s1:{d + 1}") if d else ()
    for i, v in enumerate(c3):
        env[v] = redW(sum(S_[j] * ker3[j][i] for j in range(d)), g, p)

    # ---- w = -2 : affine in (A,E), right-hand side quadratic in s -----------
    envAE = dict(env)
    for v in VARS:
        envAE.setdefault(v, sp.Integer(0))
    M2, r2, c2 = block_matrix(-2, "AE", envAE, g, p)
    part2, ker2, lk2 = GF.solve(Kf, M2, [sp.Integer(0)] * len(M2))
    e = len(ker2)
    U_ = sp.symbols(f"u1:{e + 1}") if e else ()
    conds = []
    for row in lk2:
        cval = sp.Integer(0)
        for j, cc in enumerate(row):
            cval += cc * (-r2[j])
        conds.append(("w=-2 consistency", redW(cval, g, p)))
    # particular solution: solve for each monomial of r2 separately
    mons = sorted({m for j in range(len(r2))
                   for m in sp.Poly(sp.expand(-r2[j]), *S_).monoms()}) if S_ else [()]
    partAE = [sp.Integer(0)] * len(c2)
    for mono in mons:
        rhs = []
        for j in range(len(r2)):
            pj = sp.Poly(sp.expand(-r2[j]), *S_) if S_ else None
            rhs.append(pj.coeff_monomial(mono) if pj is not None else -r2[j])
        pt, _, _ = GF.solve(Kf, M2, [redW(x, g, p) for x in rhs])
        mexpr = sp.prod([S_[i] ** a for i, a in enumerate(mono)]) if S_ else 1
        partAE = [redW(partAE[i] + mexpr * pt[i], g, p) for i in range(len(c2))]
    for i, v in enumerate(c2):
        env[v] = redW(partAE[i] + sum(U_[j] * ker2[j][i] for j in range(e)), g, p)

    # ---- w = -1 : affine in D ----------------------------------------------
    envD = dict(env)
    for v in VARS:
        envD.setdefault(v, sp.Integer(0))
    M1, r1, c1 = block_matrix(-1, "D", envD, g, p)
    _, ker1, lk1 = GF.solve(Kf, M1, [sp.Integer(0)] * len(M1))
    for row in lk1:
        cval = sp.Integer(0)
        for j, cc in enumerate(row):
            cval += cc * (-r1[j])
        conds.append(("w=-1 consistency", redW(cval, g, p)))
    PAR = list(S_) + list(U_)
    monsD = sorted({m for j in range(len(r1))
                    for m in sp.Poly(sp.expand(-r1[j]), *PAR).monoms()}) if PAR else [()]
    partD = [sp.Integer(0)] * len(c1)
    for mono in monsD:
        rhs = []
        for j in range(len(r1)):
            pj = sp.Poly(sp.expand(-r1[j]), *PAR)
            rhs.append(pj.coeff_monomial(mono))
        pt, _, _ = GF.solve(Kf, M1, [redW(x, g, p) for x in rhs])
        mexpr = sp.prod([PAR[i] ** a for i, a in enumerate(mono)])
        partD = [redW(partD[i] + mexpr * pt[i], g, p) for i in range(len(c1))]
    Z_ = sp.symbols(f"z1:{len(ker1) + 1}") if ker1 else ()
    for i, v in enumerate(c1):
        env[v] = redW(partD[i] + sum(Z_[j] * ker1[j][i] for j in range(len(ker1))),
                      g, p)

    # ---- w = 0 : pure conditions -------------------------------------------
    envF = dict(env)
    for v in VARS:
        envF.setdefault(v, sp.Integer(0))
    for idx in BYW[0]:
        conds.append(("w=0", eq_expr(idx, envF, g, p)))

    params = list(S_) + list(U_) + list(Z_)
    if verbose:
        print(f"      K = F_{p}[w]/(g), deg g = {sp.Poly(g, W).degree()}; "
              f"nullities: (B,F) {d}, (A,E) {e}, D {len(ker1)}; "
              f"{len(conds)} conditions in {len(params)} parameters", flush=True)
    return params, conds, envF, Kf


def emit_ms(path, p, g, params, conds, env, variant="real", seed=0):
    """Write the collapsed parameter system for msolve, sanitised and validated."""
    import random
    syms = list(params) + [W]
    names = [sp.sstr(s) for s in params] + ["w"]
    gauge = [redW(env["c_8_16"] - 1, g, p)]
    polys = [c for _, c in conds if sp.expand(c) != 0] + gauge
    gp = sp.Poly(g, W)
    if gp.degree() > 0:
        polys.append(sp.expand(g))
    pt = None
    if variant == "mutant":
        rnd = random.Random(seed)
        pt = {s: rnd.randrange(0, p) for s in params}
        if gp.degree() == 1:
            root = (-int(sp.Poly(g, W).all_coeffs()[1])
                    * pow(int(sp.Poly(g, W).all_coeffs()[0]), p - 2, p)) % p
        else:
            root = rnd.randrange(0, p)
        pt[W] = root
    lines = []
    for e in polys:
        pe = sp.Poly(sp.expand(e), *syms)
        terms = []
        for mono, coef in zip(pe.monoms(), pe.coeffs()):
            cc = sp.Rational(coef)
            v = (int(cc.p) % p) * pow(int(cc.q) % p, p - 2, p) % p
            if v == 0:
                continue
            terms.append("*".join([str(v)] +
                                  [f"{names[i]}^{a}" if a > 1 else names[i]
                                   for i, a in enumerate(mono) if a]))
        s = " + ".join(terms) if terms else "0"
        if pt is not None:
            val = sp.Rational(pe.eval([sp.Integer(pt[x]) for x in syms]))
            v = (int(val.p) % p) * pow(int(val.q) % p, p - 2, p) % p
            if v:
                s = s + " + " + str((-v) % p)
        lines.append(s)
    nzexpr = redW(env["d_12_24"], g, p)
    pe = sp.Poly(sp.expand(nzexpr), *syms)
    tt = []
    for mono, coef in zip(pe.monoms(), pe.coeffs()):
        cc = sp.Rational(coef)
        v = (int(cc.p) % p) * pow(int(cc.q) % p, p - 2, p) % p
        if v:
            tt.append("*".join([str(v)] + [f"{names[i]}^{a}" if a > 1 else names[i]
                                           for i, a in enumerate(mono) if a]))
    if tt:
        lines.append("sat*(" + " + ".join(tt) + ") + " + str((-1) % p))
    allnames = names + ["sat"]
    if variant == "pin":
        lines += [f"{names[0]} + {(-1) % p}", f"{names[0]} + {(-2) % p}"]
    # expand the single parenthesised saturation product, then sanitise
    flat = []
    for L in lines:
        if L.startswith("sat*("):
            inner = L[len("sat*("):L.rindex(")")]
            rest = L[L.rindex(")") + 1:]
            flat.append(" + ".join("sat*" + t.strip() for t in inner.split(" + "))
                        + rest)
        else:
            flat.append(L)
    flat = MF.sanitize_lines(flat, p)
    with open(path, "w") as fh:
        fh.write(",".join(allnames) + "\n")
        fh.write(f"{p}\n")
        fh.write(",\n".join(flat) + "\n")
    probs = MF.validate(path)
    if probs:
        raise SystemExit(f"{path}: msolve-input hazards remain: {probs[:5]}")
    return path, allnames, len(flat), pt
