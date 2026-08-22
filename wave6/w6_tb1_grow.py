#!/usr/bin/env python3
"""Grow the decisive block one step at a time until it decides trackB1.

WHY INCREMENTAL
The 166-variable root is out of reach: seven attacks, two engines, two primes,
four orders, all NO VERDICT. The 61-variable saturated block terminates but is
probably NONEMPTY, since 60 equations in 60 variables is not overdetermined.
Between "too hard to run" and "too weak to decide" there is a range of block
sizes, and the way to find it is to walk it.

Emptiness is monotone, so growing the block can only ever turn NONEMPTY into
EMPTY, never the reverse. Every step is a terminating computation, and the FIRST
step that returns EMPTY is a verdict on all of trackB1:

    block EMPTY  =>  trackB1 EMPTY

A step that returns NONEMPTY costs nothing but time and tells us to add more.
A step that times out is where the walk stops, and it is reported as the place
the method ran out -- not as a result.

ORDERING
At each step add the equation introducing the FEWEST new variables, so the
variable count grows as slowly as possible while the equation count climbs. That
drives the block toward being overdetermined, which is where emptiness lives.
The saturation row is carried at every step so the all-zero point is always
excluded -- without it a block is satisfied trivially and NONEMPTY means nothing.
"""
import sys, os, re, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import load, parse_poly

SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')
FORCED = ['c_1_0', 'c_8_14', 'd_12_21', 's_4_8']
STEP = int(os.environ.get('GROW_STEP', '12'))
TMO = int(os.environ.get('GROW_T', '420'))
MEM = os.environ.get('GROW_MEM', '3000000')


def solve(tag, V, E, p):
    zz = 'zzg'
    present = [v for v in FORCED if v in set(V)]
    Vs = V + [zz]
    Es = E + [f"{zz}*" + "*".join(present) + "-1"] if present else E
    if not present:
        Vs = V
    used = set(re.findall(r'[A-Za-z_]\w*', "\n".join(Es)))
    leak = sorted(used - set(Vs))
    assert not leak, f"REFUSING {tag}: undeclared {leak[:8]}"
    f = f'{SCR}/grow_{tag}.sing'
    open(f, 'w').write(
        f'ring R = {p}, ({",".join(Vs)}), dp;\nideal I = ' + ",\n".join(Es) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "GROW EMPTY"; } else { "GROW NONEMPTY"; '
        '"dim:"; dim(G); }\nexit;\n')
    r = subprocess.run(['bash', '-c',
                        f'ulimit -v {MEM}; timeout {TMO} Singular -q {f}'],
                       capture_output=True, text=True)
    o = r.stdout
    if 'GROW EMPTY' in o:
        return 'EMPTY', len(present)
    if 'GROW NONEMPTY' in o:
        d = re.search(r'dim:\s*\n?\s*(-?\d+)', o)
        return f'NONEMPTY(dim={d.group(1) if d else "?"})', len(present)
    return 'NOVERDICT', len(present)


def main():
    src = os.environ.get('TB1_SRC',
          '/home/user/jacobian_planar/wave6/frontier/trackB1_sat_p1000003.ms')
    vs, p, body = load(src)
    polys = [parse_poly(b, p) for b in body]
    EV = [frozenset(v for m in q for v, _ in m) for q in polys]
    blk = json.load(open('/home/user/jacobian_planar/wave6/frontier/'
                         'tb1_square_block.json'))
    cur = set(blk['eqs'])
    V = set()
    for i in cur:
        V |= EV[i]
    print(f"start: {len(cur)} equations, {len(V)} variables, p={p}", flush=True)

    while True:
        E = [body[i] for i in sorted(cur)]
        Vl = sorted(V)
        tag = f"{len(cur)}x{len(Vl)}"
        st, nf = solve(tag, Vl, E, p)
        print(f"  block {len(cur):3d} eq / {len(Vl):3d} var  "
              f"(saturating on {nf} forced-nonzero) -> {st}", flush=True)
        if st == 'EMPTY':
            print(f"\n*** BLOCK EMPTY at {len(cur)} equations / {len(Vl)} variables")
            print("*** Emptiness is monotone, so trackB1 is EMPTY. VERDICT.")
            return 0
        if st == 'NOVERDICT':
            print(f"\nwalk stops here: {len(cur)} eq / {len(Vl)} var gave no verdict "
                  f"in {TMO}s at {int(MEM)//1000}MB.")
            print("That is where the method ran out. NOT a result about trackB1.")
            return 0
        # add the equations bringing in the fewest new variables
        rest = [j for j in range(len(polys)) if j not in cur]
        if not rest:
            print("\nwhole system consumed and still NONEMPTY -- "
                  "that IS trackB1 NONEMPTY. Verify immediately.")
            return 0
        rest.sort(key=lambda j: len(EV[j] - V))
        for j in rest[:STEP]:
            cur.add(j); V |= EV[j]


if __name__ == '__main__':
    sys.exit(main())
