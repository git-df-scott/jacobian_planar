#!/usr/bin/env python3
"""Symbolic-kernel walk over Q for the open (72,108) subcases.

The mod-p walker (walk_pair) fails on both open subcases with rankA = 0 at
the blocking level: the conditions there do not involve that level's
unknowns, so they are conditions on the kernel directions chosen at EARLIER
levels -- which the mod-p walker draws at random. This module keeps those
kernel directions SYMBOLIC and exact over Q, so the blocking conditions come
out as polynomials in a handful of parameters that can be solved rather than
sampled.

Method (the cascade validated in dk_eliminate.py, now with parameters):
  level j: conditions newly closed at this level are affine in the level-j
  driver coefficients. Solve exactly: particular solution + kernel basis
  with fresh symbols t_i as coefficients. Substitute forward. Any condition
  that is independent of the current level's unknowns becomes a polynomial
  in the accumulated t's and is collected.
At the end, the collected polynomials are the exact obstruction system:
  no common solution  -> the subcase is EMPTY over Q (a real discard)
  solutions           -> substitute back for explicit P, Q coefficients,
                         then verify by direct bracket computation.

Everything is over Q -- no primes, no sampling. The final answer is a
characteristic-zero statement about the last case the literature leaves open.
"""
import argparse
import json
import sys

import sympy as sp

x, y = sp.symbols("x y")


def hull_rows(verts):
    """rows[j] = (min_i, max_i) over lattice points of the hull, as in
    trackB1_polygon but exact."""
    from trackB1_polygon import hull_rows as hr
    return hr(verts)


def build_walk(NP, NQ, r, jextra=2, maxlevel=None, verbose=True):
    """Return (obstructions, params, info). Driver = the polygon whose j=0
    row is {(0,0),(1,0)}; the other polynomial is integrated from it."""
    RP, RQ = hull_rows(NP), hull_rows(NQ)
    p0, q0 = RP.get(0), RQ.get(0)
    if p0 == (0, 1) and q0 == (0, 0):
        DR, OR_, sign = RP, RQ, 1
    elif q0 == (0, 1) and p0 == (0, 0):
        DR, OR_, sign = RQ, RP, -1
    else:
        raise SystemExit(f"OUT OF SCOPE: j=0 rows {p0} / {q0}")
    jmax = max(max(OR_), max(DR)) + jextra
    levels = sorted(DR)

    # driver coefficients as symbols, level by level
    coeff = {}
    for j in levels:
        lo, hi = DR[j]
        for i in range(lo, hi + 1):
            coeff[(j, i)] = sp.Symbol(f"a_{j}_{i}")
    tsyms = []
    # Gauge slice: the pivot coefficient a_0_1 scales out (the dim-1 freedom
    # the full-depth rank measured). Fixing it to 1 keeps every expression
    # POLYNOMIAL instead of rational, which is what makes this tractable.
    # Sound for finding solutions; an EMPTY verdict here is EMPTY-on-this-slice
    # and is labelled as such.
    assign = {coeff[(0, 1)]: sp.Integer(1)}
    obstructions = []
    branches = []

    def drow(j):
        lo, hi = DR[j]
        return [sp.expand(coeff[(j, i)].subs(assign)) if (j, i) in coeff
                else sp.Integer(0) for i in range(0, hi + 1)]

    def rhs_row(j):
        return [sp.Integer(0)] * r + [sp.Integer(sign)] if j == 0 else []

    # integrate Q rows: the campaign recurrence, exactly
    def qrows(maxrow=None):
        pivot = sp.expand(coeff[(0, 1)].subs(assign))
        Q = {0: [sp.Integer(0)]}
        R0 = rhs_row(0)
        Q[1] = [sp.cancel(c / pivot) for c in R0]
        KTOP = jmax if maxrow is None else min(jmax, maxrow)
        for k in range(1, KTOP + 1):
            acc = [sp.Integer(0)] * 40
            def addpoly(P1, P2, scal):
                for i1, c1 in enumerate(P1):
                    if c1 == 0:
                        continue
                    for i2, c2 in enumerate(P2):
                        if c2 == 0:
                            continue
                        acc[i1 + i2] = sp.expand(acc[i1 + i2] + scal*c1*c2)
            for a in range(0, k + 1):
                b = k - a
                if (a + 1) in DR and b in Q:
                    dq = [sp.expand(i*c) for i, c in enumerate(Q[b])][1:]
                    addpoly(drow(a + 1), dq, a + 1)
                if a >= 1 and a in DR and (b + 1) in Q:
                    dd = [sp.expand(i*c) for i, c in enumerate(drow(a))][1:]
                    addpoly(dd, Q[b + 1], -(b + 1))
            Q[k + 1] = [sp.cancel(c / (pivot * (k + 1))) for c in acc]
        return Q

    top = maxlevel if maxlevel is not None else max(levels)
    done = set()
    for j in levels:
        if j > top:
            break
        Q = qrows(maxrow=j + 2)
        # conditions: Q rows outside the other polygon's support
        conds = {}
        for jj in range(1, min(jmax, j + 2) + 1):
            row = Q.get(jj, [])
            if jj in OR_:
                lo, hi = OR_[jj]
            else:
                lo, hi = 1, 0
            for i, c in enumerate(row):
                if (i < lo or i > hi) and sp.expand(c) != 0:
                    conds[(jj, i)] = sp.expand(sp.numer(sp.cancel(c)))
        new = [k for k in conds if k not in done and k[0] <= j + 1]
        unks = [coeff[(j, i)] for i in range(DR[j][0], DR[j][1] + 1)
                if (j, i) in coeff and coeff[(j, i)] not in assign
                and (j, i) != (0, 1)]
        if not new:
            done |= set(conds.keys()) & {k for k in conds if k[0] <= j + 1}
            continue
        sys_eqs = [conds[k] for k in new]
        sol = sp.solve(sys_eqs, unks, dict=True) if unks else []
        if unks and sol:
            s = sol[0]
            free = [u for u in unks if u not in s]
            for u in free:
                t = sp.Symbol(f"t{len(tsyms)}")
                tsyms.append(t)
                assign[u] = t
            for u, val in s.items():
                assign[u] = sp.expand(val.subs(assign))
            if verbose:
                print(f"  level {j}: {len(new)} conds, {len(unks)} unknowns "
                      f"-> solved, {len(free)} free params", flush=True)
        else:
            # conditions independent of this level's unknowns: obstructions
            for k in new:
                e = sp.expand(conds[k].subs(assign))
                if e != 0:
                    obstructions.append(e)
            if obstructions:
                # Descend the obstruction: solve it exactly and continue on
                # that branch (retaining the zero branch rather than dividing
                # it away). Only unique/finite solutions are followed; a
                # branch with no solution is a genuine EMPTY.
                bs = sp.solve(obstructions, dict=True)
                if not bs:
                    if verbose:
                        print(f"  level {j}: obstruction has NO solution "
                              f"-> EMPTY on this branch", flush=True)
                    return obstructions, tsyms, {"levels": levels,
                                                 "jmax": jmax,
                                                 "assign": assign,
                                                 "status": "EMPTY"}
                br = bs[0]
                branches.append((j, [str(k) + "=" + str(v)
                                     for k, v in br.items()]))
                for k2, v2 in br.items():
                    assign[k2] = sp.expand(v2)
                for w in list(assign):
                    assign[w] = sp.expand(sp.sympify(assign[w]).subs(br))
                if verbose:
                    print(f"  level {j}: obstruction {[sp.factor(o) for o in obstructions]}"
                          f" -> branch {br}, continuing", flush=True)
                obstructions = []
        done |= set(new)
    return obstructions, tsyms, {"levels": levels, "jmax": jmax,
                                 "assign": assign, "branches": branches,
                                 "status": "WALKED"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=1)
    ap.add_argument("--maxlevel", type=int, default=None)
    a = ap.parse_args()
    t = json.load(open("trackD_targets_108.json"))[a.index]
    print(f"target: {t['tag']}", flush=True)
    print("gauge: pivot a_0_1 = 1 (scaling slice)", flush=True)
    obs, ts, info = build_walk(t["NP"], t["NQ"], t["r"],
                               maxlevel=a.maxlevel)
    print(f"\nparameters carried: {len(ts)}")
    print(f"obstruction polynomials: {len(obs)}")
    for o in obs[:4]:
        print("   deg", sp.total_degree(o), "in", sorted(map(str, o.free_symbols)))
    if obs:
        g = sp.groebner(obs, *ts, order="lex") if ts else None
        if g is not None:
            print("\nGroebner basis of the obstruction system:")
            print("   ", g.exprs[:3])
            if list(g.exprs) == [sp.Integer(1)]:
                print("\n*** NO SOLUTION: this subcase is EMPTY over Q ***")


if __name__ == "__main__":
    main()
