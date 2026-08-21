#!/usr/bin/env python3
"""Case (2), final step: SOLVE the (w=-1) condition instead of sampling it.

Setup (all verified in trackB1_case2_extend.py):
  * K = F_p[th]/(th^7 + CONST) = F_{p^7}, C and G from the shape-lemma RUR,
    and 2 C G' - 3 C' G = t^2 holds exactly over K.
  * (w=-3) is linear homogeneous in (B,F): solution space of dimension 3, so
    (B,F) = BF0 + sum_i beta_i * BFbasis_i,  beta in K^3.
  * (w=-2) is linear in (A,E) and **its MATRIX does not depend on (B,F)** --
    only the right-hand side does (verified: the matrix is identical across
    random (B,F)).  Hence its kernel is a FIXED 3-dimensional subspace and
        (A,E) = P2(beta) + sum_j alpha_j * Kbasis_j,  alpha in K^3,
    with P2 a FIXED linear image of the RHS, so P2 is QUADRATIC in beta.
    (An earlier note claimed the kernel basis varied with (B,F), which would
    have blocked interpolation; that was wrong.)
  * (w=-1) is linear in D with image C*{deg <= 11}, so its consistency is
        C | (-2 A' F + B E' - B' E),
    i.e. the 8 coefficients of the remainder mod C must vanish.

Those 8 conditions are polynomial in (beta, alpha): degree <= 3 in beta and
degree <= 1 in alpha, so they live in a FIXED 80-monomial basis
(20 beta-monomials of degree <= 3) x (4 alpha-monomials of degree <= 1).
Interpolate them exactly over K, then hand the system to Singular over the
algebraic extension F_p(a) with a^7 = -CONST and let it decide.

8 equations in 6 unknowns: emptiness is expected, but this DECIDES it rather
than sampling it.
"""
import sys, itertools, random
import trackB1_case2_extend as M

p = M.p
DEG = M.DEG

def beta_monos():
    out = []
    for d in range(4):
        for c in itertools.combinations_with_replacement(range(3), d):
            out.append(c)
    return out

def alpha_monos():
    return [(), (0,), (1,), (2,)]

BM, AM = beta_monos(), alpha_monos()
MONOS = [(b, a) for b in BM for a in AM]

def evaluate(C, G, BF0, BFb, P2map, Kb, beta, alpha):
    """Return the 8 remainder coefficients for these parameters."""
    vec = list(BF0)
    for cf, bv in zip(beta, BFb):
        vec = [M.kadd(vec[k], M.kmul(cf, bv[k])) for k in range(len(vec))]
    B, F = M.split_BF(vec)
    Mx, rhs = M.eq_w2_system(C, G, B, F)
    s2 = M.ksolve(Mx, rhs)
    if s2 is None:
        return None
    sol = list(s2[0])
    for cf, kv in zip(alpha, Kb):
        sol = [M.kadd(sol[k], M.kmul(cf, kv[k])) for k in range(len(sol))]
    A = M.poly_from_coeffs(sol[:9], 0)
    E = M.poly_from_coeffs(sol[9:], 1)
    expr = M.kpadd(M.kpscal(M.kpmul(M.kpder(A), F), -2),
                   M.kpadd(M.kpmul(B, M.kpder(E)),
                           M.kpscal(M.kpmul(M.kpder(B), E), -1)))
    r = M.kprem(expr, C)
    return [r[i] if i < len(r) else M.kzero() for i in range(8)]

def mono_value(mono, beta, alpha):
    b, a = mono
    v = M.kone()
    for i in b:
        v = M.kmul(v, beta[i])
    for i in a:
        v = M.kmul(v, alpha[i])
    return v

def interpolate(C, G, BF0, BFb, Kb, rng, npts=None):
    npts = npts or (len(MONOS) + 25)
    rows, vals = [], []
    while len(rows) < npts:
        beta = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        alpha = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        r = evaluate(C, G, BF0, BFb, None, Kb, beta, alpha)
        if r is None:
            continue
        rows.append([mono_value(m, beta, alpha) for m in MONOS])
        vals.append(r)
    return rows, vals

def solve_coeffs(rows, vals, which):
    rhs = [v[which] for v in vals]
    res = M.ksolve(rows, rhs)
    if res is None:
        return None
    return res[0], len(res[1])

def to_singular(coeffs):
    """K element -> Singular polynomial in a."""
    def kstr(e):
        ts = [f"{e[i]}*a^{i}" if i > 1 else (f"{e[i]}*a" if i == 1 else f"{e[i]}")
              for i in range(DEG) if e[i]]
        return "(" + "+".join(ts) + ")" if ts else "0"
    terms = []
    for cf, (b, a) in zip(coeffs, MONOS):
        if M.kis0(cf):
            continue
        s = kstr(cf)
        for i in b:
            s += f"*b({i+1})"
        for i in a:
            s += f"*al({i+1})"
        terms.append(s)
    return "+".join(terms) if terms else "0"

if __name__ == "__main__":
    const = int(sys.argv[1]) if len(sys.argv) > 1 else 7766
    M.CONST = const % p
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    C, G = M.build_CG()
    BF0, BFb = M.ksolve(*M.eq_w3_matrix(C, G))
    Mx, _ = M.eq_w2_system(C, G, *M.split_BF(BF0))
    _, Kb = M.ksolve(Mx, [M.kzero()] * len(Mx))
    print(f"K: th^7 = {(-M.CONST) % p};  (B,F) dim {len(BFb)};  "
          f"(w=-2) fixed kernel dim {len(Kb)}", flush=True)
    rows, vals = interpolate(C, G, BF0, BFb, Kb, rng)
    print(f"interpolation: {len(rows)} points, {len(MONOS)} monomials",
          flush=True)
    polys = []
    for w in range(8):
        got = solve_coeffs(rows, vals, w)
        if got is None:
            print(f"  condition {w}: INTERPOLATION INCONSISTENT "
                  f"(degree bound too low)")
            sys.exit(1)
        cf, nfree = got
        polys.append(cf)
        if nfree:
            print(f"  condition {w}: interpolation underdetermined "
                  f"({nfree} free) -- add points")
            sys.exit(1)
    # verify the interpolants on fresh points
    ok = 0
    for _ in range(6):
        beta = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        alpha = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        r = evaluate(C, G, BF0, BFb, None, Kb, beta, alpha)
        pred = []
        for cf in polys:
            acc = M.kzero()
            for c, m in zip(cf, MONOS):
                if not M.kis0(c):
                    acc = M.kadd(acc, M.kmul(c, mono_value(m, beta, alpha)))
            pred.append(acc)
        ok += all(M.kis0(M.ksub(pred[i], r[i])) for i in range(8))
    print(f"interpolants verified on fresh points: {ok}/6", flush=True)
    src = [f"ring R = ({p}, a), (b(1..3), al(1..3)), dp;",
           f"minpoly = a^{DEG} + {M.CONST};", "ideal I ="]
    src.append(",\n".join("  " + to_singular(cf) for cf in polys) + ";")
    src.append('"generators: " + string(size(simplify(I,2)));')
    src.append("ideal Gb = std(I);")
    src.append('if (size(Gb) == 1 && Gb[1] == 1) '
               '{ "VERDICT: EMPTY -- this edge branch does NOT extend"; }')
    src.append('else { "VERDICT: dim = " + string(dim(Gb)); '
               'if (dim(Gb) == 0) { "vdim = " + string(vdim(Gb)); } }')
    src.append("quit;")
    open(f"_case2_final_{const}.sing", "w").write("\n".join(src))
    print(f"[wrote _case2_final_{const}.sing]")
