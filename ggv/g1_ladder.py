#!/usr/bin/env python3
"""G1 -- the d = 8..12 reduced-chart ladder, mod p, SERIALIZED.

One msolve process at a time, chart A before chart B, primes in ascending
order.  Every (d, chart, prime) run appends one row to ggv/ladder.tsv with its
verdict class, exit status and peak RSS -- including the failure classes
(STALLED-OOM / TIMEOUT / NO-OUTPUT), which are recorded outcomes, not skips.

Protocol on a non-EMPTY verdict: re-run msolve with -P 1 on that exact input,
commit the FULL raw output as the artifact, label the row CANDIDATE-UNVERIFIED
and continue.  No analysis is performed here.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_runner import run

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MSDIR = os.path.join(REPO, "ggv", "ms_ladder")
OUTDIR = os.path.join(REPO, "ggv", "out_ladder")
TSV = os.path.join(REPO, "ggv", "ladder.tsv")
PRIMES = [1000003, 1000033, 1000039]
COLS = ["d", "chart", "prime", "verdict", "exit", "peak_rss_kb", "wall_s",
        "mem_policy", "timeout_s", "in_bytes", "out_bytes", "input", "output",
        "P1_output", "note"]

def emit(row):
    new = not os.path.exists(TSV)
    with open(TSV, "a") as f:
        if new:
            f.write("\t".join(COLS) + "\n")
        f.write("\t".join(str(row.get(c, "")) for c in COLS) + "\n")
        f.flush()

def main(ds, timeout):
    os.makedirs(OUTDIR, exist_ok=True)
    for d in ds:
        for chart in ("A", "B"):              # chart A then chart B
            for p in PRIMES:
                src = os.path.join(MSDIR, f"b16r_d{d}_{chart}_p{p}.ms")
                out = os.path.join(OUTDIR, f"b16r_d{d}_{chart}_p{p}.out")
                t0 = time.time()
                rec = run(src, out, timeout=timeout)
                row = {"d": d, "chart": chart, "prime": p,
                       "verdict": rec["verdict"], "exit": rec["exit"],
                       "peak_rss_kb": rec["peak_rss_kb"], "wall_s": rec["wall_s"],
                       "mem_policy": rec["mem_policy"], "timeout_s": rec["timeout_s"],
                       "in_bytes": rec["in_bytes"], "out_bytes": rec["out_bytes"],
                       "input": os.path.relpath(src, REPO),
                       "output": os.path.relpath(out, REPO) if rec["out_bytes"] else "",
                       "P1_output": "", "note": rec["stderr_tail"]}
                if rec["verdict"] != "EMPTY":
                    # required follow-up: -P 1 on this exact input, full raw output kept
                    p1out = os.path.join(OUTDIR, f"b16r_d{d}_{chart}_p{p}.P1.out")
                    r1 = run(src, p1out, extra_args=("-P", "1"), timeout=timeout)
                    row["P1_output"] = (os.path.relpath(p1out, REPO)
                                        if r1["out_bytes"] else "")
                    row["note"] = (f"P1 verdict={r1['verdict']} exit={r1['exit']} "
                                   f"rss_kb={r1['peak_rss_kb']} bytes={r1['out_bytes']}; "
                                   + row["note"])[:400]
                emit(row)
                print(f"d={d} {chart} p={p} -> {rec['verdict']} "
                      f"exit={rec['exit']} rss={rec['peak_rss_kb']}kB "
                      f"{round(time.time()-t0,1)}s", flush=True)

if __name__ == "__main__":
    to = int(os.environ.get("GGV_TIMEOUT", "5400"))
    main([int(x) for x in (sys.argv[1:] or ["8", "9", "10", "11", "12"])], to)
