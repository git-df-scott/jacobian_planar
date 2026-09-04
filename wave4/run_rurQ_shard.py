"""Fill the w4_edge_rur_Q prime cache in parallel shards.

Each shard runs msolve at threads=1 on its own primes and writes its own cache
file; w4_edge_rur_Q.main merges every shard it finds before reconstructing.  The
point is only throughput -- the arithmetic is identical either way.

usage: run_rurQ_shard.py <shard> <nshards> <nprimes> [chart]
"""
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_edge_rur_Q as R

shard, nshards, nprimes = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
chart = sys.argv[4] if len(sys.argv) > 4 else "one"
path = os.path.join(HERE, "artifacts", f"rurQ_primes_{chart}_s{shard}.json")

primes, n = [], 1000000
while len(primes) < nprimes:
    n += 1
    if n % 3 == 1 and sp.isprime(n):
        primes.append(n)

cache = json.load(open(path)) if os.path.exists(path) else {}
for i, p in enumerate(primes):
    if i % nshards != shard or str(p) in cache:
        continue
    cache[str(p)] = R._rur_at(p, chart)
    json.dump(cache, open(path, "w"))
    print(f"  shard {shard}: p={p} "
          f"{'ok' if cache[str(p)] else 'UNUSABLE'}", flush=True)
print(f"shard {shard} done: {sum(1 for v in cache.values() if v)} usable "
      f"of {len(cache)}")
