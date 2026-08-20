"""
Do the above-125 queue's targets come from chains that actually exist?

`campaign/audit_tracks/trackD_targets.json` lists 180 targets whose tags name a
chain and a cusp pair, e.g.

    (11,33)/19/4,8 (m,n)=2,3 | a=4 b=9 c'=0 r=2 eps=((1, 0),(2, 1))

Nothing in the campaign checks those against an independent enumeration.  This
script does: it rebuilds the admissible complete chains from the pseudocode of
arXiv:1708.07936 (gghv_audit/ggv_algorithms.py, already certified 19/19 against
the paper's own tables) and asks, for every target,

  * is there an admissible complete chain with that A0 and that final corner?
  * is (m,n) in MN of that final corner (in either orientation)?
  * does max(m,n) * v11(A0) equal the target's recorded `max`?

A target that fails any of these is reported.  This is provenance, not a
verdict: it says the queue is asking about shapes the enumeration produces.

CONTROLS
  P1 POSITIVE: at least one target matches (otherwise the tag parser is broken
     and every "no match" would be meaningless);
  P2 NEGATIVE: a deliberately corrupted tag must NOT match;
  P3 NEGATIVE: a target's max must fail if (m,n) is swapped to a pair that is
     not in MN.
"""
import json
import os
import re
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "gghv_audit"))
import ggv_algorithms as G

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


TAG = re.compile(r"^(?:F(\d+)|\((\d+),(\d+)\)/(\d+)/(\d+),(\d+))\((m,n)\)?"
                 r"|\((\d+),(\d+)\)/(\d+)/(\d+),(\d+)")


def parse_tag(tag):
    """Return (A0, final, (m,n)) when the tag carries them, else None."""
    m = re.match(r"\((\d+),(\d+)\)/(\d+)/(\d+),(\d+)\s*\(m,n\)=(\d+),(\d+)", tag)
    if m:
        a, b, fa, fl, fb, mm, nn = (int(z) for z in m.groups())
        return (a, 1, b), (fa, fl, fb), (mm, nn)
    m = re.match(r"F(\d+)\(m,n\)=(\d+),(\d+)", tag.replace(" ", ""))
    if m:
        return ("family", int(m.group(1))), None, (int(m.group(2)), int(m.group(3)))
    return None


def main():
    targets = json.load(open(os.path.join(HERE, "trackD_targets.json")))
    print("=" * 78)
    print("provenance of the above-125 queue's targets")
    print("=" * 78)
    PLLC, _ = G.get_possible_last_lower_corners(120)
    raw = G.admissible_complete_chains(100, PLLC=PLLC)
    chains = {}
    for c, last in raw:
        chains[(tuple((z[0], z[1]) for z in c), last)] = (c, last)
    index = {}
    for (_, _), (c, last) in chains.items():
        A0 = c[0][0]
        v = A0[0] + A0[2]
        for k, mm, nn in G.mn_pairs(last, max_mn=400):
            index.setdefault((A0, last), set()).add((mm, nn))
    print(f"    index: {len(chains)} distinct chains, "
          f"{len(index)} (A0, final corner) shapes")

    ok_n, bad, unparsed, fam = 0, [], 0, 0
    for t in targets:
        pt = parse_tag(t["tag"])
        if pt is None:
            unparsed += 1
            continue
        if pt[0] == "family" or pt[1] is None:
            fam += 1
            continue
        A0, final, (mm, nn) = pt
        v = A0[0] + A0[2]
        have = index.get((A0, final), set())
        good = ((mm, nn) in have or (nn, mm) in have) and \
               max(mm, nn) * v == t.get("max")
        if good:
            ok_n += 1
        else:
            bad.append({"tag": t["tag"][:60], "A0": A0, "final": final,
                        "mn": [mm, nn], "recorded_max": t.get("max"),
                        "computed_max": max(mm, nn) * v,
                        "MN_at_that_corner": sorted(have)[:6]})
    print(f"    targets: {len(targets)}; chain-tagged {ok_n + len(bad)}; "
          f"family-tagged {fam}; unparsed {unparsed}")
    check("P1 POSITIVE: chain-tagged targets are matched against the independent "
          "enumeration", ok_n > 0, f"{ok_n} matched, {len(bad)} not")
    for b in bad[:6]:
        print(f"      UNMATCHED  {b}")

    fake = "(11,33)/99/4,8 (m,n)=2,3 | a=4 b=9"
    pt = parse_tag(fake)
    A0, final, (mm, nn) = pt
    check("P2 NEGATIVE: a corrupted tag does not match",
          (mm, nn) not in index.get((A0, final), set()),
          f"corrupted final corner {final}")

    real = [t for t in targets if parse_tag(t["tag"]) and
            parse_tag(t["tag"])[1] is not None]
    if real:
        A0, final, (mm, nn) = parse_tag(real[0]["tag"])
        have = index.get((A0, final), set())
        bogus = (mm + 7, nn + 11)
        check("P3 NEGATIVE: an (m,n) that is not in MN is rejected",
              bogus not in have and (bogus[1], bogus[0]) not in have,
              f"{bogus} not in {sorted(have)[:5]}")

    json.dump({"matched": ok_n, "unmatched": bad, "family_tagged": fam,
               "unparsed": unparsed,
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "h2_target_provenance.json"), "w"), indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)


if __name__ == "__main__":
    main()
