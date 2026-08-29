"""night15 -- the deliverable table: night15/period_screen.csv."""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(os.path.join(HERE, "screen15_records.json")))
mates = {m["hash"]: m for m in json.load(open(os.path.join(HERE, "survivors15.json")))}
top = {}
p = os.path.join(HERE, "topup15.json")
if os.path.exists(p):
    top = {t["hash"]: t for t in json.load(open(p))}

COLS = ["hash", "label", "deg_P", "deg_y", "n_terms", "species_measured",
        "U_bezout_identity", "U_residual_terms", "U_deg_A", "U_deg_B",
        "SY_verdict", "FIB_witness", "max_fibre_components",
        "period_instrument", "places_at_infinity", "genus", "period_case",
        "period_value", "period_witness", "period_verdict",
        "mate_verdict", "mate_max_deg_Q", "mate_certificate",
        "mate_lambda_support", "mate_lambda_reverified"]


def species(r, d, g1, f0):
    out = []
    m = r["meta"]
    if m.get("m") == 2:
        out.append("v-quadratic")
    if m.get("m") == 3:
        out.append("S1_v_cubic")
    if m.get("m", 0) >= 4:
        out.append("v_power_m%d" % m["m"])
    if m.get("gen") == "G2":
        out.append("G2_multiple_root")
    pl = g1.get("n_places_at_infinity", f0.get("n_punctures"))
    if (pl or 0) >= 3:
        out.append("S2_ge3_places")
    gg = g1.get("genus", f0.get("genus_sum"))
    if (gg or 0) >= 1:
        out.append("S3_positive_genus")
    fd = r.get("FIB_detail")
    nf = max([x.get("nfac") or 0 for x in fd] + [0]) if isinstance(fd, list) else 0
    if nf >= 3:
        out.append("S4_ge3_components")
    if m.get("sheared"):
        out.append("S5_mixed_support")
    return "|".join(out), nf


rows = []
for r in recs:
    d = r.get("period_detail", {})
    g1 = d.get("exact_g1", {})
    fl = d.get("fibres") or []
    f0 = fl[0].get("res", {}) if fl else {}
    sp, nf = species(r, d, g1, f0)
    val = witness = case = ""
    if g1:
        case = g1.get("case", "")
        witness = g1.get("witness", "")
        val = "residues nonzero" if g1.get("residues_at_y0_nonzero") else "0"
    for f in fl:
        res = f.get("res", {})
        if res.get("verdict") == "NONVANISHING" or res.get("max_abs_residue"):
            case = case or res.get("case", "")
            witness = witness or res.get("witness", "")
            if res.get("max_abs_residue") is not None:
                val = "max|Res| = %s" % res["max_abs_residue"]
            elif res.get("ls_residual") is not None:
                val = "ls_residual = %.6g (err %.1g)" % (res["ls_residual"],
                                                         res.get("err_ls_residual", 0))
            break
    else:
        if fl and "ls_residual" in f0:
            val = "ls_residual = %.6g (err %.1g)" % (f0["ls_residual"],
                                                     f0.get("err_ls_residual", 0))
        elif fl and f0.get("residues") is not None:
            val = "residues %s" % f0.get("residues")
    m = mates.get(r["hash"])
    mv = mmax = mc = msup = mre = ""
    if m:
        mv = m["verdict"]
        st = [s for s in m["stages"] if s.get("verdict") == "EMPTY_over_Q"]
        if r["hash"] in top and top[r["hash"]]["verdict"] == "EMPTY_over_Q":
            st = st + [top[r["hash"]]]
            mv = "EMPTY_all_stages"
        if st:
            last = st[-1]
            mmax = last.get("deg_Q_bound")
            mc = last.get("certificate")
            msup = last.get("lambda_support")
            mre = last.get("lambda_reverified")
    u = r.get("U", {})
    rows.append([r["hash"], r["label"], r["deg_P"], r["deg_y"], r["n_terms"], sp,
                 u.get("U"), u.get("residual_terms"), u.get("deg_A"), u.get("deg_B"),
                 r.get("SY"), r.get("FIB"), nf,
                 d.get("instrument"),
                 g1.get("n_places_at_infinity", f0.get("n_punctures")),
                 g1.get("genus", f0.get("genus_sum")), case, val, witness,
                 r.get("period_verdict"), mv, mmax, mc, msup, mre])

with open(os.path.join(HERE, "period_screen.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(COLS)
    w.writerows(rows)
print("wrote period_screen.csv:", len(rows), "rows")
