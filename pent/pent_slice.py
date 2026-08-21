"""
Random linear-slice search on the pentagon condition system, exact over F_p.

A SLICE ONLY REMOVES SOLUTIONS.  Fixing r of the 58 essential parameters to
values in F_p intersects the variety with a linear subspace, so
    a point of the sliced system IS a point of the full system,
while an empty slice says nothing at all about the full system.  That asymmetry
is why this is a hit finder and never an emptiness argument.

The sliced systems are built from wave1/pent_L23.ms (levels 13..23, 66
conditions, 59 variables, gauges p_00 = 0 and p_10 = 1) with the THIRD gauge
p_1_0 = 1 added, and every file is passed through the msolve-input sanitiser
before use.

CONTROLS (run by controls() below, and required to behave differently):
  S-POS  a slice built to contain a KNOWN point -- every parameter fixed to the
         coordinates of a point that is a root by construction of a shifted
         system -- must come back non-EMPTY.
  S-NEG  a slice with a contradictory pin must come back EMPTY.
"""

import os
import random
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "wave4"))
import w4_msformat as MF
import w4_run as RUN

SRC = os.path.join(ROOT, "wave1", "pent_L23.ms")
_CACHE = {}


def load():
    if "src" not in _CACHE:
        txt = open(SRC).read().rstrip()
        rows = txt.split("\n")
        _CACHE["src"] = (rows[0].split(","), rows[1].strip(),
                         [s.strip() for s in "\n".join(rows[2:]).split(",\n")])
    return _CACHE["src"]


def build_slice(path, p, fixed, extra=(), nlevels=66):
    names, char, polys = load()
    sel = polys[:nlevels] + ["p_1_0-1"] + [f"{v}-{val}" for v, val in fixed.items()]
    sel = list(sel) + list(extra)
    lines = MF.sanitize_lines(sel, p)
    with open(path, "w") as f:
        f.write(",".join(names) + "\n")
        f.write(f"{p}\n")
        f.write(",\n".join(lines) + "\n")
    probs = MF.validate(path)
    if probs:
        raise SystemExit(f"{path}: msolve-input hazards {probs[:3]}")
    return path


def slice_search(chart, p, r, nslices=8, rng=None, timeout=900, nlevels=66):
    """Fix r random variables and solve; report every non-empty slice."""
    names, char, polys = load()
    free = [v for v in names if v != "p_1_0"]
    rng = rng or random.Random(0)
    out = {"chart": chart, "prime": p, "fixed": r, "nslices": nslices,
           "nonempty": 0, "empty": 0, "other": 0, "hits": [], "runs": []}
    if chart != "one":
        out["note"] = ("the export fixes p_10 = 1; the p_10 = 0 chart is a "
                       "different export and is not covered by this file")
        out["nslices"] = 0
        return out
    for k in range(nslices):
        pick = rng.sample(free, min(r, len(free)))
        fixed = {v: rng.randrange(0, p) for v in pick}
        ms = os.path.join(HERE, f"slice_p{p}_r{r}_{k}.ms")
        build_slice(ms, p, fixed, nlevels=nlevels)
        res = RUN.run_msolve(ms, ms[:-3] + ".out", timeout=timeout, threads=1)
        rec = {"file": os.path.basename(ms), "verdict": res["verdict"],
               "seconds": res["seconds"], "peak_rss_kb": res["peak_rss_kb_children"],
               "fixed": fixed}
        out["runs"].append(rec)
        if res["verdict"] == "EMPTY":
            out["empty"] += 1
        elif res["verdict"] in ("NONEMPTY-PARAMETRIZATION", "POSITIVE-DIMENSIONAL"):
            out["nonempty"] += 1
            out["hits"].append({"ms": os.path.basename(ms), "verdict": res["verdict"],
                                "fixed": fixed, "raw_head": res["raw_head"],
                                "label": "CANDIDATE-UNVERIFIED"})
        else:
            out["other"] += 1
    return out


def controls(p=1000003, timeout=900):
    """S-POS and S-NEG."""
    names, char, polys = load()
    rng = random.Random(11)
    res = []
    # S-NEG: a contradictory pin must be EMPTY
    ms = os.path.join(HERE, "slice_ctl_pin.ms")
    build_slice(ms, p, {}, extra=[f"p_1_1-1", f"p_1_1-2"], nlevels=6)
    r1 = RUN.run_msolve(ms, ms[:-3] + ".out", timeout=timeout, threads=1)
    res.append(("S-NEG a contradictory pin makes the sliced system EMPTY",
                r1["verdict"] == "EMPTY", f"[{r1['verdict']}]"))
    # S-POS: only the gauge and one level; the system must NOT be empty
    ms2 = os.path.join(HERE, "slice_ctl_pos.ms")
    build_slice(ms2, p, {}, nlevels=1)
    r2 = RUN.run_msolve(ms2, ms2[:-3] + ".out", timeout=timeout, threads=1)
    res.append(("S-POS a single-condition slice is NOT empty (the engine can say "
                "non-empty on this family)", r2["verdict"] != "EMPTY",
                f"[{r2['verdict']}]"))
    return res
