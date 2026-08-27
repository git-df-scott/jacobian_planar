#!/usr/bin/env python3
"""The linear cascade: decide the open subcase by rank, one weight at a time.

Structure established: with w = j - 2i the 92 bracket equations of
[P,Q] = x^2 split by weight as

    w=-4 : 17 eqs, 19 unknowns (the ESSENTIAL FACE -- solved, 35 solutions)
    w=-3 : 18 eqs, 19 new unknowns   LINEAR given deeper levels
    w=-2 : 19 eqs, 21 new unknowns   LINEAR
    w=-1 : 19 eqs, 13 new unknowns   LINEAR, overdetermined by 6
    w= 0 : 19 eqs, 0  new unknowns   pure consistency

So once the face is fixed everything else is linear algebra, and the case
is decided at w=-1 and w=0.

This runs the cascade MOD P at a random point of the face variety. That is
a SEARCH device, not a proof: it can show a face solution fails to extend,
and repeated failure across many face points is evidence of emptiness, but
only an exact characteristic-zero argument settles it. Any success is a
candidate that must be lifted and verified exactly.
"""
import json, random, sys
import sympy as sp
from face_param import lattice_points

p = 65521
x, y = sp.symbols("x y")
t = json.load(open("trackD_targets_108.json"))[1]
NP, NQ, r = t["NP"], t["NQ"], t["r"]
ptsP, ptsQ = lattice_points(NP), lattice_points(NQ)
w = lambda q: q[1]-2*q[0]
cP = {q: sp.Symbol(f"P{q[0]}_{q[1]}") for q in ptsP}
cQ = {q: sp.Symbol(f"Q{q[0]}_{q[1]}") for q in ptsQ}
P = sum(cP[q]*x**q[0]*y**q[1] for q in ptsP)
Q = sum(cQ[q]*x**q[0]*y**q[1] for q in ptsQ)
br = sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x) - x**r)
byw = {}
for mono, co in sp.Poly(br, x, y).terms():
    byw.setdefault(w(mono), []).append(sp.expand(co))

LP, LQ = {}, {}
for q in ptsP: LP.setdefault(w(q), []).append(q)
for q in ptsQ: LQ.setdefault(w(q), []).append(q)

def rank_modp(rows, ncol):
    M = [r[:] for r in rows]; rk = 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][c] % p), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], p-2, p)
        M[rk] = [v*inv % p for v in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] % p:
                f = M[i][c]
                M[i] = [(M[i][k]-f*M[rk][k]) % p for k in range(ncol+1)]
        rk += 1
        if rk == len(M): break
    return M, rk

def solve_level(lev, newvars, assign, rng):
    eqs = [sp.expand(e.subs(assign)) for e in byw.get(lev, [])]
    rows = []
    for e in eqs:
        pe = sp.Poly(e, *newvars) if newvars else None
        row = [int(pe.coeff_monomial(v)) % p if pe else 0 for v in newvars]
        const = int(sp.expand(e.subs({v:0 for v in newvars}))) % p
        rows.append(row + [(-const) % p])
    M, rk = rank_modp(rows, len(newvars))
    for i in range(rk, len(M)):
        if M[i][len(newvars)] % p:
            return None, rk, "INCONSISTENT"
    sol = {}
    piv = []
    for i in range(rk):
        c = next(j for j in range(len(newvars)) if M[i][j] % p)
        piv.append(c)
    free = [j for j in range(len(newvars)) if j not in piv]
    val = [0]*len(newvars)
    for j in free: val[j] = rng.randrange(p)
    for i in reversed(range(rk)):
        c = piv[i]
        val[c] = (M[i][len(newvars)] - sum(M[i][j]*val[j]
                  for j in range(c+1, len(newvars)))) % p
    for j, v in enumerate(newvars): sol[v] = val[j]
    return sol, rk, f"solved (rank {rk}, {len(free)} free)"

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = random.Random(seed)
    print(f"cascade mod {p}, seed {seed}")
    print("NOTE: the face level is seeded RANDOMLY here, so this tests")
    print("      whether a RANDOM point extends -- it does not yet use the")
    print("      35 true face solutions. Its value is to exercise the")
    print("      machinery and measure the ranks that decide the case.\n")
    assign = {}
    faceP = [cP[q] for q in LP[-2]]; faceQ = [cQ[q] for q in LQ[-3]]
    for v in faceP + faceQ: assign[v] = rng.randrange(1, p)
    for lev, newv in ((-3, [cP[q] for q in LP[-1]]+[cQ[q] for q in LQ[-2]]),
                      (-2, [cP[q] for q in LP[0]]+[cQ[q] for q in LQ[-1]]),
                      (-1, [cQ[q] for q in LQ[0]])):
        sol, rk, msg = solve_level(lev, newv, assign, rng)
        print(f"  w={lev}: {len(byw[lev])} eqs, {len(newv)} unknowns -> {msg}")
        if sol is None:
            print("  -> this face point does NOT extend"); sys.exit(0)
        assign.update(sol)
    res = [sp.expand(e.subs(assign)) % p for e in byw.get(0, [])]
    bad = [e for e in res if e % p != 0]
    print(f"  w= 0: {len(byw[0])} consistency conditions -> "
          f"{len(bad)} violated")
    print("\n  (a random face point is not expected to satisfy the face")
    print("   equation itself, so violations here are expected; the ranks")
    print("   above are the informative output.)")
