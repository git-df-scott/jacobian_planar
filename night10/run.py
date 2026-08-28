"""night10 -- STEP 1 / STEP 2 / STEP 3 on the 8 F_2 census points of night8.

Base rings: system over Z; reductions over F_2; ladders over
O2 = Z[pi]/(pi^2-2) (steps 1-2) and O3 = Z[pi]/(pi^3-2) (step 3).
"""

import json
import os
import sys

import system as S
import ram
from ram import O2, O3
import ladder as LAD
from ladder import Ladder

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = json.load(open(os.path.join(HERE, "..", "night8", "all_eight.json")))
assert CENSUS["E0_coordinate_order"] == S.VARS, "coordinate order mismatch"
POINTS = [p["point"] for p in CENSUS["points"]]
assert len(POINTS) == 8


def bits(v):
    return "".join(str(t) for t in v)


out = {"base_ring_of_system": "Z", "coordinate_order": S.VARS,
       "row_labels": S.LABELS, "ceiling_level": LAD.CEILING, "points": []}

for idx, x0 in enumerate(POINTS, start=1):
    rec = {"index": idx, "point": x0, "bits": bits(x0)}

    # --- base checks over Z ---
    r0 = S.r_eval(x0)
    assert all(t % 2 == 0 for t in r0), "r(x0) not even at point %d" % idx
    s = [t // 2 for t in r0]
    rec["r_x0_over_Z"] = r0
    rec["s_equals_r_x0_over_2"] = s
    J = S.jac_eval(x0)
    J2 = [[c % 2 for c in row] for row in J]
    rank = LAD.ram_rank(J2, S.N)
    kbasis = LAD.ker(J2, S.N)
    K2 = LAD.span(kbasis, S.N)
    rec["rank_J_mod2"] = rank
    rec["nullity_J_mod2"] = S.N - rank
    rec["kernel_size"] = len(K2)

    # --- STEP 1 (O2): for d in K2, is (s + B(d,d)) mod 2 in Im(J mod 2)? ---
    L2 = Ladder(O2, S.N, S.r_eval, S.jac_eval, x0)
    assert L2.rank == rank
    passing, formula_passing = [], []
    for d in K2:
        _, rho, ok, _ = L2.level_data({1: list(d)}, 2)
        # independent closed-form cross-check
        q = S.Q2(list(d))
        rho_formula = [(s[k] + q[k]) % 2 for k in range(S.M)]
        ok_formula, _ = LAD.solve(J2, rho_formula, S.N)
        assert rho == rho_formula, "step-1 rho mismatch at point %d, d=%s" % (idx, d)
        assert ok == ok_formula
        if ok:
            passing.append(list(d))
        if ok_formula:
            formula_passing.append(list(d))
        if not ok:
            rec.setdefault("step1_failure_rows", {})[bits(d)] = \
                [S.LABELS[i] for i, b in enumerate(rho) if b]
    rec["step1_O2_pass_count"] = len(passing)
    rec["step1_O2_passing_d1"] = passing
    rec["step1_O2_passing_d1_bits"] = [bits(d) for d in passing]
    assert passing == formula_passing

    # --- STEP 2 (O2): full pi-ladder ---
    if passing:
        res = L2.run()
        rec["step2_nodes"] = res["nodes"]
        rec["step2_max_level_reached"] = res["max_level_reached"]
        rec["step2_n_deaths"] = len(res["deaths"])
        if res["survivor"] is not None:
            rec["step2_survivor"] = res["survivor"]
        else:
            rec["step2_survivor"] = None
            lv = sorted({d["level"] for d in res["deaths"]})
            rec["step2_death_levels"] = lv
            rep = min(res["deaths"], key=lambda d: d["level"])
            rec["step2_representative_death"] = rep
    else:
        rec["step2_max_level_reached"] = 1
        rec["step2_survivor"] = None
        rec["step2_death_levels"] = [2]
        rec["step2_note"] = "no d_1 passes level 2; every branch dies at level 2"

    out["points"].append(rec)
    print("point %d %s: step1 pass %d/16, max level %s, survivor %s"
          % (idx, bits(x0), rec["step1_O2_pass_count"],
             rec.get("step2_max_level_reached"), rec.get("step2_survivor") is not None))

json.dump(out, open(os.path.join(HERE, "ramified_O2.json"), "w"), indent=1)
print("wrote ramified_O2.json")
