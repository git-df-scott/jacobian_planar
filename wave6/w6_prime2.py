#!/usr/bin/env python3
"""Case (1) at SEVERAL primes, built from the exact char-0 source.

WHY NOT REUSE seed0_p1000003.ms
-------------------------------
That file is the campaign's seed-pinned export and exists at ONE prime; the
machinery that produced it is not reproducible here. So instead of pinning the
seed we reduce the exact char-0 system `trackB1_param_system.json` modulo each
prime ourselves and ask the question directly:

    does pentagon case (1) have an ADMISSIBLE solution mod p?

This is *stronger* than the seed-pinned question — it does not presuppose the
seed decomposition at all — and it is reproducible at any prime.

SOUNDNESS OF THE REDUCTION (why EMPTY is a real conclusion)
----------------------------------------------------------
Every chain step is an implication under the nondegeneracy hypotheses, so

    {admissible solutions of the original} SUBSET {solutions of the reduced}

hence **reduced EMPTY  =>  no admissible solution**. Note this direction holds
whatever extra saturation we add and whatever `nonzero` variables get pivoted
away: dropping a nondegeneracy condition only ADMITS more solutions, so an
empty result under weaker hypotheses is a stronger statement, never a weaker
one. It can never manufacture a false emptiness.

BUG CHECKS BUILT IN
  1. denominators: refuse any prime dividing a coefficient denominator;
  2. faithfulness: evaluate the exact system and its mod-p image at the same
     random point and require agreement (catches reduction errors);
  3. symbol guard: `write_ms` refuses to emit an undeclared variable
     (this is the bug that produced a false [-1] earlier tonight);
  4. planted control at the SAME prime through the SAME `chain_core`.

Usage:  python3 w6_prime2.py PRIME [control]
"""
import sys, os, json, random
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_chain_export import chain_core, write_ms, ROOT

SRC = os.path.join(ROOT, 'campaign/audit_tracks/trackB1_param_system.json')
CHECKPOINTS = [40000, 150000, 700000]


def load_exact():
    D = json.load(open(SRC))
    eqs = []
    for e in D['equations']:
        t = {}
        for mono, co in e['terms']:
            key = tuple(sorted((str(v), int(x)) for v, x in mono))
            t[key] = t.get(key, Fraction(0)) + Fraction(int(co[0]), int(co[1]))
        eqs.append({k: v for k, v in t.items() if v})
    return list(D['variables']), eqs, list(D['nonzero'])


def reduce_modp(eqs, p):
    out = []
    for t in eqs:
        nt = {}
        for m, c in t.items():
            assert c.denominator % p != 0, (
                f"BAD PRIME {p}: a coefficient denominator is divisible by it")
            v = c.numerator % p * pow(c.denominator % p, p - 2, p) % p
            if v:
                nt[m] = v
        out.append(nt)
    return out


def ev_exact(t, pt):
    s = Fraction(0)
    for m, c in t.items():
        term = c
        for v, e in m:
            term *= pt[v] ** e
        s += term
    return s


def ev_modp(t, pt, p):
    s = 0
    for m, c in t.items():
        term = c
        for v, e in m:
            term = term * pow(pt[v], e, p) % p
        s = (s + term) % p
    return s


def faithfulness_check(V, eqs_q, eqs_p, p, trials=3):
    """The mod-p image must agree with the exact system at random points."""
    rng = random.Random(90210 + p)
    for _ in range(trials):
        pt = {v: rng.randrange(1, p) for v in V}
        for i, (tq, tp) in enumerate(zip(eqs_q, eqs_p)):
            a = ev_exact(tq, {k: Fraction(x) for k, x in pt.items()})
            a = a.numerator % p * pow(a.denominator % p, p - 2, p) % p
            b = ev_modp(tp, pt, p)
            assert a == b, f"REDUCTION UNFAITHFUL at eq{i}, p={p}: {a} != {b}"
    return True


def main():
    p = int(sys.argv[1])
    control = len(sys.argv) > 2 and sys.argv[2] == 'control'
    V, eqs_q, nonzero = load_exact()
    eqs = reduce_modp(eqs_q, p)
    print(f"p = {p}: {len(eqs)} equations, {len(V)} variables, "
          f"nondegeneracy {sorted(nonzero)}")
    faithfulness_check(V, eqs_q, eqs, p)
    print(f"  [check 1] no denominator divisible by {p}: PASS")
    print(f"  [check 2] mod-p reduction agrees with the exact system "
          f"at random points: PASS")

    tag = f'p{p}_'
    if control:
        # PLANTED CONTROL at this same prime, through the same chain_core.
        rng = random.Random(777 + p)
        pt = {v: rng.randrange(1, p) for v in V}
        for t in eqs:
            val = ev_modp(t, pt, p)
            if val:
                t[()] = (t.get((), 0) - val) % p
        eqs = [{m: c for m, c in t.items() if c} for t in eqs]
        assert all(ev_modp(t, pt, p) == 0 for t in eqs), \
            "planting failed: the planted point is not a root"
        print(f"  [check 3] planted point (all coordinates nonzero) is an exact "
              f"root of the shifted system: PASS")
        tag = f'p{p}ctl_'

    res, zeros, solved, done = chain_core(V, eqs, p, set(nonzero),
                                          CHECKPOINTS, tag)
    if res is None:
        print("CONTRADICTION reached inside the chain (see above)")
        return 2
    rem = sorted(set(V) - zeros - set(solved))
    path = os.path.join(ROOT, f'wave6/pentseed/reduced_{tag}{len(rem)}v.ms')
    ne, nv = write_ms(path, res, rem, p, set(nonzero) - zeros - set(solved))
    print(f"  final: {ne} eq, {nv} vars, {os.path.getsize(path)/1e6:.1f} MB "
          f"-> {os.path.basename(path)}")
    print(f"  [check 4] symbol guard passed on every export "
          f"(write_ms asserts no undeclared variable)")
    print(f"\nexports for p={p}{' CONTROL' if control else ''}:")
    for pth, ne_, nv_ in done + [(path, ne, nv)]:
        print(f"  {nv_:4d} vars  {ne_:4d} eq  "
              f"{os.path.getsize(pth)/1e6:8.2f} MB  {os.path.basename(pth)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
