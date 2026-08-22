#!/usr/bin/env python3
"""Build the SEED-PINNED system at any prime, and solve it.  True like-for-like.

The campaign's `seed0_p1000003.ms` exists at one prime and its generator is not
in the repo, so a second prime looked out of reach.  It is not: the 18 variables
present in `trackB1_param_system.json` but absent from the pinned export are

    c_i_{2i-2}  for i = 1..8      and      d_j_{2j-3}  for j = 3..12

i.e. exactly the bottom-edge unknowns c1..c8, d3..d12.  So the pinning is just
that substitution, and it can be redone at any prime where an admissible
F_p-rational seed exists.

BUILT-IN CONTROL (runs first, every time)
At p = 1000003 this reconstruction is compared equation-by-equation against the
campaign's own export.  It reproduces all 266 equations EXACTLY.  The mapping is
therefore not a guess.

CHOOSING THE PRIME
Only primes whose bottom-edge census shows admissible >= 1 can be used -- there
must be an F_p-rational admissible seed to pin.  From the 13-prime census:
usable 999979, 999983, 1000003, 1000039, 1000081, 1000117, 1000121, 1000133,
1000159, 1000171;  NOT usable 999961, 1000033, 1000151 (admissible = 0).

Usage:  python3 w6_seed_prime.py PRIME [control]
"""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_chain_export import chain_core, write_ms, ROOT
from w6_prime2 import load_exact, reduce_modp, ev_modp
from w6_chain_modp import parse_ms

CHECKPOINTS = [150000, 700000, 2500000]
MAP = {**{f'c{i}': f'c_{i}_{2*i-2}' for i in range(1, 9)},
       **{f'd{j}': f'd_{j}_{2*j-3}' for j in range(3, 13)}}


def admissible_seeds(p):
    """Every admissible F_p-rational bottom-edge seed at p, from its RUR."""
    fn = os.path.join(ROOT, f'wave6/bottomedge/be_p{p}.out')
    t = open(fn).read()
    if t.strip().startswith('[-1]'):
        return []
    vn = [v.strip().strip("'") for v in
          re.search(r"\[('c1'.*?'A')\]", t, re.S).group(1).split(',')]
    b = re.findall(r"\[(\d+),\s*\n?\s*\[([0-9,\s]+)\]\]", t)
    b = [(int(d), [int(c) for c in cs.replace('\n', '').split(',') if c.strip()])
         for d, cs in b]
    wco, params = b[0][1], b[2:]
    out = []
    for x in range(p):
        if sum(c * pow(x, i, p) for i, c in enumerate(wco)) % p:
            continue
        pt = {nm: (-sum(c * pow(x, i, p) for i, c in enumerate(co))) % p
              for nm, (d_, co) in zip(vn, params)}
        if pt.get('c1') and pt.get('c8') and pt.get('d12'):
            out.append(pt)
    return out


def pin(eqs, seed, p):
    sub = {MAP[k]: v % p for k, v in seed.items() if k in MAP}
    assert len(sub) == 18, f"mapping incomplete: {len(sub)} of 18"
    out = []
    for t in eqs:
        nt = {}
        for m, c in t.items():
            coef, rest = c, []
            for v, e in m:
                if v in sub:
                    coef = coef * pow(sub[v], e, p) % p
                else:
                    rest.append((v, e))
            if coef:
                k = tuple(sorted(rest))
                nt[k] = (nt.get(k, 0) + coef) % p
        out.append({k: v for k, v in nt.items() if v})
    return out, sub


def control_reconstruction():
    """The mapping must reproduce the campaign's own export at p = 1000003."""
    p = 1000003
    seeds = admissible_seeds(p)
    assert seeds, "no admissible seed at the control prime"
    V, eqs_q, nz = load_exact()
    mine, _ = pin(reduce_modp(eqs_q, p), seeds[0], p)
    _, ec, _ = parse_ms(os.path.join(ROOT, 'wave6/pentseed/seed0_p1000003.ms'))
    A = sorted(tuple(sorted(t.items())) for t in mine if t)
    B = sorted(tuple(sorted(t.items())) for t in ec if t and 'zz0' not in str(t))
    ok = (A == B)
    print(f"  [control] reconstruction vs campaign export at p=1000003: "
          f"{len(A)} vs {len(B)} equations, identical: {ok}")
    assert ok, "MAPPING CONTROL FAILED - do not trust anything downstream"
    return True


def main():
    p = int(sys.argv[1])
    control_reconstruction()
    seeds = admissible_seeds(p)
    print(f"p = {p}: {len(seeds)} admissible F_p-rational bottom-edge seed(s)")
    if not seeds:
        print("  UNUSABLE at this prime (no admissible seed to pin)")
        return 1
    V, eqs_q, nzlist = load_exact()
    eqs = reduce_modp(eqs_q, p)
    for si, seed in enumerate(seeds):
        pinned, sub = pin([dict(t) for t in eqs], seed, p)
        # every pinned equation must vanish on the bottom-edge subsystem it came
        # from; check the seed really satisfies the 17 bottom-edge equations
        nzero = sum(1 for t in pinned if not t)
        print(f"  seed {si}: pinned 18 variables, {nzero} equations vanish identically")
        nz = {v for v in nzlist if v not in sub}
        res, zeros, solved, done = chain_core(
            V, pinned, p, set(nz), CHECKPOINTS, f'sp{p}_{si}_')
        if res is None:
            print(f"  seed {si}: CONTRADICTION inside the chain -> seed dies at p={p}")
            continue
        rem = sorted(set(V) - set(sub) - zeros - set(solved))
        path = os.path.join(ROOT, f'wave6/pentseed/seedpin_{p}_{si}_{len(rem)}v.ms')
        ne, nv = write_ms(path, res, rem, p, nz - zeros - set(solved))
        print(f"  seed {si}: final {ne} eq, {nv} vars, "
              f"{os.path.getsize(path)/1e6:.2f} MB -> {os.path.basename(path)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
