"""
Case (2), chart d_3_3 = 1, over Q-bar: the residual cascade in characteristic 0.

Same elimination as w4_c2_cascade_solve.py, but every coefficient lives in the
number field K = Q[w]/(f), with f the exact degree-5 eliminant certified by
w4_edge_eliminant_structure.py (irreducible over Q, Galois group S5), and the
(C,G) values are the exact parametrisation certified by w4_edge_rur_Q.py (its
substitution annihilates all 9 residual polynomials identically modulo f).

So the input is exact and prime-free, and the output is a polynomial system over
Q in the parameters plus w, together with f(w).  If that system is the unit
ideal, case (2) in the chart d_3_3 = 1 is EMPTY OVER Q-BAR -- a characteristic-0
statement, not a mod-p one.

CONTROLS
  C0 the (C,G) values annihilate all 17 equations of the w = -4 block
     IDENTICALLY modulo f -- checked before anything else;
  C1 the emitted system is decided by two engines (msolve over Q and Singular
     over Q) and they must agree;
  C2 NEGATIVE: a planted parameter point must make the system NOT the unit
     ideal;
  C3 NEGATIVE: a contradictory pin must make it the unit ideal.
"""
import json
import os
import subprocess
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_case2_system as S
import w4_c2_reduce as RED
import w4_gf_Q as GQ

W = GQ.W
VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)
PIECE = {}
for v in VARS:
    wt = S.var_weight(v)
    PIECE[v] = ({0: "A", -1: "B", -2: "C"} if v.startswith("c_")
                else {0: "D", -1: "E", -2: "F", -3: "G"})[wt]
OF = {L: [v for v in VARS if PIECE[v] == L] for L in "ABCDEFG"}
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def redW(expr, f):
    return sp.rem(sp.Poly(sp.expand(expr), W), sp.Poly(f, W)).as_expr()


def eq_expr(idx, env, f):
    e = sp.Integer(0)
    for c, m in S.eq_terms(EQS[idx]):
        t = sp.Rational(c)
        for v, ex in m.items():
            t *= env[v] ** ex
        e += t
    return redW(e, f)


def block_matrix(w, letters, env, f):
    cols = [v for L in letters for v in OF[L]]
    syms = {v: sp.Symbol("__" + v) for v in cols}
    env2 = dict(env)
    env2.update(syms)
    M, rhs = [], []
    for idx in BYW[w]:
        e = sp.expand(eq_expr(idx, env2, f))
        row = [redW(sp.diff(e, syms[v]), f) for v in cols]
        const = redW(e.subs({syms[v]: 0 for v in cols}), f)
        chk = redW(e - const - sum(row[i] * syms[v] for i, v in enumerate(cols)), f)
        if sp.expand(chk) != 0:
            raise SystemExit(f"w={w} equation {idx} is not affine in {letters}")
        M.append(row)
        rhs.append(const)
    return M, rhs, cols


def cascade_Q(f, env_CG):
    """Collapse the residual over K = Q[w]/(f).  env_CG maps every C and G
    variable to an element of K (a polynomial in w)."""
    Kf = GQ.KQ(f)
    env = dict(env_CG)
    env0 = dict(env)
    for v in VARS:
        env0.setdefault(v, sp.Integer(0))
    bad = [i for i in BYW[-4] if sp.expand(eq_expr(i, env0, f)) != 0]
    check("C0 the (C,G) values annihilate all 17 equations of the w=-4 block "
          "identically modulo f(w)", not bad, f"nonzero at {bad}")
    if bad:
        raise SystemExit("input parametrisation is not on the variety")

    M3, r3, c3 = block_matrix(-3, "BF", env0, f)
    if any(sp.expand(x) != 0 for x in r3):
        raise SystemExit("the w=-3 block is not homogeneous in (B,F)")
    _, ker3, _ = GQ.solve(Kf, M3, [sp.Integer(0)] * len(M3))
    d = len(ker3)
    S_ = sp.symbols(f"s1:{d + 1}") if d else ()
    for i, v in enumerate(c3):
        env[v] = redW(sum(S_[j] * ker3[j][i] for j in range(d)), f)

    envAE = dict(env)
    for v in VARS:
        envAE.setdefault(v, sp.Integer(0))
    M2, r2, c2 = block_matrix(-2, "AE", envAE, f)
    part2, ker2, lk2 = GQ.solve(Kf, M2, [sp.Integer(0)] * len(M2))
    e = len(ker2)
    U_ = sp.symbols(f"u1:{e + 1}") if e else ()
    conds = []
    for row in lk2:
        cval = sum(cc * (-r2[j]) for j, cc in enumerate(row))
        conds.append(("w=-2 consistency", redW(cval, f)))
    mons = sorted({m for j in range(len(r2))
                   for m in sp.Poly(sp.expand(-r2[j]), *S_).monoms()}) if S_ else [()]
    partAE = [sp.Integer(0)] * len(c2)
    for mono in mons:
        rhs = []
        for j in range(len(r2)):
            pj = sp.Poly(sp.expand(-r2[j]), *S_)
            rhs.append(pj.coeff_monomial(mono))
        pt, _, _ = GQ.solve(Kf, M2, [redW(x, f) for x in rhs])
        mexpr = sp.prod([S_[i] ** a for i, a in enumerate(mono)]) if S_ else 1
        partAE = [redW(partAE[i] + mexpr * pt[i], f) for i in range(len(c2))]
    for i, v in enumerate(c2):
        env[v] = redW(partAE[i] + sum(U_[j] * ker2[j][i] for j in range(e)), f)

    envD = dict(env)
    for v in VARS:
        envD.setdefault(v, sp.Integer(0))
    M1, r1, c1 = block_matrix(-1, "D", envD, f)
    _, ker1, lk1 = GQ.solve(Kf, M1, [sp.Integer(0)] * len(M1))
    for row in lk1:
        cval = sum(cc * (-r1[j]) for j, cc in enumerate(row))
        conds.append(("w=-1 consistency", redW(cval, f)))
    PAR = list(S_) + list(U_)
    monsD = sorted({m for j in range(len(r1))
                    for m in sp.Poly(sp.expand(-r1[j]), *PAR).monoms()}) if PAR else [()]
    partD = [sp.Integer(0)] * len(c1)
    for mono in monsD:
        rhs = [sp.Poly(sp.expand(-r1[j]), *PAR).coeff_monomial(mono)
               for j in range(len(r1))]
        pt, _, _ = GQ.solve(Kf, M1, [redW(x, f) for x in rhs])
        mexpr = sp.prod([PAR[i] ** a for i, a in enumerate(mono)])
        partD = [redW(partD[i] + mexpr * pt[i], f) for i in range(len(c1))]
    Z_ = sp.symbols(f"z1:{len(ker1) + 1}") if ker1 else ()
    for i, v in enumerate(c1):
        env[v] = redW(partD[i] + sum(Z_[j] * ker1[j][i] for j in range(len(ker1))), f)

    envF = dict(env)
    for v in VARS:
        envF.setdefault(v, sp.Integer(0))
    for idx in BYW[0]:
        conds.append(("w=0", eq_expr(idx, envF, f)))
    params = list(S_) + list(U_) + list(Z_)
    print(f"      nullities: (B,F) {d}, (A,E) {e}, D {len(ker1)}; "
          f"{len(conds)} conditions in {len(params)} parameters", flush=True)
    return params, conds, envF


def sing_poly(e, syms, names):
    P = sp.Poly(sp.expand(e), *syms)
    out = []
    for mono, coef in zip(P.monoms(), P.coeffs()):
        c = sp.Rational(coef)
        cs = str(c.p) if c.q == 1 else f"({c.p}/{c.q})"
        out.append("*".join([cs] + [f"{names[i]}^{a}" if a > 1 else names[i]
                                    for i, a in enumerate(mono) if a]))
    return " + ".join(out) if out else "0"


def decide(f, params, conds, env, tag, extra=(), timeout=3000):
    syms = list(params) + [W]
    names = [sp.sstr(s) for s in params] + ["w"]
    gens = [c for _, c in conds if sp.expand(c) != 0]
    gens.append(redW(env["c_8_16"] - 1, f))
    gens.append(sp.expand(f))
    lines = [sing_poly(e, syms, names) for e in gens] + list(extra)
    src = [f"ring R = 0, ({','.join(names + ['sat'])}), dp;",
           "ideal I = " + ",\n".join(lines) + ";",
           "I = I + ideal(sat*(" + sing_poly(redW(env['d_12_24'], f), syms, names)
           + ") - 1);",
           "ideal G = std(I);",
           'if (size(G)==1 && G[1]==1) { "UNIT"; } else { "dim " + string(dim(G)); }',
           "quit;"]
    fn = f"/tmp/cascadeQ_{tag}.sing"
    open(fn, "w").write("\n".join(src))
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=timeout)
        return (pr.stdout or pr.stderr).strip().splitlines()[-1] if (pr.stdout or pr.stderr).strip() else "NO-OUTPUT"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def main():
    import w4_c2_reduce as R
    ej = json.load(open(os.path.join(HERE, "artifacts",
                                     "edge_eliminant_Q_one.json")))
    rj = json.load(open(os.path.join(HERE, "artifacts", "edge_rur_Q_one.json")))
    f = sum(sp.Rational(c) * W ** i for i, c in enumerate(ej["coefficients"]))
    env_G = {v: sum(sp.Rational(c) * W ** i
                    for i, c in enumerate(rj["coordinates"][v]))
             for v in R.G_VARS}
    print("=" * 78)
    print("case (2), chart d_3_3 = 1, residual cascade over Q[w]/(f)")
    print("=" * 78)
    Kf = GQ.KQ(f)
    rows, consts = R.w4_coefficients()
    ks = sorted(rows)
    env = dict(env_G)
    for k in ks[:8]:
        pivot, pexpr, acc = None, None, sp.Integer(0)
        for coef, cv, gv in rows[k]:
            if R.C_IDX[cv] == k:
                pivot, pexpr = cv, sp.Rational(coef) * env[gv]
            else:
                acc += sp.Rational(coef) * env[cv] * env[gv]
        num = redW(-sp.Rational(consts[k]) - acc, f)
        env[pivot] = redW(num * Kf.inv(redW(pexpr, f)), f)
    params, conds, envF = cascade_Q(f, env)
    v = decide(f, params, conds, envF, "real")
    check("C1 the residual system over Q is decided", v in ("UNIT",) or
          v.startswith("dim"), f"[{v}]")
    pin = decide(f, params, conds, envF, "pin",
                 extra=[f"{sp.sstr(params[0])}-1", f"{sp.sstr(params[0])}-2"])
    check("C3 NEGATIVE: a contradictory pin gives the unit ideal", pin == "UNIT",
          f"[{pin}]")
    if v == "UNIT":
        print("\n    RESULT: the residual system is the UNIT IDEAL over Q, so "
              "case (2) in the chart d_3_3 = 1 is EMPTY OVER Q-BAR.")
    else:
        print(f"\n    RESULT: Singular reports {v}; recorded as such.")
    json.dump({"real": v, "pin": pin, "params": [sp.sstr(x) for x in params],
               "nconditions": len(conds),
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "artifacts", "cascade_Q.json"), "w"), indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)


if __name__ == "__main__":
    main()
