#!/usr/bin/env python3
"""G1 -- the d = 8..12 reduced-chart ladder, mod p, SERIALIZED.

One msolve process at a time, chart A before chart B, primes in ascending
order.  Every (d, chart, prime) cell appends exactly one row to ggv/ladder.tsv
with its verdict class, exit status and peak RSS -- including the failure
classes (STALLED-OOM / TIMEOUT / CRASH / NO-OUTPUT), which are recorded
outcomes, not skips.

Protocol on a CANDIDATE-UNVERIFIED verdict -- i.e. the run produced an output
artifact and that artifact is not msolve's "[-1]:" -- re-run msolve with -P 1
on that exact input, keep the FULL raw output, label the row
CANDIDATE-UNVERIFIED and continue.  No analysis is performed here.
The -P 1 follow-up is deliberately NOT fired for a run that produced no
artifact at all (TIMEOUT / STALLED-OOM / CRASH / NO-OUTPUT): -P 1 is strictly
more work than the plain solve, so on a cell that already exhausted its
deadline or its memory it is guaranteed to fail again while consuming a second
full deadline and delaying every later cell.  Such a run is a failed run,
already recorded with its own failure class.

The ladder RESUMES: a cell already present in ggv/ladder.tsv is not re-run, so
an interrupted ladder can be restarted without losing completed work or
double-writing rows.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g_runner import run

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MSDIR = os.environ.get("GGV_MSDIR", os.path.join(REPO, "ggv", "ms_ladder"))
OUTDIR = os.environ.get("GGV_OUTDIR", os.path.join(REPO, "ggv", "out_ladder"))
TSV = os.environ.get("GGV_TSV", os.path.join(REPO, "ggv", "ladder.tsv"))
PRIMES = [1000003, 1000033, 1000039]
COLS = ["d", "chart", "prime", "verdict", "exit", "peak_rss_kb", "wall_s",
        "mem_policy", "timeout_s", "in_bytes", "out_bytes", "input", "output",
        "P1_output", "note"]


def done_cells():
    """Cells already recorded, so a restart never re-runs or double-writes one."""
    if not os.path.exists(TSV):
        return set()
    seen = set()
    with open(TSV) as f:
        rows = [l.rstrip("\n").split("\t") for l in f if l.strip()]
    if not rows:
        return seen
    ix = {h: i for i, h in enumerate(rows[0])}
    for r in rows[1:]:
        try:
            seen.add((int(r[ix["d"]]), r[ix["chart"]], int(r[ix["prime"]])))
        except (ValueError, IndexError, KeyError):
            continue
    return seen


def emit(row):
    new = not os.path.exists(TSV)
    with open(TSV, "a") as f:
        if new:
            f.write("\t".join(COLS) + "\n")
        f.write("\t".join(str(row.get(c, "")) for c in COLS) + "\n")
        f.flush()
        os.fsync(f.fileno())


def drop_if_empty(path):
    """A 0-byte artifact is a failed run, never a result: do not keep the file."""
    if os.path.exists(path) and os.path.getsize(path) == 0:
        os.remove(path)
        return True
    return False


def main(ds, timeout):
    os.makedirs(OUTDIR, exist_ok=True)
    seen = done_cells()
    if seen:
        print(f"resuming: {len(seen)} cell(s) already recorded", flush=True)
    for d in ds:
        for chart in ("A", "B"):              # chart A then chart B
            for p in PRIMES:
                if (d, chart, p) in seen:
                    print(f"d={d} {chart} p={p} -> already recorded, skipping",
                          flush=True)
                    continue
                src = os.path.join(MSDIR, f"b16r_d{d}_{chart}_p{p}.ms")
                out = os.path.join(OUTDIR, f"b16r_d{d}_{chart}_p{p}.out")
                t0 = time.time()
                row = {"d": d, "chart": chart, "prime": p, "timeout_s": timeout,
                       "P1_output": "", "output": "", "note": ""}
                try:
                    rec = run(src, out, timeout=timeout)
                except Exception as exc:
                    # A cell that cannot even be launched is RECORDED as such.
                    # Letting the exception escape would silently drop this cell
                    # and every cell after it from the ladder.
                    row.update({"verdict": "RUN-ERROR", "exit": "exception",
                                "peak_rss_kb": -1,
                                "wall_s": round(time.time() - t0, 2),
                                "mem_policy": "-", "in_bytes":
                                    os.path.getsize(src) if os.path.exists(src) else 0,
                                "out_bytes": 0,
                                "input": os.path.relpath(src, REPO),
                                "note": f"{type(exc).__name__}: {exc}"[:400]})
                    emit(row)
                    print(f"d={d} {chart} p={p} -> RUN-ERROR {exc}", flush=True)
                    continue
                drop_if_empty(out)
                row.update({"verdict": rec["verdict"], "exit": rec["exit"],
                            "peak_rss_kb": rec["peak_rss_kb"],
                            "wall_s": rec["wall_s"],
                            "mem_policy": rec["mem_policy"],
                            "timeout_s": rec["timeout_s"],
                            "in_bytes": rec["in_bytes"],
                            "out_bytes": rec["out_bytes"],
                            "input": os.path.relpath(src, REPO),
                            "output": (os.path.relpath(out, REPO)
                                       if rec["out_bytes"] else ""),
                            "note": rec["stderr_tail"]})
                if rec["verdict"] == "CANDIDATE-UNVERIFIED":
                    p1out = os.path.join(OUTDIR, f"b16r_d{d}_{chart}_p{p}.P1.out")
                    try:
                        r1 = run(src, p1out, extra_args=("-P", "1"), timeout=timeout)
                        drop_if_empty(p1out)
                        row["P1_output"] = (os.path.relpath(p1out, REPO)
                                            if r1["out_bytes"] else "")
                        row["note"] = (f"P1 verdict={r1['verdict']} "
                                       f"exit={r1['exit']} rss_kb={r1['peak_rss_kb']} "
                                       f"bytes={r1['out_bytes']}; " + row["note"])[:400]
                    except Exception as exc:
                        row["note"] = (f"P1 RUN-ERROR {type(exc).__name__}: {exc}; "
                                       + row["note"])[:400]
                emit(row)
                print(f"d={d} {chart} p={p} -> {rec['verdict']} "
                      f"exit={rec['exit']} rss={rec['peak_rss_kb']}kB "
                      f"{round(time.time()-t0,1)}s", flush=True)


if __name__ == "__main__":
    to = int(os.environ.get("GGV_TIMEOUT", "5400"))
    main([int(x) for x in (sys.argv[1:] or ["8", "9", "10", "11", "12"])], to)
