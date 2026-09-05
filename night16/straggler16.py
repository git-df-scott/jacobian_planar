"""night16 -- the eight high-degree sheared survivors.

chi(F_c) is an invariant of the fibre, and the detector computes it by
projecting to one of the two coordinate axes; the swap (x,y) -> (y,x) is a
relabelling of C^2 that changes no fibre and no chi.  For these eight P the
y-degree and the x-degree differ, so the detector is run in whichever
orientation has the SMALLER projection degree (the resultant Res_y(f, f_y)
over Q[x,c] is what costs; its size is governed by that degree).  Both
orientations are run when both are affordable, as an internal cross-check.

EXACT-PRIM and NUM-MONO are then run on the ORIGINAL P, unswapped.
"""
import json, os, sys, time
from fractions import Fraction as Fr
import sympy as sp
import atyp16 as A, period16 as PR, mono16 as M, load16
import screen16 as S16

x, y = A.x, A.y
HASHES = ["11b99f22adf6", "d57b38902c84", "96e4a2c6d1d3", "c689ce7fc834",
          "4667d741b2d6", "282a9f40c368", "b7612f47cd64", "cf1c601f3d1c"]
k, n = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 1)
OUT = "atypical16_s%d.json" % k
S = {r["hash"]: r for r in load16.survivors()}
res = json.load(open(OUT)) if os.path.exists(OUT) else []
done = {r["hash"] for r in res}

for idx, h in enumerate(HASHES):
    if idx % n != k or h in done:
        continue
    rec = S[h]
    Pd = load16.Pdict(rec)
    Pe = A.dict_to_expr(Pd)
    dy_ = max(j for i, j in Pd)
    dx_ = max(i for i, j in Pd)
    swap = dx_ < dy_
    Pdet = sp.expand(Pe.subs({x: sp.Symbol('T'), y: x}).subs({sp.Symbol('T'): y})) if swap else Pe
    t0 = time.time()
    det = A.atypical(Pdet)
    out = {"hash": h, "label": rec["label"], "deg_P": rec["deg_P"], "deg_y": rec["deg_y"],
           "deg_x": dx_, "detector_orientation": "y<->x swapped" if swap else "as given",
           "n15_instrument": "EXACT-G1",
           "n15_fibres_tested": [f.get("c") for f in rec["period_detail"].get("fibres", [])],
           "chi_gen": det["chi_gen"], "chi_gen_votes": det["chi_gen_votes"],
           "generic_c": det["generic_c"], "generic_chi": det["generic_chi"],
           "candidates_tested": [(t["c"], t["chi"]) for t in det["tested"]],
           "atypical": [{"c": a["c"], "kind": a["kind"], "chi": a["chi"]} for a in det["atypical"]],
           "suzuki_jump_sum": det["suzuki_jump_sum"],
           "suzuki_required": det["suzuki_required"],
           "suzuki_closes": det["suzuki_closes"],
           "untested_algebraic_candidates": det["untested_algebraic_candidates"],
           "t_detect": round(time.time() - t0, 1)}
    fib = []
    for a in det["atypical"]:
        e = {"c": a["c"], "kind": a["kind"], "chi": a["chi"], "chi_gen": det["chi_gen"]}
        if a["kind"] != "rational":
            e["exact"] = {"verdict": "NOT_ATTEMPTED_ALGEBRAIC_c"}
            fib.append(e); continue
        c0 = sp.Rational(a["c"])
        e["n_vert"] = a["detail"].get("n_vert")
        d0 = A.chi_fibre(Pe, c0, extra=True)
        e["n_Qfactors"] = d0.get("n_Qfactors"); e["Qfactor_degs"] = d0.get("Qfactor_degs")
        e["chi_unswapped_recheck"] = d0["chi"]
        t1 = time.time()
        e["exact"] = S16.exact_with_timeout(Pe, c0, secs=1800)
        e["t_exact"] = round(time.time() - t1, 1)
        e["num_on"] = S16.numrun(Pd, Fr(int(c0.p), int(c0.q)), budget=300.0)
        near = {}
        for eps in (Fr(1, 8), Fr(-1, 8), Fr(1, 64), Fr(-1, 64)):
            cn = Fr(int(c0.p), int(c0.q)) + eps
            cq = sp.Rational(cn.numerator, cn.denominator)
            d = {}
            try:
                d["exact_chi"] = A.chi_fibre(Pdet, cq)["chi"]
            except Exception:
                d["exact_chi"] = None
            ee = S16.exact_with_timeout(Pe, cq, secs=600)
            d["exact_periods"] = ee.get("verdict")
            d["degF"] = [cp.get("degF") for cp in ee.get("components", [])]
            near[str(cn)] = d
        e["num_near"] = near
        fib.append(e)
    out["fibres"] = fib
    ok = all(f.get("exact", {}).get("verdict") == "VANISHING_EXACT" for f in fib)
    obstructed = any(f.get("num_on", {}).get("verdict") == "NONVANISHING" for f in fib)
    out["verdict"] = ("NO_ATYPICAL_VALUE" if not fib else
                      "NEWLY-OBSTRUCTED" if obstructed else
                      "STILL-VANISHING" if ok else "UNRESOLVED")
    out["t_total"] = round(time.time() - t0, 1)
    res.append(out)
    json.dump(res, open(OUT, "w"), indent=1, default=str)
    print("[s] %s deg=%2d dy=%2d dx=%2d %s chi_gen=%s atyp=%s -> %s (%.0fs)"
          % (h, rec["deg_P"], dy_, dx_, out["detector_orientation"], out["chi_gen"],
             [a["c"] for a in out["atypical"]], out["verdict"], out["t_total"]), flush=True)
