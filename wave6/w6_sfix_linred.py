#!/usr/bin/env python3
"""Reduce the s-specialised trackB1 slice using its 21 GENUINELY LINEAR rows.

WHY THIS IS NOT THE FORCED CHAIN
--------------------------------
The forced chain reduced trackB1 by substituting high-degree expressions, and
it drove max degree 5 -> 19 and term count 8,774 -> 414,175. Every reduced
export it produced returned NO VERDICT, and the deepest one (240 MB) could not
even be loaded. Reduction by substitution is only free when the substituted
expression is LINEAR: substituting a linear form into a degree-d polynomial
leaves it degree d. Nothing can blow up.

Fixing s produces 21 such rows (they do not exist in the root -- they appear
only once the s-monomials are numeric). This script uses exactly those.

CHECKS (the campaign's errors were all caught in the artifact, never the
algorithm, so the artifact is what gets checked)
  1. every row used is asserted total-degree 1 before it is used;
  2. the reduced system is compared against the original at random points:
     assign the free variables at random, recover the eliminated ones from the
     linear relations, and require every ORIGINAL equation and its reduced
     counterpart to agree -- and both to vanish on the linear rows;
  3. the written file passes the symbol guard (no undeclared variable).
Degrees before and after are printed, so a blow-up cannot pass unnoticed.
"""
import sys, os, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import parse_poly, evalmono, rank_modp

SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')
SING = os.path.join(SCR, 'tb1_sfix.sing')


def fold(e, p):
    """collapse numeric literals with exponents (34562^2) left by substitution"""
    return re.sub(r'(?<![A-Za-z_0-9])(\d+)\^(\d+)',
                  lambda g: str(pow(int(g.group(1)), int(g.group(2)), p)), e)


def deg(mono):
    return sum(x for _, x in mono)


def render(poly):
    if not poly:
        return "0"
    out = []
    for m, c in sorted(poly.items()):
        fac = [f"{v}^{e}" if e > 1 else v for v, e in m]
        out.append(f"+{c}" + ("*" if fac else "") + "*".join(fac))
    return "".join(out).lstrip("+")


def main():
    txt = open(SING).read()
    mm = re.search(r'ring R = (\d+), \((.*?)\), dp;', txt, re.S)
    p = int(mm.group(1))
    V = [v.strip() for v in mm.group(2).split(',')]
    body = txt.split('ideal I = ', 1)[1].split(';', 1)[0]
    raw = [e.strip() for e in body.split(',\n') if e.strip()]
    polys = [parse_poly(fold(e, p), p) for e in raw]
    print(f"s-fixed slice: {len(V)} vars, {len(polys)} eqs, p={p}")

    lin_idx = [i for i, q in enumerate(polys) if max(map(deg, q), default=0) <= 1]
    print(f"  rows of total degree <= 1: {len(lin_idx)}")
    for i in lin_idx:                                   # CHECK 1
        assert max(map(deg, polys[i]), default=0) <= 1, f"row {i} is not linear"

    vidx = {v: j for j, v in enumerate(V)}
    n = len(V)
    rows = []
    for i in lin_idx:
        r = [0] * (n + 1)
        for m, c in polys[i].items():
            if not m:
                r[n] = (r[n] - c) % p          # constant to the RHS
            else:
                (v, e), = m
                r[vidx[v]] = (r[vidx[v]] + c) % p
        rows.append(r)

    # row reduce the linear subsystem to find pivots
    M = [r[:] for r in rows]
    piv = []
    rr = 0
    for c in range(n):
        pr = next((k for k in range(rr, len(M)) if M[k][c] % p), None)
        if pr is None:
            continue
        M[rr], M[pr] = M[pr], M[rr]
        inv = pow(M[rr][c], p - 2, p)
        M[rr] = [x * inv % p for x in M[rr]]
        for k in range(len(M)):
            if k != rr and M[k][c] % p:
                f = M[k][c]
                M[k] = [(a - f * b) % p for a, b in zip(M[k], M[rr])]
        piv.append((c, rr)); rr += 1
        if rr == len(M):
            break
    pivcols = {c for c, _ in piv}
    if rr < len(M):
        for k in range(rr, len(M)):
            if M[k][n] % p and not any(M[k][j] % p for j in range(n)):
                print("  linear rows are INCONSISTENT -> the slice is EMPTY outright")
                return 0
    free = [j for j in range(n) if j not in pivcols]
    print(f"  linear rank {len(piv)} -> eliminating {len(piv)} variables, "
          f"{len(free)} remain")

    # pivot variable  =  rhs - sum(coeff * free variable)
    solution = {}
    for c, r in piv:
        expr = {(): M[r][n] % p}
        for j in free:
            if M[r][j] % p:
                expr[((V[j], 1),)] = (-M[r][j]) % p
        solution[V[c]] = {k: v for k, v in expr.items() if v}

    def subst(poly):
        out = {}
        for m, c in poly.items():
            parts = [{(): c}]
            for v, e in m:
                for _ in range(e):
                    rep = solution.get(v, {((v, 1),): 1})
                    parts.append(rep)
            acc = {(): 1}
            for pt in parts:
                new = {}
                for m1, c1 in acc.items():
                    for m2, c2 in pt.items():
                        d = dict(m1)
                        for v2, e2 in m2:
                            d[v2] = d.get(v2, 0) + e2
                        k = tuple(sorted(d.items()))
                        new[k] = (new.get(k, 0) + c1 * c2) % p
                acc = {k: v for k, v in new.items() if v}
            for k, v in acc.items():
                out[k] = (out.get(k, 0) + v) % p
        return {k: v for k, v in out.items() if v}

    keep_idx = [i for i in range(len(polys)) if i not in set(lin_idx)]
    red = [subst(polys[i]) for i in keep_idx]
    red = [q for q in red if q]

    # CHECK 2: agreement with the ORIGINAL system at random points
    rng = random.Random(90210)
    freev = [V[j] for j in free]
    for trial in range(4):
        pt = {v: rng.randrange(0, p) for v in freev}
        full = dict(pt)
        for v, expr in solution.items():
            full[v] = sum(c * evalmono(m, pt, p) for m, c in expr.items()) % p
        for i in lin_idx:
            val = sum(c * evalmono(m, full, p) for m, c in polys[i].items()) % p
            assert val == 0, f"CHECK 2: linear row {i} does not vanish at the " \
                             f"recovered point (got {val})"
        for i, q in zip(keep_idx, [subst(polys[k]) for k in keep_idx]):
            a = sum(c * evalmono(m, full, p) for m, c in polys[i].items()) % p
            b = sum(c * evalmono(m, pt, p) for m, c in q.items()) % p
            assert a == b, f"CHECK 2: eq {i} original={a} reduced={b} -- " \
                           f"substitution changed the system"
    print(f"  CHECK 2: 4 random points, all {len(lin_idx)} linear rows vanish and "
          f"all {len(keep_idx)} remaining equations agree with the originals  [PASS]")

    d0 = max(max(map(deg, q), default=0) for q in polys)
    d1 = max(max(map(deg, q), default=0) for q in red)
    t0 = sum(len(q) for q in polys); t1 = sum(len(q) for q in red)
    print(f"  degree {d0} -> {d1}   terms {t0} -> {t1}   "
          f"vars {n} -> {len(freev)}   eqs {len(polys)} -> {len(red)}")
    if d1 > d0:
        print("  *** DEGREE ROSE. That is the forced-chain failure mode. Stopping.")
        return 1

    used = set()
    bodyout = []
    for q in red:
        bodyout.append(render(q))
    for tok in re.findall(r'[A-Za-z_]\w*', "\n".join(bodyout)):
        used.add(tok)
    leak = sorted(used - set(freev))
    assert not leak, f"REFUSING to write: undeclared {leak[:8]}"   # CHECK 3
    out = os.path.join(SCR, 'tb1_sfix_linred.sing')
    open(out, 'w').write(
        f'ring R = {p}, ({",".join(freev)}), dp;\nideal I = ' + ",\n".join(bodyout) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "LINRED RESULT UNIT -- slice EMPTY"; }\n'
        'else { "LINRED RESULT NOTUNIT -- slice NONEMPTY"; "dim:"; dim(G); '
        '"gbsize:"; size(G); }\nexit;\n')
    print(f"  wrote {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
