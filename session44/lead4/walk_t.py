#!/usr/bin/env python3
"""RETIRED FOR VERDICTS -- X1 control FAILED (2026-08-27).

Diagnosis: this tool looped the PIVOT p10 = (0,1) as if it were the dim-1
gauge. It is not. The recurrence divides by p10 (enters as 1/p10, NONlinear),
so p10 is a fixed nonzero parameter, not a coordinate to enumerate. The
actual dim-1 freedom on the real (72,108) charts is the driver's (0,0)
CONSTANT coefficient (verified: fixing param#0 = coeff (0,0) drops
dim_given to 0), which enters LINEARLY. So looping p10 never traced the
solution variety, and the "EMPTY at p=13,19" it printed is MEANINGLESS.

Kept only for the diagnostic scaffolding (complete_at_gauge, decide) and the
correct reduction it points to, now implemented in the full-depth Groebner
path (run_108_full.py): the full-depth systems are rigid (dim 1 = scaling),
hence exactly what facstd decides, and are fed to the two-prime queue
directly. Do NOT cite any verdict from THIS file.
"""

"""(original design note follows)

Exhaustive gauge decision for RIGID full-depth charts.

The full-depth measurement showed every published <=150 chart has
dim_full = 1, and that 1 is the scaling gauge t = p10 (the (0,1) driver
pivot). So beyond fixing t the affine tower is DETERMINISTIC (kernel dim 0
at every level). Therefore, at a prime p, the chart's solvability is decided
by a FINITE loop: for each of the p-1 nonzero gauges t, deterministically
complete the tower and test whether the top-level excess conditions all
vanish. If none do, the chart is EMPTY at p OVER ALL GAUGES -- an exhaustive
mod-p verdict, no sampling and no Groebner. A gauge that completes with zero
residual is a candidate point; it is handed to walk_pair's independent
bracket gate, and (two primes agreeing) to exact char-0 lift.

This is the walker (full-depth, deterministic) x an exhaustive gauge sweep.
It decides exactly the rigid systems the Groebner queue times out on.

Controls:
  X1 (positive): the (9,27) shape is dim_full=1 and KNOWN CLOSED
      (GGHV Cor 5.7). At full depth it must come out EMPTY here -- but the
      point of X1 is the OPPOSITE guard: build a KNOWN-SOLVABLE rigid
      instance (plant a driver, take Q's exact support as the other
      polygon, full depth) and confirm the sweep FINDS its gauge and the
      gate passes. Without a positive hit the EMPTY verdicts are worthless.
  X2 (determinism): assert kernel dim == 0 beyond the gauge at every level
      for the target at full depth; if any level has kdim>0 the "finite
      loop decides it" premise fails and the tool aborts loudly.
"""
import argparse
import json
import sys

from walk_pair import Walker, solve_affine, p as DEFAULT_P
import walk_pair
import trackB1_polygon as TP


def complete_at_gauge(w, tval, rng):
    """Deterministically complete the full-depth tower with pivot=tval.
    Returns (ok, vec, residual_labels). ok means all conditions vanish."""
    vec = [0] * len(w.idx)
    vec[w.pivot] = tval % walk_pair.p
    done = set()
    jd = max(w.levels)
    j0 = w.jmax // 2 + 1
    steps = ([j for j in w.levels if j < j0]
             + (["MERGE"] if any(j >= j0 for j in w.levels) else []))
    for j_raw in steps:
        if j_raw == "MERGE":
            unks = [k for jj in w.levels if jj >= j0
                    for k in w.vars_at[jj] if k != w.pivot]
        else:
            unks = [k for k in w.vars_at[j_raw] if k != w.pivot]
        base = w.conds_labeled(vec)
        if base is None:
            return False, vec, ["pivot killed recurrence"]
        if j_raw == "MERGE":
            new = [key for key in base if key not in done]
        else:
            new = [key for key in base
                   if key not in done and key[0] <= j_raw + 1]
        if unks:
            cols = [w.conds_labeled(vec, k) for k in unks]
            keys = set(new)
            for c in cols:
                keys |= {key for key in c if key not in done
                         and (j_raw == "MERGE" or key[0] <= j_raw + 1)}
            new = sorted(keys)
            c0 = [base.get(key, (0, 0))[0] for key in new]
            A = [[cols[q].get(key, (0, 0))[1] for q in range(len(unks))]
                 for key in new]
            sol = solve_affine(A, c0, rng, n=len(unks))
            if sol is None:
                return False, vec, [f"inconsistent at {j_raw}"]
            u, kdim = sol
            if kdim:
                # not rigid at this gauge -> premise broken for this t; the
                # caller records it, but a nonzero kdim here (after gauge
                # fixed) means extra freedom: pick zero, still valid
                pass
            for q, k in enumerate(unks):
                vec[k] = u[q]
        else:
            if any(base[key][0] != 0 for key in new):
                return False, vec, [k for k in new if base[k][0] != 0]
        done |= set(new)
    fin = w.conds_labeled(vec)
    resid = [key for key in fin if fin[key][0] != 0]
    return (not resid), vec, resid


def decide(NP, NQ, r, prime, tag="", gate=True, verbose=False):
    walk_pair.p = prime
    TP.p = prime
    w = Walker(NP, NQ, [(r, 0, 1)], tag, full_depth=True)
    import random
    rng = random.Random(1)
    hits = []
    for tval in range(1, prime):
        ok, vec, resid = complete_at_gauge(w, tval, rng)
        if ok:
            gate_ok, det = (w.bracket_gate(vec) if gate else (True, "nogate"))
            hits.append((tval, gate_ok, det, list(vec)))
            if verbose:
                print(f"    gauge t={tval}: COMPLETES  gate="
                      f"{'PASS ' + det if gate_ok else 'FAIL ' + det}",
                      flush=True)
    return w, hits


def control_X1(prime=1009):
    """Plant a solvable rigid instance; the sweep must find its gauge."""
    walk_pair.p = prime
    TP.p = prime
    NA = [(0, 0), (1, 0), (3, 2), (3, 4), (0, 3)]
    rhs = [(1, 0, 1)]
    probe = Walker(NA, [(0, 0), (0, 1), (6, 1), (6, 8), (0, 8)], rhs,
                   full_depth=True)
    import random
    rng = random.Random(2)
    tval = 7
    vec = [rng.randrange(prime) for _ in probe.idx]
    vec[probe.pivot] = tval
    Q = probe.qrows(probe.build(vec))
    NBrows = {}
    for j in range(1, probe.jmax + 1):
        row = TP.trim(Q[j][0]) if j in Q else []
        nz = [i for i, c in enumerate(row) if c % prime]
        if nz:
            NBrows[j] = (min(nz), max(nz))
    NB = [(0, 0)] + [pt for j, (lo, hi) in sorted(NBrows.items())
                     for pt in ((lo, j), (hi, j))]
    w, hits = decide(NA, NB, 1, prime, "X1", gate=True)
    passed = any(g for _, g, _, _ in hits)
    print(f"X1 planted rigid instance (p={prime}): "
          f"{len(hits)} gauge-completions, "
          f"{'a gate PASS' if passed else 'NO gate pass'}  "
          f"{'OK' if passed else 'FAIL'}")
    return passed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets")
    ap.add_argument("--index", type=int, default=0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--prime", type=int, default=1009)
    ap.add_argument("--prime2", type=int, default=1021)
    ap.add_argument("--skipcal", action="store_true")
    a = ap.parse_args()
    for pr in (a.prime, a.prime2):
        if pr % 3 != 1:
            print(f"WARN prime {pr} !=1 mod 3 (cusp (2,3) not representable)")
    if not a.skipcal:
        if not control_X1(a.prime):
            print("X1 FAILED -- tool unsound, aborting")
            sys.exit(1)
    if not a.targets:
        return
    targets = json.load(open(a.targets))
    sel = targets if a.all else [targets[a.index]]
    for t in sel:
        verds = {}
        for pr in (a.prime, a.prime2):
            w, hits = decide(t["NP"], t["NQ"], t["r"], pr, t["tag"],
                             gate=True, verbose=True)
            gate_hits = [h for h in hits if h[1]]
            verds[pr] = ("NONEMPTY" if gate_hits else
                         ("GAUGE-ONLY" if hits else "EMPTY"))
            print(f"{t['tag'][:56]}  p={pr}: {verds[pr]} "
                  f"({len(hits)} completions, {len(gate_hits)} gate-pass)",
                  flush=True)
        combined = ("NONEMPTY" if all(v == "NONEMPTY" for v in verds.values())
                    else "EMPTY" if all(v == "EMPTY" for v in verds.values())
                    else "MIXED " + str(verds))
        print(f"  => {t['tag'][:56]}: {combined}\n", flush=True)


if __name__ == "__main__":
    main()
