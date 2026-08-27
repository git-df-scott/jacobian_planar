#!/usr/bin/env python3
"""Independent (u,z)-formulation of  [P,Q] = x^2  on the open (72,108)
subcase 2 polygons

    N(P) = conv{(0,0),(1,0),(8,14),(8,16)},
    N(Q) = conv{(0,0),(2,1),(12,21),(12,24)},

and a falsification test of the predicted third forced zero  a_10_5 = 0.

Nothing here uses the "face form = R^2" analysis.  The only input is the
bracket equation with fully generic coefficients on the two polygons.

CHANGE OF VARIABLES
-------------------
Put u = x*y^2 and v = y, so a monomial x^i y^j equals u^i v^(j-2i); the
weight w = j - 2i is exactly the v-exponent.  Both polygons are "thin" in
that weight:

    N(P) lattice points have w in {0,-1,-2}
    N(Q) lattice points have w in {0,-1,-2,-3}

Writing z = 1/v the two polynomials become POLYNOMIALS in (u,z):

    P = f(u) + p(u) z + q(u) z^2                       deg_u <= 8
    Q = g(u) + r(u) z + s(u) z^2 + t(u) z^3            deg_u <= 12

with the polygon's lower boundary giving the vanishing orders

    p = O(u), q = O(u), r = O(u), s = O(u^2), t = O(u^2)

and f, g unconstrained at u = 0.  The dictionary back to the descent's
symbols  a_j_i = coefficient of x^i y^j  is

    f_a = a_{2a}_{a}   (the w = 0 edge  (0,0)-(8,16)),   a = 0..8
    p_a = a_{2a-1}_{a},                                  a = 1..8
    q_a = a_{2a-2}_{a},                                  a = 1..8

so in particular

    a_2_1  = f_1     a_4_2  = f_2     a_10_5 = f_5   <-- the prediction
    a_0_1  = q_1     a_1_1  = p_1     a_6_3  = f_3     a_3_2 = p_2

Since d(u,v)/d(x,y) has determinant y^2 = v^2 and dv/dz = -z^-2,

    [P,Q]_{x,y} = x^2   <==>   [P,Q]_{u,z} = -u^2 z^4 .

GAUGE.  a_0_1 = q_1 must be nonzero (else the y^0 row of [P,Q] cannot be
x^2), and (P,Q) -> (P/L, L*Q) leaves everything invariant, so q_1 = 1 is a
sound normalisation.  f_0 and g_0 are additive constants and never appear.
"""
from fractions import Fraction
import itertools
import sys

NVARS_P = 23      # f1..f8, p1..p8, q2..q8   (q1 == 1)
PVARS = ([f"f{a}" for a in range(1, 9)]
         + [f"p{a}" for a in range(1, 9)]
         + [f"q{a}" for a in range(2, 9)])
PIDX = {n: i for i, n in enumerate(PVARS)}

QVARS = ([f"g{b}" for b in range(1, 13)]
         + [f"r{b}" for b in range(1, 13)]
         + [f"s{b}" for b in range(2, 13)]
         + [f"t{b}" for b in range(2, 13)])


# ---------------------------------------------------------------- polynomials
# sparse dicts: exponent tuple (len NVARS_P) -> coefficient
ZERO = {}


def pconst(c, mod):
    c = c % mod if mod else Fraction(c)
    if c == 0:
        return {}
    return {(0,) * NVARS_P: c}


def pvar(name):
    e = [0] * NVARS_P
    e[PIDX[name]] = 1
    return {tuple(e): 1}


def padd(A, B, mod):
    if not A:
        return dict(B)
    if not B:
        return dict(A)
    C = dict(A)
    for m, c in B.items():
        v = C.get(m, 0) + c
        if mod:
            v %= mod
        if v:
            C[m] = v
        elif m in C:
            del C[m]
    return C


def pscal(A, c, mod):
    if not A or c == 0:
        return {}
    if mod:
        c %= mod
        if c == 0:
            return {}
        return {m: (v * c) % mod for m, v in A.items()}
    return {m: v * c for m, v in A.items()}


def pmulvar(A, name, mod):
    """multiply a polynomial by a single variable -- the only product needed"""
    if not A:
        return {}
    k = PIDX[name]
    C = {}
    for m, c in A.items():
        e = list(m)
        e[k] += 1
        C[tuple(e)] = c
    return C


def pmul(A, B, mod):
    C = {}
    for m1, c1 in A.items():
        for m2, c2 in B.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            v = C.get(m, 0) + c1 * c2
            if mod:
                v %= mod
            if v:
                C[m] = v
            elif m in C:
                del C[m]
    return C


def pstr(A):
    if not A:
        return "0"
    out = []
    for m, c in sorted(A.items()):
        f = [str(c)]
        for i, e in enumerate(m):
            if e:
                f.append(PVARS[i] + ("^%d" % e if e > 1 else ""))
        out.append("*".join(f))
    return "+".join(out).replace("+-", "-")


# ------------------------------------------------------------------ equations
# A[a] = [f_a, p_a, q_a]  as *atoms*: either ('v', name) or ('c', int)
# B[b] = [g_b, r_b, s_b, t_b]
def atomsA(a):
    qa = ("c", 1) if a == 1 else ("v", f"q{a}")
    return [("v", f"f{a}"), ("v", f"p{a}"), qa]


def atomsB(b):
    z = ("c", 0)
    return [("v", f"g{b}"), ("v", f"r{b}"),
            z if b < 2 else ("v", f"s{b}"),
            z if b < 2 else ("v", f"t{b}")]


def build_equations():
    """Return  eqs[(n,k)] = list of (coef, atomA, atomB)  and the constant.

    coefficient of u^n z^k in  [P,Q]_{u,z} + u^2 z^4 .
    [P,Q]_{u,z} = sum_{a,b} u^{a+b-1} ( a A_a B_b' - b A_a' B_b ).
    """
    eqs = {}
    const = {}
    for n in range(1, 20):
        for k in range(0, 5):
            eqs[(n, k)] = []
            const[(n, k)] = 1 if (n, k) == (2, 4) else 0
    for a in range(1, 9):
        AA = atomsA(a)
        for b in range(1, 13):
            n = a + b - 1
            if n > 19:
                continue
            BB = atomsB(b)
            for k in range(0, 5):
                terms = eqs[(n, k)]
                # + a * A_a * B_b'   ; B_b' coefficient of z^j is (j+1)B[j+1]
                for i in range(0, 3):
                    j = k - i
                    if 0 <= j <= 2:
                        c = a * (j + 1)
                        terms.append((c, AA[i], BB[j + 1]))
                # - b * A_a' * B_b   ; A_a' coefficient of z^i is (i+1)A[i+1]
                for i in range(0, 2):
                    j = k - i
                    if 0 <= j <= 3:
                        c = -b * (i + 1)
                        terms.append((c, AA[i + 1], BB[j]))
    # drop terms with a zero atom
    for key in eqs:
        eqs[key] = [(c, x, y) for (c, x, y) in eqs[key]
                    if not (x[0] == "c" and x[1] == 0)
                    and not (y[0] == "c" and y[1] == 0)]
    return eqs, const


# --------------------------------------------------------------- verification
def check_degenerate_solution():
    """P = u z^2, Q = u^2 z^3  is a solution of  [P,Q] = -u^2 z^4 ; every
    equation must hold on it.  (q1 = 1, t2 = 1, everything else 0.)"""
    eqs, const = build_equations()
    val = {}
    for v in PVARS + QVARS:
        val[v] = 0
    val["t2"] = 1

    def ev(atom):
        return atom[1] if atom[0] == "c" else val[atom[1]]
    bad = []
    for key in sorted(eqs):
        tot = const[key] * 0  # the RHS is +u^2z^4 added on the left
        tot = const[key]
        for c, x, y in eqs[key]:
            tot += c * ev(x) * ev(y)
        if tot != 0:
            bad.append((key, tot))
    return bad


def check_random_bracket(mod=1000003, seed=7):
    """Cross-check the (u,z) equations against a *direct* bracket computation
    in the original (x,y) coordinates on random coefficients."""
    import random
    rng = random.Random(seed)
    # random values for every lattice point of both polygons
    valP = {}   # (i,j) -> coeff of x^i y^j
    valQ = {}
    A = {}
    B = {}
    for a in range(0, 9):
        A[a] = [rng.randrange(mod) for _ in range(3)]
    for b in range(0, 13):
        B[b] = [rng.randrange(mod) for _ in range(4)]
    A[0][1] = A[0][2] = 0           # P has only f_0 at u^0
    B[0][1] = B[0][2] = B[0][3] = 0
    B[1][2] = B[1][3] = 0           # s,t start at u^2
    for a in range(1, 9):
        pass
    # (u,z) -> (x,y):  u^a z^k  =  x^a y^(2a-k)
    for a in range(0, 9):
        for k in range(0, 3):
            if A[a][k]:
                valP[(a, 2 * a - k)] = A[a][k]
    for b in range(0, 13):
        for k in range(0, 4):
            if B[b][k]:
                valQ[(b, 2 * b - k)] = B[b][k]
    # direct bracket in (x,y)
    br = {}
    for (i1, j1), c1 in valP.items():
        for (i2, j2), c2 in valQ.items():
            co = (i1 * j2 - j1 * i2) % mod
            if co == 0:
                continue
            key = (i1 + i2 - 1, j1 + j2 - 1)
            br[key] = (br.get(key, 0) + co * c1 * c2) % mod
    br = {k: v for k, v in br.items() if v}
    # translate to u^n z^k :  x^i y^j = u^i z^(2i-j)
    br_uz = {}
    for (i, j), c in br.items():
        br_uz[(i, 2 * i - j)] = c
    # now the (u,z) equations, evaluated: they encode [P,Q]_{u,z} + u^2 z^4
    eqs, const = build_equations()
    valmap = {}
    for a in range(1, 9):
        valmap[f"f{a}"] = A[a][0]
        valmap[f"p{a}"] = A[a][1]
        valmap[f"q{a}"] = A[a][2]
    for b in range(1, 13):
        valmap[f"g{b}"] = B[b][0]
        valmap[f"r{b}"] = B[b][1]
        if b >= 2:
            valmap[f"s{b}"] = B[b][2]
            valmap[f"t{b}"] = B[b][3]

    def ev(atom):
        if atom[0] == "c":
            return atom[1]
        if atom[1] == "q1":
            return A[1][2]
        return valmap[atom[1]]
    # note build_equations hard-codes q1 = 1; redo with A[1][2] free
    A[1][2] = 1
    valmap["q1"] = 1
    for a in range(0, 9):
        for k in range(0, 3):
            if k == 2 and a == 1:
                valP[(a, 2 * a - k)] = 1
    # recompute the direct bracket with q1 = 1 enforced
    br = {}
    for (i1, j1), c1 in valP.items():
        for (i2, j2), c2 in valQ.items():
            co = (i1 * j2 - j1 * i2) % mod
            if co == 0:
                continue
            key = (i1 + i2 - 1, j1 + j2 - 1)
            br[key] = (br.get(key, 0) + co * c1 * c2) % mod
    br_uz = {}
    for (i, j), c in br.items():
        if c % mod:
            br_uz[(i, 2 * i - j)] = c % mod
    mismatches = []
    for n in range(1, 20):
        for k in range(0, 5):
            tot = 0
            for c, x, y in eqs[(n, k)]:
                tot += c * ev(x) * ev(y)
            tot %= mod
            # [P,Q]_{x,y} = v^2 * [P,Q]_{u,v} = v^2 * (-z^2) * [P,Q]_{u,z}
            #             = -[P,Q]_{u,z}   (because v^2 z^2 = 1)
            # so the (n,k) coefficient of [P,Q]_{u,z} is MINUS the direct one.
            direct = (-br_uz.get((n, k), 0)) % mod
            if tot != direct:
                mismatches.append((n, k, tot, direct))
    return mismatches


if __name__ == "__main__":
    bad = check_degenerate_solution()
    print("degenerate solution P=u z^2, Q=u^2 z^3 :",
          "OK" if not bad else f"FAILS {bad[:5]}")
    mm = check_random_bracket()
    print("random cross-check against direct (x,y) bracket :",
          "OK" if not mm else f"MISMATCH {mm[:5]}")
    eqs, const = build_equations()
    ne = sum(1 for k in eqs if eqs[k] or const[k])
    print(f"equations: {ne} non-empty of {len(eqs)}")
    print(f"P-side unknowns: {NVARS_P}  Q-side unknowns: {len(QVARS)}")
