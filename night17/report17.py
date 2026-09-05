"""night17 -- render the per-support and per-instance markdown tables."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "records17.json")))
S, RS = D["supports"], D["records"]
by_sup = {}
for r in RS:
    by_sup.setdefault(r["support"], []).append(r)

L = []
L.append("### 4.1 Per support: system size, solution structure, survivors\n")
L.append("| support | shape | unknowns | residue equations | solution structure |"
         " instances | survivors |")
L.append("|---|---|---|---|---|---|---|")
for s in S:
    ins = by_sup.get(s["id"], [])
    st = s["structure"].get("structure", "")
    if s["structure"].get("gb_size"):
        st += " (Groebner basis of %d elements)" % s["structure"]["gb_size"]
    for k in s:
        if k.startswith("groebner_empty"):
            st = ("UNIT IDEAL with %s adjoined: NO SOLUTIONS"
                  % k[len("groebner_empty_with_"):].replace("_", " ")
                  if s[k] else st + "; solvable with " +
                  k[len("groebner_empty_with_"):].replace("_", " "))
    eqs = s["equations"]
    eqtxt = "none (every point of the support solves)" if not eqs else \
        "; ".join(e[:70] + (" ..." if len(e) > 70 else "") for e in eqs[:3]) + \
        (" ... (%d total)" % len(eqs) if len(eqs) > 3 else "")
    L.append("| %s | %s | %d | %s | %s | %d | %d |" %
             (s["id"], s["label"], s["n_unknowns"], eqtxt, st[:150], len(ins),
              sum(bool(r["survivor"]) for r in ins)))

L.append("")
L.append("### 4.2 Per instance: certificates and mate verdicts\n")
L.append("| support | id | deg | deg_y | screen | genus | punctures | Bezout |"
         " SY | survivor | mate | NUM-MONO rel |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in RS:
    sc = r["screen"]
    num = r.get("numeric_NUM_MONO", {}) or {}
    rels = [v["rel"] for v in num.values() if isinstance(v, dict) and "rel" in v]
    st = ";".join("D=%s:%s" % (x.get("deg_Q_bound"), str(x.get("verdict"))[:16])
                  for x in r.get("mate", {}).get("stages", []))
    L.append("| %s | `%s` | %d | %d | %s | %s | %s | %s (%s) | %s | %s | %s | %s |"
             % (r["support"], r["hash"], r["deg"], r["deg_y"],
                sc.get("verdict", ""), sc.get("genus", "-"),
                sc.get("n_punctures", "-"),
                "OK residual 0" if r["unimodular"] == "UNIMODULAR_CERTIFIED"
                else r["unimodular"], r.get("bezout_method"), r["sy"],
                "yes" if r["survivor"] else "no",
                st or "-", "%.1e" % max(rels) if rels else "-"))

L.append("")
L.append("### 4.3 The synthesised P (survivors)\n")
for r in RS:
    if r["survivor"]:
        L.append("* `%s`  (support %s, degree %d) — `P = %s`" %
                 (r["hash"], r["support"], r["deg"], r["P"]))
open(os.path.join(HERE, "tables17.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:8]))
print("...\ninstances %d survivors %d supports %d" %
      (len(RS), sum(bool(r["survivor"]) for r in RS), len(S)))
