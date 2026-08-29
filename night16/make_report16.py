"""night16 -- assemble ATYPICAL.md and atypical.csv from the run records."""
import csv, glob, json
from collections import Counter

R = []
for f in sorted(glob.glob("atypical16_*.json")):
    R.extend(json.load(open(f)))
order = {r["hash"]: i for i, r in enumerate(json.load(open("survivor_order16.json")))}
R.sort(key=lambda r: order.get(r["hash"], 999))
json.dump(R, open("atypical16.json", "w"), indent=1, default=str)

# ------------------------------------------------------------------- csv
COLS = ["hash", "label", "deg_P", "deg_y", "n15_instrument", "n15_fibres_tested",
        "chi_gen", "chi_gen_votes", "n_atypical", "atypical_c", "chi_at_atypical",
        "n_components_at_atypical", "component_degrees", "n_vertical_components",
        "exact_prim_verdict", "exact_prim_degF",
        "nummono_verdict_on", "nummono_ls_residual_on", "nummono_max_period_on",
        "nummono_max_abs_residue_on", "nummono_sum_abs_residues_on",
        "nummono_chi_on", "nummono_ncomp_on", "nummono_npunct_on",
        "near_c", "near_exact_chi", "near_nummono_verdict", "near_nummono_max_period",
        "verdict"]


def fmt(v):
    return ("%.3g" % v) if isinstance(v, float) else ("" if v is None else str(v))


def row(r):
    fs = r.get("fibres", [])
    d = {c: "" for c in COLS}
    for k in ("hash", "label", "deg_P", "deg_y", "n15_instrument", "chi_gen",
              "chi_gen_votes", "verdict"):
        d[k] = r.get(k, "")
    d["n15_fibres_tested"] = "|".join(str(z) for z in r.get("n15_fibres_tested", []))
    d["n_atypical"] = len(r.get("atypical", []))
    d["atypical_c"] = "|".join(a["c"] for a in r.get("atypical", []))
    d["chi_at_atypical"] = "|".join(str(a["chi"]) for a in r.get("atypical", []))
    d["n_components_at_atypical"] = "|".join(fmt(f.get("n_Qfactors")) for f in fs)
    d["component_degrees"] = "|".join(
        ",".join(str(z) for z in (f.get("Qfactor_degs") or [])) for f in fs)
    d["n_vertical_components"] = "|".join(fmt(f.get("n_vert")) for f in fs)
    d["exact_prim_verdict"] = "|".join(f.get("exact", {}).get("verdict", "") for f in fs)
    d["exact_prim_degF"] = "|".join(
        ",".join(str(cp.get("degF")) for cp in f.get("exact", {}).get("components", []))
        for f in fs)
    n = [f.get("num_on", {}) for f in fs]
    d["nummono_verdict_on"] = "|".join(str(z.get("verdict") or z.get("error", "")) for z in n)
    for tag, key in [("nummono_ls_residual_on", "ls_residual"),
                     ("nummono_max_period_on", "max_period"),
                     ("nummono_max_abs_residue_on", "max_abs_residue"),
                     ("nummono_sum_abs_residues_on", "sum_abs_residues"),
                     ("nummono_chi_on", "chi"), ("nummono_ncomp_on", "n_components"),
                     ("nummono_npunct_on", "n_punctures")]:
        d[tag] = "|".join(fmt(z.get(key)) for z in n)
    nr = fs[0].get("num_near", {}) if fs else {}
    d["near_c"] = "|".join(nr.keys())
    d["near_exact_chi"] = "|".join(fmt(v.get("exact_chi")) for v in nr.values())
    d["near_nummono_verdict"] = "|".join(
        fmt((v.get("num") or {}).get("verdict") or (v.get("num") or {}).get("error"))
        for v in nr.values())
    d["near_nummono_max_period"] = "|".join(
        fmt((v.get("num") or {}).get("max_period")) for v in nr.values())
    return d


with open("atypical.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    for r in R:
        w.writerow(row(r))

cnt = Counter(r["verdict"] for r in R)
still = [r["hash"] for r in R if r["verdict"] == "STILL-VANISHING"]
json.dump(still, open("still_vanishing16.json", "w"), indent=1)
print("rows", len(R), dict(cnt))
