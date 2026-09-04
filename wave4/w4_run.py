"""wave4 / thin msolve + Singular runner with artifact parsing.

Rules enforced here, not left to the caller:

  * a 0-byte output file is a FAILURE, never a result;
  * the verdict is read from the PARSED artifact, never from the exit code
    alone and never from the filename;
  * peak RSS and wall time are recorded for every run;
  * engines are stopped with `kill` on the exact pid, never `pkill -f`.
"""

import json
import os
import resource
import subprocess
import time


def _rusage_peak_kb(before):
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return max(0, r.ru_maxrss - before)


def run_msolve(ms_path, out_path, timeout=900, threads=1, extra=()):
    before = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    cmd = ["msolve", "-f", ms_path, "-o", out_path, "-t", str(threads)] + list(extra)
    t0 = time.time()
    timed_out = False
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        rc, so, se = pr.returncode, pr.stdout, pr.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se, timed_out = None, (e.stdout or b"").decode(errors="replace"), \
            (e.stderr or b"").decode(errors="replace"), True
    dt = time.time() - t0
    peak = _rusage_peak_kb(before)
    raw = None
    size = os.path.getsize(out_path) if os.path.exists(out_path) else -1
    if size > 0:
        with open(out_path) as f:
            raw = f.read()
    return {
        "cmd": " ".join(cmd), "returncode": rc, "timed_out": timed_out,
        "seconds": round(dt, 2), "peak_rss_kb_children": peak,
        "out_bytes": size, "stdout": so[-4000:], "stderr": se[-4000:],
        "raw_head": (raw[:400] if raw else None),
        "raw_tail": (raw[-400:] if raw and len(raw) > 400 else None),
        "verdict": classify_msolve(raw, size, rc, timed_out),
    }


def classify_msolve(raw, size, rc, timed_out):
    """Verdict from the PARSED artifact.

    msolve writes `[-1]:` when the system has no solution in the algebraic
    closure, and `[1, nvars, -1, []]:` when the solution set is positive
    dimensional.  Anything else that parses is a rational parametrization, i.e.
    a NON-EMPTY zero-dimensional solution set.
    """
    if timed_out:
        return "TIMEOUT"
    if size == 0:
        return "FAIL-EMPTY-FILE"
    if size < 0 or raw is None:
        return "FAIL-NO-FILE"
    s = raw.strip()
    if not s:
        return "FAIL-EMPTY-FILE"
    body = s.rstrip(":").strip()
    if body == "[-1]":
        return "EMPTY"
    if body.startswith("[1,") and ",-1," in body.replace(" ", ""):
        return "POSITIVE-DIMENSIONAL"
    if body.startswith("["):
        return "NONEMPTY-PARAMETRIZATION"
    return f"FAIL-UNPARSED(rc={rc})"


def run_singular(sing_path, timeout=900):
    before = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    t0 = time.time()
    timed_out = False
    try:
        pr = subprocess.run(["Singular", "-q", "--no-warn", sing_path],
                            capture_output=True, text=True, timeout=timeout)
        rc, so, se = pr.returncode, pr.stdout, pr.stderr
    except subprocess.TimeoutExpired as e:
        rc, timed_out = None, True
        so = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        se = (e.stderr or b"").decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
    dt = time.time() - t0
    return {"cmd": f"Singular -q {sing_path}", "returncode": rc,
            "timed_out": timed_out, "seconds": round(dt, 2),
            "peak_rss_kb_children": _rusage_peak_kb(before),
            "stdout": so, "stderr": se[-2000:]}


def save(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
    return path
