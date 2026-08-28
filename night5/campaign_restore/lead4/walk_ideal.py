#!/usr/bin/env python3
"""Ideal-reduction descent: no radicals, no branching by hand.

Why this exists. walk_sym solves each obstruction and substitutes the root,
so a quartic like a_3_2^4 - 9 a_3_2^2 a_6_3 + 27 a_6_3^2 = 0 injects
sqrt((3 - sqrt(-3)) a_6_3) into every later expression, and the nesting
compounds until sympy stalls (observed: stuck at level 14 for >13 minutes).
Yet that quartic only says a_6_3/a_3_2^2 = (3 +- sqrt(-3))/18 -- an element
of the fixed field Q(omega). The blow-up is a representation artefact.

The fix: never solve an obstruction. Keep it as a RELATION and reduce every
later expression modulo the ideal of accumulated relations. All arithmetic
stays polynomial with bounded degree, and no branch is ever discarded --
the ideal automatically carries every component at once, which also removes
the "I only followed bs[0]" weakness of walk_sym.

Verdicts:
  ideal contains 1        -> conditions are contradictory -> EMPTY (exact,
                             characteristic zero, all branches at once)
  ideal proper at the end -> its variety is the candidate set; a point of
                             it must then be lifted to original coordinates
                             and verified (Jacobian constant, honest
                             polynomials) before any claim.
"""
import argparse
import json
import sys

import sympy as sp

from walk_sym import hull_rows


def analyse(NP, NQ, r, maxlevel=None, verbose=True):
    RP, RQ = hull_rows(NP), hull_rows(NQ)
    p0, q0 = RP.get(0), RQ.get(0)
    if p0 == (0, 1) and q0 == (0, 0):
        DR, OR_, sign = RP, RQ, 1
    elif q0 == (0, 1) and p0 == (0, 0):
        DR, OR_, sign = RQ, RP, -1
    else:
        raise SystemExit("OUT OF SCOPE")
    jmax = max(max(OR_), max(DR)) + 2
    levels = sorted(DR)
    coeff = {(j, i): sp.Symbol(f"a_{j}_{i}")
             for j in levels for i in range(DR[j][0], DR[j][1] + 1)}
    allsyms = sorted(coeff.values(), key=str)

    assign = {coeff[(0, 1)]: sp.Integer(1)}     # scaling gauge
    relations = []                               # the accumulated ideal
    GB = None

    def reduce_mod(e):
        e = sp.expand(e)
        if GB is None or e == 0:
            return e
        try:
            return sp.expand(sp.reduced(e, GB, *allsyms)[1])
        except Exception:
            return e

    def rebuild():
        nonlocal GB
        if not relations:
            GB = None
            return False
        try:
            g = sp.groebner(relations, *allsyms, order="grevlex")
        except Exception:
            GB = None
            return False
        GB = list(g.exprs)
        return list(g.exprs) == [sp.Integer(1)]

    def qrows(maxrow):
        Q = {0: [sp.Integer(0)]}
        Q[1] = [sp.Integer(0)] * r + [sp.Integer(sign)]
        for k in range(1, min(jmax, maxrow) + 1):
            acc = [sp.Integer(0)] * 60

            def drow(jj):
                if jj not in DR:
                    return []
                lo, hi = DR[jj]
                return [reduce_mod(coeff[(jj, i)].subs(assign))
                        if (jj, i) in coeff else sp.Integer(0)
                        for i in range(0, hi + 1)]

            def addp(A, B, sc):
                for i1, c1 in enumerate(A):
                    if c1 == 0:
                        continue
                    for i2, c2 in enumerate(B):
                        if c2 == 0:
                            continue
                        acc[i1 + i2] = reduce_mod(acc[i1 + i2] + sc * c1 * c2)
            for a in range(0, k + 1):
                b = k - a
                if (a + 1) in DR and b in Q:
                    addp(drow(a + 1),
                         [sp.expand(i * c) for i, c in enumerate(Q[b])][1:],
                         a + 1)
                if a >= 1 and a in DR and (b + 1) in Q:
                    addp([sp.expand(i * c) for i, c in enumerate(drow(a))][1:],
                         Q[b + 1], -(b + 1))
            Q[k + 1] = [reduce_mod(c / (k + 1)) for c in acc]
        return Q

    top = maxlevel if maxlevel is not None else max(levels)
    done = set()
    for j in levels:
        if j > top:
            break
        Q = qrows(j + 2)
        conds = {}
        for jj in range(1, min(jmax, j + 2) + 1):
            row = Q.get(jj, [])
            lo, hi = OR_.get(jj, (1, 0))
            for i, c in enumerate(row):
                if (i < lo or i > hi):
                    e = reduce_mod(c)
                    if e != 0:
                        conds[(jj, i)] = e
        new = [k for k in conds if k not in done and k[0] <= j + 1]
        if not new:
            continue
        unks = [coeff[(j, i)] for i in range(DR[j][0], DR[j][1] + 1)
                if coeff[(j, i)] not in assign]
        solved = 0
        for key in new:
            e = reduce_mod(conds[key].subs(assign))
            if e == 0:
                continue
            hit = None
            for v in unks:
                if v in e.free_symbols and sp.degree(e, v) == 1:
                    c1 = sp.expand(sp.Poly(e, v).coeff_monomial(v))
                    if c1.is_number and c1 != 0:
                        hit = (v, sp.expand(-(e - c1 * v) / c1))
                        break
            if hit:
                assign[hit[0]] = reduce_mod(hit[1])
                for w in list(assign):
                    assign[w] = reduce_mod(sp.sympify(assign[w])
                                           .subs({hit[0]: assign[hit[0]]}))
                unks.remove(hit[0])
                solved += 1
            else:
                relations.append(sp.expand(sp.numer(sp.together(e))))
        done |= set(new)
        if relations:
            trivial = rebuild()
            if verbose:
                print(f"  level {j}: {len(new)} conds, {solved} solved, "
                      f"ideal has {len(relations)} relation(s)"
                      f"{' -> CONTAINS 1' if trivial else ''}", flush=True)
            if trivial:
                return "EMPTY", relations, assign
        elif verbose:
            print(f"  level {j}: {len(new)} conds, {solved} solved, "
                  f"ideal still trivial", flush=True)
    return "OPEN", relations, assign


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=1)
    ap.add_argument("--maxlevel", type=int, default=None)
    a = ap.parse_args()
    t = json.load(open("trackD_targets_108.json"))[a.index]
    print(f"target: {t['tag']}")
    print("gauge: a_0_1 = 1; method: ideal reduction (no radicals, all "
          "branches carried at once)\n", flush=True)
    v, rels, assign = analyse(t["NP"], t["NQ"], t["r"], maxlevel=a.maxlevel)
    print(f"\nverdict: {v}")
    print(f"relations in the ideal: {len(rels)}")
    for rr in rels[:5]:
        print("   ", sp.factor(rr))
    if v == "EMPTY":
        print("\n*** conditions are contradictory over Q -- subcase EMPTY ***")


if __name__ == "__main__":
    main()
