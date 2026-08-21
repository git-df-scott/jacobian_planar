#!/usr/bin/env python3
"""PENTAGON CASE (1) -- EXACT forced-substitution chain over Q.  No solver.

THE OPENING
-----------
The system contains SINGLE-MONOMIAL equations, e.g.
    eq0 :  c_1_0 * d_0_1 = 0
    eq20:  c_1_0 * d_1_1 = 0
and c_1_0 != 0 is one of the system's own nondegeneracy conditions.  A product
is zero and one factor is known nonzero, so the other factor is ZERO.  No
computation, no solver, no field choice -- a forced implication.

The campaign's linear reduction (w6_pent_lineloop.py) used "only total-degree-1
equations with constant coefficients", so it could not see these: they have
total degree 2.  The nondegeneracy conditions were being carried as a filter
applied at the END rather than as hypotheses used DURING reduction.

WHAT THIS DOES
  1. propagate zeros: any single-monomial equation whose factors are all known
     nonzero except one forces that one to zero;
  2. substitute zeros everywhere (drop every term containing a zeroed variable);
  3. solve any equation that has become linear in a single unknown, exactly
     over Q, and substitute that too;
  4. repeat to a fixed point.

EVERY step is an exact implication over Q given the stated nondegeneracy
conditions.  Nothing here is modular, numerical, or solver-mediated.

OUTCOMES
  CONTRADICTION -- some equation reduces to (nonzero constant) = 0, or a
     monomial in known-nonzero variables is forced to vanish.  That is a PROOF
     that case (1) is empty, checkable by re-reading the chain.
  REDUCTION -- a strictly smaller system, exported for whatever comes next.
"""
import json, os, sys
from fractions import Fraction
from collections import defaultdict

ROOT = '/home/user/jacobian_planar'
SRC = os.path.join(ROOT, 'campaign/audit_tracks/trackB1_param_system.json')


def load():
    D = json.load(open(SRC))
    eqs = []
    for e in D['equations']:
        terms = defaultdict(Fraction)
        for mono, co in e['terms']:
            key = tuple(sorted((str(v), int(x)) for v, x in mono))
            terms[key] += Fraction(int(co[0]), int(co[1]))
        eqs.append({k: v for k, v in terms.items() if v != 0})
    return list(D['variables']), eqs, list(D['nonzero'])


def subs_zero(eqs, zeros):
    """Drop every term containing a variable known to be zero."""
    out = []
    for t in eqs:
        nt = {m: c for m, c in t.items()
              if not any(v in zeros for v, _ in m)}
        out.append(nt)
    return out


def subs_linear(eqs, var, expr):
    """Replace `var` (degree 1 only) by the polynomial `expr` (dict mono->coef)."""
    out = []
    for t in eqs:
        nt = defaultdict(Fraction)
        for m, c in t.items():
            deg = dict(m).get(var, 0)
            if deg == 0:
                nt[m] += c
                continue
            if deg > 1:                      # keep it exact: only linear substitution
                nt[m] += c
                continue
            rest = tuple(sorted((v, e) for v, e in m if v != var))
            for m2, c2 in expr.items():
                merged = defaultdict(int)
                for v, e in rest:
                    merged[v] += e
                for v, e in m2:
                    merged[v] += e
                key = tuple(sorted((v, e) for v, e in merged.items() if e > 0))
                nt[key] += c * c2
        out.append({m: c for m, c in nt.items() if c != 0})
    return out


def main():
    V, eqs, nonzero = load()
    nonzero = set(nonzero)
    zeros, solved = set(), {}
    print(f"start: {len(eqs)} equations, {len(V)} variables")
    print(f"nondegeneracy (given by the system): {sorted(nonzero)}\n")

    for rnd in range(1, 400):
        eqs = subs_zero(eqs, zeros)
        new_zero, contra = set(), None

        # (1) single-monomial equations
        for i, t in enumerate(eqs):
            if len(t) != 1:
                continue
            (mono, coef), = t.items()
            if not mono:                              # nonzero constant = 0
                contra = f"eq{i}: constant {coef} = 0"
                break
            free = [v for v, _ in mono if v not in nonzero]
            if not free:
                contra = (f"eq{i}: monomial {mono} = 0 but every factor is "
                          f"required nonzero")
                break
            if len(free) == 1 and free[0] not in zeros:
                new_zero.add(free[0])
        if contra:
            print(f"round {rnd}: *** CONTRADICTION *** {contra}")
            print("\ncase (1) is EMPTY, by exact forced substitution over Q.")
            return 2

        # (2) GAUSS PIVOT: a variable v occurring in exactly one term of its
        # equation, as a bare constant*v, can be solved for as a POLYNOMIAL in
        # the others -- no denominator, exact over Q.  The campaign's linear
        # loop only allowed constant right-hand sides and so never made these.
        cand = []
        for i, t in enumerate(eqs):
            if not t:
                continue
            for m, c in t.items():
                if len(m) != 1 or m[0][1] != 1:
                    continue
                v = m[0][0]
                if v in zeros or v in solved or v in nonzero:
                    continue
                if any(v in dict(m2) for m2 in t if m2 != m):
                    continue                      # v must occur in ONE term only
                cand.append((len(t), i, v, c))
        cand.sort()                               # smallest equation first: least blow-up

        if new_zero:
            zeros |= new_zero
            print(f"round {rnd}: forced {len(new_zero)} variables to zero -> "
                  f"{sorted(new_zero)[:8]}{' ...' if len(new_zero) > 8 else ''}")
            continue
        if cand:
            _, i, v, c = cand[0]
            rhs = {m2: -c2 / c for m2, c2 in eqs[i].items()
                   if not (len(m2) == 1 and m2[0] == (v, 1))}
            before = sum(len(t) for t in eqs)
            eqs = subs_linear(eqs, v, rhs)
            eqs[i] = {}                            # the pivot equation is now spent
            after = sum(len(t) for t in eqs)
            solved[v] = rhs
            if rnd <= 6 or rnd % 20 == 0:
                print(f"round {rnd}: pivot {v} from eq{i} "
                      f"({len(rhs)} terms), total terms {before} -> {after}")
            if after > 6000000:
                print(f"round {rnd}: STOPPING -- term count {after} is blowing up")
                break
            continue
        print(f"round {rnd}: fixed point reached")
        break

    live = [t for t in eqs if t]
    triv = len(eqs) - len(live)
    remaining = sorted(set(V) - zeros - set(solved))
    print(f"\nFIXED POINT")
    print(f"  variables forced to zero : {len(zeros)}")
    print(f"  variables eliminated by polynomial pivot: {len(solved)}")
    print(f"  equations now trivial (0 = 0) : {triv}")
    print(f"  equations remaining : {len(live)}")
    print(f"  variables remaining : {len(remaining)}")
    if zeros:
        print(f"\n  zeros: {sorted(zeros)}")
    if solved:
        print(f"  eliminated by pivot: {len(solved)} -> {sorted(solved)[:14]}")
    bad = sorted(zeros & nonzero)
    if bad:
        print(f"\n*** CONTRADICTION: {bad} forced to zero but required nonzero ***")
        print("case (1) is EMPTY, by exact forced substitution over Q.")
        return 2
    out = os.path.join(ROOT, 'wave6/pentseed/forced_chain.json')
    json.dump({'zeros': sorted(zeros),
               'solved': {k: [str(v)] for k, v in solved.items()},
               'n_equations_live': len(live),
               'n_vars_remaining': len(remaining)}, open(out, 'w'), indent=1)
    print(f"\nwrote {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
