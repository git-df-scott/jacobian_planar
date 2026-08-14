#!/usr/bin/env python3
"""Case (2): does an edge solution (C,G) extend to a full (A,B,C,D,E,F,G)?

Stage 1 produced the edge variety exactly: dim 0, vdim 35, and a shape-lemma
(RUR) basis in which every coordinate is a polynomial in theta := g_12, with
minimal polynomial

  theta^35 - 18479 th^28 - 4743 th^21 + 19923 th^14 + 5389 th^7 - 3930
    = (th^7+7766)(th^7-30040)(th^7-9260)(th^14+13055 th^7-23589).

The 7-fold orbits are the residual gauge (normalizing c_8 = 1 needs lambda^7),
so there are FIVE essentially distinct solutions.  No branch has an F_p-rational
theta, but that does not matter: pick one irreducible factor and work in the
field it defines.  For th^7 = -7766 that is K = F_p[th]/(th^7+7766) = F_{p^7}
(irreducible exactly because -7766 is not a 7th power, and 7 | p-1).

Then the remaining four equations are solved over K by LINEAR ALGEBRA:

    (w=-3)   B G' - 3 B' G + 2 C F' - 2 C' F = 0      linear in (B,F)
    (w=-2)   -3 A' G + B F' - 2 B' F + 2 C E' - C' E = 0
    (w=-1)   -2 A' F + B E' - B' E + 2 C D' = 0
    (w= 0)   B D' = A' E

with supports A: t^0..t^8, B: t^1..t^8, D: t^0..t^12, E,F: t^1..t^12,
and vertex conditions a_8 != 0 (vertex (8,16)), c_8 != 0 (vertex (8,14)),
d_12 != 0 (vertex (12,24)), g_12 != 0 (vertex (12,21)), a_0 != 0 (vertex (0,0)
of N(P)), d_0 != 0 (vertex (0,0) of N(Q)).
"""
import sys, itertools

p = 65521
DEG = 7          # theta^7 = -CONST
CONST = 7766     # theta^7 + 7766 = 0  ->  theta^7 = -7766

# ------------------------------------------------------------------ field K
def kred(a):
    """reduce a list of coefficients modulo theta^7 = -CONST."""
    a = list(a)
    while len(a) > DEG:
        top = a.pop()
        if top:
            a[len(a) - DEG] = (a[len(a) - DEG] - top * CONST) % p
    while len(a) < DEG:
        a.append(0)
    return [x % p for x in a]

def kadd(a, b):
    return [(a[i] + b[i]) % p for i in range(DEG)]

def ksub(a, b):
    return [(a[i] - b[i]) % p for i in range(DEG)]

def kmul(a, b):
    o = [0] * (2 * DEG - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    o[i + j] = (o[i + j] + x * y) % p
    return kred(o)

def kscal(a, c):
    return [x * c % p for x in a]

def kzero():
    return [0] * DEG

def kone():
    r = kzero()
    r[0] = 1
    return r

def kis0(a):
    return all(x == 0 for x in a)

def kpow(a, e):
    r = kone()
    b = list(a)
    while e:
        if e & 1:
            r = kmul(r, b)
        b = kmul(b, b)
        e >>= 1
    return r

def kinv(a):
    """Inverse in K = F_{p^DEG} by Fermat: a^(q-2) with q = p^DEG.

    An extended-Euclid version written first did not terminate (its loop
    condition drove r1 to zero instead of stopping at the constant gcd).
    Fermat needs ~112 squarings here and is unambiguously correct."""
    if kis0(a):
        raise ZeroDivisionError("inverse of 0 in K")
    return kpow(a, p ** DEG - 2)

def _kinv_euclid_UNUSED(a):
    r0 = [CONST] + [0] * (DEG - 1) + [1]
    r1 = list(a) + [0]
    while len(r1) > 1 and r1[-1] == 0:
        r1.pop()
    t0, t1 = [0], [1]
    def pdeg(u):
        d = len(u) - 1
        while d > 0 and u[d] == 0:
            d -= 1
        return d
    def pmul_(u, v):
        o = [0] * (len(u) + len(v) - 1)
        for i, x in enumerate(u):
            if x:
                for j, y in enumerate(v):
                    if y:
                        o[i + j] = (o[i + j] + x * y) % p
        return o
    def psub_(u, v):
        n = max(len(u), len(v))
        return [((u[i] if i < len(u) else 0) - (v[i] if i < len(v) else 0)) % p
                for i in range(n)]
    while pdeg(r1) > 0 or r1[0] != 0:
        d0, d1 = pdeg(r0), pdeg(r1)
        if d0 < d1:
            r0, r1 = r1, r0
            t0, t1 = t1, t0
            continue
        if d1 == 0 and r1[0] == 0:
            break
        c = r0[d0] * pow(r1[d1], p - 2, p) % p
        shift = d0 - d1
        q = [0] * shift + [c]
        r0 = psub_(r0, pmul_(q, r1))
        t0 = psub_(t0, pmul_(q, t1))
        while len(r0) > 1 and r0[-1] == 0:
            r0.pop()
        if pdeg(r0) < pdeg(r1):
            r0, r1 = r1, r0
            t0, t1 = t1, t0
    # now r1 is the nonzero constant gcd (a is invertible)
    inv_c = pow(r1[0] if pdeg(r1) == 0 else r0[0], p - 2, p)
    res = t1 if pdeg(r1) == 0 else t0
    return kred([x * inv_c % p for x in res])

# --------------------------------------------- shape-lemma RUR coefficients
# each entry: variable -> list of (exponent of theta, coefficient) with the
# convention  var  =  - sum coeff * theta^exp   (from  var + sum ... = 0)
RUR = {
 "g11": [(31, -19592), (24, -16942), (17, -29970), (10, -16317), (3, 30408)],
 "g10": [(33, 24882), (26, 22968), (19, -13445), (12, -18863), (5, 17038)],
 "g9":  [(28, -32394), (21, 27224), (14, -28547), (7, -7685), (0, -2176)],
 "g8":  [(30, 9859), (23, -15597), (16, -14456), (9, -4554), (2, -26778)],
 "g7":  [(32, -8209), (25, 11305), (18, 24927), (11, 19877), (4, 24579)],
 "g6":  [(34, 4116), (27, -23722), (20, 7922), (13, -12511), (6, -28998)],
 "g5":  [(29, 19616), (22, 26319), (15, 176), (8, 452), (1, -2349)],
 "g4":  [(31, 13545), (24, 27217), (17, 28129), (10, -3833), (3, 30208)],
 "g3":  [(33, 1486), (26, 24148), (19, 7522), (12, -23922), (5, 29698)],
 "c7":  [(30, 8779), (23, 32386), (16, -19980), (9, -10878), (2, 20272)],
 "c6":  [(32, 5377), (25, -26325), (18, 13654), (11, -30660), (4, -1990)],
 "c5":  [(34, -1403), (27, 10822), (20, -25979), (13, -3136), (6, -31384)],
 "c4":  [(29, 17164), (22, 14839), (15, 154), (8, -32365), (1, 22515)],
 "c3":  [(31, 13545), (24, 27217), (17, 28129), (10, -3833), (3, 30208)],
 "c2":  [(33, 2229), (26, -29299), (19, 11283), (12, 29638), (5, -20974)],
}

def theta_pow(e):
    r = kone()
    th = kzero()
    th[1] = 1
    for _ in range(e):
        r = kmul(r, th)
    return r

def rur_value(name):
    """var = - sum coeff * theta^exp"""
    acc = kzero()
    for e, cf in RUR[name]:
        acc = kadd(acc, kscal(theta_pow(e), cf % p))
    return ksub(kzero(), acc)

def build_CG():
    th = kzero(); th[1] = 1
    C = [kzero()] * 9
    C[1] = kone()
    C[8] = kone()
    for i in range(2, 8):
        C[i] = rur_value(f"c{i}")
    G = [kzero()] * 13
    G[2] = kone()                      # g_2 = 1 is forced
    for i in range(3, 12):
        G[i] = rur_value(f"g{i}")
    G[12] = th                          # theta = g_12
    return C, G

# ------------------------------------------------------------ K[t] helpers
def kpmul(A, B):
    o = [kzero()] * (len(A) + len(B) - 1)
    for i, x in enumerate(A):
        if not kis0(x):
            for j, y in enumerate(B):
                if not kis0(y):
                    o[i + j] = kadd(o[i + j], kmul(x, y))
    return o

def kpder(A):
    return [kscal(A[i], i) for i in range(1, len(A))] or [kzero()]

def kpadd(A, B):
    n = max(len(A), len(B))
    return [kadd(A[i] if i < len(A) else kzero(),
                 B[i] if i < len(B) else kzero()) for i in range(n)]

def kpscal(A, c):
    return [kscal(a, c) for a in A]

if __name__ == "__main__":
    C, G = build_CG()
    # sanity: the edge equation must hold exactly over K
    lhs = kpadd(kpscal(kpmul(C, kpder(G)), 2),
                kpscal(kpmul(kpder(C), G), -3))
    target = [kzero(), kzero(), kone()]
    ok = all(kis0(ksub(lhs[i] if i < len(lhs) else kzero(),
                       target[i] if i < len(target) else kzero()))
             for i in range(max(len(lhs), len(target))))
    print(f"K = F_p[th]/(th^7 + {CONST}),  th^7 = {-CONST % p}")
    print(f"EDGE EQUATION 2 C G' - 3 C' G = t^2 holds over K: {ok}")
    if not ok:
        bad = [i for i in range(max(len(lhs), len(target)))
               if not kis0(ksub(lhs[i] if i < len(lhs) else kzero(),
                                target[i] if i < len(target) else kzero()))]
        print(f"   mismatching t-degrees: {bad[:12]}")
    print(f"deg C = {max(i for i,v in enumerate(C) if not kis0(v))}, "
          f"deg G = {max(i for i,v in enumerate(G) if not kis0(v))}")

# ----------------------------------------------------- linear algebra over K
def ksolve(M, rhs):
    """Solve M z = rhs over K. Returns (particular, kernel_basis) or None."""
    rows, cols = len(M), len(M[0]) if M else 0
    A = [row[:] + [rhs[r]] for r, row in enumerate(M)]
    piv = {}
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if not kis0(A[i][c])), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = kinv(A[r][c])
        A[r] = [kmul(x, iv) for x in A[r]]
        for i in range(rows):
            if i != r and not kis0(A[i][c]):
                f = A[i][c]
                A[i] = [ksub(A[i][k], kmul(f, A[r][k])) for k in range(cols + 1)]
        piv[c] = r
        r += 1
    for i in range(rows):
        if all(kis0(A[i][c]) for c in range(cols)) and not kis0(A[i][cols]):
            return None
    part = [kzero()] * cols
    for c, rr in piv.items():
        part[c] = A[rr][cols]
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for fc in free:
        v = [kzero()] * cols
        v[fc] = kone()
        for c, rr in piv.items():
            v[c] = ksub(kzero(), A[rr][fc])
        basis.append(v)
    return part, basis

def eq_w3_matrix(C, G):
    """B G' - 3 B' G + 2 C F' - 2 C' F = 0, unknowns b_1..b_8, f_1..f_12."""
    Gp, Cp = kpder(G), kpder(C)
    cols = []
    for i in range(1, 9):                       # b_i : B = t^i
        Bi = [kzero()] * i + [kone()]
        term = kpadd(kpmul(Bi, Gp), kpscal(kpmul(kpder(Bi), G), -3))
        cols.append(term)
    for i in range(1, 13):                      # f_i : F = t^i
        Fi = [kzero()] * i + [kone()]
        term = kpadd(kpscal(kpmul(C, kpder(Fi)), 2),
                     kpscal(kpmul(Cp, Fi), -2))
        cols.append(term)
    m = max(len(c) for c in cols)
    M = [[(col[r] if r < len(col) else kzero()) for col in cols]
         for r in range(m)]
    return M, [kzero()] * m

if __name__ == "__main__" and "--extend" in sys.argv:
    C, G = build_CG()
    M, rhs = eq_w3_matrix(C, G)
    print(f"\n(w=-3) system: {len(M)} equations, {len(M[0])} unknowns (B:8, F:12)")
    res = ksolve(M, rhs)
    if res is None:
        print("   INCONSISTENT -- impossible for a homogeneous system")
    else:
        part, basis = res
        print(f"   solution space over K has dimension {len(basis)}")
        if len(basis) == 0:
            print("   => B = F = 0 forced.")
            print("   Then (w=0) B D' = A' E gives A' E = 0, and (w=-1)")
            print("   -2A'F + BE' - B'E + 2CD' = 0 becomes C D' = 0, so D is")
            print("   constant -- but N(Q)'s vertex (12,24) needs d_12 != 0.")
            print("   *** CONTRADICTION: this edge branch does NOT extend ***")

# ------------------------------------------------- the rest of the cascade
def poly_from_coeffs(coeffs, lo):
    """coeffs[k] is the coefficient of t^(lo+k)."""
    return [kzero()] * lo + list(coeffs)

def split_BF(vec):
    """vec = (b_1..b_8, f_1..f_12) -> polynomials B, F."""
    B = poly_from_coeffs(vec[:8], 1)
    F = poly_from_coeffs(vec[8:], 1)
    return B, F

def eq_w2_system(C, G, B, F):
    """-3 A' G + (B F' - 2 B' F) + 2 C E' - C' E = 0; unknowns a_0..a_8, e_1..e_12."""
    const = kpadd(kpmul(B, kpder(F)), kpscal(kpmul(kpder(B), F), -2))
    cols = []
    for i in range(0, 9):                       # a_i
        Ai = [kzero()] * i + [kone()]
        cols.append(kpscal(kpmul(kpder(Ai), G), -3))
    for i in range(1, 13):                      # e_i
        Ei = [kzero()] * i + [kone()]
        cols.append(kpadd(kpscal(kpmul(C, kpder(Ei)), 2),
                          kpscal(kpmul(kpder(C), Ei), -1)))
    m = max([len(c) for c in cols] + [len(const)])
    M = [[(col[r] if r < len(col) else kzero()) for col in cols]
         for r in range(m)]
    rhs = [ksub(kzero(), const[r] if r < len(const) else kzero())
           for r in range(m)]
    return M, rhs

def eq_w1_system(C, A, B, E, F):
    """-2 A' F + (B E' - B' E) + 2 C D' = 0; unknowns d_0..d_12."""
    const = kpadd(kpscal(kpmul(kpder(A), F), -2),
                  kpadd(kpmul(B, kpder(E)), kpscal(kpmul(kpder(B), E), -1)))
    cols = []
    for i in range(0, 13):
        Di = [kzero()] * i + [kone()]
        cols.append(kpscal(kpmul(C, kpder(Di)), 2))
    m = max([len(c) for c in cols] + [len(const)])
    M = [[(col[r] if r < len(col) else kzero()) for col in cols]
         for r in range(m)]
    rhs = [ksub(kzero(), const[r] if r < len(const) else kzero())
           for r in range(m)]
    return M, rhs

def check_w0(A, B, D, E):
    """B D' = A' E."""
    lhs = kpmul(B, kpder(D))
    rhs = kpmul(kpder(A), E)
    n = max(len(lhs), len(rhs))
    return all(kis0(ksub(lhs[i] if i < len(lhs) else kzero(),
                         rhs[i] if i < len(rhs) else kzero()))
               for i in range(n))

if __name__ == "__main__" and "--full" in sys.argv:
    import random
    C, G = build_CG()
    M3, r3 = eq_w3_matrix(C, G)
    part, basis = ksolve(M3, r3)
    print(f"(w=-3): solution space dim {len(basis)} over K")
    rng = random.Random(int(sys.argv[sys.argv.index("--full") + 1])
                        if len(sys.argv) > sys.argv.index("--full") + 1 else 1)
    stats = {"w2 inconsistent": 0, "w1 inconsistent": 0,
             "w0 fails": 0, "SURVIVES": 0, "degenerate": 0}
    N = 40
    for _ in range(N):
        coef = [[rng.randrange(p) for _ in range(DEG)] for _ in basis]
        vec = list(part)
        for cf, bv in zip(coef, basis):
            vec = [kadd(vec[k], kmul(cf, bv[k])) for k in range(len(vec))]
        B, F = split_BF(vec)
        if kis0(B[-1] if B else kzero()) and all(kis0(v) for v in B):
            stats["degenerate"] += 1
            continue
        M2, r2 = eq_w2_system(C, G, B, F)
        s2 = ksolve(M2, r2)
        if s2 is None:
            stats["w2 inconsistent"] += 1
            continue
        pa, ba = s2
        A = poly_from_coeffs(pa[:9], 0)
        E = poly_from_coeffs(pa[9:], 1)
        M1, r1 = eq_w1_system(C, A, B, E, F)
        s1 = ksolve(M1, r1)
        if s1 is None:
            stats["w1 inconsistent"] += 1
            continue
        pd, bd = s1
        D = poly_from_coeffs(pd, 0)
        if not check_w0(A, B, D, E):
            stats["w0 fails"] += 1
            continue
        stats["SURVIVES"] += 1
    print(f"\nrandom points of the (w=-3) solution space, N = {N}:")
    for k, v in stats.items():
        print(f"   {k:<20} {v}")

def kprem(A, B):
    """remainder of A mod B over K."""
    A = [list(a) for a in A]
    db = max(i for i, v in enumerate(B) if not kis0(v))
    lead_inv = kinv(B[db])
    for k in range(len(A) - 1, db - 1, -1):
        if kis0(A[k]):
            continue
        f = kmul(A[k], lead_inv)
        for i in range(db + 1):
            A[k - db + i] = ksub(A[k - db + i], kmul(f, B[i]))
    return A[:db]

if __name__ == "__main__" and "--freedom" in sys.argv:
    import random
    C, G = build_CG()
    M3, r3 = eq_w3_matrix(C, G)
    p3, b3 = ksolve(M3, r3)
    print(f"(w=-3): (B,F) solution space dim {len(b3)} over K")
    rng = random.Random(7)
    # measure the (w=-2) kernel dimension, which the previous run ignored
    dims = set()
    for _ in range(6):
        vec = list(p3)
        for bv in b3:
            cf = [rng.randrange(p) for _ in range(DEG)]
            vec = [kadd(vec[k], kmul(cf, bv[k])) for k in range(len(vec))]
        B, F = split_BF(vec)
        M2, r2 = eq_w2_system(C, G, B, F)
        s2 = ksolve(M2, r2)
        if s2 is None:
            dims.add("inconsistent")
        else:
            dims.add(len(s2[1]))
    print(f"(w=-2): (A,E) kernel dimensions seen: {sorted(dims, key=str)}")
    print("\n(w=-1) is linear in D with image C*{deg <= 11}, so its")
    print("consistency is EXACTLY  C | (-2 A' F + B E' - B' E)  (8 conditions).")
    # now sample (B,F) AND the (w=-2) kernel, and test the divisibility
    tot = ok = 0
    for _ in range(60):
        vec = list(p3)
        for bv in b3:
            cf = [rng.randrange(p) for _ in range(DEG)]
            vec = [kadd(vec[k], kmul(cf, bv[k])) for k in range(len(vec))]
        B, F = split_BF(vec)
        s2 = ksolve(*eq_w2_system(C, G, B, F))
        if s2 is None:
            continue
        pa, ba = s2
        sol = list(pa)
        for bv in ba:
            cf = [rng.randrange(p) for _ in range(DEG)]
            sol = [kadd(sol[k], kmul(cf, bv[k])) for k in range(len(sol))]
        A = poly_from_coeffs(sol[:9], 0)
        E = poly_from_coeffs(sol[9:], 1)
        expr = kpadd(kpscal(kpmul(kpder(A), F), -2),
                     kpadd(kpmul(B, kpder(E)), kpscal(kpmul(kpder(B), E), -1)))
        r = kprem(expr, C)
        tot += 1
        ok += all(kis0(v) for v in r)
    print(f"\nrandom points of the FULL freedom (B,F kernel + A,E kernel):")
    print(f"   C divides the (w=-1) obstruction in {ok}/{tot} samples")

if __name__ == "__main__" and "--solve" in sys.argv:
    import random
    C, G = build_CG()
    p3, b3 = ksolve(*eq_w3_matrix(C, G))
    rng = random.Random(11)
    stats = {"w2 inconsistent": 0, "alpha SOLVED -> survivor": 0,
             "alpha inconsistent": 0}
    N = 60
    for _ in range(N):
        vec = list(p3)
        for bv in b3:
            cf = [rng.randrange(p) for _ in range(DEG)]
            vec = [kadd(vec[k], kmul(cf, bv[k])) for k in range(len(vec))]
        B, F = split_BF(vec)
        s2 = ksolve(*eq_w2_system(C, G, B, F))
        if s2 is None:
            stats["w2 inconsistent"] += 1
            continue
        pa, ba = s2
        # the (w=-1) consistency condition  C | (-2A'F + BE' - B'E)  is LINEAR
        # in the (w=-2) kernel coefficients alpha, so SOLVE it rather than
        # sampling: 8 equations (the remainder mod C) in len(ba) unknowns.
        def expr_of(sol):
            A = poly_from_coeffs(sol[:9], 0)
            E = poly_from_coeffs(sol[9:], 1)
            return kpadd(kpscal(kpmul(kpder(A), F), -2),
                         kpadd(kpmul(B, kpder(E)),
                               kpscal(kpmul(kpder(B), E), -1)))
        base = kprem(expr_of(pa), C)
        cols = []
        for bv in ba:
            sol = [kadd(pa[k], bv[k]) for k in range(len(pa))]
            col = kprem(expr_of(sol), C)
            cols.append([ksub(col[r], base[r]) for r in range(len(base))])
        M = [[cols[c][r] for c in range(len(cols))] for r in range(len(base))]
        rhs = [ksub(kzero(), base[r]) for r in range(len(base))]
        sol = ksolve(M, rhs) if cols else (None if any(
            not kis0(v) for v in base) else ([], []))
        if sol is None:
            stats["alpha inconsistent"] += 1
        else:
            stats["alpha SOLVED -> survivor"] += 1
    print(f"\nSOLVING (not sampling) the (w=-1) condition for the (w=-2) kernel,"
          f" N = {N}:")
    for k, v in stats.items():
        print(f"   {k:<28} {v}")
