"""night12 -- the P-ansatz sweep.  Seed 20260831.

Every P is a sparse element of Z[x,y] (ring: Q).  Families:

  A rand_sparse_lin    x + (2..7) random monomials, one of exact degree d
  B rand_sparse_nolin  3..8 random monomials, no linear term forced
  C struct_x           x + structured monomial mixes of degree d
  D leadsq             leading form P_d = (H_{d/2})^2, H random sparse, + tail
  E leadcube           leading form P_d = (H_{d/3})^3, H random sparse, + tail
  F coord              triangular compositions (known plane coordinates)
"""

import random
import matekit as M

SEED = 20260831


def _rand_mono(rnd, d, lo=0):
    while True:
        i = rnd.randrange(0, d + 1)
        j = rnd.randrange(0, d + 1 - i)
        if lo <= i + j <= d:
            return (i, j)


def _rand_form(rnd, e, terms):
    """random homogeneous form of degree e with `terms` monomials."""
    F = {}
    idx = rnd.sample(range(e + 1), min(terms, e + 1))
    for i in idx:
        F[(i, e - i)] = rnd.randrange(1, 6) * rnd.choice([1, -1])
    return F


def _tail(rnd, d, n):
    T = {}
    for _ in range(n):
        m = _rand_mono(rnd, max(1, d - 1))
        if m[0] + m[1] < d:
            T[m] = rnd.randrange(1, 5) * rnd.choice([1, -1])
    return T


def gen_family_A(rnd, d, n):
    out = []
    for t in range(n):
        k = rnd.randrange(2, 8)
        P = {(1, 0): 1}
        i = rnd.randrange(0, d + 1)
        P[(i, d - i)] = rnd.randrange(1, 6) * rnd.choice([1, -1])
        for _ in range(k - 1):
            m = _rand_mono(rnd, d)
            P[m] = P.get(m, 0) + rnd.randrange(1, 5) * rnd.choice([1, -1])
        P = {a: c for a, c in P.items() if c != 0}
        if M.pdeg(P) == d:
            out.append(("A_rand_sparse_lin", P))
    return out


def gen_family_B(rnd, d, n):
    out = []
    for t in range(n):
        k = rnd.randrange(3, 9)
        P = {}
        i = rnd.randrange(0, d + 1)
        P[(i, d - i)] = rnd.randrange(1, 6) * rnd.choice([1, -1])
        for _ in range(k - 1):
            m = _rand_mono(rnd, d)
            P[m] = P.get(m, 0) + rnd.randrange(1, 5) * rnd.choice([1, -1])
        P = {a: c for a, c in P.items() if c != 0}
        if M.pdeg(P) == d:
            out.append(("B_rand_sparse_nolin", P))
    return out


def gen_family_C(rnd, d, n):
    """x + structured mixes.  Shapes are chosen so the leading monomial is
    x^a y^b with a+b = d and a small set of intermediate monomials sits on the
    segment joining (1,0) to it."""
    out = []
    shapes = []
    for a in range(0, d + 1):
        b = d - a
        shapes.append((a, b))
    rnd.shuffle(shapes)
    for t in range(n):
        a, b = shapes[t % len(shapes)]
        P = {(1, 0): 1, (a, b): rnd.choice([1, -1, 2, 3])}
        r = rnd.randrange(1, 4)
        for _ in range(r):
            f = rnd.randrange(1, 4)
            aa, bb = (a * f) // 4, (b * f) // 4
            if 0 < aa + bb < d:
                P[(aa, bb)] = P.get((aa, bb), 0) + rnd.choice([1, -1, 2])
        P = {k: v for k, v in P.items() if v != 0}
        if M.pdeg(P) == d:
            out.append(("C_struct_x", P))
    return out


def gen_family_pow(rnd, d, n, power, tag):
    """leading form a perfect power: P_d = (H_e)^power, e = d // power."""
    out = []
    if d % power != 0:
        return out
    e = d // power
    for t in range(n):
        H = _rand_form(rnd, e, rnd.randrange(2, 4))
        if M.pdeg(H) != e:
            continue
        lead = M.ppow(H, power)
        P = M.padd(lead, {(1, 0): 1})
        P = M.padd(P, _tail(rnd, d, rnd.randrange(0, 3)))
        if M.pdeg(P) == d and len(P) <= 14:
            out.append((tag, P))
    return out


def _sub(A, xsub, ysub):
    """A(xsub, ysub) for polynomial dicts."""
    R = {}
    for (i, j), c in A.items():
        T = M.pmul(M.ppow(xsub, i), M.ppow(ysub, j))
        R = M.padd(R, {k: c * v for k, v in T.items()})
    return R


def gen_family_F(d):
    """Triangular compositions: exact plane coordinates with a known mate.
    Returned as (tag, P, Q_known) so the calibration arm has non-vacuous
    consistent cases."""
    out = []
    X = {(1, 0): 1}
    Y = {(0, 1): 1}
    for k in (2, 3, 4, 5):
        # F(x,y) = (x + (y + x^k)^m, y + x^k), degree k*m in the first slot
        for m in (2, 3):
            u = M.padd(Y, {(k, 0): 1})
            P = M.padd(X, M.ppow(u, m))
            if M.pdeg(P) == d:
                out.append(("F_coord", P, u))
        # F(x,y) = (y + x^k, ...) swapped
        v = M.padd(X, {(0, k): 1})
        for m in (2, 3):
            P = M.padd(Y, M.ppow(v, m))
            if M.pdeg(P) == d:
                out.append(("F_coord", P, v))
    # simple triangular
    P = M.padd(X, {(0, d): 1})
    out.append(("F_coord", P, Y))
    return out


def build_all():
    rnd = random.Random(SEED)
    main = [84, 96, 108, 126]
    calib = [4, 6, 9]
    items = []
    for d in main:
        items += gen_family_A(rnd, d, 8)
        items += gen_family_B(rnd, d, 4)
        items += gen_family_C(rnd, d, 6)
        items += gen_family_pow(rnd, d, 8, 2, "D_leadsq")
        items += gen_family_pow(rnd, d, 6, 3, "E_leadcube")
    for d in calib:
        items += gen_family_A(rnd, d, 4)
        items += gen_family_B(rnd, d, 2)
        items += gen_family_C(rnd, d, 3)
        items += gen_family_pow(rnd, d, 2, 2, "D_leadsq")
        items += gen_family_pow(rnd, d, 2, 3, "E_leadcube")
        for tag, P, Qk in gen_family_F(d):
            items.append((tag, P))
    out = []
    seen = set()
    for tag, P in items:
        key = tuple(sorted(P.items()))
        if key in seen:
            continue
        seen.add(key)
        d = M.pdeg(P)
        out.append({
            "tag": tag,
            "arm": "main" if d in main else "calib",
            "deg": d,
            "P": {("%d,%d" % a): int(c) for a, c in sorted(P.items())},
        })
    return out


if __name__ == "__main__":
    A = build_all()
    from collections import Counter
    print(len(A))
    print(Counter((r["arm"], r["deg"]) for r in A))
    print(Counter(r["tag"] for r in A))
