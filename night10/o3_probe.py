"""night10 -- bounded STEP-3 follow-up: DFS probe of the O3 = Z[pi]/(pi^3-2)
ladder to w-level 12, with a node budget.  Depth-first, so a deep branch is
found quickly if one exists."""

import json
import os

import system as S
import ladder as LAD
from ladder import Ladder
from ram import O3

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = json.load(open(os.path.join(HERE, "..", "night8", "all_eight.json")))
POINTS = [p["point"] for p in CENSUS["points"]]

LAD.NODE_BUDGET = 300000
out = {"ring": "O3 = Z[pi]/(pi^3-2), w(pi)=1, w(2)=3", "ceiling": 12, "points": []}

for idx, x0 in enumerate(POINTS, start=1):
    L = Ladder(O3, S.N, S.r_eval, S.jac_eval, x0, ceiling=12)
    try:
        res = L.run()
        budget = False
    except RuntimeError:
        res, budget = None, True
    rec = {"index": idx, "bits": "".join(map(str, x0)), "budget_exceeded": budget}
    if res:
        rec["nodes"] = res["nodes"]
        rec["max_level_reached"] = res["max_level_reached"]
        rec["n_deaths"] = len(res["deaths"])
        rec["death_levels"] = sorted({d["level"] for d in res["deaths"]})
        rec["survivor"] = res["survivor"]
        if res["deaths"]:
            rep = min(res["deaths"], key=lambda d: d["level"])
            rec["representative_death"] = rep
    out["points"].append(rec)
    print("point %d %s: budget_exceeded=%s max_level=%s survivor=%s death_levels=%s"
          % (idx, rec["bits"], budget, rec.get("max_level_reached"),
             rec.get("survivor") is not None, rec.get("death_levels")))

json.dump(out, open(os.path.join(HERE, "ramified_O3_probe.json"), "w"), indent=1)
print("wrote ramified_O3_probe.json")
