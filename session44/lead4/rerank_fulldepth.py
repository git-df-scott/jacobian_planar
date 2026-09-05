"""Re-rank all loose charts at FULL bracket depth.

The dim measured at jextra=2 counts freedoms the untruncated bracket
would kill: the (9,27) control reads dim<=69 shallow but dim<=1 full.
EMPTY verdicts are unaffected (more conditions only shrink a variety);
but the DIM RANKING that chose hunting targets was shallow. This recomputes
true dim for every loose chart, exposing which are actually tight."""
import json
import random

from walk_pair import Walker
from trackB1_polygon import rank_mod_p

out = []
for t in json.load(open("trackD_targets_loose.json")):
    try:
        w = Walker(t["NP"], t["NQ"], [(t["r"], 0, 1)], t["tag"], full_depth=True)
    except ValueError:
        continue
    rng = random.Random(7)
    vec = [rng.randrange(65521) for _ in w.idx]
    vec[w.pivot] = rng.randrange(1, 65521)
    base = w.conds_labeled(vec)
    cols = [w.conds_labeled(vec, k) for k in range(len(w.idx))]
    keys = sorted(set(base) | {k for c in cols for k in c})
    M = [[c.get(key, (0, 0))[1] for c in cols] for key in keys]
    rk = rank_mod_p(M)
    dfull = len(w.idx) - rk
    out.append((dfull, t["dim"], len(w.idx), t["max"], t["tag"]))
    print(f"dim_full={dfull:3d} (was {t['dim']:3d}) params={len(w.idx):3d} "
          f"max={t['max']:3d}  {t['tag'][:52]}", flush=True)
out.sort(reverse=True)
json.dump([{"dim_full": d, "dim_shallow": ds, "params": p, "max": mx,
            "tag": tg} for d, ds, p, mx, tg in out],
          open("rerank_fulldepth.json", "w"), indent=1)
print(f"\n{len(out)} charts; still-loose (dim_full>=5): "
      f"{sum(1 for d,*_ in out if d>=5)}")
