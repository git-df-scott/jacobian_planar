"""night20 -- assemble the census and the per-object table into irreducible.csv."""
import sys, os, json, csv, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))

CENSUS = ["cert20.json", "cert2_20.json", "cert20b.json", "cert20c.json"]
MATES = ["mate20_pass1.json", "mate20_sel.json"]

rows = {}
for f in CENSUS:
    p = os.path.join(HERE, f)
    if not os.path.exists(p):
        continue
    for r in json.load(open(p)):
        old = rows.get(r["P"])
        if old is None or (not old.get("reducible_c") and r.get("reducible_c")):
            rows[r["P"]] = dict(r, source=f)
nm = 0
for f in MATES:
    p = os.path.join(HERE, f)
    if not os.path.exists(p):
        continue
    for r in json.load(open(p)):
        if r["P"] in rows:
            rows[r["P"]].update({k: v for k, v in r.items()
                                 if k.startswith(("mate", "lambda", "rational",
                                                  "certificate", "Q", "bracket",
                                                  "verified"))})
            nm += 1

COLS = ["P", "deg", "unimodular", "bezout_U", "bezout_V", "bezout_residual",
        "baker_interior_pts", "genus", "n_special_c", "reducible_c",
        "all_fibres_irreducible", "mate_verdict", "mate_top_D",
        "mate_deg_bound_multiple", "lambda_support", "lambda_verified",
        "certificate_id", "rational_mate_found", "rational_mate_poles",
        "rational_mate_denominators_tried", "source"]

out = os.path.join(HERE, "irreducible.csv")
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(COLS)
    for P in sorted(rows, key=lambda k: (rows[k]["deg"], k)):
        r = rows[P]
        w.writerow([str(r.get(c, "")) for c in COLS])

st = {"census": len(rows),
      "mate_solved": sum(1 for r in rows.values() if r.get("mate_verdict")),
      "unimodular": sum(1 for r in rows.values() if r.get("unimodular")),
      "genus>=1": sum(1 for r in rows.values() if (r.get("genus") or 0) >= 1),
      "all_fibres_irreducible": sum(1 for r in rows.values()
                                    if r.get("all_fibres_irreducible")),
      "triple_gate_targets": sum(1 for r in rows.values()
                                 if r.get("unimodular") and (r.get("genus") or 0) >= 1
                                 and r.get("all_fibres_irreducible")),
      "mate_EMPTY": sum(1 for r in rows.values() if r.get("mate_verdict") == "EMPTY"),
      "mate_MATE": sum(1 for r in rows.values() if r.get("mate_verdict") == "MATE"),
      "lambda_all_verified": all(r.get("lambda_verified") for r in rows.values()
                                 if r.get("mate_verdict") == "EMPTY"),
      "rational_mate_found": sum(1 for r in rows.values()
                                 if r.get("rational_mate_found")),
      "degrees": sorted(set(r["deg"] for r in rows.values())),
      "genera": sorted(set(r.get("genus") for r in rows.values() if r.get("genus"))),
      "n_reducible_fibres_histogram": {},
      }
h = {}
for r in rows.values():
    k = len(r.get("reducible_c", []) or [])
    h[k] = h.get(k, 0) + 1
st["n_reducible_fibres_histogram"] = h

# is the unique reducible value always c0 = P(0,0), i.e. exactly the fibre on
# which the Newton polygon of P - c loses its (0,0) vertex?
import sympy as _sp
_x, _y, _c = _sp.symbols('x y c')
agree = dis = comps = 0
compdist = {}
for r in rows.values():
    red = r.get("reducible_c") or []
    if len(red) != 1:
        continue
    m = _sp.Poly(_sp.sympify(red[0], locals={'c': _c}), _c)
    if m.degree() != 1:
        dis += 1
        continue
    c0 = list(_sp.roots(m))[0]
    P0 = _sp.sympify(r["P"], locals={'x': _x, 'y': _y}).subs({_x: 0, _y: 0})
    if _sp.simplify(c0 - P0) == 0:
        agree += 1
    else:
        dis += 1
    for row in r.get("fibre_rows", []):
        if row["m(c)"] == red[0]:
            compdist[row["abs_components"]] = compdist.get(row["abs_components"], 0) + 1
st["unique_reducible_value_equals_P(0,0)"] = agree
st["unique_reducible_value_other"] = dis
st["components_of_the_reducible_fibre"] = compdist
json.dump(st, open(os.path.join(HERE, "stats20.json"), "w"), indent=1)
print(json.dumps(st, indent=1))
