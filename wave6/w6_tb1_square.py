#!/usr/bin/env python3
"""Extract and solve the SQUARE subsystem of trackB1.

The subsystem search found no overdetermined block (max surplus 0), so the
straightforward monotone-emptiness shortcut is unavailable. But it did surface
SQUARE blocks -- |E| = |V| -- and those are the ones worth everything here.

WHY A SQUARE BLOCK DECIDES THINGS
A square polynomial system is generically zero-dimensional: finitely many
solutions. That gives a COMPLETE decision procedure for the whole of trackB1:

  * block EMPTY            -> trackB1 is EMPTY. Monotone: a subset with no
                              solution means the superset has none. VERDICT.
  * block has finitely many solutions -> enumerate them, substitute each into
                              the remaining 224 equations, and check. Every
                              solution of trackB1 restricts to a solution of the
                              block, so this loses nothing. VERDICT either way.

Either branch terminates, which is the whole point: every Groebner attack on the
full 166-variable system has returned NO VERDICT, and a timeout is not a result.

This exports the block at both primes and solves it.
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import load, parse_poly

SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')


def grow(EV, n, seed, cap):
    cur = {seed}; V = set(EV[seed]); best = None
    for _ in range(cap):
        cand, gain = None, None
        for j in range(n):
            if j in cur:
                continue
            g = len(EV[j] - V)
            if gain is None or g < gain:
                cand, gain = j, g
        if cand is None:
            break
        cur.add(cand); V |= EV[cand]
        if len(cur) >= len(V) and (best is None or len(V) < best[1]):
            best = (frozenset(cur), len(V))
    return best


def main():
    src = os.environ.get('TB1_SRC',
          '/home/user/jacobian_planar/wave6/frontier/trackB1_sat_p1000003.ms')
    vs, p, body = load(src)
    polys = [parse_poly(b, p) for b in body]
    EV = [frozenset(v for m in q for v, _ in m) for q in polys]
    n = len(polys)
    print(f"{os.path.basename(src)}: {n} eqs, {len(vs)} vars, p={p}")

    cands = []
    for seed in range(n):
        b = grow(EV, n, seed, 120)
        if b:
            cands.append(b)
    if not cands:
        print("no square-or-better block found")
        return 1
    # Smallest variable count wins among NONTRIVIAL blocks. The 2x2 block is
    # just the two monomial rows c_1_0*d_0_1, c_1_0*d_1_1 -- it is square but
    # decides nothing, since it is solved by c_1_0 = 0 and carries no
    # saturation row to forbid that. Require a real block.
    MINV = int(os.environ.get('MINV', '20'))
    big = [t for t in cands if t[1] >= MINV]
    if big:
        cands = big
    cands.sort(key=lambda t: (t[1], len(t[0])))
    seen = set(); uniq = []
    for E, nv in cands:
        if E in seen:
            continue
        seen.add(E); uniq.append((E, nv))
    print(f"  square-or-better blocks found: {len(uniq)} distinct")
    for E, nv in uniq[:6]:
        print(f"    {len(E)} equations over {nv} variables  "
              f"(surplus {len(E)-nv:+d})")

    E, nv = uniq[0]
    idx = sorted(E)
    BV = sorted({v for i in idx for v in EV[i]})
    assert len(BV) == nv
    print(f"\n  chosen block: {len(idx)} equations, {nv} variables")
    print(f"    variables: {BV[:8]}{' ...' if len(BV)>8 else ''}")
    degs = [max((sum(x for _, x in m) for m in polys[i]), default=0) for i in idx]
    print(f"    max degree {max(degs)}, {sum(len(polys[i]) for i in idx)} terms")
    # does it contain the saturation row? that row is what forbids the zero point
    sat = [i for i in idx if any(v.startswith(('zsat', 'w_sat')) for v in EV[i])]
    print(f"    contains saturation row: {'YES ' + str(sat) if sat else 'NO'}")
    if not sat:
        print("    NOTE: without the saturation row the block may be satisfied by")
        print("    the all-zero point, so NONEMPTY here would be uninformative.")
        print("    EMPTY would still be decisive.")

    bodyout = [body[i] for i in idx]
    used = set(re.findall(r'[A-Za-z_]\w*', "\n".join(bodyout)))
    leak = sorted(used - set(BV))
    assert not leak, f"REFUSING: undeclared {leak[:8]}"
    ms = f'{SCR}/tb1_square.ms'
    open(ms, 'w').write(",".join(BV) + f"\n{p}\n" + ",\n".join(bodyout) + "\n")
    sg = f'{SCR}/tb1_square.sing'
    open(sg, 'w').write(
        f'ring R = {p}, ({",".join(BV)}), dp;\nideal I = ' + ",\n".join(bodyout) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "SQUARE RESULT UNIT -- BLOCK EMPTY -- '
        'trackB1 EMPTY"; }\n'
        'else { "SQUARE RESULT NOTUNIT -- block nonempty"; "dim:"; dim(G); '
        '"gbsize:"; size(G); "vdim:"; vdim(G); }\nexit;\n')
    json.dump({'eqs': idx, 'vars': BV},
              open('/home/user/jacobian_planar/wave6/frontier/tb1_square_block.json', 'w'),
              indent=1)
    print(f"\n  wrote {ms}")
    print(f"  wrote {sg}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
