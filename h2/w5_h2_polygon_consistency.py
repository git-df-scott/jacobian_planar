"""
Are the queue's reduced polygons consistent with the chain data in their tags?

Each target in trackD_targets.json carries BOTH a tag naming a chain and a cusp
pair (m,n) and a pair of reduced Newton polygons NP, NQ.  The chain -> polygon
map that connects them is the campaign's own construction.  Three invariants
must hold whatever the map does, and none had been checked:

  * the polygons' degrees must be in the ratio m : n UP TO ORIENTATION, since
    deg P = m*v11(A0) and deg Q = n*v11(A0) and the reduction is applied to
    both sides alike, but nothing in the tag fixes which of the stored pair is
    P;
  * `trackD_extract.orient` must accept every target -- it is the gate that
    picks the driver by looking for the j=0 row {(0,0),(1,0)}, and a target it
    rejects is recorded OUT OF SCOPE and can never produce a verdict;
  * whichever of NP, NQ carries the two-point j=0 row must be predictable from
    the tag, or the queue is storing an orientation nothing else knows about.

CONTROLS
  G1  POSITIVE: the degree ratio holds up to orientation on every chain-tagged
      target, and the orientation used is reported, not hidden.
  G1b POSITIVE: the stored polygon degrees are a property of the CHAIN alone --
      constant across every target sharing a chain prefix, whatever order that
      target's tag lists (m,n) and eps in.  (The queue enumerates a chain under
      BOTH (m,n) and (n,m); the polygons do not follow, which is the whole of
      the 11 "reversed" targets.)
  G1c NEGATIVE: mutating one target's polygon makes its chain non-constant.
  G2  NEGATIVE: perturbing one polygon vertex breaks G1 under BOTH orientations.
  G3  POSITIVE: orient() accepts every target, so nothing in the queue is
      silently unverdictable at the polygon level.
  G3b POSITIVE: which polygon carries the two-point j=0 row is exactly decided
      by whether the tag's eps pair lists (1,0) first.
  G4  NEGATIVE: mangling a j=0 row makes orient() reject that target.
"""
import json
import os
import re
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "campaign", "audit_tracks"))
import w5_h2_target_provenance as P
from trackD_extract import orient

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def deg(poly):
    return max(a + b for a, b in poly)


def ratio_orientation(t):
    """+1 if deg NP : deg NQ == m : n, -1 if == n : m, 0 if neither."""
    pt = P.parse_tag(t["tag"])
    if pt is None or pt[1] is None:
        return None
    m, n = pt[2]
    g = gcd(m, n)
    m, n = m // g, n // g
    dP, dQ = deg(t["NP"]), deg(t["NQ"])
    if dQ * m == dP * n:
        return 1
    if dP * m == dQ * n:
        return -1
    return 0


def eps_first_is_10(tag):
    m = re.search(r"eps=\(\((\d+), (\d+)\),\((\d+), (\d+)\)\)", tag)
    if m is None:
        return None
    return m.group(1) == "1" and m.group(2) == "0"


def j0(poly):
    return sorted(tuple(v) for v in poly if v[1] == 0)


def chain_key(tag):
    return tag.split(" | ")[0].split(" (m,n)")[0]


def main():
    targets = json.load(open(os.path.join(HERE, "trackD_targets.json")))
    print("=" * 78)
    print("consistency of the queue's reduced polygons with its chain tags")
    print("=" * 78)

    fwd, rev, broken = [], [], []
    for t in targets:
        o = ratio_orientation(t)
        if o is None:
            continue
        (fwd if o == 1 else rev if o == -1 else broken).append(t)
    check("G1 POSITIVE: deg NP : deg NQ equals m : n up to orientation on every "
          "chain-tagged target", not broken,
          f"{len(fwd)} in tag order, {len(rev)} reversed, {len(broken)} neither")
    for t in rev[:3]:
        print(f"      reversed (deg NP:NQ = n:m): {t['tag'][:66]}  "
              f"{deg(t['NP'])}:{deg(t['NQ'])}")

    def degs_by_chain(ts):
        d = {}
        for t in ts:
            d.setdefault(chain_key(t["tag"]), set()).add((deg(t["NP"]),
                                                          deg(t["NQ"])))
        return d

    by_chain = degs_by_chain(targets)
    split = {k: sorted(v) for k, v in by_chain.items() if len(v) > 1}
    check("G1b POSITIVE: the stored polygon degrees are constant within each "
          "chain", not split,
          f"{len(by_chain)} chains, {len(split)} with more than one degree "
          f"pair; reversed-tag chains: "
          f"{sorted({chain_key(t['tag']) for t in rev})}")

    mut = [dict(t) for t in targets]
    k0 = chain_key(mut[0]["tag"])
    idx = [i for i, t in enumerate(mut) if chain_key(t["tag"]) == k0]
    mut[idx[-1]] = dict(mut[idx[-1]],
                        NP=[list(v) for v in mut[idx[-1]]["NP"]][:-1] + [[99, 0]])
    split2 = {k: v for k, v in degs_by_chain(mut).items() if len(v) > 1}
    check("G1c NEGATIVE: mutating one target's polygon makes its chain "
          "non-constant", bool(split2),
          f"chain {k0}: {len(idx)} targets, degree pairs now "
          f"{sorted(degs_by_chain(mut)[k0])}")

    t0 = targets[0]
    NP2 = [list(v) for v in t0["NP"]]
    NP2[-1][1] += 1
    t0b = dict(t0, NP=NP2)
    check("G2 NEGATIVE: perturbing one polygon vertex breaks the ratio under "
          "both orientations", ratio_orientation(t0b) == 0,
          f"deg NP {deg(t0['NP'])} -> {deg(NP2)}, orientation "
          f"{ratio_orientation(t0)} -> {ratio_orientation(t0b)}")

    rejected = [t for t in targets if orient(t["NP"], t["NQ"]) is None]
    check("G3 POSITIVE: trackD_extract.orient accepts every target", not rejected,
          f"{len(targets) - len(rejected)} of {len(targets)} accepted; "
          f"{len(rejected)} OUT OF SCOPE")

    mismatch, drives = [], {1: 0, -1: 0}
    for t in targets:
        o = orient(t["NP"], t["NQ"])
        if o is None:
            continue
        drives[o[2]] += 1
        e = eps_first_is_10(t["tag"])
        if e is None or e != (o[2] == 1):
            mismatch.append(t["tag"][:60])
    check("G3b POSITIVE: the driver side is decided by whether the tag's eps "
          "pair lists (1,0) first", not mismatch,
          f"NP drives {drives[1]}, NQ drives {drives[-1]}; "
          f"{len(mismatch)} tags disagree")

    bad = [list(v) for v in targets[0]["NP"]]
    bad = [v for v in bad if tuple(v) != (1, 0)] + [[3, 0]]
    check("G4 NEGATIVE: mangling a j=0 row makes orient() reject the target",
          orient(bad, targets[0]["NQ"]) is None,
          f"j=0 row {j0(targets[0]['NP'])} -> {j0(bad)}")

    json.dump({"ratio_tag_order": len(fwd), "ratio_reversed": len(rev),
               "ratio_broken": [t["tag"] for t in broken],
               "reversed_tags": [t["tag"] for t in rev],
               "reversed_chains": sorted({chain_key(t["tag"]) for t in rev}),
               "chains_with_multiple_degree_pairs": {k: [list(x) for x in v] for k, v in split.items()},
               "orient_rejected": [t["tag"] for t in rejected],
               "NP_drives": drives[1], "NQ_drives": drives[-1],
               "eps_mismatch": mismatch,
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "h2_polygon_consistency.json"), "w"), indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)


if __name__ == "__main__":
    main()
