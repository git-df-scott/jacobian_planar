"""night16 -- STILL_VANISHING.md: full data for the P that vanish at every
atypical value, plus the exact mate re-solve above night15's ceiling."""
import glob, json, os
import atyp16 as A, load16

R = json.load(open("atypical16.json"))
S = {r["hash"]: r for r in load16.survivors()}
MT = {}
for f in sorted(glob.glob("mate16_*.json")):
    for z in json.load(open(f)):
        prev = MT.get(z["hash"])
        if prev is None or (prev["verdict"] != "EMPTY_all_stages"
                            and z["verdict"] == "EMPTY_all_stages"):
            MT[z["hash"]] = z

L = []
L.append("# night16 — STILL-VANISHING at every atypical value\n")
L.append("Measurements only.\n")
L.append("These are the `P` from night15's 57 PERIODS-VANISHING survivors for which")
L.append("EXACT-PRIM returns a verified primitive on **every component of every**")
L.append("**atypical fibre**, so that every period of `eta = dy/P_x` over every cycle")
L.append("of every atypical fibre vanishes exactly.  Together with night15's generic-")
L.append("fibre screen this is the strongest necessary condition the campaign has.\n")
L.append("The last section of `ATYPICAL.md` records the one row where that picture")
L.append("changes for an unrelated reason: `808e52fdb1b6` is obstructed at its")
L.append("GENERIC fibres, which night15 never sampled (it measured only c = 1 and")
L.append("c = -1, both of which are atypical values of that P).\n")
L.append("| # | hash | deg P | night15 label |")
L.append("|---|---|---|---|")
for i, r in enumerate(R):
    L.append("| %d | `%s` | %d | `%s` |" % (i + 1, r["hash"], r["deg_P"], r["label"]))
L.append("")
L.append("---\n")
for i, r in enumerate(R):
    h = r["hash"]
    rec = S[h]
    Pe = A.dict_to_expr(load16.Pdict(rec))
    L.append("## %d. `%s`\n" % (i + 1, h))
    L.append("```")
    L.append("P            = %s" % Pe)
    L.append("night15 label= %s" % r["label"])
    L.append("deg P        = %d      deg_y P = %d" % (r["deg_P"], r["deg_y"]))
    L.append("unimodular   : %s (%s)" % (rec["U"]["U"], rec["U"]["reason"]))
    L.append("non-coordinate: SY = %s, FIB = %s" % (rec["SY"], rec["FIB"]))
    L.append("night15 instrument = %s, fibres it measured = %s"
             % (r.get("n15_instrument"), r.get("n15_fibres_tested")))
    L.append("chi_gen      = %d   (votes %s, at c = %s)"
             % (r["chi_gen"], r["chi_gen_votes"], r["generic_c"]))
    L.append("candidates tested: %s" % (r["candidates_tested"],))
    if r.get("untested_algebraic_candidates"):
        L.append("untested algebraic candidates: %s"
                 % [(u["deg"], u["minpoly"]) for u in r["untested_algebraic_candidates"]])
    j = sum(a["chi"] - r["chi_gen"] for a in r["atypical"])
    L.append("Suzuki accounting: sum of jumps = %d, required 1 - chi_gen = %d, closes = %s"
             % (j, 1 - r["chi_gen"], j == 1 - r["chi_gen"]))
    for f in r["fibres"]:
        L.append("")
        L.append("  atypical c = %s   chi(F_c) = %d  (jump %+d)"
                 % (f["c"], f["chi"], f["chi"] - r["chi_gen"]))
        L.append("    components over Q: %s, degrees %s, vertical lines %s"
                 % (f.get("n_Qfactors"), f.get("Qfactor_degs"), f.get("n_vert")))
        ex = f.get("exact", {})
        L.append("    EXACT-PRIM: %s" % ex.get("verdict"))
        for cp in ex.get("components", []):
            L.append("      h = %s" % cp.get("h"))
            L.append("        F = %s   deg F = %s   verified: %s"
                     % (cp.get("F"), cp.get("degF"), cp.get("witness")))
        z = f.get("num_on", {})
        if z.get("verdict"):
            L.append("    NUM-MONO on F_c: %s  ls_residual=%.3g (err %.3g)  max_period=%.3g"
                     "  chi=%s  components=%s  punctures=%s  max|residue|=%s  sum residues=%s%s"
                     % (z["verdict"], z.get("ls_residual") or 0,
                        z.get("err_ls_residual") or 0, z.get("max_period") or 0,
                        z.get("chi"), z.get("n_components"), z.get("n_punctures"),
                        z.get("max_abs_residue"), z.get("sum_abs_residues"),
                        "  [second pass, larger budget]" if z.get("retry") else ""))
        else:
            L.append("    NUM-MONO on F_c: did not complete within the wall-clock budget")
        L.append("    nearby generic c (exact chi | EXACT-PRIM | deg F):")
        for k, v in f.get("num_near", {}).items():
            L.append("      c = %-10s chi = %-4s  %s  %s"
                     % (k, v.get("exact_chi"), v.get("exact_periods"), v.get("degF")))
    m = MT.get(h)
    if m:
        L.append("")
        L.append("  exact mate re-solve above night15's ceiling (deg Q = 2 deg P):")
        for st in m["stages"]:
            L.append("    D = %-4s n_unknowns = %-6s %-18s %s  lambda support %s "
                     "re-verified %s  (%ss)"
                     % (st.get("deg_Q_bound"), st.get("n_unknowns"), st.get("verdict"),
                        st.get("certificate"), st.get("lambda_support"),
                        st.get("lambda_reverified"), st.get("secs")))
        L.append("    overall: %s" % m["verdict"])
    L.append("```\n")
open("STILL_VANISHING.md", "w").write("\n".join(L))
print("wrote STILL_VANISHING.md,", len(R), "entries;", len(MT), "mate records")
