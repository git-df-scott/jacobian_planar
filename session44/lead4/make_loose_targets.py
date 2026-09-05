"""Emit ALL loose vertex-alive charts (dim >= 2, no forced-zero vertex) of
the 34 published chains as a walker/twoprime target file, reproducing the
CANDIDATE_MAP.md selection mechanically."""
import json
import random

import trackB1_shapes as SH
import trackD_vertex as TV
from trackD_pipeline import build_all

picks = []
for cd in build_all():
    ch = cd["chain"]
    pair = SH.Pair("probe", cd["NP"], cd["NQ"], [(cd["r"], 0, 1)], "")
    rr = SH.run_pair(pair, random.Random(1))
    if rr["status"] != "OK":
        continue
    dim = rr["nparams"] - rr["rank"]
    pv = TV.probe(cd["NP"], cd["NQ"], cd["r"])
    vfz = pv.get("forced_zero", pv) if isinstance(pv, dict) else pv
    if dim >= 2 and not vfz:
        tag = (f"{ch.name} | a={cd['a']} b={cd['b']} c'={cd['cprime']} "
               f"r={cd['r']} eps=({cd['epsP']},{cd['epsQ']})")
        picks.append({"tag": tag, "NP": cd["NP"], "NQ": cd["NQ"],
                      "r": cd["r"], "max": ch.maxdeg, "dim": dim,
                      "params": rr["nparams"], "size": cd["size"],
                      "tier": "loose"})
picks.sort(key=lambda t: -t["dim"])
json.dump(picks, open("trackD_targets_loose.json", "w"), indent=1)
print(f"{len(picks)} loose charts written")
for t in picks:
    print(f"  dim={t['dim']:3d} params={t['params']:3d} max={t['max']:3d}  {t['tag']}")
