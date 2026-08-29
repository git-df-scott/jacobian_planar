"""night15 -- assemble the measurement tables for PERIODS.md."""

import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    recs = json.load(open(os.path.join(HERE, "screen15_records.json")))
    out = []
    A = out.append
    A("### 6.1 Screening totals\n")
    A("| quantity | value |")
    A("|---|---|")
    A("| P generated and certified through the gate | %d |" % len(recs))
    cnt = Counter(r["outcome"] for r in recs)
    for k, v in sorted(cnt.items()):
        A("| %s | %d |" % (k, v))
    scr = [r for r in recs if "period_verdict" in r]
    A("| degrees covered | %d .. %d |" % (min(r["deg_P"] for r in recs),
                                          max(r["deg_P"] for r in recs)))
    A("| deg_y values | %s |" % sorted({r["deg_y"] for r in recs}))
    ub = [r for r in recs if r.get("U", {}).get("U")]
    A("| exact Bezout unimodularity, residual 0 | %d / %d |" % (len(ub), len(recs)))
    A("| SY = NON_COORDINATE | %d |" % sum(1 for r in recs if r.get("SY") == "NON_COORDINATE"))
    A("| independent fibre witness NON_COORDINATE_BY_* | %d |"
      % sum(1 for r in recs if str(r.get("FIB", "")).startswith("NON_COORDINATE")))
    A("")

    A("### 6.2 Period verdict by instrument\n")
    by = defaultdict(Counter)
    for r in scr:
        by[r["period_detail"].get("instrument", "?")][r["period_verdict"]] += 1
    A("| instrument | NONVANISHING | VANISHING | other |")
    A("|---|---|---|---|")
    for k in sorted(by):
        c = by[k]
        A("| %s | %d | %d | %d |" % (k, c["NONVANISHING"], c["VANISHING"],
                                     sum(c.values()) - c["NONVANISHING"] - c["VANISHING"]))
    A("")

    A("### 6.3 Period verdict by species\n")
    sp = defaultdict(Counter)
    for r in scr:
        for s in (r["species"] or ["(none)"]):
            sp[s][r["period_verdict"]] += 1
    A("| species | NONVANISHING | VANISHING | other |")
    A("|---|---|---|---|")
    for k in sorted(sp):
        c = sp[k]
        A("| %s | %d | %d | %d |" % (k, c["NONVANISHING"], c["VANISHING"],
                                     sum(c.values()) - c["NONVANISHING"] - c["VANISHING"]))
    A("")

    A("### 6.3b Species S1..S5 as MEASURED (not as intended)\n")
    A("Each row counts the screened P for which the measurement itself puts the")
    A("member in that species.\n")
    A("| species (measured) | count | NONVANISHING | VANISHING | other |")
    A("|---|---|---|---|---|")

    def places_of(r):
        d = r["period_detail"]
        g1 = d.get("exact_g1", {})
        if g1:
            return g1.get("n_places_at_infinity")
        f = d.get("fibres") or [{}]
        return f[0].get("res", {}).get("n_punctures")

    def genus_of(r):
        d = r["period_detail"]
        g1 = d.get("exact_g1", {})
        if g1:
            return g1.get("genus")
        f = d.get("fibres") or [{}]
        return f[0].get("res", {}).get("genus_sum")

    def nfac_of(r):
        fd = r.get("FIB_detail")
        if not isinstance(fd, list):
            return None
        return max([f.get("nfac") or 0 for f in fd] + [0])

    tests = [
        ("S1 v-cubic (m = 3)", lambda r: r["meta"].get("m") == 3),
        ("S2 >= 3 places at infinity", lambda r: (places_of(r) or 0) >= 3),
        ("S3 positive genus fibre", lambda r: (genus_of(r) or 0) >= 1),
        ("S4 fibre with >= 3 components", lambda r: (nfac_of(r) or 0) >= 3),
        ("S5 sheared / mixed support", lambda r: bool(r["meta"].get("sheared"))),
        ("deg_y >= 3 (not v-quadratic)", lambda r: r["deg_y"] >= 3),
    ]
    for name, f in tests:
        sel = [r for r in scr if f(r)]
        c = Counter(r["period_verdict"] for r in sel)
        A("| %s | %d | %d | %d | %d |" % (name, len(sel), c["NONVANISHING"],
                                          c["VANISHING"],
                                          len(sel) - c["NONVANISHING"] - c["VANISHING"]))
    A("")

    A("### 6.4 The (n, m) table for the v-power family G1\n")
    A("Every G1 member with the same `(n, m)` receives the same verdict; the")
    A("count is how many corpus members carry that pair.\n")
    A("| n | m | genus | places at infinity | verdict | case | members |")
    A("|---|---|---|---|---|---|---|")
    g1 = defaultdict(int)
    info = {}
    for r in scr:
        m = r["meta"]
        if m.get("gen") != "G1":
            continue
        k = (m["n"], m["m"])
        g1[k] += 1
        d = r["period_detail"].get("exact_g1", {})
        info[k] = (d.get("genus"), d.get("n_places_at_infinity"),
                   r["period_verdict"], d.get("case"))
    for k in sorted(g1):
        gg, pl, v, cs = info[k]
        A("| %d | %d | %s | %s | %s | %s | %d |" % (k[0], k[1], gg, pl, v, cs, g1[k]))
    A("")

    A("### 6.5 Survivors (PERIODS-VANISHING) and their exact mate solve\n")
    surv = [r for r in scr if r["period_verdict"] == "VANISHING"]
    A("%d survivors.\n" % len(surv))
    path = os.path.join(HERE, "survivors15.json")
    if os.path.exists(path):
        mates = {m["hash"]: m for m in json.load(open(path))}
        A("| hash | deg P | deg_y | label | mate verdict | stages |")
        A("|---|---|---|---|---|---|")
        for r in sorted(surv, key=lambda z: z["deg_P"]):
            m = mates.get(r["hash"])
            if not m:
                A("| %s | %d | %d | %s | (not run) | |" % (r["hash"], r["deg_P"],
                                                           r["deg_y"], r["label"][:44]))
                continue
            st = "; ".join("D=%s:%s/%s" % (s.get("deg_Q_bound"), s.get("verdict"),
                                           s.get("certificate"))
                           for s in m["stages"])
            A("| %s | %d | %d | %s | %s | %s |" % (r["hash"], r["deg_P"], r["deg_y"],
                                                   r["label"][:44], m["verdict"], st))
        A("")
        A("mate verdicts: %s" % dict(Counter(m["verdict"] for m in mates.values())))
    else:
        for r in sorted(surv, key=lambda z: z["deg_P"]):
            A("* `%s` deg %d deg_y %d  %s" % (r["hash"], r["deg_P"], r["deg_y"],
                                              r["label"]))
    A("")
    txt = "\n".join(out)
    with open(os.path.join(HERE, "RESULTS_TABLES.md"), "w") as fh:
        fh.write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
