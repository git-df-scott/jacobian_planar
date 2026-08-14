#!/usr/bin/env python3
"""Cumulative dimension of the corrected cascade, using the RATIONAL cascade.

Conditions are added in cascade order (poly_7, poly_6, ... = levels 5, 6, ...),
each interpolated exactly, and the dimension of the accumulated variety is
computed by Singular.  Unlike the exact-division version every condition is
defined at every parameter point, so interpolation is valid off the variety.

Writes each completed stage to disk immediately.
"""
import random, sys, os, time, subprocess
from trackB1_sqrt import ptrim
from trackB1_cascade_general import component1_S, component2_S
from trackB1_rational_cascade import (build_F, conditions, make_P, layout_for,
                                      spow, p)
from trackB1_cascade_general import prem
from trackB1_level_system import measure_degree, interpolate, to_singular

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")

def singular_dim(polys, nvars, timeout=2400):
    eqs = to_singular(polys, nvars)
    src = f"""
option(redSB);
ring R = {p}, x(0..{nvars-1}), dp;
ideal I = {','.join(eqs)};
ideal G = std(I);
if (size(G) == 1 && G[1] == 1) {{ "EMPTY"; }}
else {{ "DIM " + string(dim(G)); }}
quit;
"""
    fn = os.path.join(SCRATCH, f"cum2_{nvars}.sing")
    os.makedirs(SCRATCH, exist_ok=True)
    with open(fn, "w") as f:
        f.write(src)
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        o = r.stdout.strip().splitlines()
        return o[-1] if o else "?"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

def cond_w(S, M, wl, lay, w, params):
    P = make_P(S, M, wl, params, lay)
    F = build_F(S, P, wmin=w)          # only descend as far as this weight
    num, e = F[w]
    return list(ptrim(list(prem(num, spow(S, e, p), p))))

def main(tag, seed, wstop, degcap, timeout):
    rng = random.Random(seed)
    if tag == "I":
        A = [1, rng.randrange(p), rng.randrange(1, p)]
        S = component1_S(A, 1, p)
    else:
        S = None
        while S is None:
            u, v = rng.randrange(1, p), rng.randrange(1, p)
            S = component2_S(u, v, 1, p)
    M = [rng.randrange(p) for _ in range(5)]
    lay = layout_for(S)
    log = f"/home/user/jacobian_planar/trackB1_cumulative2_{tag}.log"
    with open(log, "a") as f:
        f.write(f"\n=== component {tag} seed={seed} S={S} M={M} ===\n")
    # level 4's slice P_6 is ALWAYS live: its free directions (H*y + S*z) are
    # what level 5 constrains.  Freezing them is the retracted mistake.
    wl, allpolys = [6], []
    order = [(7, 5), (6, 6), (5, 7), (4, 8), (3, 9), (2, 10), (1, 11), (0, 12)]
    for w, m in order:
        if w < wstop:
            break
        newslice = 10 - m
        if newslice <= 6 and newslice not in wl:
            wl.append(newslice)
        nvars = sum(lay[x] for x in wl)
        t0 = time.time()

        def fn(q, _w=w, _wl=list(wl)):
            return cond_w(S, M, _wl, lay, _w, q)

        deg = measure_degree(fn, nvars, rng)
        if deg is None or deg > degcap:
            line = f"poly_{w} (level {m}): degree {deg} > cap {degcap} — STOP"
            print(line, flush=True)
            open(log, "a").write(line + "\n")
            return
        polys, info = interpolate(fn, nvars, deg, rng)
        if polys is None:
            line = f"poly_{w} (level {m}): INTERPOLATION FAILED ({info}) — STOP"
            print(line, flush=True)
            open(log, "a").write(line + "\n")
            return
        allpolys = allpolys + polys
        d = singular_dim(allpolys, nvars, timeout)
        line = (f"poly_{w} (level {m}): {nvars} params, deg={deg}, "
                f"+{len(polys)} eqs (total {len(allpolys)}), "
                f"cumulative {d}   [{time.time()-t0:.0f}s]")
        print(line, flush=True)
        open(log, "a").write(line + "\n")
        if d == "EMPTY":
            print(f"  => CLOSED at level {m} for this (S, M)", flush=True)
            return
        if d in ("TIMEOUT", "?"):
            return

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "I"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    wstop = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    degcap = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    timeout = int(sys.argv[5]) if len(sys.argv) > 5 else 2400
    main(tag, seed, wstop, degcap, timeout)
