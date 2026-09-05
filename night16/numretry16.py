"""night16 -- second pass: NUM-MONO on the atypical fibres whose first pass hit
the wall-clock budget.  Larger budget, coarser-then-finer as usual."""
import glob, json, os, sys, time
from fractions import Fraction as Fr
import mono16 as M, load16

BUD = float(os.environ.get("BUD", "400"))
k, n = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 1)
OUT = "numretry16_%d.json" % k

R = []
for f in sorted(glob.glob("atypical16_*.json")):
    R.extend(json.load(open(f)))
S = {r["hash"]: r for r in load16.survivors()}
jobs = []
for r in R:
    for f in r.get("fibres", []):
        if f.get("num_on", {}).get("verdict") is None and f.get("kind") == "rational":
            jobs.append((r["hash"], f["c"]))
jobs = [j for i, j in enumerate(jobs) if i % n == k]
res = json.load(open(OUT)) if os.path.exists(OUT) else []
done = {(z["hash"], z["c"]) for z in res}
for h, c in jobs:
    if (h, c) in done:
        continue
    Pd = load16.Pdict(S[h])
    t0 = time.time()
    try:
        r = M.screen_fibre_checked(Pd, Fr(c), tol=1e-6, nsub=6, ncirc=48, budget=BUD)
        inf = r.get("infinity", {}) if "error" not in r else {}
        out = {"hash": h, "c": c,
               "verdict": r.get("verdict"), "error": r.get("error"),
               "ls_residual": r.get("ls_residual"), "max_period": r.get("max_period"),
               "rel_ls_residual": r.get("rel_ls_residual"),
               "err_ls_residual": r.get("err_ls_residual"),
               "chi": r.get("chi"), "n_components": r.get("n_components"),
               "n_punctures": r.get("n_punctures"), "genus_sum": r.get("genus_sum"),
               "n_cycles": r.get("n_independent_cycles_found"),
               "max_abs_residue": inf.get("max_abs_residue"),
               "sum_abs_residues": inf.get("sum_abs"),
               "n_places_total": inf.get("n_places_total"),
               "t": round(time.time() - t0, 1)}
    except Exception as e:
        out = {"hash": h, "c": c, "error": "%s: %s" % (type(e).__name__, e),
               "t": round(time.time() - t0, 1)}
    res.append(out)
    json.dump(res, open(OUT, "w"), indent=1, default=str)
    print("%s c=%s -> %s (%.0fs)" % (h, c, out.get("verdict") or out.get("error"),
                                     out["t"]), flush=True)
