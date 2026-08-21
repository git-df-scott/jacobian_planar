#!/usr/bin/env python3
"""Iterated LINEAR elimination on the seed-pinned pentagon system, over F_p.

This is the sound part of the level cascade and nothing more.  It uses ONLY
equations of total degree 1 -- affine-linear with CONSTANT coefficients in F_p,
no free parameters, no division by anything symbolic -- so every step is exact
and reversible.  (Contrast w6_pent_levelcascade.py / w6_pent_cascade2.py, both
of which were retracted: see CATCHES.md.)

Loop: collect the degree-1 equations, row-reduce them mod p, substitute the
pivot variables into everything else, repeat until no degree-1 equation remains.

Verdicts it can legitimately produce:
  * an INCONSISTENT linear block, or a NONZERO CONSTANT appearing after
    substitution  ->  the seed is dead (sound, no caveats);
  * otherwise a strictly smaller system, reported with its size and degrees.
It can NOT prove the seed survives -- absence of a linear contradiction says
nothing about the nonlinear part.
"""
import sys, collections, sympy as sp
P = 1000003

def redp(e):
    """Reduce every coefficient mod P and DROP terms that vanish.

    Without this, sympy multiplies residues together without reducing, so
    coefficients grow without bound and some land on multiples of P.  msolve
    then refuses the file with 'coefficient cannot be 0 modulo P' -- the same
    failure mode recorded in CATCHES.md this morning.  Measured on the
    unreduced output: 3921 of 8264 coefficients had |c| >= P and 8 were exactly
    0 mod P."""
    e = sp.expand(e)
    gens = sorted(e.free_symbols, key=str)
    if not gens:
        return sp.Integer(int(e) % P)
    po = sp.Poly(e, *gens)
    out = 0
    for mon, co in zip(po.monoms(), po.coeffs()):
        c = int(co) % P
        if not c:
            continue
        t = c
        for g, ex in zip(gens, mon):
            if ex: t *= g**ex
        out += t
    return sp.expand(out)

def rref_mod(rows, ncol):
    rank = 0; piv = {}
    for j in range(ncol):
        pr = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pr is None: continue
        rows[rank], rows[pr] = rows[pr], rows[rank]
        inv = pow(rows[rank][j], P-2, P)
        rows[rank] = [(v*inv) % P for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][j]:
                f = rows[i][j]
                rows[i] = [(a - f*b) % P for a, b in zip(rows[i], rows[rank])]
        piv[j] = rank; rank += 1
    inc = [i for i in range(rank, len(rows))
           if all(v == 0 for v in rows[i][:-1]) and rows[i][-1] % P]
    return rows, piv, rank, inc

def main(path):
    lines = open(path).read().rstrip().rstrip(',').split('\n')
    hdr, char = lines[0], int(lines[1])
    body = [b.rstrip(',') for b in lines[2:] if b.strip()]
    eqs = [sp.sympify(b.replace('^', '**')) for b in body]
    print(f"start: {len(eqs)} equations / {len(hdr.split(','))} unknowns")
    rnd = 0
    while True:
        rnd += 1
        deg1 = [e for e in eqs if sp.total_degree(e) == 1]
        if not deg1:
            print(f"round {rnd}: no degree-1 equations left -- fixed point")
            break
        cols = sorted({v for e in deg1 for v in e.free_symbols}, key=str)
        rows = []
        for e in deg1:
            r = [0]*(len(cols)+1)
            p = sp.Poly(e, *cols)
            for mon, co in zip(p.monoms(), p.coeffs()):
                c = int(co) % P
                if sum(mon) == 0: r[-1] = (r[-1]+c) % P
                else: r[mon.index(1)] = (r[mon.index(1)]+c) % P
            rows.append(r)
        rows, piv, rank, inc = rref_mod(rows, len(cols))
        if inc:
            print(f"round {rnd}: LINEAR BLOCK INCONSISTENT ({len(inc)} rows) -> SEED DIES")
            return 'DEAD-LINEAR'
        sol = {}
        for j, r in piv.items():
            expr = (-rows[r][-1]) % P
            for k in range(len(cols)):
                if k != j and rows[r][k]: expr = expr - (rows[r][k] % P)*cols[k]
            sol[cols[j]] = sp.expand(expr)
        new = []; bad = 0; zero = 0
        for e in eqs:
            if sp.total_degree(e) == 1: continue
            v = sp.expand(e.subs(sol))
            if v == 0: zero += 1; continue
            if v.free_symbols == set():
                if int(v) % P: bad += 1
                else: zero += 1
                continue
            new.append(redp(v))
        unk = sorted({v for e in new for v in e.free_symbols}, key=str)
        print(f"round {rnd}: solved {rank}, free {len(cols)-rank} | "
              f"{len(new)} eqs / {len(unk)} unknowns | vanished {zero} | nonzero-const {bad} | "
              f"degs {dict(collections.Counter(sp.total_degree(e) for e in new))}")
        if bad:
            print(f"  *** NONZERO CONSTANT AFTER SUBSTITUTION -> SEED DIES ***")
            return 'DEAD-CONST'
        eqs = new
    unk = sorted({v for e in eqs for v in e.free_symbols}, key=str)
    print(f"\nreduced system: {len(eqs)} equations / {len(unk)} unknowns")
    print("degree profile:", dict(collections.Counter(sp.total_degree(e) for e in eqs)))
    out = path.replace('.ms', '_lin.ms')
    head = ",".join(str(u) for u in unk)+"\n"
    bodyo = ",\n".join(str(sp.Poly(e, *unk).as_expr()).replace('**','^').replace(' ','') for e in eqs)
    open(out, 'w').write(head+str(P)+"\n"+bodyo+"\n")
    print("written:", out)
    return 'REDUCED'

if __name__ == '__main__':
    print(main(sys.argv[1] if len(sys.argv) > 1
               else 'wave6/pentseed/seed0_p1000003.ms'))
