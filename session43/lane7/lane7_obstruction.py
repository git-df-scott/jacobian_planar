#!/usr/bin/env python3
"""Exact level-2 obstruction of the nondegenerate (4,6) Newton stratum.

At graded level k the unknown blocks P_{px-k}, Q_{qx-k} pair ONLY with the two
top forms, so the coefficient matrix A_k depends on (h, lam, mu) alone and the
right-hand side b_k depends on the choices made at earlier levels.  Level 1 is
therefore a fixed linear system; its solution space is an affine space of
dimension n1, and level 2 is consistent exactly when

    L_j . b_2(t) = 0   for every left-null functional L_j of A_2,

with b_2(t) = -[P_{px-1}(t), Q_{qx-1}(t)] QUADRATIC in the level-1 parameters t.
Random sampling of t cannot refute a positive-codimension solution locus, so we
form those quadrics exactly and decide the ideal with a Groebner basis over F_p.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import sympy as sp

from lane7_descent import Descent, wdeg
from lane7_lib import TEMPLATES, poly_pow, rref_mod, solve_mod

P_MAIN = 1000003


def level_system(des: Descent, k: int, Ptop, Qtop):
    """Matrix A_k and its row/column labelling (independent of earlier levels)."""
    tpl, p, d = des.tpl, des.p, des.d
    g = tpl.px + tpl.qx - 1 - d - k
    unknown_p = des.pblocks.get(tpl.px - k, [])
    unknown_q = des.qblocks.get(tpl.qx - k, [])
    rows = sorted({(i + kk - 1, j + ll - 1)
                   for (i, j) in list(Ptop) + unknown_p
                   for (kk, ll) in list(Qtop) + unknown_q})
    rows = [m for m in rows if m[0] >= 0 and m[1] >= 0 and wdeg(m, d) == g]
    # every monomial of weighted degree g that the bracket can reach
    ridx = {m: r for r, m in enumerate(rows)}
    A = np.zeros((len(rows), len(unknown_p) + len(unknown_q)), dtype=np.int64)
    for col, (i, j) in enumerate(unknown_p):
        for (kk, ll), cq in Qtop.items():
            mult = i * ll - j * kk
            if mult % p:
                t = (i + kk - 1, j + ll - 1)
                if t in ridx:
                    A[ridx[t], col] = (A[ridx[t], col] + mult * cq) % p
    for col0, (kk, ll) in enumerate(unknown_q):
        col = len(unknown_p) + col0
        for (i, j), cp in Ptop.items():
            mult = i * ll - j * kk
            if mult % p:
                t = (i + kk - 1, j + ll - 1)
                if t in ridx:
                    A[ridx[t], col] = (A[ridx[t], col] + mult * cp) % p
    return A, rows, ridx, unknown_p, unknown_q, g


def left_nullspace(A, p):
    m, n = A.shape
    aug = np.concatenate([A % p, np.eye(m, dtype=np.int64)], axis=1)
    rr, piv = rref_mod(aug, p)
    return np.array([rr[r, n:] for r in range(m) if all(rr[r, :n] % p == 0)],
                    dtype=np.int64)


def analyse_template(name, p, seed, verbose=True):
    tpl = TEMPLATES[name]
    des = Descent(tpl, p)
    rng = np.random.default_rng(seed)
    lam = int(rng.integers(1, p))
    mu = int(rng.integers(1, p))
    hc = [int(rng.integers(0, p)) for _ in range(des.d - 1)] + [int(rng.integers(1, p))]
    h = {(0, 1): 1}
    if hc[-1] % p:
        h[(des.d, 0)] = hc[-1] % p
    Ptop = {m: (lam * c) % p for m, c in poly_pow(h, tpl.py, p).items()}
    Qtop = {m: (mu * c) % p for m, c in poly_pow(h, tpl.qy, p).items()}
    info = {"template": name, "p": p, "lam": lam, "mu": mu, "h": {str(k): v for k, v in h.items()}}

    A1, rows1, ridx1, up1, uq1, g1 = level_system(des, 1, Ptop, Qtop)
    b1 = np.zeros(len(rows1), dtype=np.int64)
    s1 = solve_mod(A1, b1, p)
    info["level1"] = {"rows": len(rows1), "cols": A1.shape[1], "rank": s1["rank"],
                      "nullity": s1["nullity"], "consistent": s1["consistent"]}
    K1 = s1["kernel"]
    nt = len(K1)

    A2, rows2, ridx2, up2, uq2, g2 = level_system(des, 2, Ptop, Qtop)
    L = left_nullspace(A2, p)
    info["level2"] = {"rows": len(rows2), "cols": A2.shape[1],
                      "rank": int(np.linalg.matrix_rank(A2.astype(float))),
                      "n_obstruction_functionals": len(L)}
    if len(L) == 0:
        info["verdict"] = "level 2 imposes no condition (A_2 surjective)"
        return info

    ts = sp.symbols(f"t0:{nt}")
    # P_{px-1}, Q_{qx-1} as affine functions of t (particular solution is 0)
    Pblk, Qblk = {}, {}
    for col, m in enumerate(up1):
        expr = sum(int(K1[i, col]) * ts[i] for i in range(nt))
        if expr != 0:
            Pblk[m] = expr
    for col0, m in enumerate(uq1):
        col = len(up1) + col0
        expr = sum(int(K1[i, col]) * ts[i] for i in range(nt))
        if expr != 0:
            Qblk[m] = expr
    br = {}
    for (i, j), a in Pblk.items():
        for (kk, ll), b in Qblk.items():
            mult = i * ll - j * kk
            if mult % p:
                t = (i + kk - 1, j + ll - 1)
                br[t] = sp.expand(br.get(t, 0) + mult * a * b)
    b2 = [sp.expand(-br.get(m, 0)) for m in rows2]
    quads = []
    for Lj in L:
        e = sp.expand(sum(int(Lj[r]) * b2[r] for r in range(len(rows2))))
        e = sp.Poly(e, *ts, modulus=p).as_expr() if e != 0 else e
        if e != 0:
            quads.append(e)
    info["n_quadrics"] = len(quads)
    if not quads:
        info["verdict"] = "level 2 automatically consistent"
        return info
    if verbose:
        print(f"  {name}: {len(quads)} obstruction quadric(s) in {nt} parameters")
    G = sp.groebner(quads, *ts, order="grevlex", modulus=p)
    gens = list(G.exprs)
    info["groebner_is_unit_ideal"] = (len(gens) == 1 and gens[0] == 1)
    info["groebner_gens_sample"] = [str(g)[:200] for g in gens[:6]]
    info["n_groebner_gens"] = len(gens)
    if info["groebner_is_unit_ideal"]:
        info["verdict"] = ("EXACT: no level-1 choice whatsoever admits a level-2 "
                           "solution -- the nondegenerate stratum is EMPTY at level 2")
    else:
        info["verdict"] = ("level-2 solution locus is NONEMPTY as a variety of "
                           "positive codimension -- random sampling cannot see it")
        info["fp_points"] = find_points(quads, ts, p, tries=60)
    return info


def _red(expr, p):
    """Reduce a sympy expression's integer coefficients mod p (0 if all vanish)."""
    e = sp.expand(expr)
    if e.is_number:
        return sp.Integer(int(e) % p)
    try:
        return sp.Poly(e, *sorted(e.free_symbols, key=str), modulus=p).as_expr()
    except sp.PolynomialError:
        return e


def roots_mod(expr, var, p):
    """All F_p roots of a univariate polynomial, via factorisation mod p."""
    try:
        poly = sp.Poly(expr, var, modulus=p)
    except sp.PolynomialError:
        return []
    if poly.total_degree() <= 0:
        return []
    out = []
    for fac, _ in poly.factor_list()[1]:
        if fac.degree() == 1:
            a, b = fac.all_coeffs()
            out.append(int((-b) * pow(int(a), p - 2, p) % p))
    return sorted(set(out))


def find_points(quads, ts, p, tries=40, n_slice=2, want=1):
    """Explicit F_p points on the obstruction variety.

    Slice with random hyperplanes down to dimension 0, eliminate with a lex
    Groebner basis over F_p, and lift roots back.  Any point returned is
    verified by substitution.
    """
    rng = np.random.default_rng(17)
    found = []
    free_vars = list(ts)
    for _ in range(tries):
        vals = {v: int(rng.integers(0, p)) for v in free_vars[:n_slice]}
        rest = free_vars[n_slice:]
        eqs = [sp.expand(q.subs(vals)) for q in quads]
        eqs = [e for e in eqs if e != 0]
        if not eqs:
            continue
        try:
            G = sp.groebner(eqs, *rest, order="lex", modulus=p)
        except Exception:                                  # noqa: BLE001
            continue
        gens = list(G.exprs)
        if len(gens) == 1 and gens[0] == 1:
            continue
        uni = [g for g in gens if g.free_symbols <= {rest[-1]}]
        if not uni:
            continue
        rr = roots_mod(uni[0], rest[-1], p)
        for r0 in rr:
            if len(found) >= want:
                break
            sub = dict(vals)
            sub[rest[-1]] = r0
            eqs2 = [_red(sp.expand(q.subs(sub)), p) for q in quads]
            eqs2 = [e for e in eqs2 if e != 0]
            if not eqs2:
                found.append({str(k): int(v) for k, v in sub.items()})
                break
            try:
                G2 = sp.groebner(eqs2, *rest[:-1], order="lex", modulus=p)
            except Exception:                              # noqa: BLE001
                continue
            g2 = list(G2.exprs)
            if len(g2) == 1 and g2[0] == 1:
                continue
            uni2 = [g for g in g2 if g.free_symbols <= {rest[0]}]
            if not uni2:
                continue
            for r1 in roots_mod(uni2[0], rest[0], p):
                sub2 = dict(sub)
                sub2[rest[0]] = r1
                left = [v for v in rest[:-1] if v != rest[0]]
                eqs3 = [_red(sp.expand(q.subs(sub2)), p) for q in quads]
                eqs3 = [e for e in eqs3 if e != 0]
                if not eqs3:
                    found.append({str(k): int(v) for k, v in sub2.items()})
                    break
                if len(left) == 1:
                    for r2 in roots_mod(eqs3[0], left[0], p):
                        cand = dict(sub2)
                        cand[left[0]] = r2
                        if all(_red(sp.expand(q.subs(cand)), p) == 0 for q in quads):
                            found.append({str(k): int(v) for k, v in cand.items()})
                            break
            if len(found) >= want:
                break
        if len(found) >= want:
            break
    return found


def main():
    p = P_MAIN
    names = sys.argv[1:] or ["t44", "ribbon12", "t84"]
    out = {}
    for name in names:
        for seed in (1, 2, 3):
            key = f"{name}/seed{seed}"
            print(f"--- {key} ---", flush=True)
            try:
                out[key] = analyse_template(name, p, seed)
            except Exception as exc:                      # noqa: BLE001
                out[key] = {"error": repr(exc)}
            print(json.dumps(out[key], indent=1, default=str)[:1800], flush=True)
    with open("lane7_obstruction.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
