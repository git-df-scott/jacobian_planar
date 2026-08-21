#!/usr/bin/env python3
"""Sieve, then solve.  Export the reduced SEED-PINNED system at checkpoints.

THE TRADE-OFF (Gauss's fill-in, stated quantitatively)
------------------------------------------------------
Each pivot removes one variable but densifies the survivors.  Groebner cost is
doubly exponential in the VARIABLE COUNT and roughly linear-ish in input size,
so there is an optimum: eliminate as many variables as possible while the term
count stays inside what msolve can ingest.

  the two runs that produced NO VERDICT were at 148 and 123 variables
  the chain reaches 77 variables, but at 2.6M terms

So we export at several checkpoints and solve the best one, rather than
guessing.

SATURATION (Rabinowitsch) -- essential, and easy to get wrong
------------------------------------------------------------
The question is not "does the pinned system have a solution" but "does it have
an ADMISSIBLE one", i.e. with the required-nonzero variables actually nonzero.
Without enforcing that, msolve could return a degenerate solution and we would
read a hit that is not one.  So we add a fresh variable zz and the equation

    zz * (product of required-nonzero variables) - 1 = 0

which is satisfiable exactly when every one of them is nonzero.

READING THE VERDICT
  msolve [-1]  -> no admissible solution mod p.  The seed does NOT extend at
                  this prime.  NOT a char-0 proof (this campaign proved modular
                  emptiness unsound for contradictions) but a real, specific
                  result that then needs lifting.
  msolve [0,..]-> an admissible solution mod p EXISTS: the seed extends at this
                  prime.  That is counterexample territory and demands exact
                  lifting and verification before it is anything.
  empty file   -> NO VERDICT (timeout/crash).  Never read as EMPTY.
"""
import sys, os, re
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_chain_modp import parse_ms, gcd_mono

ROOT = '/home/user/jacobian_planar'
NONZERO = ['c_1_0', 'c_8_14', 'd_12_21', 's_4_8']
CHECKPOINTS = [40000, 150000, 600000]


def write_ms(path, eqs, varlist, p, nonzero_present):
    """Write an msolve input, saturating the required-nonzero variables."""
    live = [t for t in eqs if t]
    vs = sorted(varlist)
    body = []
    for t in live:
        parts = []
        for m, c in t.items():
            f = [str(c)] + [f"{v}^{e}" if e > 1 else v for v, e in m]
            parts.append("*".join(f))
        body.append("+".join(parts).replace("+-", "-"))
    if nonzero_present:
        vs = vs + ['zz9']
        sat = "*".join(['zz9'] + sorted(nonzero_present)) + "-1"
        body.append(sat)
    # GUARD: never emit a file whose equations use an undeclared variable.
    # This exact failure produced a spurious msolve [-1] (see RETRACTION_msolve.md):
    # a pivot leaves deg>=2 monomials untouched, so the variable survives in the
    # equations while being dropped from the header, and msolve reads garbage.
    import re as _re
    used = {tok for tok in _re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    leak = sorted(used - set(vs))
    assert not leak, (f"REFUSING to write {path}: {len(leak)} variables appear in "
                      f"the equations but not the header: {leak[:8]}")
    with open(path, 'w') as f:
        f.write(",".join(vs) + "\n" + str(p) + "\n" + ",\n".join(body) + "\n")
    return len(live) + (1 if nonzero_present else 0), len(vs)


def main():
    src = os.path.join(ROOT, 'wave6/pentseed/seed0_p1000003.ms')
    V, eqs, p = parse_ms(src)
    nonzero = {v for v in NONZERO if v in V}
    zeros, solved = set(), {}
    print(f"source: {len(eqs)} eq, {len(V)} vars, p={p}, nondeg present {sorted(nonzero)}")
    done = []
    nxt = 0

    for rnd in range(1, 4000):
        eqs = [{m: c for m, c in t.items() if not any(v in zeros for v, _ in m)}
               for t in eqs]
        div = 0
        for i, t in enumerate(eqs):
            if not t or len(t) == 1:
                continue
            g = gcd_mono(t)
            ok = {v: e for v, e in g.items() if v in nonzero}
            if ok:
                nt = {}
                for m, c in t.items():
                    dm = defaultdict(int, dict(m))
                    for v, e in ok.items():
                        dm[v] -= e
                    nt[tuple(sorted((a, b) for a, b in dm.items() if b > 0))] = c
                eqs[i] = nt; div += 1
        if div:
            continue
        nz, contra = set(), None
        for i, t in enumerate(eqs):
            if len(t) != 1:
                continue
            (mono, coef), = t.items()
            if not mono:
                contra = f"eq{i}: nonzero constant {coef} = 0"; break
            free = [v for v, _ in mono if v not in nonzero]
            if not free:
                contra = f"eq{i}: {mono}=0 with every factor required nonzero"; break
            if len(free) == 1 and free[0] not in zeros:
                nz.add(free[0])
        if contra or (nz & nonzero):
            print(f"*** CONTRADICTION mod p *** {contra or sorted(nz & nonzero)}")
            return 2
        if nz:
            zeros |= nz; continue
        cand = []
        for i, t in enumerate(eqs):
            if not t:
                continue
            for m, c in t.items():
                if len(m) != 1 or m[0][1] != 1:
                    continue
                v = m[0][0]
                if v in zeros or v in solved:
                    continue
                if any(v in dict(m2) for m2 in t if m2 != m):
                    continue
                # FIX: v must appear with degree <= 1 EVERYWHERE, else the
                # deg>=2 monomials survive substitution and v is not really
                # eliminated (it then leaks out of the exported header).
                if any(dict(m3).get(v, 0) > 1 for t3 in eqs for m3 in t3):
                    continue
                cand.append((len(t), i, v, c))
        if not cand:
            print("fixed point")
            break
        cand.sort()
        _, i, v, c = cand[0]
        inv = pow(c, p - 2, p)
        rhs = {m2: (-c2 * inv) % p for m2, c2 in eqs[i].items()
               if not (len(m2) == 1 and m2[0] == (v, 1))}
        out = []
        for t in eqs:
            nt = defaultdict(int)
            for m, cc in t.items():
                if dict(m).get(v, 0) != 1:
                    nt[m] = (nt[m] + cc) % p; continue
                rest = tuple(sorted((a, b) for a, b in m if a != v))
                for m2, c2 in rhs.items():
                    mg = defaultdict(int)
                    for a, b in rest:
                        mg[a] += b
                    for a, b in m2:
                        mg[a] += b
                    key = tuple(sorted((a, b) for a, b in mg.items() if b > 0))
                    nt[key] = (nt[key] + cc * c2) % p
            out.append({m: cc for m, cc in nt.items() if cc})
        eqs = out; eqs[i] = {}
        if v in nonzero:
            nonzero.discard(v)
        solved[v] = rhs
        tot = sum(len(t) for t in eqs)
        if nxt < len(CHECKPOINTS) and tot >= CHECKPOINTS[nxt]:
            rem = sorted(set(V) - zeros - set(solved))
            path = os.path.join(ROOT, f'wave6/pentseed/reduced_{len(rem)}v.ms')
            ne, nv = write_ms(path, eqs, rem, p, nonzero)
            sz = os.path.getsize(path) / 1e6
            print(f"  checkpoint: {ne} eq, {nv} vars, {tot} terms, {sz:.1f} MB -> {path}")
            done.append((len(rem), path, ne, nv))
            nxt += 1
        if nxt >= len(CHECKPOINTS):
            break

    rem = sorted(set(V) - zeros - set(solved))
    path = os.path.join(ROOT, f'wave6/pentseed/reduced_{len(rem)}v.ms')
    ne, nv = write_ms(path, eqs, rem, p, nonzero)
    print(f"  final: {ne} eq, {nv} vars, "
          f"{os.path.getsize(path)/1e6:.1f} MB -> {path}")
    done.append((len(rem), path, ne, nv))
    print("\nexports (fewest variables is best for Groebner, if msolve can ingest it):")
    for nv_, pth, ne_, nvv in done:
        print(f"  {nvv:4d} vars  {ne_:4d} eq  {os.path.getsize(pth)/1e6:8.1f} MB  {os.path.basename(pth)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
