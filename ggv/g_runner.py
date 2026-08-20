#!/usr/bin/env python3
"""GGV evidence campaign -- serialized msolve runner with artifact-only verdicts.

Contract enforced here (campaign standing rules):
  * ONE msolve process at a time.  This module has no concurrency.
  * Verdicts are parsed from the OUTPUT ARTIFACT's bytes, never from the
    filename and never from the exit code alone.  A 0-byte or missing output
    file is a FAILED RUN (NO-OUTPUT), never a verdict.
  * Peak RSS is recorded for every run from /usr/bin/time -v.
  * Memory is bounded with an explicit, RECORDED address-space cap so a run
    dies as STALLED-OOM instead of taking the machine down.  The cap is a
    property of the run and is written into every record.

Verdict classes:
  EMPTY                  output artifact is exactly msolve's "[-1]:"
  CANDIDATE-UNVERIFIED   output artifact is non-empty and is not "[-1]:"
  STALLED-OOM            killed by the OOM killer / hit the recorded cap
  TIMEOUT                exceeded the recorded wall-clock limit
  NO-OUTPUT              process ended without producing output bytes
"""
import os, re, subprocess, sys, time

VMCAP_KB = 13_000_000          # ~13 GB address space; RECORDED in every row
DEFAULT_TIMEOUT = 3600


def classify(out_path, rc, timed_out, stderr_text):
    """Verdict from the artifact first; failure modes only when there is none."""
    data = b""
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            data = f.read()
    body = data.decode("utf-8", "replace").strip()
    if body:
        # msolve prints "[-1]:" (possibly with trailing newline) for the empty
        # variety.  Anything else with content is a candidate we do not analyse.
        if re.fullmatch(r"\[\s*-1\s*\]\s*:?", body):
            return "EMPTY", len(data)
        return "CANDIDATE-UNVERIFIED", len(data)
    if timed_out:
        return "TIMEOUT", len(data)
    oom_markers = ("std::bad_alloc", "Cannot allocate memory", "out of memory",
                   "memory exhausted", "Killed")
    if rc in (-9, 137) or any(m in stderr_text for m in oom_markers):
        return "STALLED-OOM", len(data)
    return "NO-OUTPUT", len(data)


def run(ms_in, out_path, extra_args=(), timeout=DEFAULT_TIMEOUT, vmcap_kb=VMCAP_KB):
    """Run msolve once, serialized.  Returns a record dict."""
    if not os.path.exists(ms_in):
        raise FileNotFoundError(ms_in)
    in_bytes = os.path.getsize(ms_in)
    if in_bytes == 0:
        raise ValueError(f"refusing to run on a 0-byte input: {ms_in}")
    if os.path.exists(out_path):
        os.remove(out_path)
    cmd = ["/usr/bin/time", "-v", "msolve", *extra_args, "-f", ms_in, "-o", out_path]
    shell = "ulimit -v %d; exec %s" % (vmcap_kb, " ".join("'%s'" % c for c in cmd))
    t0 = time.time()
    timed_out = False
    try:
        p = subprocess.run(["/bin/bash", "-c", shell], capture_output=True,
                           text=True, timeout=timeout)
        rc, err = p.returncode, p.stderr
    except subprocess.TimeoutExpired as e:
        timed_out = True
        rc, err = None, (e.stderr or b"").decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
    wall = time.time() - t0
    m = re.search(r"Maximum resident set size \(kbytes\): (\d+)", err or "")
    rss_kb = int(m.group(1)) if m else -1
    verdict, out_bytes = classify(out_path, rc, timed_out, err or "")
    return {"input": ms_in, "output": out_path, "args": " ".join(extra_args) or "-",
            "exit": ("TIMEOUT" if timed_out else str(rc)), "wall_s": round(wall, 2),
            "peak_rss_kb": rss_kb, "vmcap_kb": vmcap_kb, "timeout_s": timeout,
            "in_bytes": in_bytes, "out_bytes": out_bytes, "verdict": verdict,
            "stderr_tail": (err or "").strip().splitlines()[-1:] and (err or "").strip().splitlines()[-1][:200] or ""}


if __name__ == "__main__":
    rec = run(sys.argv[1], sys.argv[2], tuple(sys.argv[3:]))
    for k, v in rec.items():
        print(f"{k}\t{v}")
