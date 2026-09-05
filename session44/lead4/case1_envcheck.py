#!/usr/bin/env python3
"""Environment check: re-run the campaign's own Singular pipeline on the
target that an independent run of it decided EMPTY."""
import json, os
os.environ.setdefault("TRACKD_SCRATCH",
                      os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "_scratch_case1"))
import trackD_extract as TE
t = json.load(open("trackD_targets_validate.json"))[0]
print("target:", t["tag"])
print("expected (independent Singular pipeline): EMPTY")
res = TE.run([tuple(v) for v in t["NP"]], [tuple(v) for v in t["NQ"]],
             t["r"], "case1_envcheck", timeout=2400)
print("status", res["status"], "%.0fs" % res.get("secs", 0))
for line in (res.get("out") or "").splitlines():
    print("   ", line)
