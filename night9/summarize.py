"""night9 — merge the per-prime survey CSVs into night9/prime_survey.csv and
print the tallies.  Reporting only; computes nothing new."""
import csv, glob, json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from survey import FIELDS

rows = []
for f in sorted(glob.glob(os.path.join(HERE, "prime_survey_p*.csv"))):
    with open(f) as fh:
        rows += list(csv.DictReader(fh))
rows.sort(key=lambda r: (int(r["p"]), r["family"], r["hash"]))
with open(os.path.join(HERE, "prime_survey.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow(r)

cells = Counter(); verd = Counter(); meth = Counter()
tear = Counter(); climb = Counter()
ne_by_p = Counter(); tot_by_p = Counter()
sol_by_p = Counter()
deg = Counter(); vfail = 0
for r in rows:
    p = int(r["p"]); fam = r["family"]
    cells[(fam, p)] += 1
    tot_by_p[p] += 1
    verd[(r["verdict"], p)] += 1
    verd[("TOTAL_" + r["verdict"], 0)] += 1
    meth[r["method"]] += 1
    if r["verdict"] == "NONEMPTY":
        ne_by_p[p] += 1
        if r["count"]:
            sol_by_p[p] += int(r["count"])
    for k in ("n_tear_nonempty", "n_tear_empty", "n_tear_other"):
        tear[(k, p)] += int(r.get(k) or 0)
    deg[p] += int(r.get("n_degenerate") or 0)
    vfail += int(r.get("n_verify_fail") or 0)
    climb[("p2", p)] += int(r.get("climb_p2") or 0)
    climb[("p2_tn", p)] += int(r.get("climb_p2_tear_nonempty") or 0)
    climb[("p3", p)] += int(r.get("climb_p3") or 0)

PR = sorted({int(r["p"]) for r in rows})
out = {
    "total_cells": len(rows),
    "cells_per_family_per_prime": {"%s_p%d" % k: v for k, v in sorted(cells.items())},
    "verdict_totals": {k[0].replace("TOTAL_", ""): v
                       for k, v in verd.items() if k[0].startswith("TOTAL_")},
    "verdict_by_prime": {"p%d" % p: {v: verd[(v, p)] for v in
                                     ("NONEMPTY", "EMPTY", "INCONCLUSIVE", "TIMEOUT")
                                     if verd[(v, p)]} for p in PR},
    "method_counts": dict(meth),
    "NONEMPTY_cells_by_prime": {"p%d" % p: ne_by_p[p] for p in PR},
    "exact_F_p_solution_count_summed_over_cells_by_prime":
        {"p%d" % p: sol_by_p[p] for p in PR},
    "sampled_solutions_verified_fail": vfail,
    "degenerate_screened_by_prime": {"p%d" % p: deg[p] for p in PR},
    "tear_by_prime": {"p%d" % p: {"TEAR-NONEMPTY": tear[("n_tear_nonempty", p)],
                                  "TEAR-EMPTY": tear[("n_tear_empty", p)],
                                  "other/not-computed": tear[("n_tear_other", p)]}
                      for p in PR},
    "climb_counts_by_prime": {"p%d" % p: {"to_Z_p2": climb[("p2", p)],
                                          "to_Z_p2_from_TEAR-NONEMPTY": climb[("p2_tn", p)],
                                          "to_Z_p3": climb[("p3", p)]} for p in PR},
}
with open(os.path.join(HERE, "prime_survey_summary.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
