#!/usr/bin/env python3
"""Beat a MEMORY wall by branching, not by buying RAM.

THE SITUATION
`campaign/moduli_phase2/FRAMEWORK.md` records its frontier as closed by
infeasibility: "the unresolved cases are killed by the OOM killer inside the
time budget ... More RAM, or an F4/FGLM engine such as msolve, moves the line
further."  Tonight msolve was pointed at `k=5, h=t, D=4` for the first time and
gave NO VERDICT at 6 GB (SIGSEGV) and at 10 GB; Singular `slimgb` also gave no
verdict.  So the named fix does not suffice at this scale.

THE OPENING
That system has **6 single-monomial equations, every one a product of exactly
two variables**, over 8 distinct variables, and `c_46` occurs in 4 of them.
A monomial equation `c_i * c_j = 0` is not a constraint to be ground through --
it is a BINARY CASE SPLIT, and both sides are cheap:

    c_46 = 0        -> 4 monomial equations vanish, and c_46 leaves the system
    c_46 != 0       -> all four of its partners are FORCED to zero

Either way several variables die immediately.  The branch tree collapses instead
of growing, because the monomial equations share variables.  Each leaf is a much
smaller system than the root, and a memory wall is a statement about the root.

SOUNDNESS
The split is exhaustive: over a field, `uv = 0` implies `u = 0` or `v = 0`. So
**every leaf EMPTY implies the root EMPTY.** Any leaf that is NOT empty is a
genuine lead and is reported as such, never averaged away.

A leaf with no verdict makes the whole run NO VERDICT -- one unresolved leaf
means the root is unresolved, and that is reported rather than rounded off.
"""
import sys, os, re, subprocess
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_chain_modp import parse_ms

SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')
LEAF_TIMEOUT = int(os.environ.get('LEAF_T', '120'))
MEM_KB = os.environ.get('LEAF_MEM', '4000000')


def subs_zero(eqs, zeros):
    return [{m: c for m, c in t.items() if not any(v in zeros for v, _ in m)}
            for t in eqs]


def solve_leaf(eqs, allvars, p, tag):
    live = [t for t in eqs if t]
    if not live:
        return 'NONEMPTY', 'no equations left -- everything satisfied'
    vs = sorted({v for t in live for m in t for v, _ in m})
    if not vs:
        return 'EMPTY', 'a nonzero constant equation remains'
    # COMPOSE: run the exact forced chain on the leaf before handing it to a
    # solver.  Branch shrinks the case space, the chain shrinks the system, and
    # only what survives both reaches Groebner.  Each step is an exact
    # implication, so an EMPTY verdict downstream still proves the leaf empty.
    if os.environ.get('LEAF_CHAIN', '1') == '1':
        try:
            from w6_chain_export import chain_core
            red, z2, s2, _ = chain_core(sorted(vs), [dict(x) for x in live], p,
                                        set(), [10**9], f'lf{tag}_',
                                        log=lambda *a, **k: None)
            if red is None:
                return 'EMPTY', 'chain reached a contradiction on this leaf'
            r2 = [x for x in red if x]
            v2 = sorted({v for x in r2 for m in x for v, _ in m})
            if len(v2) < len(vs):
                live, vs = r2, v2
        except Exception:
            pass
        if not live:
            return 'NONEMPTY', 'chain removed every equation'
        if not vs:
            return 'EMPTY', 'chain left a nonzero constant'
    body = []
    for t in live:
        body.append("+".join("*".join([str(c)] + [f"{v}^{e}" if e > 1 else v
                                                  for v, e in m])
                             for m, c in t.items()).replace("+-", "-"))
    f = f'{SCR}/leaf_{tag}.sing'
    open(f, 'w').write(f'ring R = {p}, ({",".join(vs)}), dp;\nideal I = ' +
                       ",\n".join(body) + ';\noption(redSB);\nideal G = slimgb(I);\n'
                       'if (size(G)==1 && G[1]==1) { "LEAF EMPTY"; } '
                       'else { "LEAF NONEMPTY"; "dim:"; dim(G); }\nexit;\n')
    r = subprocess.run(['bash', '-c',
                        f'ulimit -v {MEM_KB}; timeout {LEAF_TIMEOUT} Singular -q {f}'],
                       capture_output=True, text=True)
    o = r.stdout
    if 'LEAF EMPTY' in o:
        return 'EMPTY', f'{len(live)} eq / {len(vs)} vars [slimgb]'
    if 'LEAF NONEMPTY' in o:
        d = re.search(r'dim:\s*\n?\s*(-?\d+)', o)
        return 'NONEMPTY', (f'{len(live)} eq / {len(vs)} vars, '
                            f'dim={d.group(1) if d else "?"} [slimgb]')
    # SECOND ENGINE (Air France 447): slimgb stalled, so try msolve on this leaf
    # before declaring no verdict.  The two engines have beaten each other on
    # different systems tonight, so neither gets to be the sole authority.
    if p == 0:
        # msolve has no char-0 emptiness mode we rely on here; slimgb already
        # answered or stalled, so do not fabricate a second opinion.
        return 'NOVERDICT', f'{len(live)} eq / {len(vs)} vars (char 0, slimgb only)'
    ms = f'{SCR}/leaf_{tag}.ms'
    open(ms, 'w').write(",".join(vs) + f"\n{p}\n" + ",\n".join(body) + "\n")
    r2 = subprocess.run(['bash', '-c',
                         f'ulimit -v {MEM_KB}; timeout {LEAF_TIMEOUT} '
                         f'msolve -f {ms} -o {ms}.out 2>/dev/null'],
                        capture_output=True, text=True)
    try:
        v = open(f'{ms}.out').read().strip()
    except OSError:
        v = ''
    if v.startswith('[-1]'):
        return 'EMPTY', f'{len(live)} eq / {len(vs)} vars [msolve]'
    if v.startswith('[0'):
        return 'NONEMPTY', f'{len(live)} eq / {len(vs)} vars [msolve]'
    return 'NOVERDICT', f'{len(live)} eq / {len(vs)} vars (both engines: no verdict)'


def branch(eqs, zeros, nonzeros, allvars, p, depth, path, out, cap=40):
    if len(out['leaves']) >= cap:
        out['truncated'] = True
        return
    eqs = subs_zero(eqs, zeros)
    # forced values and contradictions from single monomials
    changed = True
    while changed:
        changed = False
        for t in eqs:
            if len(t) != 1:
                continue
            (mono, coef), = t.items()
            if not mono:
                out['leaves'].append((path, 'EMPTY', 'nonzero constant = 0'))
                return
            free = [v for v, _ in mono if v not in nonzeros]
            if not free:
                out['leaves'].append((path, 'EMPTY',
                                      'monomial of required-nonzero vars = 0'))
                return
            if len(free) == 1 and free[0] not in zeros:
                zeros = zeros | {free[0]}
                eqs = subs_zero(eqs, zeros)
                changed = True
    # pick a branch variable: the one in the most remaining monomial equations
    cnt = defaultdict(int)
    for t in eqs:
        if len(t) == 1:
            (mono, _), = t.items()
            for v, _ in mono:
                if v not in zeros and v not in nonzeros:
                    cnt[v] += 1
    if not cnt:
        st, info = solve_leaf(eqs, allvars, p, f'{len(out["leaves"])}')
        out['leaves'].append((path, st, info))
        print(f"    leaf [{path}] -> {st}  ({info})", flush=True)
        return
    v = max(cnt, key=lambda k: cnt[k])
    branch(eqs, zeros | {v}, nonzeros, allvars, p, depth + 1, path + f'{v}=0;', out, cap)
    branch(eqs, zeros, nonzeros | {v}, allvars, p, depth + 1, path + f'{v}!=0;', out, cap)


def main():
    src = sys.argv[1]
    V, eqs, p = parse_ms(src)
    print(f"{os.path.basename(src)}: {len(eqs)} equations, {len(V)} variables, p={p}")
    out = {'leaves': [], 'truncated': False}
    branch([dict(t) for t in eqs], set(), set(), set(V), p, 0, '', out)
    st = [s for _, s, _ in out['leaves']]
    ne = [l for l in out['leaves'] if l[1] == 'NONEMPTY']
    nv = [l for l in out['leaves'] if l[1] == 'NOVERDICT']
    print(f"\nleaves: {len(st)}  EMPTY={st.count('EMPTY')}  "
          f"NONEMPTY={len(ne)}  NOVERDICT={len(nv)}"
          f"{'  (TRUNCATED)' if out['truncated'] else ''}")
    for l in ne:
        print(f"  *** LEAD leaf: {l[0]}  {l[2]}")
    for l in nv:
        print(f"  unresolved leaf: {l[0]}  {l[2]}")
    if ne:
        print("\nVERDICT: NOT EMPTY -- at least one branch has solutions (a LEAD)")
    elif nv or out['truncated']:
        print("\nVERDICT: NO VERDICT -- some leaf unresolved, so the root is unresolved")
    else:
        print("\nVERDICT: EMPTY -- every branch of an exhaustive split is empty")
    return 0


if __name__ == '__main__':
    sys.exit(main())
