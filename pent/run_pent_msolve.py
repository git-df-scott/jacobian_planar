"""
ITEM 2 (second half) -- msolve on the pentagon exports, with a graded block
split and a RUNLOG that records peak RSS and exit codes for every run.

THE SPLIT.  wave1/pent_L23.ms holds the levels-13..23 conditions in level order:
level j contributes j-12 conditions, so the first 1+2+...+(J-12) generators are
exactly levels 13..J.  Emptiness is monotone in the generator set, so running
the prefixes J = 18,19,...,23 is a sound ladder: the first J that returns EMPTY
settles the whole system, and any J that returns a live component says nothing
about emptiness either way.

THE THIRD GAUGE.  The exports fix only two of the three gauges (p_00 = 0 and
p_10 = 1).  The third, the coordinate scaling (x,y) -> (lam x, lam^-3 y), acts
on p_{j,i} by lam^(i-3j-1) after the first two are fixed, and its exponent at
(j,i) = (1,0) is -4, so the variety of the exported system contains a
one-dimensional gauge orbit through every point and CANNOT be zero-dimensional.
msolve needs dimension zero.  Each prefix is therefore run twice: as exported,
and with the extra generator p_1_0 - 1 that fixes the last gauge.  That is a
material change to the problem, not a re-run.

Every run records: generators, bytes, exit code, wall time, peak RSS (from
/usr/bin/time -v on the child), output bytes, and the parsed verdict.  A
zero-byte output is written down as a FAILURE with its exit code, never as a
result.  Exit 137 is recorded as OOM.
"""

import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "wave1", "pent_L23.ms")
RUNLOG = os.path.join(HERE, "RUNLOG.tsv")
CORES = int(os.environ.get("PENT_CORES", "2"))


def cum(J):
    return sum(j - 12 for j in range(13, J + 1))


def load():
    txt = open(SRC).read().rstrip()
    rows = txt.split("\n")
    head, char = rows[0], rows[1]
    body = "\n".join(rows[2:])
    polys = [s.strip() for s in body.split(",\n")]
    return head, char, polys


def write_prefix(path, head, char, polys, n, gauge3):
    sel = polys[:n]
    if gauge3:
        sel = sel + ["p_1_0-1"]
    with open(path, "w") as f:
        f.write(head + "\n" + char + "\n" + ",\n".join(sel) + "\n")
    return len(sel)


def classify(raw, size, rc):
    if rc == -9 or rc == 137:
        return "OOM"
    if size == 0:
        return f"FAIL-EMPTY-FILE(exit {rc})"
    s = (raw or "").strip().rstrip(":").strip()
    if s == "[-1]":
        return "EMPTY"
    if s.startswith("[1,") and ",-1," in s.replace(" ", ""):
        return "POSITIVE-DIMENSIONAL"
    if s.startswith("["):
        return "NONEMPTY-PARAMETRIZATION"
    return f"FAIL-UNPARSED(exit {rc})"


def run(ms, out, timeout):
    cmd = ["/usr/bin/time", "-v", "msolve", "-f", ms, "-o", out, "-t", str(CORES)]
    t0 = time.time()
    to = False
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        rc, err = pr.returncode, pr.stderr
    except subprocess.TimeoutExpired as e:
        rc, err, to = None, (e.stderr or b"").decode(errors="replace") \
            if isinstance(e.stderr, bytes) else (e.stderr or ""), True
    dt = time.time() - t0
    m = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", err or "")
    rss = int(m.group(1)) if m else -1
    m2 = re.search(r"Command terminated by signal (\d+)", err or "")
    if m2:
        rc = -int(m2.group(1))
    size = os.path.getsize(out) if os.path.exists(out) else -1
    raw = open(out).read()[:400] if size > 0 else ""
    verdict = "TIMEOUT" if to else classify(raw, size, rc)
    return dict(exit=rc, seconds=round(dt, 1), peak_rss_kb=rss, out_bytes=size,
                verdict=verdict, head=raw.replace("\n", " ")[:120])


def main():
    head, char, polys = load()
    print(f"  source {SRC}: {len(polys)} generators, {os.path.getsize(SRC)} bytes")
    new = not os.path.exists(RUNLOG)
    fh = open(RUNLOG, "a")
    if new:
        fh.write("timestamp\tsystem\tgenerators\tlevels\tgauges\tbytes\tthreads\t"
                 "exit\tseconds\tpeak_rss_kb\tout_bytes\tverdict\thead\n")
        fh.flush()
    plan = []
    for J in (18, 19, 20, 21, 22, 23):
        for gauge3 in (True, False):
            plan.append((J, gauge3))
    for J, gauge3 in plan:
        n = cum(J)
        tag = f"L{J}_{'g3' if gauge3 else 'g2'}"
        ms = os.path.join(HERE, f"pent_{tag}.ms")
        ngen = write_prefix(ms, head, char, polys, n, gauge3)
        r = run(ms, ms[:-3] + ".out", timeout=3600)
        fh.write("\t".join([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            f"pent_{tag}.ms", str(ngen), f"13..{J}",
                            "3" if gauge3 else "2", str(os.path.getsize(ms)),
                            str(CORES), str(r["exit"]), str(r["seconds"]),
                            str(r["peak_rss_kb"]), str(r["out_bytes"]),
                            r["verdict"], r["head"]]) + "\n")
        fh.flush()
        print(f"    pent_{tag}: {r['verdict']}  exit {r['exit']}  {r['seconds']}s  "
              f"peak {r['peak_rss_kb']} kB  out {r['out_bytes']} B", flush=True)
        if r["verdict"] == "EMPTY":
            print("      -> EMPTY at this prefix; the ladder can stop for this gauge",
                  flush=True)
    fh.close()


if __name__ == "__main__":
    main()
