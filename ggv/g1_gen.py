#!/usr/bin/env python3
"""G1 -- generate reduced-chart msolve inputs for the d = 8..12 ladder.

Uses the certified builders verbatim:
    wave5/w5_b16_reduce.py :: reduced_charts(d)   (gauge-fixed charts A, B)
    wave5/w5_b16_reduce.py :: to_ms(...)          (the campaign's .ms writer)
No equations are re-derived here.  Primes are p = 1 mod 3 only.

Structural controls, computed (never asserted) for every d:
  * every prime used satisfies p % 3 == 1;
  * reduce.weight_check(d) confirms quasi-homogeneity of the eliminated core;
  * the written .ms header lists exactly the chart's variables, and the body
    row count equals len(eqs) -- a truncated input is detected here, not later;
  * no generator is a nonzero constant (msolve silent-lie guard).
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wave5"))
from w5_b16_reduce import reduced_charts, to_ms, weight_check, PRIMES
from sympy import Poly

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(REPO, "ggv", "ms_ladder")
FAIL = []

def check(label, cond, note=""):
    print(("PASS " if cond else "FAIL ") + label + (f"   [{note}]" if note else ""))
    if not cond:
        FAIL.append(label)

def main(ds):
    os.makedirs(OUTDIR, exist_ok=True)
    check("all primes are 1 mod 3", all(p % 3 == 1 for p in PRIMES), str(PRIMES))
    manifest = {}
    for d in ds:
        t0 = time.time()
        wc = weight_check(d)
        charts = reduced_charts(d)
        gen_s = round(time.time() - t0, 2)
        check(f"d={d} quasi-homogeneous core (weight_check)", wc)
        manifest[str(d)] = {"gen_seconds": gen_s, "charts": {}}
        for name, (eqs, vars_) in charts.items():
            nonzero_const = [str(e) for e in eqs if Poly(e, *vars_).total_degree() == 0]
            check(f"d={d} chart {name}: no constant generator", not nonzero_const,
                  str(nonzero_const)[:80])
            info = {"n_eqs": len(eqs), "n_vars": len(vars_),
                    "vars": [str(v) for v in vars_], "files": {}}
            for p in PRIMES:
                path = os.path.join(OUTDIR, f"b16r_d{d}_{name}_p{p}.ms")
                text = to_ms(eqs, vars_, p)
                open(path, "w").write(text)
                lines = open(path).read().rstrip("\n").split("\n")
                hdr_ok = lines[0] == ",".join(str(v) for v in vars_)
                char_ok = lines[1] == str(p)
                rows_ok = (len(lines) - 2) == len(eqs)
                check(f"d={d} {name} p={p}: header+char+row-count intact",
                      hdr_ok and char_ok and rows_ok,
                      f"rows={len(lines)-2} expected={len(eqs)} bytes={os.path.getsize(path)}")
                info["files"][str(p)] = {"path": os.path.relpath(path, REPO),
                                         "bytes": os.path.getsize(path),
                                         "rows": len(lines) - 2}
            manifest[str(d)]["charts"][name] = info
        print(f"  d={d}: generated in {gen_s}s  "
              + "  ".join(f"{n}:{len(e)}eq/{len(v)}var" for n, (e, v) in charts.items()))
    mpath = os.path.join(REPO, "ggv", "ladder_inputs.json")
    json.dump(manifest, open(mpath, "w"), indent=2, sort_keys=True)
    print("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL))
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main([int(x) for x in (sys.argv[1:] or ["8", "9", "10", "11", "12"])]))
