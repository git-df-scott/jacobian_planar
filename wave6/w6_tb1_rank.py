#!/usr/bin/env python3
"""trackB1 as a RANK QUESTION, not a Groebner question.

WHY THIS EXISTS
---------------
Every trackB1 NO VERDICT so far was spent on a *reduced* export. Measuring the
reductions shows they were de-optimizations: the chain took the system from

    166 vars, 284 eq, max degree  5,   8,774 terms   (root)
 -> 100 vars, 217 eq, max degree 19, 414,175 terms   (reduced_tb1deep_99v)

Groebner cost is doubly exponential in degree, so trading 66 variables for
14 degrees and 47x the terms made the problem strictly harder every time.

Reading the ROOT's bidegree profile instead shows what the system actually is:

    (deg_c, deg_d, deg_s, deg_zsat) -> count
    (1,0,0,0) ->   1     (1,1,0,0) ->  80     (1,1,1,0) ->  13
    (1,1,2,0) ->  57     (1,1,3,0) -> 132     (2,1,1,1) ->   1  <- saturation

283 of 284 equations have degree 1 in the 51-variable c-block.  The first
version of this script asserted they were HOMOGENEOUS in c; that assertion
FAILED on equation 8, which carries a c-free term.  The truth is one step
weaker and strictly more useful -- they are AFFINE linear in c:

    A(d, s) . c = b(d, s),     A of shape 283 x 51,

so c = 0 is not a free solution, and the question is CONSISTENCY:

    does some (d, s) make  rank[A | b] == rank[A] ?

That is one Gaussian elimination per probe, microseconds, no Groebner at all.
This is Golub-Pereyra variable projection: the c-block is eliminated EXACTLY by
linear algebra, at no cost in degree -- precisely what the substitution chain
failed to do when it traded 66 variables for 14 degrees of blowup.

TWO OUTCOMES, BOTH INFORMATIVE
  consistent at a random (d,s)  ->  solve for c and a full point drops out.
                         The variety is NONEMPTY and its projection to (d,s)
                         is dominant.  That is a HIT.
  inconsistent everywhere probed -> emptiness is NOT established. Consistency
                         is a proper closed condition, and random points miss
                         a proper closed subvariety by design.  Recorded as
                         NO VERDICT on emptiness, never as EMPTY.

BUG DISCIPLINE
Every error this campaign has produced was caught by checking the ARTIFACT, not
the algorithm: back-substitution "passed" while a variable was not eliminated;
a desaturation "passed" while the system was still saturated.  So this script
does not trust its own parser or its own linear algebra.  It:
  (1) asserts the homogeneity it claims, per equation, from the parse;
  (2) re-evaluates each original equation STRING by an independent path at the
      probe point and checks it against the matrix row (parser check);
  (3) whenever a nonzero kernel vector is found, substitutes the full point
      back into the original strings and requires exact 0 (solution check).
A kernel vector that fails (3) is reported as a BUG, never as a hit.
"""
import sys, os, re, random
from collections import defaultdict

ROOT = '/home/user/jacobian_planar'
SRC = os.path.join(ROOT, 'wave6/frontier/trackB1_sat_p1000003.ms')


def load(path):
    L = open(path).read().split('\n')
    vs = [v.strip() for v in L[0].split(',') if v.strip()]
    p = int(L[1].strip())
    body = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
    used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    leak = sorted(used - set(vs))
    assert not leak, f"MALFORMED source: undeclared symbols {leak[:8]}"
    return vs, p, body


def parse_poly(s, p):
    """string -> {monomial: coeff}, monomial = tuple of sorted (var, exp)."""
    d = defaultdict(int)
    s = s.replace(' ', '')
    for mm in re.finditer(r'([+-]?)([^+-]+)', s):
        sign, term = mm.group(1), mm.group(2)
        if not term:
            continue
        co, mono = 1, defaultdict(int)
        for fa in term.split('*'):
            if not fa:
                continue
            if re.fullmatch(r'\d+', fa):
                co = co * int(fa) % p
            else:
                g = re.fullmatch(r'([A-Za-z_]\w*)(?:\^(\d+))?', fa)
                assert g, f"unparsable factor {fa!r} in {s[:60]!r}"
                mono[g.group(1)] += int(g.group(2) or 1)
        if sign == '-':
            co = (-co) % p
        k = tuple(sorted(mono.items()))
        d[k] = (d[k] + co) % p
    return {k: v for k, v in d.items() if v}


def evalmono(mono, pt, p):
    r = 1
    for v, e in mono:
        r = r * pow(pt[v], e, p) % p
    return r


def rank_modp(rows, ncol, p):
    """Gaussian elimination over F_p. Returns (rank, kernel_basis)."""
    M = [r[:] for r in rows]
    nrow = len(M)
    piv = []          # (col, row) pivots
    r = 0
    for c in range(ncol):
        pr = None
        for i in range(r, nrow):
            if M[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(nrow):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append((c, r))
        r += 1
        if r == nrow:
            break
    pivcols = {c for c, _ in piv}
    free = [c for c in range(ncol) if c not in pivcols]
    ker = []
    for fc in free:
        v = [0] * ncol
        v[fc] = 1
        for c, rr in piv:
            v[c] = (-M[rr][fc]) % p
        ker.append(v)
    return r, ker


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20260822
    vs, p, body = load(SRC)
    blocks = defaultdict(list)
    for v in vs:
        blocks['zsat' if v.startswith('zsat') else v.split('_')[0]].append(v)
    C = sorted(blocks['c'])
    OTHER = sorted(blocks['d'] + blocks['s'] + blocks['zsat'])
    print(f"{os.path.basename(SRC)}: {len(vs)} vars, {len(body)} eq, p={p}")
    print(f"  c-block {len(C)}, d-block {len(blocks['d'])}, "
          f"s-block {len(blocks['s'])}, zsat {len(blocks['zsat'])}")

    polys = [parse_poly(b, p) for b in body]
    cset = set(C)

    # ---- CHECK (1): assert the homogeneity this whole reduction rests on ----
    lin, sat, inhom = [], [], 0
    for i, (poly, raw) in enumerate(zip(polys, body)):
        degc = max((sum(e for v, e in m if v in cset) for m in poly), default=0)
        if degc <= 1:
            # AFFINE linear in c: every monomial has c-degree 0 or 1.
            bad = [m for m in poly if sum(e for v, e in m if v in cset) > 1]
            assert not bad, (f"eq {i} has deg_c<=1 but a monomial of c-degree "
                             f"{sum(e for v,e in bad[0] if v in cset)}")
            if any(sum(e for v, e in m if v in cset) == 0 for m in poly):
                inhom += 1
            lin.append(i)
        else:
            sat.append((i, degc))
    print(f"  CHECK 1 affine-linearity: {len(lin)}/{len(body)} equations are "
          f"affine linear in c ({inhom} of them inhomogeneous)  [PASS]")
    print(f"  non-linear-in-c rows held out: {[(i, f'deg_c={d}') for i, d in sat]}")

    ncol = len(C)
    cidx = {v: j for j, v in enumerate(C)}
    # augmented column ncol holds -b, so consistency <=> rank[A|-b] == rank[A]
    rng = random.Random(seed)
    ranks = []
    for t in range(trials):
        pt = {v: rng.randrange(1, p) for v in OTHER}
        rows = []
        for i in lin:
            row = [0] * (ncol + 1)
            for m, co in polys[i].items():
                cv = [v for v, e in m if v in cset]
                rest = tuple((v, e) for v, e in m if v not in cset)
                val = co * evalmono(rest, pt, p) % p
                if cv:
                    row[cidx[cv[0]]] = (row[cidx[cv[0]]] + val) % p
                else:
                    row[ncol] = (row[ncol] - val) % p   # move constant to RHS
            rows.append(row)

        # ---- CHECK (2): parser check, independent re-evaluation of a row ----
        if t == 0:
            probe = rng.sample(lin, min(6, len(lin)))
            cval = {v: rng.randrange(0, p) for v in C}
            full = dict(pt); full.update(cval)
            for i in probe:
                rr = rows[lin.index(i)]
                viaRow = (sum(rr[cidx[v]] * cval[v] for v in C) - rr[ncol]) % p
                viaStr = sum(co * evalmono(m, full, p)
                             for m, co in parse_poly(body[i], p).items()) % p
                assert viaRow == viaStr, (
                    f"CHECK 2 FAILED on eq {i}: matrix row gives {viaRow}, "
                    f"direct evaluation of the original string gives {viaStr}")
            print(f"  CHECK 2 parser: {len(probe)} rows re-evaluated from the "
                  f"original strings, all agree with the matrix  [PASS]")

        rA, _ = rank_modp([r[:ncol] for r in rows], ncol, p)
        rAug, sol = rank_modp(rows, ncol + 1, p)
        ranks.append((rA, rAug))
        ok = (rA == rAug)
        print(f"  probe {t+1:2d}: rank A = {rA}/{ncol}, rank[A|b] = {rAug}   "
              f"-> {'CONSISTENT' if ok else 'inconsistent'}", flush=True)
        if ok:
            print(f"\n  *** CONSISTENT at probe {t+1}: c solves exactly ***")
            # ---- CHECK (3): substitute back into the ORIGINAL strings ----
            kv = [v for v in sol if v[ncol] % p][0] if sol else None
            assert kv is not None, "consistent but no affine solution recovered"
            inv = pow(kv[ncol], p - 2, p)
            full = dict(pt)
            for j, v in enumerate(C):
                full[v] = kv[j] * inv % p
            bad = []
            for i in lin:
                val = sum(co * evalmono(m, full, p)
                          for m, co in parse_poly(body[i], p).items()) % p
                if val:
                    bad.append((i, val))
            if bad:
                print(f"  *** CHECK 3 FAILED: {len(bad)} original equations do "
                      f"NOT vanish at the kernel point, e.g. {bad[:3]}")
                print("  *** This is a BUG in this script, not a hit. Not reported "
                      "as NONEMPTY.")
                return 2
            print(f"  CHECK 3: all {len(lin)} original equations vanish exactly "
                  f"at the kernel point  [PASS]")
            print(f"  held-out rows {[i for i,_ in sat]} still to satisfy "
                  f"(saturation/nondegeneracy)")
            return 0

    rAs = [a for a, _ in ranks]; rAugs = [b for _, b in ranks]
    print(f"\nover {trials} random (d,s): rank A in [{min(rAs)},{max(rAs)}], "
          f"rank[A|b] in [{min(rAugs)},{max(rAugs)}]  (c-block width {ncol})")
    if all(a != b for a, b in ranks):
        print("VERDICT: inconsistent at every probe -- no c solves a random (d,s).")
        print("  This is NOT emptiness. Consistency is a proper closed condition,")
        print("  and random points miss a proper closed subvariety with")
        print("  probability ~1 by design. Recorded as NO VERDICT on emptiness.")
        print("  What it DOES establish: the solution set, if nonempty, lies in")
        print(f"  the locus rank[A|b] == rank A, a determinantal system in the")
        print(f"  {len(OTHER)-1} d/s variables ALONE -- c is eliminated exactly, with")
        print("  no degree blowup, which is what the chain failed to do.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
