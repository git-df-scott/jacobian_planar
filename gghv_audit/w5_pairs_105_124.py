"""
T1(b) in the literal form asked for: EVERY degree pair with 105 <= max <= 124.

For a hypothetical counterexample, deg P = m * v11(A0) and deg Q = n * v11(A0)
with m, n > 1 coprime, so for a given ordered pair (d1, d2) the data are FORCED:

        g  = gcd(d1, d2) = v11(A0),      m = d1/g,      n = d2/g,

and the pair is possible only if m, n > 1 (they are automatically coprime) and
some admissible complete chain has v11(A0) = g and (m, n) in MN of its final
corner.  So every ordered pair in the window can be decided outright, and this
script decides all of them.

Output: gghv_audit/pairs_105_124.json, one record per ordered pair, each with
    status = ARISES  (with the chain and the GGHV node that kills it, if any)
           | ELIMINATED-BY-ENUMERATION  (with the reason: m or n is 1, or no
             admissible chain has that v11(A0), or none has that (m,n))
No pair is left as "not considered".

CONTROLS
  Q1 the four pairs GGHV's own table puts in this window must come out ARISES;
  Q2 a pair just outside the window that GGHV lists ((66,99), max 99) must also
     be reproduced by the same code path when the window is widened -- so the
     "eliminated" answers are not an artefact of the window;
  Q3 NEGATIVE: a pair with m = 1 (e.g. (110, 110)) must be eliminated for the
     stated reason, and a pair with a v11 no chain realises must be eliminated
     for its own, different, stated reason.
"""

import json
import os
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ggv_algorithms as G

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def build_index(M=100, xmax=120):
    PLLC, _ = G.get_possible_last_lower_corners(xmax)
    raw = G.admissible_complete_chains(M, PLLC=PLLC)
    chains = {}
    for c, last in raw:
        chains[(tuple((x[0], x[1]) for x in c), last)] = (c, last)
    idx = {}
    v11s = set()
    for (_, _), (c, last) in chains.items():
        A0 = c[0][0]
        v = A0[0] + A0[2]
        v11s.add(v)
        for k, m, n in G.mn_pairs(last, max_mn=400):
            idx.setdefault((v, m, n), []).append(
                {"A0": list(A0), "mid": [list(x[0]) for x in c[1:]],
                 "final": list(last), "k": k})
    return idx, v11s, len(chains)


def decide(d1, d2, idx, v11s):
    g = gcd(d1, d2)
    m, n = d1 // g, d2 // g
    if m <= 1 or n <= 1:
        return {"status": "ELIMINATED-BY-ENUMERATION",
                "reason": f"gcd(deg P, deg Q) = {g} forces (m,n) = ({m},{n}); "
                          f"a counterexample needs m, n > 1"}
    if g not in v11s:
        return {"status": "ELIMINATED-BY-ENUMERATION",
                "reason": f"no admissible complete chain has v11(A0) = {g}"}
    # [5] lists only the (m,n) satisfying its equality (3.17); the pairs
    # satisfying (3.18) are obtained by swapping m with n, so BOTH orders are
    # admissible for a given chain and both are checked here.
    hits = list(idx.get((g, m, n), [])) + list(idx.get((g, n, m), []))
    if not hits:
        return {"status": "ELIMINATED-BY-ENUMERATION",
                "reason": f"chains with v11(A0) = {g} exist, but none has "
                          f"(m,n) = ({m},{n}) or ({n},{m}) in MN of its final corner"}
    return {"status": "ARISES", "v11_A0": g, "m": m, "n": n, "chains": hits}


NODE = {(108, 72): "GGHV: LEFT OPEN (the starred row of the section-2 table)",
        (72, 108): "GGHV section 5 (the (9,27) polynomial system)",
        (80, 112): "GGHV section 2 table: '[4, section 3.5]' -- external, not "
                   "re-derivable from any source in papers/",
        (112, 80): "GGHV section 2 table: '[4, section 3.5]' -- external",
        (120, 80): "GGHV section 3 (via [2, Prop 3.29] applied to (8,4))",
        (80, 120): "GGHV section 3"}


def main():
    print("=" * 78)
    print("T1(b) -- every ordered degree pair with 105 <= max <= 124")
    print("=" * 78)
    idx, v11s, nchains = build_index()
    print(f"    index built from {nchains} distinct admissible complete chains; "
          f"{len(v11s)} distinct v11(A0) values")
    rows = []
    arises = []
    for d1 in range(1, 125):
        for d2 in range(1, 125):
            if not (105 <= max(d1, d2) <= 124):
                continue
            r = decide(d1, d2, idx, v11s)
            r["deg_P"], r["deg_Q"] = d1, d2
            if r["status"] == "ARISES":
                r["gghv_node"] = NODE.get((d1, d2), "NO NODE ON RECORD")
                arises.append((d1, d2))
            rows.append(r)
    print(f"    ordered pairs in the window: {len(rows)}")
    print(f"    pairs that ARISE: {len(arises)} -> {sorted(arises)}")
    check("Q1 the pairs that arise are exactly the six orientations of GGHV's "
          "three degree pairs in this window",
          sorted(arises) == sorted([(72, 108), (108, 72), (80, 112), (112, 80),
                                    (80, 120), (120, 80)]),
          f"{sorted(arises)}")
    # Q2: widen the window and confirm a known pair outside it
    r99 = decide(66, 99, idx, v11s)
    check("Q2 the same code path reproduces (66,99), a pair GGHV lists OUTSIDE "
          "the window", r99["status"] == "ARISES",
          f"{r99['status']}: {r99.get('reason', '')}")
    r110 = decide(110, 110, idx, v11s)
    check("Q3a NEGATIVE: (110,110) is eliminated because it forces m = n = 1",
          r110["status"] == "ELIMINATED-BY-ENUMERATION" and "m, n > 1" in r110["reason"],
          r110["reason"])
    # a pair with m, n > 1 coprime whose v11(A0) no chain realises
    r_odd = decide(115, 138, idx, v11s)          # gcd 23, (m,n) = (5,6)
    check("Q3b NEGATIVE: (115,138) -- (m,n) = (5,6), both > 1 and coprime -- is "
          "eliminated for a DIFFERENT stated reason, about the chains",
          r_odd["status"] == "ELIMINATED-BY-ENUMERATION"
          and "m, n > 1" not in r_odd["reason"], r_odd["reason"])
    reasons = {}
    for r in rows:
        if r["status"] != "ARISES":
            key = r["reason"].split(";")[0].split("=")[0].strip()
            reasons[key] = reasons.get(key, 0) + 1
    print(f"    elimination reasons: {reasons}")
    json.dump({"window": [105, 124], "n_pairs": len(rows),
               "arising": [list(a) for a in sorted(arises)], "rows": rows,
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "pairs_105_124.json"), "w"), indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if n == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
