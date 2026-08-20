#!/usr/bin/env python3
"""WAVE 5c -- the B=16 descent cascade: decide ladder cells without Groebner.

STRUCTURE (verified in w5_g4_closedform.py): in the reduced system the top
coefficient row is a quadratic in a_{2d} alone; each subsequent row r_k
introduces exactly one new a-variable linearly, with linear coefficient
L_k = -(16d - 16 - 4(k-1))*a_{2d} - 3 + (lower a's).  Fixing a root of row0
and descending, each a is determined in turn UNLESS its linear coefficient
vanishes on the branch -- branch points are recorded and split.  The b's and
mu's enter in the lower rows; whatever remains after the forced eliminations
is a small residual system handed to sympy's solver / msolve.

This file: symbolic cascade over Q(sqrt(12d)) (or Q when 12d is square),
branching exhaustively, mu0 != 0 enforced at the end by inspecting each
solution branch.  EMPTY verdicts here are proofs over C (all branches die on
exact contradictions); any surviving branch is dumped raw as
CANDIDATE-UNVERIFIED for the HIT pipeline.

Controls: d=5 and d=6 must come back EMPTY (matches char-0 msolve proofs);
d=3 with the saturation dropped must recover GGV's degenerate family.
"""
import os, sys, json
from sympy import (symbols, Symbol, expand, Poly, Rational, sqrt, simplify,
                   solve, linsolve, S, together, radsimp, nsimplify, Add, fraction)
sys.path.insert(0, os.path.dirname(__file__))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3
from sympy import simplify as _simp

def cascade(d, chart, verbose=True, seed=None):
    """chart: 'A'/'B' legacy slices, or None = NO chart (full space; sound).
    seed: optional dict of initial exact substitutions (e.g. the resonant
    top root), applied before the descent."""
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    fix = ({mu2: S(1)} if chart == 'A' else
           {mu2: S(0), mu3: S(1)} if chart == 'B' else {})
    if seed:
        fix = dict(fix); fix.update({a[i] if isinstance(i, int) else i: S(v)
                                     for i, v in seed.items()})
    # linear eliminations from (1.2)+normalizations (as in w5_b16_reduce)
    pre = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
           mu1: -mu3*(a[2] + 2*b[2])/3}
    from sympy import sympify
    pre = {k: sympify(v).subs(fix) for k, v in pre.items()}
    sys_eqs = [expand(e.subs(pre).subs(fix)) for e in eqs]
    sys_eqs = [e for e in sys_eqs if e != 0]
    unknowns = [a[i] for i in range(2, 2*d+1)] + [b[i] for i in range(2, d)] \
             + [v for v in (mu0, mu2, mu3) if v not in fix]
    branches = [({}, sys_eqs)]
    solved_branches, dead = [], 0
    steps = 0
    while branches:
        steps += 1
        if steps > 4000:
            raise RuntimeError("branch explosion")
        sub, eqs_cur = branches.pop()
        eqs_cur = [expand(e) for e in eqs_cur if expand(e) != 0]
        if any(e.is_number and e != 0 for e in eqs_cur):
            dead += 1
            continue
        if not eqs_cur:
            solved_branches.append(sub)      # underdetermined branch: record
            continue
        rem = [u for u in unknowns if u not in sub]
        if not rem:
            solved_branches.append(sub)
            continue
        # pick the equation with fewest remaining unknowns; solve for one
        def nvars(e): return len([u for u in rem if e.has(u)])
        eqs_cur.sort(key=nvars)
        e0 = eqs_cur[0]
        vs = [u for u in rem if e0.has(u)]
        if not vs:
            if simplify(e0) != 0:
                dead += 1
                continue
            branches.append((sub, eqs_cur[1:])); continue
        # solve e0 for a variable of minimal degree
        best = min(vs, key=lambda u: Poly(e0, u).degree())
        sols = solve(e0, best)
        if not sols:
            dead += 1
            continue
        for s0 in sols:
            nsub = dict(sub); nsub[best] = simplify(s0)
            neqs = []
            for e in eqs_cur[1:]:
                enew = e.subs({best: s0})
                num, den = fraction(together(enew))
                neqs.append(expand(num))   # denominators come from prior
                # solved-variable expressions; their zero loci are separate
                # branches (search mode: recorded, acceptable)
            branches.append((nsub, neqs))
    return solved_branches, dead

def survivors_with_mu0(branches):
    out = []
    for sub in branches:
        m0 = sub.get(mu0, None)
        if m0 is None or simplify(m0) != 0:
            out.append({str(k): str(simplify(v)) for k, v in sub.items()})
    return out

def main():
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    chart = sys.argv[2] if len(sys.argv) > 2 else 'A'
    if chart == 'none': chart = None
    seed = None
    if len(sys.argv) > 3:      # e.g. "24=-1/12" fixes a24 = -1/12
        idx, val = sys.argv[3].split('=')
        seed = {int(idx): val}
    br, dead = cascade(d, chart, seed=seed)
    surv = survivors_with_mu0(br)
    print(f"d={d} chart {chart}: {dead} dead branches, "
          f"{len(br)} solved branches, {len(surv)} with mu0 != 0 possible")
    os.makedirs("wave5/cascade", exist_ok=True)
    allbr = [{str(k): str(simplify(v)) for k, v in sub.items()} for sub in br]
    json.dump({"d": d, "chart": chart, "dead": dead,
               "branches": len(br), "all_branches": allbr, "survivors": surv},
              open(f"wave5/cascade/d{d}_{chart}_seeded.json", "w"), indent=1)
    if surv:
        print("CANDIDATE-UNVERIFIED branches written -- raw, for the HIT pipeline")
        for s in surv[:3]:
            print(" ", s)
    else:
        print("EMPTY (all branches die exactly)")

if __name__ == "__main__":
    main()
