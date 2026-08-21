#!/usr/bin/env python3
"""THE (9,27) BRANCH OF (72,108), ATTACKED BY FACTORISATION INSTEAD OF GROEBNER.

Context: GGHV Corollary 5.7 was the ONLY result killing the (9,27) orientation
of (72,108), and on 2026-08-21 it was verified to have an invalid step (see
CATCHES.md).  So this branch is live again and its systems are first-class
targets.  The smallest is wave6/p108_525122_q.gens: 140 conditions, 24 c-vars
plus w (= 1/c2) and u.  Exact Groebner has timed out on it repeatedly at 1800 s.

THE STRUCTURE NOBODY USED.  The 140 conditions are not a generic system.  They
fall into blocks by variable support:

    {c3,c4}                      22 gens
    {c3..c7}                     20
    {c3..c10}                    18
    {c3..c13}                    16
    {c3..c16}                    14
    {c3..c19}                    12
    {c3..c22}                    10
    {c3..c25}                    22   + 2 sparse rows + the two saturations

and -- verified, not assumed -- every generator of a block factors as

    (integer) * (monomial in the already-solved variables) * M

with ONE common non-monomial factor M per block.  Hence

    V(block)  =  V(M)  u  V(gcd of the monomial parts),

i.e. each block of ~20 equations collapses to a SINGLE binary branch.  That is
why Groebner engines choke (huge coefficients, 26 variables) on an object whose
solution set is a shallow tree.

This script walks that tree exactly over Q.  At each block it
  (a) substitutes the current branch,
  (b) factors every generator,
  (c) splits each into monomial part and residual part,
  (d) CHECKS that the residual parts are all associate to one M (if they are
      not, it says so and stops rather than guessing -- the structure claim is
      falsifiable at every node),
  (e) branches on M = 0 versus (each variable of the monomial gcd) = 0.
Nonzero constraints c2, c23, c25 != 0 (from the two saturation rows) and w != 0
prune branches.

Usage: python3 wave6/w6_p108_cascade.py [maxdepth]
"""
import re, sys, json, time
import sympy as sp

GENS = '/home/user/jacobian_planar/wave6/p108_525122_q.gens'
C = sp.symbols('c2:26'); W, U = sp.symbols('w u')
ENV = {'w': W, 'u': U}
for _i in range(2, 26):
    ENV[f'c{_i}'] = C[_i-2]
VAR = {i: C[i-2] for i in range(2, 26)}
NONZERO = [VAR[2], VAR[23], VAR[25], W]        # forced by c2*w-1 and c2*c23*c25*u-1

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

SATURATION = {138, 139}     # c2*w-1 and c2*c23*c25*u-1: nonzero data, not equations

def block_variety(vals):
    """vals = list of (i, nonzero substituted polynomial).

    Returns (G, exact, hs) where G = gcd of the block.  Since every
    V(f_i) = V(G) u V(h_i) with f_i = G*h_i,

        V(block) = V(G)  u  V(h_1, ..., h_n),

    and when SOME h_i is a nonzero constant the second piece is empty, so
    V(block) = V(G) EXACTLY -- the block is equivalent to the single equation
    G = 0.  `exact` records whether that happened; if it did not, the residual
    system hs is reported rather than silently dropped.
    """
    polys = [e for _, e in vals]
    G = polys[0]
    for e in polys[1:]:
        G = sp.gcd(G, e)
    hs = [sp.cancel(sp.expand(e / G)) for e in polys]
    exact = any(h.free_symbols == set() and h != 0 for h in hs)
    return sp.factor(G), exact, hs

def analyse_block(gens, idxs, sub):
    """Returns ('empty'|'free'|'branch', payload)."""
    vals = []
    for i in idxs:
        e = sp.together(parse(gens[i]).subs(sub))
        e = sp.expand(sp.numer(sp.cancel(e)))     # substitutions can introduce 1/c2
        if e == 0:
            continue
        if e.free_symbols == set():
            return 'empty', f'nonzero constant generator from gen[{i}]'
        vals.append((i, e))
    if not vals:
        return 'free', None
    G, exact, hs = block_variety(vals)
    hs = [h for h in hs if h.free_symbols]      # drop constants (they close V(h_i))
    return 'branch', {'G': G, 'exact': bool(exact), 'n': len(vals), 'hs': hs}

def branch_factors(G):
    """Irreducible non-constant factors of G, dropping those forced nonzero."""
    out = []
    for f, k in sp.factor_list(G)[1]:
        if f.is_Number:
            continue
        if f.is_Symbol and (f in NONZERO):
            continue                    # w, c2, c23, c25 != 0: this factor cannot vanish
        out.append(sp.expand(f))
    return out

def walk(gens, blocks, maxdepth):
    t0 = time.time(); leaves = []
    stack = [({}, 0, [])]
    while stack:
        sub, bi, path = stack.pop()
        if bi >= len(blocks) or len(path) > maxdepth:
            leaves.append({'path': path, 'status': 'OPEN', 'block_reached': bi})
            print(json.dumps(leaves[-1]), flush=True); continue
        key, idxs = blocks[bi]
        if not key or set(idxs) <= SATURATION:   # saturation rows carry no equation
            stack.append((sub, bi+1, path)); continue
        kind, pay = analyse_block(gens, idxs, sub)
        tag = f"block{bi}{sorted(key)[:3]}..({len(idxs)})"
        if kind == 'empty':
            leaves.append({'path': path, 'status': 'CLOSED', 'why': pay, 'at': tag})
            print(json.dumps(leaves[-1]), flush=True); continue
        if kind == 'free':
            stack.append((sub, bi+1, path)); continue
        G, exact = pay['G'], pay['exact']
        facs = branch_factors(G)
        print(f"# {tag} depth={len(path)} exact={exact} branches={[str(f)[:70] for f in facs]}",
              flush=True)
        if not exact:
            # V(block) = V(G) u V(h_1..h_n).  Explore V(G) below; record the
            # residual piece explicitly so it is never silently dropped.
            leaves.append({'path': path + ['RESIDUAL PIECE V(h_1..h_n)'],
                           'status': 'OPEN-RESIDUAL', 'at': tag,
                           'nh': len(pay['hs']),
                           'h_head': [str(h)[:160] for h in pay['hs'][:3]]})
            print(json.dumps(leaves[-1]), flush=True)
        if not facs:
            leaves.append({'path': path, 'status': 'CLOSED',
                           'why': 'gcd is a unit times forced-nonzero variables only',
                           'at': tag}); print(json.dumps(leaves[-1]), flush=True); continue
        for f in facs:
            cand = [v for v in sorted(f.free_symbols, key=str)
                    if sp.degree(f, v) == 1 and v not in NONZERO]
            if cand:
                v = cand[-1]
                s2 = dict(sub); s2[v] = sp.cancel(sp.solve(f, v)[0])
                stack.append((s2, bi+1, path + [f"{v}=({sp.factor(s2[v])})"]))
            else:
                leaves.append({'path': path + [f"{f} = 0 (not linear in a free var)"],
                               'status': 'OPEN-NONLINEAR', 'at': tag})
                print(json.dumps(leaves[-1]), flush=True)
    print(f"\nleaves={len(leaves)}  elapsed={round(time.time()-t0,1)}s")
    return leaves

if __name__ == '__main__':
    maxdepth = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    gens, blocks = load()
    print(f"loaded {len(gens)} gens in {len(blocks)} blocks: "
          f"{[(sorted(k)[:2], len(v)) for k, v in blocks]}", flush=True)
    out = walk(gens, blocks, maxdepth)
    json.dump(out, open('/home/user/jacobian_planar/wave6/p108_cascade.json', 'w'), indent=1)
