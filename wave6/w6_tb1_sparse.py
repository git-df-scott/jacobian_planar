#!/usr/bin/env python3
"""Probe the COORDINATE SUBSPACES that random sampling provably cannot hit.

The random probes all returned inconsistent, and the honest reading of that was
"consistency is a proper closed condition and random points miss proper closed
subvarieties by design". That reading cuts both ways: it says the random probe
was never capable of finding the solution locus, so its failure is weak
evidence. The natural closed subvarieties of an affine space are the coordinate
subspaces, and a random point is never sparse.

So probe sparse points deliberately. The saturation row
    zsat * c_1_0 * c_8_14 * d_12_21 * s_4_8 - 1
forces exactly four variables nonzero. Every OTHER coordinate is free to
vanish, and a solution sitting on such a subspace is fully admissible.

For each pattern: zero the chosen parameters, randomise the rest, and test
whether A(d,s) c = b(d,s) is consistent. Any hit is a genuine lead and is
verified by substitution into the original equation strings before it is
reported -- the same three artifact checks as w6_tb1_rank.py, whose recovery
path had a sign error that only a planted control caught.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import load, parse_poly, evalmono, rank_modp

SRC = os.environ.get('TB1_SRC',
      '/home/user/jacobian_planar/wave6/frontier/trackB1_sat_p1000003.ms')
FORCED_NONZERO = {'c_1_0', 'c_8_14', 'd_12_21', 's_4_8'}


def main():
    vs, p, body = load(SRC)
    C = sorted(v for v in vs if v.startswith('c_'))
    OTHER = sorted(v for v in vs if v not in set(C))
    assert set(C) | set(OTHER) == set(vs)
    cset = set(C); n = len(C)
    polys = [parse_poly(b, p) for b in body]
    lin = [i for i, q in enumerate(polys)
           if max((sum(e for v, e in m if v in cset) for m in q), default=0) <= 1]
    cidx = {v: j for j, v in enumerate(C)}
    S = sorted(v for v in vs if v.startswith('s_'))
    D = sorted(v for v in vs if v.startswith('d_'))
    print(f"{os.path.basename(SRC)}: p={p}, c-block {n}, d-block {len(D)}, s-block {S}")
    print(f"forced nonzero by saturation: {sorted(FORCED_NONZERO)}\n")

    def probe(zeroset, rng):
        pt = {}
        for v in OTHER:
            pt[v] = 0 if (v in zeroset and v not in FORCED_NONZERO) else rng.randrange(1, p)
        rows = []
        for i in lin:
            row = [0] * (n + 1)
            for m, co in polys[i].items():
                cv = [v for v, e in m if v in cset]
                rest = tuple((v, e) for v, e in m if v not in cset)
                val = co * evalmono(rest, pt, p) % p
                if cv: row[cidx[cv[0]]] = (row[cidx[cv[0]]] + val) % p
                else:  row[n] = (row[n] - val) % p
            rows.append(row)
        rA, _ = rank_modp([r[:n] for r in rows], n, p)
        rAug, sol = rank_modp(rows, n + 1, p)
        return rA, rAug, sol, pt

    pats = []
    freeS = [v for v in S if v not in FORCED_NONZERO]
    for k in range(1, len(freeS) + 1):
        import itertools
        for comb in itertools.combinations(freeS, k):
            pats.append((f"s zero: {','.join(comb)}", set(comb)))
    freeD = [v for v in D if v not in FORCED_NONZERO]
    pats.append(("all free s zero + half of d zero", set(freeS) | set(freeD[:len(freeD)//2])))
    pats.append(("all free s zero + other half of d zero", set(freeS) | set(freeD[len(freeD)//2:])))
    pats.append(("all free d zero", set(freeD)))
    pats.append(("all free s and all free d zero", set(freeS) | set(freeD)))

    rng = random.Random(4242)
    hits = []
    for name, zs in pats:
        rA, rAug, sol, pt = probe(zs, rng)
        ok = (rA == rAug)
        print(f"  {name:52s} rank A={rA:2d} rank[A|b]={rAug:2d} -> "
              f"{'*** CONSISTENT ***' if ok else 'inconsistent'}", flush=True)
        if ok:
            hits.append((name, zs, sol, pt))

    if not hits:
        print(f"\n{len(pats)} coordinate-subspace patterns, all inconsistent.")
        print("Still NO VERDICT on emptiness -- these are finitely many of the")
        print("proper closed subvarieties, not all of them. But it does close the")
        print("cheapest place a solution could have been hiding from random probes.")
        return 0

    for name, zs, sol, pt in hits:
        print(f"\n*** LEAD on subspace [{name}] -- verifying against the originals ***")
        kv = [v for v in sol if v[n] % p]
        if not kv:
            print("  consistent but no affine solution recovered -- reporting as a BUG")
            continue
        inv = pow(kv[0][n], p - 2, p)
        full = dict(pt)
        for j, v in enumerate(C):
            full[v] = (-kv[0][j]) * inv % p
        bad = [i for i in lin
               if sum(co * evalmono(m, full, p)
                      for m, co in polys[i].items()) % p]
        if bad:
            print(f"  CHECK FAILED: {len(bad)} originals do not vanish -> BUG, not a hit")
            continue
        print(f"  all {len(lin)} original equations vanish exactly")
        sat = [i for i in range(len(body)) if i not in lin]
        for i in sat:
            val = sum(co * evalmono(m, full, p)
                      for m, co in polys[i].items()) % p
            print(f"  held-out row {i} evaluates to {val} "
                  f"({'SATISFIED' if val == 0 else 'NOT satisfied'})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
