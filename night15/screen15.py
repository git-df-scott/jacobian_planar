"""night15 -- the period screen at scale, plus the exact mate solve on survivors.

For every P in gen15.corpus():
  1. U   : exact Bezout certificate  A P_x + B P_y = 1  (cert15)
  2. SY  : Shpilrain-Yu verdict, must be NON_COORDINATE (sy15)
  3. FIB : an independent non-coordinate witness on the fibres (fib15)
  4. the period screen on several fibres:
        deg_y P == 2  ->  EXACT-HE, closed form, exact over Q(sqrt(.))
        deg_y P >= 3  ->  NUM-MONO, numerical monodromy periods
  5. partition into PERIODS-NONVANISHING / PERIODS-VANISHING
Survivors go to mate15 for the exact mate solve.
"""

import json
import os
import sys
import time
from fractions import Fraction as F

import pk15 as P14
import cert15
import sy15
import fib15
import exact_he15
import mono15
import gen15
import exact_g1_15

HERE = os.path.dirname(os.path.abspath(__file__))
CS_EXACT = [F(1), F(-1), F(3, 2), F(0), F(2), F(-3, 5)]
CS_NUM = [F(1), F(-1)]
_DEFERRED_CACHE = {}


def deg_y(P):
    return max(j for (i, j) in P)


def period_screen(P, meta, num_budget=44, num_timeout_note=None):
    """Returns (verdict, detail).  verdict in NONVANISHING / VANISHING /
    NOT_SCREENED / UNRESOLVED."""
    dy = deg_y(P)
    det = {"deg_y": dy, "fibres": []}

    # ---- EXACT-G1 covers the whole v-power family in closed form --------
    if meta.get("gen") == "G1" and meta.get("m", 0) >= 2:
        g1 = exact_g1_15.screen(meta["n"], meta["m"])
        det["exact_g1"] = g1
        if g1.get("verdict") in ("NONVANISHING", "VANISHING"):
            det["instrument"] = "EXACT-G1"
            # cross-check against EXACT-HE on the deg_y = 2 members
            if dy == 2:
                agree = []
                for c in CS_EXACT[:3]:
                    he = exact_he15.screen(P, c)
                    det["fibres"].append({"c": str(c), "res": he})
                    agree.append(he.get("verdict") == g1["verdict"])
                det["exact_he_agrees"] = all(agree)
            return g1["verdict"], det
        det["exact_g1_deferred"] = True
        # The deferred case is decided ONCE per (n, m).  After the shears of
        # G3 the member is P = h0 y + c x^n y^m; the further Jacobian-1 map
        # (x, y) -> (alpha x, y/alpha) and an overall scaling of P (which
        # scales eta and relabels the fibres, leaving vanishing untouched)
        # normalise it to y + x^n y^m.  So the verdict on lam != 0 depends only
        # on (n, m), and one NUM-MONO run on the normal form settles all of
        # them.  Both fibres c = 1, -1 are run.
        key = (meta["n"], meta["m"])
        if key not in _DEFERRED_CACHE:
            nf = {(0, 1): F(1), (key[0], key[1]): F(1)}
            sub = {"normal_form": "y + x^%d*y^%d" % key, "fibres": []}
            verdict = "UNRESOLVED"
            for c in CS_NUM:
                try:
                    r = mono15.screen_fibre_checked(nf, c)
                except Exception as e:                    # noqa: BLE001
                    r = {"error": "%s: %s" % (type(e).__name__, e)}
                sub["fibres"].append({"c": str(c), "res": r})
                if r.get("verdict") == "NONVANISHING":
                    verdict = "NONVANISHING"
                    break
            if verdict != "NONVANISHING":
                vs = [f["res"].get("verdict") for f in sub["fibres"]]
                verdict = "VANISHING" if vs and all(v == "VANISHING" for v in vs) \
                    else "UNRESOLVED"
            sub["verdict"] = verdict
            _DEFERRED_CACHE[key] = sub
        det["instrument"] = "EXACT-G1+NUM-MONO(normal form)"
        det["deferred_resolution"] = _DEFERRED_CACHE[key]
        return _DEFERRED_CACHE[key]["verdict"], det

    if dy == 2:
        det["instrument"] = "EXACT-HE"
        for c in CS_EXACT:
            try:
                r = exact_he15.screen(P, c)
            except Exception as e:                        # noqa: BLE001
                r = {"applicable": False, "reason": "%s: %s" % (type(e).__name__, e)}
            det["fibres"].append({"c": str(c), "res": r})
            if r.get("verdict") == "NONVANISHING":
                det["witness_c"] = str(c)
                return "NONVANISHING", det
        vs = [f["res"].get("verdict") for f in det["fibres"]]
        if all(v == "VANISHING" for v in vs):
            return "VANISHING", det
        return "UNRESOLVED", det

    det["instrument"] = "NUM-MONO"
    # cost guard: dy * (number of branch points) drives the run time.
    try:
        nb = len(mono15._disc_and_lc_roots(P, F(1)))
    except Exception as e:                                # noqa: BLE001
        det["cost_error"] = str(e)
        return "NOT_SCREENED", det
    det["n_branch"] = nb
    if dy * nb > num_budget:
        det["skipped"] = "cost dy*n_branch = %d > %d" % (dy * nb, num_budget)
        return "NOT_SCREENED", det
    for c in CS_NUM:
        t = time.time()
        try:
            r = mono15.screen_fibre_checked(P, c)
        except Exception as e:                            # noqa: BLE001
            r = {"error": "%s: %s" % (type(e).__name__, e)}
        r["secs"] = round(time.time() - t, 1)
        det["fibres"].append({"c": str(c), "res": r})
        if r.get("verdict") == "NONVANISHING":
            det["witness_c"] = str(c)
            return "NONVANISHING", det
    vs = [f["res"].get("verdict") for f in det["fibres"]]
    if vs and all(v == "VANISHING" for v in vs):
        return "VANISHING", det
    return "UNRESOLVED", det


def main(limit=None, out_json="screen15_records.json", csv_path="period_screen.csv"):
    C = gen15.corpus()
    if limit:
        C = C[:limit]
    recs = []
    csv = ["hash,label,deg_P,deg_y,species,U_bezout,U_residual_terms,SY,FIB,"
           "instrument,n_places_inf,genus,period_verdict,witness"]
    t0 = time.time()
    for idx, (P, lab, meta) in enumerate(C):
        h = P14.phash(P)
        rec = {"hash": h, "label": lab, "meta": meta,
               "deg_P": P14.tdeg(P), "deg_y": deg_y(P),
               "n_terms": len(P), "P": {"%d,%d" % k: [v.numerator, v.denominator]
                                        for k, v in P.items()},
               "species": gen15.species_of(P, meta)}
        u = cert15.bezout_unimodular(P)
        rec["U"] = u
        if not u.get("U"):
            rec["outcome"] = "REJECTED_not_unimodular"
            recs.append(rec)
            print("[%3d] %s deg=%d  REJECTED (U): %s" % (idx, h, rec["deg_P"], u.get("reason")))
            sys.stdout.flush()
            continue
        sy, st = sy15.certify(P, node_budget=200000)
        rec["SY"] = sy
        rec["SY_stats"] = st
        try:
            fv, fres = fib15.screen(P, lams=(0, 1, -1), timeout=90)
        except Exception as e:                            # noqa: BLE001
            fv, fres = "ERROR", str(e)
        rec["FIB"] = fv
        rec["FIB_detail"] = fres
        if sy != "NON_COORDINATE" and not str(fv).startswith("NON_COORDINATE"):
            rec["outcome"] = "REJECTED_no_noncoordinate_witness"
            recs.append(rec)
            print("[%3d] %s deg=%d  REJECTED (SY=%s FIB=%s)" % (idx, h, rec["deg_P"], sy, fv))
            sys.stdout.flush()
            continue
        v, det = period_screen(P, meta)
        rec["period_verdict"] = v
        rec["period_detail"] = det
        rec["outcome"] = "PERIODS-" + v if v in ("NONVANISHING", "VANISHING") else v
        recs.append(rec)
        f0 = det["fibres"][0]["res"] if det["fibres"] else {}
        g1 = det.get("exact_g1", {})
        npl = f0.get("n_places_at_infinity", f0.get("n_punctures",
                                                    g1.get("n_places_at_infinity")))
        gg = f0.get("genus", f0.get("genus_sum", g1.get("genus")))
        csv.append("%s,%s,%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            h, '"%s"' % lab.replace('"', "'"), rec["deg_P"], rec["deg_y"],
            "|".join(rec["species"]), u.get("U"), u.get("residual_terms"),
            sy, fv, det.get("instrument"), npl, gg, v,
            '"%s"' % str(f0.get("witness", det.get("skipped", "")))[:80].replace('"', "'")))
        print("[%3d] %s deg=%2d dy=%d %-10s SY=%-15s FIB=%-22s -> %s  (%.0fs)"
              % (idx, h, rec["deg_P"], rec["deg_y"], det.get("instrument"),
                 sy, fv, v, time.time() - t0))
        sys.stdout.flush()
        if idx % 20 == 19:
            with open(os.path.join(HERE, out_json), "w") as fh:
                json.dump(recs, fh, default=str)
            with open(os.path.join(HERE, csv_path), "w") as fh:
                fh.write("\n".join(csv) + "\n")
    with open(os.path.join(HERE, out_json), "w") as fh:
        json.dump(recs, fh, default=str)
    with open(os.path.join(HERE, csv_path), "w") as fh:
        fh.write("\n".join(csv) + "\n")
    from collections import Counter
    print("\nOUTCOMES:", Counter(r["outcome"] for r in recs))


if __name__ == "__main__":
    main(limit=int(sys.argv[1]) if len(sys.argv) > 1 else None)
