#!/usr/bin/env python3
"""GGV evidence campaign -- serialized msolve runner with artifact-only verdicts.

Contract enforced here (campaign standing rules):
  * ONE msolve process at a time.  This module has no concurrency, and on a
    timeout it kills the WHOLE process group it started -- an orphaned engine
    left running past its deadline would silently overlap the next job.
  * Verdicts are parsed from the OUTPUT ARTIFACT's bytes, never from the
    filename and never from the exit code alone.  A 0-byte or missing output
    file is a FAILED RUN, never a verdict.
  * Peak RSS is recorded for every run from /usr/bin/time -v.
  * Memory policy: NO artificial address-space cap.  An address-space ceiling
    was tried first and rejected -- msolve's virtual reservations exceed its
    resident set, so the cap turned survivable runs into SIGSEGV on an
    unchecked failed allocation, i.e. it changed the mathematics.  Instead the
    engine is given oom_score_adj 1000 so the kernel OOM killer takes the
    engine and nothing else; that arrives as returncode -9/137 and is recorded
    as STALLED-OOM, exactly as the campaign tooling contract specifies.

Verdict classes:
  EMPTY                  output artifact is exactly msolve's "[-1]:"
  CANDIDATE-UNVERIFIED   output artifact is non-empty and is not "[-1]:"
  STALLED-OOM            killed by the OOM killer, or reported out of memory
  TIMEOUT                exceeded the recorded wall-clock limit
  CRASH                  died on a signal that is not the OOM kill (e.g. SIGSEGV)
  NO-OUTPUT              ended without producing output bytes for any other reason
"""
import os, re, signal, subprocess, sys, time

DEFAULT_TIMEOUT = 3600
OOM_MARKERS = ("std::bad_alloc", "Cannot allocate memory", "out of memory",
               "memory exhausted", "Out of memory")


def classify(out_path, rc, timed_out, stderr_text):
    """Verdict from the artifact first; failure modes only when there is none."""
    data = b""
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            data = f.read()
    body = data.decode("utf-8", "replace").strip()
    if body:
        # msolve prints "[-1]:" for the empty variety.  Anything else with
        # content is a candidate this pipeline does not analyse.
        if re.fullmatch(r"\[\s*-1\s*\]\s*:?", body):
            return "EMPTY", len(data)
        return "CANDIDATE-UNVERIFIED", len(data)
    if timed_out:
        return "TIMEOUT", len(data)
    err = stderr_text or ""
    if rc in (-9, 137) or any(m in err for m in OOM_MARKERS) or "Killed" in err:
        return "STALLED-OOM", len(data)
    if isinstance(rc, int) and (rc < 0 or rc > 128):
        return "CRASH", len(data)
    return "NO-OUTPUT", len(data)


def run(ms_in, out_path, extra_args=(), timeout=DEFAULT_TIMEOUT):
    """Run msolve once, serialized, in its own process group.  Returns a record."""
    if not os.path.exists(ms_in):
        raise FileNotFoundError(ms_in)
    in_bytes = os.path.getsize(ms_in)
    if in_bytes == 0:
        raise ValueError(f"refusing to run on a 0-byte input: {ms_in}")
    if os.path.exists(out_path):
        os.remove(out_path)
    quoted = " ".join("'%s'" % c for c in
                      ["/usr/bin/time", "-v", "msolve", *extra_args,
                       "-f", ms_in, "-o", out_path])
    # oom_score_adj is inherited across exec, so the engine (not this session)
    # is what the kernel reclaims first.
    script = "echo 1000 > /proc/self/oom_score_adj 2>/dev/null; exec " + quoted
    t0 = time.time()
    timed_out = False
    p = subprocess.Popen(["/bin/bash", "-c", script], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        _, err = p.communicate(timeout=timeout)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        # kill the whole group: /usr/bin/time and the engine underneath it
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(os.getpgid(p.pid), sig)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                _, err = p.communicate(timeout=30)
                break
            except subprocess.TimeoutExpired:
                err = ""
        else:
            err = ""
        rc = p.returncode
        # no engine of ours may outlive its deadline
        deadline = time.time() + 60
        while time.time() < deadline:
            leftover = subprocess.run(["pgrep", "-x", "msolve"],
                                      capture_output=True, text=True).stdout.split()
            if not leftover:
                break
            for pid in leftover:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except (ProcessLookupError, ValueError, PermissionError):
                    pass
            time.sleep(1)
    wall = time.time() - t0
    m = re.search(r"Maximum resident set size \(kbytes\): (\d+)", err or "")
    rss_kb = int(m.group(1)) if m else -1
    verdict, out_bytes = classify(out_path, rc, timed_out, err or "")
    tail = ""
    if err:
        lines = [l for l in err.strip().splitlines() if l.strip()]
        if lines:
            tail = lines[-1].strip()[:200]
    return {"input": ms_in, "output": out_path, "args": " ".join(extra_args) or "-",
            "exit": ("TIMEOUT" if timed_out else str(rc)), "wall_s": round(wall, 2),
            "peak_rss_kb": rss_kb, "mem_policy": "oom_score_adj=1000, no vm cap",
            "timeout_s": timeout, "in_bytes": in_bytes, "out_bytes": out_bytes,
            "verdict": verdict, "stderr_tail": tail}


if __name__ == "__main__":
    rec = run(sys.argv[1], sys.argv[2], tuple(sys.argv[3:]))
    for k, v in rec.items():
        print(f"{k}\t{v}")
