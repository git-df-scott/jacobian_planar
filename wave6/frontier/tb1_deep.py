#!/usr/bin/env python3
"""Chain trackB1 (saturated) to a fixed point mod p, then export for solving.

Tier 1's blocker is the REDUCTION, not the solver: branching bought 3 variables
because trackB1 has only two monomial equations and both share c_1_0.  The
exact chain is the lever, and mod p it does not suffer the Fraction blow-up that
makes the char-0 version slow.
"""
import sys, os
sys.path.insert(0, '/home/user/jacobian_planar/wave6')
from w6_chain_modp import parse_ms
from w6_chain_export import chain_core, write_ms

src = sys.argv[1] if len(sys.argv) > 1 else 'wave6/frontier/trackB1_sat_p1000003.ms'
V, eqs, p = parse_ms(src)
nz = {'c_1_0', 'c_8_14', 'd_12_21', 's_4_8'}
print(f"{os.path.basename(src)}: {len(eqs)} eq, {len(V)} vars, p={p}", flush=True)
res, zeros, solved, done = chain_core(V, [dict(t) for t in eqs], p, set(nz),
                                      [400000, 1500000, 5000000], 'tb1deep_')
if res is None:
    print("CONTRADICTION -> EMPTY")
else:
    rem = sorted(set(V) - zeros - set(solved))
    live = [t for t in res if t]
    print(f"chain: {len(zeros)} zeros, {len(solved)} pivots -> "
          f"{len(live)} equations, {len(rem)} variables (was {len(eqs)}/{len(V)})",
          flush=True)
    path = f'wave6/frontier/trackB1_chained_{len(rem)}v_p{p}.ms'
    ne, nv = write_ms(path, res, rem, p, nz - zeros - set(solved))
    print(f"wrote {path}: {ne} eq, {nv} vars, {os.path.getsize(path)/1e6:.2f}MB")
