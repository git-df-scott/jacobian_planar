#!/usr/bin/env python3
"""Search the p_1_1=0 chart on the necessary square top-edge locus.

For a genuine pentagon point, the top form of P is a*S^2 with S quartic.
This probe fixes a=p_1_0=s_0=s_4=1, exhausts s_1,s_2,s_3 over F_p, and solves
the nine remaining affine variables exactly.  The slice is witness-capable but
an empty slice is NO VERDICT on the root.
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


TOP_NAMES = [f"p_{8+i}_{i}" for i in range(9)]


def square_coefficients(s, p):
    out = [0] * 9
    for i, a in enumerate(s):
        for j, b in enumerate(s):
            out[i + j] = (out[i + j] + a * b) % p
    return out


def constrained_solve(early, fixed_late, prime):
    M, v = affine_system(early, prime)
    fixed_indices = {AFFINE_VARS.index(name): value % prime
                     for name, value in fixed_late.items()}
    free_indices = [i for i in range(len(AFFINE_VARS)) if i not in fixed_indices]
    shifted = [(v[r] + sum(M[r][c] * value
                           for c, value in fixed_indices.items())) % prime
               for r in range(len(v))]
    reduced = [[M[r][c] for c in free_indices] for r in range(len(M))]
    rm, ra, ok, solution = solve_affine(reduced, shifted, prime)
    if not ok or solution is None:
        return (rm, ra), None
    late = [0] * len(AFFINE_VARS)
    for c, value in fixed_indices.items():
        late[c] = value
    for k, c in enumerate(free_indices):
        late[c] = solution[k]
    return (rm, ra), insert_affine(early, late)


def freeze(point, check, prime, tag):
    os.makedirs("codex_p11zero/witnesses", exist_ok=True)
    path = f"codex_p11zero/witnesses/top_{tag}_p{prime}.json"
    with open(path, "x") as handle:
        json.dump({
            "prime": prime,
            "slice": "p_1_1=0,p_1_0=1,a=1,s_0=s_4=1",
            "point": dict(sorted(point.items())),
            "verification": check.__dict__,
            "label": "MOD-p NONEMPTY -- CE LEAD" if check.candidate else
                     "66-EQUATION LEAD -- ROOT NO VERDICT",
        }, handle, indent=2, sort_keys=True)
    print(f"FROZEN {path}")


def main(prime=29):
    if prime <= 24:
        raise SystemExit("prime must exceed 24")
    total = prime ** 3
    print(f"Exhaustive square-top slice over F_{prime}: {total} points", flush=True)
    ranks = Counter()
    consistent = promising = 0
    base = {name: 0 for name in EARLY_VARS}
    base["p_1_0"] = 1
    base["p_1_1"] = 0

    for s1 in range(prime):
        for s2 in range(prime):
            for s3 in range(prime):
                s = [1, s1, s2, s3, 1]
                top = square_coefficients(s, prime)
                early = dict(base)
                fixed_late = {}
                for name, value in zip(TOP_NAMES, top):
                    if name in AFFINE_VARS:
                        fixed_late[name] = value
                    else:
                        early[name] = value
                rank_pair, point = constrained_solve(early, fixed_late, prime)
                ranks[rank_pair] += 1
                if point is None:
                    continue
                consistent += 1
                check = verify(point, prime)
                if check.vertices_nonzero:
                    promising += 1
                    tag = f"{s1}_{s2}_{s3}"
                    print(f"PROMISING s={s}: {check}", flush=True)
                    freeze(point, check, prime, tag)
                if check.candidate:
                    print("MOD-p NONEMPTY -- CE LEAD")
                    return 0
        print(f"  s1={s1}: consistent={consistent}, promising={promising}", flush=True)

    print(f"Complete: consistent={consistent}/{total}; promising={promising}; "
          f"ranks={dict(ranks)}")
    print("VERDICT: NO VERDICT")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 29))
