#!/usr/bin/env python3
"""Pentagon subsystem emptiness ladder, restart-resilient.

Rationale (Example 6): if a SUBSYSTEM is rigorously EMPTY then the FULL system
is EMPTY.  We add the two gauges that make the torus rank 0 (verified), so each
run is a well-posed question about the chart {p_1_0 != 0, p_1_1 != 0}.

Generators are added smallest-first by term count, so the cheapest decisive
question is asked first.  Every result is checkpointed to ladder_state.json
before the next run starts, so a container restart loses at most one run.

VERDICTS: EMPTY / NONEMPTY / NO VERDICT.  exit!=0, empty output, timeout and
OOM are all NO VERDICT and are recorded as such.
"""
import json, os, subprocess, sys, time

SRC = "/tmp/w/wave1/pent_L23.ms"
STATE = "/tmp/hunt/ladder_state.json"
GAUGES = ["p_1_0-1", "p_1_1-1"]

def load():
    lines = [l.rstrip() for l in open(SRC)]
    body = "\n".join(lines[2:]).rstrip().rstrip(',')
    polys = [p.strip() for p in body.split(",\n") if p.strip()]
    return lines[0], lines[1], polys

def nterms(p):
    return len([t for t in p.replace('-', '+').split('+') if t.strip()])

def run(k, polys, vars_, prime, timeout):
    order = sorted(range(len(polys)), key=lambda i: nterms(polys[i]))
    sel = [polys[i] for i in order[:k]]
    path = f"/tmp/hunt/lad_{k}.ms"
    with open(path, "w") as f:
        f.write(vars_ + "\n" + prime + "\n")
        f.write(",\n".join(sel + GAUGES) + "\n")
    out = f"/tmp/hunt/lad_{k}.out"
    if os.path.exists(out):
        os.remove(out)
    t0 = time.time()
    try:
        r = subprocess.run(["msolve", "-t", "1", "-f", path, "-o", out],
                           capture_output=True, timeout=timeout)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = "timeout"
    el = round(time.time() - t0, 1)
    raw = ""
    if os.path.exists(out) and os.path.getsize(out) > 0:
        raw = open(out).read()[:200].strip()
    # verdict logic -- failures are NO VERDICT, never EMPTY
    if rc != 0 or not raw:
        verdict = "NO VERDICT"
        reason = f"rc={rc} out_bytes={len(raw)}"
    elif raw.startswith("[-1]"):
        verdict, reason = "EMPTY", "msolve [-1]"
    else:
        verdict, reason = "NONEMPTY", raw[:120]
    return {"k": k, "ngens": len(sel), "verdict": verdict, "reason": reason,
            "seconds": el, "bytes": os.path.getsize(path)}

def main():
    vars_, prime, polys = load()
    state = json.load(open(STATE)) if os.path.exists(STATE) else {"runs": []}
    done = {r["k"] for r in state["runs"]}
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 240
    for k in [2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 30, 36, 44, 52, 60, 66]:
        if k in done:
            continue
        rec = run(k, polys, vars_, prime, budget)
        state["runs"].append(rec)
        json.dump(state, open(STATE, "w"), indent=1)
        print(json.dumps(rec), flush=True)
        if rec["verdict"] == "EMPTY":
            print("DECISIVE: subsystem EMPTY => full pentagon chart EMPTY", flush=True)
            break
        if rec["verdict"] == "NO VERDICT":
            print("stalled at k=%d; larger k will not be cheaper" % k, flush=True)
            break

main()
