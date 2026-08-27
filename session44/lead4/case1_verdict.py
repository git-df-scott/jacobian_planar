#!/usr/bin/env python3
"""Decide subcase 1 modulo p: run the cascade + vertex non-degeneracy on
EVERY one of the five essential-face covers, at a prime where all five are
F_p-rational."""
import sys
import case1_nondeg as ND
from case1_point import find

p = int(sys.argv[1]); stopW = int(sys.argv[2]) if len(sys.argv) > 2 else -12
for w in range(5):
    r, err = find(p, w)
    if err:
        print("cover %d: %s" % (w, err), flush=True)
        continue
    print("=== p=%d cover %d/%d  f=%s" % (p, w, r[4], r[1]), flush=True)
    ND.main(p, w, stopW)
    print("", flush=True)
