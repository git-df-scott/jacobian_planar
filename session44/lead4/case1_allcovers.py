#!/usr/bin/env python3
"""Run the weight descent on ALL FIVE covers at a prime where all five are
F_p-rational (h splits completely and 7 does not divide p-1)."""
import sys
from case1_descend import run
from case1_point import find

p = int(sys.argv[1]) if len(sys.argv) > 1 else 5189
for w in range(5):
    r, err = find(p, w)
    if err:
        print("cover %d: %s" % (w, err), flush=True)
        continue
    av, f, g, bad, nr = r
    print("=== p=%d cover %d/%d  f=%s" % (p, w, nr, f), flush=True)
    res, err = run(p, w, verbose=True)
    print("   RESULT cover %d: %s" % (w, res if res else err), flush=True)
