#!/usr/bin/env python3
"""Cumulative dimension of the corrected cascade, level by level.

The levels are COUPLED: level 5 is empty for generic level-4 free directions,
yet the joint variety in (P_6-params, P_5) is 13-dimensional out of 15.  So the
only sound way to run the cascade is to accumulate the conditions and track the
dimension of the common solution variety.

At stage m the live parameters are
    P_6 : the level-4 parametrization  M^2/(4a) + H(S)*y + S*z   (7 or 6)
    P_5, P_4, P_3, P_2, P_1, P_0, P_-1 : full slices as introduced
and the equations are rem(N_k, S^3) = 0 for k = 5..m (level 4 holds identically
by the parametrization).  Each level's equations are interpolated EXACTLY (the
degree is measured by finite differences along random lines and the monomial
sample matrix is checked for full rank), then Singular computes the dimension.

Writes results incrementally to trackB1_cumulative_<tag>.log so a container
restart never loses completed stages.
"""
import random, sys, os, json, time
from trackB1_sqrt import ptrim
from trackB1_cascade_general import component1_S, component2_S
from trackB1_joint import make_P, cond_at, layout_for
from trackB1_level_system import (measure_degree, interpolate, to_singular, p)
import subprocess

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")

def singular_dim(polys, nvars, timeout=1800):
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
    fn = os.path.join(SCRATCH, "cum.sing")
    os.makedirs(SCRATCH, exist_ok=True)
    with open(fn, "w") as f:
        f.write(src)
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "?"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

def main(tag, seed, mmax, degcap):
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
    log = f"/home/user/jacobian_planar/trackB1_cumulative_{tag}.log"
    with open(log, "a") as f:
        f.write(f"\n=== component {tag} seed={seed} S={S} M={M} ===\n")
    wl, allpolys = [], []
    for m in range(4, mmax + 1):
        w = 10 - m
        if w <= 6:
            wl.append(w)
        nvars = sum(lay[x] for x in wl)
        if m == 4:
            line = (f"level 4: parametrized (P_6 = M^2/4a + H*y + S*z), "
                    f"{nvars} params, holds identically")
            print(line, flush=True)
            with open(log, "a") as f:
                f.write(line + "\n")
            continue
        t0 = time.time()

        def fn(q, _m=m, _wl=list(wl)):
            return cond_at(S, make_P(S, M, _wl, q, lay), _m)

        deg = measure_degree(fn, nvars, rng)
        if deg is None or deg > degcap:
            line = f"level {m}: degree {deg} exceeds cap {degcap} — STOP"
            print(line, flush=True)
            with open(log, "a") as f:
                f.write(line + "\n")
            return
        polys, info = interpolate(fn, nvars, deg, rng)
        if polys is None:
            line = f"level {m}: INTERPOLATION FAILED ({info}) — STOP"
            print(line, flush=True)
            with open(log, "a") as f:
                f.write(line + "\n")
            return
        allpolys = allpolys + polys
        d = singular_dim(allpolys, nvars)
        line = (f"level {m}: w={w}, {nvars} params, deg={deg}, "
                f"+{len(polys)} eqs (total {len(allpolys)}), "
                f"cumulative {d}   [{time.time()-t0:.0f}s]")
        print(line, flush=True)
        with open(log, "a") as f:
            f.write(line + "\n")
        if d == "EMPTY":
            print(f"  => CASE CLOSED at level {m} for this (S, M)", flush=True)
            return
        if d == "TIMEOUT":
            print("  => Singular timed out; stopping", flush=True)
            return

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "I"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    mmax = int(sys.argv[3]) if len(sys.argv) > 3 else 11
    degcap = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    main(tag, seed, mmax, degcap)
