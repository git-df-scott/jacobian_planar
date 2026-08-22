"""Decide case (2) of GGHV Prop 4.3 on ONE branch of the edge eliminant.

The edge equation 2CG' - 3C'G = t^2 has a zero-dimensional solution scheme of
vdim 35; its eliminant factors over F_p (p = 65521) as

    (th^7 + 7766)(th^7 - 30040)(th^7 - 9260)(th^14 + 13055 th^7 - 23589),

four irreducible factors, 7+7+7+14 = 35.  Each gives a residue field K over
which C and G are explicit (shape-lemma RUR).  This script takes one factor,
runs the whole remaining chain, and reports the verdict.

Chain, in order:
    (w=-4)  2CG' - 3C'G = t^2                          [solved: gives C,G]
    (w=-3)  BG' - 3B'G + 2CF' - 2C'F = 0               [linear in (B,F)]
    (w=-2)  -3A'G + BF' - 2B'F + 2CE' - C'E = 0        [linear in (A,E)]
    (w=-1)  -2A'F + BE' - B'E + 2CD' = 0               [linear in D]
    (w= 0)  BD' = A'E

(w=-3) is homogeneous, so (B,F) = sum beta_i v_i.  (w=-2) has a matrix
independent of (B,F), so (A,E) = P2(beta) + sum alpha_j k_j with P2 quadratic
in beta.  (w=-1) is solvable for D iff C divides -2A'F + BE' - B'E (8
conditions); given that, (w=0) becomes the division-free
B(2A'F - BE' + B'E) = 2C A'E.  Both are polynomial in (beta, alpha) in a
fixed monomial basis, so we interpolate them exactly and hand the ideal to
Singular.

Interpolation points are taken in F_p rather than all of K: the monomial
VALUES are then in F_p, so one F_p RREF (numpy) replaces a Gaussian
elimination over F_{p^7}/F_{p^14} in Python.  The interpolants are then
checked against fresh FULL-K-random points, which is what actually certifies
them.
"""
import sys, random, time
import numpy as np
import trackB1_case2_extend as M
import trackB1_case2_final as FN
import _w0 as W
from _w0np import rref_mod_p

p = M.p          # default; run() re-reads M.p for other primes

BRANCHES = {
    # name: monic minimal polynomial coefficients [m_0, ..., m_{d-1}]
    "A": ("th^7 + 7766", [7766] + [0] * 6),
    "B": ("th^7 - 30040", [-30040 % p] + [0] * 6),
    "C": ("th^7 - 9260", [-9260 % p] + [0] * 6),
    "D": ("th^14 + 13055*th^7 - 23589",
          [-23589 % p] + [0] * 6 + [13055] + [0] * 6),
}


def kfmt(e):
    ts = [f"{e[i]}*th^{i}" if i > 1 else (f"{e[i]}*th" if i == 1 else f"{e[i]}")
          for i in range(M.DEG) if e[i]]
    return "+".join(ts) if ts else "0"


def sing_minpoly(coeffs):
    ts = []
    for i, c in enumerate(coeffs):
        if c % p:
            ts.append(f"{c % p}" if i == 0 else
                      (f"{c % p}*a" if i == 1 else f"{c % p}*a^{i}"))
    return f"a^{len(coeffs)}" + ("+" + "+".join(ts) if ts else "")


def iszero(P):
    return all(M.kis0(c) for c in P)


def setup():
    C, G = M.build_CG()
    edge = M.kpadd(M.kpadd(M.kpscal(M.kpmul(C, M.kpder(G)), 2),
                           M.kpscal(M.kpmul(M.kpder(C), G), -3)),
                   [M.kzero(), M.kzero(), M.ksub(M.kzero(), M.kone())])
    if not iszero(edge):
        raise RuntimeError("edge equation FAILS on this branch -- RUR wrong")
    BF0, BFb = M.ksolve(*M.eq_w3_matrix(C, G))
    Mx, _ = M.eq_w2_system(C, G, *M.split_BF(BF0))
    _, Kb = M.ksolve(Mx, [M.kzero()] * len(Mx))
    return C, G, BF0, BFb, Kb


def interp(name, monos, resid, C, G, BF0, BFb, Kb, rng, extra=30, verify=8):
    """Interpolate `resid` in the basis `monos` using F_p sample points."""
    DEG = M.DEG
    rows, vals = [], []
    while len(rows) < len(monos) + extra:
        bi = [rng.randrange(p) for _ in range(3)]
        ai = [rng.randrange(p) for _ in range(3)]
        beta = [[v] + [0] * (DEG - 1) for v in bi]
        alpha = [[v] + [0] * (DEG - 1) for v in ai]
        r = resid(C, G, BF0, BFb, Kb, beta, alpha)
        if r is None:
            continue
        row = []
        for b, a in monos:
            v = 1
            for i in b:
                v = v * bi[i] % p
            for i in a:
                v = v * ai[i] % p
            row.append(v)
        rows.append(row)
        vals.append(r)
    NEQ = max(len(v) for v in vals)
    A = np.array(rows, dtype=np.int64)
    B = np.zeros((len(rows), NEQ * DEG), dtype=np.int64)
    for i, v in enumerate(vals):
        for w in range(NEQ):
            e = v[w] if w < len(v) else M.kzero()
            for l in range(DEG):
                B[i, w * DEG + l] = e[l] % p
    sols, rank, cons = rref_mod_p(A, B, M.p)
    if rank < len(monos):
        raise RuntimeError(f"{name}: underdetermined (rank {rank})")
    if not all(cons):
        raise RuntimeError(f"{name}: inconsistent -- degree bound too low")
    polys = [[[int(sols[mi, w * DEG + l]) for l in range(DEG)]
              for mi in range(len(monos))] for w in range(NEQ)]
    ok = 0
    for _ in range(verify):
        beta = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        alpha = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        r = resid(C, G, BF0, BFb, Kb, beta, alpha)
        if r is None:
            continue
        good = True
        for w in range(NEQ):
            acc = M.kzero()
            for c, m in zip(polys[w], monos):
                if not M.kis0(c):
                    acc = M.kadd(acc, M.kmul(c, W.monval(m, beta, alpha)))
            if not M.kis0(M.ksub(acc, r[w] if w < len(r) else M.kzero())):
                good = False
                break
        ok += good
    if ok != verify:
        raise RuntimeError(f"{name}: K-random verification {ok}/{verify}")
    print(f"    {name}: {NEQ} conditions, {len(monos)} monomials, "
          f"K-verify {ok}/{verify}")
    return polys


def to_sing(polys, monos):
    out = []
    for cf in polys:
        terms = []
        for c, (b, a) in zip(cf, monos):
            if M.kis0(c):
                continue
            ts = [(f"{c[i]}*a^{i}" if i > 1 else
                   (f"{c[i]}*a" if i == 1 else f"{c[i]}"))
                  for i in range(M.DEG) if c[i]]
            s = "(" + "+".join(ts) + ")"
            for i in b:
                s += f"*b({i+1})"
            for i in a:
                s += f"*al({i+1})"
            terms.append(s)
        if terms:
            out.append("+".join(terms))
    return out


def w1_resid(C, G, BF0, BFb, Kb, beta, alpha):
    return FN.evaluate(C, G, BF0, BFb, None, Kb, beta, alpha)


def run(key, seed=17, table=None):
    global p
    label, mod = (table or BRANCHES)[key]
    M.set_modulus(mod)
    p = M.p          # rebind for interp()/sing_minpoly()/the ring header
    rng = random.Random(seed)
    t0 = time.time()
    print(f"\n=== branch {key}:  K = F_p[th]/({label}),  "
          f"[K:F_p] = {M.DEG} ===")
    C, G, BF0, BFb, Kb = setup()
    print(f"    edge equation holds; (w=-3) dim {len(BFb)}, "
          f"(w=-2) kernel dim {len(Kb)}")
    w1 = interp("(w=-1)", FN.MONOS, w1_resid, C, G, BF0, BFb, Kb, rng)
    w0 = interp("(w= 0)", W.MON, W.w0_resid, C, G, BF0, BFb, Kb, rng)
    g1, g0 = to_sing(w1, FN.MONOS), to_sing(w0, W.MON)
    print(f"    nonzero generators: (w=-1) {len(g1)}, (w=0) {len(g0)} "
          f"[{time.time()-t0:.0f}s]")
    L = [f"ring R = ({p}, a), (b(1..3), al(1..3)), dp;",
         f"minpoly = {sing_minpoly(mod)};",
         'LIB "primdec.lib";',
         "ideal I = " + ",\n".join(g1 + g0) + ";",
         "ideal Gb = std(I);",
         'if (size(Gb)==1 && Gb[1]==1) { "VERDICT: EMPTY"; }',
         'else { "VERDICT: dim = " + string(dim(Gb));',
         '  list pd = minAssGTZ(I); "components: " + string(size(pd));',
         '  int i; for (i=1;i<=size(pd);i++) {',
         '    "  comp "+string(i)+": dim "+string(dim(std(pd[i]))); pd[i]; } }',
         "quit;"]
    fn = f"_c2_branch_{M.p}_{key}.sing"
    open(fn, "w").write("\n".join(L))
    print(f"    [wrote {fn}]")
    return fn


if __name__ == "__main__":
    for key in (sys.argv[1:] or ["A", "B", "C", "D"]):
        try:
            run(key)
        except Exception as ex:
            print(f"    branch {key} FAILED: {type(ex).__name__}: {ex}")
