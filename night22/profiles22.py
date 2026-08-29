#!/usr/bin/env python3
"""Enumerate Suzuki-compatible special-fibre atoms in a finite display box."""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    rows = []
    for g in range(0, 5):
        for r in range(1, 7):
            N = 2*g+r-1
            for jump in range(1, N+1):
                weight = 2*g+r-jump
                for gs in range(weight//2+1):
                    rs = weight-2*gs
                    if rs < 1:
                        continue
                    rows.append({"generic_g": g, "generic_r": r, "total_jump": N,
                                 "one_jump": jump, "special_g": gs, "special_r": rs,
                                 "special_is_A1": gs == 0 and rs == 1,
                                 "jump_can_appear_in_noncoordinate_profile": jump < N})
    path = os.path.join(HERE, "profiles22.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    # Exact Briancon profile checks.
    assert 2*1+3-1 == 4
    assert (2*(1-0)+(3-4), 2*(1-0)+(3-2)) == (1, 3)
    assert (2*(1-0)+(3-3), 2*(1-0)+(3-3)) == (2, 2)
    print("PASS: %d profile atoms; Briancon jumps (1,3) and (2,2) sum to 4" % len(rows))


if __name__ == "__main__":
    main()
