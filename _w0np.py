"""(w=0) for case (2), interpolated with F_p-rational sample points.

Same target as _w0.py / _w0fast.py -- the division-free form

    B (2 A'F - B E' + B'E)  =  2 C A' E

as a polynomial identity in (beta, alpha) in K^3 x K^3, degree <= 4 in beta
and <= 2 in alpha, i.e. a fixed 35 x 10 = 350 monomial basis.

The speedup: sample beta_i, alpha_j in F_p (not all of K).  The monomial
VALUES are then in F_p, so the interpolation matrix is an F_p matrix even
though the unknown coefficients still live in K.  Writing each unknown
coefficient in the theta-basis decouples the K-system into DEG independent
F_p systems sharing one matrix -- one numpy RREF instead of a 370x350
Gaussian elimination over F_{p^7} in pure Python.

This is legitimate: individual monomial degrees are <= 4 << p, so a
polynomial of this shape that vanishes on all of F_p^6 is the zero
polynomial (Schwartz-Zippel / combinatorial Nullstellensatz).  Verified
directly below on fresh points with FULL K-random coordinates, which is the
real check that the F_p-point interpolant is the right polynomial over K.
"""
import sys, random, time
import numpy as np
import trackB1_case2_extend as M
import _w0 as W

p, DEG = M.p, M.DEG
MON = W.MON


def kconst(v):
    """F_p scalar -> K element."""
    e = [0] * DEG
    e[0] = v % p
    return e


def rref_mod_p(A, B):
    """RREF of [A|B] over F_p.  Returns (solutions, rank, consistent-flags).

    A: (m,n) int64, B: (m,k) int64.  Solution j is the unique preimage when
    rank == n; a row that is zero across A but nonzero in column j marks that
    right-hand side inconsistent.
    """
    m, n = A.shape
    k = B.shape[1]
    Aug = np.concatenate([A % p, B % p], axis=1).astype(np.int64)
    piv = []
    r = 0
    for c in range(n):
        nz = np.nonzero(Aug[r:, c])[0]
        if nz.size == 0:
            continue
        pr = r + int(nz[0])
        if pr != r:
            Aug[[r, pr]] = Aug[[pr, r]]
        inv = pow(int(Aug[r, c]), p - 2, p)
        Aug[r] = (Aug[r] * inv) % p
        col = Aug[:, c].copy()
        col[r] = 0
        rows = np.nonzero(col)[0]
        if rows.size:
            Aug[rows] = (Aug[rows] - np.outer(col[rows], Aug[r])) % p
        piv.append((c, r))
        r += 1
        if r == m:
            break
    rank = len(piv)
    zero_rows = np.nonzero(~Aug[:, :n].any(axis=1))[0]
    consistent = [bool(not Aug[zero_rows, n + j].any()) for j in range(k)]
    sols = np.zeros((n, k), dtype=np.int64)
    for c, rr in piv:
        sols[c] = Aug[rr, n:]
    return sols, rank, consistent


def run(const, seed, extra=30):
    M.CONST = const % p
    rng = random.Random(seed)
    t0 = time.time()
    C, G, BF0, BFb, Kb = W.setup(const)

    need = len(MON) + extra
    rows, vals = [], []
    while len(rows) < need:
        bi = [rng.randrange(p) for _ in range(3)]
        ai = [rng.randrange(p) for _ in range(3)]
        beta = [kconst(v) for v in bi]
        alpha = [kconst(v) for v in ai]
        r = W.w0_resid(C, G, BF0, BFb, Kb, beta, alpha)
        if r is None:
            continue
        # monomial values are plain F_p products of the sampled scalars
        row = []
        for b, a in MON:
            v = 1
            for i in b:
                v = v * bi[i] % p
            for i in a:
                v = v * ai[i] % p
            row.append(v)
        rows.append(row)
        vals.append(r)
    NEQ = max(len(v) for v in vals)
    print(f"evaluations: {len(rows)} F_p points, {len(MON)} monomials, "
          f"{NEQ} conditions [{time.time()-t0:.0f}s]", flush=True)

    A = np.array(rows, dtype=np.int64)
    # right-hand sides: condition w, theta-component l
    B = np.zeros((len(rows), NEQ * DEG), dtype=np.int64)
    for i, v in enumerate(vals):
        for w in range(NEQ):
            e = v[w] if w < len(v) else M.kzero()
            for l in range(DEG):
                B[i, w * DEG + l] = e[l] % p
    sols, rank, cons = rref_mod_p(A, B)
    print(f"one F_p elimination: rank {rank}/{len(MON)} "
          f"[{time.time()-t0:.0f}s]", flush=True)
    if rank < len(MON):
        print("  UNDERDETERMINED -- more points needed")
        return None
    if not all(cons):
        print("  INCONSISTENT -- degree bound too low")
        return None

    polys = []
    for w in range(NEQ):
        cf = []
        for mi in range(len(MON)):
            cf.append([int(sols[mi, w * DEG + l]) for l in range(DEG)])
        polys.append(cf)

    # verify with FULL K-random coordinates -- the real test that the
    # F_p-sampled interpolant is correct as a polynomial over K
    ok = 0
    trials = 8
    for _ in range(trials):
        beta = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        alpha = [[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        r = W.w0_resid(C, G, BF0, BFb, Kb, beta, alpha)
        if r is None:
            continue
        good = True
        for w in range(NEQ):
            acc = M.kzero()
            for c, m in zip(polys[w], MON):
                if not M.kis0(c):
                    acc = M.kadd(acc, M.kmul(c, W.monval(m, beta, alpha)))
            tgt = r[w] if w < len(r) else M.kzero()
            if not M.kis0(M.ksub(acc, tgt)):
                good = False
                break
        ok += good
    print(f"K-random verification: {ok}/{trials} [{time.time()-t0:.0f}s]",
          flush=True)
    if ok != trials:
        print("  VERIFICATION FAILED -- F_p sampling did not determine the "
              "polynomial; widen the monomial basis")
        return None

    def kstr(e):
        ts = [(f"{e[i]}*a^{i}" if i > 1 else (f"{e[i]}*a" if i == 1
                                             else f"{e[i]}"))
              for i in range(DEG) if e[i]]
        return "(" + "+".join(ts) + ")" if ts else "0"

    out = []
    for cf in polys:
        terms = []
        for c, (b, a) in zip(cf, MON):
            if M.kis0(c):
                continue
            s = kstr(c)
            for i in b:
                s += f"*b({i+1})"
            for i in a:
                s += f"*al({i+1})"
            terms.append(s)
        out.append("+".join(terms) if terms else "0")
    nz = [o for o in out if o != "0"]
    open(f"_w0_{const}.txt", "w").write(",\n".join(nz))
    print(f"[wrote _w0_{const}.txt : {len(nz)} nonzero of {NEQ} conditions "
          f"[{time.time()-t0:.0f}s]]", flush=True)
    return nz


if __name__ == "__main__":
    const = int(sys.argv[1]) if len(sys.argv) > 1 else 7766
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 11
    run(const, seed)
