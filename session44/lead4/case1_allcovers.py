#!/usr/bin/env python3
"""Accumulate the cascade conditions for ALL FIVE covers at a prime where all
five essential-face covers are F_p-rational (h splits, 7 nmid p-1)."""
import sys
from case1_descend import run
from case1_point import find

p = int(sys.argv[1]) if len(sys.argv) > 1 else 5189
stopW = int(sys.argv[2]) if len(sys.argv) > 2 else -8
for w in range(5):
    r, err = find(p, w)
    if err:
        print("cover %d: %s" % (w, err), flush=True)
        continue
    av, f, g, bad, nr = r
    print("=== p=%d cover %d/%d  f=%s" % (p, w, nr, f), flush=True)
    res, err = run(p, w, verbose=False, check_at=(),
                   dump="_scratch_case1/conds_%d_%d.txt" % (p, w),
                   stopW=stopW)
    print("   accumulated: %s" % (res,), flush=True)
