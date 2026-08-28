"""night10 -- per-level branch census for the O2 ladder, and STEP 3 over O3."""

import json
import os

import system as S
import ladder as LAD
from ladder import Ladder
from ram import O2, O3

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = json.load(open(os.path.join(HERE, "..", "night8", "all_eight.json")))
POINTS = [p["point"] for p in CENSUS["points"]]


def bits(v):
    return "".join(str(t) for t in v)


def level_census(R, x0, maxlevel=12):
    """BFS: number of live branches at each level, deaths per level."""
    L = Ladder(R, S.N, S.r_eval, S.jac_eval, x0, ceiling=maxlevel)
    live = [{}]           # list of ds dicts
    per_level = []
    for m in range(1, maxlevel + 1):
        nxt, ndeath, death_rep = [], 0, None
        for ds in live:
            wm, rho, ok, sols = L.level_data(ds, m)
            if not ok:
                ndeath += 1
                if death_rep is None:
                    aug = [list(r) + [rho[i]] for i, r in enumerate(L.J2)]
                    death_rep = dict(
                        ds={k: list(v) for k, v in ds.items()},
                        rho_rows=[S.LABELS[i] for i, b in enumerate(rho) if b],
                        wmin_before=wm, rank_J=L.rank,
                        rank_aug=LAD.ram_rank(aug, S.N + 1))
                continue
            for d in sols:
                ds2 = dict(ds)
                ds2[m] = list(d)
                res = L.resid(ds2)
                assert min(R.w(u) for u in res) > m
                nxt.append(ds2)
        per_level.append(dict(level=m, branches_in=len(live), died=ndeath,
                              branches_out=len(nxt), death_representative=death_rep))
        live = nxt
        if not live:
            break
    return L, per_level, live


out = {"ceiling": 12, "points": []}
for idx, x0 in enumerate(POINTS, start=1):
    rec = {"index": idx, "bits": bits(x0)}

    # ---- O2 full level census ----
    L, per_level, live = level_census(O2, x0, 12)
    rec["O2_level_census"] = per_level
    rec["O2_survivors_at_12"] = len(live)
    if live:
        ds = live[0]
        rec["O2_survivor_example"] = {
            "ds": {k: list(v) for k, v in ds.items()},
            "trunc_pairs": [list(u) for u in L.trunc(ds)],
            "residual_pairs": [list(u) for u in L.resid(ds)],
        }

    # ---- STEP 3: O3 level-2 test only ----
    L3 = Ladder(O3, S.N, S.r_eval, S.jac_eval, x0, ceiling=2)
    K2 = L3.kernel
    w1, rho1, ok1, sols1 = L3.level_data({}, 1)
    passing3 = []
    for d in K2:
        _, rho, ok, _ = L3.level_data({1: list(d)}, 2)
        # closed-form cross-check for the cubic base: rho = Q2(d) mod 2  (no s)
        q = [t % 2 for t in S.Q2(list(d))]
        assert rho == q, "O3 level-2 rho mismatch at point %d" % idx
        if ok:
            passing3.append(list(d))
    rec["O3_w_r_x0"] = w1
    rec["O3_level1_rho_zero"] = all(t == 0 for t in rho1)
    rec["O3_step1_pass_count"] = len(passing3)
    rec["O3_step1_passing_d1_bits"] = [bits(d) for d in passing3]
    out["points"].append(rec)

    print("point %d %s | O2 levels: %s | O2 survivors@12=%d | O3 pass %d/16 %s"
          % (idx, bits(x0),
             ",".join("L%d:%d->%d" % (p["level"], p["branches_in"], p["branches_out"])
                      for p in per_level),
             len(live), len(passing3), rec["O3_step1_passing_d1_bits"]))

json.dump(out, open(os.path.join(HERE, "ramified_detail.json"), "w"), indent=1)
print("wrote ramified_detail.json")
