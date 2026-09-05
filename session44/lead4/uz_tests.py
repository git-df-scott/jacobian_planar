#!/usr/bin/env python3
"""The falsification tests.

The obstruction ideal I lives in Q[f1..f8, p1..p8, q2..q8] (q1 = 1 gauge).
It is weighted-homogeneous for  W(f_a)=5a+1, W(p_a)=5a-2, W(q_a)=5a-5,
which is exactly the residual 1-parameter gauge torus after q1 = 1.  So any
coefficient of nonzero weight can be normalised to 1 whenever it is nonzero
(over an algebraically closed field).  That converts every "is X forced to
vanish?" question into a consistency question with X = 1 -- no Rabinowitsch
variable needed.

  T1  I + (f5-1)                     f5 = a_10_5 nonzero at all?
  T2  I + (f1, f2, f5-1)             THE PREDICTION TEST
  T3  I + (f1, f2)                   is the constrained system consistent?
  T4  I + (f1-1)                     is a_2_1 = 0 really forced?  (control)
  T5  I + (f1, f2, f8-1)             can the vertex (8,16) be nonzero?
  T6  I + (f1, f2, f5-1, f8-1)       ... not usable, two gauge fixings
"""
import os
import subprocess
import sys
import time

from uz_export import obstruction_system, write_ms, write_singular

HERE = os.path.dirname(os.path.abspath(__file__))


def build(fixed, extra_named):
    live, polys = obstruction_system(fixed)
    body = [s for _, s in polys] + list(extra_named)
    return live, body


def run_msolve(name, variables, body, char, threads=4, timeout=3600):
    path = os.path.join(HERE, f"{name}.ms")
    out = os.path.join(HERE, f"{name}.out")
    write_ms(path, variables, body, char)
    t0 = time.time()
    try:
        subprocess.run(["msolve", "-f", path, "-o", out, "-t", str(threads)],
                       check=False, timeout=timeout,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return name, char, "TIMEOUT", time.time() - t0
    txt = open(out).read().strip() if os.path.exists(out) else ""
    if txt.startswith("[-1]"):
        v = "NO SOLUTION (ideal = (1))"
    elif txt.startswith("[1,") and ",-1,[]" in txt.replace(" ", ""):
        v = "INFINITELY MANY SOLUTIONS (positive dimension)"
    elif txt:
        v = "SOLUTIONS EXIST (0-dimensional parametrisation returned)"
    else:
        v = "no output"
    return name, char, v, time.time() - t0


TESTS = {
    "T1_f5nz":        ({}, ["f5-1"]),
    "T2_f1f2_f5nz":   ({"f1": 0, "f2": 0}, ["f5-1"]),
    "T3_f1f2":        ({"f1": 0, "f2": 0}, []),
    "T4_f1nz":        ({}, ["f1-1"]),
    "T5_f1f2_f8nz":   ({"f1": 0, "f2": 0}, ["f8-1"]),
    "T7_f1_p1_f2nz":  ({"f1": 0, "p1": 0}, ["f2-1"]),
    "T8_f1f2p1_f5nz": ({"f1": 0, "f2": 0, "p1": 0}, ["f5-1"]),
    "T9_f1f2_f3nz":   ({"f1": 0, "f2": 0}, ["f3-1"]),
    "T10_f1f2_f4nz":  ({"f1": 0, "f2": 0}, ["f4-1"]),
    "T11_f1f2_f6nz":  ({"f1": 0, "f2": 0}, ["f6-1"]),
    "T12_f1f2_f7nz":  ({"f1": 0, "f2": 0}, ["f7-1"]),
    "T13_f1f2_p1nz":  ({"f1": 0, "f2": 0}, ["p1-1"]),
}

if __name__ == "__main__":
    chars = [int(c) for c in (sys.argv[1].split(",") if len(sys.argv) > 1
                              else ["65521"])]
    names = sys.argv[2].split(",") if len(sys.argv) > 2 else list(TESTS)
    for nm in names:
        fixed, extra = TESTS[nm]
        live, body = build(fixed, extra)
        for ch in chars:
            r = run_msolve(f"{nm}_c{ch}", live, body, ch)
            print(f"{r[0]:24s} char={r[1]:<12} {r[2]:52s} {r[3]:7.1f}s",
                  flush=True)
