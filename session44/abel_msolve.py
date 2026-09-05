#!/usr/bin/env python3
"""B=16 Abel ladder emptiness via msolve — 'is there a mu0 != 0 solution?'

Exports the deg(q1)=k system (mu3 gauged to 1 unless --free) saturated with
mu0*s-1, in msolve's input format over Q, and asks msolve to solve.  msolve
returns [-1] / dimension -1  <=>  empty variety  <=>  NO mu0 != 0 solution
at that degree (this is an EXACT characteristic-zero verdict, not modular).

Calibration: deg 3 saturated must be EMPTY; deg 3 unsaturated must be
non-empty (the mu0=0 solution).
"""
import argparse
import subprocess
import sys
import tempfile

import sympy as sp

import abel_b16 as ab


def export(k, free=False, saturate=True):
    eqs, unk, q1, A = ab.build_identity(k)
    s = sp.Symbol("s_sat")
    if free:
        sub, vars2 = {}, list(unk)
    else:
        sub, vars2 = {ab.mu3: 1}, [v for v in unk if v != ab.mu3]
    gens = []
    for e in eqs:
        pe = sp.Poly(sp.expand(e.subs(sub)), *vars2, domain="QQ")
        L = 1
        for c in pe.coeffs():
            L = sp.ilcm(L, sp.Rational(c).q)
        gens.append(sp.expand(e.subs(sub) * L))
    if saturate:
        gens.append(ab.mu0 * s - 1)
        vars2 = vars2 + [s]
    return gens, vars2


def to_msolve(gens, vars2):
    vs = ",".join(str(v) for v in vars2)
    lines = [vs, "0"]                      # variables, then char 0
    polys = []
    for g in gens:
        polys.append(str(sp.expand(g)).replace("**", "^").replace(" ", ""))
    lines.append(",\n".join(polys))
    return "\n".join(lines) + "\n"


def run(k, free=False, saturate=True, timeout=1500):
    gens, vars2 = export(k, free, saturate)
    txt = to_msolve(gens, vars2)
    with tempfile.NamedTemporaryFile("w", suffix=".ms", delete=False) as f:
        f.write(txt)
        path = f.name
    try:
        r = subprocess.run(["msolve", "-f", path],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    out = (r.stdout or "").strip()
    # msolve default: empty variety over C prints "[-1]:"; dim 0 -> "[0]:...";
    # positive-dimensional -> "[d]:" with d>=1.
    if out.startswith("[-1]"):
        return "EMPTY", out[:200]
    if out and out[0] == "[":
        return "NONEMPTY", out[:200]
    return f"UNPARSED:{out[:80]}", out[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("k", type=int)
    ap.add_argument("--free", action="store_true")
    ap.add_argument("--nosat", action="store_true")
    ap.add_argument("--timeout", type=int, default=1500)
    ap.add_argument("--skipcal", action="store_true")
    a = ap.parse_args()
    if not a.skipcal:
        if not ab.calibrate():
            sys.exit(1)
        v, o = run(3, saturate=True)
        print(f"CAL deg3 sat: {v} (expect EMPTY)  raw={o!r}")
        v2, o2 = run(3, saturate=False)
        print(f"CAL deg3 unsat: {v2} (expect NONEMPTY)  raw={o2!r}")
        if not (v == "EMPTY" and v2.startswith("NONEMPTY")):
            print("CAL FAIL"); sys.exit(1)
    verdict, raw = run(a.k, free=a.free, saturate=not a.nosat,
                       timeout=a.timeout)
    tag = "free-mu3" if a.free else "mu3=1"
    print(f"deg(q1)={a.k} {tag} sat={not a.nosat}: {verdict}")
    print("raw:", raw)


if __name__ == "__main__":
    main()
