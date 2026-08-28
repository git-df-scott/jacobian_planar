"""night9 — build night9/CROSS_PRIME.md from night9/cross_prime.csv.

Reporting only; computes nothing new.  De-duplicates the CSV (a resumed run
can append a row twice) keeping the last row for each (hash, p).
"""
import csv, json, os, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cross_prime import PRIMES, CLIMBERS, CHOSEN, FIELDS

rows = list(csv.DictReader(open(os.path.join(HERE, "cross_prime.csv"))))
seen = OrderedDict()
for r in rows:
    seen[(r["hash"], int(r["p"]))] = r
rows = list(seen.values())
with open(os.path.join(HERE, "cross_prime.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader()
    for r in sorted(rows, key=lambda r: (r["hash"], int(r["p"]))):
        w.writerow(r)

sup = {}
for f in os.listdir(os.path.join(HERE, "supports")):
    d = json.load(open(os.path.join(HERE, "supports", f)))
    sup[d["hash"]] = d

by = {}
for r in rows:
    by[(r["hash"], int(r["p"]))] = r

order = CLIMBERS + CHOSEN


def cell(r):
    if r is None:
        return "-"
    v = r["verdict"]
    if v != "NONEMPTY":
        return v[0] if v == "EMPTY" else v
    nd = int(r["n_nondegenerate"] or 0)
    ne = int(r["tear_nonempty"] or 0)
    te = int(r["tear_empty"] or 0)
    to = int(r["tear_other"] or 0)
    t = ("NE%d" % ne if ne else "") + ("E%d" % te if te else "") + \
        ("?%d" % to if to else "")
    c2 = int(r["climb_p2"] or 0); c3 = int(r["climb_p3"] or 0)
    s = "N/%d/%s" % (nd, t or "-")
    if c2 or c3:
        s += "/c2=%d,c3=%d" % (c2, c3)
    return s


L = []
L.append("# night9 — the cross-prime experiment\n")
L.append("""Scope note. Measurements only. Every result is labelled with its
characteristic. No assessment of what any of these numbers mean is offered.

Twelve distinguished supports, each run at **every** prime in
`{2, 3, 5, 7, 11, 13, 17, 19, 23}` — 108 cells. Selection:

* **(a)** the four supports whose solutions climbed to `Z/p^2` in the sweep:
  `3ee4c514dba8`, `c764f008a1a1`, `cf8c7ed97c0c` (found at `p = 3`) and
  `e3ff048903ae` (found at `p = 5`);
* **(b)** eight further cells that were TEAR-NONEMPTY *and* carried
  non-degenerate solutions, chosen for enumerability — smallest
  `min(|S_P|,|S_Q|)` and lowest total degree first — and spread over the two
  families and over the primes at which they were found.

Method and standards are exactly those of `night9/README.md` §3–§6:
complete `exhaustive-bilinear` enumeration when `p^nfree <= 10^7`, otherwise
Groebner over `GF(p)` **with the field equations** `z^p - z` (300 s timeout,
a timeout recorded as TIMEOUT and never as EMPTY); on NONEMPTY the complete
solution set is enumerated (cap 60000) and split by the additive-type
degeneracy screen; up to 8 non-degenerate solutions per cell are verified by
direct substitution, tear-classified mod `p`, and pushed through the Hensel
steps to `Z/p^2` and then `Z/p^3`, TEAR-NONEMPTY first.

Raw data: `night9/cross_prime.csv`, per-cell JSON in `night9/cross_prime/`.
""")

L.append("\n## 1. The twelve supports\n")
L.append("| hash | origin | S_P | S_Q | n |")
L.append("|---|---|---|---|---|")
for h in order:
    d = sup[h]
    o = "climb to Z/p^2" if h in CLIMBERS else "TEAR-NONEMPTY, non-degenerate"
    L.append("| `%s` | %s | %s | %s | %d |" % (
        h, o,
        " ".join("(%d,%d)" % tuple(m) for m in d["support_P"]),
        " ".join("(%d,%d)" % tuple(m) for m in d["support_Q"]),
        d["nP"] + d["nQ"]))

L.append("\n## 2. The support-by-prime matrix\n")
L.append("""Cell legend. `EMPTY` / `TIMEOUT` as recorded. For a NONEMPTY cell:
`N/<non-degenerate count>/<tear tally>` where the tear tally counts the
sampled non-degenerate solutions as `NE` = TEAR-NONEMPTY, `E` = TEAR-EMPTY,
`?` = TEAR-NOT-COMPUTED (caps of `README.md` §5); `/c2=..,c3=..` is appended
when any solution climbed to `Z/p^2` resp. `Z/p^3`.
""")
L.append("| hash | " + " | ".join("p=%d" % p for p in PRIMES) + " |")
L.append("|---|" + "---|" * len(PRIMES))
for h in order:
    L.append("| `%s` | " % h +
             " | ".join(cell(by.get((h, p))) for p in PRIMES) + " |")

# tallies
L.append("\n## 3. Tallies\n")
nv = {v: 0 for v in ("NONEMPTY", "EMPTY", "TIMEOUT", "INCONCLUSIVE")}
for r in rows:
    nv[r["verdict"]] = nv.get(r["verdict"], 0) + 1
L.append("Cells run: **%d**. Verdicts: " % len(rows) +
         ", ".join("%s %d" % (k, v) for k, v in nv.items() if v) + ".")
meth = {}
for r in rows:
    meth[r["method"]] = meth.get(r["method"], 0) + 1
L.append("\nMethods: " + ", ".join("`%s` %d" % (k, v) for k, v in sorted(meth.items())) + ".")
vf = sum(int(r["n_verify_fail"] or 0) for r in rows)
L.append("\nDirect-substitution verification failures: **%d**." % vf)

L.append("\n### Per-support totals\n")
L.append("| hash | NONEMPTY primes | primes with >=1 non-degenerate solution | TEAR-NONEMPTY primes | primes with a Z/p^2 climb | Z/p^3 climbs |")
L.append("|---|---|---|---|---|---|")
answer = []
for h in order:
    ne = [p for p in PRIMES if by.get((h, p)) and by[(h, p)]["verdict"] == "NONEMPTY"]
    nd = [p for p in ne if int(by[(h, p)]["n_nondegenerate"] or 0) > 0]
    tn = [p for p in ne if int(by[(h, p)]["tear_nonempty"] or 0) > 0]
    c2 = [p for p in ne if int(by[(h, p)]["climb_p2"] or 0) > 0]
    c3 = sum(int(by[(h, p)]["climb_p3"] or 0) for p in ne)
    answer.append((h, nd))
    f = lambda L_: ", ".join(str(x) for x in L_) if L_ else "none"
    L.append("| `%s` | %s | %s | %s | %s | %d |" %
             (h, f(ne), f(nd), f(tn), f(c2), c3))

L.append("\n## 4. The quantity of interest\n")
L.append("""Does any single support show **non-degenerate NONEMPTY at three or
more distinct primes**? Recorded without interpretation:
""")
hits3 = [(h, nd) for h, nd in answer if len(nd) >= 3]
for h, nd in answer:
    L.append("* `%s`: non-degenerate NONEMPTY at %d prime(s) — %s" %
             (h, len(nd), ", ".join("p=%d" % p for p in nd) if nd else "none"))
L.append("")
if hits3:
    L.append("Supports reaching three or more: **%d** — %s." %
             (len(hits3), ", ".join("`%s` (%d primes)" % (h, len(nd))
                                    for h, nd in hits3)))
else:
    L.append("Supports reaching three or more distinct primes: **none** "
             "(0 of 12). The maximum over the twelve is **%d** prime(s)." %
             max(len(nd) for _, nd in answer))

open(os.path.join(HERE, "CROSS_PRIME.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[-40:]))
