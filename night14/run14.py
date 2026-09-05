"""night14 -- prospecting pipeline.

For each generated candidate: U-test (mod-p shadow, then the char-0 verdict)
then the SY-certificate on every U-passer.  Records one row per candidate.
The measured quantity of the lane: U = PASS together with SY = NON_COORDINATE.
"""

import json
import os
import random
import sys
import time

import poly14 as P14
import sy14
import utest14
import fib14
import families14 as G

PLAN = [("F2", 30), ("F2b", 30), ("F1", 20), ("F1b", 20), ("F3", 20), ("F4", 20)]
LAMS = (0, 1, -1)
SEED = 20260828


def run(plan=PLAN, seed=SEED, out="records.json"):
    rng = random.Random(seed)
    seen = set()
    rows = []
    for fam, count in plan:
        made = 0
        tries = 0
        while made < count and tries < count * 40:
            tries += 1
            got = G.GENERATORS[fam](rng)
            f, lab, P = got[0], got[1], got[2]
            hints = list(got[3]) if len(got) > 3 else []
            if not P or P14.tdeg(P) < 1:
                continue
            hh = P14.phash(P)
            if hh in seen:
                continue
            seen.add(hh)
            made += 1
            row = {"family": f, "label": lab, "hash": hh,
                   "poly": P14.to_str(P),
                   "monomials": [[list(k), str(v)] for k, v in sorted(P.items())],
                   "tdeg": P14.tdeg(P), "degx": P14.degx(P), "degy": P14.degy(P),
                   "nterms": len(P)}
            u = utest14.utest(P)
            row.update(u)
            if u["u_q"] == "PASS":
                t0 = time.time()
                v, st = sy14.certify(P)
                row["sy"] = v
                row["sy_nodes"] = st["nodes"]
                row["sy_leaves"] = st["leaves"]
                row["t_sy"] = round(time.time() - t0, 3)
                t0 = time.time()
                lams = list(LAMS) + [l for l in hints if l not in LAMS]
                fv, fres = fib14.screen(P, lams=lams, timeout=90)
                row["fib"] = fv
                row["fib_detail"] = [(str(r["lam"]), r["nfac"], r["genus"]) for r in fres]
                row["t_fib"] = round(time.time() - t0, 3)
            else:
                row["sy"] = "NOT_RUN"
                row["t_sy"] = 0.0
                row["fib"] = "NOT_RUN"
                row["fib_detail"] = []
                row["t_fib"] = 0.0
            row["crux"] = (row["u_q"] == "PASS" and row["sy"] == "NON_COORDINATE")
            # cross-instrument agreement on the U-passers
            if row["u_q"] == "PASS":
                if row["sy"] == "NON_COORDINATE":
                    row["agree"] = "CORROBORATED" if row["fib"].startswith("NON_COORDINATE") \
                        else "SY_ONLY"
                elif row["sy"] == "COORDINATE":
                    row["agree"] = "CONFLICT" if row["fib"].startswith("NON_COORDINATE") \
                        else "CONSISTENT"
                else:
                    row["agree"] = "NA"
            else:
                row["agree"] = "NA"
            rows.append(row)
            print("%-4s %-46s tdeg=%-3d Q=%-5s SY=%-15s FIB=%-21s %s"
                  % (f, row["poly"][:46], row["tdeg"], row["u_q"],
                     row["sy"], row["fib"], "CRUX" if row["crux"] else ""))
            sys.stdout.flush()
    with open(out, "w") as fh:
        json.dump(rows, fh, indent=1)
    return rows


def tally(rows):
    fams = []
    for r in rows:
        if r["family"] not in fams:
            fams.append(r["family"])
    lines = []
    hdr = ("| family | candidates | U PASS | U FAIL | SY COORD | SY NON_COORD "
           "| SY budget-out | U+SY objects | COORD rate among U-passers |")
    lines.append(hdr)
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for f in fams + ["ALL"]:
        rs = rows if f == "ALL" else [r for r in rows if r["family"] == f]
        n = len(rs)
        up = sum(r["u_q"] == "PASS" for r in rs)
        uf = sum(r["u_q"] == "FAIL" for r in rs)
        sc = sum(r["sy"] == "COORDINATE" for r in rs)
        sn = sum(r["sy"] == "NON_COORDINATE" for r in rs)
        sb = sum(r["sy"] == "BUDGET_EXHAUSTED" for r in rs)
        cx = sum(bool(r["crux"]) for r in rs)
        rate = ("%.0f%% (%d/%d)" % (100.0 * sc / up, sc, up)) if up else "n/a"
        lines.append("| %s | %d | %d | %d | %d | %d | %d | %d | %s |"
                     % (f, n, up, uf, sc, sn, sb, cx, rate))
    lines.append("")
    lines.append("| family | U-passers | SY NON_COORD corroborated by FIB | SY NON_COORD, FIB inconclusive "
                 "| SY COORD, FIB consistent | conflicts |")
    lines.append("|---|---|---|---|---|---|")
    for f in fams + ["ALL"]:
        rs = [r for r in (rows if f == "ALL" else [r for r in rows if r["family"] == f])
              if r["u_q"] == "PASS"]
        lines.append("| %s | %d | %d | %d | %d | %d |"
                     % (f, len(rs),
                        sum(r["agree"] == "CORROBORATED" for r in rs),
                        sum(r["agree"] == "SY_ONLY" for r in rs),
                        sum(r["agree"] == "CONSISTENT" for r in rs),
                        sum(r["agree"] == "CONFLICT" for r in rs)))
    return "\n".join(lines)


def write_csv(rows, path="records.csv"):
    import csv
    cols = ["family", "hash", "poly", "tdeg", "degx", "degy", "nterms",
            "u_modp", "u_q", "t_modp", "t_q", "sy", "sy_nodes", "sy_leaves",
            "t_sy", "fib", "t_fib", "agree", "crux", "label"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    t0 = time.time()
    rows = run()
    write_csv(rows)
    print()
    print(tally(rows))
    print("\ntotal wall %.1fs   candidates %d" % (time.time() - t0, len(rows)))
