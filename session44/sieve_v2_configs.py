#!/usr/bin/env python3
"""Sieve v2a — exact configuration enumeration for REDUCIBLE tears.

Session 43's Euler identity, for a tear stratified into components A_i with
constant fibre count n_i (0 <= n_i <= d-1) plus isolated deeper points P_k
with fibre count m_k (each a chi=1 stratum, its ambient components' chi
reduced accordingly):

    sum_i (d - n_i) chi(A_i^o) + sum_k (d - m_k) = d - 1.

Enumerates all configurations for d = 6, 7, 8 with 1..3 components,
chi(A_i^o) in [-4, 1], 0..2 deeper points.  Records the structural fact the
enumeration makes obvious: chi = 0 components contribute nothing (invisible
passengers), so component count is NOT bounded by the identity — boundedness
must come from the group/geometry layer (splice presentations; future work).
"""
import itertools

for d in (6, 7, 8):
    total = 0
    exemplars = []
    for ncomp in (1, 2, 3):
        for chis in itertools.product(range(-4, 2), repeat=ncomp):
            for ns in itertools.product(range(d), repeat=ncomp):
                if list(zip(chis, ns)) != sorted(zip(chis, ns)):
                    continue  # canonical order, avoid double count
                for ndeep in (0, 1, 2):
                    for ms in itertools.combinations_with_replacement(
                            range(d), ndeep):
                        lhs = sum((d - n) * c for c, n in zip(chis, ns)) \
                            + sum(d - m for m in ms)
                        if lhs == d - 1:
                            total += 1
                            if len(exemplars) < 4 and ncomp > 1:
                                exemplars.append((chis, ns, ms))
    print(f"d={d}: {total} admissible reducible-tear configurations "
          f"(<=3 comps, chi>=-4, <=2 deep points)")
    for e in exemplars:
        print(f"   e.g. chis={e[0]} ns={e[1]} deep_ms={e[2]}")
print()
print("STRUCTURAL NOTE: any chi=0 component contributes 0 to the identity —")
print("component count is unbounded by Euler data alone; the finiteness of")
print("the irreducible case (m=1, chi=1 forced) does NOT extend. The group")
print("layer (EN splice presentations) is where reducible-tear finiteness")
print("must come from. Recorded as the v2b target.")
