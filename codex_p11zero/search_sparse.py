#!/usr/bin/env python3
"""Witness-first exact search on coordinate-sparse p_1_1=0 loci.

Every probe solves the complete 66-equation affine late block.  Consistent
points are immediately tested against level 24, all termination equations,
the direct bracket identity, and exact Newton-polygon vertex nonvanishing.
Failure to find a point is NO VERDICT.
"""

from collections import Counter
import json
import os
import sys

from pentagon_core import (
    AFFINE_VARS,
    EARLY_VARS,
    affine_system,
    insert_affine,
    solve_affine,
    verify,
)


def solve_point(early, prime):
    M, v = affine_system(early, prime)
    rm, ra, ok, sol = solve_affine(M, v, prime)
    if not ok or sol is None:
        return (rm, ra), None, None
    point = insert_affine(early, sol)
    return (rm, ra), point, verify(point, prime)


def freeze(point, check, prime, tag):
    os.makedirs("codex_p11zero/witnesses", exist_ok=True)
    path = f"codex_p11zero/witnesses/{tag}_p{prime}.json"
    payload = {
        "prime": prime,
        "chart": {"p_1_1": 0, "p_1_0_nonzero": True},
        "point": dict(sorted(point.items())),
        "verification": check.__dict__,
        "label": "MOD-p NONEMPTY -- CE LEAD" if check.candidate else
                 "66-EQUATION LEAD -- ROOT NO VERDICT",
    }
    with open(path, "x") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
    print(f"FROZEN {path}")


def main(prime=43):
    if prime <= 40:
        raise SystemExit("prime must exceed 40")
    base = {name: 0 for name in EARLY_VARS}
    base["p_1_1"] = 0
    ranks = Counter()
    consistent = 0
    full_candidates = 0

    # Stage A: complete two-coordinate torus-aware grid.  These two entries are
    # required nonzero P data: the chart coordinate p_1_0 and vertex p_8_0.
    total = (prime - 1) ** 2
    print(f"STAGE A: exhaustive p_1_0,p_8_0 in F_{prime}^* ({total} probes)", flush=True)
    for p10 in range(1, prime):
        for p80 in range(1, prime):
            early = dict(base)
            early["p_1_0"] = p10
            early["p_8_0"] = p80
            rank_pair, point, check = solve_point(early, prime)
            ranks[rank_pair] += 1
            if point is None:
                continue
            consistent += 1
            print(f"  66-EQ CONSISTENT p_1_0={p10} p_8_0={p80}: {check}", flush=True)
            freeze(point, check, prime, f"stageA_{p10}_{p80}")
            if check.candidate:
                full_candidates += 1
                print("MOD-p NONEMPTY -- CE LEAD")
                return 0

    print(f"STAGE A complete: consistent={consistent}/{total}; ranks={dict(ranks)}", flush=True)

    # Stage B: one additional coordinate at unit value.  This is not exhaustive;
    # it is a cheap audit of every coordinate hyperplane direction.
    print("STAGE B: each remaining early coordinate = 1 once", flush=True)
    for name in EARLY_VARS:
        if name in {"p_1_0", "p_1_1", "p_8_0"}:
            continue
        early = dict(base)
        early["p_1_0"] = 1
        early["p_8_0"] = 1
        early[name] = 1
        rank_pair, point, check = solve_point(early, prime)
        ranks[rank_pair] += 1
        if point is None:
            continue
        consistent += 1
        print(f"  66-EQ CONSISTENT extra={name}: {check}", flush=True)
        freeze(point, check, prime, f"stageB_{name}")
        if check.candidate:
            full_candidates += 1
            print("MOD-p NONEMPTY -- CE LEAD")
            return 0

    print(f"SEARCH complete: 66-equation consistent leads={consistent}; "
          f"full candidates={full_candidates}; ranks={dict(ranks)}")
    print("VERDICT: NO VERDICT")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 43))
