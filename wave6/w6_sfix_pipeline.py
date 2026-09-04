#!/usr/bin/env python3
"""s-slice pipeline for trackB1: fix s at a seed, linearly reduce, emit Singular.

Usage:  python3 wave6/w6_sfix_pipeline.py SEED [OUTTAG]

WHY SEVERAL SEEDS
One s-value returning EMPTY says nothing about trackB1 -- it is a statement
about a single point of the 4-dimensional s-space. Several independent s all
returning EMPTY is evidence that the GENERIC s-slice is empty, which would
confine any solution over a proper closed subset of that 4-space. Four
dimensions is small enough to then attack directly, which is the only route
here that ends in an actual verdict rather than another wall.

A NONEMPTY at any seed is a genuine point and outranks everything else.

Reuses the checked reduction in w6_sfix_linred.py: linear rows only (so no
degree can rise), rank computed rather than row-count assumed, and equivalence
against the ORIGINAL equations verified at random points before anything is
written.
"""
import sys, os, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import parse_poly, evalmono

R = '/home/user/jacobian_planar/'
SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')
SRC = R + 'campaign/audit_tracks/trackB1_case1_full_p65521.ms'
FORCED_NONZERO = {'c_1_0', 'c_8_14', 'd_12_21', 's_4_8'}


def deg(m): return sum(x for _, x in m)


def render(poly):
    if not poly: return "0"
    out = []
    for m, c in sorted(poly.items()):
        fac = [f"{v}^{e}" if e > 1 else v for v, e in m]
        out.append(f"+{c}" + ("*" if fac else "") + "*".join(fac))
    return "".join(out).lstrip("+")


def main():
    seed = int(sys.argv[1]); tag = sys.argv[2] if len(sys.argv) > 2 else f's{seed}'
    L = open(SRC).read().split('\n')
    V = [v.strip() for v in L[0].split(',') if v.strip()]
    p = int(L[1])
    raw = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
    S = [v for v in V if v.startswith('s_')]
    rng = random.Random(seed)
    sval = {v: rng.randrange(1, p) for v in S}   # s_4_8 nonzero: saturation needs it
    keep = [v for v in V if v not in set(S)]
    polys = []
    for e in raw:
        q = parse_poly(e, p)
        out = {}
        for m, c in q.items():
            coef = c; rest = []
            for v, ex in m:
                if v in sval: coef = coef * pow(sval[v], ex, p) % p
                else: rest.append((v, ex))
            if coef % p:
                k = tuple(sorted(rest))
                out[k] = (out.get(k, 0) + coef) % p
        polys.append({k: v for k, v in out.items() if v})
    print(f"seed {seed}: s = {sval}")
    print(f"  after s-substitution: {len(keep)} vars, {len(polys)} eqs, "
          f"max degree {max(max(map(deg,q),default=0) for q in polys)}, "
          f"{sum(len(q) for q in polys)} terms")

    lin_idx = [i for i, q in enumerate(polys) if max(map(deg, q), default=0) <= 1]
    vidx = {v: j for j, v in enumerate(keep)}; n = len(keep)
    rows = []
    for i in lin_idx:
        r = [0]*(n+1)
        for m, c in polys[i].items():
            if not m: r[n] = (r[n]-c) % p
            else:
                (v, e), = m; r[vidx[v]] = (r[vidx[v]]+c) % p
        rows.append(r)
    M = [r[:] for r in rows]; piv = []; rr = 0
    for c in range(n):
        pr = next((k for k in range(rr, len(M)) if M[k][c] % p), None)
        if pr is None: continue
        M[rr], M[pr] = M[pr], M[rr]
        inv = pow(M[rr][c], p-2, p); M[rr] = [x*inv % p for x in M[rr]]
        for k in range(len(M)):
            if k != rr and M[k][c] % p:
                f = M[k][c]; M[k] = [(a-f*b) % p for a, b in zip(M[k], M[rr])]
        piv.append((c, rr)); rr += 1
        if rr == len(M): break
    for k in range(rr, len(M)):
        if M[k][n] % p and not any(M[k][j] % p for j in range(n)):
            print("  linear rows INCONSISTENT -> this slice is EMPTY outright"); return 0
    pivcols = {c for c, _ in piv}
    free = [j for j in range(n) if j not in pivcols]
    print(f"  {len(lin_idx)} linear rows, rank {len(piv)} -> eliminate {len(piv)}, "
          f"{len(free)} remain")
    solution = {}
    for c, r in piv:
        expr = {(): M[r][n] % p}
        for j in free:
            if M[r][j] % p: expr[((keep[j], 1),)] = (-M[r][j]) % p
        solution[keep[c]] = {k: v for k, v in expr.items() if v}

    def subst(poly):
        out = {}
        for m, c in poly.items():
            acc = {(): c}
            for v, e in m:
                for _ in range(e):
                    rep = solution.get(v, {((v, 1),): 1})
                    new = {}
                    for m1, c1 in acc.items():
                        for m2, c2 in rep.items():
                            d = dict(m1)
                            for v2, e2 in m2: d[v2] = d.get(v2, 0)+e2
                            k = tuple(sorted(d.items()))
                            new[k] = (new.get(k, 0)+c1*c2) % p
                    acc = {k: v for k, v in new.items() if v}
            for k, v in acc.items(): out[k] = (out.get(k, 0)+v) % p
        return {k: v for k, v in out.items() if v}

    keep_idx = [i for i in range(len(polys)) if i not in set(lin_idx)]
    red = [subst(polys[i]) for i in keep_idx]
    freev = [keep[j] for j in free]
    rng2 = random.Random(seed ^ 0x5eed)
    for _ in range(3):
        pt = {v: rng2.randrange(0, p) for v in freev}
        full = dict(pt)
        for v, expr in solution.items():
            full[v] = sum(c*evalmono(m, pt, p) for m, c in expr.items()) % p
        for i in lin_idx:
            assert sum(c*evalmono(m, full, p) for m, c in polys[i].items()) % p == 0, \
                f"linear row {i} does not vanish"
        for i, q in zip(keep_idx, red):
            a = sum(c*evalmono(m, full, p) for m, c in polys[i].items()) % p
            b = sum(c*evalmono(m, pt, p) for m, c in q.items()) % p
            assert a == b, f"eq {i}: original {a} != reduced {b}"
    print(f"  CHECK: 3 random points, {len(lin_idx)} linear rows vanish, "
          f"{len(keep_idx)} equations agree with originals  [PASS]")
    red = [q for q in red if q]
    d1 = max(max(map(deg, q), default=0) for q in red)
    print(f"  reduced: {len(freev)} vars, {len(red)} eqs, degree {d1}, "
          f"{sum(len(q) for q in red)} terms")
    body = [render(q) for q in red]
    used = set(re.findall(r'[A-Za-z_]\w*', "\n".join(body)))
    leak = sorted(used - set(freev))
    assert not leak, f"REFUSING to write: undeclared {leak[:8]}"
    out = f'{SCR}/tb1_{tag}.sing'
    open(out, 'w').write(
        f'ring R = {p}, ({",".join(freev)}), dp;\nideal I = ' + ",\n".join(body) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        f'if (size(G)==1 && G[1]==1) {{ "{tag.upper()} RESULT UNIT -- slice EMPTY"; }}\n'
        f'else {{ "{tag.upper()} RESULT NOTUNIT -- slice NONEMPTY"; "dim:"; dim(G); '
        '"gbsize:"; size(G); }\nexit;\n')
    print(f"  wrote {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
