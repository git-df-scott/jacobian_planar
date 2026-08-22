#!/usr/bin/env python3
"""Exact tangent-space audit at the degenerate full-system solution."""

import sys

from pentagon_core import VARS, jacobian, nullspace_mod, rank_mod, verify


def main(prime=43):
    point = {name: 0 for name in VARS}
    point["p_1_0"] = 1
    point["p_1_1"] = 0
    check = verify(point, prime)
    if not (check.exported_zero and check.full_zero and check.bracket_zero):
        raise AssertionError("anchor is not an exact full-system solution")

    chart_vars = [name for name in VARS if name != "p_1_1"]
    for full, label in ((False, "66-export"), (True, "full-support")):
        J = jacobian(point, prime, chart_vars, full=full)
        rank = rank_mod(J, prime)
        kernel = nullspace_mod(J, prime)
        print(f"{label}: equations={len(J)} variables={len(chart_vars)} "
              f"rank={rank} tangent_dim={len(kernel)}")
        for vertex in ("p_8_0", "p_14_8", "p_16_8"):
            index = chart_vars.index(vertex)
            movable = any(vector[index] % prime for vector in kernel)
            print(f"  tangent can turn on {vertex}: {movable}")
    print("VERDICT: NO VERDICT")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 43))
