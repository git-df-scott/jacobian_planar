"""Direct verification of the case-(2) solution point found by the elimination.

The Singular verdict was: (w=-1) and (w=0) together cut out exactly
    b(2) = b(3) = al(2) = al(3) = 0,
so (B,F) = beta_1 * BFb[0] and (A,E) = P2 + alpha_1 * Kb[0].

This script does NOT use the interpolants.  It builds A..G from scratch at
that point and checks all five weight equations, the polynomial degrees, the
Newton-polygon vertex coefficients, and finally computes [P,Q] directly from
the assembled two-variable polynomials.

  P = A(t) + B(t)/y + C(t)/y^2,   Q = D(t) + E(t)/y + F(t)/y^2 + G(t)/y^3,
  t = x y^2,  so  A_i -> (i,2i), B_i -> (i,2i-1), C_i -> (i,2i-2),
  D_i -> (i,2i), E_i -> (i,2i-1), F_i -> (i,2i-2), G_i -> (i,2i-3).
"""
import sys
import trackB1_case2_extend as M
import _w0 as W

p = M.p


def kfmt(e):
    # M.DEG changes with the branch, so read it at call time
    ts = [f"{e[i]}*th^{i}" if i > 1 else (f"{e[i]}*th" if i == 1 else f"{e[i]}")
          for i in range(M.DEG) if e[i]]
    return "+".join(ts) if ts else "0"


def kpdeg(P):
    d = -1
    for i, c in enumerate(P):
        if not M.kis0(c):
            d = i
    return d


def kpsub(A, B):
    n = max(len(A), len(B))
    return [M.ksub(A[i] if i < len(A) else M.kzero(),
                   B[i] if i < len(B) else M.kzero()) for i in range(n)]


def iszero(P):
    return all(M.kis0(c) for c in P)


# ---------------------------------------------------------------- 2-var
def bracket(P, Q):
    """P, Q are dicts (i,j) -> K.  Returns [P,Q] = P_x Q_y - P_y Q_x."""
    out = {}
    for (i1, j1), a in P.items():
        if M.kis0(a):
            continue
        for (i2, j2), b in Q.items():
            if M.kis0(b):
                continue
            c = (i1 * j2 - j1 * i2) % p
            if c == 0:
                continue
            k = (i1 + i2 - 1, j1 + j2 - 1)
            out[k] = M.kadd(out.get(k, M.kzero()), M.kscal(M.kmul(a, b), c))
    return {k: v for k, v in out.items() if not M.kis0(v)}


def assemble(pieces):
    """pieces: list of (poly, shift) with monomial (i, 2i - shift)."""
    out = {}
    for poly, sh in pieces:
        for i, c in enumerate(poly):
            if M.kis0(c):
                continue
            out[(i, 2 * i - sh)] = M.kadd(out.get((i, 2 * i - sh), M.kzero()), c)
    return out


def main(branch="A", beta1_val=1, alpha1_val=1):
    import _c2_branch as BR
    label, mod = BR.BRANCHES[branch]
    M.set_modulus(mod)
    print(f"### branch {branch}: K = F_p[th]/({label})")
    C, G = M.build_CG()

    # ---- (w=-4): the edge equation, already solved
    e4 = kpsub(M.kpadd(M.kpscal(M.kpmul(C, M.kpder(G)), 2),
                       M.kpscal(M.kpmul(M.kpder(C), G), -3)),
               [M.kzero(), M.kzero(), M.kone()])
    print(f"(w=-4)  2CG' - 3C'G = t^2 : {'OK' if iszero(e4) else 'FAIL'}")

    # ---- (w=-3): (B,F) = beta_1 * BFb[0]
    BF0, BFb = M.ksolve(*M.eq_w3_matrix(C, G))
    print(f"        (w=-3) particular is zero: {all(M.kis0(v) for v in BF0)},"
          f"  kernel dim {len(BFb)}")
    b1 = M.kzero(); b1[0] = beta1_val % p
    vec = [M.kmul(b1, v) for v in BFb[0]]
    B, F = M.split_BF(vec)
    e3 = M.kpadd(M.kpadd(M.kpmul(B, M.kpder(G)),
                         M.kpscal(M.kpmul(M.kpder(B), G), -3)),
                 M.kpadd(M.kpscal(M.kpmul(C, M.kpder(F)), 2),
                         M.kpscal(M.kpmul(M.kpder(C), F), -2)))
    print(f"(w=-3)  BG' - 3B'G + 2CF' - 2C'F = 0 : "
          f"{'OK' if iszero(e3) else 'FAIL'}")

    # ---- (w=-2): (A,E) = particular + alpha_1 * Kb[0]
    Mx, rhs = M.eq_w2_system(C, G, B, F)
    s2 = M.ksolve(Mx, rhs)
    if s2 is None:
        print("(w=-2)  INCONSISTENT"); return
    sol = list(s2[0])
    Kb = M.ksolve(Mx, [M.kzero()] * len(Mx))[1]
    a1 = M.kzero(); a1[0] = alpha1_val % p
    sol = [M.kadd(sol[k], M.kmul(a1, Kb[0][k])) for k in range(len(sol))]
    A = M.poly_from_coeffs(sol[:9], 0)
    E = M.poly_from_coeffs(sol[9:], 1)
    e2 = M.kpadd(M.kpscal(M.kpmul(M.kpder(A), G), -3),
                 M.kpadd(M.kpadd(M.kpmul(B, M.kpder(F)),
                                 M.kpscal(M.kpmul(M.kpder(B), F), -2)),
                         M.kpadd(M.kpscal(M.kpmul(C, M.kpder(E)), 2),
                                 M.kpscal(M.kpmul(M.kpder(C), E), -1))))
    print(f"(w=-2)  -3A'G + BF' - 2B'F + 2CE' - C'E = 0 : "
          f"{'OK' if iszero(e2) else 'FAIL'}   [(w=-2) kernel dim {len(Kb)}]")
    print(f"        Kb[0] = pure A-constant? "
          f"{all(M.kis0(c) for i,c in enumerate(Kb[0]) if i != 0)}")

    # ---- (w=-1): solve for D
    Mx1, rhs1 = M.eq_w1_system(C, A, B, E, F)
    s1 = M.ksolve(Mx1, rhs1)
    if s1 is None:
        print("(w=-1)  INCONSISTENT -- no D exists"); return
    D = M.poly_from_coeffs(s1[0], 0)
    e1 = M.kpadd(M.kpscal(M.kpmul(M.kpder(A), F), -2),
                 M.kpadd(M.kpadd(M.kpmul(B, M.kpder(E)),
                                 M.kpscal(M.kpmul(M.kpder(B), E), -1)),
                         M.kpscal(M.kpmul(C, M.kpder(D)), 2)))
    print(f"(w=-1)  -2A'F + BE' - B'E + 2CD' = 0 : "
          f"{'OK' if iszero(e1) else 'FAIL'}   [D freedom dim {len(s1[1])}]")

    # ---- (w=0)
    e0 = kpsub(M.kpmul(B, M.kpder(D)), M.kpmul(M.kpder(A), E))
    print(f"(w= 0)  BD' = A'E : {'OK' if iszero(e0) else 'FAIL'}")

    # ---- degrees and vertex coefficients
    print()
    for nm, poly, lo, hi in [("A", A, 0, 8), ("B", B, 1, 8), ("C", C, 1, 8),
                             ("D", D, 0, 12), ("E", E, 1, 12),
                             ("F", F, 1, 12), ("G", G, 2, 12)]:
        d = kpdeg(poly)
        low = next((i for i, c in enumerate(poly) if not M.kis0(c)), None)
        ok = (d <= hi) and (low is None or low >= lo)
        print(f"  {nm}: deg {d:3d} (allowed {lo}..{hi}), lowest term "
              f"{low}  {'ok' if ok else 'SUPPORT VIOLATION'}")

    print()
    print("  Newton-polygon vertex coefficients of P:")
    print(f"    (0,0)  a_0  = {kfmt(A[0])}")
    print(f"    (1,0)  c_1  = {kfmt(C[1])}")
    print(f"    (8,16) a_8  = {kfmt(A[8]) if len(A) > 8 else '0'}")
    print(f"    (8,14) c_8  = {kfmt(C[8])}")
    print("  Newton-polygon vertex coefficients of Q:")
    print(f"    (0,0)  d_0  = {kfmt(D[0])}")
    print(f"    (2,1)  g_2  = {kfmt(G[2])}")
    print(f"    (12,24) d_12 = {kfmt(D[12]) if len(D) > 12 else '0'}")
    print(f"    (12,21) g_12 = {kfmt(G[12])}")

    # ---- the real test: assemble and bracket directly
    print()
    Pd = assemble([(A, 0), (B, 1), (C, 2)])
    Qd = assemble([(D, 0), (E, 1), (F, 2), (G, 3)])
    neg = [k for k in list(Pd) + list(Qd) if k[0] < 0 or k[1] < 0]
    print(f"  negative exponents: {neg if neg else 'none'}")
    br = bracket(Pd, Qd)
    tgt = {(2, 0): M.kone()}
    diff = {k: v for k, v in br.items()
            if not M.kis0(M.ksub(v, tgt.get(k, M.kzero())))}
    for k, v in tgt.items():
        if k not in br:
            diff[k] = v
    print(f"  [P,Q] has {len(br)} terms; "
          f"[P,Q] - x^2 has {len(diff)} nonzero terms")
    if diff:
        for k in sorted(diff)[:8]:
            print(f"     {k}: {kfmt(diff[k])}")
    print()
    if not diff:
        print("  *** [P,Q] = x^2 EXACTLY over K ***")
    else:
        print("  [P,Q] != x^2")
    return dict(A=A, B=B, C=C, D=D, E=E, F=F, G=G, P=Pd, Q=Qd)


if __name__ == "__main__":
    keys = sys.argv[1:] or ["A", "B", "C", "D"]
    for k in keys:
        for (b1, a1) in [(1, 1), (3, 0), (7, 12345)]:
            print(f"\n--- beta_1 = {b1}, alpha_1 = {a1} ---")
            main(k, b1, a1)
