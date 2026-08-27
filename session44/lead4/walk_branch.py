#!/usr/bin/env python3
"""Full branching descent over Q for the open (72,108) subcases.

Refines walk_sym: at every obstruction ALL solution branches are retained
and explored (never divide a factor away without keeping its zero branch),
and after the driver levels are exhausted the FULL condition set (every row
up to jmax, not just those closed level-by-level) is checked.

Outcomes per branch:
  EMPTY      an obstruction with no solution, or a leftover nonzero condition
             that no remaining freedom can fix
  VERTEX     a coefficient required nonzero (a polygon vertex) forced to 0
  CANDIDATE  all conditions satisfied -> explicit coefficients; must then be
             verified by direct bracket computation before any claim

Gauge: pivot a_0_1 = 1 (scaling slice), kept to kdeep expressions polynomial.
"""
import argparse
import json
import sys

import sympy as sp

from walk_sym import hull_rows




MODP = None


def _red(e):
    """Reduce rational coefficients mod MODP (identity when MODP is None).

    The descent's algebra is unchanged; only the coefficient ring changes.
    Rational-coefficient growth is what stalls the exact walk, and mod p each
    coefficient is a single small integer. A modular run is a SEARCH device:
    an EMPTY here is emptiness mod p only, and any candidate must be lifted
    and re-verified exactly before it means anything.
    """
    e = sp.expand(e)
    if MODP is None:
        return e
    if not e.free_symbols:
        r = sp.Rational(e)
        return sp.Integer((r.p * pow(int(r.q), MODP - 2, MODP)) % MODP)
    out = 0
    for mono, c in e.as_coefficients_dict().items():
        r = sp.Rational(c)
        cc = (r.p * pow(int(r.q), MODP - 2, MODP)) % MODP
        if cc:
            out += sp.Integer(cc) * mono
    return sp.expand(out)

def branch_solve(e, unks):
    """Solve one condition e = 0, returning a LIST of substitution dicts --
    one per factor (every zero branch retained). None means unsatisfiable."""
    e = sp.expand(e)
    if e == 0:
        return [{}]
    if not e.free_symbols:
        return None                      # nonzero constant: dead
    out = []
    for base, _mult in sp.factor_list(e)[1]:
        vs = sorted(base.free_symbols, key=str)
        if not vs:
            continue
        pick = None
        for v in vs:
            if v in unks and sp.degree(base, v) == 1:
                pick = v
                break
        if pick is None:
            for v in vs:
                if sp.degree(base, v) == 1:
                    pick = v
                    break
        if pick is not None:
            c1 = sp.expand(sp.Poly(base, pick).coeff_monomial(pick))
            c0 = sp.expand(base - c1 * pick)
            if c1.free_symbols:
                # keep both: c1 = 0 branch, and the solved branch
                out.append({})           # c1=0 handled by other factors/levels
            out.append({pick: sp.cancel(-c0 / c1)})
        else:
            v = vs[0]
            for rt in sp.roots(sp.Poly(base, v)):
                out.append({v: rt})
    seen, uniq = set(), []
    for d in out:
        key = tuple(sorted((str(k), str(v)) for k, v in d.items()))
        if key not in seen:
            seen.add(key)
            uniq.append(d)
    return uniq or None

def analyse(NP, NQ, r, maxbranch=40, verbose=True):
    RP, RQ = hull_rows(NP), hull_rows(NQ)
    p0, q0 = RP.get(0), RQ.get(0)
    if p0 == (0, 1) and q0 == (0, 0):
        DR, OR_, sign, drv_verts = RP, RQ, 1, NP
    elif q0 == (0, 1) and p0 == (0, 0):
        DR, OR_, sign, drv_verts = RQ, RP, -1, NQ
    else:
        raise SystemExit("OUT OF SCOPE")
    jmax = max(max(OR_), max(DR)) + 2
    levels = sorted(DR)
    coeff = {(j, i): sp.Symbol(f"a_{j}_{i}")
             for j in levels for i in range(DR[j][0], DR[j][1] + 1)}
    required = {coeff[(j, i)] for (i, j) in drv_verts if (j, i) in coeff
                and (i, j) != (0, 0)}

    def qrows(assign, maxrow):
        pivot = sp.Integer(1)
        Q = {0: [sp.Integer(0)]}
        R0 = ([sp.Integer(0)] * r + [sp.Integer(sign)])
        Q[1] = list(R0)
        for k in range(1, min(jmax, maxrow) + 1):
            acc = [sp.Integer(0)] * 60
            def addp(A, B, sc):
                for i1, c1 in enumerate(A):
                    if c1 == 0:
                        continue
                    for i2, c2 in enumerate(B):
                        if c2 == 0:
                            continue
                        acc[i1 + i2] = _red(acc[i1 + i2] + sc * c1 * c2)
            def drow(jj):
                if jj not in DR:
                    return []
                lo, hi = DR[jj]
                return [sp.expand(coeff[(jj, i)].subs(assign))
                        if (jj, i) in coeff else sp.Integer(0)
                        for i in range(0, hi + 1)]
            for a in range(0, k + 1):
                b = k - a
                if (a + 1) in DR and b in Q:
                    addp(drow(a + 1),
                         [sp.expand(i * c) for i, c in enumerate(Q[b])][1:],
                         a + 1)
                if a >= 1 and a in DR and (b + 1) in Q:
                    addp([sp.expand(i * c) for i, c in enumerate(drow(a))][1:],
                         Q[b + 1], -(b + 1))
            Q[k + 1] = [_red(c / (k + 1)) for c in acc]
        return Q

    def conds(assign, upto):
        Q = qrows(assign, upto + 1)
        out = {}
        for jj in range(1, min(jmax, upto + 1) + 1):
            row = Q.get(jj, [])
            lo, hi = OR_.get(jj, (1, 0))
            for i, c in enumerate(row):
                if i < lo or i > hi:
                    e = _red(c)
                    if e != 0:
                        out[(jj, i)] = e
        return out

    results = []
    stack = [({coeff[(0, 1)]: sp.Integer(1)}, [], 0)]
    while stack and len(results) < maxbranch:
        assign, hist, start = stack.pop()
        dead = None
        for j in levels:
            if j < start:
                continue
            C = conds(assign, j + 1)
            unks = [coeff[(j, i)] for i in range(DR[j][0], DR[j][1] + 1)
                    if coeff[(j, i)] not in assign]
            eqs = [v for k, v in C.items() if k[0] <= j + 1]
            eqs = [_red(e) for e in eqs if _red(e) != 0]
            if not eqs:
                continue
            sols = None
            for e in eqs:
                got = branch_solve(e, unks)
                if got is None:
                    sols = None
                    break
                if any(g for g in got):
                    sols = got
                    break
                sols = [{}]
            if not sols:
                dead = f"level {j}: {len(eqs)} condition(s), no solution"
                break
            if len(sols) > 1:
                for extra in sols[1:]:
                    a2 = dict(assign)
                    a2.update({k: sp.expand(v) for k, v in extra.items()})
                    stack.append((a2, hist + [f"L{j}:{extra}"], j))
            s0 = sols[0]
            bad = [k for k in s0 if k in required and sp.expand(s0[k]) == 0]
            if bad:
                dead = f"level {j}: required vertex {bad} forced to 0"
                break
            assign = dict(assign)
            assign.update({k: _red(v) for k, v in s0.items()})
            if s0:
                hist = hist + [f"L{j}:{ {str(k): str(v) for k,v in s0.items()} }"]
        if dead:
            results.append(("EMPTY", dead, hist))
            if verbose:
                print(f"  branch -> EMPTY ({dead})", flush=True)
            continue
        left = conds(assign, jmax)
        left = {k: v for k, v in left.items() if sp.expand(v) != 0}
        if not left:
            results.append(("CANDIDATE", assign, hist))
            if verbose:
                print("  branch -> ALL CONDITIONS SATISFIED (candidate)",
                      flush=True)
        else:
            freev = sorted({s for v in left.values() for s in v.free_symbols},
                           key=str)
            sols = sp.solve(list(left.values()), freev, dict=True) if freev \
                else []
            if not sols:
                results.append(("EMPTY", f"final: {len(left)} conditions "
                                f"unsatisfiable", hist))
                if verbose:
                    print(f"  branch -> EMPTY (final {len(left)} conds)",
                          flush=True)
            else:
                results.append(("CANDIDATE-FINAL", (assign, sols[0]), hist))
                if verbose:
                    print(f"  branch -> candidate after solving "
                          f"{len(left)} final conditions", flush=True)
    return results, {"levels": levels, "jmax": jmax, "required": required}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=1)
    a = ap.parse_args()
    t = json.load(open("trackD_targets_108.json"))[a.index]
    print(f"target: {t['tag']}")
    print("gauge: pivot a_0_1 = 1 (scaling slice)\n", flush=True)
    res, info = analyse(t["NP"], t["NQ"], t["r"])
    print(f"\nbranches explored: {len(res)}")
    from collections import Counter
    print(Counter(r[0] for r in res))
    for kind, data, hist in res:
        if kind.startswith("CANDIDATE"):
            print("\n*** CANDIDATE BRANCH ***")
            print("  history:", hist[:6])


if __name__ == "__main__":
    main()
