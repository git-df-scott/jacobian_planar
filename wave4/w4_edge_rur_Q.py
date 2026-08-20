"""
The case-(2) w=-4 block's RATIONAL PARAMETRISATION over Q, reconstructed and
then VERIFIED EXACTLY.

The eliminant over Q is already in hand (w4_edge_eliminant_Q.py): degree 5,
irreducible, Galois group S5.  msolve's parametrisation writes every coordinate
as a polynomial in the eliminant's variable w (its denominator for this system
is the constant 1), so the whole parametrisation is 11 polynomials of degree
<= 4 over Q -- 55 rational numbers.

Each is reconstructed by CRT + rational reconstruction across primes p = 1 (3),
exactly as the eliminant was.  What makes the result a RESULT rather than a
guess is not the reconstruction but the check that follows it:

    substituting the reconstructed coordinates into the 9 exact residual
    polynomials over Q and reducing modulo f(w) must give IDENTICALLY ZERO,

which is an exact identity in Q[w]/(f) and does not refer to any prime.  The
chart d_3_3 = 1 and the gauge d_2_1 = 1 must hold identically too.

CONTROLS
  R1 POSITIVE: all 9 residual polynomials vanish identically mod f(w);
  R2 POSITIVE: the chart and gauge equations hold identically mod f(w);
  R3 NEGATIVE: perturbing ONE reconstructed coefficient breaks R1, so R1 is not
     vacuous;
  R4 the eliminant used is the one certified by w4_edge_eliminant_structure.py.
"""
import json
import os
import sys
from fractions import Fraction
from functools import reduce

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_c2_reduce as RED
import w4_c2_residual as RS
import w4_run as RUN

W = sp.Symbol("w")
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def crt(rs, ms):
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


CACHE = {}


def _cache_path(chart):
    return os.path.join(HERE, "artifacts", f"rurQ_primes_{chart}.json")


def rur_at(p, chart="one"):
    """The mod-p parametrisation, cached on disk so diagnosis is cheap."""
    key = str(p)
    if key in CACHE:
        return CACHE[key]
    d = _rur_at(p, chart)
    CACHE[key] = d
    json.dump(CACHE, open(_cache_path(chart), "w"))
    return d


def _rur_at(p, chart="one"):
    ms = f"/tmp/rurQ_{chart}_{p}.ms"
    RS.export_w4(p, chart, ms)
    r = RUN.run_msolve(ms, ms[:-3] + ".out", timeout=900, threads=1)
    if r["verdict"] != "NONEMPTY-PARAMETRIZATION":
        return None
    rur = RS.parse_rur(ms[:-3] + ".out")
    vals, _ = RS.rur_values(rur)
    sign = None
    for s in (1, -1):
        ok, _ = RS.verify_rur(vals, s, rur, p, chart=chart,
                              gauge=RS.GAUGE_BY_CHART[chart])
        if ok:
            sign = s
            break
    if sign is None:
        return None
    return {"elim": [c % p for c in rur["elim"]],
            "coords": {v: [(sign * c) % p for c in vals[v]] for v in RED.G_VARS},
            "sign": sign}


def main(nbuild=60, chart="one"):
    print("=" * 78)
    print("the case-(2) w=-4 parametrisation over Q, reconstructed and verified")
    print("=" * 78)
    primes, n = [], 1000000
    while len(primes) < nbuild:
        n += 1
        if n % 3 == 1 and sp.isprime(n):
            primes.append(n)
    global CACHE
    import glob
    for c in [_cache_path(chart)] + sorted(glob.glob(
            os.path.join(HERE, "artifacts", f"rurQ_primes_{chart}_s*.json"))):
        if os.path.exists(c):
            CACHE.update({k: v for k, v in json.load(open(c)).items()
                          if v is not None})
    data = {}
    for p in primes:
        d = rur_at(p, chart)
        if d is not None and len(d["elim"]) == 6:
            data[p] = d
    print(f"    usable primes: {len(data)} of {len(primes)}, all = 1 (mod 3)")
    good = sorted(data)
    # the exact eliminant, already certified
    ej = json.load(open(os.path.join(HERE, "artifacts",
                                     "edge_eliminant_Q_one.json")))
    fcoeffs = [sp.Rational(c) for c in ej["coefficients"]]
    f = sp.Poly(sum(c * W ** i for i, c in enumerate(fcoeffs)), W)
    check("R4 the eliminant used is the certified degree-5 polynomial",
          f.degree() == 5 and f.is_irreducible, f"degree {f.degree()}")

    def rec(vec_of_lists, k, build):
        x, M = crt([data[p][k[0]][k[1]][j] if k[0] == "coords"
                    else data[p][k[0]][j] for p in build], build)
        return ratrec(x, M)

    # Reconstruct EVERY coefficient independently against the full prime set,
    # and report which ones fail, rather than stopping at the first.  A
    # coefficient that reconstructs against the first half of the primes must
    # reconstruct to the SAME rational against all of them -- that agreement is
    # what makes a reconstruction more than a guess (R0).
    half = good[:len(good) // 2]
    coords, failed, unstable, bits = {}, [], [], 0
    for v in RED.G_VARS:
        deg = max(len(data[p]["coords"][v]) for p in good) - 1
        cs = []
        for j in range(deg + 1):
            xs = [(data[p]["coords"][v][j] if j < len(data[p]["coords"][v])
                   else 0) for p in good]
            x, M = crt(xs, good)
            r = ratrec(x, M)
            xh, Mh = crt(xs[:len(half)], half)
            rh = ratrec(xh, Mh)
            if r is None:
                failed.append((v, j))
                cs.append(None)
                continue
            if rh is not None and rh != r:
                unstable.append((v, j))
            bits = max(bits, r.numerator.bit_length(),
                       r.denominator.bit_length())
            cs.append(r)
        coords[v] = cs
    ok_all = not failed
    build = good
    check("R0 POSITIVE: every coefficient that reconstructs at half the primes "
          "reconstructs to the same rational at all of them", not unstable,
          f"{len(unstable)} unstable of "
          f"{sum(len(c) for c in coords.values()) - len(failed)} reconstructed")
    print(f"    reconstruction used {len(build)} primes")
    check("every coordinate polynomial reconstructed to rationals", ok_all,
          f"{len(failed)} of {sum(len(c) for c in coords.values())} "
          f"coefficients did not reconstruct at "
          f"{len(good)} primes ({sum(p.bit_length() for p in good)} bits); "
          f"largest reconstructed coefficient {bits} bits; first failures "
          f"{failed[:5]}")
    if not ok_all:
        json.dump({"chart": chart, "primes": good, "status": "NOT-RECONSTRUCTED",
                   "failed_coefficients": [[v, j] for v, j in failed],
                   "unstable": [[v, j] for v, j in unstable],
                   "max_bits_reconstructed": bits,
                   "checks": [[a, b, c] for a, b, c in RESULTS]},
                  open(os.path.join(HERE, "artifacts",
                                    f"edge_rur_Q_{chart}.json"), "w"), indent=1)
        return 1

    env = {v: sum(sp.Rational(c) * W ** i for i, c in enumerate(coords[v]))
           for v in RED.G_VARS}

    def rem_f(e):
        return sp.rem(sp.Poly(sp.expand(e), W), f)

    polys, gs = RED.reduced_polys_Q()
    names = [str(s) for s in gs]
    sub = {gs[i]: env[names[i]] for i in range(len(names))}
    bad = []
    for k, e in enumerate(polys):
        if not rem_f(e.subs(sub)).is_zero:
            bad.append(k)
    check("R1 POSITIVE: all 9 residual polynomials vanish IDENTICALLY modulo "
          "f(w) at the reconstructed parametrisation -- an exact identity over Q",
          not bad, f"nonzero at {bad}")
    ok2 = rem_f(env["d_3_3"] - 1).is_zero and rem_f(env["d_2_1"] - 1).is_zero
    check("R2 POSITIVE: the chart d_3_3 = 1 and the gauge d_2_1 = 1 hold "
          "identically modulo f(w)", ok2)

    pert = dict(coords)
    v0 = RED.G_VARS[2]
    pert[v0] = list(coords[v0])
    pert[v0][0] = pert[v0][0] + 1
    env2 = {v: sum(sp.Rational(c) * W ** i for i, c in enumerate(pert[v]))
            for v in RED.G_VARS}
    sub2 = {gs[i]: env2[names[i]] for i in range(len(names))}
    bad2 = [k for k, e in enumerate(polys) if not rem_f(e.subs(sub2)).is_zero]
    check("R3 NEGATIVE: perturbing one reconstructed coefficient breaks R1",
          bool(bad2), f"{len(bad2)} of 9 residual polynomials now nonzero")

    out = {"chart": chart, "primes_used": len(build),
           "eliminant_degree": int(f.degree()),
           "coordinates": {v: [str(c) for c in coords[v]] for v in RED.G_VARS},
           "checks": [[a, b, c] for a, b, c in RESULTS]}
    json.dump(out, open(os.path.join(HERE, "artifacts",
                                     f"edge_rur_Q_{chart}.json"), "w"), indent=1)
    npass = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {npass}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 60))
