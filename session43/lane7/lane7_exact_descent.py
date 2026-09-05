#!/usr/bin/env python3
"""EXACT graded descent with one-step lookahead, on nondegenerate Newton strata.

Level k has unknown blocks P_{px-k}, Q_{qx-k} and equations in weighted degree
g = px+qx-1-d-k; k runs all the way to g=0, so the levels past k=qx are the
residual rows with no unknowns at all (the "E2=E1=0, E0=1" rows).

Key structural fact used here: the level-k matrix A_k depends only on the two
top forms, and the level-(k+1) right-hand side is AFFINE in the level-k
unknowns.  So appending the level-(k+1) consistency conditions to level k keeps
every level linear, and the descent is exact rather than a random walk.  The one
genuinely nonlinear step is level 1 -> 2, where both blocks are unknown at once
and the obstruction is a system of quadrics (handled in lane7_obstruction.py).
"""
from __future__ import annotations

import json
import sys

import numpy as np
import sympy as sp

from lane7_descent import Descent, wdeg
from lane7_lib import TEMPLATES, poly_pow, replay, solve_mod
from lane7_obstruction import find_points, left_nullspace, level_system

P_MAIN = 1000003


def known_term(des, P, Q, k):
    """sum_{0<i<k} [P_{px-i}, Q_{qx-k+i}] -- everything already determined."""
    tpl, p = des.tpl, des.p
    out = {}
    for i in range(1, k):
        a, b = tpl.px - i, tpl.qx - (k - i)
        if a < 0 or b < 0:
            continue
        A, B = P.get(a), Q.get(b)
        if not A or not B:
            continue
        for m, c in des.bracket_block(A, B).items():
            out[m] = (out.get(m, 0) + c) % p
    return out


def rhs_vector(des, P, Q, k, rows, ridx):
    p = des.p
    b = np.zeros(len(rows), dtype=np.int64)
    known = known_term(des, P, Q, k)
    for m, c in known.items():
        if m in ridx:
            b[ridx[m]] = (b[ridx[m]] - c) % p
        elif c % p:
            return None            # a known term outside the row set: inconsistent
    g = des.tpl.px + des.tpl.qx - 1 - des.d - k
    if g == 0 and (0, 0) in ridx:
        b[ridx[(0, 0)]] = (b[ridx[(0, 0)]] + 1) % p
    elif g == 0:
        return None                # constant row unreachable => [P,Q]=1 impossible
    return b


def rows_for(des, k, Ptop, Qtop):
    A, rows, ridx, up, uq, g = level_system(des, k, Ptop, Qtop)
    if g == 0 and (0, 0) not in ridx:
        rows = rows + [(0, 0)]
        ridx = dict(ridx)
        ridx[(0, 0)] = len(rows) - 1
        A = np.concatenate([A, np.zeros((1, A.shape[1]), dtype=np.int64)])
    return A, rows, ridx, up, uq, g


def run_exact(des: Descent, lam, mu, hc, rng, level1_point=None, verbose=True):
    tpl, p, d = des.tpl, des.p, des.d
    # h must be WEIGHTED-homogeneous of weighted degree d (weights (1,d)):
    # the only monomials of weighted degree d are y and x^d.
    h = {(0, 1): 1}
    if hc[-1] % p:
        h[(des.d if hasattr(des, 'd') else d, 0)] = hc[-1] % p
    Ptop = {m: (lam * c) % p for m, c in poly_pow(h, tpl.py, p).items()}
    Qtop = {m: (mu * c) % p for m, c in poly_pow(h, tpl.qy, p).items()}
    P = {tpl.px: Ptop}
    Q = {tpl.qx: Qtop}
    kmax = tpl.px + tpl.qx - 1 - d
    log = []
    for k in range(1, kmax + 1):
        A, rows, ridx, up, uq, g = rows_for(des, k, Ptop, Qtop)
        b = rhs_vector(des, P, Q, k, rows, ridx)
        if b is None:
            return None, None, {"failed_level": k, "g": g,
                                "reason": "rhs outside row space"}, log
        if k == 1 and level1_point is not None:
            z = level1_point
        else:
            # one-step lookahead: level k+1 consistency is affine in these unknowns
            extraA, extrab = None, None
            if k + 1 <= kmax and A.shape[1]:
                An, rn, rin, upn, uqn, gn = rows_for(des, k + 1, Ptop, Qtop)
                L = left_nullspace(An, p)
                if len(L):
                    base = _look_rhs(des, P, Q, k, up, uq, np.zeros(A.shape[1], np.int64),
                                     k + 1, rn, rin)
                    cols = []
                    for c in range(A.shape[1]):
                        e = np.zeros(A.shape[1], dtype=np.int64)
                        e[c] = 1
                        v = _look_rhs(des, P, Q, k, up, uq, e, k + 1, rn, rin)
                        cols.append((v - base) % p)
                    M = np.stack(cols, axis=1) % p
                    extraA = (L @ M) % p
                    extrab = (-(L @ base)) % p
            if extraA is not None and len(extraA):
                Acomb = np.concatenate([A, extraA])
                bcomb = np.concatenate([b, extrab])
            else:
                Acomb, bcomb = A, b
            sol = solve_mod(Acomb, bcomb, p)
            if not sol["consistent"]:
                bare = solve_mod(A, b, p)
                return None, None, {"failed_level": k, "g": g,
                                    "reason": "inconsistent (with lookahead)",
                                    "consistent_without_lookahead": bare["consistent"],
                                    "bare_nullity": int(bare["nullity"]),
                                    "n_lookahead_rows": int(len(extraA)),
                                    "rows": len(rows), "cols": int(A.shape[1])}, log
            z = sol["particular"].copy()
            if sol["kernel"] is not None and len(sol["kernel"]):
                z = (z + rng.integers(0, p, size=len(sol["kernel"])) @ sol["kernel"]) % p
            log.append({"k": k, "g": g, "rows": len(rows), "cols": int(A.shape[1]),
                        "nullity_with_lookahead": int(sol["nullity"])})
        if A.shape[1] == 0 and not solve_mod(A, b, p)["consistent"]:
            return None, None, {"failed_level": k, "g": g,
                                "reason": "residual row violated"}, log
        for c, m in enumerate(up):
            if z[c] % p:
                P.setdefault(tpl.px - k, {})[m] = int(z[c] % p)
        for c0, m in enumerate(uq):
            if z[len(up) + c0] % p:
                Q.setdefault(tpl.qx - k, {})[m] = int(z[len(up) + c0] % p)
    Pf, Qf = {}, {}
    for blk in P.values():
        for m, c in blk.items():
            Pf[m] = (Pf.get(m, 0) + c) % p
    for blk in Q.values():
        for m, c in blk.items():
            Qf[m] = (Qf.get(m, 0) + c) % p
    return ({m: c for m, c in Pf.items() if c}, {m: c for m, c in Qf.items() if c},
            None, log)


def _look_rhs(des, P, Q, k, up, uq, z, kn, rows_n, ridx_n):
    """b_{kn} evaluated with the level-k blocks set from z."""
    tpl, p = des.tpl, des.p
    P2 = dict(P)
    Q2 = dict(Q)
    P2[tpl.px - k] = {m: int(z[c] % p) for c, m in enumerate(up) if z[c] % p}
    Q2[tpl.qx - k] = {m: int(z[len(up) + c0] % p) for c0, m in enumerate(uq)
                      if z[len(up) + c0] % p}
    b = np.zeros(len(rows_n), dtype=np.int64)
    for m, c in known_term(des, P2, Q2, kn).items():
        if m in ridx_n:
            b[ridx_n[m]] = (b[ridx_n[m]] - c) % p
    g = tpl.px + tpl.qx - 1 - des.d - kn
    if g == 0 and (0, 0) in ridx_n:
        b[ridx_n[(0, 0)]] = (b[ridx_n[(0, 0)]] + 1) % p
    return b


def level1_points(des, lam, mu, hc, p, n_slice_options=(3, 2, 4, 1), want=1):
    """Solve the level-1/level-2 quadratic obstruction exactly, return F_p points."""
    from lane7_obstruction import analyse_template  # noqa: F401  (kept for parity)
    tpl = des.tpl
    # h must be WEIGHTED-homogeneous of weighted degree d (weights (1,d)):
    # the only monomials of weighted degree d are y and x^d.
    h = {(0, 1): 1}
    if hc[-1] % p:
        h[(des.d if hasattr(des, 'd') else d, 0)] = hc[-1] % p
    Ptop = {m: (lam * c) % p for m, c in poly_pow(h, tpl.py, p).items()}
    Qtop = {m: (mu * c) % p for m, c in poly_pow(h, tpl.qy, p).items()}
    A1, rows1, ridx1, up1, uq1, g1 = rows_for(des, 1, Ptop, Qtop)
    s1 = solve_mod(A1, np.zeros(len(rows1), dtype=np.int64), p)
    K1 = s1["kernel"]
    nt = len(K1)
    A2, rows2, ridx2, up2, uq2, g2 = rows_for(des, 2, Ptop, Qtop)
    L = left_nullspace(A2, p)
    ts = sp.symbols(f"t0:{nt}")
    Pblk, Qblk = {}, {}
    for c, m in enumerate(up1):
        e = sum(int(K1[i, c]) * ts[i] for i in range(nt))
        if e != 0:
            Pblk[m] = e
    for c0, m in enumerate(uq1):
        c = len(up1) + c0
        e = sum(int(K1[i, c]) * ts[i] for i in range(nt))
        if e != 0:
            Qblk[m] = e
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
        if e != 0:
            quads.append(sp.Poly(e, *ts, modulus=p).as_expr())
    pts = []
    for ns in n_slice_options:
        if ns >= nt:
            continue
        pts = find_points(quads, ts, p, tries=60, n_slice=ns, want=want)
        if pts:
            break
    out = []
    for pt in pts:
        tv = np.array([pt.get(str(v), 0) for v in ts], dtype=np.int64)
        out.append((K1.T @ tv) % p if len(K1) else np.zeros(A1.shape[1], np.int64))
    return out, len(quads), nt, [str(q)[:120] for q in quads[:3]]


def main():
    p = P_MAIN
    names = sys.argv[1:] or ["t44", "ribbon12"]
    res = {}
    for name in names:
        tpl = TEMPLATES[name]
        des = Descent(tpl, p)
        des.levels = tpl.px + tpl.qx - des.d          # k = 0 .. px+qx-1-d
        rng = np.random.default_rng(31)
        entry = {"template": name, "kmax": tpl.px + tpl.qx - 1 - des.d, "runs": []}
        for trial in range(3):
            lam = int(rng.integers(1, p))
            mu = int(rng.integers(1, p))
            hc = [int(rng.integers(0, p)) for _ in range(des.d - 1)] + \
                 [int(rng.integers(1, p))]
            pts, nq, nt, qsample = level1_points(des, lam, mu, hc, p, want=20)
            run = {"lam": lam, "mu": mu, "n_level2_quadrics": nq,
                   "level1_nullity": nt, "level2_fp_points_found": len(pts),
                   "quadric_sample": qsample}
            if not pts:
                run["result"] = "no F_p point on the level-2 obstruction variety found"
                entry["runs"].append(run)
                continue
            errs = []
            P = Q = None
            for pt in pts:
                P, Q, err, log = run_exact(des, lam, mu, hc, rng, level1_point=pt)
                errs.append(err)
                if err is None:
                    break
            run["descent_log"] = log
            run["n_points_tried"] = len(errs)
            run["death_levels"] = sorted({(e["failed_level"], e["g"]) for e in errs if e})
            run["death_detail"] = errs[0]
            if err is not None:
                run["result"] = "descent died at every level-2 point tried"
                run["error"] = errs[0]
            else:
                rp = replay(P, Q, p)
                run["result"] = "DESCENT COMPLETED"
                run["replay_bracket_is_one"] = rp["bracket_is_one"]
                run["values"] = {k: rp[k] for k in ("P00", "P10", "Q00", "Q10")}
                run["P"] = {str(k): v for k, v in P.items()}
                run["Q"] = {str(k): v for k, v in Q.items()}
            entry["runs"].append(run)
            print(json.dumps(run, indent=1, default=str)[:2500], flush=True)
        res[name] = entry
        print(f"=== {name}: " +
              json.dumps([r["result"] for r in entry["runs"]]), flush=True)
    with open("lane7_exact_descent.json", "w") as fh:
        json.dump(res, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
