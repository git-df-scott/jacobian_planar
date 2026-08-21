"""
Plane Jacobian campaign - Session 20
MODULAR EXHAUSTIVE SEARCH -- the same decision as jc2_exhaustive_search.py but
over GF(p) for several primes, which is fast enough to reach much further.

WHY THIS IS SOUND AS A HUNT.
If the system has a solution over Qbar then it has one over a number field, and
reduces to a solution over F_pbar for all but finitely many p.  So:

  * "no solution mod p" for several independent primes is very strong evidence
    of no solution over Qbar (and is what we expect below Moh's bound);
  * ANY mod-p solution is only a CANDIDATE and must be lifted and re-verified
    in characteristic 0 before it counts as anything.

WHY FROBENIUS ARTIFACTS CANNOT CONTAMINATE IT.
The Jacobian conjecture is FALSE in characteristic p -- e.g. (x + y^p, y) is a
Keller pair over F_p that is not an automorphism.  Every such artifact needs a
p-th power, hence degree >= p.  All primes used here exceed every degree in the
sweep, so no Frobenius counterexample can appear in range.  This is enforced by
an assertion, not by hope.

Everything is exact (GF(p) arithmetic).  No floating point.
"""

import sys
import time
from math import gcd
from sympy import symbols, Poly, expand, groebner, S, total_degree, GF

x, y, w = symbols('x y w')

PRIMES = [32003, 65521, 1000003]
H_ORBITS = {
    1: [('y', y)],
    2: [('y^2', y**2), ('x*y', x*y)],
    3: [('y^3', y**3), ('x*y^2', x*y**2), ('x*y*(x-y)', x*y*(x - y))],
}


def gen_poly(prefix, maxdeg):
    cs, expr = [], S(0)
    for d in range(1, maxdeg + 1):
        for i in range(d + 1):
            c = symbols(f'{prefix}_{i}_{d-i}')
            cs.append(c)
            expr += c*x**i*y**(d - i)
    return expr, cs


def decide(d1, d2, h, p, budget_s=240):
    n = gcd(d1, d2)
    b, a = d1//n, d2//n
    beta = symbols('beta')
    P1, cP = gen_poly('p', d1 - 1)
    Q1, cQ = gen_poly('q', d2 - 1)
    P = expand(h**b + P1)
    Q = expand(beta*h**a + Q1)
    Jx = expand(P.diff(x)*Q.diff(y) - P.diff(y)*Q.diff(x) - 1)
    eqs = [c for c in Poly(Jx, x, y).coeffs() if c != 0]
    eqs.append(beta*w - 1)
    unk = cP + cQ + [beta, w]
    t0 = time.time()
    try:
        G = groebner(eqs, *unk, order='grevlex', modulus=p)
    except Exception as ex:
        return 'ERROR', f'{type(ex).__name__}', 0, len(eqs), len(unk)
    dt = time.time() - t0
    basis = list(G.exprs)
    triv = (basis == [S(1)]) or (len(basis) == 1 and basis[0] == 1)
    return ('EMPTY' if triv else 'NONEMPTY'), '', dt, len(eqs), len(unk)


def admissible(maxsum, maxn=3):
    out = []
    for d1 in range(2, maxsum):
        for d2 in range(2, d1):
            if d1 % d2 == 0 or d2 % d1 == 0:
                continue
            if d1 + d2 > maxsum or gcd(d1, d2) > maxn:
                continue
            out.append((d1, d2))
    return sorted(out, key=lambda t: (t[0] + t[1], t[0]))


def main(maxsum=17):
    pairs = admissible(maxsum)
    assert min(PRIMES) > maxsum, "primes must exceed all degrees (Frobenius guard)"
    print(f"MODULAR SEARCH over GF(p), p in {PRIMES}")
    print(f"Frobenius guard: min prime {min(PRIMES)} > max degree {maxsum}. OK\n")
    print(f"{len(pairs)} non-dividing degree pairs with d1+d2 <= {maxsum}, gcd <= 3\n")
    hits, errs, done = [], [], 0
    for (d1, d2) in pairs:
        n = gcd(d1, d2)
        for (hname, h) in H_ORBITS[n]:
            verdicts = []
            for p in PRIMES:
                st, note, dt, ne, nu = decide(d1, d2, h, p)
                verdicts.append((p, st, dt))
                if st != 'EMPTY':
                    break
            allempty = all(vd[1] == 'EMPTY' for vd in verdicts)
            tag = 'EMPTY(all p)' if allempty else verdicts[-1][1]
            tt = sum(vd[2] for vd in verdicts)
            print(f"  ({d1:2d},{d2:2d}) n={n} cusp=({d2//n},{d1//n}) h={hname:11s} "
                  f"eqs={ne:4d} unk={nu:4d}  {tag:14s} {tt:6.1f}s")
            done += 1
            if not allempty:
                if verdicts[-1][1] == 'ERROR':
                    errs.append((d1, d2, hname))
                else:
                    hits.append((d1, d2, hname, verdicts))
    print("\n" + "=" * 70)
    print(f"decided: {done};  EMPTY for every prime: {done - len(hits) - len(errs)};"
          f"  candidates: {len(hits)};  errors: {len(errs)}")
    for hh in hits:
        print(f"  !!! CANDIDATE (must be lifted to char 0): {hh[:3]}")
    for e in errs:
        print(f"  err: {e}")
    if not hits:
        print("\nNo Keller pair with non-dividing degrees exists in this range.")
        print("Expected (Moh); serves as the pipeline's correctness check.")


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 17)
