"""night16 -- the atypical re-screen of night15's 57 PERIODS-VANISHING survivors.

For each P:  (1) exact atypical-value detector (atyp16),
             (2) EXACT-PRIM on every atypical fibre (period16),
             (3) NUM-MONO on the atypical fibre and at two nearby generic c.
"""
import json, os, sys, time, traceback
from fractions import Fraction as Fr
import sympy as sp

import atyp16 as A
import period16 as PR
import mono16 as M
import load16

OUTJ = "atypical16.json"
BUDGET = 40.0
EPS = [Fr(1, 8), Fr(-1, 8), Fr(1, 64), Fr(-1, 64)]

import signal


class TO(Exception):
    pass


def _alarm(sig, frm):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)


def exact_with_timeout(Pe, cval, secs=180, Dmax=6):
    signal.alarm(secs)
    try:
        return PR.exact_periods_vanish(Pe, cval, Dmax=Dmax)
    except TO:
        return {"verdict": "TIMEOUT", "secs": secs}
    except Exception as ex:
        return {"verdict": "ERROR", "err": "%s: %s" % (type(ex).__name__, ex)}
    finally:
        signal.alarm(0)


def numrun(Pd, c):
    t0 = time.time()
    try:
        r = M.screen_fibre_checked(Pd, c, tol=1e-6, nsub=6, ncirc=48, budget=BUDGET)
    except Exception as e:
        return {"error": "%s: %s" % (type(e).__name__, e), "t": time.time() - t0}
    if "error" in r:
        return {"error": r["error"], "t": time.time() - t0}
    inf = r.get("infinity", {})
    return {"verdict": r.get("verdict"), "ls_residual": r.get("ls_residual"),
            "rel_ls_residual": r.get("rel_ls_residual"),
            "max_period": r.get("max_period"),
            "err_ls_residual": r.get("err_ls_residual"),
            "n_components": r.get("n_components"), "chi": r.get("chi"),
            "n_punctures": r.get("n_punctures"), "genus_sum": r.get("genus_sum"),
            "n_cycles": r.get("n_independent_cycles_found"),
            "max_abs_residue": inf.get("max_abs_residue"),
            "sum_abs_residues": inf.get("sum_abs"),
            "n_places_total": inf.get("n_places_total"),
            "t": round(time.time() - t0, 1)}


def one(rec):
    Pd = load16.Pdict(rec)
    Pe = A.dict_to_expr(Pd)
    out = {"hash": rec["hash"], "label": rec["label"], "deg_P": rec["deg_P"],
           "deg_y": rec["deg_y"], "n15_instrument": rec["period_detail"].get("instrument",
                                  "EXACT-G1" if "exact_g1" in rec["period_detail"] else "EXACT-HE"),
           "n15_fibres_tested": [f.get("c") for f in rec["period_detail"].get("fibres", [])]}
    t0 = time.time()
    det = A.atypical(Pe)
    out["chi_gen"] = det["chi_gen"]
    out["chi_gen_votes"] = det["chi_gen_votes"]
    out["generic_c"] = det["generic_c"]
    out["generic_chi"] = det["generic_chi"]
    out["candidates_tested"] = [(t["c"], t["chi"]) for t in det["tested"]]
    out["atypical"] = [{"c": a["c"], "kind": a["kind"], "chi": a["chi"]} for a in det["atypical"]]
    out["t_detect"] = round(time.time() - t0, 1)

    fib = []
    for a in det["atypical"]:
        e = {"c": a["c"], "kind": a["kind"], "chi": a["chi"], "chi_gen": det["chi_gen"]}
        if a["kind"] != "rational":
            e["exact"] = {"verdict": "NOT_ATTEMPTED_ALGEBRAIC_c"}
            fib.append(e); continue
        c0 = sp.Rational(a["c"])
        det0 = a["detail"]
        e["n_vert"] = det0.get("n_vert")
        e["n_Qfactors"] = det0.get("n_Qfactors")
        e["Qfactor_degs"] = det0.get("Qfactor_degs")
        t1 = time.time()
        e["exact"] = exact_with_timeout(Pe, c0)
        e["t_exact"] = round(time.time() - t1, 1)
        e["num_on"] = numrun(Pd, Fr(int(c0.p), int(c0.q)))
        near = {}
        for eps in EPS:
            cn = Fr(int(c0.p), int(c0.q)) + eps
            cq = sp.Rational(cn.numerator, cn.denominator)
            d = {}
            try:
                d["exact_chi"] = A.chi_fibre(Pe, cq)["chi"]
            except Exception as ex:
                d["exact_chi"] = None
            ee = exact_with_timeout(Pe, cq, secs=180)
            d["exact_periods"] = ee.get("verdict")
            d["degF"] = [cp.get("degF") for cp in ee.get("components", [])]
            near[str(cn)] = d
        e["num_near"] = near
        fib.append(e)
    out["fibres"] = fib

    ok = all(f.get("exact", {}).get("verdict") == "VANISHING_EXACT" for f in fib)
    obstructed = any(f.get("num_on", {}).get("verdict") == "NONVANISHING" for f in fib)
    if not fib:
        out["verdict"] = "NO_ATYPICAL_VALUE"
    elif obstructed:
        out["verdict"] = "NEWLY-OBSTRUCTED"
    elif ok:
        out["verdict"] = "STILL-VANISHING"
    else:
        out["verdict"] = "UNRESOLVED"
    out["t_total"] = round(time.time() - t0, 1)
    return out


def main():
    S = load16.survivors()
    done = {}
    if os.path.exists(OUTJ):
        done = {r["hash"]: r for r in json.load(open(OUTJ))}
    res = []
    for i, rec in enumerate(S):
        if rec["hash"] in done:
            res.append(done[rec["hash"]]); continue
        try:
            r = one(rec)
        except Exception as ex:
            r = {"hash": rec["hash"], "label": rec["label"], "deg_P": rec["deg_P"],
                 "deg_y": rec["deg_y"], "verdict": "ERROR",
                 "err": traceback.format_exc()[-800:]}
        res.append(r)
        print("[%2d/57] %s deg=%2d dy=%2d chi_gen=%s atyp=%s -> %s (%.0fs)"
              % (i + 1, r["hash"], r["deg_P"], r["deg_y"], r.get("chi_gen"),
                 [a["c"] for a in r.get("atypical", [])], r["verdict"],
                 r.get("t_total", 0)), flush=True)
        json.dump(res, open(OUTJ, "w"), indent=1, default=str)
    json.dump(res, open(OUTJ, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
