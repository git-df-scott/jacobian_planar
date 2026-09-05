#!/usr/bin/env python3
"""
Run every map-verification file in this directory and print a summary table.

Each map file is standalone: it contains the explicit polynomials and its own
checks, prints PASS/FAIL per check, and exits nonzero on any failure.

  python3 run_all.py            # run all
  python3 run_all.py --quick    # skip the two slowest (degree 7 and 12)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (file, dimension, expected det J, expected geometric degree, slow?)
MAPS = [
    ("dim3_degree6.py",            3, "2",      6,  False),
    ("gallagher_dim3_degree6.py",  3, "1",      6,  False),
    ("dim3_degree7.py",            3, "2",      7,  True),
    ("gallagher_dim3_degree12.py", 3, "1",     12,  True),
    ("gao_F5_dim4_degree10.py",    4, "160/29", 10, False),
    ("alpoge_dim3_degree3.py",     3, "2",      3,  False),
    ("gao_G_dim3_degree4.py",      3, "2",      4,  False),
    ("gallagher_dim3_degree3.py",  3, "1",      3,  False),
]


def main():
    quick = "--quick" in sys.argv
    rows = []
    for fname, dim, detj, deg, slow in MAPS:
        if quick and slow:
            rows.append((fname, dim, detj, deg, "SKIPPED", "-"))
            continue
        path = os.path.join(HERE, fname)
        print("running %s ..." % fname, flush=True)
        r = subprocess.run([sys.executable, path], capture_output=True, text=True)
        out = r.stdout
        m = re.search(r"MEASURED geometric deg\s*:\s*(\S+)", out)
        measured = m.group(1) if m else "?"
        nfail = out.count("[FAIL]")
        status = "PASS" if (r.returncode == 0 and nfail == 0) else "FAIL(%d)" % nfail
        rows.append((fname, dim, detj, deg, status, measured))

    w = max(len(r[0]) for r in rows) + 2
    print("\n" + "=" * (w + 52))
    print("%-*s %4s %10s %9s %10s %9s" % (w, "map file", "dim", "det J", "expected", "status", "MEASURED"))
    print("-" * (w + 52))
    bad = 0
    for fname, dim, detj, deg, status, measured in rows:
        print("%-*s %4d %10s %9d %10s %9s" % (w, fname, dim, detj, deg, status, measured))
        if status.startswith("FAIL"):
            bad += 1
    print("=" * (w + 52))
    if bad:
        print("%d map(s) FAILED" % bad)
        return 1
    print("all runs passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
