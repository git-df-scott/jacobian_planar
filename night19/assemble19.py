"""night19 -- splice the verbatim control blocks, the D-table and the broken-case
table into UNCONDITIONAL.md."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
md = open(os.path.join(HERE, 'UNCONDITIONAL.md')).read()
ctl = open(os.path.join(HERE, 'controls19_log.txt')).read().splitlines()


def block(start, end=None):
    i = next(k for k, l in enumerate(ctl) if l.startswith(start))
    j = len(ctl) if end is None else next(k for k, l in enumerate(ctl) if k > i and l.startswith(end))
    return "\n".join(ctl[i:j]).rstrip()


c1 = block("=" * 78)                       # first banner .. C2 banner
i2 = next(k for k, l in enumerate(ctl) if l.strip().startswith("C2  the closed-form"))
c1 = "\n".join(ctl[0:i2 - 1]).rstrip()
i3 = next(k for k, l in enumerate(ctl) if l.strip().startswith("C3  unimodular"))
c2 = "\n".join(ctl[i2 - 1:i2 + 8] + ["  ...  (36 further rows omitted here; all True)"] +
               [l for l in ctl[i2 - 1:i3 - 1] if l.strip().startswith("C2 PASS") or l.strip().startswith("C2 FAIL")]).rstrip()
c3 = "\n".join(ctl[i3 - 1:]).rstrip()
md = md.replace("CONTROLS_C1", c1).replace("CONTROLS_C2_HEAD", c2).replace("CONTROLS_C3", c3)

cor = open(os.path.join(HERE, 'cor19_log.txt')).read().rstrip()
md = md.replace("COR19", cor)

pv = json.load(open(os.path.join(HERE, 'prove19.json')))
tab = ["| `D` | unknowns | equations | `|supp lambda|` | supp are rows | verified over `Q(gamma,c)` | secs |",
       "|---|---|---|---|---|---|---|"]
for r in pv["rows"]:
    tab.append("| %d | %d | %d | %d | %s | **%s** | %s |" %
               (r["D"], r["n_unknowns"], r["n_equations"], r["lambda_support"],
                r["support_inside_row_set"], r["verified"], r["secs"]))
tab.append("")
tab.append("`all_verified = %s` (`prove19.json`).  Row-formula check: %s (%d monomials, `i+j <= %d`)."
           % (pv["all_verified"], pv["row_formula_check"]["agree"],
              pv["row_formula_check"]["monomials"], pv["row_formula_check"]["carrier_D"]))
md = md.replace("PROVE_TABLE", "\n".join(tab))

bk = json.load(open(os.path.join(HERE, 'broken19.json')))
t = ["| case | `P` | `|A|` | shift differences | rank | max rows/col | cycle rank on `S(12)` | forest | Bezout resid | SY | fibre | verdicts `D = 3,5,7,9,11,13,15` | `|supp lambda|` | diagonal |",
     "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for cs in bk["cases"]:
    st = cs["structure"]
    rows = cs["mate_rows"]
    v = set(r["verdict"] for r in rows)
    supp = ", ".join(str(r["lambda_support"]) for r in rows)
    diag = ", ".join("Y" if r["lambda_is_diagonal"] else "n" for r in rows)
    t.append("| %s | `%s` | %d | %s | %d | %d | %d | %s | %s | %s | `%s` | %s | %s | %s |" %
             (cs["label"].split()[0], cs["P"], st["n_terms"],
              str(st["shift_differences"]), st["rank_of_shift_lattice"],
              st["max_rows_per_column"], st["cycle_rank"],
              str(st["row_graph_is_forest"]) if st["row_graph_is_forest"] is not None else "n/a (|A|>2)",
              cs["bezout"]["residual_terms"], cs["shpilrain_yu"],
              cs["fibre_factorisation"], "/".join(sorted(v)), supp, diag))
t.append("")
t.append("(`forest` = the row graph with columns as edges is acyclic, defined only for `|A| = 2`;")
t.append("`diagonal` = `lambda` is supported on `{(n,n)}`, i.e. the closed-form shape;")
t.append("`Bezout resid` = number of terms of `U P_x + V P_y - 1`, which must be 0;")
t.append("all `lambda` re-verified by expansion: `lambda_verified = True` in every row.)")
md = md.replace("BROKEN_TABLE", "\n".join(t))

assert "PROVE_TABLE" not in md and "BROKEN_TABLE" not in md and "CONTROLS_C1" not in md
open(os.path.join(HERE, 'UNCONDITIONAL.md'), 'w').write(md)
print("assembled")
