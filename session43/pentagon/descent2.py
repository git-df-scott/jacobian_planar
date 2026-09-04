#!/usr/bin/env python3
"""Edge descent, rungs 18 -> 12, done by NUMERIC rank detection at random points.

Method.  Symbolic minor enumeration is too slow past rung 16 (405 dense 8x8
determinants in ~15 symbols).  Instead: specialise the free A-coefficients to
random rationals, at which point every rung is a rational linear system and
rank(Mat) vs rank([Mat|vec]) is instant.  A hypothesis H (a condition on the
A_i) is CONFIRMED at rung d if imposing H makes the rung consistent at many
independent random points, and REFUTED if it does not.  The confirmed condition
is then re-derived symbolically with only the relevant A_i left as symbols.

CRITICAL (lesson A3/A14).  Where a rung's Mat is column-rank-deficient the
solution carries a free constant of integration.  That constant is kept as a
SYMBOL and carried into the next rung.  Choosing it greedily is exactly what
manufactured the false obstruction retracted in A3.

Gauge.  r = 1: the y-scaling y -> lambda y is a torus action preserving every
monomial support, and pentev's gauges (p_0_0 = 0, p_0_1 = 1) involve x only.
alpha, beta are left as random nonzero rationals, not gauged.
"""
import sympy as sp, random
from itertools import combinations
y = sp.symbols('y'); M, N = 8, 12
r = sp.Integer(1)

def rung_edge(d, A, B):
    s = 0
    for i in range(1, M+1):
        k = d+1-i
        if 2 <= k <= N and i in A and k in B:
            s += (2*k-3*i)*A[i]*B[k] + y*(i*A[i]*sp.diff(B[k],y) - k*sp.diff(A[i],y)*B[k])
    return sp.expand(s)

def gen(name, deg):
    c = [sp.Symbol(f'{name}{i}') for i in range(deg+1)]
    return sum(c[i]*y**i for i in range(deg+1)), c

def build(seed, zero_at_r):
    """A_i with random rational coeffs; A_i(1)=0 imposed for i in zero_at_r."""
    rnd = random.Random(seed)
    R = lambda: sp.Integer(rnd.randrange(1, 60))
    al, be = R(), R()
    A = {8: al*(y-r)**2}
    B = {12: be*(y-r)**3}
    for i in range(1, 8):
        deg = 10 - i
        cs = [R() for _ in range(deg+1)]
        Ai = sum(cs[j]*y**j for j in range(deg+1))
        if i in zero_at_r:
            Ai = sp.expand(Ai - Ai.subs(y, r))       # force A_i(1) = 0
        A[i] = sp.expand(Ai)
    if 7 not in zero_at_r:
        raise SystemExit("rung 17 already forces A_7(r)=0")
    B[11] = sp.expand(sp.Rational(3,2)*be/al*(y-r)*A[7])
    assert sp.expand(rung_edge(18, A, B)) == 0, "rung 18 identity failed"
    return A, B

def descend(A, B, dmax=18, dmin=12, verbose=False):
    """Returns dict d -> (consistent?, n_eqs, n_unk, rank, kerdim)."""
    out = {}
    free = []
    for d in range(dmax-1, dmin-1, -1):      # 17..12  (18 already used)
        k = d+1-M
        Bk, cB = gen(f'b{k}_', 15-k)
        expr = rung_edge(d, A, {**B, k: Bk})
        eqs = sp.Poly(expr, y).all_coeffs()
        unk = cB + free
        Mat, vec = sp.linear_eq_to_matrix(eqs, unk)
        rM = Mat.rank(); rA = Mat.row_join(vec).rank()
        ok = (rM == rA)
        out[d] = (ok, Mat.shape[0], len(unk), rM)
        if not ok:
            if verbose: print(f"   rung {d}: INCONSISTENT ({Mat.shape[0]}x{len(unk)}, rank {rM})")
            return out
        sol = sp.solve(eqs, cB, dict=True)
        if not sol:
            out[d] = (False, Mat.shape[0], len(unk), rM); return out
        s = sol[0]
        Bk = sp.expand(Bk.subs(s))
        newfree = sorted(set(Bk.free_symbols) & set(cB), key=str)   # kept SYMBOLIC
        free += newfree
        B[k] = Bk
        if verbose:
            print(f"   rung {d}: consistent, {Mat.shape[0]} eqs, {len(unk)} unk, "
                  f"rank {rM}, free consts carried: {newfree}")
    return out

print("=== hypothesis test at rung 15 (and below) ===")
HYP = {
    "H0 none (control, expect FAIL)":        {7},
    "H1 A_6(r)=0":                           {7,6},
    "H2 A_5(r)=0":                           {7,5},
    "H3 A_6(r)=A_5(r)=0":                    {7,6,5},
    "H4 A_i(r)=0 for i=1..7":                {7,6,5,4,3,2,1},
}
for name, Z in HYP.items():
    res = []
    for seed in (1, 2, 3):
        A, B = build(seed, Z)
        out = descend(A, B, verbose=False)
        lowest = min(out) if out else None
        bad = [d for d in out if not out[d][0]]
        res.append(min(bad) if bad else "12 (all consistent)")
    print(f"  {name:32s} -> first inconsistent rung, 3 seeds: {res}")
