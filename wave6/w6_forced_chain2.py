#!/usr/bin/env python3
"""PENTAGON CASE (1) -- forced chain v2.  Exploit EVERY hypothesis.

v1 left two things on the table, both from being too conservative:

  (a) eq41 is  -1 + c_1_0 = 0,  i.e. c_1_0 = 1 EXACTLY -- a gauge
      normalisation sitting in plain sight.  v1's pivot rule skipped any
      variable listed as nondegenerate, so it refused to solve for c_1_0.
      Correct rule: DO eliminate it, and carry "value != 0" forward as the
      discharged form of the condition.  Here the value is 1, so the
      condition c_1_0 != 0 is discharged outright.

  (b) eq282 is  12*c_8_15*s_4_8^3 - 8*d_12_23*s_4_8^2 = 0, whose terms share
      the factor s_4_8^2 -- and s_4_8 != 0 is REQUIRED.  Dividing a common
      monomial factor out of an equation is sound whenever every variable in
      that factor is known nonzero, and it makes the equation strictly
      simpler.  v1 never looked for common factors at all.
      (eq278 gives the same relation via 57/38 = 3/2 -- an independent
      confirmation, and evidence the two are dependent.)

Rules, applied to a fixed point, cheapest first so the densifying pivots run
last:
  0. substitute variables already known to be constants / zero
  1. divide out common monomial factors all of whose variables are known
     nonzero
  2. single-monomial equation with exactly one non-nondegenerate factor
     -> that factor is ZERO
  3. polynomial pivot: a variable occurring as a bare constant*v in exactly
     one term of its equation is eliminated exactly over Q
Every step is an exact implication over Q under the stated hypotheses.

CONTRADICTION at any point = PROOF that case (1) is empty.
"""
import json, os, sys
from fractions import Fraction
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_forced_chain import load, subs_zero, subs_linear

ROOT = '/home/user/jacobian_planar'


def gcd_mono(t):
    it = iter(t); g = dict(next(it))
    for m in it:
        dm = dict(m)
        for v in list(g):
            if v not in dm:
                del g[v]
            else:
                g[v] = min(g[v], dm[v])
        if not g:
            break
    return g


def div_mono(t, g):
    out = {}
    for m, c in t.items():
        dm = defaultdict(int, dict(m))
        for v, e in g.items():
            dm[v] -= e
        out[tuple(sorted((v, e) for v, e in dm.items() if e > 0))] = c
    return out


def main():
    V, eqs, nonzero0 = load()
    nonzero = set(nonzero0)
    zeros, solved = set(), {}
    # branch control:  argv1 = "zero:VAR"  or  "nonzero:VAR"
    if len(sys.argv) > 1 and ':' in sys.argv[1]:
        kind, var = sys.argv[1].split(':', 1)
        if kind == 'zero':
            zeros.add(var); print(f"BRANCH: assuming {var} = 0")
        else:
            nonzero.add(var); print(f"BRANCH: assuming {var} != 0")
    discharged, branches = [], []
    print(f"start: {len(eqs)} equations, {len(V)} variables")
    print(f"nondegeneracy hypotheses: {sorted(nonzero)}\n")

    for rnd in range(1, 600):
        eqs = subs_zero(eqs, zeros)

        # --- 1. divide out common monomial factors known to be nonzero
        div = 0
        for i, t in enumerate(eqs):
            if not t or len(t) == 1:
                continue
            g = gcd_mono(t)
            if not g:
                continue
            ok = {v: e for v, e in g.items() if v in nonzero}
            rest = {v: e for v, e in g.items() if v not in nonzero}
            if ok:
                eqs[i] = div_mono(t, ok); div += 1
            if rest:
                branches.append((i, dict(rest)))
        if div:
            print(f"round {rnd}: divided a known-nonzero common factor out of "
                  f"{div} equations")
            continue

        # --- 2. contradictions and forced zeros from single monomials
        new_zero, contra = set(), None
        for i, t in enumerate(eqs):
            if len(t) != 1:
                continue
            (mono, coef), = t.items()
            if not mono:
                contra = f"eq{i}: nonzero constant {coef} = 0"
                break
            free = [v for v, _ in mono if v not in nonzero]
            if not free:
                contra = f"eq{i}: {mono} = 0 but every factor is required nonzero"
                break
            if len(free) == 1 and free[0] not in zeros:
                new_zero.add(free[0])
        if contra:
            print(f"round {rnd}: *** CONTRADICTION *** {contra}")
            print("\ncase (1) is EMPTY -- exact, over Q, no solver trusted.")
            return 2
        if new_zero & nonzero:
            print(f"round {rnd}: *** CONTRADICTION *** {sorted(new_zero & nonzero)} "
                  f"forced to zero but required nonzero")
            print("\ncase (1) is EMPTY -- exact, over Q, no solver trusted.")
            return 2
        if new_zero:
            zeros |= new_zero
            print(f"round {rnd}: forced to zero: {sorted(new_zero)}")
            continue

        # --- 3. polynomial pivots (nondegenerate variables NOW allowed)
        cand = []
        for i, t in enumerate(eqs):
            if not t:
                continue
            for m, c in t.items():
                if len(m) != 1 or m[0][1] != 1:
                    continue
                v = m[0][0]
                if v in zeros or v in solved:
                    continue
                if any(v in dict(m2) for m2 in t if m2 != m):
                    continue
                # prefer constant-valued pivots, then small equations
                isconst = len(t) == 2 and any(not m2 for m2 in t)
                cand.append((0 if isconst else 1, len(t), i, v, c))
        cand.sort()
        if not cand:
            print(f"round {rnd}: fixed point reached")
            break
        _, _, i, v, c = cand[0]
        rhs = {m2: -c2 / c for m2, c2 in eqs[i].items()
               if not (len(m2) == 1 and m2[0] == (v, 1))}
        if v in nonzero:
            if len(rhs) == 1 and () in rhs:
                if rhs[()] == 0:
                    print(f"round {rnd}: *** CONTRADICTION *** {v} = 0 but required nonzero")
                    return 2
                discharged.append((v, rhs[()]))
                nonzero.discard(v)
                print(f"round {rnd}: {v} = {rhs[()]}  -- nondegeneracy DISCHARGED")
            else:
                nonzero.discard(v)
                discharged.append((v, 'polynomial'))
        before = sum(len(t) for t in eqs)
        eqs = subs_linear(eqs, v, rhs); eqs[i] = {}
        after = sum(len(t) for t in eqs)
        solved[v] = rhs
        if rnd <= 8 or rnd % 25 == 0:
            print(f"round {rnd}: pivot {v} from eq{i} ({len(rhs)} terms), "
                  f"terms {before} -> {after}")
        if after > 1500000:
            print(f"round {rnd}: STOPPING -- term count {after} blowing up")
            break

    live = [t for t in eqs if t]
    print(f"\nFIXED POINT")
    print(f"  zeros: {len(zeros)} {sorted(zeros)}")
    print(f"  eliminated by pivot: {len(solved)}")
    print(f"  nondegeneracy discharged: {discharged}")
    print(f"  equations remaining: {len(live)}   variables remaining: "
          f"{len(set(V) - zeros - set(solved))}")
    if branches:
        seen = {}
        for i, r in branches:
            seen.update(r)
        print(f"  UNUSED case-splits available (common factors not known nonzero): "
              f"{sorted(seen)}")
    json.dump({'zeros': sorted(zeros), 'n_pivots': len(solved),
               'discharged': [[a, str(b)] for a, b in discharged],
               'n_live': len(live)},
              open(os.path.join(ROOT, 'wave6/pentseed/forced_chain2.json'), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
