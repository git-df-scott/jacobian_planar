#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 1 -- INDEPENDENT re-derivation of the pentagon
y-adic Jacobian rank.  Simultaneously audit item A2.9.

WHY IT MATTERS.  The only thing standing between the (72,108) pentagons and
"completely unknown" is the recorded evidence  rank 60 of 61  =>  dim <= 1.
If the true rank is 59, the bound is dim <= 2 and the recorded evidence is
wrong.  Plan 43 flags this as the single number the pentagon story rests on,
and it has never been recomputed.

INDEPENDENCE.  Nothing is imported from the campaign.  The Newton polygons, the
bracket expansion, the y-adic recursion, the condition set, the dual-number
differentiation and the rank are all rebuilt here from the mathematics:

    P = sum_j P_j(x) y^j,  Q = sum_j Q_j(x) y^j,  [P,Q] = P_x Q_y - P_y Q_x = x^2

    coeff of y^k :  sum_{a+b=k+1} ( b P_a' Q_b  -  a P_a Q_b' ) = x^2 * delta_{k,0}

    N(Q)'s j=0 row is the single point (0,0), so Q_0 is constant and Q_0' = 0.
    k = 0  gives  P_0' Q_1 = x^2, i.e. p_10 Q_1 = x^2.
    k >= 1 gives  (k+1) p_10 Q_{k+1} = sum_{a=1..k} ( a P_a Q_{k+1-a}'
                                                    - (k+1-a) P_a' Q_{k+1-a} )
    so Q is a FUNCTION of P.

CONDITIONS.  N(Q) requires, for 13 <= j <= 24, that the coefficient of x^i in
Q_j vanish for every i < j - 12; and Q_j = 0 for j > 24.

The Jacobian of those conditions with respect to P's 61 lattice coefficients is
computed by DUAL NUMBERS (a finite difference over F_p is a secant, not a
derivative -- the campaign is right about that), one parameter at a time, and
its rank is taken by Gaussian elimination over F_p.  Run at several random
points and at two primes = 1 (mod 3), including one the campaign never used.
"""
import random, sys
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

# ---------------- polygons, rebuilt from the lower-edge inequalities ---------
def P_rows(jmax=16):
    """N(P): lower edges j >= 0 and j >= 2(i-1); upper cut i <= 8."""
    r = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 8), min(8, j // 2 + 1)
        if lo <= hi: r[j] = (lo, hi)
    return r
def Q_rows(jmax=24):
    """N(Q): lower edges i <= 2j and j >= 2i-3; upper cut i <= 12."""
    r = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 12), min(12, 2 * j, (j + 3) // 2)
        if lo <= hi: r[j] = (lo, hi)
    return r

PR, QR = P_rows(), Q_rows()
PARAMS = [(j, i) for j in sorted(PR) for i in range(PR[j][0], PR[j][1] + 1)]
print("="*78); print("H1b step 1 -- INDEPENDENT y-adic Jacobian rank, (72,108) pentagons")
print("="*78)
check("N(P) has 61 lattice points (independent polygon rebuild)",
      len(PARAMS) == 61, "PROVED-exact", f"{len(PARAMS)} points, j = 0..16")
check("N(Q)'s j=0 row is the single point (0,0), so Q_0 is a constant",
      QR[0] == (0, 0), "PROVED-exact", "this is what makes the recursion solvable")

# ---------------- dual-number arithmetic over F_p ---------------------------
def run(p, Pvals, dpar=None):
    """y-adic recursion mod p.  Coefficients are pairs (value, derivative)
    when dpar is a parameter index, else plain values with derivative 0.
    Returns the list of Q_j as dual-number coefficient lists."""
    def mul(a, b):
        if not a or not b: return []
        o = [(0, 0)] * (len(a) + len(b) - 1)
        for i, (xv, xd) in enumerate(a):
            if xv or xd:
                for j, (yv, yd) in enumerate(b):
                    if yv or yd:
                        ov, od = o[i + j]
                        o[i + j] = ((ov + xv * yv) % p, (od + xv * yd + xd * yv) % p)
        return trim(o)
    def add(a, b):
        n = max(len(a), len(b))
        return trim([(((a[i][0] if i < len(a) else 0) + (b[i][0] if i < len(b) else 0)) % p,
                      ((a[i][1] if i < len(a) else 0) + (b[i][1] if i < len(b) else 0)) % p)
                     for i in range(n)])
    def scal(a, c):
        c %= p
        return trim([(v * c % p, d * c % p) for v, d in a]) if c else []
    def trim(a):
        while a and a[-1] == (0, 0): a.pop()
        return a
    def deriv(a):
        return trim([(i * a[i][0] % p, i * a[i][1] % p) for i in range(1, len(a))]) if len(a) > 1 else []

    # build P_j as dual coefficient lists
    Pd = {}
    for k, (j, i) in enumerate(PARAMS):
        v = Pvals[k] % p
        d = 1 if (dpar is not None and k == dpar) else 0
        row = Pd.setdefault(j, [])
        while len(row) <= i: row.append((0, 0))
        row[i] = (v, d)
    for j in Pd: Pd[j] = trim(Pd[j])
    JMAX = 40
    P = [Pd.get(j, []) for j in range(JMAX + 2)]

    p10 = P[0][1] if len(P[0]) > 1 else (0, 0)
    if p10[0] == 0: return None                      # gauge-degenerate sample
    inv10 = pow(p10[0], p - 2, p)
    # 1/p10 as a dual number: d(1/u) = -u'/u^2
    inv10d = (-p10[1] * inv10 % p) * inv10 % p
    def dmulinv(a):   # multiply a by 1/p10 (dual)
        return trim([((v * inv10) % p, (d * inv10 + v * inv10d) % p) for v, d in a])

    Q = [[] for _ in range(JMAX + 2)]
    Q[0] = [(random.randrange(1, p), 0)]             # Q_0 constant; Q_0' = 0
    Q[1] = dmulinv([(0, 0), (0, 0), (1, 0)])         # p10 Q_1 = x^2
    for k in range(1, JMAX):
        acc = []
        for a in range(1, k + 1):
            b = k + 1 - a
            if b < 0 or a >= len(P) or not P[a]: continue
            acc = add(acc, scal(mul(P[a], deriv(Q[b])), a))
            acc = add(acc, scal(mul(deriv(P[a]), Q[b]), -(k + 1 - a)))
        Q[k + 1] = dmulinv(scal(acc, pow(k + 1, p - 2, p)))
    return Q

def conditions(Q):
    """N(Q)'s live conditions: coeff of x^i in Q_j vanishes for i < j-12
    (13<=j<=24), and Q_j = 0 for j > 24."""
    out = []
    for j in range(13, 25):
        for i in range(0, j - 12):
            out.append(Q[j][i] if i < len(Q[j]) else (0, 0))
    for j in range(25, 41):
        for i in range(len(Q[j])):
            out.append(Q[j][i])
    return out

def rank_mod(M, p):
    M = [row[:] for row in M]; nr, nc = len(M), (len(M[0]) if M else 0); r = 0
    for c in range(nc):
        piv = next((i for i in range(r, nr) if M[i][c] % p), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        r += 1
        if r == nr: break
    return r

for prime, tag in ((65521, "campaign prime"), (1000003, "FRESH prime, never used here")):
    print(f"\n--- p = {prime}  ({tag}; p = 1 mod 3: {prime % 3 == 1}) ---")
    ranks, ncond = [], None
    for trial in range(3):
        rng = random.Random(9000 + trial)
        Pv = [rng.randrange(1, prime) for _ in PARAMS]
        base = run(prime, Pv)
        if base is None: continue
        c0 = conditions(base)
        ncond = len(c0)
        # Jacobian: one dual run per parameter
        cols = []
        for k in range(len(PARAMS)):
            Qk = run(prime, Pv, dpar=k)
            cols.append([c[1] for c in conditions(Qk)])
        J = [[cols[k][r] for k in range(len(PARAMS))] for r in range(ncond)]
        ranks.append(rank_mod(J, prime))
    print(f"    conditions: {ncond}   parameters: {len(PARAMS)}   ranks at 3 random points: {ranks}")
    check(f"p={prime}: exact Jacobian rank is 60 (campaign's recorded value)",
          ranks and all(r == 60 for r in ranks), "CERTIFIED",
          f"ranks {ranks}; dim <= 61 - 60 = {61 - (ranks[0] if ranks else 0)}")

print("\n" + "="*78)
if FAIL:
    print("H1b step 1 FAILED -- the recorded rank does NOT reproduce:"); [print("   -", f) for f in FAIL]
    sys.exit(1)
print("""H1b step 1 RESULT.  rank = 60 of 61 CONFIRMED by a fully independent
rebuild -- own polygons, own bracket expansion, own recursion, own dual-number
differentiation, own rank -- at the campaign's prime AND at a fresh prime.

So  dim <= 1  stands as evidence.  Audit item A2.9 closes: the number the whole
pentagon story rests on is right.

IMPORTANT: this is a LOCAL bound (dim <= 61 - rank at the sampled point) and it
is NOT a verdict.  dim <= 1 permits a 1-parameter family OR isolated points --
and isolated points are exactly what a counterexample would look like.  The
rank does not distinguish them.  That is step 2: the SCHEME, not the rank.""")
print("="*78)
