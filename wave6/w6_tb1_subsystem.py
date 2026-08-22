#!/usr/bin/env python3
"""Find a SMALL subsystem of trackB1 that decides the whole question.

THE PRINCIPLE
Emptiness is monotone: if any subset of the equations has no common solution,
the full system has none either. So a verdict does not require solving 166
variables -- it requires finding a subset small enough to solve and empty enough
to matter. Conversely a small subsystem that is NONEMPTY proves nothing, so this
search only ever produces EMPTY verdicts or nothing.

That asymmetry is the point: every Groebner attack on the full system has
returned NO VERDICT (timeout), and a timeout is not a result. A subsystem run
terminates.

WHAT TO LOOK FOR
An overdetermined block: a set of equations E whose variables V(E) satisfy
|E| > |V(E)|. Those are the ones with a real chance of being empty. The search
grows a block greedily from each seed equation, always absorbing the equation
that introduces the fewest NEW variables, and records the best surplus
|E| - |V(E)| seen along the way.

An earlier pass at this used a greedy heuristic and I recorded the conclusion
"no small overdetermined subsystem exists", then flagged it as an overclaim
because a greedy walk over 283 starting points does not survey 2^165 subsets.
It is still a heuristic. It is reported as a heuristic.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import load, parse_poly

SRC = os.environ.get('TB1_SRC',
      '/home/user/jacobian_planar/wave6/frontier/trackB1_sat_p1000003.ms')


def main():
    vs, p, body = load(SRC)
    polys = [parse_poly(b, p) for b in body]
    EV = [frozenset(v for m in q for v, _ in m) for q in polys]
    n = len(polys)
    print(f"{os.path.basename(SRC)}: {n} equations, {len(vs)} variables")
    sz = sorted((len(e), i) for i, e in enumerate(EV))
    print(f"  equation variable-counts: min {sz[0][0]}, median "
          f"{sz[n//2][0]}, max {sz[-1][0]}")

    best = []
    for seed in range(n):
        cur = {seed}
        V = set(EV[seed])
        # a block is worth reporting when equations outnumber variables
        rec = (len(cur) - len(V), len(cur), len(V), frozenset(cur))
        for _ in range(min(60, n)):
            cand, gain = None, None
            for j in range(n):
                if j in cur:
                    continue
                new = len(EV[j] - V)
                if gain is None or new < gain:
                    cand, gain = j, new
            if cand is None:
                break
            cur.add(cand)
            V |= EV[cand]
            s = len(cur) - len(V)
            if s > rec[0]:
                rec = (s, len(cur), len(V), frozenset(cur))
        best.append(rec)

    best.sort(key=lambda r: (-r[0], r[2]))
    print("\n  best blocks by surplus (|E| - |V|), greedy from each seed:")
    seen = set()
    shown = 0
    for s, ne, nv, E in best:
        key = (ne, nv)
        if key in seen:
            continue
        seen.add(key)
        print(f"    {ne:3d} equations over {nv:3d} variables   surplus {s:+d}")
        shown += 1
        if shown >= 12:
            break

    top = best[0]
    print(f"\n  best overall: {top[1]} equations, {top[2]} variables, "
          f"surplus {top[0]:+d}")
    if top[0] <= 0:
        print("  no overdetermined block found by this greedy walk.")
        print("  HEURISTIC ONLY: 283 greedy paths do not survey 2^165 subsets.")

    # also report the smallest-variable blocks regardless of surplus -- a small
    # block can be empty without being overdetermined
    bysize = sorted(best, key=lambda r: r[2])
    print("\n  smallest blocks by variable count (solvable regardless of surplus):")
    seen = set()
    out = []
    for s, ne, nv, E in bysize:
        if (ne, nv) in seen:
            continue
        seen.add((ne, nv))
        out.append({'eqs': sorted(E), 'ne': ne, 'nv': nv, 'surplus': s})
        print(f"    {ne:3d} equations over {nv:3d} variables   surplus {s:+d}")
        if len(out) >= 8:
            break
    json.dump(out, open('/home/user/jacobian_planar/wave6/frontier/tb1_blocks.json', 'w'),
              indent=1)
    print("\n  wrote wave6/frontier/tb1_blocks.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
