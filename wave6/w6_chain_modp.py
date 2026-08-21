#!/usr/bin/env python3
"""Forced chain over F_p on the SEED-PINNED pentagon system.  The live question.

WHY MOD P
---------
The chain over Q stalls on COEFFICIENT densification (8.6K -> 4.3M terms), not
on a fixed point: exact rational arithmetic makes every substitution grow the
numerators.  Mod p the coefficients are bounded by construction, so the same
chain runs much further on the same machine.

WHY THE SEED-PINNED SYSTEM
--------------------------
`wave6/pentseed/seed0_p1000003.ms` (267 eq / 148 unk) is the system that
decides the campaign's most promising open lead: does the single admissible
bottom-edge seed extend to a full solution?  Two Groebner runs on it produced
NO VERDICT (one 90-minute timeout, one OOM).  The forced chain is a tool the
campaign did not have when those runs were launched.

READING THE RESULT -- carefully
-------------------------------
A contradiction mod p is NOT a proof over Q.  This campaign proved that
"modular emptiness is unsound for contradictions" this morning, and that rule
applies here too.  But there is a real difference between an msolve EMPTY and
this: a forced chain produces a DERIVATION, a specific finite sequence of
implications ending in (nonzero) = 0.  That derivation names the obstruction,
and each step can then be re-checked in characteristic zero.  So:

  contradiction mod p -> a CANDIDATE obstruction with an explicit witness,
                         to be re-derived over Q before it is a verdict;
  large reduction     -> a smaller system for whatever comes next;
  fixed point, alive  -> the seed survives every forced consequence mod p.
"""
import re, sys, os
from collections import defaultdict

ROOT = '/home/user/jacobian_planar'
NONZERO = ['c_1_0', 'c_8_14', 'd_12_21', 's_4_8']


def parse_ms(path):
    L = open(path).read().split('\n')
    V = [v.strip() for v in L[0].split(',') if v.strip()]
    p = int(L[1].strip())
    body = "\n".join(L[2:])
    eqs = []
    for chunk in body.split(',\n'):
        chunk = chunk.strip().rstrip(',').strip()
        if not chunk:
            continue
        t = defaultdict(int)
        # split into signed terms
        for m in re.finditer(r'([+-]?)\s*([^+-]+)', chunk):
            sign, body_ = m.group(1), m.group(2).strip()
            if not body_:
                continue
            facs = body_.split('*')
            coef = 1
            mono = defaultdict(int)
            for f in facs:
                f = f.strip()
                if not f:
                    continue
                if re.fullmatch(r'\d+', f):
                    coef = coef * int(f) % p
                else:
                    mm = re.fullmatch(r'([A-Za-z_]\w*)(?:\^(\d+))?', f)
                    if not mm:
                        coef = coef * int(f) % p
                    else:
                        mono[mm.group(1)] += int(mm.group(2) or 1)
            if sign == '-':
                coef = (-coef) % p
            key = tuple(sorted(mono.items()))
            t[key] = (t[key] + coef) % p
        eqs.append({k: v for k, v in t.items() if v})
    return V, eqs, p


def gcd_mono(t):
    it = iter(t); g = dict(next(it))
    for m in it:
        dm = dict(m)
        for v in list(g):
            if v not in dm:
                del g[v]
            else:
                g[v] = min(g[v], dm[v])
        if not g:
            break
    return g


def run(path):
    V, eqs, p = parse_ms(path)
    nonzero = {v for v in NONZERO if v in V}
    print(f"{os.path.basename(path)}: {len(eqs)} equations, {len(V)} variables, p = {p}")
    print(f"nondegeneracy hypotheses present: {sorted(nonzero)}")
    print(f"initial term count: {sum(len(t) for t in eqs)}\n")
    zeros, solved = set(), {}

    for rnd in range(1, 3000):
        # substitute zeros
        eqs = [{m: c for m, c in t.items() if not any(v in zeros for v, _ in m)}
               for t in eqs]
        # divide out known-nonzero common factors
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
                    nt[tuple(sorted((v, e) for v, e in dm.items() if e > 0))] = c
                eqs[i] = nt; div += 1
        if div:
            continue
        # forced zeros / contradictions
        nz, contra = set(), None
        for i, t in enumerate(eqs):
            if len(t) != 1:
                continue
            (mono, coef), = t.items()
            if not mono:
                contra = f"eq{i}: nonzero constant {coef} = 0"; break
            free = [v for v, _ in mono if v not in nonzero]
            if not free:
                contra = f"eq{i}: {mono} = 0 with every factor required nonzero"; break
            if len(free) == 1 and free[0] not in zeros:
                nz.add(free[0])
        if contra or (nz & nonzero):
            what = contra or f"{sorted(nz & nonzero)} forced to zero but required nonzero"
            print(f"round {rnd}: *** CONTRADICTION mod p *** {what}")
            print(f"  after {len(zeros)} forced zeros and {len(solved)} pivots")
            print("\n  CANDIDATE obstruction. NOT a verdict: modular contradictions are")
            print("  unsound for this campaign, so it must be re-derived over Q.")
            return 2
        if nz:
            zeros |= nz
            print(f"round {rnd}: forced to zero ({len(zeros)} total): {sorted(nz)[:6]}")
            continue
        # polynomial pivots
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
            print(f"round {rnd}: FIXED POINT")
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
                dm = dict(m)
                if dm.get(v, 0) != 1:
                    nt[m] = (nt[m] + cc) % p
                    continue
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
        if rnd % 20 == 0 or len(solved) < 5:
            print(f"round {rnd}: pivot {v} ({len(rhs)} terms), "
                  f"{len(solved)} eliminated, total terms {tot}")
        if tot > 2500000:
            print(f"round {rnd}: STOPPING -- {tot} terms")
            break

    live = [t for t in eqs if t]
    rem = len(V) - len(zeros) - len(solved)
    print(f"\nRESULT: {len(live)} equations, {rem} variables "
          f"({len(zeros)} zeros, {len(solved)} pivots)")
    print(f"  overdetermined by {len(live) - rem}")
    print(f"  seed survives every forced consequence mod p -- NOT a proof it extends")
    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1
                 else os.path.join(ROOT, 'wave6/pentseed/seed0_p1000003.ms')))
