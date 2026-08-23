#!/usr/bin/env python3
"""Scan the strip families for {P,Q} = x^k, smallest support first.

For each (mu, rmax, smax) with rmax+smax = (k+1)mu-1 and rmax >= mu (so P can
carry the vertex (1,0)), and each m making M = smax*m/rmax integral, run the
general engine.  Ordered by the number of unknowns.
"""
import sys, itertools
from fractions import Fraction
from math import ceil
import general

MAXVARS = int(sys.argv[1]) if len(sys.argv) > 1 else 26
BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 600
KS = [2, 1]

jobs = []
for k in KS:
    for mu in range(1, 6):
        Ltop = (k + 1) * mu - 1
        for rmax in range(mu, Ltop + 1):
            smax = Ltop - rmax
            for m in range(1, 40):
                M = general.config(mu, rmax, smax, k, m)
                if M is None or M < 1:
                    continue
                lo_f = {r: ceil(Fraction(r, mu)) for r in range(rmax + 1)}
                if m < max(lo_f.values()):
                    continue   # some P-slice would be empty; the top vertex would not exist
                nv = sum(max(0, m - lo_f[r] + 1) for r in range(rmax + 1))
                if nv > MAXVARS or nv < 3:
                    continue
                degP, degQ = (mu + 1) * m, (mu + 1) * M
                jobs.append((nv, k, mu, rmax, smax, m, degP, degQ))
jobs.sort()
print(f"{len(jobs)} configurations, <= {MAXVARS} unknowns, {BUDGET}s each\n", flush=True)
for nv, k, mu, rmax, smax, m, degP, degQ in jobs:
    print(f"### vars~{nv}  k={k} mu={mu} (rmax,smax)=({rmax},{smax}) m={m} "
          f"-> (degP,degQ)=({degP},{degQ})", flush=True)
    general.run(mu, rmax, smax, k, m, 32003, BUDGET)
