#!/usr/bin/env python3
"""FIRST search of COMPONENT II: the P_7 divisor lattice on both components.

Level 3 of the ladder forces extra divisibility of P_7 by factors of S (proved
for component I: S | P_7).  The ladder then spirals.  This maps the spiral by
brute force: for every divisor D = A^alpha B^beta of a power of S with
deg D <= 8, set P_7 = D * M with M random and record where the cascade dies.

COMPONENT I   S = c A^2, A quadratic squarefree   -> D = A^alpha, alpha <= 4
COMPONENT II  S = c A^2 B, deg A = 1, deg B = 2   -> D = A^alpha B^beta,
                                                     alpha + 2 beta <= 8

Bracket verdicts use the SCALE-INVARIANT test (br proportional to z^2), not
equality with -z^2: [P,Q] = kappa x^2, kappa != 0, is an equally good Keller
pair.
"""
import random, sys, json, time
from collections import Counter
from trackB1_sqrt import pmul, ptrim
from trackB1_cascade_general import (run, half_radical, component1_S,
                                     component2_S)
from trackB1_bracket_audit import cascade_bracket

p = 65521

def ppow(f, k, p):
    out = [1]
    for _ in range(k):
        out = pmul(out, f, p)
    return out

def verdict(S, P7, p, randfree, tries=1):
    """P_7 given directly (not via H*M)."""
    from trackB1_cascade_general import prange
    lo7, hi7 = prange(7)
    if len(P7) - 1 > hi7:
        return ("P7_DEGREE", None)
    # run() takes M with P_7 = H(S)*M; feed H=1 by passing P7 through a shim
    import trackB1_cascade_general as CG
    real_hr = CG.half_radical
    CG.half_radical = lambda S_, p_: [1]
    try:
        v, lvl, P = CG.run(S, P7, p, rand_free=randfree)
    finally:
        CG.half_radical = real_hr
    if v != "SURVIVED_LADDER":
        return (v, lvl)
    plow = {w: P[w] for w in range(7, -2, -1) if w in P}
    res = cascade_bracket(S, 1, 1, plow, p)
    return (res["verdict"], res.get("level"))

def grid(name, gen_S, divisors, nsamp, randfree, seed):
    random.seed(seed)
    print(f"\n{'='*74}\n{name}   (p={p}, {nsamp} samples/cell, "
          f"free-dirs={'random' if randfree else 'zero'})\n{'='*74}")
    rows = []
    survivors = []
    for label, dgen in divisors:
        tally = Counter()
        tried = 0
        while sum(tally.values()) < nsamp and tried < 40 * nsamp:
            tried += 1
            got = gen_S()
            if got is None:
                continue
            S, parts = got
            D = dgen(parts)
            if D is None or len(D) - 1 > 8:
                continue
            dM = 8 - (len(D) - 1)
            M = [random.randrange(p) for _ in range(dM + 1)]
            if not any(M):
                continue
            P7 = pmul(D, M, p)
            v = verdict(S, P7, p, randfree)
            tally[v] += 1
            if v[0] == "PROPORTIONAL":
                survivors.append((S, P7))
        top = sorted(tally.items(), key=lambda t: -t[1])
        summary = "  ".join(f"{str(k)}:{c}" for k, c in top[:3])
        star = "  <<<<<< SURVIVOR" if any(k[0] == "PROPORTIONAL"
                                         for k in tally) else ""
        print(f"  P_7 = {label:<12} deg D={len(D)-1}, deg M={8-(len(D)-1)}"
              f"   {summary}{star}")
        rows.append((label, dict((str(k), c) for k, c in tally.items())))
    return rows, survivors

def gen1():
    A = [1, random.randrange(p), random.randrange(1, p)]
    S = component1_S(A, 1, p)
    if S is None:
        return None
    return S, {"A": A}

def gen2():
    u, v = random.randrange(1, p), random.randrange(1, p)
    S = component2_S(u, v, 1, p)
    if S is None:
        return None
    a1 = (2 * (5 * u * u - 4 * v)) % p
    a0 = (u * (7 * u * u - 12 * v)) % p
    return S, {"A": ptrim([a0, a1]), "B": ptrim([v % p, u % p, 1])}

if __name__ == "__main__":
    nsamp = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    randfree = len(sys.argv) > 3 and sys.argv[3] == "rand"
    t0 = time.time()

    div1 = [(f"A^{al}", (lambda al: lambda pr: ppow(pr["A"], al, p))(al))
            for al in range(0, 5)]
    div2 = []
    for al in range(0, 9):
        for be in range(0, 5):
            if al + 2 * be > 8:
                continue
            div2.append((f"A^{al} B^{be}",
                         (lambda al, be: lambda pr: pmul(ppow(pr["A"], al, p),
                                                         ppow(pr["B"], be, p),
                                                         p))(al, be)))
    r1, s1 = grid("COMPONENT I (perfect squares) -- REGRESSION vs published table",
                  gen1, div1, nsamp, randfree, seed)
    r2, s2 = grid("COMPONENT II (new locus) -- FIRST SEARCH EVER",
                  gen2, div2, nsamp, randfree, seed)
    print(f"\nelapsed {time.time()-t0:.0f}s")
    print(f"SURVIVORS: component I {len(s1)}, component II {len(s2)}")
    if s1 or s2:
        with open('/home/user/jacobian_planar/trackB1_survivors.json', 'w') as f:
            json.dump({"I": [[S, P7] for S, P7 in s1[:50]],
                       "II": [[S, P7] for S, P7 in s2[:50]]}, f)
        print("[survivors written to trackB1_survivors.json]")
