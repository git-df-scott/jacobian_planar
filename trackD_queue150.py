"""Queue the >150 family chains into trackD_targets.json, through the same
gates the 34-shape catalogue went through:

  1. compiler        trackD_chain_map.reduced_candidates   (validated 6/6)
  2. eps filter      eps_P + eps_Q = (r+1,1) + the engine's j=0 row shape
  3. vertex probe    a required vertex of the non-driver must not be
                     identically zero as a function of the driver
  4. sweep           y-adic + exact dual-number Jacobian, keep dim <= 1

Only shapes clearing all four are appended, tagged tier="gen>150" so the
>150 additions stay distinguishable from the Sec.6 catalogue.
"""
import json, random, sys
from trackD_generate import generate
from trackD_chain_map import reduced_candidates, check_eps
from trackD_pipeline import npoints, run_one
from trackD_vertex import probe

bound = int(sys.argv[1]) if len(sys.argv) > 1 else 300
rng = random.Random(11)
chains = [c for c in generate(bound) if c.maxdeg > 150]
print(f"{len(chains)} generated family chains above 150")
add, stats = [], dict(shapes=0, eps=0, vtx=0, tight=0)
for ch in chains:
    cands, _ = reduced_candidates(ch)
    stats["shapes"] += len(cands)
    kept = [c for c in cands if check_eps(c)[0]]
    stats["eps"] += len(kept)
    for cd in kept:
        pr = probe(cd["NP"], cd["NQ"], cd["r"])
        if pr["status"] != "OK" or pr["forced_zero"]:
            continue
        stats["vtx"] += 1
        cd["mode"] = "gen"
        cd["size"] = npoints(cd["NP"]) + npoints(cd["NQ"])
        r = run_one(cd, rng)
        if r["status"] != "OK" or r["dim_bound"] > 1:
            continue
        stats["tight"] += 1
        add.append({"tag": f"{ch.name} | a={cd['a']} b={cd['b']} "
                           f"c'={cd['cprime']} r={cd['r']} "
                           f"eps=({cd['epsP']},{cd['epsQ']})",
                    "NP": cd["NP"], "NQ": cd["NQ"], "r": cd["r"],
                    "max": ch.maxdeg, "mode": "gen>150", "tier": "gen>150",
                    "params": r["nparams"], "conds": r["nconds"],
                    "rank": r["rank"], "size": cd["size"]})
        print(f"  QUEUED max={ch.maxdeg:4d} params={r['nparams']:4d} "
              f"conds={r['nconds']:4d} dim<={r['dim_bound']}  {add[-1]['tag'][:60]}",
              flush=True)
print(f"\ncandidates {stats['shapes']} -> eps {stats['eps']} -> vertex-live "
      f"{stats['vtx']} -> tight {stats['tight']}")
T = json.load(open("trackD_targets.json"))
for t in T:
    t.setdefault("tier", "sec6>=125")
existing = {t["tag"] for t in T}
new = [a for a in add if a["tag"] not in existing]
json.dump(T + new, open("trackD_targets.json", "w"), indent=1)
print(f"[trackD_targets.json: {len(T)} existing + {len(new)} new = {len(T)+len(new)}]")
