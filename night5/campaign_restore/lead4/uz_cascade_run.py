#!/usr/bin/env python3
"""Full explicit cascade solve, one GF(p)-rational q at a time.

For a fixed q:
   p = lam*v1 + mu*v2                (kernel of the 7 linear (n,3) equations)
   M f = -Q(p)                       (the 7 (n,2) equations; M depends only on
                                      q, Q is quadratic in p -- the weighted
                                      grading forbids f*p mixing)
   f = f_part(lam,mu) + nu*k         (k spans ker M)
then the (n,1) and (n,0) obstructions become polynomials in (lam,mu,nu),
solved directly.  a_10_5 = f5 is then read off every solution.
"""
import itertools
import sys

from uz_qsolve import qsolutions
from uz_eliminate import run
from uz_system import PVARS, PIDX
from uz_cascade import nullspace, solve_affine, partial

PV = ["p%d" % a for a in range(1, 9)]
FV = ["f%d" % a for a in range(1, 9)]


# ---- tiny polynomial ring GF(mod)[lam,mu,nu] -------------------------------
def tadd(A, B, mod):
    C = dict(A)
    for m, c in B.items():
        v = (C.get(m, 0) + c) % mod
        if v:
            C[m] = v
        elif m in C:
            del C[m]
    return C


def tmul(A, B, mod):
    C = {}
    for m1, c1 in A.items():
        for m2, c2 in B.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            v = (C.get(m, 0) + c1 * c2) % mod
            if v:
                C[m] = v
            elif m in C:
                del C[m]
    return C


def tscal(A, c, mod):
    c %= mod
    if c == 0:
        return {}
    return {m: v * c % mod for m, v in A.items()}


def tpow(A, e, mod, nv=None):
    R = {(0,) * (nv if nv else len(next(iter(A)))): 1}
    for _ in range(e):
        R = tmul(R, A, mod)
    return R


def analyse(path):
    MOD, qsols = qsolutions(path, verbose=False)
    obs, _ = run(mod=MOD, fixed={}, verbose=False)
    obs = dict(obs)
    E3 = [obs[(n, 3)] for n in range(13, 20)]
    E2 = [obs[(n, 2)] for n in range(13, 20)]
    E1 = [obs[(n, 1)] for n in range(13, 20)]
    E0 = [obs[(n, 0)] for n in range(2, 20)]
    results = []
    for si, q in enumerate(qsols):
        val = {v: 0 for v in PVARS}
        val.update(q)
        # ---- p layer: 7 linear homogeneous equations
        A = []
        for e in E3:
            d = partial(e, val, MOD, PV)
            row = [0] * 8
            for mono, c in d.items():
                row[list(mono).index(1)] = c
            A.append(row)
        ker = nullspace(A, MOD)
        # ---- f layer: M f + Q(p) = 0
        Mrows, Qrows = [], []
        for e in E2:
            d = partial(e, val, MOD, FV + PV)
            row = [0] * 8
            quad = {}
            for mono, c in d.items():
                fpart = mono[:8]
                ppart = mono[8:]
                if sum(fpart) == 1 and sum(ppart) == 0:
                    row[list(fpart).index(1)] = c
                elif sum(fpart) == 0 and sum(ppart) == 2:
                    quad[ppart] = c
                else:
                    raise RuntimeError(f"unexpected (n,2) monomial {mono}")
            Mrows.append(row)
            Qrows.append(quad)
        # p = sum_j x_j * ker[j]  (x = lam, mu, ...)
        nk = len(ker)
        names = ["lam", "mu", "nu"][:nk] + ["nu"]
        # Q as a quadratic form in the kernel coordinates
        # Qvec[(i,j)] = 7-vector coefficient of x_i x_j
        Qvec = {}
        for i in range(nk):
            for j in range(i, nk):
                vec = []
                for quad in Qrows:
                    tot = 0
                    for ppart, c in quad.items():
                        idx = [a for a in range(8) for _ in range(ppart[a])]
                        assert len(idx) == 2
                        a, b = idx
                        if i == j:
                            tot += c * ker[i][a] * ker[i][b]
                        else:
                            tot += c * (ker[i][a] * ker[j][b]
                                        + ker[j][a] * ker[i][b])
                    vec.append(tot % MOD)
                Qvec[(i, j)] = vec
        sols = {}
        rankM = len(nullspace([r[:] for r in zip(*Mrows)], MOD))  # placeholder
        kerM = nullspace(Mrows, MOD)
        parts = {}
        bad = False
        for key, vec in Qvec.items():
            r = solve_affine(Mrows, [(-v) % MOD for v in vec], MOD)
            if r is None:
                bad = True
                break
            parts[key] = r[0]
        results.append(dict(mod=MOD, q=q, ker=ker, kerM=kerM, parts=parts,
                            bad=bad, Mrows=Mrows, E1=E1, E0=E0, val=val,
                            nk=nk))
    return results


def build_param_polys(res):
    """Return the (n,1) and (n,0) obstructions as polynomials in
    lam, mu (kernel coords of p) and nu (coefficient of ker M)."""
    MOD = res["mod"]
    nk = res["nk"]
    ker = res["ker"]
    kerM = res["kerM"]
    parts = res["parts"]
    nf = len(kerM)
    NV = nk + nf
    def gen(i):
        e = [0] * NV
        e[i] = 1
        return {tuple(e): 1}
    X = [gen(i) for i in range(nk)]
    NUS = [gen(nk + i) for i in range(nf)]
    # p_a
    pexpr = []
    for a in range(8):
        e = {}
        for i in range(nk):
            e = tadd(e, tscal(X[i], ker[i][a], MOD), MOD)
        pexpr.append(e)
    # f_a
    fexpr = []
    for a in range(8):
        e = {}
        for i in range(nf):
            e = tadd(e, tscal(NUS[i], kerM[i][a], MOD), MOD)
        for (i, j), vec in parts.items():
            term = tmul(X[i], X[j], MOD)
            e = tadd(e, tscal(term, vec[a], MOD), MOD)
        fexpr.append(e)
    return pexpr, fexpr, NV


def subst(poly, res, pexpr, fexpr, NV):
    MOD = res["mod"]
    val = res["val"]
    out = {}
    for m, c in poly.items():
        term = {(0,) * NV: c % MOD}
        for i, e in enumerate(m):
            if not e:
                continue
            name = PVARS[i]
            if name[0] == "q":
                term = tscal(term, pow(val[name], e, MOD), MOD)
            elif name[0] == "p":
                term = tmul(term, tpow(pexpr[int(name[1:]) - 1], e, MOD, NV),
                            MOD)
            else:
                term = tmul(term, tpow(fexpr[int(name[1:]) - 1], e, MOD, NV),
                            MOD)
        out = tadd(out, term, MOD)
    return out


VN = ["lam", "mu", "nu1", "nu2", "nu3", "nu4"]


def tstr(P):
    if not P:
        return "0"
    out = []
    for m, c in sorted(P.items()):
        f = [str(c)]
        for i, e in enumerate(m):
            if e:
                f.append(VN[i] + ("^%d" % e if e > 1 else ""))
        out.append("*".join(f))
    return "+".join(out)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        for res in analyse(path):
            MOD = res["mod"]
            print(f"--- mod {MOD}  q = {res['q']}")
            print(f"    p-kernel dim {res['nk']}, ker(M) dim "
                  f"{len(res['kerM'])}, f-system solvable: {not res['bad']}")
            if res["bad"]:
                print("    (n,2) layer inconsistent for this q -> no solution")
                continue
            pexpr, fexpr, NV = build_param_polys(res)
            print("    f5 as a polynomial in (lam,mu,nu):",
                  tstr(fexpr[4]))
            polys = []
            for e in res["E1"] + res["E0"]:
                P = subst(e, res, pexpr, fexpr, NV)
                if P:
                    polys.append(P)
            print(f"    {len(polys)} nonzero equations in (lam,mu,nu); "
                  f"degrees {sorted({sum(m) for P in polys for m in P})}")
            import pickle
            pickle.dump((MOD, polys, fexpr, pexpr, res["q"], NV),
                        open(f"cascade_{MOD}_{list(res['q'].values())[0]}.pkl",
                             "wb"))
