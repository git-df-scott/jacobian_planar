#!/usr/bin/env python3
"""Use the block-cascade to REDUCE the (9,27) system, then hand each surviving
branch to msolve as a small exact system.

Context: GGHV Corollary 5.7 -- the sole result killing the (9,27) orientation of
(72,108) -- was shown today to have an invalid step (CATCHES.md), so this branch
is live.  wave6/p108_525122_q.gens (140 conditions, c2..c25, w = 1/c2, u) had
timed out repeatedly under direct elimination.

The system is a cascade: its conditions partition into blocks by variable
support, and in each block the gcd is ATTAINED BY SOME GENERATOR, so the block
is equivalent to the single equation gcd = 0 and its irreducible factors are the
branches.  (Verified per node; see w6_p108_cascade.py.)

This script walks the tree but does NOT try to reach verdicts by factorisation
alone.  At each node it
  * substitutes when a branch factor is linear in a free variable,
  * CARRIES the factor as an extra constraint when it is not (no branch lost),
  * carries the residual piece V(h_1..h_n) as its own branch when the gcd is not
    attained (no branch lost),
and at the leaves it writes the accumulated system to msolve format.  Forced-
nonzero variables (c2, c23, c25 from the two saturation rows, and w) are never
used as branch factors and are saturated in the exported system.

Soundness: the union of the exported leaves covers the whole variety, so ALL
leaves EMPTY  ==>  the (9,27) branch system is empty.  A non-empty leaf is a
candidate and must be lifted and verified exactly before any claim.
"""
import re, sys, json, time, os
import sympy as sp

GENS = '/home/user/jacobian_planar/wave6/p108_525122_q.gens'
OUT  = '/home/user/jacobian_planar/wave6/p108branch'
C = sp.symbols('c2:26'); W, U = sp.symbols('w u')
ENV = {'w': W, 'u': U}
for _i in range(2, 26):
    ENV[f'c{_i}'] = ENV.get(f'c{_i}', C[_i-2])
VAR = {i: C[i-2] for i in range(2, 26)}
NONZERO = [VAR[2], VAR[23], VAR[25], W]
SATURATION = {138, 139}

def load():
    s = open(GENS).read().strip().rstrip(',')
    gens = [g.strip() for g in s.split(',') if g.strip()]
    def vs(g): return frozenset(int(v) for v in re.findall(r'c\((\d+)\)', g))
    blocks = {}
    for i, g in enumerate(gens):
        blocks.setdefault(vs(g), []).append(i)
    order = sorted(blocks, key=lambda t: (max(t) if t else 0, len(t)))
    return gens, [(k, blocks[k]) for k in order]

def parse(g):
    return sp.sympify(re.sub(r'c\((\d+)\)', r'c\1', g.replace('^', '**')), locals=ENV)

def sub_expand(e, sub):
    return sp.expand(sp.numer(sp.cancel(sp.together(e.subs(sub)))))

def block_gcd(vals):
    G = vals[0]
    for e in vals[1:]:
        G = sp.gcd(G, e)
    hs = [sp.cancel(sp.expand(e / G)) for e in vals]
    exact = any(h.free_symbols == set() and h != 0 for h in hs)
    return sp.factor(G), exact, [h for h in hs if h.free_symbols]

def branch_factors(G):
    out = []
    for f, k in sp.factor_list(G)[1]:
        if f.is_Number or (f.is_Symbol and f in NONZERO):
            continue
        out.append(sp.expand(f))
    return out

def write_ms(tag, eqs, extra_nonzero=()):
    eqs = [sp.expand(e) for e in eqs if sp.expand(e) != 0]
    for e in eqs:
        if e.free_symbols == set():
            return {'tag': tag, 'status': 'EMPTY-BY-CONSTANT', 'constant': str(e)}
    ts = sp.symbols(f'z0:{len(NONZERO)+len(extra_nonzero)}')
    for v, z in zip(list(NONZERO) + list(extra_nonzero), ts):
        eqs.append(sp.expand(v*z - 1))
    unk = sorted({v for e in eqs for v in e.free_symbols}, key=str)
    cleared = []
    for e in eqs:
        p = sp.Poly(e, *unk); den = 1
        for co in p.coeffs():
            den = sp.lcm(den, co.q if hasattr(co, 'q') else 1)
        cleared.append(sp.expand(e*den))
    head = ",".join(str(u) for u in unk) + "\n"
    body = ",\n".join(str(sp.Poly(e, *unk).as_expr()).replace('**', '^').replace(' ', '')
                      for e in cleared)
    os.makedirs(OUT, exist_ok=True)
    for p in (1000003, 1000033):
        open(f"{OUT}/{tag}_p{p}.ms", "w").write(head + str(p) + "\n" + body + "\n")
    open(f"{OUT}/{tag}_q.ms", "w").write(head + "0\n" + body + "\n")
    return {'tag': tag, 'status': 'EXPORTED', 'eqs': len(cleared), 'unknowns': len(unk),
            'max_deg': int(max(sp.total_degree(e) for e in cleared))}

def walk(gens, blocks, maxleaves=40):
    leaves = []
    stack = [({}, [], 0, 'L')]          # (substitution, carried constraints, block index, tag)
    while stack and len(leaves) < maxleaves:
        sub, carried, bi, tag = stack.pop()
        if bi >= len(blocks):
            rest = []
            for key, idxs in blocks:
                if set(idxs) <= SATURATION:
                    continue
                for i in idxs:
                    rest.append(sub_expand(parse(gens[i]), sub))
            leaves.append(write_ms(tag, carried + rest))
            print(json.dumps(leaves[-1]), flush=True); continue
        key, idxs = blocks[bi]
        if not key or set(idxs) <= SATURATION:
            stack.append((sub, carried, bi+1, tag)); continue
        vals = []
        dead = False
        for i in idxs:
            e = sub_expand(parse(gens[i]), sub)
            if e == 0:
                continue
            if e.free_symbols == set():
                leaves.append({'tag': tag, 'status': 'CLOSED-CONSTANT', 'at': bi})
                print(json.dumps(leaves[-1]), flush=True); dead = True; break
            vals.append(e)
        if dead:
            continue
        if not vals:
            stack.append((sub, carried, bi+1, tag)); continue
        G, exact, hs = block_gcd(vals)
        facs = branch_factors(G)
        if not exact:                       # residual piece V(h_1..h_n): keep it
            stack.append((sub, carried + hs, bi+1, tag + 'R'))
        if not facs:
            leaves.append({'tag': tag, 'status': 'CLOSED-UNIT-GCD', 'at': bi})
            print(json.dumps(leaves[-1]), flush=True); continue
        for fi, f in enumerate(facs):
            cand = [v for v in sorted(f.free_symbols, key=str)
                    if sp.degree(f, v) == 1 and v not in NONZERO]
            if cand:
                v = cand[-1]
                s2 = dict(sub); s2[v] = sp.cancel(sp.solve(f, v)[0])
                stack.append((s2, carried, bi+1, tag + str(fi)))
            else:                            # nonlinear factor: carry it
                stack.append((sub, carried + [f], bi+1, tag + str(fi) + 'n'))
    return leaves

if __name__ == '__main__':
    gens, blocks = load()
    print(f"loaded {len(gens)} gens, {len(blocks)} blocks", flush=True)
    t0 = time.time()
    L = walk(gens, blocks)
    json.dump(L, open('/home/user/jacobian_planar/wave6/p108_branches.json', 'w'), indent=1)
    print(f"\n{len(L)} leaves in {round(time.time()-t0,1)}s", flush=True)
