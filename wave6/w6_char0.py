#!/usr/bin/env python3
"""Characteristic-ZERO attempt on case (1).  The step that modular runs cannot do.

WHY THIS IS THE PIECE THAT MATTERS
----------------------------------
Agreement at many primes is evidence, not proof.  The precise gap: if the
system had a solution over C it would have one over Qbar, and that solution
reduces to a solution modulo all but FINITELY many primes -- so emptiness at a
GOOD prime would settle it, but we cannot certify which primes are good without
extra work.  Two ways to close it:

  (a) a Nullstellensatz certificate over Q, verified by exact expansion --
      a proof that trusts no solver (scoped in CERTIFICATE_ROUTE.md; degree 1
      is 46,978 unknowns and out of reach here);
  (b) run the elimination and the solver in characteristic ZERO.  An EMPTY
      verdict there is a characteristic-zero statement directly.

This script does (b): the same forced chain, but over Q with exact Fraction
arithmetic, exported with cleared denominators for msolve in characteristic 0.

HONEST COST
The chain over Q densifies in BOTH the number of terms and the SIZE of the
coefficients, so the export is capped.  A shallower reduction with a solvable
char-0 Gröbner beats a deeper one that cannot be ingested.
"""
import sys, os, json
from fractions import Fraction
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_forced_chain import load, subs_zero, subs_linear
from w6_forced_chain2 import gcd_mono, div_mono

ROOT = '/home/user/jacobian_planar'


def write_ms_q(path, eqs, varlist, nonzero):
    """msolve input in characteristic 0: integer coefficients, '0' on line 2."""
    live = [t for t in eqs if t]
    vs = sorted(varlist)
    body, maxcoef = [], 0
    for t in live:
        den = 1
        for c in t.values():
            den = den * c.denominator // gcd(den, c.denominator)
        parts = []
        for m, c in t.items():
            n = int(c * den)
            maxcoef = max(maxcoef, abs(n))
            parts.append("*".join([str(n)] + [f"{v}^{e}" if e > 1 else v
                                              for v, e in m]))
        body.append("+".join(parts).replace("+-", "-"))
    if nonzero:
        vs = vs + ['zzq']
        body.append("*".join(['zzq'] + sorted(nonzero)) + "-1")
    # same symbol guard that caught the false [-1]
    import re
    used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    leak = sorted(used - set(vs))
    assert not leak, f"REFUSING to write {path}: undeclared variables {leak[:8]}"
    open(path, 'w').write(",".join(vs) + "\n0\n" + ",\n".join(body) + "\n")
    return len(body), len(vs), maxcoef


def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 60000
    V, eqs, nonzero0 = load()
    nonzero = set(nonzero0)
    zeros, solved = set(), {}
    print(f"char-0 chain: {len(eqs)} equations, {len(V)} variables, term cap {cap}")
    for rnd in range(1, 2000):
        eqs = subs_zero(eqs, zeros)
        div = 0
        for i, t in enumerate(eqs):
            if not t or len(t) == 1:
                continue
            g = gcd_mono(t)
            ok = {v: e for v, e in g.items() if v in nonzero}
            if ok:
                eqs[i] = div_mono(t, ok); div += 1
        if div:
            continue
        nz, contra = set(), None
        for i, t in enumerate(eqs):
            if len(t) != 1:
                continue
            (mono, coef), = t.items()
            if not mono:
                contra = f"eq{i}: nonzero constant {coef} = 0"; break
            free = [v for v, _ in mono if v not in nonzero]
            if not free:
                contra = f"eq{i}: {mono}=0 with every factor required nonzero"; break
            if len(free) == 1 and free[0] not in zeros:
                nz.add(free[0])
        if contra or (nz & nonzero):
            print(f"*** CONTRADICTION over Q *** {contra or sorted(nz & nonzero)}")
            print("case (1) is EMPTY in characteristic zero, by exact substitution.")
            return 2
        if nz:
            zeros |= nz; continue
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
                if any(dict(m3).get(v, 0) > 1 for t3 in eqs for m3 in t3):
                    continue
                cand.append((len(t), i, v, c))
        if not cand:
            print("fixed point"); break
        cand.sort()
        _, i, v, c = cand[0]
        rhs = {m2: -c2 / c for m2, c2 in eqs[i].items()
               if not (len(m2) == 1 and m2[0] == (v, 1))}
        eqs = subs_linear(eqs, v, rhs); eqs[i] = {}
        if v in nonzero:
            nonzero.discard(v)
        solved[v] = rhs
        tot = sum(len(t) for t in eqs)
        if tot >= cap:
            print(f"  stopping at term cap: {tot} terms after {len(solved)} pivots")
            break
    rem = sorted(set(V) - zeros - set(solved))
    path = os.path.join(ROOT, f'wave6/pentseed/char0_{len(rem)}v.ms')
    ne, nv, mx = write_ms_q(path, eqs, rem, nonzero)
    print(f"  exported {ne} equations, {nv} variables, "
          f"{os.path.getsize(path)/1e6:.2f} MB, largest |coefficient| ~ 10^{len(str(mx))-1}")
    print(f"  -> {path}")
    print("  symbol guard passed (no undeclared variable)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
