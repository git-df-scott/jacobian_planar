#!/usr/bin/env python3
"""Forced-vertex oracle: the saturated question as a rank test.

The 66 conditions are exactly affine in the 13 late variables, and p_16_8 is one
of them.  Rather than solving for late and hoping p_16_8 comes out nonzero
(it is 0 on every known family), FORCE p_16_8 = 1 and ask whether the remaining
12-variable affine system is consistent:

    M . late + v = 0,  late = (late', p_16_8=1)
    =>  M' . late'  =  -(v + m)        m = the p_16_8 column

Consistent  <=>  rank(M') == rank([M' | -(v+m)]).  Milliseconds per point.
A consistent early point is a genuine solution with p_16_8 != 0 -- i.e. a
counterexample CANDIDATE, subject to the full six-vertex test.
"""
import sys, random
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, EARLY, LATE, p
from oracle import build, rref

K = LATE.index("p_16_8")
OTHER = [i for i in range(len(LATE)) if i != K]

def forced_consistent(early, val=1):
    M, v = build(early)
    m = [M[r][K] for r in range(66)]
    Mp = [[M[r][c] for c in OTHER] for r in range(66)]
    rhs = [(-(v[r] + val*m[r])) % p for r in range(66)]
    n = len(OTHER)
    _, pM = rref([row[:] for row in Mp], n)
    aug = [Mp[r][:] + [rhs[r]] for r in range(66)]
    rA, pA = rref(aug, n + 1)
    ok = (n not in pA)
    sol = None
    if ok:
        sol = [0]*n
        for i, c in enumerate(pA):
            if c < n: sol[c] = rA[i][n]
    return len(pM), len(pA), ok, sol

def full_late(sol, val=1):
    out = [0]*len(LATE)
    for i, c in enumerate(OTHER): out[c] = sol[i]
    out[K] = val
    return out

def verify(early, late):
    d = dict(early)
    for i, nm in enumerate(LATE): d[nm] = late[i]
    return conditions(d)

def controls():
    """POS: build an early point whose forced system IS consistent by construction,
    by planting the right-hand side.  NEG: perturb it off the column space."""
    rnd = random.Random(2)
    early = {v: rnd.randrange(p) for v in EARLY}
    M, v = build(early)
    m = [M[r][K] for r in range(66)]
    Mp = [[M[r][c] for c in OTHER] for r in range(66)]
    lp = [rnd.randrange(p) for _ in OTHER]
    rhs = [(-sum(Mp[r][c]*lp[c] for c in range(len(OTHER)))) % p for r in range(66)]
    n = len(OTHER)
    _, pM = rref([row[:] for row in Mp], n)
    aug = [Mp[r][:] + [rhs[r]] for r in range(66)]
    rA, pA = rref(aug, n+1)
    pos = (n not in pA)
    aug2 = [Mp[r][:] + [(rhs[r] + (1 if r == 0 else 0)) % p] for r in range(66)]
    _, pA2 = rref(aug2, n+1)
    neg = (n in pA2)
    return pos, neg, len(pM)

if __name__ == "__main__":
    pos, neg, rk = controls()
    print(f"CONTROL POS (planted rhs consistent): {'PASS' if pos else 'FAIL'}   rank(M')={rk}")
    print(f"CONTROL NEG (perturbed rhs inconsistent): {'PASS' if neg else 'FAIL'}")
    inv3 = pow(3, p-2, p)
    print("\nforced p_16_8 = 1 at points of the known families (all have p_16_8 = 0,")
    print("so these MUST come back inconsistent -- a real-data negative control):")
    rnd = random.Random(9)
    for tag, mk in [("family A", lambda: {**{v:0 for v in EARLY}, "p_1_0":1,
                       "p_2_0":rnd.randrange(p), "p_3_0":rnd.randrange(p),
                       "p_4_0":rnd.randrange(p), "p_5_0":rnd.randrange(p)}),
                    ("family B lam=1", lambda: {**{v:0 for v in EARLY}, "p_1_0":1,
                       "p_1_1":1, "p_2_0":1, "p_3_0":inv3})]:
        e = mk()
        rm, ra, ok, _ = forced_consistent(e)
        print(f"   {tag}: rank {rm}/{ra} consistent={ok}")
    print("\ngeneric early points, p_16_8 forced to 1:")
    for t in range(5):
        e = {v: rnd.randrange(p) for v in EARLY}
        rm, ra, ok, _ = forced_consistent(e)
        print(f"   trial {t}: rank {rm}/{ra} consistent={ok}")
