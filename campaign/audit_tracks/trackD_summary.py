"""Triage table from trackD_results.json.

dim_bound 1 is the BASELINE, not a survival: the p_00 column of the Jacobian
is identically zero in every shape (adding a constant to P changes no
bracket), so the polygon conditions can never do better than 1.  Both open
(8,28) cases sit at exactly 1.  dim_bound >= 2 means the polygon conditions
left genuine freedom and the shape needs more than this machine.
"""
import json, collections, sys

rows = json.load(open("trackD_results.json"))
by_chain = collections.defaultdict(list)
for r in rows:
    by_chain[r["chain"]].append(r)

print(f"{'chain':38s} {'max':>4s} {'shapes':>6s} {'mode':>8s} "
      f"{'best dim':>8s} {'worst dim':>9s}  verdict")
print("-" * 108)
tight_chains, loose_chains = [], []
for name in sorted(by_chain, key=lambda n: (-by_chain[n][0]["chain_max"], n)):
    rs = by_chain[name]
    ok = [r for r in rs if r["status"] == "OK"]
    if not ok:
        print(f"{name[:38]:38s} {rs[0]['chain_max']:4d} {len(rs):6d} "
              f"{rs[0]['mode']:>8s} {'-':>8s} {'-':>9s}  ALL OUT OF SCOPE")
        continue
    dims = [r["dim_bound"] for r in ok]
    best, worst = min(dims), max(dims)
    mode = ok[0]["mode"]
    if worst <= 1:
        verdict = "every shape cut to <= 1 (ready for elimination)"
        tight_chains.append(name)
    elif best <= 1:
        verdict = f"{sum(1 for d in dims if d >= 2)}/{len(dims)} shapes loose"
        loose_chains.append(name)
    else:
        verdict = "NO shape cut below 2 -- polygon conditions too weak"
        loose_chains.append(name)
    print(f"{name[:38]:38s} {ok[0]['chain_max']:4d} {len(ok):6d} "
          f"{mode:>8s} {best:8d} {worst:9d}  {verdict}")

print()
print(f"chains where EVERY shape is cut to dim <= 1: {len(tight_chains)}")
print(f"chains with at least one loose shape:        {len(loose_chains)}")

loose = [r for r in rows if r["status"] == "OK" and r["dim_bound"] >= 2]
print(f"\nloose shapes ({len(loose)} of {len(rows)}), worst first:")
for r in sorted(loose, key=lambda r: -r["dim_bound"])[:25]:
    print(f"  dim<={r['dim_bound']:4d}  params={r['nparams']:4d} "
          f"conds={r['nconds']:4d} rank={r['rank']:4d}  {r['name'][:70]}")

ge125 = [r for r in rows if r["status"] == "OK" and r["chain_max"] >= 125]
print(f"\n--- the >= 125 frontier ({len(ge125)} shape runs) ---")
g = collections.defaultdict(list)
for r in ge125:
    g[r["chain"]].append(r["dim_bound"])
for name in sorted(g, key=lambda n: -max(x["chain_max"] for x in rows
                                         if x["chain"] == name)):
    mx = max(x["chain_max"] for x in rows if x["chain"] == name)
    print(f"  max={mx:4d}  {name[:44]:44s} shapes={len(g[name]):3d} "
          f"dim range {min(g[name])}..{max(g[name])}")
