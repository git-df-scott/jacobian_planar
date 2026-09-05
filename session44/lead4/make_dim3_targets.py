"""Build the trackD_twoprime targets file for the dim-3 loose charts.

CANDIDATE_MAP.md instrument (1): the two nearly-tight loose charts
(params=127, rank=124, dim=3, all required vertices alive) found by the
calibrated rank+vertex sweep over the 134 eps-passing charts:

    F17            (m,n)=(2,3)  r=1   max  99
    (9,27)/9,24/11/3,8 (m,n)=(2,3)  r=1   max 108

This script re-runs the SAME instruments (run_pair rank bound + vertex
probe) on every chart of those two chains and keeps exactly the charts with
dim == 3 and an empty forced-zero list, so the selection is reproduced, not
hand-copied.  Output: trackD_targets_dim3.json in the twoprime format.
"""
import json
import random

import trackB1_shapes as SH
import trackD_vertex as TV
from trackD_pipeline import build_all


def main():
    picks = []
    for cd in build_all():
        ch = cd["chain"]
        if ch.name not in ("F17(m,n)=2,3", "(9,27)/9,24/11/3,8 (m,n)=2,3"):
            continue
        pair = SH.Pair("probe", cd["NP"], cd["NQ"], [(cd["r"], 0, 1)], "")
        rr = SH.run_pair(pair, random.Random(1))
        if rr["status"] != "OK":
            continue
        dim = rr["nparams"] - rr["rank"]
        pv = TV.probe(cd["NP"], cd["NQ"], cd["r"])
        vfz = pv.get("forced_zero", pv) if isinstance(pv, dict) else pv
        print(f"{ch.name}(m,n) r={cd['r']} eps=({cd['epsP']},{cd['epsQ']}) "
              f"params={rr['nparams']} rank={rr['rank']} dim={dim} vfz={vfz}")
        if dim == 3 and not vfz:
            tag = (f"{ch.name} | a={cd['a']} b={cd['b']} c'={cd['cprime']} "
                   f"r={cd['r']} eps=({cd['epsP']},{cd['epsQ']})")
            picks.append({"tag": tag, "NP": cd["NP"], "NQ": cd["NQ"],
                          "r": cd["r"], "max": ch.maxdeg,
                          "params": rr["nparams"], "size": cd["size"],
                          "tier": "dim3-loose"})
    print(f"\n{len(picks)} dim-3 loose charts kept")
    with open("trackD_targets_dim3.json", "w") as f:
        json.dump(picks, f, indent=1)
    for p in picks:
        print(" ", p["tag"])


if __name__ == "__main__":
    main()
