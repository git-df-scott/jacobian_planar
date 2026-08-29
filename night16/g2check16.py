"""night16 -- follow-up measurement on 808e52fdb1b6.

The detector found that BOTH fibres night15 measured for this P (c = 1 and
c = -1) are ATYPICAL values of it, so its night15 PERIODS-VANISHING verdict
rests on no generic fibre at all.  This script measures generic fibres.
"""
import json
from fractions import Fraction as Fr
import sympy as sp
import atyp16 as A, mono16 as M, period16 as PR, load16

H = "808e52fdb1b6"
rec = {r["hash"]: r for r in load16.survivors()}[H]
Pd = load16.Pdict(rec)
Pe = A.dict_to_expr(Pd)
out = {"hash": H, "P": str(Pe), "label": rec["label"],
       "night15_fibres": [f.get("c") for f in rec["period_detail"]["fibres"]],
       "rows": []}
print("P =", Pe)
print("night15 measured only c =", out["night15_fibres"],
      "-- both are atypical values of this P")
for c in (3, 5, -3, 2, sp.Rational(1, 2)):
    cq = sp.Rational(c)
    d = A.chi_fibre(Pe, cq, extra=True)
    r = M.screen_fibre_checked(Pd, Fr(cq.p, cq.q), tol=1e-6, nsub=6, ncirc=48,
                               budget=600.0)
    e = PR.exact_periods_vanish(Pe, cq, Dmax=8)
    row = {"c": str(cq), "exact_chi": d["chi"], "n_Qfactors": d["n_Qfactors"],
           "nummono_verdict": r.get("verdict"), "error": r.get("error"),
           "ls_residual": r.get("ls_residual"),
           "rel_ls_residual": r.get("rel_ls_residual"),
           "err_ls_residual": r.get("err_ls_residual"),
           "max_period": r.get("max_period"),
           "err_max_period": r.get("err_max_period"),
           "nummono_chi": r.get("chi"), "n_components": r.get("n_components"),
           "n_punctures": r.get("n_punctures"), "genus_sum": r.get("genus_sum"),
           "max_abs_residue": (r.get("infinity") or {}).get("max_abs_residue"),
           "sum_abs_residues": (r.get("infinity") or {}).get("sum_abs"),
           "exact_prim": e["verdict"],
           "exact_prim_degF": [cp.get("degF") for cp in e["components"]]}
    out["rows"].append(row)
    print(json.dumps(row), flush=True)
json.dump(out, open("g2check16.json", "w"), indent=1, default=str)
