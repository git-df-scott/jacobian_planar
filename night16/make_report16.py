"""night16 -- assemble ATYPICAL.md and atypical.csv from the run records."""
import csv, glob, json, os
from collections import Counter

R = []
for f in sorted(glob.glob("atypical16_*.json")):
    R.extend(json.load(open(f)))
RT = []
for f in sorted(glob.glob("numretry16_*.json")):
    RT.extend(json.load(open(f)))
RTD = {(z["hash"], z["c"]): z for z in RT}
for r in R:
    for fb in r.get("fibres", []):
        key = (r["hash"], fb.get("c"))
        if key in RTD and fb.get("num_on", {}).get("verdict") is None:
            z = dict(RTD[key]); z["retry"] = True
            fb["num_on"] = z

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
        "near_c", "near_exact_chi", "near_exact_periods", "near_exact_degF",
        "suzuki_jump_sum", "suzuki_required", "suzuki_closes",
        "untested_algebraic_candidates", "detector_orientation", "verdict"]


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
    d["near_exact_periods"] = "|".join(fmt(v.get("exact_periods")) for v in nr.values())
    d["near_exact_degF"] = "|".join(
        ",".join(str(z) for z in (v.get("degF") or [])) for v in nr.values())
    j = sum(a["chi"] - r["chi_gen"] for a in r.get("atypical", []))
    d["suzuki_jump_sum"] = j
    d["suzuki_required"] = 1 - r["chi_gen"]
    d["suzuki_closes"] = (j == 1 - r["chi_gen"])
    d["untested_algebraic_candidates"] = "|".join(
        "deg %d: %s" % (u["deg"], u["minpoly"])
        for u in r.get("untested_algebraic_candidates", []))
    d["detector_orientation"] = r.get("detector_orientation", "as given")
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

# ------------------------------------------------------------------- ATYPICAL.md
def md_table(R):
    L = []
    L.append("| # | hash | deg P | deg_y | chi_gen | atypical c | chi(F_c) | jump | "
             "components of F_c (degrees) | EXACT-PRIM on F_c (deg F per component) | "
             "NUM-MONO on F_c: ls-residual / max period / max residue | "
             "nearby generic c: exact chi | verdict |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(R):
        fs = r.get("fibres", [])
        ac = "; ".join(a["c"] for a in r["atypical"]) or "NONE"
        ch = "; ".join(str(a["chi"]) for a in r["atypical"]) or "-"
        jp = "; ".join(str(a["chi"] - r["chi_gen"]) for a in r["atypical"]) or "-"
        comp = "; ".join("%s (%s)" % (f.get("n_Qfactors"),
                                      ",".join(str(z) for z in (f.get("Qfactor_degs") or [])))
                         for f in fs)
        ep = "; ".join("%s [%s]" % (f.get("exact", {}).get("verdict", ""),
                                    ",".join(str(cp.get("degF"))
                                             for cp in f.get("exact", {}).get("components", [])))
                       for f in fs)
        nm = []
        for f in fs:
            z = f.get("num_on", {})
            if z.get("verdict"):
                nm.append("%s %.2g / %.2g / %.2g" % (z["verdict"], z.get("ls_residual") or 0,
                                                     z.get("max_period") or 0,
                                                     z.get("max_abs_residue") or 0))
            else:
                nm.append("budget exceeded")
        nr = fs[0].get("num_near", {}) if fs else {}
        near = "; ".join("%s:%s" % (k, v.get("exact_chi")) for k, v in nr.items())
        L.append("| %d | `%s` | %d | %d | %d | %s | %s | %s | %s | %s | %s | %s | **%s** |"
                 % (i + 1, r["hash"], r["deg_P"], r["deg_y"], r["chi_gen"], ac, ch, jp,
                    comp, ep, " ; ".join(nm), near, r["verdict"]))
    return "\n".join(L)


head = open("ATYPICAL_head.md").read()
mid = open("ATYPICAL_mid.md").read()
tail = open("ATYPICAL_tail.md").read() if os.path.exists("ATYPICAL_tail.md") else ""
ctl = "\n```\n" + open("controls16_log.txt").read().rstrip() + "\n```\n"
ctl += "\n```\n" + open("controls16b_log.txt").read().rstrip() + "\n```\n"
MT = {}
for f in sorted(glob.glob("mate16_*.json")):
    for z in json.load(open(f)):
        prev = MT.get(z["hash"])
        if prev is None or (prev["verdict"] != "EMPTY_all_stages"
                            and z["verdict"] == "EMPTY_all_stages"):
            MT[z["hash"]] = z
ML = []
ML.append("| # | hash | deg P | carriers D tried (night15 stopped at D = 2 deg P) | "
          "n unknowns | verdict | certificate | lambda support | lambda re-verified over Q |")
ML.append("|---|---|---|---|---|---|---|---|---|")
nemp = nnc = 0
for i, r in enumerate(R):
    z = MT.get(r["hash"])
    if not z:
        ML.append("| %d | `%s` | %d | - | - | NOT RUN | | | |" % (i + 1, r["hash"], r["deg_P"]))
        continue
    nemp += z["verdict"] == "EMPTY_all_stages"
    nnc += z["verdict"] != "EMPTY_all_stages"
    ML.append("| %d | `%s` | %d | %s | %s | %s | %s | %s | %s |"
              % (i + 1, r["hash"], r["deg_P"],
                 ", ".join(str(s0.get("deg_Q_bound")) for s0 in z["stages"]),
                 ", ".join(str(s0.get("n_unknowns")) for s0 in z["stages"]),
                 z["verdict"],
                 ", ".join(str(s0.get("certificate")) for s0 in z["stages"]),
                 ", ".join(str(s0.get("lambda_support")) for s0 in z["stages"]),
                 ", ".join(str(s0.get("lambda_reverified")) for s0 in z["stages"])))
summ = ("\n**%d of %d came back `EMPTY_over_Q` at every carrier tried, each with an "
        "exact rational lambda certificate re-verified over Q. %d are `NOT_CERTIFIED` "
        "(prime-relative only; never reported as emptiness).**\n\n"
        "Four of the rows (`a814ad47ed0c`, `96e4a2c6d1d3`, `282a9f40c368`, "
        "`cf1c601f3d1c`, all of degree 20 or 24) first came back `NOT_CERTIFIED` "
        "because their carriers (903 to 1326 unknowns) exceeded the exact-lambda "
        "solver's default size cap of 900, even though the system was already "
        "inconsistent at the scheduling prime (rank_p[A|e] = rank_p(A) + 1).  They were "
        "re-run with the cap raised to 1600 and all four then produced exact lambda "
        "certificates, re-verified over Q (lambda supports of 326 to 728 rows; 244 to "
        "1891 seconds per carrier).\n\n"
        "**No system was consistent at any carrier: the HIT GATE did not fire.**\n"
        % (nemp, nemp + nnc, nnc))
open("ATYPICAL.md", "w").write(head + ctl + mid + "\n" + md_table(R) + "\n" + tail
                               + "\n".join(ML) + "\n" + summ)
print("wrote ATYPICAL.md")
