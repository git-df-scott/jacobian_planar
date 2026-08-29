"""night15 -- finish the two survivors whose 2*deg P carrier exceeded the
default exact-lambda budget, with the cap raised."""
import json, os, time, sys
from fractions import Fraction as F
import pk15 as P14, mate15
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "night12"))
import matekit as M, exact as EX

HERE = os.path.dirname(os.path.abspath(__file__))
recs = {r["hash"]: r for r in json.load(open(os.path.join(HERE, "screen15_records.json")))}
surv = json.load(open(os.path.join(HERE, "survivors15.json")))
out = []
for s in surv:
    if s["verdict"] == "EMPTY_all_stages":
        continue
    r = recs[s["hash"]]
    P = P14.clean({tuple(int(t) for t in k.split(",")): F(v[0], v[1])
                   for k, v in r["P"].items()})
    d = P14.tdeg(P)
    S = mate15.carrier(2 * d)
    Pi = {k: int(v) for k, v in P.items()}
    print("%s deg=%d  carrier D=%d n=%d" % (s["hash"], d, 2 * d, len(S)))
    sys.stdout.flush()
    t = time.time()
    rows, _ = M.build_system(Pi, S)
    lam, why = mate15.exact_lambda(rows, len(S), cap=4000)
    ok = lam is not None and EX.verify_lambda(lam, rows, len(S))
    print("   %s  (%s)  %.0fs" % ("EMPTY_over_Q / lambda_exact" if ok else "NOT_CERTIFIED",
                                  why, time.time() - t))
    sys.stdout.flush()
    out.append({"hash": s["hash"], "deg_P": d, "deg_Q_bound": 2 * d,
                "n_unknowns": len(S), "verdict": "EMPTY_over_Q" if ok else "NOT_CERTIFIED",
                "certificate": "lambda_exact" if ok else "none",
                "lambda_support": len(lam) if lam else 0,
                "lambda_reverified": bool(ok), "why": why,
                "lambda_vector": EX._lam_out(lam) if lam else None,
                "secs": round(time.time() - t, 1)})
json.dump(out, open(os.path.join(HERE, "topup15.json"), "w"), indent=1, default=str)
