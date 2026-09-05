#!/usr/bin/env python3
"""Faithful scan of the strip families for {P,Q} = x^k.

Unlike batch.py (superseded), the Q-side degrees are NOT prescribed: each
g_sigma is allowed any T-degree up to a generous common N, so the search is
over ALL strip-type Q, not just those matching one prescribed window set.
Validated: it returns non-empty on tops=(4,2), mu=1, which is witness W3.

Ordered by number of unknowns, smallest support first.
"""
import sys, itertools
from math import ceil
from fractions import Fraction
import general2

MAXVARS = int(sys.argv[1]) if len(sys.argv) > 1 else 20
BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 300
TOPMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 8

jobs = []
for k in (2, 1):
    for mu in range(1, 4):
        Ltop = (k + 1) * mu - 1
        for rmax in range(mu, Ltop + 1):
            smax = Ltop - rmax
            lo_f = {r: ceil(Fraction(r, mu)) for r in range(rmax + 1)}
            ranges = [range(lo_f[r], TOPMAX + 1) for r in range(rmax + 1)]
            for tops in itertools.product(*ranges):
                if tops[mu] < 1:
                    continue
                nv = sum(tops[r] - lo_f[r] + 1 for r in range(rmax + 1))
                if not (3 <= nv <= MAXVARS):
                    continue
                degP = max((mu + 1) * tops[r] - r for r in range(rmax + 1))
                jobs.append((nv, degP, k, mu, rmax, smax, tops))
jobs.sort()
print(f"{len(jobs)} configurations, <= {MAXVARS} unknowns, {BUDGET}s each", flush=True)
hits = []
for nv, degP, k, mu, rmax, smax, tops in jobs:
    line = general2.run(mu, rmax, smax, k, list(tops), None, 32003, BUDGET)
    if line and 'VERDICT dim -1' not in line and 'TIMEOUT' not in line:
        hits.append(line)
        print("  ^^^ NON-EMPTY", flush=True)
print(f"\n=== {len(hits)} non-empty configurations ===")
for h in hits:
    print(h)
