#!/usr/bin/env python3
"""GGV campaign GATE -- must pass before any new computation.

Three parts:
  1. wave5/w5_b16_abel.py must print ALL PASS (transcription certification).
  2. wave5/ms2/b16r_d5_{A,B}_p1000003.ms must both re-solve to [-1].
  3. NEGATIVE CONTROLS on the verdict classifier itself, required to FAIL the
     EMPTY verdict:
       - a zero-dimensional ideal <x^2-1, y-2> must NOT classify as EMPTY;
       - a 0-byte output artifact must NOT classify as EMPTY.
Every condition below is computed from a run or a file; none is a literal.
"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_runner import run, classify

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("GGV_SCRATCH", tempfile.mkdtemp(prefix="ggvgate"))
FAIL = []

def check(label, cond, note=""):
    print(("PASS " if cond else "FAIL ") + label + (f"   [{note}]" if note else ""))
    if not cond:
        FAIL.append(label)

# --- 1. transcription certifier -------------------------------------------
p = subprocess.run([sys.executable, os.path.join(REPO, "wave5", "w5_b16_abel.py")],
                   capture_output=True, text=True, cwd=REPO)
abel_out = p.stdout
check("GATE-1 w5_b16_abel.py prints ALL PASS",
      abel_out.strip().endswith("ALL PASS") and p.returncode == 0,
      f"exit={p.returncode}")

# --- 2. d=5 reduced-chart regression --------------------------------------
for chart in ("A", "B"):
    src = os.path.join(REPO, "wave5", "ms2", f"b16r_d5_{chart}_p1000003.ms")
    out = os.path.join(SCRATCH, f"gate_d5_{chart}.out")
    rec = run(src, out, timeout=1800)
    check(f"GATE-2 d=5 chart {chart} p=1000003 re-solves to EMPTY",
          rec["verdict"] == "EMPTY",
          f"verdict={rec['verdict']} exit={rec['exit']} rss_kb={rec['peak_rss_kb']} "
          f"wall={rec['wall_s']}s out_bytes={rec['out_bytes']}")

# --- 3. classifier negative controls --------------------------------------
zd_in = os.path.join(SCRATCH, "neg_zerodim.ms")
open(zd_in, "w").write("x,y\n1000003\nx^2-1,\ny-2\n")
zd_out = os.path.join(SCRATCH, "neg_zerodim.out")
rec_zd = run(zd_in, zd_out, timeout=120)
check("GATE-3 negative control: zero-dimensional ideal is NOT classified EMPTY",
      rec_zd["verdict"] != "EMPTY",
      f"verdict={rec_zd['verdict']} out_bytes={rec_zd['out_bytes']}")

zero_out = os.path.join(SCRATCH, "neg_zerobyte.out")
open(zero_out, "wb").close()
v_zero, n_zero = classify(zero_out, 0, False, "")
check("GATE-3 negative control: 0-byte artifact is NOT classified EMPTY",
      v_zero != "EMPTY", f"verdict={v_zero} bytes={n_zero}")

# a positive control for the classifier so the two negatives carry information
emp_out = os.path.join(SCRATCH, "pos_empty.out")
open(emp_out, "w").write("[-1]:\n")
v_emp, _ = classify(emp_out, 0, False, "")
check("GATE-3 positive control: a literal [-1]: artifact IS classified EMPTY",
      v_emp == "EMPTY", f"verdict={v_emp}")

print("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL))
sys.exit(1 if FAIL else 0)
