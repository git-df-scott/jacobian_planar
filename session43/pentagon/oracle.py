"""Consistency oracle for the pentagon, via the verified affine-in-late structure.

For any early point e in F_p^46 the 66 conditions are  M(e).late + v(e) = 0.
Solutions over the late block exist  <=>  rank(M) == rank([M | -v]).
Cost: 14 evaluations of the straight-line recursion (~ms), then a 66x14 rank.

CONTROLS (Example 10):
  POS  replace v by -M.late0 for a chosen late0: oracle MUST report consistent
       and recover a valid late (not necessarily late0 if M has a kernel).
  NEG  perturb the right-hand side off the column space: MUST report inconsistent.
"""
import sys, random
sys.path.insert(0, '/tmp/hunt')
from pentev import conditions, VARS, EARLY, LATE, p

def build(early):
    """Return M (66x13) and v (66) with conditions = M.late + v."""
    base = dict(early)
    for v_ in LATE:
        base[v_] = 0
    v = conditions(base)
    M = []
    for k, name in enumerate(LATE):
        d = dict(base)
        d[name] = 1
        col = conditions(d)
        M.append([(col[r] - v[r]) % p for r in range(66)])
    # M currently columns-major -> transpose to rows
    return [[M[c][r] for c in range(len(LATE))] for r in range(66)], v

def rref(rows, ncols):
    rows = [r[:] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        sel = next((i for i in range(r, len(rows)) if rows[i][c] % p), None)
        if sel is None:
            continue
        rows[r], rows[sel] = rows[sel], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(rows[i][j] - f * rows[r][j]) % p for j in range(len(rows[i]))]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return rows, piv

def consistent(M, v):
    """rank(M) vs rank([M|-v]); if consistent also return one solution."""
    n = len(LATE)
    rM, pM = rref([row[:] for row in M], n)
    aug = [M[r][:] + [(-v[r]) % p] for r in range(66)]
    rA, pA = rref(aug, n + 1)
    ok = (n not in pA)          # last column is not a pivot  <=>  consistent
    sol = None
    if ok:
        sol = [0] * n
        for i, c in enumerate(pA):
            if c < n:
                sol[c] = rA[i][n]
    return len(pM), len(pA), ok, sol

def verify(early, late):
    d = dict(early)
    for k, name in enumerate(LATE):
        d[name] = late[k]
    return conditions(d)

def controls(seed=5):
    rnd = random.Random(seed)
    early = {v: rnd.randrange(p) for v in EARLY}
    M, v = build(early)
    out = []
    # POS: force the rhs into the column space
    late0 = [rnd.randrange(p) for _ in LATE]
    vpos = [(-sum(M[r][c] * late0[c] for c in range(len(LATE)))) % p for r in range(66)]
    rm, ra, ok, sol = consistent(M, vpos)
    good = ok and all(x == 0 for x in [(sum(M[r][c] * sol[c] for c in range(len(LATE))) + vpos[r]) % p for r in range(66)])
    out.append(("POS planted rhs is consistent and a solution is recovered", good, f"rank {rm}/{ra}"))
    # NEG: push the rhs off the column space
    vneg = vpos[:]
    vneg[0] = (vneg[0] + 1) % p
    rm2, ra2, ok2, _ = consistent(M, vneg)
    out.append(("NEG perturbed rhs is inconsistent", (not ok2), f"rank {rm2}/{ra2}"))
    return out

if __name__ == "__main__":
    for msg, ok, info in controls():
        print(("PASS " if ok else "FAIL ") + msg + "  " + info)
    rnd = random.Random(11)
    print("\ngeneric early points:")
    for t in range(5):
        early = {v: rnd.randrange(p) for v in EARLY}
        M, v = build(early)
        rm, ra, ok, sol = consistent(M, v)
        print(f"  trial {t}: rank(M)={rm} rank([M|-v])={ra} consistent={ok}")
