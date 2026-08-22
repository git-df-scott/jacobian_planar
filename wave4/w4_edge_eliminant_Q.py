"""
Case (2), w=-4 block: the eliminant over Q by multi-modular reconstruction.

WHY MULTI-MODULAR.  The exact char-0 solve is the expensive part; the mod-p
solve is seconds.  The eliminant of the block (with the chart d_3_3 = 1, the
gauge d_2_1 = 1 and the vertex conditions saturated) is a single univariate
polynomial over Q of degree 5 -- msolve's rational parametrisation gives its
reduction at every prime.  So it is reconstructed here by CRT plus rational
reconstruction of the six coefficients.

WHAT MAKES IT A RESULT AND NOT A GUESS.  Reconstruction is verified at primes
that were NOT used to build it: the reconstructed rational polynomial is reduced
at each held-out prime and must equal the eliminant msolve computes there
independently.  A reconstruction that fails a held-out prime is reported as
NOT-RECONSTRUCTED, never rounded into an answer.

CONTROLS
  E1  every prime used satisfies p = 1 (mod 3);
  E2  every prime gives the SAME eliminant degree (a prime that did not would be
      a bad prime and is dropped, loudly);
  E3  POSITIVE: the reconstruction reproduces the eliminant at >= 3 held-out
      primes;
  E4  NEGATIVE: a deliberately corrupted coefficient FAILS the held-out check,
      so E3 is not vacuous.
"""

import os
import sys
from fractions import Fraction

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_c2_residual as RS
import w4_run as RUN

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def eliminant_mod(p, chart="one", tmpdir="/tmp"):
    ms = os.path.join(tmpdir, f"elimQ_{chart}_{p}.ms")
    RS.export_w4(p, chart, ms)
    r = RUN.run_msolve(ms, ms[:-3] + ".out", timeout=600, threads=1)
    if r["verdict"] != "NONEMPTY-PARAMETRIZATION":
        return None, r["verdict"]
    rur = RS.parse_rur(ms[:-3] + ".out")
    return [c % p for c in rur["elim"]], "ok"


def crt(rs, ms):
    from functools import reduce
    M = reduce(lambda a, b: a * b, ms)
    x = 0
    for r, m in zip(rs, ms):
        Mi = M // m
        x = (x + r * Mi * pow(Mi, -1, m)) % M
    return x, M


def ratrec(a, m):
    from math import isqrt, gcd
    bound = isqrt(m // 2)
    r0, r1, s0, s1 = m, a % m, 0, 1
    while r1 > bound:
        if r1 == 0:
            return None
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound or gcd(abs(r1), abs(s1)) != 1:
        return None
    return Fraction(r1 if s1 > 0 else -r1, abs(s1))


def main(nbuild=90, nhold=6, chart="one"):
    print("=" * 78)
    print(f"case (2) w=-4 eliminant over Q, chart d_3_3 = {1 if chart=='one' else 0}")
    print("=" * 78)
    primes = []
    n = 1000000
    while len(primes) < nbuild + nhold:
        n += 1
        if n % 3 == 1 and sp.isprime(n):
            primes.append(n)
    check("E1 every prime used satisfies p = 1 (mod 3)",
          all(p % 3 == 1 for p in primes), f"{len(primes)} primes")
    elim, bad = {}, []
    for p in primes:
        e, why = eliminant_mod(p, chart)
        if e is None:
            bad.append((p, why))
        else:
            elim[p] = e
    degs = {p: len(e) - 1 for p, e in elim.items()}
    common = max(set(degs.values()), key=list(degs.values()).count) if degs else None
    good = [p for p in elim if degs[p] == common]
    check("E2 all usable primes agree on the eliminant degree",
          len(good) == len(elim) and not bad,
          f"degree {common} at {len(good)} primes; dropped {bad}; "
          f"degrees {sorted(set(degs.values()))}")
    hold = good[-nhold:]
    pool = good[:-nhold]

    def reduces_to(poly_coeffs, p):
        out = []
        for c in poly_coeffs:
            c = Fraction(c)
            out.append((c.numerator % p) * pow(c.denominator % p, p - 2, p) % p)
        return out

    # ADAPTIVE: add primes until every coefficient reconstructs AND the result
    # reproduces the eliminant at primes that were not used to build it.
    coeffs, used, ok_all, okhold = None, 0, False, False
    for k in range(6, len(pool) + 1):
        build = pool[:k]
        cs, good_k = [], True
        for i in range(common + 1):
            x, M = crt([elim[p][i] for p in build], build)
            r = ratrec(x, M)
            if r is None:
                good_k = False
                break
            cs.append(r)
        if not good_k:
            continue
        if all(reduces_to(cs, p) == elim[p] for p in hold):
            coeffs, used, ok_all, okhold = cs, k, True, True
            break
    print(f"    reconstruction used {used} build primes; {len(hold)} held out")
    check("every coefficient reconstructed to a rational and the result is "
          "stable", ok_all, f"used {used} of {len(pool)} available build primes")
    if not ok_all:
        print("    NOT-RECONSTRUCTED at this prime budget -- recorded as such, "
              "not rounded into an answer")
        return 1
    w = sp.Symbol("w")
    f = sum(sp.Rational(c) * w ** i for i, c in enumerate(coeffs))
    print(f"    eliminant over Q (numerator sizes: "
          f"{[len(str(sp.Rational(c).p)) for c in coeffs]} digits): {sp.factor(f)}")

    okhold = all(reduces_to(coeffs, p) == elim[p] for p in hold)
    check(f"E3 POSITIVE: the reconstruction reproduces the eliminant at "
          f"{len(hold)} HELD-OUT primes", okhold, f"{hold}")
    bad_coeffs = list(coeffs)
    bad_coeffs[0] = bad_coeffs[0] + 1
    okbad = all(reduces_to(bad_coeffs, p) == elim[p] for p in hold)
    check("E4 NEGATIVE: a corrupted coefficient FAILS the held-out check",
          not okbad, "so E3 is not vacuous")

    fac = sp.factor_list(sp.Poly(f, w))
    print(f"    factorisation over Q: {[ (sp.sstr(b), m) for b, m in fac[1] ]}")
    print(f"    rational roots: {sp.ground_roots(sp.Poly(f, w))}")
    n_ = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n_}/{len(RESULTS)} checks passed")
    print("=" * 78)
    import json
    json.dump({"chart": chart, "degree": common,
               "coefficients": [str(c) for c in coeffs],
               "build_primes_used": used, "held_out_primes": hold,
               "factorisation": [[sp.sstr(b), int(m)] for b, m in fac[1]],
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "artifacts",
                                f"edge_eliminant_Q_{chart}.json"), "w"), indent=1)
    return 0 if n_ == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
